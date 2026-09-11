# WS23 — B2B, Reseller & OTA Partner Management board 3

**10 screens · 10 operations · 10 schemas · 1 permissions**

Platform P10 Partner Web · ships as **ticvai-control** ·
partner audience · web ·
online only

## Who this is for

**partner on web.** Everything below is how you know what is
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

- **Every control that can be refused must be gated.** 1 permissions apply here:
  `PLATFORM_TENANT_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **0 of these operations work offline**
  
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `PTR-042` | Partner Operations Command Center | commandCentre | 1 | 0 | — |
| `PTR-043` | Partner Orders & Booking Management | listDetail | 1 | 0 | — |
| `PTR-044` | Reservations, Holds & Release Management | listDetail | 1 | 0 | — |
| `PTR-045` | Partner Cancellations, Refunds & Amendments | listDetail | 1 | 0 | — |
| `PTR-046` | Partner Statement & Account Activity | commandCentre | 1 | 0 | — |
| `PTR-047` | Partner Reconciliation & Exception Management | listDetail | 1 | 0 | — |
| `PTR-048` | Commission Calculation & Settlement Management | listDetail | 1 | 0 | — |
| `PTR-049` | Partner Disputes, Cases & Service Management | listDetail | 1 | 0 | — |
| `PTR-050` | Partner Performance Scorecard & Risk Monitoring | listDetail | 1 | 0 | — |
| `PTR-051` | Partner AI Intelligence & Relationship Optimization | listDetail | 1 | 0 | — |

## Thin screens in this batch

**PTR-044, PTR-045, PTR-047, PTR-048, PTR-050, PTR-051 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "PTR-042",
  "name": "Partner Operations Command Center",
  "module": "Partners",
  "requiresModule": "partner",
  "wave": 3,
  "source": {
   "pack": "B2B, Reseller & OTA Partner Management_Reference.pdf",
   "board": "3",
   "number": "8.3.1",
   "page": 44
  },
  "implementation": {
   "app": "partner-web",
   "route": "/partners/partner-operations-command-center-ptr-042",
   "component": "apps/partner-web/src/routes/partners/PartnerOperationsCommandCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "PTR-001"
   ],
   "exitTo": [
    "PTR-001",
    "PTR-043",
    "PTR-044",
    "PTR-045",
    "PTR-046",
    "PTR-047",
    "PTR-048",
    "PTR-049",
    "PTR-050",
    "PTR-051"
   ],
   "inferred": false,
   "notes": "**The board's hub.** The workshop specified this module as boards of ten and opened each with a command centre; the other nine screens are that board's detail, so they are reached from here and return here.",
   "transitions": [
    {
     "to": "PTR-001",
     "trigger": "Partner Login / MFA",
     "carries": [
      "accountId",
      "sessionId"
     ],
     "provenance": "derived — PTR-001 declares entryState.params accountId, sessionId, so an edge into it must carry them"
    },
    {
     "to": "PTR-043",
     "trigger": "Works in Partner Orders & Booking Management",
     "provenance": "flow F132 step 1→2",
     "operation": "listPartner2"
    },
    {
     "to": "PTR-044",
     "trigger": "Works in Reservations, Holds & Release Management",
     "provenance": "flow F132 step 3→4",
     "operation": "listPartner2"
    },
    {
     "to": "PTR-045",
     "trigger": "Works in Partner Cancellations, Refunds & Amendments",
     "provenance": "flow F132 step 5→6",
     "operation": "listPartner2"
    },
    {
     "to": "PTR-046",
     "trigger": "Works in Partner Statement & Account Activity",
     "provenance": "flow F132 step 7→8",
     "operation": "listPartner2"
    },
    {
     "to": "PTR-047",
     "trigger": "Works in Partner Reconciliation & Exception Management",
     "provenance": "flow F132 step 9→10",
     "operation": "listPartner2"
    },
    {
     "to": "PTR-048",
     "trigger": "Works in Commission Calculation & Settlement Management",
     "provenance": "flow F132 step 11→12",
     "operation": "listPartner2"
    },
    {
     "to": "PTR-049",
     "trigger": "Works in Partner Disputes, Cases & Service Management",
     "provenance": "flow F132 step 13→14",
     "operation": "listPartner2"
    },
    {
     "to": "PTR-050",
     "trigger": "Works in Partner Performance Scorecard & Risk Monitoring",
     "provenance": "flow F132 step 15→16",
     "operation": "listPartner2"
    },
    {
     "to": "PTR-051",
     "trigger": "Works in Partner AI Intelligence & Relationship Optimization",
     "provenance": "flow F132 step 17→18",
     "operation": "listPartner2"
    }
   ]
  },
  "density": "compact",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen both a metric directory (§Display) and a per-row directory (§Each partner should show) — counts over a population, then the population",
  "purpose": "Provide commercial, operations and finance teams with one real-time view of active B2B, reseller and OTA business.",
  "purposeNote": "Authorized users can understand current partner activity, financial exposure and operational exceptions from one centralized workspace.",
  "layout": {
   "template": "dashboard",
   "regions": [
    {
     "name": "contentBody",
     "slot": "filters",
     "components": [
      {
       "kind": "searchField",
       "label": "Search partner operations",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 44 §Filter by"
      },
      {
       "kind": "multiSelect",
       "label": "Filter by",
       "columns": [
        "PartnerOperationsCommandCenterView.partner",
        "PartnerOperationsCommandCenterView.partnerType",
        "Venue",
        "Event",
        "Market",
        "PartnerOperationsCommandCenterView.accountManager",
        "Channel",
        "Date",
        "PartnerOperationsCommandCenterView.operationalStatus",
        "PartnerOperationsCommandCenterView.risk"
       ],
       "notes": "The pack filters this screen by partner, partner type, venue, event, market, account manager and 4 more — which are present is a decision the pack already made.",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 44 §Filter by"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "Partner Sales Today",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 44 §Display",
       "bindsTo": "PartnerOperationsCommandCenterView.partnerSalesToday"
      },
      {
       "kind": "metricTile",
       "label": "Partner Sales MTD",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 44 §Display",
       "bindsTo": "PartnerOperationsCommandCenterView.partnerSalesMtd"
      },
      {
       "kind": "metricTile",
       "label": "Active Partner Orders",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 44 §Display",
       "bindsTo": "PartnerOperationsCommandCenterView.activePartnerOrders"
      },
      {
       "kind": "metricTile",
       "label": "Active Reservations/Holds",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 44 §Display"
      },
      {
       "kind": "metricTile",
       "label": "Tickets Sold",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 44 §Display",
       "bindsTo": "PartnerOperationsCommandCenterView.ticketsSold"
      },
      {
       "kind": "metricTile",
       "label": "Cancellations",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 44 §Display",
       "bindsTo": "PartnerOperationsCommandCenterView.cancellations"
      },
      {
       "kind": "metricTile",
       "label": "Refunds",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 44 §Display",
       "bindsTo": "PartnerOperationsCommandCenterView.refunds"
      },
      {
       "kind": "metricTile",
       "label": "Outstanding Receivables",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 44 §Display",
       "bindsTo": "PartnerOperationsCommandCenterView.outstandingReceivables"
      },
      {
       "kind": "metricTile",
       "label": "Commission Payable",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 44 §Display",
       "bindsTo": "PartnerOperationsCommandCenterView.commissionPayable"
      },
      {
       "kind": "metricTile",
       "label": "Pending Settlements",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 44 §Display",
       "bindsTo": "PartnerOperationsCommandCenterView.pendingSettlements"
      },
      {
       "kind": "metricTile",
       "label": "Operational Exceptions",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 44 §Display",
       "bindsTo": "PartnerOperationsCommandCenterView.operationalExceptions"
      },
      {
       "kind": "metricTile",
       "label": "Partners Requiring Attention",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 44 §Display",
       "bindsTo": "PartnerOperationsCommandCenterView.partnersRequiringAttention"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "moduleTiles",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every partner operations",
       "columns": [
        "PartnerOperationsCommandCenterView.partner",
        "PartnerOperationsCommandCenterView.partnerType",
        "PartnerOperationsCommandCenterView.accountManager",
        "PartnerOperationsCommandCenterView.orders",
        "PartnerOperationsCommandCenterView.tickets",
        "PartnerOperationsCommandCenterView.grossSales",
        "PartnerOperationsCommandCenterView.netSales",
        "PartnerOperationsCommandCenterView.commission",
        "PartnerOperationsCommandCenterView.outstandingBalance",
        "PartnerOperationsCommandCenterView.creditUtilization",
        "PartnerOperationsCommandCenterView.allocationUtilization",
        "PartnerOperationsCommandCenterView.cancellationRate",
        "PartnerOperationsCommandCenterView.operationalStatus",
        "PartnerOperationsCommandCenterView.risk"
       ],
       "bindsTo": "PartnerOperationsCommandCenterView",
       "operation": "listPartner2",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 44 §Each partner should show"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected partner operations",
       "bindsTo": "PartnerOperationsCommandCenterView",
       "columns": [
        "PartnerOperationsCommandCenterView.partner",
        "PartnerOperationsCommandCenterView.partnerType",
        "PartnerOperationsCommandCenterView.accountManager",
        "PartnerOperationsCommandCenterView.orders",
        "PartnerOperationsCommandCenterView.tickets",
        "PartnerOperationsCommandCenterView.grossSales",
        "PartnerOperationsCommandCenterView.netSales",
        "PartnerOperationsCommandCenterView.commission",
        "PartnerOperationsCommandCenterView.outstandingBalance",
        "PartnerOperationsCommandCenterView.creditUtilization",
        "PartnerOperationsCommandCenterView.allocationUtilization",
        "PartnerOperationsCommandCenterView.cancellationRate",
        "PartnerOperationsCommandCenterView.operationalStatus",
        "PartnerOperationsCommandCenterView.risk"
       ],
       "notes": null,
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 44 §Each partner should show"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The partner operations list; the counts above it resolve separately.",
   "error": "Could not load. Names which read failed and leaves the partner operations untouched.",
   "emptyFirstRun": "No partner operations yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the partner operations are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listPartner2",
    "contract": "subscription",
    "purpose": "Partner Operations Command Center",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P10 Partner Web.dc.html#ptr-042"
  },
  "apisNote": "Regenerated 9 September 2026 from B2B, Reseller & OTA Partner Management_Reference.pdf page 44. 30 of 35 labels bound to a contract property; 36 of 47 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "_platform": {
   "code": "P10",
   "audience": "partner",
   "formFactor": "web",
   "shortName": "Partner Web",
   "name": "Partner Web — Reseller Portal",
   "offlineCapable": false,
   "app": "partner-web",
   "operator": "partner",
   "targetApp": {
    "app": "ticvai-control",
    "name": "TICVAI Control",
    "shell": "web",
    "siblings": [
     "P09",
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
  "id": "PTR-043",
  "name": "Partner Orders & Booking Management",
  "module": "Partners",
  "requiresModule": "partner",
  "wave": 3,
  "source": {
   "pack": "B2B, Reseller & OTA Partner Management_Reference.pdf",
   "board": "3",
   "number": "8.3.2",
   "page": 46
  },
  "implementation": {
   "app": "partner-web",
   "route": "/partners/partner-orders-booking-management-ptr-043",
   "component": "apps/partner-web/src/routes/partners/PartnerOrdersBookingManagement.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "PTR-042"
   ],
   "exitTo": [
    "PTR-042"
   ],
   "inferred": false,
   "notes": "**Reached from PTR-042, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "PTR-042",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F132 step 2→3",
     "operation": "listPartnerOrderBooking"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Provide a consolidated operational view of orders created by each partner.",
  "purposeNote": "Operations can locate and service any partner transaction while preserving central order and commercial-rule integrity.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "filters",
     "components": [
      {
       "kind": "searchField",
       "label": "Search partner orders booking",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 46 §Search/filter by"
      },
      {
       "kind": "multiSelect",
       "label": "Filter by",
       "columns": [
        "Partner",
        "Partner Order Reference",
        "TICVAI Order ID",
        "Event",
        "Venue",
        "Product",
        "Booking Date",
        "Visit/Event Date",
        "Status",
        "Agent",
        "Channel"
       ],
       "notes": "The pack filters this screen by partner, partner order reference, ticvai order id, event, venue, product and 5 more — which are present is a decision the pack already made.",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 46 §Search/filter by"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every partner orders booking",
       "columns": [
        "TICVAI Order ID",
        "PartnerOrdersBookingManagementView.partnerReference",
        "Partner",
        "PartnerOrdersBookingManagementView.agentUser",
        "PartnerOrdersBookingManagementView.customerGuestWhereApplicable",
        "Booking Date",
        "Event",
        "PartnerOrdersBookingManagementView.products",
        "PartnerOrdersBookingManagementView.quantity",
        "PartnerOrdersBookingManagementView.grossValue",
        "PartnerOrdersBookingManagementView.partnerRate",
        "PartnerOrdersBookingManagementView.commission",
        "PartnerOrdersBookingManagementView.netAmount",
        "PartnerOrdersBookingManagementView.paymentMethod",
        "PartnerOrdersBookingManagementView.billingStatus",
        "PartnerOrdersBookingManagementView.fulfillmentStatus"
       ],
       "bindsTo": "PartnerOrdersBookingManagementView",
       "operation": "listPartnerOrderBooking",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 46 §Display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected partner orders booking",
       "bindsTo": "PartnerOrdersBookingManagementView",
       "columns": [
        "TICVAI Order ID",
        "PartnerOrdersBookingManagementView.partnerReference",
        "Partner",
        "PartnerOrdersBookingManagementView.agentUser",
        "PartnerOrdersBookingManagementView.customerGuestWhereApplicable",
        "Booking Date",
        "Event",
        "PartnerOrdersBookingManagementView.products",
        "PartnerOrdersBookingManagementView.quantity",
        "PartnerOrdersBookingManagementView.grossValue",
        "PartnerOrdersBookingManagementView.partnerRate",
        "PartnerOrdersBookingManagementView.commission",
        "PartnerOrdersBookingManagementView.netAmount",
        "PartnerOrdersBookingManagementView.paymentMethod",
        "PartnerOrdersBookingManagementView.billingStatus",
        "PartnerOrdersBookingManagementView.fulfillmentStatus"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Important Architecture”.",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 46 §Display"
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
       "notes": "**The pack separates these permissions and no action on the screen claims them yet:** View, Modify, Cancel, Rebook, Resend Tickets, Reissue, Add Internal Note, Escalate, Open Financial Record. Each needs attaching to the control it gates, or the screen needs the control.",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 46 §Subject to permission"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The partner orders booking list.",
   "error": "Could not load. Names which read failed and leaves the partner orders booking untouched.",
   "emptyFirstRun": "No partner orders booking yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the partner orders booking are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listPartnerOrderBooking",
    "contract": "subscription",
    "purpose": "Partner Orders & Booking Management",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "TICVAI Order ID",
    "PartnerOrdersBookingManagementView.partnerReference",
    "Partner",
    "PartnerOrdersBookingManagementView.agentUser",
    "PartnerOrdersBookingManagementView.customerGuestWhereApplicable",
    "Booking Date"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P10 Partner Web.dc.html#ptr-043"
  },
  "apisNote": "Regenerated 9 September 2026 from B2B, Reseller & OTA Partner Management_Reference.pdf page 46. 12 of 27 labels bound to a contract property; 36 of 50 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "_platform": {
   "code": "P10",
   "audience": "partner",
   "formFactor": "web",
   "shortName": "Partner Web",
   "name": "Partner Web — Reseller Portal",
   "offlineCapable": false,
   "app": "partner-web",
   "operator": "partner",
   "targetApp": {
    "app": "ticvai-control",
    "name": "TICVAI Control",
    "shell": "web",
    "siblings": [
     "P09",
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
  "id": "PTR-044",
  "name": "Reservations, Holds & Release Management",
  "module": "Partners",
  "requiresModule": "partner",
  "wave": 3,
  "source": {
   "pack": "B2B, Reseller & OTA Partner Management_Reference.pdf",
   "board": "3",
   "number": "8.3.3",
   "page": 48
  },
  "implementation": {
   "app": "partner-web",
   "route": "/partners/reservations-holds-release-management-ptr-044",
   "component": "apps/partner-web/src/routes/partners/ReservationsHoldsReleaseManagement.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "PTR-042"
   ],
   "exitTo": [
    "PTR-042"
   ],
   "inferred": false,
   "notes": "**Reached from PTR-042, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "PTR-042",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F132 step 4→5",
     "operation": "listReservationHoldRelease"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Manage inventory temporarily reserved by B2B partners before final confirmation. This is particularly important for tour operators, corporate groups and travel-trade partners.",
  "purposeNote": "Partner reservations and holds cannot indefinitely block sellable capacity and are automatically governed by configured duration, allocation and approval rules.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every reservations holds release",
       "columns": [
        "ReservationsHoldsReleaseManagementView.activeHolds",
        "ReservationsHoldsReleaseManagementView.heldTickets",
        "ReservationsHoldsReleaseManagementView.heldValue",
        "ReservationsHoldsReleaseManagementView.expiringToday",
        "ReservationsHoldsReleaseManagementView.expiredHolds",
        "ReservationsHoldsReleaseManagementView.convertedHolds",
        "ReservationsHoldsReleaseManagementView.releasedInventory"
       ],
       "bindsTo": "ReservationsHoldsReleaseManagementView",
       "operation": "listReservationHoldRelease",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 48 §Display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected reservations holds release",
       "bindsTo": "ReservationsHoldsReleaseManagementView",
       "columns": [
        "ReservationsHoldsReleaseManagementView.activeHolds",
        "ReservationsHoldsReleaseManagementView.heldTickets",
        "ReservationsHoldsReleaseManagementView.heldValue",
        "ReservationsHoldsReleaseManagementView.expiringToday",
        "ReservationsHoldsReleaseManagementView.expiredHolds",
        "ReservationsHoldsReleaseManagementView.convertedHolds",
        "ReservationsHoldsReleaseManagementView.releasedInventory"
       ],
       "notes": "The pack groups this record's detail under its own headings: “When a hold expires”.",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 48 §Display"
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
       "notes": "**The pack separates these permissions and no action on the screen claims them yet:** Extend Hold, Reduce Hold, Release Hold, Convert to Booking, Reassign where permitted, Escalate. Each needs attaching to the control it gates, or the screen needs the control.",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 48 §Authorized users can"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The reservations holds release list.",
   "error": "Could not load. Names which read failed and leaves the reservations holds release untouched.",
   "emptyFirstRun": "No reservations holds release yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the reservations holds release are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listReservationHoldRelease",
    "contract": "subscription",
    "purpose": "Reservations, Holds & Release Management",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "ReservationsHoldsReleaseManagementView.activeHolds",
    "ReservationsHoldsReleaseManagementView.heldTickets",
    "ReservationsHoldsReleaseManagementView.heldValue",
    "ReservationsHoldsReleaseManagementView.expiringToday",
    "ReservationsHoldsReleaseManagementView.expiredHolds",
    "ReservationsHoldsReleaseManagementView.convertedHolds"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P10 Partner Web.dc.html#ptr-044"
  },
  "apisNote": "Regenerated 9 September 2026 from B2B, Reseller & OTA Partner Management_Reference.pdf page 48. 7 of 7 labels bound to a contract property; 25 of 41 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "_platform": {
   "code": "P10",
   "audience": "partner",
   "formFactor": "web",
   "shortName": "Partner Web",
   "name": "Partner Web — Reseller Portal",
   "offlineCapable": false,
   "app": "partner-web",
   "operator": "partner",
   "targetApp": {
    "app": "ticvai-control",
    "name": "TICVAI Control",
    "shell": "web",
    "siblings": [
     "P09",
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
  "id": "PTR-045",
  "name": "Partner Cancellations, Refunds & Amendments",
  "module": "Partners",
  "requiresModule": "partner",
  "wave": 3,
  "source": {
   "pack": "B2B, Reseller & OTA Partner Management_Reference.pdf",
   "board": "3",
   "number": "8.3.4",
   "page": 49
  },
  "implementation": {
   "app": "partner-web",
   "route": "/partners/partner-cancellations-refunds-amendments-ptr-045",
   "component": "apps/partner-web/src/routes/partners/PartnerCancellationsRefundsAmendments.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "PTR-042"
   ],
   "exitTo": [
    "PTR-042"
   ],
   "inferred": false,
   "notes": "**Reached from PTR-042, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "PTR-042",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F132 step 6→7",
     "operation": "listPartnerCancellationRefund"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Manage post-booking changes according to the partner's commercial agreement and product policies.",
  "purposeNote": "Partner booking changes are processed according to applicable commercial and product policies with complete financial and inventory impact visibility.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 49"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 49"
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
       "impliedBy": "listPartnerCancellationRefund",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The partner cancellations refunds list.",
   "error": "Could not load. Names which read failed and leaves the partner cancellations refunds untouched.",
   "emptyFirstRun": "No partner cancellations refunds yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the partner cancellations refunds are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listPartnerCancellationRefund",
    "contract": "subscription",
    "purpose": "Partner Cancellations, Refunds & Amendments",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "PartnerCancellationsRefundsAmendmentsView.fullCancellation",
    "PartnerCancellationsRefundsAmendmentsView.partialCancellation",
    "PartnerCancellationsRefundsAmendmentsView.dateChange",
    "PartnerCancellationsRefundsAmendmentsView.performanceChange",
    "PartnerCancellationsRefundsAmendmentsView.quantityReduction"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P10 Partner Web.dc.html#ptr-045"
  },
  "apisNote": "Regenerated 9 September 2026 from B2B, Reseller & OTA Partner Management_Reference.pdf page 49. 0 of 0 labels bound to a contract property; 0 of 34 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "_platform": {
   "code": "P10",
   "audience": "partner",
   "formFactor": "web",
   "shortName": "Partner Web",
   "name": "Partner Web — Reseller Portal",
   "offlineCapable": false,
   "app": "partner-web",
   "operator": "partner",
   "targetApp": {
    "app": "ticvai-control",
    "name": "TICVAI Control",
    "shell": "web",
    "siblings": [
     "P09",
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
  "id": "PTR-046",
  "name": "Partner Statement & Account Activity",
  "module": "Partners",
  "requiresModule": "partner",
  "wave": 3,
  "source": {
   "pack": "B2B, Reseller & OTA Partner Management_Reference.pdf",
   "board": "3",
   "number": "8.3.5",
   "page": 51
  },
  "implementation": {
   "app": "partner-web",
   "route": "/partners/partner-statement-account-activity-ptr-046",
   "component": "apps/partner-web/src/routes/partners/PartnerStatementAccountActivity.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "PTR-042"
   ],
   "exitTo": [
    "PTR-042"
   ],
   "inferred": false,
   "notes": "**Reached from PTR-042, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "PTR-042",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F132 step 8→9",
     "operation": "listPartnerStatementAccount"
    }
   ]
  },
  "density": "compact",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen both a metric directory (§Display) and a per-row directory (§Each line should show) — counts over a population, then the population",
  "purpose": "Give finance and commercial teams a complete financial statement for each partner account.",
  "purposeNote": "Finance and authorized partner users can reconcile all commercial account activity against a clear running balance and supporting transaction references.",
  "layout": {
   "template": "dashboard",
   "regions": [
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "Opening Balance",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 51 §Display",
       "bindsTo": "PartnerStatementAccountActivityView.openingBalance"
      },
      {
       "kind": "metricTile",
       "label": "Sales",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 51 §Display",
       "bindsTo": "PartnerStatementAccountActivityView.sales"
      },
      {
       "kind": "metricTile",
       "label": "Payments",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 51 §Display",
       "bindsTo": "PartnerStatementAccountActivityView.payments"
      },
      {
       "kind": "metricTile",
       "label": "Credits",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 51 §Display",
       "bindsTo": "PartnerStatementAccountActivityView.credits"
      },
      {
       "kind": "metricTile",
       "label": "Refunds",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 51 §Display",
       "bindsTo": "PartnerStatementAccountActivityView.refunds"
      },
      {
       "kind": "metricTile",
       "label": "Commission",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 51 §Display",
       "bindsTo": "PartnerStatementAccountActivityView.commission"
      },
      {
       "kind": "metricTile",
       "label": "Adjustments",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 51 §Display",
       "bindsTo": "PartnerStatementAccountActivityView.adjustments"
      },
      {
       "kind": "metricTile",
       "label": "Closing Balance",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 51 §Display",
       "bindsTo": "PartnerStatementAccountActivityView.closingBalance"
      },
      {
       "kind": "metricTile",
       "label": "Overdue Balance",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 51 §Display",
       "bindsTo": "PartnerStatementAccountActivityView.overdueBalance"
      },
      {
       "kind": "metricTile",
       "label": "Available Credit",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 51 §Display",
       "bindsTo": "PartnerStatementAccountActivityView.availableCredit"
      },
      {
       "kind": "metricTile",
       "label": "Current",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 51 §Display",
       "bindsTo": "PartnerStatementAccountActivityView.current"
      },
      {
       "kind": "metricTile",
       "label": "1–30 Days",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 51 §Display"
      },
      {
       "kind": "metricTile",
       "label": "31–60 Days",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 51 §Display"
      },
      {
       "kind": "metricTile",
       "label": "61–90 Days",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 51 §Display"
      },
      {
       "kind": "metricTile",
       "label": "90+ Days",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 51 §Display"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "moduleTiles",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every partner statement account",
       "columns": [
        "PartnerStatementAccountActivityView.date",
        "PartnerStatementAccountActivityView.transactionType",
        "PartnerStatementAccountActivityView.reference",
        "PartnerStatementAccountActivityView.orderInvoice",
        "PartnerStatementAccountActivityView.debit",
        "PartnerStatementAccountActivityView.credit",
        "PartnerStatementAccountActivityView.runningBalance",
        "PartnerStatementAccountActivityView.dueDate",
        "PartnerStatementAccountActivityView.status"
       ],
       "bindsTo": "PartnerStatementAccountActivityView",
       "operation": "listPartnerStatementAccount",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 51 §Each line should show"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected partner statement account",
       "bindsTo": "PartnerStatementAccountActivityView",
       "columns": [
        "PartnerStatementAccountActivityView.date",
        "PartnerStatementAccountActivityView.transactionType",
        "PartnerStatementAccountActivityView.reference",
        "PartnerStatementAccountActivityView.orderInvoice",
        "PartnerStatementAccountActivityView.debit",
        "PartnerStatementAccountActivityView.credit",
        "PartnerStatementAccountActivityView.runningBalance",
        "PartnerStatementAccountActivityView.dueDate",
        "PartnerStatementAccountActivityView.status"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Generate by”, “Partner Access”, “Architecture”.",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 51 §Each line should show"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The partner statement account list; the counts above it resolve separately.",
   "error": "Could not load. Names which read failed and leaves the partner statement account untouched.",
   "emptyFirstRun": "No partner statement account yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the partner statement account are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listPartnerStatementAccount",
    "contract": "subscription",
    "purpose": "Partner Statement & Account Activity",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P10 Partner Web.dc.html#ptr-046"
  },
  "apisNote": "Regenerated 9 September 2026 from B2B, Reseller & OTA Partner Management_Reference.pdf page 51. 20 of 20 labels bound to a contract property; 24 of 43 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "_platform": {
   "code": "P10",
   "audience": "partner",
   "formFactor": "web",
   "shortName": "Partner Web",
   "name": "Partner Web — Reseller Portal",
   "offlineCapable": false,
   "app": "partner-web",
   "operator": "partner",
   "targetApp": {
    "app": "ticvai-control",
    "name": "TICVAI Control",
    "shell": "web",
    "siblings": [
     "P09",
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
  "id": "PTR-047",
  "name": "Partner Reconciliation & Exception Management",
  "module": "Partners",
  "requiresModule": "partner",
  "wave": 3,
  "source": {
   "pack": "B2B, Reseller & OTA Partner Management_Reference.pdf",
   "board": "3",
   "number": "8.3.6",
   "page": 52
  },
  "implementation": {
   "app": "partner-web",
   "route": "/partners/partner-reconciliation-exception-management-ptr-047",
   "component": "apps/partner-web/src/routes/partners/PartnerReconciliationExceptionManagement.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "PTR-042"
   ],
   "exitTo": [
    "PTR-042"
   ],
   "inferred": false,
   "notes": "**Reached from PTR-042, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "PTR-042",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F132 step 10→11",
     "operation": "listPartnerReconciliationException"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Reconcile operational bookings against financial and channel records and identify discrepancies.",
  "purposeNote": "Partner operational and financial records can be reconciled systematically, with every unresolved difference tracked through resolution.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every partner reconciliation exception",
       "columns": [
        "PartnerReconciliationExceptionManagementView.recordsReconciled",
        "PartnerReconciliationExceptionManagementView.unmatchedOrders",
        "PartnerReconciliationExceptionManagementView.amountMismatches",
        "PartnerReconciliationExceptionManagementView.missingTickets",
        "PartnerReconciliationExceptionManagementView.pricingDifferences",
        "PartnerReconciliationExceptionManagementView.commissionDifferences",
        "PartnerReconciliationExceptionManagementView.paymentDifferences",
        "PartnerReconciliationExceptionManagementView.pendingInvestigation"
       ],
       "bindsTo": "PartnerReconciliationExceptionManagementView",
       "operation": "listPartnerReconciliationException",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 52 §Display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected partner reconciliation exception",
       "bindsTo": "PartnerReconciliationExceptionManagementView",
       "columns": [
        "PartnerReconciliationExceptionManagementView.recordsReconciled",
        "PartnerReconciliationExceptionManagementView.unmatchedOrders",
        "PartnerReconciliationExceptionManagementView.amountMismatches",
        "PartnerReconciliationExceptionManagementView.missingTickets",
        "PartnerReconciliationExceptionManagementView.pricingDifferences",
        "PartnerReconciliationExceptionManagementView.commissionDifferences",
        "PartnerReconciliationExceptionManagementView.paymentDifferences",
        "PartnerReconciliationExceptionManagementView.pendingInvestigation"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Partner Orders”, “Partner Reference OTA-82714”, “Exception Types”.",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 52 §Display"
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
       "notes": "**The pack separates these permissions and no action on the screen claims them yet:** Match, Correct, Accept Difference, Create Adjustment, Assign, Escalate, Dispute. Each needs attaching to the control it gates, or the screen needs the control.",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 52 §Authorized users can"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The partner reconciliation exception list.",
   "error": "Could not load. Names which read failed and leaves the partner reconciliation exception untouched.",
   "emptyFirstRun": "No partner reconciliation exception yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the partner reconciliation exception are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listPartnerReconciliationException",
    "contract": "subscription",
    "purpose": "Partner Reconciliation & Exception Management",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "PartnerReconciliationExceptionManagementView.recordsReconciled",
    "PartnerReconciliationExceptionManagementView.unmatchedOrders",
    "PartnerReconciliationExceptionManagementView.amountMismatches",
    "PartnerReconciliationExceptionManagementView.missingTickets",
    "PartnerReconciliationExceptionManagementView.pricingDifferences",
    "PartnerReconciliationExceptionManagementView.commissionDifferences"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P10 Partner Web.dc.html#ptr-047"
  },
  "apisNote": "Regenerated 9 September 2026 from B2B, Reseller & OTA Partner Management_Reference.pdf page 52. 8 of 8 labels bound to a contract property; 15 of 39 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "_platform": {
   "code": "P10",
   "audience": "partner",
   "formFactor": "web",
   "shortName": "Partner Web",
   "name": "Partner Web — Reseller Portal",
   "offlineCapable": false,
   "app": "partner-web",
   "operator": "partner",
   "targetApp": {
    "app": "ticvai-control",
    "name": "TICVAI Control",
    "shell": "web",
    "siblings": [
     "P09",
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
  "id": "PTR-048",
  "name": "Commission Calculation & Settlement Management",
  "module": "Partners",
  "requiresModule": "partner",
  "wave": 3,
  "source": {
   "pack": "B2B, Reseller & OTA Partner Management_Reference.pdf",
   "board": "3",
   "number": "8.3.7",
   "page": 54
  },
  "implementation": {
   "app": "partner-web",
   "route": "/partners/commission-calculation-settlement-management-ptr-048",
   "component": "apps/partner-web/src/routes/partners/CommissionCalculationSettlementManagement.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "PTR-042"
   ],
   "exitTo": [
    "PTR-042"
   ],
   "inferred": false,
   "notes": "**Reached from PTR-042, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "PTR-042",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F132 step 12→13",
     "operation": "listCommissionCalculationSettlement"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Calculate, approve and settle commission or incentive amounts owed under partner commercial agreements.",
  "purposeNote": "until relevant transactions and adjustments have been reconciled.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every commission calculation settlement",
       "columns": [
        "CommissionCalculationSettlementManagementView.commissionEarned",
        "CommissionCalculationSettlementManagementView.commissionPending",
        "CommissionCalculationSettlementManagementView.approved",
        "CommissionCalculationSettlementManagementView.onHold",
        "CommissionCalculationSettlementManagementView.paid",
        "CommissionCalculationSettlementManagementView.reversed",
        "CommissionCalculationSettlementManagementView.incentivesEarned",
        "CommissionCalculationSettlementManagementView.nextSettlement"
       ],
       "bindsTo": "CommissionCalculationSettlementManagementView",
       "operation": "listCommissionCalculationSettlement",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 54 §Display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected commission calculation settlement",
       "bindsTo": "CommissionCalculationSettlementManagementView",
       "columns": [
        "CommissionCalculationSettlementManagementView.commissionEarned",
        "CommissionCalculationSettlementManagementView.commissionPending",
        "CommissionCalculationSettlementManagementView.approved",
        "CommissionCalculationSettlementManagementView.onHold",
        "CommissionCalculationSettlementManagementView.paid",
        "CommissionCalculationSettlementManagementView.reversed",
        "CommissionCalculationSettlementManagementView.incentivesEarned",
        "CommissionCalculationSettlementManagementView.nextSettlement"
       ],
       "notes": "The pack groups this record's detail under its own headings: “For each transaction”, “Automatically account for”, “Exception states”, “Settlement Batch”, “Important Boundary”.",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 54 §Display"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The commission calculation settlement list.",
   "error": "Could not load. Names which read failed and leaves the commission calculation settlement untouched.",
   "emptyFirstRun": "No commission calculation settlement yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the commission calculation settlement are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listCommissionCalculationSettlement",
    "contract": "subscription",
    "purpose": "Commission Calculation & Settlement Management",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "CommissionCalculationSettlementManagementView.commissionEarned",
    "CommissionCalculationSettlementManagementView.commissionPending",
    "CommissionCalculationSettlementManagementView.approved",
    "CommissionCalculationSettlementManagementView.onHold",
    "CommissionCalculationSettlementManagementView.paid",
    "CommissionCalculationSettlementManagementView.reversed"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P10 Partner Web.dc.html#ptr-048"
  },
  "apisNote": "Regenerated 9 September 2026 from B2B, Reseller & OTA Partner Management_Reference.pdf page 54. 8 of 8 labels bound to a contract property; 8 of 42 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "_platform": {
   "code": "P10",
   "audience": "partner",
   "formFactor": "web",
   "shortName": "Partner Web",
   "name": "Partner Web — Reseller Portal",
   "offlineCapable": false,
   "app": "partner-web",
   "operator": "partner",
   "targetApp": {
    "app": "ticvai-control",
    "name": "TICVAI Control",
    "shell": "web",
    "siblings": [
     "P09",
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
  "id": "PTR-049",
  "name": "Partner Disputes, Cases & Service Management",
  "module": "Partners",
  "requiresModule": "partner",
  "wave": 3,
  "source": {
   "pack": "B2B, Reseller & OTA Partner Management_Reference.pdf",
   "board": "3",
   "number": "8.3.8",
   "page": 56
  },
  "implementation": {
   "app": "partner-web",
   "route": "/partners/partner-disputes-cases-service-management-ptr-049",
   "component": "apps/partner-web/src/routes/partners/PartnerDisputesCasesServiceManagement.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "PTR-042"
   ],
   "exitTo": [
    "PTR-042"
   ],
   "inferred": false,
   "notes": "**Reached from PTR-042, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "PTR-042",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F132 step 14→15",
     "operation": "listPartnerDisputeCase"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Monitor) and no metric row",
  "purpose": "Provide a structured case-management environment for partner operational and commercial disputes.",
  "purposeNote": "Every partner dispute has a traceable owner, SLA, supporting evidence, financial context and documented resolution.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 6 actions on this screen and the screen declares 1 operation.** Unserved: Booking Dispute, Pricing Dispute, Ticket Issue, Allocation Issue, Finance review, Technical review. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 56 §Support"
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
       "label": "Every partner disputes cases",
       "columns": [
        "PartnerDisputesCasesServiceManagementView.firstResponse",
        "PartnerDisputesCasesServiceManagementView.resolutionTarget",
        "PartnerDisputesCasesServiceManagementView.timeOpen",
        "PartnerDisputesCasesServiceManagementView.slaBreach"
       ],
       "bindsTo": "PartnerDisputesCasesServiceManagementView",
       "operation": "listPartnerDisputeCase",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 56 §Monitor"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected partner disputes cases",
       "bindsTo": "PartnerDisputesCasesServiceManagementView",
       "columns": [
        "PartnerDisputesCasesServiceManagementView.firstResponse",
        "PartnerDisputesCasesServiceManagementView.resolutionTarget",
        "PartnerDisputesCasesServiceManagementView.timeOpen",
        "PartnerDisputesCasesServiceManagementView.slaBreach"
       ],
       "notes": null,
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 56 §Monitor"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Booking Dispute",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 56 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Pricing Dispute",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 56 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Ticket Issue",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 56 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Allocation Issue",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 56 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Finance review",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 56 §Allow"
      },
      {
       "kind": "secondaryButton",
       "label": "Technical review",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 56 §Allow"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The partner disputes cases list.",
   "error": "Could not load. Names which read failed and leaves the partner disputes cases untouched.",
   "emptyFirstRun": "No partner disputes cases yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the partner disputes cases are still there. The pack's own statuses are Proposed → Resolved → Closed — the state names which is selected.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listPartnerDisputeCase",
    "contract": "subscription",
    "purpose": "Partner Disputes, Cases & Service Management",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "PartnerDisputesCasesServiceManagementView.firstResponse",
    "PartnerDisputesCasesServiceManagementView.resolutionTarget",
    "PartnerDisputesCasesServiceManagementView.timeOpen",
    "PartnerDisputesCasesServiceManagementView.slaBreach"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P10 Partner Web.dc.html#ptr-049"
  },
  "apisNote": "Regenerated 9 September 2026 from B2B, Reseller & OTA Partner Management_Reference.pdf page 56. 4 of 4 labels bound to a contract property; 25 of 45 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "_platform": {
   "code": "P10",
   "audience": "partner",
   "formFactor": "web",
   "shortName": "Partner Web",
   "name": "Partner Web — Reseller Portal",
   "offlineCapable": false,
   "app": "partner-web",
   "operator": "partner",
   "targetApp": {
    "app": "ticvai-control",
    "name": "TICVAI Control",
    "shell": "web",
    "siblings": [
     "P09",
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
  "id": "PTR-050",
  "name": "Partner Performance Scorecard & Risk Monitoring",
  "module": "Partners",
  "requiresModule": "partner",
  "wave": 3,
  "source": {
   "pack": "B2B, Reseller & OTA Partner Management_Reference.pdf",
   "board": "3",
   "number": "8.3.9",
   "page": 57
  },
  "implementation": {
   "app": "partner-web",
   "route": "/partners/partner-performance-scorecard-risk-monitoring-ptr-050",
   "component": "apps/partner-web/src/routes/partners/PartnerPerformanceScorecardRiskMonitoring.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "PTR-042"
   ],
   "exitTo": [
    "PTR-042"
   ],
   "inferred": false,
   "notes": "**Reached from PTR-042, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "PTR-042",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F132 step 16→17",
     "operation": "listPartnerPerformanceScorecard"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Show) and no metric row",
  "purpose": "Create a consistent scorecard for evaluating the quality and commercial value of every partner relationship.",
  "purposeNote": "Management can objectively compare partners and identify commercial, operational or financial deterioration before it becomes a material issue.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every partner performance scorecard",
       "columns": [
        "PartnerPerformanceScorecardRiskMonitoringView.improving",
        "PartnerPerformanceScorecardRiskMonitoringView.stable",
        "PartnerPerformanceScorecardRiskMonitoringView.declining"
       ],
       "bindsTo": "PartnerPerformanceScorecardRiskMonitoringView",
       "operation": "listPartnerPerformanceScorecard",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 57 §Show"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected partner performance scorecard",
       "bindsTo": "PartnerPerformanceScorecardRiskMonitoringView",
       "columns": [
        "PartnerPerformanceScorecardRiskMonitoringView.improving",
        "PartnerPerformanceScorecardRiskMonitoringView.stable",
        "PartnerPerformanceScorecardRiskMonitoringView.declining"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Commercial”, “Allocation”, “Financial”, “Operational”, “Technical”, “Compliance”.",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 57 §Show"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The partner performance scorecard list.",
   "error": "Could not load. Names which read failed and leaves the partner performance scorecard untouched.",
   "emptyFirstRun": "No partner performance scorecard yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the partner performance scorecard are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listPartnerPerformanceScorecard",
    "contract": "subscription",
    "purpose": "Partner Performance Scorecard & Risk Monitoring",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "PartnerPerformanceScorecardRiskMonitoringView.improving",
    "PartnerPerformanceScorecardRiskMonitoringView.stable",
    "PartnerPerformanceScorecardRiskMonitoringView.declining"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P10 Partner Web.dc.html#ptr-050"
  },
  "apisNote": "Regenerated 9 September 2026 from B2B, Reseller & OTA Partner Management_Reference.pdf page 57. 3 of 3 labels bound to a contract property; 3 of 42 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "_platform": {
   "code": "P10",
   "audience": "partner",
   "formFactor": "web",
   "shortName": "Partner Web",
   "name": "Partner Web — Reseller Portal",
   "offlineCapable": false,
   "app": "partner-web",
   "operator": "partner",
   "targetApp": {
    "app": "ticvai-control",
    "name": "TICVAI Control",
    "shell": "web",
    "siblings": [
     "P09",
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
  "id": "PTR-051",
  "name": "Partner AI Intelligence & Relationship Optimization",
  "module": "Partners",
  "requiresModule": "partner",
  "wave": 3,
  "source": {
   "pack": "B2B, Reseller & OTA Partner Management_Reference.pdf",
   "board": "3",
   "number": "8.3.10",
   "page": 59
  },
  "implementation": {
   "app": "partner-web",
   "route": "/partners/partner-ai-intelligence-relationship-optimization-ptr-051",
   "component": "apps/partner-web/src/routes/partners/PartnerAiIntelligenceRelationshipOptimization.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "PTR-042"
   ],
   "exitTo": [
    "PTR-042"
   ],
   "inferred": false,
   "notes": "**Reached from PTR-042, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation."
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Analyze) and no metric row",
  "purpose": "Provide TICVAI's AI decision-support layer across the complete partner lifecycle. This screen should combine information from Boards 1, 2 and 3.",
  "purposeNote": "Management receives explainable partner-level intelligence and scenario modelling that supports growth, margin, allocation and risk decisions without bypassing commercial governance. Board 3 — Final Screen Register Screen Backend Screen Primary Responsibility 8.3.1 Partner Operations Command Center Live partner operations 8.3.2 Partner Orders & Booking Management Partner transactions",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every partner intelligence relationship",
       "columns": [
        "PartnerAiIntelligenceRelationshipOptimizationView.partnerProfile",
        "PartnerAiIntelligenceRelationshipOptimizationView.territory",
        "PartnerAiIntelligenceRelationshipOptimizationView.agreements",
        "PartnerAiIntelligenceRelationshipOptimizationView.rates",
        "PartnerAiIntelligenceRelationshipOptimizationView.commission",
        "PartnerAiIntelligenceRelationshipOptimizationView.credit",
        "PartnerAiIntelligenceRelationshipOptimizationView.paymentBehavior",
        "PartnerAiIntelligenceRelationshipOptimizationView.allocation",
        "PartnerAiIntelligenceRelationshipOptimizationView.orders",
        "PartnerAiIntelligenceRelationshipOptimizationView.cancellations",
        "PartnerAiIntelligenceRelationshipOptimizationView.settlement",
        "PartnerAiIntelligenceRelationshipOptimizationView.cases",
        "PartnerAiIntelligenceRelationshipOptimizationView.channelPerformance",
        "PartnerAiIntelligenceRelationshipOptimizationView.historicalTrends"
       ],
       "bindsTo": "PartnerAiIntelligenceRelationshipOptimizationView",
       "operation": "listPartnerRelationship",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 59 §Analyze"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected partner intelligence relationship",
       "bindsTo": "PartnerAiIntelligenceRelationshipOptimizationView",
       "columns": [
        "PartnerAiIntelligenceRelationshipOptimizationView.partnerProfile",
        "PartnerAiIntelligenceRelationshipOptimizationView.territory",
        "PartnerAiIntelligenceRelationshipOptimizationView.agreements",
        "PartnerAiIntelligenceRelationshipOptimizationView.rates",
        "PartnerAiIntelligenceRelationshipOptimizationView.commission",
        "PartnerAiIntelligenceRelationshipOptimizationView.credit",
        "PartnerAiIntelligenceRelationshipOptimizationView.paymentBehavior",
        "PartnerAiIntelligenceRelationshipOptimizationView.allocation",
        "PartnerAiIntelligenceRelationshipOptimizationView.orders",
        "PartnerAiIntelligenceRelationshipOptimizationView.cancellations",
        "PartnerAiIntelligenceRelationshipOptimizationView.settlement",
        "PartnerAiIntelligenceRelationshipOptimizationView.cases",
        "PartnerAiIntelligenceRelationshipOptimizationView.channelPerformance",
        "PartnerAiIntelligenceRelationshipOptimizationView.historicalTrends"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Commercial”, “Allocation”, “Credit”, “Risk”, “Growth”, “Natural-Language Analysis”.",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 59 §Analyze"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The partner intelligence relationship list.",
   "error": "Could not load. Names which read failed and leaves the partner intelligence relationship untouched.",
   "emptyFirstRun": "No partner intelligence relationship yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the partner intelligence relationship are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listPartnerRelationship",
    "contract": "subscription",
    "purpose": "Partner AI Intelligence & Relationship Optimization",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "PartnerAiIntelligenceRelationshipOptimizationView.partnerProfile",
    "PartnerAiIntelligenceRelationshipOptimizationView.territory",
    "PartnerAiIntelligenceRelationshipOptimizationView.agreements",
    "PartnerAiIntelligenceRelationshipOptimizationView.rates",
    "PartnerAiIntelligenceRelationshipOptimizationView.commission",
    "PartnerAiIntelligenceRelationshipOptimizationView.credit"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P10 Partner Web.dc.html#ptr-051"
  },
  "apisNote": "Regenerated 9 September 2026 from B2B, Reseller & OTA Partner Management_Reference.pdf page 59. 14 of 14 labels bound to a contract property; 14 of 96 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "_platform": {
   "code": "P10",
   "audience": "partner",
   "formFactor": "web",
   "shortName": "Partner Web",
   "name": "Partner Web — Reseller Portal",
   "offlineCapable": false,
   "app": "partner-web",
   "operator": "partner",
   "targetApp": {
    "app": "ticvai-control",
    "name": "TICVAI Control",
    "shell": "web",
    "siblings": [
     "P09",
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
 "listCommissionCalculationSettlement": {
  "method": "GET",
  "path": "/commission-calculation-settlement",
  "contract": "subscription",
  "summary": "Commission Calculation & Settlement Management",
  "permission": "PLATFORM_TENANT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [],
  "requestBody": null,
  "responds": "CommissionCalculationSettlementManagementView"
 },
 "listPartner2": {
  "method": "GET",
  "path": "/partner-2",
  "contract": "subscription",
  "summary": "Partner Operations Command Center",
  "permission": "PLATFORM_TENANT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": "venue",
    "in": "query",
    "required": false
   },
   {
    "name": "event",
    "in": "query",
    "required": false
   },
   {
    "name": "market",
    "in": "query",
    "required": false
   },
   {
    "name": "channel",
    "in": "query",
    "required": false
   },
   {
    "name": "date",
    "in": "query",
    "required": false
   }
  ],
  "requestBody": null,
  "responds": "PartnerOperationsCommandCenterView"
 },
 "listPartnerCancellationRefund": {
  "method": "GET",
  "path": "/partner-cancellation-refund",
  "contract": "subscription",
  "summary": "Partner Cancellations, Refunds & Amendments",
  "permission": "PLATFORM_TENANT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [],
  "requestBody": null,
  "responds": "PartnerCancellationsRefundsAmendmentsView"
 },
 "listPartnerDisputeCase": {
  "method": "GET",
  "path": "/partner-dispute-case",
  "contract": "subscription",
  "summary": "Partner Disputes, Cases & Service Management",
  "permission": "PLATFORM_TENANT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [],
  "requestBody": null,
  "responds": "PartnerDisputesCasesServiceManagementView"
 },
 "listPartnerOrderBooking": {
  "method": "GET",
  "path": "/partner-order-booking",
  "contract": "subscription",
  "summary": "Partner Orders & Booking Management",
  "permission": "PLATFORM_TENANT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": "partner",
    "in": "query",
    "required": false
   },
   {
    "name": "partnerOrderReference",
    "in": "query",
    "required": false
   },
   {
    "name": "ticvaiOrderId",
    "in": "query",
    "required": false
   },
   {
    "name": "event",
    "in": "query",
    "required": false
   },
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
    "name": "bookingDate",
    "in": "query",
    "required": false
   },
   {
    "name": "visitEventDate",
    "in": "query",
    "required": false
   }
  ],
  "requestBody": null,
  "responds": "PartnerOrdersBookingManagementView"
 },
 "listPartnerPerformanceScorecard": {
  "method": "GET",
  "path": "/partner-performance-scorecard",
  "contract": "subscription",
  "summary": "Partner Performance Scorecard & Risk Monitoring",
  "permission": "PLATFORM_TENANT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [],
  "requestBody": null,
  "responds": "PartnerPerformanceScorecardRiskMonitoringView"
 },
 "listPartnerReconciliationException": {
  "method": "GET",
  "path": "/partner-reconciliation-exception",
  "contract": "subscription",
  "summary": "Partner Reconciliation & Exception Management",
  "permission": "PLATFORM_TENANT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [],
  "requestBody": null,
  "responds": "PartnerReconciliationExceptionManagementView"
 },
 "listPartnerRelationship": {
  "method": "GET",
  "path": "/partner-relationship",
  "contract": "subscription",
  "summary": "Partner AI Intelligence & Relationship Optimization",
  "permission": "PLATFORM_TENANT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [],
  "requestBody": null,
  "responds": "PartnerAiIntelligenceRelationshipOptimizationView"
 },
 "listPartnerStatementAccount": {
  "method": "GET",
  "path": "/partner-statement-account",
  "contract": "subscription",
  "summary": "Partner Statement & Account Activity",
  "permission": "PLATFORM_TENANT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [],
  "requestBody": null,
  "responds": "PartnerStatementAccountActivityView"
 },
 "listReservationHoldRelease": {
  "method": "GET",
  "path": "/reservation-hold-release",
  "contract": "subscription",
  "summary": "Reservations, Holds & Release Management",
  "permission": "PLATFORM_TENANT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [],
  "requestBody": null,
  "responds": "ReservationsHoldsReleaseManagementView"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "CommissionCalculationSettlementManagementView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over subscription state, assembled at read time from tables that already exist",
  "description": "**What Commission Calculation & Settlement Management displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "commissionEarned": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Commission Earned"
   },
   "commissionPending": {
    "type": "integer",
    "description": "Commission Pending"
   },
   "approved": {
    "type": "integer",
    "description": "Approved"
   },
   "onHold": {
    "type": "string",
    "description": "On Hold"
   },
   "paid": {
    "type": "string",
    "description": "Paid"
   },
   "reversed": {
    "type": "string",
    "description": "Reversed"
   },
   "incentivesEarned": {
    "type": "string",
    "description": "Incentives Earned"
   },
   "nextSettlement": {
    "type": "string",
    "format": "date-time",
    "description": "Next Settlement"
   },
   "order": {
    "type": "string",
    "description": "Order"
   },
   "partner": {
    "type": "string",
    "description": "Partner"
   },
   "product": {
    "type": "string",
    "description": "Product"
   },
   "grossValue": {
    "type": "string",
    "description": "Gross Value"
   },
   "netRate": {
    "type": "number",
    "description": "Net Rate"
   },
   "commissionBasis": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Commission Basis"
   },
   "commission": {
    "type": "number",
    "description": "Commission %"
   },
   "commissionAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Commission Amount"
   },
   "incentive": {
    "type": "string",
    "description": "Incentive"
   },
   "adjustment": {
    "type": "string",
    "description": "Adjustment"
   },
   "payableAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Payable Amount"
   },
   "perTransaction": {
    "type": "string",
    "description": "Per Transaction"
   },
   "weekly": {
    "type": "string",
    "description": "Weekly"
   },
   "monthly": {
    "type": "string",
    "description": "Monthly"
   },
   "eventBased": {
    "type": "string",
    "description": "Event-Based"
   },
   "customCycle": {
    "type": "string",
    "description": "Custom Cycle"
   },
   "cancellation": {
    "type": "string",
    "description": "Cancellation"
   },
   "chargeback": {
    "type": "string",
    "description": "Chargeback"
   },
   "partialFulfillment": {
    "type": "string",
    "description": "Partial fulfillment"
   },
   "commissionCorrection": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Commission correction"
   },
   "incentiveQualification": {
    "type": "string",
    "description": "Incentive qualification"
   },
   "currency": {
    "type": "string",
    "description": "Currency"
   },
   "period": {
    "type": "string",
    "format": "date-time",
    "description": "Period"
   },
   "legalEntity": {
    "type": "string",
    "description": "Legal Entity"
   }
  }
 },
 "PartnerAiIntelligenceRelationshipOptimizationView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over subscription state, assembled at read time from tables that already exist",
  "description": "**What Partner AI Intelligence & Relationship Optimization displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "partnerProfile": {
    "type": "string",
    "description": "Partner profile"
   },
   "territory": {
    "type": "string",
    "description": "Territory"
   },
   "agreements": {
    "type": "string",
    "description": "Agreements"
   },
   "rates": {
    "type": "string",
    "description": "Rates"
   },
   "commission": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Commission"
   },
   "credit": {
    "type": "string",
    "description": "Credit"
   },
   "paymentBehavior": {
    "type": "string",
    "description": "Payment behavior"
   },
   "allocation": {
    "type": "string",
    "description": "Allocation"
   },
   "orders": {
    "type": "string",
    "description": "Orders"
   },
   "cancellations": {
    "type": "string",
    "description": "Cancellations"
   },
   "settlement": {
    "type": "string",
    "description": "Settlement"
   },
   "cases": {
    "type": "string",
    "description": "Cases"
   },
   "channelPerformance": {
    "type": "string",
    "description": "Channel performance"
   },
   "historicalTrends": {
    "type": "string",
    "description": "Historical trends"
   },
   "releasing320Tickets": {
    "type": "string",
    "description": "releasing 320 tickets"
   },
   "velocity": {
    "type": "string",
    "description": "velocity"
   },
   "usingConfigurableBusinessCriteria": {
    "type": "string",
    "description": "using configurable business criteria"
   },
   "additionalSales": {
    "type": "string",
    "description": "Additional Sales"
   },
   "revenue": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Revenue"
   },
   "margin": {
    "type": "number",
    "description": "Margin"
   },
   "creditExposure": {
    "type": "string",
    "description": "Credit Exposure"
   },
   "inventoryRisk": {
    "type": "string",
    "description": "Inventory Risk"
   },
   "recommendation": {
    "type": "string",
    "description": "Recommendation"
   },
   "reason": {
    "type": "string",
    "description": "Reason"
   },
   "expectedImpact": {
    "type": "string",
    "description": "Expected Impact"
   },
   "confidence": {
    "type": "string",
    "description": "Confidence"
   },
   "risks": {
    "type": "string",
    "description": "Risks"
   },
   "supportingMetrics": {
    "type": "string",
    "description": "Supporting Metrics"
   },
   "management": {
    "type": "string",
    "description": "management"
   },
   "screenBackendScreenPrimaryResponsibility": {
    "type": "string",
    "description": "Screen Backend Screen Primary Responsibility"
   },
   "partnerReconciliationExceptionOperationalFinancial": {
    "type": "string",
    "description": "Partner Reconciliation & Exception Operational/financial"
   },
   "area8CompleteArchitecture": {
    "type": "string",
    "description": "Area 8 — Complete Architecture"
   },
   "whoIsThePartner": {
    "type": "string",
    "description": "Who is the partner?"
   },
   "board2CommercialManagement": {
    "type": "string",
    "description": "Board 2 — Commercial Management"
   },
   "billingAllocationLimits": {
    "type": "string",
    "description": "Billing → Allocation → Limits"
   },
   "howIsTheRelationshipPerforming": {
    "type": "string",
    "description": "How is the relationship performing?"
   },
   "ai": {
    "type": "string",
    "description": "AI"
   },
   "dashboard": {
    "type": "string",
    "description": "dashboard"
   },
   "launchTheAppropriateGovernedWorkflow": {
    "type": "string",
    "description": "launch the appropriate governed workflow"
   },
   "chartAddedAtTheEnd": {
    "type": "string",
    "description": "chart added at the end"
   }
  }
 },
 "PartnerCancellationsRefundsAmendmentsView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over subscription state, assembled at read time from tables that already exist",
  "description": "**What Partner Cancellations, Refunds & Amendments displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "fullCancellation": {
    "type": "string",
    "description": "Full Cancellation"
   },
   "partialCancellation": {
    "type": "string",
    "description": "Partial Cancellation"
   },
   "dateChange": {
    "type": "string",
    "format": "date-time",
    "description": "Date Change"
   },
   "performanceChange": {
    "type": "string",
    "description": "Performance Change"
   },
   "quantityReduction": {
    "type": "integer",
    "description": "Quantity Reduction"
   },
   "productChange": {
    "type": "string",
    "description": "Product Change"
   },
   "ticketReissue": {
    "type": "string",
    "description": "Ticket Reissue"
   },
   "customerNameChangeWherePermitted": {
    "type": "string",
    "description": "Customer Name Change where permitted"
   },
   "transactionValue": {
    "type": "string",
    "description": "Transaction value"
   },
   "eventProximity": {
    "type": "string",
    "description": "Event proximity"
   },
   "cancellationPercentage": {
    "type": "number",
    "description": "Cancellation percentage"
   },
   "partnerStatus": {
    "type": "string",
    "description": "Partner status"
   },
   "exceptionRequest": {
    "type": "string",
    "description": "Exception request"
   },
   "originalState": {
    "type": "string",
    "description": "Original state"
   },
   "newState": {
    "type": "integer",
    "description": "New state"
   },
   "user": {
    "type": "string",
    "description": "User"
   },
   "reason": {
    "type": "string",
    "description": "Reason"
   },
   "financialImpact": {
    "type": "string",
    "description": "Financial impact"
   },
   "approval": {
    "type": "string",
    "description": "Approval"
   }
  }
 },
 "PartnerDisputesCasesServiceManagementView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over subscription state, assembled at read time from tables that already exist",
  "description": "**What Partner Disputes, Cases & Service Management displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "bookingDispute": {
    "type": "string",
    "description": "Booking Dispute"
   },
   "pricingDispute": {
    "type": "string",
    "description": "Pricing Dispute"
   },
   "commissionDispute": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Commission Dispute"
   },
   "creditDispute": {
    "type": "string",
    "description": "Credit Dispute"
   },
   "invoiceDispute": {
    "type": "string",
    "description": "Invoice Dispute"
   },
   "cancellationDispute": {
    "type": "string",
    "description": "Cancellation Dispute"
   },
   "ticketIssue": {
    "type": "string",
    "description": "Ticket Issue"
   },
   "allocationIssue": {
    "type": "string",
    "description": "Allocation Issue"
   },
   "apiIssue": {
    "type": "string",
    "description": "API Issue"
   },
   "settlementDispute": {
    "type": "string",
    "description": "Settlement Dispute"
   },
   "caseId": {
    "type": "string",
    "description": "Case ID"
   },
   "partner": {
    "type": "string",
    "description": "Partner"
   },
   "contact": {
    "type": "string",
    "description": "Contact"
   },
   "category": {
    "type": "string",
    "description": "Category"
   },
   "priority": {
    "type": "string",
    "description": "Priority"
   },
   "relatedOrder": {
    "type": "string",
    "description": "Related Order"
   },
   "relatedInvoice": {
    "type": "string",
    "description": "Related Invoice"
   },
   "relatedSettlement": {
    "type": "string",
    "description": "Related Settlement"
   },
   "amountInDispute": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Amount in Dispute"
   },
   "description": {
    "type": "string",
    "description": "Description"
   },
   "evidence": {
    "type": "string",
    "description": "Evidence"
   },
   "owner": {
    "type": "string",
    "description": "Owner"
   },
   "sla": {
    "type": "string",
    "description": "SLA"
   },
   "status": {
    "type": "string",
    "description": "Status"
   },
   "proposedResolvedClosed": {
    "type": "integer",
    "description": "Proposed → Resolved → Closed"
   },
   "firstResponse": {
    "type": "string",
    "description": "First Response"
   },
   "resolutionTarget": {
    "type": "string",
    "description": "Resolution Target"
   },
   "timeOpen": {
    "type": "string",
    "format": "date-time",
    "description": "Time Open"
   },
   "slaBreach": {
    "type": "string",
    "description": "SLA Breach"
   },
   "notes": {
    "type": "string",
    "description": "Notes"
   },
   "attachments": {
    "type": "string",
    "description": "Attachments"
   },
   "assignments": {
    "type": "string",
    "description": "Assignments"
   },
   "departmentEscalation": {
    "type": "string",
    "description": "Department escalation"
   },
   "financeReview": {
    "type": "string",
    "description": "Finance review"
   },
   "technicalReview": {
    "type": "string",
    "description": "Technical review"
   }
  }
 },
 "PartnerOperationsCommandCenterView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over subscription state, assembled at read time from tables that already exist",
  "description": "**What Partner Operations Command Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "partnerSalesToday": {
    "type": "string",
    "description": "Partner Sales Today"
   },
   "partnerSalesMtd": {
    "type": "string",
    "description": "Partner Sales MTD"
   },
   "activePartnerOrders": {
    "type": "integer",
    "description": "Active Partner Orders"
   },
   "activeReservations": {
    "type": "integer",
    "description": "Active Reservations"
   },
   "activeHolds": {
    "type": "integer",
    "description": "Active Holds"
   },
   "ticketsSold": {
    "type": "string",
    "description": "Tickets Sold"
   },
   "cancellations": {
    "type": "integer",
    "description": "Cancellations"
   },
   "refunds": {
    "type": "integer",
    "description": "Refunds"
   },
   "outstandingReceivables": {
    "type": "integer",
    "description": "Outstanding Receivables"
   },
   "commissionPayable": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Commission Payable"
   },
   "pendingSettlements": {
    "type": "integer",
    "description": "Pending Settlements"
   },
   "operationalExceptions": {
    "type": "integer",
    "description": "Operational Exceptions"
   },
   "partnersRequiringAttention": {
    "type": "string",
    "description": "Partners Requiring Attention"
   },
   "partner": {
    "type": "string",
    "description": "Partner"
   },
   "partnerType": {
    "type": "string",
    "description": "Partner Type"
   },
   "accountManager": {
    "type": "string",
    "description": "Account Manager"
   },
   "orders": {
    "type": "integer",
    "description": "Orders"
   },
   "tickets": {
    "type": "integer",
    "description": "Tickets"
   },
   "grossSales": {
    "type": "integer",
    "description": "Gross Sales"
   },
   "netSales": {
    "type": "integer",
    "description": "Net Sales"
   },
   "commission": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Commission"
   },
   "outstandingBalance": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Outstanding Balance"
   },
   "creditUtilization": {
    "type": "number",
    "description": "Credit Utilization"
   },
   "allocationUtilization": {
    "type": "number",
    "description": "Allocation Utilization"
   },
   "cancellationRate": {
    "type": "number",
    "description": "Cancellation Rate"
   },
   "operationalStatus": {
    "type": "integer",
    "description": "Operational Status"
   },
   "risk": {
    "type": "string",
    "description": "Risk"
   }
  }
 },
 "PartnerOrdersBookingManagementView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over subscription state, assembled at read time from tables that already exist",
  "description": "**What Partner Orders & Booking Management displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "partnerReference": {
    "type": "string",
    "description": "Partner Reference"
   },
   "agentUser": {
    "type": "string",
    "description": "Agent/User"
   },
   "customerGuestWhereApplicable": {
    "type": "string",
    "description": "Customer/Guest where applicable"
   },
   "products": {
    "type": "integer",
    "description": "Products"
   },
   "quantity": {
    "type": "integer",
    "description": "Quantity"
   },
   "grossValue": {
    "type": "string",
    "description": "Gross Value"
   },
   "partnerRate": {
    "type": "number",
    "description": "Partner Rate"
   },
   "commission": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Commission"
   },
   "netAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Net Amount"
   },
   "paymentMethod": {
    "type": "string",
    "description": "Payment Method"
   },
   "billingStatus": {
    "type": "integer",
    "description": "Billing Status"
   },
   "fulfillmentStatus": {
    "type": "integer",
    "description": "Fulfillment Status"
   },
   "modify": {
    "type": "string",
    "description": "Modify"
   },
   "rebook": {
    "type": "string",
    "description": "Rebook"
   },
   "agreement": {
    "type": "string",
    "description": "Agreement"
   },
   "productEligibility": {
    "type": "string",
    "description": "Product eligibility"
   },
   "rate": {
    "type": "number",
    "description": "Rate"
   },
   "allocation": {
    "type": "string",
    "description": "Allocation"
   },
   "credit": {
    "type": "string",
    "description": "Credit"
   },
   "bookingLimit": {
    "type": "integer",
    "description": "Booking limit"
   },
   "cancellationPolicy": {
    "type": "string",
    "description": "Cancellation policy"
   }
  }
 },
 "PartnerPerformanceScorecardRiskMonitoringView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over subscription state, assembled at read time from tables that already exist",
  "description": "**What Partner Performance Scorecard & Risk Monitoring displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "sales": {
    "type": "string",
    "description": "Sales"
   },
   "revenue": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Revenue"
   },
   "growth": {
    "type": "string",
    "description": "Growth"
   },
   "margin": {
    "type": "number",
    "description": "Margin"
   },
   "averageOrderValue": {
    "type": "number",
    "description": "Average Order Value"
   },
   "utilization": {
    "type": "number",
    "description": "Utilization"
   },
   "sellThrough": {
    "type": "string",
    "description": "Sell-through"
   },
   "returnedInventory": {
    "type": "string",
    "description": "Returned Inventory"
   },
   "paymentTimeliness": {
    "type": "string",
    "description": "Payment Timeliness"
   },
   "creditUtilization": {
    "type": "number",
    "description": "Credit Utilization"
   },
   "overdueBalance": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Overdue Balance"
   },
   "cancellationRate": {
    "type": "number",
    "description": "Cancellation Rate"
   },
   "errorRate": {
    "type": "number",
    "description": "Error Rate"
   },
   "supportCases": {
    "type": "string",
    "description": "Support Cases"
   },
   "apiSuccess": {
    "type": "string",
    "description": "API Success"
   },
   "transactionFailureRate": {
    "type": "number",
    "description": "Transaction Failure Rate"
   },
   "documentation": {
    "type": "string",
    "description": "Documentation"
   },
   "agreementStatus": {
    "type": "string",
    "description": "Agreement Status"
   },
   "securityGuaranteeStatus": {
    "type": "string",
    "description": "Security/Guarantee Status"
   },
   "improving": {
    "type": "string",
    "description": "Improving"
   },
   "stable": {
    "type": "string",
    "description": "Stable"
   },
   "declining": {
    "type": "string",
    "description": "Declining"
   },
   "samePartnerType": {
    "type": "string",
    "description": "Same partner type"
   },
   "sameMarket": {
    "type": "string",
    "description": "Same market"
   },
   "sameChannel": {
    "type": "string",
    "description": "Same channel"
   },
   "portfolioAverage": {
    "type": "number",
    "description": "Portfolio average"
   }
  }
 },
 "PartnerReconciliationExceptionManagementView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over subscription state, assembled at read time from tables that already exist",
  "description": "**What Partner Reconciliation & Exception Management displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "ticvaiOrders": {
    "type": "string",
    "description": "↔ TICVAI Orders"
   },
   "ticketsIssued": {
    "type": "string",
    "description": "↔ Tickets Issued"
   },
   "partnerRates": {
    "type": "string",
    "description": "↔ Partner Rates"
   },
   "paymentsCredit": {
    "type": "string",
    "description": "↔ Payments/Credit"
   },
   "commission": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "↔ Commission"
   },
   "invoices": {
    "type": "string",
    "description": "↔ Invoices"
   },
   "cancellationsRefunds": {
    "type": "string",
    "description": "↔ Cancellations/Refunds"
   },
   "recordsReconciled": {
    "type": "string",
    "description": "Records Reconciled"
   },
   "unmatchedOrders": {
    "type": "integer",
    "description": "Unmatched Orders"
   },
   "amountMismatches": {
    "type": "integer",
    "description": "Amount Mismatches"
   },
   "missingTickets": {
    "type": "integer",
    "description": "Missing Tickets"
   },
   "pricingDifferences": {
    "type": "integer",
    "description": "Pricing Differences"
   },
   "commissionDifferences": {
    "type": "integer",
    "description": "Commission Differences"
   },
   "paymentDifferences": {
    "type": "integer",
    "description": "Payment Differences"
   },
   "pendingInvestigation": {
    "type": "integer",
    "description": "Pending Investigation"
   },
   "partnerAmountAed12450": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Partner Amount: AED 12,450"
   },
   "differenceAed150": {
    "type": "string",
    "description": "Difference: AED 150"
   },
   "mismatchType": {
    "type": "string",
    "enum": [
     "missingTransaction",
     "duplicateTransaction",
     "price",
     "quantity",
     "tax",
     "commission",
     "payment",
     "cancellation",
     "settlement"
    ],
    "description": "Vocabulary listed under Exception Types."
   },
   "match": {
    "type": "string",
    "description": "Match"
   },
   "correct": {
    "type": "string",
    "description": "Correct"
   },
   "acceptDifference": {
    "type": "string",
    "description": "Accept Difference"
   },
   "dispute": {
    "type": "string",
    "description": "Dispute"
   }
  }
 },
 "PartnerStatementAccountActivityView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over subscription state, assembled at read time from tables that already exist",
  "description": "**What Partner Statement & Account Activity displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "openingBalance": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Opening Balance"
   },
   "sales": {
    "type": "integer",
    "description": "Sales"
   },
   "payments": {
    "type": "integer",
    "description": "Payments"
   },
   "credits": {
    "type": "integer",
    "description": "Credits"
   },
   "refunds": {
    "type": "integer",
    "description": "Refunds"
   },
   "commission": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Commission"
   },
   "adjustments": {
    "type": "integer",
    "description": "Adjustments"
   },
   "closingBalance": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Closing Balance"
   },
   "overdueBalance": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Overdue Balance"
   },
   "availableCredit": {
    "type": "string",
    "description": "Available Credit"
   },
   "current": {
    "type": "string",
    "description": "Current"
   },
   "date": {
    "type": "string",
    "format": "date-time",
    "description": "Date"
   },
   "transactionType": {
    "type": "string",
    "description": "Transaction Type"
   },
   "reference": {
    "type": "string",
    "description": "Reference"
   },
   "orderInvoice": {
    "type": "string",
    "description": "Order/Invoice"
   },
   "debit": {
    "type": "string",
    "description": "Debit"
   },
   "credit": {
    "type": "string",
    "description": "Credit"
   },
   "runningBalance": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Running Balance"
   },
   "dueDate": {
    "type": "string",
    "format": "date-time",
    "description": "Due Date"
   },
   "status": {
    "type": "integer",
    "description": "Status"
   },
   "daily": {
    "type": "string",
    "description": "Daily"
   },
   "weekly": {
    "type": "string",
    "description": "Weekly"
   },
   "monthly": {
    "type": "string",
    "description": "Monthly"
   },
   "customDateRange": {
    "type": "string",
    "format": "date-time",
    "description": "Custom Date Range"
   }
  }
 },
 "ReservationsHoldsReleaseManagementView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over subscription state, assembled at read time from tables that already exist",
  "description": "**What Reservations, Holds & Release Management displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "activeHolds": {
    "type": "integer",
    "description": "Active Holds"
   },
   "heldTickets": {
    "type": "integer",
    "description": "Held Tickets"
   },
   "heldValue": {
    "type": "string",
    "description": "Held Value"
   },
   "expiringToday": {
    "type": "string",
    "description": "Expiring Today"
   },
   "expiredHolds": {
    "type": "integer",
    "description": "Expired Holds"
   },
   "convertedHolds": {
    "type": "integer",
    "description": "Converted Holds"
   },
   "releasedInventory": {
    "type": "string",
    "description": "Released Inventory"
   },
   "holdId": {
    "type": "string",
    "description": "Hold ID"
   },
   "partner": {
    "type": "string",
    "description": "Partner"
   },
   "event": {
    "type": "string",
    "description": "Event"
   },
   "product": {
    "type": "string",
    "description": "Product"
   },
   "quantity": {
    "type": "integer",
    "description": "Quantity"
   },
   "seatZoneWhereApplicable": {
    "type": "string",
    "description": "Seat/Zone where applicable"
   },
   "holdCreated": {
    "type": "string",
    "format": "date-time",
    "description": "Hold Created"
   },
   "holdExpiry": {
    "type": "string",
    "format": "date-time",
    "description": "Hold Expiry"
   },
   "createdBy": {
    "type": "string",
    "format": "date-time",
    "description": "Created By"
   },
   "commercialValue": {
    "type": "string",
    "description": "Commercial Value"
   },
   "allocationSource": {
    "type": "string",
    "description": "Allocation Source"
   },
   "status": {
    "type": "string",
    "description": "Status"
   },
   "maximumHoldQuantity": {
    "type": "integer",
    "description": "Maximum Hold Quantity"
   },
   "holdDuration": {
    "type": "string",
    "format": "date-time",
    "description": "Hold Duration"
   },
   "numberOfExtensions": {
    "type": "integer",
    "description": "Number of Extensions"
   },
   "partnerHoldLimit": {
    "type": "integer",
    "description": "Partner Hold Limit"
   },
   "eventCutoff": {
    "type": "string",
    "description": "Event Cutoff"
   },
   "approvalRequirement": {
    "type": "string",
    "description": "Approval Requirement"
   },
   "reduceHold": {
    "type": "string",
    "description": "Reduce Hold"
   },
   "reassignWherePermitted": {
    "type": "string",
    "description": "Reassign where permitted"
   },
   "unlessAnApprovedExtensionExists": {
    "type": "string",
    "description": "unless an approved extension exists"
   }
  }
 }
}
```
