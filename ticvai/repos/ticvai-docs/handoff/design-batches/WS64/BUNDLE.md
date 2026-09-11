# WS64 — Ticket Resale Marketplace board 3

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
| `ADM-298` | My Tickets & Resale Marketplace Entry | configEditor | 1 | 0 | — |
| `ADM-299` | Resale Eligibility & Ticket Selection | listDetail | 1 | 0 | — |
| `ADM-300` | Create Listing & Resale Price Selection | listDetail | 1 | 0 | — |
| `ADM-301` | Fees, Seller Proceeds & Listing Confirmation | listDetail | 1 | 0 | — |
| `ADM-302` | My Resale Listings & Seller Dashboard | commandCentre | 1 | 0 | — |
| `ADM-303` | Official Resale Marketplace & Buyer Discovery | listDetail | 1 | 0 | — |
| `ADM-304` | Resale Ticket Detail, Seat Selection & Primary-vs-Resale Experience | listDetail | 1 | 0 | — |
| `ADM-305` | Buyer Checkout, Inventory Hold & Secure Payment | configEditor | 1 | 0 | — |
| `ADM-306` | Resale Confirmation, Ownership Transfer & Ticket Delivery | listDetail | 1 | 0 | — |
| `ADM-307` | White-Label Marketplace Deployment & Experience Architecture | configEditor | 1 | 0 | — |

## Thin screens in this batch

**ADM-299, ADM-300, ADM-301, ADM-304, ADM-305, ADM-306 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "ADM-298",
  "name": "My Tickets & Resale Marketplace Entry",
  "module": "Commercial",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Ticket Resale Marketplace_Reference.pdf",
   "board": "3",
   "number": "3.3.1",
   "page": 40
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/my-tickets-resale-marketplace-entry-adm-298",
   "component": "apps/ticvai-web/src/routes/commercial/MyTicketsResaleMarketplaceEntry.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-002"
   ],
   "exitTo": [
    "ADM-002",
    "ADM-299",
    "ADM-300",
    "ADM-301",
    "ADM-302",
    "ADM-303",
    "ADM-304",
    "ADM-305",
    "ADM-306",
    "ADM-307"
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
     "to": "ADM-299",
     "trigger": "Works in Resale Eligibility & Ticket Selection",
     "provenance": "flow F173 step 1→2",
     "operation": "listTicketResaleMarketplace"
    },
    {
     "to": "ADM-300",
     "trigger": "Works in Create Listing & Resale Price Selection",
     "provenance": "flow F173 step 3→4",
     "operation": "listTicketResaleMarketplace"
    },
    {
     "to": "ADM-301",
     "trigger": "Works in Fees, Seller Proceeds & Listing Confirmation",
     "provenance": "flow F173 step 5→6",
     "operation": "listTicketResaleMarketplace"
    },
    {
     "to": "ADM-302",
     "trigger": "Works in My Resale Listings & Seller Dashboard",
     "provenance": "flow F173 step 7→8",
     "operation": "listTicketResaleMarketplace"
    },
    {
     "to": "ADM-303",
     "trigger": "Works in Official Resale Marketplace & Buyer Discovery",
     "provenance": "flow F173 step 9→10",
     "operation": "listTicketResaleMarketplace"
    },
    {
     "to": "ADM-304",
     "trigger": "Works in Resale Ticket Detail, Seat Selection & Primary-vs-Resale Experience",
     "provenance": "flow F173 step 11→12",
     "operation": "listTicketResaleMarketplace"
    },
    {
     "to": "ADM-305",
     "trigger": "Works in Buyer Checkout, Inventory Hold & Secure Payment",
     "provenance": "flow F173 step 13→14",
     "operation": "listTicketResaleMarketplace"
    },
    {
     "to": "ADM-306",
     "trigger": "Works in Resale Confirmation, Ownership Transfer & Ticket Delivery",
     "provenance": "flow F173 step 15→16",
     "operation": "listTicketResaleMarketplace"
    },
    {
     "to": "ADM-307",
     "trigger": "Works in White-Label Marketplace Deployment & Experience Architecture",
     "provenance": "flow F173 step 17→18",
     "operation": "listTicketResaleMarketplace"
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Depending on ticket configuration) and no display directory — it is settings, not a population",
  "purpose": "Provide the authenticated ticket holder with a simple and secure entry point into the official resale journey. The preferred starting point should be the customer's existing: My Account → My Tickets rather than asking customers to manually enter ticket numbers or upload ticket PDFs.",
  "purposeNote": "An authenticated customer can immediately identify which owned tickets are eligible for resale and begin the official resale process without manually proving ticket ownership.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "View Ticket",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 40 §Depending on ticket configuration"
      },
      {
       "kind": "selectField",
       "label": "Add to Wallet",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 40 §Depending on ticket configuration"
      },
      {
       "kind": "selectField",
       "label": "Transfer",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 40 §Depending on ticket configuration"
      },
      {
       "kind": "selectField",
       "label": "Exchange",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 40 §Depending on ticket configuration"
      },
      {
       "kind": "selectField",
       "label": "Upgrade",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 40 §Depending on ticket configuration"
      },
      {
       "kind": "selectField",
       "label": "Resell Ticket",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 40 §Depending on ticket configuration"
      },
      {
       "kind": "selectField",
       "label": "Request Refund",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 40 §Depending on ticket configuration"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The tickets resale marketplace configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the tickets resale marketplace untouched.",
   "emptyFirstRun": "No tickets resale marketplace configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listTicketResaleMarketplace",
    "contract": "orders",
    "purpose": "My Tickets & Resale Marketplace Entry",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-298"
  },
  "apisNote": "Regenerated 9 September 2026 from Ticket Resale Marketplace_Reference.pdf page 40. 0 of 0 labels bound to a contract property; 7 of 44 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-299",
  "name": "Resale Eligibility & Ticket Selection",
  "module": "Commercial",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Ticket Resale Marketplace_Reference.pdf",
   "board": "3",
   "number": "3.3.2",
   "page": 42
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/resale-eligibility-ticket-selection-adm-299",
   "component": "apps/ticvai-web/src/routes/commercial/ResaleEligibilityTicketSelection.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-298"
   ],
   "exitTo": [
    "ADM-298"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-298, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-298",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F173 step 2→3",
     "operation": "listResaleEligibilityTicket"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Explain whether the selected ticket can be resold before allowing a listing to be created.",
  "purposeNote": "Customers receive an immediate, understandable and authoritative resale eligibility decision before entering the listing process.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every resale eligibility ticket",
       "columns": [
        "✓ Your ticket is eligible for resale",
        "ResaleEligibilityTicketSelectionView.event",
        "ResaleEligibilityTicketSelectionView.date",
        "ResaleEligibilityTicketSelectionView.venue",
        "ResaleEligibilityTicketSelectionView.seat",
        "ResaleEligibilityTicketSelectionView.originalPrice",
        "ResaleEligibilityTicketSelectionView.resaleClosingTime",
        "ResaleEligibilityTicketSelectionView.applicableMarketplaceConditions"
       ],
       "bindsTo": "ResaleEligibilityTicketSelectionView",
       "operation": "listResaleEligibilityTicket",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 42 §Display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected resale eligibility ticket",
       "bindsTo": "ResaleEligibilityTicketSelectionView",
       "columns": [
        "✓ Your ticket is eligible for resale",
        "ResaleEligibilityTicketSelectionView.event",
        "ResaleEligibilityTicketSelectionView.date",
        "ResaleEligibilityTicketSelectionView.venue",
        "ResaleEligibilityTicketSelectionView.seat",
        "ResaleEligibilityTicketSelectionView.originalPrice",
        "ResaleEligibilityTicketSelectionView.resaleClosingTime",
        "ResaleEligibilityTicketSelectionView.applicableMarketplaceConditions"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Eligibility Check”, “Check applicable conditions such as”, “Do not simply display”, “Multiple Tickets”, “Backend Boundary”.",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 42 §Display"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The resale eligibility ticket list.",
   "error": "Could not load. Names which read failed and leaves the resale eligibility ticket untouched.",
   "emptyFirstRun": "No resale eligibility ticket yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the resale eligibility ticket are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listResaleEligibilityTicket",
    "contract": "orders",
    "purpose": "Resale Eligibility & Ticket Selection",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "✓ Your ticket is eligible for resale",
    "ResaleEligibilityTicketSelectionView.event",
    "ResaleEligibilityTicketSelectionView.date",
    "ResaleEligibilityTicketSelectionView.venue",
    "ResaleEligibilityTicketSelectionView.seat",
    "ResaleEligibilityTicketSelectionView.originalPrice"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-299"
  },
  "apisNote": "Regenerated 9 September 2026 from Ticket Resale Marketplace_Reference.pdf page 42. 7 of 8 labels bound to a contract property; 8 of 43 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-300",
  "name": "Create Listing & Resale Price Selection",
  "module": "Commercial",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Ticket Resale Marketplace_Reference.pdf",
   "board": "3",
   "number": "3.3.3",
   "page": 43
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/create-listing-resale-price-selection-adm-300",
   "component": "apps/ticvai-web/src/routes/commercial/CreateListingResalePriceSelection.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-298"
   ],
   "exitTo": [
    "ADM-298"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-298, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-298",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F173 step 4→5",
     "operation": "listCreateListingResale"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Allow an eligible seller to select a resale price within the client's approved marketplace rules.",
  "purposeNote": "A seller can select a valid resale price while TICVAI automatically enforces the operator's configured commercial rules.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Ticket Resale Marketplace_Reference.pdf, page 43"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Ticket Resale Marketplace_Reference.pdf, page 43"
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
       "impliedBy": "listCreateListingResale",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The create listing resale list.",
   "error": "Could not load. Names which read failed and leaves the create listing resale untouched.",
   "emptyFirstRun": "No create listing resale yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the create listing resale are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listCreateListingResale",
    "contract": "orders",
    "purpose": "Create Listing & Resale Price Selection",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "CreateListingResalePriceSelectionView.faceValueOnly",
    "CreateListingResalePriceSelectionView.fixedPrice",
    "CreateListingResalePriceSelectionView.sellerSelectedPrice",
    "CreateListingResalePriceSelectionView.cappedPrice",
    "CreateListingResalePriceSelectionView.operatorControlled"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-300"
  },
  "apisNote": "Regenerated 9 September 2026 from Ticket Resale Marketplace_Reference.pdf page 43. 0 of 0 labels bound to a contract property; 0 of 21 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-301",
  "name": "Fees, Seller Proceeds & Listing Confirmation",
  "module": "Commercial",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Ticket Resale Marketplace_Reference.pdf",
   "board": "3",
   "number": "3.3.4",
   "page": 45
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/fees-seller-proceeds-listing-confirmation-adm-301",
   "component": "apps/ticvai-web/src/routes/commercial/FeesSellerProceedsListingConfirmation.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-298"
   ],
   "exitTo": [
    "ADM-298"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-298, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-298",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F173 step 6→7",
     "operation": "listFeeSellerProceed"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Provide complete financial transparency before the seller commits to publishing the listing. This is essential to prevent later disputes.",
  "purposeNote": "The seller understands the resale price, applicable fees, estimated proceeds and settlement conditions before submitting the ticket for listing.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Ticket Resale Marketplace_Reference.pdf, page 45"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Ticket Resale Marketplace_Reference.pdf, page 45"
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
       "impliedBy": "listFeeSellerProceed",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The fees seller proceeds list.",
   "error": "Could not load. Names which read failed and leaves the fees seller proceeds untouched.",
   "emptyFirstRun": "No fees seller proceeds yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the fees seller proceeds are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listFeeSellerProceed",
    "contract": "orders",
    "purpose": "Fees, Seller Proceeds & Listing Confirmation",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "FeesSellerProceedsListingConfirmationView.yourSellingPrice",
    "FeesSellerProceedsListingConfirmationView.aed2200",
    "FeesSellerProceedsListingConfirmationView.aed000",
    "FeesSellerProceedsListingConfirmationView.youWillReceiveAed19800",
    "FeesSellerProceedsListingConfirmationView.clearlyExplainApplicableSettlementRules"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-301"
  },
  "apisNote": "Regenerated 9 September 2026 from Ticket Resale Marketplace_Reference.pdf page 45. 0 of 0 labels bound to a contract property; 0 of 27 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-302",
  "name": "My Resale Listings & Seller Dashboard",
  "module": "Commercial",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Ticket Resale Marketplace_Reference.pdf",
   "board": "3",
   "number": "3.3.5",
   "page": 46
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/my-resale-listings-seller-dashboard-adm-302",
   "component": "apps/ticvai-web/src/routes/commercial/MyResaleListingsSellerDashboard.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-298"
   ],
   "exitTo": [
    "ADM-298"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-298, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-298",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F173 step 8→9",
     "operation": "listResaleListingSeller"
    }
   ]
  },
  "density": "compact",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen both a metric directory (§Display; Show) and a per-row directory (§Each listing shows) — counts over a population, then the population",
  "purpose": "Give sellers a dedicated self-service workspace to manage their resale activity after publishing.",
  "purposeNote": "Sellers can independently understand and manage the complete status of their listings and settlements without contacting venue support for routine actions.",
  "layout": {
   "template": "dashboard",
   "regions": [
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "Active Listings",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 46 §Display",
       "bindsTo": "MyResaleListingsSellerDashboardView.activeListings"
      },
      {
       "kind": "metricTile",
       "label": "Pending Approval",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 46 §Display",
       "bindsTo": "MyResaleListingsSellerDashboardView.pendingApproval"
      },
      {
       "kind": "metricTile",
       "label": "Sold",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 46 §Display",
       "bindsTo": "MyResaleListingsSellerDashboardView.sold"
      },
      {
       "kind": "metricTile",
       "label": "Expiring Soon",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 46 §Display",
       "bindsTo": "MyResaleListingsSellerDashboardView.expiringSoon"
      },
      {
       "kind": "metricTile",
       "label": "Seller Proceeds",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 46 §Display",
       "bindsTo": "MyResaleListingsSellerDashboardView.sellerProceeds"
      },
      {
       "kind": "metricTile",
       "label": "Pending Settlement",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 46 §Display",
       "bindsTo": "MyResaleListingsSellerDashboardView.pendingSettlement"
      },
      {
       "kind": "metricTile",
       "label": "Paid Settlements",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 46 §Display",
       "bindsTo": "MyResaleListingsSellerDashboardView.paidSettlements"
      },
      {
       "kind": "metricTile",
       "label": "SOLD ✓",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 46 §Show"
      },
      {
       "kind": "metricTile",
       "label": "Selling Price: AED 220",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 46 §Show",
       "bindsTo": "MyResaleListingsSellerDashboardView.sellingPriceAed220"
      },
      {
       "kind": "metricTile",
       "label": "Estimated Proceeds: AED 198",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 46 §Show",
       "bindsTo": "MyResaleListingsSellerDashboardView.estimatedProceedsAed198"
      },
      {
       "kind": "metricTile",
       "label": "Settlement: Scheduled after event",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 46 §Show",
       "bindsTo": "MyResaleListingsSellerDashboardView.settlementScheduledAfterEvent"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "moduleTiles",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every resale listings seller",
       "columns": [
        "MyResaleListingsSellerDashboardView.event",
        "MyResaleListingsSellerDashboardView.date",
        "MyResaleListingsSellerDashboardView.seat",
        "MyResaleListingsSellerDashboardView.listingPrice",
        "MyResaleListingsSellerDashboardView.originalPrice",
        "MyResaleListingsSellerDashboardView.marketplaceStatus",
        "MyResaleListingsSellerDashboardView.viewsWhereApplicable",
        "MyResaleListingsSellerDashboardView.listingDate",
        "MyResaleListingsSellerDashboardView.expiry",
        "MyResaleListingsSellerDashboardView.sellerProceeds",
        "MyResaleListingsSellerDashboardView.settlementStatus"
       ],
       "bindsTo": "MyResaleListingsSellerDashboardView",
       "operation": "listResaleListingSeller",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 46 §Each listing shows"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected resale listings seller",
       "bindsTo": "MyResaleListingsSellerDashboardView",
       "columns": [
        "MyResaleListingsSellerDashboardView.event",
        "MyResaleListingsSellerDashboardView.date",
        "MyResaleListingsSellerDashboardView.seat",
        "MyResaleListingsSellerDashboardView.listingPrice",
        "MyResaleListingsSellerDashboardView.originalPrice",
        "MyResaleListingsSellerDashboardView.marketplaceStatus",
        "MyResaleListingsSellerDashboardView.viewsWhereApplicable",
        "MyResaleListingsSellerDashboardView.listingDate",
        "MyResaleListingsSellerDashboardView.expiry",
        "MyResaleListingsSellerDashboardView.sellerProceeds",
        "MyResaleListingsSellerDashboardView.settlementStatus"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Reserved by Buyer”.",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 46 §Each listing shows"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The resale listings seller list; the counts above it resolve separately.",
   "error": "Could not load. Names which read failed and leaves the resale listings seller untouched.",
   "emptyFirstRun": "No resale listings seller yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the resale listings seller are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listResaleListingSeller",
    "contract": "orders",
    "purpose": "My Resale Listings & Seller Dashboard",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-302"
  },
  "apisNote": "Regenerated 9 September 2026 from Ticket Resale Marketplace_Reference.pdf page 46. 21 of 21 labels bound to a contract property; 22 of 35 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-303",
  "name": "Official Resale Marketplace & Buyer Discovery",
  "module": "Commercial",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Ticket Resale Marketplace_Reference.pdf",
   "board": "3",
   "number": "3.3.6",
   "page": 48
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/official-resale-marketplace-buyer-discovery-adm-303",
   "component": "apps/ticvai-web/src/routes/commercial/OfficialResaleMarketplaceBuyerDiscovery.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-298"
   ],
   "exitTo": [
    "ADM-298"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-298, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-298",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F173 step 10→11",
     "operation": "listOfficialResaleMarketplace"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Provide buyers with a trusted client-branded marketplace for discovering authentic resale inventory.",
  "purposeNote": "Customers can discover legitimate resale inventory in a trusted marketplace without interacting directly with unknown sellers.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 4 actions on this screen and the screen declares 1 operation.** Unserved: Ticket Type, Price, Primary only. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Ticket Resale Marketplace_Reference.pdf, page 48 §Support"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Ticket Resale Marketplace_Reference.pdf, page 48"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Ticket Resale Marketplace_Reference.pdf, page 48"
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
       "label": "Ticket Type",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 48 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Price",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 48 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Resale only",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 48 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Primary only",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 48 §Support"
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
   "loading": "The official resale marketplace list.",
   "error": "Could not load. Names which read failed and leaves the official resale marketplace untouched.",
   "emptyFirstRun": "No official resale marketplace yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the official resale marketplace are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listOfficialResaleMarketplace",
    "contract": "orders",
    "purpose": "Official Resale Marketplace & Buyer Discovery",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "OfficialResaleMarketplaceBuyerDiscoveryView.officialTicketsOfficialResale",
    "OfficialResaleMarketplaceBuyerDiscoveryView.asASeparateMarketplacePage",
    "OfficialResaleMarketplaceBuyerDiscoveryView.event",
    "OfficialResaleMarketplaceBuyerDiscoveryView.venue",
    "OfficialResaleMarketplaceBuyerDiscoveryView.date"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-303"
  },
  "apisNote": "Regenerated 9 September 2026 from Ticket Resale Marketplace_Reference.pdf page 48. 0 of 0 labels bound to a contract property; 4 of 34 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-304",
  "name": "Resale Ticket Detail, Seat Selection & Primary-vs-Resale Experience",
  "module": "Commercial",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Ticket Resale Marketplace_Reference.pdf",
   "board": "3",
   "number": "3.3.7",
   "page": 49
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/resale-ticket-detail-seat-selection-primary-vs-resale-ex-adm-304",
   "component": "apps/ticvai-web/src/routes/commercial/ResaleTicketDetailSeatSelectionPrimaryVsResaleEx.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-298"
   ],
   "exitTo": [
    "ADM-298"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-298, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-298",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F173 step 12→13",
     "operation": "listResaleTicketDetail"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Allow customers to understand exactly what they are purchasing and distinguish resale inventory from primary inventory.",
  "purposeNote": "Buyers clearly understand whether a ticket is primary or resale inventory, its location/entitlements and the complete applicable price before checkout.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every resale ticket detail",
       "columns": [
        "ResaleTicketDetailSeatSelectionPrimaryVsResaleExperiView.event",
        "ResaleTicketDetailSeatSelectionPrimaryVsResaleExperiView.venue",
        "ResaleTicketDetailSeatSelectionPrimaryVsResaleExperiView.performance",
        "ResaleTicketDetailSeatSelectionPrimaryVsResaleExperiView.ticketType",
        "ResaleTicketDetailSeatSelectionPrimaryVsResaleExperiView.section",
        "ResaleTicketDetailSeatSelectionPrimaryVsResaleExperiView.row",
        "ResaleTicketDetailSeatSelectionPrimaryVsResaleExperiView.seat",
        "ResaleTicketDetailSeatSelectionPrimaryVsResaleExperiView.accessibilityAttributes",
        "ResaleTicketDetailSeatSelectionPrimaryVsResaleExperiView.applicableBenefits",
        "ResaleTicketDetailSeatSelectionPrimaryVsResaleExperiView.resalePrice",
        "ResaleTicketDetailSeatSelectionPrimaryVsResaleExperiView.fees",
        "ResaleTicketDetailSeatSelectionPrimaryVsResaleExperiView.applicableRestrictions"
       ],
       "bindsTo": "ResaleTicketDetailSeatSelectionPrimaryVsResaleExperiView",
       "operation": "listResaleTicketDetail",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 49 §Display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected resale ticket detail",
       "bindsTo": "ResaleTicketDetailSeatSelectionPrimaryVsResaleExperiView",
       "columns": [
        "ResaleTicketDetailSeatSelectionPrimaryVsResaleExperiView.event",
        "ResaleTicketDetailSeatSelectionPrimaryVsResaleExperiView.venue",
        "ResaleTicketDetailSeatSelectionPrimaryVsResaleExperiView.performance",
        "ResaleTicketDetailSeatSelectionPrimaryVsResaleExperiView.ticketType",
        "ResaleTicketDetailSeatSelectionPrimaryVsResaleExperiView.section",
        "ResaleTicketDetailSeatSelectionPrimaryVsResaleExperiView.row",
        "ResaleTicketDetailSeatSelectionPrimaryVsResaleExperiView.seat",
        "ResaleTicketDetailSeatSelectionPrimaryVsResaleExperiView.accessibilityAttributes",
        "ResaleTicketDetailSeatSelectionPrimaryVsResaleExperiView.applicableBenefits",
        "ResaleTicketDetailSeatSelectionPrimaryVsResaleExperiView.resalePrice",
        "ResaleTicketDetailSeatSelectionPrimaryVsResaleExperiView.fees",
        "ResaleTicketDetailSeatSelectionPrimaryVsResaleExperiView.applicableRestrictions"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Reserved Seating”, “Unavailable”, “AED 195”, “Important Commercial Benefit”, “Listing Availability”.",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 49 §Display"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The resale ticket detail list.",
   "error": "Could not load. Names which read failed and leaves the resale ticket detail untouched.",
   "emptyFirstRun": "No resale ticket detail yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the resale ticket detail are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listResaleTicketDetail",
    "contract": "orders",
    "purpose": "Resale Ticket Detail, Seat Selection & Primary-vs-Resale Experience",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "ResaleTicketDetailSeatSelectionPrimaryVsResaleExperiView.event",
    "ResaleTicketDetailSeatSelectionPrimaryVsResaleExperiView.venue",
    "ResaleTicketDetailSeatSelectionPrimaryVsResaleExperiView.performance",
    "ResaleTicketDetailSeatSelectionPrimaryVsResaleExperiView.ticketType",
    "ResaleTicketDetailSeatSelectionPrimaryVsResaleExperiView.section",
    "ResaleTicketDetailSeatSelectionPrimaryVsResaleExperiView.row"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-304"
  },
  "apisNote": "Regenerated 9 September 2026 from Ticket Resale Marketplace_Reference.pdf page 49. 12 of 12 labels bound to a contract property; 14 of 25 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-305",
  "name": "Buyer Checkout, Inventory Hold & Secure Payment",
  "module": "Commercial",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Ticket Resale Marketplace_Reference.pdf",
   "board": "3",
   "number": "3.3.8",
   "page": 51
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/buyer-checkout-inventory-hold-secure-payment-adm-305",
   "component": "apps/ticvai-web/src/routes/commercial/BuyerCheckoutInventoryHoldSecurePayment.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-298"
   ],
   "exitTo": [
    "ADM-298"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-298, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-298",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F173 step 14→15",
     "operation": "listBuyerCheckoutInventory"
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Select Resale Ticket) and no display directory — it is settings, not a population",
  "purpose": "Provide a normal, secure TICVAI checkout while protecting the resale listing from simultaneous purchase.",
  "purposeNote": "One buyer can securely purchase the resale ticket while TICVAI prevents concurrent purchase and maintains complete transaction integrity.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "↓",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 51 §Select Resale Ticket"
      },
      {
       "kind": "dataTable",
       "derived": true,
       "impliedBy": "listBuyerCheckoutInventory",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The buyer checkout inventory configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the buyer checkout inventory untouched.",
   "emptyFirstRun": "No buyer checkout inventory configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listBuyerCheckoutInventory",
    "contract": "orders",
    "purpose": "Buyer Checkout, Inventory Hold & Secure Payment",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-305"
  },
  "apisNote": "Regenerated 9 September 2026 from Ticket Resale Marketplace_Reference.pdf page 51. 0 of 0 labels bound to a contract property; 1 of 25 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-306",
  "name": "Resale Confirmation, Ownership Transfer & Ticket Delivery",
  "module": "Commercial",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Ticket Resale Marketplace_Reference.pdf",
   "board": "3",
   "number": "3.3.9",
   "page": 52
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/resale-confirmation-ownership-transfer-ticket-delivery-adm-306",
   "component": "apps/ticvai-web/src/routes/commercial/ResaleConfirmationOwnershipTransferTicketDeliver.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-298"
   ],
   "exitTo": [
    "ADM-298"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-298, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-298",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F173 step 16→17",
     "operation": "listResaleConfirmationOwnership"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Provide the customer-facing completion experience after successful payment while the backend performs the secure entitlement transfer.",
  "purposeNote": "After successful resale, the buyer receives control of the valid entitlement and applicable credentials, while the seller can no longer use the transferred ticket.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Ticket Resale Marketplace_Reference.pdf, page 52"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Ticket Resale Marketplace_Reference.pdf, page 52"
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
       "impliedBy": "listResaleConfirmationOwnership",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The resale confirmation ownership list.",
   "error": "Could not load. Names which read failed and leaves the resale confirmation ownership untouched.",
   "emptyFirstRun": "No resale confirmation ownership yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the resale confirmation ownership are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listResaleConfirmationOwnership",
    "contract": "orders",
    "purpose": "Resale Confirmation, Ownership Transfer & Ticket Delivery",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "ResaleConfirmationOwnershipTransferTicketDeliveryView.followedBy",
    "ResaleConfirmationOwnershipTransferTicketDeliveryView.yourTicketIsReady",
    "ResaleConfirmationOwnershipTransferTicketDeliveryView.currentOwnerSellerA",
    "ResaleConfirmationOwnershipTransferTicketDeliveryView.previousOwnerSellerA",
    "ResaleConfirmationOwnershipTransferTicketDeliveryView.currentOwnerBuyerB"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-306"
  },
  "apisNote": "Regenerated 9 September 2026 from Ticket Resale Marketplace_Reference.pdf page 52. 0 of 0 labels bound to a contract property; 0 of 35 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-307",
  "name": "White-Label Marketplace Deployment & Experience Architecture",
  "module": "Commercial",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Ticket Resale Marketplace_Reference.pdf",
   "board": "3",
   "number": "3.3.10",
   "page": 54
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/white-label-marketplace-deployment-experience-architectu-adm-307",
   "component": "apps/ticvai-web/src/routes/commercial/WhiteLabelMarketplaceDeploymentExperienceArchite.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-298"
   ],
   "exitTo": [
    "ADM-298"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-298, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation."
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population",
  "purpose": "This is the key architecture/configuration screen It defines how each TICVAI client chooses to expose the resale marketplace to its customers. Deployment Model A — Embedded White-Label",
  "purposeNote": "Each TICVAI tenant can deploy a secure, branded resale marketplace using embedded, hosted or headless architecture without requiring a separate marketplace backend implementation. Board 3 — Final Screen Register # Customer / Experience Screen Primary Responsibility 3.3.1 My Tickets & Resale Marketplace Entry Seller marketplace entry",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 2 actions on this screen and the screen declares 1 operation.** Unserved: Domain configuration, Additional client languages. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Ticket Resale Marketplace_Reference.pdf, page 54 §Support"
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
       "label": "Marketplace Name",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 54 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Client Logo",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 54 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Brand Colors",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 54 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Typography",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 54 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Domain/Subdomain",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 54 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Support Contact",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 54 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Legal Links",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 54 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Seller Terms",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 54 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Buyer Terms",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 54 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Privacy",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 54 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Languages",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 54 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Authentication method",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 54 §Configure"
      },
      {
       "kind": "selectField",
       "label": "My Tickets",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 54 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Sell",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 54 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Buy",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 54 §Configure"
      },
      {
       "kind": "selectField",
       "label": "My Listings",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 54 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Transactions",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 54 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Settlements",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 54 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Help",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 54 §Configure"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Domain configuration",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 54 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Additional client languages",
       "provenance": "pack Ticket Resale Marketplace_Reference.pdf, page 54 §Support"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The white-label marketplace deployment configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the white-label marketplace deployment untouched.",
   "emptyFirstRun": "No white-label marketplace deployment configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listWhiteLabelMarketplace",
    "contract": "orders",
    "purpose": "White-Label Marketplace Deployment & Experience Architecture",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-307"
  },
  "apisNote": "Regenerated 9 September 2026 from Ticket Resale Marketplace_Reference.pdf page 54. 0 of 0 labels bound to a contract property; 21 of 131 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
 "listBuyerCheckoutInventory": {
  "method": "GET",
  "path": "/buyer-checkout-inventory",
  "contract": "orders",
  "summary": "Buyer Checkout, Inventory Hold & Secure Payment",
  "permission": "ORDER_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "BuyerCheckoutInventoryHoldSecurePaymentView"
 },
 "listCreateListingResale": {
  "method": "GET",
  "path": "/create-listing-resale",
  "contract": "orders",
  "summary": "Create Listing & Resale Price Selection",
  "permission": "ORDER_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "CreateListingResalePriceSelectionView"
 },
 "listFeeSellerProceed": {
  "method": "GET",
  "path": "/fee-seller-proceed",
  "contract": "orders",
  "summary": "Fees, Seller Proceeds & Listing Confirmation",
  "permission": "ORDER_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "FeesSellerProceedsListingConfirmationView"
 },
 "listOfficialResaleMarketplace": {
  "method": "GET",
  "path": "/official-resale-marketplace",
  "contract": "orders",
  "summary": "Official Resale Marketplace & Buyer Discovery",
  "permission": "ORDER_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "OfficialResaleMarketplaceBuyerDiscoveryView"
 },
 "listResaleConfirmationOwnership": {
  "method": "GET",
  "path": "/resale-confirmation-ownership",
  "contract": "orders",
  "summary": "Resale Confirmation, Ownership Transfer & Ticket Delivery",
  "permission": "ORDER_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "ResaleConfirmationOwnershipTransferTicketDeliveryView"
 },
 "listResaleEligibilityTicket": {
  "method": "GET",
  "path": "/resale-eligibility-ticket",
  "contract": "orders",
  "summary": "Resale Eligibility & Ticket Selection",
  "permission": "ORDER_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "ResaleEligibilityTicketSelectionView"
 },
 "listResaleListingSeller": {
  "method": "GET",
  "path": "/resale-listing-seller",
  "contract": "orders",
  "summary": "My Resale Listings & Seller Dashboard",
  "permission": "ORDER_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "MyResaleListingsSellerDashboardView"
 },
 "listResaleTicketDetail": {
  "method": "GET",
  "path": "/resale-ticket-detail",
  "contract": "orders",
  "summary": "Resale Ticket Detail, Seat Selection & Primary-vs-Resale Experience",
  "permission": "ORDER_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "ResaleTicketDetailSeatSelectionPrimaryVsResaleExperiView"
 },
 "listTicketResaleMarketplace": {
  "method": "GET",
  "path": "/ticket-resale-marketplace",
  "contract": "orders",
  "summary": "My Tickets & Resale Marketplace Entry",
  "permission": "ORDER_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "MyTicketsResaleMarketplaceEntryView"
 },
 "listWhiteLabelMarketplace": {
  "method": "GET",
  "path": "/white-label-marketplace",
  "contract": "orders",
  "summary": "White-Label Marketplace Deployment & Experience Architecture",
  "permission": "ORDER_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "WhiteLabelMarketplaceDeploymentExperienceArchitecturView"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "BuyerCheckoutInventoryHoldSecurePaymentView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over orders state, assembled at read time from tables that already exist",
  "description": "**What Buyer Checkout, Inventory Hold & Secure Payment displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "architecture": {
    "type": "string",
    "description": "architecture"
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
   "billingDetails": {
    "type": "string",
    "description": "Billing details"
   },
   "requiredParticipantInformation": {
    "type": "string",
    "description": "Required participant information"
   }
  }
 },
 "CreateListingResalePriceSelectionView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over orders state, assembled at read time from tables that already exist",
  "description": "**What Create Listing & Resale Price Selection displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "faceValueOnly": {
    "type": "string",
    "description": "Face Value Only"
   },
   "fixedPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Fixed Price"
   },
   "sellerSelectedPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Seller Selected Price"
   },
   "cappedPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Capped Price"
   },
   "operatorControlled": {
    "type": "string",
    "description": "Operator Controlled"
   },
   "aiRecommendedPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "AI Recommended Price"
   },
   "recommendedPriceAed215": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Recommended Price: AED 215"
   }
  }
 },
 "FeesSellerProceedsListingConfirmationView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over orders state, assembled at read time from tables that already exist",
  "description": "**What Fees, Seller Proceeds & Listing Confirmation displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "yourSellingPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Your Selling Price (the pack shows AED 220.00)"
   },
   "aed2200": {
    "type": "string",
    "description": "− AED 22.00"
   },
   "aed000": {
    "type": "string",
    "description": "− AED 0.00"
   },
   "youWillReceiveAed19800": {
    "type": "string",
    "description": "You will receive AED 198.00"
   },
   "clearlyExplainApplicableSettlementRules": {
    "type": "string",
    "description": "Clearly explain applicable settlement rules"
   },
   "marketplaceTerms": {
    "type": "integer",
    "description": "Marketplace Terms"
   },
   "sellerTerms": {
    "type": "integer",
    "description": "Seller Terms"
   },
   "cancellationPolicy": {
    "type": "string",
    "description": "Cancellation Policy"
   },
   "settlementConditions": {
    "type": "integer",
    "description": "Settlement Conditions"
   },
   "eventCancellationTreatment": {
    "type": "string",
    "description": "Event Cancellation Treatment"
   },
   "applicablePrivacyNotice": {
    "type": "string",
    "description": "Applicable privacy notice"
   },
   "storeTheApplicableTermsVersionAcceptance": {
    "type": "string",
    "description": "Store the applicable terms/version acceptance"
   },
   "eventMuseumNight": {
    "type": "string",
    "description": "Event: Museum Night"
   },
   "seatA18": {
    "type": "string",
    "description": "Seat: A18"
   },
   "originalPriceAed200": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Original Price: AED 200"
   },
   "resalePriceAed220": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Resale Price: AED 220"
   },
   "feeAed22": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Fee: AED 22"
   },
   "estimatedProceedsAed198": {
    "type": "string",
    "description": "Estimated Proceeds: AED 198"
   }
  }
 },
 "MyResaleListingsSellerDashboardView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over orders state, assembled at read time from tables that already exist",
  "description": "**What My Resale Listings & Seller Dashboard displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "activeListings": {
    "type": "integer",
    "description": "Active Listings"
   },
   "pendingApproval": {
    "type": "integer",
    "description": "Pending Approval"
   },
   "sold": {
    "type": "string",
    "description": "Sold"
   },
   "expiringSoon": {
    "type": "string",
    "description": "Expiring Soon"
   },
   "sellerProceeds": {
    "type": "integer",
    "description": "Seller Proceeds"
   },
   "pendingSettlement": {
    "type": "integer",
    "description": "Pending Settlement"
   },
   "paidSettlements": {
    "type": "integer",
    "description": "Paid Settlements"
   },
   "event": {
    "type": "string",
    "description": "Event"
   },
   "date": {
    "type": "string",
    "format": "date-time",
    "description": "Date"
   },
   "seat": {
    "type": "string",
    "description": "Seat"
   },
   "listingPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Listing Price"
   },
   "originalPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Original Price"
   },
   "marketplaceStatus": {
    "type": "string",
    "description": "Marketplace Status"
   },
   "viewsWhereApplicable": {
    "type": "string",
    "description": "Views where applicable"
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
   "settlementStatus": {
    "type": "string",
    "description": "Settlement Status"
   },
   "acceptAiPriceRecommendation": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Accept AI Price Recommendation"
   },
   "relist": {
    "type": "string",
    "description": "Relist"
   },
   "contactSupport": {
    "type": "boolean",
    "description": "Contact Support"
   },
   "sellingPriceAed220": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Selling Price: AED 220"
   },
   "estimatedProceedsAed198": {
    "type": "string",
    "description": "Estimated Proceeds: AED 198"
   },
   "settlementScheduledAfterEvent": {
    "type": "string",
    "format": "date-time",
    "description": "Settlement: Scheduled after event"
   }
  }
 },
 "MyTicketsResaleMarketplaceEntryView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over orders state, assembled at read time from tables that already exist",
  "description": "**What My Tickets & Resale Marketplace Entry displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "eventProduct": {
    "type": "string",
    "description": "Event/Product"
   },
   "venue": {
    "type": "string",
    "description": "Venue"
   },
   "dateTime": {
    "type": "string",
    "format": "date-time",
    "description": "Date/Time"
   },
   "ticketType": {
    "type": "string",
    "description": "Ticket Type"
   },
   "sectionRowSeat": {
    "type": "string",
    "description": "Section/Row/Seat"
   },
   "ticketHolder": {
    "type": "string",
    "description": "Ticket Holder"
   },
   "virtualTicketIdReference": {
    "type": "string",
    "description": "Virtual Ticket ID reference"
   },
   "ticketStatus": {
    "type": "string",
    "description": "Ticket Status"
   },
   "resaleStatus": {
    "type": "string",
    "description": "Resale Status"
   },
   "availableActions": {
    "type": "string",
    "description": "Available Actions"
   },
   "exchange": {
    "type": "string",
    "description": "Exchange"
   },
   "resellTicket": {
    "type": "string",
    "description": "Resell Ticket"
   },
   "requestRefund": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Request Refund"
   },
   "customerAccount": {
    "type": "string",
    "description": "Customer account"
   },
   "sso": {
    "type": "string",
    "description": "SSO"
   },
   "passwordlessLogin": {
    "type": "string",
    "description": "Passwordless login"
   },
   "otp": {
    "type": "string",
    "description": "OTP"
   },
   "appAuthentication": {
    "type": "string",
    "description": "App authentication"
   },
   "clientLogo": {
    "type": "string",
    "description": "Client logo"
   },
   "brand": {
    "type": "string",
    "description": "Brand"
   },
   "colors": {
    "type": "string",
    "description": "Colors"
   },
   "typography": {
    "type": "string",
    "description": "Typography"
   },
   "language": {
    "type": "string",
    "description": "Language"
   },
   "supportDetails": {
    "type": "string",
    "description": "Support details"
   },
   "marketplaceName": {
    "type": "string",
    "description": "Marketplace name"
   }
  }
 },
 "OfficialResaleMarketplaceBuyerDiscoveryView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over orders state, assembled at read time from tables that already exist",
  "description": "**What Official Resale Marketplace & Buyer Discovery displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "officialTicketsOfficialResale": {
    "type": "string",
    "description": "Official Tickets + Official Resale"
   },
   "asASeparateMarketplacePage": {
    "type": "string",
    "description": "as a separate marketplace page"
   },
   "event": {
    "type": "string",
    "description": "Event"
   },
   "venue": {
    "type": "string",
    "description": "Venue"
   },
   "date": {
    "type": "string",
    "format": "date-time",
    "description": "Date"
   },
   "performance": {
    "type": "string",
    "description": "Performance"
   },
   "ticketType": {
    "type": "string",
    "description": "Ticket Type"
   },
   "section": {
    "type": "string",
    "description": "Section"
   },
   "price": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Price"
   },
   "quantity": {
    "type": "integer",
    "description": "Quantity"
   },
   "accessibility": {
    "type": "string",
    "description": "Accessibility"
   },
   "resaleOnly": {
    "type": "string",
    "description": "Resale only"
   },
   "primaryOnly": {
    "type": "string",
    "description": "Primary only"
   },
   "andWhereAppropriate": {
    "type": "string",
    "description": "and, where appropriate"
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
   "address": {
    "type": "string",
    "description": "Address"
   },
   "paymentInformation": {
    "type": "string",
    "description": "Payment information"
   }
  }
 },
 "ResaleConfirmationOwnershipTransferTicketDeliveryView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over orders state, assembled at read time from tables that already exist",
  "description": "**What Resale Confirmation, Ownership Transfer & Ticket Delivery displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "followedBy": {
    "type": "string",
    "description": "followed by"
   },
   "yourTicketIsReady": {
    "type": "string",
    "description": "Your Ticket Is Ready ✓"
   },
   "currentOwnerSellerA": {
    "type": "string",
    "description": "Current Owner: Seller A"
   },
   "previousOwnerSellerA": {
    "type": "string",
    "description": "Previous Owner: Seller A"
   },
   "currentOwnerBuyerB": {
    "type": "string",
    "description": "Current Owner: Buyer B"
   },
   "dynamicQr": {
    "type": "string",
    "description": "Dynamic QR"
   },
   "mobileTicket": {
    "type": "string",
    "description": "Mobile Ticket"
   },
   "appleWallet": {
    "type": "string",
    "description": "Apple Wallet"
   },
   "googleWallet": {
    "type": "string",
    "description": "Google Wallet"
   },
   "rfidNfcAssignmentWhereApplicable": {
    "type": "string",
    "description": "RFID/NFC assignment where applicable"
   },
   "otherSupportedCredentialMedia": {
    "type": "string",
    "description": "Other supported credential media"
   },
   "yourTicketHasBeenSold": {
    "type": "string",
    "description": "Your ticket has been sold"
   },
   "settlementStatusPending": {
    "type": "integer",
    "description": "Settlement Status: Pending"
   }
  }
 },
 "ResaleEligibilityTicketSelectionView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over orders state, assembled at read time from tables that already exist",
  "description": "**What Resale Eligibility & Ticket Selection displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "ticketOwnership": {
    "type": "string",
    "description": "Ticket ownership"
   },
   "paymentStatus": {
    "type": "string",
    "description": "Payment status"
   },
   "ticketValidity": {
    "type": "string",
    "description": "Ticket validity"
   },
   "scanUseStatus": {
    "type": "string",
    "description": "Scan/use status"
   },
   "eventStatus": {
    "type": "string",
    "description": "Event status"
   },
   "resaleWindow": {
    "type": "string",
    "format": "date-time",
    "description": "Resale window"
   },
   "ticketType": {
    "type": "string",
    "description": "Ticket type"
   },
   "product": {
    "type": "string",
    "description": "Product"
   },
   "promotionRestrictions": {
    "type": "string",
    "description": "Promotion restrictions"
   },
   "membershipRestrictions": {
    "type": "string",
    "description": "Membership restrictions"
   },
   "existingListing": {
    "type": "string",
    "description": "Existing listing"
   },
   "fraudSecurityHold": {
    "type": "string",
    "description": "Fraud/security hold"
   },
   "with": {
    "type": "string",
    "description": "with"
   },
   "event": {
    "type": "string",
    "description": "Event"
   },
   "date": {
    "type": "string",
    "format": "date-time",
    "description": "Date"
   },
   "venue": {
    "type": "string",
    "description": "Venue"
   },
   "seat": {
    "type": "string",
    "description": "Seat"
   },
   "originalPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Original price"
   },
   "resaleClosingTime": {
    "type": "string",
    "format": "date-time",
    "description": "Resale closing time"
   },
   "applicableMarketplaceConditions": {
    "type": "integer",
    "description": "Applicable marketplace conditions"
   },
   "error5042": {
    "type": "string",
    "description": "Error 5042"
   },
   "a14": {
    "type": "string",
    "description": "A14 ☑"
   },
   "a15": {
    "type": "string",
    "description": "A15 ☑"
   },
   "a16": {
    "type": "string",
    "description": "A16 ☐"
   },
   "a17": {
    "type": "string",
    "description": "A17 ☐"
   },
   "sellIndividually": {
    "type": "string",
    "description": "Sell individually"
   },
   "sellSelectedTickets": {
    "type": "string",
    "description": "Sell selected tickets"
   },
   "sellTogetherOnly": {
    "type": "string",
    "description": "Sell together only"
   },
   "adjacentSeatGroup": {
    "type": "string",
    "description": "Adjacent-seat group"
   }
  }
 },
 "ResaleTicketDetailSeatSelectionPrimaryVsResaleExperiView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over orders state, assembled at read time from tables that already exist",
  "description": "**What Resale Ticket Detail, Seat Selection & Primary-vs-Resale Experience displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "integrateWithTicvaiSeatMap": {
    "type": "string",
    "description": "Integrate with TICVAI Seat Map"
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
   "ticketType": {
    "type": "string",
    "description": "Ticket Type"
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
   "accessibilityAttributes": {
    "type": "integer",
    "description": "Accessibility attributes"
   },
   "applicableBenefits": {
    "type": "integer",
    "description": "Applicable benefits"
   },
   "resalePrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Resale Price"
   },
   "fees": {
    "type": "integer",
    "description": "Fees"
   },
   "applicableRestrictions": {
    "type": "integer",
    "description": "Applicable restrictions"
   },
   "originalFaceValueAed200": {
    "type": "string",
    "description": "Original Face Value: AED 200"
   },
   "officialResalePriceAed220": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Official Resale Price: AED 220"
   },
   "theCustomerCanChoose": {
    "type": "string",
    "description": "The customer can choose"
   },
   "primaryInventoryResaleInventory": {
    "type": "string",
    "description": "Primary Inventory + Resale Inventory"
   },
   "whileMaintainingTheirBackendDistinction": {
    "type": "string",
    "description": "while maintaining their backend distinction"
   }
  }
 },
 "WhiteLabelMarketplaceDeploymentExperienceArchitecturView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over orders state, assembled at read time from tables that already exist",
  "description": "**What White-Label Marketplace Deployment & Experience Architecture displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "embeddedPages": {
    "type": "string",
    "description": "Embedded pages"
   },
   "embeddedComponents": {
    "type": "string",
    "description": "Embedded components"
   },
   "clientNavigation": {
    "type": "string",
    "description": "Client navigation"
   },
   "clientAuthentication": {
    "type": "string",
    "description": "Client authentication"
   },
   "ssoSessionPassing": {
    "type": "string",
    "description": "SSO/session passing"
   },
   "clientBranding": {
    "type": "string",
    "description": "Client branding"
   },
   "domainConfiguration": {
    "type": "string",
    "description": "Domain configuration"
   },
   "analytics": {
    "type": "string",
    "description": "Analytics"
   },
   "localization": {
    "type": "string",
    "description": "Localization"
   },
   "deepLinking": {
    "type": "string",
    "description": "Deep linking"
   },
   "mobileResponsiveBehavior": {
    "type": "string",
    "description": "Mobile responsive behavior"
   },
   "english": {
    "type": "string",
    "description": "English"
   },
   "arabicRtl": {
    "type": "string",
    "description": "Arabic RTL"
   },
   "additionalClientLanguages": {
    "type": "string",
    "description": "Additional client languages"
   },
   "secureSessions": {
    "type": "string",
    "description": "Secure sessions"
   },
   "authentication": {
    "type": "string",
    "description": "Authentication"
   },
   "authorization": {
    "type": "string",
    "description": "Authorization"
   },
   "rateLimiting": {
    "type": "number",
    "description": "Rate limiting"
   },
   "botProtectionWhereApplicable": {
    "type": "string",
    "description": "Bot protection where applicable"
   },
   "fraudIntegration": {
    "type": "string",
    "description": "Fraud integration"
   },
   "dataProtection": {
    "type": "string",
    "description": "Data protection"
   },
   "sessionExpiry": {
    "type": "string",
    "format": "date-time",
    "description": "Session expiry"
   },
   "auditLogging": {
    "type": "string",
    "description": "Audit logging"
   },
   "marketplaceName": {
    "type": "string",
    "description": "Marketplace Name"
   },
   "clientLogo": {
    "type": "string",
    "description": "Client Logo"
   },
   "brandColors": {
    "type": "string",
    "description": "Brand Colors"
   },
   "typography": {
    "type": "string",
    "description": "Typography"
   },
   "domainSubdomain": {
    "type": "string",
    "description": "Domain/Subdomain"
   },
   "supportContact": {
    "type": "string",
    "description": "Support Contact"
   },
   "legalLinks": {
    "type": "string",
    "description": "Legal Links"
   },
   "sellerTerms": {
    "type": "string",
    "description": "Seller Terms"
   },
   "buyerTerms": {
    "type": "string",
    "description": "Buyer Terms"
   },
   "privacy": {
    "type": "string",
    "description": "Privacy"
   },
   "languages": {
    "type": "string",
    "description": "Languages"
   },
   "authenticationMethod": {
    "type": "string",
    "description": "Authentication method"
   },
   "myTickets": {
    "type": "string",
    "description": "My Tickets"
   },
   "sell": {
    "type": "string",
    "description": "Sell"
   },
   "buy": {
    "type": "string",
    "description": "Buy"
   },
   "myListings": {
    "type": "string",
    "description": "My Listings"
   },
   "transactions": {
    "type": "string",
    "description": "Transactions"
   }
  }
 }
}
```
