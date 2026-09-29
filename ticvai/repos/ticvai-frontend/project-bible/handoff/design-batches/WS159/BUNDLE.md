# WS159 — Resource Management Configuration board 5

**10 screens · 12 operations · 10 schemas · 4 permissions**

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
  `RESOURCE_BOOK, RESOURCE_CONFIGURE, RESOURCE_MANAGE, RESOURCE_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `BO-893` | Experience Resource Requirement Builder | configEditor | 2 | 0 | — |
| `BO-894` | Staff-to-Experience Qualification Mapping | configEditor | 2 | 0 | — |
| `BO-895` | Resource Combination Builder | configEditor | 2 | 0 | — |
| `BO-896` | Ticket Demand & Resource Capacity Mapping | listDetail | 1 | 0 | — |
| `BO-897` | Customer Resource Selection Configuration | configEditor | 1 | 0 | — |
| `BO-898` | Skill-Based & Smart Resource Selection | listDetail | 1 | 0 | — |
| `BO-899` | Customer / Cashier Resource Assignment Experience | configEditor | 2 | 0 | — |
| `BO-900` | Dynamic Resource Allocation Engine | configEditor | 2 | 0 | — |
| `BO-901` | Priority, Scoring & Allocation Policy | listDetail | 2 | 0 | — |
| `BO-902` | Automatic Replacement & Assignment Recovery | configEditor | 1 | 0 | — |

## Thin screens in this batch

**BO-897, BO-899, BO-901 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "BO-893",
  "name": "Experience Resource Requirement Builder",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Resource_Management_Configuration_Reference.pdf",
   "board": "5",
   "number": "01",
   "page": 65
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/experience-resource-requirement-builder-bo-893",
   "component": "apps/venue-management-web/src/routes/rentals/ExperienceResourceRequirementBuilder.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-100"
   ],
   "exitTo": [
    "BO-100",
    "BO-894",
    "BO-895",
    "BO-896",
    "BO-897",
    "BO-898",
    "BO-899",
    "BO-900",
    "BO-901",
    "BO-902"
   ],
   "transitions": [
    {
     "to": "BO-100",
     "trigger": "Back to Venue Home",
     "provenance": "structural — pack board 5 wiring, 19 September 2026",
     "back": true
    },
    {
     "to": "BO-894",
     "trigger": "Staff-to-Experience Qualification Mapping",
     "provenance": "structural — pack board 5 wiring, 19 September 2026",
     "carries": [
      "resourceId"
     ]
    },
    {
     "to": "BO-895",
     "trigger": "Resource Combination Builder",
     "provenance": "structural — pack board 5 wiring, 19 September 2026"
    },
    {
     "to": "BO-896",
     "trigger": "Ticket Demand & Resource Capacity Mapping",
     "provenance": "structural — pack board 5 wiring, 19 September 2026"
    },
    {
     "to": "BO-897",
     "trigger": "Customer Resource Selection Configuration",
     "provenance": "structural — pack board 5 wiring, 19 September 2026"
    },
    {
     "to": "BO-898",
     "trigger": "Skill-Based & Smart Resource Selection",
     "provenance": "structural — pack board 5 wiring, 19 September 2026"
    },
    {
     "to": "BO-899",
     "trigger": "Customer / Cashier Resource Assignment Experience",
     "provenance": "structural — pack board 5 wiring, 19 September 2026"
    },
    {
     "to": "BO-900",
     "trigger": "Dynamic Resource Allocation Engine",
     "provenance": "structural — pack board 5 wiring, 19 September 2026"
    },
    {
     "to": "BO-901",
     "trigger": "Priority, Scoring & Allocation Policy",
     "provenance": "structural — pack board 5 wiring, 19 September 2026"
    },
    {
     "to": "BO-902",
     "trigger": "Automatic Replacement & Assignment Recovery",
     "provenance": "structural — pack board 5 wiring, 19 September 2026"
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population",
  "purpose": "Define which operational resources are required for each attraction, experience, ticket product, session, or service.",
  "purposeNote": "Administrators can define all operational resource requirements for an experience and TICVAI can use those requirements during availability, sale, reservation, and assignment.",
  "gaps": [
   {
    "operation": null,
    "why": "**Experience Resource Requirement Builder declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either the write operations are missing or this screen is a view of something another screen builds.",
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
       "label": "Mandatory/optional",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 65 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Minimum quantity",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 65 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Maximum quantity",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 65 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Fixed/dynamic quantity",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 65 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Customer visible",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 65 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Customer selectable",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 65 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Auto-assign",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 65 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Allocation timing",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 65 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Priority",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 65 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Effective dates",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 65 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Visual Requirement Map",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 65 §Configure"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The experience resource requirement configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the experience resource requirement untouched.",
   "emptyFirstRun": "No experience resource requirement configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [
   {
    "operationId": "getExperienceResourceRequirements",
    "contract": "resources",
    "purpose": "What the experience needs",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "setExperienceResourceRequirements",
    "contract": "resources",
    "purpose": "Bind the requirements",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "getExperienceResourceRequirements"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-893",
   "workshopBoard": "wireframes/WS130 Resource Management Configuration Board 5.dc.html#bo-893"
  },
  "apisNote": "Regenerated 9 September 2026 from Resource_Management_Configuration_Reference.pdf page 65. 0 of 0 labels bound to a contract property; 11 of 51 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "experienceId",
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
  "id": "BO-894",
  "name": "Staff-to-Experience Qualification Mapping",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Resource_Management_Configuration_Reference.pdf",
   "board": "5",
   "number": "02",
   "page": 66
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/staff-to-experience-qualification-mapping-bo-894",
   "component": "apps/venue-management-web/src/routes/rentals/StaffToExperienceQualificationMapping.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-893"
   ],
   "exitTo": [
    "BO-893"
   ],
   "transitions": [
    {
     "to": "BO-893",
     "trigger": "Back to Experience Resource Requirement Builder",
     "provenance": "structural — pack board 5 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Administrators shall configure) and no display directory — it is settings, not a population",
  "purpose": "Define which types of employees are permitted to deliver a specific experience.",
  "purposeNote": "Every staff-based experience can be linked to machine-readable staff eligibility requirements that",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Required role",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 66 §Administrators shall configure"
      },
      {
       "kind": "selectField",
       "label": "Required skill",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 66 §Administrators shall configure"
      },
      {
       "kind": "selectField",
       "label": "Minimum skill level",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 66 §Administrators shall configure"
      },
      {
       "kind": "selectField",
       "label": "Required certification",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 66 §Administrators shall configure"
      },
      {
       "kind": "selectField",
       "label": "Required language",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 66 §Administrators shall configure"
      },
      {
       "kind": "selectField",
       "label": "Required venue authorization",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 66 §Administrators shall configure"
      },
      {
       "kind": "selectField",
       "label": "Experience-specific qualification",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 66 §Administrators shall configure"
      },
      {
       "kind": "selectField",
       "label": "Preferred attributes",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 66 §Administrators shall configure"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The staff-to-experience qualification mapping configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the staff-to-experience qualification mapping untouched.",
   "emptyFirstRun": "No staff-to-experience qualification mapping configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [
   {
    "operationId": "setResourceQualifications",
    "contract": "resources",
    "purpose": "What a person is certified to do",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "suggestResources",
    "contract": "resources",
    "purpose": "Staff who qualify",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-894",
   "workshopBoard": "wireframes/WS130 Resource Management Configuration Board 5.dc.html#bo-894"
  },
  "apisNote": "Regenerated 9 September 2026 from Resource_Management_Configuration_Reference.pdf page 66. 0 of 0 labels bound to a contract property; 8 of 24 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-895",
  "name": "Resource Combination Builder",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Resource_Management_Configuration_Reference.pdf",
   "board": "5",
   "number": "03",
   "page": 67
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/resource-combination-builder-bo-895",
   "component": "apps/venue-management-web/src/routes/rentals/ResourceCombinationBuilder.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-893"
   ],
   "exitTo": [
    "BO-893"
   ],
   "transitions": [
    {
     "to": "BO-893",
     "trigger": "Back to Experience Resource Requirement Builder",
     "provenance": "structural — pack board 5 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Option A; Option B) and no display directory — it is settings, not a population",
  "purpose": "Allow experiences to require multiple resources in valid combinations.",
  "purposeNote": "Administrators can configure flexible multi-resource combinations and TICVAI can determine whether at least one valid combination exists before confirming availability.",
  "gaps": [
   {
    "operation": null,
    "why": "**Resource Combination Builder declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either the write operations are missing or this screen is a view of something another screen builds.",
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
       "kind": "textField",
       "label": "2 × Level 2 Instructors",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 67 §Option A"
      },
      {
       "kind": "textField",
       "label": "1 × Level 3 Instructor",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 67 §Option B"
      },
      {
       "kind": "selectField",
       "label": "+",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 67 §Option B"
      },
      {
       "kind": "textField",
       "label": "1 × Level 1 Instructor",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 67 §Option B"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The resource combination configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the resource combination untouched.",
   "emptyFirstRun": "No resource combination configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [
   {
    "operationId": "listResourcePackages",
    "contract": "resources",
    "purpose": "Existing combinations",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "createResourcePackage",
    "contract": "resources",
    "purpose": "Build a combination",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listResourcePackages"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-895",
   "workshopBoard": "wireframes/WS130 Resource Management Configuration Board 5.dc.html#bo-895"
  },
  "apisNote": "Regenerated 9 September 2026 from Resource_Management_Configuration_Reference.pdf page 67. 0 of 0 labels bound to a contract property; 4 of 40 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-896",
  "name": "Ticket Demand & Resource Capacity Mapping",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Resource_Management_Configuration_Reference.pdf",
   "board": "5",
   "number": "04",
   "page": 69
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/ticket-demand-resource-capacity-mapping-bo-896",
   "component": "apps/venue-management-web/src/routes/rentals/TicketDemandResourceCapacityMapping.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-893"
   ],
   "exitTo": [
    "BO-893"
   ],
   "transitions": [
    {
     "to": "BO-893",
     "trigger": "Back to Experience Resource Requirement Builder",
     "provenance": "structural — pack board 5 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Connect ticket sales and participant quantity directly to resource requirements.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Resource_Management_Configuration_Reference.pdf, page 69"
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
       "kind": "datePicker",
       "label": "From",
       "operation": "getResourceUtilisation",
       "notes": "Sends `?from=` (required).",
       "provenance": "contract resources.yaml GET /resource-utilisation"
      },
      {
       "kind": "datePicker",
       "label": "To",
       "operation": "getResourceUtilisation",
       "notes": "Sends `?to=` (required).",
       "provenance": "contract resources.yaml GET /resource-utilisation"
      },
      {
       "kind": "selectField",
       "label": "Group by",
       "operation": "getResourceUtilisation",
       "notes": "Sends `?groupBy=` (resource, resourceType, category, venue).",
       "provenance": "contract resources.yaml GET /resource-utilisation"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "Session capacity",
       "columns": [
        "Session capacity"
       ],
       "notes": "The pack asks for session capacity; the contract has no field for it.",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 69"
      },
      {
       "kind": "metricTile",
       "label": "Maximum operational capacity",
       "columns": [
        "Maximum operational capacity"
       ],
       "notes": "The pack's 32 of 40: capacity the available resources can support. Nothing computes it.",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 69"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Resource capacity",
       "bindsTo": "ResourceUtilisation",
       "columns": [
        "ResourceUtilisation.label",
        "ResourceUtilisation.availableMinutes",
        "ResourceUtilisation.bookedMinutes",
        "ResourceUtilisation.blockedMinutes",
        "ResourceUtilisation.utilisationPercent",
        "ResourceUtilisation.bookingCount"
       ],
       "operation": "getResourceUtilisation",
       "provenance": "contract resources.yaml GET /resource-utilisation"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "Capacity mapping for the selected resource",
       "bindsTo": "ResourceUtilisation",
       "columns": [
        "ResourceUtilisation.key",
        "ResourceUtilisation.label",
        "ResourceUtilisation.availableMinutes",
        "ResourceUtilisation.bookedMinutes",
        "ResourceUtilisation.utilisationPercent",
        "Capacity model",
        "Resource ratio",
        "Available qualified resources",
        "Maximum operational capacity"
       ],
       "operation": "getResourceUtilisation",
       "notes": "The mapping chain is Ticket demand, participants, resource demand, resource capacity, saleable capacity.",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 69"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The ticket demand resource list.",
   "error": "Could not load. Names which read failed and leaves the ticket demand resource untouched.",
   "emptyFirstRun": "No ticket demand resource yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the ticket demand resource are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getResourceUtilisation",
    "contract": "resources",
    "purpose": "Capacity against demand",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-896",
   "workshopBoard": "wireframes/WS130 Resource Management Configuration Board 5.dc.html#bo-896"
  },
  "apisNote": "Regenerated 9 September 2026 from Resource_Management_Configuration_Reference.pdf page 69. 0 of 0 labels bound to a contract property; 0 of 8 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here. **Layout drafted 29 September (VM close-out)** from pack Resource_Management_Configuration_Reference.pdf p.69; contract resources.yaml GET /resource-utilisation. Pack labels with no schema field yet (shown as plain labels): Session capacity, Maximum operational capacity, Capacity model (Fixed / Ratio / Tiered / Capacity-based), Resource ratio (e.g. 1:8), Available qualified resources, Ticket demand, Participant count.",
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
  "id": "BO-897",
  "name": "Customer Resource Selection Configuration",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Resource_Management_Configuration_Reference.pdf",
   "board": "5",
   "number": "05",
   "page": 70
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/customer-resource-selection-configuration-bo-897",
   "component": "apps/venue-management-web/src/routes/rentals/CustomerResourceSelectionConfiguration.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-893"
   ],
   "exitTo": [
    "BO-893"
   ],
   "transitions": [
    {
     "to": "BO-893",
     "trigger": "Back to Experience Resource Requirement Builder",
     "provenance": "structural — pack board 5 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Administrators shall configure) and no display directory — it is settings, not a population",
  "purpose": "Control whether customers or cashiers may choose a specific staff member or resource during purchase.",
  "purposeNote": "Administrators can determine precisely how resource selection works for each experience and sales channel.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "No Selection",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 70 §Administrators shall configure"
      },
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "setResourceSelectionPolicy",
       "label": "Save",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "setResourceSelectionPolicy"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The customer resource selection configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the customer resource selection untouched.",
   "emptyFirstRun": "No customer resource selection configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [
   {
    "operationId": "setResourceSelectionPolicy",
    "contract": "resources",
    "purpose": "Whether the guest may choose, per ticket type",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-897",
   "workshopBoard": "wireframes/WS130 Resource Management Configuration Board 5.dc.html#bo-897"
  },
  "apisNote": "Regenerated 9 September 2026 from Resource_Management_Configuration_Reference.pdf page 70. 0 of 0 labels bound to a contract property; 1 of 32 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-898",
  "name": "Skill-Based & Smart Resource Selection",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Resource_Management_Configuration_Reference.pdf",
   "board": "5",
   "number": "06",
   "page": 71
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/skill-based-smart-resource-selection-bo-898",
   "component": "apps/venue-management-web/src/routes/rentals/SkillBasedSmartResourceSelection.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-893"
   ],
   "exitTo": [
    "BO-893"
   ],
   "transitions": [
    {
     "to": "BO-893",
     "trigger": "Back to Experience Resource Requirement Builder",
     "provenance": "structural — pack board 5 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Allow users to request the type or capability of resource they require without manually choosing an individual resource.",
  "purposeNote": "Users can find suitable resources by operational characteristics rather than requiring knowledge of specific resource names.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Resource_Management_Configuration_Reference.pdf, page 71"
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
       "kind": "selectField",
       "label": "Resource type",
       "operation": "suggestResources",
       "notes": "Sends `?resourceTypeId=` (e.g. Ski Instructor).",
       "provenance": "contract resources.yaml GET /resource-suggestions"
      },
      {
       "kind": "datePicker",
       "label": "From",
       "operation": "suggestResources",
       "notes": "Sends `?from=`.",
       "provenance": "contract resources.yaml GET /resource-suggestions"
      },
      {
       "kind": "datePicker",
       "label": "To",
       "operation": "suggestResources",
       "notes": "Sends `?to=`.",
       "provenance": "contract resources.yaml GET /resource-suggestions"
      },
      {
       "kind": "textField",
       "label": "Required attributes",
       "operation": "suggestResources",
       "notes": "Sends `?attributes=`: level, language, skill, accessibility capability, equipment type, room capacity.",
       "provenance": "contract resources.yaml GET /resource-suggestions"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Eligible resources",
       "bindsTo": "Resource",
       "columns": [
        "Resource.name",
        "Resource.code",
        "Resource.kind",
        "Resource.venueId",
        "Resource.attributes",
        "Resource.requiresQualification",
        "Resource.status",
        "Match score"
       ],
       "operation": "suggestResources",
       "notes": "Only eligible resources are returned. The pack ranks them with a match percentage (Maria Garcia 98%), which is not a field.",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 71"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected resource",
       "bindsTo": "Resource",
       "columns": [
        "Resource.id",
        "Resource.code",
        "Resource.name",
        "Resource.kind",
        "Resource.venueId",
        "Resource.scopePath",
        "Resource.attributes",
        "Resource.requiresQualification",
        "Resource.setupMinutes",
        "Resource.teardownMinutes",
        "Resource.status",
        "Resource.isActive",
        "Match score",
        "Match reasons"
       ],
       "operation": "suggestResources",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 72"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The skill-based smart resource list.",
   "error": "Could not load. Names which read failed and leaves the skill-based smart resource untouched.",
   "emptyFirstRun": "No skill-based smart resource yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the skill-based smart resource are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "suggestResources",
    "contract": "resources",
    "purpose": "Attribute matching, not a model",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-898",
   "workshopBoard": "wireframes/WS130 Resource Management Configuration Board 5.dc.html#bo-898"
  },
  "apisNote": "Regenerated 9 September 2026 from Resource_Management_Configuration_Reference.pdf page 71. 0 of 0 labels bound to a contract property; 0 of 34 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here. **Layout drafted 29 September (VM close-out)** from pack Resource_Management_Configuration_Reference.pdf p.71; pack Resource_Management_Configuration_Reference.pdf p.72; contract resources.yaml GET /resource-suggestions. Pack labels with no schema field yet (shown as plain labels): Match score, Match reasons (qualification, language, availability, venue, workload, cost).",
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
  "id": "BO-899",
  "name": "Customer / Cashier Resource Assignment Experience",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Resource_Management_Configuration_Reference.pdf",
   "board": "5",
   "number": "07",
   "page": 72
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/customer-cashier-resource-assignment-experience-bo-899",
   "component": "apps/venue-management-web/src/routes/rentals/CustomerCashierResourceAssignmentExperience.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-893"
   ],
   "exitTo": [
    "BO-893"
   ],
   "transitions": [
    {
     "to": "BO-893",
     "trigger": "Back to Experience Resource Requirement Builder",
     "provenance": "structural — pack board 5 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§AI Recommended Option) and no display directory — it is settings, not a population",
  "purpose": "Provide the fast, visual assignment interface shown during ticket or experience purchase. This screen shall be optimized for speed and simplicity.",
  "purposeNote": "Cashiers and authorized customer channels can assign resources through a simple visual workflow without understanding backend scheduling complexity.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "✨ Best Match",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 72 §AI Recommended Option"
      },
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "allocateResources",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "allocateResources"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The customer cashier resource configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the customer cashier resource untouched.",
   "emptyFirstRun": "No customer cashier resource configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [
   {
    "operationId": "allocateResources",
    "contract": "resources",
    "purpose": "Assign at the counter",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "getResourceCalendar",
     "listResourceBookings"
    ]
   },
   {
    "operationId": "suggestResources",
    "contract": "resources",
    "purpose": "What is free and suitable",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-899",
   "workshopBoard": "wireframes/WS130 Resource Management Configuration Board 5.dc.html#bo-899"
  },
  "apisNote": "Regenerated 9 September 2026 from Resource_Management_Configuration_Reference.pdf page 72. 0 of 0 labels bound to a contract property; 1 of 27 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-900",
  "name": "Dynamic Resource Allocation Engine",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Resource_Management_Configuration_Reference.pdf",
   "board": "5",
   "number": "08",
   "page": 73
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/dynamic-resource-allocation-engine-bo-900",
   "component": "apps/venue-management-web/src/routes/rentals/DynamicResourceAllocationEngine.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-893"
   ],
   "exitTo": [
    "BO-893"
   ],
   "transitions": [
    {
     "to": "BO-893",
     "trigger": "Back to Experience Resource Requirement Builder",
     "provenance": "structural — pack board 5 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Administrators shall configure) and no display directory — it is settings, not a population",
  "purpose": "Configure how TICVAI automatically chooses a resource when a customer or cashier does not make a specific selection.",
  "purposeNote": "mobile, and API channels.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Manual",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 73 §Administrators shall configure"
      },
      {
       "kind": "selectField",
       "label": "Automatic",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 73 §Administrators shall configure"
      },
      {
       "kind": "textField",
       "label": "AI recommended + user confirmation",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 73 §Administrators shall configure"
      },
      {
       "kind": "selectField",
       "label": "Fully automatic",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 73 §Administrators shall configure"
      },
      {
       "kind": "selectField",
       "label": "Allocation Timing",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 73 §Administrators shall configure"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The dynamic resource allocation configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the dynamic resource allocation untouched.",
   "emptyFirstRun": "No dynamic resource allocation configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [
   {
    "operationId": "allocateResources",
    "contract": "resources",
    "purpose": "Allocate against the requirement",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "getResourceCalendar",
     "listResourceBookings"
    ]
   },
   {
    "operationId": "getResourceAllocationPolicy",
    "contract": "resources",
    "purpose": "The strategy in force",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-900",
   "workshopBoard": "wireframes/WS130 Resource Management Configuration Board 5.dc.html#bo-900"
  },
  "apisNote": "Regenerated 9 September 2026 from Resource_Management_Configuration_Reference.pdf page 73. 0 of 0 labels bound to a contract property; 5 of 34 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-901",
  "name": "Priority, Scoring & Allocation Policy",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Resource_Management_Configuration_Reference.pdf",
   "board": "5",
   "number": "09",
   "page": 74
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/priority-scoring-allocation-policy-bo-901",
   "component": "apps/venue-management-web/src/routes/rentals/PriorityScoringAllocationPolicy.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-893"
   ],
   "exitTo": [
    "BO-893"
   ],
   "transitions": [
    {
     "to": "BO-893",
     "trigger": "Back to Experience Resource Requirement Builder",
     "provenance": "structural — pack board 5 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Configure how TICVAI ranks eligible resources when several resources could satisfy the same requirement.",
  "purposeNote": "Resource allocation priorities are configurable, transparent, testable, and explainable.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Resource_Management_Configuration_Reference.pdf, page 74"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Resource_Management_Configuration_Reference.pdf, page 74"
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
       "impliedBy": "setResourceAllocationPolicy",
       "label": "Save",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "setResourceAllocationPolicy"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The priority scoring allocation list.",
   "error": "Could not load. Names which read failed and leaves the priority scoring allocation untouched.",
   "emptyFirstRun": "No priority scoring allocation yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the priority scoring allocation are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getResourceAllocationPolicy",
    "contract": "resources",
    "purpose": "Rotation, priority and scoring",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "setResourceAllocationPolicy",
    "contract": "resources",
    "purpose": "Change the strategy",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "getResourceAllocationPolicy"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-901",
   "workshopBoard": "wireframes/WS130 Resource Management Configuration Board 5.dc.html#bo-901"
  },
  "apisNote": "Regenerated 9 September 2026 from Resource_Management_Configuration_Reference.pdf page 74. 0 of 0 labels bound to a contract property; 0 of 38 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-902",
  "name": "Automatic Replacement & Assignment Recovery",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Resource_Management_Configuration_Reference.pdf",
   "board": "5",
   "number": "10",
   "page": 76
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/automatic-replacement-assignment-recovery-bo-902",
   "component": "apps/venue-management-web/src/routes/rentals/AutomaticReplacementAssignmentRecovery.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-893"
   ],
   "exitTo": [
    "BO-893"
   ],
   "transitions": [
    {
     "to": "BO-893",
     "trigger": "Back to Experience Resource Requirement Builder",
     "provenance": "structural — pack board 5 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Administrators shall configure) and no display directory — it is settings, not a population",
  "purpose": "Automatically detect when an assigned resource becomes unavailable and protect the customer's booking by finding a suitable replacement. Provide TICVAI with a centralized Physical Resource & Rental Operations Engine for managing equipment, operational assets, and customer-rental resources throughout their complete lifecycle. Board 6 shall manage resources such as: Towels Strollers Wheelchairs Lockers Cabanas Helmets Sports equipment Cameras Projectors AV equipment Lighting equipment Sound systems Furniture Booths Vehicles Operational equipment Customer-defined physical assets",
  "purposeNote": "When an assigned resource becomes unavailable, TICVAI detects affected bookings and either automatically replaces the resource or presents governed replacement recommendations without losing the underlying customer reservation. Board 5 Shared Resource Availability Logic Resource-dependent products shall use a common availability calculation:",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Automatic",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 76 §Administrators shall configure"
      },
      {
       "kind": "selectField",
       "label": "Approval Required",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 76 §Administrators shall configure"
      },
      {
       "kind": "selectField",
       "label": "Manual",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 76 §Administrators shall configure"
      },
      {
       "kind": "selectField",
       "label": "Customer Impact",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 76 §Administrators shall configure"
      },
      {
       "kind": "selectField",
       "label": "Customer notification",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 76 §Administrators shall configure"
      },
      {
       "kind": "selectField",
       "label": "Updated ticket/booking",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 76 §Administrators shall configure"
      },
      {
       "kind": "selectField",
       "label": "Employee notification",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 76 §Administrators shall configure"
      },
      {
       "kind": "selectField",
       "label": "Operational notification",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 76 §Administrators shall configure"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The automatic replacement recovery configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the automatic replacement recovery untouched.",
   "emptyFirstRun": "No automatic replacement recovery configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [
   {
    "operationId": "replaceResourceAllocation",
    "contract": "resources",
    "purpose": "Swap in an approved substitute",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "getResourceCalendar",
     "listResourceBookings"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-902",
   "workshopBoard": "wireframes/WS130 Resource Management Configuration Board 5.dc.html#bo-902"
  },
  "apisNote": "Regenerated 9 September 2026 from Resource_Management_Configuration_Reference.pdf page 76. 0 of 0 labels bound to a contract property; 8 of 162 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "bookingId",
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
 "allocateResources": {
  "method": "POST",
  "path": "/resource-allocations",
  "contract": "resources",
  "summary": "Fill a requirement from the pool, rotating rather than repeating",
  "permission": "RESOURCE_BOOK",
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
  "responds": "ResourceBooking"
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
 "getExperienceResourceRequirements": {
  "method": "GET",
  "path": "/experiences/{experienceId}/resource-requirements",
  "contract": "resources",
  "summary": "What an experience needs before it can run",
  "permission": "RESOURCE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "ResourceRequirement"
 },
 "getResourceAllocationPolicy": {
  "method": "GET",
  "path": "/resource-allocation-policy",
  "contract": "resources",
  "summary": "How the platform chooses between equally valid resources",
  "permission": "RESOURCE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "ResourceAllocationPolicy"
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
 "replaceResourceAllocation": {
  "method": "POST",
  "path": "/resource-allocations/{bookingId}/replace",
  "contract": "resources",
  "summary": "Swap in a substitute when the allocated resource falls through",
  "permission": "RESOURCE_BOOK",
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
  "responds": "ResourceBooking"
 },
 "setExperienceResourceRequirements": {
  "method": "PUT",
  "path": "/experiences/{experienceId}/resource-requirements",
  "contract": "resources",
  "summary": "Bind resource requirements to an experience",
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
  "responds": "ResourceRequirement"
 },
 "setResourceAllocationPolicy": {
  "method": "PUT",
  "path": "/resource-allocation-policy",
  "contract": "resources",
  "summary": "Rotation, priority and scoring",
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
  "requestBody": "ResourceAllocationPolicy",
  "responds": "ResourceAllocationPolicy"
 },
 "setResourceQualifications": {
  "method": "PUT",
  "path": "/resources/{resourceId}/qualifications",
  "contract": "resources",
  "summary": "What a person resource is certified to do, and until when",
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
  "responds": "Qualification"
 },
 "setResourceSelectionPolicy": {
  "method": "PUT",
  "path": "/resource-selection-policy",
  "contract": "resources",
  "summary": "Whether the guest may choose the resource, per ticket type",
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
  "requestBody": "ResourceSelectionPolicy",
  "responds": null
 },
 "suggestResources": {
  "method": "GET",
  "path": "/resource-suggestions",
  "contract": "resources",
  "summary": "Resources matching a requirement, by attribute",
  "permission": "RESOURCE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "resourceTypeId",
    "in": "query",
    "required": null
   },
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
    "name": "attributes",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "Resource"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "Qualification": {
  "type": "object",
  "x-ticvai-persistence": "resources.qualification",
  "description": "1.2.36. **A role is not a skill**, and the check happens before assignment rather than after.\n",
  "required": [
   "code",
   "name"
  ],
  "properties": {
   "resourceId": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "description": "**The resource that holds this qualification.** Set from the path of `setResourceQualifications`; without it a stored qualification belongs to nobody and the check before assignment has nothing to check against. One row per resource and `code`.\n"
   },
   "code": {
    "type": "string"
   },
   "name": {
    "type": "string"
   },
   "issuedAt": {
    "type": "string",
    "format": "date",
    "nullable": true
   },
   "expiresAt": {
    "type": "string",
    "format": "date",
    "nullable": true,
    "description": "**The field that makes this worth having.** A certification with no expiry is one nobody renews, and a lifeguard certificate that lapsed last month is a safety failure rather than a data-quality one.\n"
   },
   "issuer": {
    "type": "string",
    "nullable": true
   },
   "documentAssetId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "scopePath": {
    "type": "string",
    "description": "**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `venue` scope.**"
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
 "ResourceAllocationPolicy": {
  "type": "object",
  "x-ticvai-persistence": "resources.allocation_policy",
  "description": "Board 5.08, and the 26 August rotation decision. **Named rather than hidden in the allocator**, so somebody can answer why cabana three never gets used.\n",
  "properties": {
   "strategy": {
    "type": "string",
    "enum": [
     "rotate",
     "leastUtilised",
     "priorityOrder",
     "nearestFirst"
    ],
    "default": "rotate",
    "description": "**`rotate` is the default because 26 August made it one.** *\"rotate across all available resources… rather than repeatedly reusing the same resource, to avoid overburdening any single resource while others remain unused.\"*\n"
   },
   "respectResourcePriority": {
    "type": "boolean",
    "default": true
   },
   "scoringWeights": {
    "type": "object",
    "additionalProperties": {
     "type": "number"
    }
   },
   "allowPartialAllocation": {
    "type": "boolean",
    "default": false,
    "description": "**False by default.** A stage allocated without its sound system is worse than no allocation, because it looks finished.\n"
   },
   "scopePath": {
    "type": "string"
   }
  }
 },
 "ResourceBooking": {
  "type": "object",
  "x-ticvai-persistence": "resources.booking",
  "required": [
   "id",
   "resourceId",
   "from",
   "to",
   "status"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "resourceId": {
    "type": "string",
    "format": "uuid"
   },
   "subjectId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "orderId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "from": {
    "type": "string",
    "format": "date-time"
   },
   "to": {
    "type": "string",
    "format": "date-time"
   },
   "status": {
    "$ref": "#/components/schemas/ResourceBookingStatus"
   },
   "holdId": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$",
    "nullable": true,
    "description": "The `ResourceHold` this booking was converted from, where a guest picked the resource on a venue map (rev 3 REV3-15). Null for a staff booking or an allocation.\n"
   },
   "recurrenceGroupId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Ties the occurrences of a recurring booking. **Cancelling one week does not cancel the series**, and cancelling the series is a separate act with a separate confirmation.\n"
   },
   "depositAuthorisationId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The hold, through `orders.authoriseStoredValue` (CF-126). **A deposit taken and refunded is two transactions and a fee; held and released is neither.**\n"
   },
   "checkedOutAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "dueBackAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "returnedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "conditionOut": {
    "type": "string",
    "nullable": true
   },
   "conditionIn": {
    "type": "string",
    "nullable": true
   },
   "syncedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true,
    "description": "When the latest offline check-out or check-in write reached the server. **The device times are `checkedOutAt` and `returnedAt`**, taken from each write's `recordedAt`; this is the server's half of the pair naming-and-style 5.2 requires. Null while pending.\n"
   }
  }
 },
 "ResourceBookingStatus": {
  "type": "string",
  "enum": [
   "reserved",
   "checkedOut",
   "returned",
   "overdue",
   "cancelled",
   "noShow"
  ]
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
 "ResourceSelectionPolicy": {
  "type": "object",
  "x-ticvai-persistence": "resources.selection_policy",
  "description": "**Whether the guest may choose the resource, per ticket type**: the body of `setResourceSelectionPolicy` and its row, one per ticket type, replaced by each `PUT` (decided 29 September, data model DM4).\n",
  "required": [
   "ticketTypeId",
   "mode"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "ticketTypeId": {
    "type": "string",
    "format": "uuid",
    "description": "One policy per ticket type; a `PUT` for a ticket type that has one replaces it."
   },
   "mode": {
    "type": "string",
    "enum": [
     "autoAssign",
     "guestMayChoose"
    ]
   },
   "resourceTypeId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "showQualifications": {
    "type": "boolean",
    "default": false
   },
   "updatedAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "The partition key (ADR-0005), written at `venue` scope."
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
 }
}
```
