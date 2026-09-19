# WS57 — Sales Channel Management board 1

**10 screens · 10 operations · 15 schemas · 2 permissions**

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
- **0 of these operations work offline**
  
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `ADM-258` | Sales Channel Command Center | commandCentre | 1 | 0 | — |
| `ADM-259` | Channel Creation & Profile Configuration | configEditor | 1 | 0 | — |
| `ADM-260` | Product & Catalogue Assignment | listDetail | 1 | 2 | — |
| `ADM-261` | Channel Pricing & Commercial Profile Assignment | listDetail | 1 | 0 | — |
| `ADM-262` | Inventory, Capacity & Channel Allocation | listDetail | 1 | 0 | — |
| `ADM-263` | Channel Sales Schedule & Availability Windows | listDetail | 1 | 0 | — |
| `ADM-264` | Customer & Eligibility Rules by Channel | configEditor | 1 | 0 | — |
| `ADM-265` | Channel Sales Rules, Limits & Restrictions | configEditor | 1 | 0 | — |
| `ADM-266` | Channel Fees, Payment & Fulfillment Configuration | configEditor | 1 | 0 | — |
| `ADM-267` | Channel Publication, Readiness & AI Validation | configEditor | 1 | 0 | — |

## Thin screens in this batch

**ADM-261, ADM-262, ADM-263 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

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
     "carries": [
      "tenantId"
     ],
     "provenance": "derived — ADM-002 declares entryState.params tenantId, so an edge into it must carry them"
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
     "to": "ADM-263",
     "trigger": "Works in Channel Sales Schedule & Availability Windows",
     "provenance": "flow F166 step 9→10",
     "operation": "listSaleChannel"
    },
    {
     "to": "ADM-264",
     "trigger": "Works in Customer & Eligibility Rules by Channel",
     "provenance": "flow F166 step 11→12",
     "operation": "listSaleChannel"
    },
    {
     "to": "ADM-265",
     "trigger": "Works in Channel Sales Rules, Limits & Restrictions",
     "provenance": "flow F166 step 13→14",
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
    }
   ]
  },
  "density": "compact",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen both a metric directory (§Display) and a per-row directory (§Each record should display) — counts over a population, then the population",
  "purpose": "Provide administrators with one centralized view of every TICVAI sales channel and its current operational/configuration status.",
  "purposeNote": "An administrator can see every configured sales channel, its status, scope, product coverage and configuration issues from one central workspace.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 3 actions on this screen and the screen declares 1 operation.** Unserved: Partner Portal, Third-Party Channel, Custom Channel. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
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
       "bindsTo": "SalesChannelCommandCenterView.totalChannels"
      },
      {
       "kind": "metricTile",
       "label": "Active Channels",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 3 §Display",
       "bindsTo": "SalesChannelCommandCenterView.activeChannels"
      },
      {
       "kind": "metricTile",
       "label": "Inactive Channels",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 3 §Display",
       "bindsTo": "SalesChannelCommandCenterView.inactiveChannels"
      },
      {
       "kind": "metricTile",
       "label": "Channels in Draft",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 3 §Display",
       "bindsTo": "SalesChannelCommandCenterView.channelsInDraft"
      },
      {
       "kind": "metricTile",
       "label": "Channels With Errors",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 3 §Display",
       "bindsTo": "SalesChannelCommandCenterView.channelsWithErrors"
      },
      {
       "kind": "metricTile",
       "label": "Products Distributed",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 3 §Display",
       "bindsTo": "SalesChannelCommandCenterView.productsDistributed"
      },
      {
       "kind": "metricTile",
       "label": "Channels With Capacity Alerts",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 3 §Display",
       "bindsTo": "SalesChannelCommandCenterView.channelsWithCapacityAlerts"
      },
      {
       "kind": "metricTile",
       "label": "Channels With Pricing Issues",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 3 §Display",
       "bindsTo": "SalesChannelCommandCenterView.channelsWithPricingIssues"
      },
      {
       "kind": "metricTile",
       "label": "Scheduled Activations",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 3 §Display",
       "bindsTo": "SalesChannelCommandCenterView.scheduledActivations"
      },
      {
       "kind": "metricTile",
       "label": "Scheduled Deactivations",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 3 §Display",
       "bindsTo": "SalesChannelCommandCenterView.scheduledDeactivations"
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
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-258"
  },
  "apisNote": "Regenerated 9 September 2026 from Sales_Channel_Management_Reference.pdf page 3. 22 of 22 labels bound to a contract property; 37 of 57 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population",
  "purpose": "Create and define a sales channel before products and commercial rules are assigned.",
  "purposeNote": "An authorized administrator can create a new channel with a unique identity, operational scope and ownership without technical development.",
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
    "trigger": "onAction",
    "invalidates": [
     "createChannelProfile"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-259"
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
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Control exactly which products are available through each sales channel.",
  "purposeNote": "Administrators can determine precisely which approved products each channel is authorized to distribute without duplicating the product configuration itself.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 4 actions on this screen and the screen declares 1 operation.** Unserved: Assign Products, Remove Products, Disable, Import Assignment. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
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
    "trigger": "onAction",
    "invalidates": [
     "setProductCatalogue"
    ]
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
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-260"
  },
  "apisNote": "Regenerated 9 September 2026 from Sales_Channel_Management_Reference.pdf page 7. 10 of 10 labels bound to a contract property; 14 of 39 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
    "trigger": "onAction",
    "invalidates": [
     "setChannelPricingCommercial"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-261"
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
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Control how much product inventory or event capacity is available to each sales channel.",
  "purposeNote": "exceed the underlying approved inventory/capacity.",
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
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-262"
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
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Control when each channel is permitted to sell.",
  "purposeNote": "Every channel can have independently governed selling windows without modifying the underlying product validity.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every channel sales schedule",
       "columns": [
        "ChannelSalesScheduleAvailabilityWindowsView.activeSellingPeriods",
        "ChannelSalesScheduleAvailabilityWindowsView.scheduledOpenings",
        "ChannelSalesScheduleAvailabilityWindowsView.scheduledClosures",
        "ChannelSalesScheduleAvailabilityWindowsView.blackouts",
        "ChannelSalesScheduleAvailabilityWindowsView.conflicts",
        "ChannelSalesScheduleAvailabilityWindowsView.eventDates"
       ],
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
       "columns": [
        "ChannelSalesScheduleAvailabilityWindowsView.activeSellingPeriods",
        "ChannelSalesScheduleAvailabilityWindowsView.scheduledOpenings",
        "ChannelSalesScheduleAvailabilityWindowsView.scheduledClosures",
        "ChannelSalesScheduleAvailabilityWindowsView.blackouts",
        "ChannelSalesScheduleAvailabilityWindowsView.conflicts",
        "ChannelSalesScheduleAvailabilityWindowsView.eventDates"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Channel-Specific Scheduling”, “Automated Actions”.",
       "provenance": "pack Sales_Channel_Management_Reference.pdf, page 11 §Display"
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
   }
  ],
  "entryState": {
   "preloaded": [
    "ChannelSalesScheduleAvailabilityWindowsView.activeSellingPeriods",
    "ChannelSalesScheduleAvailabilityWindowsView.scheduledOpenings",
    "ChannelSalesScheduleAvailabilityWindowsView.scheduledClosures",
    "ChannelSalesScheduleAvailabilityWindowsView.blackouts",
    "ChannelSalesScheduleAvailabilityWindowsView.conflicts",
    "ChannelSalesScheduleAvailabilityWindowsView.eventDates"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-263"
  },
  "apisNote": "Regenerated 9 September 2026 from Sales_Channel_Management_Reference.pdf page 11. 6 of 6 labels bound to a contract property; 15 of 32 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population",
  "purpose": "Determine who is allowed to purchase through a particular channel.",
  "purposeNote": "purchased.",
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
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-264"
  },
  "apisNote": "Regenerated 9 September 2026 from Sales_Channel_Management_Reference.pdf page 12. 0 of 0 labels bound to a contract property; 5 of 29 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population",
  "purpose": "Configure operational restrictions that apply specifically to a sales channel.",
  "purposeNote": "Administrators can enforce channel-specific operational and transaction restrictions without changing the master product definition.",
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
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-265"
  },
  "apisNote": "Regenerated 9 September 2026 from Sales_Channel_Management_Reference.pdf page 13. 0 of 0 labels bound to a contract property; 17 of 33 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population",
  "purpose": "Define the commercial and fulfillment behavior associated with each channel.",
  "purposeNote": "Each channel exposes only approved payment, fee and fulfillment methods supported by its operational configuration.",
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
    "trigger": "onAction",
    "invalidates": [
     "setChannelFeePayment"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-266"
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
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configuration works) and no display directory — it is settings, not a population",
  "purpose": "Perform final validation before a sales channel or channel/product configuration becomes commercially active. Board 2 manages the live operational layer of TICVAI's sales-channel ecosystem after channels have been configured and activated in Board 1.",
  "purposeNote": "No sales channel becomes operational until its required product, pricing, capacity, schedule, payment, fulfillment and governance dependencies have passed configured readiness validation. Board 1 — Final Screen Register",
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
    "trigger": "onAction",
    "invalidates": [
     "publishChannelReadinessValidation"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-267"
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
  "parameters": [],
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
  "parameters": [],
  "requestBody": null,
  "responds": "ChannelSalesRulesLimitsRestrictionsView"
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
  "parameters": [],
  "requestBody": null,
  "responds": "ChannelSalesScheduleAvailabilityWindowsView"
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
  "parameters": [],
  "requestBody": null,
  "responds": "CustomerEligibilityRulesByChannelView"
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
  "parameters": [],
  "requestBody": null,
  "responds": "InventoryCapacityChannelAllocationView"
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
  "parameters": [],
  "requestBody": null,
  "responds": "SalesChannelCommandCenterView"
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
  "parameters": [],
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
  "parameters": [],
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
  "parameters": [],
  "requestBody": "ChannelPricingCommercialProfileAssignmentInput",
  "responds": "ChannelPricingCommercialProfileAssignmentView"
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
  "parameters": [],
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
    "description": "Channel Name"
   },
   "channelCode": {
    "type": "string",
    "description": "Channel Code"
   },
   "channelType": {
    "type": "string",
    "description": "Channel Type"
   },
   "internalDescription": {
    "type": "string",
    "description": "Internal Description"
   },
   "customerFacingName": {
    "type": "string",
    "description": "Customer-Facing Name"
   },
   "tenant": {
    "type": "string",
    "description": "Tenant"
   },
   "brand": {
    "type": "string",
    "description": "Brand"
   },
   "businessUnit": {
    "type": "string",
    "description": "Business Unit"
   },
   "country": {
    "type": "string",
    "description": "Country"
   },
   "market": {
    "type": "string",
    "description": "Market"
   },
   "currency": {
    "type": "string",
    "description": "Currency"
   },
   "timeZone": {
    "type": "string",
    "format": "date-time",
    "description": "Time Zone"
   },
   "owner": {
    "type": "string",
    "description": "Owner"
   },
   "responsibleDepartment": {
    "type": "string",
    "description": "Responsible Department"
   },
   "mayRequire": {
    "type": "string",
    "description": "may require"
   },
   "venue": {
    "type": "string",
    "description": "Venue"
   },
   "workstationGroups": {
    "type": "string",
    "description": "Workstation groups"
   },
   "cashierAccess": {
    "type": "string",
    "description": "Cashier access"
   },
   "webstore": {
    "type": "string",
    "description": "Webstore"
   },
   "domainBrand": {
    "type": "string",
    "description": "Domain/brand"
   },
   "digitalCustomerJourney": {
    "type": "string",
    "description": "Digital customer journey"
   },
   "partner": {
    "type": "string",
    "description": "Partner"
   },
   "apiConnection": {
    "type": "string",
    "description": "API connection"
   },
   "allocationRules": {
    "type": "string",
    "description": "Allocation rules"
   },
   "global": {
    "type": "string",
    "description": "Global"
   },
   "region": {
    "type": "string",
    "description": "Region"
   },
   "attraction": {
    "type": "string",
    "description": "Attraction"
   },
   "event": {
    "type": "string",
    "description": "Event"
   },
   "location": {
    "type": "string",
    "description": "Location"
   },
   "selectedBusinessUnit": {
    "type": "string",
    "description": "Selected business unit"
   },
   "commercialOwner": {
    "type": "string",
    "description": "Commercial Owner"
   },
   "operationalOwner": {
    "type": "string",
    "description": "Operational Owner"
   },
   "technicalOwner": {
    "type": "string",
    "description": "Technical Owner"
   },
   "financeOwner": {
    "type": "string",
    "description": "Finance Owner"
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
    "description": "Channel Name"
   },
   "channelCode": {
    "type": "string",
    "description": "Channel Code"
   },
   "channelType": {
    "type": "string",
    "description": "Channel Type"
   },
   "internalDescription": {
    "type": "string",
    "description": "Internal Description"
   },
   "customerFacingName": {
    "type": "string",
    "description": "Customer-Facing Name"
   },
   "tenant": {
    "type": "string",
    "description": "Tenant"
   },
   "brand": {
    "type": "string",
    "description": "Brand"
   },
   "businessUnit": {
    "type": "string",
    "description": "Business Unit"
   },
   "country": {
    "type": "string",
    "description": "Country"
   },
   "market": {
    "type": "string",
    "description": "Market"
   },
   "currency": {
    "type": "string",
    "description": "Currency"
   },
   "timeZone": {
    "type": "string",
    "format": "date-time",
    "description": "Time Zone"
   },
   "owner": {
    "type": "string",
    "description": "Owner"
   },
   "responsibleDepartment": {
    "type": "string",
    "description": "Responsible Department"
   },
   "mayRequire": {
    "type": "string",
    "description": "may require"
   },
   "venue": {
    "type": "string",
    "description": "Venue"
   },
   "workstationGroups": {
    "type": "string",
    "description": "Workstation groups"
   },
   "cashierAccess": {
    "type": "string",
    "description": "Cashier access"
   },
   "webstore": {
    "type": "string",
    "description": "Webstore"
   },
   "domainBrand": {
    "type": "string",
    "description": "Domain/brand"
   },
   "digitalCustomerJourney": {
    "type": "string",
    "description": "Digital customer journey"
   },
   "partner": {
    "type": "string",
    "description": "Partner"
   },
   "apiConnection": {
    "type": "string",
    "description": "API connection"
   },
   "allocationRules": {
    "type": "string",
    "description": "Allocation rules"
   },
   "global": {
    "type": "string",
    "description": "Global"
   },
   "region": {
    "type": "string",
    "description": "Region"
   },
   "attraction": {
    "type": "string",
    "description": "Attraction"
   },
   "event": {
    "type": "string",
    "description": "Event"
   },
   "location": {
    "type": "string",
    "description": "Location"
   },
   "selectedBusinessUnit": {
    "type": "string",
    "description": "Selected business unit"
   },
   "commercialOwner": {
    "type": "string",
    "description": "Commercial Owner"
   },
   "operationalOwner": {
    "type": "string",
    "description": "Operational Owner"
   },
   "technicalOwner": {
    "type": "string",
    "description": "Technical Owner"
   },
   "financeOwner": {
    "type": "string",
    "description": "Finance Owner"
   }
  }
 },
 "ChannelFeesPaymentFulfillmentConfigurationInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures",
  "description": "**What Channel Fees, Payment & Fulfillment Configuration submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "bookingFee": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Booking Fee"
   },
   "transactionFee": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Transaction Fee"
   },
   "channelFee": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Channel Fee"
   },
   "serviceFee": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Service Fee"
   },
   "deliveryFee": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Delivery Fee"
   },
   "paymentFee": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Payment Fee"
   },
   "creditDebitCard": {
    "type": "string",
    "description": "Credit/Debit Card"
   },
   "cash": {
    "type": "string",
    "description": "Cash"
   },
   "digitalWallet": {
    "type": "string",
    "description": "Digital Wallet"
   },
   "paymentLink": {
    "type": "string",
    "description": "Payment Link"
   },
   "accountCredit": {
    "type": "string",
    "description": "Account Credit"
   },
   "b2bCredit": {
    "type": "string",
    "description": "B2B Credit"
   },
   "otherConfiguredMethods": {
    "type": "string",
    "description": "Other configured methods"
   },
   "digitalTicket": {
    "type": "string",
    "description": "Digital Ticket"
   },
   "email": {
    "type": "string",
    "description": "Email"
   },
   "mobileApp": {
    "type": "string",
    "description": "Mobile App"
   },
   "appleGoogleWallet": {
    "type": "string",
    "description": "Apple/Google Wallet"
   },
   "posPrint": {
    "type": "string",
    "description": "POS Print"
   },
   "kioskPrint": {
    "type": "string",
    "description": "Kiosk Print"
   },
   "rfid": {
    "type": "string",
    "description": "RFID"
   },
   "nfc": {
    "type": "string",
    "description": "NFC"
   },
   "wristband": {
    "type": "string",
    "description": "Wristband"
   },
   "collection": {
    "type": "string",
    "description": "Collection"
   },
   "card": {
    "type": "string",
    "description": "Card"
   },
   "wallet": {
    "type": "string",
    "description": "Wallet"
   },
   "mobileWallet": {
    "type": "string",
    "description": "Mobile Wallet"
   },
   "printedTicket": {
    "type": "string",
    "description": "Printed Ticket"
   },
   "voucher": {
    "type": "string",
    "description": "Voucher"
   },
   "apiTicketDelivery": {
    "type": "string",
    "description": "API Ticket Delivery"
   }
  }
 },
 "ChannelFeesPaymentFulfillmentConfigurationView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over catalogue state, assembled at read time from tables that already exist",
  "description": "**What Channel Fees, Payment & Fulfillment Configuration displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "bookingFee": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Booking Fee"
   },
   "transactionFee": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Transaction Fee"
   },
   "channelFee": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Channel Fee"
   },
   "serviceFee": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Service Fee"
   },
   "deliveryFee": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Delivery Fee"
   },
   "paymentFee": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Payment Fee"
   },
   "creditDebitCard": {
    "type": "string",
    "description": "Credit/Debit Card"
   },
   "cash": {
    "type": "string",
    "description": "Cash"
   },
   "digitalWallet": {
    "type": "string",
    "description": "Digital Wallet"
   },
   "paymentLink": {
    "type": "string",
    "description": "Payment Link"
   },
   "accountCredit": {
    "type": "string",
    "description": "Account Credit"
   },
   "b2bCredit": {
    "type": "string",
    "description": "B2B Credit"
   },
   "otherConfiguredMethods": {
    "type": "string",
    "description": "Other configured methods"
   },
   "digitalTicket": {
    "type": "string",
    "description": "Digital Ticket"
   },
   "email": {
    "type": "string",
    "description": "Email"
   },
   "mobileApp": {
    "type": "string",
    "description": "Mobile App"
   },
   "appleGoogleWallet": {
    "type": "string",
    "description": "Apple/Google Wallet"
   },
   "posPrint": {
    "type": "string",
    "description": "POS Print"
   },
   "kioskPrint": {
    "type": "string",
    "description": "Kiosk Print"
   },
   "rfid": {
    "type": "string",
    "description": "RFID"
   },
   "nfc": {
    "type": "string",
    "description": "NFC"
   },
   "wristband": {
    "type": "string",
    "description": "Wristband"
   },
   "collection": {
    "type": "string",
    "description": "Collection"
   },
   "card": {
    "type": "string",
    "description": "Card"
   },
   "wallet": {
    "type": "string",
    "description": "Wallet"
   },
   "mobileWallet": {
    "type": "string",
    "description": "Mobile Wallet"
   },
   "printedTicket": {
    "type": "string",
    "description": "Printed Ticket"
   },
   "voucher": {
    "type": "string",
    "description": "Voucher"
   },
   "apiTicketDelivery": {
    "type": "string",
    "description": "API Ticket Delivery"
   }
  }
 },
 "ChannelPricingCommercialProfileAssignmentInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table covers these fields** — the closest is catalogue.price_list at 6%, so this is not an update to anything the package stores today and no new table has been decided",
  "description": "**What Channel Pricing & Commercial Profile Assignment submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.\n\n**The pack defines this as a record**, under *For each assignment* - one of only 13 drafted writes that does. That is the client writing a row rather than a screen, and it is where the table conversation should start.",
  "properties": {
   "standardPriceList": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Standard Price List"
   },
   "channelPriceList": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Channel Price List"
   },
   "b2bRate": {
    "type": "number",
    "description": "B2B Rate"
   },
   "resellerRate": {
    "type": "number",
    "description": "Reseller Rate"
   },
   "otaRate": {
    "type": "number",
    "description": "OTA Rate"
   },
   "posPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "POS Price"
   },
   "promotionalPriceProfile": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Promotional Price Profile"
   },
   "dynamicPricingProfile": {
    "type": "string",
    "description": "Dynamic Pricing Profile"
   },
   "priceProfile": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Price Profile"
   },
   "currency": {
    "type": "string",
    "description": "Currency"
   },
   "effectiveFrom": {
    "type": "string",
    "description": "Effective From"
   },
   "effectiveTo": {
    "type": "string",
    "description": "Effective To"
   },
   "venue": {
    "type": "string",
    "description": "Venue"
   },
   "event": {
    "type": "string",
    "description": "Event"
   },
   "product": {
    "type": "string",
    "description": "Product"
   },
   "customerSegment": {
    "type": "string",
    "description": "Customer Segment"
   },
   "priority": {
    "type": "string",
    "description": "Priority"
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
   "standardPriceList": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Standard Price List"
   },
   "channelPriceList": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Channel Price List"
   },
   "b2bRate": {
    "type": "number",
    "description": "B2B Rate"
   },
   "resellerRate": {
    "type": "number",
    "description": "Reseller Rate"
   },
   "otaRate": {
    "type": "number",
    "description": "OTA Rate"
   },
   "posPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "POS Price"
   },
   "promotionalPriceProfile": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Promotional Price Profile"
   },
   "dynamicPricingProfile": {
    "type": "string",
    "description": "Dynamic Pricing Profile"
   },
   "priceProfile": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Price Profile"
   },
   "currency": {
    "type": "string",
    "description": "Currency"
   },
   "effectiveFrom": {
    "type": "string",
    "description": "Effective From"
   },
   "effectiveTo": {
    "type": "string",
    "description": "Effective To"
   },
   "venue": {
    "type": "string",
    "description": "Venue"
   },
   "event": {
    "type": "string",
    "description": "Event"
   },
   "product": {
    "type": "string",
    "description": "Product"
   },
   "customerSegment": {
    "type": "string",
    "description": "Customer Segment"
   },
   "priority": {
    "type": "string",
    "description": "Priority"
   }
  }
 },
 "ChannelPublicationReadinessAiValidationInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures",
  "description": "**What Channel Publication, Readiness & AI Validation submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "complete": {
    "type": "string",
    "description": "Complete"
   },
   "assigned": {
    "type": "string",
    "description": "Assigned"
   },
   "valid": {
    "type": "string",
    "description": "Valid"
   },
   "available": {
    "type": "string",
    "description": "Available"
   },
   "configured": {
    "type": "string",
    "description": "Configured"
   },
   "readyWhereRequired": {
    "type": "boolean",
    "description": "Ready where required"
   },
   "critical": {
    "type": "string",
    "description": "Critical"
   },
   "high": {
    "type": "string",
    "description": "High"
   },
   "medium": {
    "type": "string",
    "description": "Medium"
   },
   "low": {
    "type": "string",
    "description": "Low"
   },
   "recommendation": {
    "type": "string",
    "description": "Recommendation"
   },
   "period": {
    "type": "string",
    "format": "date-time",
    "description": "period"
   },
   "preview": {
    "type": "string",
    "description": "Preview"
   },
   "returnForChanges": {
    "type": "string",
    "description": "Return for Changes"
   },
   "beforeActivation": {
    "type": "string",
    "description": "before activation"
   },
   "troubleshootGovernAndOptimizeThem": {
    "type": "string",
    "description": "troubleshoot, govern and optimize them?"
   },
   "managingAvailabilityAndSynchronization": {
    "type": "string",
    "description": "managing availability and synchronization"
   }
  }
 },
 "ChannelPublicationReadinessAiValidationView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over catalogue state, assembled at read time from tables that already exist",
  "description": "**What Channel Publication, Readiness & AI Validation displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "complete": {
    "type": "string",
    "description": "Complete"
   },
   "assigned": {
    "type": "string",
    "description": "Assigned"
   },
   "valid": {
    "type": "string",
    "description": "Valid"
   },
   "available": {
    "type": "string",
    "description": "Available"
   },
   "configured": {
    "type": "string",
    "description": "Configured"
   },
   "readyWhereRequired": {
    "type": "boolean",
    "description": "Ready where required"
   },
   "critical": {
    "type": "string",
    "description": "Critical"
   },
   "high": {
    "type": "string",
    "description": "High"
   },
   "medium": {
    "type": "string",
    "description": "Medium"
   },
   "low": {
    "type": "string",
    "description": "Low"
   },
   "recommendation": {
    "type": "string",
    "description": "Recommendation"
   },
   "period": {
    "type": "string",
    "format": "date-time",
    "description": "period"
   },
   "preview": {
    "type": "string",
    "description": "Preview"
   },
   "returnForChanges": {
    "type": "string",
    "description": "Return for Changes"
   },
   "beforeActivation": {
    "type": "string",
    "description": "before activation"
   },
   "troubleshootGovernAndOptimizeThem": {
    "type": "string",
    "description": "troubleshoot, govern and optimize them?"
   },
   "managingAvailabilityAndSynchronization": {
    "type": "string",
    "description": "managing availability and synchronization"
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
    "description": "Minimum Quantity"
   },
   "maximumQuantity": {
    "type": "integer",
    "description": "Maximum Quantity"
   },
   "maximumPerTransaction": {
    "type": "string",
    "description": "Maximum Per Transaction"
   },
   "maximumPerCustomer": {
    "type": "string",
    "description": "Maximum Per Customer"
   },
   "maximumPerDay": {
    "type": "string",
    "description": "Maximum Per Day"
   },
   "maximumPerEvent": {
    "type": "string",
    "description": "Maximum Per Event"
   },
   "maximumPerProduct": {
    "type": "string",
    "description": "Maximum Per Product"
   },
   "reservationPermitted": {
    "type": "string",
    "description": "Reservation permitted"
   },
   "holdPermitted": {
    "type": "string",
    "description": "Hold permitted"
   },
   "paymentLinkPermitted": {
    "type": "string",
    "description": "Payment link permitted"
   },
   "partialPaymentPermitted": {
    "type": "string",
    "description": "Partial payment permitted"
   },
   "discountPermitted": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Discount permitted"
   },
   "promoCodePermitted": {
    "type": "string",
    "description": "Promo code permitted"
   },
   "exchangePermitted": {
    "type": "string",
    "description": "Exchange permitted"
   },
   "reschedulePermitted": {
    "type": "string",
    "description": "Reschedule permitted"
   },
   "permissionControlled": {
    "type": "string",
    "description": "Permission-controlled"
   },
   "visible": {
    "type": "string",
    "description": "Visible"
   },
   "effectiveDated": {
    "type": "string",
    "description": "Effective-dated"
   },
   "audited": {
    "type": "string",
    "description": "Audited"
   },
   "withControlledOverrideGovernance": {
    "type": "string",
    "description": "with controlled override governance"
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
    "format": "date-time",
    "description": "Sales Start Date"
   },
   "salesStartTime": {
    "type": "string",
    "format": "date-time",
    "description": "Sales Start Time"
   },
   "salesEndDate": {
    "type": "string",
    "format": "date-time",
    "description": "Sales End Date"
   },
   "salesEndTime": {
    "type": "string",
    "format": "date-time",
    "description": "Sales End Time"
   },
   "timeZone": {
    "type": "string",
    "format": "date-time",
    "description": "Time Zone"
   },
   "daysOfWeek": {
    "type": "string",
    "description": "Days of Week"
   },
   "hoursOfOperation": {
    "type": "string",
    "description": "Hours of Operation"
   },
   "blackoutDates": {
    "type": "string",
    "description": "Blackout Dates"
   },
   "eventRelativeWindows": {
    "type": "string",
    "description": "Event-relative windows"
   },
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
   },
   "changeApplicableRule": {
    "type": "string",
    "description": "Change applicable rule"
   }
  }
 },
 "CustomerEligibilityRulesByChannelView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over catalogue state, assembled at read time from tables that already exist",
  "description": "**What Customer & Eligibility Rules by Channel displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "customerType": {
    "type": "string",
    "description": "Customer Type"
   },
   "membership": {
    "type": "string",
    "description": "Membership"
   },
   "loyaltyTier": {
    "type": "string",
    "description": "Loyalty Tier"
   },
   "country": {
    "type": "string",
    "description": "Country"
   },
   "residency": {
    "type": "string",
    "description": "Residency"
   },
   "age": {
    "type": "string",
    "description": "Age"
   },
   "corporateAccount": {
    "type": "string",
    "description": "Corporate Account"
   },
   "partner": {
    "type": "string",
    "description": "Partner"
   },
   "customerSegment": {
    "type": "string",
    "description": "Customer Segment"
   },
   "promoEligibility": {
    "type": "string",
    "description": "Promo Eligibility"
   },
   "authenticationStatus": {
    "type": "string",
    "description": "Authentication Status"
   },
   "purchaseHistory": {
    "type": "string",
    "description": "Purchase History"
   },
   "salesTerritory": {
    "type": "string",
    "description": "Sales Territory"
   },
   "b2c": {
    "type": "string",
    "description": "B2C"
   },
   "pos": {
    "type": "string",
    "description": "POS"
   },
   "ota": {
    "type": "string",
    "description": "OTA"
   },
   "internationalReseller": {
    "type": "string",
    "description": "International Reseller"
   },
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
   "withExplanation": {
    "type": "string",
    "description": "with explanation"
   }
  }
 },
 "InventoryCapacityChannelAllocationView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over catalogue state, assembled at read time from tables that already exist",
  "description": "**What Inventory, Capacity & Channel Allocation displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "exampleOtaReceives15": {
    "type": "number",
    "description": "Example: OTA receives 15%"
   },
   "productEvent": {
    "type": "string",
    "description": "Product/Event"
   },
   "capacityPool": {
    "type": "integer",
    "description": "Capacity Pool"
   },
   "channel": {
    "type": "string",
    "description": "Channel"
   },
   "allocation": {
    "type": "string",
    "description": "Allocation"
   },
   "minimum": {
    "type": "string",
    "description": "Minimum"
   },
   "maximum": {
    "type": "string",
    "description": "Maximum"
   },
   "replenishmentRule": {
    "type": "string",
    "description": "Replenishment Rule"
   },
   "oversellPermission": {
    "type": "string",
    "description": "Oversell Permission"
   },
   "waitlistBehaviorWhereApplicable": {
    "type": "string",
    "description": "Waitlist behavior where applicable"
   },
   "allocated": {
    "type": "string",
    "description": "Allocated"
   },
   "sold": {
    "type": "string",
    "description": "Sold"
   },
   "held": {
    "type": "string",
    "description": "Held"
   },
   "remaining": {
    "type": "string",
    "description": "Remaining"
   },
   "utilization": {
    "type": "number",
    "description": "Utilization %"
   },
   "released": {
    "type": "string",
    "description": "Released"
   },
   "returned": {
    "type": "string",
    "description": "Returned"
   }
  }
 },
 "ProductCatalogueAssignmentInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures",
  "description": "**What Product & Catalogue Assignment submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "individualProduct": {
    "type": "string",
    "description": "Individual product"
   },
   "productFamily": {
    "type": "string",
    "description": "Product family"
   },
   "productCategory": {
    "type": "string",
    "description": "Product category"
   },
   "event": {
    "type": "string",
    "description": "Event"
   },
   "attraction": {
    "type": "string",
    "description": "Attraction"
   },
   "venueCatalogue": {
    "type": "string",
    "description": "Venue catalogue"
   },
   "productCollection": {
    "type": "string",
    "description": "Product collection"
   },
   "entireApprovedCatalogue": {
    "type": "string",
    "description": "Entire approved catalogue"
   },
   "draftProducts": {
    "type": "string",
    "description": "Draft products"
   },
   "retiredProducts": {
    "type": "string",
    "description": "Retired products"
   },
   "productsOutsideValidity": {
    "type": "string",
    "description": "Products outside validity"
   },
   "productsUnavailableForTheChannel": {
    "type": "string",
    "description": "Products unavailable for the channel"
   }
  }
 },
 "ProductCatalogueAssignmentView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over catalogue state, assembled at read time from tables that already exist",
  "description": "**What Product & Catalogue Assignment displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "individualProduct": {
    "type": "string",
    "description": "Individual product"
   },
   "productFamily": {
    "type": "string",
    "description": "Product family"
   },
   "productCategory": {
    "type": "string",
    "description": "Product category"
   },
   "event": {
    "type": "string",
    "description": "Event"
   },
   "attraction": {
    "type": "string",
    "description": "Attraction"
   },
   "venueCatalogue": {
    "type": "string",
    "description": "Venue catalogue"
   },
   "productCollection": {
    "type": "string",
    "description": "Product collection"
   },
   "entireApprovedCatalogue": {
    "type": "string",
    "description": "Entire approved catalogue"
   },
   "product": {
    "type": "string",
    "description": "Product"
   },
   "productType": {
    "type": "string",
    "description": "Product Type"
   },
   "venue": {
    "type": "string",
    "description": "Venue"
   },
   "status": {
    "type": "integer",
    "description": "Status"
   },
   "validity": {
    "type": "string",
    "description": "Validity"
   },
   "channelStatus": {
    "type": "integer",
    "description": "Channel Status"
   },
   "pricingStatus": {
    "type": "integer",
    "description": "Pricing Status"
   },
   "capacityStatus": {
    "type": "integer",
    "description": "Capacity Status"
   },
   "effectiveFrom": {
    "type": "string",
    "description": "Effective From"
   },
   "effectiveTo": {
    "type": "string",
    "description": "Effective To"
   },
   "draftProducts": {
    "type": "string",
    "description": "Draft products"
   },
   "retiredProducts": {
    "type": "string",
    "description": "Retired products"
   },
   "productsOutsideValidity": {
    "type": "string",
    "description": "Products outside validity"
   },
   "productsUnavailableForTheChannel": {
    "type": "string",
    "description": "Products unavailable for the channel"
   }
  }
 },
 "SalesChannelCommandCenterView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over catalogue state, assembled at read time from tables that already exist",
  "description": "**What Sales Channel Command Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "b2cWeb": {
    "type": "string",
    "description": "B2C Web"
   },
   "b2cMobileApp": {
    "type": "string",
    "description": "B2C Mobile App"
   },
   "pos": {
    "type": "string",
    "description": "POS"
   },
   "mobilePos": {
    "type": "string",
    "description": "Mobile POS"
   },
   "flyingPos": {
    "type": "string",
    "description": "Flying POS"
   },
   "kiosk": {
    "type": "string",
    "description": "Kiosk"
   },
   "callCenter": {
    "type": "string",
    "description": "Call Center"
   },
   "b2bPortal": {
    "type": "string",
    "description": "B2B Portal"
   },
   "reseller": {
    "type": "string",
    "description": "Reseller"
   },
   "ota": {
    "type": "string",
    "description": "OTA"
   },
   "api": {
    "type": "string",
    "description": "API"
   },
   "partnerPortal": {
    "type": "string",
    "description": "Partner Portal"
   },
   "marketplace": {
    "type": "string",
    "description": "Marketplace"
   },
   "thirdPartyChannel": {
    "type": "string",
    "description": "Third-Party Channel"
   },
   "customChannel": {
    "type": "string",
    "description": "Custom Channel"
   },
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
    "type": "string",
    "description": "Channels in Draft"
   },
   "channelsWithErrors": {
    "type": "integer",
    "description": "Channels With Errors"
   },
   "productsDistributed": {
    "type": "string",
    "description": "Products Distributed"
   },
   "channelsWithCapacityAlerts": {
    "type": "integer",
    "description": "Channels With Capacity Alerts"
   },
   "channelsWithPricingIssues": {
    "type": "string",
    "description": "Channels With Pricing Issues"
   },
   "scheduledActivations": {
    "type": "integer",
    "description": "Scheduled Activations"
   },
   "scheduledDeactivations": {
    "type": "integer",
    "description": "Scheduled Deactivations"
   },
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
    "description": "Channel Type"
   },
   "brand": {
    "type": "string",
    "description": "Brand"
   },
   "venueScope": {
    "type": "string",
    "description": "Venue/Scope"
   },
   "products": {
    "type": "string",
    "description": "Products"
   },
   "currency": {
    "type": "string",
    "description": "Currency"
   },
   "status": {
    "type": "string",
    "description": "Status"
   },
   "publicationStatus": {
    "type": "string",
    "description": "Publication Status"
   },
   "integrationStatus": {
    "type": "string",
    "description": "Integration Status"
   },
   "lastUpdated": {
    "type": "string",
    "format": "date-time",
    "description": "Last Updated"
   },
   "owner": {
    "type": "string",
    "description": "Owner"
   },
   "priceProfile": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "price profile"
   }
  }
 }
}
```
