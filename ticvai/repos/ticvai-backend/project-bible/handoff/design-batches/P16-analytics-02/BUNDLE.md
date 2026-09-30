# P16-analytics-02 — P16 · Analytics (2 of 2)

**1 screens · 6 operations · 6 schemas · 2 permissions**

Platform P16 Venue Analytics · ships as **venue-management** ·
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
  `AI_CONFIGURE, AI_USE`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `ANL-071` | AI Maturity & Learning | listDetail | 6 | 2 | — |

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "ANL-071",
  "name": "AI Maturity & Learning",
  "module": "Analytics",
  "requiresModule": "ai",
  "wave": 3,
  "implementation": {
   "app": "venue-management-web",
   "route": "/analytics/ai-maturity",
   "component": "apps/venue-management-web/src/routes/analytics/AiMaturity.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ANL-010"
   ],
   "exitTo": [
    "ANL-010"
   ],
   "inferred": false,
   "transitions": [
    {
     "to": "ANL-010",
     "trigger": "Suggestions & Advice",
     "back": true,
     "provenance": "29 September pass (group A)"
    }
   ]
  },
  "notes": "**Added 29 September (AI functions review, the product owner's \"build it right, it gets more accurate with time\").** No customer is told an AI feature \"comes later\": every answer starts from a baseline and learns. This is where the venue sees how far each answer has come, gives the figures the baseline stands on, and imports its own history from the systems it used before TICVAI. Importing 12 months or more moves the answers it covers straight to Established.",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listAiCapabilityMaturity` reads a population (one row per question the AI answers) and the detail is the row",
  "purpose": "See where each AI answer stands, what it is based on and what it needs next; set the venue AI profile; import the venue's own history.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every AI answer, by stage",
       "bindsTo": "AiCapabilityMaturity",
       "columns": [
        "AiCapabilityMaturity.capabilityKey",
        "AiCapabilityMaturity.suggestionKind",
        "AiCapabilityMaturity.forecastDefinitionKey",
        "AiCapabilityMaturity.stage",
        "AiCapabilityMaturity.maturity",
        "AiCapabilityMaturity.since"
       ],
       "operation": "listAiCapabilityMaturity",
       "notes": "Stage badge, the \"Based on\" line, the share of own data and what the next stage needs.",
       "provenance": "29 September pass (group A)"
      },
      {
       "kind": "multiSelect",
       "label": "Stage",
       "operation": "listAiCapabilityMaturity",
       "provenance": "29 September pass (group A)"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "Venue AI profile",
       "bindsTo": "AiVenueSettings",
       "columns": [
        "AiVenueSettings.venueType",
        "AiVenueSettings.capacity",
        "AiVenueSettings.openingHours",
        "AiVenueSettings.typicalWeekdayAttendance",
        "AiVenueSettings.typicalWeekendAttendance",
        "AiVenueSettings.peakMonths",
        "AiVenueSettings.averageSpend",
        "AiVenueSettings.fnbAttachRate",
        "AiVenueSettings.staffProductivity"
       ],
       "operation": "getAiVenueSettings",
       "notes": "**The venue can correct its profile at any time** — the honest answer to a baseline that is wrong for an unusual venue in the first weeks.",
       "provenance": "29 September pass (group A)"
      },
      {
       "kind": "dataTable",
       "label": "History imports",
       "bindsTo": "AiHistoryImport",
       "columns": [
        "AiHistoryImport.dataKind",
        "AiHistoryImport.status",
        "AiHistoryImport.periodFrom",
        "AiHistoryImport.periodTo",
        "AiHistoryImport.monthsCovered",
        "AiHistoryImport.rowsLoaded",
        "AiHistoryImport.rowsRejected"
       ],
       "operation": "listVenueHistoryImports",
       "provenance": "29 September pass (group A)"
      },
      {
       "kind": "detailPanel",
       "label": "Import findings",
       "bindsTo": "AiHistoryImport.findings",
       "operation": "getVenueHistoryImport",
       "notes": "Each rejected row and why, so the venue can fix the export and import again.",
       "provenance": "29 September pass (group A)"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Save venue AI profile",
       "operation": "setAiVenueSettings",
       "provenance": "29 September pass (group A)"
      },
      {
       "kind": "secondaryButton",
       "label": "Import history",
       "operation": "importVenueHistory",
       "notes": "**Loaded into the AI data only, never the ledger**: an imported sale teaches the forecast and is never counted as revenue. The form says so.",
       "provenance": "29 September pass (group A)"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The stage of each answer; the venue profile resolves separately.",
   "error": "Could not load. **Every AI answer still works** — this page reports on them and changes none.",
   "emptyFirstRun": "**Nothing answered yet.** Every question starts at Starting from the venue AI profile and the starting pattern for the venue type. The action fills in the profile, or imports history.",
   "emptyNoResults": "No answer is at this stage. Names the filter and offers to clear it.",
   "emptyNoAccess": "You do not have AI permission at this venue. Names `AI_USE`, and `AI_CONFIGURE` for the profile and imports."
  },
  "apis": [
   {
    "operationId": "listAiCapabilityMaturity",
    "contract": "ai",
    "purpose": "Where each answer stands",
    "trigger": "onLoad",
    "provenance": "29 September pass (group A)"
   },
   {
    "operationId": "getAiVenueSettings",
    "contract": "ai",
    "purpose": "The venue AI profile",
    "trigger": "onLoad",
    "provenance": "29 September pass (group A)"
   },
   {
    "operationId": "setAiVenueSettings",
    "contract": "ai",
    "purpose": "Correct the venue AI profile",
    "trigger": "onAction",
    "invalidates": [
     "getAiVenueSettings",
     "listAiCapabilityMaturity"
    ],
    "provenance": "29 September pass (group A)"
   },
   {
    "operationId": "listVenueHistoryImports",
    "contract": "ai",
    "purpose": "Past imports and their result",
    "trigger": "onLoad",
    "provenance": "29 September pass (group A)"
   },
   {
    "operationId": "getVenueHistoryImport",
    "contract": "ai",
    "purpose": "One import's findings",
    "trigger": "onAction",
    "provenance": "29 September pass (group A)"
   },
   {
    "operationId": "importVenueHistory",
    "contract": "ai",
    "purpose": "Import the venue's own history",
    "trigger": "onAction",
    "invalidates": [
     "listVenueHistoryImports"
    ],
    "provenance": "29 September pass (group A)"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "venueId",
     "from": "session"
    },
    {
     "name": "importId",
     "from": "deepLink",
     "optional": true
    }
   ],
   "coldEntry": "A link from an import-finished notification opens the import named by `importId`; without it the page opens on the maturity list."
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P16 Venue Analytics.dc.html#anl-071"
  },
  "overlays": [
   {
    "id": "formSetAiVenueSettings",
    "component": "modal",
    "trigger": "Save venue AI profile",
    "body": "**Collects what `setAiVenueSettings` sends before it is called.** Required: `venueId`, `venueType`. Any figure left empty takes the starting pattern's default for the venue type.",
    "bindsTo": "AiVenueSettings",
    "confirm": {
     "label": "Save venue AI profile",
     "operation": "setAiVenueSettings"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "venueType",
      "isOutdoor",
      "capacity",
      "openingHours",
      "typicalWeekdayAttendance",
      "typicalWeekendAttendance",
      "peakMonths",
      "averageSpend",
      "fnbAttachRate",
      "staffProductivity"
     ]
    },
    "provenance": "29 September pass (group A)"
   },
   {
    "id": "formImportVenueHistory",
    "component": "modal",
    "trigger": "Import history",
    "body": "**Collects what `importVenueHistory` sends before it is called.** Required: `dataKind`, `assetId` (the uploaded export), `columnMapping`. Optional: `sourceSystem`, `dryRun` (check without loading). A second import of the same kind and period replaces the first.",
    "confirm": {
     "label": "Import history",
     "operation": "importVenueHistory"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "dataKind",
      "assetId",
      "columnMapping",
      "sourceSystem",
      "dryRun"
     ]
    },
    "provenance": "29 September pass (group A)"
   }
  ],
  "_platform": {
   "code": "P16",
   "formFactor": "web",
   "app": "venue-management-web",
   "operator": "venue",
   "name": "Venue Analytics — Cross-Domain Reporting",
   "shortName": "Venue Analytics",
   "audience": "staff",
   "offlineCapable": false,
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P08",
     "P12",
     "P13"
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
 "getAiVenueSettings": {
  "method": "GET",
  "path": "/venues/{venueId}/ai-settings",
  "contract": "ai",
  "summary": "The venue AI profile the baselines stand on",
  "permission": "AI_USE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "AiVenueSettings"
 },
 "getVenueHistoryImport": {
  "method": "GET",
  "path": "/history-imports/{importId}",
  "contract": "ai",
  "summary": "One history import, with its findings",
  "permission": "AI_USE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "AiHistoryImport"
 },
 "importVenueHistory": {
  "method": "POST",
  "path": "/venues/{venueId}/history-imports",
  "contract": "ai",
  "summary": "Import the venue's own historical exports for the AI baselines",
  "permission": "AI_CONFIGURE",
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
 "listAiCapabilityMaturity": {
  "method": "GET",
  "path": "/capability-maturity",
  "contract": "ai",
  "summary": "Where each AI answer stands on the way from baseline to learned",
  "permission": "AI_USE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "stage",
    "in": "query",
    "required": null
   },
   {
    "name": "capabilityKey",
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
 "listVenueHistoryImports": {
  "method": "GET",
  "path": "/venues/{venueId}/history-imports",
  "contract": "ai",
  "summary": "The venue's history imports",
  "permission": "AI_USE",
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
 "setAiVenueSettings": {
  "method": "PUT",
  "path": "/venues/{venueId}/ai-settings",
  "contract": "ai",
  "summary": "Set the venue AI profile",
  "permission": "AI_CONFIGURE",
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
  "requestBody": "AiVenueSettings",
  "responds": "AiVenueSettings"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "AiCapabilityMaturity": {
  "type": "object",
  "x-ticvai-persistence": "ai.capability_maturity",
  "description": "**The stage of each question the venue's AI answers** (29 September, AI functions review). Written by the nightly re-estimate; a stage change is a new row, so the page can show when each answer moved.",
  "required": [
   "capabilityKey",
   "stage"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "capabilityKey": {
    "type": "string"
   },
   "suggestionKind": {
    "allOf": [
     {
      "$ref": "#/components/schemas/SuggestionKind"
     }
    ],
    "nullable": true
   },
   "forecastDefinitionKey": {
    "type": "string",
    "nullable": true
   },
   "stage": {
    "type": "string",
    "enum": [
     "starting",
     "learning",
     "established",
     "learned"
    ]
   },
   "maturity": {
    "$ref": "#/components/schemas/AiMaturity"
   },
   "producerRef": {
    "type": "string",
    "description": "The producer and version answering now."
   },
   "since": {
    "type": "string",
    "format": "date-time"
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."
   }
  }
 },
 "AiHistoryImport": {
  "type": "object",
  "x-ticvai-persistence": "ai.history_import",
  "description": "**One import of a venue's own history** (29 September, AI functions review). A job: validated, then loaded into `ai.history_observation`, never into the ledger.",
  "required": [
   "id",
   "venueId",
   "dataKind",
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
   "dataKind": {
    "type": "string",
    "enum": [
     "attendance",
     "admissions",
     "ticketSales",
     "fnbSales",
     "retailSales",
     "queueReadings",
     "staffShifts"
    ]
   },
   "assetId": {
    "type": "string",
    "format": "uuid",
    "x-ticvai-references": "assets.media_asset"
   },
   "sourceSystem": {
    "type": "string",
    "nullable": true
   },
   "columnMapping": {
    "type": "object",
    "additionalProperties": {
     "type": "string"
    }
   },
   "dryRun": {
    "type": "boolean",
    "default": false
   },
   "status": {
    "type": "string",
    "enum": [
     "queued",
     "validating",
     "loading",
     "completed",
     "completedWithRejections",
     "failed"
    ],
    "readOnly": true
   },
   "periodFrom": {
    "type": "string",
    "format": "date",
    "nullable": true,
    "readOnly": true
   },
   "periodTo": {
    "type": "string",
    "format": "date",
    "nullable": true,
    "readOnly": true
   },
   "monthsCovered": {
    "type": "integer",
    "readOnly": true
   },
   "rowsRead": {
    "type": "integer",
    "readOnly": true
   },
   "rowsLoaded": {
    "type": "integer",
    "readOnly": true
   },
   "rowsRejected": {
    "type": "integer",
    "readOnly": true
   },
   "findings": {
    "type": "array",
    "readOnly": true,
    "items": {
     "type": "object",
     "properties": {
      "row": {
       "type": "integer"
      },
      "code": {
       "type": "string",
       "enum": [
        "badDate",
        "badNumber",
        "negativeValue",
        "duplicateDay",
        "unmappedColumn",
        "outOfRange"
       ]
      },
      "detail": {
       "type": "string"
      }
     }
    }
   },
   "requestedByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "x-ticvai-references": "identity.principal"
   },
   "createdAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   },
   "completedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."
   }
  }
 },
 "AiMaturity": {
  "type": "object",
  "x-ticvai-persistence": "none — embedded as jsonb on ai.suggestion and ai.forecast_version",
  "description": "**Where an answer stands, on every answer** (29 September, AI functions review; baseline then learn). The customer sees a stage badge and a \"Based on\" chip, never a bare percentage (design 5.6), and \"Limited historical data\" while the starting pattern carries more than half the weight.",
  "required": [
   "stage",
   "basedOn"
  ],
  "properties": {
   "stage": {
    "type": "string",
    "enum": [
     "starting",
     "learning",
     "established",
     "learned"
    ],
    "description": "`starting`: the baseline (venue AI settings, the starting pattern for the venue type, the UAE calendar, weather). `learning`: own data carries short-range patterns (about 4 weeks). `established`: own level and trend lead, the baseline fills gaps such as a holiday not yet seen (about 3 months, or at once with 12+ months imported). `learned`: a model trained on this tenant's data, promoted by an admin (AI-D16)."
   },
   "basedOn": {
    "type": "string",
    "description": "The \"Based on\" line, in words, e.g. *Based on: your venue profile, UAE calendar, weather, 23 days of your sales*. Always present."
   },
   "sources": {
    "type": "array",
    "items": {
     "type": "object",
     "required": [
      "source"
     ],
     "properties": {
      "source": {
       "type": "string",
       "enum": [
        "venueSettings",
        "startingPattern",
        "calendar",
        "weather",
        "bookingsOnHand",
        "ownHistory",
        "importedHistory",
        "configuration",
        "trainedModel"
       ]
      },
      "detail": {
       "type": "string",
       "nullable": true,
       "description": "e.g. *23 days*, *water park pattern v3*, *Eid al-Adha 2027*."
      },
      "observations": {
       "type": "integer",
       "nullable": true
      }
     }
    }
   },
   "ownDataShare": {
    "type": "number",
    "minimum": 0,
    "maximum": 1,
    "description": "The weight own data carries, `n / (k + n)`. Below 0.5 the answer is marked \"Limited historical data\"."
   },
   "limitedHistory": {
    "type": "boolean"
   },
   "nextStage": {
    "type": "object",
    "nullable": true,
    "description": "What the next stage needs, e.g. *8 more Saturdays of sales*, or *an admin promotion*.",
    "properties": {
     "stage": {
      "type": "string",
      "enum": [
       "learning",
       "established",
       "learned"
      ]
     },
     "needs": {
      "type": "string"
     },
     "expectedBy": {
      "type": "string",
      "format": "date",
      "nullable": true
     }
    }
   }
  }
 },
 "AiVenueSettings": {
  "type": "object",
  "x-ticvai-persistence": "ai.venue_settings",
  "description": "**The venue AI profile** (29 September, AI functions review): the figures a venue gives at onboarding so every data-driven answer is useful before it has history. One row per venue; configuration, not history. Defaults come from the starting pattern for `venueType`, which TICVAI writes from published sources and made-up example curves, **never from another tenant's data** (AI-D01, AIP-149).",
  "required": [
   "venueId",
   "venueType"
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
   "venueType": {
    "type": "string",
    "enum": [
     "waterPark",
     "themePark",
     "familyEntertainmentCentre",
     "museum",
     "arena",
     "zooAquarium",
     "other"
    ]
   },
   "isOutdoor": {
    "type": "boolean",
    "default": true,
    "description": "Outdoor venues take the summer-heat and weather effects."
   },
   "capacity": {
    "type": "integer",
    "minimum": 1,
    "nullable": true
   },
   "openingHours": {
    "type": "array",
    "description": "The usual week. Exceptions come from the venue calendar.",
    "items": {
     "type": "object",
     "properties": {
      "dayOfWeek": {
       "type": "integer",
       "minimum": 1,
       "maximum": 7
      },
      "opensAt": {
       "type": "string"
      },
      "closesAt": {
       "type": "string"
      }
     }
    }
   },
   "typicalWeekdayAttendance": {
    "type": "integer",
    "minimum": 0,
    "nullable": true
   },
   "typicalWeekendAttendance": {
    "type": "integer",
    "minimum": 0,
    "nullable": true
   },
   "peakMonths": {
    "type": "array",
    "items": {
     "type": "integer",
     "minimum": 1,
     "maximum": 12
    }
   },
   "averageSpend": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "nullable": true
   },
   "fnbAttachRate": {
    "type": "number",
    "minimum": 0,
    "maximum": 1,
    "nullable": true
   },
   "staffProductivity": {
    "type": "object",
    "additionalProperties": {
     "type": "number"
    },
    "description": "Per role, units per staff hour, e.g. `{\"cashier\": 40, \"gate\": 300}`. Defaults from the pattern."
   },
   "startingPatternKey": {
    "type": "string",
    "readOnly": true,
    "description": "The pattern and version in use, e.g. `waterPark@3`."
   },
   "updatedAt": {
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
 "SuggestionKind": {
  "type": "string",
  "description": "What is being suggested. **A closed set, and the reason it is closed is the swap.** Every entry here is a question a venue asks that a model could answer better than a rule — and each one starts as a heuristic and becomes a model when there is data.\n**Six of these were drawn as their own endpoints on the client F&B boards** — `suggestPrice`, `simulateScenario`, `simulateSlaPolicy`, `suggestRequisition`, `suggestReplenishment`, `publishDemandPlan`. **Building six endpoints means six places to change when a model changes**, and the model will change more often than the venue's question does.\n**What each kind is based on, and when the venue's own data takes over. Proposed, client to correct (decided 28 September, audit R213; re-read 29 September, AI functions review).** The figure after each rule is **the point where own data takes over from the baseline, not a refusal**: below it the kind answers from the baseline (venue AI settings, the starting pattern for the venue type, the UAE calendar, the weather) with `maturity.stage` `starting`, and between it and about three months it blends the two (`learning`). The day-one baseline per kind: `replenishment`, `requisition`, `prepPlan`, `staffing`, `demandForecast` and `scenario` from the baseline forecast (typical attendance from the venue AI settings x the venue-type month curve x the calendar x weather, bookings on hand as a floor); `menuEngineering` ranked by margin with popularity marked learning; `slaTarget` a standard default; `waitTime` people ahead / configured capacity; `upsell` the relationship map and business priority; `segmentation` known guest attributes; `anomaly` the venue's configured thresholds and actual against the forecast's low end; `sendTime` the channel's typical hour; `wasteRisk` shelf life and par against the forecast; `queueBalancing` configured capacity per queue. Only a missing setting refuses (422 `AiMissingSettingProblem`).\n- `price`: unit cost plus the category's target margin, held inside the price band. Minimum: a current cost, no history.\n- `replenishment`: par level minus on-hand plus expected use over the supplier lead time. Minimum: 14 days of stock movements.\n- `requisition`: the next service's prep-plan ingredient needs minus kitchen stock. Minimum: 14 days of sales.\n- `demandForecast`: the average of the same weekday over the last 8 weeks, adjusted by admissions already booked. Minimum: 8 weeks of sales.\n- `prepPlan`: forecast covers for the service times each item's share of the last 4 same weekdays. Minimum: 4 weeks of sales.\n- `menuEngineering`: each item placed by popularity against margin, over 90 days. Minimum: 90 days of sales.\n- `staffing`: forecast demand divided by the role's standard covers per staff hour. Minimum: 8 weeks of sales (the forecast it rests on).\n- `slaTarget`: the 80th percentile of actual times over the last 30 days. Minimum: 30 days of timed events.\n- `waitTime`: people ahead divided by the throughput of the last 30 minutes. Minimum: 30 minutes of throughput today.\n- `upsell`: the item most often bought with the basket's items over 90 days. Minimum: 90 days of orders.\n- `segmentation`: recency, frequency and spend scores over 12 months. Minimum: 90 days of orders.\n- `anomaly`: a value outside three standard deviations of the same weekday over 8 weeks. Minimum: 8 weeks of the measure.\n- `scenario`: the demand forecast re-run with the stated changes. Minimum: as `demandForecast`.\n- `sendTime` (added 29 September): per recipient, the hour inside `context.sendWindow` in which they have most often opened or clicked over the last 90 days (marketing-crm attribution touches), and where `context.channel` is `best`, the consented channel with the highest engagement. A recipient with fewer than three touches gets their segment's modal hour, and one with none the window's start. Asked with `subjectRef` a segment id or `context.subjectIds` (at most 10,000). `value` is `{recommendations: [{subjectId, sendAt, channel, basisTouches}]}`. Minimum: 90 days of message touches at the scope.\n- `wasteRisk` (added 29 September): per item at an outlet or store location, planned production and stock on hand minus forecast demand over the item's shelf life, plus batches expiring inside the horizon (`inventory.listExpiringBatches`). `value` is `{items: [{itemRef, quantityAtRisk, valueAtCost, expiresAt, recommendedAction (reducePrep, promote, transfer, useInRecipe), transferTo}]}`. Minimum: 14 days of recorded waste and of sales.\n- `queueBalancing` (added 29 September): per queue or attraction at `subjectRef` (a venue) over `horizon`, the forecast wait (the `queue` forecast definition) against throughput capacity, a recommended virtual-queue return-slot allocation by queue type, and guest redirection from over-used to under-used attractions. `value` is `{queues: [{queueId, forecastWaitMinutes, capacityPerHour, returnSlotsPerInterval, redirectTo}]}`. Minimum: 14 days of queue readings.\n- `itinerary` (added 29 September, MOB-6, guest-allowed): refines a `venue-map` visit plan the guest owns. `subjectRef` is the plan id; `value` is `{planId, baseVersion, changes, rationale}`, applied with `updateVisitPlan` as the guest. Minimum: none; the rules plan is the baseline. Every change names a point or performance of that day's venue only, rides, dining and retail alike (30 September client meeting, MoM 4.7).\n",
  "enum": [
   "price",
   "replenishment",
   "requisition",
   "demandForecast",
   "prepPlan",
   "menuEngineering",
   "staffing",
   "slaTarget",
   "waitTime",
   "upsell",
   "segmentation",
   "anomaly",
   "scenario",
   "sendTime",
   "wasteRisk",
   "queueBalancing",
   "itinerary"
  ]
 }
}
```
