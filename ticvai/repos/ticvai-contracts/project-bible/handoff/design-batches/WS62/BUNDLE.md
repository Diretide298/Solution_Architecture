# WS62 — Ticket Resale Marketplace board 1

**10 screens · 10 operations · 14 schemas · 2 permissions**

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
  `ORDER_CREATE, ORDER_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **0 of these operations work offline**
  
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `ADM-278` | Resale Marketplace Command Center | commandCentre | 1 | 0 | — |
| `ADM-279` | Resale Eligibility Rule Configuration | configEditor | 1 | 0 | — |
| `ADM-280` | Resale Policy & Marketplace Settings | configEditor | 1 | 0 | — |
| `ADM-281` | Listing Creation & Seller Configuration | configEditor | 1 | 0 | — |
| `ADM-282` | Resale Pricing & Price Guardrails | configEditor | 1 | 0 | — |
| `ADM-283` | Resale Fees, Commission & Seller Proceeds | configEditor | 1 | 0 | — |
| `ADM-284` | Listing Approval & Moderation | listDetail | 1 | 0 | — |
| `ADM-285` | Resale Inventory & Availability Management | listDetail | 1 | 0 | — |
| `ADM-286` | Listing Lifecycle, Expiry & Cancellation | configEditor | 1 | 0 | — |
| `ADM-287` | AI Resale Configuration & Marketplace Recommendations | configEditor | 1 | 0 | — |

## Thin screens in this batch

**ADM-285 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "ADM-278",
  "name": "Resale Marketplace Command Center",
  "module": "Commercial",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Ticket Resale Marketplace_Reference.pdf",
   "board": "1",
   "number": "3.1.1",
   "page": 4
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/resale-marketplace-command-center-adm-278",
   "component": "apps/ticvai-web/src/routes/commercial/ResaleMarketplaceCommandCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-002"
   ],
   "exitTo": [
    "ADM-002",
    "ADM-279",
    "ADM-280",
    "ADM-281",
    "ADM-282",
    "ADM-283",
    "ADM-284",
    "ADM-285",
    "ADM-286",
    "ADM-287"
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
     "to": "ADM-279",
     "trigger": "Works in Resale Eligibility Rule Configuration",
     "provenance": "flow F171 step 1→2",
     "operation": "listResaleMarketplace"
    },
    {
     "to": "ADM-280",
     "trigger": "Works in Resale Policy & Marketplace Settings",
     "provenance": "flow F171 step 3→4",
     "operation": "listResaleMarketplace"
    },
    {
     "to": "ADM-281",
     "trigger": "Works in Listing Creation & Seller Configuration",
     "provenance": "flow F171 step 5→6",
     "operation": "listResaleMarketplace"
    },
    {
     "to": "ADM-282",
     "trigger": "Works in Resale Pricing & Price Guardrails",
     "provenance": "flow F171 step 7→8",
     "operation": "listResaleMarketplace"
    },
    {
     "to": "ADM-283",
     "trigger": "Works in Resale Fees, Commission & Seller Proceeds",
     "provenance": "flow F171 step 9→10",
     "operation": "listResaleMarketplace"
    },
    {
     "to": "ADM-284",
     "trigger": "Works in Listing Approval & Moderation",
     "provenance": "flow F171 step 11→12",
     "operation": "listResaleMarketplace"
    },
    {
     "to": "ADM-285",
     "trigger": "Works in Resale Inventory & Availability Management",
     "provenance": "flow F171 step 13→14",
     "operation": "listResaleMarketplace"
    },
    {
     "to": "ADM-286",
     "trigger": "Works in Listing Lifecycle, Expiry & Cancellation",
     "provenance": "flow F171 step 15→16",
     "operation": "listResaleMarketplace"
    },
    {
     "to": "ADM-287",
     "trigger": "Works in AI Resale Configuration & Marketplace Recommendations",
     "provenance": "flow F171 step 17→18",
     "operation": "listResaleMarketplace"
    }
   ]
  },
  "density": "compact",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen both a metric directory (§Display) and a per-row directory (§Each listing should show) — counts over a population, then the population",
  "purpose": "Provide administrators with a centralized operational view of the TICVAI resale marketplace.",
  "purposeNote": "An authorized administrator can understand the current state of the resale marketplace, identify listings requiring attention and navigate directly to the appropriate operational action.",
  "layout": {
   "template": "dashboard",
   "regions": [
    {
     "name": "contentBody",
     "slot": "filters",
     "components": [
      {
       "kind": "searchField",
       "label": "Search resale marketplace",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 4 §Filter by"
      },
      {
       "kind": "multiSelect",
       "label": "Filter by",
       "columns": [
        "ResaleMarketplaceCommandCenterView.venue",
        "Event",
        "Product",
        "ResaleMarketplaceCommandCenterView.seller",
        "Date",
        "Listing status",
        "Price range",
        "Resale channel",
        "Risk level",
        "Approval status"
       ],
       "notes": "The pack filters this screen by venue, event, product, seller, date, listing status and 4 more — which are present is a decision the pack already made.",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 4 §Filter by"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "Active Listings",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 4 §Display",
       "bindsTo": "ResaleMarketplaceCommandCenterView.activeListings"
      },
      {
       "kind": "metricTile",
       "label": "Pending Approval",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 4 §Display",
       "bindsTo": "ResaleMarketplaceCommandCenterView.pendingApproval"
      },
      {
       "kind": "metricTile",
       "label": "Tickets Available for Resale",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 4 §Display",
       "bindsTo": "ResaleMarketplaceCommandCenterView.ticketsAvailableForResale"
      },
      {
       "kind": "metricTile",
       "label": "Listings Sold Today",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 4 §Display",
       "bindsTo": "ResaleMarketplaceCommandCenterView.listingsSoldToday"
      },
      {
       "kind": "metricTile",
       "label": "Expiring Listings",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 4 §Display",
       "bindsTo": "ResaleMarketplaceCommandCenterView.expiringListings"
      },
      {
       "kind": "metricTile",
       "label": "Suspended Listings",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 4 §Display",
       "bindsTo": "ResaleMarketplaceCommandCenterView.suspendedListings"
      },
      {
       "kind": "metricTile",
       "label": "Rejected Listings",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 4 §Display",
       "bindsTo": "ResaleMarketplaceCommandCenterView.rejectedListings"
      },
      {
       "kind": "metricTile",
       "label": "Average Resale Price",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 4 §Display",
       "bindsTo": "ResaleMarketplaceCommandCenterView.averageResalePrice"
      },
      {
       "kind": "metricTile",
       "label": "Gross Resale Value",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 4 §Display",
       "bindsTo": "ResaleMarketplaceCommandCenterView.grossResaleValue"
      },
      {
       "kind": "metricTile",
       "label": "Marketplace Fees",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 4 §Display",
       "bindsTo": "ResaleMarketplaceCommandCenterView.marketplaceFees"
      },
      {
       "kind": "metricTile",
       "label": "Seller Proceeds",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 4 §Display",
       "bindsTo": "ResaleMarketplaceCommandCenterView.sellerProceeds"
      },
      {
       "kind": "metricTile",
       "label": "Conversion Rate",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 4 §Display",
       "bindsTo": "ResaleMarketplaceCommandCenterView.conversionRate"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "moduleTiles",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every resale marketplace",
       "columns": [
        "ResaleMarketplaceCommandCenterView.listingId",
        "ResaleMarketplaceCommandCenterView.originalOrderTicketId",
        "ResaleMarketplaceCommandCenterView.eventProduct",
        "ResaleMarketplaceCommandCenterView.venue",
        "ResaleMarketplaceCommandCenterView.eventDate",
        "ResaleMarketplaceCommandCenterView.sectionRowSeat",
        "ResaleMarketplaceCommandCenterView.seller",
        "ResaleMarketplaceCommandCenterView.originalPrice",
        "ResaleMarketplaceCommandCenterView.listedPrice",
        "ResaleMarketplaceCommandCenterView.priceVariance",
        "ResaleMarketplaceCommandCenterView.marketplaceFee",
        "ResaleMarketplaceCommandCenterView.sellerProceeds",
        "ResaleMarketplaceCommandCenterView.listingDate",
        "ResaleMarketplaceCommandCenterView.expiry",
        "ResaleMarketplaceCommandCenterView.status",
        "ResaleMarketplaceCommandCenterView.riskIndicator"
       ],
       "bindsTo": "ResaleMarketplaceCommandCenterView",
       "operation": "listResaleMarketplace",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 4 §Each listing should show"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected resale marketplace",
       "bindsTo": "ResaleMarketplaceCommandCenterView",
       "columns": [
        "ResaleMarketplaceCommandCenterView.listingId",
        "ResaleMarketplaceCommandCenterView.originalOrderTicketId",
        "ResaleMarketplaceCommandCenterView.eventProduct",
        "ResaleMarketplaceCommandCenterView.venue",
        "ResaleMarketplaceCommandCenterView.eventDate",
        "ResaleMarketplaceCommandCenterView.sectionRowSeat",
        "ResaleMarketplaceCommandCenterView.seller",
        "ResaleMarketplaceCommandCenterView.originalPrice",
        "ResaleMarketplaceCommandCenterView.listedPrice",
        "ResaleMarketplaceCommandCenterView.priceVariance",
        "ResaleMarketplaceCommandCenterView.marketplaceFee",
        "ResaleMarketplaceCommandCenterView.sellerProceeds",
        "ResaleMarketplaceCommandCenterView.listingDate",
        "ResaleMarketplaceCommandCenterView.expiry",
        "ResaleMarketplaceCommandCenterView.status",
        "ResaleMarketplaceCommandCenterView.riskIndicator"
       ],
       "notes": null,
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 4 §Each listing should show"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The resale marketplace list; the counts above it resolve separately.",
   "error": "Could not load. Names which read failed and leaves the resale marketplace untouched.",
   "emptyFirstRun": "No resale marketplace yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the resale marketplace are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listResaleMarketplace",
    "contract": "orders",
    "purpose": "Resale Marketplace Command Center",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-278"
  },
  "apisNote": "Regenerated 9 September 2026 from Ticket Resale Marketplace_Reference.pdf page 4. 30 of 38 labels bound to a contract property; 38 of 49 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-279",
  "name": "Resale Eligibility Rule Configuration",
  "module": "Commercial",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Ticket Resale Marketplace_Reference.pdf",
   "board": "1",
   "number": "3.1.2",
   "page": 5
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/resale-eligibility-rule-configuration-adm-279",
   "component": "apps/ticvai-web/src/routes/commercial/ResaleEligibilityRuleConfiguration.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-278"
   ],
   "exitTo": [
    "ADM-278"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-278, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-278",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F171 step 2→3",
     "operation": "setResaleEligibilityRule"
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Administrators can define eligibility by; Configure) and no display directory — it is settings, not a population",
  "purpose": "Define whether a ticket is allowed to enter the resale marketplace. Not every TICVAI ticket should automatically be resellable.",
  "purposeNote": "for resale.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 2 actions on this screen and the screen declares 1 operation.** Unserved: Identity verification requirement, Membership restriction. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Ticket Resale Marketplace_Reference.pdf, page 5 §Support"
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
       "label": "Product",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 5 §Administrators can define eligibility by"
      },
      {
       "kind": "selectField",
       "label": "Ticket type",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 5 §Administrators can define eligibility by"
      },
      {
       "kind": "selectField",
       "label": "Event",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 5 §Administrators can define eligibility by"
      },
      {
       "kind": "selectField",
       "label": "Venue",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 5 §Administrators can define eligibility by"
      },
      {
       "kind": "selectField",
       "label": "Performance",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 5 §Administrators can define eligibility by"
      },
      {
       "kind": "selectField",
       "label": "Membership type",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 5 §Administrators can define eligibility by"
      },
      {
       "kind": "selectField",
       "label": "Sales channel",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 5 §Administrators can define eligibility by"
      },
      {
       "kind": "selectField",
       "label": "Customer segment",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 5 §Administrators can define eligibility by"
      },
      {
       "kind": "selectField",
       "label": "Price category",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 5 §Administrators can define eligibility by"
      },
      {
       "kind": "selectField",
       "label": "Promotion",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 5 §Administrators can define eligibility by"
      },
      {
       "kind": "selectField",
       "label": "Ticket status",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 5 §Administrators can define eligibility by"
      },
      {
       "kind": "selectField",
       "label": "Payment status",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 5 §Administrators can define eligibility by"
      },
      {
       "kind": "selectField",
       "label": "Ticket ownership status",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 5 §Administrators can define eligibility by"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Identity verification requirement",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 5 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Membership restriction",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 5 §Support"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The resale eligibility rule configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the resale eligibility rule untouched.",
   "emptyFirstRun": "No resale eligibility rule configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setResaleEligibilityRule",
    "contract": "orders",
    "purpose": "Resale Eligibility Rule Configuration",
    "trigger": "onAction",
    "invalidates": [
     "setResaleEligibilityRule"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-279"
  },
  "apisNote": "Regenerated 9 September 2026 from Ticket Resale Marketplace_Reference.pdf page 5. 0 of 0 labels bound to a contract property; 15 of 42 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-280",
  "name": "Resale Policy & Marketplace Settings",
  "module": "Commercial",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Ticket Resale Marketplace_Reference.pdf",
   "board": "1",
   "number": "3.1.3",
   "page": 7
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/resale-policy-marketplace-settings-adm-280",
   "component": "apps/ticvai-web/src/routes/commercial/ResalePolicyMarketplaceSettings.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-278"
   ],
   "exitTo": [
    "ADM-278"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-278, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-278",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F171 step 4→5",
     "operation": "listResalePolicyMarketplace"
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Administrators can define; Configure) and no display directory — it is settings, not a population",
  "purpose": "Configure the overall business policies governing a resale marketplace.",
  "purposeNote": "Administrators can establish different resale marketplace policies for different organizations, venues, events and products without software development.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Marketplace name",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 7 §Administrators can define"
      },
      {
       "kind": "selectField",
       "label": "Marketplace status",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 7 §Administrators can define"
      },
      {
       "kind": "selectField",
       "label": "Applicable organization",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 7 §Administrators can define"
      },
      {
       "kind": "selectField",
       "label": "Venue",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 7 §Administrators can define"
      },
      {
       "kind": "selectField",
       "label": "Brand",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 7 §Administrators can define"
      },
      {
       "kind": "selectField",
       "label": "Currency",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 7 §Administrators can define"
      },
      {
       "kind": "selectField",
       "label": "Time zone",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 7 §Administrators can define"
      },
      {
       "kind": "selectField",
       "label": "Supported language",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 7 §Administrators can define"
      },
      {
       "kind": "selectField",
       "label": "Marketplace sales channel",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 7 §Administrators can define"
      },
      {
       "kind": "selectField",
       "label": "Customer terms",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 7 §Administrators can define"
      },
      {
       "kind": "selectField",
       "label": "Seller terms",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 7 §Administrators can define"
      },
      {
       "kind": "selectField",
       "label": "Seller verification",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 7 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Identity requirements",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 7 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Bank/payout information",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 7 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Seller terms acceptance",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 7 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Listing confirmation",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 7 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Seller notifications",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 7 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Buyer terms",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 7 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Marketplace disclosures",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 7 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Resale ticket labeling",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 7 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Refund conditions",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 7 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Service fees",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 7 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Purchase limits",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 7 §Configure"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The resale policy marketplace configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the resale policy marketplace untouched.",
   "emptyFirstRun": "No resale policy marketplace configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listResalePolicyMarketplace",
    "contract": "orders",
    "purpose": "Resale Policy & Marketplace Settings",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-280"
  },
  "apisNote": "Regenerated 9 September 2026 from Ticket Resale Marketplace_Reference.pdf page 7. 0 of 0 labels bound to a contract property; 23 of 32 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-281",
  "name": "Listing Creation & Seller Configuration",
  "module": "Commercial",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Ticket Resale Marketplace_Reference.pdf",
   "board": "1",
   "number": "3.1.4",
   "page": 9
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/listing-creation-seller-configuration-adm-281",
   "component": "apps/ticvai-web/src/routes/commercial/ListingCreationSellerConfiguration.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-278"
   ],
   "exitTo": [
    "ADM-278"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-278, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-278",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F171 step 6→7",
     "operation": "createListingSeller"
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure whether seller may; Capture) and no display directory — it is settings, not a population",
  "purpose": "Define how eligible ticket holders create resale listings.",
  "purposeNote": "An eligible ticket holder can create a resale listing through a controlled workflow without allowing invalid, already-used or unauthorized tickets to enter the marketplace.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 2 actions on this screen and the screen declares 1 operation.** Unserved: Single ticket listing, Multiple ticket listing. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Ticket Resale Marketplace_Reference.pdf, page 9 §Support"
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
       "label": "Choose selling price",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 9 §Configure whether seller may"
      },
      {
       "kind": "selectField",
       "label": "Accept recommended price",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 9 §Configure whether seller may"
      },
      {
       "kind": "selectField",
       "label": "Edit active listing",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 9 §Configure whether seller may"
      },
      {
       "kind": "selectField",
       "label": "Withdraw listing",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 9 §Configure whether seller may"
      },
      {
       "kind": "selectField",
       "label": "Relist expired listing",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 9 §Configure whether seller may"
      },
      {
       "kind": "selectField",
       "label": "Change price",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 9 §Configure whether seller may"
      },
      {
       "kind": "selectField",
       "label": "Select payout method",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 9 §Configure whether seller may"
      },
      {
       "kind": "selectField",
       "label": "Listing ID",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 9 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Ticket ID",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 9 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Seller",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 9 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Listing price",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 9 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Original price",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 9 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Fee",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 9 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Estimated proceeds",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 9 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Listing date",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 9 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Expiration",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 9 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Seller terms acceptance",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 9 §Capture"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Single ticket listing",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 9 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Multiple ticket listing",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 9 §Support"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The listing creation seller configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the listing creation seller untouched.",
   "emptyFirstRun": "No listing creation seller configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "createListingSeller",
    "contract": "orders",
    "purpose": "Listing Creation & Seller Configuration",
    "trigger": "onAction",
    "invalidates": [
     "createListingSeller"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-281"
  },
  "apisNote": "Regenerated 9 September 2026 from Ticket Resale Marketplace_Reference.pdf page 9. 0 of 0 labels bound to a contract property; 19 of 42 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-282",
  "name": "Resale Pricing & Price Guardrails",
  "module": "Commercial",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Ticket Resale Marketplace_Reference.pdf",
   "board": "1",
   "number": "3.1.5",
   "page": 10
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/resale-pricing-price-guardrails-adm-282",
   "component": "apps/ticvai-web/src/routes/commercial/ResalePricingPriceGuardrails.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-278"
   ],
   "exitTo": [
    "ADM-278"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-278, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-278",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F171 step 8→9",
     "operation": "listResalePricingPrice"
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure; Configured resale policy) and no display directory — it is settings, not a population",
  "purpose": "Control the permitted resale price while protecting the operator, seller and buyer.",
  "purposeNote": "No resale listing can be published at a price outside the applicable approved marketplace pricing policy.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Face-value only",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 10 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Minimum resale price",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 10 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Maximum resale price",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 10 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Maximum markup %",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 10 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Maximum discount %",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 10 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Fixed resale price",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 10 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Dynamic permitted range",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 10 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Event-specific range",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 10 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Product-specific range",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 10 §Configure"
      },
      {
       "kind": "textField",
       "label": "Seller can edit price",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 10 §Configure"
      },
      {
       "kind": "textField",
       "label": "Number of price changes",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 10 §Configure"
      },
      {
       "kind": "textField",
       "label": "Minimum interval between changes",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 10 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Automatic price reduction",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 10 §Configure"
      },
      {
       "kind": "textField",
       "label": "Freeze price after reservation",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 10 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Price adjustment cutoff",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 10 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Minimum: AED 160",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 10 §Configured resale policy"
      },
      {
       "kind": "selectField",
       "label": "Maximum: AED 240",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 10 §Configured resale policy"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The resale pricing price configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the resale pricing price untouched.",
   "emptyFirstRun": "No resale pricing price configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listResalePricingPrice",
    "contract": "orders",
    "purpose": "Resale Pricing & Price Guardrails",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-282"
  },
  "apisNote": "Regenerated 9 September 2026 from Ticket Resale Marketplace_Reference.pdf page 10. 0 of 0 labels bound to a contract property; 17 of 38 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-283",
  "name": "Resale Fees, Commission & Seller Proceeds",
  "module": "Commercial",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Ticket Resale Marketplace_Reference.pdf",
   "board": "1",
   "number": "3.1.6",
   "page": 12
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/resale-fees-commission-seller-proceeds-adm-283",
   "component": "apps/ticvai-web/src/routes/commercial/ResaleFeesCommissionSellerProceeds.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-278"
   ],
   "exitTo": [
    "ADM-278"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-278, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-278",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F171 step 10→11",
     "operation": "listResaleFeeCommission"
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Define by) and no display directory — it is settings, not a population",
  "purpose": "Configure the commercial model of the resale marketplace.",
  "purposeNote": "estimated seller proceeds using configured rules.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 6 actions on this screen and the screen declares 1 operation.** Unserved: Seller fee, Buyer fee, Percentage fee, Administrative fee, Venue fee, Tax on fee. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Ticket Resale Marketplace_Reference.pdf, page 12 §Support"
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
       "label": "Tenant",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 12 §Define by"
      },
      {
       "kind": "selectField",
       "label": "Venue",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 12 §Define by"
      },
      {
       "kind": "selectField",
       "label": "Event",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 12 §Define by"
      },
      {
       "kind": "selectField",
       "label": "Product",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 12 §Define by"
      },
      {
       "kind": "selectField",
       "label": "Seller type",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 12 §Define by"
      },
      {
       "kind": "selectField",
       "label": "Buyer type",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 12 §Define by"
      },
      {
       "kind": "selectField",
       "label": "Channel",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 12 §Define by"
      },
      {
       "kind": "selectField",
       "label": "Currency",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 12 §Define by"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Seller fee",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 12 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Buyer fee",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 12 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Percentage fee",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 12 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Administrative fee",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 12 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Venue fee",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 12 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Tax on fee",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 12 §Support"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The resale fees commission configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the resale fees commission untouched.",
   "emptyFirstRun": "No resale fees commission configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listResaleFeeCommission",
    "contract": "orders",
    "purpose": "Resale Fees, Commission & Seller Proceeds",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-283"
  },
  "apisNote": "Regenerated 9 September 2026 from Ticket Resale Marketplace_Reference.pdf page 12. 0 of 0 labels bound to a contract property; 14 of 32 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-284",
  "name": "Listing Approval & Moderation",
  "module": "Commercial",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Ticket Resale Marketplace_Reference.pdf",
   "board": "1",
   "number": "3.1.7",
   "page": 13
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/listing-approval-moderation-adm-284",
   "component": "apps/ticvai-web/src/routes/commercial/ListingApprovalModeration.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-278"
   ],
   "exitTo": [
    "ADM-278"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-278, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-278",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F171 step 12→13",
     "operation": "approveListingModeration"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Determine whether listings are published automatically or require operator review.",
  "purposeNote": "Listings requiring governance cannot become publicly available until the configured approval or risk-control conditions are satisfied.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every listing approval moderation",
       "columns": [
        "ListingApprovalModerationView.listing",
        "ListingApprovalModerationView.seller",
        "ListingApprovalModerationView.ticket",
        "ListingApprovalModerationView.event",
        "ListingApprovalModerationView.originalPrice",
        "ListingApprovalModerationView.listingPrice",
        "ListingApprovalModerationView.priceVariance",
        "ListingApprovalModerationView.riskScore",
        "Trigger reason",
        "ListingApprovalModerationView.submittedDate"
       ],
       "bindsTo": "ListingApprovalModerationView",
       "operation": "approveListingModeration",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 13 §Display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected listing approval moderation",
       "bindsTo": "ListingApprovalModerationView",
       "columns": [
        "ListingApprovalModerationView.listing",
        "ListingApprovalModerationView.seller",
        "ListingApprovalModerationView.ticket",
        "ListingApprovalModerationView.event",
        "ListingApprovalModerationView.originalPrice",
        "ListingApprovalModerationView.listingPrice",
        "ListingApprovalModerationView.priceVariance",
        "ListingApprovalModerationView.riskScore",
        "Trigger reason",
        "ListingApprovalModerationView.submittedDate"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Automatic Approval”, “Manual Approval”, “Risk-Based Approval”.",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 13 §Display"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Approve",
       "provenance": "contract operation approveListingModeration",
       "permission": "Approve"
      },
      {
       "kind": "banner",
       "label": "Permissions this screen separates",
       "notes": "**The pack separates these permissions and no action on the screen claims them yet:** Reject, Request Information, Suspend, Escalate, Add Internal Note. Each needs attaching to the control it gates, or the screen needs the control.",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 13 §Authorized users can"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The listing approval moderation list.",
   "error": "Could not load. Names which read failed and leaves the listing approval moderation untouched.",
   "emptyFirstRun": "No listing approval moderation yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the listing approval moderation are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "approveListingModeration",
    "contract": "orders",
    "purpose": "Listing Approval & Moderation",
    "trigger": "onAction",
    "invalidates": [
     "approveListingModeration"
    ]
   }
  ],
  "entryState": {
   "preloaded": [
    "ListingApprovalModerationView.listing",
    "ListingApprovalModerationView.seller",
    "ListingApprovalModerationView.ticket",
    "ListingApprovalModerationView.event",
    "ListingApprovalModerationView.originalPrice",
    "ListingApprovalModerationView.listingPrice"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-284"
  },
  "apisNote": "Regenerated 9 September 2026 from Ticket Resale Marketplace_Reference.pdf page 13. 9 of 10 labels bound to a contract property; 16 of 37 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-285",
  "name": "Resale Inventory & Availability Management",
  "module": "Commercial",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Ticket Resale Marketplace_Reference.pdf",
   "board": "1",
   "number": "3.1.8",
   "page": 15
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/resale-inventory-availability-management-adm-285",
   "component": "apps/ticvai-web/src/routes/commercial/ResaleInventoryAvailabilityManagement.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-278"
   ],
   "exitTo": [
    "ADM-278"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-278, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-278",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F171 step 14→15",
     "operation": "listResaleInventoryAvailability"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Maintain an accurate, synchronized view of tickets currently available through resale.",
  "purposeNote": "Marketplace availability accurately represents eligible resale inventory and prevents the same ticket from being sold or listed more than once.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Ticket Resale Marketplace_Reference.pdf, page 15"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Ticket Resale Marketplace_Reference.pdf, page 15"
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
       "impliedBy": "listResaleInventoryAvailability",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The resale inventory availability list.",
   "error": "Could not load. Names which read failed and leaves the resale inventory availability untouched.",
   "emptyFirstRun": "No resale inventory availability yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the resale inventory availability are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listResaleInventoryAvailability",
    "contract": "orders",
    "purpose": "Resale Inventory & Availability Management",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "ResaleInventoryAvailabilityManagementView.event",
    "ResaleInventoryAvailabilityManagementView.performance",
    "ResaleInventoryAvailabilityManagementView.product",
    "ResaleInventoryAvailabilityManagementView.section",
    "ResaleInventoryAvailabilityManagementView.row"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-285"
  },
  "apisNote": "Regenerated 9 September 2026 from Ticket Resale Marketplace_Reference.pdf page 15. 0 of 0 labels bound to a contract property; 0 of 29 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-286",
  "name": "Listing Lifecycle, Expiry & Cancellation",
  "module": "Commercial",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Ticket Resale Marketplace_Reference.pdf",
   "board": "1",
   "number": "3.1.9",
   "page": 16
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/listing-lifecycle-expiry-cancellation-adm-286",
   "component": "apps/ticvai-web/src/routes/commercial/ListingLifecycleExpiryCancellation.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-278"
   ],
   "exitTo": [
    "ADM-278"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-278, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-278",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F171 step 16→17",
     "operation": "listListingLifecycleExpiry"
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure; Configure whether the ticket) and no display directory — it is settings, not a population",
  "purpose": "Control the full lifecycle of a resale listing from creation until sale, withdrawal or expiry.",
  "purposeNote": "Every resale listing follows a controlled and traceable lifecycle, with automatic removal when it is no longer commercially or operationally valid.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "textField",
       "label": "Seller can withdraw anytime",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 16 §Configure"
      },
      {
       "kind": "textField",
       "label": "Seller cannot withdraw while reserved",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 16 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Cancellation cutoff",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 16 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Cancellation fee",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 16 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Maximum withdrawals",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 16 §Configure"
      },
      {
       "kind": "textField",
       "label": "Returns to customer as normal ticket",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 16 §Configure whether the ticket"
      },
      {
       "kind": "selectField",
       "label": "Can be relisted",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 16 §Configure whether the ticket"
      },
      {
       "kind": "selectField",
       "label": "Requires operator action",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 16 §Configure whether the ticket"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The listing lifecycle expiry configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the listing lifecycle expiry untouched.",
   "emptyFirstRun": "No listing lifecycle expiry configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listListingLifecycleExpiry",
    "contract": "orders",
    "purpose": "Listing Lifecycle, Expiry & Cancellation",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-286"
  },
  "apisNote": "Regenerated 9 September 2026 from Ticket Resale Marketplace_Reference.pdf page 16. 0 of 0 labels bound to a contract property; 8 of 41 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-287",
  "name": "AI Resale Configuration & Marketplace Recommendations",
  "module": "Commercial",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Ticket Resale Marketplace_Reference.pdf",
   "board": "1",
   "number": "3.1.10",
   "page": 18
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/ai-resale-configuration-marketplace-recommendations-adm-287",
   "component": "apps/ticvai-web/src/routes/commercial/AiResaleConfigurationMarketplaceRecommendations.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-278"
   ],
   "exitTo": [
    "ADM-278"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-278, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation."
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configuration; AI Resale Configuration & Marketplace) and no display directory — it is settings, not a population",
  "purpose": "Provide TICVAI's AI intelligence layer for optimizing resale configuration while keeping commercial control with the operator. Board 2 manages what happens once a resale listing attracts a buyer and enters the transaction stage.",
  "purposeNote": "Administrators receive explainable, actionable AI recommendations for marketplace configuration and performance without AI bypassing approved commercial, security or governance controls. Board 1 — Final Screen Register Screen Backend Screen Primary Responsibility 3.1.1 Resale Marketplace Command Center Marketplace oversight Screen Backend Screen Primary Responsibility 3.1.2 Resale Eligibility Rule Configuration Determine what can be resold 3.1.3 Resale Policy & Marketplace Settings Marketplace business policies 3.1.4 Listing Creation & Seller Configuration Seller/listing journey 3.1.5 Resale P",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Pricing recommendations",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 18 §Configuration"
      },
      {
       "kind": "selectField",
       "label": "Demand prediction",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 18 §Configuration"
      },
      {
       "kind": "selectField",
       "label": "Listing recommendations",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 18 §Configuration"
      },
      {
       "kind": "selectField",
       "label": "Seller risk recommendations",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 18 §Configuration"
      },
      {
       "kind": "selectField",
       "label": "Expiry recommendations",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 18 §Configuration"
      },
      {
       "kind": "selectField",
       "label": "Marketplace optimization",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 18 §Configuration"
      },
      {
       "kind": "selectField",
       "label": "Anomaly detection",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 18 §Configuration"
      },
      {
       "kind": "selectField",
       "label": "3.1.10 AI optimization",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 18 §AI Resale Configuration & Marketplace"
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
       "provenance": "contract operation setResaleMarketplaceRecommendation"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The resale marketplace recommendations configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the resale marketplace recommendations untouched.",
   "emptyFirstRun": "No resale marketplace recommendations configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setResaleMarketplaceRecommendation",
    "contract": "orders",
    "purpose": "AI Resale Configuration & Marketplace Recommendations",
    "trigger": "onAction",
    "invalidates": [
     "setResaleMarketplaceRecommendation"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-287"
  },
  "apisNote": "Regenerated 9 September 2026 from Ticket Resale Marketplace_Reference.pdf page 18. 0 of 0 labels bound to a contract property; 8 of 74 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
 "approveListingModeration": {
  "method": "PUT",
  "path": "/listing-moderation",
  "contract": "orders",
  "summary": "Listing Approval & Moderation",
  "permission": "ORDER_CREATE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": "ListingApprovalModerationInput",
  "responds": "ListingApprovalModerationView"
 },
 "createListingSeller": {
  "method": "POST",
  "path": "/listing-seller",
  "contract": "orders",
  "summary": "Listing Creation & Seller Configuration",
  "permission": "ORDER_CREATE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": "ListingCreationSellerConfigurationInput",
  "responds": "ListingCreationSellerConfigurationView"
 },
 "listListingLifecycleExpiry": {
  "method": "GET",
  "path": "/listing-lifecycle-expiry",
  "contract": "orders",
  "summary": "Listing Lifecycle, Expiry & Cancellation",
  "permission": "ORDER_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "ListingLifecycleExpiryCancellationView"
 },
 "listResaleFeeCommission": {
  "method": "GET",
  "path": "/resale-fee-commission",
  "contract": "orders",
  "summary": "Resale Fees, Commission & Seller Proceeds",
  "permission": "ORDER_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "ResaleFeesCommissionSellerProceedsView"
 },
 "listResaleInventoryAvailability": {
  "method": "GET",
  "path": "/resale-inventory-availability",
  "contract": "orders",
  "summary": "Resale Inventory & Availability Management",
  "permission": "ORDER_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "ResaleInventoryAvailabilityManagementView"
 },
 "listResaleMarketplace": {
  "method": "GET",
  "path": "/resale-marketplace",
  "contract": "orders",
  "summary": "Resale Marketplace Command Center",
  "permission": "ORDER_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "event",
    "in": "query",
    "required": false
   },
   {
    "name": "product",
    "in": "query",
    "required": false
   },
   {
    "name": "date",
    "in": "query",
    "required": false
   },
   {
    "name": "listingStatus",
    "in": "query",
    "required": false
   },
   {
    "name": "priceRange",
    "in": "query",
    "required": false
   },
   {
    "name": "resaleChannel",
    "in": "query",
    "required": false
   },
   {
    "name": "riskLevel",
    "in": "query",
    "required": false
   },
   {
    "name": "approvalStatus",
    "in": "query",
    "required": false
   }
  ],
  "requestBody": null,
  "responds": "ResaleMarketplaceCommandCenterView"
 },
 "listResalePolicyMarketplace": {
  "method": "GET",
  "path": "/resale-policy-marketplace",
  "contract": "orders",
  "summary": "Resale Policy & Marketplace Settings",
  "permission": "ORDER_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "ResalePolicyMarketplaceSettingsView"
 },
 "listResalePricingPrice": {
  "method": "GET",
  "path": "/resale-pricing-price",
  "contract": "orders",
  "summary": "Resale Pricing & Price Guardrails",
  "permission": "ORDER_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "ResalePricingPriceGuardrailsView"
 },
 "setResaleEligibilityRule": {
  "method": "PUT",
  "path": "/resale-eligibility-rule",
  "contract": "orders",
  "summary": "Resale Eligibility Rule Configuration",
  "permission": "ORDER_CREATE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": "ResaleEligibilityRuleConfigurationInput",
  "responds": "ResaleEligibilityRuleConfigurationView"
 },
 "setResaleMarketplaceRecommendation": {
  "method": "PUT",
  "path": "/resale-marketplace-recommendation",
  "contract": "orders",
  "summary": "AI Resale Configuration & Marketplace Recommendations",
  "permission": "ORDER_CREATE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": "AiResaleConfigurationMarketplaceRecommendationsInput",
  "responds": "AiResaleConfigurationMarketplaceRecommendationsView"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "AiResaleConfigurationMarketplaceRecommendationsInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures",
  "description": "**What AI Resale Configuration & Marketplace Recommendations submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "highDemand": {
    "type": "string",
    "description": "high demand"
   },
   "category": {
    "type": "string",
    "description": "category"
   },
   "pricingRecommendations": {
    "type": "string",
    "description": "Pricing recommendations"
   },
   "demandPrediction": {
    "type": "string",
    "description": "Demand prediction"
   },
   "listingRecommendations": {
    "type": "string",
    "description": "Listing recommendations"
   },
   "sellerRiskRecommendations": {
    "type": "string",
    "description": "Seller risk recommendations"
   },
   "expiryRecommendations": {
    "type": "string",
    "format": "date-time",
    "description": "Expiry recommendations"
   },
   "marketplaceOptimization": {
    "type": "string",
    "description": "Marketplace optimization"
   },
   "anomalyDetection": {
    "type": "string",
    "description": "Anomaly detection"
   },
   "accept": {
    "type": "string",
    "description": "Accept"
   },
   "modify": {
    "type": "string",
    "description": "Modify"
   },
   "ignore": {
    "type": "string",
    "description": "Ignore"
   },
   "model": {
    "type": "string",
    "description": "model"
   },
   "synchronization": {
    "type": "string",
    "description": "synchronization"
   },
   "financialTransaction": {
    "type": "string",
    "description": "financial transaction"
   }
  }
 },
 "AiResaleConfigurationMarketplaceRecommendationsView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over orders state, assembled at read time from tables that already exist",
  "description": "**What AI Resale Configuration & Marketplace Recommendations displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "highDemand": {
    "type": "string",
    "description": "high demand"
   },
   "category": {
    "type": "string",
    "description": "category"
   },
   "pricingRecommendations": {
    "type": "string",
    "description": "Pricing recommendations"
   },
   "demandPrediction": {
    "type": "string",
    "description": "Demand prediction"
   },
   "listingRecommendations": {
    "type": "string",
    "description": "Listing recommendations"
   },
   "sellerRiskRecommendations": {
    "type": "string",
    "description": "Seller risk recommendations"
   },
   "expiryRecommendations": {
    "type": "string",
    "format": "date-time",
    "description": "Expiry recommendations"
   },
   "marketplaceOptimization": {
    "type": "string",
    "description": "Marketplace optimization"
   },
   "anomalyDetection": {
    "type": "string",
    "description": "Anomaly detection"
   },
   "accept": {
    "type": "string",
    "description": "Accept"
   },
   "modify": {
    "type": "string",
    "description": "Modify"
   },
   "ignore": {
    "type": "string",
    "description": "Ignore"
   },
   "model": {
    "type": "string",
    "description": "model"
   },
   "synchronization": {
    "type": "string",
    "description": "synchronization"
   },
   "financialTransaction": {
    "type": "string",
    "description": "financial transaction"
   }
  }
 },
 "ListingApprovalModerationInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures",
  "description": "**What Listing Approval & Moderation submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "highResalePrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "High resale price"
   },
   "unusualDiscount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Unusual discount"
   },
   "highValueTicket": {
    "type": "string",
    "description": "High-value ticket"
   },
   "vipTicket": {
    "type": "string",
    "description": "VIP ticket"
   },
   "sellerRisk": {
    "type": "string",
    "description": "Seller risk"
   },
   "newSeller": {
    "type": "integer",
    "description": "New seller"
   },
   "multipleListings": {
    "type": "string",
    "description": "Multiple listings"
   },
   "identityIssue": {
    "type": "string",
    "description": "Identity issue"
   },
   "paymentIssue": {
    "type": "string",
    "description": "Payment issue"
   },
   "ticketOwnershipConcern": {
    "type": "string",
    "description": "Ticket ownership concern"
   },
   "fraudIndicator": {
    "type": "string",
    "description": "Fraud indicator"
   },
   "requestInformation": {
    "type": "string",
    "description": "Request Information"
   }
  }
 },
 "ListingApprovalModerationView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over orders state, assembled at read time from tables that already exist",
  "description": "**What Listing Approval & Moderation displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "highResalePrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "High resale price"
   },
   "unusualDiscount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Unusual discount"
   },
   "highValueTicket": {
    "type": "string",
    "description": "High-value ticket"
   },
   "vipTicket": {
    "type": "string",
    "description": "VIP ticket"
   },
   "sellerRisk": {
    "type": "string",
    "description": "Seller risk"
   },
   "newSeller": {
    "type": "integer",
    "description": "New seller"
   },
   "multipleListings": {
    "type": "string",
    "description": "Multiple listings"
   },
   "identityIssue": {
    "type": "string",
    "description": "Identity issue"
   },
   "paymentIssue": {
    "type": "string",
    "description": "Payment issue"
   },
   "ticketOwnershipConcern": {
    "type": "string",
    "description": "Ticket ownership concern"
   },
   "fraudIndicator": {
    "type": "string",
    "description": "Fraud indicator"
   },
   "listing": {
    "type": "string",
    "description": "Listing"
   },
   "seller": {
    "type": "string",
    "description": "Seller"
   },
   "ticket": {
    "type": "string",
    "description": "Ticket"
   },
   "event": {
    "type": "string",
    "description": "Event"
   },
   "originalPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Original price"
   },
   "listingPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Listing price"
   },
   "priceVariance": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Price variance"
   },
   "riskScore": {
    "type": "number",
    "description": "Risk score"
   },
   "submittedDate": {
    "type": "string",
    "format": "date-time",
    "description": "Submitted date"
   },
   "requestInformation": {
    "type": "string",
    "description": "Request Information"
   }
  }
 },
 "ListingCreationSellerConfigurationInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures",
  "description": "**What Listing Creation & Seller Configuration submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "acceptTermsSubmitListing": {
    "type": "string",
    "description": "Accept Terms → Submit Listing"
   },
   "event": {
    "type": "string",
    "description": "Event"
   },
   "venue": {
    "type": "string",
    "description": "Venue"
   },
   "dateTime": {
    "type": "string",
    "format": "date-time",
    "description": "Date/time"
   },
   "ticketType": {
    "type": "string",
    "description": "Ticket type"
   },
   "section": {
    "type": "string",
    "description": "Section"
   },
   "row": {
    "type": "string",
    "description": "Row"
   },
   "seat": {
    "type": "string",
    "description": "Seat"
   },
   "originalPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Original price"
   },
   "ticketStatus": {
    "type": "string",
    "description": "Ticket status"
   },
   "resaleEligibility": {
    "type": "string",
    "description": "Resale eligibility"
   },
   "chooseSellingPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Choose selling price"
   },
   "acceptRecommendedPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Accept recommended price"
   },
   "relistExpiredListing": {
    "type": "string",
    "description": "Relist expired listing"
   },
   "changePrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Change price"
   },
   "listingId": {
    "type": "string",
    "description": "Listing ID"
   },
   "ticketId": {
    "type": "string",
    "description": "Ticket ID"
   },
   "seller": {
    "type": "string",
    "description": "Seller"
   },
   "listingPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Listing price"
   },
   "fee": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Fee"
   },
   "estimatedProceeds": {
    "type": "string",
    "description": "Estimated proceeds"
   },
   "listingDate": {
    "type": "string",
    "format": "date-time",
    "description": "Listing date"
   },
   "expiration": {
    "type": "string",
    "description": "Expiration"
   },
   "sellerTermsAcceptance": {
    "type": "string",
    "description": "Seller terms acceptance"
   },
   "singleTicketListing": {
    "type": "string",
    "description": "Single ticket listing"
   },
   "multipleTicketListing": {
    "type": "string",
    "description": "Multiple ticket listing"
   },
   "adjacentSeatGroup": {
    "type": "string",
    "description": "Adjacent-seat group"
   },
   "ticketOwnership": {
    "type": "string",
    "description": "Ticket ownership"
   },
   "ticketValidity": {
    "type": "string",
    "description": "Ticket validity"
   },
   "paymentStatus": {
    "type": "string",
    "description": "Payment status"
   },
   "existingListing": {
    "type": "string",
    "description": "Existing listing"
   },
   "ticketScanStatus": {
    "type": "string",
    "description": "Ticket scan status"
   }
  }
 },
 "ListingCreationSellerConfigurationView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over orders state, assembled at read time from tables that already exist",
  "description": "**What Listing Creation & Seller Configuration displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "acceptTermsSubmitListing": {
    "type": "string",
    "description": "Accept Terms → Submit Listing"
   },
   "event": {
    "type": "string",
    "description": "Event"
   },
   "venue": {
    "type": "string",
    "description": "Venue"
   },
   "dateTime": {
    "type": "string",
    "format": "date-time",
    "description": "Date/time"
   },
   "ticketType": {
    "type": "string",
    "description": "Ticket type"
   },
   "section": {
    "type": "string",
    "description": "Section"
   },
   "row": {
    "type": "string",
    "description": "Row"
   },
   "seat": {
    "type": "string",
    "description": "Seat"
   },
   "originalPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Original price"
   },
   "ticketStatus": {
    "type": "string",
    "description": "Ticket status"
   },
   "resaleEligibility": {
    "type": "string",
    "description": "Resale eligibility"
   },
   "chooseSellingPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Choose selling price"
   },
   "acceptRecommendedPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Accept recommended price"
   },
   "relistExpiredListing": {
    "type": "string",
    "description": "Relist expired listing"
   },
   "changePrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Change price"
   },
   "listingId": {
    "type": "string",
    "description": "Listing ID"
   },
   "ticketId": {
    "type": "string",
    "description": "Ticket ID"
   },
   "seller": {
    "type": "string",
    "description": "Seller"
   },
   "listingPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Listing price"
   },
   "fee": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Fee"
   },
   "estimatedProceeds": {
    "type": "string",
    "description": "Estimated proceeds"
   },
   "listingDate": {
    "type": "string",
    "format": "date-time",
    "description": "Listing date"
   },
   "expiration": {
    "type": "string",
    "description": "Expiration"
   },
   "sellerTermsAcceptance": {
    "type": "string",
    "description": "Seller terms acceptance"
   },
   "singleTicketListing": {
    "type": "string",
    "description": "Single ticket listing"
   },
   "multipleTicketListing": {
    "type": "string",
    "description": "Multiple ticket listing"
   },
   "adjacentSeatGroup": {
    "type": "string",
    "description": "Adjacent-seat group"
   },
   "ticketOwnership": {
    "type": "string",
    "description": "Ticket ownership"
   },
   "ticketValidity": {
    "type": "string",
    "description": "Ticket validity"
   },
   "paymentStatus": {
    "type": "string",
    "description": "Payment status"
   },
   "existingListing": {
    "type": "string",
    "description": "Existing listing"
   },
   "ticketScanStatus": {
    "type": "string",
    "description": "Ticket scan status"
   }
  }
 },
 "ListingLifecycleExpiryCancellationView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over orders state, assembled at read time from tables that already exist",
  "description": "**What Listing Lifecycle, Expiry & Cancellation displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "rejected": {
    "type": "integer",
    "description": "Rejected"
   },
   "suspended": {
    "type": "string",
    "description": "Suspended"
   },
   "withdrawn": {
    "type": "string",
    "description": "Withdrawn"
   },
   "cancelled": {
    "type": "integer",
    "description": "Cancelled"
   },
   "expired": {
    "type": "integer",
    "description": "Expired"
   },
   "xMinutesBeforeEvent": {
    "type": "string",
    "description": "X minutes before event"
   },
   "xHoursBeforeEvent": {
    "type": "string",
    "description": "X hours before event"
   },
   "atEventStart": {
    "type": "string",
    "description": "At event start"
   },
   "atConfiguredDate": {
    "type": "string",
    "format": "date-time",
    "description": "At configured date"
   },
   "atConfiguredTime": {
    "type": "string",
    "format": "date-time",
    "description": "At configured time"
   },
   "sellerCanWithdrawAnytime": {
    "type": "string",
    "description": "Seller can withdraw anytime"
   },
   "sellerCannotWithdrawWhileReserved": {
    "type": "string",
    "description": "Seller cannot withdraw while reserved"
   },
   "cancellationCutoff": {
    "type": "string",
    "description": "Cancellation cutoff"
   },
   "cancellationFee": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Cancellation fee"
   },
   "maximumWithdrawals": {
    "type": "string",
    "description": "Maximum withdrawals"
   },
   "ticketBecomesInvalid": {
    "type": "string",
    "description": "Ticket becomes invalid"
   },
   "eventIsCancelled": {
    "type": "string",
    "description": "Event is cancelled"
   },
   "eventChangesMaterially": {
    "type": "string",
    "description": "Event changes materially"
   },
   "ticketIsRefunded": {
    "type": "string",
    "description": "Ticket is refunded"
   },
   "ticketIsTransferred": {
    "type": "string",
    "description": "Ticket is transferred"
   },
   "paymentIsReversed": {
    "type": "string",
    "description": "Payment is reversed"
   },
   "eligibilityChanges": {
    "type": "string",
    "description": "Eligibility changes"
   },
   "fraudIsDetected": {
    "type": "string",
    "description": "Fraud is detected"
   },
   "requiresOperatorAction": {
    "type": "string",
    "description": "Requires operator action"
   },
   "listingApproved": {
    "type": "string",
    "description": "Listing approved"
   },
   "listingRejected": {
    "type": "string",
    "description": "Listing rejected"
   },
   "priceChanged": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Price changed"
   },
   "listingExpiring": {
    "type": "string",
    "description": "Listing expiring"
   },
   "listingExpired": {
    "type": "string",
    "description": "Listing expired"
   },
   "listingSuspended": {
    "type": "string",
    "description": "Listing suspended"
   },
   "listingWithdrawn": {
    "type": "string",
    "description": "Listing withdrawn"
   },
   "listingSold": {
    "type": "string",
    "description": "Listing sold"
   }
  }
 },
 "ResaleEligibilityRuleConfigurationInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures",
  "description": "**What Resale Eligibility Rule Configuration submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "product": {
    "type": "string",
    "description": "Product"
   },
   "ticketType": {
    "type": "string",
    "description": "Ticket type"
   },
   "event": {
    "type": "string",
    "description": "Event"
   },
   "venue": {
    "type": "string",
    "description": "Venue"
   },
   "performance": {
    "type": "string",
    "description": "Performance"
   },
   "membershipType": {
    "type": "string",
    "description": "Membership type"
   },
   "salesChannel": {
    "type": "string",
    "description": "Sales channel"
   },
   "customerSegment": {
    "type": "string",
    "description": "Customer segment"
   },
   "priceCategory": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Price category"
   },
   "promotion": {
    "type": "string",
    "description": "Promotion"
   },
   "ticketStatus": {
    "type": "string",
    "description": "Ticket status"
   },
   "paymentStatus": {
    "type": "string",
    "description": "Payment status"
   },
   "ticketOwnershipStatus": {
    "type": "string",
    "description": "Ticket ownership status"
   },
   "ticketIsFullyPaid": {
    "type": "string",
    "description": "Ticket is fully paid"
   },
   "ticketHasNotBeenScanned": {
    "type": "string",
    "description": "Ticket has not been scanned"
   },
   "ticketHasNotExpired": {
    "type": "string",
    "description": "Ticket has not expired"
   },
   "eventHasNotStarted": {
    "type": "string",
    "description": "Event has not started"
   },
   "ticketIsNotRefunded": {
    "type": "string",
    "description": "Ticket is not refunded"
   },
   "ticketIsNotComplimentary": {
    "type": "string",
    "description": "Ticket is not complimentary"
   },
   "ticketIsNotStaff": {
    "type": "string",
    "description": "Ticket is not staff"
   },
   "ticketIsNotInternal": {
    "type": "string",
    "description": "Ticket is not internal"
   },
   "ticketIsNotBlocked": {
    "type": "string",
    "description": "Ticket is not blocked"
   },
   "ticketIsNotUnderDispute": {
    "type": "string",
    "description": "Ticket is not under dispute"
   },
   "specificResaleStartEndDate": {
    "type": "string",
    "format": "date-time",
    "description": "Specific resale start/end date"
   },
   "allowResaleImmediatelyAfterPurchase": {
    "type": "boolean",
    "description": "Allow resale immediately after purchase"
   },
   "blackoutPeriod": {
    "type": "string",
    "format": "date-time",
    "description": "Blackout period"
   },
   "maximumResaleAttempts": {
    "type": "integer",
    "description": "Maximum resale attempts"
   },
   "maximumListingsPerCustomer": {
    "type": "string",
    "description": "Maximum listings per customer"
   },
   "minimumOwnershipPeriod": {
    "type": "string",
    "format": "date-time",
    "description": "Minimum ownership period"
   },
   "identityVerificationRequirement": {
    "type": "string",
    "description": "Identity verification requirement"
   },
   "originalPurchaserOnly": {
    "type": "string",
    "description": "Original purchaser only"
   },
   "membershipRestriction": {
    "type": "string",
    "description": "Membership restriction"
   }
  }
 },
 "ResaleEligibilityRuleConfigurationView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over orders state, assembled at read time from tables that already exist",
  "description": "**What Resale Eligibility Rule Configuration displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "product": {
    "type": "string",
    "description": "Product"
   },
   "ticketType": {
    "type": "string",
    "description": "Ticket type"
   },
   "event": {
    "type": "string",
    "description": "Event"
   },
   "venue": {
    "type": "string",
    "description": "Venue"
   },
   "performance": {
    "type": "string",
    "description": "Performance"
   },
   "membershipType": {
    "type": "string",
    "description": "Membership type"
   },
   "salesChannel": {
    "type": "string",
    "description": "Sales channel"
   },
   "customerSegment": {
    "type": "string",
    "description": "Customer segment"
   },
   "priceCategory": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Price category"
   },
   "promotion": {
    "type": "string",
    "description": "Promotion"
   },
   "ticketStatus": {
    "type": "string",
    "description": "Ticket status"
   },
   "paymentStatus": {
    "type": "string",
    "description": "Payment status"
   },
   "ticketOwnershipStatus": {
    "type": "string",
    "description": "Ticket ownership status"
   },
   "ticketIsFullyPaid": {
    "type": "string",
    "description": "Ticket is fully paid"
   },
   "ticketHasNotBeenScanned": {
    "type": "string",
    "description": "Ticket has not been scanned"
   },
   "ticketHasNotExpired": {
    "type": "string",
    "description": "Ticket has not expired"
   },
   "eventHasNotStarted": {
    "type": "string",
    "description": "Event has not started"
   },
   "ticketIsNotRefunded": {
    "type": "string",
    "description": "Ticket is not refunded"
   },
   "ticketIsNotComplimentary": {
    "type": "string",
    "description": "Ticket is not complimentary"
   },
   "ticketIsNotStaff": {
    "type": "string",
    "description": "Ticket is not staff"
   },
   "ticketIsNotInternal": {
    "type": "string",
    "description": "Ticket is not internal"
   },
   "ticketIsNotBlocked": {
    "type": "string",
    "description": "Ticket is not blocked"
   },
   "ticketIsNotUnderDispute": {
    "type": "string",
    "description": "Ticket is not under dispute"
   },
   "specificResaleStartEndDate": {
    "type": "string",
    "format": "date-time",
    "description": "Specific resale start/end date"
   },
   "allowResaleImmediatelyAfterPurchase": {
    "type": "boolean",
    "description": "Allow resale immediately after purchase"
   },
   "blackoutPeriod": {
    "type": "string",
    "format": "date-time",
    "description": "Blackout period"
   },
   "maximumResaleAttempts": {
    "type": "integer",
    "description": "Maximum resale attempts"
   },
   "maximumListingsPerCustomer": {
    "type": "string",
    "description": "Maximum listings per customer"
   },
   "minimumOwnershipPeriod": {
    "type": "string",
    "format": "date-time",
    "description": "Minimum ownership period"
   },
   "identityVerificationRequirement": {
    "type": "string",
    "description": "Identity verification requirement"
   },
   "originalPurchaserOnly": {
    "type": "string",
    "description": "Original purchaser only"
   },
   "membershipRestriction": {
    "type": "string",
    "description": "Membership restriction"
   }
  }
 },
 "ResaleFeesCommissionSellerProceedsView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over orders state, assembled at read time from tables that already exist",
  "description": "**What Resale Fees, Commission & Seller Proceeds displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "sellerFee": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Seller fee"
   },
   "buyerFee": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Buyer fee"
   },
   "marketplaceCommission": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Marketplace commission"
   },
   "flatTransactionFee": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Flat transaction fee"
   },
   "percentageFee": {
    "type": "number",
    "description": "Percentage fee"
   },
   "paymentProcessingFee": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Payment processing fee"
   },
   "administrativeFee": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Administrative fee"
   },
   "venueFee": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Venue fee"
   },
   "taxOnFee": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Tax on fee"
   },
   "tenant": {
    "type": "string",
    "description": "Tenant"
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
   "sellerType": {
    "type": "string",
    "description": "Seller type"
   },
   "buyerType": {
    "type": "string",
    "description": "Buyer type"
   },
   "channel": {
    "type": "string",
    "description": "Channel"
   },
   "currency": {
    "type": "string",
    "description": "Currency"
   },
   "listingPriceAed250": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Listing Price: AED 250"
   },
   "sellerProceedsAed225": {
    "type": "string",
    "description": "Seller Proceeds: AED 225"
   },
   "ticketAed250": {
    "type": "string",
    "description": "Ticket: AED 250"
   },
   "buyerServiceFeeAed12": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Buyer Service Fee: AED 12"
   },
   "totalAed262": {
    "type": "integer",
    "description": "Total: AED 262"
   }
  }
 },
 "ResaleInventoryAvailabilityManagementView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over orders state, assembled at read time from tables that already exist",
  "description": "**What Resale Inventory & Availability Management displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "event": {
    "type": "string",
    "description": "Event"
   },
   "performance": {
    "type": "string",
    "description": "Performance"
   },
   "product": {
    "type": "string",
    "description": "Product"
   },
   "section": {
    "type": "string",
    "description": "Section"
   },
   "row": {
    "type": "string",
    "description": "Row"
   },
   "seat": {
    "type": "string",
    "description": "Seat"
   },
   "price": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Price"
   },
   "listingStatus": {
    "type": "integer",
    "description": "Listing status"
   },
   "unsoldOriginalTicketInventory": {
    "type": "string",
    "description": "Unsold original ticket inventory"
   }
  }
 },
 "ResaleMarketplaceCommandCenterView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over orders state, assembled at read time from tables that already exist",
  "description": "**What Resale Marketplace Command Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "activeListings": {
    "type": "integer",
    "description": "Active Listings"
   },
   "pendingApproval": {
    "type": "integer",
    "description": "Pending Approval"
   },
   "ticketsAvailableForResale": {
    "type": "string",
    "description": "Tickets Available for Resale"
   },
   "listingsSoldToday": {
    "type": "string",
    "description": "Listings Sold Today"
   },
   "expiringListings": {
    "type": "integer",
    "description": "Expiring Listings"
   },
   "suspendedListings": {
    "type": "integer",
    "description": "Suspended Listings"
   },
   "rejectedListings": {
    "type": "integer",
    "description": "Rejected Listings"
   },
   "averageResalePrice": {
    "type": "number",
    "description": "Average Resale Price"
   },
   "grossResaleValue": {
    "type": "string",
    "description": "Gross Resale Value"
   },
   "marketplaceFees": {
    "type": "integer",
    "description": "Marketplace Fees"
   },
   "sellerProceeds": {
    "type": "integer",
    "description": "Seller Proceeds"
   },
   "conversionRate": {
    "type": "number",
    "description": "Conversion Rate"
   },
   "listingId": {
    "type": "string",
    "description": "Listing ID"
   },
   "originalOrderTicketId": {
    "type": "string",
    "description": "Original Order/Ticket ID"
   },
   "eventProduct": {
    "type": "string",
    "description": "Event/Product"
   },
   "venue": {
    "type": "string",
    "description": "Venue"
   },
   "eventDate": {
    "type": "string",
    "format": "date-time",
    "description": "Event Date"
   },
   "sectionRowSeat": {
    "type": "string",
    "description": "Section/Row/Seat"
   },
   "seller": {
    "type": "string",
    "description": "Seller"
   },
   "originalPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Original Price"
   },
   "listedPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Listed Price"
   },
   "priceVariance": {
    "type": "number",
    "description": "Price Variance %"
   },
   "marketplaceFee": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Marketplace Fee"
   },
   "listingDate": {
    "type": "string",
    "format": "date-time",
    "description": "Listing Date"
   },
   "expiry": {
    "type": "string",
    "format": "date-time",
    "description": "Expiry"
   },
   "status": {
    "type": "integer",
    "description": "Status"
   },
   "riskIndicator": {
    "type": "string",
    "description": "Risk Indicator"
   },
   "andExceptionStates": {
    "type": "string",
    "description": "and exception states"
   }
  }
 },
 "ResalePolicyMarketplaceSettingsView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over orders state, assembled at read time from tables that already exist",
  "description": "**What Resale Policy & Marketplace Settings displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "marketplaceName": {
    "type": "string",
    "description": "Marketplace name"
   },
   "marketplaceStatus": {
    "type": "string",
    "description": "Marketplace status"
   },
   "applicableOrganization": {
    "type": "string",
    "description": "Applicable organization"
   },
   "venue": {
    "type": "string",
    "description": "Venue"
   },
   "brand": {
    "type": "string",
    "description": "Brand"
   },
   "currency": {
    "type": "string",
    "description": "Currency"
   },
   "timeZone": {
    "type": "string",
    "format": "date-time",
    "description": "Time zone"
   },
   "supportedLanguage": {
    "type": "string",
    "description": "Supported language"
   },
   "marketplaceSalesChannel": {
    "type": "string",
    "description": "Marketplace sales channel"
   },
   "customerTerms": {
    "type": "string",
    "description": "Customer terms"
   },
   "sellerTerms": {
    "type": "string",
    "description": "Seller terms"
   },
   "sellerSelectsAPermittedPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Seller selects a permitted price"
   },
   "operatorDeterminesResalePrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Operator determines resale price"
   },
   "sellerVerification": {
    "type": "string",
    "description": "Seller verification"
   },
   "identityRequirements": {
    "type": "string",
    "description": "Identity requirements"
   },
   "bankPayoutInformation": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Bank/payout information"
   },
   "sellerTermsAcceptance": {
    "type": "string",
    "description": "Seller terms acceptance"
   },
   "listingConfirmation": {
    "type": "string",
    "description": "Listing confirmation"
   },
   "sellerNotifications": {
    "type": "string",
    "description": "Seller notifications"
   },
   "buyerTerms": {
    "type": "string",
    "description": "Buyer terms"
   },
   "marketplaceDisclosures": {
    "type": "string",
    "description": "Marketplace disclosures"
   },
   "resaleTicketLabeling": {
    "type": "string",
    "description": "Resale ticket labeling"
   },
   "serviceFees": {
    "type": "string",
    "description": "Service fees"
   },
   "purchaseLimits": {
    "type": "string",
    "description": "Purchase limits"
   }
  }
 },
 "ResalePricingPriceGuardrailsView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over orders state, assembled at read time from tables that already exist",
  "description": "**What Resale Pricing & Price Guardrails displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "faceValueOnly": {
    "type": "string",
    "description": "Face-value only"
   },
   "minimumResalePrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Minimum resale price"
   },
   "maximumResalePrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Maximum resale price"
   },
   "maximumMarkup": {
    "type": "number",
    "description": "Maximum markup %"
   },
   "maximumDiscount": {
    "type": "number",
    "description": "Maximum discount %"
   },
   "fixedResalePrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Fixed resale price"
   },
   "dynamicPermittedRange": {
    "type": "string",
    "description": "Dynamic permitted range"
   },
   "eventSpecificRange": {
    "type": "string",
    "description": "Event-specific range"
   },
   "productSpecificRange": {
    "type": "string",
    "description": "Product-specific range"
   },
   "sellerCanEditPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Seller can edit price"
   },
   "numberOfPriceChanges": {
    "type": "integer",
    "description": "Number of price changes"
   },
   "minimumIntervalBetweenChanges": {
    "type": "string",
    "description": "Minimum interval between changes"
   },
   "automaticPriceReduction": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Automatic price reduction"
   },
   "priceAdjustmentCutoff": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Price adjustment cutoff"
   },
   "minimumAed160": {
    "type": "string",
    "description": "Minimum: AED 160"
   },
   "maximumAed240": {
    "type": "string",
    "description": "Maximum: AED 240"
   },
   "originalFaceValue": {
    "type": "string",
    "description": "Original face value"
   },
   "originalPaidPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Original paid price"
   },
   "currentSellingPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Current selling price"
   },
   "currentDynamicPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Current dynamic price"
   },
   "eventPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Event price"
   },
   "priceCategory": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Price category"
   }
  }
 }
}
```
