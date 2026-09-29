# WS155 — Resource Management Configuration board 1

**10 screens · 26 operations · 17 schemas · 4 permissions**

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

- **Every control that can be refused must be gated.** 4 permissions apply here:
  `APPROVAL_CONFIGURE, RESOURCE_CONFIGURE, RESOURCE_MANAGE, RESOURCE_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `BO-854` | Resource Management Command Center | configEditor | 3 | 0 | — |
| `BO-855` | Resource Type Configuration | configEditor | 3 | 0 | — |
| `BO-856` | Resource Category Management | configEditor | 3 | 0 | — |
| `BO-857` | Resource Creation & Profile | configEditor | 5 | 0 | — |
| `BO-858` | Configurable Attribute Builder | configEditor | 2 | 0 | — |
| `BO-859` | Resource Hierarchy & Parent–Child Relationships | listDetail | 2 | 0 | — |
| `BO-860` | Resource Dependency Rules | listDetail | 2 | 0 | — |
| `BO-861` | Resource Package & Bundle Configuration | configEditor | 3 | 0 | — |
| `BO-862` | Multi-Venue Resource Assignment | listDetail | 2 | 0 | — |
| `BO-863` | Resource Lifecycle, Governance & Audit | configEditor | 6 | 0 | — |

## Thin screens in this batch

**BO-859, BO-860, BO-862 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "BO-854",
  "name": "Resource Management Command Center",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Resource_Management_Configuration_Reference.pdf",
   "board": "1",
   "number": "01",
   "page": 5
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/resource-management-command-center-bo-854",
   "component": "apps/venue-management-web/src/routes/rentals/ResourceManagementCommandCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-100"
   ],
   "exitTo": [
    "BO-100",
    "BO-855",
    "BO-856",
    "BO-857",
    "BO-858",
    "BO-859",
    "BO-860",
    "BO-861",
    "BO-862",
    "BO-863"
   ],
   "transitions": [
    {
     "to": "BO-100",
     "trigger": "Back to Venue Home",
     "provenance": "structural — pack board 1 wiring, 19 September 2026",
     "back": true
    },
    {
     "to": "BO-855",
     "trigger": "Resource Type Configuration",
     "provenance": "structural — pack board 1 wiring, 19 September 2026",
     "carries": [
      "resourceTypeId"
     ]
    },
    {
     "to": "BO-856",
     "trigger": "Resource Category Management",
     "provenance": "structural — pack board 1 wiring, 19 September 2026"
    },
    {
     "to": "BO-857",
     "trigger": "Resource Creation & Profile",
     "provenance": "structural — pack board 1 wiring, 19 September 2026",
     "carries": [
      "resourceId"
     ]
    },
    {
     "to": "BO-858",
     "trigger": "Configurable Attribute Builder",
     "provenance": "structural — pack board 1 wiring, 19 September 2026"
    },
    {
     "to": "BO-859",
     "trigger": "Resource Hierarchy & Parent–Child Relationships",
     "provenance": "structural — pack board 1 wiring, 19 September 2026",
     "carries": [
      "resourceId"
     ]
    },
    {
     "to": "BO-860",
     "trigger": "Resource Dependency Rules",
     "provenance": "structural — pack board 1 wiring, 19 September 2026",
     "carries": [
      "resourceId"
     ]
    },
    {
     "to": "BO-861",
     "trigger": "Resource Package & Bundle Configuration",
     "provenance": "structural — pack board 1 wiring, 19 September 2026"
    },
    {
     "to": "BO-862",
     "trigger": "Multi-Venue Resource Assignment",
     "provenance": "structural — pack board 1 wiring, 19 September 2026",
     "carries": [
      "resourceId"
     ]
    },
    {
     "to": "BO-863",
     "trigger": "Resource Lifecycle, Governance & Audit",
     "provenance": "structural — pack board 1 wiring, 19 September 2026",
     "carries": [
      "resourceId"
     ]
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Backend Configuration) and no display directory — it is settings, not a population",
  "purpose": "Provide administrators and operational managers with the main entry point for Resource Management and an instant overview of the organization's complete resource inventory.",
  "purposeNote": "Authorized users can view the complete permitted resource estate, filter and search resources, identify configuration issues, and launch governed resource-management actions directly from the command center.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Total active resources",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 5 §Backend Configuration"
      },
      {
       "kind": "selectField",
       "label": "Resources by type",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 5 §Backend Configuration"
      },
      {
       "kind": "selectField",
       "label": "Resources by venue",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 5 §Backend Configuration"
      },
      {
       "kind": "selectField",
       "label": "Available resources",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 5 §Backend Configuration"
      },
      {
       "kind": "selectField",
       "label": "Assigned resources",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 5 §Backend Configuration"
      },
      {
       "kind": "selectField",
       "label": "Reserved resources",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 5 §Backend Configuration"
      },
      {
       "kind": "selectField",
       "label": "Resources under maintenance",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 5 §Backend Configuration"
      },
      {
       "kind": "selectField",
       "label": "Suspended resources",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 5 §Backend Configuration"
      },
      {
       "kind": "selectField",
       "label": "Retired resources",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 5 §Backend Configuration"
      },
      {
       "kind": "textField",
       "label": "Resources with expiring certifications",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 5 §Backend Configuration"
      },
      {
       "kind": "textField",
       "label": "Resources with unresolved configuration issues",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 5 §Backend Configuration"
      },
      {
       "kind": "selectField",
       "label": "Recently created resources",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 5 §Backend Configuration"
      },
      {
       "kind": "selectField",
       "label": "Recently modified resources",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 5 §Backend Configuration"
      },
      {
       "kind": "selectField",
       "label": "Tenant",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 5 §Backend Configuration"
      },
      {
       "kind": "selectField",
       "label": "Business unit",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 5 §Backend Configuration"
      },
      {
       "kind": "selectField",
       "label": "Country",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 5 §Backend Configuration"
      },
      {
       "kind": "selectField",
       "label": "Venue",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 5 §Backend Configuration"
      },
      {
       "kind": "selectField",
       "label": "Resource type",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 5 §Backend Configuration"
      },
      {
       "kind": "selectField",
       "label": "Category",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 5 §Backend Configuration"
      },
      {
       "kind": "selectField",
       "label": "Status",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 5 §Backend Configuration"
      },
      {
       "kind": "selectField",
       "label": "Owner",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 5 §Backend Configuration"
      },
      {
       "kind": "selectField",
       "label": "Department",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 5 §Backend Configuration"
      },
      {
       "kind": "selectField",
       "label": "Tags",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 5 §Backend Configuration"
      },
      {
       "kind": "selectField",
       "label": "Availability status",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 5 §Backend Configuration"
      },
      {
       "kind": "selectField",
       "label": "Effective date",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 5 §Backend Configuration"
      },
      {
       "kind": "selectField",
       "label": "Create resource",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 5 §Backend Configuration"
      },
      {
       "kind": "selectField",
       "label": "Create resource type",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 5 §Backend Configuration"
      },
      {
       "kind": "selectField",
       "label": "Create category",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 5 §Backend Configuration"
      },
      {
       "kind": "selectField",
       "label": "Import resources",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 5 §Backend Configuration"
      },
      {
       "kind": "selectField",
       "label": "Duplicate resource",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 5 §Backend Configuration"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The resource configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the resource untouched.",
   "emptyFirstRun": "No resource configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [
   {
    "operationId": "listResources",
    "contract": "resources",
    "purpose": "Resources at this venue",
    "trigger": "onLoad"
   },
   {
    "operationId": "listResourceTypes",
    "contract": "resources",
    "purpose": "Resources by type",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "getResourceUtilisation",
    "contract": "resources",
    "purpose": "Utilisation across the estate",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-854",
   "workshopBoard": "wireframes/WS126 Resource Management Configuration Board 1.dc.html#bo-854"
  },
  "apisNote": "Regenerated 9 September 2026 from Resource_Management_Configuration_Reference.pdf page 5. 0 of 0 labels bound to a contract property; 39 of 49 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-855",
  "name": "Resource Type Configuration",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Resource_Management_Configuration_Reference.pdf",
   "board": "1",
   "number": "02",
   "page": 6
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/resource-type-configuration-bo-855",
   "component": "apps/venue-management-web/src/routes/rentals/ResourceTypeConfiguration.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-854"
   ],
   "exitTo": [
    "BO-854"
   ],
   "transitions": [
    {
     "to": "BO-854",
     "trigger": "Back to Resource Management Command Center",
     "provenance": "structural — pack board 1 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Backend Configuration) and no display directory — it is settings, not a population",
  "purpose": "Allow administrators to define the different classes of resources supported by the organization without requiring software development.",
  "purposeNote": "Administrators can create reusable resource types and define which operational capabilities and attributes apply to each type without code changes.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Staff",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 6 §Backend Configuration"
      },
      {
       "kind": "selectField",
       "label": "Instructor",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 6 §Backend Configuration"
      },
      {
       "kind": "selectField",
       "label": "Security personnel",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 6 §Backend Configuration"
      },
      {
       "kind": "selectField",
       "label": "Venue",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 6 §Backend Configuration"
      },
      {
       "kind": "selectField",
       "label": "Room",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 6 §Backend Configuration"
      },
      {
       "kind": "selectField",
       "label": "Hall",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 6 §Backend Configuration"
      },
      {
       "kind": "selectField",
       "label": "Area",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 6 §Backend Configuration"
      },
      {
       "kind": "selectField",
       "label": "Cabana",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 6 §Backend Configuration"
      },
      {
       "kind": "selectField",
       "label": "Equipment",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 6 §Backend Configuration"
      },
      {
       "kind": "selectField",
       "label": "Asset",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 6 §Backend Configuration"
      },
      {
       "kind": "selectField",
       "label": "Rental item",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 6 §Backend Configuration"
      },
      {
       "kind": "selectField",
       "label": "Vehicle",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 6 §Backend Configuration"
      },
      {
       "kind": "selectField",
       "label": "Locker",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 6 §Backend Configuration"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The resource type configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the resource type untouched.",
   "emptyFirstRun": "No resource type configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [
   {
    "operationId": "listResourceTypes",
    "contract": "resources",
    "purpose": "The classes defined so far",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "createResourceType",
    "contract": "resources",
    "purpose": "Define a class",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listResourceTypes"
    ]
   },
   {
    "operationId": "updateResourceType",
    "contract": "resources",
    "purpose": "Change a class",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listResourceTypes"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-855",
   "workshopBoard": "wireframes/WS126 Resource Management Configuration Board 1.dc.html#bo-855"
  },
  "apisNote": "Regenerated 9 September 2026 from Resource_Management_Configuration_Reference.pdf page 6. 0 of 0 labels bound to a contract property; 13 of 42 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "resourceTypeId",
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
  "id": "BO-856",
  "name": "Resource Category Management",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Resource_Management_Configuration_Reference.pdf",
   "board": "1",
   "number": "03",
   "page": 7
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/resource-category-management-bo-856",
   "component": "apps/venue-management-web/src/routes/rentals/ResourceCategoryManagement.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-854"
   ],
   "exitTo": [
    "BO-854"
   ],
   "transitions": [
    {
     "to": "BO-854",
     "trigger": "Back to Resource Management Command Center",
     "provenance": "structural — pack board 1 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Backend Configuration) and no display directory — it is settings, not a population",
  "purpose": "Provide a flexible classification structure beneath resource types so resources can be organized, searched, reported, and governed consistently.",
  "purposeNote": "Resources can be grouped into configurable hierarchical categories and subcategories that can subsequently be used throughout search, scheduling, reporting, automation, and integrations.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Equipment",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 7 §Backend Configuration"
      },
      {
       "kind": "selectField",
       "label": "AV",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 7 §Backend Configuration"
      },
      {
       "kind": "selectField",
       "label": "Lighting",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 7 §Backend Configuration"
      },
      {
       "kind": "selectField",
       "label": "Sound",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 7 §Backend Configuration"
      },
      {
       "kind": "selectField",
       "label": "Furniture",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 7 §Backend Configuration"
      },
      {
       "kind": "selectField",
       "label": "Staff",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 7 §Backend Configuration"
      },
      {
       "kind": "selectField",
       "label": "Instructor",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 7 §Backend Configuration"
      },
      {
       "kind": "selectField",
       "label": "Operations",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 7 §Backend Configuration"
      },
      {
       "kind": "selectField",
       "label": "Security",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 7 §Backend Configuration"
      },
      {
       "kind": "selectField",
       "label": "Technical Crew",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 7 §Backend Configuration"
      },
      {
       "kind": "selectField",
       "label": "Rental",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 7 §Backend Configuration"
      },
      {
       "kind": "selectField",
       "label": "Towels",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 7 §Backend Configuration"
      },
      {
       "kind": "selectField",
       "label": "Strollers",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 7 §Backend Configuration"
      },
      {
       "kind": "selectField",
       "label": "Lockers",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 7 §Backend Configuration"
      },
      {
       "kind": "selectField",
       "label": "Cabanas",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 7 §Backend Configuration"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The resource category configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the resource category untouched.",
   "emptyFirstRun": "No resource category configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [
   {
    "operationId": "listResourceCategories",
    "contract": "resources",
    "purpose": "The classification tree",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "createResourceCategory",
    "contract": "resources",
    "purpose": "Add a category",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listResourceCategories"
    ]
   },
   {
    "operationId": "updateResourceCategory",
    "contract": "resources",
    "purpose": "Change a category",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listResourceCategories"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-856",
   "workshopBoard": "wireframes/WS126 Resource Management Configuration Board 1.dc.html#bo-856"
  },
  "apisNote": "Regenerated 9 September 2026 from Resource_Management_Configuration_Reference.pdf page 7. 0 of 0 labels bound to a contract property; 15 of 35 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "categoryId",
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
  "id": "BO-857",
  "name": "Resource Creation & Profile",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Resource_Management_Configuration_Reference.pdf",
   "board": "1",
   "number": "04",
   "page": 8
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/resource-creation-profile-bo-857",
   "component": "apps/venue-management-web/src/routes/rentals/ResourceCreationProfile.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-854"
   ],
   "exitTo": [
    "BO-854"
   ],
   "transitions": [
    {
     "to": "BO-854",
     "trigger": "Back to Resource Management Command Center",
     "provenance": "structural — pack board 1 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Backend Configuration; Operational Configuration) and no display directory — it is settings, not a population",
  "purpose": "Provide the principal workspace for creating and maintaining an individual resource.",
  "purposeNote": "Authorized users can create and maintain a complete resource profile, save it as draft, validate its configuration, submit it through governance, and activate it for downstream use.",
  "gaps": [
   {
    "operation": null,
    "why": "**Resource Creation & Profile declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either the write operations are missing or this screen is a view of something another screen builds.",
    "source": "contract — the screen's declared operations"
   }
  ],
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Active status",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 8 §Operational Configuration"
      },
      {
       "kind": "selectField",
       "label": "Reservable status",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 8 §Operational Configuration"
      },
      {
       "kind": "selectField",
       "label": "Rentable status",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 8 §Operational Configuration"
      },
      {
       "kind": "selectField",
       "label": "Capacity",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 8 §Operational Configuration"
      },
      {
       "kind": "selectField",
       "label": "Unit of measure",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 8 §Operational Configuration"
      },
      {
       "kind": "selectField",
       "label": "Customer selectable",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 8 §Operational Configuration"
      },
      {
       "kind": "selectField",
       "label": "Priority",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 8 §Operational Configuration"
      },
      {
       "kind": "selectField",
       "label": "Availability mode",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 8 §Operational Configuration"
      },
      {
       "kind": "selectField",
       "label": "Scheduling mode",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 8 §Operational Configuration"
      },
      {
       "kind": "selectField",
       "label": "Default duration",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 8 §Operational Configuration"
      },
      {
       "kind": "selectField",
       "label": "Minimum booking duration",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 8 §Operational Configuration"
      },
      {
       "kind": "selectField",
       "label": "Maximum booking duration",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 8 §Operational Configuration"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The resource creation profile configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the resource creation profile untouched.",
   "emptyFirstRun": "No resource creation profile configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [
   {
    "operationId": "getResource",
    "contract": "resources",
    "purpose": "The resource being edited",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "createResource",
    "contract": "resources",
    "purpose": "Create it",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listResources"
    ]
   },
   {
    "operationId": "updateResource",
    "contract": "resources",
    "purpose": "Save the profile",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "getResource",
     "listResources"
    ]
   },
   {
    "operationId": "setResourceLifecycleState",
    "contract": "resources",
    "purpose": "Submit, activate, suspend or retire",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "getResource",
     "listResources",
     "getResourceAuditTrail"
    ]
   },
   {
    "operationId": "cloneResource",
    "contract": "resources",
    "purpose": "Copy it",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listResources"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-857",
   "workshopBoard": "wireframes/WS126 Resource Management Configuration Board 1.dc.html#bo-857"
  },
  "apisNote": "Regenerated 9 September 2026 from Resource_Management_Configuration_Reference.pdf page 8. 0 of 0 labels bound to a contract property; 12 of 63 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "resourceId",
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
  "id": "BO-858",
  "name": "Configurable Attribute Builder",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Resource_Management_Configuration_Reference.pdf",
   "board": "1",
   "number": "05",
   "page": 10
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/configurable-attribute-builder-bo-858",
   "component": "apps/venue-management-web/src/routes/rentals/ConfigurableAttributeBuilder.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-854"
   ],
   "exitTo": [
    "BO-854"
   ],
   "transitions": [
    {
     "to": "BO-854",
     "trigger": "Back to Resource Management Command Center",
     "provenance": "structural — pack board 1 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Backend Configuration) and no display directory — it is settings, not a population",
  "purpose": "Allow customers to extend resource records with their own attributes without changing the core application.",
  "purposeNote": "Administrators can extend resource records with reusable, validated, type-specific attributes without requiring application development.",
  "gaps": [
   {
    "operation": null,
    "why": "**Configurable Attribute Builder declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either the write operations are missing or this screen is a view of something another screen builds.",
    "source": "contract — the screen's declared operations"
   }
  ],
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Skill level",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 10 §Backend Configuration"
      },
      {
       "kind": "selectField",
       "label": "Height",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 10 §Backend Configuration"
      },
      {
       "kind": "selectField",
       "label": "Weight",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 10 §Backend Configuration"
      },
      {
       "kind": "selectField",
       "label": "Seating capacity",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 10 §Backend Configuration"
      },
      {
       "kind": "selectField",
       "label": "Equipment model",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 10 §Backend Configuration"
      },
      {
       "kind": "selectField",
       "label": "Serial number",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 10 §Backend Configuration"
      },
      {
       "kind": "selectField",
       "label": "Size",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 10 §Backend Configuration"
      },
      {
       "kind": "selectField",
       "label": "Manufacturer",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 10 §Backend Configuration"
      },
      {
       "kind": "selectField",
       "label": "Color",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 10 §Backend Configuration"
      },
      {
       "kind": "selectField",
       "label": "Power requirement",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 10 §Backend Configuration"
      },
      {
       "kind": "selectField",
       "label": "Warranty expiry",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 10 §Backend Configuration"
      },
      {
       "kind": "selectField",
       "label": "Maximum occupancy",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 10 §Backend Configuration"
      },
      {
       "kind": "selectField",
       "label": "Language",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 10 §Backend Configuration"
      },
      {
       "kind": "selectField",
       "label": "Certification level",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 10 §Backend Configuration"
      },
      {
       "kind": "selectField",
       "label": "Rental condition",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 10 §Backend Configuration"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The configurable attribute configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the configurable attribute untouched.",
   "emptyFirstRun": "No configurable attribute configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [
   {
    "operationId": "listResourceAttributes",
    "contract": "resources",
    "purpose": "Attributes defined so far",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "createResourceAttribute",
    "contract": "resources",
    "purpose": "Define an attribute",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listResourceAttributes"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-858",
   "workshopBoard": "wireframes/WS126 Resource Management Configuration Board 1.dc.html#bo-858"
  },
  "apisNote": "Regenerated 9 September 2026 from Resource_Management_Configuration_Reference.pdf page 10. 0 of 0 labels bound to a contract property; 15 of 52 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-859",
  "name": "Resource Hierarchy & Parent–Child Relationships",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Resource_Management_Configuration_Reference.pdf",
   "board": "1",
   "number": "06",
   "page": 11
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/resource-hierarchy-parent-child-relationships-bo-859",
   "component": "apps/venue-management-web/src/routes/rentals/ResourceHierarchyParentChildRelationships.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-854"
   ],
   "exitTo": [
    "BO-854"
   ],
   "transitions": [
    {
     "to": "BO-854",
     "trigger": "Back to Resource Management Command Center",
     "provenance": "structural — pack board 1 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Represent physical and operational relationships between resources.",
  "purposeNote": "Administrators can create and manage multi-level resource hierarchies, and the platform validates those relationships before they are used operationally.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Resource_Management_Configuration_Reference.pdf, page 11"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Resource_Management_Configuration_Reference.pdf, page 11"
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
       "impliedBy": "getResourceHierarchy",
       "notes": "One record, read-only."
      },
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "setResourceHierarchy",
       "label": "Save resource hierarchy",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "setResourceHierarchy"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The resource hierarchy parent–child list.",
   "error": "Could not load. Names which read failed and leaves the resource hierarchy parent–child untouched.",
   "emptyFirstRun": "No resource hierarchy parent–child yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the resource hierarchy parent–child are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getResourceHierarchy",
    "contract": "resources",
    "purpose": "The tree",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "setResourceHierarchy",
    "contract": "resources",
    "purpose": "Re-parent or attach",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "getResourceHierarchy"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-859",
   "workshopBoard": "wireframes/WS126 Resource Management Configuration Board 1.dc.html#bo-859"
  },
  "apisNote": "Regenerated 9 September 2026 from Resource_Management_Configuration_Reference.pdf page 11. 0 of 0 labels bound to a contract property; 0 of 40 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "resourceId",
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
  "id": "BO-860",
  "name": "Resource Dependency Rules",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Resource_Management_Configuration_Reference.pdf",
   "board": "1",
   "number": "07",
   "page": 13
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/resource-dependency-rules-bo-860",
   "component": "apps/venue-management-web/src/routes/rentals/ResourceDependencyRules.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-854"
   ],
   "exitTo": [
    "BO-854"
   ],
   "transitions": [
    {
     "to": "BO-854",
     "trigger": "Back to Resource Management Command Center",
     "provenance": "structural — pack board 1 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§The system shall display) and no metric row",
  "purpose": "Define operational relationships where one resource requires, depends upon, conflicts with, or influences another resource.",
  "purposeNote": "Administrators can define reusable dependency rules, and the system validates those dependencies before affected resources can be reserved or assigned.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Resource_Management_Configuration_Reference.pdf, page 13 §The system shall display"
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
       "label": "Every resource dependency rules",
       "columns": [
        "Missing dependencies",
        "Resource conflicts",
        "Circular dependency warnings",
        "Unavailable dependent resources"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 13 §The system shall display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected resource dependency rules",
       "bindsTo": null,
       "columns": [
        "Missing dependencies",
        "Resource conflicts",
        "Circular dependency warnings",
        "Unavailable dependent resources"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Private Ski Lesson”.",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 13 §The system shall display"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The resource dependency rules list.",
   "error": "Could not load. Names which read failed and leaves the resource dependency rules untouched.",
   "emptyFirstRun": "No resource dependency rules yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the resource dependency rules are still there. The pack's own statuses are Sound System A — the state names which is selected.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getResourceDependencies",
    "contract": "resources",
    "purpose": "Rules in force",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "setResourceDependencies",
    "contract": "resources",
    "purpose": "Define what must come with it",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "getResourceDependencies"
    ]
   }
  ],
  "entryState": {
   "preloaded": [
    "Missing dependencies",
    "Resource conflicts",
    "Circular dependency warnings",
    "Unavailable dependent resources"
   ],
   "params": [
    {
     "name": "resourceId",
     "from": "navigation"
    }
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-860",
   "workshopBoard": "wireframes/WS126 Resource Management Configuration Board 1.dc.html#bo-860"
  },
  "apisNote": "Regenerated 9 September 2026 from Resource_Management_Configuration_Reference.pdf page 13. 0 of 4 labels bound to a contract property; 15 of 34 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-861",
  "name": "Resource Package & Bundle Configuration",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Resource_Management_Configuration_Reference.pdf",
   "board": "1",
   "number": "08",
   "page": 14
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/resource-package-bundle-configuration-bo-861",
   "component": "apps/venue-management-web/src/routes/rentals/ResourcePackageBundleConfiguration.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-854"
   ],
   "exitTo": [
    "BO-854"
   ],
   "transitions": [
    {
     "to": "BO-854",
     "trigger": "Back to Resource Management Command Center",
     "provenance": "structural — pack board 1 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Administrators shall configure) and no display directory — it is settings, not a population",
  "purpose": "Allow commonly used combinations of resources to be predefined and assigned as a single operational package.",
  "purposeNote": "Administrators can create reusable resource packages containing fixed or dynamically selected resources and use those packages later during experience, event, reservation, and operational allocation.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Package code",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 14 §Administrators shall configure"
      },
      {
       "kind": "selectField",
       "label": "Package name",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 14 §Administrators shall configure"
      },
      {
       "kind": "selectField",
       "label": "Description",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 14 §Administrators shall configure"
      },
      {
       "kind": "selectField",
       "label": "Applicable venues",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 14 §Administrators shall configure"
      },
      {
       "kind": "selectField",
       "label": "Included resources",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 14 §Administrators shall configure"
      },
      {
       "kind": "selectField",
       "label": "Included resource types",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 14 §Administrators shall configure"
      },
      {
       "kind": "selectField",
       "label": "Required quantities",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 14 §Administrators shall configure"
      },
      {
       "kind": "selectField",
       "label": "Mandatory/optional components",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 14 §Administrators shall configure"
      },
      {
       "kind": "selectField",
       "label": "Substitute resources",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 14 §Administrators shall configure"
      },
      {
       "kind": "selectField",
       "label": "Allocation priority",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 14 §Administrators shall configure"
      },
      {
       "kind": "selectField",
       "label": "Effective dates",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 14 §Administrators shall configure"
      },
      {
       "kind": "selectField",
       "label": "Minimum/maximum duration",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 14 §Administrators shall configure"
      },
      {
       "kind": "selectField",
       "label": "Approval requirement",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 14 §Administrators shall configure"
      },
      {
       "kind": "selectField",
       "label": "Internal package cost",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 14 §Administrators shall configure"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The resource package bundle configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the resource package bundle untouched.",
   "emptyFirstRun": "No resource package bundle configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [
   {
    "operationId": "listResourcePackages",
    "contract": "resources",
    "purpose": "The packages",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "createResourcePackage",
    "contract": "resources",
    "purpose": "Define one",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listResourcePackages"
    ]
   },
   {
    "operationId": "updateResourcePackage",
    "contract": "resources",
    "purpose": "Change one",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listResourcePackages"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-861",
   "workshopBoard": "wireframes/WS126 Resource Management Configuration Board 1.dc.html#bo-861"
  },
  "apisNote": "Regenerated 9 September 2026 from Resource_Management_Configuration_Reference.pdf page 14. 0 of 0 labels bound to a contract property; 14 of 42 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "packageId",
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
  "id": "BO-862",
  "name": "Multi-Venue Resource Assignment",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Resource_Management_Configuration_Reference.pdf",
   "board": "1",
   "number": "09",
   "page": 15
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/multi-venue-resource-assignment-bo-862",
   "component": "apps/venue-management-web/src/routes/rentals/MultiVenueResourceAssignment.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-854"
   ],
   "exitTo": [
    "BO-854"
   ],
   "transitions": [
    {
     "to": "BO-854",
     "trigger": "Back to Resource Management Command Center",
     "provenance": "structural — pack board 1 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Control where resources may operate and whether they can be shared across venues.",
  "purposeNote": "Resources can be assigned to one or multiple venues under controlled rules, with conflicts and transfer constraints validated before operational allocation.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Resource_Management_Configuration_Reference.pdf, page 15"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Resource_Management_Configuration_Reference.pdf, page 15"
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
       "impliedBy": "setResourceVenueAssignment",
       "label": "Save",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "detailPanel",
       "derived": true,
       "impliedBy": "getResource",
       "notes": "One record, read-only."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "setResourceVenueAssignment"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The multi-venue resource list.",
   "error": "Could not load. Names which read failed and leaves the multi-venue resource untouched.",
   "emptyFirstRun": "No multi-venue resource yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the multi-venue resource are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setResourceVenueAssignment",
    "contract": "resources",
    "purpose": "Where it may operate",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "getResource"
    ]
   },
   {
    "operationId": "getResource",
    "contract": "resources",
    "purpose": "The resource being assigned",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-862",
   "workshopBoard": "wireframes/WS126 Resource Management Configuration Board 1.dc.html#bo-862"
  },
  "apisNote": "Regenerated 9 September 2026 from Resource_Management_Configuration_Reference.pdf page 15. 0 of 0 labels bound to a contract property; 0 of 27 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "resourceId",
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
  "id": "BO-863",
  "name": "Resource Lifecycle, Governance & Audit",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Resource_Management_Configuration_Reference.pdf",
   "board": "1",
   "number": "10",
   "page": 16
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/resource-lifecycle-governance-audit-bo-863",
   "component": "apps/venue-management-web/src/routes/rentals/ResourceLifecycleGovernanceAudit.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-854"
   ],
   "exitTo": [
    "BO-854"
   ],
   "transitions": [
    {
     "to": "BO-854",
     "trigger": "Back to Resource Management Command Center",
     "provenance": "structural — pack board 1 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Administrators shall configure) and no display directory — it is settings, not a population",
  "purpose": "Manage the entire operational lifecycle of a resource from creation through retirement while maintaining full traceability. Provide TICVAI with a centralized, real-time Resource Scheduling & Availability Engine where authorized users can visually see when resources are available, reserved, assigned, unavailable, under maintenance, or in conflict and can allocate or reassign them directly from the calendar. The calendar must operate as an interactive operational workspace, not simply a calendar display.",
  "purposeNote": "The complete lifecycle of every resource is governed by permissions and configurable workflows, while every material configuration change remains permanently traceable through immutable audit history.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Allowed status transitions",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 16 §Administrators shall configure"
      },
      {
       "kind": "selectField",
       "label": "Approval requirements",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 16 §Administrators shall configure"
      },
      {
       "kind": "selectField",
       "label": "Effective dates",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 16 §Administrators shall configure"
      },
      {
       "kind": "selectField",
       "label": "Retirement reason",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 16 §Administrators shall configure"
      },
      {
       "kind": "selectField",
       "label": "Suspension reason",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 16 §Administrators shall configure"
      },
      {
       "kind": "selectField",
       "label": "Replacement resource",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 16 §Administrators shall configure"
      },
      {
       "kind": "selectField",
       "label": "Disposal information",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 16 §Administrators shall configure"
      },
      {
       "kind": "selectField",
       "label": "Depreciation reference",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 16 §Administrators shall configure"
      },
      {
       "kind": "selectField",
       "label": "Asset-retirement information",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 16 §Administrators shall configure"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Maker-checker approval",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 16 §Actions may require"
      },
      {
       "kind": "secondaryButton",
       "label": "Manager approval",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 16 §Actions may require"
      },
      {
       "kind": "secondaryButton",
       "label": "Finance approval",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 16 §Actions may require"
      },
      {
       "kind": "secondaryButton",
       "label": "Operations approval",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 16 §Actions may require"
      },
      {
       "kind": "secondaryButton",
       "label": "Create",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 16 §Actions may require"
      },
      {
       "kind": "secondaryButton",
       "label": "Edit",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 16 §Actions may require"
      },
      {
       "kind": "secondaryButton",
       "label": "Approve",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 16 §Actions may require"
      },
      {
       "kind": "secondaryButton",
       "label": "Activate",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 16 §Actions may require"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The resource lifecycle governance configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the resource lifecycle governance untouched.",
   "emptyFirstRun": "No resource lifecycle governance configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [
   {
    "operationId": "getResourceAuditTrail",
    "contract": "resources",
    "purpose": "The immutable timeline",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "setResourceLifecycleState",
    "contract": "resources",
    "purpose": "Move it through its lifecycle",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "getResource",
     "listResources",
     "getResourceAuditTrail"
    ]
   },
   {
    "operationId": "setApprovalControlPolicy",
    "contract": "approvals",
    "purpose": "Require maker-checker (four-eyes) on resource changes",
    "trigger": "onAction",
    "provenance": "decided 29 September, VM close-out (venue management and configuration): serves the pack action(s) Maker-checker approval; Manager approval, Finance approval, Operations approval; Create; Edit"
   },
   {
    "operationId": "setApprovalMatrix",
    "contract": "approvals",
    "purpose": "Route resource changes to manager, finance or operations approvers",
    "trigger": "onAction",
    "provenance": "decided 29 September, VM close-out (venue management and configuration): serves the pack action(s) Maker-checker approval; Manager approval, Finance approval, Operations approval; Create; Edit"
   },
   {
    "operationId": "createResource",
    "contract": "resources",
    "purpose": "Create a resource",
    "trigger": "onAction",
    "provenance": "decided 29 September, VM close-out (venue management and configuration): serves the pack action(s) Maker-checker approval; Manager approval, Finance approval, Operations approval; Create; Edit",
    "invalidates": [
     "getResourceAuditTrail"
    ]
   },
   {
    "operationId": "updateResource",
    "contract": "resources",
    "purpose": "Edit a resource",
    "trigger": "onAction",
    "provenance": "decided 29 September, VM close-out (venue management and configuration): serves the pack action(s) Maker-checker approval; Manager approval, Finance approval, Operations approval; Create; Edit",
    "invalidates": [
     "getResourceAuditTrail"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-863",
   "workshopBoard": "wireframes/WS126 Resource Management Configuration Board 1.dc.html#bo-863"
  },
  "apisNote": "Regenerated 9 September 2026 from Resource_Management_Configuration_Reference.pdf page 16. 0 of 0 labels bound to a contract property; 29 of 101 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here. **Pack actions reconciled 29 September (VM close-out):** Approve, Activate … are choices sent by `setResourceLifecycleState` (state approved|active (list continues through the lifecycle enum)); Maker-checker approval: `setApprovalControlPolicy`; Manager approval, Finance approval, Operations approval: `setApprovalMatrix`; Create: `createResource`; Edit: `updateResource`.",
  "entryState": {
   "params": [
    {
     "name": "resourceId",
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
 "cloneResource": {
  "method": "POST",
  "path": "/resources/{resourceId}/clone",
  "contract": "resources",
  "summary": "Copy a resource and its configuration into new ones",
  "permission": "RESOURCE_MANAGE",
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
  "responds": "Resource"
 },
 "createResource": {
  "method": "POST",
  "path": "/resources",
  "contract": "resources",
  "summary": "Define a bookable resource",
  "permission": "RESOURCE_MANAGE",
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
  "requestBody": "Resource",
  "responds": "Resource"
 },
 "createResourceAttribute": {
  "method": "POST",
  "path": "/resource-attributes",
  "contract": "resources",
  "summary": "Define a customer attribute",
  "permission": "RESOURCE_CONFIGURE",
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
  "requestBody": "ResourceAttributeDefinition",
  "responds": "ResourceAttributeDefinition"
 },
 "createResourceCategory": {
  "method": "POST",
  "path": "/resource-categories",
  "contract": "resources",
  "summary": "Add a category or subcategory",
  "permission": "RESOURCE_CONFIGURE",
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
  "requestBody": "ResourceCategory",
  "responds": "ResourceCategory"
 },
 "createResourcePackage": {
  "method": "POST",
  "path": "/resource-packages",
  "contract": "resources",
  "summary": "Define a reusable combination",
  "permission": "RESOURCE_CONFIGURE",
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
  "requestBody": "ResourcePackage",
  "responds": "ResourcePackage"
 },
 "createResourceType": {
  "method": "POST",
  "path": "/resource-types",
  "contract": "resources",
  "summary": "Define a class of resource",
  "permission": "RESOURCE_CONFIGURE",
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
  "requestBody": "ResourceType",
  "responds": "ResourceType"
 },
 "getResource": {
  "method": "GET",
  "path": "/resources/{resourceId}",
  "contract": "resources",
  "summary": "One resource, with every configured section",
  "permission": "RESOURCE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "Resource"
 },
 "getResourceAuditTrail": {
  "method": "GET",
  "path": "/resources/{resourceId}/audit",
  "contract": "resources",
  "summary": "Every material change, with who and why",
  "permission": "RESOURCE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "ResourceAuditEntry"
 },
 "getResourceDependencies": {
  "method": "GET",
  "path": "/resources/{resourceId}/dependencies",
  "contract": "resources",
  "summary": "What this resource requires, conflicts with, or substitutes for",
  "permission": "RESOURCE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "ResourceDependency"
 },
 "getResourceHierarchy": {
  "method": "GET",
  "path": "/resources/{resourceId}/hierarchy",
  "contract": "resources",
  "summary": "What this resource contains, and what contains it",
  "permission": "RESOURCE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "ResourceHierarchy"
 },
 "getResourceUtilisation": {
  "method": "GET",
  "path": "/resource-utilisation",
  "contract": "resources",
  "summary": "How much of each resource's available time was used",
  "permission": "RESOURCE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "from",
    "in": "query",
    "required": true
   },
   {
    "name": "to",
    "in": "query",
    "required": true
   },
   {
    "name": "groupBy",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "ResourceUtilisation"
 },
 "listResourceAttributes": {
  "method": "GET",
  "path": "/resource-attributes",
  "contract": "resources",
  "summary": "The customer-defined fields on a resource",
  "permission": "RESOURCE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "ResourceAttributeDefinition"
 },
 "listResourceCategories": {
  "method": "GET",
  "path": "/resource-categories",
  "contract": "resources",
  "summary": "The classification tree beneath the types",
  "permission": "RESOURCE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "ResourceCategory"
 },
 "listResourcePackages": {
  "method": "GET",
  "path": "/resource-packages",
  "contract": "resources",
  "summary": "Predefined combinations assigned as one",
  "permission": "RESOURCE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "ResourcePackage"
 },
 "listResourceTypes": {
  "method": "GET",
  "path": "/resource-types",
  "contract": "resources",
  "summary": "The classes of resource this organisation supports",
  "permission": "RESOURCE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "ResourceType"
 },
 "listResources": {
  "method": "GET",
  "path": "/resources",
  "contract": "resources",
  "summary": "Resources at this venue",
  "permission": "RESOURCE_VIEW",
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
    "name": "availableFrom",
    "in": "query",
    "required": null
   },
   {
    "name": "availableTo",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "Resource"
 },
 "setApprovalControlPolicy": {
  "method": "PUT",
  "path": "/approval-control-policies",
  "contract": "approvals",
  "summary": "Require a second, independent pair of eyes",
  "permission": "APPROVAL_CONFIGURE",
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
  "requestBody": "ApprovalControlPolicy",
  "responds": "ApprovalControlPolicy"
 },
 "setApprovalMatrix": {
  "method": "PUT",
  "path": "/approval-matrices",
  "contract": "approvals",
  "summary": "Configure what requires approval",
  "permission": "APPROVAL_CONFIGURE",
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
  "requestBody": "ApprovalMatrix",
  "responds": "ApprovalMatrix"
 },
 "setResourceDependencies": {
  "method": "PUT",
  "path": "/resources/{resourceId}/dependencies",
  "contract": "resources",
  "summary": "Define what must come with it, and what cannot",
  "permission": "RESOURCE_CONFIGURE",
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
  "responds": "ResourceDependency"
 },
 "setResourceHierarchy": {
  "method": "PUT",
  "path": "/resources/{resourceId}/hierarchy",
  "contract": "resources",
  "summary": "Re-parent a resource, or attach children to it",
  "permission": "RESOURCE_MANAGE",
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
  "requestBody": "ResourceHierarchy",
  "responds": "ResourceHierarchy"
 },
 "setResourceLifecycleState": {
  "method": "POST",
  "path": "/resources/{resourceId}/state",
  "contract": "resources",
  "summary": "Move a resource through its lifecycle, with a reason",
  "permission": "RESOURCE_MANAGE",
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
  "responds": "Resource"
 },
 "setResourceVenueAssignment": {
  "method": "PUT",
  "path": "/resources/{resourceId}/venues",
  "contract": "resources",
  "summary": "Where it may operate, and whether it travels",
  "permission": "RESOURCE_MANAGE",
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
  "requestBody": "ResourceVenueAssignment",
  "responds": "ResourceVenueAssignment"
 },
 "updateResource": {
  "method": "PUT",
  "path": "/resources/{resourceId}",
  "contract": "resources",
  "summary": "Change a resource",
  "permission": "RESOURCE_MANAGE",
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
  "requestBody": "Resource",
  "responds": "Resource"
 },
 "updateResourceCategory": {
  "method": "PUT",
  "path": "/resource-categories/{categoryId}",
  "contract": "resources",
  "summary": "Change a category",
  "permission": "RESOURCE_CONFIGURE",
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
  "requestBody": "ResourceCategory",
  "responds": "ResourceCategory"
 },
 "updateResourcePackage": {
  "method": "PUT",
  "path": "/resource-packages/{packageId}",
  "contract": "resources",
  "summary": "Change a combination",
  "permission": "RESOURCE_CONFIGURE",
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
  "requestBody": "ResourcePackage",
  "responds": "ResourcePackage"
 },
 "updateResourceType": {
  "method": "PUT",
  "path": "/resource-types/{resourceTypeId}",
  "contract": "resources",
  "summary": "Change a class of resource",
  "permission": "RESOURCE_CONFIGURE",
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
  "requestBody": "ResourceType",
  "responds": "ResourceType"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "ApprovalControlPolicy": {
  "type": "object",
  "x-ticvai-persistence": "approvals.control_policy",
  "description": "Approvals boards 6.2 and 6.3. **Which decisions one person may not take alone** — distinct from which roles one person may not hold, which is `identity.setSegregationRules`.\n",
  "required": [
   "code",
   "control"
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
   "appliesToRequestKinds": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/ApprovalKind"
    }
   },
   "appliesAboveValue": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "control": {
    "type": "string",
    "enum": [
     "fourEyes",
     "dualControl",
     "separationFromRequester",
     "separationFromExecutor"
    ],
    "description": "**`fourEyes` is two different people; `dualControl` is two people from different groups.** The second is stronger and is what a finance auditor means, and collapsing them makes the stronger control unexpressible.\n"
   },
   "requiredApproverGroupIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "minimumApprovers": {
    "type": "integer",
    "default": 2
   },
   "requiresStepUp": {
    "type": "boolean",
    "default": false
   },
   "requiresSignature": {
    "type": "boolean",
    "default": false
   },
   "breakGlassAllowed": {
    "type": "boolean",
    "default": false,
    "description": "**Whether the control may be overridden in an emergency**, and if so it raises an alert rather than passing quietly. A control with no break-glass will be worked around by hand at three in the morning, which is worse.\n"
   },
   "scopePath": {
    "type": "string"
   },
   "isActive": {
    "type": "boolean",
    "default": true
   }
  }
 },
 "ApprovalKind": {
  "type": "string",
  "description": "11.1.7 and 11.1.30–11.1.37. **The first four already exist as bespoke implementations** and this contract is what they collapse into.\n**Which actions route here — decided 28 September, audit R144.** Finance and procurement acts go through this engine to a **finance approver**: closing a fiscal period (`periodClose`), reopening one (`periodReopen`), cancelling a purchase order (`purchaseOrderCancel`) and closing one short (`purchaseOrderShortClose`). The tenant default matrix for each of these names the finance approver role; a venue may tighten it and never loosen it. Starting a release rollout routes through `releasePromotion` to the platform release manager (a holder of `PLATFORM_RELEASE_PROMOTE`). **Not every `requiresApproval` goes here:** reopening a shift, recounting a stock count and a retail return above the venue threshold take a supervisor's step-up on the same device instead, and never raise a request.\n",
  "enum": [
   "refund",
   "priceOverride",
   "discountOverride",
   "complimentaryTicket",
   "membershipCancellation",
   "accessPermissionChange",
   "configurationChange",
   "aiRecommendation",
   "releasePromotion",
   "requisition",
   "stockWriteOff",
   "journalEntry",
   "periodClose",
   "periodReopen",
   "purchaseOrderCancel",
   "purchaseOrderShortClose",
   "tenantMigration"
  ]
 },
 "ApprovalMatrix": {
  "type": "object",
  "x-ticvai-persistence": "approvals.matrix",
  "required": [
   "kind",
   "scopeLevel",
   "rules"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "kind": {
    "$ref": "#/components/schemas/ApprovalKind"
   },
   "scopeLevel": {
    "type": "string",
    "enum": [
     "tenant",
     "region",
     "venue"
    ]
   },
   "scopePath": {
    "type": "string",
    "readOnly": true
   },
   "version": {
    "type": "integer",
    "readOnly": true,
    "description": "11.1.80. **A request is decided by the rules it was raised under.** Changing the matrix mid-flight would mean an approver answering a question that changed while they read it.\n**(`kind`, `scopePath`, `version`) is unique**, and a stored version is never edited: a request's `matrixVersion` names exactly one rule set (decided 28 September, audit R129 (2)).\n"
   },
   "rules": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/ApprovalRule"
    }
   },
   "isActive": {
    "type": "boolean"
   }
  }
 },
 "ApprovalRule": {
  "type": "object",
  "x-ticvai-persistence": "approvals.rule",
  "required": [
   "order",
   "approverRoleIds",
   "mode"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "description": "**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"
   },
   "order": {
    "type": "integer",
    "description": "**First match wins.** Explicit ordering is what makes a matrix reviewable — an unordered set of overlapping rules is one nobody can reason about.\n"
   },
   "minAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "maxAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "riskScoreAbove": {
    "type": "number",
    "nullable": true,
    "description": "11.1.12. **Nothing supplies this yet** — risk scoring is parked with the model-dependent AI. The field exists so adding the engine later is configuration rather than a schema change.\n"
   },
   "condition": {
    "type": "string",
    "nullable": true,
    "description": "11.1.13. Evaluated against the attributes the caller supplied.\n\n**No condition language is defined yet** (pull audit R104, 26 September): the grammar, the attributes it may name and how two conditions are compared for `unreachableRule` are an open decision, not something to infer from this field.\n"
   },
   "approverRoleIds": {
    "type": "array",
    "minItems": 1,
    "description": "Role ids from `identity.listRoles` (`Role.id`), which is where an editor gets the names to show and pick from. This contract stores the ids only.\n",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "approverScopeLevel": {
    "type": "string",
    "enum": [
     "venue",
     "department",
     "region",
     "tenant"
    ],
    "description": "11.1.39. Which organisational level the approver must sit at."
   },
   "mode": {
    "$ref": "#/components/schemas/ApprovalMode"
   },
   "levels": {
    "type": "integer",
    "default": 1,
    "description": "11.1.3. Multi-level chains ask each level in turn."
   },
   "requiresMfa": {
    "type": "boolean",
    "default": false
   },
   "requiresSignature": {
    "type": "boolean",
    "default": false
   },
   "slaMinutes": {
    "type": "integer",
    "nullable": true,
    "description": "11.1.14. Null means no SLA, which is different from a long one."
   },
   "escalateAfterMinutes": {
    "type": "integer",
    "nullable": true
   },
   "escalateToRoleIds": {
    "type": "array",
    "description": "Role ids from `identity.listRoles`, as `approverRoleIds`.",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "expiresAfterMinutes": {
    "type": "integer",
    "nullable": true,
    "description": "11.1.53. An unanswered request eventually stops waiting."
   }
  }
 },
 "Resource": {
  "type": "object",
  "x-ticvai-persistence": "resources.resource",
  "description": "**A specific object, not a quantity of interchangeable ones.** A venue with forty identical strollers has forty resources, because guest number twelve returned stroller number twelve.\n",
  "required": [
   "id",
   "code",
   "name",
   "kind",
   "venueId"
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
   "kind": {
    "$ref": "#/components/schemas/ResourceKind"
   },
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "scopePath": {
    "type": "string"
   },
   "parentResourceId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "**A pool cabana belongs to the pool area; a seat belongs to an auditorium.** Booking a parent takes its children with it, which is the behaviour a venue expects and would otherwise have to enforce by hand.\n"
   },
   "principalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "For a resource of kind `instructor` or `staff`. **`workforce` still owns their rota** — this says whether they are qualified and whether they are already committed.\n"
   },
   "attributes": {
    "type": "object",
    "additionalProperties": true,
    "description": "Configurable per kind — capacity, size, shade, power, poolside."
   },
   "setupMinutes": {
    "type": "integer",
    "default": 0,
    "description": "**Before the booking, not inside it.** An auditorium booked 14:00–16:00 is unavailable from 13:30 with a 30-minute setup, and a calendar that cannot express that double-books every time.\n"
   },
   "teardownMinutes": {
    "type": "integer",
    "default": 0
   },
   "requiresQualification": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Qualification codes a person must hold to be assigned to this."
   },
   "depositAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "status": {
    "type": "string",
    "enum": [
     "available",
     "booked",
     "checkedOut",
     "maintenance",
     "retired"
    ]
   },
   "isActive": {
    "type": "boolean",
    "default": true
   }
  }
 },
 "ResourceAttributeDefinition": {
  "type": "object",
  "x-ticvai-persistence": "resources.attribute_definition",
  "description": "Board 1.05. **A typed, validated field the customer adds.** The alternative was a column per customer request, which is a release per customer.\n",
  "required": [
   "code",
   "label",
   "dataType"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "code": {
    "type": "string"
   },
   "label": {
    "type": "string"
   },
   "dataType": {
    "type": "string",
    "enum": [
     "text",
     "number",
     "decimal",
     "currency",
     "date",
     "dateTime",
     "boolean",
     "singleSelect",
     "multiSelect",
     "lookup",
     "attachment",
     "url",
     "measurement",
     "formula"
    ]
   },
   "applicableResourceTypeIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "applicableCategoryIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "mandatory": {
    "type": "boolean",
    "default": false
   },
   "defaultValue": {
    "nullable": true
   },
   "allowedValues": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "minimum": {
    "type": "number",
    "nullable": true
   },
   "maximum": {
    "type": "number",
    "nullable": true
   },
   "validationExpression": {
    "type": "string",
    "nullable": true
   },
   "searchable": {
    "type": "boolean",
    "default": false,
    "description": "**The flag that decides whether `suggestResources` can use it.** An attribute nobody can filter by cannot take part in skill-based matching, which is the main reason the customer defined it.\n"
   },
   "scopePath": {
    "type": "string"
   }
  }
 },
 "ResourceAuditEntry": {
  "type": "object",
  "x-ticvai-persistence": "resources.resource_audit",
  "description": "Board 1.10. **Immutable, and it carries the previous value.**",
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "resourceId": {
    "type": "string",
    "format": "uuid"
   },
   "at": {
    "type": "string",
    "format": "date-time"
   },
   "actorId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "action": {
    "type": "string"
   },
   "field": {
    "type": "string",
    "nullable": true
   },
   "previousValue": {
    "nullable": true
   },
   "newValue": {
    "nullable": true
   },
   "reason": {
    "type": "string",
    "nullable": true
   },
   "sourceChannel": {
    "type": "string",
    "nullable": true
   },
   "apiOrigin": {
    "type": "string",
    "nullable": true
   },
   "correlationId": {
    "type": "string",
    "nullable": true
   },
   "scopePath": {
    "type": "string"
   }
  }
 },
 "ResourceCategory": {
  "type": "object",
  "x-ticvai-persistence": "resources.resource_category",
  "description": "Board 1.03. Beneath the type — *Equipment → AV → Lighting*, *Rental → Towels*. **Configuration cascades down the tree**, which is the reason it is a tree.\n",
  "required": [
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
   "description": {
    "type": "string",
    "nullable": true
   },
   "parentCategoryId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "applicableResourceTypeIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "displayOrder": {
    "type": "integer",
    "default": 0
   },
   "tags": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "reportingGroup": {
    "type": "string",
    "nullable": true
   },
   "costCentre": {
    "type": "string",
    "nullable": true
   },
   "defaultAttributes": {
    "type": "object",
    "additionalProperties": true
   },
   "defaultApprovalWorkflowId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "scopePath": {
    "type": "string"
   },
   "isActive": {
    "type": "boolean",
    "default": true
   }
  }
 },
 "ResourceDependency": {
  "type": "object",
  "x-ticvai-persistence": "resources.resource_dependency",
  "description": "Board 1.07. **Evaluated before an assignment is confirmed.** *Stage A requires Sound System A and Lighting Rig A.*\n",
  "required": [
   "kind"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "kind": {
    "type": "string",
    "enum": [
     "requires",
     "requiresOneOf",
     "requiresAll",
     "conflictsWith",
     "cannotOperateSimultaneously",
     "preferredWith",
     "substituteFor",
     "backupFor",
     "sharesCapacityWith"
    ]
   },
   "targetResourceId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "targetResourceTypeId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "minimumQuantity": {
    "type": "integer",
    "default": 1
   },
   "maximumQuantity": {
    "type": "integer",
    "nullable": true
   },
   "mandatory": {
    "type": "boolean",
    "default": true
   },
   "priority": {
    "type": "integer",
    "default": 0
   },
   "effectiveFrom": {
    "type": "string",
    "format": "date",
    "nullable": true
   },
   "effectiveTo": {
    "type": "string",
    "format": "date",
    "nullable": true
   },
   "venueId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "scopePath": {
    "type": "string"
   }
  }
 },
 "ResourceHierarchy": {
  "type": "object",
  "description": "Board 1.06. Ancestors and the immediate subtree, with the relationship named.",
  "properties": {
   "resourceId": {
    "type": "string",
    "format": "uuid"
   },
   "ancestors": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/ResourceRelation"
    }
   },
   "children": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/ResourceRelation"
    }
   }
  }
 },
 "ResourceKind": {
  "type": "string",
  "description": "BL-135. **`locker` was an entitlement kind in `orders` and nothing issued, assigned or released one.** A locker is a specific object checked out to a named guest and returned — which is this context exactly, and modelling it as an entitlement would have needed a second check-out mechanism.\nA seed for `ResourceType` rather than the law (board 1.02): a customer adding a class does it with `createResourceType`, not by waiting for this list to grow.\n**`table` is a non-dining spot** (decided 29 September, rev 3 GAP-C2, confirmed by Chinmay): a beach or event table placed on a venue map, picked and sold like a cabana (`createResourceHold`, then the order). **A dining table is not this**: restaurant tables stay `fnb` tables, booked with `fnb.createTableReservation` and the waitlist (audit R073 (d)).\n",
  "enum": [
   "cabana",
   "lounger",
   "locker",
   "wheelchair",
   "stroller",
   "equipment",
   "room",
   "auditorium",
   "vehicle",
   "instructor",
   "staff",
   "table",
   "pitch",
   "studio",
   "other"
  ],
  "x-ticvai-refuses": {
   "mealPlan": "**Listed by 5.5.8b and deliberately not a kind.** 5.5.8b groups meal plans with lockers and parking, but a meal plan is a balance rather than an object. It resolves to `retail.Wallet` with a `mealPlan` credit kind (CF-126), not to a resource — so it is not offered here, and a form built from this enum cannot offer it either."
  }
 },
 "ResourcePackage": {
  "type": "object",
  "x-ticvai-persistence": "resources.resource_package",
  "description": "Board 1.08. **A package may hold placeholders.** \"One technician\" is a slot, and naming a person would make the package unbookable whenever they are off.\n",
  "required": [
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
   "description": {
    "type": "string",
    "nullable": true
   },
   "applicableVenueIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "components": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/ResourceRequirement"
    }
   },
   "allocationPriority": {
    "type": "integer",
    "default": 0
   },
   "effectiveFrom": {
    "type": "string",
    "format": "date",
    "nullable": true
   },
   "effectiveTo": {
    "type": "string",
    "format": "date",
    "nullable": true
   },
   "minimumMinutes": {
    "type": "integer",
    "nullable": true
   },
   "maximumMinutes": {
    "type": "integer",
    "nullable": true
   },
   "requiresApproval": {
    "type": "boolean",
    "default": false
   },
   "internalCost": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "scopePath": {
    "type": "string"
   }
  }
 },
 "ResourceRelation": {
  "type": "object",
  "x-ticvai-persistence": "resources.resource_relation",
  "required": [
   "resourceId",
   "relation"
  ],
  "properties": {
   "resourceId": {
    "type": "string",
    "format": "uuid"
   },
   "relation": {
    "type": "string",
    "enum": [
     "contains",
     "belongsTo",
     "locatedIn",
     "operatedBy",
     "supportedBy",
     "partOf",
     "dedicatedTo"
    ]
   },
   "effectiveFrom": {
    "type": "string",
    "format": "date",
    "nullable": true
   },
   "priority": {
    "type": "integer",
    "default": 0
   },
   "scopePath": {
    "type": "string"
   }
  }
 },
 "ResourceRequirement": {
  "type": "object",
  "x-ticvai-persistence": "resources.resource_requirement",
  "description": "**A type and a quantity, never a named resource.** This is what makes the 26 August rule enforceable — the product states what it needs and the platform decides which one.\nFor resources placed on a published venue map the rule is superseded (decided 29 September, rev 3 REV3-15): the guest names the resource through a `ResourceHold`, and no requirement is needed.\n",
  "required": [
   "quantity"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "resourceTypeId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "categoryId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "resourceId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "**A fixed component, and the exception rather than the rule.** Meeting Room A really is Meeting Room A; the technician is not.\n"
   },
   "quantity": {
    "type": "integer",
    "default": 1
   },
   "mandatory": {
    "type": "boolean",
    "default": true
   },
   "requiredQualifications": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "requiredAttributes": {
    "type": "object",
    "additionalProperties": true
   },
   "substituteResourceIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "scopePath": {
    "type": "string"
   }
  }
 },
 "ResourceType": {
  "type": "object",
  "x-ticvai-persistence": "resources.resource_type",
  "description": "Board 1.02. **The class, and the ten switches that decide which parts of the platform a resource of this class touches.** `Resource.kind` was an enum and this is the table behind it — a customer adding \"Golf Buggy\" does not need a release.\n",
  "required": [
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
   "description": {
    "type": "string",
    "nullable": true
   },
   "icon": {
    "type": "string",
    "nullable": true
   },
   "displayColour": {
    "type": "string",
    "nullable": true
   },
   "nature": {
    "type": "string",
    "enum": [
     "physical",
     "human",
     "virtual"
    ],
    "description": "**Human resources point at a principal and are rostered by `workforce`.** The nature decides which other context owns the thing, which is why it is not a free label.\n"
   },
   "reservable": {
    "type": "boolean",
    "default": true
   },
   "rentable": {
    "type": "boolean",
    "default": false
   },
   "capacityControlled": {
    "type": "boolean",
    "default": false
   },
   "scheduleControlled": {
    "type": "boolean",
    "default": true
   },
   "inventoryControlled": {
    "type": "boolean",
    "default": false
   },
   "qualificationRequired": {
    "type": "boolean",
    "default": false
   },
   "maintenanceControlled": {
    "type": "boolean",
    "default": false
   },
   "checkInOutSupported": {
    "type": "boolean",
    "default": false
   },
   "depositApplicable": {
    "type": "boolean",
    "default": false
   },
   "customerSelectable": {
    "type": "boolean",
    "default": false,
    "description": "**A ceiling, not a permission.** Whether a guest may actually choose is decided per ticket type by `setResourceSelectionPolicy`; a type with this false can never be choosable, and a type with it true still is not until a product says so.\n"
   },
   "scopePath": {
    "type": "string"
   },
   "isActive": {
    "type": "boolean",
    "default": true
   }
  }
 },
 "ResourceUtilisation": {
  "type": "object",
  "description": "Board 10.02. **Booked time over available time**, where available knows about schedules, blocks, setup and travel.\n",
  "properties": {
   "key": {
    "type": "string"
   },
   "label": {
    "type": "string"
   },
   "availableMinutes": {
    "type": "integer"
   },
   "bookedMinutes": {
    "type": "integer"
   },
   "blockedMinutes": {
    "type": "integer"
   },
   "utilisationPercent": {
    "type": "number"
   },
   "bookingCount": {
    "type": "integer"
   }
  }
 },
 "ResourceVenueAssignment": {
  "type": "object",
  "x-ticvai-persistence": "resources.venue_assignment",
  "description": "Board 1.09. **The travel buffer is subtracted from availability**, like setup and teardown, so a shared instructor is not double-booked across a journey they cannot make.\n",
  "required": [
   "primaryVenueId"
  ],
  "properties": {
   "primaryVenueId": {
    "type": "string",
    "format": "uuid"
   },
   "secondaryVenueIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "sharedPool": {
    "type": "boolean",
    "default": false
   },
   "crossVenueBookingAllowed": {
    "type": "boolean",
    "default": false
   },
   "travelBufferMinutes": {
    "type": "integer",
    "default": 0
   },
   "transferRequired": {
    "type": "boolean",
    "default": false
   },
   "effectiveFrom": {
    "type": "string",
    "format": "date",
    "nullable": true
   },
   "effectiveTo": {
    "type": "string",
    "format": "date",
    "nullable": true
   },
   "scopePath": {
    "type": "string"
   }
  }
 }
}
```
