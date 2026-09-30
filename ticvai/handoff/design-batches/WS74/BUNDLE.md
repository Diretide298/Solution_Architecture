# WS74 — Digital Asset Management DAM board 1

**10 screens · 15 operations · 16 schemas · 3 permissions**

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

- **Every control that can be refused must be gated.** 3 permissions apply here:
  `AI_USE, ASSET_LIBRARY_MANAGE, ASSET_LIBRARY_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `CMS-061` | Digital Asset Management Command Center | listDetail | 2 | 0 | — |
| `CMS-062` | Central Digital Asset Library | listDetail | 3 | 0 | — |
| `CMS-063` | Upload & Asset Ingestion Workspace | listDetail | 3 | 0 | — |
| `CMS-064` | Folder, Collection & Workspace Management | listDetail | 2 | 0 | — |
| `CMS-065` | Metadata & Taxonomy Management | listDetail | 2 | 0 | — |
| `CMS-066` | Tags, Keywords & Classification | configEditor | 2 | 0 | — |
| `CMS-067` | Advanced Search & Discovery | listDetail | 1 | 0 | — |
| `CMS-068` | Digital Asset 360° Profile | listDetail | 3 | 0 | — |
| `CMS-069` | Bulk Asset Management Workspace | listDetail | 1 | 0 | — |
| `CMS-070` | Asset Activity, Recent Assets & Library Health | listDetail | 1 | 0 | — |

## Thin screens in this batch

**CMS-063, CMS-068, CMS-069 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "CMS-061",
  "name": "Digital Asset Management Command Center",
  "module": "Media Library",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Digital Asset Management DAM.pdf",
   "board": "1",
   "number": "1",
   "page": 3
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/media-library/digital-asset-management-command-center-cms-061",
   "component": "apps/venue-management-web/src/routes/media-library/DigitalAssetManagementCommandCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "CMS-001"
   ],
   "exitTo": [
    "CMS-001",
    "CMS-062",
    "CMS-063",
    "CMS-064",
    "CMS-065",
    "CMS-066",
    "CMS-067",
    "CMS-068",
    "CMS-069",
    "CMS-070"
   ],
   "transitions": [
    {
     "to": "CMS-001",
     "trigger": "Back to Tenant Workspace",
     "provenance": "structural — pack board 1 wiring, 11 September 2026",
     "back": true
    },
    {
     "to": "CMS-062",
     "trigger": "Central Digital Asset Library",
     "provenance": "structural — pack board 1 wiring, 11 September 2026"
    },
    {
     "to": "CMS-063",
     "trigger": "Upload & Asset Ingestion Workspace",
     "provenance": "structural — pack board 1 wiring, 11 September 2026"
    },
    {
     "to": "CMS-064",
     "trigger": "Folder, Collection & Workspace Management",
     "provenance": "structural — pack board 1 wiring, 11 September 2026"
    },
    {
     "to": "CMS-065",
     "trigger": "Metadata & Taxonomy Management",
     "provenance": "structural — pack board 1 wiring, 11 September 2026"
    },
    {
     "to": "CMS-066",
     "trigger": "Tags, Keywords & Classification",
     "provenance": "structural — pack board 1 wiring, 11 September 2026"
    },
    {
     "to": "CMS-067",
     "trigger": "Advanced Search & Discovery",
     "provenance": "structural — pack board 1 wiring, 11 September 2026"
    },
    {
     "to": "CMS-068",
     "trigger": "Digital Asset 360° Profile",
     "provenance": "structural — pack board 1 wiring, 11 September 2026"
    },
    {
     "to": "CMS-069",
     "trigger": "Bulk Asset Management Workspace",
     "provenance": "structural — pack board 1 wiring, 11 September 2026"
    },
    {
     "to": "CMS-070",
     "trigger": "Asset Activity, Recent Assets & Library Health",
     "provenance": "structural — pack board 1 wiring, 11 September 2026"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display; Show) and no metric row",
  "purpose": "Provide a centralized operational dashboard showing the complete digital asset estate across the authorized tenant and venue scope.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 3 actions on this screen and the screen declares 0 operations.** Unserved: Upload Assets, Browse Library, Create Collection. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Digital Asset Management DAM.pdf, page 3 §Quick Actions"
   },
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Digital Asset Management DAM.pdf, page 3 §Display"
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
       "label": "Every digital asset",
       "columns": [
        "Total Digital Assets",
        "Images",
        "Videos",
        "Uploads",
        "Updates",
        "Downloads",
        "Shares",
        "Recently Used"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Digital Asset Management DAM.pdf, page 3 §Display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected digital asset",
       "bindsTo": null,
       "columns": [
        "Total Digital Assets",
        "Images",
        "Videos",
        "Uploads",
        "Updates",
        "Downloads",
        "Shares",
        "Recently Used"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Digital Asset Management”, “Unclassified 128”, “Charts by”.",
       "provenance": "pack Digital Asset Management DAM.pdf, page 3 §Display"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Upload Assets",
       "provenance": "pack Digital Asset Management DAM.pdf, page 3 §Quick Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Browse Library",
       "provenance": "pack Digital Asset Management DAM.pdf, page 3 §Quick Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Create Collection",
       "provenance": "pack Digital Asset Management DAM.pdf, page 3 §Quick Actions"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The digital asset list.",
   "error": "Could not load. Names which read failed and leaves the digital asset untouched.",
   "emptyFirstRun": "No digital asset yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the digital asset are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "searchMedia",
    "contract": "assets",
    "purpose": "The estate, counted and charted",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "getMediaUsageAnalytics",
    "contract": "assets",
    "purpose": "Storage, uploads and library health",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "entryState": {
   "preloaded": [
    "Total Digital Assets",
    "Images",
    "Videos",
    "Uploads",
    "Updates",
    "Downloads"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P13 Venue CMS.dc.html#cms-061",
   "workshopBoard": "wireframes/WS44 Digital Asset Management DAM Board 1.dc.html#cms-061"
  },
  "apisNote": "Regenerated 9 September 2026 from Digital Asset Management DAM.pdf page 3. 0 of 8 labels bound to a contract property; 11 of 33 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "CMS-062",
  "name": "Central Digital Asset Library",
  "module": "Media Library",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Digital Asset Management DAM.pdf",
   "board": "1",
   "number": "2",
   "page": 5
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/media-library/central-digital-asset-library-cms-062",
   "component": "apps/venue-management-web/src/routes/media-library/CentralDigitalAssetLibrary.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "CMS-061"
   ],
   "exitTo": [
    "CMS-061"
   ],
   "transitions": [
    {
     "to": "CMS-061",
     "trigger": "Back to Digital Asset Management Command Center",
     "provenance": "structural — pack board 1 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Each card should show) and no metric row",
  "purpose": "Provide the main workspace for browsing all digital assets available to the authorized user.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 7 actions on this screen and the screen declares 0 operations.** Unserved: File Size, Ticket Media, Preview, View Details, Download, Add to Collection, Move. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Digital Asset Management DAM.pdf, page 5 §Support"
   },
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Digital Asset Management DAM.pdf, page 5 §Each card should show"
   }
  ],
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "filters",
     "components": [
      {
       "kind": "searchField",
       "label": "Search central digital asset",
       "provenance": "pack Digital Asset Management DAM.pdf, page 5 §Allow filtering by"
      },
      {
       "kind": "multiSelect",
       "label": "Filter by",
       "columns": [
        "Tenant",
        "Venue",
        "Asset Type",
        "Category",
        "Collection",
        "Tags",
        "Owner",
        "Created Date",
        "Updated Date",
        "Status",
        "File Format"
       ],
       "notes": "The pack filters this screen by tenant, venue, asset type, category, collection, tags and 5 more — which are present is a decision the pack already made.",
       "provenance": "pack Digital Asset Management DAM.pdf, page 5 §Allow filtering by"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every central digital asset",
       "columns": [
        "Thumbnail",
        "asset name",
        "asset type",
        "category",
        "dimensions/duration where applicable",
        "file size",
        "status",
        "owner",
        "updated date"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Digital Asset Management DAM.pdf, page 5 §Each card should show"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected central digital asset",
       "bindsTo": null,
       "columns": [
        "Thumbnail",
        "asset name",
        "asset type",
        "category",
        "dimensions/duration where applicable",
        "file size",
        "status",
        "owner",
        "updated date"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Image”, “Venue Media”, “Archive”.",
       "provenance": "pack Digital Asset Management DAM.pdf, page 5 §Each card should show"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "File Size",
       "provenance": "pack Digital Asset Management DAM.pdf, page 5 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Ticket Media",
       "provenance": "pack Digital Asset Management DAM.pdf, page 5 §Support at minimum"
      },
      {
       "kind": "secondaryButton",
       "label": "Preview",
       "provenance": "pack Digital Asset Management DAM.pdf, page 5 §Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "View Details",
       "provenance": "pack Digital Asset Management DAM.pdf, page 5 §Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Download",
       "provenance": "pack Digital Asset Management DAM.pdf, page 5 §Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Add to Collection",
       "provenance": "pack Digital Asset Management DAM.pdf, page 5 §Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Move",
       "provenance": "pack Digital Asset Management DAM.pdf, page 5 §Actions"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The central digital asset list.",
   "error": "Could not load. Names which read failed and leaves the central digital asset untouched.",
   "emptyFirstRun": "No central digital asset yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the central digital asset are still there. The pack's own statuses are 🟢 Active — the state names which is selected.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "searchMedia",
    "contract": "assets",
    "purpose": "Browse and filter the library",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "listCollections",
    "contract": "assets",
    "purpose": "Collections to file into",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "semanticSearch",
    "contract": "ai",
    "purpose": "Natural-language search of the media library (kind media)",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   }
  ],
  "entryState": {
   "preloaded": [
    "Thumbnail",
    "asset name",
    "asset type",
    "category",
    "dimensions/duration where applicable",
    "file size"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P13 Venue CMS.dc.html#cms-062",
   "workshopBoard": "wireframes/WS44 Digital Asset Management DAM Board 1.dc.html#cms-062"
  },
  "apisNote": "Regenerated 9 September 2026 from Digital Asset Management DAM.pdf page 5. 0 of 20 labels bound to a contract property; 28 of 50 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "CMS-063",
  "name": "Upload & Asset Ingestion Workspace",
  "module": "Media Library",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Digital Asset Management DAM.pdf",
   "board": "1",
   "number": "3",
   "page": 6
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/media-library/upload-asset-ingestion-workspace-cms-063",
   "component": "apps/venue-management-web/src/routes/media-library/UploadAssetIngestionWorkspace.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "CMS-061"
   ],
   "exitTo": [
    "CMS-061"
   ],
   "transitions": [
    {
     "to": "CMS-061",
     "trigger": "Back to Digital Asset Management Command Center",
     "provenance": "structural — pack board 1 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Provide a controlled process for adding digital assets into TICVAI. before or after upload.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 3 actions on this screen and the screen declares 0 operations.** Unserved: Browse Files, Bulk Upload, Import from Approved Source. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Digital Asset Management DAM.pdf, page 6 §Support"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Digital Asset Management DAM.pdf, page 6"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Digital Asset Management DAM.pdf, page 6"
   }
  ],
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Browse Files",
       "provenance": "pack Digital Asset Management DAM.pdf, page 6 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Bulk Upload",
       "provenance": "pack Digital Asset Management DAM.pdf, page 6 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Import from Approved Source",
       "provenance": "pack Digital Asset Management DAM.pdf, page 6 §Support"
      }
     ]
    },
    {
     "name": "contentBody",
     "components": []
    }
   ]
  },
  "states": {
   "loading": "The upload asset ingestion list.",
   "error": "Could not load. Names which read failed and leaves the upload asset ingestion untouched.",
   "emptyFirstRun": "No upload asset ingestion yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the upload asset ingestion are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "createUpload",
    "contract": "assets",
    "purpose": "Start an upload",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "searchMedia"
    ]
   },
   {
    "operationId": "completeUpload",
    "contract": "assets",
    "purpose": "Finish it",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "searchMedia",
     "getMediaUsageAnalytics"
    ]
   },
   {
    "operationId": "analyseMediaAsset",
    "contract": "assets",
    "purpose": "Auto-tag on ingest",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "getMediaAsset"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P13 Venue CMS.dc.html#cms-063",
   "workshopBoard": "wireframes/WS44 Digital Asset Management DAM Board 1.dc.html#cms-063"
  },
  "apisNote": "Regenerated 9 September 2026 from Digital Asset Management DAM.pdf page 6. 0 of 0 labels bound to a contract property; 3 of 31 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "assetId",
     "from": "navigation"
    },
    {
     "name": "uploadId",
     "from": "navigation"
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
  "id": "CMS-064",
  "name": "Folder, Collection & Workspace Management",
  "module": "Media Library",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Digital Asset Management DAM.pdf",
   "board": "1",
   "number": "4",
   "page": 8
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/media-library/folder-collection-workspace-management-cms-064",
   "component": "apps/venue-management-web/src/routes/media-library/FolderCollectionWorkspaceManagement.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "CMS-061"
   ],
   "exitTo": [
    "CMS-061"
   ],
   "transitions": [
    {
     "to": "CMS-061",
     "trigger": "Back to Digital Asset Management Command Center",
     "provenance": "structural — pack board 1 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Allow users to organize assets without relying only on physical file-storage concepts.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 12 actions on this screen and the screen declares 0 operations.** Unserved: Manual Collection, Dynamic Collection, Campaign Collection, Brand Collection, Event Collection, Create Folder, Create Collection, Move Assets …. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Digital Asset Management DAM.pdf, page 8 §Support"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Digital Asset Management DAM.pdf, page 8"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Digital Asset Management DAM.pdf, page 8"
   }
  ],
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Manual Collection",
       "provenance": "pack Digital Asset Management DAM.pdf, page 8 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Dynamic Collection",
       "provenance": "pack Digital Asset Management DAM.pdf, page 8 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Campaign Collection",
       "provenance": "pack Digital Asset Management DAM.pdf, page 8 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Brand Collection",
       "provenance": "pack Digital Asset Management DAM.pdf, page 8 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Event Collection",
       "provenance": "pack Digital Asset Management DAM.pdf, page 8 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Create Folder",
       "provenance": "pack Digital Asset Management DAM.pdf, page 8 §Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Create Collection",
       "provenance": "pack Digital Asset Management DAM.pdf, page 8 §Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Move Assets",
       "provenance": "pack Digital Asset Management DAM.pdf, page 8 §Actions"
      }
     ]
    },
    {
     "name": "contentBody",
     "components": []
    }
   ]
  },
  "states": {
   "loading": "The folder collection list.",
   "error": "Could not load. Names which read failed and leaves the folder collection untouched.",
   "emptyFirstRun": "No folder collection yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the folder collection are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listCollections",
    "contract": "assets",
    "purpose": "Folders and collections",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "createCollection",
    "contract": "assets",
    "purpose": "Create one",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listCollections"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P13 Venue CMS.dc.html#cms-064",
   "workshopBoard": "wireframes/WS44 Digital Asset Management DAM Board 1.dc.html#cms-064"
  },
  "apisNote": "Regenerated 9 September 2026 from Digital Asset Management DAM.pdf page 8. 0 of 0 labels bound to a contract property; 12 of 33 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "CMS-065",
  "name": "Metadata & Taxonomy Management",
  "module": "Media Library",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Digital Asset Management DAM.pdf",
   "board": "1",
   "number": "5",
   "page": 9
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/media-library/metadata-taxonomy-management-cms-065",
   "component": "apps/venue-management-web/src/routes/media-library/MetadataTaxonomyManagement.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "CMS-061"
   ],
   "exitTo": [
    "CMS-061"
   ],
   "transitions": [
    {
     "to": "CMS-061",
     "trigger": "Back to Digital Asset Management Command Center",
     "provenance": "structural — pack board 1 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Create the structured metadata model that makes TICVAI's DAM searchable and scalable.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 9 actions on this screen and the screen declares 0 operations.** Unserved: Asset Name, Asset Type, Venue, Campaign, Event, Attraction, Owner, Source …. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Digital Asset Management DAM.pdf, page 9 §Support"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Digital Asset Management DAM.pdf, page 9"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Digital Asset Management DAM.pdf, page 9"
   }
  ],
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Asset Name",
       "provenance": "pack Digital Asset Management DAM.pdf, page 9 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Asset Type",
       "provenance": "pack Digital Asset Management DAM.pdf, page 9 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Venue",
       "provenance": "pack Digital Asset Management DAM.pdf, page 9 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Campaign",
       "provenance": "pack Digital Asset Management DAM.pdf, page 9 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Event",
       "provenance": "pack Digital Asset Management DAM.pdf, page 9 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Attraction",
       "provenance": "pack Digital Asset Management DAM.pdf, page 9 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Owner",
       "provenance": "pack Digital Asset Management DAM.pdf, page 9 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Source",
       "provenance": "pack Digital Asset Management DAM.pdf, page 9 §Support"
      }
     ]
    },
    {
     "name": "contentBody",
     "components": []
    }
   ]
  },
  "states": {
   "loading": "The metadata taxonomy list.",
   "error": "Could not load. Names which read failed and leaves the metadata taxonomy untouched.",
   "emptyFirstRun": "No metadata taxonomy yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the metadata taxonomy are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getMediaTaxonomy",
    "contract": "assets",
    "purpose": "Categories and metadata fields",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "setMediaTaxonomy",
    "contract": "assets",
    "purpose": "Define them",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "getMediaTaxonomy"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P13 Venue CMS.dc.html#cms-065",
   "workshopBoard": "wireframes/WS44 Digital Asset Management DAM Board 1.dc.html#cms-065"
  },
  "apisNote": "Regenerated 9 September 2026 from Digital Asset Management DAM.pdf page 9. 0 of 0 labels bound to a contract property; 9 of 51 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "CMS-066",
  "name": "Tags, Keywords & Classification",
  "module": "Media Library",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Digital Asset Management DAM.pdf",
   "board": "1",
   "number": "6",
   "page": 11
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/media-library/tags-keywords-classification-cms-066",
   "component": "apps/venue-management-web/src/routes/media-library/TagsKeywordsClassification.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "CMS-061"
   ],
   "exitTo": [
    "CMS-061"
   ],
   "transitions": [
    {
     "to": "CMS-061",
     "trigger": "Back to Digital Asset Management Command Center",
     "provenance": "structural — pack board 1 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Select 100 assets and apply) and no display directory — it is settings, not a population",
  "purpose": "Provide flexible classification in addition to formal taxonomy.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Venue: Dubai Park",
       "provenance": "pack Digital Asset Management DAM.pdf, page 11 §Select 100 assets and apply"
      },
      {
       "kind": "selectField",
       "label": "Category: Marketing",
       "provenance": "pack Digital Asset Management DAM.pdf, page 11 §Select 100 assets and apply"
      },
      {
       "kind": "selectField",
       "label": "Campaign: Summer 2026",
       "provenance": "pack Digital Asset Management DAM.pdf, page 11 §Select 100 assets and apply"
      },
      {
       "kind": "selectField",
       "label": "Tags: Family, Outdoor",
       "provenance": "pack Digital Asset Management DAM.pdf, page 11 §Select 100 assets and apply"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The tags keywords classification configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the tags keywords classification untouched.",
   "emptyFirstRun": "No tags keywords classification configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [
   {
    "operationId": "setMediaAssetTags",
    "contract": "assets",
    "purpose": "Tags and keywords, with their origin",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "searchMedia",
     "getMediaAsset"
    ]
   },
   {
    "operationId": "getMediaTaxonomy",
    "contract": "assets",
    "purpose": "The controlled vocabularies",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P13 Venue CMS.dc.html#cms-066",
   "workshopBoard": "wireframes/WS44 Digital Asset Management DAM Board 1.dc.html#cms-066"
  },
  "apisNote": "Regenerated 9 September 2026 from Digital Asset Management DAM.pdf page 11. 0 of 0 labels bound to a contract property; 4 of 10 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "assetId",
     "from": "navigation"
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
  "id": "CMS-067",
  "name": "Advanced Search & Discovery",
  "module": "Media Library",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Digital Asset Management DAM.pdf",
   "board": "1",
   "number": "7",
   "page": 12
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/media-library/advanced-search-discovery-cms-067",
   "component": "apps/venue-management-web/src/routes/media-library/AdvancedSearchDiscovery.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "CMS-061"
   ],
   "exitTo": [
    "CMS-061"
   ],
   "transitions": [
    {
     "to": "CMS-061",
     "trigger": "Back to Digital Asset Management Command Center",
     "provenance": "structural — pack board 1 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Allow users to find assets quickly even when the library contains hundreds of thousands or millions of records.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 5 actions on this screen and the screen declares 0 operations.** Unserved: Asset Type, File Format, Venue, Collection, Owner. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Digital Asset Management DAM.pdf, page 12 §Support"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Digital Asset Management DAM.pdf, page 12"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Digital Asset Management DAM.pdf, page 12"
   }
  ],
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Asset Type",
       "provenance": "pack Digital Asset Management DAM.pdf, page 12 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "File Format",
       "provenance": "pack Digital Asset Management DAM.pdf, page 12 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Venue",
       "provenance": "pack Digital Asset Management DAM.pdf, page 12 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Collection",
       "provenance": "pack Digital Asset Management DAM.pdf, page 12 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Owner",
       "provenance": "pack Digital Asset Management DAM.pdf, page 12 §Support"
      }
     ]
    },
    {
     "name": "contentBody",
     "components": []
    }
   ]
  },
  "states": {
   "loading": "The advanced search discovery list.",
   "error": "Could not load. Names which read failed and leaves the advanced search discovery untouched.",
   "emptyFirstRun": "No advanced search discovery yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the advanced search discovery are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "searchMedia",
    "contract": "assets",
    "purpose": "Advanced search",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P13 Venue CMS.dc.html#cms-067",
   "workshopBoard": "wireframes/WS44 Digital Asset Management DAM Board 1.dc.html#cms-067"
  },
  "apisNote": "Regenerated 9 September 2026 from Digital Asset Management DAM.pdf page 12. 0 of 0 labels bound to a contract property; 5 of 38 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "CMS-068",
  "name": "Digital Asset 360° Profile",
  "module": "Media Library",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Digital Asset Management DAM.pdf",
   "board": "1",
   "number": "8",
   "page": 13
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/media-library/digital-asset-360-profile-cms-068",
   "component": "apps/venue-management-web/src/routes/media-library/DigitalAsset360Profile.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "CMS-061"
   ],
   "exitTo": [
    "CMS-061"
   ],
   "transitions": [
    {
     "to": "CMS-061",
     "trigger": "Back to Digital Asset Management Command Center",
     "provenance": "structural — pack board 1 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Show; Display) and no metric row",
  "purpose": "Provide one authoritative record for every digital asset.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Digital Asset Management DAM.pdf, page 13 §Show"
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
       "label": "Every digital asset 360°",
       "columns": [
        "Asset ID",
        "title",
        "filename",
        "type",
        "format",
        "category",
        "owner",
        "tenant",
        "venue",
        "upload date",
        "last modified",
        "file size",
        "Campaign",
        "Event",
        "Attraction",
        "Language",
        "Tags",
        "Keywords"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Digital Asset Management DAM.pdf, page 13 §Show"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected digital asset 360°",
       "bindsTo": null,
       "columns": [
        "Asset ID",
        "title",
        "filename",
        "type",
        "format",
        "category",
        "owner",
        "tenant",
        "venue",
        "upload date",
        "last modified",
        "file size",
        "Campaign",
        "Event",
        "Attraction",
        "Language",
        "Tags",
        "Keywords"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Preview”, “JPEG”, “Board Boundaries”.",
       "provenance": "pack Digital Asset Management DAM.pdf, page 13 §Show"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The digital asset 360° list.",
   "error": "Could not load. Names which read failed and leaves the digital asset 360° untouched.",
   "emptyFirstRun": "No digital asset 360° yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the digital asset 360° are still there. The pack's own statuses are 🟢 Active — the state names which is selected.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getMediaAsset",
    "contract": "assets",
    "purpose": "The asset, in full",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "listMediaAssetVersions",
    "contract": "assets",
    "purpose": "Its revisions",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "getMediaDistribution",
    "contract": "assets",
    "purpose": "Where it is used",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "entryState": {
   "preloaded": [
    "Asset ID",
    "title",
    "filename",
    "type",
    "format",
    "category"
   ],
   "params": [
    {
     "name": "assetId",
     "from": "navigation"
    },
    {
     "name": "mediaId",
     "from": "navigation"
    }
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P13 Venue CMS.dc.html#cms-068",
   "workshopBoard": "wireframes/WS44 Digital Asset Management DAM Board 1.dc.html#cms-068"
  },
  "apisNote": "Regenerated 9 September 2026 from Digital Asset Management DAM.pdf page 13. 0 of 18 labels bound to a contract property; 19 of 31 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "CMS-069",
  "name": "Bulk Asset Management Workspace",
  "module": "Media Library",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Digital Asset Management DAM.pdf",
   "board": "1",
   "number": "9",
   "page": 15
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/media-library/bulk-asset-management-workspace-cms-069",
   "component": "apps/venue-management-web/src/routes/media-library/BulkAssetManagementWorkspace.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "CMS-061"
   ],
   "exitTo": [
    "CMS-061"
   ],
   "transitions": [
    {
     "to": "CMS-061",
     "trigger": "Back to Digital Asset Management Command Center",
     "provenance": "structural — pack board 1 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Allow enterprise users to efficiently manage large groups of digital assets.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 3 actions on this screen and the screen declares 0 operations.** Unserved: Select Individual, Select Search Results, Select Collection. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Digital Asset Management DAM.pdf, page 15 §Support"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Digital Asset Management DAM.pdf, page 15"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Digital Asset Management DAM.pdf, page 15"
   }
  ],
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Select Individual",
       "provenance": "pack Digital Asset Management DAM.pdf, page 15 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Select Search Results",
       "provenance": "pack Digital Asset Management DAM.pdf, page 15 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Select Collection",
       "provenance": "pack Digital Asset Management DAM.pdf, page 15 §Support"
      }
     ]
    },
    {
     "name": "contentBody",
     "components": []
    }
   ]
  },
  "states": {
   "loading": "The bulk asset list.",
   "error": "Could not load. Names which read failed and leaves the bulk asset untouched.",
   "emptyFirstRun": "No bulk asset yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the bulk asset are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "bulkUpdateMediaAssets",
    "contract": "assets",
    "purpose": "Retag, reclassify or archive many",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "searchMedia",
     "getMediaUsageAnalytics"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P13 Venue CMS.dc.html#cms-069",
   "workshopBoard": "wireframes/WS44 Digital Asset Management DAM Board 1.dc.html#cms-069"
  },
  "apisNote": "Regenerated 9 September 2026 from Digital Asset Management DAM.pdf page 15. 0 of 0 labels bound to a contract property; 3 of 12 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "CMS-070",
  "name": "Asset Activity, Recent Assets & Library Health",
  "module": "Media Library",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Digital Asset Management DAM.pdf",
   "board": "1",
   "number": "10",
   "page": 16
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/media-library/asset-activity-recent-assets-library-health-cms-070",
   "component": "apps/venue-management-web/src/routes/media-library/AssetActivityRecentAssetsLibraryHealth.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "CMS-061"
   ],
   "exitTo": [
    "CMS-061"
   ],
   "transitions": [
    {
     "to": "CMS-061",
     "trigger": "Back to Digital Asset Management Command Center",
     "provenance": "structural — pack board 1 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display; Show) and no metric row",
  "purpose": "Give administrators and DAM managers visibility into the health and operational quality of the asset library.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 8 actions on this screen and the screen declares 0 operations.** Unserved: Review Unclassified, Fix Metadata, Review Duplicate Candidates, Review Orphaned Assets, View Activity Log, Board 1 — Shared Configuration Requirements, Asset types, supported file formats. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Digital Asset Management DAM.pdf, page 16 §Actions"
   },
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Digital Asset Management DAM.pdf, page 16 §Display"
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
       "label": "Every asset activity recent",
       "columns": [
        "Assets Added",
        "Assets Updated",
        "Unclassified Assets",
        "Missing Metadata",
        "Orphaned Assets",
        "Used Storage",
        "Monthly Growth"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Digital Asset Management DAM.pdf, page 16 §Display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected asset activity recent",
       "bindsTo": null,
       "columns": [
        "Assets Added",
        "Assets Updated",
        "Unclassified Assets",
        "Missing Metadata",
        "Orphaned Assets",
        "Used Storage",
        "Monthly Growth"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Digital Asset Management”, “Activity Asset User Time”, “Orphaned Assets”, “DAM-IMG-008421”, “Physical File”, “Digital Asset Master Record”.",
       "provenance": "pack Digital Asset Management DAM.pdf, page 16 §Display"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Review Unclassified",
       "provenance": "pack Digital Asset Management DAM.pdf, page 16 §Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Fix Metadata",
       "provenance": "pack Digital Asset Management DAM.pdf, page 16 §Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Review Duplicate Candidates",
       "provenance": "pack Digital Asset Management DAM.pdf, page 16 §Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Review Orphaned Assets",
       "provenance": "pack Digital Asset Management DAM.pdf, page 16 §Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "View Activity Log",
       "provenance": "pack Digital Asset Management DAM.pdf, page 16 §Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Board 1 — Shared Configuration Requirements",
       "provenance": "pack Digital Asset Management DAM.pdf, page 16 §Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Asset types",
       "provenance": "pack Digital Asset Management DAM.pdf, page 16 §Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "supported file formats",
       "provenance": "pack Digital Asset Management DAM.pdf, page 16 §Actions"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The asset activity recent list.",
   "error": "Could not load. Names which read failed and leaves the asset activity recent untouched.",
   "emptyFirstRun": "No asset activity recent yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the asset activity recent are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getMediaUsageAnalytics",
    "contract": "assets",
    "purpose": "Activity and library health",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "entryState": {
   "preloaded": [
    "Assets Added",
    "Assets Updated",
    "Unclassified Assets",
    "Missing Metadata",
    "Orphaned Assets",
    "Used Storage"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P13 Venue CMS.dc.html#cms-070",
   "workshopBoard": "wireframes/WS44 Digital Asset Management DAM Board 1.dc.html#cms-070"
  },
  "apisNote": "Regenerated 9 September 2026 from Digital Asset Management DAM.pdf page 16. 0 of 7 labels bound to a contract property; 16 of 136 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
 "analyseMediaAsset": {
  "method": "POST",
  "path": "/media-assets/{assetId}/analyse",
  "contract": "assets",
  "summary": "Auto-tag, describe and classify an asset",
  "permission": "ASSET_LIBRARY_MANAGE",
  "offlineCapable": null,
  "conflictPolicy": null,
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
 "bulkUpdateMediaAssets": {
  "method": "POST",
  "path": "/media-assets/bulk",
  "contract": "assets",
  "summary": "Retag, reclassify, move or archive many assets at once",
  "permission": "ASSET_LIBRARY_MANAGE",
  "offlineCapable": null,
  "conflictPolicy": null,
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
 "getMediaDistribution": {
  "method": "GET",
  "path": "/media-distribution",
  "contract": "assets",
  "summary": "Where an asset is used and how it is delivered",
  "permission": "ASSET_LIBRARY_VIEW",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "assetId",
    "in": "query",
    "required": true
   }
  ],
  "requestBody": null,
  "responds": "MediaDistribution"
 },
 "getMediaTaxonomy": {
  "method": "GET",
  "path": "/media-taxonomy",
  "contract": "assets",
  "summary": "The categories, metadata fields and controlled vocabularies",
  "permission": "ASSET_LIBRARY_VIEW",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "tenant",
  "parameters": [],
  "requestBody": null,
  "responds": "MediaTaxonomy"
 },
 "getMediaUsageAnalytics": {
  "method": "GET",
  "path": "/media-usage",
  "contract": "assets",
  "summary": "Downloads, views, shares and library health",
  "permission": "ASSET_LIBRARY_VIEW",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": "from",
    "in": "query",
    "required": null
   },
   {
    "name": "to",
    "in": "query",
    "required": null
   },
   {
    "name": "groupBy",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "MediaUsageRow"
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
 "listMediaAssetVersions": {
  "method": "GET",
  "path": "/media-assets/{assetId}/versions",
  "contract": "assets",
  "summary": "Every revision, and what replacing it would affect",
  "permission": "ASSET_LIBRARY_VIEW",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "MediaAssetVersion"
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
 "semanticSearch": {
  "method": "POST",
  "path": "/search",
  "contract": "ai",
  "summary": "Search meaning, not words",
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
  "responds": "SearchResult"
 },
 "setMediaAssetTags": {
  "method": "PUT",
  "path": "/media-assets/{assetId}/tags",
  "contract": "assets",
  "summary": "Tags and keywords, whoever or whatever supplied them",
  "permission": "ASSET_LIBRARY_MANAGE",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "MediaTag"
 },
 "setMediaTaxonomy": {
  "method": "PUT",
  "path": "/media-taxonomy",
  "contract": "assets",
  "summary": "Define categories, fields and keyword vocabularies",
  "permission": "ASSET_LIBRARY_MANAGE",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "MediaTaxonomy",
  "responds": "MediaTaxonomy"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
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
 "MediaAssetVersion": {
  "type": "object",
  "x-ticvai-persistence": "assets.asset_version",
  "description": "Boards 2.6 and 2.7. **Usage impact belongs to the version read**, because replacing a logo is routine or an incident depending on where it appears.\n",
  "properties": {
   "assetId": {
    "type": "string",
    "format": "uuid"
   },
   "version": {
    "type": "integer"
   },
   "fileName": {
    "type": "string"
   },
   "sizeBytes": {
    "type": "integer"
   },
   "checksum": {
    "type": "string",
    "nullable": true
   },
   "createdBy": {
    "type": "string",
    "format": "uuid"
   },
   "createdAt": {
    "type": "string",
    "format": "date-time"
   },
   "note": {
    "type": "string",
    "nullable": true
   },
   "isCurrent": {
    "type": "boolean"
   },
   "usageImpact": {
    "type": "array",
    "readOnly": true,
    "items": {
     "type": "object",
     "properties": {
      "surface": {
       "type": "string",
       "enum": [
        "campaign",
        "journey",
        "ticketTemplate",
        "screen",
        "publishedPage",
        "product",
        "signage"
       ]
      },
      "referenceId": {
       "type": "string",
       "format": "uuid"
      },
      "label": {
       "type": "string"
      },
      "live": {
       "type": "boolean"
      }
     }
    }
   },
   "scopePath": {
    "type": "string"
   }
  }
 },
 "MediaDistribution": {
  "type": "object",
  "description": "Boards 4.2 and 4.5. **The usage map that makes replacement safe.**",
  "properties": {
   "assetId": {
    "type": "string",
    "format": "uuid"
   },
   "deliveryUrls": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "channel": {
       "type": "string"
      },
      "rendition": {
       "type": "string"
      },
      "url": {
       "type": "string"
      },
      "cdn": {
       "type": "string",
       "nullable": true
      }
     }
    }
   },
   "usedBy": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "surface": {
       "type": "string"
      },
      "referenceId": {
       "type": "string",
       "format": "uuid"
      },
      "label": {
       "type": "string"
      },
      "live": {
       "type": "boolean"
      }
     }
    }
   },
   "lastDeliveredAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
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
 "MediaTag": {
  "type": "object",
  "x-ticvai-persistence": "assets.tag",
  "description": "Board 2.2. **A tag carries its origin and confidence**, so machine labels can be filtered without being deleted.\n",
  "required": [
   "value"
  ],
  "properties": {
   "value": {
    "type": "string"
   },
   "vocabulary": {
    "type": "string",
    "nullable": true
   },
   "source": {
    "type": "string",
    "enum": [
     "human",
     "autoTag",
     "import",
     "inherited"
    ],
    "default": "human"
   },
   "confidence": {
    "type": "number",
    "nullable": true
   },
   "accepted": {
    "type": "boolean",
    "default": true,
    "description": "A proposed auto-tag below the promotion threshold sits here as false."
   },
   "addedBy": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "addedAt": {
    "type": "string",
    "format": "date-time"
   },
   "scopePath": {
    "type": "string"
   }
  }
 },
 "MediaTaxonomy": {
  "type": "object",
  "x-ticvai-persistence": "assets.taxonomy",
  "description": "Boards 1.5 and 1.6. **Metadata fields are per asset type**, because an image has dimensions and a contract has an expiry.\n",
  "properties": {
   "categories": {
    "type": "array",
    "items": {
     "type": "object",
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
      "parentCategoryId": {
       "type": "string",
       "format": "uuid",
       "nullable": true
      },
      "applicableAssetTypes": {
       "type": "array",
       "items": {
        "type": "string"
       }
      }
     }
    }
   },
   "fields": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "code": {
       "type": "string"
      },
      "label": {
       "type": "string"
      },
      "dataType": {
       "type": "string"
      },
      "applicableAssetTypes": {
       "type": "array",
       "items": {
        "type": "string"
       }
      },
      "mandatory": {
       "type": "boolean"
      },
      "allowedValues": {
       "type": "array",
       "items": {
        "type": "string"
       }
      }
     }
    }
   },
   "keywordVocabularies": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "code": {
       "type": "string"
      },
      "terms": {
       "type": "array",
       "items": {
        "type": "string"
       }
      },
      "closed": {
       "type": "boolean",
       "default": false,
       "description": "**A closed vocabulary refuses terms not in the list.** Open vocabularies are how a library ends up with `logo`, `logos`, `Logo` and `brand-logo`.\n"
      }
     }
    }
   },
   "scopePath": {
    "type": "string"
   }
  }
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
 "MediaUsageRow": {
  "type": "object",
  "description": "Boards 1.10 and 4.9. **Assets never used is the number that justifies the library.**",
  "properties": {
   "key": {
    "type": "string"
   },
   "label": {
    "type": "string"
   },
   "assetCount": {
    "type": "integer"
   },
   "storageBytes": {
    "type": "integer"
   },
   "downloads": {
    "type": "integer"
   },
   "views": {
    "type": "integer"
   },
   "shares": {
    "type": "integer"
   },
   "neverUsedCount": {
    "type": "integer"
   },
   "unclassifiedCount": {
    "type": "integer"
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
 "SearchResult": {
  "type": "object",
  "x-ticvai-persistence": "none — computed",
  "properties": {
   "kind": {
    "type": "string"
   },
   "id": {
    "type": "string"
   },
   "title": {
    "type": "string"
   },
   "excerpt": {
    "type": "string"
   },
   "relevance": {
    "type": "number"
   },
   "collectionId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "scopePath": {
    "type": "string"
   },
   "assetId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "For kind `media`, the asset (29 September, build; 23.1.6)."
   },
   "mediaType": {
    "type": "string",
    "nullable": true,
    "enum": [
     "image",
     "video",
     "audio",
     "document"
    ]
   },
   "matchedOn": {
    "type": "string",
    "nullable": true,
    "enum": [
     "title",
     "description",
     "tags",
     "aiDescription"
    ],
    "description": "Which text the match came from, so a wrong hit can be traced to a wrong tag."
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
 }
}
```
