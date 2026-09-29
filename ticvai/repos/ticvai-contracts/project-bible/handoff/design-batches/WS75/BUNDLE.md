# WS75 — Digital Asset Management DAM board 2

**10 screens · 12 operations · 12 schemas · 3 permissions**

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
  `ASSET_LIBRARY_MANAGE, ASSET_LIBRARY_VIEW, ASSET_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `CMS-071` | AI Asset Intelligence Command Center | listDetail | 2 | 0 | — |
| `CMS-072` | AI Auto-Tagging & Content Understanding | listDetail | 2 | 1 | — |
| `CMS-073` | Semantic & Natural-Language Asset Search | listDetail | 1 | 0 | — |
| `CMS-074` | Visual Similarity & Related Asset Discovery | listDetail | 1 | 0 | — |
| `CMS-075` | Duplicate & Near-Duplicate Management | listDetail | 3 | 2 | — |
| `CMS-076` | Asset Version Control & Revision History | listDetail | 2 | 0 | — |
| `CMS-077` | Version Comparison & Replacement Impact | listDetail | 1 | 0 | — |
| `CMS-078` | Transformation & Rendition Management | configEditor | 2 | 0 | — |
| `CMS-079` | Rendition Processing & Delivery Readiness | listDetail | 1 | 1 | — |
| `CMS-080` | AI Quality, Intelligence Review & Recommendations | listDetail | 1 | 1 | — |

## Thin screens in this batch

**CMS-073, CMS-076, CMS-077 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "CMS-071",
  "name": "AI Asset Intelligence Command Center",
  "module": "Media Library",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Digital Asset Management DAM.pdf",
   "board": "2",
   "number": "1",
   "page": 25
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/media-library/ai-asset-intelligence-command-center-cms-071",
   "component": "apps/venue-management-web/src/routes/media-library/AiAssetIntelligenceCommandCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "CMS-001"
   ],
   "exitTo": [
    "CMS-001",
    "CMS-072",
    "CMS-073",
    "CMS-074",
    "CMS-075",
    "CMS-076",
    "CMS-077",
    "CMS-078",
    "CMS-079",
    "CMS-080"
   ],
   "transitions": [
    {
     "to": "CMS-001",
     "trigger": "Back to Tenant Workspace",
     "provenance": "structural — pack board 2 wiring, 11 September 2026",
     "back": true
    },
    {
     "to": "CMS-072",
     "trigger": "AI Auto-Tagging & Content Understanding",
     "provenance": "structural — pack board 2 wiring, 11 September 2026"
    },
    {
     "to": "CMS-073",
     "trigger": "Semantic & Natural-Language Asset Search",
     "provenance": "structural — pack board 2 wiring, 11 September 2026"
    },
    {
     "to": "CMS-074",
     "trigger": "Visual Similarity & Related Asset Discovery",
     "provenance": "structural — pack board 2 wiring, 11 September 2026"
    },
    {
     "to": "CMS-075",
     "trigger": "Duplicate & Near-Duplicate Management",
     "provenance": "structural — pack board 2 wiring, 11 September 2026"
    },
    {
     "to": "CMS-076",
     "trigger": "Asset Version Control & Revision History",
     "provenance": "structural — pack board 2 wiring, 11 September 2026"
    },
    {
     "to": "CMS-077",
     "trigger": "Version Comparison & Replacement Impact",
     "provenance": "structural — pack board 2 wiring, 11 September 2026"
    },
    {
     "to": "CMS-078",
     "trigger": "Transformation & Rendition Management",
     "provenance": "structural — pack board 2 wiring, 11 September 2026"
    },
    {
     "to": "CMS-079",
     "trigger": "Rendition Processing & Delivery Readiness",
     "provenance": "structural — pack board 2 wiring, 11 September 2026"
    },
    {
     "to": "CMS-080",
     "trigger": "AI Quality, Intelligence Review & Recommendations",
     "provenance": "structural — pack board 2 wiring, 11 September 2026"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display; Show) and no metric row",
  "purpose": "Provide DAM administrators and content teams with an overview of AI processing, version activity, duplicate detection, rendition generation, and asset-quality issues.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 5 actions on this screen and the screen declares 0 operations.** Unserved: Review AI Results, Duplicate Review, Version Activity, Rendition Queue, Processing Failures. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Digital Asset Management DAM.pdf, page 25 §Quick Actions"
   },
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Digital Asset Management DAM.pdf, page 25 §Display"
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
       "label": "Every asset intelligence",
       "columns": [
        "AI-Processed Assets",
        "Pending AI Processing",
        "AI Tags Generated",
        "Duplicate Candidates",
        "Version Updates",
        "Renditions Generated",
        "Processing Failures",
        "Assets Requiring Review",
        "Processed",
        "Queued",
        "Processing",
        "Review Required",
        "Failed",
        "95–100%",
        "80–94%",
        "60–79%",
        "Below Threshold"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Digital Asset Management DAM.pdf, page 25 §Display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected asset intelligence",
       "bindsTo": null,
       "columns": [
        "AI-Processed Assets",
        "Pending AI Processing",
        "AI Tags Generated",
        "Duplicate Candidates",
        "Version Updates",
        "Renditions Generated",
        "Processing Failures",
        "Assets Requiring Review",
        "Processed",
        "Queued",
        "Processing",
        "Review Required",
        "Failed",
        "95–100%",
        "80–94%",
        "60–79%",
        "Below Threshold"
       ],
       "notes": null,
       "provenance": "pack Digital Asset Management DAM.pdf, page 25 §Display"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Review AI Results",
       "provenance": "pack Digital Asset Management DAM.pdf, page 25 §Quick Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Duplicate Review",
       "provenance": "pack Digital Asset Management DAM.pdf, page 25 §Quick Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Version Activity",
       "provenance": "pack Digital Asset Management DAM.pdf, page 25 §Quick Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Rendition Queue",
       "provenance": "pack Digital Asset Management DAM.pdf, page 25 §Quick Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Processing Failures",
       "provenance": "pack Digital Asset Management DAM.pdf, page 25 §Quick Actions"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The asset intelligence list.",
   "error": "Could not load. Names which read failed and leaves the asset intelligence untouched.",
   "emptyFirstRun": "No asset intelligence yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the asset intelligence are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listAssets",
    "contract": "maintenance",
    "purpose": "List assets",
    "trigger": "onLoad"
   },
   {
    "operationId": "getMediaUsageAnalytics",
    "contract": "assets",
    "purpose": "What the library looks like to AI",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "entryState": {
   "preloaded": [
    "AI-Processed Assets",
    "Pending AI Processing",
    "AI Tags Generated",
    "Duplicate Candidates",
    "Version Updates",
    "Renditions Generated"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P13 Venue CMS.dc.html#cms-071",
   "workshopBoard": "wireframes/WS45 Digital Asset Management DAM Board 2.dc.html#cms-071"
  },
  "apisNote": "Regenerated 9 September 2026 from Digital Asset Management DAM.pdf page 25. 0 of 17 labels bound to a contract property; 22 of 28 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "CMS-072",
  "name": "AI Auto-Tagging & Content Understanding",
  "module": "Media Library",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Digital Asset Management DAM.pdf",
   "board": "2",
   "number": "2",
   "page": 27
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/media-library/ai-auto-tagging-content-understanding-cms-072",
   "component": "apps/venue-management-web/src/routes/media-library/AiAutoTaggingContentUnderstanding.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "CMS-071"
   ],
   "exitTo": [
    "CMS-071"
   ],
   "transitions": [
    {
     "to": "CMS-071",
     "trigger": "Back to AI Asset Intelligence Command Center",
     "provenance": "structural — pack board 2 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Automatically analyze uploaded assets and generate useful descriptive metadata.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 4 actions on this screen and the screen declares 0 operations.** Unserved: Accept, Reject, Edit, Accept All Above Threshold. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Digital Asset Management DAM.pdf, page 27 §Actions"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Digital Asset Management DAM.pdf, page 27"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Digital Asset Management DAM.pdf, page 27"
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
       "label": "Accept",
       "provenance": "pack Digital Asset Management DAM.pdf, page 27 §Actions"
      },
      {
       "kind": "destructiveButton",
       "label": "Reject",
       "provenance": "pack Digital Asset Management DAM.pdf, page 27 §Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Edit",
       "provenance": "pack Digital Asset Management DAM.pdf, page 27 §Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Accept All Above Threshold",
       "provenance": "pack Digital Asset Management DAM.pdf, page 27 §Actions"
      }
     ]
    },
    {
     "name": "contentBody",
     "components": []
    }
   ]
  },
  "overlays": [
   {
    "id": "confirmReject",
    "component": "confirmDialog",
    "trigger": "Reject",
    "body": "**Reject on a auto-tagging content understanding is not reversible from this screen.** Names what it affects and what it leaves alone. The pack requires the decision to reach the audit trail, so the dialog states that it is recorded.",
    "provenance": "pack Digital Asset Management DAM.pdf, page 27 §Actions"
   }
  ],
  "states": {
   "loading": "The auto-tagging content understanding list.",
   "error": "Could not load. Names which read failed and leaves the auto-tagging content understanding untouched.",
   "emptyFirstRun": "No auto-tagging content understanding yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the auto-tagging content understanding are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "analyseMediaAsset",
    "contract": "assets",
    "purpose": "Auto-tag and describe",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "getMediaAsset"
    ]
   },
   {
    "operationId": "setMediaAssetTags",
    "contract": "assets",
    "purpose": "Promote the proposals",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "searchMedia",
     "getMediaAsset"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P13 Venue CMS.dc.html#cms-072",
   "workshopBoard": "wireframes/WS45 Digital Asset Management DAM Board 2.dc.html#cms-072"
  },
  "apisNote": "Regenerated 9 September 2026 from Digital Asset Management DAM.pdf page 27. 0 of 0 labels bound to a contract property; 4 of 17 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "CMS-073",
  "name": "Semantic & Natural-Language Asset Search",
  "module": "Media Library",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Digital Asset Management DAM.pdf",
   "board": "2",
   "number": "3",
   "page": 28
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/media-library/semantic-natural-language-asset-search-cms-073",
   "component": "apps/venue-management-web/src/routes/media-library/SemanticNaturalLanguageAssetSearch.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "CMS-071"
   ],
   "exitTo": [
    "CMS-071"
   ],
   "transitions": [
    {
     "to": "CMS-071",
     "trigger": "Back to AI Asset Intelligence Command Center",
     "provenance": "structural — pack board 2 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Each result should show) and no metric row",
  "purpose": "Allow users to search based on meaning rather than exact filenames or tags. Board 1 provided structured search.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Digital Asset Management DAM.pdf, page 28 §Each result should show"
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
       "label": "Every semantic natural-language asset",
       "columns": [
        "Thumbnail",
        "asset",
        "relevance score",
        "AI tags",
        "matching reason",
        "format",
        "dimensions"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Digital Asset Management DAM.pdf, page 28 §Each result should show"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected semantic natural-language asset",
       "bindsTo": null,
       "columns": [
        "Thumbnail",
        "asset",
        "relevance score",
        "AI tags",
        "matching reason",
        "format",
        "dimensions"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Digital Asset Management”, “Security”.",
       "provenance": "pack Digital Asset Management DAM.pdf, page 28 §Each result should show"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The semantic natural-language asset list.",
   "error": "Could not load. Names which read failed and leaves the semantic natural-language asset untouched.",
   "emptyFirstRun": "No semantic natural-language asset yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the semantic natural-language asset are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "searchMedia",
    "contract": "assets",
    "purpose": "Semantic search",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "entryState": {
   "preloaded": [
    "Thumbnail",
    "asset",
    "relevance score",
    "AI tags",
    "matching reason",
    "format"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P13 Venue CMS.dc.html#cms-073",
   "workshopBoard": "wireframes/WS45 Digital Asset Management DAM Board 2.dc.html#cms-073"
  },
  "apisNote": "Regenerated 9 September 2026 from Digital Asset Management DAM.pdf page 28. 0 of 7 labels bound to a contract property; 7 of 24 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "CMS-074",
  "name": "Visual Similarity & Related Asset Discovery",
  "module": "Media Library",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Digital Asset Management DAM.pdf",
   "board": "2",
   "number": "4",
   "page": 29
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/media-library/visual-similarity-related-asset-discovery-cms-074",
   "component": "apps/venue-management-web/src/routes/media-library/VisualSimilarityRelatedAssetDiscovery.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "CMS-071"
   ],
   "exitTo": [
    "CMS-071"
   ],
   "transitions": [
    {
     "to": "CMS-071",
     "trigger": "Back to AI Asset Intelligence Command Center",
     "provenance": "structural — pack board 2 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Allow users to find visually related or similar media.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Digital Asset Management DAM.pdf, page 29"
   }
  ],
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "filters",
     "slot": "filters",
     "components": [
      {
       "kind": "searchField",
       "label": "Source asset",
       "operation": "findSimilarMediaAssets",
       "notes": "Sends `?assetId=` (required).",
       "provenance": "contract assets.yaml GET /media-assets/similar"
      },
      {
       "kind": "numberField",
       "label": "Minimum similarity",
       "operation": "findSimilarMediaAssets",
       "notes": "Sends `?minSimilarity=`.",
       "provenance": "contract assets.yaml GET /media-assets/similar"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Similar assets",
       "bindsTo": "MediaSimilarity",
       "columns": [
        "MediaSimilarity.assetId",
        "MediaSimilarity.similarity",
        "MediaSimilarity.relation",
        "MediaSimilarity.differingFields",
        "Thumbnail"
       ],
       "operation": "findSimilarMediaAssets",
       "notes": "`relation` keeps similar, duplicate candidate and variant apart, as the pack requires; the pack's Version and Rendition are not among its values.",
       "provenance": "pack Digital Asset Management DAM.pdf, page 29"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected match",
       "bindsTo": "MediaSimilarity",
       "columns": [
        "MediaSimilarity.assetId",
        "MediaSimilarity.similarity",
        "MediaSimilarity.relation",
        "MediaSimilarity.differingFields",
        "Similarity factors",
        "Matched because"
       ],
       "operation": "findSimilarMediaAssets",
       "notes": "The pack's Explain Match (\"94% - Family, Water Attraction, Outdoor, Daytime\").",
       "provenance": "pack Digital Asset Management DAM.pdf, page 29"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The visual similarity related list.",
   "error": "Could not load. Names which read failed and leaves the visual similarity related untouched.",
   "emptyFirstRun": "No visual similarity related yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the visual similarity related are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "findSimilarMediaAssets",
    "contract": "assets",
    "purpose": "Visually similar and related",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P13 Venue CMS.dc.html#cms-074",
   "workshopBoard": "wireframes/WS45 Digital Asset Management DAM Board 2.dc.html#cms-074"
  },
  "apisNote": "Regenerated 9 September 2026 from Digital Asset Management DAM.pdf page 29. 0 of 0 labels bound to a contract property; 0 of 21 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here. **Layout drafted 29 September (VM close-out)** from pack Digital Asset Management DAM.pdf p.29; contract assets.yaml GET /media-assets/similar. Pack labels with no schema field yet (shown as plain labels): Thumbnail, Similarity factors (composition, objects, scene, colours, subject), Matched-because explanation, Relation values: version, rendition.",
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
  "id": "CMS-075",
  "name": "Duplicate & Near-Duplicate Management",
  "module": "Media Library",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Digital Asset Management DAM.pdf",
   "board": "2",
   "number": "5",
   "page": 30
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/media-library/duplicate-near-duplicate-management-cms-075",
   "component": "apps/venue-management-web/src/routes/media-library/DuplicateNearDuplicateManagement.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "CMS-071"
   ],
   "exitTo": [
    "CMS-071"
   ],
   "transitions": [
    {
     "to": "CMS-071",
     "trigger": "Back to AI Asset Intelligence Command Center",
     "provenance": "structural — pack board 2 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "notes": "**Archive and quarantine are reversible; deletion is the only end of an asset's life (decided 28 September, audit STATE-MEDIA).** Archive Duplicate archives the copy (`updateMediaAsset`, `status: archived`) and can be undone with Restore Archived Copy; Delete Duplicate (`deleteMediaAsset`) removes it for good.",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Prevent the DAM from becoming filled with unnecessary copies of identical or nearly identical content.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 7 actions on this screen and the screen declares 0 operations.** Unserved: Exact Duplicate, Near Duplicate, Keep Both, Mark Related, Create Version Relationship, Replace Duplicate, Archive Duplicate. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Digital Asset Management DAM.pdf, page 30 §Support"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Digital Asset Management DAM.pdf, page 30"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Digital Asset Management DAM.pdf, page 30"
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
       "label": "Exact Duplicate",
       "provenance": "pack Digital Asset Management DAM.pdf, page 30 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Near Duplicate",
       "provenance": "pack Digital Asset Management DAM.pdf, page 30 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Keep Both",
       "provenance": "pack Digital Asset Management DAM.pdf, page 30 §Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Mark Related",
       "provenance": "pack Digital Asset Management DAM.pdf, page 30 §Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Create Version Relationship",
       "provenance": "pack Digital Asset Management DAM.pdf, page 30 §Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Replace Duplicate",
       "provenance": "pack Digital Asset Management DAM.pdf, page 30 §Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Archive Duplicate",
       "operation": "updateMediaAsset",
       "notes": "Sends `status: archived`; reversible — an archived copy can be restored (decided 28 September, audit STATE-MEDIA).",
       "provenance": "pack Digital Asset Management DAM.pdf, page 30 §Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Restore Archived Copy",
       "operation": "updateMediaAsset",
       "notes": "Shown on an archived copy. Sends `status: ready` (decided 28 September, audit STATE-MEDIA).",
       "provenance": "contract assets.yaml PATCH /media/{mediaId}"
      },
      {
       "kind": "destructiveButton",
       "label": "Delete Duplicate",
       "operation": "deleteMediaAsset",
       "notes": "The only end of a copy's life; refused while the copy is referenced (decided 28 September, audit STATE-MEDIA).",
       "provenance": "contract assets.yaml DELETE /media/{mediaId}"
      }
     ]
    },
    {
     "name": "contentBody",
     "components": []
    }
   ]
  },
  "overlays": [
   {
    "id": "confirmArchiveDuplicate",
    "component": "confirmDialog",
    "trigger": "Archive Duplicate",
    "body": "**Archive Duplicate is reversible** (decided 28 September, audit STATE-MEDIA): the copy leaves use and can be restored to `ready`; it is refused while the copy is referenced. Names what it affects and what it leaves alone. The pack requires the decision to reach the audit trail, so the dialog states that it is recorded.",
    "confirm": {
     "label": "Archive",
     "operation": "updateMediaAsset"
    },
    "provenance": "pack Digital Asset Management DAM.pdf, page 30 §Actions"
   },
   {
    "id": "confirmDeleteDuplicate",
    "component": "confirmDialog",
    "trigger": "Delete Duplicate",
    "body": "**Deletes the copy for good** — deletion is the only end of an asset's life (decided 28 September, audit STATE-MEDIA). Names the copy and the asset it duplicates, lists every reference when refused as in use, and offers Archive instead where the copy may be wanted again.",
    "confirm": {
     "label": "Delete",
     "operation": "deleteMediaAsset"
    },
    "provenance": "contract assets.yaml DELETE /media/{mediaId}"
   }
  ],
  "states": {
   "loading": "The duplicate near-duplicate list.",
   "error": "Could not load. Names which read failed and leaves the duplicate near-duplicate untouched.",
   "emptyFirstRun": "No duplicate near-duplicate yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the duplicate near-duplicate are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "findSimilarMediaAssets",
    "contract": "assets",
    "purpose": "Duplicates above the threshold",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "deleteMediaAsset",
    "contract": "assets",
    "purpose": "Delete the copy — the only end of an asset's life (audit STATE-MEDIA)",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "searchMedia"
    ]
   },
   {
    "operationId": "updateMediaAsset",
    "contract": "assets",
    "purpose": "Archive a copy, or restore an archived one (decided 28 September, audit STATE-MEDIA)",
    "trigger": "onAction",
    "invalidates": [
     "findSimilarMediaAssets"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P13 Venue CMS.dc.html#cms-075",
   "workshopBoard": "wireframes/WS45 Digital Asset Management DAM Board 2.dc.html#cms-075"
  },
  "apisNote": "Regenerated 9 September 2026 from Digital Asset Management DAM.pdf page 30. 0 of 0 labels bound to a contract property; 7 of 23 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "mediaId",
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
  "id": "CMS-076",
  "name": "Asset Version Control & Revision History",
  "module": "Media Library",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Digital Asset Management DAM.pdf",
   "board": "2",
   "number": "6",
   "page": 31
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/media-library/asset-version-control-revision-history-cms-076",
   "component": "apps/venue-management-web/src/routes/media-library/AssetVersionControlRevisionHistory.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "CMS-071"
   ],
   "exitTo": [
    "CMS-071"
   ],
   "transitions": [
    {
     "to": "CMS-071",
     "trigger": "Back to AI Asset Intelligence Command Center",
     "provenance": "structural — pack board 2 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Maintain controlled versions of the same logical digital asset without creating unrelated master records.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Digital Asset Management DAM.pdf, page 31"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Digital Asset Management DAM.pdf, page 31"
   }
  ],
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "components": [
      {
       "kind": "dataTable",
       "derived": true,
       "impliedBy": "listMediaAssetVersions",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      },
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "replaceMediaAsset",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "replaceMediaAsset"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The asset version revision list.",
   "error": "Could not load. Names which read failed and leaves the asset version revision untouched.",
   "emptyFirstRun": "No asset version revision yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the asset version revision are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listMediaAssetVersions",
    "contract": "assets",
    "purpose": "Revision history",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "replaceMediaAsset",
    "contract": "assets",
    "purpose": "Replace the current version",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listMediaAssetVersions",
     "getMediaDistribution"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P13 Venue CMS.dc.html#cms-076",
   "workshopBoard": "wireframes/WS45 Digital Asset Management DAM Board 2.dc.html#cms-076"
  },
  "apisNote": "Regenerated 9 September 2026 from Digital Asset Management DAM.pdf page 31. 0 of 0 labels bound to a contract property; 0 of 15 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
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
  "id": "CMS-077",
  "name": "Version Comparison & Replacement Impact",
  "module": "Media Library",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Digital Asset Management DAM.pdf",
   "board": "2",
   "number": "7",
   "page": 32
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/media-library/version-comparison-replacement-impact-cms-077",
   "component": "apps/venue-management-web/src/routes/media-library/VersionComparisonReplacementImpact.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "CMS-071"
   ],
   "exitTo": [
    "CMS-071"
   ],
   "transitions": [
    {
     "to": "CMS-071",
     "trigger": "Back to AI Asset Intelligence Command Center",
     "provenance": "structural — pack board 2 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Allow users to compare versions and understand the consequences of making a new version current.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Digital Asset Management DAM.pdf, page 32"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Digital Asset Management DAM.pdf, page 32"
   }
  ],
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "components": [
      {
       "kind": "dataTable",
       "derived": true,
       "impliedBy": "listMediaAssetVersions",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The version comparison replacement list.",
   "error": "Could not load. Names which read failed and leaves the version comparison replacement untouched.",
   "emptyFirstRun": "No version comparison replacement yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the version comparison replacement are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listMediaAssetVersions",
    "contract": "assets",
    "purpose": "Two versions, and what replacing breaks",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P13 Venue CMS.dc.html#cms-077",
   "workshopBoard": "wireframes/WS45 Digital Asset Management DAM Board 2.dc.html#cms-077"
  },
  "apisNote": "Regenerated 9 September 2026 from Digital Asset Management DAM.pdf page 32. 0 of 0 labels bound to a contract property; 0 of 17 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "CMS-078",
  "name": "Transformation & Rendition Management",
  "module": "Media Library",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Digital Asset Management DAM.pdf",
   "board": "2",
   "number": "8",
   "page": 33
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/media-library/transformation-rendition-management-cms-078",
   "component": "apps/venue-management-web/src/routes/media-library/TransformationRenditionManagement.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "CMS-071"
   ],
   "exitTo": [
    "CMS-071"
   ],
   "transitions": [
    {
     "to": "CMS-071",
     "trigger": "Back to AI Asset Intelligence Command Center",
     "provenance": "structural — pack board 2 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Administrators should configure) and no display directory — it is settings, not a population",
  "purpose": "Generate channel-appropriate media from a master asset without forcing users to manually upload many independent copies.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Rendition Presets",
       "provenance": "pack Digital Asset Management DAM.pdf, page 33 §Administrators should configure"
      },
      {
       "kind": "dataTable",
       "derived": true,
       "impliedBy": "listMediaRenditions",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      },
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "requestMediaRendition",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "requestMediaRendition"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The transformation rendition configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the transformation rendition untouched.",
   "emptyFirstRun": "No transformation rendition configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [
   {
    "operationId": "listMediaRenditions",
    "contract": "assets",
    "purpose": "The derived sizes",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "requestMediaRendition",
    "contract": "assets",
    "purpose": "Generate one",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listMediaRenditions"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P13 Venue CMS.dc.html#cms-078",
   "workshopBoard": "wireframes/WS45 Digital Asset Management DAM Board 2.dc.html#cms-078"
  },
  "apisNote": "Regenerated 9 September 2026 from Digital Asset Management DAM.pdf page 33. 0 of 0 labels bound to a contract property; 1 of 22 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "CMS-079",
  "name": "Rendition Processing & Delivery Readiness",
  "module": "Media Library",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Digital Asset Management DAM.pdf",
   "board": "2",
   "number": "9",
   "page": 34
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/media-library/rendition-processing-delivery-readiness-cms-079",
   "component": "apps/venue-management-web/src/routes/media-library/RenditionProcessingDeliveryReadiness.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "CMS-071"
   ],
   "exitTo": [
    "CMS-071"
   ],
   "transitions": [
    {
     "to": "CMS-071",
     "trigger": "Back to AI Asset Intelligence Command Center",
     "provenance": "structural — pack board 2 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Monitor media-processing jobs and ensure required formats are ready before content is distributed.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 4 actions on this screen and the screen declares 0 operations.** Unserved: Retry, Cancel, View Error, Regenerate. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Digital Asset Management DAM.pdf, page 34 §Actions"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Digital Asset Management DAM.pdf, page 34"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Digital Asset Management DAM.pdf, page 34"
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
       "label": "Retry",
       "provenance": "pack Digital Asset Management DAM.pdf, page 34 §Actions"
      },
      {
       "kind": "destructiveButton",
       "label": "Cancel",
       "provenance": "pack Digital Asset Management DAM.pdf, page 34 §Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "View Error",
       "provenance": "pack Digital Asset Management DAM.pdf, page 34 §Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Regenerate",
       "provenance": "pack Digital Asset Management DAM.pdf, page 34 §Actions"
      }
     ]
    },
    {
     "name": "contentBody",
     "components": []
    }
   ]
  },
  "overlays": [
   {
    "id": "confirmCancel",
    "component": "confirmDialog",
    "trigger": "Cancel",
    "body": "**Cancel on a rendition processing delivery is not reversible from this screen.** Names what it affects and what it leaves alone. The pack requires the decision to reach the audit trail, so the dialog states that it is recorded.",
    "provenance": "pack Digital Asset Management DAM.pdf, page 34 §Actions"
   }
  ],
  "states": {
   "loading": "The rendition processing delivery list.",
   "error": "Could not load. Names which read failed and leaves the rendition processing delivery untouched.",
   "emptyFirstRun": "No rendition processing delivery yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the rendition processing delivery are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listMediaRenditions",
    "contract": "assets",
    "purpose": "Processing state and readiness",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P13 Venue CMS.dc.html#cms-079",
   "workshopBoard": "wireframes/WS45 Digital Asset Management DAM Board 2.dc.html#cms-079"
  },
  "apisNote": "Regenerated 9 September 2026 from Digital Asset Management DAM.pdf page 34. 0 of 0 labels bound to a contract property; 4 of 17 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "CMS-080",
  "name": "AI Quality, Intelligence Review & Recommendations",
  "module": "Media Library",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Digital Asset Management DAM.pdf",
   "board": "2",
   "number": "10",
   "page": 35
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/media-library/ai-quality-intelligence-review-recommendations-cms-080",
   "component": "apps/venue-management-web/src/routes/media-library/AiQualityIntelligenceReviewRecommendations.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "CMS-071"
   ],
   "exitTo": [
    "CMS-071"
   ],
   "transitions": [
    {
     "to": "CMS-071",
     "trigger": "Back to AI Asset Intelligence Command Center",
     "provenance": "structural — pack board 2 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Track) and no metric row",
  "purpose": "Provide a governed review workspace for AI results and identify content-quality issues before assets are reused or distributed.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 12 actions on this screen and the screen declares 0 operations.** Unserved: Accept Recommendation, Reject, Review Asset, Generate Rendition, Resolve Issue, Board 2 — Shared Configuration Requirements, AI processing enabled/disabled, supported AI capabilities …. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Digital Asset Management DAM.pdf, page 35 §Actions"
   },
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Digital Asset Management DAM.pdf, page 35 §Track"
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
       "label": "Every quality intelligence review",
       "columns": [
        "Assets processed",
        "images analyzed",
        "video minutes analyzed",
        "audio minutes transcribed",
        "OCR pages",
        "embedding generation",
        "semantic searches",
        "AI requests",
        "estimated/actual AI consumption cost"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Digital Asset Management DAM.pdf, page 35 §Track"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected quality intelligence review",
       "bindsTo": null,
       "columns": [
        "Assets processed",
        "images analyzed",
        "video minutes analyzed",
        "audio minutes transcribed",
        "OCR pages",
        "embedding generation",
        "semantic searches",
        "AI requests",
        "estimated/actual AI consumption cost"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Digital Asset Management”, “Quality Score”, “Issues”, “Review Queue”, “DAM-IMG-008421”, “Versions”.",
       "provenance": "pack Digital Asset Management DAM.pdf, page 35 §Track"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Accept Recommendation",
       "provenance": "pack Digital Asset Management DAM.pdf, page 35 §Actions"
      },
      {
       "kind": "destructiveButton",
       "label": "Reject",
       "provenance": "pack Digital Asset Management DAM.pdf, page 35 §Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Review Asset",
       "provenance": "pack Digital Asset Management DAM.pdf, page 35 §Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Generate Rendition",
       "provenance": "pack Digital Asset Management DAM.pdf, page 35 §Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Resolve Issue",
       "provenance": "pack Digital Asset Management DAM.pdf, page 35 §Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Board 2 — Shared Configuration Requirements",
       "provenance": "pack Digital Asset Management DAM.pdf, page 35 §Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "AI processing enabled/disabled",
       "provenance": "pack Digital Asset Management DAM.pdf, page 35 §Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "supported AI capabilities",
       "provenance": "pack Digital Asset Management DAM.pdf, page 35 §Actions"
      }
     ]
    }
   ]
  },
  "overlays": [
   {
    "id": "confirmReject",
    "component": "confirmDialog",
    "trigger": "Reject",
    "body": "**Reject on a quality intelligence review is not reversible from this screen.** Names what it affects and what it leaves alone. The pack requires the decision to reach the audit trail, so the dialog states that it is recorded.",
    "provenance": "pack Digital Asset Management DAM.pdf, page 35 §Actions"
   }
  ],
  "states": {
   "loading": "The quality intelligence review list.",
   "error": "Could not load. Names which read failed and leaves the quality intelligence review untouched.",
   "emptyFirstRun": "No quality intelligence review yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the quality intelligence review are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getMediaUsageAnalytics",
    "contract": "assets",
    "purpose": "Quality and coverage",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "entryState": {
   "preloaded": [
    "Assets processed",
    "images analyzed",
    "video minutes analyzed",
    "audio minutes transcribed",
    "OCR pages",
    "embedding generation"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P13 Venue CMS.dc.html#cms-080",
   "workshopBoard": "wireframes/WS45 Digital Asset Management DAM Board 2.dc.html#cms-080"
  },
  "apisNote": "Regenerated 9 September 2026 from Digital Asset Management DAM.pdf page 35. 0 of 9 labels bound to a contract property; 27 of 158 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
 "findSimilarMediaAssets": {
  "method": "GET",
  "path": "/media-assets/similar",
  "contract": "assets",
  "summary": "Visually similar, near-duplicate and related assets",
  "permission": "ASSET_LIBRARY_VIEW",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "assetId",
    "in": "query",
    "required": true
   },
   {
    "name": "minSimilarity",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "MediaSimilarity"
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
 "listAssets": {
  "method": "GET",
  "path": "/assets",
  "contract": "maintenance",
  "summary": "List assets",
  "permission": "ASSET_VIEW",
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
    "name": "categoryId",
    "in": "query",
    "required": null
   },
   {
    "name": "status",
    "in": "query",
    "required": null
   },
   {
    "name": "maintenanceDue",
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
 "listMediaRenditions": {
  "method": "GET",
  "path": "/media-assets/{assetId}/renditions",
  "contract": "assets",
  "summary": "The derived sizes and formats, and whether they are ready",
  "permission": "ASSET_LIBRARY_VIEW",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "MediaRendition"
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
 "requestMediaRendition": {
  "method": "POST",
  "path": "/media-assets/{assetId}/renditions",
  "contract": "assets",
  "summary": "Generate a size or format",
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
  "requestBody": "MediaRendition",
  "responds": null
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
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
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
 "MediaRendition": {
  "type": "object",
  "x-ticvai-persistence": "assets.rendition",
  "description": "Boards 2.8 and 2.9. **Readiness is the fact that matters**, not existence.",
  "required": [
   "preset"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "preset": {
    "type": "string",
    "description": "e.g. `thumbnail`, `web1600`, `printCmyk`, `hls720`."
   },
   "format": {
    "type": "string",
    "nullable": true
   },
   "width": {
    "type": "integer",
    "nullable": true
   },
   "height": {
    "type": "integer",
    "nullable": true
   },
   "sizeBytes": {
    "type": "integer",
    "nullable": true
   },
   "status": {
    "type": "string",
    "enum": [
     "queued",
     "processing",
     "ready",
     "failed"
    ]
   },
   "failureReason": {
    "type": "string",
    "nullable": true
   },
   "url": {
    "type": "string",
    "nullable": true
   },
   "scopePath": {
    "type": "string"
   }
  }
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
 "MediaSimilarity": {
  "type": "object",
  "description": "Boards 2.4 and 2.5. **Duplicate and related are one score at two thresholds.**",
  "properties": {
   "assetId": {
    "type": "string",
    "format": "uuid"
   },
   "similarity": {
    "type": "number"
   },
   "relation": {
    "type": "string",
    "enum": [
     "exactDuplicate",
     "nearDuplicate",
     "variant",
     "related"
    ]
   },
   "differingFields": {
    "type": "array",
    "items": {
     "type": "string"
    }
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
 }
}
```
