# WS63 — Ticket Resale Marketplace board 2

**10 screens · 10 operations · 10 schemas · 1 permissions**

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

- **Every control that can be refused must be gated.** 1 permissions apply here:
  `ORDER_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **0 of these operations work offline**
  
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `ADM-288` | Resale Operations Command Center | commandCentre | 1 | 0 | — |
| `ADM-289` | Buyer Purchase & Resale Order Management | configEditor | 1 | 0 | — |
| `ADM-290` | Ticket Ownership Transfer Management | listDetail | 1 | 0 | — |
| `ADM-291` | Credential Revocation & Regeneration | configEditor | 1 | 0 | — |
| `ADM-292` | Resale Fraud & Duplicate Sale Protection | listDetail | 1 | 0 | — |
| `ADM-293` | Capacity & Inventory Reconciliation | commandCentre | 1 | 0 | — |
| `ADM-294` | Seller Settlement & Payout Management | listDetail | 1 | 0 | — |
| `ADM-295` | Refunds, Disputes & Resale Exceptions | listDetail | 1 | 0 | — |
| `ADM-296` | Resale Audit & Ownership History | configEditor | 1 | 0 | — |
| `ADM-297` | Resale Analytics & AI Intelligence | commandCentre | 1 | 0 | — |

## Thin screens in this batch

**ADM-290, ADM-292 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "ADM-288",
  "name": "Resale Operations Command Center",
  "module": "Commercial",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Ticket Resale Marketplace_Reference.pdf",
   "board": "2",
   "number": "3.2.1",
   "page": 21
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/resale-operations-command-center-adm-288",
   "component": "apps/ticvai-web/src/routes/commercial/ResaleOperationsCommandCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-002"
   ],
   "exitTo": [
    "ADM-002",
    "ADM-289",
    "ADM-290",
    "ADM-291",
    "ADM-292",
    "ADM-293",
    "ADM-294",
    "ADM-295",
    "ADM-296",
    "ADM-297"
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
     "to": "ADM-289",
     "trigger": "Works in Buyer Purchase & Resale Order Management",
     "provenance": "flow F172 step 1→2",
     "operation": "listResale"
    },
    {
     "to": "ADM-290",
     "trigger": "Works in Ticket Ownership Transfer Management",
     "provenance": "flow F172 step 3→4",
     "operation": "listResale"
    },
    {
     "to": "ADM-291",
     "trigger": "Works in Credential Revocation & Regeneration",
     "provenance": "flow F172 step 5→6",
     "operation": "listResale"
    },
    {
     "to": "ADM-292",
     "trigger": "Works in Resale Fraud & Duplicate Sale Protection",
     "provenance": "flow F172 step 7→8",
     "operation": "listResale"
    },
    {
     "to": "ADM-293",
     "trigger": "Works in Capacity & Inventory Reconciliation",
     "provenance": "flow F172 step 9→10",
     "operation": "listResale"
    },
    {
     "to": "ADM-294",
     "trigger": "Works in Seller Settlement & Payout Management",
     "provenance": "flow F172 step 11→12",
     "operation": "listResale"
    },
    {
     "to": "ADM-295",
     "trigger": "Works in Refunds, Disputes & Resale Exceptions",
     "provenance": "flow F172 step 13→14",
     "operation": "listResale"
    },
    {
     "to": "ADM-296",
     "trigger": "Works in Resale Audit & Ownership History",
     "provenance": "flow F172 step 15→16",
     "operation": "listResale"
    },
    {
     "to": "ADM-297",
     "trigger": "Works in Resale Analytics & AI Intelligence",
     "provenance": "flow F172 step 17→18",
     "operation": "listResale"
    }
   ]
  },
  "density": "compact",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen both a metric directory (§Display) and a per-row directory (§Each resale transaction shall show) — counts over a population, then the population",
  "purpose": "Provide operations teams with a real-time control center for all resale transactions after listings move into purchase/fulfillment.",
  "purposeNote": "Operations can monitor every resale transaction from buyer payment through final completion and immediately identify transactions requiring intervention.",
  "layout": {
   "template": "dashboard",
   "regions": [
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "Resale Transactions Today",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 21 §Display",
       "bindsTo": "ResaleOperationsCommandCenterView.resaleTransactionsToday"
      },
      {
       "kind": "metricTile",
       "label": "Gross Resale Value",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 21 §Display",
       "bindsTo": "ResaleOperationsCommandCenterView.grossResaleValue"
      },
      {
       "kind": "metricTile",
       "label": "Completed Transfers",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 21 §Display",
       "bindsTo": "ResaleOperationsCommandCenterView.completedTransfers"
      },
      {
       "kind": "metricTile",
       "label": "Pending Transfers",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 21 §Display",
       "bindsTo": "ResaleOperationsCommandCenterView.pendingTransfers"
      },
      {
       "kind": "metricTile",
       "label": "Failed Transfers",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 21 §Display",
       "bindsTo": "ResaleOperationsCommandCenterView.failedTransfers"
      },
      {
       "kind": "metricTile",
       "label": "Credential Reissues",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 21 §Display",
       "bindsTo": "ResaleOperationsCommandCenterView.credentialReissues"
      },
      {
       "kind": "metricTile",
       "label": "Pending Seller Settlements",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 21 §Display",
       "bindsTo": "ResaleOperationsCommandCenterView.pendingSellerSettlements"
      },
      {
       "kind": "metricTile",
       "label": "Settlement Value",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 21 §Display",
       "bindsTo": "ResaleOperationsCommandCenterView.settlementValue"
      },
      {
       "kind": "metricTile",
       "label": "Transactions Under Review",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 21 §Display",
       "bindsTo": "ResaleOperationsCommandCenterView.transactionsUnderReview"
      },
      {
       "kind": "metricTile",
       "label": "Fraud Alerts",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 21 §Display",
       "bindsTo": "ResaleOperationsCommandCenterView.fraudAlerts"
      },
      {
       "kind": "metricTile",
       "label": "Disputes",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 21 §Display",
       "bindsTo": "ResaleOperationsCommandCenterView.disputes"
      },
      {
       "kind": "metricTile",
       "label": "Refunds",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 21 §Display",
       "bindsTo": "ResaleOperationsCommandCenterView.refunds"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "moduleTiles",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every resale operations",
       "columns": [
        "ResaleOperationsCommandCenterView.resaleTransactionId",
        "ResaleOperationsCommandCenterView.listingId",
        "ResaleOperationsCommandCenterView.originalOrderId",
        "ResaleOperationsCommandCenterView.originalTicketId",
        "ResaleOperationsCommandCenterView.event",
        "ResaleOperationsCommandCenterView.venue",
        "ResaleOperationsCommandCenterView.seller",
        "ResaleOperationsCommandCenterView.buyer",
        "ResaleOperationsCommandCenterView.sectionRowSeat",
        "ResaleOperationsCommandCenterView.resalePrice",
        "ResaleOperationsCommandCenterView.buyerTotal",
        "ResaleOperationsCommandCenterView.sellerProceeds",
        "ResaleOperationsCommandCenterView.purchaseStatus",
        "ResaleOperationsCommandCenterView.ownershipStatus",
        "ResaleOperationsCommandCenterView.credentialStatus",
        "ResaleOperationsCommandCenterView.settlementStatus",
        "ResaleOperationsCommandCenterView.riskScore",
        "ResaleOperationsCommandCenterView.transactionDate"
       ],
       "bindsTo": "ResaleOperationsCommandCenterView",
       "operation": "listResale",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 21 §Each resale transaction shall show"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected resale operations",
       "bindsTo": "ResaleOperationsCommandCenterView",
       "columns": [
        "ResaleOperationsCommandCenterView.resaleTransactionId",
        "ResaleOperationsCommandCenterView.listingId",
        "ResaleOperationsCommandCenterView.originalOrderId",
        "ResaleOperationsCommandCenterView.originalTicketId",
        "ResaleOperationsCommandCenterView.event",
        "ResaleOperationsCommandCenterView.venue",
        "ResaleOperationsCommandCenterView.seller",
        "ResaleOperationsCommandCenterView.buyer",
        "ResaleOperationsCommandCenterView.sectionRowSeat",
        "ResaleOperationsCommandCenterView.resalePrice",
        "ResaleOperationsCommandCenterView.buyerTotal",
        "ResaleOperationsCommandCenterView.sellerProceeds",
        "ResaleOperationsCommandCenterView.purchaseStatus",
        "ResaleOperationsCommandCenterView.ownershipStatus",
        "ResaleOperationsCommandCenterView.credentialStatus",
        "ResaleOperationsCommandCenterView.settlementStatus",
        "ResaleOperationsCommandCenterView.riskScore",
        "ResaleOperationsCommandCenterView.transactionDate"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Exception statuses”.",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 21 §Each resale transaction shall show"
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
       "notes": "**The pack separates these permissions and no action on the screen claims them yet:** Open transaction, Retry transfer, Hold transaction, Release transaction, Escalate, View credential, View settlement, View fraud assessment, View audit history. Each needs attaching to the control it gates, or the screen needs the control.",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 21 §Authorized users can"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The resale operations list; the counts above it resolve separately.",
   "error": "Could not load. Names which read failed and leaves the resale operations untouched.",
   "emptyFirstRun": "No resale operations yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the resale operations are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listResale",
    "contract": "orders",
    "purpose": "Resale Operations Command Center",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-288"
  },
  "apisNote": "Regenerated 9 September 2026 from Ticket Resale Marketplace_Reference.pdf page 21. 30 of 30 labels bound to a contract property; 39 of 53 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-289",
  "name": "Buyer Purchase & Resale Order Management",
  "module": "Commercial",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Ticket Resale Marketplace_Reference.pdf",
   "board": "2",
   "number": "3.2.2",
   "page": 23
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/buyer-purchase-resale-order-management-adm-289",
   "component": "apps/ticvai-web/src/routes/commercial/BuyerPurchaseResaleOrderManagement.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-288"
   ],
   "exitTo": [
    "ADM-288"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-288, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-288",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F172 step 2→3",
     "operation": "listBuyerPurchaseResale"
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure; Capture/reference) and no display directory — it is settings, not a population",
  "purpose": "Manage the buyer-side purchase transaction and ensure that a resale ticket is temporarily protected while checkout occurs.",
  "purposeNote": "A buyer can securely purchase a resale ticket without the same listing being sold concurrently to another buyer, and TICVAI retains the complete relationship to the original transaction.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Hold duration",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 23 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Hold extension rules",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 23 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Payment timeout",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 23 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Automatic release",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 23 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Concurrent buyer handling",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 23 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Customer ID",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 23 §Capture/reference"
      },
      {
       "kind": "selectField",
       "label": "Name",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 23 §Capture/reference"
      },
      {
       "kind": "selectField",
       "label": "Email",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 23 §Capture/reference"
      },
      {
       "kind": "selectField",
       "label": "Mobile",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 23 §Capture/reference"
      },
      {
       "kind": "selectField",
       "label": "Membership",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 23 §Capture/reference"
      },
      {
       "kind": "selectField",
       "label": "Loyalty profile",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 23 §Capture/reference"
      },
      {
       "kind": "textField",
       "label": "Identity verification where required",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 23 §Capture/reference"
      },
      {
       "kind": "selectField",
       "label": "Billing information",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 23 §Capture/reference"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The buyer purchase resale configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the buyer purchase resale untouched.",
   "emptyFirstRun": "No buyer purchase resale configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listBuyerPurchaseResale",
    "contract": "orders",
    "purpose": "Buyer Purchase & Resale Order Management",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-289"
  },
  "apisNote": "Regenerated 9 September 2026 from Ticket Resale Marketplace_Reference.pdf page 23. 0 of 0 labels bound to a contract property; 13 of 37 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-290",
  "name": "Ticket Ownership Transfer Management",
  "module": "Commercial",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Ticket Resale Marketplace_Reference.pdf",
   "board": "2",
   "number": "3.2.3",
   "page": 25
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/ticket-ownership-transfer-management-adm-290",
   "component": "apps/ticvai-web/src/routes/commercial/TicketOwnershipTransferManagement.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-288"
   ],
   "exitTo": [
    "ADM-288"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-288, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-288",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F172 step 4→5",
     "operation": "listTicketOwnershipTransfer"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Securely transfer the ticket entitlement from the original seller to the resale buyer.",
  "purposeNote": "the permanent ticket ownership history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Ticket Resale Marketplace_Reference.pdf, page 25"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Ticket Resale Marketplace_Reference.pdf, page 25"
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
       "impliedBy": "listTicketOwnershipTransfer",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The ticket ownership transfer list.",
   "error": "Could not load. Names which read failed and leaves the ticket ownership transfer untouched.",
   "emptyFirstRun": "No ticket ownership transfer yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the ticket ownership transfer are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listTicketOwnershipTransfer",
    "contract": "orders",
    "purpose": "Ticket Ownership Transfer Management",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "TicketOwnershipTransferManagementView.customer",
    "TicketOwnershipTransferManagementView.originalOrder",
    "TicketOwnershipTransferManagementView.ticket",
    "TicketOwnershipTransferManagementView.ownershipStatus",
    "TicketOwnershipTransferManagementView.newResaleOrder"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-290"
  },
  "apisNote": "Regenerated 9 September 2026 from Ticket Resale Marketplace_Reference.pdf page 25. 0 of 0 labels bound to a contract property; 0 of 34 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-291",
  "name": "Credential Revocation & Regeneration",
  "module": "Commercial",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Ticket Resale Marketplace_Reference.pdf",
   "board": "2",
   "number": "3.2.4",
   "page": 26
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/credential-revocation-regeneration-adm-291",
   "component": "apps/ticvai-web/src/routes/commercial/CredentialRevocationRegeneration.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-288"
   ],
   "exitTo": [
    "ADM-288"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-288, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-288",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F172 step 6→7",
     "operation": "listCredentialRevocationRegeneration"
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Depending on TICVAI configuration; Deliver through configured channels) and no display directory — it is settings, not a population",
  "purpose": "Ensure the seller's old ticket credential cannot continue to provide access after resale. This is one of the most important security functions in the module.",
  "purposeNote": "Following a successful resale, the seller's credential cannot provide valid access and the buyer receives a new valid credential linked to the transferred entitlement.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Static QR",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 26 §Depending on TICVAI configuration"
      },
      {
       "kind": "selectField",
       "label": "Dynamic QR",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 26 §Depending on TICVAI configuration"
      },
      {
       "kind": "selectField",
       "label": "Barcode",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 26 §Depending on TICVAI configuration"
      },
      {
       "kind": "selectField",
       "label": "NFC",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 26 §Depending on TICVAI configuration"
      },
      {
       "kind": "selectField",
       "label": "RFID",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 26 §Depending on TICVAI configuration"
      },
      {
       "kind": "selectField",
       "label": "Mobile Wallet pass",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 26 §Depending on TICVAI configuration"
      },
      {
       "kind": "selectField",
       "label": "Digital ticket",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 26 §Depending on TICVAI configuration"
      },
      {
       "kind": "selectField",
       "label": "Wearable credential",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 26 §Depending on TICVAI configuration"
      },
      {
       "kind": "selectField",
       "label": "TICVAI account",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 26 §Deliver through configured channels"
      },
      {
       "kind": "selectField",
       "label": "Mobile app",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 26 §Deliver through configured channels"
      },
      {
       "kind": "selectField",
       "label": "Email",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 26 §Deliver through configured channels"
      },
      {
       "kind": "selectField",
       "label": "Wallet",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 26 §Deliver through configured channels"
      },
      {
       "kind": "textField",
       "label": "Other configured delivery methods",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 26 §Deliver through configured channels"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The credential revocation regeneration configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the credential revocation regeneration untouched.",
   "emptyFirstRun": "No credential revocation regeneration configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listCredentialRevocationRegeneration",
    "contract": "orders",
    "purpose": "Credential Revocation & Regeneration",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-291"
  },
  "apisNote": "Regenerated 9 September 2026 from Ticket Resale Marketplace_Reference.pdf page 26. 0 of 0 labels bound to a contract property; 13 of 31 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-292",
  "name": "Resale Fraud & Duplicate Sale Protection",
  "module": "Commercial",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Ticket Resale Marketplace_Reference.pdf",
   "board": "2",
   "number": "3.2.5",
   "page": 28
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/resale-fraud-duplicate-sale-protection-adm-292",
   "component": "apps/ticvai-web/src/routes/commercial/ResaleFraudDuplicateSaleProtection.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-288"
   ],
   "exitTo": [
    "ADM-288"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-288, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-288",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F172 step 8→9",
     "operation": "listResaleFraudDuplicate"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Monitor) and no metric row",
  "purpose": "Protect TICVAI, venues, sellers and buyers from resale abuse and fraudulent ticket activity.",
  "purposeNote": "Potentially fraudulent resale activity is identified before or during fulfillment, with configurable intervention based on risk level.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every resale fraud duplicate",
       "columns": [
        "Duplicate listings",
        "ResaleFraudDuplicateSaleProtectionView.multipleResaleAttempts",
        "ResaleFraudDuplicateSaleProtectionView.sameTicketListedSimultaneously",
        "ResaleFraudDuplicateSaleProtectionView.unusualSellerVolume",
        "ResaleFraudDuplicateSaleProtectionView.highFrequencyResale",
        "ResaleFraudDuplicateSaleProtectionView.suspiciousPricing",
        "ResaleFraudDuplicateSaleProtectionView.multipleAccounts",
        "ResaleFraudDuplicateSaleProtectionView.paymentAnomalies",
        "ResaleFraudDuplicateSaleProtectionView.identityMismatch",
        "ResaleFraudDuplicateSaleProtectionView.credentialReuse",
        "ResaleFraudDuplicateSaleProtectionView.repeatedFailedTransactions",
        "ResaleFraudDuplicateSaleProtectionView.accountDeviceAnomaliesWherePermitted"
       ],
       "bindsTo": "ResaleFraudDuplicateSaleProtectionView",
       "operation": "listResaleFraudDuplicate",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 28 §Monitor"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected resale fraud duplicate",
       "bindsTo": "ResaleFraudDuplicateSaleProtectionView",
       "columns": [
        "Duplicate listings",
        "ResaleFraudDuplicateSaleProtectionView.multipleResaleAttempts",
        "ResaleFraudDuplicateSaleProtectionView.sameTicketListedSimultaneously",
        "ResaleFraudDuplicateSaleProtectionView.unusualSellerVolume",
        "ResaleFraudDuplicateSaleProtectionView.highFrequencyResale",
        "ResaleFraudDuplicateSaleProtectionView.suspiciousPricing",
        "ResaleFraudDuplicateSaleProtectionView.multipleAccounts",
        "ResaleFraudDuplicateSaleProtectionView.paymentAnomalies",
        "ResaleFraudDuplicateSaleProtectionView.identityMismatch",
        "ResaleFraudDuplicateSaleProtectionView.credentialReuse",
        "ResaleFraudDuplicateSaleProtectionView.repeatedFailedTransactions",
        "ResaleFraudDuplicateSaleProtectionView.accountDeviceAnomaliesWherePermitted"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Each transaction can receive”, “Detect attempted use of”, “Human Review”.",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 28 §Monitor"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The resale fraud duplicate list.",
   "error": "Could not load. Names which read failed and leaves the resale fraud duplicate untouched.",
   "emptyFirstRun": "No resale fraud duplicate yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the resale fraud duplicate are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listResaleFraudDuplicate",
    "contract": "orders",
    "purpose": "Resale Fraud & Duplicate Sale Protection",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "Duplicate listings",
    "ResaleFraudDuplicateSaleProtectionView.multipleResaleAttempts",
    "ResaleFraudDuplicateSaleProtectionView.sameTicketListedSimultaneously",
    "ResaleFraudDuplicateSaleProtectionView.unusualSellerVolume",
    "ResaleFraudDuplicateSaleProtectionView.highFrequencyResale",
    "ResaleFraudDuplicateSaleProtectionView.suspiciousPricing"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-292"
  },
  "apisNote": "Regenerated 9 September 2026 from Ticket Resale Marketplace_Reference.pdf page 28. 11 of 12 labels bound to a contract property; 19 of 32 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-293",
  "name": "Capacity & Inventory Reconciliation",
  "module": "Commercial",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Ticket Resale Marketplace_Reference.pdf",
   "board": "2",
   "number": "3.2.6",
   "page": 29
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/capacity-inventory-reconciliation-adm-293",
   "component": "apps/ticvai-web/src/routes/commercial/CapacityInventoryReconciliation.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-288"
   ],
   "exitTo": [
    "ADM-288"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-288, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-288",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F172 step 10→11",
     "operation": "listCapacityInventoryReconciliation"
    }
   ]
  },
  "density": "compact",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen both a metric directory (§Detect) and a per-row directory (§For each event show) — counts over a population, then the population",
  "purpose": "Ensure resale activity never creates additional venue capacity or corrupts primary ticket inventory.",
  "purposeNote": "The number of valid admissions and seat assignments remains consistent with configured venue/event capacity regardless of resale activity.",
  "layout": {
   "template": "dashboard",
   "regions": [
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "Duplicate active entitlement",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 29 §Detect"
      },
      {
       "kind": "metricTile",
       "label": "Seat assigned to multiple active owners",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 29 §Detect"
      },
      {
       "kind": "metricTile",
       "label": "Listing without ticket",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 29 §Detect"
      },
      {
       "kind": "metricTile",
       "label": "Sold resale listing still active",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 29 §Detect",
       "bindsTo": "CapacityInventoryReconciliationView.soldResaleListingStillActive"
      },
      {
       "kind": "metricTile",
       "label": "Ownership mismatch",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 29 §Detect",
       "bindsTo": "CapacityInventoryReconciliationView.ownershipMismatch"
      },
      {
       "kind": "metricTile",
       "label": "Credential mismatch",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 29 §Detect",
       "bindsTo": "CapacityInventoryReconciliationView.credentialMismatch"
      },
      {
       "kind": "metricTile",
       "label": "Capacity discrepancy",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 29 §Detect",
       "bindsTo": "CapacityInventoryReconciliationView.capacityDiscrepancy"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "moduleTiles",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every capacity inventory reconciliation",
       "columns": [
        "CapacityInventoryReconciliationView.venueCapacity",
        "CapacityInventoryReconciliationView.sellableCapacity",
        "CapacityInventoryReconciliationView.primaryTicketsSold",
        "CapacityInventoryReconciliationView.primaryInventoryRemaining",
        "CapacityInventoryReconciliationView.ticketsListedForResale",
        "CapacityInventoryReconciliationView.resaleTicketsSold",
        "CapacityInventoryReconciliationView.holds",
        "CapacityInventoryReconciliationView.cancelledTickets",
        "CapacityInventoryReconciliationView.refundedTickets",
        "CapacityInventoryReconciliationView.activeEntitlements"
       ],
       "bindsTo": "CapacityInventoryReconciliationView",
       "operation": "listCapacityInventoryReconciliation",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 29 §For each event show"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected capacity inventory reconciliation",
       "bindsTo": "CapacityInventoryReconciliationView",
       "columns": [
        "CapacityInventoryReconciliationView.venueCapacity",
        "CapacityInventoryReconciliationView.sellableCapacity",
        "CapacityInventoryReconciliationView.primaryTicketsSold",
        "CapacityInventoryReconciliationView.primaryInventoryRemaining",
        "CapacityInventoryReconciliationView.ticketsListedForResale",
        "CapacityInventoryReconciliationView.resaleTicketsSold",
        "CapacityInventoryReconciliationView.holds",
        "CapacityInventoryReconciliationView.cancelledTickets",
        "CapacityInventoryReconciliationView.refundedTickets",
        "CapacityInventoryReconciliationView.activeEntitlements"
       ],
       "notes": "The pack groups this record's detail under its own headings: “A resale represents”, “Sold / New Owner”.",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 29 §For each event show"
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
       "notes": "**The pack separates these permissions and no action on the screen claims them yet:** Investigate, Re-sync, Correct mapping, Hold ticket, Escalate, Generate reconciliation report. Each needs attaching to the control it gates, or the screen needs the control.",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 29 §Authorized users can"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The capacity inventory reconciliation list; the counts above it resolve separately.",
   "error": "Could not load. Names which read failed and leaves the capacity inventory reconciliation untouched.",
   "emptyFirstRun": "No capacity inventory reconciliation yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the capacity inventory reconciliation are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listCapacityInventoryReconciliation",
    "contract": "orders",
    "purpose": "Capacity & Inventory Reconciliation",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "CapacityInventoryReconciliationView.venueCapacity",
    "CapacityInventoryReconciliationView.sellableCapacity",
    "CapacityInventoryReconciliationView.primaryTicketsSold",
    "CapacityInventoryReconciliationView.primaryInventoryRemaining",
    "CapacityInventoryReconciliationView.ticketsListedForResale",
    "CapacityInventoryReconciliationView.resaleTicketsSold"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-293"
  },
  "apisNote": "Regenerated 9 September 2026 from Ticket Resale Marketplace_Reference.pdf page 29. 14 of 14 labels bound to a contract property; 23 of 30 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-294",
  "name": "Seller Settlement & Payout Management",
  "module": "Commercial",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Ticket Resale Marketplace_Reference.pdf",
   "board": "2",
   "number": "3.2.7",
   "page": 30
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/seller-settlement-payout-management-adm-294",
   "component": "apps/ticvai-web/src/routes/commercial/SellerSettlementPayoutManagement.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-288"
   ],
   "exitTo": [
    "ADM-288"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-288, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-288",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F172 step 12→13",
     "operation": "listSellerSettlementPayout"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Show) and no metric row",
  "purpose": "Manage the financial amount owed to sellers following successful resale.",
  "purposeNote": "Every completed resale produces an auditable seller settlement record with accurate proceeds, deductions, payout timing and settlement status.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 3 actions on this screen and the screen declares 1 operation.** Unserved: Manual hold, Compliance hold, Refund/dispute hold. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Ticket Resale Marketplace_Reference.pdf, page 30 §Support"
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
       "label": "Every seller settlement payout",
       "columns": [
        "SellerSettlementPayoutManagementView.settlementId",
        "SellerSettlementPayoutManagementView.resaleTransaction",
        "SellerSettlementPayoutManagementView.seller",
        "SellerSettlementPayoutManagementView.listingPrice",
        "SellerSettlementPayoutManagementView.sellerFee",
        "SellerSettlementPayoutManagementView.commission",
        "SellerSettlementPayoutManagementView.processingFee",
        "SellerSettlementPayoutManagementView.applicableTax",
        "SellerSettlementPayoutManagementView.adjustments",
        "SellerSettlementPayoutManagementView.sellerProceeds",
        "SellerSettlementPayoutManagementView.currency",
        "SellerSettlementPayoutManagementView.payoutMethod",
        "SellerSettlementPayoutManagementView.settlementStatus",
        "SellerSettlementPayoutManagementView.expectedPayoutDate"
       ],
       "bindsTo": "SellerSettlementPayoutManagementView",
       "operation": "listSellerSettlementPayout",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 30 §Show"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected seller settlement payout",
       "bindsTo": "SellerSettlementPayoutManagementView",
       "columns": [
        "SellerSettlementPayoutManagementView.settlementId",
        "SellerSettlementPayoutManagementView.resaleTransaction",
        "SellerSettlementPayoutManagementView.seller",
        "SellerSettlementPayoutManagementView.listingPrice",
        "SellerSettlementPayoutManagementView.sellerFee",
        "SellerSettlementPayoutManagementView.commission",
        "SellerSettlementPayoutManagementView.processingFee",
        "SellerSettlementPayoutManagementView.applicableTax",
        "SellerSettlementPayoutManagementView.adjustments",
        "SellerSettlementPayoutManagementView.sellerProceeds",
        "SellerSettlementPayoutManagementView.currency",
        "SellerSettlementPayoutManagementView.payoutMethod",
        "SellerSettlementPayoutManagementView.settlementStatus",
        "SellerSettlementPayoutManagementView.expectedPayoutDate"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Suggested”, “Exception statuses”, “A venue may prefer”, “Finance Integration”.",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 30 §Show"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Manual hold",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 30 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Compliance hold",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 30 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Refund/dispute hold",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 30 §Support"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The seller settlement payout list.",
   "error": "Could not load. Names which read failed and leaves the seller settlement payout untouched.",
   "emptyFirstRun": "No seller settlement payout yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the seller settlement payout are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listSellerSettlementPayout",
    "contract": "orders",
    "purpose": "Seller Settlement & Payout Management",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "SellerSettlementPayoutManagementView.settlementId",
    "SellerSettlementPayoutManagementView.resaleTransaction",
    "SellerSettlementPayoutManagementView.seller",
    "SellerSettlementPayoutManagementView.listingPrice",
    "SellerSettlementPayoutManagementView.sellerFee",
    "SellerSettlementPayoutManagementView.commission"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-294"
  },
  "apisNote": "Regenerated 9 September 2026 from Ticket Resale Marketplace_Reference.pdf page 30. 14 of 14 labels bound to a contract property; 23 of 38 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-295",
  "name": "Refunds, Disputes & Resale Exceptions",
  "module": "Commercial",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Ticket Resale Marketplace_Reference.pdf",
   "board": "2",
   "number": "3.2.8",
   "page": 32
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/refunds-disputes-resale-exceptions-adm-295",
   "component": "apps/ticvai-web/src/routes/commercial/RefundsDisputesResaleExceptions.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-288"
   ],
   "exitTo": [
    "ADM-288"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-288, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-288",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F172 step 14→15",
     "operation": "listRefundDisputeResale"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Handle exceptional scenarios that occur after a resale transaction.",
  "purposeNote": "Operations can resolve resale exceptions without breaking the original order, resale transaction, ownership, credential or financial history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 7 actions on this screen and the screen declares 1 operation.** Unserved: Failed ownership transfer, Failed credential issuance, Duplicate transaction, Ticket access issue, Incorrect ticket, Venue change, Seat change. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Ticket Resale Marketplace_Reference.pdf, page 32 §Support"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Ticket Resale Marketplace_Reference.pdf, page 32"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Ticket Resale Marketplace_Reference.pdf, page 32"
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
       "label": "Failed ownership transfer",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 32 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Failed credential issuance",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 32 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Duplicate transaction",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 32 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Ticket access issue",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 32 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Incorrect ticket",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 32 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Venue change",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 32 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Seat change",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 32 §Support"
      },
      {
       "kind": "banner",
       "label": "Permissions this screen separates",
       "notes": "**The pack separates these permissions and no action on the screen claims them yet:** Refund buyer, Reverse settlement, Hold settlement, Reissue credential, Retry transfer, Cancel transaction, Return ownership, Provide replacement ticket, Escalate. Each needs attaching to the control it gates, or the screen needs the control.",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 32 §Depending on permission"
      }
     ]
    },
    {
     "name": "contentBody",
     "components": []
    }
   ]
  },
  "states": {
   "loading": "The refunds disputes resale list.",
   "error": "Could not load. Names which read failed and leaves the refunds disputes resale untouched.",
   "emptyFirstRun": "No refunds disputes resale yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the refunds disputes resale are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listRefundDisputeResale",
    "contract": "orders",
    "purpose": "Refunds, Disputes & Resale Exceptions",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "RefundsDisputesResaleExceptionsView.eventCancellation",
    "RefundsDisputesResaleExceptionsView.eventPostponement",
    "RefundsDisputesResaleExceptionsView.buyerRefund",
    "RefundsDisputesResaleExceptionsView.sellerDispute",
    "RefundsDisputesResaleExceptionsView.buyerDispute"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-295"
  },
  "apisNote": "Regenerated 9 September 2026 from Ticket Resale Marketplace_Reference.pdf page 32. 0 of 0 labels bound to a contract property; 16 of 47 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-296",
  "name": "Resale Audit & Ownership History",
  "module": "Commercial",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Ticket Resale Marketplace_Reference.pdf",
   "board": "2",
   "number": "3.2.9",
   "page": 34
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/resale-audit-ownership-history-adm-296",
   "component": "apps/ticvai-web/src/routes/commercial/ResaleAuditOwnershipHistory.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-288"
   ],
   "exitTo": [
    "ADM-288"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-288, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-288",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F172 step 16→17",
     "operation": "listResaleOwnership"
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Capture) and no display directory — it is settings, not a population",
  "purpose": "Provide complete end-to-end traceability of every ticket that enters the resale ecosystem.",
  "purposeNote": "ownership transfer, credential replacement and financial settlement.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "filters",
     "components": [
      {
       "kind": "searchField",
       "label": "Search resale audit ownership",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 34 §Administrators can search by"
      },
      {
       "kind": "multiSelect",
       "label": "Filter by",
       "columns": [
        "ResaleAuditOwnershipHistoryView.ticketId",
        "ResaleAuditOwnershipHistoryView.credential",
        "ResaleAuditOwnershipHistoryView.order",
        "ResaleAuditOwnershipHistoryView.resaleTransaction",
        "ResaleAuditOwnershipHistoryView.seller",
        "ResaleAuditOwnershipHistoryView.buyer",
        "ResaleAuditOwnershipHistoryView.seat",
        "ResaleAuditOwnershipHistoryView.event",
        "ResaleAuditOwnershipHistoryView.paymentReference"
       ],
       "notes": "The pack filters this screen by ticket id, credential, order, resale transaction, seller, buyer and 3 more — which are present is a decision the pack already made.",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 34 §Administrators can search by"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Timestamp",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 34 §Capture"
      },
      {
       "kind": "selectField",
       "label": "User/system",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 34 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Action",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 34 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Original order",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 34 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Resale order",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 34 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Ticket",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 34 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Seller",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 34 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Buyer",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 34 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Listing",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 34 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Price",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 34 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Fee",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 34 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Credential",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 34 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Ownership",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 34 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Payment",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 34 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Settlement",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 34 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Approval",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 34 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Device/channel where applicable",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 34 §Capture"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The resale audit ownership configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the resale audit ownership untouched.",
   "emptyFirstRun": "No resale audit ownership configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoResults": "The filter narrowed it and the resale audit ownership are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listResaleOwnership",
    "contract": "orders",
    "purpose": "Resale Audit & Ownership History",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-296"
  },
  "apisNote": "Regenerated 9 September 2026 from Ticket Resale Marketplace_Reference.pdf page 34. 9 of 9 labels bound to a contract property; 26 of 45 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-297",
  "name": "Resale Analytics & AI Intelligence",
  "module": "Commercial",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Ticket Resale Marketplace_Reference.pdf",
   "board": "2",
   "number": "3.2.10",
   "page": 35
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/resale-analytics-ai-intelligence-adm-297",
   "component": "apps/ticvai-web/src/routes/commercial/ResaleAnalyticsAiIntelligence.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-288"
   ],
   "exitTo": [
    "ADM-288"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-288, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation."
  },
  "density": "compact",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen a metric directory (§Display) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's",
  "purpose": "Provide management with commercial, operational and predictive intelligence about the resale marketplace. Board 3 defines how the end customer actually accesses, uses, sells through, and buys from The existing resale architecture already defines the backend marketplace configuration and transaction processing across Boards 1 and 2. Board 3 closes the missing experience layer: Board 1 — Configure Marketplace Eligibility → Policy → Listings → Pricing → Fees → Approval → Inventory Board 2 — Execute Resale Transaction Buyer → Payment → Ownership Transfer → Credentials → Fraud → Settlement → Audit Board 3 — Customer Experience Seller Journey → Buyer Journey → White-Label Portal → Client B2C Integration → Hosted Marketplace → Headless/API",
  "purposeNote": "Management can evaluate the commercial and operational performance of resale and use explainable AI insights to improve primary pricing, marketplace policies and future event strategy. Board 2 — Final Screen Register Screen Backend Screen Primary Responsibility",
  "layout": {
   "template": "dashboard",
   "regions": [
    {
     "name": "contentBody",
     "slot": "filters",
     "components": [
      {
       "kind": "searchField",
       "label": "Search resale analytics intelligence",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 35 §Analyze by"
      },
      {
       "kind": "multiSelect",
       "label": "Filter by",
       "columns": [
        "Venue",
        "Event",
        "Product",
        "Ticket type",
        "Section",
        "Seat category",
        "Seller segment",
        "Buyer segment",
        "Sales channel",
        "Time before event",
        "Price range"
       ],
       "notes": "The pack filters this screen by venue, event, product, ticket type, section, seat category and 5 more — which are present is a decision the pack already made.",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 35 §Analyze by"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "Gross Resale Value",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 35 §Display",
       "bindsTo": "ResaleAnalyticsAiIntelligenceView.grossResaleValue"
      },
      {
       "kind": "metricTile",
       "label": "Resale Transactions",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 35 §Display",
       "bindsTo": "ResaleAnalyticsAiIntelligenceView.resaleTransactions"
      },
      {
       "kind": "metricTile",
       "label": "Resale Conversion Rate",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 35 §Display",
       "bindsTo": "ResaleAnalyticsAiIntelligenceView.resaleConversionRate"
      },
      {
       "kind": "metricTile",
       "label": "Average Listing Price",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 35 §Display",
       "bindsTo": "ResaleAnalyticsAiIntelligenceView.averageListingPrice"
      },
      {
       "kind": "metricTile",
       "label": "Average Sale Price",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 35 §Display",
       "bindsTo": "ResaleAnalyticsAiIntelligenceView.averageSalePrice"
      },
      {
       "kind": "metricTile",
       "label": "Average Markup/Discount",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 35 §Display"
      },
      {
       "kind": "metricTile",
       "label": "Seller Proceeds",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 35 §Display",
       "bindsTo": "ResaleAnalyticsAiIntelligenceView.sellerProceeds"
      },
      {
       "kind": "metricTile",
       "label": "Marketplace Revenue",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 35 §Display",
       "bindsTo": "ResaleAnalyticsAiIntelligenceView.marketplaceRevenue"
      },
      {
       "kind": "metricTile",
       "label": "Average Time to Sell",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 35 §Display",
       "bindsTo": "ResaleAnalyticsAiIntelligenceView.averageTimeToSell"
      },
      {
       "kind": "metricTile",
       "label": "Listings-to-Sales Ratio",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 35 §Display",
       "bindsTo": "ResaleAnalyticsAiIntelligenceView.listingsToSalesRatio"
      },
      {
       "kind": "metricTile",
       "label": "Fraud Rate",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 35 §Display",
       "bindsTo": "ResaleAnalyticsAiIntelligenceView.fraudRate"
      },
      {
       "kind": "metricTile",
       "label": "Refund/Dispute Rate",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 35 §Display",
       "bindsTo": "ResaleAnalyticsAiIntelligenceView.refundDisputeRate"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The resale analytics intelligence list; the counts above it resolve separately.",
   "error": "Could not load. Names which read failed and leaves the resale analytics intelligence untouched.",
   "emptyFirstRun": "No resale analytics intelligence yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the resale analytics intelligence are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listResale2",
    "contract": "orders",
    "purpose": "Resale Analytics & AI Intelligence",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "ResaleAnalyticsAiIntelligenceView.grossResaleValue",
    "ResaleAnalyticsAiIntelligenceView.resaleTransactions",
    "ResaleAnalyticsAiIntelligenceView.resaleConversionRate",
    "ResaleAnalyticsAiIntelligenceView.averageListingPrice",
    "ResaleAnalyticsAiIntelligenceView.averageSalePrice",
    "Average Markup/Discount"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-297"
  },
  "apisNote": "Regenerated 9 September 2026 from Ticket Resale Marketplace_Reference.pdf page 35. 11 of 22 labels bound to a contract property; 23 of 107 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
 "listBuyerPurchaseResale": {
  "method": "GET",
  "path": "/buyer-purchase-resale",
  "contract": "orders",
  "summary": "Buyer Purchase & Resale Order Management",
  "permission": "ORDER_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "BuyerPurchaseResaleOrderManagementView"
 },
 "listCapacityInventoryReconciliation": {
  "method": "GET",
  "path": "/capacity-inventory-reconciliation",
  "contract": "orders",
  "summary": "Capacity & Inventory Reconciliation",
  "permission": "ORDER_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "CapacityInventoryReconciliationView"
 },
 "listCredentialRevocationRegeneration": {
  "method": "GET",
  "path": "/credential-revocation-regeneration",
  "contract": "orders",
  "summary": "Credential Revocation & Regeneration",
  "permission": "ORDER_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "CredentialRevocationRegenerationView"
 },
 "listRefundDisputeResale": {
  "method": "GET",
  "path": "/refund-dispute-resale",
  "contract": "orders",
  "summary": "Refunds, Disputes & Resale Exceptions",
  "permission": "ORDER_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "RefundsDisputesResaleExceptionsView"
 },
 "listResale": {
  "method": "GET",
  "path": "/resale",
  "contract": "orders",
  "summary": "Resale Operations Command Center",
  "permission": "ORDER_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "ResaleOperationsCommandCenterView"
 },
 "listResale2": {
  "method": "GET",
  "path": "/resale-2",
  "contract": "orders",
  "summary": "Resale Analytics & AI Intelligence",
  "permission": "ORDER_VIEW",
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
    "name": "ticketType",
    "in": "query",
    "required": false
   },
   {
    "name": "section",
    "in": "query",
    "required": false
   },
   {
    "name": "seatCategory",
    "in": "query",
    "required": false
   },
   {
    "name": "sellerSegment",
    "in": "query",
    "required": false
   },
   {
    "name": "buyerSegment",
    "in": "query",
    "required": false
   }
  ],
  "requestBody": null,
  "responds": "ResaleAnalyticsAiIntelligenceView"
 },
 "listResaleFraudDuplicate": {
  "method": "GET",
  "path": "/resale-fraud-duplicate",
  "contract": "orders",
  "summary": "Resale Fraud & Duplicate Sale Protection",
  "permission": "ORDER_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "ResaleFraudDuplicateSaleProtectionView"
 },
 "listResaleOwnership": {
  "method": "GET",
  "path": "/resale-ownership",
  "contract": "orders",
  "summary": "Resale Audit & Ownership History",
  "permission": "ORDER_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "ResaleAuditOwnershipHistoryView"
 },
 "listSellerSettlementPayout": {
  "method": "GET",
  "path": "/seller-settlement-payout",
  "contract": "orders",
  "summary": "Seller Settlement & Payout Management",
  "permission": "ORDER_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "SellerSettlementPayoutManagementView"
 },
 "listTicketOwnershipTransfer": {
  "method": "GET",
  "path": "/ticket-ownership-transfer",
  "contract": "orders",
  "summary": "Ticket Ownership Transfer Management",
  "permission": "ORDER_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "TicketOwnershipTransferManagementView"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "BuyerPurchaseResaleOrderManagementView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over orders state, assembled at read time from tables that already exist",
  "description": "**What Buyer Purchase & Resale Order Management displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "confirmationTransfer": {
    "type": "string",
    "description": "Confirmation → Transfer"
   },
   "holdDuration": {
    "type": "string",
    "format": "date-time",
    "description": "Hold duration"
   },
   "holdExtensionRules": {
    "type": "string",
    "description": "Hold extension rules"
   },
   "paymentTimeout": {
    "type": "string",
    "description": "Payment timeout"
   },
   "automaticRelease": {
    "type": "string",
    "description": "Automatic release"
   },
   "concurrentBuyerHandling": {
    "type": "string",
    "description": "Concurrent buyer handling"
   },
   "customerId": {
    "type": "string",
    "description": "Customer ID"
   },
   "name": {
    "type": "string",
    "description": "Name"
   },
   "email": {
    "type": "string",
    "description": "Email"
   },
   "mobile": {
    "type": "string",
    "description": "Mobile"
   },
   "membership": {
    "type": "string",
    "description": "Membership"
   },
   "loyaltyProfile": {
    "type": "string",
    "description": "Loyalty profile"
   },
   "identityVerificationWhereRequired": {
    "type": "boolean",
    "description": "Identity verification where required"
   },
   "billingInformation": {
    "type": "string",
    "description": "Billing information"
   },
   "resaleTicketPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Resale ticket price"
   },
   "buyerServiceFee": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Buyer service fee"
   },
   "taxes": {
    "type": "string",
    "description": "Taxes"
   },
   "otherPermittedCharges": {
    "type": "string",
    "description": "Other permitted charges"
   },
   "totalPayable": {
    "type": "integer",
    "description": "Total payable"
   },
   "card": {
    "type": "string",
    "description": "Card"
   },
   "wallet": {
    "type": "string",
    "description": "Wallet"
   },
   "supportedAlternativePaymentMethods": {
    "type": "string",
    "description": "Supported alternative payment methods"
   },
   "paymentAuthorization": {
    "type": "string",
    "description": "Payment authorization"
   },
   "paymentCapture": {
    "type": "string",
    "description": "Payment capture"
   },
   "failureHandling": {
    "type": "string",
    "description": "Failure handling"
   }
  }
 },
 "CapacityInventoryReconciliationView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over orders state, assembled at read time from tables that already exist",
  "description": "**What Capacity & Inventory Reconciliation displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "venueCapacity": {
    "type": "integer",
    "description": "Venue capacity"
   },
   "sellableCapacity": {
    "type": "integer",
    "description": "Sellable capacity"
   },
   "primaryTicketsSold": {
    "type": "string",
    "description": "Primary tickets sold"
   },
   "primaryInventoryRemaining": {
    "type": "string",
    "description": "Primary inventory remaining"
   },
   "ticketsListedForResale": {
    "type": "string",
    "description": "Tickets listed for resale"
   },
   "resaleTicketsSold": {
    "type": "string",
    "description": "Resale tickets sold"
   },
   "holds": {
    "type": "string",
    "description": "Holds"
   },
   "cancelledTickets": {
    "type": "integer",
    "description": "Cancelled tickets"
   },
   "refundedTickets": {
    "type": "string",
    "description": "Refunded tickets"
   },
   "activeEntitlements": {
    "type": "integer",
    "description": "Active entitlements"
   },
   "processExplicitlyReturnsIt": {
    "type": "string",
    "description": "process explicitly returns it"
   },
   "soldResaleListingStillActive": {
    "type": "integer",
    "description": "Sold resale listing still active"
   },
   "ownershipMismatch": {
    "type": "string",
    "description": "Ownership mismatch"
   },
   "credentialMismatch": {
    "type": "string",
    "description": "Credential mismatch"
   },
   "capacityDiscrepancy": {
    "type": "integer",
    "description": "Capacity discrepancy"
   },
   "investigate": {
    "type": "string",
    "description": "Investigate"
   },
   "reSync": {
    "type": "string",
    "description": "Re-sync"
   },
   "correctMapping": {
    "type": "string",
    "description": "Correct mapping"
   },
   "holdTicket": {
    "type": "string",
    "description": "Hold ticket"
   }
  }
 },
 "CredentialRevocationRegenerationView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over orders state, assembled at read time from tables that already exist",
  "description": "**What Credential Revocation & Regeneration displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "oldCredentialRevoke": {
    "type": "string",
    "description": "Old Credential → Revoke"
   },
   "staticQr": {
    "type": "string",
    "description": "Static QR"
   },
   "dynamicQr": {
    "type": "string",
    "description": "Dynamic QR"
   },
   "barcode": {
    "type": "string",
    "description": "Barcode"
   },
   "nfc": {
    "type": "string",
    "description": "NFC"
   },
   "rfid": {
    "type": "string",
    "description": "RFID"
   },
   "mobileWalletPass": {
    "type": "string",
    "description": "Mobile Wallet pass"
   },
   "digitalTicket": {
    "type": "string",
    "description": "Digital ticket"
   },
   "wearableCredential": {
    "type": "string",
    "description": "Wearable credential"
   },
   "revokedResold": {
    "type": "string",
    "description": "Revoked — Resold"
   },
   "newCredentialId": {
    "type": "string",
    "description": "New credential ID"
   },
   "newQr": {
    "type": "integer",
    "description": "New QR"
   },
   "newToken": {
    "type": "integer",
    "description": "New token"
   },
   "buyerAssociation": {
    "type": "string",
    "description": "Buyer association"
   },
   "originalTicketRelationship": {
    "type": "string",
    "description": "Original ticket relationship"
   },
   "newSecurityKeysTokenWhereApplicable": {
    "type": "integer",
    "description": "New security keys/token where applicable"
   },
   "newWalletPassWhereApplicable": {
    "type": "integer",
    "description": "New wallet pass where applicable"
   },
   "ticvaiAccount": {
    "type": "string",
    "description": "TICVAI account"
   },
   "mobileApp": {
    "type": "string",
    "description": "Mobile app"
   },
   "email": {
    "type": "string",
    "description": "Email"
   },
   "wallet": {
    "type": "string",
    "description": "Wallet"
   },
   "otherConfiguredDeliveryMethods": {
    "type": "string",
    "description": "Other configured delivery methods"
   }
  }
 },
 "RefundsDisputesResaleExceptionsView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over orders state, assembled at read time from tables that already exist",
  "description": "**What Refunds, Disputes & Resale Exceptions displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "eventCancellation": {
    "type": "string",
    "description": "Event cancellation"
   },
   "eventPostponement": {
    "type": "string",
    "description": "Event postponement"
   },
   "buyerRefund": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Buyer refund"
   },
   "sellerDispute": {
    "type": "string",
    "description": "Seller dispute"
   },
   "buyerDispute": {
    "type": "string",
    "description": "Buyer dispute"
   },
   "paymentChargeback": {
    "type": "string",
    "description": "Payment chargeback"
   },
   "failedOwnershipTransfer": {
    "type": "integer",
    "description": "Failed ownership transfer"
   },
   "failedCredentialIssuance": {
    "type": "integer",
    "description": "Failed credential issuance"
   },
   "ticketAccessIssue": {
    "type": "string",
    "description": "Ticket access issue"
   },
   "sellerPayoutDispute": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Seller payout dispute"
   },
   "incorrectTicket": {
    "type": "string",
    "description": "Incorrect ticket"
   },
   "venueChange": {
    "type": "string",
    "description": "Venue change"
   },
   "seatChange": {
    "type": "string",
    "description": "Seat change"
   },
   "caseId": {
    "type": "string",
    "description": "Case ID"
   },
   "resaleTransaction": {
    "type": "string",
    "description": "Resale transaction"
   },
   "originalOrder": {
    "type": "string",
    "description": "Original order"
   },
   "seller": {
    "type": "string",
    "description": "Seller"
   },
   "buyer": {
    "type": "string",
    "description": "Buyer"
   },
   "event": {
    "type": "string",
    "description": "Event"
   },
   "financialAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Financial amount"
   },
   "credentialStatus": {
    "type": "string",
    "description": "Credential status"
   },
   "settlementStatus": {
    "type": "string",
    "description": "Settlement status"
   },
   "caseOwner": {
    "type": "string",
    "description": "Case owner"
   },
   "sla": {
    "type": "string",
    "description": "SLA"
   },
   "evidence": {
    "type": "string",
    "description": "Evidence"
   },
   "notes": {
    "type": "string",
    "description": "Notes"
   },
   "resolution": {
    "type": "string",
    "description": "Resolution"
   },
   "holdSettlement": {
    "type": "string",
    "description": "Hold settlement"
   },
   "returnOwnership": {
    "type": "string",
    "description": "Return ownership"
   },
   "provideReplacementTicket": {
    "type": "string",
    "description": "Provide replacement ticket"
   },
   "whoReceivesTheRefund": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Who receives the refund?"
   }
  }
 },
 "ResaleAnalyticsAiIntelligenceView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over orders state, assembled at read time from tables that already exist",
  "description": "**What Resale Analytics & AI Intelligence displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "grossResaleValue": {
    "type": "string",
    "description": "Gross Resale Value"
   },
   "resaleTransactions": {
    "type": "integer",
    "description": "Resale Transactions"
   },
   "resaleConversionRate": {
    "type": "number",
    "description": "Resale Conversion Rate"
   },
   "averageListingPrice": {
    "type": "number",
    "description": "Average Listing Price"
   },
   "averageSalePrice": {
    "type": "number",
    "description": "Average Sale Price"
   },
   "averageMarkup": {
    "type": "number",
    "description": "Average Markup"
   },
   "averageDiscount": {
    "type": "number",
    "description": "Average Discount"
   },
   "sellerProceeds": {
    "type": "integer",
    "description": "Seller Proceeds"
   },
   "marketplaceRevenue": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Marketplace Revenue"
   },
   "averageTimeToSell": {
    "type": "string",
    "format": "date-time",
    "description": "Average Time to Sell"
   },
   "listingsToSalesRatio": {
    "type": "number",
    "description": "Listings-to-Sales Ratio"
   },
   "fraudRate": {
    "type": "number",
    "description": "Fraud Rate"
   },
   "refundDisputeRate": {
    "type": "number",
    "description": "Refund/Dispute Rate"
   },
   "including": {
    "type": "string",
    "description": "including"
   },
   "primaryAvailability": {
    "type": "string",
    "description": "Primary availability"
   },
   "resaleAvailability": {
    "type": "string",
    "description": "Resale availability"
   },
   "primaryPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Primary price"
   },
   "averageResalePrice": {
    "type": "number",
    "description": "Average resale price"
   },
   "demand": {
    "type": "string",
    "description": "Demand"
   },
   "conversion": {
    "type": "number",
    "description": "Conversion"
   },
   "sellThrough": {
    "type": "string",
    "description": "Sell-through"
   },
   "primaryPriceForWeekendPerformances": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "primary price for weekend performances"
   },
   "expectedResaleDemand": {
    "type": "string",
    "description": "Expected resale demand"
   },
   "expectedListingVolume": {
    "type": "integer",
    "description": "Expected listing volume"
   },
   "expectedResalePrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Expected resale price"
   },
   "expectedConversion": {
    "type": "number",
    "description": "Expected conversion"
   },
   "expectedMarketplaceRevenue": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Expected marketplace revenue"
   },
   "policyPermitsIt": {
    "type": "string",
    "description": "policy permits it"
   },
   "monitoring": {
    "type": "string",
    "description": "monitoring"
   },
   "exceptionsAuditAnalytics": {
    "type": "string",
    "description": "Exceptions → Audit → Analytics"
   },
   "modelAEmbeddedWhiteLabel": {
    "type": "string",
    "description": "Model A — Embedded White-Label"
   },
   "modelBTicvaiHostedWhiteLabel": {
    "type": "string",
    "description": "Model B — TICVAI-Hosted White-Label"
   },
   "andCommercialPolicies": {
    "type": "string",
    "description": "and commercial policies"
   },
   "modelCHeadlessApi": {
    "type": "string",
    "description": "Model C — Headless/API"
   },
   "engine": {
    "type": "string",
    "description": "engine"
   },
   "customerProposition": {
    "type": "string",
    "description": "customer proposition"
   }
  }
 },
 "ResaleAuditOwnershipHistoryView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over orders state, assembled at read time from tables that already exist",
  "description": "**What Resale Audit & Ownership History displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "timestamp": {
    "type": "string",
    "format": "date-time",
    "description": "Timestamp"
   },
   "userSystem": {
    "type": "string",
    "description": "User/system"
   },
   "action": {
    "type": "string",
    "description": "Action"
   },
   "originalOrder": {
    "type": "string",
    "description": "Original order"
   },
   "resaleOrder": {
    "type": "string",
    "description": "Resale order"
   },
   "ticket": {
    "type": "string",
    "description": "Ticket"
   },
   "seller": {
    "type": "string",
    "description": "Seller"
   },
   "buyer": {
    "type": "string",
    "description": "Buyer"
   },
   "listing": {
    "type": "string",
    "description": "Listing"
   },
   "price": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Price"
   },
   "fee": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Fee"
   },
   "credential": {
    "type": "string",
    "description": "Credential"
   },
   "ownership": {
    "type": "string",
    "description": "Ownership"
   },
   "payment": {
    "type": "string",
    "description": "Payment"
   },
   "settlement": {
    "type": "string",
    "description": "Settlement"
   },
   "approval": {
    "type": "string",
    "description": "Approval"
   },
   "deviceChannelWhereApplicable": {
    "type": "string",
    "description": "Device/channel where applicable"
   },
   "ticketId": {
    "type": "string",
    "description": "Ticket ID"
   },
   "order": {
    "type": "string",
    "description": "Order"
   },
   "resaleTransaction": {
    "type": "string",
    "description": "Resale transaction"
   },
   "seat": {
    "type": "string",
    "description": "Seat"
   },
   "event": {
    "type": "string",
    "description": "Event"
   },
   "paymentReference": {
    "type": "string",
    "description": "Payment reference"
   },
   "subjectToRolePermissions": {
    "type": "string",
    "description": "subject to role permissions"
   },
   "finance": {
    "type": "string",
    "description": "Finance"
   },
   "compliance": {
    "type": "string",
    "description": "Compliance"
   },
   "fraudInvestigation": {
    "type": "string",
    "description": "Fraud investigation"
   },
   "customerDispute": {
    "type": "string",
    "description": "Customer dispute"
   },
   "venueOperations": {
    "type": "string",
    "description": "Venue operations"
   }
  }
 },
 "ResaleFraudDuplicateSaleProtectionView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over orders state, assembled at read time from tables that already exist",
  "description": "**What Resale Fraud & Duplicate Sale Protection displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "multipleResaleAttempts": {
    "type": "integer",
    "description": "Multiple resale attempts"
   },
   "sameTicketListedSimultaneously": {
    "type": "string",
    "description": "Same ticket listed simultaneously"
   },
   "unusualSellerVolume": {
    "type": "integer",
    "description": "Unusual seller volume"
   },
   "highFrequencyResale": {
    "type": "string",
    "description": "High-frequency resale"
   },
   "suspiciousPricing": {
    "type": "string",
    "description": "Suspicious pricing"
   },
   "multipleAccounts": {
    "type": "integer",
    "description": "Multiple accounts"
   },
   "paymentAnomalies": {
    "type": "integer",
    "description": "Payment anomalies"
   },
   "identityMismatch": {
    "type": "string",
    "description": "Identity mismatch"
   },
   "credentialReuse": {
    "type": "string",
    "description": "Credential reuse"
   },
   "repeatedFailedTransactions": {
    "type": "integer",
    "description": "Repeated failed transactions"
   },
   "accountDeviceAnomaliesWherePermitted": {
    "type": "string",
    "description": "Account/device anomalies where permitted"
   },
   "withExplainableContributingFactors": {
    "type": "string",
    "description": "with explainable contributing factors"
   },
   "allow": {
    "type": "boolean",
    "description": "Allow"
   },
   "requireVerification": {
    "type": "boolean",
    "description": "Require verification"
   },
   "holdTransaction": {
    "type": "string",
    "description": "Hold transaction"
   },
   "requireManualReview": {
    "type": "boolean",
    "description": "Require manual review"
   },
   "revokedSellerCredential": {
    "type": "string",
    "description": "Revoked seller credential"
   },
   "duplicatedCredentials": {
    "type": "string",
    "description": "Duplicated credentials"
   },
   "invalidatedTickets": {
    "type": "string",
    "description": "Invalidated tickets"
   }
  }
 },
 "ResaleOperationsCommandCenterView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over orders state, assembled at read time from tables that already exist",
  "description": "**What Resale Operations Command Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "resaleTransactionsToday": {
    "type": "string",
    "description": "Resale Transactions Today"
   },
   "grossResaleValue": {
    "type": "string",
    "description": "Gross Resale Value"
   },
   "completedTransfers": {
    "type": "integer",
    "description": "Completed Transfers"
   },
   "pendingTransfers": {
    "type": "integer",
    "description": "Pending Transfers"
   },
   "failedTransfers": {
    "type": "integer",
    "description": "Failed Transfers"
   },
   "credentialReissues": {
    "type": "integer",
    "description": "Credential Reissues"
   },
   "pendingSellerSettlements": {
    "type": "integer",
    "description": "Pending Seller Settlements"
   },
   "settlementValue": {
    "type": "string",
    "description": "Settlement Value"
   },
   "transactionsUnderReview": {
    "type": "string",
    "description": "Transactions Under Review"
   },
   "fraudAlerts": {
    "type": "integer",
    "description": "Fraud Alerts"
   },
   "disputes": {
    "type": "integer",
    "description": "Disputes"
   },
   "refunds": {
    "type": "integer",
    "description": "Refunds"
   },
   "resaleTransactionId": {
    "type": "string",
    "description": "Resale Transaction ID"
   },
   "listingId": {
    "type": "string",
    "description": "Listing ID"
   },
   "originalOrderId": {
    "type": "string",
    "description": "Original Order ID"
   },
   "originalTicketId": {
    "type": "string",
    "description": "Original Ticket ID"
   },
   "event": {
    "type": "string",
    "description": "Event"
   },
   "venue": {
    "type": "string",
    "description": "Venue"
   },
   "seller": {
    "type": "string",
    "description": "Seller"
   },
   "buyer": {
    "type": "string",
    "description": "Buyer"
   },
   "sectionRowSeat": {
    "type": "string",
    "description": "Section / Row / Seat"
   },
   "resalePrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Resale Price"
   },
   "buyerTotal": {
    "type": "string",
    "description": "Buyer Total"
   },
   "sellerProceeds": {
    "type": "string",
    "description": "Seller Proceeds"
   },
   "purchaseStatus": {
    "type": "string",
    "description": "Purchase Status"
   },
   "ownershipStatus": {
    "type": "string",
    "description": "Ownership Status"
   },
   "credentialStatus": {
    "type": "string",
    "description": "Credential Status"
   },
   "settlementStatus": {
    "type": "string",
    "description": "Settlement Status"
   },
   "riskScore": {
    "type": "number",
    "description": "Risk Score"
   },
   "transactionDate": {
    "type": "string",
    "format": "date-time",
    "description": "Transaction Date"
   },
   "statusesType": {
    "type": "string",
    "enum": [
     "paymentFailed",
     "transferFailed",
     "underReview",
     "suspended",
     "refunded",
     "disputed",
     "cancelled"
    ],
    "description": "Vocabulary listed under Exception statuses."
   },
   "holdTransaction": {
    "type": "string",
    "description": "Hold transaction"
   }
  }
 },
 "SellerSettlementPayoutManagementView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over orders state, assembled at read time from tables that already exist",
  "description": "**What Seller Settlement & Payout Management displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "settlementId": {
    "type": "string",
    "description": "Settlement ID"
   },
   "resaleTransaction": {
    "type": "string",
    "description": "Resale Transaction"
   },
   "seller": {
    "type": "string",
    "description": "Seller"
   },
   "listingPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Listing Price"
   },
   "sellerFee": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Seller Fee"
   },
   "commission": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Commission"
   },
   "processingFee": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Processing fee"
   },
   "applicableTax": {
    "type": "string",
    "description": "Applicable tax"
   },
   "adjustments": {
    "type": "integer",
    "description": "Adjustments"
   },
   "sellerProceeds": {
    "type": "integer",
    "description": "Seller Proceeds"
   },
   "currency": {
    "type": "string",
    "description": "Currency"
   },
   "payoutMethod": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Payout method"
   },
   "settlementStatus": {
    "type": "integer",
    "description": "Settlement status"
   },
   "expectedPayoutDate": {
    "type": "string",
    "format": "date-time",
    "description": "Expected payout date"
   },
   "statusesType": {
    "type": "string",
    "enum": [
     "onHold",
     "failed",
     "reversed",
     "disputed"
    ],
    "description": "Vocabulary listed under Exception statuses."
   },
   "immediatelyAfterResale": {
    "type": "string",
    "description": "Immediately after resale"
   },
   "xDaysAfterResale": {
    "type": "string",
    "description": "X days after resale"
   },
   "afterEventCompletion": {
    "type": "string",
    "description": "After event completion"
   },
   "xDaysAfterEvent": {
    "type": "string",
    "description": "X days after event"
   },
   "afterAccessValidation": {
    "type": "string",
    "description": "After access validation"
   },
   "operatorDefinedSettlementCycle": {
    "type": "string",
    "description": "Operator-defined settlement cycle"
   },
   "minimumPayoutThreshold": {
    "type": "integer",
    "description": "Minimum payout threshold"
   },
   "settlementBatches": {
    "type": "string",
    "description": "Settlement batches"
   },
   "sellerVerification": {
    "type": "string",
    "description": "Seller verification"
   },
   "paymentAccountVerification": {
    "type": "string",
    "description": "Payment account verification"
   },
   "manualHold": {
    "type": "string",
    "description": "Manual hold"
   },
   "complianceHold": {
    "type": "string",
    "description": "Compliance hold"
   },
   "refundDisputeHold": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Refund/dispute hold"
   }
  }
 },
 "TicketOwnershipTransferManagementView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over orders state, assembled at read time from tables that already exist",
  "description": "**What Ticket Ownership Transfer Management displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "customer": {
    "type": "string",
    "description": "Customer"
   },
   "originalOrder": {
    "type": "string",
    "description": "Original order"
   },
   "ticket": {
    "type": "string",
    "description": "Ticket"
   },
   "ownershipStatus": {
    "type": "string",
    "description": "Ownership status"
   },
   "newResaleOrder": {
    "type": "integer",
    "description": "New resale order"
   },
   "identity": {
    "type": "string",
    "description": "Identity"
   },
   "membershipAccount": {
    "type": "string",
    "description": "Membership/account"
   },
   "event": {
    "type": "string",
    "description": "Event"
   },
   "product": {
    "type": "string",
    "description": "Product"
   },
   "seat": {
    "type": "string",
    "description": "Seat"
   },
   "entitlements": {
    "type": "string",
    "description": "Entitlements"
   },
   "validity": {
    "type": "string",
    "description": "Validity"
   },
   "buyerPaymentCompleted": {
    "type": "string",
    "description": "Buyer payment completed"
   },
   "listingRemainsValid": {
    "type": "string",
    "description": "Listing remains valid"
   },
   "sellerStillOwnsTicket": {
    "type": "string",
    "description": "Seller still owns ticket"
   },
   "ticketHasNotBeenScanned": {
    "type": "string",
    "description": "Ticket has not been scanned"
   },
   "ticketHasNotBeenRefunded": {
    "type": "string",
    "description": "Ticket has not been refunded"
   },
   "eventRemainsActive": {
    "type": "integer",
    "description": "Event remains active"
   },
   "capacityRemainsValid": {
    "type": "integer",
    "description": "Capacity remains valid"
   },
   "noFraudHoldExists": {
    "type": "string",
    "description": "No fraud hold exists"
   },
   "sellerOwnershipHistoricalTransferred": {
    "type": "string",
    "description": "Seller Ownership: Historical / Transferred"
   },
   "buyerOwnershipActive": {
    "type": "integer",
    "description": "Buyer Ownership: Active"
   },
   "admissionEntitlement": {
    "type": "string",
    "description": "Admission entitlement"
   },
   "seatAssignment": {
    "type": "string",
    "description": "Seat assignment"
   },
   "addOnsWherePermitted": {
    "type": "string",
    "description": "Add-ons where permitted"
   },
   "accessRights": {
    "type": "string",
    "description": "Access rights"
   },
   "associatedBenefits": {
    "type": "string",
    "description": "Associated benefits"
   }
  }
 }
}
```
