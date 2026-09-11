# WS01 — Access Control board 1

**10 screens · 10 operations · 15 schemas · 2 permissions**

Platform P08 Venue Management · ships as **venue-management** ·
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

- **Every control that can be refused must be gated.** 2 permissions apply here:
  `ACCESS_POINT_CONFIGURE, SCOPE_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **1 of these operations work offline**: listAccessPoints
  — and the rest do not. A surface that looks the same online and off is lying.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `BO-144` | Access Control Command Center | listDetail | 1 | 0 | — |
| `BO-145` | Venue & Park Access Structure | listDetail | 1 | 0 | — |
| `BO-146` | Access Area & Zone Builder | listDetail | 1 | 0 | — |
| `BO-147` | Attraction Access Configuration | listDetail | 1 | 0 | — |
| `BO-148` | Access Point Directory | configEditor | 1 | 0 | — |
| `BO-149` | Gate & Lane Configuration | listDetail | 1 | 0 | — |
| `BO-150` | Access Control Graphical Map Designer | listDetail | 1 | 0 | — |
| `BO-151` | Access Location Grouping | listDetail | 1 | 0 | — |
| `BO-152` | Operating Calendar & Special Access Days | configEditor | 1 | 0 | — |
| `BO-153` | Topology Validation & Publication | listDetail | 1 | 0 | — |

## Thin screens in this batch

**BO-144, BO-145, BO-146, BO-147, BO-149, BO-150, BO-151, BO-153 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "BO-144",
  "name": "Access Control Command Center",
  "module": "Access & Venue",
  "requiresModule": "access",
  "wave": 3,
  "source": {
   "pack": "Access Control Module_Reference.pdf",
   "board": "1",
   "number": "1",
   "page": 6
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/access-control-command-center-bo-144",
   "component": "apps/venue-management-web/src/routes/access-venue/AccessControlCommandCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-100"
   ],
   "exitTo": [
    "BO-100",
    "BO-145",
    "BO-146",
    "BO-147",
    "BO-148",
    "BO-149",
    "BO-150",
    "BO-151",
    "BO-152",
    "BO-153"
   ],
   "inferred": false,
   "notes": "**The board's hub.** The workshop specified this module as boards of ten and opened each with a command centre; the other nine screens are that board's detail, so they are reached from here and return here.",
   "transitions": [
    {
     "to": "BO-100",
     "trigger": "Venue Home",
     "carries": [
      "venueId"
     ],
     "provenance": "derived — BO-100 declares entryState.params venueId, so an edge into it must carry them"
    },
    {
     "to": "BO-145",
     "trigger": "Works in Venue & Park Access Structure",
     "provenance": "flow F111 step 1→2",
     "operation": "listAccess"
    },
    {
     "to": "BO-146",
     "trigger": "Works in Access Area & Zone Builder",
     "provenance": "flow F111 step 3→4",
     "operation": "listAccess"
    },
    {
     "to": "BO-147",
     "trigger": "Works in Attraction Access Configuration",
     "provenance": "flow F111 step 5→6",
     "operation": "listAccess"
    },
    {
     "to": "BO-148",
     "trigger": "Works in Access Point Directory",
     "provenance": "flow F111 step 7→8",
     "operation": "listAccess"
    },
    {
     "to": "BO-149",
     "trigger": "Works in Gate & Lane Configuration",
     "provenance": "flow F111 step 9→10",
     "operation": "listAccess"
    },
    {
     "to": "BO-150",
     "trigger": "Works in Access Control Graphical Map Designer",
     "provenance": "flow F111 step 11→12",
     "operation": "listAccess"
    },
    {
     "to": "BO-151",
     "trigger": "Works in Access Location Grouping",
     "provenance": "flow F111 step 13→14",
     "operation": "listAccess"
    },
    {
     "to": "BO-152",
     "trigger": "Works in Operating Calendar & Special Access Days",
     "provenance": "flow F111 step 15→16",
     "operation": "listAccess"
    },
    {
     "to": "BO-153",
     "trigger": "Works in Topology Validation & Publication",
     "provenance": "flow F111 step 17→18",
     "operation": "listAccess"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Dashboard should show) and no metric row",
  "purpose": "Central operational/configuration landing page for the complete Access Control module.",
  "purposeNote": "Administrator can understand the complete access-control estate and identify operational/configuration problems from one screen.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every access",
       "columns": [
        "AccessControlCommandCenterView.totalVenues",
        "AccessControlCommandCenterView.activeAccessPoints",
        "AccessControlCommandCenterView.entryGates",
        "AccessControlCommandCenterView.exitGates",
        "AccessControlCommandCenterView.attractionGates",
        "AccessControlCommandCenterView.turnstiles",
        "AccessControlCommandCenterView.handheldDevices",
        "Devices online/offline",
        "Gates open/closed",
        "AccessControlCommandCenterView.currentInVenueOccupancy",
        "AccessControlCommandCenterView.currentAdmissionRate",
        "AccessControlCommandCenterView.failedScans",
        "AccessControlCommandCenterView.overrides",
        "AccessControlCommandCenterView.securityAlerts",
        "AccessControlCommandCenterView.offlineDevices",
        "AccessControlCommandCenterView.synchronizationStatus"
       ],
       "bindsTo": "AccessControlCommandCenterView",
       "operation": "listAccess",
       "provenance": "pack Access Control Module_Reference.pdf, page 6 §Dashboard should show"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected access",
       "bindsTo": "AccessControlCommandCenterView",
       "columns": [
        "AccessControlCommandCenterView.totalVenues",
        "AccessControlCommandCenterView.activeAccessPoints",
        "AccessControlCommandCenterView.entryGates",
        "AccessControlCommandCenterView.exitGates",
        "AccessControlCommandCenterView.attractionGates",
        "AccessControlCommandCenterView.turnstiles",
        "AccessControlCommandCenterView.handheldDevices",
        "Devices online/offline",
        "Gates open/closed",
        "AccessControlCommandCenterView.currentInVenueOccupancy",
        "AccessControlCommandCenterView.currentAdmissionRate",
        "AccessControlCommandCenterView.failedScans",
        "AccessControlCommandCenterView.overrides",
        "AccessControlCommandCenterView.securityAlerts",
        "AccessControlCommandCenterView.offlineDevices",
        "AccessControlCommandCenterView.synchronizationStatus"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Display hierarchy such as”.",
       "provenance": "pack Access Control Module_Reference.pdf, page 6 §Dashboard should show"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The access list.",
   "error": "Could not load. Names which read failed and leaves the access untouched.",
   "emptyFirstRun": "No access yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the access are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listAccess",
    "contract": "access",
    "purpose": "Access Control Command Center",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "AccessControlCommandCenterView.totalVenues",
    "AccessControlCommandCenterView.activeAccessPoints",
    "AccessControlCommandCenterView.entryGates",
    "AccessControlCommandCenterView.exitGates",
    "AccessControlCommandCenterView.attractionGates",
    "AccessControlCommandCenterView.turnstiles"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-144"
  },
  "apisNote": "Regenerated 9 September 2026 from Access Control Module_Reference.pdf page 6. 14 of 16 labels bound to a contract property; 16 of 30 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "_platform": {
   "code": "P08",
   "audience": "staff",
   "formFactor": "web",
   "shortName": "Venue Management",
   "name": "Venue Management — Back Office",
   "offlineCapable": false,
   "app": "venue-management-web",
   "operator": "venue",
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P12",
     "P13",
     "P16"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "BO-145",
  "name": "Venue & Park Access Structure",
  "module": "Access & Venue",
  "requiresModule": "access",
  "wave": 3,
  "source": {
   "pack": "Access Control Module_Reference.pdf",
   "board": "1",
   "number": "2",
   "page": 7
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/venue-park-access-structure-bo-145",
   "component": "apps/venue-management-web/src/routes/access-venue/VenueParkAccessStructure.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-144"
   ],
   "exitTo": [
    "BO-144"
   ],
   "inferred": false,
   "notes": "**Reached from BO-144, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-144",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F111 step 2→3",
     "operation": "listVenueParkAccess"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Define the highest-level physical access hierarchy.",
  "purposeNote": "Any tenant can model single-site or multi-park operations without development.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Access Control Module_Reference.pdf, page 7"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Access Control Module_Reference.pdf, page 7"
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
       "impliedBy": "listVenueParkAccess",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The venue park access list.",
   "error": "Could not load. Names which read failed and leaves the venue park access untouched.",
   "emptyFirstRun": "No venue park access yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the venue park access are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listVenueParkAccess",
    "contract": "access",
    "purpose": "Venue & Park Access Structure",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "VenueParkAccessStructureView.venue",
    "VenueParkAccessStructureView.park",
    "VenueParkAccessStructureView.building",
    "VenueParkAccessStructureView.eventSpace",
    "VenueParkAccessStructureView.waterpark"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-145"
  },
  "apisNote": "Regenerated 9 September 2026 from Access Control Module_Reference.pdf page 7. 0 of 0 labels bound to a contract property; 0 of 30 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "_platform": {
   "code": "P08",
   "audience": "staff",
   "formFactor": "web",
   "shortName": "Venue Management",
   "name": "Venue Management — Back Office",
   "offlineCapable": false,
   "app": "venue-management-web",
   "operator": "venue",
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P12",
     "P13",
     "P16"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "BO-146",
  "name": "Access Area & Zone Builder",
  "module": "Access & Venue",
  "requiresModule": "access",
  "wave": 3,
  "source": {
   "pack": "Access Control Module_Reference.pdf",
   "board": "1",
   "number": "3",
   "page": 8
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/access-area-zone-builder-bo-146",
   "component": "apps/venue-management-web/src/routes/access-venue/AccessAreaZoneBuilder.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-144"
   ],
   "exitTo": [
    "BO-144"
   ],
   "inferred": false,
   "notes": "**Reached from BO-144, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-144",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F111 step 4→5",
     "operation": "setAccessAreaZone"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Divide a venue into controlled access areas.",
  "purposeNote": "Access-controlled zones can be configured and reorganized without software changes.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Access Control Module_Reference.pdf, page 8"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Access Control Module_Reference.pdf, page 8"
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
       "label": "Save changes",
       "provenance": "contract operation setAccessAreaZone"
      }
     ]
    },
    {
     "name": "contentBody",
     "components": [
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "setAccessAreaZone"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The access area zone list.",
   "error": "Could not load. Names which read failed and leaves the access area zone untouched.",
   "emptyFirstRun": "No access area zone yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the access area zone are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setAccessAreaZone",
    "contract": "access",
    "purpose": "Access Area & Zone Builder",
    "trigger": "onAction",
    "invalidates": [
     "setAccessAreaZone"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-146"
  },
  "apisNote": "Regenerated 9 September 2026 from Access Control Module_Reference.pdf page 8. 0 of 0 labels bound to a contract property; 0 of 24 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "_platform": {
   "code": "P08",
   "audience": "staff",
   "formFactor": "web",
   "shortName": "Venue Management",
   "name": "Venue Management — Back Office",
   "offlineCapable": false,
   "app": "venue-management-web",
   "operator": "venue",
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P12",
     "P13",
     "P16"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "BO-147",
  "name": "Attraction Access Configuration",
  "module": "Access & Venue",
  "requiresModule": "access",
  "wave": 3,
  "source": {
   "pack": "Access Control Module_Reference.pdf",
   "board": "1",
   "number": "4",
   "page": 9
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/attraction-access-configuration-bo-147",
   "component": "apps/venue-management-web/src/routes/access-venue/AttractionAccessConfiguration.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-144"
   ],
   "exitTo": [
    "BO-144"
   ],
   "inferred": false,
   "notes": "**Reached from BO-144, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-144",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F111 step 6→7",
     "operation": "setAttractionAccess"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Configure attractions as access-controlled destinations.",
  "purposeNote": "An attraction can independently enforce admission requirements without changing the base ticket product.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Access Control Module_Reference.pdf, page 9"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Access Control Module_Reference.pdf, page 9"
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
       "label": "Save changes",
       "provenance": "contract operation setAttractionAccess"
      }
     ]
    },
    {
     "name": "contentBody",
     "components": [
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "setAttractionAccess"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The attraction access list.",
   "error": "Could not load. Names which read failed and leaves the attraction access untouched.",
   "emptyFirstRun": "No attraction access yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the attraction access are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setAttractionAccess",
    "contract": "access",
    "purpose": "Attraction Access Configuration",
    "trigger": "onAction",
    "invalidates": [
     "setAttractionAccess"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-147"
  },
  "apisNote": "Regenerated 9 September 2026 from Access Control Module_Reference.pdf page 9. 0 of 0 labels bound to a contract property; 0 of 20 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "_platform": {
   "code": "P08",
   "audience": "staff",
   "formFactor": "web",
   "shortName": "Venue Management",
   "name": "Venue Management — Back Office",
   "offlineCapable": false,
   "app": "venue-management-web",
   "operator": "venue",
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P12",
     "P13",
     "P16"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "BO-148",
  "name": "Access Point Directory",
  "module": "Access & Venue",
  "requiresModule": "access",
  "wave": 3,
  "source": {
   "pack": "Access Control Module_Reference.pdf",
   "board": "1",
   "number": "5",
   "page": 10
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/access-point-directory-bo-148",
   "component": "apps/venue-management-web/src/routes/access-venue/AccessPointDirectory.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-144"
   ],
   "exitTo": [
    "BO-144"
   ],
   "inferred": false,
   "notes": "**Reached from BO-144, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-144",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F111 step 8→9",
     "operation": "listAccessPoints"
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Additional settings) and no display directory — it is settings, not a population",
  "purpose": "Create the logical access points where validation occurs. An Access Point is different from a physical reader/device.",
  "purposeNote": "Operations can logically group multiple physical devices under one controlled access point.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "operating schedule",
       "provenance": "pack Access Control Module_Reference.pdf, page 10 §Additional settings"
      },
      {
       "kind": "selectField",
       "label": "allowed direction",
       "provenance": "pack Access Control Module_Reference.pdf, page 10 §Additional settings"
      },
      {
       "kind": "selectField",
       "label": "capacity",
       "provenance": "pack Access Control Module_Reference.pdf, page 10 §Additional settings"
      },
      {
       "kind": "selectField",
       "label": "default mode",
       "provenance": "pack Access Control Module_Reference.pdf, page 10 §Additional settings"
      },
      {
       "kind": "selectField",
       "label": "associated zone",
       "provenance": "pack Access Control Module_Reference.pdf, page 10 §Additional settings"
      },
      {
       "kind": "selectField",
       "label": "allowed ticket categories",
       "provenance": "pack Access Control Module_Reference.pdf, page 10 §Additional settings"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The access point configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the access point untouched.",
   "emptyFirstRun": "No access point configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listAccessPoints",
    "contract": "access",
    "purpose": "List access points",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-148"
  },
  "apisNote": "Regenerated 9 September 2026 from Access Control Module_Reference.pdf page 10. 0 of 0 labels bound to a contract property; 6 of 24 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "_platform": {
   "code": "P08",
   "audience": "staff",
   "formFactor": "web",
   "shortName": "Venue Management",
   "name": "Venue Management — Back Office",
   "offlineCapable": false,
   "app": "venue-management-web",
   "operator": "venue",
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P12",
     "P13",
     "P16"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "BO-149",
  "name": "Gate & Lane Configuration",
  "module": "Access & Venue",
  "requiresModule": "access",
  "wave": 3,
  "source": {
   "pack": "Access Control Module_Reference.pdf",
   "board": "1",
   "number": "6",
   "page": 11
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/gate-lane-configuration-bo-149",
   "component": "apps/venue-management-web/src/routes/access-venue/GateLaneConfiguration.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-144"
   ],
   "exitTo": [
    "BO-144"
   ],
   "inferred": false,
   "notes": "**Reached from BO-144, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-144",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F111 step 10→11",
     "operation": "setGateLane"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Configure individual physical gates/lanes.",
  "purposeNote": "Every physical lane can have independent configuration while inheriting settings from its parent access point.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Access Control Module_Reference.pdf, page 11"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Access Control Module_Reference.pdf, page 11"
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
       "label": "Save changes",
       "provenance": "contract operation setGateLane"
      }
     ]
    },
    {
     "name": "contentBody",
     "components": [
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "setGateLane"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The gate lane list.",
   "error": "Could not load. Names which read failed and leaves the gate lane untouched.",
   "emptyFirstRun": "No gate lane yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the gate lane are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setGateLane",
    "contract": "access",
    "purpose": "Gate & Lane Configuration",
    "trigger": "onAction",
    "invalidates": [
     "setGateLane"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-149"
  },
  "apisNote": "Regenerated 9 September 2026 from Access Control Module_Reference.pdf page 11. 0 of 0 labels bound to a contract property; 0 of 26 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "_platform": {
   "code": "P08",
   "audience": "staff",
   "formFactor": "web",
   "shortName": "Venue Management",
   "name": "Venue Management — Back Office",
   "offlineCapable": false,
   "app": "venue-management-web",
   "operator": "venue",
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P12",
     "P13",
     "P16"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "BO-150",
  "name": "Access Control Graphical Map Designer",
  "module": "Access & Venue",
  "requiresModule": "access",
  "wave": 3,
  "source": {
   "pack": "Access Control Module_Reference.pdf",
   "board": "1",
   "number": "7",
   "page": 12
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/access-control-graphical-map-designer-bo-150",
   "component": "apps/venue-management-web/src/routes/access-venue/AccessControlGraphicalMapDesigner.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-144"
   ],
   "exitTo": [
    "BO-144"
   ],
   "inferred": false,
   "notes": "**Reached from BO-144, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-144",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F111 step 12→13",
     "operation": "setAccessGraphicalMap"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Create a graphical digital twin of the access-control environment.",
  "purposeNote": "Access infrastructure can be configured and monitored geographically from a venue map.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Access Control Module_Reference.pdf, page 12"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Access Control Module_Reference.pdf, page 12"
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
       "label": "Save changes",
       "provenance": "contract operation setAccessGraphicalMap"
      }
     ]
    },
    {
     "name": "contentBody",
     "components": [
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "setAccessGraphicalMap"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The access graphical map list.",
   "error": "Could not load. Names which read failed and leaves the access graphical map untouched.",
   "emptyFirstRun": "No access graphical map yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the access graphical map are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setAccessGraphicalMap",
    "contract": "access",
    "purpose": "Access Control Graphical Map Designer",
    "trigger": "onAction",
    "invalidates": [
     "setAccessGraphicalMap"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-150"
  },
  "apisNote": "Regenerated 9 September 2026 from Access Control Module_Reference.pdf page 12. 0 of 0 labels bound to a contract property; 0 of 17 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "_platform": {
   "code": "P08",
   "audience": "staff",
   "formFactor": "web",
   "shortName": "Venue Management",
   "name": "Venue Management — Back Office",
   "offlineCapable": false,
   "app": "venue-management-web",
   "operator": "venue",
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P12",
     "P13",
     "P16"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "BO-151",
  "name": "Access Location Grouping",
  "module": "Access & Venue",
  "requiresModule": "access",
  "wave": 3,
  "source": {
   "pack": "Access Control Module_Reference.pdf",
   "board": "1",
   "number": "8",
   "page": 13
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/access-location-grouping-bo-151",
   "component": "apps/venue-management-web/src/routes/access-venue/AccessLocationGrouping.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-144"
   ],
   "exitTo": [
    "BO-144"
   ],
   "inferred": false,
   "notes": "**Reached from BO-144, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-144",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F111 step 14→15",
     "operation": "listAccessLocationGrouping"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Group multiple access points for operational and capacity purposes.",
  "purposeNote": "Multiple access-control devices can contribute to common occupancy and operational statistics.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Access Control Module_Reference.pdf, page 13"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Access Control Module_Reference.pdf, page 13"
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
       "impliedBy": "listAccessLocationGrouping",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The access location grouping list.",
   "error": "Could not load. Names which read failed and leaves the access location grouping untouched.",
   "emptyFirstRun": "No access location grouping yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the access location grouping are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listAccessLocationGrouping",
    "contract": "access",
    "purpose": "Access Location Grouping",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-151"
  },
  "apisNote": "Regenerated 9 September 2026 from Access Control Module_Reference.pdf page 13. 0 of 0 labels bound to a contract property; 0 of 10 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "_platform": {
   "code": "P08",
   "audience": "staff",
   "formFactor": "web",
   "shortName": "Venue Management",
   "name": "Venue Management — Back Office",
   "offlineCapable": false,
   "app": "venue-management-web",
   "operator": "venue",
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P12",
     "P13",
     "P16"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "BO-152",
  "name": "Operating Calendar & Special Access Days",
  "module": "Access & Venue",
  "requiresModule": "access",
  "wave": 3,
  "source": {
   "pack": "Access Control Module_Reference.pdf",
   "board": "1",
   "number": "9",
   "page": 13
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/operating-calendar-special-access-days-bo-152",
   "component": "apps/venue-management-web/src/routes/access-venue/OperatingCalendarSpecialAccessDays.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-144"
   ],
   "exitTo": [
    "BO-144"
   ],
   "inferred": false,
   "notes": "**Reached from BO-144, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-144",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F111 step 16→17",
     "operation": "listOperatingCalendarSpecial"
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population",
  "purpose": "Allow access topology and operating behavior to change by date/time.",
  "purposeNote": "Special-date access configurations can automatically replace standard operation without manual gate-by- gate changes.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "normal operating days",
       "provenance": "pack Access Control Module_Reference.pdf, page 13 §Configure"
      },
      {
       "kind": "selectField",
       "label": "weekends",
       "provenance": "pack Access Control Module_Reference.pdf, page 13 §Configure"
      },
      {
       "kind": "selectField",
       "label": "holidays",
       "provenance": "pack Access Control Module_Reference.pdf, page 13 §Configure"
      },
      {
       "kind": "selectField",
       "label": "seasonal schedules",
       "provenance": "pack Access Control Module_Reference.pdf, page 13 §Configure"
      },
      {
       "kind": "selectField",
       "label": "private events",
       "provenance": "pack Access Control Module_Reference.pdf, page 13 §Configure"
      },
      {
       "kind": "selectField",
       "label": "free-entry days",
       "provenance": "pack Access Control Module_Reference.pdf, page 13 §Configure"
      },
      {
       "kind": "selectField",
       "label": "maintenance periods",
       "provenance": "pack Access Control Module_Reference.pdf, page 13 §Configure"
      },
      {
       "kind": "selectField",
       "label": "special events",
       "provenance": "pack Access Control Module_Reference.pdf, page 13 §Configure"
      },
      {
       "kind": "selectField",
       "label": "ladies-only sessions",
       "provenance": "pack Access Control Module_Reference.pdf, page 13 §Configure"
      },
      {
       "kind": "selectField",
       "label": "school/group sessions",
       "provenance": "pack Access Control Module_Reference.pdf, page 13 §Configure"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The operating calendar special configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the operating calendar special untouched.",
   "emptyFirstRun": "No operating calendar special configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listOperatingCalendarSpecial",
    "contract": "access",
    "purpose": "Operating Calendar & Special Access Days",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-152"
  },
  "apisNote": "Regenerated 9 September 2026 from Access Control Module_Reference.pdf page 13. 0 of 0 labels bound to a contract property; 10 of 18 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "_platform": {
   "code": "P08",
   "audience": "staff",
   "formFactor": "web",
   "shortName": "Venue Management",
   "name": "Venue Management — Back Office",
   "offlineCapable": false,
   "app": "venue-management-web",
   "operator": "venue",
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P12",
     "P13",
     "P16"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "BO-153",
  "name": "Topology Validation & Publication",
  "module": "Access & Venue",
  "requiresModule": "access",
  "wave": 3,
  "source": {
   "pack": "Access Control Module_Reference.pdf",
   "board": "1",
   "number": "10",
   "page": 14
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/topology-validation-publication-bo-153",
   "component": "apps/venue-management-web/src/routes/access-venue/TopologyValidationPublication.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-144"
   ],
   "exitTo": [
    "BO-144"
   ],
   "inferred": false,
   "notes": "**Reached from BO-144, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation."
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Final validation and controlled deployment of access configuration. Before publication, TICVAI automatically validates: orphan gates devices without access points access points without zones incorrect entry/exit direction missing offline configuration conflicting operating calendars inaccessible zones missing emergency configuration capacity inconsistencies missing reader/device association policy dependencies.",
  "purposeNote": "No access topology enters production without validation, authorization, version tracking and rollback capability. Board 1 — Final Backend Navigation The left-side navigation for this board should therefore be:",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Access Control Module_Reference.pdf, page 14"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Access Control Module_Reference.pdf, page 14"
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
       "label": "Publish",
       "provenance": "contract operation publishTopologyValidation"
      },
      {
       "kind": "publishGate",
       "label": "What publishing changes",
       "notes": "**Names what goes live, where, and from when.** A publish with no stated consequence is one somebody presses meaning to save.",
       "provenance": "authored — required by check-screens for publishTopologyValidation"
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
   "loading": "The topology validation publication list.",
   "error": "Could not load. Names which read failed and leaves the topology validation publication untouched.",
   "emptyFirstRun": "No topology validation publication yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the topology validation publication are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "publishTopologyValidation",
    "contract": "access",
    "purpose": "Topology Validation & Publication",
    "trigger": "onAction",
    "invalidates": [
     "publishTopologyValidation"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-153"
  },
  "apisNote": "Regenerated 9 September 2026 from Access Control Module_Reference.pdf page 14. 0 of 0 labels bound to a contract property; 0 of 43 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "_platform": {
   "code": "P08",
   "audience": "staff",
   "formFactor": "web",
   "shortName": "Venue Management",
   "name": "Venue Management — Back Office",
   "offlineCapable": false,
   "app": "venue-management-web",
   "operator": "venue",
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P12",
     "P13",
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
 "listAccess": {
  "method": "GET",
  "path": "/access",
  "contract": "access",
  "summary": "Access Control Command Center",
  "permission": "SCOPE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "AccessControlCommandCenterView"
 },
 "listAccessLocationGrouping": {
  "method": "GET",
  "path": "/access-location-grouping",
  "contract": "access",
  "summary": "Access Location Grouping",
  "permission": "SCOPE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "AccessLocationGroupingView"
 },
 "listAccessPoints": {
  "method": "GET",
  "path": "/access-points",
  "contract": "access",
  "summary": "List access points",
  "permission": "SCOPE_VIEW",
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
 "listOperatingCalendarSpecial": {
  "method": "GET",
  "path": "/operating-calendar-special",
  "contract": "access",
  "summary": "Operating Calendar & Special Access Days",
  "permission": "SCOPE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "OperatingCalendarSpecialAccessDaysView"
 },
 "listVenueParkAccess": {
  "method": "GET",
  "path": "/venue-park-access",
  "contract": "access",
  "summary": "Venue & Park Access Structure",
  "permission": "SCOPE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "VenueParkAccessStructureView"
 },
 "publishTopologyValidation": {
  "method": "PUT",
  "path": "/topology-validation",
  "contract": "access",
  "summary": "Topology Validation & Publication",
  "permission": "ACCESS_POINT_CONFIGURE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": "TopologyValidationPublicationInput",
  "responds": "TopologyValidationPublicationView"
 },
 "setAccessAreaZone": {
  "method": "PUT",
  "path": "/access-area-zone",
  "contract": "access",
  "summary": "Access Area & Zone Builder",
  "permission": "ACCESS_POINT_CONFIGURE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": "AccessAreaZoneBuilderInput",
  "responds": "AccessAreaZoneBuilderView"
 },
 "setAccessGraphicalMap": {
  "method": "PUT",
  "path": "/access-graphical-map",
  "contract": "access",
  "summary": "Access Control Graphical Map Designer",
  "permission": "ACCESS_POINT_CONFIGURE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": "AccessControlGraphicalMapDesignerInput",
  "responds": "AccessControlGraphicalMapDesignerView"
 },
 "setAttractionAccess": {
  "method": "PUT",
  "path": "/attraction-access",
  "contract": "access",
  "summary": "Attraction Access Configuration",
  "permission": "ACCESS_POINT_CONFIGURE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": "AttractionAccessConfigurationInput",
  "responds": "AttractionAccessConfigurationView"
 },
 "setGateLane": {
  "method": "PUT",
  "path": "/gate-lane",
  "contract": "access",
  "summary": "Gate & Lane Configuration",
  "permission": "ACCESS_POINT_CONFIGURE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": "GateLaneConfigurationInput",
  "responds": "GateLaneConfigurationView"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "AccessAreaZoneBuilderInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table covers these fields** — the closest is access.parking_facility at 14%, so this is not an update to anything the package stores today and no new table has been decided",
  "description": "**What Access Area & Zone Builder submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.\n\n**The pack defines this as a record**, under *Each zone receives* - one of only 13 drafted writes that does. That is the client writing a row rather than a screen, and it is where the table conversation should start.",
  "properties": {
   "zoneType": {
    "type": "string",
    "enum": [
     "public",
     "ticketed",
     "vip",
     "staff",
     "backOfHouse",
     "attraction",
     "restricted",
     "fastPass",
     "event",
     "temporary"
    ],
    "description": "Vocabulary listed under Create."
   },
   "capacity": {
    "type": "integer",
    "description": "capacity"
   },
   "operatingSchedule": {
    "type": "string",
    "description": "operating schedule"
   },
   "securityClassification": {
    "type": "string",
    "description": "security classification"
   },
   "entryRequirements": {
    "type": "string",
    "description": "entry requirements"
   },
   "exitRequirements": {
    "type": "string",
    "description": "exit requirements"
   },
   "allowedCredentialClasses": {
    "type": "string",
    "description": "allowed credential classes"
   }
  },
  "x-ticvai-record-definition": "Each zone receives"
 },
 "AccessAreaZoneBuilderView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Access Area & Zone Builder displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "zoneType": {
    "type": "string",
    "enum": [
     "public",
     "ticketed",
     "vip",
     "staff",
     "backOfHouse",
     "attraction",
     "restricted",
     "fastPass",
     "event",
     "temporary"
    ],
    "description": "Vocabulary listed under Create."
   },
   "capacity": {
    "type": "integer",
    "description": "capacity"
   },
   "operatingSchedule": {
    "type": "string",
    "description": "operating schedule"
   },
   "securityClassification": {
    "type": "string",
    "description": "security classification"
   },
   "entryRequirements": {
    "type": "string",
    "description": "entry requirements"
   },
   "exitRequirements": {
    "type": "string",
    "description": "exit requirements"
   },
   "allowedCredentialClasses": {
    "type": "string",
    "description": "allowed credential classes"
   }
  }
 },
 "AccessControlCommandCenterView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Access Control Command Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "totalVenues": {
    "type": "integer",
    "description": "Total venues"
   },
   "activeAccessPoints": {
    "type": "integer",
    "description": "Active access points"
   },
   "entryGates": {
    "type": "integer",
    "description": "Entry gates"
   },
   "exitGates": {
    "type": "integer",
    "description": "Exit gates"
   },
   "attractionGates": {
    "type": "integer",
    "description": "Attraction gates"
   },
   "turnstiles": {
    "type": "integer",
    "description": "Turnstiles"
   },
   "handheldDevices": {
    "type": "integer",
    "description": "Handheld devices"
   },
   "devicesOnline": {
    "type": "integer",
    "description": "Devices online"
   },
   "devicesOffline": {
    "type": "integer",
    "description": "Devices offline"
   },
   "gatesOpen": {
    "type": "integer",
    "description": "Gates open"
   },
   "gatesClosed": {
    "type": "integer",
    "description": "Gates closed"
   },
   "currentInVenueOccupancy": {
    "type": "integer",
    "description": "Current in-venue occupancy"
   },
   "currentAdmissionRate": {
    "type": "number",
    "description": "Current admission rate"
   },
   "failedScans": {
    "type": "integer",
    "description": "Failed scans"
   },
   "overrides": {
    "type": "integer",
    "description": "Overrides"
   },
   "securityAlerts": {
    "type": "integer",
    "description": "Security alerts"
   },
   "offlineDevices": {
    "type": "integer",
    "description": "Offline devices"
   },
   "synchronizationStatus": {
    "type": "integer",
    "description": "Synchronization status"
   }
  }
 },
 "AccessControlGraphicalMapDesignerInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures",
  "description": "**What Access Control Graphical Map Designer submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "cad": {
    "type": "string",
    "description": "CAD"
   },
   "pdf": {
    "type": "string",
    "description": "PDF"
   },
   "image": {
    "type": "string",
    "description": "image"
   },
   "venuePlan": {
    "type": "string",
    "description": "venue plan"
   },
   "architecturalDrawing": {
    "type": "string",
    "description": "architectural drawing"
   },
   "ontoTheMap": {
    "type": "string",
    "description": "onto the map"
   },
   "ai": {
    "type": "string",
    "description": "AI"
   }
  }
 },
 "AccessControlGraphicalMapDesignerView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Access Control Graphical Map Designer displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "cad": {
    "type": "string",
    "description": "CAD"
   },
   "pdf": {
    "type": "string",
    "description": "PDF"
   },
   "image": {
    "type": "string",
    "description": "image"
   },
   "venuePlan": {
    "type": "string",
    "description": "venue plan"
   },
   "architecturalDrawing": {
    "type": "string",
    "description": "architectural drawing"
   },
   "ontoTheMap": {
    "type": "string",
    "description": "onto the map"
   },
   "ai": {
    "type": "string",
    "description": "AI"
   }
  }
 },
 "AccessLocationGroupingView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Access Location Grouping displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "gate01": {
    "type": "string",
    "description": "Gate 01"
   },
   "gate02": {
    "type": "string",
    "description": "Gate 02"
   },
   "gate03": {
    "type": "string",
    "description": "Gate 03"
   },
   "gate04": {
    "type": "string",
    "description": "Gate 04"
   },
   "coasterGate": {
    "type": "string",
    "description": "Coaster Gate"
   },
   "dropTowerGate": {
    "type": "string",
    "description": "Drop Tower Gate"
   },
   "adventureHallGate": {
    "type": "string",
    "description": "Adventure Hall Gate"
   },
   "normalOperatingDays": {
    "type": "string",
    "description": "normal operating days"
   },
   "weekends": {
    "type": "string",
    "description": "weekends"
   },
   "holidays": {
    "type": "string",
    "description": "holidays"
   },
   "seasonalSchedules": {
    "type": "string",
    "description": "seasonal schedules"
   },
   "privateEvents": {
    "type": "string",
    "description": "private events"
   },
   "freeEntryDays": {
    "type": "string",
    "description": "free-entry days"
   },
   "maintenancePeriods": {
    "type": "string",
    "description": "maintenance periods"
   }
  }
 },
 "AttractionAccessConfigurationInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table covers these fields** — the closest is access.parking_facility at 6%, so this is not an update to anything the package stores today and no new table has been decided",
  "description": "**What Attraction Access Configuration submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.\n\n**The pack defines this as a record**, under *For each attraction* - one of only 13 drafted writes that does. That is the client writing a row rather than a screen, and it is where the table conversation should start.",
  "properties": {
   "attractionId": {
    "type": "string",
    "description": "Attraction ID"
   },
   "name": {
    "type": "string",
    "description": "Name"
   },
   "venue": {
    "type": "string",
    "description": "Venue"
   },
   "zone": {
    "type": "string",
    "description": "Zone"
   },
   "capacity": {
    "type": "integer",
    "description": "Capacity"
   },
   "entryPoints": {
    "type": "string",
    "description": "Entry points"
   },
   "exitPoints": {
    "type": "string",
    "description": "Exit points"
   },
   "fastPassSupport": {
    "type": "boolean",
    "description": "Fast Pass support"
   },
   "heightRestriction": {
    "type": "string",
    "description": "Height restriction"
   },
   "ageRestriction": {
    "type": "string",
    "description": "Age restriction"
   },
   "adultCompanionRequirement": {
    "type": "string",
    "description": "Adult companion requirement"
   },
   "membershipAccess": {
    "type": "string",
    "description": "Membership access"
   },
   "vipAccess": {
    "type": "string",
    "description": "VIP access"
   },
   "entitlementRequirement": {
    "type": "string",
    "description": "entitlement requirement"
   },
   "biometricRequirement": {
    "type": "string",
    "description": "biometric requirement"
   },
   "operatingCalendar": {
    "type": "string",
    "description": "operating calendar"
   },
   "temporaryClosureBehavior": {
    "type": "string",
    "description": "temporary closure behavior"
   }
  },
  "x-ticvai-record-definition": "For each attraction"
 },
 "AttractionAccessConfigurationView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Attraction Access Configuration displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "attractionId": {
    "type": "string",
    "description": "Attraction ID"
   },
   "name": {
    "type": "string",
    "description": "Name"
   },
   "venue": {
    "type": "string",
    "description": "Venue"
   },
   "zone": {
    "type": "string",
    "description": "Zone"
   },
   "capacity": {
    "type": "integer",
    "description": "Capacity"
   },
   "entryPoints": {
    "type": "string",
    "description": "Entry points"
   },
   "exitPoints": {
    "type": "string",
    "description": "Exit points"
   },
   "fastPassSupport": {
    "type": "boolean",
    "description": "Fast Pass support"
   },
   "heightRestriction": {
    "type": "string",
    "description": "Height restriction"
   },
   "ageRestriction": {
    "type": "string",
    "description": "Age restriction"
   },
   "adultCompanionRequirement": {
    "type": "string",
    "description": "Adult companion requirement"
   },
   "membershipAccess": {
    "type": "string",
    "description": "Membership access"
   },
   "vipAccess": {
    "type": "string",
    "description": "VIP access"
   },
   "entitlementRequirement": {
    "type": "string",
    "description": "entitlement requirement"
   },
   "biometricRequirement": {
    "type": "string",
    "description": "biometric requirement"
   },
   "operatingCalendar": {
    "type": "string",
    "description": "operating calendar"
   },
   "temporaryClosureBehavior": {
    "type": "string",
    "description": "temporary closure behavior"
   }
  }
 },
 "GateLaneConfigurationInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures",
  "description": "**What Gate & Lane Configuration submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "gateId": {
    "type": "string",
    "description": "Gate ID"
   },
   "gateName": {
    "type": "string",
    "description": "Gate name"
   },
   "accessPoint": {
    "type": "string",
    "description": "Access point"
   },
   "location": {
    "type": "string",
    "description": "Location"
   },
   "laneNumber": {
    "type": "string",
    "description": "lane number"
   },
   "entry": {
    "type": "string",
    "description": "Entry"
   },
   "exit": {
    "type": "string",
    "description": "Exit"
   },
   "bidirectional": {
    "type": "string",
    "description": "Bidirectional"
   },
   "reEntry": {
    "type": "string",
    "description": "Re-entry"
   },
   "crossover": {
    "type": "string",
    "description": "Crossover"
   },
   "type": {
    "type": "string",
    "enum": [
     "standard",
     "vip",
     "fastPass",
     "accessible",
     "group",
     "staff",
     "attraction"
    ],
    "description": "Vocabulary listed under Gate type."
   },
   "validation": {
    "type": "string",
    "description": "Validation"
   },
   "freeSpin": {
    "type": "string",
    "description": "Free Spin"
   },
   "closed": {
    "type": "integer",
    "description": "Closed"
   },
   "emergencyDropArm": {
    "type": "string",
    "description": "Emergency / Drop Arm"
   },
   "manual": {
    "type": "string",
    "description": "Manual"
   },
   "countOnly": {
    "type": "integer",
    "description": "Count Only"
   }
  }
 },
 "GateLaneConfigurationView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Gate & Lane Configuration displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "gateId": {
    "type": "string",
    "description": "Gate ID"
   },
   "gateName": {
    "type": "string",
    "description": "Gate name"
   },
   "accessPoint": {
    "type": "string",
    "description": "Access point"
   },
   "location": {
    "type": "string",
    "description": "Location"
   },
   "laneNumber": {
    "type": "string",
    "description": "lane number"
   },
   "entry": {
    "type": "string",
    "description": "Entry"
   },
   "exit": {
    "type": "string",
    "description": "Exit"
   },
   "bidirectional": {
    "type": "string",
    "description": "Bidirectional"
   },
   "reEntry": {
    "type": "string",
    "description": "Re-entry"
   },
   "crossover": {
    "type": "string",
    "description": "Crossover"
   },
   "type": {
    "type": "string",
    "enum": [
     "standard",
     "vip",
     "fastPass",
     "accessible",
     "group",
     "staff",
     "attraction"
    ],
    "description": "Vocabulary listed under Gate type."
   },
   "validation": {
    "type": "string",
    "description": "Validation"
   },
   "freeSpin": {
    "type": "string",
    "description": "Free Spin"
   },
   "closed": {
    "type": "integer",
    "description": "Closed"
   },
   "emergencyDropArm": {
    "type": "string",
    "description": "Emergency / Drop Arm"
   },
   "manual": {
    "type": "string",
    "description": "Manual"
   },
   "countOnly": {
    "type": "integer",
    "description": "Count Only"
   }
  }
 },
 "OperatingCalendarSpecialAccessDaysView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Operating Calendar & Special Access Days displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "normalOperatingDays": {
    "type": "string",
    "description": "normal operating days"
   },
   "weekends": {
    "type": "string",
    "description": "weekends"
   },
   "holidays": {
    "type": "string",
    "description": "holidays"
   },
   "seasonalSchedules": {
    "type": "string",
    "description": "seasonal schedules"
   },
   "privateEvents": {
    "type": "string",
    "description": "private events"
   },
   "freeEntryDays": {
    "type": "string",
    "description": "free-entry days"
   },
   "maintenancePeriods": {
    "type": "string",
    "description": "maintenance periods"
   },
   "specialEvents": {
    "type": "string",
    "description": "special events"
   },
   "ladiesOnlySessions": {
    "type": "string",
    "description": "ladies-only sessions"
   },
   "schoolGroupSessions": {
    "type": "string",
    "description": "school/group sessions"
   },
   "afterHoursEvents": {
    "type": "string",
    "description": "after-hours events"
   },
   "ai": {
    "type": "string",
    "description": "AI"
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
 "TopologyValidationPublicationInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures",
  "description": "**What Topology Validation & Publication submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "entireTenant": {
    "type": "string",
    "description": "Entire tenant"
   },
   "venue": {
    "type": "string",
    "description": "Venue"
   },
   "park": {
    "type": "string",
    "description": "Park"
   },
   "zone": {
    "type": "string",
    "description": "Zone"
   },
   "accessPoint": {
    "type": "string",
    "description": "Access point"
   },
   "selectedGates": {
    "type": "string",
    "description": "Selected gates"
   },
   "selectedDevices": {
    "type": "string",
    "description": "Selected devices"
   },
   "withRollbackToPreviousConfiguration": {
    "type": "string",
    "description": "with rollback to previous configuration"
   },
   "scanned": {
    "type": "string",
    "description": "scanned"
   },
   "development": {
    "type": "string",
    "description": "development"
   }
  }
 },
 "TopologyValidationPublicationView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Topology Validation & Publication displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "entireTenant": {
    "type": "string",
    "description": "Entire tenant"
   },
   "venue": {
    "type": "string",
    "description": "Venue"
   },
   "park": {
    "type": "string",
    "description": "Park"
   },
   "zone": {
    "type": "string",
    "description": "Zone"
   },
   "accessPoint": {
    "type": "string",
    "description": "Access point"
   },
   "selectedGates": {
    "type": "string",
    "description": "Selected gates"
   },
   "selectedDevices": {
    "type": "string",
    "description": "Selected devices"
   },
   "withRollbackToPreviousConfiguration": {
    "type": "string",
    "description": "with rollback to previous configuration"
   },
   "scanned": {
    "type": "string",
    "description": "scanned"
   },
   "development": {
    "type": "string",
    "description": "development"
   }
  }
 },
 "VenueParkAccessStructureView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Venue & Park Access Structure displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "venue": {
    "type": "string",
    "description": "Venue"
   },
   "park": {
    "type": "string",
    "description": "Park"
   },
   "building": {
    "type": "string",
    "description": "Building"
   },
   "eventSpace": {
    "type": "string",
    "description": "Event space"
   },
   "waterpark": {
    "type": "string",
    "description": "Waterpark"
   },
   "themePark": {
    "type": "string",
    "description": "Theme park"
   },
   "museum": {
    "type": "string",
    "description": "Museum"
   },
   "arena": {
    "type": "string",
    "description": "Arena"
   },
   "stadium": {
    "type": "string",
    "description": "Stadium"
   },
   "exhibition": {
    "type": "string",
    "description": "Exhibition"
   },
   "temporaryVenue": {
    "type": "string",
    "description": "temporary venue"
   },
   "name": {
    "type": "string",
    "description": "Name"
   },
   "code": {
    "type": "string",
    "description": "Code"
   },
   "tenant": {
    "type": "string",
    "description": "Tenant"
   },
   "parentEntity": {
    "type": "string",
    "description": "Parent entity"
   },
   "timeZone": {
    "type": "string",
    "format": "date-time",
    "description": "Time zone"
   },
   "operatingCalendar": {
    "type": "string",
    "description": "Operating calendar"
   },
   "capacity": {
    "type": "integer",
    "description": "Capacity"
   },
   "accessControlEnabled": {
    "type": "boolean",
    "description": "Access-control enabled"
   },
   "defaultEntryPolicy": {
    "type": "string",
    "description": "Default entry policy"
   },
   "defaultExitPolicy": {
    "type": "string",
    "description": "Default exit policy"
   },
   "defaultCredentialRules": {
    "type": "string",
    "description": "Default credential rules"
   },
   "offlinePolicy": {
    "type": "integer",
    "description": "Offline policy"
   },
   "emergencyBehavior": {
    "type": "string",
    "description": "Emergency behavior"
   },
   "supportMultiParkEnvironments": {
    "type": "string",
    "description": "Support multi-park environments"
   }
  }
 }
}
```
