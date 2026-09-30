# WS57 — Sales Channel Management board 1

**10 screens · 11 operations · 21 schemas · 2 permissions**

Platform P09 TICVAI Web · ships as **ticvai-control** ·
platformAdmin audience · web ·
online only

## Who this is for

**platformAdmin on web.** Everything below is how you know what is
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
  `PRODUCT_CONFIGURE, PRODUCT_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `ADM-258` | Sales Channel Command Center | commandCentre | 3 | 0 | — |
| `ADM-259` | Channel Creation & Profile Configuration | configEditor | 1 | 0 | — |
| `ADM-260` | Product & Catalogue Assignment | listDetail | 1 | 2 | — |
| `ADM-261` | Channel Pricing & Commercial Profile Assignment | listDetail | 1 | 0 | — |
| `ADM-262` | Inventory, Capacity & Channel Allocation | listDetail | 1 | 0 | — |
| `ADM-263` | Channel Sales Schedule & Availability Windows | listDetail | 2 | 1 | — |
| `ADM-264` | Customer & Eligibility Rules by Channel | configEditor | 2 | 1 | — |
| `ADM-265` | Channel Sales Rules, Limits & Restrictions | configEditor | 2 | 1 | — |
| `ADM-266` | Channel Fees, Payment & Fulfillment Configuration | configEditor | 1 | 0 | — |
| `ADM-267` | Channel Publication, Readiness & AI Validation | configEditor | 1 | 0 | — |

## Thin screens in this batch

**ADM-261, ADM-262 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "ADM-258",
  "name": "Sales Channel Command Center",
  "module": "Commercial",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Sales_Channel_Management_Reference.pdf",
   "board": "1",
   "number": "4.1.1",
   "page": 3
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/sales-channel-command-center-adm-258",
   "component": "apps/ticvai-web/src/routes/commercial/SalesChannelCommandCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-002"
   ],
   "exitTo": [
    "ADM-002",
    "ADM-259",
    "ADM-260",
    "ADM-261",
    "ADM-262",
    "ADM-263",
    "ADM-264",
    "ADM-265",
    "ADM-266",
    "ADM-267"
   ],
   "inferred": false,
   "notes": "**The board's hub.** The workshop specified this module as boards of ten and opened each with a command centre; the other nine screens are that board's detail, so they are reached from here and return here.",
   "transitions": [
    {
     "to": "ADM-002",
     "trigger": "Platform Dashboard",
     "provenance": "derived — ADM-002 declares entryState.params  and ADM-258 holds none of them, so the edge carries nothing and ADM-002 opens cold"
    },
    {
     "to": "ADM-259",
     "trigger": "Works in Channel Creation & Profile Configuration",
     "provenance": "flow F166 step 1→2",
     "operation": "listSaleChannel"
    },
    {
     "to": "ADM-260",
     "trigger": "Works in Product & Catalogue Assignment",
     "provenance": "flow F166 step 3→4",
     "operation": "listSaleChannel"
    },
    {
     "to": "ADM-261",
     "trigger": "Works in Channel Pricing & Commercial Profile Assignment",
     "provenance": "flow F166 step 5→6",
     "operation": "listSaleChannel"
    },
    {
     "to": "ADM-262",
     "trigger": "Works in Inventory, Capacity & Channel Allocation",
     "provenance": "flow F166 step 7→8",
     "operation": "listSaleChannel"
    },
    {
     "to": "ADM-266",
     "trigger": "Works in Channel Fees, Payment & Fulfillment Configuration",
     "provenance": "flow F166 step 15→16",
     "operation": "listSaleChannel"
    },
    {
     "to": "ADM-267",
     "trigger": "Works in Channel Publication, Readiness & AI Validation",
     "provenance": "flow F166 step 17→18",
     "operation": "listSaleChannel"
    },
    {
     "to": "ADM-263",
     "trigger": "Works in Channel Sales Schedule & Availability Windows",
     "provenance": "flow F166 step 9→10",
     "operation": "listSaleChannel",
     "carries": [
      "ruleId"
     ]
    },
    {
     "to": "ADM-264",
     "trigger": "Works in Customer & Eligibility Rules by Channel",
     "provenance": "flow F166 step 11→12",
     "operation": "listSaleChannel",
     "carries": [
      "ruleId"
     ]
    },
    {
     "to": "ADM-265",
     "trigger": "Works in Channel Sales Rules, Limits & Restrictions",
     "provenance": "flow F166 step 13→14",
     "operation": "listSaleChannel",
     "carries": [
      "ruleId"
     ]
    }
   ]
  },
  "density": "compact",
  "purposeNote": "An administrator can see every configured sales channel, its status, scope, product coverage and configuration issues from one central workspace.",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen both a metric directory (§Display) and a per-row directory (§Each record should display) — counts over a population, then the population",
  "purpose": "Provide administrators with one centralized view of every TICVAI sales channel and its current operational/configuration status.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 8 actions on this screen and the screen declares 1 operation.** Unserved: POS, Mobile POS, Flying POS, Call Center, API, Partner Portal, Third-Party Channel, Custom Channel. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Sales_Channel_Management_Reference.pdf, page 3 §Support channels such as"
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
       "label": "Total Channels",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 3 §Display",
       "bindsTo": "SalesChannelCommandCenterSummary.totalChannels"
      },
      {
       "kind": "metricTile",
       "label": "Active Channels",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 3 §Display",
       "bindsTo": "SalesChannelCommandCenterSummary.activeChannels"
      },
      {
       "kind": "metricTile",
       "label": "Inactive Channels",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 3 §Display",
       "bindsTo": "SalesChannelCommandCenterSummary.inactiveChannels"
      },
      {
       "kind": "metricTile",
       "label": "Channels in Draft",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 3 §Display",
       "bindsTo": "SalesChannelCommandCenterSummary.channelsInDraft"
      },
      {
       "kind": "metricTile",
       "label": "Channels With Errors",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 3 §Display",
       "bindsTo": "SalesChannelCommandCenterSummary.channelsWithErrors"
      },
      {
       "kind": "metricTile",
       "label": "Products Distributed",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 3 §Display",
       "bindsTo": "SalesChannelCommandCenterSummary.productsDistributed"
      },
      {
       "kind": "metricTile",
       "label": "Channels With Capacity Alerts",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 3 §Display",
       "bindsTo": "SalesChannelCommandCenterSummary.channelsWithCapacityAlerts"
      },
      {
       "kind": "metricTile",
       "label": "Channels With Pricing Issues",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 3 §Display",
       "bindsTo": "SalesChannelCommandCenterSummary.channelsWithPricingIssues"
      },
      {
       "kind": "metricTile",
       "label": "Scheduled Activations",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 3 §Display",
       "bindsTo": "SalesChannelCommandCenterSummary.scheduledActivations"
      },
      {
       "kind": "metricTile",
       "label": "Scheduled Deactivations",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 3 §Display",
       "bindsTo": "SalesChannelCommandCenterSummary.scheduledDeactivations"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "moduleTiles",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every sales channel",
       "columns": [
        "SalesChannelCommandCenterView.channelId",
        "SalesChannelCommandCenterView.channelName",
        "SalesChannelCommandCenterView.channelType",
        "SalesChannelCommandCenterView.brand",
        "SalesChannelCommandCenterView.venueScope",
        "SalesChannelCommandCenterView.products",
        "SalesChannelCommandCenterView.currency",
        "SalesChannelCommandCenterView.status",
        "SalesChannelCommandCenterView.publicationStatus",
        "SalesChannelCommandCenterView.integrationStatus",
        "SalesChannelCommandCenterView.lastUpdated",
        "SalesChannelCommandCenterView.owner"
       ],
       "bindsTo": "SalesChannelCommandCenterView",
       "operation": "listSaleChannel",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 3 §Each record should display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected sales channel",
       "bindsTo": "SalesChannelCommandCenterView",
       "columns": [
        "SalesChannelCommandCenterView.channelId",
        "SalesChannelCommandCenterView.channelName",
        "SalesChannelCommandCenterView.channelType",
        "SalesChannelCommandCenterView.brand",
        "SalesChannelCommandCenterView.venueScope",
        "SalesChannelCommandCenterView.products",
        "SalesChannelCommandCenterView.currency",
        "SalesChannelCommandCenterView.status",
        "SalesChannelCommandCenterView.publicationStatus",
        "SalesChannelCommandCenterView.integrationStatus",
        "SalesChannelCommandCenterView.lastUpdated",
        "SalesChannelCommandCenterView.owner"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Channel Readiness Alert”.",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 3 §Each record should display"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "POS",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 3 §Support channels such as"
      },
      {
       "kind": "secondaryButton",
       "label": "Mobile POS",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 3 §Support channels such as"
      },
      {
       "kind": "secondaryButton",
       "label": "Flying POS",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 3 §Support channels such as"
      },
      {
       "kind": "secondaryButton",
       "label": "Call Center",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 3 §Support channels such as"
      },
      {
       "kind": "secondaryButton",
       "label": "API",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 3 §Support channels such as"
      },
      {
       "kind": "secondaryButton",
       "label": "Partner Portal",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 3 §Support channels such as"
      },
      {
       "kind": "secondaryButton",
       "label": "Third-Party Channel",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 3 §Support channels such as"
      },
      {
       "kind": "secondaryButton",
       "label": "Custom Channel",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 3 §Support channels such as"
      },
      {
       "kind": "banner",
       "label": "Permissions this screen separates",
       "notes": "**The pack separates these permissions and no action on the screen claims them yet:** Create Channel, Edit, Duplicate, Activate, Suspend, Disable, View Products, View Capacity, Validate, Schedule, Open Analytics. Each needs attaching to the control it gates, or the screen needs the control.",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 3 §Authorized users can"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The sales channel list; the counts above it resolve separately.",
   "error": "Could not load. Names which read failed and leaves the sales channel untouched.",
   "emptyFirstRun": "No sales channel yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the sales channel are still there. The pack's own statuses are → Disabled → Archived — the state names which is selected.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listSaleChannel",
    "contract": "catalogue",
    "purpose": "Sales Channel Command Center",
    "trigger": "onLoad"
   },
   {
    "operationId": "listChannelSaleSchedule",
    "contract": "catalogue",
    "purpose": "Channel Sales Schedule & Availability Windows",
    "trigger": "onLoad"
   },
   {
    "operationId": "listChannelSaleRule",
    "contract": "catalogue",
    "purpose": "Channel Sales Rules, Limits & Restrictions",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-258",
   "workshopBoard": "wireframes/WS138 Sales Channel Management Board 1.dc.html#adm-258"
  },
  "apisNote": "Regenerated 9 September 2026 from Sales_Channel_Management_Reference.pdf page 3. 22 of 22 labels bound to a contract property; 42 of 57 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "_platform": {
   "code": "P09",
   "audience": "platformAdmin",
   "formFactor": "web",
   "shortName": "TICVAI Web",
   "name": "TICVAI Web — Platform Console",
   "offlineCapable": false,
   "app": "ticvai-web",
   "operator": "ticvai",
   "targetApp": {
    "app": "ticvai-control",
    "name": "TICVAI Control",
    "shell": "web",
    "siblings": [
     "P10",
     "P11",
     "P14",
     "P17"
    ],
    "note": "**TICVAI operates all five**, whoever signs in. The partner portal, the accreditation intake, the developer portal and the sign-up are outward faces of the control plane, not separate products — but their users are not TICVAI staff, and the permission model has to hold that line. **P17 added 11 September 2026**: a prospect buying TICVAI has no tenant and no cell, so the control plane is the only thing that can serve them.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "ADM-259",
  "name": "Channel Creation & Profile Configuration",
  "module": "Commercial",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Sales_Channel_Management_Reference.pdf",
   "board": "1",
   "number": "4.1.2",
   "page": 5
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/channel-creation-profile-configuration-adm-259",
   "component": "apps/ticvai-web/src/routes/commercial/ChannelCreationProfileConfiguration.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-258"
   ],
   "exitTo": [
    "ADM-258"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-258, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-258",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F166 step 2→3",
     "operation": "createChannelProfile"
    }
   ]
  },
  "density": "compact",
  "purposeNote": "An authorized administrator can create a new channel with a unique identity, operational scope and ownership without technical development.",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population",
  "purpose": "Create and define a sales channel before products and commercial rules are assigned.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Channel Name",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 5 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Channel Code",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 5 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Channel Type",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 5 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Internal Description",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 5 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Customer-Facing Name",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 5 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Tenant",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 5 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Brand",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 5 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Business Unit",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 5 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Country",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 5 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Market",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 5 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Currency",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 5 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Time Zone",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 5 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Owner",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 5 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Responsible Department",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 5 §Configure"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Create",
       "provenance": "contract operation createChannelProfile"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The channel creation profile configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the channel creation profile untouched.",
   "emptyFirstRun": "No channel creation profile configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "createChannelProfile",
    "contract": "catalogue",
    "purpose": "Channel Creation & Profile Configuration",
    "trigger": "onAction"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-259",
   "workshopBoard": "wireframes/WS138 Sales Channel Management Board 1.dc.html#adm-259"
  },
  "apisNote": "Regenerated 9 September 2026 from Sales_Channel_Management_Reference.pdf page 5. 0 of 0 labels bound to a contract property; 14 of 42 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "_platform": {
   "code": "P09",
   "audience": "platformAdmin",
   "formFactor": "web",
   "shortName": "TICVAI Web",
   "name": "TICVAI Web — Platform Console",
   "offlineCapable": false,
   "app": "ticvai-web",
   "operator": "ticvai",
   "targetApp": {
    "app": "ticvai-control",
    "name": "TICVAI Control",
    "shell": "web",
    "siblings": [
     "P10",
     "P11",
     "P14",
     "P17"
    ],
    "note": "**TICVAI operates all five**, whoever signs in. The partner portal, the accreditation intake, the developer portal and the sign-up are outward faces of the control plane, not separate products — but their users are not TICVAI staff, and the permission model has to hold that line. **P17 added 11 September 2026**: a prospect buying TICVAI has no tenant and no cell, so the control plane is the only thing that can serve them.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "ADM-260",
  "name": "Product & Catalogue Assignment",
  "module": "Commercial",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Sales_Channel_Management_Reference.pdf",
   "board": "1",
   "number": "4.1.3",
   "page": 7
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/product-catalogue-assignment-adm-260",
   "component": "apps/ticvai-web/src/routes/commercial/ProductCatalogueAssignment.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-258"
   ],
   "exitTo": [
    "ADM-258"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-258, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-258",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F166 step 4→5",
     "operation": "setProductCatalogue"
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Administrators can determine precisely which approved products each channel is authorized to distribute without duplicating the product configuration itself.",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Control exactly which products are available through each sales channel.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 6 actions on this screen and the screen declares 1 operation.** Unserved: Assign Products, Remove Products, Disable, Copy Assignment, Import Assignment. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Sales_Channel_Management_Reference.pdf, page 7 §Support"
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
       "label": "Every product catalogue",
       "columns": [
        "ProductCatalogueAssignmentView.product",
        "ProductCatalogueAssignmentView.productType",
        "ProductCatalogueAssignmentView.venue",
        "ProductCatalogueAssignmentView.status",
        "ProductCatalogueAssignmentView.validity",
        "ProductCatalogueAssignmentView.channelStatus",
        "ProductCatalogueAssignmentView.pricingStatus",
        "ProductCatalogueAssignmentView.capacityStatus",
        "ProductCatalogueAssignmentView.effectiveFrom",
        "ProductCatalogueAssignmentView.effectiveTo"
       ],
       "bindsTo": "ProductCatalogueAssignmentView",
       "operation": "setProductCatalogue",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 7 §Display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected product catalogue",
       "bindsTo": "ProductCatalogueAssignmentView",
       "columns": [
        "ProductCatalogueAssignmentView.product",
        "ProductCatalogueAssignmentView.productType",
        "ProductCatalogueAssignmentView.venue",
        "ProductCatalogueAssignmentView.status",
        "ProductCatalogueAssignmentView.validity",
        "ProductCatalogueAssignmentView.channelStatus",
        "ProductCatalogueAssignmentView.pricingStatus",
        "ProductCatalogueAssignmentView.capacityStatus",
        "ProductCatalogueAssignmentView.effectiveFrom",
        "ProductCatalogueAssignmentView.effectiveTo"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Administrators can assign”, “Global Channel Catalogue”, “Venue Catalogue”, “For example”, “Important Architecture”, “This screen only determines”.",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 7 §Display"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Assign Products",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 7 §Support"
      },
      {
       "kind": "destructiveButton",
       "label": "Remove Products",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 7 §Support"
      },
      {
       "kind": "destructiveButton",
       "label": "Disable",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 7 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Set Effective Dates",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 7 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Copy Assignment",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 7 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Import Assignment",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 7 §Support"
      }
     ]
    }
   ]
  },
  "overlays": [
   {
    "id": "confirmRemoveProducts",
    "component": "confirmDialog",
    "trigger": "Remove Products",
    "body": "**Remove Products on a product catalogue is not reversible from this screen.** Names what it affects and what it leaves alone. The pack requires the decision to reach the audit trail, so the dialog states that it is recorded.",
    "provenance": "pack Sales_Channel_Management_Reference.pdf, page 7 §Support"
   },
   {
    "id": "confirmDisable",
    "component": "confirmDialog",
    "trigger": "Disable",
    "body": "**Disable on a product catalogue is not reversible from this screen.** Names what it affects and what it leaves alone. The pack requires the decision to reach the audit trail, so the dialog states that it is recorded.",
    "provenance": "pack Sales_Channel_Management_Reference.pdf, page 7 §Support"
   }
  ],
  "states": {
   "loading": "The product catalogue list.",
   "error": "Could not load. Names which read failed and leaves the product catalogue untouched.",
   "emptyFirstRun": "No product catalogue yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the product catalogue are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setProductCatalogue",
    "contract": "catalogue",
    "purpose": "Product & Catalogue Assignment",
    "trigger": "onAction"
   }
  ],
  "entryState": {
   "preloaded": [
    "ProductCatalogueAssignmentView.product",
    "ProductCatalogueAssignmentView.productType",
    "ProductCatalogueAssignmentView.venue",
    "ProductCatalogueAssignmentView.status",
    "ProductCatalogueAssignmentView.validity",
    "ProductCatalogueAssignmentView.channelStatus"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-260",
   "workshopBoard": "wireframes/WS138 Sales Channel Management Board 1.dc.html#adm-260"
  },
  "apisNote": "Regenerated 9 September 2026 from Sales_Channel_Management_Reference.pdf page 7. 10 of 10 labels bound to a contract property; 16 of 39 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "_platform": {
   "code": "P09",
   "audience": "platformAdmin",
   "formFactor": "web",
   "shortName": "TICVAI Web",
   "name": "TICVAI Web — Platform Console",
   "offlineCapable": false,
   "app": "ticvai-web",
   "operator": "ticvai",
   "targetApp": {
    "app": "ticvai-control",
    "name": "TICVAI Control",
    "shell": "web",
    "siblings": [
     "P10",
     "P11",
     "P14",
     "P17"
    ],
    "note": "**TICVAI operates all five**, whoever signs in. The partner portal, the accreditation intake, the developer portal and the sign-up are outward faces of the control plane, not separate products — but their users are not TICVAI staff, and the permission model has to hold that line. **P17 added 11 September 2026**: a prospect buying TICVAI has no tenant and no cell, so the control plane is the only thing that can serve them.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "ADM-261",
  "name": "Channel Pricing & Commercial Profile Assignment",
  "module": "Commercial",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Sales_Channel_Management_Reference.pdf",
   "board": "1",
   "number": "4.1.4",
   "page": 8
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/channel-pricing-commercial-profile-assignment-adm-261",
   "component": "apps/ticvai-web/src/routes/commercial/ChannelPricingCommercialProfileAssignment.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-258"
   ],
   "exitTo": [
    "ADM-258"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-258, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-258",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F166 step 6→7",
     "operation": "setChannelPricingCommercial"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Determine which pricing configuration a channel consumes.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Sales_Channel_Management_Reference.pdf, page 8"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Sales_Channel_Management_Reference.pdf, page 8"
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
       "provenance": "contract operation setChannelPricingCommercial"
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
       "impliedBy": "setChannelPricingCommercial"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The channel pricing commercial list.",
   "error": "Could not load. Names which read failed and leaves the channel pricing commercial untouched.",
   "emptyFirstRun": "No channel pricing commercial yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the channel pricing commercial are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setChannelPricingCommercial",
    "contract": "catalogue",
    "purpose": "Channel Pricing & Commercial Profile Assignment",
    "trigger": "onAction"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-261",
   "workshopBoard": "wireframes/WS138 Sales Channel Management Board 1.dc.html#adm-261"
  },
  "apisNote": "Regenerated 9 September 2026 from Sales_Channel_Management_Reference.pdf page 8. 0 of 0 labels bound to a contract property; 0 of 19 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "_platform": {
   "code": "P09",
   "audience": "platformAdmin",
   "formFactor": "web",
   "shortName": "TICVAI Web",
   "name": "TICVAI Web — Platform Console",
   "offlineCapable": false,
   "app": "ticvai-web",
   "operator": "ticvai",
   "targetApp": {
    "app": "ticvai-control",
    "name": "TICVAI Control",
    "shell": "web",
    "siblings": [
     "P10",
     "P11",
     "P14",
     "P17"
    ],
    "note": "**TICVAI operates all five**, whoever signs in. The partner portal, the accreditation intake, the developer portal and the sign-up are outward faces of the control plane, not separate products — but their users are not TICVAI staff, and the permission model has to hold that line. **P17 added 11 September 2026**: a prospect buying TICVAI has no tenant and no cell, so the control plane is the only thing that can serve them.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "ADM-262",
  "name": "Inventory, Capacity & Channel Allocation",
  "module": "Commercial",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Sales_Channel_Management_Reference.pdf",
   "board": "1",
   "number": "4.1.5",
   "page": 10
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/inventory-capacity-channel-allocation-adm-262",
   "component": "apps/ticvai-web/src/routes/commercial/InventoryCapacityChannelAllocation.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-258"
   ],
   "exitTo": [
    "ADM-258"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-258, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-258",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F166 step 8→9",
     "operation": "listInventoryCapacityChannel"
    }
   ]
  },
  "density": "compact",
  "purposeNote": "exceed the underlying approved inventory/capacity.",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Control how much product inventory or event capacity is available to each sales channel.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every inventory capacity channel",
       "columns": [
        "InventoryCapacityChannelAllocationView.allocated",
        "InventoryCapacityChannelAllocationView.sold",
        "InventoryCapacityChannelAllocationView.held",
        "InventoryCapacityChannelAllocationView.remaining",
        "InventoryCapacityChannelAllocationView.utilization",
        "InventoryCapacityChannelAllocationView.released",
        "InventoryCapacityChannelAllocationView.returned"
       ],
       "bindsTo": "InventoryCapacityChannelAllocationView",
       "operation": "listInventoryCapacityChannel",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 10 §Display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected inventory capacity channel",
       "bindsTo": "InventoryCapacityChannelAllocationView",
       "columns": [
        "InventoryCapacityChannelAllocationView.allocated",
        "InventoryCapacityChannelAllocationView.sold",
        "InventoryCapacityChannelAllocationView.held",
        "InventoryCapacityChannelAllocationView.remaining",
        "InventoryCapacityChannelAllocationView.utilization",
        "InventoryCapacityChannelAllocationView.released",
        "InventoryCapacityChannelAllocationView.returned"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Shared Pool”, “Dedicated Allocation”, “Percentage Allocation”, “Dynamic Allocation”.",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 10 §Display"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The inventory capacity channel list.",
   "error": "Could not load. Names which read failed and leaves the inventory capacity channel untouched.",
   "emptyFirstRun": "No inventory capacity channel yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the inventory capacity channel are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listInventoryCapacityChannel",
    "contract": "catalogue",
    "purpose": "Inventory, Capacity & Channel Allocation",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "InventoryCapacityChannelAllocationView.allocated",
    "InventoryCapacityChannelAllocationView.sold",
    "InventoryCapacityChannelAllocationView.held",
    "InventoryCapacityChannelAllocationView.remaining",
    "InventoryCapacityChannelAllocationView.utilization",
    "InventoryCapacityChannelAllocationView.released"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-262",
   "workshopBoard": "wireframes/WS138 Sales Channel Management Board 1.dc.html#adm-262"
  },
  "apisNote": "Regenerated 9 September 2026 from Sales_Channel_Management_Reference.pdf page 10. 7 of 7 labels bound to a contract property; 18 of 35 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "_platform": {
   "code": "P09",
   "audience": "platformAdmin",
   "formFactor": "web",
   "shortName": "TICVAI Web",
   "name": "TICVAI Web — Platform Console",
   "offlineCapable": false,
   "app": "ticvai-web",
   "operator": "ticvai",
   "targetApp": {
    "app": "ticvai-control",
    "name": "TICVAI Control",
    "shell": "web",
    "siblings": [
     "P10",
     "P11",
     "P14",
     "P17"
    ],
    "note": "**TICVAI operates all five**, whoever signs in. The partner portal, the accreditation intake, the developer portal and the sign-up are outward faces of the control plane, not separate products — but their users are not TICVAI staff, and the permission model has to hold that line. **P17 added 11 September 2026**: a prospect buying TICVAI has no tenant and no cell, so the control plane is the only thing that can serve them.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "ADM-263",
  "name": "Channel Sales Schedule & Availability Windows",
  "module": "Commercial",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Sales_Channel_Management_Reference.pdf",
   "board": "1",
   "number": "4.1.6",
   "page": 11
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/channel-sales-schedule-availability-windows-adm-263",
   "component": "apps/ticvai-web/src/routes/commercial/ChannelSalesScheduleAvailabilityWindows.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-258"
   ],
   "exitTo": [
    "ADM-258"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-258, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-258",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F166 step 10→11",
     "operation": "listChannelSaleSchedule"
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Every channel can have independently governed selling windows without modifying the underlying product validity.",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Control when each channel is permitted to sell.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "Active selling periods",
       "bindsTo": "ChannelSalesScheduleAvailabilityWindowsSummary.activeSellingPeriods",
       "operation": "listChannelSaleSchedule",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Scheduled openings",
       "bindsTo": "ChannelSalesScheduleAvailabilityWindowsSummary.scheduledOpenings",
       "operation": "listChannelSaleSchedule",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Scheduled closures",
       "bindsTo": "ChannelSalesScheduleAvailabilityWindowsSummary.scheduledClosures",
       "operation": "listChannelSaleSchedule",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Blackouts",
       "bindsTo": "ChannelSalesScheduleAvailabilityWindowsSummary.blackouts",
       "operation": "listChannelSaleSchedule",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Conflicts",
       "bindsTo": "ChannelSalesScheduleAvailabilityWindowsSummary.conflicts",
       "operation": "listChannelSaleSchedule",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Event dates",
       "bindsTo": "ChannelSalesScheduleAvailabilityWindowsSummary.eventDates",
       "operation": "listChannelSaleSchedule",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every channel sales schedule",
       "bindsTo": "ChannelSalesScheduleAvailabilityWindowsView",
       "operation": "listChannelSaleSchedule",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 11 §Display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected channel sales schedule",
       "bindsTo": "ChannelSalesScheduleAvailabilityWindowsView",
       "notes": "The pack groups this record's detail under its own headings: “Channel-Specific Scheduling”, “Automated Actions”.",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 11 §Display"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Save channel sales rule",
       "operation": "setChannelSalesRule",
       "permission": "PRODUCT_CONFIGURE",
       "notes": "**One rule on a channel** (29 September, writers pass).",
       "provenance": "contract catalogue.yaml PUT /channel-sales-rules/{ruleId}"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The channel sales schedule list.",
   "error": "Could not load. Names which read failed and leaves the channel sales schedule untouched.",
   "emptyFirstRun": "No channel sales schedule yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the channel sales schedule are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listChannelSaleSchedule",
    "contract": "catalogue",
    "purpose": "Channel Sales Schedule & Availability Windows",
    "trigger": "onLoad"
   },
   {
    "operationId": "setChannelSalesRule",
    "contract": "catalogue",
    "purpose": "Create or replace a channel sales window, limit or eligibility rule",
    "trigger": "onAction",
    "invalidates": [
     "listChannelSaleSchedule"
    ]
   }
  ],
  "entryState": {
   "preloaded": [
    "ChannelSalesScheduleAvailabilityWindowsSummary.activeSellingPeriods",
    "ChannelSalesScheduleAvailabilityWindowsSummary.scheduledOpenings",
    "ChannelSalesScheduleAvailabilityWindowsSummary.scheduledClosures",
    "ChannelSalesScheduleAvailabilityWindowsSummary.blackouts",
    "ChannelSalesScheduleAvailabilityWindowsSummary.conflicts",
    "ChannelSalesScheduleAvailabilityWindowsSummary.eventDates"
   ],
   "params": [
    {
     "name": "ruleId",
     "from": "navigation",
     "optional": true
    }
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-263",
   "workshopBoard": "wireframes/WS138 Sales Channel Management Board 1.dc.html#adm-263"
  },
  "apisNote": "Regenerated 9 September 2026 from Sales_Channel_Management_Reference.pdf page 11. 6 of 6 labels bound to a contract property; 15 of 32 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "overlays": [
   {
    "id": "formSetChannelSalesRule",
    "component": "modal",
    "trigger": "Save channel sales rule",
    "body": "**Collects what `setChannelSalesRule` sends before it is called.** Required: `id`, `scopePath`, `salesChannelId`, `ruleKind`, `isActive`. Optional: `productId`, `name`, `ruleLevel`, `overridesProductRule`, `effectiveFrom`, `effectiveTo`, `salesStartDate`, `salesStartTime`, `salesEndDate`, `salesEndTime`, `timeZone`, `daysOfWeek` and 31 more. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "ChannelSalesRule",
    "confirm": {
     "label": "Save channel sales rule",
     "operation": "setChannelSalesRule"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "scopePath",
      "salesChannelId",
      "ruleKind",
      "isActive",
      "productId",
      "name",
      "ruleLevel",
      "overridesProductRule",
      "effectiveFrom",
      "effectiveTo",
      "salesStartDate",
      "salesStartTime",
      "salesEndDate",
      "salesEndTime",
      "timeZone",
      "daysOfWeek",
      "hoursOfOperation"
     ]
    },
    "provenance": "contract catalogue.yaml PUT /channel-sales-rules/{ruleId}"
   }
  ],
  "_platform": {
   "code": "P09",
   "audience": "platformAdmin",
   "formFactor": "web",
   "shortName": "TICVAI Web",
   "name": "TICVAI Web — Platform Console",
   "offlineCapable": false,
   "app": "ticvai-web",
   "operator": "ticvai",
   "targetApp": {
    "app": "ticvai-control",
    "name": "TICVAI Control",
    "shell": "web",
    "siblings": [
     "P10",
     "P11",
     "P14",
     "P17"
    ],
    "note": "**TICVAI operates all five**, whoever signs in. The partner portal, the accreditation intake, the developer portal and the sign-up are outward faces of the control plane, not separate products — but their users are not TICVAI staff, and the permission model has to hold that line. **P17 added 11 September 2026**: a prospect buying TICVAI has no tenant and no cell, so the control plane is the only thing that can serve them.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "ADM-264",
  "name": "Customer & Eligibility Rules by Channel",
  "module": "Commercial",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Sales_Channel_Management_Reference.pdf",
   "board": "1",
   "number": "4.1.7",
   "page": 12
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/customer-eligibility-rules-by-channel-adm-264",
   "component": "apps/ticvai-web/src/routes/commercial/CustomerEligibilityRulesByChannel.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-258"
   ],
   "exitTo": [
    "ADM-258"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-258, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-258",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F166 step 12→13",
     "operation": "listCustomerEligibilityRule"
    }
   ]
  },
  "density": "compact",
  "purposeNote": "purchased.",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population",
  "purpose": "Determine who is allowed to purchase through a particular channel.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Guest allowed",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 12 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Login required",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 12 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Membership required",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 12 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Corporate account required",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 12 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Identity verification required",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 12 §Configure"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Save channel sales rule",
       "operation": "setChannelSalesRule",
       "permission": "PRODUCT_CONFIGURE",
       "notes": "**One rule on a channel** (29 September, writers pass).",
       "provenance": "contract catalogue.yaml PUT /channel-sales-rules/{ruleId}"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The customer eligibility rules configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the customer eligibility rules untouched.",
   "emptyFirstRun": "No customer eligibility rules configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listCustomerEligibilityRule",
    "contract": "catalogue",
    "purpose": "Customer & Eligibility Rules by Channel",
    "trigger": "onLoad"
   },
   {
    "operationId": "setChannelSalesRule",
    "contract": "catalogue",
    "purpose": "Create or replace a channel sales window, limit or eligibility rule",
    "trigger": "onAction",
    "invalidates": [
     "listCustomerEligibilityRule"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-264",
   "workshopBoard": "wireframes/WS138 Sales Channel Management Board 1.dc.html#adm-264"
  },
  "apisNote": "Regenerated 9 September 2026 from Sales_Channel_Management_Reference.pdf page 12. 0 of 0 labels bound to a contract property; 5 of 29 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "overlays": [
   {
    "id": "formSetChannelSalesRule",
    "component": "modal",
    "trigger": "Save channel sales rule",
    "body": "**Collects what `setChannelSalesRule` sends before it is called.** Required: `id`, `scopePath`, `salesChannelId`, `ruleKind`, `isActive`. Optional: `productId`, `name`, `ruleLevel`, `overridesProductRule`, `effectiveFrom`, `effectiveTo`, `salesStartDate`, `salesStartTime`, `salesEndDate`, `salesEndTime`, `timeZone`, `daysOfWeek` and 31 more. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "ChannelSalesRule",
    "confirm": {
     "label": "Save channel sales rule",
     "operation": "setChannelSalesRule"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "scopePath",
      "salesChannelId",
      "ruleKind",
      "isActive",
      "productId",
      "name",
      "ruleLevel",
      "overridesProductRule",
      "effectiveFrom",
      "effectiveTo",
      "salesStartDate",
      "salesStartTime",
      "salesEndDate",
      "salesEndTime",
      "timeZone",
      "daysOfWeek",
      "hoursOfOperation"
     ]
    },
    "provenance": "contract catalogue.yaml PUT /channel-sales-rules/{ruleId}"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "ruleId",
     "from": "navigation",
     "optional": true
    }
   ]
  },
  "_platform": {
   "code": "P09",
   "audience": "platformAdmin",
   "formFactor": "web",
   "shortName": "TICVAI Web",
   "name": "TICVAI Web — Platform Console",
   "offlineCapable": false,
   "app": "ticvai-web",
   "operator": "ticvai",
   "targetApp": {
    "app": "ticvai-control",
    "name": "TICVAI Control",
    "shell": "web",
    "siblings": [
     "P10",
     "P11",
     "P14",
     "P17"
    ],
    "note": "**TICVAI operates all five**, whoever signs in. The partner portal, the accreditation intake, the developer portal and the sign-up are outward faces of the control plane, not separate products — but their users are not TICVAI staff, and the permission model has to hold that line. **P17 added 11 September 2026**: a prospect buying TICVAI has no tenant and no cell, so the control plane is the only thing that can serve them.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "ADM-265",
  "name": "Channel Sales Rules, Limits & Restrictions",
  "module": "Commercial",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Sales_Channel_Management_Reference.pdf",
   "board": "1",
   "number": "4.1.8",
   "page": 13
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/channel-sales-rules-limits-restrictions-adm-265",
   "component": "apps/ticvai-web/src/routes/commercial/ChannelSalesRulesLimitsRestrictions.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-258"
   ],
   "exitTo": [
    "ADM-258"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-258, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-258",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F166 step 14→15",
     "operation": "listChannelSaleRule"
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Administrators can enforce channel-specific operational and transaction restrictions without changing the master product definition.",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population",
  "purpose": "Configure operational restrictions that apply specifically to a sales channel.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Minimum Quantity",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 13 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Maximum Quantity",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 13 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Maximum Per Transaction",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 13 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Maximum Per Customer",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 13 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Maximum Per Day",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 13 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Maximum Per Event",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 13 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Maximum Per Product",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 13 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Reservation permitted",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 13 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Hold permitted",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 13 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Payment link permitted",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 13 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Partial payment permitted",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 13 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Split payment permitted",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 13 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Discount permitted",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 13 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Promo code permitted",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 13 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Upgrade permitted",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 13 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Exchange permitted",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 13 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Reschedule permitted",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 13 §Configure"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Save channel sales rule",
       "operation": "setChannelSalesRule",
       "permission": "PRODUCT_CONFIGURE",
       "notes": "**One rule on a channel** (29 September, writers pass).",
       "provenance": "contract catalogue.yaml PUT /channel-sales-rules/{ruleId}"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The channel sales rules configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the channel sales rules untouched.",
   "emptyFirstRun": "No channel sales rules configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listChannelSaleRule",
    "contract": "catalogue",
    "purpose": "Channel Sales Rules, Limits & Restrictions",
    "trigger": "onLoad"
   },
   {
    "operationId": "setChannelSalesRule",
    "contract": "catalogue",
    "purpose": "Create or replace a channel sales window, limit or eligibility rule",
    "trigger": "onAction",
    "invalidates": [
     "listChannelSaleRule"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-265",
   "workshopBoard": "wireframes/WS138 Sales Channel Management Board 1.dc.html#adm-265"
  },
  "apisNote": "Regenerated 9 September 2026 from Sales_Channel_Management_Reference.pdf page 13. 0 of 0 labels bound to a contract property; 17 of 33 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "overlays": [
   {
    "id": "formSetChannelSalesRule",
    "component": "modal",
    "trigger": "Save channel sales rule",
    "body": "**Collects what `setChannelSalesRule` sends before it is called.** Required: `id`, `scopePath`, `salesChannelId`, `ruleKind`, `isActive`. Optional: `productId`, `name`, `ruleLevel`, `overridesProductRule`, `effectiveFrom`, `effectiveTo`, `salesStartDate`, `salesStartTime`, `salesEndDate`, `salesEndTime`, `timeZone`, `daysOfWeek` and 31 more. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "ChannelSalesRule",
    "confirm": {
     "label": "Save channel sales rule",
     "operation": "setChannelSalesRule"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "scopePath",
      "salesChannelId",
      "ruleKind",
      "isActive",
      "productId",
      "name",
      "ruleLevel",
      "overridesProductRule",
      "effectiveFrom",
      "effectiveTo",
      "salesStartDate",
      "salesStartTime",
      "salesEndDate",
      "salesEndTime",
      "timeZone",
      "daysOfWeek",
      "hoursOfOperation"
     ]
    },
    "provenance": "contract catalogue.yaml PUT /channel-sales-rules/{ruleId}"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "ruleId",
     "from": "navigation",
     "optional": true
    }
   ]
  },
  "_platform": {
   "code": "P09",
   "audience": "platformAdmin",
   "formFactor": "web",
   "shortName": "TICVAI Web",
   "name": "TICVAI Web — Platform Console",
   "offlineCapable": false,
   "app": "ticvai-web",
   "operator": "ticvai",
   "targetApp": {
    "app": "ticvai-control",
    "name": "TICVAI Control",
    "shell": "web",
    "siblings": [
     "P10",
     "P11",
     "P14",
     "P17"
    ],
    "note": "**TICVAI operates all five**, whoever signs in. The partner portal, the accreditation intake, the developer portal and the sign-up are outward faces of the control plane, not separate products — but their users are not TICVAI staff, and the permission model has to hold that line. **P17 added 11 September 2026**: a prospect buying TICVAI has no tenant and no cell, so the control plane is the only thing that can serve them.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "ADM-266",
  "name": "Channel Fees, Payment & Fulfillment Configuration",
  "module": "Commercial",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Sales_Channel_Management_Reference.pdf",
   "board": "1",
   "number": "4.1.9",
   "page": 14
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/channel-fees-payment-fulfillment-configuration-adm-266",
   "component": "apps/ticvai-web/src/routes/commercial/ChannelFeesPaymentFulfillmentConfiguration.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-258"
   ],
   "exitTo": [
    "ADM-258"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-258, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-258",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F166 step 16→17",
     "operation": "setChannelFeePayment"
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Each channel exposes only approved payment, fee and fulfillment methods supported by its operational configuration.",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population",
  "purpose": "Define the commercial and fulfillment behavior associated with each channel.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Digital Ticket",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 14 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Email",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 14 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Mobile App",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 14 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Apple/Google Wallet",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 14 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Print at Home",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 14 §Configure"
      },
      {
       "kind": "selectField",
       "label": "POS Print",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 14 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Kiosk Print",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 14 §Configure"
      },
      {
       "kind": "selectField",
       "label": "RFID",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 14 §Configure"
      },
      {
       "kind": "selectField",
       "label": "NFC",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 14 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Wristband",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 14 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Collection",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 14 §Configure"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Save changes",
       "provenance": "contract operation setChannelFeePayment"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The channel fees payment configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the channel fees payment untouched.",
   "emptyFirstRun": "No channel fees payment configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setChannelFeePayment",
    "contract": "catalogue",
    "purpose": "Channel Fees, Payment & Fulfillment Configuration",
    "trigger": "onAction"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-266",
   "workshopBoard": "wireframes/WS138 Sales Channel Management Board 1.dc.html#adm-266"
  },
  "apisNote": "Regenerated 9 September 2026 from Sales_Channel_Management_Reference.pdf page 14. 0 of 0 labels bound to a contract property; 11 of 42 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "_platform": {
   "code": "P09",
   "audience": "platformAdmin",
   "formFactor": "web",
   "shortName": "TICVAI Web",
   "name": "TICVAI Web — Platform Console",
   "offlineCapable": false,
   "app": "ticvai-web",
   "operator": "ticvai",
   "targetApp": {
    "app": "ticvai-control",
    "name": "TICVAI Control",
    "shell": "web",
    "siblings": [
     "P10",
     "P11",
     "P14",
     "P17"
    ],
    "note": "**TICVAI operates all five**, whoever signs in. The partner portal, the accreditation intake, the developer portal and the sign-up are outward faces of the control plane, not separate products — but their users are not TICVAI staff, and the permission model has to hold that line. **P17 added 11 September 2026**: a prospect buying TICVAI has no tenant and no cell, so the control plane is the only thing that can serve them.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "ADM-267",
  "name": "Channel Publication, Readiness & AI Validation",
  "module": "Commercial",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Sales_Channel_Management_Reference.pdf",
   "board": "1",
   "number": "4.1.10",
   "page": 16
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/channel-publication-readiness-ai-validation-adm-267",
   "component": "apps/ticvai-web/src/routes/commercial/ChannelPublicationReadinessAiValidation.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-258"
   ],
   "exitTo": [
    "ADM-258"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-258, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation."
  },
  "density": "compact",
  "purposeNote": "No sales channel becomes operational until its required product, pricing, capacity, schedule, payment, fulfillment and governance dependencies have passed configured readiness validation. Board 1 — Final Screen Register",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configuration works) and no display directory — it is settings, not a population",
  "purpose": "Perform final validation before a sales channel or channel/product configuration becomes commercially active. Board 2 manages the live operational layer of TICVAI's sales-channel ecosystem after channels have been configured and activated in Board 1.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "textField",
       "label": "4.1.1 Channel Publication, Readiness & AI",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 16 §Configuration works"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Publish",
       "provenance": "contract operation publishChannelReadinessValidation"
      },
      {
       "kind": "banner",
       "label": "Permissions this screen separates",
       "notes": "**The pack separates these permissions and no action on the screen claims them yet:** Validate, Preview, Submit for Approval, Schedule Activation, Activate, Return for Changes, Suspend. Each needs attaching to the control it gates, or the screen needs the control.",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 16 §Authorized users can"
      },
      {
       "kind": "publishGate",
       "label": "What publishing changes",
       "notes": "**Names what goes live, where, and from when.** A publish with no stated consequence is one somebody presses meaning to save.",
       "provenance": "authored — required by check-screens for publishChannelReadinessValidation"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The channel publication readiness configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the channel publication readiness untouched.",
   "emptyFirstRun": "No channel publication readiness configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "publishChannelReadinessValidation",
    "contract": "catalogue",
    "purpose": "Channel Publication, Readiness & AI Validation",
    "trigger": "onAction"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-267",
   "workshopBoard": "wireframes/WS138 Sales Channel Management Board 1.dc.html#adm-267"
  },
  "apisNote": "Regenerated 9 September 2026 from Sales_Channel_Management_Reference.pdf page 16. 0 of 0 labels bound to a contract property; 8 of 88 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "_platform": {
   "code": "P09",
   "audience": "platformAdmin",
   "formFactor": "web",
   "shortName": "TICVAI Web",
   "name": "TICVAI Web — Platform Console",
   "offlineCapable": false,
   "app": "ticvai-web",
   "operator": "ticvai",
   "targetApp": {
    "app": "ticvai-control",
    "name": "TICVAI Control",
    "shell": "web",
    "siblings": [
     "P10",
     "P11",
     "P14",
     "P17"
    ],
    "note": "**TICVAI operates all five**, whoever signs in. The partner portal, the accreditation intake, the developer portal and the sign-up are outward faces of the control plane, not separate products — but their users are not TICVAI staff, and the permission model has to hold that line. **P17 added 11 September 2026**: a prospect buying TICVAI has no tenant and no cell, so the control plane is the only thing that can serve them.",
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
 "createChannelProfile": {
  "method": "POST",
  "path": "/channel-profile",
  "contract": "catalogue",
  "summary": "Channel Creation & Profile Configuration",
  "permission": "PRODUCT_CONFIGURE",
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
  "requestBody": "ChannelCreationProfileConfigurationInput",
  "responds": "ChannelCreationProfileConfigurationView"
 },
 "listChannelSaleRule": {
  "method": "GET",
  "path": "/channel-sale-rule",
  "contract": "catalogue",
  "summary": "Channel Sales Rules, Limits & Restrictions",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "channel",
    "in": "query",
    "required": false
   },
   {
    "name": "product",
    "in": "query",
    "required": false
   },
   {
    "name": "ruleLevel",
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
 "listChannelSaleSchedule": {
  "method": "GET",
  "path": "/channel-sale-schedule",
  "contract": "catalogue",
  "summary": "Channel Sales Schedule & Availability Windows",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "channel",
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
    "name": "from",
    "in": "query",
    "required": false
   },
   {
    "name": "to",
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
 "listCustomerEligibilityRule": {
  "method": "GET",
  "path": "/customer-eligibility-rule",
  "contract": "catalogue",
  "summary": "Customer & Eligibility Rules by Channel",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "channel",
    "in": "query",
    "required": false
   },
   {
    "name": "product",
    "in": "query",
    "required": false
   },
   {
    "name": "dimension",
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
 "listInventoryCapacityChannel": {
  "method": "GET",
  "path": "/inventory-capacity-channel",
  "contract": "catalogue",
  "summary": "Inventory, Capacity & Channel Allocation",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
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
    "name": "channel",
    "in": "query",
    "required": false
   },
   {
    "name": "venue",
    "in": "query",
    "required": false
   },
   {
    "name": "allocationType",
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
 "listSaleChannel": {
  "method": "GET",
  "path": "/sale-channel",
  "contract": "catalogue",
  "summary": "Sales Channel Command Center",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "channelType",
    "in": "query",
    "required": false
   },
   {
    "name": "status",
    "in": "query",
    "required": false
   },
   {
    "name": "venue",
    "in": "query",
    "required": false
   },
   {
    "name": "brand",
    "in": "query",
    "required": false
   },
   {
    "name": "search",
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
 "publishChannelReadinessValidation": {
  "method": "PUT",
  "path": "/channel-readiness-validation",
  "contract": "catalogue",
  "summary": "Channel Publication, Readiness & AI Validation",
  "permission": "PRODUCT_CONFIGURE",
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
  "requestBody": "ChannelPublicationReadinessAiValidationInput",
  "responds": "ChannelPublicationReadinessAiValidationView"
 },
 "setChannelFeePayment": {
  "method": "PUT",
  "path": "/channel-fee-payment",
  "contract": "catalogue",
  "summary": "Channel Fees, Payment & Fulfillment Configuration",
  "permission": "PRODUCT_CONFIGURE",
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
  "requestBody": "ChannelFeesPaymentFulfillmentConfigurationInput",
  "responds": "ChannelFeesPaymentFulfillmentConfigurationView"
 },
 "setChannelPricingCommercial": {
  "method": "PUT",
  "path": "/channel-pricing-commercial",
  "contract": "catalogue",
  "summary": "Channel Pricing & Commercial Profile Assignment",
  "permission": "PRODUCT_CONFIGURE",
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
  "requestBody": "ChannelPricingCommercialProfileAssignmentInput",
  "responds": "ChannelPricingCommercialProfileAssignmentView"
 },
 "setChannelSalesRule": {
  "method": "PUT",
  "path": "/channel-sales-rules/{ruleId}",
  "contract": "catalogue",
  "summary": "Create or replace a channel sales window, limit or eligibility rule",
  "permission": "PRODUCT_CONFIGURE",
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
  "requestBody": "ChannelSalesRule",
  "responds": "ChannelSalesRule"
 },
 "setProductCatalogue": {
  "method": "PUT",
  "path": "/product-catalogue",
  "contract": "catalogue",
  "summary": "Product & Catalogue Assignment",
  "permission": "PRODUCT_CONFIGURE",
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
  "requestBody": "ProductCatalogueAssignmentInput",
  "responds": "ProductCatalogueAssignmentView"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "ChannelCreationProfileConfigurationInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures",
  "description": "**What Channel Creation & Profile Configuration submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "channelName": {
    "type": "string",
    "description": "Channel Name (internal)",
    "maxLength": 120
   },
   "channelCode": {
    "type": "string",
    "description": "Channel Code: unique within the tenant, 2-20 upper-case letters, digits or hyphens (decided 29 September, readiness close-out)",
    "pattern": "^[A-Z0-9-]{2,20}$"
   },
   "channelType": {
    "type": "string",
    "enum": [
     "b2cWeb",
     "b2cMobileApp",
     "pos",
     "mobilePos",
     "flyingPos",
     "kiosk",
     "callCentre",
     "b2bPortal",
     "reseller",
     "ota",
     "api",
     "partnerPortal",
     "marketplace",
     "thirdPartyChannel",
     "customChannel"
    ],
    "description": "Channel Type (pack p.3-4 Channel Types). The type decides which configuration applies (p.6); each type reports under one SalesChannel value (see salesChannel)"
   },
   "internalDescription": {
    "type": "string",
    "description": "Internal Description"
   },
   "customerFacingName": {
    "type": "string",
    "description": "Customer-Facing Name",
    "maxLength": 120
   },
   "brand": {
    "type": "string",
    "description": "Brand ID"
   },
   "businessUnit": {
    "type": "string",
    "description": "Business Unit ID"
   },
   "country": {
    "type": "string",
    "description": "Country: ISO 3166-1 alpha-2",
    "pattern": "^[A-Z]{2}$"
   },
   "market": {
    "type": "string",
    "description": "Market (a configured market code)"
   },
   "currency": {
    "type": "string",
    "description": "Currency: ISO 4217 code",
    "pattern": "^[A-Z]{3}$"
   },
   "timeZone": {
    "type": "string",
    "description": "Time Zone: IANA name, e.g. Asia/Dubai"
   },
   "owner": {
    "type": "string",
    "description": "Owner (user ID)"
   },
   "responsibleDepartment": {
    "type": "string",
    "description": "Responsible Department"
   },
   "venue": {
    "type": "string",
    "description": "Venue ID: required for the POS types (pack p.6) and when scopeLevel is venue",
    "nullable": true
   },
   "workstationGroups": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Workstation groups (IDs) that may sell on a POS-type channel (pack p.6)"
   },
   "cashierAccess": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Cashier access: role IDs allowed to sell on a POS-type channel (pack p.6)"
   },
   "webstore": {
    "type": "string",
    "description": "Webstore ID for a B2C-type channel (pack p.6)",
    "nullable": true
   },
   "domainBrand": {
    "type": "string",
    "description": "Domain/brand: the storefront domain for a B2C-type channel (pack p.6)",
    "nullable": true
   },
   "digitalCustomerJourney": {
    "type": "string",
    "description": "Digital customer journey: the checkout journey template ID for a B2C-type channel (pack p.6)",
    "nullable": true
   },
   "partner": {
    "type": "string",
    "description": "Partner ID for an OTA, reseller or partner channel (pack p.6); the partner record lives in B2B/OTA",
    "nullable": true
   },
   "apiConnection": {
    "type": "string",
    "description": "API connection: the connector ID from ADM-269 for an OTA/API channel (pack p.6); the external platform is named as data on the connector",
    "nullable": true
   },
   "commercialOwner": {
    "type": "string",
    "description": "Commercial Owner (user ID)"
   },
   "operationalOwner": {
    "type": "string",
    "description": "Operational Owner (user ID)"
   },
   "technicalOwner": {
    "type": "string",
    "description": "Technical Owner (user ID)"
   },
   "financeOwner": {
    "type": "string",
    "description": "Finance Owner (user ID)"
   },
   "scopeLevel": {
    "type": "string",
    "enum": [
     "global",
     "country",
     "region",
     "venue",
     "attraction",
     "event",
     "location",
     "businessUnit"
    ],
    "description": "Operational Scope level (pack p.6)"
   },
   "scopeId": {
    "type": "string",
    "description": "ID of the scoped item (country code, region, venue, attraction, event, location or business unit); empty for global",
    "nullable": true
   },
   "salesChannel": {
    "$ref": "../shared/common.yaml#/components/schemas/SalesChannel",
    "description": "The shared reporting dimension for this channel; defaults from channelType (see listSaleChannel) (decided 29 September, readiness close-out)"
   }
  }
 },
 "ChannelCreationProfileConfigurationView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over catalogue state, assembled at read time from tables that already exist",
  "description": "**What Channel Creation & Profile Configuration displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "channelName": {
    "type": "string",
    "description": "Channel Name (internal)",
    "maxLength": 120
   },
   "channelCode": {
    "type": "string",
    "description": "Channel Code: unique within the tenant, 2-20 upper-case letters, digits or hyphens (decided 29 September, readiness close-out)",
    "pattern": "^[A-Z0-9-]{2,20}$"
   },
   "channelType": {
    "type": "string",
    "enum": [
     "b2cWeb",
     "b2cMobileApp",
     "pos",
     "mobilePos",
     "flyingPos",
     "kiosk",
     "callCentre",
     "b2bPortal",
     "reseller",
     "ota",
     "api",
     "partnerPortal",
     "marketplace",
     "thirdPartyChannel",
     "customChannel"
    ],
    "description": "Channel Type (pack p.3-4 Channel Types). The type decides which configuration applies (p.6); each type reports under one SalesChannel value (see salesChannel)"
   },
   "internalDescription": {
    "type": "string",
    "description": "Internal Description"
   },
   "customerFacingName": {
    "type": "string",
    "description": "Customer-Facing Name",
    "maxLength": 120
   },
   "tenant": {
    "type": "string",
    "description": "Tenant"
   },
   "brand": {
    "type": "string",
    "description": "Brand ID"
   },
   "businessUnit": {
    "type": "string",
    "description": "Business Unit ID"
   },
   "country": {
    "type": "string",
    "description": "Country: ISO 3166-1 alpha-2",
    "pattern": "^[A-Z]{2}$"
   },
   "market": {
    "type": "string",
    "description": "Market (a configured market code)"
   },
   "currency": {
    "type": "string",
    "description": "Currency: ISO 4217 code",
    "pattern": "^[A-Z]{3}$"
   },
   "timeZone": {
    "type": "string",
    "description": "Time Zone: IANA name, e.g. Asia/Dubai"
   },
   "owner": {
    "type": "string",
    "description": "Owner (user ID)"
   },
   "responsibleDepartment": {
    "type": "string",
    "description": "Responsible Department"
   },
   "venue": {
    "type": "string",
    "description": "Venue ID: required for the POS types (pack p.6) and when scopeLevel is venue",
    "nullable": true
   },
   "workstationGroups": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Workstation groups (IDs) that may sell on a POS-type channel (pack p.6)"
   },
   "cashierAccess": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Cashier access: role IDs allowed to sell on a POS-type channel (pack p.6)"
   },
   "webstore": {
    "type": "string",
    "description": "Webstore ID for a B2C-type channel (pack p.6)",
    "nullable": true
   },
   "domainBrand": {
    "type": "string",
    "description": "Domain/brand: the storefront domain for a B2C-type channel (pack p.6)",
    "nullable": true
   },
   "digitalCustomerJourney": {
    "type": "string",
    "description": "Digital customer journey: the checkout journey template ID for a B2C-type channel (pack p.6)",
    "nullable": true
   },
   "partner": {
    "type": "string",
    "description": "Partner ID for an OTA, reseller or partner channel (pack p.6); the partner record lives in B2B/OTA",
    "nullable": true
   },
   "apiConnection": {
    "type": "string",
    "description": "API connection: the connector ID from ADM-269 for an OTA/API channel (pack p.6); the external platform is named as data on the connector",
    "nullable": true
   },
   "commercialOwner": {
    "type": "string",
    "description": "Commercial Owner (user ID)"
   },
   "operationalOwner": {
    "type": "string",
    "description": "Operational Owner (user ID)"
   },
   "technicalOwner": {
    "type": "string",
    "description": "Technical Owner (user ID)"
   },
   "financeOwner": {
    "type": "string",
    "description": "Finance Owner (user ID)"
   },
   "scopeLevel": {
    "type": "string",
    "enum": [
     "global",
     "country",
     "region",
     "venue",
     "attraction",
     "event",
     "location",
     "businessUnit"
    ],
    "description": "Operational Scope level (pack p.6)"
   },
   "scopeId": {
    "type": "string",
    "description": "ID of the scoped item (country code, region, venue, attraction, event, location or business unit); empty for global",
    "nullable": true
   },
   "salesChannel": {
    "$ref": "../shared/common.yaml#/components/schemas/SalesChannel",
    "description": "The shared reporting dimension for this channel; defaults from channelType (see listSaleChannel) (decided 29 September, readiness close-out)"
   },
   "channelId": {
    "type": "string",
    "description": "Channel ID, assigned by TICVAI",
    "readOnly": true
   },
   "status": {
    "type": "string",
    "description": "Status: draft, configuration, validation, approved, scheduled, active, suspended, disabled or archived (the pack's suggested lifecycle, p.5); a new channel starts in draft",
    "readOnly": true
   }
  }
 },
 "ChannelFeesPaymentFulfillmentConfigurationInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures",
  "description": "**What Channel Fees, Payment & Fulfillment Configuration submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "channelId": {
    "type": "string",
    "description": "Channel ID"
   },
   "fees": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "feeType": {
       "type": "string",
       "enum": [
        "booking",
        "transaction",
        "channel",
        "service",
        "delivery",
        "payment"
       ]
      },
      "feeProfileId": {
       "type": "string"
      }
     }
    },
    "description": "Fee Associations (pack p.14-15): which approved fee profile applies for each fee type; amounts are the Pricing/Fee Engine's"
   },
   "paymentMethods": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "card",
      "cash",
      "digitalWallet",
      "paymentLink",
      "accountCredit",
      "b2bCredit"
     ]
    },
    "description": "Payment Methods the channel may expose (pack p.15)"
   },
   "otherPaymentMethodCodes": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Other configured payment methods, by their Payment configuration code"
   },
   "fulfillmentMethods": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "digitalTicket",
      "email",
      "mobileApp",
      "appleGoogleWallet",
      "printAtHome",
      "posPrint",
      "kioskPrint",
      "rfid",
      "nfc",
      "wristband",
      "collection",
      "voucher",
      "apiTicketDelivery",
      "bulkCsvExport"
     ]
    },
    "description": "Fulfillment Methods (pack p.15-16; bulkCsvExport is the pre-generated ticket batch for partners that do not integrate, MoM 31 Aug §4.3)"
   }
  }
 },
 "ChannelFeesPaymentFulfillmentConfigurationView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over catalogue state, assembled at read time from tables that already exist",
  "description": "**What Channel Fees, Payment & Fulfillment Configuration displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "channelId": {
    "type": "string",
    "description": "Channel ID"
   },
   "fees": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "feeType": {
       "type": "string",
       "enum": [
        "booking",
        "transaction",
        "channel",
        "service",
        "delivery",
        "payment"
       ]
      },
      "feeProfileId": {
       "type": "string"
      }
     }
    },
    "description": "Fee Associations (pack p.14-15): which approved fee profile applies for each fee type; amounts are the Pricing/Fee Engine's"
   },
   "paymentMethods": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "card",
      "cash",
      "digitalWallet",
      "paymentLink",
      "accountCredit",
      "b2bCredit"
     ]
    },
    "description": "Payment Methods the channel may expose (pack p.15)"
   },
   "otherPaymentMethodCodes": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Other configured payment methods, by their Payment configuration code"
   },
   "fulfillmentMethods": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "digitalTicket",
      "email",
      "mobileApp",
      "appleGoogleWallet",
      "printAtHome",
      "posPrint",
      "kioskPrint",
      "rfid",
      "nfc",
      "wristband",
      "collection",
      "voucher",
      "apiTicketDelivery",
      "bulkCsvExport"
     ]
    },
    "description": "Fulfillment Methods (pack p.15-16; bulkCsvExport is the pre-generated ticket batch for partners that do not integrate, MoM 31 Aug §4.3)"
   },
   "validationIssues": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "code": {
       "type": "string",
       "enum": [
        "paymentMethodNotApproved",
        "feeProfileMissing",
        "mediaProfileMissing",
        "incompatibleCombination"
       ]
      },
      "message": {
       "type": "string"
      }
     }
    },
    "description": "Validation (pack p.16): incompatible combinations, e.g. RFID fulfilment with no RFID media profile for the venue/channel"
   }
  }
 },
 "ChannelPricingCommercialProfileAssignmentInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table covers these fields** — the closest is catalogue.price_list at 6%, so this is not an update to anything the package stores today and no new table has been decided",
  "description": "**What Channel Pricing & Commercial Profile Assignment submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.\n\n**The pack defines this as a record**, under *For each assignment* - one of only 13 drafted writes that does. That is the client writing a row rather than a screen, and it is where the table conversation should start.",
  "properties": {
   "priceProfile": {
    "type": "string",
    "description": "Price Profile: the ID of the approved price list or profile consumed (the Pricing Engine calculates the price)"
   },
   "currency": {
    "type": "string",
    "description": "Currency: ISO 4217 code",
    "pattern": "^[A-Z]{3}$"
   },
   "effectiveFrom": {
    "type": "string",
    "format": "date",
    "description": "Effective From"
   },
   "effectiveTo": {
    "type": "string",
    "format": "date",
    "description": "Effective To; empty for open-ended",
    "nullable": true
   },
   "venue": {
    "type": "string",
    "description": "Venue ID",
    "nullable": true
   },
   "event": {
    "type": "string",
    "description": "Event ID",
    "nullable": true
   },
   "product": {
    "type": "string",
    "description": "Product ID",
    "nullable": true
   },
   "customerSegment": {
    "type": "string",
    "description": "Customer Segment ID",
    "nullable": true
   },
   "priority": {
    "type": "integer",
    "description": "Priority: when several assignments match, the lower number wins",
    "minimum": 1
   },
   "channelId": {
    "type": "string",
    "description": "Channel ID"
   },
   "pricingSource": {
    "type": "string",
    "enum": [
     "standardPriceList",
     "channelPriceList",
     "b2bRate",
     "resellerRate",
     "otaRate",
     "posPrice",
     "promotionalPriceProfile",
     "dynamicPricingProfile"
    ],
    "description": "Pricing Association (pack p.8): which kind of approved pricing this assignment consumes"
   },
   "overridePermission": {
    "type": "string",
    "description": "Override Permission: the permission a user needs to override price on this channel",
    "nullable": true
   },
   "fixedPriceOnly": {
    "type": "boolean",
    "description": "Price Override Governance: use fixed price only"
   },
   "promotionAllowed": {
    "type": "boolean",
    "description": "Price Override Governance: apply promotion"
   },
   "discountAllowed": {
    "type": "boolean",
    "description": "Price Override Governance: apply discount"
   },
   "priceOverrideAllowed": {
    "type": "boolean",
    "description": "Price Override Governance: override price"
   },
   "overrideRequiresApproval": {
    "type": "boolean",
    "description": "Price Override Governance: require approval for override"
   },
   "dynamicPricingAllowed": {
    "type": "boolean",
    "description": "Price Override Governance: use dynamic pricing"
   }
  },
  "x-ticvai-record-definition": "For each assignment"
 },
 "ChannelPricingCommercialProfileAssignmentView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over catalogue state, assembled at read time from tables that already exist",
  "description": "**What Channel Pricing & Commercial Profile Assignment displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "priceProfile": {
    "type": "string",
    "description": "Price Profile: the ID of the approved price list or profile consumed (the Pricing Engine calculates the price)"
   },
   "currency": {
    "type": "string",
    "description": "Currency: ISO 4217 code",
    "pattern": "^[A-Z]{3}$"
   },
   "effectiveFrom": {
    "type": "string",
    "format": "date",
    "description": "Effective From"
   },
   "effectiveTo": {
    "type": "string",
    "format": "date",
    "description": "Effective To; empty for open-ended",
    "nullable": true
   },
   "venue": {
    "type": "string",
    "description": "Venue ID",
    "nullable": true
   },
   "event": {
    "type": "string",
    "description": "Event ID",
    "nullable": true
   },
   "product": {
    "type": "string",
    "description": "Product ID",
    "nullable": true
   },
   "customerSegment": {
    "type": "string",
    "description": "Customer Segment ID",
    "nullable": true
   },
   "priority": {
    "type": "integer",
    "description": "Priority: when several assignments match, the lower number wins",
    "minimum": 1
   },
   "channelId": {
    "type": "string",
    "description": "Channel ID"
   },
   "pricingSource": {
    "type": "string",
    "enum": [
     "standardPriceList",
     "channelPriceList",
     "b2bRate",
     "resellerRate",
     "otaRate",
     "posPrice",
     "promotionalPriceProfile",
     "dynamicPricingProfile"
    ],
    "description": "Pricing Association (pack p.8): which kind of approved pricing this assignment consumes"
   },
   "overridePermission": {
    "type": "string",
    "description": "Override Permission: the permission a user needs to override price on this channel",
    "nullable": true
   },
   "fixedPriceOnly": {
    "type": "boolean",
    "description": "Price Override Governance: use fixed price only"
   },
   "promotionAllowed": {
    "type": "boolean",
    "description": "Price Override Governance: apply promotion"
   },
   "discountAllowed": {
    "type": "boolean",
    "description": "Price Override Governance: apply discount"
   },
   "priceOverrideAllowed": {
    "type": "boolean",
    "description": "Price Override Governance: override price"
   },
   "overrideRequiresApproval": {
    "type": "boolean",
    "description": "Price Override Governance: require approval for override"
   },
   "dynamicPricingAllowed": {
    "type": "boolean",
    "description": "Price Override Governance: use dynamic pricing"
   },
   "validationIssues": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "code": {
       "type": "string",
       "enum": [
        "missingPrice",
        "expiredPrice",
        "currencyMismatch",
        "conflictingProfiles",
        "invalidOverride"
       ]
      },
      "message": {
       "type": "string"
      }
     }
    },
    "description": "Price Validation (pack p.9)"
   }
  }
 },
 "ChannelPublicationReadinessAiValidationInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures",
  "description": "**What Channel Publication, Readiness & AI Validation submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "channelId": {
    "type": "string",
    "description": "Channel ID"
   },
   "action": {
    "type": "string",
    "enum": [
     "validate",
     "preview",
     "submitForApproval",
     "scheduleActivation",
     "activate",
     "returnForChanges",
     "suspend"
    ],
    "description": "Publication Action (pack p.17)"
   },
   "scheduledAt": {
    "type": "string",
    "format": "date-time",
    "description": "Activation time for scheduleActivation",
    "nullable": true
   },
   "reason": {
    "type": "string",
    "description": "Reason: mandatory when overriding warnings or returning for changes",
    "nullable": true
   },
   "overrideWarnings": {
    "type": "boolean",
    "description": "Proceed despite warnings (needs the override permission and a reason); critical issues cannot be overridden"
   }
  }
 },
 "ChannelPublicationReadinessAiValidationView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over catalogue state, assembled at read time from tables that already exist",
  "description": "**What Channel Publication, Readiness & AI Validation displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "channelId": {
    "type": "string",
    "description": "Channel: the configured channel's ID from the Sales Channel Command Center (ADM-258)"
   },
   "status": {
    "type": "string",
    "description": "Status after the action: draft, configuration, validation, approved, scheduled, active, suspended, disabled or archived (the pack's suggested lifecycle, p.5)"
   },
   "readinessScore": {
    "type": "number",
    "description": "Channel Readiness %",
    "minimum": 0,
    "maximum": 100
   },
   "checklist": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "area": {
       "type": "string",
       "enum": [
        "channelProfile",
        "products",
        "pricing",
        "capacity",
        "schedule",
        "eligibility",
        "salesRules",
        "payment",
        "fulfillment",
        "integration"
       ]
      },
      "result": {
       "type": "string",
       "enum": [
        "passed",
        "warning",
        "failed",
        "notRequired"
       ]
      },
      "scorePercent": {
       "type": "number"
      }
     }
    },
    "description": "Readiness Checklist (pack p.16) with each area's score (p.17)"
   },
   "issues": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "severity": {
       "type": "string",
       "enum": [
        "critical",
        "high",
        "medium",
        "low",
        "recommendation"
       ]
      },
      "area": {
       "type": "string",
       "enum": [
        "channelProfile",
        "products",
        "pricing",
        "capacity",
        "schedule",
        "eligibility",
        "salesRules",
        "payment",
        "fulfillment",
        "integration"
       ]
      },
      "code": {
       "type": "string"
      },
      "message": {
       "type": "string"
      }
     }
    },
    "description": "Issues by Issue Severity (pack p.17)"
   },
   "aiInsights": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "AI Validation findings (pack p.17, e.g. B2B price above the public promotional price, allocations exceeding capacity). Advisory only: nothing is changed until a user acts."
   }
  }
 },
 "ChannelSalesRule": {
  "type": "object",
  "x-ticvai-persistence": "catalogue.channel_sales_rule",
  "description": "**When, how much and to whom a channel may sell** (29 September, data model DM3). Merges the channel sales schedule (ADM-261), sales limits and restrictions (ADM-265) and customer eligibility by channel (ADM-262): each is a rule on a channel, optionally for one product, with an effective window. `ruleKind` says which group of fields applies; the others are null. A product-level rule is overridden only where `overridesProductRule`.",
  "required": [
   "id",
   "scopePath",
   "salesChannelId",
   "ruleKind",
   "isActive"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "**The partition key** (ADR-0005). Operations write it at `venue` scope."
   },
   "salesChannelId": {
    "type": "string",
    "format": "uuid"
   },
   "productId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "ruleKind": {
    "type": "string",
    "enum": [
     "salesWindow",
     "salesLimit",
     "eligibility"
    ]
   },
   "name": {
    "type": "string",
    "maxLength": 200,
    "nullable": true
   },
   "ruleLevel": {
    "type": "string",
    "enum": [
     "platform",
     "product",
     "channel",
     "contractPartner"
    ],
    "default": "channel"
   },
   "overridesProductRule": {
    "type": "boolean",
    "default": false
   },
   "effectiveFrom": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "effectiveTo": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "isActive": {
    "type": "boolean",
    "default": true
   },
   "salesStartDate": {
    "type": "string",
    "format": "date",
    "nullable": true
   },
   "salesStartTime": {
    "type": "string",
    "format": "time",
    "nullable": true
   },
   "salesEndDate": {
    "type": "string",
    "format": "date",
    "nullable": true
   },
   "salesEndTime": {
    "type": "string",
    "format": "time",
    "nullable": true
   },
   "timeZone": {
    "type": "string",
    "maxLength": 64,
    "nullable": true
   },
   "daysOfWeek": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "mon",
      "tue",
      "wed",
      "thu",
      "fri",
      "sat",
      "sun"
     ]
    }
   },
   "hoursOfOperation": {
    "type": "object",
    "additionalProperties": true,
    "nullable": true,
    "description": "`[{opensAt, closesAt}]`."
   },
   "blackoutDates": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "ISO dates."
   },
   "eventRelativeWindow": {
    "type": "object",
    "additionalProperties": true,
    "nullable": true,
    "description": "`{anchor, opensMinutesBefore, closesMinutesBefore}`."
   },
   "minimumLeadDays": {
    "type": "integer",
    "nullable": true,
    "minimum": 0
   },
   "minimumQuantity": {
    "type": "integer",
    "nullable": true,
    "minimum": 0
   },
   "maximumQuantity": {
    "type": "integer",
    "nullable": true,
    "minimum": 1
   },
   "maximumPerTransaction": {
    "type": "integer",
    "nullable": true,
    "minimum": 1
   },
   "maximumPerCustomer": {
    "type": "integer",
    "nullable": true,
    "minimum": 1
   },
   "maximumPerDay": {
    "type": "integer",
    "nullable": true,
    "minimum": 1
   },
   "maximumPerEvent": {
    "type": "integer",
    "nullable": true,
    "minimum": 1
   },
   "maximumPerProduct": {
    "type": "integer",
    "nullable": true,
    "minimum": 1
   },
   "isReservationPermitted": {
    "type": "boolean",
    "nullable": true
   },
   "isHoldPermitted": {
    "type": "boolean",
    "nullable": true
   },
   "isPaymentLinkPermitted": {
    "type": "boolean",
    "nullable": true
   },
   "isPartialPaymentPermitted": {
    "type": "boolean",
    "nullable": true
   },
   "isSplitPaymentPermitted": {
    "type": "boolean",
    "nullable": true
   },
   "isDiscountPermitted": {
    "type": "boolean",
    "nullable": true
   },
   "isPromoCodePermitted": {
    "type": "boolean",
    "nullable": true
   },
   "isExchangePermitted": {
    "type": "boolean",
    "nullable": true
   },
   "isReschedulePermitted": {
    "type": "boolean",
    "nullable": true
   },
   "isUpgradePermitted": {
    "type": "boolean",
    "nullable": true
   },
   "restrictions": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "noRefunds",
      "noCashPayment",
      "noComplimentary",
      "noManualDiscount",
      "noSameDaySales",
      "noSeatChanges"
     ]
    }
   },
   "eligibilityDimension": {
    "type": "string",
    "enum": [
     "customerType",
     "membership",
     "loyaltyTier",
     "country",
     "residency",
     "age",
     "corporateAccount",
     "partner",
     "customerSegment",
     "promoEligibility",
     "authenticationStatus",
     "purchaseHistory",
     "salesTerritory",
     null
    ],
    "nullable": true
   },
   "eligibilityOperator": {
    "type": "string",
    "enum": [
     "equals",
     "notEquals",
     "in",
     "notIn",
     "greaterThanOrEqual",
     "lessThanOrEqual",
     "between",
     null
    ],
    "nullable": true
   },
   "eligibilityValues": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "eligibilityEffect": {
    "type": "string",
    "enum": [
     "allow",
     "deny",
     null
    ],
    "nullable": true
   },
   "isGuestAllowed": {
    "type": "boolean",
    "nullable": true
   },
   "isLoginRequired": {
    "type": "boolean",
    "nullable": true
   },
   "isMembershipRequired": {
    "type": "boolean",
    "nullable": true
   },
   "isCorporateAccountRequired": {
    "type": "boolean",
    "nullable": true
   },
   "isIdentityVerificationRequired": {
    "type": "boolean",
    "nullable": true
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
 "ChannelSalesRulesLimitsRestrictionsView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over catalogue state, assembled at read time from tables that already exist",
  "description": "**What Channel Sales Rules, Limits & Restrictions displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "minimumQuantity": {
    "type": "integer",
    "description": "Minimum Quantity per transaction",
    "minimum": 1,
    "nullable": true
   },
   "maximumQuantity": {
    "type": "integer",
    "description": "Maximum Quantity; empty for no limit",
    "minimum": 1,
    "nullable": true
   },
   "maximumPerTransaction": {
    "type": "integer",
    "description": "Maximum Per Transaction; empty for no limit",
    "minimum": 1,
    "nullable": true
   },
   "maximumPerCustomer": {
    "type": "integer",
    "description": "Maximum Per Customer; empty for no limit",
    "minimum": 1,
    "nullable": true
   },
   "maximumPerDay": {
    "type": "integer",
    "description": "Maximum Per Day; empty for no limit",
    "minimum": 1,
    "nullable": true
   },
   "maximumPerEvent": {
    "type": "integer",
    "description": "Maximum Per Event; empty for no limit",
    "minimum": 1,
    "nullable": true
   },
   "maximumPerProduct": {
    "type": "integer",
    "description": "Maximum Per Product; empty for no limit",
    "minimum": 1,
    "nullable": true
   },
   "reservationPermitted": {
    "type": "boolean",
    "description": "Reservation permitted"
   },
   "holdPermitted": {
    "type": "boolean",
    "description": "Hold permitted"
   },
   "paymentLinkPermitted": {
    "type": "boolean",
    "description": "Payment link permitted"
   },
   "partialPaymentPermitted": {
    "type": "boolean",
    "description": "Partial payment permitted"
   },
   "discountPermitted": {
    "type": "boolean",
    "description": "Discount permitted"
   },
   "promoCodePermitted": {
    "type": "boolean",
    "description": "Promo code permitted"
   },
   "exchangePermitted": {
    "type": "boolean",
    "description": "Exchange permitted"
   },
   "reschedulePermitted": {
    "type": "boolean",
    "description": "Reschedule permitted"
   },
   "ruleId": {
    "type": "string",
    "description": "Rule ID"
   },
   "channelId": {
    "type": "string",
    "description": "Channel: the configured channel's ID from the Sales Channel Command Center (ADM-258)"
   },
   "product": {
    "type": "string",
    "description": "Product ID; empty for every product on the channel",
    "nullable": true
   },
   "ruleLevel": {
    "type": "string",
    "enum": [
     "platform",
     "product",
     "channel",
     "contractPartner"
    ],
    "description": "Rule Priority level (pack p.14)"
   },
   "overridesProductRule": {
    "type": "boolean",
    "description": "Channel Overrides: this channel rule overrides a general product rule"
   },
   "splitPaymentPermitted": {
    "type": "boolean",
    "description": "Split payment permitted"
   },
   "upgradePermitted": {
    "type": "boolean",
    "description": "Upgrade permitted"
   },
   "restrictions": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "noRefunds",
      "noCashPayment",
      "noComplimentary",
      "noManualDiscount",
      "noSameDaySales",
      "noSeatChanges"
     ]
    },
    "description": "Channel Restrictions (pack p.14 examples as a closed list) (decided 29 September, readiness close-out)"
   },
   "effectiveFrom": {
    "type": "string",
    "format": "date",
    "description": "Effective From"
   },
   "effectiveTo": {
    "type": "string",
    "format": "date",
    "description": "Effective To; empty for open-ended",
    "nullable": true
   }
  }
 },
 "ChannelSalesScheduleAvailabilityWindowsSummary": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection; the headline tiles over the list, computed at read time for the filters in force",
  "description": "**The headline figures on Channel Sales Schedule & Availability Windows.** The pack's KPI cards, split out of the row (decided 29 September, readiness close-out): a count describes the list, not each item in it.",
  "properties": {
   "activeSellingPeriods": {
    "type": "integer",
    "description": "Active selling periods"
   },
   "scheduledOpenings": {
    "type": "integer",
    "description": "Scheduled openings"
   },
   "scheduledClosures": {
    "type": "integer",
    "description": "Scheduled closures"
   },
   "blackouts": {
    "type": "integer",
    "description": "Blackouts"
   },
   "conflicts": {
    "type": "integer",
    "description": "Conflicts"
   },
   "eventDates": {
    "type": "integer",
    "description": "Event dates"
   }
  }
 },
 "ChannelSalesScheduleAvailabilityWindowsView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over catalogue state, assembled at read time from tables that already exist",
  "description": "**What Channel Sales Schedule & Availability Windows displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "salesStartDate": {
    "type": "string",
    "format": "date",
    "description": "Sales Start Date",
    "nullable": true
   },
   "salesStartTime": {
    "type": "string",
    "description": "Sales Start Time, HH:MM local to timeZone",
    "pattern": "^([01][0-9]|2[0-3]):[0-5][0-9]$",
    "nullable": true
   },
   "salesEndDate": {
    "type": "string",
    "format": "date",
    "description": "Sales End Date",
    "nullable": true
   },
   "salesEndTime": {
    "type": "string",
    "description": "Sales End Time, HH:MM local to timeZone",
    "pattern": "^([01][0-9]|2[0-3]):[0-5][0-9]$",
    "nullable": true
   },
   "timeZone": {
    "type": "string",
    "description": "Time Zone: IANA name"
   },
   "daysOfWeek": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "mon",
      "tue",
      "wed",
      "thu",
      "fri",
      "sat",
      "sun"
     ]
    },
    "description": "Days of Week the channel sells; empty means every day"
   },
   "hoursOfOperation": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "opensAt": {
       "type": "string"
      },
      "closesAt": {
       "type": "string"
      }
     }
    },
    "description": "Hours of Operation: HH:MM ranges within each selling day"
   },
   "blackoutDates": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "date"
    },
    "description": "Blackout Dates"
   },
   "eventRelativeWindows": {
    "type": "object",
    "nullable": true,
    "description": "Event-relative windows (pack p.11: B2C opens 90 days before, OTA closes 4 hours before, kiosk opens 2 hours before admission; MoM: onsite closes 15 min before a timed show). Offsets in minutes before the anchor; negative means after",
    "properties": {
     "anchor": {
      "type": "string",
      "enum": [
       "eventStart",
       "admissionStart",
       "eventEnd"
      ]
     },
     "opensMinutesBefore": {
      "type": "integer",
      "nullable": true
     },
     "closesMinutesBefore": {
      "type": "integer",
      "nullable": true
     }
    }
   },
   "channelId": {
    "type": "string",
    "description": "Channel: the configured channel's ID from the Sales Channel Command Center (ADM-258)"
   },
   "product": {
    "type": "string",
    "description": "Product ID the window applies to; empty for every product on the channel",
    "nullable": true
   },
   "minimumLeadDays": {
    "type": "integer",
    "description": "Minimum days between purchase and visit: 0 allows same-day, 1 is the MoM's next-day minimum for online sales (MoM 31 Aug §4.11)",
    "minimum": 0,
    "default": 0
   },
   "aiInsights": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Unusual schedule configurations AI detects (pack p.12, e.g. OTA closing after admission has ended). Advisory only: nothing is changed until a user acts."
   }
  }
 },
 "CustomerEligibilityRulesByChannelView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over catalogue state, assembled at read time from tables that already exist",
  "description": "**What Customer & Eligibility Rules by Channel displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "guestAllowed": {
    "type": "boolean",
    "description": "Guest allowed"
   },
   "loginRequired": {
    "type": "boolean",
    "description": "Login required"
   },
   "membershipRequired": {
    "type": "boolean",
    "description": "Membership required"
   },
   "corporateAccountRequired": {
    "type": "boolean",
    "description": "Corporate account required"
   },
   "identityVerificationRequired": {
    "type": "boolean",
    "description": "Identity verification required"
   },
   "ruleId": {
    "type": "string",
    "description": "Rule ID"
   },
   "ruleName": {
    "type": "string",
    "description": "Rule name, e.g. UAE Resident Offer"
   },
   "channelId": {
    "type": "string",
    "description": "Channel: the configured channel's ID from the Sales Channel Command Center (ADM-258)"
   },
   "product": {
    "type": "string",
    "description": "Product ID; empty for every product on the channel",
    "nullable": true
   },
   "dimension": {
    "type": "string",
    "enum": [
     "customerType",
     "membership",
     "loyaltyTier",
     "country",
     "residency",
     "age",
     "corporateAccount",
     "partner",
     "customerSegment",
     "promoEligibility",
     "authenticationStatus",
     "purchaseHistory",
     "salesTerritory"
    ],
    "description": "Eligibility Dimension (pack p.12)"
   },
   "operator": {
    "type": "string",
    "enum": [
     "equals",
     "notEquals",
     "in",
     "notIn",
     "greaterThanOrEqual",
     "lessThanOrEqual",
     "between"
    ],
    "description": "How values are compared (decided 29 September, readiness close-out)"
   },
   "values": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Values the dimension is compared with (e.g. residency = AE, customer account type = approvedTravelAgent)"
   },
   "effect": {
    "type": "string",
    "enum": [
     "allow",
     "deny"
    ],
    "description": "Whether a match allows or denies purchase on the channel"
   },
   "aiInsights": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Contradictory channel/customer rules AI detects (pack p.13). Advisory only: nothing is changed until a user acts."
   }
  }
 },
 "InventoryCapacityChannelAllocationView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over catalogue state, assembled at read time from tables that already exist",
  "description": "**What Inventory, Capacity & Channel Allocation displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "productEvent": {
    "type": "string",
    "description": "Product/Event: the product or event ID the pool belongs to"
   },
   "capacityPool": {
    "type": "string",
    "description": "Capacity Pool ID"
   },
   "channel": {
    "type": "string",
    "description": "Channel: the configured channel's ID from the Sales Channel Command Center (ADM-258)"
   },
   "allocation": {
    "type": "number",
    "description": "Allocation: units for dedicated, percent of the pool for percentage; empty for sharedPool",
    "minimum": 0,
    "nullable": true
   },
   "minimum": {
    "type": "integer",
    "description": "Minimum units the channel keeps (not released below this)",
    "minimum": 0,
    "nullable": true
   },
   "maximum": {
    "type": "integer",
    "description": "Maximum units the channel may reach, including dynamic growth",
    "minimum": 0,
    "nullable": true
   },
   "replenishmentRule": {
    "type": "object",
    "nullable": true,
    "description": "Replenishment Rule: automatic migration from another channel (MoM 31 Aug §4.11, e.g. when B2C sells out pull 20% from B2B)",
    "properties": {
     "sourceChannelId": {
      "type": "string"
     },
     "trigger": {
      "type": "string",
      "enum": [
       "soldOut",
       "belowThreshold"
      ]
     },
     "thresholdUnits": {
      "type": "integer",
      "nullable": true
     },
     "sharePercent": {
      "type": "number",
      "nullable": true
     },
     "units": {
      "type": "integer",
      "nullable": true
     }
    }
   },
   "oversellAllowance": {
    "type": "integer",
    "description": "Oversell allowance in units; 0 means no oversell",
    "minimum": 0,
    "default": 0
   },
   "waitlistBehavior": {
    "type": "string",
    "enum": [
     "none",
     "joinWaitlist",
     "notifyOnRelease"
    ],
    "description": "Waitlist behavior where applicable (decided 29 September, readiness close-out)"
   },
   "allocated": {
    "type": "integer",
    "description": "Allocated"
   },
   "sold": {
    "type": "integer",
    "description": "Sold"
   },
   "held": {
    "type": "integer",
    "description": "Held"
   },
   "remaining": {
    "type": "integer",
    "description": "Remaining"
   },
   "utilization": {
    "type": "number",
    "description": "Utilization %: sold plus held over allocated, 0-100",
    "minimum": 0,
    "maximum": 100
   },
   "released": {
    "type": "integer",
    "description": "Released: units given back to the shared pool by a release rule"
   },
   "returned": {
    "type": "integer",
    "description": "Returned: units returned manually"
   },
   "allocationType": {
    "type": "string",
    "enum": [
     "sharedPool",
     "dedicated",
     "percentage",
     "dynamic"
    ],
    "description": "Allocation Type (pack p.10)"
   },
   "releaseThreshold": {
    "type": "integer",
    "description": "Release Threshold: unsold units above which the excess returns to the shared pool (pack p.10, e.g. 300)",
    "nullable": true
   },
   "releaseHoursBeforeEvent": {
    "type": "integer",
    "description": "Release point relative to the event, in hours before start (pack p.10, e.g. 48)",
    "nullable": true
   },
   "releaseDate": {
    "type": "string",
    "format": "date-time",
    "description": "Release Date: fixed release point, used instead of the event-relative one",
    "nullable": true
   },
   "aiInsights": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "AI reallocation suggestions (pack p.11). Advisory only: nothing is changed until a user acts."
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
 "ProductCatalogueAssignmentInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures",
  "description": "**What Product & Catalogue Assignment submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "channelId": {
    "type": "string",
    "description": "Channel ID"
   },
   "assignmentMethod": {
    "type": "string",
    "enum": [
     "individualProduct",
     "productFamily",
     "productCategory",
     "event",
     "attraction",
     "venueCatalogue",
     "productCollection",
     "entireApprovedCatalogue"
    ],
    "description": "Assignment Method (pack p.7)"
   },
   "targetIds": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "IDs of the products, families, categories, events, attractions, venue catalogues or collections assigned; empty for entireApprovedCatalogue"
   },
   "excludedProductIds": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Channel-specific overrides: products excluded from what is inherited (pack p.8, e.g. B2C excludes corporate tickets)"
   },
   "enabled": {
    "type": "boolean",
    "description": "Enable or disable the assignment on the channel"
   },
   "effectiveFrom": {
    "type": "string",
    "format": "date",
    "description": "Effective From"
   },
   "effectiveTo": {
    "type": "string",
    "format": "date",
    "description": "Effective To; empty for open-ended",
    "nullable": true
   }
  }
 },
 "ProductCatalogueAssignmentView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over catalogue state, assembled at read time from tables that already exist",
  "description": "**What Product & Catalogue Assignment displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "product": {
    "type": "string",
    "description": "Product ID"
   },
   "productType": {
    "$ref": "#/components/schemas/ProductKind",
    "description": "Product Type"
   },
   "venue": {
    "type": "string",
    "description": "Venue ID"
   },
   "status": {
    "$ref": "#/components/schemas/ProductLifecycleState",
    "description": "Status: the product's own lifecycle state in Product Catalogue"
   },
   "validity": {
    "type": "string",
    "description": "Validity: the product's validity period as set in Product Catalogue, shown for reference"
   },
   "channelStatus": {
    "type": "string",
    "description": "Channel Status: enabled, disabled or scheduled on this channel (decided 29 September, readiness close-out)"
   },
   "pricingStatus": {
    "type": "string",
    "description": "Pricing Status: valid, missing or expired for this channel (from ADM-261) (decided 29 September, readiness close-out)"
   },
   "capacityStatus": {
    "type": "string",
    "description": "Capacity Status: allocated, sharedPool or none for this channel (from ADM-262) (decided 29 September, readiness close-out)"
   },
   "effectiveFrom": {
    "type": "string",
    "format": "date",
    "description": "Effective From"
   },
   "effectiveTo": {
    "type": "string",
    "format": "date",
    "description": "Effective To; empty for open-ended",
    "nullable": true
   },
   "channelId": {
    "type": "string",
    "description": "Channel: the configured channel's ID from the Sales Channel Command Center (ADM-258)"
   },
   "assignmentMethod": {
    "type": "string",
    "enum": [
     "individualProduct",
     "productFamily",
     "productCategory",
     "event",
     "attraction",
     "venueCatalogue",
     "productCollection",
     "entireApprovedCatalogue"
    ],
    "description": "Assignment Method the product came in by (pack p.7)"
   },
   "inheritedFrom": {
    "type": "string",
    "enum": [
     "globalChannelCatalogue",
     "venueCatalogue",
     "channelOverride"
    ],
    "description": "Inheritance level the assignment comes from (pack p.7-8)"
   },
   "validationIssues": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "code": {
       "type": "string",
       "enum": [
        "draftProduct",
        "retiredProduct",
        "missingPricing",
        "missingEntitlement",
        "outsideValidity",
        "unavailableForChannel"
       ]
      },
      "message": {
       "type": "string"
      }
     }
    },
    "description": "Validation (pack p.8): why this product should not be published on the channel"
   }
  }
 },
 "ProductKind": {
  "type": "string",
  "description": "**`openDated` added 24 August** from the client's *Create Ticket Flow* board, which names six main ticket types and this was the one with no kind: **valid on any date within an eligible range, rather than for a named performance or a fixed date.**\nThe mechanism already existed — `access.entitlement` carries `valid_from`, `valid_to`, `entries_allowed` and `frozen_days`, which is exactly an open-dated pass. **What was missing was the product saying it is one**, so a catalogue could not offer it and a report could not count it.\n**`datedAdmission` is a different thing and the two were being conflated**: dated is *this Tuesday*, open-dated is *any Tuesday between March and June*. A guest buying the second and being sold the first has bought the wrong ticket.\n**Transport uses two existing kinds, not a new one** (decided 29 September, rev 3 REV3-21). A one-way trip is `timedAdmission`: `transport.createTransportRoute` creates the route's product with one variant per passenger type, and each departure is a performance. A multi-trip or unlimited pass is `openDated`: `transport.createTransportPassType` creates it, with `EntitlementTemplate.entriesAllowed` = the pass's trips (null for unlimited), the validity = `validityDays`, and `EntitlementTemplate.transportRestriction` naming the station pair the pass was bought for, so `access` refuses it on another journey. The sale path is unchanged: both are cart lines, priced by `transport.quoteTransportFare` (orders `TransportLineAttributes`).\n",
  "enum": [
   "admission",
   "timedAdmission",
   "datedAdmission",
   "openDated",
   "seated",
   "membership",
   "bundle",
   "fnb",
   "retail",
   "rental",
   "addOn",
   "giftCard"
  ]
 },
 "ProductLifecycleState": {
  "type": "string",
  "enum": [
   "draft",
   "inReview",
   "approved",
   "live",
   "withdrawn",
   "archived"
  ]
 },
 "SalesChannelCommandCenterSummary": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection; the headline tiles over the list, computed at read time for the filters in force",
  "description": "**The headline figures on Sales Channel Command Center.** The pack's KPI cards, split out of the row (decided 29 September, readiness close-out): a count describes the list, not each item in it.",
  "properties": {
   "totalChannels": {
    "type": "integer",
    "description": "Total Channels"
   },
   "activeChannels": {
    "type": "integer",
    "description": "Active Channels"
   },
   "inactiveChannels": {
    "type": "integer",
    "description": "Inactive Channels"
   },
   "channelsInDraft": {
    "type": "integer",
    "description": "Channels in Draft"
   },
   "channelsWithErrors": {
    "type": "integer",
    "description": "Channels With Errors"
   },
   "productsDistributed": {
    "type": "integer",
    "description": "Products Distributed: distinct products assigned to at least one active channel"
   },
   "channelsWithCapacityAlerts": {
    "type": "integer",
    "description": "Channels With Capacity Alerts"
   },
   "channelsWithPricingIssues": {
    "type": "integer",
    "description": "Channels With Pricing Issues"
   },
   "scheduledActivations": {
    "type": "integer",
    "description": "Scheduled Activations"
   },
   "scheduledDeactivations": {
    "type": "integer",
    "description": "Scheduled Deactivations"
   }
  }
 },
 "SalesChannelCommandCenterView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over catalogue state, assembled at read time from tables that already exist",
  "description": "**What Sales Channel Command Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "channelId": {
    "type": "string",
    "description": "Channel ID"
   },
   "channelName": {
    "type": "string",
    "description": "Channel Name"
   },
   "channelType": {
    "type": "string",
    "enum": [
     "b2cWeb",
     "b2cMobileApp",
     "pos",
     "mobilePos",
     "flyingPos",
     "kiosk",
     "callCentre",
     "b2bPortal",
     "reseller",
     "ota",
     "api",
     "partnerPortal",
     "marketplace",
     "thirdPartyChannel",
     "customChannel"
    ],
    "description": "Channel Type (pack p.3-4 Channel Types). The type decides which configuration applies (p.6); each type reports under one SalesChannel value (see salesChannel)"
   },
   "brand": {
    "type": "string",
    "description": "Brand"
   },
   "venueScope": {
    "type": "string",
    "description": "Venue/Scope: the channel's operational scope level and the name of the scoped item (e.g. a venue name, or Global)"
   },
   "products": {
    "type": "integer",
    "description": "Products: number of products assigned to the channel"
   },
   "currency": {
    "type": "string",
    "description": "Currency: ISO 4217 code",
    "pattern": "^[A-Z]{3}$"
   },
   "status": {
    "type": "string",
    "description": "Status: draft, configuration, validation, approved, scheduled, active, suspended, disabled or archived (the pack's suggested lifecycle, p.5)"
   },
   "publicationStatus": {
    "type": "string",
    "description": "Publication Status: unpublished, pendingApproval, scheduled or published (decided 29 September, readiness close-out)"
   },
   "integrationStatus": {
    "type": "string",
    "description": "Integration Status: notRequired, notConfigured, connected, degraded or offline (decided 29 September, readiness close-out)"
   },
   "lastUpdated": {
    "type": "string",
    "format": "date-time",
    "description": "Last Updated"
   },
   "owner": {
    "type": "string",
    "description": "Owner: the channel's commercial owner (user ID)"
   },
   "salesChannel": {
    "$ref": "../shared/common.yaml#/components/schemas/SalesChannel",
    "description": "The shared reporting dimension this channel's sales are attributed to (b2cWeb -> guestWeb, b2cMobileApp -> guestApp, the POS types -> pos, callCentre, b2bPortal -> b2b, ota and marketplace -> ota, api, reseller/partnerPortal/thirdPartyChannel -> partner; a custom channel picks one) (decided 29 September, readiness close-out)"
   },
   "aiInsights": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Configuration problems AI flags on this channel (pack p.5, e.g. products assigned without a valid price profile for the channel). Advisory only: nothing is changed until a user acts."
   }
  }
 }
}
```
