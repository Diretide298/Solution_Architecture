# WS74 — Digital Asset Management DAM board 1

**10 screens · 0 operations · 0 schemas · 0 permissions**

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

- **Every control that can be refused must be gated.** 0 permissions apply here:
  ``. A control nobody can use must say so,
  not sit enabled and fail.
- **0 of these operations work offline**
  
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `CMS-061` | Digital Asset Management Command Center | listDetail | 0 | 0 | — |
| `CMS-062` | Central Digital Asset Library | listDetail | 0 | 0 | — |
| `CMS-063` | Upload & Asset Ingestion Workspace | listDetail | 0 | 0 | — |
| `CMS-064` | Folder, Collection & Workspace Management | listDetail | 0 | 0 | — |
| `CMS-065` | Metadata & Taxonomy Management | listDetail | 0 | 0 | — |
| `CMS-066` | Tags, Keywords & Classification | configEditor | 0 | 0 | — |
| `CMS-067` | Advanced Search & Discovery | listDetail | 0 | 0 | — |
| `CMS-068` | Digital Asset 360° Profile | listDetail | 0 | 0 | — |
| `CMS-069` | Bulk Asset Management Workspace | listDetail | 0 | 0 | — |
| `CMS-070` | Asset Activity, Recent Assets & Library Health | listDetail | 0 | 0 | — |

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
  "apis": [],
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
   "board": "wireframes/P13 Venue CMS.dc.html#cms-061"
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
  "apis": [],
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
   "board": "wireframes/P13 Venue CMS.dc.html#cms-062"
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
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P13 Venue CMS.dc.html#cms-063"
  },
  "apisNote": "Regenerated 9 September 2026 from Digital Asset Management DAM.pdf page 6. 0 of 0 labels bound to a contract property; 3 of 31 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P13 Venue CMS.dc.html#cms-064"
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
    "why": "**The pack names 7 actions on this screen and the screen declares 0 operations.** Unserved: Asset Name, Asset Type, Campaign, Event, Attraction, Owner, Upload Date. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
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
       "label": "Upload Date",
       "provenance": "pack Digital Asset Management DAM.pdf, page 9 §Support"
      }
     ]
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
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P13 Venue CMS.dc.html#cms-065"
  },
  "apisNote": "Regenerated 9 September 2026 from Digital Asset Management DAM.pdf page 9. 0 of 0 labels bound to a contract property; 7 of 51 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P13 Venue CMS.dc.html#cms-066"
  },
  "apisNote": "Regenerated 9 September 2026 from Digital Asset Management DAM.pdf page 11. 0 of 0 labels bound to a contract property; 4 of 10 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
    "why": "**The pack names 4 actions on this screen and the screen declares 0 operations.** Unserved: Asset Type, File Format, Collection, Owner. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
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
       "label": "Collection",
       "provenance": "pack Digital Asset Management DAM.pdf, page 12 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Owner",
       "provenance": "pack Digital Asset Management DAM.pdf, page 12 §Support"
      }
     ]
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
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P13 Venue CMS.dc.html#cms-067"
  },
  "apisNote": "Regenerated 9 September 2026 from Digital Asset Management DAM.pdf page 12. 0 of 0 labels bound to a contract property; 4 of 38 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "apis": [],
  "entryState": {
   "preloaded": [
    "Asset ID",
    "title",
    "filename",
    "type",
    "format",
    "category"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P13 Venue CMS.dc.html#cms-068"
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
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P13 Venue CMS.dc.html#cms-069"
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
  "apis": [],
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
   "board": "wireframes/P13 Venue CMS.dc.html#cms-070"
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
{}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{}
```
