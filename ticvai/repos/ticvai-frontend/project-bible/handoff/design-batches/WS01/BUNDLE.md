# WS01 — Access Control board 1

**10 screens · 19 operations · 29 schemas · 3 permissions**

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

- **Every control that can be refused must be gated.** 3 permissions apply here:
  `ACCESS_POINT_CONFIGURE, SCOPE_MANAGE, SCOPE_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `BO-144` | Access Control Command Center | listDetail | 2 | 0 | — |
| `BO-145` | Venue & Park Access Structure | listDetail | 4 | 0 | — |
| `BO-146` | Access Area & Zone Builder | listDetail | 1 | 0 | — |
| `BO-147` | Attraction Access Configuration | listDetail | 1 | 0 | — |
| `BO-148` | Access Point Directory | configEditor | 1 | 0 | — |
| `BO-149` | Gate & Lane Configuration | listDetail | 1 | 0 | — |
| `BO-150` | Access Control Graphical Map Designer | listDetail | 1 | 0 | — |
| `BO-151` | Access Location Grouping | listDetail | 3 | 2 | — |
| `BO-152` | Operating Calendar & Special Access Days | configEditor | 3 | 2 | — |
| `BO-153` | Topology Validation & Publication | listDetail | 2 | 1 | — |

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
     "provenance": "derived — BO-100 declares entryState.params  and BO-144 holds none of them, so the edge carries nothing and BO-100 opens cold"
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
  "purposeNote": "Administrator can understand the complete access-control estate and identify operational/configuration problems from one screen.",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Dashboard should show) and no metric row",
  "purpose": "Central operational/configuration landing page for the complete Access Control module.",
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
   },
   {
    "operationId": "createAccessPoint",
    "contract": "access",
    "purpose": "Add an access point to the estate from the command centre",
    "trigger": "onAction",
    "provenance": "decided 29 September, VM close-out (venue management and configuration)",
    "invalidates": [
     "listAccess"
    ]
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
   "board": "wireframes/P08 Venue Management.dc.html#bo-144",
   "workshopBoard": "wireframes/WS18 Access Control Board 1.dc.html#bo-144"
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
  "purposeNote": "Any tenant can model single-site or multi-park operations without development.",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Define the highest-level physical access hierarchy.",
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
      },
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "createOrgUnit",
       "label": "Create org unit",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "createOrgUnit"
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
   },
   {
    "operationId": "listOrgUnits",
    "contract": "tenancy",
    "purpose": "The venue, park and zone tree the access structure hangs from",
    "trigger": "onLoad",
    "provenance": "decided 29 September, VM close-out (venue management and configuration)"
   },
   {
    "operationId": "createOrgUnit",
    "contract": "tenancy",
    "purpose": "Add a venue, park or zone node",
    "trigger": "onAction",
    "provenance": "decided 29 September, VM close-out (venue management and configuration)",
    "invalidates": [
     "listOrgUnits"
    ]
   },
   {
    "operationId": "updateOrgUnit",
    "contract": "tenancy",
    "purpose": "Rename, move or deactivate a node",
    "trigger": "onAction",
    "provenance": "decided 29 September, VM close-out (venue management and configuration)",
    "invalidates": [
     "listOrgUnits"
    ]
   }
  ],
  "entryState": {
   "preloaded": [
    "VenueParkAccessStructureView.entityType"
   ],
   "params": [
    {
     "name": "orgUnitId",
     "from": "navigation"
    }
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-145",
   "workshopBoard": "wireframes/WS18 Access Control Board 1.dc.html#bo-145"
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
  "purposeNote": "Access-controlled zones can be configured and reorganized without software changes.",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Divide a venue into controlled access areas.",
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
    "trigger": "onAction"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-146",
   "workshopBoard": "wireframes/WS18 Access Control Board 1.dc.html#bo-146"
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
  "purposeNote": "An attraction can independently enforce admission requirements without changing the base ticket product.",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Configure attractions as access-controlled destinations.",
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
    "trigger": "onAction"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-147",
   "workshopBoard": "wireframes/WS18 Access Control Board 1.dc.html#bo-147"
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
  "purposeNote": "Operations can logically group multiple physical devices under one controlled access point.",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Additional settings) and no display directory — it is settings, not a population",
  "purpose": "Create the logical access points where validation occurs. An Access Point is different from a physical reader/device.",
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
   "board": "wireframes/P08 Venue Management.dc.html#bo-148",
   "workshopBoard": "wireframes/WS18 Access Control Board 1.dc.html#bo-148"
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
  "purposeNote": "Every physical lane can have independent configuration while inheriting settings from its parent access point.",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Configure individual physical gates/lanes.",
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
    "trigger": "onAction"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-149",
   "workshopBoard": "wireframes/WS18 Access Control Board 1.dc.html#bo-149"
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
  "purposeNote": "Access infrastructure can be configured and monitored geographically from a venue map.",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Create a graphical digital twin of the access-control environment.",
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
    "trigger": "onAction"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-150",
   "workshopBoard": "wireframes/WS18 Access Control Board 1.dc.html#bo-150"
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
  "purposeNote": "Multiple access-control devices can contribute to common occupancy and operational statistics.",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Group multiple access points for operational and capacity purposes.",
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
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Save access point group",
       "operation": "setAccessPointGroup",
       "permission": "ACCESS_POINT_CONFIGURE",
       "notes": "**The write behind Access Location Grouping** (BO-151): a named group of access points in one venue (e.g.",
       "provenance": "contract access.yaml PUT /access-point-groups"
      },
      {
       "kind": "destructiveButton",
       "label": "Delete access point group",
       "operation": "deleteAccessPointGroup",
       "permission": "ACCESS_POINT_CONFIGURE",
       "notes": "Deletes a group.",
       "provenance": "contract access.yaml DELETE /access-point-groups/{groupId}"
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
   },
   {
    "operationId": "setAccessPointGroup",
    "contract": "access",
    "purpose": "Create or replace an access-point group",
    "trigger": "onAction",
    "invalidates": [
     "listAccessLocationGrouping"
    ]
   },
   {
    "operationId": "deleteAccessPointGroup",
    "contract": "access",
    "purpose": "Delete an access-point group",
    "trigger": "onAction",
    "invalidates": [
     "listAccessLocationGrouping"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-151",
   "workshopBoard": "wireframes/WS18 Access Control Board 1.dc.html#bo-151"
  },
  "apisNote": "Regenerated 9 September 2026 from Access Control Module_Reference.pdf page 13. 0 of 0 labels bound to a contract property; 0 of 10 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "overlays": [
   {
    "id": "formSetAccessPointGroup",
    "component": "modal",
    "trigger": "Save access point group",
    "body": "**Collects what `setAccessPointGroup` sends before it is called.** Required: `id`, `venueId`, `name`, `scopePath`. Optional: `parentGroupId`, `accessPointIds`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "AccessAccessPointGroup",
    "confirm": {
     "label": "Save access point group",
     "operation": "setAccessPointGroup"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "venueId",
      "name",
      "scopePath",
      "parentGroupId",
      "accessPointIds"
     ]
    },
    "provenance": "contract access.yaml PUT /access-point-groups"
   },
   {
    "id": "confirmDeleteAccessPointGroup",
    "component": "confirmDialog",
    "trigger": "Delete access point group",
    "body": "**Names what `deleteAccessPointGroup` changes and what it leaves alone**, in the consequence rather than the verb. A record this affects should be identified in the dialog, not just counted.",
    "provenance": "contract access.yaml DELETE /access-point-groups/{groupId}"
   }
  ],
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
  "purposeNote": "Special-date access configurations can automatically replace standard operation without manual gate-by- gate changes.",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population",
  "purpose": "Allow access topology and operating behavior to change by date/time.",
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
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Save operating calendar entry",
       "operation": "setOperatingCalendarEntry",
       "permission": "ACCESS_POINT_CONFIGURE",
       "notes": "**The write behind Operating Calendar & Special Access Days** (BO-152) and Special Event, Free View & Alternative Admission (BO-222): one dated entry (a holiday, private event, free-entry day, special event and so on), whether tickets must be validated, and for a free-view or special-event window its admission type.",
       "provenance": "contract access.yaml PUT /operating-calendar-entries"
      },
      {
       "kind": "destructiveButton",
       "label": "Delete operating calendar entry",
       "operation": "deleteOperatingCalendarEntry",
       "permission": "ACCESS_POINT_CONFIGURE",
       "notes": "Deletes one calendar entry.",
       "provenance": "contract access.yaml DELETE /operating-calendar-entries/{entryId}"
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
   },
   {
    "operationId": "setOperatingCalendarEntry",
    "contract": "access",
    "purpose": "Create or replace an operating calendar entry",
    "trigger": "onAction",
    "invalidates": [
     "listOperatingCalendarSpecial"
    ]
   },
   {
    "operationId": "deleteOperatingCalendarEntry",
    "contract": "access",
    "purpose": "Delete an operating calendar entry",
    "trigger": "onAction",
    "invalidates": [
     "listOperatingCalendarSpecial"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-152",
   "workshopBoard": "wireframes/WS18 Access Control Board 1.dc.html#bo-152"
  },
  "apisNote": "Regenerated 9 September 2026 from Access Control Module_Reference.pdf page 13. 0 of 0 labels bound to a contract property; 10 of 18 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "overlays": [
   {
    "id": "formSetOperatingCalendarEntry",
    "component": "modal",
    "trigger": "Save operating calendar entry",
    "body": "**Collects what `setOperatingCalendarEntry` sends before it is called.** Required: `id`, `venueId`, `dayType`, `startsAt`, `endsAt`, `scopePath`. Optional: `name`, `ticketValidationRequired`, `admissionType`, `attractionValidation`, `manualAttendanceRequired`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "AccessOperatingCalendarEntry",
    "confirm": {
     "label": "Save operating calendar entry",
     "operation": "setOperatingCalendarEntry"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "venueId",
      "dayType",
      "startsAt",
      "endsAt",
      "scopePath",
      "name",
      "ticketValidationRequired",
      "admissionType",
      "attractionValidation",
      "manualAttendanceRequired"
     ]
    },
    "provenance": "contract access.yaml PUT /operating-calendar-entries"
   },
   {
    "id": "confirmDeleteOperatingCalendarEntry",
    "component": "confirmDialog",
    "trigger": "Delete operating calendar entry",
    "body": "**Names what `deleteOperatingCalendarEntry` changes and what it leaves alone**, in the consequence rather than the verb. A record this affects should be identified in the dialog, not just counted.",
    "provenance": "contract access.yaml DELETE /operating-calendar-entries/{entryId}"
   }
  ],
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
  "purposeNote": "No access topology enters production without validation, authorization, version tracking and rollback capability. Board 1 — Final Backend Navigation The left-side navigation for this board should therefore be:",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Final validation and controlled deployment of access configuration. Before publication, TICVAI automatically validates: orphan gates devices without access points access points without zones incorrect entry/exit direction missing offline configuration conflicting operating calendars inaccessible zones missing emergency configuration capacity inconsistencies missing reader/device association policy dependencies.",
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
      },
      {
       "kind": "secondaryButton",
       "label": "Rollback configuration version",
       "operation": "rollbackConfigurationVersion",
       "permission": "ACCESS_POINT_CONFIGURE",
       "notes": "**Rolls back the version in force** (Topology Validation & Publication, BO-153; rule sets roll back through `publishRuleConflictCheck` with step `rollBack`): the active version becomes `rolledBack` and the version it replaced (`previousVersionId`) becomes `active` again and is redistributed to the targets.",
       "provenance": "contract access.yaml POST /configuration-versions/{versionId}/rollback"
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
    "trigger": "onAction"
   },
   {
    "operationId": "rollbackConfigurationVersion",
    "contract": "access",
    "purpose": "Roll back an active access configuration version",
    "trigger": "onAction"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-153",
   "workshopBoard": "wireframes/WS18 Access Control Board 1.dc.html#bo-153"
  },
  "apisNote": "Regenerated 9 September 2026 from Access Control Module_Reference.pdf page 14. 0 of 0 labels bound to a contract property; 0 of 43 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "overlays": [
   {
    "id": "formRollbackConfigurationVersion",
    "component": "modal",
    "trigger": "Rollback configuration version",
    "body": "**Collects what `rollbackConfigurationVersion` sends before it is called.** Required: `reason`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Rollback configuration version",
     "operation": "rollbackConfigurationVersion"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "reason"
     ]
    },
    "provenance": "contract access.yaml POST /configuration-versions/{versionId}/rollback"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "versionId",
     "from": "navigation",
     "optional": true
    }
   ]
  },
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
 "createAccessPoint": {
  "method": "POST",
  "path": "/access-points",
  "contract": "access",
  "summary": "Create an access point",
  "permission": "ACCESS_POINT_CONFIGURE",
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
  "requestBody": "CreateAccessPointRequest",
  "responds": "AccessPoint"
 },
 "createOrgUnit": {
  "method": "POST",
  "path": "/org-units",
  "contract": "tenancy",
  "summary": "Create a scope node",
  "permission": "SCOPE_MANAGE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "brand",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "CreateScopeNodeRequest",
  "responds": "OrgUnit"
 },
 "deleteAccessPointGroup": {
  "method": "DELETE",
  "path": "/access-point-groups/{groupId}",
  "contract": "access",
  "summary": "Delete an access-point group",
  "permission": "ACCESS_POINT_CONFIGURE",
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
 "deleteOperatingCalendarEntry": {
  "method": "DELETE",
  "path": "/operating-calendar-entries/{entryId}",
  "contract": "access",
  "summary": "Delete an operating calendar entry",
  "permission": "ACCESS_POINT_CONFIGURE",
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
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "TopologyValidationPublicationInput",
  "responds": "TopologyValidationPublicationView"
 },
 "rollbackConfigurationVersion": {
  "method": "POST",
  "path": "/configuration-versions/{versionId}/rollback",
  "contract": "access",
  "summary": "Roll back an active access configuration version",
  "permission": "ACCESS_POINT_CONFIGURE",
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
  "responds": "AccessConfigurationVersion"
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
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
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
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "AccessControlGraphicalMapDesignerInput",
  "responds": "AccessControlGraphicalMapDesignerView"
 },
 "setAccessPointGroup": {
  "method": "PUT",
  "path": "/access-point-groups",
  "contract": "access",
  "summary": "Create or replace an access-point group",
  "permission": "ACCESS_POINT_CONFIGURE",
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
  "requestBody": "AccessAccessPointGroup",
  "responds": "AccessAccessPointGroup"
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
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
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
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "GateLaneConfigurationInput",
  "responds": "GateLaneConfigurationView"
 },
 "setOperatingCalendarEntry": {
  "method": "PUT",
  "path": "/operating-calendar-entries",
  "contract": "access",
  "summary": "Create or replace an operating calendar entry",
  "permission": "ACCESS_POINT_CONFIGURE",
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
  "requestBody": "AccessOperatingCalendarEntry",
  "responds": "AccessOperatingCalendarEntry"
 },
 "updateOrgUnit": {
  "method": "PATCH",
  "path": "/org-units/{orgUnitId}",
  "contract": "tenancy",
  "summary": "Rename or deactivate a scope node",
  "permission": "SCOPE_MANAGE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "brand",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "OrgUnit"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "AccessAccessPointGroup": {
  "type": "object",
  "x-ticvai-persistence": "access.access_point_group",
  "description": "A named group of access points in one venue (e.g. Main Entrance), optionally nested, whose counts roll up to a common occupancy (declared 29 September, data-model close-out DM1)",
  "required": [
   "id",
   "venueId",
   "name",
   "scopePath"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "name": {
    "type": "string",
    "description": "Group name, e.g. Main Entrance"
   },
   "parentGroupId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Enclosing group, for nested groups"
   },
   "accessPointIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    },
    "description": "Member access points (access.access_point)"
   },
   "scopePath": {
    "type": "string",
    "description": "ltree of the owning scope node (ADR-0005)"
   },
   "createdAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   },
   "updatedAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   }
  }
 },
 "AccessAreaZoneBuilderInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table covers these fields** — the closest is access.parking_facility at 14%, so this is not an update to anything the package stores today and no new table has been decided",
  "description": "**What Access Area & Zone Builder submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.\n\n**The pack defines this as a record**, under *Each zone receives* - one of only 13 drafted writes that does. That is the client writing a row rather than a screen, and it is where the table conversation should start.",
  "properties": {
   "name": {
    "type": "string",
    "description": "Zone name, e.g. VIP Lounge"
   },
   "venueId": {
    "type": "string",
    "description": "Venue the zone belongs to"
   },
   "zoneId": {
    "type": "string",
    "description": "Zone being written"
   },
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
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Credential classes admitted to the zone"
   },
   "parentId": {
    "type": "string",
    "description": "Park or zone this zone sits under in the venue structure"
   }
  },
  "x-ticvai-record-definition": "Each zone receives",
  "required": [
   "zoneId",
   "venueId",
   "name",
   "zoneType"
  ]
 },
 "AccessAreaZoneBuilderView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Access Area & Zone Builder displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "name": {
    "type": "string",
    "description": "Zone name, e.g. VIP Lounge"
   },
   "venueId": {
    "type": "string",
    "description": "Venue the zone belongs to"
   },
   "zoneId": {
    "type": "string",
    "description": "Zone being written"
   },
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
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Credential classes admitted to the zone"
   },
   "parentId": {
    "type": "string",
    "description": "Park or zone this zone sits under in the venue structure"
   }
  },
  "required": [
   "zoneId",
   "venueId",
   "name",
   "zoneType"
  ]
 },
 "AccessConfigurationVersion": {
  "type": "object",
  "x-ticvai-persistence": "access.configuration_version",
  "description": "One version of access configuration (a topology or a rule set) moving through simulate, validate, schedule, publish and roll back, with its target, schedule, validation findings and the previous version kept for rollback (declared 29 September, data-model close-out DM1)",
  "required": [
   "id",
   "configurationKind",
   "version",
   "status",
   "scopePath"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "venueId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "configurationKind": {
    "type": "string",
    "enum": [
     "topology",
     "ruleSet"
    ]
   },
   "version": {
    "type": "string",
    "description": "Version label"
   },
   "snapshot": {
    "type": "object",
    "description": "The configuration captured by this version, restored on rollback"
   },
   "status": {
    "type": "string",
    "enum": [
     "draft",
     "validated",
     "pendingApproval",
     "scheduled",
     "active",
     "inactive",
     "rolledBack"
    ],
    "default": "draft"
   },
   "lastStep": {
    "type": "string",
    "enum": [
     "simulate",
     "validate",
     "schedule",
     "publish",
     "rollBack"
    ],
    "nullable": true,
    "description": "Last lifecycle step run on this version"
   },
   "targetScope": {
    "type": "string",
    "enum": [
     "tenant",
     "venue",
     "park",
     "zone",
     "accessPoint",
     "selectedGates",
     "selectedDevices"
    ],
    "nullable": true,
    "description": "What the publication covers"
   },
   "targetIds": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "IDs within the target scope"
   },
   "publishMode": {
    "type": "string",
    "enum": [
     "now",
     "scheduled"
    ],
    "nullable": true
   },
   "scheduledAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "publishedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "validationIssues": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Blocking findings from pre-publication validation"
   },
   "conflicts": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Rule conflicts found by the conflict check (advisory)"
   },
   "previousVersionId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Version this one replaces, for rollback"
   },
   "approvalRequestId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Approval request raised in the approvals engine"
   },
   "createdByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "scopePath": {
    "type": "string",
    "description": "ltree of the owning scope node (ADR-0005)"
   },
   "createdAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   },
   "updatedAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
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
    "description": "Admissions per minute across the estate"
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
   "synchronizationStatus": {
    "type": "string",
    "enum": [
     "inSync",
     "syncPending",
     "syncFailed"
    ],
    "description": "Estate-wide offline sync state of devices"
   }
  }
 },
 "AccessControlGraphicalMapDesignerInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures",
  "description": "**What Access Control Graphical Map Designer submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "venueId": {
    "type": "string",
    "description": "Venue the map belongs to"
   },
   "mapId": {
    "type": "string",
    "description": "Map being written"
   },
   "sourceFileType": {
    "type": "string",
    "enum": [
     "cad",
     "pdf",
     "image",
     "venuePlan",
     "architecturalDrawing"
    ],
    "description": "Kind of drawing uploaded as the map base"
   },
   "sourceFile": {
    "type": "string",
    "description": "Reference to the uploaded drawing"
   }
  },
  "required": [
   "mapId",
   "venueId"
  ]
 },
 "AccessControlGraphicalMapDesignerView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Access Control Graphical Map Designer displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "venueId": {
    "type": "string",
    "description": "Venue the map belongs to"
   },
   "mapId": {
    "type": "string",
    "description": "Map being written"
   },
   "sourceFileType": {
    "type": "string",
    "enum": [
     "cad",
     "pdf",
     "image",
     "venuePlan",
     "architecturalDrawing"
    ],
    "description": "Kind of drawing uploaded as the map base"
   },
   "sourceFile": {
    "type": "string",
    "description": "Reference to the uploaded drawing"
   }
  },
  "required": [
   "mapId",
   "venueId"
  ]
 },
 "AccessLocationGroupingView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Access Location Grouping displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "name": {
    "type": "string",
    "description": "Group name, e.g. Main Entrance"
   },
   "groupId": {
    "type": "string"
   },
   "venueId": {
    "type": "string"
   },
   "parentGroupId": {
    "type": "string",
    "description": "Enclosing group, for nested groups"
   },
   "accessPointIds": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Access points whose counts roll up into this group"
   }
  },
  "required": [
   "groupId",
   "name"
  ]
 },
 "AccessOperatingCalendarEntry": {
  "type": "object",
  "x-ticvai-persistence": "access.operating_calendar_entry",
  "description": "One dated entry in a venue operating calendar (normal day, holiday, private event, free-entry day, special event and so on), with whether tickets must be validated. Merges access.special_admission_window, whose free-view and special-event windows are entries carrying an admission type (declared 29 September, data-model close-out DM1)",
  "required": [
   "id",
   "venueId",
   "dayType",
   "startsAt",
   "endsAt",
   "scopePath"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "dayType": {
    "type": "string",
    "enum": [
     "normalOperatingDay",
     "weekend",
     "holiday",
     "seasonalSchedule",
     "privateEvent",
     "freeEntryDay",
     "maintenancePeriod",
     "specialEvent",
     "ladiesOnlySession",
     "schoolGroupSession",
     "afterHoursEvent"
    ],
    "description": "Kind of calendar entry"
   },
   "name": {
    "type": "string",
    "nullable": true
   },
   "startsAt": {
    "type": "string",
    "format": "date-time"
   },
   "endsAt": {
    "type": "string",
    "format": "date-time"
   },
   "ticketValidationRequired": {
    "type": "boolean",
    "default": true,
    "description": "False on free-entry days"
   },
   "admissionType": {
    "type": "string",
    "enum": [
     "freeViewDay",
     "specialEvent"
    ],
    "nullable": true,
    "description": "Set on special admission windows only"
   },
   "attractionValidation": {
    "type": "boolean",
    "nullable": true,
    "description": "Special windows: attraction gates keep validating tickets"
   },
   "manualAttendanceRequired": {
    "type": "boolean",
    "nullable": true,
    "description": "Special windows: operator enters attendance count"
   },
   "scopePath": {
    "type": "string",
    "description": "ltree of the owning scope node (ADR-0005)"
   },
   "createdAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   },
   "updatedAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   }
  }
 },
 "AccessPoint": {
  "x-ticvai-persistence": "access.access_point",
  "type": "object",
  "required": [
   "id",
   "code",
   "name",
   "venueId",
   "operatingMode",
   "isActive"
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
   "externalCredentialSources": {
    "allOf": [
     {
      "$ref": "#/components/schemas/ExternalCredentialSourceList"
     }
    ],
    "description": "BL-108. **A hotel room card admitting a guest to a water park** — externally issued, and the platform validates it without having sold it.\n**The entitlement is created on first use, not on check-in.** A hotel with 400 rooms does not want 400 entitlements a night for guests who never visit.\n"
   },
   "scanAnomalyRules": {
    "allOf": [
     {
      "$ref": "#/components/schemas/ScanAnomalyRuleList"
     }
    ],
    "description": "BL-104. **Rule-based scan anomalies, separated from the parked model-based engine** — device sharing, simultaneous entries at two gates, an impossible walking time between them.\n**These are deterministic and need no model**, which is why they are here and not in `ai`: two entries eight seconds apart at gates four hundred metres apart is arithmetic.\n"
   },
   "operatingMode": {
    "allOf": [
     {
      "$ref": "#/components/schemas/AccessPointOperatingMode"
     }
    ],
    "default": "normal",
    "description": "**Set by the podium with `setTurnstileMode`, and it wins** (audit R221). BL-107 and BL-109. **A closed turnstile and one in emergency drop-arm mode look the same in the model and are opposite in meaning.** Closed refuses everybody; drop-arm lets everybody through, and it is the state that exists for an evacuation.\n**`podium` is a supervised validation position** — a member of staff directing a group through a lane, validating by eye against a list. It scans nothing and it is how school parties actually enter.\n**`freeFlow` counts without validating.** Useful at a free event, and a mode that must be visibly distinct from a broken reader.\n"
   },
   "vehicleLocationCapture": {
    "type": "boolean",
    "default": false,
    "description": "BL-023. **Nothing helped a guest find their vehicle.** Where the access point is a car park entry, the level and zone are captured against the visit so the app can answer it — **the guest who cannot find their car at 11pm is the last impression of the day.**\n"
   },
   "mode": {
    "allOf": [
     {
      "$ref": "#/components/schemas/TurnstileMode"
     }
    ],
    "nullable": true,
    "description": "Narrows `operatingMode` only: `freeRotation` or `closed` within `normal` or `podium`, null otherwise and whenever the turnstile validates in its fixed `direction` (audit R221).\n"
   },
   "direction": {
    "allOf": [
     {
      "$ref": "#/components/schemas/Direction"
     }
    ],
    "description": "**Fixed per access point** (audit R221): set in the back office by `createAccessPoint` and `updateAccessPoint`, never by the podium.\n"
   },
   "antiPassbackEnabled": {
    "type": "boolean"
   },
   "requiresExitBeforeReentry": {
    "type": "boolean",
    "default": false,
    "description": "Written by `createAccessPoint` and `updateAccessPoint`, and returned so the edit form reads back what it wrote."
   },
   "driver": {
    "type": "string",
    "nullable": true,
    "description": "Driver identifier for the controller behind this access point, as written by `createAccessPoint` and `updateAccessPoint`. Where the reader speaks OSDP the driver is standards-based; the controller layer above it is vendor-specific.\n"
   },
   "geofence": {
    "allOf": [
     {
      "$ref": "#/components/schemas/AccessPointGeofence"
     }
    ],
    "nullable": true,
    "description": "Written by `setAccessPointGeofence`; null until one is set. **One `jsonb` column on the access point row** (`access.access_point.geofence`), read with the point when a handheld validates against it.\n"
   },
   "isActive": {
    "type": "boolean"
   },
   "lastHeartbeatAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   }
  }
 },
 "AccessPointGeofence": {
  "type": "object",
  "x-ticvai-persistence-kind": "valueObject",
  "x-ticvai-persistence-column": "jsonb",
  "description": "Where a handheld may validate for one access point, and what happens outside it. The body of `setAccessPointGeofence` and the value of `AccessPoint.geofence`.\n",
  "required": [
   "enforcement"
  ],
  "properties": {
   "latitude": {
    "type": "number"
   },
   "longitude": {
    "type": "number"
   },
   "radiusMetres": {
    "type": "integer",
    "minimum": 5,
    "maximum": 5000
   },
   "enforcement": {
    "type": "string",
    "enum": [
     "off",
     "warn",
     "deny"
    ],
    "description": "`off` keeps the fence on record and checks nothing; `warn` lets a validation from outside the fence through with a warning; `deny` refuses it.\n"
   },
   "allowProximityBeacon": {
    "type": "boolean",
    "description": "Accept a BLE proximity assertion in place of GPS. Better indoors."
   }
  }
 },
 "AccessPointOperatingMode": {
  "type": "string",
  "description": "BL-107 and BL-109. **What the gate does, and what the podium sets** (`setTurnstileMode`, decided 28 September, audit R221). `closed` refuses everybody; `dropArm` lets everybody through and exists for an evacuation; `podium` is supervised validation by eye; `freeFlow` counts without validating; `maintenance` takes the lane out of use.\n",
  "enum": [
   "normal",
   "freeFlow",
   "dropArm",
   "closed",
   "podium",
   "maintenance"
  ]
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
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Access point IDs used to enter"
   },
   "exitPoints": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Access point IDs used to exit"
   },
   "fastPassSupport": {
    "type": "boolean",
    "description": "Fast Pass support"
   },
   "heightRestriction": {
    "type": "integer",
    "description": "Minimum rider height in cm, e.g. 130"
   },
   "ageRestriction": {
    "type": "integer",
    "description": "Minimum age in years"
   },
   "adultCompanionRequirement": {
    "type": "boolean",
    "description": "Adult companion requirement"
   },
   "membershipAccess": {
    "type": "boolean",
    "description": "Membership access"
   },
   "vipAccess": {
    "type": "boolean",
    "description": "VIP access"
   },
   "entitlementRequirement": {
    "type": "string",
    "description": "entitlement requirement"
   },
   "biometricRequirement": {
    "type": "boolean",
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
  "x-ticvai-record-definition": "For each attraction",
  "required": [
   "attractionId",
   "name",
   "venue"
  ]
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
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Access point IDs used to enter"
   },
   "exitPoints": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Access point IDs used to exit"
   },
   "fastPassSupport": {
    "type": "boolean",
    "description": "Fast Pass support"
   },
   "heightRestriction": {
    "type": "integer",
    "description": "Minimum rider height in cm, e.g. 130"
   },
   "ageRestriction": {
    "type": "integer",
    "description": "Minimum age in years"
   },
   "adultCompanionRequirement": {
    "type": "boolean",
    "description": "Adult companion requirement"
   },
   "membershipAccess": {
    "type": "boolean",
    "description": "Membership access"
   },
   "vipAccess": {
    "type": "boolean",
    "description": "VIP access"
   },
   "entitlementRequirement": {
    "type": "string",
    "description": "entitlement requirement"
   },
   "biometricRequirement": {
    "type": "boolean",
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
  "required": [
   "attractionId",
   "name",
   "venue"
  ]
 },
 "CreateAccessPointRequest": {
  "type": "object",
  "required": [
   "code",
   "name",
   "venueId",
   "direction"
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
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "direction": {
    "$ref": "#/components/schemas/Direction"
   },
   "antiPassbackEnabled": {
    "type": "boolean",
    "default": false
   },
   "requiresExitBeforeReentry": {
    "type": "boolean",
    "default": false
   },
   "driver": {
    "type": "string"
   }
  }
 },
 "CreateScopeNodeRequest": {
  "type": "object",
  "required": [
   "level",
   "parentId",
   "code",
   "name"
  ],
  "properties": {
   "level": {
    "$ref": "#/components/schemas/ScopeLevel"
   },
   "parentId": {
    "type": "string",
    "format": "uuid",
    "description": "Required for every level except tenant, which the cell creates at provisioning."
   },
   "code": {
    "type": "string",
    "maxLength": 64,
    "pattern": "^[a-z0-9_]+$",
    "description": "Becomes the final ltree segment. Immutable once created."
   },
   "name": {
    "type": "string",
    "maxLength": 200
   }
  }
 },
 "Direction": {
  "type": "string",
  "enum": [
   "entry",
   "exit",
   "reentry",
   "crossover"
  ]
 },
 "ExternalCredentialSourceList": {
  "type": "array",
  "x-ticvai-persistence-kind": "valueObject",
  "x-ticvai-persistence-column": "jsonb",
  "description": "**One `jsonb` column on the access point row** (`access.access_point.external_credential_sources`). Read with the access point when a credential is presented; a source is never queried on its own.\n",
  "items": {
   "type": "object",
   "properties": {
    "kind": {
     "type": "string",
     "enum": [
      "hotelRoomCard",
      "corporateBadge",
      "cityPass",
      "transitCard",
      "partnerToken"
     ]
    },
    "providerName": {
     "type": "string"
    },
    "endpoint": {
     "type": "string"
    },
    "credentialRef": {
     "type": "string"
    },
    "grantsProductId": {
     "type": "string",
     "format": "uuid"
    }
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
   "direction": {
    "type": "string",
    "enum": [
     "entry",
     "exit",
     "bidirectional"
    ],
    "description": "Lane direction, inherited from the access point unless set"
   },
   "reEntry": {
    "type": "boolean",
    "description": "Lane accepts re-entry scans"
   },
   "crossover": {
    "type": "boolean",
    "description": "Lane is a crossover lane between parks"
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
   "operationalMode": {
    "allOf": [
     {
      "$ref": "#/components/schemas/AccessPointOperatingMode"
     }
    ],
    "description": "Default operating mode of the lane, in the AccessPointOperatingMode vocabulary the podium sets (R221). Aligned (decided 29 September, writers pass): the old validation, freeSpin, emergencyDropArm, manual and countOnly are normal, freeFlow, dropArm, podium and freeFlow."
   },
   "laneSize": {
    "type": "string",
    "enum": [
     "standard",
     "wide"
    ],
    "description": "Wide lanes take buggies and wheelchairs"
   }
  },
  "required": [
   "gateId",
   "accessPoint"
  ]
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
   "direction": {
    "type": "string",
    "enum": [
     "entry",
     "exit",
     "bidirectional"
    ],
    "description": "Lane direction, inherited from the access point unless set"
   },
   "reEntry": {
    "type": "boolean",
    "description": "Lane accepts re-entry scans"
   },
   "crossover": {
    "type": "boolean",
    "description": "Lane is a crossover lane between parks"
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
   "operationalMode": {
    "allOf": [
     {
      "$ref": "#/components/schemas/AccessPointOperatingMode"
     }
    ],
    "description": "Default operating mode of the lane, in the AccessPointOperatingMode vocabulary the podium sets (R221). Aligned (decided 29 September, writers pass): the old validation, freeSpin, emergencyDropArm, manual and countOnly are normal, freeFlow, dropArm, podium and freeFlow."
   },
   "laneSize": {
    "type": "string",
    "enum": [
     "standard",
     "wide"
    ],
    "description": "Wide lanes take buggies and wheelchairs"
   }
  },
  "required": [
   "gateId",
   "accessPoint"
  ]
 },
 "OperatingCalendarSpecialAccessDaysView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Operating Calendar & Special Access Days displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "endsAt": {
    "type": "string",
    "format": "date-time"
   },
   "startsAt": {
    "type": "string",
    "format": "date-time"
   },
   "entryId": {
    "type": "string"
   },
   "dayType": {
    "type": "string",
    "enum": [
     "normalOperatingDay",
     "weekend",
     "holiday",
     "seasonalSchedule",
     "privateEvent",
     "freeEntryDay",
     "maintenancePeriod",
     "specialEvent",
     "ladiesOnlySession",
     "schoolGroupSession",
     "afterHoursEvent"
    ],
    "description": "Kind of calendar entry"
   },
   "venueId": {
    "type": "string"
   },
   "name": {
    "type": "string"
   },
   "ticketValidationRequired": {
    "type": "boolean",
    "description": "False on free-entry days"
   }
  },
  "required": [
   "entryId",
   "dayType",
   "startsAt",
   "endsAt"
  ]
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
 "ScanAnomalyRuleList": {
  "type": "array",
  "x-ticvai-persistence-kind": "valueObject",
  "x-ticvai-persistence-column": "jsonb",
  "description": "**One `jsonb` column on the access point row** (`access.access_point.scan_anomaly_rules`). Read with the access point at validation, and a rule is never queried on its own.\n",
  "items": {
   "type": "object",
   "properties": {
    "rule": {
     "type": "string",
     "enum": [
      "simultaneousEntry",
      "impossibleTravelTime",
      "rapidReentry",
      "sharedDevice",
      "velocityBreach"
     ]
    },
    "action": {
     "type": "string",
     "enum": [
      "log",
      "flag",
      "requireSupervisor",
      "deny"
     ]
    },
    "thresholdSeconds": {
     "type": "integer",
     "nullable": true
    }
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
 "TopologyValidationPublicationInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures",
  "description": "**What Topology Validation & Publication submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "publishMode": {
    "type": "string",
    "enum": [
     "now",
     "scheduled"
    ]
   },
   "configurationVersionId": {
    "type": "string",
    "description": "Topology version being published"
   },
   "targetScope": {
    "type": "string",
    "enum": [
     "tenant",
     "venue",
     "park",
     "zone",
     "accessPoint",
     "selectedGates",
     "selectedDevices"
    ],
    "description": "What the publication covers"
   },
   "targetIds": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "IDs within the target scope"
   },
   "scheduledAt": {
    "type": "string",
    "format": "date-time"
   },
   "validationIssues": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Blocking findings from pre-publication validation"
   }
  },
  "required": [
   "configurationVersionId",
   "targetScope",
   "publishMode"
  ]
 },
 "TopologyValidationPublicationView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Topology Validation & Publication displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "publishMode": {
    "type": "string",
    "enum": [
     "now",
     "scheduled"
    ]
   },
   "configurationVersionId": {
    "type": "string",
    "description": "Topology version being published"
   },
   "targetScope": {
    "type": "string",
    "enum": [
     "tenant",
     "venue",
     "park",
     "zone",
     "accessPoint",
     "selectedGates",
     "selectedDevices"
    ],
    "description": "What the publication covers"
   },
   "targetIds": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "IDs within the target scope"
   },
   "scheduledAt": {
    "type": "string",
    "format": "date-time"
   },
   "validationIssues": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Blocking findings from pre-publication validation"
   }
  },
  "required": [
   "configurationVersionId",
   "targetScope",
   "publishMode"
  ]
 },
 "TurnstileMode": {
  "type": "string",
  "description": "**Reduced to two values — decided 28 September, audit R221.** Entry, exit, re-entry and crossover were the access point's `Direction` under another name, and two fields that could disagree left the gate to guess. Direction is fixed per access point; within `normal` or `podium` operation the turnstile may only be let spin free or held closed.\n",
  "enum": [
   "freeRotation",
   "closed"
  ]
 },
 "VenueParkAccessStructureView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Venue & Park Access Structure displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "entityType": {
    "type": "string",
    "enum": [
     "venue",
     "park",
     "building",
     "eventSpace",
     "waterpark",
     "themePark",
     "museum",
     "arena",
     "stadium",
     "exhibition",
     "temporaryVenue"
    ],
    "description": "What kind of place this entity is"
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
    "description": "IANA time zone, e.g. Asia/Dubai"
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
    "type": "string",
    "description": "Reference to the offline validation policy the entity inherits"
   },
   "emergencyBehavior": {
    "type": "string",
    "description": "Emergency behavior"
   },
   "supportMultiParkEnvironments": {
    "type": "boolean",
    "description": "Support multi-park environments"
   }
  },
  "required": [
   "code",
   "name",
   "entityType"
  ]
 }
}
```
