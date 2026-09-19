# P13-white-label-02 — P13 · White Label (2 of 2)

**10 screens · 26 operations · 35 schemas · 8 permissions**

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
  `GUEST_MANAGE, GUEST_VIEW, LEDGER_POST, MARKETING_MANAGE, ROLE_MANAGE, TENANT_CONFIGURE, TENANT_PUBLISH, USER_MANAGE`. A control nobody can use must say so,
  not sit enabled and fail.
- **2 of these operations work offline**: getTenantAppStatus, listRoles
  — and the rest do not. A surface that looks the same online and off is lying.
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
| `CMS-014` | Publishing Workflow | statusTracker | 3 | 0 | — |
| `CMS-015` | Version History | listDetail | 3 | 0 | — |
| `CMS-016` | Site Settings | statusTracker | 1 | 0 | — |
| `CMS-017` | Domain & Certificate | listDetail | 4 | 0 | — |
| `CMS-018` | Consent & Legal | listDetail | 11 | 1 | — |
| `CMS-019` | User Access | listDetail | 2 | 0 | — |
| `CMS-020` | Change Log | listDetail | 1 | 0 | — |

## Thin screens in this batch

**CMS-016 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

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
     "carries": [
      "tenantId"
     ],
     "provenance": "derived — CMS-001 declares entryState.params tenantId, so an edge into it must carry them"
    },
    {
     "to": "CMS-002",
     "trigger": "Brand Kit",
     "carries": [
      "uploadId"
     ],
     "provenance": "derived — CMS-002 declares entryState.params uploadId, so an edge into it must carry them"
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
     "provenance": "derived — CMS-003 declares entryState.params bannerId, pageId, policyKind, version, so an edge into it must carry them"
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
       "label": "Save changes",
       "operation": "setSeoMetadata",
       "provenance": "contract marketing-crm.yaml PUT /seo-metadata"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "carried",
     "components": [
      {
       "kind": "detailPanel",
       "notes": "Structure from the wireframe board. Components not yet enumerated.",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "Detail loads",
   "error": "Could not load",
   "emptyFirstRun": "Not found — it may have been deleted or moved out of scope",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
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
     "carries": [
      "tenantId"
     ],
     "provenance": "derived — CMS-001 declares entryState.params tenantId, so an edge into it must carry them"
    },
    {
     "to": "CMS-002",
     "trigger": "Brand Kit",
     "carries": [
      "uploadId"
     ],
     "provenance": "derived — CMS-002 declares entryState.params uploadId, so an edge into it must carry them"
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
     "provenance": "derived — CMS-003 declares entryState.params bannerId, pageId, policyKind, version, so an edge into it must carry them"
    }
   ]
  },
  "notes": "Definition derived from the wireframe board on 14 August. Components, states and operations still to be written. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual.",
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the screen declares only writes (`setLanguages`) and no read of a population — it is settings, not a list",
  "purpose": "Fill in what every language is missing.",
  "gaps": [
   {
    "operation": "setLanguages",
    "why": "**`setLanguages` declares no request body shape**, so nothing says what this editor edits. The fields cannot be derived and the screen needs the contract before it needs a designer.",
    "source": "contract white-label.yaml PUT /tenant-config/languages"
   }
  ],
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Save changes",
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
       "kind": "detailPanel",
       "notes": "Structure from the wireframe board. Components not yet enumerated.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "setLanguages",
       "label": "Save languages",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "setLanguages",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The saved translations.",
   "error": "Could not load. Names which read failed and leaves the translations untouched.",
   "emptyFirstRun": "No translations configured. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
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
     "carries": [
      "tenantId"
     ],
     "provenance": "derived — CMS-001 declares entryState.params tenantId, so an edge into it must carry them"
    },
    {
     "to": "CMS-002",
     "trigger": "Brand Kit",
     "carries": [
      "uploadId"
     ],
     "provenance": "derived — CMS-002 declares entryState.params uploadId, so an edge into it must carry them"
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
     "provenance": "derived — CMS-003 declares entryState.params bannerId, pageId, policyKind, version, so an edge into it must carry them"
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
       "label": "The selected rtl preview",
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
       "label": "Validate",
       "operation": "validateTenantConfig",
       "provenance": "contract white-label.yaml POST /tenant-config/validate"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "carried",
     "components": [
      {
       "kind": "detailPanel",
       "notes": "Structure from the wireframe board. Components not yet enumerated.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "validateTenantConfig",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The rtl preview list.",
   "error": "Could not load. Names which read failed and leaves the rtl preview untouched.",
   "emptyFirstRun": "No rtl preview yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the rtl preview are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
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
    "CMS-015"
   ],
   "inferred": true,
   "fromFlows": true,
   "transitions": [
    {
     "to": "CMS-015",
     "trigger": "Rolls back when something is wrong",
     "provenance": "flow F22 step 5→6"
    },
    {
     "to": "CMS-001",
     "trigger": "Tenant Workspace",
     "carries": [
      "tenantId"
     ],
     "provenance": "derived — CMS-001 declares entryState.params tenantId, so an edge into it must carry them"
    },
    {
     "to": "CMS-002",
     "trigger": "Brand Kit",
     "carries": [
      "uploadId"
     ],
     "provenance": "derived — CMS-002 declares entryState.params uploadId, so an edge into it must carry them"
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
     "provenance": "derived — CMS-003 declares entryState.params bannerId, pageId, policyKind, version, so an edge into it must carry them"
    }
   ]
  },
  "notes": "Definition derived from the wireframe board on 14 August. Components, states and operations still to be written. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual.",
  "density": "compact",
  "pattern": "statusTracker",
  "patternReason": "`getTenantAppStatus` reads one record and nothing reads a population — the screen is about that one thing",
  "purpose": "Move a change from draft to live, with someone accountable.",
  "layout": {
   "template": "detail",
   "regions": [
    {
     "name": "contentBody",
     "slot": "record",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected publishing workflow",
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
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Publish",
       "operation": "publishTenantConfig",
       "provenance": "contract white-label.yaml POST /tenant-config/publish"
      },
      {
       "kind": "secondaryButton",
       "label": "Validate",
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
    },
    {
     "name": "contentBody",
     "slot": "carried",
     "components": [
      {
       "kind": "detailPanel",
       "notes": "Structure from the wireframe board. Components not yet enumerated.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "publishTenantConfig",
       "label": "Publish tenant config",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "publishTenantConfig",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "publishGate",
       "impliedBy": "publishTenantConfig",
       "notes": "Declares `publishTenantConfig`. **The gate names what the publish will affect before it happens** — a disabled Publish with no reason is the state operators escalate.\n",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The publishing workflow list.",
   "error": "Could not load. Names which read failed and leaves the publishing workflow untouched.",
   "emptyFirstRun": "No publishing workflow yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the publishing workflow are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
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
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P13 Venue CMS.dc.html#cms-014"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 3 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
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
     "carries": [
      "tenantId"
     ],
     "provenance": "derived — CMS-001 declares entryState.params tenantId, so an edge into it must carry them"
    },
    {
     "to": "CMS-002",
     "trigger": "Brand Kit",
     "carries": [
      "uploadId"
     ],
     "provenance": "derived — CMS-002 declares entryState.params uploadId, so an edge into it must carry them"
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
     "provenance": "derived — CMS-003 declares entryState.params bannerId, pageId, policyKind, version, so an edge into it must carry them"
    }
   ]
  },
  "notes": "Definition derived from the wireframe board on 14 August. Components, states and operations still to be written. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual.",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listConfigVersions` reads a population and nothing reads one of them; the detail is the row until a `get` exists",
  "purpose": "See what changed and go back if it was wrong.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every version history",
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
       "label": "The selected version history",
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
       "label": "Diff",
       "operation": "diffConfigVersion",
       "provenance": "contract white-label.yaml GET /tenant-config/versions/{version}/diff"
      },
      {
       "kind": "secondaryButton",
       "label": "Restore",
       "operation": "restoreConfigVersion",
       "provenance": "contract white-label.yaml POST /tenant-config/versions/{version}/restore"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "carried",
     "components": [
      {
       "kind": "detailPanel",
       "notes": "Structure from the wireframe board. Components not yet enumerated.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "dataTable",
       "derived": true,
       "impliedBy": "listConfigVersions",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "restoreConfigVersion",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The version history list.",
   "error": "Could not load. Names which read failed and leaves the version history untouched.",
   "emptyFirstRun": "No version history yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the version history are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
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
    "trigger": "onLoad"
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
     "carries": [
      "tenantId"
     ],
     "provenance": "derived — CMS-001 declares entryState.params tenantId, so an edge into it must carry them"
    },
    {
     "to": "CMS-002",
     "trigger": "Brand Kit",
     "carries": [
      "uploadId"
     ],
     "provenance": "derived — CMS-002 declares entryState.params uploadId, so an edge into it must carry them"
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
     "provenance": "derived — CMS-003 declares entryState.params bannerId, pageId, policyKind, version, so an edge into it must carry them"
    }
   ]
  },
  "notes": "Definition derived from the wireframe board on 14 August. Components, states and operations still to be written. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual.",
  "density": "compact",
  "pattern": "statusTracker",
  "patternReason": "`getTenantConfig` reads one record and nothing reads a population — the screen is about that one thing",
  "purpose": "The values the whole site inherits from.",
  "layout": {
   "template": "detail",
   "regions": [
    {
     "name": "contentBody",
     "slot": "record",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected site settings",
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
     "name": "contentBody",
     "slot": "carried",
     "components": [
      {
       "kind": "detailPanel",
       "notes": "Structure from the wireframe board. Components not yet enumerated.",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The site settings list.",
   "error": "Could not load. Names which read failed and leaves the site settings untouched.",
   "emptyFirstRun": "No site settings yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the site settings are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getTenantConfig",
    "contract": "white-label",
    "purpose": "Full working configuration",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P13 Venue CMS.dc.html#cms-016"
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
     "carries": [
      "tenantId"
     ],
     "provenance": "derived — CMS-001 declares entryState.params tenantId, so an edge into it must carry them"
    },
    {
     "to": "CMS-002",
     "trigger": "Brand Kit",
     "carries": [
      "uploadId"
     ],
     "provenance": "derived — CMS-002 declares entryState.params uploadId, so an edge into it must carry them"
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
     "provenance": "derived — CMS-003 declares entryState.params bannerId, pageId, policyKind, version, so an edge into it must carry them"
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
       "label": "Every domain certificate",
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
       "label": "The selected domain certificate",
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
       "label": "Claim",
       "operation": "claimCustomDomain",
       "provenance": "contract white-label.yaml POST /tenant-domains"
      },
      {
       "kind": "secondaryButton",
       "label": "Verify",
       "operation": "verifyCustomDomain",
       "provenance": "contract white-label.yaml POST /tenant-domains/{domainId}/verify"
      },
      {
       "kind": "secondaryButton",
       "label": "Release hold",
       "operation": "relinquishCustomDomain",
       "provenance": "contract white-label.yaml DELETE /tenant-domains/{domainId}"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "carried",
     "components": [
      {
       "kind": "detailPanel",
       "notes": "Structure from the wireframe board. Components not yet enumerated.",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "Detail loads",
   "error": "Could not load",
   "emptyFirstRun": "Not found — it may have been deleted or moved out of scope",
   "emptyNoResults": "The filter narrowed it and the domain certificate are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
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
  "requiresModule": "marketing",
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
     "carries": [
      "tenantId"
     ],
     "provenance": "derived — CMS-001 declares entryState.params tenantId, so an edge into it must carry them"
    },
    {
     "to": "CMS-002",
     "trigger": "Brand Kit",
     "carries": [
      "uploadId"
     ],
     "provenance": "derived — CMS-002 declares entryState.params uploadId, so an edge into it must carry them"
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
     "provenance": "derived — CMS-003 declares entryState.params bannerId, pageId, policyKind, version, so an edge into it must carry them"
    }
   ]
  },
  "notes": "Definition derived from the wireframe board on 14 August. Components, states and operations still to be written. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual.",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listGuestDevices` reads the population and `getGuestConsents` reads one of them — list, select, act",
  "purpose": "Manage the notices every consent is captured against.",
  "gaps": [
   {
    "operation": "getConsentHistory",
    "why": "**5 declared operations reach no component on this screen**: getConsentHistory, getGuestLoyalty, getGuestProfile, getWishlist, searchGuests. Either the screen is missing what calls them, or the declaration is residue.",
    "source": "the screen's own declarations"
   }
  ],
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every consent legal",
       "bindsTo": "GuestDevice",
       "columns": [
        "GuestDevice.id",
        "GuestDevice.subjectId",
        "GuestDevice.platform",
        "GuestDevice.tokenFingerprint",
        "GuestDevice.appVersion",
        "GuestDevice.osVersion",
        "GuestDevice.deviceModel",
        "GuestDevice.locale",
        "GuestDevice.status",
        "GuestDevice.failureCount",
        "GuestDevice.registeredAt",
        "GuestDevice.lastSeenAt"
       ],
       "operation": "listGuestDevices",
       "provenance": "contract marketing-crm.yaml GET /guests/{subjectId}/devices"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected consent legal",
       "bindsTo": "ConsentState",
       "columns": [
        "ConsentState.subjectId",
        "ConsentState.purposes"
       ],
       "operation": "getGuestConsents",
       "provenance": "contract marketing-crm.yaml GET /guests/{subjectId}/consents"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Record",
       "operation": "recordConsent",
       "provenance": "contract marketing-crm.yaml POST /guests/{subjectId}/consents"
      },
      {
       "kind": "secondaryButton",
       "label": "Adjust",
       "operation": "adjustLoyaltyPoints",
       "provenance": "contract marketing-crm.yaml POST /guests/{subjectId}/loyalty/adjust"
      },
      {
       "kind": "destructiveButton",
       "label": "Merge",
       "operation": "mergeGuestProfiles",
       "provenance": "contract marketing-crm.yaml POST /guests/{subjectId}/merge"
      },
      {
       "kind": "secondaryButton",
       "label": "Save changes",
       "operation": "updateGuestProfile",
       "provenance": "contract marketing-crm.yaml PATCH /guests/{subjectId}"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "carried",
     "components": [
      {
       "kind": "detailPanel",
       "notes": "Structure from the wireframe board. Components not yet enumerated.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "dataTable",
       "derived": true,
       "impliedBy": "listGuestDevices",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "searchField",
       "derived": true,
       "impliedBy": "searchGuests",
       "label": "Search",
       "notes": "A search that returns nothing must say so differently from a search not yet run.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "recordConsent",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "overlays": [
   {
    "id": "confirmMergeGuestProfiles",
    "component": "confirmDialog",
    "trigger": "Merge",
    "body": "**Names what `mergeGuestProfiles` changes and what it leaves alone**, in the consequence rather than the verb. A consent legal this affects should be identified in the dialog, not just counted.",
    "provenance": "contract marketing-crm.yaml POST /guests/{subjectId}/merge"
   }
  ],
  "states": {
   "loading": "The consent legal list.",
   "error": "Could not load. Names which read failed and leaves the consent legal untouched.",
   "emptyFirstRun": "No consent legal yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the consent legal are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getGuestConsents",
    "contract": "marketing-crm",
    "purpose": "Read a guest's consent state",
    "trigger": "onLoad"
   },
   {
    "operationId": "getConsentHistory",
    "contract": "marketing-crm",
    "purpose": "Full consent history",
    "trigger": "onLoad"
   },
   {
    "operationId": "recordConsent",
    "contract": "marketing-crm",
    "purpose": "Record a consent decision",
    "trigger": "onAction",
    "invalidates": [
     "listGuestDevices"
    ]
   },
   {
    "operationId": "adjustLoyaltyPoints",
    "contract": "marketing-crm",
    "purpose": "Manually adjust points",
    "trigger": "onAction",
    "invalidates": [
     "listGuestDevices"
    ]
   },
   {
    "operationId": "getGuestLoyalty",
    "contract": "marketing-crm",
    "purpose": "A guest's loyalty position",
    "trigger": "onLoad"
   },
   {
    "operationId": "getGuestProfile",
    "contract": "marketing-crm",
    "purpose": "Read a guest profile",
    "trigger": "onLoad"
   },
   {
    "operationId": "getWishlist",
    "contract": "marketing-crm",
    "purpose": "Read a guest's saved items",
    "trigger": "onLoad"
   },
   {
    "operationId": "listGuestDevices",
    "contract": "marketing-crm",
    "purpose": "A guest's registered devices",
    "trigger": "onLoad"
   },
   {
    "operationId": "mergeGuestProfiles",
    "contract": "marketing-crm",
    "purpose": "Merge a duplicate profile into this one",
    "trigger": "onAction",
    "invalidates": [
     "listGuestDevices"
    ]
   },
   {
    "operationId": "searchGuests",
    "contract": "marketing-crm",
    "purpose": "Search guest profiles",
    "trigger": "onLoad"
   },
   {
    "operationId": "updateGuestProfile",
    "contract": "marketing-crm",
    "purpose": "Amend a guest profile",
    "trigger": "onAction",
    "invalidates": [
     "listGuestDevices"
    ]
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "subjectId",
     "from": "session"
    }
   ],
   "coldEntry": "Resolves from the session; a cold arrival is the ordinary case.",
   "preloaded": [
    "ConsentState.subjectId",
    "ConsentState.purposes"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P13 Venue CMS.dc.html#cms-018"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 11 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
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
     "carries": [
      "tenantId"
     ],
     "provenance": "derived — CMS-001 declares entryState.params tenantId, so an edge into it must carry them"
    },
    {
     "to": "CMS-002",
     "trigger": "Brand Kit",
     "carries": [
      "uploadId"
     ],
     "provenance": "derived — CMS-002 declares entryState.params uploadId, so an edge into it must carry them"
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
     "provenance": "derived — CMS-003 declares entryState.params bannerId, pageId, policyKind, version, so an edge into it must carry them"
    }
   ]
  },
  "notes": "Definition derived from the wireframe board on 14 August. Components, states and operations still to be written. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual.",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listPrincipals` reads a population and nothing reads one of them; the detail is the row until a `get` exists",
  "purpose": "Say who in the tenant may change what.",
  "gaps": [
   {
    "operation": "listRoles",
    "why": "**1 declared operation reach no component on this screen**: listRoles. Either the screen is missing what calls them, or the declaration is residue.",
    "source": "the screen's own declarations"
   }
  ],
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every user access",
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
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected user access",
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
    },
    {
     "name": "contentBody",
     "slot": "carried",
     "components": [
      {
       "kind": "detailPanel",
       "notes": "Structure from the wireframe board. Components not yet enumerated.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "dataTable",
       "derived": true,
       "impliedBy": "listPrincipals",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The user access list.",
   "error": "Could not load. Names which read failed and leaves the user access untouched.",
   "emptyFirstRun": "No user access yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the user access are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
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
  "id": "CMS-020",
  "name": "Change Log",
  "module": "White Label",
  "requiresModule": "core",
  "wave": 2,
  "capability": "C00",
  "implementation": {
   "app": "venue-management-web",
   "route": "/white-label/change-log",
   "component": "apps/venue-management-web/src/routes/white-label/ChangeLogDetail.tsx",
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
     "carries": [
      "tenantId"
     ],
     "provenance": "derived — CMS-001 declares entryState.params tenantId, so an edge into it must carry them"
    },
    {
     "to": "CMS-002",
     "trigger": "Brand Kit",
     "carries": [
      "uploadId"
     ],
     "provenance": "derived — CMS-002 declares entryState.params uploadId, so an edge into it must carry them"
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
     "provenance": "derived — CMS-003 declares entryState.params bannerId, pageId, policyKind, version, so an edge into it must carry them"
    }
   ]
  },
  "notes": "Definition derived from the wireframe board on 14 August. Components, states and operations still to be written. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual.",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listConfigVersions` reads a population and nothing reads one of them; the detail is the row until a `get` exists",
  "purpose": "See who changed what, before the publish that carried it.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every change log",
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
       "label": "The selected change log",
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
     "name": "contentBody",
     "slot": "carried",
     "components": [
      {
       "kind": "detailPanel",
       "notes": "Structure from the wireframe board. Components not yet enumerated.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "dataTable",
       "derived": true,
       "impliedBy": "listConfigVersions",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The change log list.",
   "error": "Could not load. Names which read failed and leaves the change log untouched.",
   "emptyFirstRun": "No change log yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the change log are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listConfigVersions",
    "contract": "white-label",
    "purpose": "Version history",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
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
   "board": "wireframes/P13 Venue CMS.dc.html#cms-020"
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
 }
]
```

## `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
 "adjustLoyaltyPoints": {
  "method": "POST",
  "path": "/guests/{subjectId}/loyalty/adjust",
  "contract": "marketing-crm",
  "summary": "Manually adjust points",
  "permission": "LEDGER_POST",
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
  "responds": "LoyaltyPosition"
 },
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
 "getConsentHistory": {
  "method": "GET",
  "path": "/guests/{subjectId}/consents/history",
  "contract": "marketing-crm",
  "summary": "Full consent history",
  "permission": "GUEST_VIEW",
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
 "getGuestConsents": {
  "method": "GET",
  "path": "/guests/{subjectId}/consents",
  "contract": "marketing-crm",
  "summary": "Read a guest's consent state",
  "permission": "GUEST_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "ConsentState"
 },
 "getGuestLoyalty": {
  "method": "GET",
  "path": "/guests/{subjectId}/loyalty",
  "contract": "marketing-crm",
  "summary": "A guest's loyalty position",
  "permission": "GUEST_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "LoyaltyPosition"
 },
 "getGuestProfile": {
  "method": "GET",
  "path": "/guests/{subjectId}",
  "contract": "marketing-crm",
  "summary": "Read a guest profile",
  "permission": "GUEST_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "GuestProfileDetail"
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
 "getWishlist": {
  "method": "GET",
  "path": "/guests/{subjectId}/wishlist",
  "contract": "marketing-crm",
  "summary": "Read a guest's saved items",
  "permission": null,
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "subject",
  "parameters": [],
  "requestBody": null,
  "responds": "Wishlist"
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
 "listGuestDevices": {
  "method": "GET",
  "path": "/guests/{subjectId}/devices",
  "contract": "marketing-crm",
  "summary": "A guest's registered devices",
  "permission": null,
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "subject",
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
  "responds": "GuestDevice"
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
 "mergeGuestProfiles": {
  "method": "POST",
  "path": "/guests/{subjectId}/merge",
  "contract": "marketing-crm",
  "summary": "Merge a duplicate profile into this one",
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
  "requestBody": null,
  "responds": "MergeResult"
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
 "recordConsent": {
  "method": "POST",
  "path": "/guests/{subjectId}/consents",
  "contract": "marketing-crm",
  "summary": "Record a consent decision",
  "permission": null,
  "offlineCapable": false,
  "conflictPolicy": "append",
  "scopeLevel": "subject",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "RecordConsentRequest",
  "responds": "ConsentState"
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
  "parameters": [],
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
 "searchGuests": {
  "method": "GET",
  "path": "/guests",
  "contract": "marketing-crm",
  "summary": "Search guest profiles",
  "permission": "GUEST_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "search",
    "in": "query",
    "required": null
   },
   {
    "name": "segmentId",
    "in": "query",
    "required": null
   },
   {
    "name": "hasConsentFor",
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
 "updateGuestProfile": {
  "method": "PATCH",
  "path": "/guests/{subjectId}",
  "contract": "marketing-crm",
  "summary": "Amend a guest profile",
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
  "requestBody": null,
  "responds": "GuestProfileDetail"
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
 "AppIcons": {
  "x-ticvai-persistence": "none — embedded in tenant_config",
  "type": "object",
  "required": [
   "sourceAssetRef",
   "changeScope"
  ],
  "properties": {
   "sourceAssetRef": {
    "type": "string"
   },
   "derived": {
    "type": "array",
    "readOnly": true,
    "items": {
     "type": "object",
     "properties": {
      "platform": {
       "type": "string"
      },
      "size": {
       "type": "string"
      },
      "assetRef": {
       "type": "string"
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
    "readOnly": true
   },
   "liveVersion": {
    "type": "string",
    "nullable": true,
    "description": "Icon currently shipped. Differs from the draft until the next release."
   },
   "requiresRebuild": {
    "type": "boolean",
    "readOnly": true
   }
  }
 },
 "BrandIdentity": {
  "x-ticvai-persistence": "none — embedded in tenant_config",
  "type": "object",
  "required": [
   "logoAssetRef"
  ],
  "properties": {
   "logoAssetRef": {
    "type": "string"
   },
   "logoDarkAssetRef": {
    "type": "string",
    "nullable": true,
    "description": "Used on dark backgrounds. Falls back to the primary logo."
   },
   "faviconAssetRef": {
    "type": "string",
    "nullable": true
   },
   "splashImageAssetRefs": {
    "type": "array",
    "items": {
     "type": "string"
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
    "description": "Always `buildTime` for native apps."
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
   "arabicFontMissing"
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
        "type": "string"
       }
      }
     }
    }
   },
   "scopePath": {
    "type": "string",
    "description": "**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `tenant` scope.**"
   }
  }
 },
 "ConsentDecision": {
  "type": "string",
  "enum": [
   "granted",
   "withdrawn",
   "notAsked"
  ]
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
 "ConsentSource": {
  "type": "string",
  "enum": [
   "guestApp",
   "website",
   "kiosk",
   "pos",
   "callCentre",
   "import",
   "agentRecorded"
  ]
 },
 "ConsentState": {
  "x-ticvai-persistence": "none — projection over consent_record",
  "type": "object",
  "required": [
   "subjectId",
   "purposes"
  ],
  "properties": {
   "subjectId": {
    "type": "string",
    "format": "uuid"
   },
   "purposes": {
    "type": "array",
    "items": {
     "type": "object",
     "required": [
      "purpose",
      "decision",
      "requiresRenewal"
     ],
     "properties": {
      "purpose": {
       "$ref": "#/components/schemas/ConsentPurpose"
      },
      "decision": {
       "$ref": "#/components/schemas/ConsentDecision"
      },
      "channels": {
       "type": "array",
       "items": {
        "$ref": "#/components/schemas/MessageChannel"
       }
      },
      "noticeVersion": {
       "type": "string",
       "nullable": true
      },
      "requiresRenewal": {
       "type": "boolean",
       "description": "True where the notice has been superseded since consent was given."
      },
      "decidedAt": {
       "type": "string",
       "format": "date-time",
       "nullable": true
      }
     }
    }
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
    "type": "string",
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
    "description": "Required when Arabic is enabled. A Latin face alone leaves Arabic in a system fallback that will not match.\n"
   },
   "secondaryLatin": {
    "type": "string",
    "nullable": true
   },
   "secondaryArabic": {
    "type": "string",
    "nullable": true
   },
   "customFontAssetRefs": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "changeScope": {
    "allOf": [
     {
      "$ref": "#/components/schemas/ChangeScope"
     }
    ],
    "readOnly": true,
    "description": "Custom font files are `buildTime`; selecting a bundled face is `runtime`."
   }
  }
 },
 "FooterConfig": {
  "type": "object",
  "x-ticvai-persistence": "control.footer_config",
  "description": "BL-002. **`setHeader` and `HeaderConfig` exist and the footer does not**, which looked like symmetry until you notice it is not: **a header is chrome and a footer is a link surface.**\nA footer carries the legal links — terms, privacy, accessibility statement, cookie preferences — and **those are the ones a regulator checks.** Treating it as a mirror of the header would have given it a logo and no way to reach a privacy notice.\n",
  "required": [
   "id",
   "scopePath"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "scopePath": {
    "type": "string"
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
 "GuestDevice": {
  "type": "object",
  "x-ticvai-persistence": "marketing.guest_device",
  "required": [
   "id",
   "subjectId",
   "platform",
   "status",
   "registeredAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "subjectId": {
    "type": "string",
    "format": "uuid"
   },
   "platform": {
    "type": "string",
    "enum": [
     "ios",
     "android",
     "web"
    ]
   },
   "tokenFingerprint": {
    "type": "string",
    "description": "Hash of the token, not the token. The token itself is write-only — returning it would put a push credential in every response a support agent can read.\n"
   },
   "appVersion": {
    "type": "string",
    "nullable": true
   },
   "osVersion": {
    "type": "string",
    "nullable": true
   },
   "deviceModel": {
    "type": "string",
    "nullable": true
   },
   "locale": {
    "type": "string",
    "nullable": true
   },
   "status": {
    "type": "string",
    "enum": [
     "active",
     "revoked",
     "failed"
    ]
   },
   "failureCount": {
    "type": "integer",
    "description": "Consecutive delivery failures. Past the threshold the device is marked failed and stops being targeted — a dead token retried forever is wasted quota and a misleading delivery rate.\n"
   },
   "registeredAt": {
    "type": "string",
    "format": "date-time"
   },
   "lastSeenAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "revokedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   }
  }
 },
 "GuestProfile": {
  "x-ticvai-persistence": "marketing.guest_profile",
  "type": "object",
  "required": [
   "subjectId",
   "isActive"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "description": "**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"
   },
   "subjectId": {
    "type": "string",
    "format": "uuid",
    "description": "Opaque reference. Personal data lives in the separately erasable store, which is what makes erasure possible against an append-only ledger.\n"
   },
   "displayName": {
    "type": "string",
    "nullable": true
   },
   "email": {
    "type": "string",
    "nullable": true
   },
   "phone": {
    "type": "string",
    "nullable": true
   },
   "preferredLanguage": {
    "type": "string",
    "nullable": true
   },
   "preferredChannel": {
    "$ref": "#/components/schemas/MessageChannel"
   },
   "guestLinkId": {
    "type": "string",
    "nullable": true,
    "description": "Present where the guest is linked across cells. Marketing acts locally."
   },
   "tags": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "engagementScore": {
    "type": "integer",
    "nullable": true,
    "minimum": 0,
    "maximum": 100,
    "description": "22.2.20 and 22.2.21. **`lifetimeValue` and `visitCount` existed, so value was a stored figure and engagement was not.** They are different questions: a guest who spent a lot once and a guest who visits monthly have the same LTV and need opposite treatment.\n**Recency, frequency and breadth, not spend** — spend is already `lifetimeValue`, and folding it in here would make one number twice.\n"
   },
   "engagementTier": {
    "type": "string",
    "nullable": true,
    "enum": [
     "new",
     "active",
     "occasional",
     "lapsing",
     "lapsed",
     "dormant"
    ],
    "description": "5.3.19. **Automatic classification, computed rather than assigned.** `lapsing` is the tier the whole field exists for — **a guest who has not been for a while and still might is the only one marketing can change**, and lumping them with `lapsed` wastes the window.\n"
   },
   "lifetimeValue": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "visitCount": {
    "type": "integer"
   },
   "lastVisitAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "isActive": {
    "type": "boolean"
   }
  }
 },
 "GuestProfileDetail": {
  "x-ticvai-persistence": "marketing.guest_profile",
  "allOf": [
   {
    "$ref": "#/components/schemas/GuestProfile"
   },
   {
    "type": "object",
    "properties": {
     "id": {
      "type": "string",
      "format": "uuid",
      "readOnly": true,
      "description": "**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"
     },
     "consents": {
      "$ref": "#/components/schemas/ConsentState"
     },
     "loyalty": {
      "$ref": "#/components/schemas/LoyaltyPosition"
     },
     "openCaseCount": {
      "type": "integer"
     },
     "recentOrderIds": {
      "type": "array",
      "items": {
       "type": "string"
      }
     },
     "membershipIds": {
      "type": "array",
      "items": {
       "type": "string",
       "format": "uuid"
      }
     },
     "notes": {
      "type": "string",
      "nullable": true
     }
    }
   }
  ]
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
     "type": "string"
    }
   },
   "defaultLanguage": {
    "type": "string"
   },
   "rtlLanguages": {
    "type": "array",
    "readOnly": true,
    "items": {
     "type": "string"
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
 "LocalisedText": {
  "x-ticvai-persistence": "none — jsonb column",
  "type": "object",
  "additionalProperties": {
   "type": "string"
  }
 },
 "LoyaltyPosition": {
  "x-ticvai-persistence": "marketing.loyalty_position",
  "type": "object",
  "required": [
   "subjectId",
   "programmeId",
   "pointsBalance",
   "tierCode"
  ],
  "properties": {
   "subjectId": {
    "type": "string",
    "format": "uuid"
   },
   "programmeId": {
    "type": "string",
    "format": "uuid"
   },
   "pointsBalance": {
    "type": "integer"
   },
   "lifetimePoints": {
    "type": "integer"
   },
   "tierCode": {
    "type": "string"
   },
   "tierName": {
    "type": "string"
   },
   "pointsToNextTier": {
    "type": "integer",
    "nullable": true
   },
   "nextExpiryPoints": {
    "type": "integer",
    "nullable": true
   },
   "nextExpiryAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   }
  }
 },
 "MergeResult": {
  "x-ticvai-persistence": "none — computed",
  "type": "object",
  "required": [
   "survivingSubjectId",
   "absorbedSubjectId",
   "transferred"
  ],
  "properties": {
   "survivingSubjectId": {
    "type": "string",
    "format": "uuid"
   },
   "absorbedSubjectId": {
    "type": "string",
    "format": "uuid"
   },
   "transferred": {
    "type": "object",
    "properties": {
     "orders": {
      "type": "integer"
     },
     "cases": {
      "type": "integer"
     },
     "loyaltyPoints": {
      "type": "integer"
     }
    }
   },
   "consentOutcome": {
    "type": "array",
    "description": "Per purpose, the resulting position. Where the two profiles disagreed, the more restrictive position won.\n",
    "items": {
     "type": "object",
     "properties": {
      "purpose": {
       "$ref": "#/components/schemas/ConsentPurpose"
      },
      "result": {
       "$ref": "#/components/schemas/ConsentDecision"
      },
      "wasRestricted": {
       "type": "boolean"
      }
     }
    }
   }
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
    "description": "Navigation items and homepage sections pointing at this module.",
    "items": {
     "type": "string"
    }
   }
  }
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
 "RecordConsentRequest": {
  "x-ticvai-persistence": "none — request only",
  "type": "object",
  "required": [
   "purpose",
   "decision",
   "noticeVersion",
   "source",
   "recordedAt"
  ],
  "properties": {
   "purpose": {
    "$ref": "#/components/schemas/ConsentPurpose"
   },
   "decision": {
    "$ref": "#/components/schemas/ConsentDecision"
   },
   "channels": {
    "type": "array",
    "description": "Omit to apply to every channel the purpose covers.",
    "items": {
     "$ref": "#/components/schemas/MessageChannel"
    }
   },
   "noticeVersion": {
    "type": "string"
   },
   "source": {
    "$ref": "#/components/schemas/ConsentSource"
   },
   "recordedAt": {
    "type": "string",
    "format": "date-time"
   }
  }
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
    "type": "string",
    "description": "**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `tenant` scope.**"
   }
  }
 },
 "TenantAppStatus": {
  "x-ticvai-persistence": "none — computed",
  "type": "object",
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
    "type": "boolean"
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
    "type": "string"
   },
   "hasUnpublishedChanges": {
    "type": "boolean"
   },
   "activeModuleCount": {
    "type": "integer"
   },
   "licensedModuleCount": {
    "type": "integer"
   },
   "activePageCount": {
    "type": "integer"
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
   "recentChanges": {
    "type": "array",
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
  "required": [
   "tenantId",
   "version",
   "brand",
   "theme",
   "fonts",
   "navigation",
   "homepage",
   "languages"
  ],
  "properties": {
   "tenantId": {
    "type": "string",
    "format": "uuid"
   },
   "version": {
    "type": "string"
   },
   "isDraft": {
    "type": "boolean"
   },
   "brand": {
    "$ref": "#/components/schemas/BrandIdentity"
   },
   "appIcons": {
    "$ref": "#/components/schemas/AppIcons"
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
      "type": "string"
     },
     "backgroundColour": {
      "type": "string"
     },
     "textColour": {
      "type": "string"
     }
    }
   },
   "cornerRadius": {
    "type": "integer",
    "minimum": 0,
    "maximum": 32
   }
  }
 },
 "Wishlist": {
  "type": "object",
  "required": [
   "subjectId",
   "items"
  ],
  "x-ticvai-persistence": "none — wrapper. The items are the table, keyed by subject",
  "properties": {
   "subjectId": {
    "type": "string",
    "format": "uuid"
   },
   "items": {
    "type": "array",
    "x-ticvai-persistence": "marketing.wishlist_item",
    "items": {
     "type": "object",
     "required": [
      "id",
      "variantId",
      "addedAt",
      "isAvailable"
     ],
     "properties": {
      "id": {
       "type": "string",
       "format": "uuid"
      },
      "variantId": {
       "type": "string",
       "format": "uuid"
      },
      "productName": {
       "type": "string"
      },
      "performanceId": {
       "type": "string",
       "format": "uuid",
       "nullable": true
      },
      "performanceStartsAt": {
       "type": "string",
       "format": "date-time",
       "nullable": true
      },
      "price": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      },
      "imageAssetRef": {
       "type": "string",
       "nullable": true
      },
      "isAvailable": {
       "type": "boolean",
       "description": "False where the product has been withdrawn or the performance has passed. Returned rather than dropped — a guest who saved something and finds it silently gone assumes the feature is broken.\n"
      },
      "unavailableReason": {
       "type": "string",
       "nullable": true
      },
      "note": {
       "type": "string",
       "nullable": true
      },
      "addedAt": {
       "type": "string",
       "format": "date-time"
      }
     }
    }
   }
  }
 }
}
```
