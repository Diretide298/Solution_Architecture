# WS164 — Resource Management Configuration board 10

**10 screens · 12 operations · 13 schemas · 6 permissions**

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

- **Every control that can be refused must be gated.** 6 permissions apply here:
  `PLATFORM_TENANT_VIEW, PRODUCT_VIEW, REPORT_VIEW_TENANT, RESOURCE_CONFIGURE, RESOURCE_MANAGE, RESOURCE_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `BO-943` | Resource Analytics Command Center | listDetail | 2 | 0 | — |
| `BO-944` | Resource Utilization & Capacity Analytics | listDetail | 1 | 0 | — |
| `BO-945` | Resource Cost, Revenue & Efficiency Analytics | listDetail | 5 | 2 | — |
| `BO-946` | Demand Forecast Accuracy & Planning Performance | commandCentre | 1 | 0 | — |
| `BO-947` | Resource KPI, SLA & Performance Framework | listDetail | 1 | 0 | — |
| `BO-948` | Resource Governance & Policy Center | listDetail | 2 | 0 | — |
| `BO-949` | Approval, Exception & Override Control Center | listDetail | 1 | 0 | — |
| `BO-950` | Audit Trail & Resource Decision History | configEditor | 1 | 0 | — |
| `BO-951` | Resource Integration & System Health Center | listDetail | 1 | 0 | — |
| `BO-952` | Executive Resource Intelligence & AI Improvement Center | commandCentre | 1 | 0 | — |

## Thin screens in this batch

**BO-947, BO-948, BO-949, BO-951 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "BO-943",
  "name": "Resource Analytics Command Center",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Resource_Management_Configuration_Reference.pdf",
   "board": "10",
   "number": "01",
   "page": 153
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/resource-analytics-command-center-bo-943",
   "component": "apps/venue-management-web/src/routes/rentals/ResourceAnalyticsCommandCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-100"
   ],
   "exitTo": [
    "BO-100",
    "BO-944",
    "BO-945",
    "BO-946",
    "BO-947",
    "BO-948",
    "BO-949",
    "BO-950",
    "BO-951",
    "BO-952"
   ],
   "transitions": [
    {
     "to": "BO-100",
     "trigger": "Back to Venue Home",
     "provenance": "structural — pack board 10 wiring, 19 September 2026",
     "back": true
    },
    {
     "to": "BO-944",
     "trigger": "Resource Utilization & Capacity Analytics",
     "provenance": "structural — pack board 10 wiring, 19 September 2026"
    },
    {
     "to": "BO-945",
     "trigger": "Resource Cost, Revenue & Efficiency Analytics",
     "provenance": "structural — pack board 10 wiring, 19 September 2026"
    },
    {
     "to": "BO-946",
     "trigger": "Demand Forecast Accuracy & Planning Performance",
     "provenance": "structural — pack board 10 wiring, 19 September 2026"
    },
    {
     "to": "BO-947",
     "trigger": "Resource KPI, SLA & Performance Framework",
     "provenance": "structural — pack board 10 wiring, 19 September 2026"
    },
    {
     "to": "BO-948",
     "trigger": "Resource Governance & Policy Center",
     "provenance": "structural — pack board 10 wiring, 19 September 2026"
    },
    {
     "to": "BO-949",
     "trigger": "Approval, Exception & Override Control Center",
     "provenance": "structural — pack board 10 wiring, 19 September 2026"
    },
    {
     "to": "BO-950",
     "trigger": "Audit Trail & Resource Decision History",
     "provenance": "structural — pack board 10 wiring, 19 September 2026",
     "carries": [
      "resourceId"
     ]
    },
    {
     "to": "BO-951",
     "trigger": "Resource Integration & System Health Center",
     "provenance": "structural — pack board 10 wiring, 19 September 2026"
    },
    {
     "to": "BO-952",
     "trigger": "Executive Resource Intelligence & AI Improvement Center",
     "provenance": "structural — pack board 10 wiring, 19 September 2026"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Provide executives and operational managers with a single enterprise dashboard showing the overall health and performance of Resource Management.",
  "purposeNote": "Authorized management users can understand overall Resource Management performance and identify areas requiring attention from a single dashboard.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Resource_Management_Configuration_Reference.pdf, page 153 §Display"
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
       "label": "Every resource analytics",
       "columns": [
        "Total active resources",
        "Available resources",
        "Currently assigned",
        "Utilization %",
        "Resource readiness %",
        "Staff utilization",
        "Physical asset utilization",
        "Resource conflicts",
        "Unfulfilled resource demand",
        "Overtime",
        "Maintenance downtime",
        "Resource-related operational cost",
        "Forecast vs actual demand",
        "AI recommendations implemented",
        "Resource Breakdown"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 153 §Display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected resource analytics",
       "bindsTo": null,
       "columns": [
        "Total active resources",
        "Available resources",
        "Currently assigned",
        "Utilization %",
        "Resource readiness %",
        "Staff utilization",
        "Physical asset utilization",
        "Resource conflicts",
        "Unfulfilled resource demand",
        "Overtime",
        "Maintenance downtime",
        "Resource-related operational cost",
        "Forecast vs actual demand",
        "AI recommendations implemented",
        "Resource Breakdown"
       ],
       "notes": null,
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 153 §Display"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Venue",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 153 §Allow analysis by"
      },
      {
       "kind": "secondaryButton",
       "label": "Attraction",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 153 §Allow analysis by"
      },
      {
       "kind": "secondaryButton",
       "label": "Event",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 153 §Allow analysis by"
      },
      {
       "kind": "secondaryButton",
       "label": "Resource category",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 153 §Allow analysis by"
      },
      {
       "kind": "secondaryButton",
       "label": "Resource type",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 153 §Allow analysis by"
      },
      {
       "kind": "secondaryButton",
       "label": "Equipment",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 153 §Allow analysis by"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The resource analytics list.",
   "error": "Could not load. Names which read failed and leaves the resource analytics untouched.",
   "emptyFirstRun": "No resource analytics yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the resource analytics are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listResources",
    "contract": "resources",
    "purpose": "Resources at this venue",
    "trigger": "onLoad"
   },
   {
    "operationId": "getResourceUtilisation",
    "contract": "resources",
    "purpose": "Utilisation across the estate",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "entryState": {
   "preloaded": [
    "Total active resources",
    "Available resources",
    "Currently assigned",
    "Utilization %",
    "Resource readiness %",
    "Staff utilization"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-943",
   "workshopBoard": "wireframes/WS135 Resource Management Configuration Board 10.dc.html#bo-943"
  },
  "apisNote": "Regenerated 9 September 2026 from Resource_Management_Configuration_Reference.pdf page 153. 0 of 15 labels bound to a contract property; 21 of 41 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here. **Pack actions reconciled 29 September (VM close-out):** Venue, Attraction, Event, Resource category, Resource type, Equipment are choices sent by `getResourceUtilisation` (groupBy venue|resourceType|category; field gap: attraction/event/equipment not in groupBy enum).",
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
  "id": "BO-944",
  "name": "Resource Utilization & Capacity Analytics",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Resource_Management_Configuration_Reference.pdf",
   "board": "10",
   "number": "02",
   "page": 155
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/resource-utilization-capacity-analytics-bo-944",
   "component": "apps/venue-management-web/src/routes/rentals/ResourceUtilizationCapacityAnalytics.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-943"
   ],
   "exitTo": [
    "BO-943"
   ],
   "transitions": [
    {
     "to": "BO-943",
     "trigger": "Back to Resource Analytics Command Center",
     "provenance": "structural — pack board 10 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Measure how effectively resources are being utilized and identify overused or underused capacity.",
  "purposeNote": "Managers can understand resource utilization, idle capacity, overutilization, and capacity pressure across the organization.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Resource_Management_Configuration_Reference.pdf, page 155"
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
       "notes": "Sends `?groupBy=`; venue gives the pack's venue comparison.",
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
       "label": "Available capacity",
       "bindsTo": "ResourceUtilisation",
       "columns": [
        "ResourceUtilisation.availableMinutes"
       ],
       "operation": "getResourceUtilisation",
       "notes": "Summed and shown in hours.",
       "provenance": "contract resources.yaml GET /resource-utilisation"
      },
      {
       "kind": "metricTile",
       "label": "Scheduled",
       "bindsTo": "ResourceUtilisation",
       "columns": [
        "ResourceUtilisation.bookedMinutes"
       ],
       "operation": "getResourceUtilisation",
       "notes": "Summed and shown in hours.",
       "provenance": "contract resources.yaml GET /resource-utilisation"
      },
      {
       "kind": "metricTile",
       "label": "Utilization",
       "bindsTo": "ResourceUtilisation",
       "columns": [
        "ResourceUtilisation.utilisationPercent"
       ],
       "operation": "getResourceUtilisation",
       "provenance": "contract resources.yaml GET /resource-utilisation"
      },
      {
       "kind": "metricTile",
       "label": "Actual usage",
       "columns": [
        "Actual usage"
       ],
       "notes": "The pack's formula is actual utilised hours over available; the contract has booked, not actual.",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 155"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "chart",
       "label": "Resource ranking by utilization",
       "bindsTo": "ResourceUtilisation",
       "columns": [
        "ResourceUtilisation.label",
        "ResourceUtilisation.utilisationPercent"
       ],
       "operation": "getResourceUtilisation",
       "notes": "Under- and over-utilised resources stand out against the configured target, which has no field.",
       "provenance": "contract resources.yaml GET /resource-utilisation"
      },
      {
       "kind": "dataTable",
       "label": "Utilization by resource",
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
    }
   ]
  },
  "states": {
   "loading": "The resource utilization capacity list.",
   "error": "Could not load. Names which read failed and leaves the resource utilization capacity untouched.",
   "emptyFirstRun": "No resource utilization capacity yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the resource utilization capacity are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getResourceUtilisation",
    "contract": "resources",
    "purpose": "Utilisation and capacity",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-944",
   "workshopBoard": "wireframes/WS135 Resource Management Configuration Board 10.dc.html#bo-944"
  },
  "apisNote": "Regenerated 9 September 2026 from Resource_Management_Configuration_Reference.pdf page 155. 0 of 0 labels bound to a contract property; 0 of 20 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here. **Layout drafted 29 September (VM close-out)** from pack Resource_Management_Configuration_Reference.pdf p.155; contract resources.yaml GET /resource-utilisation. Pack labels with no schema field yet (shown as plain labels): Actual usage, Assigned time, Idle time, Maintenance time, Day/time breakdown (heatmap), Utilization target.",
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
  "id": "BO-945",
  "name": "Resource Cost, Revenue & Efficiency Analytics",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Resource_Management_Configuration_Reference.pdf",
   "board": "10",
   "number": "03",
   "page": 156
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/resource-cost-revenue-efficiency-analytics-bo-945",
   "component": "apps/venue-management-web/src/routes/rentals/ResourceCostRevenueEfficiencyAnalytics.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-943"
   ],
   "exitTo": [
    "BO-943"
   ],
   "transitions": [
    {
     "to": "BO-943",
     "trigger": "Back to Resource Analytics Command Center",
     "provenance": "structural — pack board 10 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Measure the financial and operational efficiency of resources.",
  "purposeNote": "Authorized users can analyze resource-related costs and operational/commercial efficiency while maintaining clear ownership boundaries with Finance.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Resource_Management_Configuration_Reference.pdf, page 156"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Resource_Management_Configuration_Reference.pdf, page 156"
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
       "label": "Transfer cost",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 156 §Support analysis of"
      },
      {
       "kind": "secondaryButton",
       "label": "Asset operating cost",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 156 §Support analysis of"
      },
      {
       "kind": "secondaryButton",
       "label": "Resource replacement cost",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 156 §Support analysis of"
      },
      {
       "kind": "secondaryButton",
       "label": "Create resource cost",
       "operation": "createResourceCost",
       "permission": "RESOURCE_MANAGE",
       "notes": "**The writer of `resources.resource_cost`** (decided 29 September, writers pass).",
       "provenance": "contract resources.yaml POST /resource-costs"
      },
      {
       "kind": "destructiveButton",
       "label": "Delete resource cost",
       "operation": "deleteResourceCost",
       "permission": "RESOURCE_MANAGE",
       "notes": "Removes one `resources.resource_cost` row (decided 29 September, writers pass).",
       "provenance": "contract resources.yaml DELETE /resource-costs/{costId}"
      }
     ]
    },
    {
     "name": "contentBody",
     "components": [
      {
       "kind": "textField",
       "label": "Resource id",
       "operation": "listResourceCosts",
       "notes": "Sends `?resourceId=` to `listResourceCosts`.",
       "provenance": "contract resources.yaml GET /resource-costs"
      },
      {
       "kind": "selectField",
       "label": "Kind",
       "operation": "listResourceCosts",
       "notes": "Sends `?kind=` to `listResourceCosts`.",
       "provenance": "contract resources.yaml GET /resource-costs"
      },
      {
       "kind": "datePicker",
       "label": "From",
       "operation": "listResourceCosts",
       "notes": "Sends `?from=` to `listResourceCosts`.",
       "provenance": "contract resources.yaml GET /resource-costs"
      },
      {
       "kind": "datePicker",
       "label": "To",
       "operation": "listResourceCosts",
       "notes": "Sends `?to=` to `listResourceCosts`.",
       "provenance": "contract resources.yaml GET /resource-costs"
      },
      {
       "kind": "dataTable",
       "label": "Every resource cost entry",
       "bindsTo": "ResourceCostEntry",
       "columns": [
        "ResourceCostEntry.id",
        "ResourceCostEntry.resourceId",
        "ResourceCostEntry.kind",
        "ResourceCostEntry.amount",
        "ResourceCostEntry.incurredOn",
        "ResourceCostEntry.fromVenueId",
        "ResourceCostEntry.toVenueId",
        "ResourceCostEntry.note",
        "ResourceCostEntry.scopePath"
       ],
       "operation": "listResourceCosts",
       "provenance": "contract resources.yaml GET /resource-costs"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The resource cost revenue list.",
   "error": "Could not load. Names which read failed and leaves the resource cost revenue untouched.",
   "emptyFirstRun": "No resource cost revenue yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the resource cost revenue are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getResourceUtilisation",
    "contract": "resources",
    "purpose": "Cost and efficiency against use",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "getResourceCostAnalytics",
    "contract": "resources",
    "purpose": "What resources cost and earn, grouped",
    "trigger": "onLoad"
   },
   {
    "operationId": "listResourceCosts",
    "contract": "resources",
    "purpose": "Cost entries booked against resources",
    "trigger": "onLoad"
   },
   {
    "operationId": "createResourceCost",
    "contract": "resources",
    "purpose": "Book a transfer, operating or replacement cost against a resource",
    "trigger": "onAction",
    "invalidates": [
     "getResourceUtilisation",
     "getResourceCostAnalytics",
     "listResourceCosts"
    ]
   },
   {
    "operationId": "deleteResourceCost",
    "contract": "resources",
    "purpose": "Remove a cost entry booked in error",
    "trigger": "onAction",
    "invalidates": [
     "getResourceUtilisation",
     "getResourceCostAnalytics",
     "listResourceCosts"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-945",
   "workshopBoard": "wireframes/WS135 Resource Management Configuration Board 10.dc.html#bo-945"
  },
  "apisNote": "Regenerated 9 September 2026 from Resource_Management_Configuration_Reference.pdf page 156. 0 of 0 labels bound to a contract property; 3 of 24 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here. **Pack actions reconciled 29 September (VM close-out):** still owed by a contract change: `getResourceCostAnalytics`.",
  "overlays": [
   {
    "id": "formCreateResourceCost",
    "component": "modal",
    "trigger": "Create resource cost",
    "body": "**Collects what `createResourceCost` sends before it is called.** Required: `id`, `resourceId`, `kind`, `amount`, `incurredOn`. Optional: `fromVenueId`, `toVenueId`, `note`, `scopePath`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "ResourceCostEntry",
    "confirm": {
     "label": "Create resource cost",
     "operation": "createResourceCost"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "resourceId",
      "kind",
      "amount",
      "incurredOn",
      "fromVenueId",
      "toVenueId",
      "note",
      "scopePath"
     ]
    },
    "provenance": "contract resources.yaml POST /resource-costs"
   },
   {
    "id": "confirmDeleteResourceCost",
    "component": "confirmDialog",
    "trigger": "Delete resource cost",
    "body": "**Names what `deleteResourceCost` changes and what it leaves alone**, in the consequence rather than the verb. A record this affects should be identified in the dialog, not just counted.",
    "provenance": "contract resources.yaml DELETE /resource-costs/{costId}"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "costId",
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
  "id": "BO-946",
  "name": "Demand Forecast Accuracy & Planning Performance",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Resource_Management_Configuration_Reference.pdf",
   "board": "10",
   "number": "04",
   "page": 157
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/demand-forecast-accuracy-planning-performance-bo-946",
   "component": "apps/venue-management-web/src/routes/rentals/DemandForecastAccuracyPlanningPerformance.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-943"
   ],
   "exitTo": [
    "BO-943"
   ],
   "transitions": [
    {
     "to": "BO-943",
     "trigger": "Back to Resource Analytics Command Center",
     "provenance": "structural — pack board 10 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen a metric directory (§Display; Track) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's",
  "purpose": "Measure how accurately TICVAI's forecasting and planning engines predicted actual resource demand.",
  "purposeNote": "resource planning is improving operational performance.",
  "layout": {
   "template": "dashboard",
   "regions": [
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "Forecast Demand",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 157 §Display"
      },
      {
       "kind": "metricTile",
       "label": "Planned Resources",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 157 §Display"
      },
      {
       "kind": "metricTile",
       "label": "Actual Demand",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 157 §Display"
      },
      {
       "kind": "metricTile",
       "label": "Actual Resources Used",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 157 §Display"
      },
      {
       "kind": "metricTile",
       "label": "Attendance forecast accuracy",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 157 §Track"
      },
      {
       "kind": "metricTile",
       "label": "Resource demand forecast accuracy",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 157 §Track"
      },
      {
       "kind": "metricTile",
       "label": "Staffing forecast accuracy",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 157 §Track"
      },
      {
       "kind": "metricTile",
       "label": "Equipment forecast accuracy",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 157 §Track"
      },
      {
       "kind": "metricTile",
       "label": "Forecast shortage rate",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 157 §Track"
      },
      {
       "kind": "metricTile",
       "label": "Overstaffing rate",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 157 §Track"
      },
      {
       "kind": "metricTile",
       "label": "Understaffing rate",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 157 §Track"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The demand forecast accuracy list; the counts above it resolve separately.",
   "error": "Could not load. Names which read failed and leaves the demand forecast accuracy untouched.",
   "emptyFirstRun": "No demand forecast accuracy yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the demand forecast accuracy are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listDemandBookingCurve",
    "contract": "catalogue",
    "purpose": "Forecast accuracy",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-946",
   "workshopBoard": "wireframes/WS135 Resource Management Configuration Board 10.dc.html#bo-946"
  },
  "apisNote": "Regenerated 9 September 2026 from Resource_Management_Configuration_Reference.pdf page 157. 0 of 0 labels bound to a contract property; 11 of 25 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-947",
  "name": "Resource KPI, SLA & Performance Framework",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Resource_Management_Configuration_Reference.pdf",
   "board": "10",
   "number": "05",
   "page": 158
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/resource-kpi-sla-performance-framework-bo-947",
   "component": "apps/venue-management-web/src/routes/rentals/ResourceKpiSlaPerformanceFramework.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-943"
   ],
   "exitTo": [
    "BO-943"
   ],
   "transitions": [
    {
     "to": "BO-943",
     "trigger": "Back to Resource Analytics Command Center",
     "provenance": "structural — pack board 10 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§KPI Library; Each KPI shall support) and no metric row",
  "purpose": "Allow organizations to define measurable Resource Management performance standards.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Resource_Management_Configuration_Reference.pdf, page 158 §KPI Library"
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
       "label": "Every resource kpi sla",
       "columns": [
        "Resource utilization",
        "Assignment fulfillment",
        "Staffing coverage",
        "Resource readiness",
        "Equipment availability",
        "Maintenance downtime",
        "Conflict resolution time",
        "Resource replacement time",
        "Attendance compliance",
        "Overtime",
        "Rental return rate",
        "Forecast accuracy",
        "Name",
        "Description",
        "Formula",
        "Target",
        "Warning threshold",
        "Critical threshold",
        "Applicable venue",
        "Applicable resource",
        "Effective period",
        "Owner"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 158 §KPI Library"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected resource kpi sla",
       "bindsTo": null,
       "columns": [
        "Resource utilization",
        "Assignment fulfillment",
        "Staffing coverage",
        "Resource readiness",
        "Equipment availability",
        "Maintenance downtime",
        "Conflict resolution time",
        "Resource replacement time",
        "Attendance compliance",
        "Overtime",
        "Rental return rate",
        "Forecast accuracy",
        "Name",
        "Description",
        "Formula",
        "Target",
        "Warning threshold",
        "Critical threshold",
        "Applicable venue",
        "Applicable resource",
        "Effective period",
        "Owner"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Target”.",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 158 §KPI Library"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The resource kpi sla list.",
   "error": "Could not load. Names which read failed and leaves the resource kpi sla untouched.",
   "emptyFirstRun": "No resource kpi sla yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the resource kpi sla are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getResourceUtilisation",
    "contract": "resources",
    "purpose": "The KPI base",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "entryState": {
   "preloaded": [
    "Resource utilization",
    "Assignment fulfillment",
    "Staffing coverage",
    "Resource readiness",
    "Equipment availability",
    "Maintenance downtime"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-947",
   "workshopBoard": "wireframes/WS135 Resource Management Configuration Board 10.dc.html#bo-947"
  },
  "apisNote": "Regenerated 9 September 2026 from Resource_Management_Configuration_Reference.pdf page 158. 0 of 22 labels bound to a contract property; 22 of 25 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-948",
  "name": "Resource Governance & Policy Center",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Resource_Management_Configuration_Reference.pdf",
   "board": "10",
   "number": "06",
   "page": 159
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/resource-governance-policy-center-bo-948",
   "component": "apps/venue-management-web/src/routes/rentals/ResourceGovernancePolicyCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-943"
   ],
   "exitTo": [
    "BO-943"
   ],
   "transitions": [
    {
     "to": "BO-943",
     "trigger": "Back to Resource Analytics Command Center",
     "provenance": "structural — pack board 10 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Centralize the administrative policies controlling how Resource Management behaves.",
  "purposeNote": "Administrators can centrally manage Resource Management policies with controlled inheritance, versioning, and effective dating.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Resource_Management_Configuration_Reference.pdf, page 159"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Resource_Management_Configuration_Reference.pdf, page 159"
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
   "loading": "The resource governance policy list.",
   "error": "Could not load. Names which read failed and leaves the resource governance policy untouched.",
   "emptyFirstRun": "No resource governance policy yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the resource governance policy are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getResourceAllocationPolicy",
    "contract": "resources",
    "purpose": "Policy in force",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "setResourceAllocationPolicy",
    "contract": "resources",
    "purpose": "Change it",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "getResourceAllocationPolicy"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-948",
   "workshopBoard": "wireframes/WS135 Resource Management Configuration Board 10.dc.html#bo-948"
  },
  "apisNote": "Regenerated 9 September 2026 from Resource_Management_Configuration_Reference.pdf page 159. 0 of 0 labels bound to a contract property; 0 of 44 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-949",
  "name": "Approval, Exception & Override Control Center",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Resource_Management_Configuration_Reference.pdf",
   "board": "10",
   "number": "07",
   "page": 160
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/approval-exception-override-control-center-bo-949",
   "component": "apps/venue-management-web/src/routes/rentals/ApprovalExceptionOverrideControlCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-943"
   ],
   "exitTo": [
    "BO-943"
   ],
   "transitions": [
    {
     "to": "BO-943",
     "trigger": "Back to Resource Analytics Command Center",
     "provenance": "structural — pack board 10 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Each request shall show) and no metric row",
  "purpose": "Provide one centralized workspace for governed Resource Management exceptions.",
  "purposeNote": "Resource exceptions and overrides are processed through controlled, permission-based workflows rather than informal administrative changes.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Resource_Management_Configuration_Reference.pdf, page 160 §Each request shall show"
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
       "label": "Every approval exception override",
       "columns": [
        "Request",
        "Resource",
        "Requester",
        "Venue",
        "Reason",
        "Operational impact",
        "Financial impact",
        "Risk",
        "AI recommendation",
        "Required approver"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 160 §Each request shall show"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected approval exception override",
       "bindsTo": null,
       "columns": [
        "Request",
        "Resource",
        "Requester",
        "Venue",
        "Reason",
        "Operational impact",
        "Financial impact",
        "Risk",
        "AI recommendation",
        "Required approver"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Include”, “Request”, “Issue”.",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 160 §Each request shall show"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The approval exception override list.",
   "error": "Could not load. Names which read failed and leaves the approval exception override untouched.",
   "emptyFirstRun": "No approval exception override yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the approval exception override are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listMemberExceptionOverride",
    "contract": "subscription",
    "purpose": "Member Exceptions, Overrides & Service Recovery",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "Request",
    "Resource",
    "Requester",
    "Venue",
    "Reason",
    "Operational impact"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-949",
   "workshopBoard": "wireframes/WS135 Resource Management Configuration Board 10.dc.html#bo-949"
  },
  "apisNote": "Regenerated 9 September 2026 from Resource_Management_Configuration_Reference.pdf page 160. 0 of 10 labels bound to a contract property; 10 of 29 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-950",
  "name": "Audit Trail & Resource Decision History",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Resource_Management_Configuration_Reference.pdf",
   "board": "10",
   "number": "08",
   "page": 162
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/audit-trail-resource-decision-history-bo-950",
   "component": "apps/venue-management-web/src/routes/rentals/AuditTrailResourceDecisionHistory.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-943"
   ],
   "exitTo": [
    "BO-943"
   ],
   "transitions": [
    {
     "to": "BO-943",
     "trigger": "Back to Resource Analytics Command Center",
     "provenance": "structural — pack board 10 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Capture; Each event shall capture) and no display directory — it is settings, not a population",
  "purpose": "Provide immutable traceability of significant Resource Management changes and decisions.",
  "purposeNote": "Authorized users can reconstruct the complete history of material Resource Management decisions and identify exactly how and why each change occurred.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Resource creation",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 162 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Resource modification",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 162 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Availability change",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 162 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Assignment",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 162 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Reassignment",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 162 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Cancellation",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 162 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Staff override",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 162 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Maintenance block",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 162 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Rental transaction",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 162 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Deposit adjustment",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 162 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Event allocation",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 162 §Capture"
      },
      {
       "kind": "selectField",
       "label": "AI recommendation",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 162 §Capture"
      },
      {
       "kind": "selectField",
       "label": "AI execution",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 162 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Approval",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 162 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Policy change",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 162 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Who",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 162 §Each event shall capture"
      },
      {
       "kind": "selectField",
       "label": "What",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 162 §Each event shall capture"
      },
      {
       "kind": "selectField",
       "label": "When",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 162 §Each event shall capture"
      },
      {
       "kind": "selectField",
       "label": "Where",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 162 §Each event shall capture"
      },
      {
       "kind": "selectField",
       "label": "Previous Value",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 162 §Each event shall capture"
      },
      {
       "kind": "selectField",
       "label": "New Value",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 162 §Each event shall capture"
      },
      {
       "kind": "selectField",
       "label": "Reason",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 162 §Each event shall capture"
      },
      {
       "kind": "selectField",
       "label": "Source",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 162 §Each event shall capture"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The audit trail resource configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the audit trail resource untouched.",
   "emptyFirstRun": "No audit trail resource configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [
   {
    "operationId": "getResourceAuditTrail",
    "contract": "resources",
    "purpose": "Decision history",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-950",
   "workshopBoard": "wireframes/WS135 Resource Management Configuration Board 10.dc.html#bo-950"
  },
  "apisNote": "Regenerated 9 September 2026 from Resource_Management_Configuration_Reference.pdf page 162. 0 of 0 labels bound to a contract property; 23 of 50 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-951",
  "name": "Resource Integration & System Health Center",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Resource_Management_Configuration_Reference.pdf",
   "board": "10",
   "number": "09",
   "page": 163
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/resource-integration-system-health-center-bo-951",
   "component": "apps/venue-management-web/src/routes/rentals/ResourceIntegrationSystemHealthCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-943"
   ],
   "exitTo": [
    "BO-943"
   ],
   "transitions": [
    {
     "to": "BO-943",
     "trigger": "Back to Resource Analytics Command Center",
     "provenance": "structural — pack board 10 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Monitor all technical integrations and synchronization services supporting Resource Management.",
  "purposeNote": "Administrators can monitor integration health and understand the operational impact of synchronization failures.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Resource_Management_Configuration_Reference.pdf, page 163 §Display"
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
       "label": "Every resource integration system",
       "columns": [
        "System",
        "Status",
        "Last Sync",
        "Transactions",
        "Errors",
        "Latency"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 163 §Display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected resource integration system",
       "bindsTo": null,
       "columns": [
        "System",
        "Status",
        "Last Sync",
        "Transactions",
        "Errors",
        "Latency"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Potential connections include”, “HRMS”, “Workforce Provider”, “Operational Impact”, “It should explain”.",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 163 §Display"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "banner",
       "label": "Permissions this screen separates",
       "notes": "**The pack separates these permissions and no action on the screen claims them yet:** Retry, View error, Inspect payload/reference, Reprocess, Escalate, Open affected records. Each needs attaching to the control it gates, or the screen needs the control.",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 163 §Authorized users may"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The resource integration system list.",
   "error": "Could not load. Names which read failed and leaves the resource integration system untouched.",
   "emptyFirstRun": "No resource integration system yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the resource integration system are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listAnalyticsPipelines",
    "contract": "reporting",
    "purpose": "Integration and data health",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "entryState": {
   "preloaded": [
    "System",
    "Status",
    "Last Sync",
    "Transactions",
    "Errors",
    "Latency"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-951",
   "workshopBoard": "wireframes/WS135 Resource Management Configuration Board 10.dc.html#bo-951"
  },
  "apisNote": "Regenerated 9 September 2026 from Resource_Management_Configuration_Reference.pdf page 163. 0 of 6 labels bound to a contract property; 12 of 39 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-952",
  "name": "Executive Resource Intelligence & AI Improvement Center",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Resource_Management_Configuration_Reference.pdf",
   "board": "10",
   "number": "10",
   "page": 165
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/executive-resource-intelligence-ai-improvement-center-bo-952",
   "component": "apps/venue-management-web/src/routes/rentals/ExecutiveResourceIntelligenceAiImprovementCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-943"
   ],
   "exitTo": [
    "BO-943"
   ],
   "transitions": [
    {
     "to": "BO-943",
     "trigger": "Back to Resource Analytics Command Center",
     "provenance": "structural — pack board 10 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen both a metric directory (§Track) and a per-row directory (§Each recommendation shall show) — counts over a population, then the population",
  "purpose": "Complete the Resource Management module with an executive AI workspace that converts operational data into management recommendations. This should be the hero screen of Board 10.",
  "purposeNote": "Executives can use Resource Management data and AI intelligence to identify measurable opportunities for improving capacity, cost, reliability, utilization, and operational performance. Board 10 — Resource Management Control Tower Board 10 effectively becomes the Control Tower sitting above the previous nine boards. The architecture should conceptually operate as: Board 1–2 Resource Master + Availability ↓ Board 3–4 Workforce + Rostering ↓",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Resource_Management_Configuration_Reference.pdf, page 165 §Each recommendation shall show"
   }
  ],
  "layout": {
   "template": "dashboard",
   "regions": [
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "Recommendations generated",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 165 §Track"
      },
      {
       "kind": "metricTile",
       "label": "Recommendations accepted",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 165 §Track"
      },
      {
       "kind": "metricTile",
       "label": "Recommendations rejected",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 165 §Track"
      },
      {
       "kind": "metricTile",
       "label": "Auto-actions executed",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 165 §Track"
      },
      {
       "kind": "metricTile",
       "label": "Forecast accuracy",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 165 §Track"
      },
      {
       "kind": "metricTile",
       "label": "Optimization savings predicted",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 165 §Track"
      },
      {
       "kind": "metricTile",
       "label": "Optimization savings realized",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 165 §Track"
      },
      {
       "kind": "metricTile",
       "label": "Replacement success",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 165 §Track"
      },
      {
       "kind": "metricTile",
       "label": "Conflict-resolution success",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 165 §Track"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "moduleTiles",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every executive resource intelligence",
       "columns": [
        "Evidence",
        "Confidence",
        "Expected benefit",
        "Risk",
        "Affected resources",
        "Financial impact",
        "Operational impact"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 165 §Each recommendation shall show"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected executive resource intelligence",
       "bindsTo": null,
       "columns": [
        "Evidence",
        "Confidence",
        "Expected benefit",
        "Risk",
        "Affected resources",
        "Financial impact",
        "Operational impact"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Executive Question”, “Overall Utilization”, “Resource Readiness”, “Assignment Fulfillment”, “Overtime”, “Resource-Related Cost”.",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 165 §Each recommendation shall show"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The executive resource intelligence list; the counts above it resolve separately.",
   "error": "Could not load. Names which read failed and leaves the executive resource intelligence untouched.",
   "emptyFirstRun": "No executive resource intelligence yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the executive resource intelligence are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getResourceUtilisation",
    "contract": "resources",
    "purpose": "Executive resource view",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-952",
   "workshopBoard": "wireframes/WS135 Resource Management Configuration Board 10.dc.html#bo-952"
  },
  "apisNote": "Regenerated 9 September 2026 from Resource_Management_Configuration_Reference.pdf page 165. 0 of 7 labels bound to a contract property; 16 of 141 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
 "createResourceCost": {
  "method": "POST",
  "path": "/resource-costs",
  "contract": "resources",
  "summary": "Book a transfer, operating or replacement cost against a resource",
  "permission": "RESOURCE_MANAGE",
  "offlineCapable": false,
  "conflictPolicy": "append",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "ResourceCostEntry",
  "responds": "ResourceCostEntry"
 },
 "deleteResourceCost": {
  "method": "DELETE",
  "path": "/resource-costs/{costId}",
  "contract": "resources",
  "summary": "Remove a cost entry booked in error",
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
  "responds": null
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
 "getResourceCostAnalytics": {
  "method": "GET",
  "path": "/resource-cost-analytics",
  "contract": "resources",
  "summary": "What resources cost and earn, grouped",
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
  "responds": "ResourceCostAnalytics"
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
 "listAnalyticsPipelines": {
  "method": "GET",
  "path": "/analytics-pipelines",
  "contract": "reporting",
  "summary": "Data sources, refresh state and freshness",
  "permission": "REPORT_VIEW_TENANT",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "tenant",
  "parameters": [],
  "requestBody": null,
  "responds": "AnalyticsPipeline"
 },
 "listDemandBookingCurve": {
  "method": "GET",
  "path": "/demand-booking-curve",
  "contract": "catalogue",
  "summary": "AI Demand Forecasting & Booking Curve Studio",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "venue",
    "in": "query",
    "required": false
   },
   {
    "name": "product",
    "in": "query",
    "required": false
   },
   {
    "name": "event",
    "in": "query",
    "required": false
   },
   {
    "name": "performance",
    "in": "query",
    "required": false
   },
   {
    "name": "channel",
    "in": "query",
    "required": false
   },
   {
    "name": "horizon",
    "in": "query",
    "required": false
   },
   {
    "name": "dateFrom",
    "in": "query",
    "required": false
   },
   {
    "name": "dateTo",
    "in": "query",
    "required": false
   },
   {
    "name": "priceCategory",
    "in": "query",
    "required": false
   },
   {
    "name": "sectionCode",
    "in": "query",
    "required": false
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
 "listMemberExceptionOverride": {
  "method": "GET",
  "path": "/member-exception-override",
  "contract": "subscription",
  "summary": "Member Exceptions, Overrides & Service Recovery",
  "permission": "PLATFORM_TENANT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": "exceptionType",
    "in": "query",
    "required": false
   },
   {
    "name": "approvalStatus",
    "in": "query",
    "required": false
   },
   {
    "name": "membershipId",
    "in": "query",
    "required": false
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
 "listResourceCosts": {
  "method": "GET",
  "path": "/resource-costs",
  "contract": "resources",
  "summary": "Cost entries booked against resources",
  "permission": "RESOURCE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "resourceId",
    "in": "query",
    "required": null
   },
   {
    "name": "kind",
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
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "AiDemandForecastingBookingCurveStudioView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over catalogue state, assembled at read time from tables that already exist",
  "description": "**What AI Demand Forecasting & Booking Curve Studio displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "venue": {
    "type": "string",
    "description": "Venue id"
   },
   "product": {
    "type": "string",
    "description": "Product id",
    "nullable": true
   },
   "event": {
    "type": "string",
    "description": "Event id",
    "nullable": true
   },
   "performance": {
    "type": "string",
    "description": "Performance id",
    "nullable": true
   },
   "date": {
    "type": "string",
    "description": "Date",
    "format": "date"
   },
   "timeslot": {
    "type": "string",
    "description": "Timeslot",
    "nullable": true
   },
   "priceCategory": {
    "type": "string",
    "description": "Price category",
    "nullable": true
   },
   "sectionCode": {
    "type": "string",
    "nullable": true,
    "description": "Seat-map section (`seating.Section.code`) the row forecasts; null for a row at price-category or performance level (29 September, build pass, group G2; 21.11.4)"
   },
   "channel": {
    "$ref": "#/components/schemas/Channel",
    "description": "Channel"
   },
   "confidence": {
    "type": "number",
    "description": "Forecast Confidence, percent"
   },
   "forecastFinalOccupancy": {
    "type": "number",
    "description": "Forecast Final Occupancy, percent"
   },
   "demand": {
    "type": "integer",
    "description": "Forecast demand"
   },
   "attendance": {
    "type": "integer",
    "description": "Forecast attendance"
   },
   "occupancy": {
    "type": "number",
    "description": "Forecast occupancy, percent"
   },
   "sellThrough": {
    "type": "number",
    "description": "Forecast sell-through, percent"
   },
   "expectedSellOutTime": {
    "type": "string",
    "description": "Expected Sell-Out Time; empty if no sell-out forecast",
    "format": "date-time",
    "nullable": true
   },
   "revenue": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Forecast revenue"
   },
   "conversion": {
    "type": "number",
    "description": "Forecast conversion, percent"
   },
   "remainingInventory": {
    "type": "integer",
    "description": "Forecast remaining inventory at event"
   },
   "mape": {
    "type": "number",
    "description": "MAPE over closed forecasts at this level, percent"
   },
   "forecastBias": {
    "type": "number",
    "description": "Forecast Bias (positive = over-forecast), percent"
   },
   "overForecast": {
    "type": "number",
    "description": "Share of closed forecasts that over-forecast, percent"
   },
   "underForecast": {
    "type": "number",
    "description": "Share of closed forecasts that under-forecast, percent"
   },
   "forecastId": {
    "type": "string",
    "description": "Forecast id"
   },
   "horizon": {
    "type": "string",
    "description": "Forecast Horizon",
    "enum": [
     "intraday",
     "tomorrow",
     "days7",
     "days30",
     "eventHorizon",
     "seasonalHorizon"
    ]
   },
   "bookingCurve": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "daysBeforeEvent": {
       "type": "integer",
       "description": "T minus days"
      },
      "historicalExpectedPercentSold": {
       "type": "number",
       "description": "Historical expected curve, percent sold"
      },
      "actualPercentSold": {
       "type": "number",
       "nullable": true,
       "description": "Current actual curve, percent sold (empty for future points)"
      },
      "forecastPercentSold": {
       "type": "number",
       "description": "AI forecast curve, percent sold"
      }
     }
    },
    "description": "Booking Curve"
   },
   "signalContributions": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "signal": {
       "type": "string",
       "enum": [
        "internalSales",
        "bookingVelocity",
        "occupancy",
        "historicalEvents",
        "nearbyEvent",
        "weather",
        "marketTourism",
        "competitor",
        "priceElasticity",
        "other"
       ],
       "description": "Signal category"
      },
      "contributionPercent": {
       "type": "number",
       "description": "Explanatory share of the forecast"
      }
     }
    },
    "description": "Model Inputs: which signals contributed"
   },
   "confidenceReasons": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "strongHistoricalData",
      "stableBookingPattern",
      "reliableExternalSignals",
      "limitedHistoricalData",
      "volatileBookingPattern",
      "degradedExternalSignals"
     ]
    },
    "description": "Reasons behind the forecast confidence"
   },
   "modelVersion": {
    "type": "string",
    "description": "Model version that produced the forecast"
   },
   "generatedAt": {
    "type": "string",
    "description": "When the forecast was produced",
    "format": "date-time"
   }
  }
 },
 "AnalyticsPipeline": {
  "type": "object",
  "x-ticvai-persistence": "reporting.pipeline",
  "description": "BI board 10.7. **Freshness decides whether a dashboard can be trusted.**",
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "name": {
    "type": "string"
   },
   "sourceKind": {
    "type": "string"
   },
   "datasets": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "schedule": {
    "type": "string",
    "nullable": true
   },
   "lastRunAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "lastSuccessAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "freshnessMinutes": {
    "type": "integer",
    "nullable": true
   },
   "expectedFreshnessMinutes": {
    "type": "integer",
    "nullable": true
   },
   "status": {
    "type": "string",
    "enum": [
     "healthy",
     "degraded",
     "stale",
     "failed",
     "paused"
    ]
   },
   "lastError": {
    "type": "string",
    "nullable": true
   },
   "rowsLastRun": {
    "type": "integer",
    "nullable": true
   },
   "scopePath": {
    "type": "string"
   }
  }
 },
 "Channel": {
  "type": "string",
  "enum": [
   "pos",
   "kiosk",
   "web",
   "mobile",
   "b2b",
   "ota",
   "callCentre"
  ]
 },
 "MemberExceptionsOverridesServiceRecoveryView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over subscription state, assembled at read time from tables that already exist",
  "description": "**What Member Exceptions, Overrides & Service Recovery displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "member": {
    "type": "string",
    "description": "Member"
   },
   "membership": {
    "type": "string",
    "description": "Membership"
   },
   "requestedAction": {
    "type": "string",
    "description": "Requested Action"
   },
   "standardPolicyResult": {
    "type": "string",
    "description": "Standard Policy Result"
   },
   "requestedException": {
    "type": "string",
    "description": "Requested Exception"
   },
   "reason": {
    "type": "string",
    "description": "Reason"
   },
   "supportingDocumentation": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Supporting Documentation: document ids"
   },
   "financialImpact": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "nullable": true,
    "description": "Financial Impact of the exception"
   },
   "entitlementImpact": {
    "type": "string",
    "description": "Entitlement Impact"
   },
   "requestor": {
    "type": "string",
    "description": "Requestor"
   },
   "exceptionType": {
    "type": "string",
    "enum": [
     "eligibilityOverride",
     "activationExtension",
     "expiryExtension",
     "complimentaryRenewal",
     "complimentaryBenefit",
     "entitlementAdjustment",
     "freezeException",
     "suspensionOverride",
     "replacementCredential",
     "renewalException",
     "dependentException"
    ],
    "description": "Exception Type (pack p.32)"
   },
   "exceptionValue": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "nullable": true,
    "description": "Value used for approval routing"
   },
   "durationDays": {
    "type": "integer",
    "description": "Duration in days, for extensions",
    "nullable": true
   },
   "membershipTier": {
    "type": "string",
    "description": "Membership Tier"
   },
   "exceptionId": {
    "type": "string",
    "description": "Exception ID"
   },
   "approvalStatus": {
    "type": "string",
    "description": "Approval status: pending, approved, rejected or applied"
   },
   "approver": {
    "type": "string",
    "description": "Approver; must differ from the requestor for high-value exceptions",
    "nullable": true
   },
   "remedy": {
    "type": "string",
    "enum": [
     "extendMembership",
     "guestTicket",
     "complimentaryVisit",
     "feeWaiver",
     "benefitCredit",
     "renewalDiscount",
     "alternativeEntitlement"
    ],
    "description": "Service Recovery remedy (pack p.33)",
    "nullable": true
   },
   "aiSuggestion": {
    "type": "string",
    "description": "AI suggestion, advisory",
    "nullable": true
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
    "default": 0,
    "description": "After the booking. **Kept as it is** (decided 29 September, W10): with a `cleaningPolicy` of `afterEveryBooking` the cleaning buffer is added after the teardown, so a room with no teardown and a 15-minute clean is free 15 minutes after each booking ends.\n"
   },
   "cleaningPolicy": {
    "allOf": [
     {
      "$ref": "#/components/schemas/ResourceCleaningPolicy"
     }
    ],
    "nullable": true,
    "description": "How the resource is cleaned between uses (decided 29 September, W10). Null means no cleaning is scheduled beyond `teardownMinutes`."
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
 "ResourceCleaningPolicy": {
  "x-ticvai-persistence": "none — columns on resources.resource",
  "type": "object",
  "description": "**When the resource is cleaned, and what that takes out of availability** (decided 29 September, W10; the meeting-room case from the 29 September website review).\n- `afterEveryBooking` (option A): `bufferMinutes` blocked after every booking, after its teardown. - `timesPerDay` (option B): `cleaningsPerDay` cleanings of `bufferMinutes` each, between `windowStart` and `windowEnd`, **placed by the system**. The targets are spread evenly across the window; each is put in the free gap nearest its target that is long enough, and never on a booking, a hold or a block. **A confirmed booking is never moved for a cleaning.** Placement is computed on read from the day's bookings, so it moves when bookings change, and a start time is offered only if every cleaning of that day can still be placed after it is booked.\n`createResource` and `updateResource` refuse a policy with `timesPerDay` and no `cleaningsPerDay`, or a window that ends before it starts, with `422`.\n",
  "required": [
   "mode",
   "bufferMinutes"
  ],
  "properties": {
   "mode": {
    "type": "string",
    "enum": [
     "afterEveryBooking",
     "timesPerDay"
    ]
   },
   "bufferMinutes": {
    "type": "integer",
    "minimum": 5,
    "maximum": 240,
    "description": "Minutes one cleaning takes. The prototype uses 15 (proposed default, client to correct)."
   },
   "cleaningsPerDay": {
    "type": "integer",
    "minimum": 1,
    "maximum": 24,
    "nullable": true,
    "description": "Required for `timesPerDay`; ignored for `afterEveryBooking`."
   },
   "windowStart": {
    "type": "string",
    "pattern": "^([01][0-9]|2[0-3]):[0-5][0-9]$",
    "nullable": true,
    "description": "Venue-local time the cleaning window opens. Null means the resource's opening time."
   },
   "windowEnd": {
    "type": "string",
    "pattern": "^([01][0-9]|2[0-3]):[0-5][0-9]$",
    "nullable": true,
    "description": "Venue-local time the cleaning window closes. Null means the resource's closing time."
   }
  }
 },
 "ResourceCostAnalytics": {
  "type": "object",
  "x-ticvai-persistence": "none — projection over resources.resource_cost, bookings and maintenance work orders, computed at read time",
  "description": "One group's cost and revenue for the window (decided 29 September, readiness close-out; BO-945).",
  "required": [
   "key",
   "label"
  ],
  "properties": {
   "key": {
    "type": "string"
   },
   "label": {
    "type": "string"
   },
   "transferCost": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "operatingCost": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "replacementCost": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "revenue": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "bookedHours": {
    "type": "number"
   },
   "costPerBookedHour": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "nullable": true,
    "description": "Total cost over booked hours; null when nothing was booked."
   }
  }
 },
 "ResourceCostEntry": {
  "type": "object",
  "x-ticvai-persistence": "resources.resource_cost",
  "description": "**One cost booked against a resource**: a transfer between locations, an operating cost or a replacement. `getResourceCostAnalytics` sums these per group and window (decided 29 September, data model DM4).\n",
  "required": [
   "id",
   "resourceId",
   "kind",
   "amount",
   "incurredOn"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "resourceId": {
    "type": "string",
    "format": "uuid"
   },
   "kind": {
    "type": "string",
    "enum": [
     "transfer",
     "operating",
     "replacement"
    ]
   },
   "amount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "incurredOn": {
    "type": "string",
    "format": "date"
   },
   "fromVenueId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "A `transfer` only, with `toVenueId`."
   },
   "toVenueId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "note": {
    "type": "string",
    "nullable": true
   },
   "createdAt": {
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
