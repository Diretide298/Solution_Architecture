# WS75 — Digital Asset Management DAM board 2

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
| `CMS-071` | AI Asset Intelligence Command Center | listDetail | 0 | 0 | — |
| `CMS-072` | AI Auto-Tagging & Content Understanding | listDetail | 0 | 1 | — |
| `CMS-073` | Semantic & Natural-Language Asset Search | listDetail | 0 | 0 | — |
| `CMS-074` | Visual Similarity & Related Asset Discovery | listDetail | 0 | 0 | — |
| `CMS-075` | Duplicate & Near-Duplicate Management | listDetail | 0 | 1 | — |
| `CMS-076` | Asset Version Control & Revision History | listDetail | 0 | 0 | — |
| `CMS-077` | Version Comparison & Replacement Impact | listDetail | 0 | 0 | — |
| `CMS-078` | Transformation & Rendition Management | configEditor | 0 | 0 | — |
| `CMS-079` | Rendition Processing & Delivery Readiness | listDetail | 0 | 1 | — |
| `CMS-080` | AI Quality, Intelligence Review & Recommendations | listDetail | 0 | 1 | — |

## Thin screens in this batch

**CMS-073, CMS-074, CMS-076, CMS-077, CMS-078 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

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
  "apis": [],
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
   "board": "wireframes/P13 Venue CMS.dc.html#cms-071"
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
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P13 Venue CMS.dc.html#cms-072"
  },
  "apisNote": "Regenerated 9 September 2026 from Digital Asset Management DAM.pdf page 27. 0 of 0 labels bound to a contract property; 4 of 17 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "apis": [],
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
   "board": "wireframes/P13 Venue CMS.dc.html#cms-073"
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
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Digital Asset Management DAM.pdf, page 29"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Digital Asset Management DAM.pdf, page 29"
   }
  ],
  "layout": {
   "template": "split",
   "regions": []
  },
  "states": {
   "loading": "The visual similarity related list.",
   "error": "Could not load. Names which read failed and leaves the visual similarity related untouched.",
   "emptyFirstRun": "No visual similarity related yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the visual similarity related are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P13 Venue CMS.dc.html#cms-074"
  },
  "apisNote": "Regenerated 9 September 2026 from Digital Asset Management DAM.pdf page 29. 0 of 0 labels bound to a contract property; 0 of 21 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
       "kind": "destructiveButton",
       "label": "Archive Duplicate",
       "provenance": "pack Digital Asset Management DAM.pdf, page 30 §Actions"
      }
     ]
    }
   ]
  },
  "overlays": [
   {
    "id": "confirmArchiveDuplicate",
    "component": "confirmDialog",
    "trigger": "Archive Duplicate",
    "body": "**Archive Duplicate on a duplicate near-duplicate is not reversible from this screen.** Names what it affects and what it leaves alone. The pack requires the decision to reach the audit trail, so the dialog states that it is recorded.",
    "provenance": "pack Digital Asset Management DAM.pdf, page 30 §Actions"
   }
  ],
  "states": {
   "loading": "The duplicate near-duplicate list.",
   "error": "Could not load. Names which read failed and leaves the duplicate near-duplicate untouched.",
   "emptyFirstRun": "No duplicate near-duplicate yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the duplicate near-duplicate are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P13 Venue CMS.dc.html#cms-075"
  },
  "apisNote": "Regenerated 9 September 2026 from Digital Asset Management DAM.pdf page 30. 0 of 0 labels bound to a contract property; 7 of 23 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
   "regions": []
  },
  "states": {
   "loading": "The asset version revision list.",
   "error": "Could not load. Names which read failed and leaves the asset version revision untouched.",
   "emptyFirstRun": "No asset version revision yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the asset version revision are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P13 Venue CMS.dc.html#cms-076"
  },
  "apisNote": "Regenerated 9 September 2026 from Digital Asset Management DAM.pdf page 31. 0 of 0 labels bound to a contract property; 0 of 15 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
   "regions": []
  },
  "states": {
   "loading": "The version comparison replacement list.",
   "error": "Could not load. Names which read failed and leaves the version comparison replacement untouched.",
   "emptyFirstRun": "No version comparison replacement yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the version comparison replacement are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P13 Venue CMS.dc.html#cms-077"
  },
  "apisNote": "Regenerated 9 September 2026 from Digital Asset Management DAM.pdf page 32. 0 of 0 labels bound to a contract property; 0 of 17 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P13 Venue CMS.dc.html#cms-078"
  },
  "apisNote": "Regenerated 9 September 2026 from Digital Asset Management DAM.pdf page 33. 0 of 0 labels bound to a contract property; 1 of 22 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P13 Venue CMS.dc.html#cms-079"
  },
  "apisNote": "Regenerated 9 September 2026 from Digital Asset Management DAM.pdf page 34. 0 of 0 labels bound to a contract property; 4 of 17 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "apis": [],
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
   "board": "wireframes/P13 Venue CMS.dc.html#cms-080"
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
{}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{}
```
