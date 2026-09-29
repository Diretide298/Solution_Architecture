# WS166 — Seat Management Venue Mapping Reference v1.0 board 2

**10 screens · 10 operations · 14 schemas · 2 permissions**

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
  `CAPACITY_CONFIGURE, PRODUCT_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `BO-963` | Import Command Center | listDetail | 2 | 0 | — |
| `BO-964` | PDF & Image Import | listDetail | 2 | 0 | — |
| `BO-965` | SVG & CAD Import | listDetail | 2 | 0 | — |
| `BO-966` | CSV & Excel Import | listDetail | 2 | 0 | — |
| `BO-967` | AI Section Recognition | listDetail | 2 | 0 | — |
| `BO-968` | AI Row & Seat Recognition | listDetail | 2 | 0 | — |
| `BO-969` | AI Aisle, VIP & Accessibility | listDetail | 2 | 0 | — |
| `BO-970` | AI Numbering & Labeling | listDetail | 1 | 0 | — |
| `BO-971` | Validation & Correction | listDetail | 2 | 0 | — |
| `BO-972` | AI Venue Designer & Publish | listDetail | 2 | 0 | — |

## Thin screens in this batch

**BO-963, BO-964, BO-965, BO-966, BO-967, BO-968, BO-969, BO-970, BO-971, BO-972 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "BO-963",
  "name": "Import Command Center",
  "module": "Access & Venue",
  "requiresModule": "seating",
  "wave": 3,
  "source": {
   "pack": "Seat_Management_Venue_Mapping_Reference v1.0.pdf",
   "board": "2",
   "number": "01",
   "page": 10
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/import-command-center-bo-963",
   "component": "apps/venue-management-web/src/routes/access-venue/ImportCommandCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-100"
   ],
   "exitTo": [
    "BO-100",
    "BO-964",
    "BO-965",
    "BO-966",
    "BO-967",
    "BO-968",
    "BO-969",
    "BO-970",
    "BO-971",
    "BO-972"
   ],
   "transitions": [
    {
     "to": "BO-100",
     "trigger": "Back to Venue Home",
     "provenance": "structural — pack board 2 wiring, 19 September 2026",
     "back": true
    },
    {
     "to": "BO-964",
     "trigger": "PDF & Image Import",
     "provenance": "structural — pack board 2 wiring, 19 September 2026",
     "carries": [
      "jobId",
      "seatMapId"
     ]
    },
    {
     "to": "BO-965",
     "trigger": "SVG & CAD Import",
     "provenance": "structural — pack board 2 wiring, 19 September 2026",
     "carries": [
      "jobId",
      "seatMapId"
     ]
    },
    {
     "to": "BO-966",
     "trigger": "CSV & Excel Import",
     "provenance": "structural — pack board 2 wiring, 19 September 2026",
     "carries": [
      "jobId",
      "seatMapId"
     ]
    },
    {
     "to": "BO-967",
     "trigger": "AI Section Recognition",
     "provenance": "structural — pack board 2 wiring, 19 September 2026",
     "carries": [
      "importId",
      "seatMapId"
     ]
    },
    {
     "to": "BO-968",
     "trigger": "AI Row & Seat Recognition",
     "provenance": "structural — pack board 2 wiring, 19 September 2026",
     "carries": [
      "importId",
      "seatMapId"
     ]
    },
    {
     "to": "BO-969",
     "trigger": "AI Aisle, VIP & Accessibility",
     "provenance": "structural — pack board 2 wiring, 19 September 2026",
     "carries": [
      "importId",
      "seatMapId"
     ]
    },
    {
     "to": "BO-970",
     "trigger": "AI Numbering & Labeling",
     "provenance": "structural — pack board 2 wiring, 19 September 2026",
     "carries": [
      "seatMapId"
     ]
    },
    {
     "to": "BO-971",
     "trigger": "Validation & Correction",
     "provenance": "structural — pack board 2 wiring, 19 September 2026",
     "carries": [
      "importId",
      "seatMapId"
     ]
    },
    {
     "to": "BO-972",
     "trigger": "AI Venue Designer & Publish",
     "provenance": "structural — pack board 2 wiring, 19 September 2026",
     "carries": [
      "jobId",
      "seatMapId"
     ]
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Monitor every seat-map import from submission to publication. Show queued, processing, completed, failed and review-required jobs with source format, venue, owner and elapsed time. Display average confidence, issue counts, model version and jobs blocked by malware, unsupported content or validation failures. Support retry, cancel, duplicate, assign reviewer, open result and download controlled error reports. Retain source files, model/version, confidence, reviewer corrections and publication evidence; never allow AI output to bypass validation or approval. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 10"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 10"
   }
  ],
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "components": [
      {
       "kind": "detailPanel",
       "derived": true,
       "impliedBy": "getSeatMapImport",
       "notes": "One record, read-only."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The import list.",
   "error": "Could not load. Names which read failed and leaves the import untouched.",
   "emptyFirstRun": "No import yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the import are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getSeatMapImport",
    "contract": "seating",
    "purpose": "How the import went",
    "trigger": "onAction"
   },
   {
    "operationId": "getImportJob",
    "contract": "seating",
    "purpose": "Progress of a running import",
    "trigger": "onAction"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-963",
   "workshopBoard": "wireframes/WS141 Seat Management Venue Mapping Reference v1.0 Board 2.dc.html#bo-963"
  },
  "apisNote": "Regenerated 9 September 2026 from Seat_Management_Venue_Mapping_Reference v1.0.pdf page 10. 0 of 0 labels bound to a contract property; 0 of 10 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "importId",
     "from": "navigation"
    },
    {
     "name": "jobId",
     "from": "navigation"
    },
    {
     "name": "seatMapId",
     "from": "navigation"
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
 },
 {
  "id": "BO-964",
  "name": "PDF & Image Import",
  "module": "Access & Venue",
  "requiresModule": "seating",
  "wave": 3,
  "source": {
   "pack": "Seat_Management_Venue_Mapping_Reference v1.0.pdf",
   "board": "2",
   "number": "02",
   "page": 10
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/pdf-image-import-bo-964",
   "component": "apps/venue-management-web/src/routes/access-venue/PdfImageImport.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-963"
   ],
   "exitTo": [
    "BO-963"
   ],
   "transitions": [
    {
     "to": "BO-963",
     "trigger": "Back to Import Command Center",
     "provenance": "structural — pack board 2 wiring, 19 September 2026",
     "back": true,
     "carries": [
      "jobId",
      "seatMapId"
     ]
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Ingest PDF, PNG, JPG and supported scanned map sources. Provide drag-and-drop upload, page selection, preview, crop, rotation, de-skew, contrast and noise-reduction controls. Calibrate scale using known distance, dimensions or reference objects and capture venue orientation and focal point. Require file validation, malware scanning, size limits and a clear unsupported-or-low-quality recovery path. Retain source files, model/version, confidence, reviewer corrections and publication evidence; never allow AI output to bypass validation or approval. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 10"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 10"
   }
  ],
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "components": [
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "importSeatMap",
       "label": "Import seat map",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "detailPanel",
       "derived": true,
       "impliedBy": "getImportJob",
       "notes": "One record, read-only."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "importSeatMap"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The pdf image import list.",
   "error": "Could not load. Names which read failed and leaves the pdf image import untouched.",
   "emptyFirstRun": "No pdf image import yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the pdf image import are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "importSeatMap",
    "contract": "seating",
    "purpose": "Import from a plan or image",
    "trigger": "onAction",
    "invalidates": [
     "getImportJob"
    ]
   },
   {
    "operationId": "getImportJob",
    "contract": "seating",
    "purpose": "Watch it run",
    "trigger": "onAction"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-964",
   "workshopBoard": "wireframes/WS141 Seat Management Venue Mapping Reference v1.0 Board 2.dc.html#bo-964"
  },
  "apisNote": "Regenerated 9 September 2026 from Seat_Management_Venue_Mapping_Reference v1.0.pdf page 10. 0 of 0 labels bound to a contract property; 0 of 9 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "jobId",
     "from": "navigation"
    },
    {
     "name": "seatMapId",
     "from": "navigation"
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
 },
 {
  "id": "BO-965",
  "name": "SVG & CAD Import",
  "module": "Access & Venue",
  "requiresModule": "seating",
  "wave": 3,
  "source": {
   "pack": "Seat_Management_Venue_Mapping_Reference v1.0.pdf",
   "board": "2",
   "number": "03",
   "page": 10
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/svg-cad-import-bo-965",
   "component": "apps/venue-management-web/src/routes/access-venue/SvgCadImport.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-963"
   ],
   "exitTo": [
    "BO-963"
   ],
   "transitions": [
    {
     "to": "BO-963",
     "trigger": "Back to Import Command Center",
     "provenance": "structural — pack board 2 wiring, 19 September 2026",
     "back": true,
     "carries": [
      "jobId",
      "seatMapId"
     ]
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Convert vector and CAD geometry while preserving useful source layers. Support approved SVG, DXF and DWG workflows with unit, scale, origin, coordinate and rotation mapping. Map source layers to sections, rows, seats, aisles, stage, text, amenities, obstructions and ignored content. Simplify excessive geometry, close open paths, remove duplicates and preview the transformed result before recognition. Configuration Scope of Work | Version 1.0 10 Retain source files, model/version, confidence, reviewer corrections and publication evidence; never allow AI output to bypass validation or approval. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 10"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 10"
   }
  ],
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "components": [
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "importSeatGeometry",
       "label": "Import seat geometry",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "detailPanel",
       "derived": true,
       "impliedBy": "getImportJob",
       "notes": "One record, read-only."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "importSeatGeometry"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The svg cad import list.",
   "error": "Could not load. Names which read failed and leaves the svg cad import untouched.",
   "emptyFirstRun": "No svg cad import yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the svg cad import are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "importSeatGeometry",
    "contract": "seating",
    "purpose": "Import vector geometry",
    "trigger": "onAction",
    "invalidates": [
     "getImportJob"
    ]
   },
   {
    "operationId": "getImportJob",
    "contract": "seating",
    "purpose": "Watch it run",
    "trigger": "onAction"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-965",
   "workshopBoard": "wireframes/WS141 Seat Management Venue Mapping Reference v1.0 Board 2.dc.html#bo-965"
  },
  "apisNote": "Regenerated 9 September 2026 from Seat_Management_Venue_Mapping_Reference v1.0.pdf page 10. 0 of 0 labels bound to a contract property; 0 of 10 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "jobId",
     "from": "navigation"
    },
    {
     "name": "seatMapId",
     "from": "navigation"
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
 },
 {
  "id": "BO-966",
  "name": "CSV & Excel Import",
  "module": "Access & Venue",
  "requiresModule": "seating",
  "wave": 3,
  "source": {
   "pack": "Seat_Management_Venue_Mapping_Reference v1.0.pdf",
   "board": "2",
   "number": "04",
   "page": 11
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/csv-excel-import-bo-966",
   "component": "apps/venue-management-web/src/routes/access-venue/CsvExcelImport.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-963"
   ],
   "exitTo": [
    "BO-963"
   ],
   "transitions": [
    {
     "to": "BO-963",
     "trigger": "Back to Import Command Center",
     "provenance": "structural — pack board 2 wiring, 19 September 2026",
     "back": true,
     "carries": [
      "jobId",
      "seatMapId"
     ]
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Build maps or update seat master data from structured rows. Map columns for venue, level, section, row, seat, coordinates, type, category, price band, accessibility and status. Configure delimiter, header, encoding, sheet, data type, defaults and transformation rules with a sample-data preview. Detect missing identifiers, duplicates, invalid coordinates, inconsistent row sequences and unmapped values before import. Retain source files, model/version, confidence, reviewer corrections and publication evidence; never allow AI output to bypass validation or approval. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 11"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 11"
   }
  ],
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "components": [
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "importSeatManifest",
       "label": "Import seat manifest",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "detailPanel",
       "derived": true,
       "impliedBy": "getImportJob",
       "notes": "One record, read-only."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "importSeatManifest"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The csv excel import list.",
   "error": "Could not load. Names which read failed and leaves the csv excel import untouched.",
   "emptyFirstRun": "No csv excel import yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the csv excel import are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "importSeatManifest",
    "contract": "seating",
    "purpose": "Row and seat naming from a manifest",
    "trigger": "onAction",
    "invalidates": [
     "getImportJob"
    ]
   },
   {
    "operationId": "getImportJob",
    "contract": "seating",
    "purpose": "Watch it run",
    "trigger": "onAction"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-966",
   "workshopBoard": "wireframes/WS141 Seat Management Venue Mapping Reference v1.0 Board 2.dc.html#bo-966"
  },
  "apisNote": "Regenerated 9 September 2026 from Seat_Management_Venue_Mapping_Reference v1.0.pdf page 11. 0 of 0 labels bound to a contract property; 0 of 10 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "jobId",
     "from": "navigation"
    },
    {
     "name": "seatMapId",
     "from": "navigation"
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
 },
 {
  "id": "BO-967",
  "name": "AI Section Recognition",
  "module": "Access & Venue",
  "requiresModule": "seating",
  "wave": 3,
  "source": {
   "pack": "Seat_Management_Venue_Mapping_Reference v1.0.pdf",
   "board": "2",
   "number": "05",
   "page": 11
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/ai-section-recognition-bo-967",
   "component": "apps/venue-management-web/src/routes/access-venue/AiSectionRecognition.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-963"
   ],
   "exitTo": [
    "BO-963"
   ],
   "transitions": [
    {
     "to": "BO-963",
     "trigger": "Back to Import Command Center",
     "provenance": "structural — pack board 2 wiring, 19 September 2026",
     "back": true,
     "carries": [
      "importId",
      "seatMapId"
     ]
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Recognize venue levels, sections and standing zones from source geometry. Display detected boundaries, labels, hierarchy, capacity estimate and per-object confidence on the source preview. Allow accept, reject, merge, split, rename and redraw with AI correction suggestions and reason capture. Flag ambiguous, overlapping, disconnected or unlabelled areas and prevent silent assignment to the wrong level. Retain source files, model/version, confidence, reviewer corrections and publication evidence; never allow AI output to bypass validation or approval. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 11"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 11"
   }
  ],
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "components": [
      {
       "kind": "detailPanel",
       "derived": true,
       "impliedBy": "getSeatMapImport",
       "notes": "One record, read-only."
      },
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "validateSeatMap",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "validateSeatMap"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The section recognition list.",
   "error": "Could not load. Names which read failed and leaves the section recognition untouched.",
   "emptyFirstRun": "No section recognition yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the section recognition are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getSeatMapImport",
    "contract": "seating",
    "purpose": "What the import recognised",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "validateSeatMap",
    "contract": "seating",
    "purpose": "Correct and confirm",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-967",
   "workshopBoard": "wireframes/WS141 Seat Management Venue Mapping Reference v1.0 Board 2.dc.html#bo-967"
  },
  "apisNote": "Regenerated 9 September 2026 from Seat_Management_Venue_Mapping_Reference v1.0.pdf page 11. 0 of 0 labels bound to a contract property; 0 of 8 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "importId",
     "from": "navigation"
    },
    {
     "name": "seatMapId",
     "from": "navigation"
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
 },
 {
  "id": "BO-968",
  "name": "AI Row & Seat Recognition",
  "module": "Access & Venue",
  "requiresModule": "seating",
  "wave": 3,
  "source": {
   "pack": "Seat_Management_Venue_Mapping_Reference v1.0.pdf",
   "board": "2",
   "number": "06",
   "page": 11
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/ai-row-seat-recognition-bo-968",
   "component": "apps/venue-management-web/src/routes/access-venue/AiRowSeatRecognition.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-963"
   ],
   "exitTo": [
    "BO-963"
   ],
   "transitions": [
    {
     "to": "BO-963",
     "trigger": "Back to Import Command Center",
     "provenance": "structural — pack board 2 wiring, 19 September 2026",
     "back": true,
     "carries": [
      "importId",
      "seatMapId"
     ]
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Detect rows and individual seat positions at production scale. Recognize row curves, direction, gaps, seat dots, repeated symbols and wheelchair spaces with confidence heat maps. Allow threshold, gap, snap, spacing and symbol-class controls followed by selective reprocessing. Present detected counts by section and reconcile them with stated capacities, labels and expected patterns. Retain source files, model/version, confidence, reviewer corrections and publication evidence; never allow AI output to bypass validation or approval. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 11"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 11"
   }
  ],
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "components": [
      {
       "kind": "detailPanel",
       "derived": true,
       "impliedBy": "getSeatMapImport",
       "notes": "One record, read-only."
      },
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "updateSeats",
       "label": "Save seats",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "updateSeats"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The row seat recognition list.",
   "error": "Could not load. Names which read failed and leaves the row seat recognition untouched.",
   "emptyFirstRun": "No row seat recognition yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the row seat recognition are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getSeatMapImport",
    "contract": "seating",
    "purpose": "Rows and seats recognised",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "updateSeats",
    "contract": "seating",
    "purpose": "Correct them",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-968",
   "workshopBoard": "wireframes/WS141 Seat Management Venue Mapping Reference v1.0 Board 2.dc.html#bo-968"
  },
  "apisNote": "Regenerated 9 September 2026 from Seat_Management_Venue_Mapping_Reference v1.0.pdf page 11. 0 of 0 labels bound to a contract property; 0 of 9 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "importId",
     "from": "navigation"
    },
    {
     "name": "seatMapId",
     "from": "navigation"
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
 },
 {
  "id": "BO-969",
  "name": "AI Aisle, VIP & Accessibility",
  "module": "Access & Venue",
  "requiresModule": "seating",
  "wave": 3,
  "source": {
   "pack": "Seat_Management_Venue_Mapping_Reference v1.0.pdf",
   "board": "2",
   "number": "07",
   "page": 11
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/ai-aisle-vip-accessibility-bo-969",
   "component": "apps/venue-management-web/src/routes/access-venue/AiAisleVipAccessibility.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-963"
   ],
   "exitTo": [
    "BO-963"
   ],
   "transitions": [
    {
     "to": "BO-963",
     "trigger": "Back to Import Command Center",
     "provenance": "structural — pack board 2 wiring, 19 September 2026",
     "back": true,
     "carries": [
      "importId",
      "seatMapId"
     ]
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Recognize special geometry and operational attributes that affect seating. Detect aisles, entrances, exits, stages, VIP areas, suites, boxes, wheelchair positions and accessible routes. Show confidence, source evidence and conflicts where a detected object overlaps inventory or breaks route continuity. Allow the reviewer to change object class, boundary and attributes without restarting the full import. Configuration Scope of Work | Version 1.0 11 Retain source files, model/version, confidence, reviewer corrections and publication evidence; never allow AI output to bypass validation or approval. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 11"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 11"
   }
  ],
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "components": [
      {
       "kind": "detailPanel",
       "derived": true,
       "impliedBy": "getSeatMapImport",
       "notes": "One record, read-only."
      },
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "setMapZones",
       "label": "Save map zones",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "setMapZones"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The aisle vip accessibility list.",
   "error": "Could not load. Names which read failed and leaves the aisle vip accessibility untouched.",
   "emptyFirstRun": "No aisle vip accessibility yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the aisle vip accessibility are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getSeatMapImport",
    "contract": "seating",
    "purpose": "Aisles, VIP and accessible areas",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "setMapZones",
    "contract": "seating",
    "purpose": "Correct the zones",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-969",
   "workshopBoard": "wireframes/WS141 Seat Management Venue Mapping Reference v1.0 Board 2.dc.html#bo-969"
  },
  "apisNote": "Regenerated 9 September 2026 from Seat_Management_Venue_Mapping_Reference v1.0.pdf page 11. 0 of 0 labels bound to a contract property; 0 of 10 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "importId",
     "from": "navigation"
    },
    {
     "name": "seatMapId",
     "from": "navigation"
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
 },
 {
  "id": "BO-970",
  "name": "AI Numbering & Labeling",
  "module": "Access & Venue",
  "requiresModule": "seating",
  "wave": 3,
  "source": {
   "pack": "Seat_Management_Venue_Mapping_Reference v1.0.pdf",
   "board": "2",
   "number": "08",
   "page": 12
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/ai-numbering-labeling-bo-970",
   "component": "apps/venue-management-web/src/routes/access-venue/AiNumberingLabeling.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-963"
   ],
   "exitTo": [
    "BO-963"
   ],
   "transitions": [
    {
     "to": "BO-963",
     "trigger": "Back to Import Command Center",
     "provenance": "structural — pack board 2 wiring, 19 September 2026",
     "back": true,
     "carries": [
      "seatMapId"
     ]
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Generate consistent section, row and seat identifiers from recognized geometry. Configure alphabetic, numeric, alphanumeric, odd/even, continuous, reset-by-row and venue-specific numbering patterns. Preview before/after labels, direction, padding, skipped values, reserved labels and accessible-seat suffixes. Detect duplicates, gaps, reversals and conflicts with existing venue identifiers before applying changes. Retain source files, model/version, confidence, reviewer corrections and publication evidence; never allow AI output to bypass validation or approval. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 12"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 12"
   }
  ],
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "components": [
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "updateSeats",
       "label": "Save seats",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "updateSeats"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The numbering labeling list.",
   "error": "Could not load. Names which read failed and leaves the numbering labeling untouched.",
   "emptyFirstRun": "No numbering labeling yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the numbering labeling are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "updateSeats",
    "contract": "seating",
    "purpose": "Numbering and labelling",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-970",
   "workshopBoard": "wireframes/WS141 Seat Management Venue Mapping Reference v1.0 Board 2.dc.html#bo-970"
  },
  "apisNote": "Regenerated 9 September 2026 from Seat_Management_Venue_Mapping_Reference v1.0.pdf page 12. 0 of 0 labels bound to a contract property; 0 of 9 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "seatMapId",
     "from": "navigation"
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
 },
 {
  "id": "BO-971",
  "name": "Validation & Correction",
  "module": "Access & Venue",
  "requiresModule": "seating",
  "wave": 3,
  "source": {
   "pack": "Seat_Management_Venue_Mapping_Reference v1.0.pdf",
   "board": "2",
   "number": "09",
   "page": 12
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/validation-correction-bo-971",
   "component": "apps/venue-management-web/src/routes/access-venue/ValidationCorrection.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-963"
   ],
   "exitTo": [
    "BO-963"
   ],
   "transitions": [
    {
     "to": "BO-963",
     "trigger": "Back to Import Command Center",
     "provenance": "structural — pack board 2 wiring, 19 September 2026",
     "back": true,
     "carries": [
      "importId",
      "seatMapId"
     ]
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Provide one controlled workspace for resolving AI and import exceptions. Compare the source and generated map side by side with issue list, filters, severity and confidence. Offer manual draw, move, split, merge, add, delete, renumber, relabel and property-edit tools on a correction layer. Re-run selected recognizers, validate affected objects and preserve every AI suggestion, human edit and reviewer decision. Retain source files, model/version, confidence, reviewer corrections and publication evidence; never allow AI output to bypass validation or approval. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 12"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 12"
   }
  ],
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "components": [
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "validateSeatMap",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "detailPanel",
       "derived": true,
       "impliedBy": "getSeatMapImport",
       "notes": "One record, read-only."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "validateSeatMap"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The validation correction list.",
   "error": "Could not load. Names which read failed and leaves the validation correction untouched.",
   "emptyFirstRun": "No validation correction yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the validation correction are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "validateSeatMap",
    "contract": "seating",
    "purpose": "Validate the draft",
    "trigger": "onAction"
   },
   {
    "operationId": "getSeatMapImport",
    "contract": "seating",
    "purpose": "What the import produced",
    "trigger": "onAction"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-971",
   "workshopBoard": "wireframes/WS141 Seat Management Venue Mapping Reference v1.0 Board 2.dc.html#bo-971"
  },
  "apisNote": "Regenerated 9 September 2026 from Seat_Management_Venue_Mapping_Reference v1.0.pdf page 12. 0 of 0 labels bound to a contract property; 0 of 9 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "importId",
     "from": "navigation"
    },
    {
     "name": "seatMapId",
     "from": "navigation"
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
 },
 {
  "id": "BO-972",
  "name": "AI Venue Designer & Publish",
  "module": "Access & Venue",
  "requiresModule": "seating",
  "wave": 3,
  "source": {
   "pack": "Seat_Management_Venue_Mapping_Reference v1.0.pdf",
   "board": "2",
   "number": "10",
   "page": 12
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/ai-venue-designer-publish-bo-972",
   "component": "apps/venue-management-web/src/routes/access-venue/AiVenueDesignerPublish.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-963"
   ],
   "exitTo": [
    "BO-963"
   ],
   "transitions": [
    {
     "to": "BO-963",
     "trigger": "Back to Import Command Center",
     "provenance": "structural — pack board 2 wiring, 19 September 2026",
     "back": true,
     "carries": [
      "jobId",
      "seatMapId"
     ]
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Generate or refine a seat map from a natural-language brief and release the approved result. Accept venue type, dimensions, levels, target capacity, stage, section mix, accessibility and circulation requirements. Generate multiple explainable variants with capacity, sightline, accessible inventory and constraint summaries. Require full map validation, human review, approval and controlled one-click publication with version and rollback. Retain source files, model/version, confidence, reviewer corrections and publication evidence; never allow AI output to bypass validation or approval. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history. Configuration Scope of Work | Version 1.0 12 Board 3 - Layouts, Templates & Versions Figure 3. High-definition configuration board with all 10 screens. Visual reference: information architecture and configuration coverage; detailed production behavior is defined in the following scope. Configuration Scope of Work | Version 1.0 13",
  "gaps": [
   {
    "operation": null,
    "why": "**AI Venue Designer & Publish declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either the write operations are missing or this screen is a view of something another screen builds.",
    "source": "contract — the screen's declared operations"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 12"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 12"
   }
  ],
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "components": [
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "commitImportJob",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "commitImportJob"
      },
      {
       "kind": "publishGate",
       "label": "What publishing changes",
       "notes": "**Replaces the map every channel sells from.** Seats already sold keep their labels; seats that no longer exist in the new map are listed before this proceeds.",
       "provenance": "authored — required by check-screens, 19 September 2026"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The venue designer publish list.",
   "error": "Could not load. Names which read failed and leaves the venue designer publish untouched.",
   "emptyFirstRun": "No venue designer publish yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the venue designer publish are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "commitImportJob",
    "contract": "seating",
    "purpose": "Accept the draft",
    "trigger": "onAction",
    "invalidates": [
     "listSeatMaps"
    ]
   },
   {
    "operationId": "publishSeatMap",
    "contract": "seating",
    "purpose": "Publish",
    "trigger": "onAction",
    "invalidates": [
     "listSeatMaps",
     "getSeatMap"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-972",
   "workshopBoard": "wireframes/WS141 Seat Management Venue Mapping Reference v1.0 Board 2.dc.html#bo-972"
  },
  "apisNote": "Regenerated 9 September 2026 from Seat_Management_Venue_Mapping_Reference v1.0.pdf page 12. 0 of 0 labels bound to a contract property; 0 of 23 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "jobId",
     "from": "navigation"
    },
    {
     "name": "seatMapId",
     "from": "navigation"
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
 "commitImportJob": {
  "method": "POST",
  "path": "/seat-maps/{seatMapId}/import/{jobId}",
  "contract": "seating",
  "summary": "Apply a parsed import",
  "permission": "CAPACITY_CONFIGURE",
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
  "responds": "ImportJob"
 },
 "getImportJob": {
  "method": "GET",
  "path": "/seat-maps/{seatMapId}/import/{jobId}",
  "contract": "seating",
  "summary": "Import progress and findings",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "ImportJob"
 },
 "getSeatMapImport": {
  "method": "GET",
  "path": "/seat-map-imports/{importId}",
  "contract": "seating",
  "summary": "How the import went",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "SeatMapImportJob"
 },
 "importSeatGeometry": {
  "method": "POST",
  "path": "/seat-maps/{seatMapId}/import/geometry",
  "contract": "seating",
  "summary": "Import seat geometry from a plan",
  "permission": "CAPACITY_CONFIGURE",
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
  "requestBody": "ImportGeometryRequest",
  "responds": null
 },
 "importSeatManifest": {
  "method": "POST",
  "path": "/seat-maps/{seatMapId}/import/manifest",
  "contract": "seating",
  "summary": "Import the logical seat structure",
  "permission": "CAPACITY_CONFIGURE",
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
  "requestBody": "ImportManifestRequest",
  "responds": null
 },
 "importSeatMap": {
  "method": "POST",
  "path": "/seat-map-imports",
  "contract": "seating",
  "summary": "Import a seat map from a plan or a manifest",
  "permission": "CAPACITY_CONFIGURE",
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
  "responds": "SeatMapImportJob"
 },
 "publishSeatMap": {
  "method": "POST",
  "path": "/seat-maps/{seatMapId}/publish",
  "contract": "seating",
  "summary": "Validate and publish a seat map",
  "permission": "CAPACITY_CONFIGURE",
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
  "responds": "SeatMap"
 },
 "setMapZones": {
  "method": "PUT",
  "path": "/seat-maps/{seatMapId}/zones",
  "contract": "seating",
  "summary": "Standing areas, suites, stages and obstructions",
  "permission": "CAPACITY_CONFIGURE",
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
  "responds": "MapZone"
 },
 "updateSeats": {
  "method": "PATCH",
  "path": "/seat-maps/{seatMapId}/seats",
  "contract": "seating",
  "summary": "Bulk-amend seats",
  "permission": "CAPACITY_CONFIGURE",
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
  "requestBody": "BulkUpdateSeatsRequest",
  "responds": null
 },
 "validateSeatMap": {
  "method": "POST",
  "path": "/seat-maps/{seatMapId}/validate",
  "contract": "seating",
  "summary": "Run validation without publishing",
  "permission": "PRODUCT_VIEW",
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
  "responds": "ValidationReport"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "BulkUpdateSeatsRequest": {
  "x-ticvai-persistence": "none — request only",
  "type": "object",
  "required": [
   "selection"
  ],
  "properties": {
   "selection": {
    "type": "object",
    "description": "Seats to amend. Combine filters; an empty selection is rejected.",
    "properties": {
     "seatIds": {
      "type": "array",
      "items": {
       "type": "string"
      }
     },
     "sectionCodes": {
      "type": "array",
      "items": {
       "type": "string"
      }
     },
     "rowLabels": {
      "type": "array",
      "items": {
       "type": "string"
      }
     }
    }
   },
   "categoryId": {
    "type": "string",
    "format": "uuid"
   },
   "attribute": {
    "$ref": "#/components/schemas/SeatAttribute"
   },
   "isActive": {
    "type": "boolean"
   }
  }
 },
 "ImportGeometryRequest": {
  "x-ticvai-persistence": "none — request only",
  "type": "object",
  "required": [
   "fileReference",
   "format"
  ],
  "properties": {
   "fileReference": {
    "type": "string"
   },
   "format": {
    "type": "string",
    "enum": [
     "svgPlan",
     "pdfPlan"
    ]
   },
   "layerMapping": {
    "type": "object",
    "description": "Named layers in the source. Layer-aware extraction is far more reliable than shape recognition, so it is preferred wherever the source supports it — **and the client's amphitheatre file confirms the bet**: `VC-Seats`, `VC-wheelchairseating` and `VC-Steps` map straight onto the three roles below.\n**Each role takes a list, not a name** (CF-122). The same file carries two distinct layers both named `Layer 1`, steps drawn on both `steps` and `VC-Steps`, and AutoCAD's default `0`. A single string silently kept one and dropped the rest.\n**Names are decoded before matching.** PDF layer names arrive UTF-16BE and read as mojibake if taken as bytes, so a role that looks unmatched may simply be undecoded.\n",
    "properties": {
     "seatsLayer": {
      "type": "array",
      "items": {
       "type": "string"
      }
     },
     "accessibleSeatsLayer": {
      "type": "array",
      "items": {
       "type": "string"
      }
     },
     "sectionBoundaryLayer": {
      "type": "array",
      "items": {
       "type": "string"
      }
     },
     "stepsLayer": {
      "type": "array",
      "items": {
       "type": "string"
      }
     },
     "stageLayer": {
      "type": "array",
      "items": {
       "type": "string"
      }
     },
     "unmappedLayers": {
      "type": "array",
      "readOnly": true,
      "description": "Layers found in the source and claimed by no role. **Reported rather than ignored** — a plan with an unmapped layer is a plan where something was not extracted, and the operator is the only one who knows whether it mattered.\n",
      "items": {
       "type": "string"
      }
     }
    }
   },
   "digitNormalisation": {
    "type": "boolean",
    "default": true,
    "description": "**Section codes carrying Arabic-Indic digits never join to the manifest** (CF-122). `A١` and `A1` are the same section to a person and two sections to a string comparison, and the failure is silent — the row simply does not match.\nNormalised before the join. Disable only where a venue genuinely uses both forms as distinct codes, which would be its own problem.\n"
   },
   "joinOn": {
    "type": "string",
    "enum": [
     "sectionAndRow",
     "labelText",
     "ordinal"
    ],
    "default": "sectionAndRow",
    "description": "How plan geometry is matched to manifest seats."
   }
  }
 },
 "ImportJob": {
  "x-ticvai-persistence": "seating.import_job",
  "type": "object",
  "required": [
   "id",
   "seatMapId",
   "kind",
   "status",
   "createdAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "seatMapId": {
    "type": "string",
    "format": "uuid"
   },
   "kind": {
    "type": "string",
    "enum": [
     "manifest",
     "geometry"
    ]
   },
   "status": {
    "$ref": "#/components/schemas/ImportJobStatus"
   },
   "parsedSeatCount": {
    "type": "integer"
   },
   "matchedSeatCount": {
    "type": "integer",
    "description": "Geometry imports — seats successfully joined to the manifest."
   },
   "unmatchedSeatCount": {
    "type": "integer",
    "description": "Present in one source but not the other. A seat in the plan with no manifest entry is a finding, not a seat.\n"
   },
   "outcome": {
    "type": "string",
    "readOnly": true,
    "enum": [
     "parsed",
     "parsedWithFindings",
     "noSeatsFound",
     "noLayersMatched",
     "unreadable"
    ],
    "description": "**All four CF-122 defects failed silently — an import that found nothing reported success.** A job that parses zero seats is not a parsed job, and the operator was left to notice an empty seat map later.\n`noLayersMatched` is the specific one worth separating: **the file was readable and no role claimed a layer**, which almost always means the names needed decoding or a role needed a second entry rather than that the file was wrong.\n"
   },
   "layersFound": {
    "type": "array",
    "readOnly": true,
    "description": "Every layer name in the source, decoded. **Shown whether or not extraction worked**, so an operator can map a role by reading rather than by guessing.\n",
    "items": {
     "type": "string"
    }
   },
   "findings": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/ValidationFinding"
    }
   },
   "createdAt": {
    "type": "string",
    "format": "date-time"
   },
   "completedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   }
  }
 },
 "ImportJobStatus": {
  "type": "string",
  "enum": [
   "parsing",
   "previewReady",
   "committing",
   "committed",
   "failed"
  ]
 },
 "ImportManifestRequest": {
  "x-ticvai-persistence": "none — request only",
  "type": "object",
  "required": [
   "fileReference",
   "format",
   "columnMapping"
  ],
  "properties": {
   "fileReference": {
    "type": "string",
    "description": "Object storage reference. The file is not posted through this API."
   },
   "format": {
    "type": "string",
    "enum": [
     "csvManifest",
     "xlsxManifest"
    ]
   },
   "sheetName": {
    "type": "string",
    "description": "Spreadsheets only. Trailing spaces in sheet names are common — quote exactly."
   },
   "headerRow": {
    "type": "integer",
    "default": 1
   },
   "columnMapping": {
    "type": "object",
    "description": "Which column holds what. Required because manifests arrive with different headings from every venue.\n",
    "required": [
     "sectionColumn",
     "rowColumn",
     "seatColumn"
    ],
    "properties": {
     "sectionColumn": {
      "type": "string"
     },
     "rowColumn": {
      "type": "string"
     },
     "seatColumn": {
      "type": "string"
     },
     "categoryColumn": {
      "type": "string"
     },
     "attributeColumn": {
      "type": "string"
     }
    }
   },
   "replaceExisting": {
    "type": "boolean",
    "default": false,
    "description": "False merges. True replaces, and is refused where tickets are sold against the map.\n"
   }
  }
 },
 "MapZone": {
  "type": "object",
  "x-ticvai-persistence": "seating.zone",
  "description": "BL-166. **`seating` is strong on everything that is a seat and the map itself was only seats.**\n**A standing area is a capacity without individual seats**, and modelling it as seats means inventing seat numbers nobody prints and a guest cannot find. A suite is the opposite — one sellable unit containing many seats, sold whole.\nNon-sellable zones matter too: **a stage, an entry and a sightline obstruction are not inventory and they change what the seats beside them are worth.**\n",
  "required": [
   "id",
   "seatMapId",
   "kind",
   "name"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "seatMapId": {
    "type": "string",
    "format": "uuid"
   },
   "kind": {
    "type": "string",
    "enum": [
     "standing",
     "suite",
     "box",
     "lounge",
     "accessiblePlatform",
     "stage",
     "entry",
     "exit",
     "concourse",
     "obstruction",
     "camera",
     "aisle"
    ]
   },
   "name": {
    "type": "string"
   },
   "capacity": {
    "type": "integer",
    "nullable": true,
    "description": "**For a standing zone this is the inventory** — sold as a count rather than as seats. Null for a stage or an obstruction, which sell nothing.\n"
   },
   "seatCategoryId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "containsSeatIds": {
    "type": "array",
    "description": "For a suite or box. **Sold whole, so the seats inside are held together** — selling one seat of a suite is not a thing a venue does.\n",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "obstructsZoneIds": {
    "type": "array",
    "description": "What this blocks the view of. **A pillar is not inventory and it decides what the seats behind it are worth**, which is the only reason to draw it.\n",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "geometry": {
    "type": "string",
    "nullable": true
   }
  }
 },
 "Point": {
  "type": "object",
  "required": [
   "x",
   "y"
  ],
  "properties": {
   "x": {
    "type": "number"
   },
   "y": {
    "type": "number"
   }
  }
 },
 "SeatAttribute": {
  "type": "string",
  "description": "BL-168. **Extended from eight values on 18 August.** Amenity and view filters needed attributes the original set did not carry, and a guest filtering for *aisle seat with power* was filtering on something the model could not express.\n",
  "enum": [
   "standard",
   "accessible",
   "companion",
   "obstructedView",
   "restrictedLegroom",
   "premium",
   "houseSeat",
   "buffer",
   "aisle",
   "endOfRow",
   "extraLegroom",
   "powerOutlet",
   "tableService",
   "shaded",
   "covered",
   "nearExit",
   "nearAccessibleWc",
   "wheelchairTransfer",
   "limitedRecline",
   "sofa",
   "beanbag"
  ]
 },
 "SeatMap": {
  "x-ticvai-persistence": "seating.seat_map",
  "allOf": [
   {
    "$ref": "#/components/schemas/SeatMapSummary"
   },
   {
    "type": "object",
    "required": [
     "sections"
    ],
    "properties": {
     "description": {
      "type": "string",
      "nullable": true
     },
     "viewBox": {
      "type": "object",
      "description": "Coordinate space for rendering. Absent when there is no geometry.",
      "nullable": true,
      "properties": {
       "width": {
        "type": "number"
       },
       "height": {
        "type": "number"
       }
      }
     },
     "stagePosition": {
      "$ref": "#/components/schemas/Point"
     },
     "sections": {
      "type": "array",
      "items": {
       "$ref": "#/components/schemas/Section"
      }
     },
     "isActive": {
      "type": "boolean"
     }
    }
   }
  ]
 },
 "SeatMapImportJob": {
  "type": "object",
  "description": "**AI-assisted import from a PDF, an image or a spreadsheet** (21 August decision). A venue arriving with a printed plan and a seat manifest should not rebuild 396 rows by hand.\n\n**It proposes and a person accepts — it never publishes.** ADR-0020: a suggestion proposes, a person decides. An imported map lands as a draft with its confidence and whatever it could not read, because **a seat map wrong by two rows is worse than one that took an afternoon.**",
  "required": [
   "id",
   "status",
   "source"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "status": {
    "type": "string",
    "enum": [
     "queued",
     "reading",
     "proposed",
     "accepted",
     "rejected",
     "failed"
    ]
   },
   "source": {
    "type": "string",
    "enum": [
     "pdf",
     "image",
     "excel",
     "csv"
    ]
   },
   "seatMapId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The draft it produced, once it has one."
   },
   "seatsDetected": {
    "type": "integer",
    "nullable": true
   },
   "sectionsDetected": {
    "type": "integer",
    "nullable": true
   },
   "confidence": {
    "type": "number",
    "nullable": true,
    "minimum": 0,
    "maximum": 1
   },
   "unreadable": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "**What it could not read, named.** A blank list and a low confidence are different problems: the first is a bad scan, the second is a plan it half-understood."
   },
   "basis": {
    "type": "string",
    "enum": [
     "heuristic",
     "model"
    ],
    "description": "ADR-0020 — the same abstraction as every other suggestion."
   }
  }
 },
 "SeatMapSummary": {
  "x-ticvai-persistence": "seating.seat_map",
  "type": "object",
  "required": [
   "id",
   "name",
   "venueId",
   "status",
   "seatCount"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "name": {
    "type": "string"
   },
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "status": {
    "$ref": "#/components/schemas/SeatMapStatus"
   },
   "seatCount": {
    "type": "integer"
   },
   "sectionCount": {
    "type": "integer"
   },
   "hasGeometry": {
    "type": "boolean",
    "description": "False when only a manifest has been imported. Such a map can be sold from a list but not rendered.\n"
   },
   "publishedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   }
  }
 },
 "Section": {
  "x-ticvai-persistence": "seating.section",
  "type": "object",
  "required": [
   "code",
   "name",
   "rowCount",
   "seatCount"
  ],
  "properties": {
   "code": {
    "type": "string"
   },
   "name": {
    "type": "string"
   },
   "rowCount": {
    "type": "integer"
   },
   "seatCount": {
    "type": "integer"
   },
   "boundary": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/Point"
    },
    "description": "Polygon for rendering. Absent without geometry."
   },
   "viewAssetId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "x-ticvai-references": "assets.MediaAsset",
    "description": "**The view of the stage from this section, as a photo**, uploaded through `assets` like any other media (decided 29 September, rev 3 23SEP-14). Optional: where it is null the client renders the view from the imported geometry (the section `boundary`, the map's `stagePosition` and the seat positions), so a closer section shows a larger stage and fewer rows ahead. Set with `updateSeatMap` `sectionViews`, which is allowed on a published map because a photo does not change the map's shape.\n"
   },
   "rows": {
    "type": "array",
    "items": {
     "type": "object",
     "required": [
      "label",
      "seatCount"
     ],
     "properties": {
      "label": {
       "type": "string"
      },
      "seatCount": {
       "type": "integer"
      },
      "numberingDirection": {
       "type": "string",
       "enum": [
        "leftToRight",
        "rightToLeft"
       ],
       "description": "Which end row numbering starts from. Not recoverable from a manifest and must be stated — it determines whether a guest finds their seat.\n"
      }
     }
    }
   },
   "scopePath": {
    "type": "string",
    "description": "**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `venue` scope.**"
   }
  }
 },
 "ValidationFinding": {
  "x-ticvai-persistence": "none — computed",
  "type": "object",
  "required": [
   "kind",
   "severity",
   "message"
  ],
  "properties": {
   "kind": {
    "$ref": "#/components/schemas/ValidationFindingKind"
   },
   "severity": {
    "$ref": "#/components/schemas/ValidationSeverity"
   },
   "message": {
    "type": "string"
   },
   "sectionCode": {
    "type": "string",
    "nullable": true
   },
   "rowLabel": {
    "type": "string",
    "nullable": true
   },
   "seatNumbers": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "affectedCount": {
    "type": "integer"
   }
  }
 },
 "ValidationReport": {
  "x-ticvai-persistence": "none — computed",
  "type": "object",
  "required": [
   "seatMapId",
   "passed",
   "errorCount",
   "warningCount",
   "findings"
  ],
  "properties": {
   "seatMapId": {
    "type": "string",
    "format": "uuid"
   },
   "passed": {
    "type": "boolean",
    "description": "False when any finding has severity `error`."
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
     "$ref": "#/components/schemas/ValidationFinding"
    }
   }
  }
 }
}
```
