# WS23 — B2B, Reseller & OTA Partner Management board 3

**10 screens · 17 operations · 25 schemas · 4 permissions**

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

- **Every control that can be refused must be gated.** 4 permissions apply here:
  `CASE_MANAGE, ORDER_MODIFY, PLATFORM_TENANT_VIEW, SETTLEMENT_RECONCILE`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `PTR-042` | Partner Operations Command Center | commandCentre | 2 | 0 | — |
| `PTR-043` | Partner Orders & Booking Management | listDetail | 1 | 0 | — |
| `PTR-044` | Reservations, Holds & Release Management | listDetail | 1 | 0 | — |
| `PTR-045` | Partner Cancellations, Refunds & Amendments | listDetail | 2 | 1 | — |
| `PTR-046` | Partner Statement & Account Activity | commandCentre | 1 | 0 | — |
| `PTR-047` | Partner Reconciliation & Exception Management | listDetail | 2 | 1 | — |
| `PTR-048` | Commission Calculation & Settlement Management | listDetail | 3 | 2 | — |
| `PTR-049` | Partner Disputes, Cases & Service Management | listDetail | 3 | 2 | — |
| `PTR-050` | Partner Performance Scorecard & Risk Monitoring | listDetail | 1 | 0 | — |
| `PTR-051` | Partner AI Intelligence & Relationship Optimization | listDetail | 1 | 0 | — |

## Thin screens in this batch

**PTR-045, PTR-050, PTR-051 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

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
  "purposeNote": "Authorized users can understand current partner activity, financial exposure and operational exceptions from one centralized workspace.",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen both a metric directory (§Display) and a per-row directory (§Each partner should show) — counts over a population, then the population",
  "purpose": "Provide commercial, operations and finance teams with one real-time view of active B2B, reseller and OTA business.",
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
       "bindsTo": "PartnerOperationsCommandCenterSummary.partnerSalesToday"
      },
      {
       "kind": "metricTile",
       "label": "Partner Sales MTD",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 44 §Display",
       "bindsTo": "PartnerOperationsCommandCenterSummary.partnerSalesMtd"
      },
      {
       "kind": "metricTile",
       "label": "Active Partner Orders",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 44 §Display",
       "bindsTo": "PartnerOperationsCommandCenterSummary.activePartnerOrders"
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
       "bindsTo": "PartnerOperationsCommandCenterSummary.ticketsSold"
      },
      {
       "kind": "metricTile",
       "label": "Cancellations",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 44 §Display",
       "bindsTo": "PartnerOperationsCommandCenterSummary.cancellations"
      },
      {
       "kind": "metricTile",
       "label": "Refunds",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 44 §Display",
       "bindsTo": "PartnerOperationsCommandCenterSummary.refunds"
      },
      {
       "kind": "metricTile",
       "label": "Outstanding Receivables",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 44 §Display",
       "bindsTo": "PartnerOperationsCommandCenterSummary.outstandingReceivables"
      },
      {
       "kind": "metricTile",
       "label": "Commission Payable",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 44 §Display",
       "bindsTo": "PartnerOperationsCommandCenterSummary.commissionPayable"
      },
      {
       "kind": "metricTile",
       "label": "Pending Settlements",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 44 §Display",
       "bindsTo": "PartnerOperationsCommandCenterSummary.pendingSettlements"
      },
      {
       "kind": "metricTile",
       "label": "Operational Exceptions",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 44 §Display",
       "bindsTo": "PartnerOperationsCommandCenterSummary.operationalExceptions"
      },
      {
       "kind": "metricTile",
       "label": "Partners Requiring Attention",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 44 §Display",
       "bindsTo": "PartnerOperationsCommandCenterSummary.partnersRequiringAttention"
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
   },
   {
    "operationId": "listPartner",
    "contract": "subscription",
    "purpose": "Partner Management Command Center",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P10 Partner Web.dc.html#ptr-042",
   "workshopBoard": "wireframes/WS40 B2B, Reseller & OTA Partner Management Board 3.dc.html#ptr-042"
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
  "purposeNote": "Operations can locate and service any partner transaction while preserving central order and commercial-rule integrity.",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Provide a consolidated operational view of orders created by each partner.",
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
        "PartnerOrdersBookingManagementView.customerName",
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
        "PartnerOrdersBookingManagementView.customerName",
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
    "PartnerOrdersBookingManagementView.customerName",
    "Booking Date"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P10 Partner Web.dc.html#ptr-043",
   "workshopBoard": "wireframes/WS40 B2B, Reseller & OTA Partner Management Board 3.dc.html#ptr-043"
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
  "purposeNote": "Partner reservations and holds cannot indefinitely block sellable capacity and are automatically governed by configured duration, allocation and approval rules.",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Manage inventory temporarily reserved by B2B partners before final confirmation. This is particularly important for tour operators, corporate groups and travel-trade partners.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "Active Holds",
       "bindsTo": "ReservationsHoldsReleaseManagementSummary.activeHolds",
       "operation": "listReservationHoldRelease",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Held Tickets",
       "bindsTo": "ReservationsHoldsReleaseManagementSummary.heldTickets",
       "operation": "listReservationHoldRelease",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Held Value",
       "bindsTo": "ReservationsHoldsReleaseManagementSummary.heldValue",
       "operation": "listReservationHoldRelease",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Expiring Today",
       "bindsTo": "ReservationsHoldsReleaseManagementSummary.expiringToday",
       "operation": "listReservationHoldRelease",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Expired Holds",
       "bindsTo": "ReservationsHoldsReleaseManagementSummary.expiredHolds",
       "operation": "listReservationHoldRelease",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Converted Holds",
       "bindsTo": "ReservationsHoldsReleaseManagementSummary.convertedHolds",
       "operation": "listReservationHoldRelease",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Released Inventory, tickets",
       "bindsTo": "ReservationsHoldsReleaseManagementSummary.releasedInventory",
       "operation": "listReservationHoldRelease",
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
       "label": "Every reservations holds release",
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
    "ReservationsHoldsReleaseManagementSummary.activeHolds",
    "ReservationsHoldsReleaseManagementSummary.heldTickets",
    "ReservationsHoldsReleaseManagementSummary.heldValue",
    "ReservationsHoldsReleaseManagementSummary.expiringToday",
    "ReservationsHoldsReleaseManagementSummary.expiredHolds",
    "ReservationsHoldsReleaseManagementSummary.convertedHolds"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P10 Partner Web.dc.html#ptr-044",
   "workshopBoard": "wireframes/WS40 B2B, Reseller & OTA Partner Management Board 3.dc.html#ptr-044"
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
  "purposeNote": "Partner booking changes are processed according to applicable commercial and product policies with complete financial and inventory impact visibility.",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Manage post-booking changes according to the partner's commercial agreement and product policies.",
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
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Create partner change request",
       "operation": "createPartnerChangeRequest",
       "permission": "ORDER_MODIFY",
       "notes": "The request raised from PTR-045 (decided 29 September, writers pass; DM4).",
       "provenance": "contract subscription.yaml POST /partner-change-requests"
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
   },
   {
    "operationId": "createPartnerChangeRequest",
    "contract": "subscription",
    "purpose": "A partner asks to cancel or amend a booking",
    "trigger": "onAction",
    "invalidates": [
     "listPartnerCancellationRefund"
    ]
   }
  ],
  "entryState": {
   "preloaded": [
    "PartnerCancellationsRefundsAmendmentsView.requestType"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P10 Partner Web.dc.html#ptr-045",
   "workshopBoard": "wireframes/WS40 B2B, Reseller & OTA Partner Management Board 3.dc.html#ptr-045"
  },
  "apisNote": "Regenerated 9 September 2026 from B2B, Reseller & OTA Partner Management_Reference.pdf page 49. 0 of 0 labels bound to a contract property; 0 of 34 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "overlays": [
   {
    "id": "formCreatePartnerChangeRequest",
    "component": "modal",
    "trigger": "Create partner change request",
    "body": "**Collects what `createPartnerChangeRequest` sends before it is called.** Required: `orderId`, `requestType`. Optional: `quantity`, `targetPerformanceId`, `targetProductId`, `newCustomerName`, `feeWaiverRequested`, `reason`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "PartnerChangeRequestInput",
    "confirm": {
     "label": "Create partner change request",
     "operation": "createPartnerChangeRequest"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "orderId",
      "requestType",
      "quantity",
      "targetPerformanceId",
      "targetProductId",
      "newCustomerName",
      "feeWaiverRequested",
      "reason"
     ]
    },
    "provenance": "contract subscription.yaml POST /partner-change-requests"
   }
  ],
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
  "purposeNote": "Finance and authorized partner users can reconcile all commercial account activity against a clear running balance and supporting transaction references.",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen both a metric directory (§Display) and a per-row directory (§Each line should show) — counts over a population, then the population",
  "purpose": "Give finance and commercial teams a complete financial statement for each partner account.",
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
       "bindsTo": "PartnerStatementAccountActivitySummary.openingBalance"
      },
      {
       "kind": "metricTile",
       "label": "Sales",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 51 §Display",
       "bindsTo": "PartnerStatementAccountActivitySummary.sales"
      },
      {
       "kind": "metricTile",
       "label": "Payments",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 51 §Display",
       "bindsTo": "PartnerStatementAccountActivitySummary.payments"
      },
      {
       "kind": "metricTile",
       "label": "Credits",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 51 §Display",
       "bindsTo": "PartnerStatementAccountActivitySummary.credits"
      },
      {
       "kind": "metricTile",
       "label": "Refunds",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 51 §Display",
       "bindsTo": "PartnerStatementAccountActivitySummary.refunds"
      },
      {
       "kind": "metricTile",
       "label": "Commission",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 51 §Display",
       "bindsTo": "PartnerStatementAccountActivitySummary.commission"
      },
      {
       "kind": "metricTile",
       "label": "Adjustments",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 51 §Display",
       "bindsTo": "PartnerStatementAccountActivitySummary.adjustments"
      },
      {
       "kind": "metricTile",
       "label": "Closing Balance",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 51 §Display",
       "bindsTo": "PartnerStatementAccountActivitySummary.closingBalance"
      },
      {
       "kind": "metricTile",
       "label": "Overdue Balance",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 51 §Display",
       "bindsTo": "PartnerStatementAccountActivitySummary.overdueBalance"
      },
      {
       "kind": "metricTile",
       "label": "Available Credit",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 51 §Display",
       "bindsTo": "PartnerStatementAccountActivitySummary.availableCredit"
      },
      {
       "kind": "metricTile",
       "label": "Current",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 51 §Display",
       "bindsTo": "PartnerStatementAccountActivitySummary.current"
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
   "board": "wireframes/P10 Partner Web.dc.html#ptr-046",
   "workshopBoard": "wireframes/WS40 B2B, Reseller & OTA Partner Management Board 3.dc.html#ptr-046"
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
  "purposeNote": "Partner operational and financial records can be reconciled systematically, with every unresolved difference tracked through resolution.",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Reconcile operational bookings against financial and channel records and identify discrepancies.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "Records Reconciled",
       "bindsTo": "PartnerReconciliationExceptionManagementSummary.recordsReconciled",
       "operation": "listPartnerReconciliationException",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Unmatched Orders",
       "bindsTo": "PartnerReconciliationExceptionManagementSummary.unmatchedOrders",
       "operation": "listPartnerReconciliationException",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Amount Mismatches",
       "bindsTo": "PartnerReconciliationExceptionManagementSummary.amountMismatches",
       "operation": "listPartnerReconciliationException",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Missing Tickets",
       "bindsTo": "PartnerReconciliationExceptionManagementSummary.missingTickets",
       "operation": "listPartnerReconciliationException",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Pricing Differences",
       "bindsTo": "PartnerReconciliationExceptionManagementSummary.pricingDifferences",
       "operation": "listPartnerReconciliationException",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Commission Differences",
       "bindsTo": "PartnerReconciliationExceptionManagementSummary.commissionDifferences",
       "operation": "listPartnerReconciliationException",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Payment Differences",
       "bindsTo": "PartnerReconciliationExceptionManagementSummary.paymentDifferences",
       "operation": "listPartnerReconciliationException",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Pending Investigation",
       "bindsTo": "PartnerReconciliationExceptionManagementSummary.pendingInvestigation",
       "operation": "listPartnerReconciliationException",
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
       "label": "Every partner reconciliation exception",
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
      },
      {
       "kind": "primaryButton",
       "label": "Act on partner reconciliation exception",
       "operation": "actOnPartnerReconciliationException",
       "permission": "SETTLEMENT_RECONCILE",
       "notes": "The owner actions on PTR-047 (decided 29 September, writers pass; DM4); the rows themselves are created and re-matched by the reconciliation job.",
       "provenance": "contract subscription.yaml POST /partner-reconciliation-exceptions/{exceptionId}/actions"
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
   },
   {
    "operationId": "actOnPartnerReconciliationException",
    "contract": "subscription",
    "purpose": "Work a partner reconciliation exception",
    "trigger": "onAction",
    "invalidates": [
     "listPartnerReconciliationException"
    ]
   }
  ],
  "entryState": {
   "preloaded": [
    "PartnerReconciliationExceptionManagementSummary.recordsReconciled",
    "PartnerReconciliationExceptionManagementSummary.unmatchedOrders",
    "PartnerReconciliationExceptionManagementSummary.amountMismatches",
    "PartnerReconciliationExceptionManagementSummary.missingTickets",
    "PartnerReconciliationExceptionManagementSummary.pricingDifferences",
    "PartnerReconciliationExceptionManagementSummary.commissionDifferences"
   ],
   "params": [
    {
     "name": "exceptionId",
     "from": "navigation",
     "optional": true
    }
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P10 Partner Web.dc.html#ptr-047",
   "workshopBoard": "wireframes/WS40 B2B, Reseller & OTA Partner Management Board 3.dc.html#ptr-047"
  },
  "apisNote": "Regenerated 9 September 2026 from B2B, Reseller & OTA Partner Management_Reference.pdf page 52. 8 of 8 labels bound to a contract property; 15 of 39 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "overlays": [
   {
    "id": "formActOnPartnerReconciliationException",
    "component": "modal",
    "trigger": "Act on partner reconciliation exception",
    "body": "**Collects what `actOnPartnerReconciliationException` sends before it is called.** Required: `action`. Optional: `assigneePrincipalId`, `adjustmentRef`, `note`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Act on partner reconciliation exception",
     "operation": "actOnPartnerReconciliationException"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "action",
      "assigneePrincipalId",
      "adjustmentRef",
      "note"
     ]
    },
    "provenance": "contract subscription.yaml POST /partner-reconciliation-exceptions/{exceptionId}/actions"
   }
  ],
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
  "purposeNote": "until relevant transactions and adjustments have been reconciled.",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Calculate, approve and settle commission or incentive amounts owed under partner commercial agreements.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 1 actions on this screen and the screen declares 1 operation.** Unserved: Per Transaction. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 54 §Support"
   }
  ],
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "Commission Earned",
       "bindsTo": "CommissionCalculationSettlementManagementSummary.commissionEarned",
       "operation": "listCommissionCalculationSettlement",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Commission Pending",
       "bindsTo": "CommissionCalculationSettlementManagementSummary.commissionPending",
       "operation": "listCommissionCalculationSettlement",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Approved",
       "bindsTo": "CommissionCalculationSettlementManagementSummary.approved",
       "operation": "listCommissionCalculationSettlement",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "On Hold",
       "bindsTo": "CommissionCalculationSettlementManagementSummary.onHold",
       "operation": "listCommissionCalculationSettlement",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Paid",
       "bindsTo": "CommissionCalculationSettlementManagementSummary.paid",
       "operation": "listCommissionCalculationSettlement",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Reversed",
       "bindsTo": "CommissionCalculationSettlementManagementSummary.reversed",
       "operation": "listCommissionCalculationSettlement",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Incentives Earned",
       "bindsTo": "CommissionCalculationSettlementManagementSummary.incentivesEarned",
       "operation": "listCommissionCalculationSettlement",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Next Settlement date",
       "bindsTo": "CommissionCalculationSettlementManagementSummary.nextSettlement",
       "operation": "listCommissionCalculationSettlement",
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
       "label": "Every commission calculation settlement",
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
       "notes": "The pack groups this record's detail under its own headings: “For each transaction”, “Automatically account for”, “Exception states”, “Settlement Batch”, “Important Boundary”.",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 54 §Display"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Per Transaction",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 54 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Act on partner commission line",
       "operation": "actOnPartnerCommissionLine",
       "permission": "SETTLEMENT_RECONCILE",
       "notes": "The line actions on PTR-048 (decided 29 September, writers pass; DM4).",
       "provenance": "contract subscription.yaml POST /partner-commission-lines/{lineId}/actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Act on partner settlement batch",
       "operation": "actOnPartnerSettlementBatch",
       "permission": "SETTLEMENT_RECONCILE",
       "notes": "The batch actions on PTR-048 (decided 29 September, writers pass; DM4).",
       "provenance": "contract subscription.yaml POST /partner-settlement-batches/{batchId}/actions"
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
   },
   {
    "operationId": "actOnPartnerCommissionLine",
    "contract": "subscription",
    "purpose": "Hold, release, dispute or reverse a single commission line",
    "trigger": "onAction",
    "invalidates": [
     "listCommissionCalculationSettlement"
    ]
   },
   {
    "operationId": "actOnPartnerSettlementBatch",
    "contract": "subscription",
    "purpose": "Move a commission settlement batch through Finance",
    "trigger": "onAction",
    "invalidates": [
     "listCommissionCalculationSettlement"
    ]
   }
  ],
  "entryState": {
   "preloaded": [
    "CommissionCalculationSettlementManagementSummary.commissionEarned",
    "CommissionCalculationSettlementManagementSummary.commissionPending",
    "CommissionCalculationSettlementManagementSummary.approved",
    "CommissionCalculationSettlementManagementSummary.onHold",
    "CommissionCalculationSettlementManagementSummary.paid",
    "CommissionCalculationSettlementManagementSummary.reversed"
   ],
   "params": [
    {
     "name": "lineId",
     "from": "navigation",
     "optional": true
    },
    {
     "name": "batchId",
     "from": "navigation",
     "optional": true
    }
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P10 Partner Web.dc.html#ptr-048",
   "workshopBoard": "wireframes/WS40 B2B, Reseller & OTA Partner Management Board 3.dc.html#ptr-048"
  },
  "apisNote": "Regenerated 9 September 2026 from B2B, Reseller & OTA Partner Management_Reference.pdf page 54. 8 of 8 labels bound to a contract property; 9 of 42 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "overlays": [
   {
    "id": "formActOnPartnerCommissionLine",
    "component": "modal",
    "trigger": "Act on partner commission line",
    "body": "**Collects what `actOnPartnerCommissionLine` sends before it is called.** Required: `action`. Optional: `reason`, `caseId`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Act on partner commission line",
     "operation": "actOnPartnerCommissionLine"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "action",
      "reason",
      "caseId"
     ]
    },
    "provenance": "contract subscription.yaml POST /partner-commission-lines/{lineId}/actions"
   },
   {
    "id": "formActOnPartnerSettlementBatch",
    "component": "modal",
    "trigger": "Act on partner settlement batch",
    "body": "**Collects what `actOnPartnerSettlementBatch` sends before it is called.** Required: `action`. Optional: `scheduledDate`, `reason`, `caseId`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Act on partner settlement batch",
     "operation": "actOnPartnerSettlementBatch"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "action",
      "scheduledDate",
      "reason",
      "caseId"
     ]
    },
    "provenance": "contract subscription.yaml POST /partner-settlement-batches/{batchId}/actions"
   }
  ],
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
  "purposeNote": "Every partner dispute has a traceable owner, SLA, supporting evidence, financial context and documented resolution.",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Monitor) and no metric row",
  "purpose": "Provide a structured case-management environment for partner operational and commercial disputes.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 8 actions on this screen; 6 are served since the writers pass (29 September): Booking Dispute, Pricing Dispute, Credit Dispute, Ticket Issue, Allocation Issue, API Issue by `createPartnerCase`.** Still unserved: Finance review, Technical review. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
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
       "label": "Credit Dispute",
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
       "label": "API Issue",
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
      },
      {
       "kind": "secondaryButton",
       "label": "Create partner case",
       "operation": "createPartnerCase",
       "permission": "CASE_MANAGE",
       "notes": "Raised from PTR-049 by staff or by the partner (decided 29 September, writers pass; DM4).",
       "provenance": "contract subscription.yaml POST /partner-cases"
      },
      {
       "kind": "secondaryButton",
       "label": "Act on partner case",
       "operation": "actOnPartnerCase",
       "permission": "CASE_MANAGE",
       "provenance": "contract subscription.yaml POST /partner-cases/{caseId}/actions"
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
   },
   {
    "operationId": "createPartnerCase",
    "contract": "subscription",
    "purpose": "Open a partner dispute or service case",
    "trigger": "onAction",
    "invalidates": [
     "listPartnerDisputeCase"
    ]
   },
   {
    "operationId": "actOnPartnerCase",
    "contract": "subscription",
    "purpose": "Work a partner case",
    "trigger": "onAction",
    "invalidates": [
     "listPartnerDisputeCase"
    ]
   }
  ],
  "entryState": {
   "preloaded": [
    "PartnerDisputesCasesServiceManagementView.firstResponse",
    "PartnerDisputesCasesServiceManagementView.resolutionTarget",
    "PartnerDisputesCasesServiceManagementView.timeOpen",
    "PartnerDisputesCasesServiceManagementView.slaBreach"
   ],
   "params": [
    {
     "name": "caseId",
     "from": "navigation"
    }
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P10 Partner Web.dc.html#ptr-049",
   "workshopBoard": "wireframes/WS40 B2B, Reseller & OTA Partner Management Board 3.dc.html#ptr-049"
  },
  "apisNote": "Regenerated 9 September 2026 from B2B, Reseller & OTA Partner Management_Reference.pdf page 56. 4 of 4 labels bound to a contract property; 27 of 45 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "overlays": [
   {
    "id": "formCreatePartnerCase",
    "component": "modal",
    "trigger": "Create partner case",
    "body": "**Collects what `createPartnerCase` sends before it is called.** Required: `id`, `partnerId`, `category`, `priority`, `description`, `status`, `resolutionTargetAt`. Optional: `contactId`, `orderId`, `invoiceReference`, `settlementBatchId`, `amountInDispute`, `evidence`, `ownerPrincipalId`, `slaPolicyId`, `firstResponseAt`, `resolvedAt`, `scopePath`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "PartnerCase",
    "confirm": {
     "label": "Create partner case",
     "operation": "createPartnerCase"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "partnerId",
      "category",
      "priority",
      "description",
      "status",
      "resolutionTargetAt",
      "contactId",
      "orderId",
      "invoiceReference",
      "settlementBatchId",
      "amountInDispute",
      "evidence",
      "ownerPrincipalId",
      "slaPolicyId",
      "firstResponseAt",
      "resolvedAt",
      "scopePath"
     ]
    },
    "provenance": "contract subscription.yaml POST /partner-cases"
   },
   {
    "id": "formActOnPartnerCase",
    "component": "modal",
    "trigger": "Act on partner case",
    "body": "**Collects what `actOnPartnerCase` sends before it is called.** Required: `action`. Optional: `ownerPrincipalId`, `resolution`, `reason`, `note`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Act on partner case",
     "operation": "actOnPartnerCase"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "action",
      "ownerPrincipalId",
      "resolution",
      "reason",
      "note"
     ]
    },
    "provenance": "contract subscription.yaml POST /partner-cases/{caseId}/actions"
   }
  ],
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
  "purposeNote": "Management can objectively compare partners and identify commercial, operational or financial deterioration before it becomes a material issue.",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Show) and no metric row",
  "purpose": "Create a consistent scorecard for evaluating the quality and commercial value of every partner relationship.",
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
        "PartnerPerformanceScorecardRiskMonitoringView.trend"
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
        "PartnerPerformanceScorecardRiskMonitoringView.trend"
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
    "PartnerPerformanceScorecardRiskMonitoringView.trend"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P10 Partner Web.dc.html#ptr-050",
   "workshopBoard": "wireframes/WS40 B2B, Reseller & OTA Partner Management Board 3.dc.html#ptr-050"
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
  "purposeNote": "Management receives explainable partner-level intelligence and scenario modelling that supports growth, margin, allocation and risk decisions without bypassing commercial governance. Board 3 — Final Screen Register Screen Backend Screen Primary Responsibility 8.3.1 Partner Operations Command Center Live partner operations 8.3.2 Partner Orders & Booking Management Partner transactions",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Analyze) and no metric row",
  "purpose": "Provide TICVAI's AI decision-support layer across the complete partner lifecycle. This screen should combine information from Boards 1, 2 and 3.",
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
        "PartnerAiIntelligenceRelationshipOptimizationView.inputsConsidered"
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
        "PartnerAiIntelligenceRelationshipOptimizationView.inputsConsidered"
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
    "PartnerAiIntelligenceRelationshipOptimizationView.inputsConsidered"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P10 Partner Web.dc.html#ptr-051",
   "workshopBoard": "wireframes/WS40 B2B, Reseller & OTA Partner Management Board 3.dc.html#ptr-051"
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
 "actOnPartnerCase": {
  "method": "POST",
  "path": "/partner-cases/{caseId}/actions",
  "contract": "subscription",
  "summary": "Work a partner case",
  "permission": "CASE_MANAGE",
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
  "requestBody": null,
  "responds": "PartnerCase"
 },
 "actOnPartnerCommissionLine": {
  "method": "POST",
  "path": "/partner-commission-lines/{lineId}/actions",
  "contract": "subscription",
  "summary": "Hold, release, dispute or reverse a single commission line",
  "permission": "SETTLEMENT_RECONCILE",
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
  "requestBody": null,
  "responds": "PartnerCommissionLine"
 },
 "actOnPartnerReconciliationException": {
  "method": "POST",
  "path": "/partner-reconciliation-exceptions/{exceptionId}/actions",
  "contract": "subscription",
  "summary": "Work a partner reconciliation exception",
  "permission": "SETTLEMENT_RECONCILE",
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
  "requestBody": null,
  "responds": "PartnerReconciliationException"
 },
 "actOnPartnerSettlementBatch": {
  "method": "POST",
  "path": "/partner-settlement-batches/{batchId}/actions",
  "contract": "subscription",
  "summary": "Move a commission settlement batch through Finance",
  "permission": "SETTLEMENT_RECONCILE",
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
  "requestBody": null,
  "responds": "PartnerSettlementBatch"
 },
 "createPartnerCase": {
  "method": "POST",
  "path": "/partner-cases",
  "contract": "subscription",
  "summary": "Open a partner dispute or service case",
  "permission": "CASE_MANAGE",
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
  "requestBody": "PartnerCase",
  "responds": "PartnerCase"
 },
 "createPartnerChangeRequest": {
  "method": "POST",
  "path": "/partner-change-requests",
  "contract": "subscription",
  "summary": "A partner asks to cancel or amend a booking",
  "permission": "ORDER_MODIFY",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   },
   {
    "name": "dryRun",
    "in": "query",
    "required": false
   }
  ],
  "requestBody": "PartnerChangeRequestInput",
  "responds": "PartnerChangeRequest"
 },
 "listCommissionCalculationSettlement": {
  "method": "GET",
  "path": "/commission-calculation-settlement",
  "contract": "subscription",
  "summary": "Commission Calculation & Settlement Management",
  "permission": "PLATFORM_TENANT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": "partnerId",
    "in": "query",
    "required": false
   },
   {
    "name": "status",
    "in": "query",
    "required": false
   },
   {
    "name": "period",
    "in": "query",
    "required": false
   },
   {
    "name": "settlementBatchId",
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
 "listPartner": {
  "method": "GET",
  "path": "/partner",
  "contract": "subscription",
  "summary": "Partner Management Command Center",
  "permission": "PLATFORM_TENANT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": "brand",
    "in": "query",
    "required": false
   },
   {
    "name": "venue",
    "in": "query",
    "required": false
   },
   {
    "name": "accountManager",
    "in": "query",
    "required": false
   },
   {
    "name": "status",
    "in": "query",
    "required": false
   },
   {
    "name": "risk",
    "in": "query",
    "required": false
   },
   {
    "name": "integrationType",
    "in": "query",
    "required": false
   },
   {
    "name": "partnerType",
    "in": "query",
    "required": false
   },
   {
    "name": "country",
    "in": "query",
    "required": false
   },
   {
    "name": "territory",
    "in": "query",
    "required": false
   },
   {
    "name": "agreementStatus",
    "in": "query",
    "required": false
   },
   {
    "name": "creditStatus",
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
    "name": "partnerId",
    "in": "query",
    "required": false
   },
   {
    "name": "partnerType",
    "in": "query",
    "required": false
   },
   {
    "name": "accountManager",
    "in": "query",
    "required": false
   },
   {
    "name": "operationalStatus",
    "in": "query",
    "required": false
   },
   {
    "name": "risk",
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
 "listPartnerCancellationRefund": {
  "method": "GET",
  "path": "/partner-cancellation-refund",
  "contract": "subscription",
  "summary": "Partner Cancellations, Refunds & Amendments",
  "permission": "PLATFORM_TENANT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": "partnerId",
    "in": "query",
    "required": false
   },
   {
    "name": "requestType",
    "in": "query",
    "required": false
   },
   {
    "name": "status",
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
 "listPartnerDisputeCase": {
  "method": "GET",
  "path": "/partner-dispute-case",
  "contract": "subscription",
  "summary": "Partner Disputes, Cases & Service Management",
  "permission": "PLATFORM_TENANT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": "partnerId",
    "in": "query",
    "required": false
   },
   {
    "name": "category",
    "in": "query",
    "required": false
   },
   {
    "name": "status",
    "in": "query",
    "required": false
   },
   {
    "name": "priority",
    "in": "query",
    "required": false
   },
   {
    "name": "owner",
    "in": "query",
    "required": false
   },
   {
    "name": "slaBreach",
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
   },
   {
    "name": "status",
    "in": "query",
    "required": false
   },
   {
    "name": "agent",
    "in": "query",
    "required": false
   },
   {
    "name": "channel",
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
 "listPartnerPerformanceScorecard": {
  "method": "GET",
  "path": "/partner-performance-scorecard",
  "contract": "subscription",
  "summary": "Partner Performance Scorecard & Risk Monitoring",
  "permission": "PLATFORM_TENANT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": "partnerId",
    "in": "query",
    "required": false
   },
   {
    "name": "partnerType",
    "in": "query",
    "required": false
   },
   {
    "name": "market",
    "in": "query",
    "required": false
   },
   {
    "name": "riskRating",
    "in": "query",
    "required": false
   },
   {
    "name": "trend",
    "in": "query",
    "required": false
   },
   {
    "name": "period",
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
 "listPartnerReconciliationException": {
  "method": "GET",
  "path": "/partner-reconciliation-exception",
  "contract": "subscription",
  "summary": "Partner Reconciliation & Exception Management",
  "permission": "PLATFORM_TENANT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": "partnerId",
    "in": "query",
    "required": false
   },
   {
    "name": "mismatchType",
    "in": "query",
    "required": false
   },
   {
    "name": "status",
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
 "listPartnerRelationship": {
  "method": "GET",
  "path": "/partner-relationship",
  "contract": "subscription",
  "summary": "Partner AI Intelligence & Relationship Optimization",
  "permission": "PLATFORM_TENANT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": "partnerId",
    "in": "query",
    "required": false
   },
   {
    "name": "category",
    "in": "query",
    "required": false
   },
   {
    "name": "opportunityClass",
    "in": "query",
    "required": false
   },
   {
    "name": "status",
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
 "listPartnerStatementAccount": {
  "method": "GET",
  "path": "/partner-statement-account",
  "contract": "subscription",
  "summary": "Partner Statement & Account Activity",
  "permission": "PLATFORM_TENANT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": "partnerId",
    "in": "query",
    "required": false
   },
   {
    "name": "period",
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
    "name": "transactionType",
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
 "listReservationHoldRelease": {
  "method": "GET",
  "path": "/reservation-hold-release",
  "contract": "subscription",
  "summary": "Reservations, Holds & Release Management",
  "permission": "PLATFORM_TENANT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": "partnerId",
    "in": "query",
    "required": false
   },
   {
    "name": "event",
    "in": "query",
    "required": false
   },
   {
    "name": "status",
    "in": "query",
    "required": false
   },
   {
    "name": "expiringBefore",
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
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "CommissionCalculationSettlementManagementSummary": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection; the headline tiles over the list, computed at read time for the filters in force",
  "description": "**The headline figures on Commission Calculation & Settlement Management.** The pack's KPI cards, split out of the row (decided 29 September, readiness close-out): a count describes the list, not each item in it.",
  "properties": {
   "commissionEarned": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Commission Earned"
   },
   "commissionPending": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Commission Pending"
   },
   "approved": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Approved"
   },
   "onHold": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "On Hold"
   },
   "paid": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Paid"
   },
   "reversed": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Reversed"
   },
   "incentivesEarned": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Incentives Earned"
   },
   "nextSettlement": {
    "type": "string",
    "format": "date",
    "description": "Next Settlement date",
    "nullable": true
   }
  }
 },
 "CommissionCalculationSettlementManagementView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over control.partner_commission_line (PartnerCommissionLine) and control.partner_settlement_batch and the existing subscription state, assembled at read time (data model DM4)",
  "description": "**What Commission Calculation & Settlement Management displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "orderNumber": {
    "type": "string",
    "description": "Order number"
   },
   "partner": {
    "type": "string",
    "description": "Partner trading name"
   },
   "product": {
    "type": "string",
    "description": "Product"
   },
   "grossValue": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Gross Value"
   },
   "netRate": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Net Rate"
   },
   "commissionBasis": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Commission Basis"
   },
   "commissionPercent": {
    "type": "number",
    "description": "Commission %",
    "nullable": true
   },
   "commissionAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Commission Amount"
   },
   "incentive": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Incentive"
   },
   "adjustment": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Adjustment"
   },
   "payableAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Payable Amount"
   },
   "period": {
    "type": "string",
    "description": "Settlement period label, e.g. 2026-09"
   },
   "legalEntity": {
    "type": "string",
    "description": "Legal Entity"
   },
   "lineId": {
    "type": "string",
    "format": "uuid",
    "description": "Calculation line id"
   },
   "orderId": {
    "type": "string",
    "format": "uuid",
    "description": "Order"
   },
   "partnerId": {
    "type": "string",
    "format": "uuid",
    "description": "Partner"
   },
   "agreementVersion": {
    "type": "integer",
    "description": "Agreement version in force at the time of the sale"
   },
   "settlementPeriod": {
    "type": "string",
    "enum": [
     "perTransaction",
     "weekly",
     "monthly",
     "eventBased",
     "customCycle"
    ],
    "description": "Settlement Period"
   },
   "adjustmentReason": {
    "type": "string",
    "enum": [
     "cancellation",
     "refund",
     "chargeback",
     "partialFulfillment",
     "commissionCorrection",
     "incentiveQualification"
    ],
    "description": "Adjustment reason",
    "nullable": true
   },
   "status": {
    "type": "string",
    "description": "Settlement status: calculated, reconciled, financeReview, approved, scheduled, paid, onHold, disputed, reversed"
   },
   "settlementBatchId": {
    "type": "string",
    "description": "Settlement batch",
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
 "PartnerAgreementStatus": {
  "type": "string",
  "enum": [
   "pendingApproval",
   "active",
   "expiringSoon",
   "expired",
   "suspended",
   "terminated"
  ]
 },
 "PartnerAiIntelligenceRelationshipOptimizationView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over subscription state, assembled at read time from tables that already exist",
  "description": "**What Partner AI Intelligence & Relationship Optimization displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
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
    "type": "number",
    "description": "Confidence, 0-1"
   },
   "risks": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Risks"
   },
   "supportingMetrics": {
    "type": "array",
    "description": "Supporting Metrics",
    "items": {
     "type": "object",
     "properties": {
      "name": {
       "type": "string"
      },
      "value": {
       "type": "string"
      }
     }
    }
   },
   "recommendationId": {
    "type": "string",
    "format": "uuid",
    "description": "Recommendation id"
   },
   "partnerId": {
    "type": "string",
    "format": "uuid",
    "description": "Partner"
   },
   "partner": {
    "type": "string",
    "description": "Partner trading name"
   },
   "category": {
    "type": "string",
    "enum": [
     "commercial",
     "allocation",
     "credit",
     "risk",
     "growth"
    ],
    "description": "Recommendation category"
   },
   "opportunityClass": {
    "type": "string",
    "enum": [
     "grow",
     "maintain",
     "review",
     "restrict"
    ],
    "description": "Partner Opportunity Matrix class, from configurable business criteria"
   },
   "inputsConsidered": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "partnerProfile",
      "territory",
      "agreements",
      "rates",
      "commission",
      "credit",
      "paymentBehavior",
      "allocation",
      "orders",
      "cancellations",
      "settlement",
      "cases",
      "channelPerformance",
      "historicalTrends"
     ]
    },
    "description": "AI Inputs the recommendation drew on"
   },
   "scenarioEstimate": {
    "type": "object",
    "nullable": true,
    "description": "Scenario Simulation estimate, where the recommendation carries one",
    "properties": {
     "additionalSales": {
      "type": "integer"
     },
     "revenue": {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     },
     "margin": {
      "type": "number"
     },
     "creditExposure": {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     },
     "inventoryRisk": {
      "type": "string"
     }
    }
   },
   "status": {
    "type": "string",
    "description": "Recommendation status: open, accepted, modified, rejected, assigned"
   },
   "createdAt": {
    "type": "string",
    "format": "date-time",
    "description": "Generated at"
   }
  }
 },
 "PartnerCancellationsRefundsAmendmentsView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over control.partner_change_request (PartnerChangeRequest) and the existing subscription state, assembled at read time (data model DM4)",
  "description": "**What Partner Cancellations, Refunds & Amendments displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "originalState": {
    "type": "string",
    "description": "Audit: original state of the booking (summary)"
   },
   "newState": {
    "type": "string",
    "description": "Audit: new state of the booking (summary)",
    "nullable": true
   },
   "requestedBy": {
    "type": "string",
    "description": "Audit: requesting user"
   },
   "reason": {
    "type": "string",
    "description": "Reason"
   },
   "financialImpact": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Financial impact (net change to the partner account)"
   },
   "approvedBy": {
    "type": "string",
    "description": "Approved by",
    "nullable": true
   },
   "requestId": {
    "type": "string",
    "format": "uuid",
    "description": "Amendment request id"
   },
   "partnerId": {
    "type": "string",
    "format": "uuid",
    "description": "Partner"
   },
   "partner": {
    "type": "string",
    "description": "Partner trading name"
   },
   "orderId": {
    "type": "string",
    "format": "uuid",
    "description": "Order"
   },
   "orderNumber": {
    "type": "string",
    "description": "Order number"
   },
   "requestType": {
    "type": "string",
    "enum": [
     "fullCancellation",
     "partialCancellation",
     "dateChange",
     "performanceChange",
     "quantityReduction",
     "productChange",
     "ticketReissue",
     "customerNameChange",
     "refundRequest"
    ],
    "description": "Request type"
   },
   "quantity": {
    "type": "integer",
    "description": "Tickets affected",
    "nullable": true
   },
   "originalValue": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Original Value"
   },
   "cancellationAllowed": {
    "type": "boolean",
    "description": "Cancellation/change allowed under the evaluated policy"
   },
   "cancellationFee": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Cancellation Fee"
   },
   "refundOrCredit": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Refund/Credit to the partner"
   },
   "allocationImpact": {
    "type": "integer",
    "description": "Allocation impact, units returned (+) or taken (-)"
   },
   "commissionAdjustment": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Commission Adjustment"
   },
   "approvalReasons": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "transactionValue",
      "eventProximity",
      "cancellationPercentage",
      "partnerStatus",
      "exceptionRequest"
     ]
    },
    "description": "Why approval is required; empty when none"
   },
   "status": {
    "type": "string",
    "description": "Status: requested, pendingApproval, approved, rejected, processed"
   },
   "requestedAt": {
    "type": "string",
    "format": "date-time",
    "description": "Requested at"
   },
   "aiInsights": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Advisory AI unusual-cancellation-pattern flags"
   }
  }
 },
 "PartnerCase": {
  "type": "object",
  "x-ticvai-persistence": "control.partner_case",
  "description": "A partner dispute or service case: category, priority, what it relates to, the amount in dispute, the evidence, the owner and the SLA. Partner cases stay apart from `marketing.case`, which is a guest's service case with a guest lifecycle (decided 29 September, data model DM4)\n\n**Written by** createPartnerCase and actOnPartnerCase (assign, investigate, wait on the partner or a team, propose, accept or reject a resolution, reopen, close) (decided 29 September, writers pass; DM4).",
  "required": [
   "id",
   "partnerId",
   "category",
   "priority",
   "description",
   "status",
   "resolutionTargetAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "partnerId": {
    "type": "string",
    "format": "uuid",
    "description": "The partner (control.partner)."
   },
   "contactId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Partner contact (control.partner_contact)."
   },
   "category": {
    "type": "string",
    "enum": [
     "bookingDispute",
     "pricingDispute",
     "commissionDispute",
     "creditDispute",
     "invoiceDispute",
     "cancellationDispute",
     "ticketIssue",
     "allocationIssue",
     "apiIssue",
     "settlementDispute"
    ],
    "description": "Category."
   },
   "priority": {
    "type": "string",
    "enum": [
     "low",
     "medium",
     "high",
     "urgent"
    ],
    "description": "Priority (decided 29 September, readiness close-out)."
   },
   "orderId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Related order (orders.sales_order)."
   },
   "invoiceReference": {
    "type": "string",
    "nullable": true,
    "description": "Related invoice number."
   },
   "settlementBatchId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Related settlement (control.partner_settlement_batch)."
   },
   "amountInDispute": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "nullable": true,
    "description": "Amount in dispute."
   },
   "description": {
    "type": "string",
    "description": "Description."
   },
   "evidence": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Evidence: attachment references."
   },
   "ownerPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Owner, a staff principal."
   },
   "slaPolicyId": {
    "x-ticvai-references": "approvals.sla_policy",
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The SLA policy applied (approvals.sla_policy, the approvals engine's ApprovalSlaPolicy), which sets the first-response and resolution targets and the reminder/breach behaviour; `resolutionTargetAt` is computed from it when the case is opened. Replaces the free-text `slaPolicy` (decided 29 September, writers pass; DM4)"
   },
   "status": {
    "type": "string",
    "enum": [
     "open",
     "assigned",
     "investigating",
     "waitingPartner",
     "waitingInternal",
     "resolutionProposed",
     "resolved",
     "closed"
    ],
    "default": "open",
    "readOnly": true,
    "description": "Status (states/partner-case.yaml). Created `open` by createPartnerCase and moved only by actOnPartnerCase (decided 29 September, writers pass; DM4)"
   },
   "firstResponseAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "description": "First response at."
   },
   "resolutionTargetAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true,
    "description": "Resolution target, computed from the SLA policy (`slaPolicyId`) when the case is opened; time in `waitingPartner` extends it (decided 29 September, writers pass; DM4)"
   },
   "resolvedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "description": "Resolved at."
   },
   "scopePath": {
    "type": "string",
    "description": "The partition key (ADR-0005), written at `tenant` scope."
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
 "PartnerChangeRequest": {
  "type": "object",
  "x-ticvai-persistence": "control.partner_change_request",
  "description": "A partner's request to cancel or amend a booking, with the outcome the policy evaluated: whether it is allowed, the fee, the refund or credit, and the allocation and commission impact. A refund it produces is an `orders.refund`; this row is the request and its evaluation (decided 29 September, data model DM4)\n\n**Written by** createPartnerChangeRequest, which creates the row and evaluates it against policy in the same call; approval, where needed, is decided in approvals and the order change is carried out in orders (decided 29 September, writers pass; DM4).",
  "required": [
   "id",
   "partnerId",
   "orderId",
   "requestType",
   "status",
   "requestedAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "partnerId": {
    "type": "string",
    "format": "uuid",
    "description": "The partner (control.partner)."
   },
   "orderId": {
    "type": "string",
    "format": "uuid",
    "description": "Order (orders.sales_order)."
   },
   "requestType": {
    "type": "string",
    "enum": [
     "fullCancellation",
     "partialCancellation",
     "dateChange",
     "performanceChange",
     "quantityReduction",
     "productChange",
     "ticketReissue",
     "customerNameChange",
     "refundRequest"
    ],
    "description": "Request type."
   },
   "quantity": {
    "type": "integer",
    "minimum": 0,
    "nullable": true,
    "description": "Tickets affected."
   },
   "reason": {
    "type": "string",
    "nullable": true,
    "description": "Reason."
   },
   "originalState": {
    "type": "string",
    "description": "Audit: original state of the booking (summary)."
   },
   "newState": {
    "type": "string",
    "nullable": true,
    "description": "Audit: new state of the booking (summary)."
   },
   "originalValue": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "nullable": true,
    "description": "Original value."
   },
   "cancellationAllowed": {
    "type": "boolean",
    "description": "Cancellation/change allowed under the evaluated policy."
   },
   "cancellationFee": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "nullable": true,
    "description": "Cancellation fee."
   },
   "refundOrCredit": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "nullable": true,
    "description": "Refund/credit to the partner."
   },
   "financialImpact": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "nullable": true,
    "description": "Net change to the partner account."
   },
   "allocationImpact": {
    "type": "integer",
    "nullable": true,
    "description": "Allocation impact, units returned (+) or taken (-)."
   },
   "commissionAdjustment": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "nullable": true,
    "description": "Commission adjustment."
   },
   "approvalReasons": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "transactionValue",
      "eventProximity",
      "cancellationPercentage",
      "partnerStatus",
      "exceptionRequest"
     ]
    },
    "description": "Why approval is required; empty when none."
   },
   "status": {
    "type": "string",
    "enum": [
     "requested",
     "pendingApproval",
     "approved",
     "rejected",
     "processed"
    ],
    "default": "requested",
    "description": "Status."
   },
   "requestedByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "description": "Requesting user."
   },
   "approvedByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Approver."
   },
   "approvalRequestId": {
    "type": "string",
    "nullable": true,
    "readOnly": true,
    "description": "Approval request, when one was needed."
   },
   "refundId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The refund it produced (orders.refund), once processed."
   },
   "requestedAt": {
    "type": "string",
    "format": "date-time",
    "description": "Requested at."
   },
   "targetPerformanceId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The performance (catalogue.performance) asked for, for dateChange and performanceChange (decided 29 September, writers pass; DM4)"
   },
   "targetProductId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The product (catalogue.product) asked for, for productChange (decided 29 September, writers pass; DM4)"
   },
   "newCustomerName": {
    "type": "string",
    "nullable": true,
    "description": "The name asked for, for customerNameChange (decided 29 September, writers pass; DM4)"
   },
   "feeWaiverRequested": {
    "type": "boolean",
    "default": false,
    "description": "The partner asks for the cancellation fee to be waived; a waiver always needs approval (`approvalReasons` gains exceptionRequest) (decided 29 September, writers pass; DM4)"
   },
   "scopePath": {
    "type": "string",
    "description": "The partition key (ADR-0005), written at `tenant` scope."
   },
   "updatedAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   }
  }
 },
 "PartnerChangeRequestInput": {
  "type": "object",
  "x-ticvai-persistence": "none — request only; stored as control.partner_change_request (PartnerChangeRequest) with its evaluation (decided 29 September, writers pass; DM4)",
  "description": "What a partner sends to cancel or amend a booking (createPartnerChangeRequest). The evaluation (allowed, fee, refund, impacts, status) is computed, never sent (decided 29 September, writers pass; DM4)",
  "required": [
   "orderId",
   "requestType"
  ],
  "properties": {
   "orderId": {
    "type": "string",
    "format": "uuid",
    "description": "The partner's order (orders.sales_order)"
   },
   "requestType": {
    "type": "string",
    "enum": [
     "fullCancellation",
     "partialCancellation",
     "dateChange",
     "performanceChange",
     "quantityReduction",
     "productChange",
     "ticketReissue",
     "customerNameChange",
     "refundRequest"
    ]
   },
   "quantity": {
    "type": "integer",
    "minimum": 1,
    "nullable": true,
    "description": "Tickets affected; required for partialCancellation and quantityReduction"
   },
   "targetPerformanceId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Required for dateChange and performanceChange"
   },
   "targetProductId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Required for productChange"
   },
   "newCustomerName": {
    "type": "string",
    "nullable": true,
    "description": "Required for customerNameChange"
   },
   "feeWaiverRequested": {
    "type": "boolean",
    "default": false
   },
   "reason": {
    "type": "string",
    "nullable": true
   }
  }
 },
 "PartnerCommissionLine": {
  "type": "object",
  "x-ticvai-persistence": "control.partner_commission_line",
  "description": "The commission calculated on one partner order under the agreement version in force at the sale, and where it stands in settlement. Amounts are in the agreement's settlement currency (decided 29 September, data model DM4)\n\n**Rows are created by the commission calculation job** when a partner order is confirmed (and a correcting line when one is cancelled or refunded); no operation creates one by hand. A single line is held, released, disputed or reversed with actOnPartnerCommissionLine; a line in a batch otherwise moves with actOnPartnerSettlementBatch (decided 29 September, writers pass; DM4).",
  "required": [
   "id",
   "partnerId",
   "agreementId",
   "agreementVersion",
   "orderId",
   "status"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "partnerId": {
    "type": "string",
    "format": "uuid",
    "description": "The partner (control.partner)."
   },
   "agreementId": {
    "type": "string",
    "format": "uuid",
    "description": "The agreement (control.partner_agreement) this row belongs to."
   },
   "agreementVersion": {
    "type": "integer",
    "description": "Agreement version in force at the time of the sale."
   },
   "orderId": {
    "type": "string",
    "format": "uuid",
    "description": "Order (orders.sales_order)."
   },
   "productId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Product (catalogue.product)."
   },
   "grossValue": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Gross value."
   },
   "netRate": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "nullable": true,
    "description": "Net rate."
   },
   "commissionBasis": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Commission basis."
   },
   "commissionPercent": {
    "type": "number",
    "nullable": true,
    "description": "Commission percent."
   },
   "commissionAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Commission amount."
   },
   "incentive": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "nullable": true,
    "description": "Incentive."
   },
   "adjustment": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "nullable": true,
    "description": "Adjustment."
   },
   "adjustmentReason": {
    "type": "string",
    "enum": [
     "cancellation",
     "refund",
     "chargeback",
     "partialFulfillment",
     "commissionCorrection",
     "incentiveQualification"
    ],
    "nullable": true,
    "description": "Adjustment reason."
   },
   "payableAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Payable amount."
   },
   "settlementPeriod": {
    "type": "string",
    "enum": [
     "perTransaction",
     "weekly",
     "monthly",
     "eventBased",
     "customCycle"
    ],
    "description": "Settlement period."
   },
   "period": {
    "type": "string",
    "description": "Settlement period label, e.g. 2026-09."
   },
   "legalEntityId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Legal entity (ledger.legal_entity)."
   },
   "status": {
    "type": "string",
    "enum": [
     "calculated",
     "reconciled",
     "financeReview",
     "approved",
     "scheduled",
     "paid",
     "onHold",
     "disputed",
     "reversed"
    ],
    "default": "calculated",
    "description": "Settlement status."
   },
   "settlementBatchId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Settlement batch (control.partner_settlement_batch)."
   },
   "scopePath": {
    "type": "string",
    "description": "The partition key (ADR-0005), written at `tenant` scope."
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
 "PartnerDisputesCasesServiceManagementView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over control.partner_case (PartnerCase) and the existing subscription state, assembled at read time (data model DM4)",
  "description": "**What Partner Disputes, Cases & Service Management displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "caseId": {
    "type": "string",
    "description": "Case ID"
   },
   "partner": {
    "type": "string",
    "description": "Partner trading name"
   },
   "contact": {
    "type": "string",
    "description": "Partner contact",
    "nullable": true
   },
   "category": {
    "type": "string",
    "enum": [
     "bookingDispute",
     "pricingDispute",
     "commissionDispute",
     "creditDispute",
     "invoiceDispute",
     "cancellationDispute",
     "ticketIssue",
     "allocationIssue",
     "apiIssue",
     "settlementDispute"
    ],
    "description": "Category (Case Types)"
   },
   "priority": {
    "type": "string",
    "enum": [
     "low",
     "medium",
     "high",
     "urgent"
    ],
    "description": "Priority (decided 29 September, readiness close-out)"
   },
   "relatedOrder": {
    "type": "string",
    "description": "Related Order",
    "nullable": true
   },
   "relatedInvoice": {
    "type": "string",
    "description": "Related Invoice",
    "nullable": true
   },
   "relatedSettlement": {
    "type": "string",
    "description": "Related Settlement",
    "nullable": true
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
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Evidence: attachment references"
   },
   "owner": {
    "type": "string",
    "description": "Owner",
    "nullable": true
   },
   "sla": {
    "type": "string",
    "description": "SLA policy applied"
   },
   "status": {
    "type": "string",
    "description": "Status: open, assigned, investigating, waitingPartner, waitingInternal, resolutionProposed, resolved, closed"
   },
   "firstResponse": {
    "type": "string",
    "format": "date-time",
    "description": "First Response at",
    "nullable": true
   },
   "resolutionTarget": {
    "type": "string",
    "format": "date-time",
    "description": "Resolution Target"
   },
   "timeOpen": {
    "type": "integer",
    "description": "Time Open, hours"
   },
   "slaBreach": {
    "type": "boolean",
    "description": "SLA Breach"
   },
   "partnerId": {
    "type": "string",
    "format": "uuid",
    "description": "Partner"
   },
   "aiSummary": {
    "type": "string",
    "description": "Advisory AI case summary",
    "nullable": true
   }
  }
 },
 "PartnerManagementCommandCenterSummary": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection; the headline tiles over the list, computed at read time for the filters in force",
  "description": "**The headline figures on Partner Management Command Center.** The pack's KPI cards, split out of the row (decided 29 September, readiness close-out): a count describes the list, not each item in it.",
  "properties": {
   "totalPartners": {
    "type": "integer",
    "description": "Total Partners"
   },
   "activePartners": {
    "type": "integer",
    "description": "Active Partners"
   },
   "pendingOnboarding": {
    "type": "integer",
    "description": "Pending Onboarding"
   },
   "pendingApproval": {
    "type": "integer",
    "description": "Pending Approval"
   },
   "suspendedPartners": {
    "type": "integer",
    "description": "Suspended Partners"
   },
   "expiringAgreements": {
    "type": "integer",
    "description": "Expiring Agreements: partners whose active agreement ends within its expiryAlertDays (default 30) (decided 29 September, readiness close-out)"
   },
   "documentationIssues": {
    "type": "integer",
    "description": "Documentation Issues: partners with a mandatory document missing, rejected, expiring or expired"
   },
   "partnersWithCreditHolds": {
    "type": "integer",
    "description": "Partners With Credit Holds: partners whose credit status is onHold or blocked"
   },
   "connectedOtaApiPartners": {
    "type": "integer",
    "description": "Connected OTA/API Partners"
   },
   "partnerSalesYtd": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Partner Sales YTD: gross value of partner orders this calendar year (decided 29 September, readiness close-out)"
   },
   "partnerRevenueYtd": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Partner Revenue YTD: partner sales net of commission this calendar year (decided 29 September, readiness close-out)"
   },
   "highRiskPartners": {
    "type": "integer",
    "description": "High-Risk Partners"
   }
  }
 },
 "PartnerManagementCommandCenterView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over control.partner (Partner), control.partner_credit_profile, control.partner_application, control.partner_scope_assignment and control.partner_distribution_right and the existing subscription state, assembled at read time (data model DM4)",
  "description": "**What Partner Management Command Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "partnerId": {
    "type": "string",
    "format": "uuid",
    "description": "Partner ID"
   },
   "tradingName": {
    "type": "string",
    "description": "Trading Name"
   },
   "legalEntity": {
    "type": "string",
    "description": "Legal Entity"
   },
   "partnerType": {
    "type": "string",
    "description": "Partner type code from the tenant's configurable partner-type list (MoM 31 Aug 4.3: configurable category/type), seeded with the pack's p.7 list: b2bReseller, travelAgent, tourOperator, ota, corporateCustomer, hotelConcierge, destinationManagementCompany, affiliate, wholesaler, distributor, governmentPartner, schoolInstitution, apiPartner, internalGroupCompany"
   },
   "country": {
    "type": "string",
    "description": "Country, ISO 3166-1 alpha-2"
   },
   "territory": {
    "type": "string",
    "description": "Territory: summary of the authorised markets (listTerritoryMarketDistribution)"
   },
   "assignedBrands": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Assigned Brand/Venue: brand names in the partner's business scope (setPartnerBrandVenue)"
   },
   "assignedVenues": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Assigned Brand/Venue: venue names in the partner's business scope (setPartnerBrandVenue)"
   },
   "commercialOwner": {
    "type": "string",
    "description": "Commercial Owner: staff display name of the account manager"
   },
   "distributionChannel": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "b2bPortal",
      "api",
      "otaConnection",
      "agentPortal",
      "affiliateLink",
      "voucherDistribution",
      "bulkTicketExport",
      "other"
     ]
    },
    "description": "Distribution Channel: Distribution methods: b2bPortal (the TICVAI B2B portal), api (partner consumes the TICVAI API), otaConnection (TICVAI integrates into the OTA, either direction per MoM 31 Aug 4.3), agentPortal, affiliateLink, voucherDistribution, bulkTicketExport (pre-generated QR tickets as CSV, MoM 5 Aug option 3), other"
   },
   "accountStatus": {
    "type": "string",
    "description": "Account Status: lead, applicant, underReview, approved, configuration, active, restricted, suspended, terminated or archived (pack p.6 and p.18 merged with MoM 31 Aug 4.3 lead -> submitted -> active -> suspended; \"submitted\" is applicant)"
   },
   "onboardingStatus": {
    "type": "string",
    "description": "Onboarding Status: the application stage (application, businessVerification, documentation, commercialReview, financeReview, technicalReview, approval, configuration, activation) or complete"
   },
   "agreementStatus": {
    "allOf": [
     {
      "$ref": "#/components/schemas/PartnerAgreementStatus"
     }
    ],
    "nullable": true,
    "description": "Agreement Status of the partner's current agreement; empty when none"
   },
   "creditStatus": {
    "type": "string",
    "description": "Credit Status: notEnabled, withinLimit, warning (at the warning threshold), highRisk, onHold or blocked (decided 29 September, readiness close-out)"
   },
   "integrationStatus": {
    "type": "string",
    "enum": [
     "none",
     "testing",
     "connected",
     "degraded",
     "disconnected"
    ],
    "x-ticvai-persisted": false,
    "description": "Integration Status: none, testing, connected, degraded or disconnected (decided 29 September, readiness close-out). **Derived at read time, not a column** (decided 29 September, writers pass; DM4), from the partner's OTA/API channel listings (control.channel_listing) and the health of its API clients (control.api_client, with webhook deliveries in control.webhook_delivery), first match wins: `none` when the partner has no channel listing and no API client; `disconnected` when every listing is `paused` or `delisted` or every production API client is `suspended` or `revoked`; `degraded` when a `live` listing's `lastPushedAt` is older than twice its `pushIntervalMinutes`, or webhook deliveries to the partner failed in the last hour; `connected` when a `live` listing or an `active` production client exists and none of the above holds; otherwise `testing` (only `draft` listings or only sandbox clients). The thresholds are proposed, the venue may correct them."
   },
   "lastActivity": {
    "type": "string",
    "format": "date-time",
    "description": "Last Activity"
   },
   "riskRating": {
    "type": "string",
    "enum": [
     "low",
     "medium",
     "high",
     "critical"
    ],
    "description": "Risk rating, Low / Medium / High / Critical (pack p.58); drives the Risk filter and the High-Risk Partners KPI"
   },
   "aiInsights": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Partner Attention Required: advisory AI flags such as an agreement expiring against forward bookings (pack p.6)"
   }
  }
 },
 "PartnerOperationsCommandCenterSummary": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection; the headline tiles over the list, computed at read time for the filters in force",
  "description": "**The headline figures on Partner Operations Command Center.** The pack's KPI cards, split out of the row (decided 29 September, readiness close-out): a count describes the list, not each item in it.",
  "properties": {
   "partnerSalesToday": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Partner Sales Today"
   },
   "partnerSalesMtd": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
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
    "type": "integer",
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
    "$ref": "../shared/common.yaml#/components/schemas/Money",
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
    "type": "integer",
    "description": "Partners Requiring Attention"
   },
   "activityFeed": {
    "type": "array",
    "description": "Activity Feed: recent partner events, newest first",
    "items": {
     "type": "object",
     "properties": {
      "at": {
       "type": "string",
       "format": "date-time"
      },
      "partnerId": {
       "type": "string",
       "format": "uuid"
      },
      "message": {
       "type": "string"
      }
     }
    }
   }
  }
 },
 "PartnerOperationsCommandCenterView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over subscription state, assembled at read time from tables that already exist",
  "description": "**What Partner Operations Command Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "partner": {
    "type": "string",
    "description": "Partner trading name"
   },
   "partnerType": {
    "type": "string",
    "description": "Partner Type code"
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
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Gross Sales"
   },
   "netSales": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
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
    "description": "Credit Utilization, percent"
   },
   "allocationUtilization": {
    "type": "number",
    "description": "Allocation Utilization, percent"
   },
   "cancellationRate": {
    "type": "number",
    "description": "Cancellation Rate, percent"
   },
   "operationalStatus": {
    "type": "string",
    "description": "Operational Status: normal, attention, restricted, suspended"
   },
   "risk": {
    "type": "string",
    "enum": [
     "low",
     "medium",
     "high",
     "critical"
    ],
    "description": "Risk"
   },
   "partnerId": {
    "type": "string",
    "format": "uuid",
    "description": "Partner"
   },
   "aiInsights": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Advisory AI attention flags for this partner"
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
   "customerName": {
    "type": "string",
    "description": "Customer/Guest where applicable",
    "nullable": true
   },
   "products": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Products"
   },
   "quantity": {
    "type": "integer",
    "description": "Quantity"
   },
   "grossValue": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Gross Value"
   },
   "partnerRate": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Partner Rate applied"
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
    "enum": [
     "creditAccount",
     "prepaid",
     "card"
    ],
    "description": "Payment Method (the three payment models)"
   },
   "billingStatus": {
    "type": "string",
    "description": "Billing Status: unbilled, invoiced, paid, overdue or credited"
   },
   "fulfillmentStatus": {
    "type": "string",
    "description": "Fulfillment Status: pending, partiallyIssued, issued or delivered"
   },
   "orderId": {
    "type": "string",
    "format": "uuid",
    "description": "TICVAI Order ID"
   },
   "orderNumber": {
    "type": "string",
    "description": "TICVAI order number"
   },
   "partnerId": {
    "type": "string",
    "format": "uuid",
    "description": "Partner"
   },
   "partnerName": {
    "type": "string",
    "description": "Partner"
   },
   "bookingDate": {
    "type": "string",
    "format": "date-time",
    "description": "Booking Date"
   },
   "event": {
    "type": "string",
    "description": "Event",
    "nullable": true
   },
   "visitDate": {
    "type": "string",
    "format": "date",
    "description": "Visit/Event Date",
    "nullable": true
   },
   "orderStatus": {
    "type": "string",
    "description": "Order status: draft, held, confirmed, partiallyFulfilled, fulfilled, cancelled, refunded, failed"
   },
   "salesChannel": {
    "$ref": "../shared/common.yaml#/components/schemas/SalesChannel",
    "description": "Channel"
   }
  }
 },
 "PartnerPerformanceScorecardRiskMonitoringView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over control.partner, control.partner_document, control.partner_security, control.partner_allocation and control.partner_case and the existing subscription state, assembled at read time (data model DM4)",
  "description": "**What Partner Performance Scorecard & Risk Monitoring displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "sales": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Commercial: gross sales"
   },
   "revenue": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Commercial: revenue net of commission"
   },
   "growth": {
    "type": "number",
    "description": "Commercial: growth against the previous period, percent"
   },
   "margin": {
    "type": "number",
    "description": "Commercial: margin, percent"
   },
   "averageOrderValue": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Commercial: average order value"
   },
   "utilization": {
    "type": "number",
    "description": "Allocation: utilisation, percent"
   },
   "sellThrough": {
    "type": "number",
    "description": "Allocation: sell-through, percent"
   },
   "returnedInventory": {
    "type": "integer",
    "description": "Allocation: returned inventory, units"
   },
   "averagePaymentDelayDays": {
    "type": "number",
    "description": "Financial: average payment delay, days"
   },
   "creditUtilization": {
    "type": "number",
    "description": "Financial: credit utilisation, percent"
   },
   "overdueBalance": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Financial: overdue balance"
   },
   "cancellationRate": {
    "type": "number",
    "description": "Operational: cancellation rate, percent"
   },
   "errorRate": {
    "type": "number",
    "description": "Operational: error rate, percent"
   },
   "supportCases": {
    "type": "integer",
    "description": "Operational: support cases"
   },
   "apiSuccessRate": {
    "type": "number",
    "description": "Technical: API success rate, percent",
    "nullable": true
   },
   "transactionFailureRate": {
    "type": "number",
    "description": "Technical: transaction failure rate, percent",
    "nullable": true
   },
   "documentation": {
    "type": "string",
    "description": "Compliance: documentation state, compliant, expiring, incomplete or nonCompliant"
   },
   "agreementStatus": {
    "allOf": [
     {
      "$ref": "#/components/schemas/PartnerAgreementStatus"
     }
    ],
    "nullable": true,
    "description": "Compliance: agreement status"
   },
   "securityGuaranteeStatus": {
    "type": "string",
    "description": "Compliance: security/guarantee state, covered, partiallyCovered, expired or notRequired"
   },
   "partnerId": {
    "type": "string",
    "format": "uuid",
    "description": "Partner"
   },
   "partner": {
    "type": "string",
    "description": "Partner trading name"
   },
   "partnerType": {
    "type": "string",
    "description": "Partner Type code"
   },
   "period": {
    "type": "string",
    "description": "Scorecard period, e.g. 2026-09"
   },
   "refundRate": {
    "type": "number",
    "description": "Operational: refund rate, percent"
   },
   "syncReliability": {
    "type": "number",
    "description": "Technical: sync reliability, percent",
    "nullable": true
   },
   "overallScore": {
    "type": "integer",
    "description": "Partner Score, 0-100"
   },
   "dimensionScores": {
    "type": "object",
    "description": "Score by dimension, each 0-100",
    "properties": {
     "commercial": {
      "type": "integer"
     },
     "financial": {
      "type": "integer"
     },
     "allocation": {
      "type": "integer"
     },
     "operational": {
      "type": "integer"
     },
     "technical": {
      "type": "integer"
     },
     "compliance": {
      "type": "integer"
     }
    }
   },
   "riskRating": {
    "type": "string",
    "enum": [
     "low",
     "medium",
     "high",
     "critical"
    ],
    "description": "Risk Rating"
   },
   "trend": {
    "type": "string",
    "enum": [
     "improving",
     "stable",
     "declining"
    ],
    "description": "Trend"
   },
   "benchmark": {
    "type": "object",
    "description": "Benchmarking: average overall score of the comparison groups",
    "properties": {
     "samePartnerType": {
      "type": "number"
     },
     "sameMarket": {
      "type": "number"
     },
     "sameChannel": {
      "type": "number"
     },
     "portfolioAverage": {
      "type": "number"
     }
    }
   },
   "aiInsights": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Advisory AI risk detection"
   }
  }
 },
 "PartnerReconciliationException": {
  "type": "object",
  "x-ticvai-persistence": "control.partner_reconciliation_exception",
  "description": "A mismatch found reconciling a partner's records with TICVAI's: the source compared, the two amounts, the type, and who is resolving it. The difference is the two amounts subtracted, not stored (decided 29 September, data model DM4)\n\n**Rows are created by the partner reconciliation job**, which compares the partner's file or statement with TICVAI's records and re-matches open rows on each run; no operation creates one by hand. An owner works it with actOnPartnerReconciliationException (decided 29 September, writers pass; DM4).",
  "required": [
   "id",
   "partnerId",
   "comparedSource",
   "mismatchType",
   "status"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "partnerId": {
    "type": "string",
    "format": "uuid",
    "description": "The partner (control.partner)."
   },
   "orderId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "TICVAI order (orders.sales_order), when one matched."
   },
   "partnerReference": {
    "type": "string",
    "nullable": true,
    "description": "Partner reference."
   },
   "comparedSource": {
    "type": "string",
    "enum": [
     "ticvaiOrders",
     "ticketsIssued",
     "partnerRates",
     "paymentsCredit",
     "commission",
     "invoices",
     "cancellationsRefunds"
    ],
    "description": "Reconciliation source the partner record was compared against."
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
    "description": "Exception type."
   },
   "partnerAmount": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "nullable": true,
    "description": "Partner amount."
   },
   "ticvaiAmount": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "nullable": true,
    "description": "TICVAI amount."
   },
   "status": {
    "type": "string",
    "enum": [
     "open",
     "investigating",
     "matched",
     "corrected",
     "differenceAccepted",
     "adjusted",
     "disputed",
     "escalated"
    ],
    "default": "open",
    "description": "Resolution status."
   },
   "assigneePrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Assigned to."
   },
   "rootCauseGroup": {
    "type": "string",
    "nullable": true,
    "description": "Advisory AI root-cause group shared with similar exceptions."
   },
   "scopePath": {
    "type": "string",
    "description": "The partition key (ADR-0005), written at `tenant` scope."
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
 "PartnerReconciliationExceptionManagementSummary": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection; the headline tiles over the list, computed at read time for the filters in force",
  "description": "**The headline figures on Partner Reconciliation & Exception Management.** The pack's KPI cards, split out of the row (decided 29 September, readiness close-out): a count describes the list, not each item in it.",
  "properties": {
   "recordsReconciled": {
    "type": "integer",
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
   }
  }
 },
 "PartnerReconciliationExceptionManagementView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over control.partner_reconciliation_exception (PartnerReconciliationException) and the existing subscription state, assembled at read time (data model DM4)",
  "description": "**What Partner Reconciliation & Exception Management displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "partnerAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Partner Amount"
   },
   "difference": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Difference (TICVAI minus partner)"
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
   "exceptionId": {
    "type": "string",
    "format": "uuid",
    "description": "Exception id"
   },
   "partnerId": {
    "type": "string",
    "format": "uuid",
    "description": "Partner"
   },
   "partner": {
    "type": "string",
    "description": "Partner trading name"
   },
   "partnerReference": {
    "type": "string",
    "description": "Partner Reference"
   },
   "orderId": {
    "type": "string",
    "format": "uuid",
    "description": "TICVAI order",
    "nullable": true
   },
   "comparedSource": {
    "type": "string",
    "enum": [
     "ticvaiOrders",
     "ticketsIssued",
     "partnerRates",
     "paymentsCredit",
     "commission",
     "invoices",
     "cancellationsRefunds"
    ],
    "description": "Reconciliation source the partner record was compared against"
   },
   "ticvaiAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "TICVAI Amount"
   },
   "status": {
    "type": "string",
    "description": "Resolution status: open, investigating, matched, corrected, differenceAccepted, adjusted, disputed, escalated"
   },
   "assignee": {
    "type": "string",
    "description": "Assigned to",
    "nullable": true
   },
   "rootCauseGroup": {
    "type": "string",
    "description": "Advisory AI root-cause group shared with similar exceptions",
    "nullable": true
   }
  }
 },
 "PartnerSettlementBatch": {
  "type": "object",
  "x-ticvai-persistence": "control.partner_settlement_batch",
  "description": "A commission settlement batch: the lines for one partner, currency, period and legal entity paid together. Its total is the sum of its lines (decided 29 September, data model DM4)\n\n**Batches are created by the settlement job** for each partner, currency, period and legal entity with reconciled lines; no operation creates one by hand. Finance moves a batch with actOnPartnerSettlementBatch (decided 29 September, writers pass; DM4).",
  "required": [
   "id",
   "partnerId",
   "currency",
   "period",
   "status"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "partnerId": {
    "type": "string",
    "format": "uuid",
    "description": "The partner (control.partner)."
   },
   "legalEntityId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Legal entity (ledger.legal_entity)."
   },
   "currency": {
    "type": "string",
    "pattern": "^[A-Z]{3}$",
    "description": "Settlement currency, ISO 4217."
   },
   "period": {
    "type": "string",
    "description": "Settlement period label, e.g. 2026-09."
   },
   "settlementPeriod": {
    "type": "string",
    "enum": [
     "perTransaction",
     "weekly",
     "monthly",
     "eventBased",
     "customCycle"
    ],
    "description": "Settlement period."
   },
   "status": {
    "type": "string",
    "enum": [
     "calculated",
     "reconciled",
     "financeReview",
     "approved",
     "scheduled",
     "paid",
     "onHold",
     "disputed",
     "reversed"
    ],
    "default": "calculated",
    "description": "Settlement status."
   },
   "scheduledDate": {
    "type": "string",
    "format": "date",
    "nullable": true,
    "description": "Date the batch is scheduled to be paid."
   },
   "scopePath": {
    "type": "string",
    "description": "The partition key (ADR-0005), written at `tenant` scope."
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
 "PartnerStatementAccountActivitySummary": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection; the headline tiles over the list, computed at read time for the filters in force",
  "description": "**The headline figures on Partner Statement & Account Activity.** The pack's KPI cards, split out of the row (decided 29 September, readiness close-out): a count describes the list, not each item in it.",
  "properties": {
   "openingBalance": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Opening Balance"
   },
   "sales": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Sales"
   },
   "payments": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Payments"
   },
   "credits": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Credits"
   },
   "refunds": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Refunds"
   },
   "commission": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Commission"
   },
   "adjustments": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
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
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Available Credit"
   },
   "current": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Aging: current (not yet due)"
   },
   "aged1To30": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Aging: 1-30 days"
   },
   "aged31To60": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Aging: 31-60 days"
   },
   "aged61To90": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Aging: 61-90 days"
   },
   "aged90Plus": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Aging: 90+ days"
   }
  }
 },
 "PartnerStatementAccountActivityView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over subscription state, assembled at read time from tables that already exist",
  "description": "**What Partner Statement & Account Activity displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "date": {
    "type": "string",
    "format": "date",
    "description": "Date"
   },
   "transactionType": {
    "type": "string",
    "enum": [
     "booking",
     "invoice",
     "payment",
     "refund",
     "creditNote",
     "commission",
     "manualAdjustment",
     "deposit",
     "settlement"
    ],
    "description": "Transaction Type"
   },
   "reference": {
    "type": "string",
    "description": "Reference"
   },
   "orderInvoice": {
    "type": "string",
    "description": "Order/Invoice number",
    "nullable": true
   },
   "debit": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Debit"
   },
   "credit": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Credit"
   },
   "runningBalance": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Running Balance"
   },
   "dueDate": {
    "type": "string",
    "format": "date",
    "description": "Due Date",
    "nullable": true
   },
   "status": {
    "type": "string",
    "description": "Status: open, partiallyPaid, paid, overdue or void"
   }
  }
 },
 "ReservationsHoldsReleaseManagementSummary": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection; the headline tiles over the list, computed at read time for the filters in force",
  "description": "**The headline figures on Reservations, Holds & Release Management.** The pack's KPI cards, split out of the row (decided 29 September, readiness close-out): a count describes the list, not each item in it.",
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
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Held Value"
   },
   "expiringToday": {
    "type": "integer",
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
    "type": "integer",
    "description": "Released Inventory, tickets"
   }
  }
 },
 "ReservationsHoldsReleaseManagementView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over subscription state, assembled at read time from tables that already exist",
  "description": "**What Reservations, Holds & Release Management displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "holdId": {
    "type": "string",
    "format": "uuid",
    "description": "Hold ID"
   },
   "partner": {
    "type": "string",
    "description": "Partner trading name"
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
   "seatZone": {
    "type": "string",
    "description": "Seat/Zone where applicable",
    "nullable": true
   },
   "holdCreatedAt": {
    "type": "string",
    "format": "date-time",
    "description": "Hold Created"
   },
   "holdExpiresAt": {
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
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Commercial Value"
   },
   "allocationSource": {
    "type": "string",
    "enum": [
     "partnerAllocation",
     "channelAllocation",
     "generalCapacity"
    ],
    "description": "Allocation Source"
   },
   "status": {
    "type": "string",
    "description": "Status: active, extended, converted, released, expired"
   },
   "extensionsUsed": {
    "type": "integer",
    "description": "Extensions used so far"
   },
   "partnerId": {
    "type": "string",
    "format": "uuid",
    "description": "Partner"
   },
   "aiInsights": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Advisory AI conversion-probability and release suggestions"
   }
  }
 }
}
```
