# P08-orders-money-02 — P08 · Orders & Money (2 of 3)

**10 screens · 51 operations · 54 schemas · 25 permissions**

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

- **Every control that can be refused must be gated.** 25 permissions apply here:
  `CASH_LIFT, LEDGER_VIEW, ORDER_CREATE, ORDER_DISCOUNT, ORDER_EXCHANGE, ORDER_MODIFY, ORDER_REFUND, ORDER_REPRINT, ORDER_RESCHEDULE, ORDER_VIEW, ORDER_VOID, OVERSHORT_ACCEPT`…. A control nobody can use must say so,
  not sit enabled and fail.
- **19 of these operations work offline**: applyManualDiscount, closeShift, createCashMovement, createOrder, getCurrentShift, getOrder, getRefundPolicy, getShift
  — and the rest do not. A surface that looks the same online and off is lying.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `BO-040` | Variance Approval | approvalInbox | 13 | 2 | — |
| `BO-041` | Cash Movements | approvalInbox | 13 | 2 | — |
| `BO-042` | Banking & Safe | approvalInbox | 13 | 2 | — |
| `BO-043` | Daily Reconciliation | listDetail | 7 | 0 | — |
| `BO-047` | Order Corrections & Exceptions | listDetail | 14 | 1 | — |
| `BO-048` | Retail Products | listDetail | 4 | 0 | — |
| `BO-051` | Purchase Orders | listDetail | 13 | 1 | — |
| `BO-059` | Sales Reports | listDetail | 9 | 1 | — |
| `BO-061` | Scheduled Reports | listDetail | 9 | 1 | — |
| `BO-062` | Venue Profile | listDetail | 4 | 0 | — |

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "BO-040",
  "name": "Variance Approval",
  "module": "Orders & Money",
  "requiresModule": "core",
  "wave": 1,
  "capability": "C00",
  "implementation": {
   "app": "venue-management-web",
   "route": "/venue-operations/variance-approval",
   "component": "apps/venue-management-web/src/routes/venue-operations/VarianceApprovalDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "exitTo": [
    "BO-001",
    "BO-007",
    "BO-008",
    "BO-009",
    "BO-089"
   ],
   "inferred": true,
   "fromFlows": true,
   "transitions": [
    {
     "to": "BO-089",
     "trigger": "Posts the remaining journals",
     "provenance": "flow F13 step 2→3"
    },
    {
     "to": "BO-001",
     "trigger": "Queue Directory",
     "carries": [
      "eventId",
      "feedId",
      "queueId"
     ],
     "provenance": "derived — BO-001 declares entryState.params eventId, feedId, queueId, so an edge into it must carry them"
    },
    {
     "to": "BO-007",
     "trigger": "Product Directory",
     "carries": [
      "productId"
     ],
     "provenance": "derived — BO-007 declares entryState.params productId, so an edge into it must carry them"
    },
    {
     "to": "BO-008",
     "trigger": "Product Detail & Variants",
     "carries": [
      "productId",
      "venueId"
     ],
     "provenance": "derived — BO-008 declares entryState.params productId, venueId, so an edge into it must carry them"
    },
    {
     "to": "BO-009",
     "trigger": "Pricing Rules",
     "carries": [
      "priceListId"
     ],
     "provenance": "derived — BO-009 declares entryState.params priceListId, so an edge into it must carry them"
    }
   ]
  },
  "notes": "Definition derived from the wireframe board on 14 August. CF-53 — 67 of these 73 had no definition at all. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual.",
  "density": "compact",
  "pattern": "approvalInbox",
  "patternReason": "`approveShiftOpen` decides items that `listShifts` queues — every row is waiting for a person, so the empty state is success",
  "purpose": "Accept or refuse a till that did not balance.",
  "gaps": [
   {
    "operation": "getShift",
    "why": "**2 declared operations reach no component on this screen**: getShift, listCashMovements. Either the screen is missing what calls them, or the declaration is residue.",
    "source": "the screen's own declarations"
   }
  ],
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "queue",
     "components": [
      {
       "kind": "dataTable",
       "label": "Waiting for a decision",
       "bindsTo": "Shift",
       "columns": [
        "Shift.id",
        "Shift.workstationId",
        "Shift.venueId",
        "Shift.scopePath",
        "Shift.principalId",
        "Shift.principalDisplayName",
        "Shift.incidents",
        "Shift.status",
        "Shift.currency",
        "Shift.currencyScale",
        "Shift.depositBoxCode",
        "Shift.bagNumber"
       ],
       "operation": "listShifts",
       "provenance": "contract shift.yaml GET /shifts"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "item",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected variance approval",
       "bindsTo": "Shift",
       "columns": [
        "Shift.id",
        "Shift.workstationId",
        "Shift.venueId",
        "Shift.scopePath",
        "Shift.principalId",
        "Shift.principalDisplayName",
        "Shift.incidents",
        "Shift.status",
        "Shift.currency",
        "Shift.currencyScale",
        "Shift.depositBoxCode",
        "Shift.bagNumber",
        "Shift.openingFloat",
        "Shift.salesTotal",
        "Shift.refundsTotal",
        "Shift.liftsTotal"
       ],
       "operation": "getCurrentShift",
       "provenance": "contract shift.yaml GET /shifts/current"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "decision",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Accept",
       "operation": "acceptShiftVariance",
       "provenance": "contract shift.yaml POST /shifts/{shiftId}/accept-variance"
      },
      {
       "kind": "secondaryButton",
       "label": "Approve",
       "operation": "approveShiftOpen",
       "provenance": "contract shift.yaml POST /shifts/{shiftId}/approve-open"
      },
      {
       "kind": "destructiveButton",
       "label": "Close",
       "operation": "closeShift",
       "provenance": "contract shift.yaml POST /shifts/{shiftId}/close"
      },
      {
       "kind": "secondaryButton",
       "label": "Create",
       "operation": "createCashMovement",
       "provenance": "contract shift.yaml POST /shifts/{shiftId}/cash-movements"
      },
      {
       "kind": "secondaryButton",
       "label": "Open",
       "operation": "openShift",
       "provenance": "contract shift.yaml POST /shifts"
      },
      {
       "kind": "secondaryButton",
       "label": "Record",
       "operation": "recordNoSale",
       "provenance": "contract shift.yaml POST /shifts/{shiftId}/no-sale"
      },
      {
       "kind": "secondaryButton",
       "label": "Reopen",
       "operation": "reopenShift",
       "provenance": "contract shift.yaml POST /shifts/{shiftId}/reopen"
      },
      {
       "kind": "secondaryButton",
       "label": "Resume",
       "operation": "resumeShift",
       "provenance": "contract shift.yaml POST /shifts/{shiftId}/resume"
      },
      {
       "kind": "destructiveButton",
       "label": "Suspend",
       "operation": "suspendShift",
       "provenance": "contract shift.yaml POST /shifts/{shiftId}/suspend"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "carried",
     "components": [
      {
       "kind": "detailPanel",
       "notes": "Structure from the wireframe board. Components not yet enumerated.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "dataTable",
       "derived": true,
       "impliedBy": "listShifts",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "acceptShiftVariance",
       "label": "Accept shift variance",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "acceptShiftVariance",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "overlays": [
   {
    "id": "confirmCloseShift",
    "component": "confirmDialog",
    "trigger": "Close",
    "body": "**Names what `closeShift` changes and what it leaves alone**, in the consequence rather than the verb. A variance approval this affects should be identified in the dialog, not just counted.",
    "provenance": "contract shift.yaml POST /shifts/{shiftId}/close"
   },
   {
    "id": "confirmSuspendShift",
    "component": "confirmDialog",
    "trigger": "Suspend",
    "body": "**Names what `suspendShift` changes and what it leaves alone**, in the consequence rather than the verb. A variance approval this affects should be identified in the dialog, not just counted.",
    "provenance": "contract shift.yaml POST /shifts/{shiftId}/suspend"
   }
  ],
  "states": {
   "loading": "The variance approval list.",
   "error": "Could not load. Names which read failed and leaves the variance approval untouched.",
   "emptyFirstRun": "**Nothing is waiting, which is the good outcome.** An empty queue means every item has been decided; it offers no create action, because creating work is not what it needs.",
   "emptyNoResults": "The filter narrowed it and the variance approval are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listShifts",
    "contract": "shift",
    "purpose": "List shifts",
    "trigger": "onLoad"
   },
   {
    "operationId": "acceptShiftVariance",
    "contract": "shift",
    "purpose": "Accept an over/short beyond the threshold",
    "trigger": "onAction",
    "invalidates": [
     "listShifts"
    ]
   },
   {
    "operationId": "approveShiftOpen",
    "contract": "shift",
    "purpose": "Approve a shift opening outside tolerance",
    "trigger": "onAction",
    "invalidates": [
     "listShifts"
    ]
   },
   {
    "operationId": "closeShift",
    "contract": "shift",
    "purpose": "Blind close-out",
    "trigger": "onAction",
    "invalidates": [
     "listShifts"
    ]
   },
   {
    "operationId": "createCashMovement",
    "contract": "shift",
    "purpose": "Record a cash lift or add",
    "trigger": "onAction",
    "invalidates": [
     "listShifts"
    ]
   },
   {
    "operationId": "getCurrentShift",
    "contract": "shift",
    "purpose": "The open or suspended shift on the session's workstation",
    "trigger": "onLoad"
   },
   {
    "operationId": "getShift",
    "contract": "shift",
    "purpose": "Read a shift",
    "trigger": "onLoad"
   },
   {
    "operationId": "listCashMovements",
    "contract": "shift",
    "purpose": "Lifts, adds and the opening float",
    "trigger": "onLoad"
   },
   {
    "operationId": "openShift",
    "contract": "shift",
    "purpose": "Open a shift",
    "trigger": "onAction",
    "invalidates": [
     "listShifts"
    ]
   },
   {
    "operationId": "recordNoSale",
    "contract": "shift",
    "purpose": "Open the drawer without a sale",
    "trigger": "onAction",
    "invalidates": [
     "listShifts"
    ]
   },
   {
    "operationId": "reopenShift",
    "contract": "shift",
    "purpose": "Reopen a shift closed in error",
    "trigger": "onAction",
    "invalidates": [
     "listShifts"
    ]
   },
   {
    "operationId": "resumeShift",
    "contract": "shift",
    "purpose": "Resume a suspended shift",
    "trigger": "onAction",
    "invalidates": [
     "listShifts"
    ]
   },
   {
    "operationId": "suspendShift",
    "contract": "shift",
    "purpose": "Suspend a shift so another user can log in",
    "trigger": "onAction",
    "invalidates": [
     "listShifts"
    ]
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "shiftId",
     "from": "session"
    }
   ],
   "coldEntry": "Resolves from the session; a cold arrival is the ordinary case.",
   "preloaded": [
    "Shift.id",
    "Shift.workstationId",
    "Shift.venueId",
    "Shift.scopePath",
    "Shift.principalId"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-040"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 13 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
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
  "id": "BO-041",
  "name": "Cash Movements",
  "module": "Orders & Money",
  "requiresModule": "core",
  "wave": 2,
  "capability": "C00",
  "implementation": {
   "app": "venue-management-web",
   "route": "/venue-operations/cash-movements",
   "component": "apps/venue-management-web/src/routes/venue-operations/CashMovementsDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "exitTo": [
    "BO-001",
    "BO-007",
    "BO-008",
    "BO-009"
   ],
   "inferred": true,
   "transitions": [
    {
     "to": "BO-001",
     "trigger": "Queue Directory",
     "carries": [
      "eventId",
      "feedId",
      "queueId"
     ],
     "provenance": "derived — BO-001 declares entryState.params eventId, feedId, queueId, so an edge into it must carry them"
    },
    {
     "to": "BO-007",
     "trigger": "Product Directory",
     "carries": [
      "productId"
     ],
     "provenance": "derived — BO-007 declares entryState.params productId, so an edge into it must carry them"
    },
    {
     "to": "BO-008",
     "trigger": "Product Detail & Variants",
     "carries": [
      "productId",
      "venueId"
     ],
     "provenance": "derived — BO-008 declares entryState.params productId, venueId, so an edge into it must carry them"
    },
    {
     "to": "BO-009",
     "trigger": "Pricing Rules",
     "carries": [
      "priceListId"
     ],
     "provenance": "derived — BO-009 declares entryState.params priceListId, so an edge into it must carry them"
    }
   ]
  },
  "notes": "Definition derived from the wireframe board on 14 August. CF-53 — 67 of these 73 had no definition at all. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual.",
  "density": "compact",
  "pattern": "approvalInbox",
  "patternReason": "`approveShiftOpen` decides items that `listCashMovements` queues — every row is waiting for a person, so the empty state is success",
  "purpose": "Track money in and out of a drawer that is not a sale.",
  "gaps": [
   {
    "operation": "getShift",
    "why": "**2 declared operations reach no component on this screen**: getShift, listShifts. Either the screen is missing what calls them, or the declaration is residue.",
    "source": "the screen's own declarations"
   }
  ],
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "queue",
     "components": [
      {
       "kind": "dataTable",
       "label": "Waiting for a decision",
       "bindsTo": "CashMovement",
       "columns": [
        "CashMovement.id",
        "CashMovement.kind",
        "CashMovement.amount",
        "CashMovement.denominations",
        "CashMovement.reference",
        "CashMovement.reason",
        "CashMovement.recordedAt",
        "CashMovement.shiftId",
        "CashMovement.authorisedByPrincipalId",
        "CashMovement.sequence",
        "CashMovement.syncedAt"
       ],
       "operation": "listCashMovements",
       "provenance": "contract shift.yaml GET /shifts/{shiftId}/cash-movements"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "item",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected cash movements",
       "bindsTo": "Shift",
       "columns": [
        "Shift.id",
        "Shift.workstationId",
        "Shift.venueId",
        "Shift.scopePath",
        "Shift.principalId",
        "Shift.principalDisplayName",
        "Shift.incidents",
        "Shift.status",
        "Shift.currency",
        "Shift.currencyScale",
        "Shift.depositBoxCode",
        "Shift.bagNumber",
        "Shift.openingFloat",
        "Shift.salesTotal",
        "Shift.refundsTotal",
        "Shift.liftsTotal"
       ],
       "operation": "getCurrentShift",
       "provenance": "contract shift.yaml GET /shifts/current"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "decision",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Create",
       "operation": "createCashMovement",
       "provenance": "contract shift.yaml POST /shifts/{shiftId}/cash-movements"
      },
      {
       "kind": "secondaryButton",
       "label": "Accept",
       "operation": "acceptShiftVariance",
       "provenance": "contract shift.yaml POST /shifts/{shiftId}/accept-variance"
      },
      {
       "kind": "secondaryButton",
       "label": "Approve",
       "operation": "approveShiftOpen",
       "provenance": "contract shift.yaml POST /shifts/{shiftId}/approve-open"
      },
      {
       "kind": "destructiveButton",
       "label": "Close",
       "operation": "closeShift",
       "provenance": "contract shift.yaml POST /shifts/{shiftId}/close"
      },
      {
       "kind": "secondaryButton",
       "label": "Open",
       "operation": "openShift",
       "provenance": "contract shift.yaml POST /shifts"
      },
      {
       "kind": "secondaryButton",
       "label": "Record",
       "operation": "recordNoSale",
       "provenance": "contract shift.yaml POST /shifts/{shiftId}/no-sale"
      },
      {
       "kind": "secondaryButton",
       "label": "Reopen",
       "operation": "reopenShift",
       "provenance": "contract shift.yaml POST /shifts/{shiftId}/reopen"
      },
      {
       "kind": "secondaryButton",
       "label": "Resume",
       "operation": "resumeShift",
       "provenance": "contract shift.yaml POST /shifts/{shiftId}/resume"
      },
      {
       "kind": "destructiveButton",
       "label": "Suspend",
       "operation": "suspendShift",
       "provenance": "contract shift.yaml POST /shifts/{shiftId}/suspend"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "carried",
     "components": [
      {
       "kind": "detailPanel",
       "notes": "Structure from the wireframe board. Components not yet enumerated.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "dataTable",
       "derived": true,
       "impliedBy": "listCashMovements",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "createCashMovement",
       "label": "Create cash movement",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "createCashMovement",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "overlays": [
   {
    "id": "confirmCloseShift",
    "component": "confirmDialog",
    "trigger": "Close",
    "body": "**Names what `closeShift` changes and what it leaves alone**, in the consequence rather than the verb. A cash movements this affects should be identified in the dialog, not just counted.",
    "provenance": "contract shift.yaml POST /shifts/{shiftId}/close"
   },
   {
    "id": "confirmSuspendShift",
    "component": "confirmDialog",
    "trigger": "Suspend",
    "body": "**Names what `suspendShift` changes and what it leaves alone**, in the consequence rather than the verb. A cash movements this affects should be identified in the dialog, not just counted.",
    "provenance": "contract shift.yaml POST /shifts/{shiftId}/suspend"
   }
  ],
  "states": {
   "loading": "The cash movements list.",
   "error": "Could not load. Names which read failed and leaves the cash movements untouched.",
   "emptyFirstRun": "**Nothing is waiting, which is the good outcome.** An empty queue means every item has been decided; it offers no create action, because creating work is not what it needs.",
   "emptyNoResults": "The filter narrowed it and the cash movements are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listCashMovements",
    "contract": "shift",
    "purpose": "Lifts, adds and the opening float",
    "trigger": "onLoad"
   },
   {
    "operationId": "createCashMovement",
    "contract": "shift",
    "purpose": "Record a cash lift or add",
    "trigger": "onAction",
    "invalidates": [
     "listCashMovements"
    ]
   },
   {
    "operationId": "acceptShiftVariance",
    "contract": "shift",
    "purpose": "Accept an over/short beyond the threshold",
    "trigger": "onAction",
    "invalidates": [
     "listCashMovements"
    ]
   },
   {
    "operationId": "approveShiftOpen",
    "contract": "shift",
    "purpose": "Approve a shift opening outside tolerance",
    "trigger": "onAction",
    "invalidates": [
     "listCashMovements"
    ]
   },
   {
    "operationId": "closeShift",
    "contract": "shift",
    "purpose": "Blind close-out",
    "trigger": "onAction",
    "invalidates": [
     "listCashMovements"
    ]
   },
   {
    "operationId": "getCurrentShift",
    "contract": "shift",
    "purpose": "The open or suspended shift on the session's workstation",
    "trigger": "onLoad"
   },
   {
    "operationId": "getShift",
    "contract": "shift",
    "purpose": "Read a shift",
    "trigger": "onLoad"
   },
   {
    "operationId": "listShifts",
    "contract": "shift",
    "purpose": "List shifts",
    "trigger": "onLoad"
   },
   {
    "operationId": "openShift",
    "contract": "shift",
    "purpose": "Open a shift",
    "trigger": "onAction",
    "invalidates": [
     "listCashMovements"
    ]
   },
   {
    "operationId": "recordNoSale",
    "contract": "shift",
    "purpose": "Open the drawer without a sale",
    "trigger": "onAction",
    "invalidates": [
     "listCashMovements"
    ]
   },
   {
    "operationId": "reopenShift",
    "contract": "shift",
    "purpose": "Reopen a shift closed in error",
    "trigger": "onAction",
    "invalidates": [
     "listCashMovements"
    ]
   },
   {
    "operationId": "resumeShift",
    "contract": "shift",
    "purpose": "Resume a suspended shift",
    "trigger": "onAction",
    "invalidates": [
     "listCashMovements"
    ]
   },
   {
    "operationId": "suspendShift",
    "contract": "shift",
    "purpose": "Suspend a shift so another user can log in",
    "trigger": "onAction",
    "invalidates": [
     "listCashMovements"
    ]
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "shiftId",
     "from": "session"
    }
   ],
   "coldEntry": "Resolves from the session; a cold arrival is the ordinary case.",
   "preloaded": [
    "Shift.id",
    "Shift.workstationId",
    "Shift.venueId",
    "Shift.scopePath",
    "Shift.principalId"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-041"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 13 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
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
  "id": "BO-042",
  "name": "Banking & Safe",
  "module": "Orders & Money",
  "requiresModule": "core",
  "wave": 2,
  "capability": "C00",
  "implementation": {
   "app": "venue-management-web",
   "route": "/venue-operations/banking-safe",
   "component": "apps/venue-management-web/src/routes/venue-operations/BankingSafeDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "exitTo": [
    "BO-001",
    "BO-007",
    "BO-008",
    "BO-009"
   ],
   "inferred": true,
   "transitions": [
    {
     "to": "BO-001",
     "trigger": "Queue Directory",
     "carries": [
      "eventId",
      "feedId",
      "queueId"
     ],
     "provenance": "derived — BO-001 declares entryState.params eventId, feedId, queueId, so an edge into it must carry them"
    },
    {
     "to": "BO-007",
     "trigger": "Product Directory",
     "carries": [
      "productId"
     ],
     "provenance": "derived — BO-007 declares entryState.params productId, so an edge into it must carry them"
    },
    {
     "to": "BO-008",
     "trigger": "Product Detail & Variants",
     "carries": [
      "productId",
      "venueId"
     ],
     "provenance": "derived — BO-008 declares entryState.params productId, venueId, so an edge into it must carry them"
    },
    {
     "to": "BO-009",
     "trigger": "Pricing Rules",
     "carries": [
      "priceListId"
     ],
     "provenance": "derived — BO-009 declares entryState.params priceListId, so an edge into it must carry them"
    }
   ]
  },
  "notes": "Definition derived from the wireframe board on 14 August. CF-53 — 67 of these 73 had no definition at all. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual.",
  "density": "compact",
  "pattern": "approvalInbox",
  "patternReason": "`approveShiftOpen` decides items that `listCashMovements` queues — every row is waiting for a person, so the empty state is success",
  "purpose": "Move the day’s cash out of the tills.",
  "gaps": [
   {
    "operation": "getShift",
    "why": "**2 declared operations reach no component on this screen**: getShift, listShifts. Either the screen is missing what calls them, or the declaration is residue.",
    "source": "the screen's own declarations"
   }
  ],
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "queue",
     "components": [
      {
       "kind": "dataTable",
       "label": "Waiting for a decision",
       "bindsTo": "CashMovement",
       "columns": [
        "CashMovement.id",
        "CashMovement.kind",
        "CashMovement.amount",
        "CashMovement.denominations",
        "CashMovement.reference",
        "CashMovement.reason",
        "CashMovement.recordedAt",
        "CashMovement.shiftId",
        "CashMovement.authorisedByPrincipalId",
        "CashMovement.sequence",
        "CashMovement.syncedAt"
       ],
       "operation": "listCashMovements",
       "provenance": "contract shift.yaml GET /shifts/{shiftId}/cash-movements"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "item",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected banking safe",
       "bindsTo": "Shift",
       "columns": [
        "Shift.id",
        "Shift.workstationId",
        "Shift.venueId",
        "Shift.scopePath",
        "Shift.principalId",
        "Shift.principalDisplayName",
        "Shift.incidents",
        "Shift.status",
        "Shift.currency",
        "Shift.currencyScale",
        "Shift.depositBoxCode",
        "Shift.bagNumber",
        "Shift.openingFloat",
        "Shift.salesTotal",
        "Shift.refundsTotal",
        "Shift.liftsTotal"
       ],
       "operation": "getCurrentShift",
       "provenance": "contract shift.yaml GET /shifts/current"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "decision",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Accept",
       "operation": "acceptShiftVariance",
       "provenance": "contract shift.yaml POST /shifts/{shiftId}/accept-variance"
      },
      {
       "kind": "secondaryButton",
       "label": "Approve",
       "operation": "approveShiftOpen",
       "provenance": "contract shift.yaml POST /shifts/{shiftId}/approve-open"
      },
      {
       "kind": "destructiveButton",
       "label": "Close",
       "operation": "closeShift",
       "provenance": "contract shift.yaml POST /shifts/{shiftId}/close"
      },
      {
       "kind": "secondaryButton",
       "label": "Create",
       "operation": "createCashMovement",
       "provenance": "contract shift.yaml POST /shifts/{shiftId}/cash-movements"
      },
      {
       "kind": "secondaryButton",
       "label": "Open",
       "operation": "openShift",
       "provenance": "contract shift.yaml POST /shifts"
      },
      {
       "kind": "secondaryButton",
       "label": "Record",
       "operation": "recordNoSale",
       "provenance": "contract shift.yaml POST /shifts/{shiftId}/no-sale"
      },
      {
       "kind": "secondaryButton",
       "label": "Reopen",
       "operation": "reopenShift",
       "provenance": "contract shift.yaml POST /shifts/{shiftId}/reopen"
      },
      {
       "kind": "secondaryButton",
       "label": "Resume",
       "operation": "resumeShift",
       "provenance": "contract shift.yaml POST /shifts/{shiftId}/resume"
      },
      {
       "kind": "destructiveButton",
       "label": "Suspend",
       "operation": "suspendShift",
       "provenance": "contract shift.yaml POST /shifts/{shiftId}/suspend"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "carried",
     "components": [
      {
       "kind": "detailPanel",
       "notes": "Structure from the wireframe board. Components not yet enumerated.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "dataTable",
       "derived": true,
       "impliedBy": "listCashMovements",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "acceptShiftVariance",
       "label": "Accept shift variance",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "acceptShiftVariance",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "overlays": [
   {
    "id": "confirmCloseShift",
    "component": "confirmDialog",
    "trigger": "Close",
    "body": "**Names what `closeShift` changes and what it leaves alone**, in the consequence rather than the verb. A banking safe this affects should be identified in the dialog, not just counted.",
    "provenance": "contract shift.yaml POST /shifts/{shiftId}/close"
   },
   {
    "id": "confirmSuspendShift",
    "component": "confirmDialog",
    "trigger": "Suspend",
    "body": "**Names what `suspendShift` changes and what it leaves alone**, in the consequence rather than the verb. A banking safe this affects should be identified in the dialog, not just counted.",
    "provenance": "contract shift.yaml POST /shifts/{shiftId}/suspend"
   }
  ],
  "states": {
   "loading": "The banking safe list.",
   "error": "Could not load. Names which read failed and leaves the banking safe untouched.",
   "emptyFirstRun": "**Nothing is waiting, which is the good outcome.** An empty queue means every item has been decided; it offers no create action, because creating work is not what it needs.",
   "emptyNoResults": "The filter narrowed it and the banking safe are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listCashMovements",
    "contract": "shift",
    "purpose": "Lifts, adds and the opening float",
    "trigger": "onLoad"
   },
   {
    "operationId": "acceptShiftVariance",
    "contract": "shift",
    "purpose": "Accept an over/short beyond the threshold",
    "trigger": "onAction",
    "invalidates": [
     "listCashMovements"
    ]
   },
   {
    "operationId": "approveShiftOpen",
    "contract": "shift",
    "purpose": "Approve a shift opening outside tolerance",
    "trigger": "onAction",
    "invalidates": [
     "listCashMovements"
    ]
   },
   {
    "operationId": "closeShift",
    "contract": "shift",
    "purpose": "Blind close-out",
    "trigger": "onAction",
    "invalidates": [
     "listCashMovements"
    ]
   },
   {
    "operationId": "createCashMovement",
    "contract": "shift",
    "purpose": "Record a cash lift or add",
    "trigger": "onAction",
    "invalidates": [
     "listCashMovements"
    ]
   },
   {
    "operationId": "getCurrentShift",
    "contract": "shift",
    "purpose": "The open or suspended shift on the session's workstation",
    "trigger": "onLoad"
   },
   {
    "operationId": "getShift",
    "contract": "shift",
    "purpose": "Read a shift",
    "trigger": "onLoad"
   },
   {
    "operationId": "listShifts",
    "contract": "shift",
    "purpose": "List shifts",
    "trigger": "onLoad"
   },
   {
    "operationId": "openShift",
    "contract": "shift",
    "purpose": "Open a shift",
    "trigger": "onAction",
    "invalidates": [
     "listCashMovements"
    ]
   },
   {
    "operationId": "recordNoSale",
    "contract": "shift",
    "purpose": "Open the drawer without a sale",
    "trigger": "onAction",
    "invalidates": [
     "listCashMovements"
    ]
   },
   {
    "operationId": "reopenShift",
    "contract": "shift",
    "purpose": "Reopen a shift closed in error",
    "trigger": "onAction",
    "invalidates": [
     "listCashMovements"
    ]
   },
   {
    "operationId": "resumeShift",
    "contract": "shift",
    "purpose": "Resume a suspended shift",
    "trigger": "onAction",
    "invalidates": [
     "listCashMovements"
    ]
   },
   {
    "operationId": "suspendShift",
    "contract": "shift",
    "purpose": "Suspend a shift so another user can log in",
    "trigger": "onAction",
    "invalidates": [
     "listCashMovements"
    ]
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "shiftId",
     "from": "session"
    }
   ],
   "coldEntry": "Resolves from the session; a cold arrival is the ordinary case.",
   "preloaded": [
    "Shift.id",
    "Shift.workstationId",
    "Shift.venueId",
    "Shift.scopePath",
    "Shift.principalId"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-042"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 13 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
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
  "id": "BO-043",
  "name": "Daily Reconciliation",
  "module": "Orders & Money",
  "requiresModule": "core",
  "wave": 1,
  "capability": "C00",
  "implementation": {
   "app": "venue-management-web",
   "route": "/venue-operations/daily-reconciliation",
   "component": "apps/venue-management-web/src/routes/venue-operations/DailyReconciliationDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "exitTo": [
    "BO-001",
    "BO-007",
    "BO-008",
    "BO-009",
    "BO-074"
   ],
   "inferred": true,
   "transitions": [
    {
     "to": "BO-074",
     "trigger": "Chart of Accounts",
     "provenance": "flow F98 step 1→2"
    },
    {
     "to": "BO-001",
     "trigger": "Queue Directory",
     "carries": [
      "eventId",
      "feedId",
      "queueId"
     ],
     "provenance": "derived — BO-001 declares entryState.params eventId, feedId, queueId, so an edge into it must carry them"
    },
    {
     "to": "BO-007",
     "trigger": "Product Directory",
     "carries": [
      "productId"
     ],
     "provenance": "derived — BO-007 declares entryState.params productId, so an edge into it must carry them"
    },
    {
     "to": "BO-008",
     "trigger": "Product Detail & Variants",
     "carries": [
      "productId",
      "venueId"
     ],
     "provenance": "derived — BO-008 declares entryState.params productId, venueId, so an edge into it must carry them"
    },
    {
     "to": "BO-009",
     "trigger": "Pricing Rules",
     "carries": [
      "priceListId"
     ],
     "provenance": "derived — BO-009 declares entryState.params priceListId, so an edge into it must carry them"
    }
   ]
  },
  "notes": "Definition derived from the wireframe board on 14 August. CF-53 — 67 of these 73 had no definition at all. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual.",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listSettlements` reads the population and `getTrialBalance` reads one of them — list, select, act",
  "purpose": "Prove the day balances before anyone goes home.",
  "gaps": [
   {
    "operation": "getSettlement",
    "why": "**3 declared operations reach no component on this screen**: getSettlement, listLedgerEntries, listSettlementExceptions. Either the screen is missing what calls them, or the declaration is residue.",
    "source": "the screen's own declarations"
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
       "label": "Every daily reconciliation",
       "bindsTo": "Settlement",
       "columns": [
        "Settlement.id",
        "Settlement.providerName",
        "Settlement.periodStart",
        "Settlement.periodEnd",
        "Settlement.status",
        "Settlement.lineCount",
        "Settlement.matchedCount",
        "Settlement.exceptionCount",
        "Settlement.providerGross",
        "Settlement.providerFees",
        "Settlement.providerNet",
        "Settlement.ledgerGross"
       ],
       "operation": "listSettlements",
       "provenance": "contract finance.yaml GET /settlements"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected daily reconciliation",
       "bindsTo": "TrialBalance",
       "columns": [
        "TrialBalance.fiscalPeriodId",
        "TrialBalance.isBalanced",
        "TrialBalance.totalDebit",
        "TrialBalance.totalCredit",
        "TrialBalance.accounts"
       ],
       "operation": "getTrialBalance",
       "provenance": "contract finance.yaml GET /ledger/trial-balance"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Ingest",
       "operation": "ingestSettlementFile",
       "provenance": "contract finance.yaml POST /settlements"
      },
      {
       "kind": "secondaryButton",
       "label": "Resolve",
       "operation": "resolveSettlementException",
       "provenance": "contract finance.yaml POST /settlements/{settlementId}/exceptions"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "carried",
     "components": [
      {
       "kind": "detailPanel",
       "notes": "Structure from the wireframe board. Components not yet enumerated.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "dataTable",
       "derived": true,
       "impliedBy": "listSettlements",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "ingestSettlementFile",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The daily reconciliation list.",
   "error": "Could not load. Names which read failed and leaves the daily reconciliation untouched.",
   "emptyFirstRun": "No daily reconciliation yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the daily reconciliation are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getTrialBalance",
    "contract": "finance",
    "purpose": "Trial balance for a period",
    "trigger": "onLoad"
   },
   {
    "operationId": "listSettlements",
    "contract": "finance",
    "purpose": "List settlement batches",
    "trigger": "onLoad"
   },
   {
    "operationId": "getSettlement",
    "contract": "finance",
    "purpose": "Settlement detail with match results",
    "trigger": "onLoad"
   },
   {
    "operationId": "ingestSettlementFile",
    "contract": "finance",
    "purpose": "Ingest a provider settlement file",
    "trigger": "onAction",
    "invalidates": [
     "listSettlements"
    ]
   },
   {
    "operationId": "listLedgerEntries",
    "contract": "finance",
    "purpose": "Query the ledger",
    "trigger": "onLoad"
   },
   {
    "operationId": "listSettlementExceptions",
    "contract": "finance",
    "purpose": "Unmatched or mismatched settlement lines",
    "trigger": "onLoad"
   },
   {
    "operationId": "resolveSettlementException",
    "contract": "finance",
    "purpose": "Resolve a settlement exception",
    "trigger": "onAction",
    "invalidates": [
     "listSettlements"
    ]
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "settlementId",
     "from": "deepLink"
    }
   ],
   "coldEntry": "**A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know whether the record moved, closed or never existed, because those are three different next actions. **The scope is resolved from the session, never from the link**: a link cannot move somebody to a venue they do not hold. Arrives with `settlementId`.",
   "preloaded": [
    "TrialBalance.fiscalPeriodId",
    "TrialBalance.isBalanced",
    "TrialBalance.totalDebit",
    "TrialBalance.totalCredit",
    "TrialBalance.accounts"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-043"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 7 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
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
  "id": "BO-047",
  "name": "Order Corrections & Exceptions",
  "module": "Orders & Money",
  "requiresModule": "ticketing",
  "wave": 2,
  "capability": "C00",
  "implementation": {
   "app": "venue-management-web",
   "route": "/venue-operations/f-b-order-management",
   "component": "apps/venue-management-web/src/routes/venue-operations/FBOrderManagementDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "exitTo": [
    "BO-001",
    "BO-007",
    "BO-008",
    "BO-009"
   ],
   "inferred": true,
   "transitions": [
    {
     "to": "BO-001",
     "trigger": "Queue Directory",
     "carries": [
      "eventId",
      "feedId",
      "queueId"
     ],
     "provenance": "derived — BO-001 declares entryState.params eventId, feedId, queueId, so an edge into it must carry them"
    },
    {
     "to": "BO-007",
     "trigger": "Product Directory",
     "carries": [
      "productId"
     ],
     "provenance": "derived — BO-007 declares entryState.params productId, so an edge into it must carry them"
    },
    {
     "to": "BO-008",
     "trigger": "Product Detail & Variants",
     "carries": [
      "productId",
      "venueId"
     ],
     "provenance": "derived — BO-008 declares entryState.params productId, venueId, so an edge into it must carry them"
    },
    {
     "to": "BO-009",
     "trigger": "Pricing Rules",
     "carries": [
      "priceListId"
     ],
     "provenance": "derived — BO-009 declares entryState.params priceListId, so an edge into it must carry them"
    }
   ]
  },
  "notes": "Definition derived from the wireframe board on 14 August. CF-53 — 67 of these 73 had no definition at all. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual.",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listOrders` reads the population and `getOrder` reads one of them — list, select, act",
  "purpose": "Fix an order that has gone wrong.",
  "gaps": [
   {
    "operation": "getOrderStatement",
    "why": "**2 declared operations reach no component on this screen**: getOrderStatement, listOrderRefunds. Either the screen is missing what calls them, or the declaration is residue.",
    "source": "the screen's own declarations"
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
       "label": "Every order",
       "bindsTo": "OrderSummary",
       "columns": [
        "OrderSummary.id",
        "OrderSummary.orderNumber",
        "OrderSummary.status",
        "OrderSummary.grossAmount",
        "OrderSummary.refundedAmount",
        "OrderSummary.channel",
        "OrderSummary.lineCount"
       ],
       "operation": "listOrders",
       "provenance": "contract orders.yaml GET /orders"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected order",
       "bindsTo": "Order",
       "columns": [
        "Order.id",
        "Order.orderNumber",
        "Order.channel",
        "Order.venueId",
        "Order.scopePath",
        "Order.status",
        "Order.currency",
        "Order.currencyScale",
        "Order.grossAmount",
        "Order.taxAmount",
        "Order.netAmount",
        "Order.refundedAmount",
        "Order.totalPriceVariance",
        "Order.lines",
        "Order.payments",
        "Order.principalId"
       ],
       "operation": "getOrder",
       "provenance": "contract orders.yaml GET /orders/{orderId}"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Create",
       "operation": "createOrder",
       "provenance": "contract orders.yaml POST /orders"
      },
      {
       "kind": "secondaryButton",
       "label": "Apply",
       "operation": "applyManualDiscount",
       "provenance": "contract orders.yaml POST /orders/{orderId}/discounts"
      },
      {
       "kind": "secondaryButton",
       "label": "Create",
       "operation": "createRefund",
       "provenance": "contract orders.yaml POST /orders/{orderId}/refunds"
      },
      {
       "kind": "secondaryButton",
       "label": "Exchange",
       "operation": "exchangeOrderLines",
       "provenance": "contract orders.yaml POST /orders/{orderId}/exchanges"
      },
      {
       "kind": "secondaryButton",
       "label": "Hold",
       "operation": "holdOrder",
       "provenance": "contract orders.yaml POST /orders/{orderId}/hold"
      },
      {
       "kind": "secondaryButton",
       "label": "Modify",
       "operation": "modifyOrder",
       "provenance": "contract orders.yaml POST /orders/{orderId}/modify"
      },
      {
       "kind": "secondaryButton",
       "label": "Reprint",
       "operation": "reprintOrder",
       "provenance": "contract orders.yaml POST /orders/{orderId}/reprints"
      },
      {
       "kind": "secondaryButton",
       "label": "Reschedule",
       "operation": "rescheduleOrder",
       "provenance": "contract orders.yaml POST /orders/{orderId}/reschedule"
      },
      {
       "kind": "secondaryButton",
       "label": "Resume",
       "operation": "resumeOrder",
       "provenance": "contract orders.yaml POST /orders/{orderId}/resume"
      },
      {
       "kind": "destructiveButton",
       "label": "Void",
       "operation": "voidOrder",
       "provenance": "contract orders.yaml POST /orders/{orderId}/voids"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "carried",
     "components": [
      {
       "kind": "detailPanel",
       "notes": "Structure from the wireframe board. Components not yet enumerated.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "dataTable",
       "derived": true,
       "impliedBy": "listOrders",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "createOrder",
       "label": "Create order",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "destructiveButton",
       "derived": true,
       "impliedBy": "voidOrder",
       "label": "Void order",
       "notes": "**Always confirms, never the default focus.** The consequence goes in the body — *cancel 3 orders worth AED 480* is a confirmation, *are you sure* is not.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "createOrder",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "confirmDialog",
       "derived": true,
       "label": "Confirm",
       "notes": "**The consequence goes in the body, not the title.** *Cancel 3 orders worth AED 480* is a confirmation; *are you sure* is not — and a dialog that cannot name what it destroys is a dialog somebody dismisses.\n\n**Added 31 August.** `confirmDialog` and `modal` were both in the component library and used **zero times across 492 screens**, while `destructiveButton` was used 39 times and its own entry reads *always requires confirmation*.",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "overlays": [
   {
    "id": "confirmVoidOrder",
    "component": "confirmDialog",
    "trigger": "Void",
    "body": "**Names what `voidOrder` changes and what it leaves alone**, in the consequence rather than the verb. A order this affects should be identified in the dialog, not just counted.",
    "provenance": "contract orders.yaml POST /orders/{orderId}/voids"
   }
  ],
  "states": {
   "loading": "The order list.",
   "error": "Could not load. Names which read failed and leaves the order untouched.",
   "emptyFirstRun": "No order yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the order are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listOrders",
    "contract": "orders",
    "purpose": "List orders",
    "trigger": "onLoad"
   },
   {
    "operationId": "getOrder",
    "contract": "orders",
    "purpose": "Read an order",
    "trigger": "onLoad"
   },
   {
    "operationId": "createOrder",
    "contract": "orders",
    "purpose": "Create an order",
    "trigger": "onAction",
    "invalidates": [
     "listOrders"
    ]
   },
   {
    "operationId": "applyManualDiscount",
    "contract": "orders",
    "purpose": "Apply a discount a cashier chose",
    "trigger": "onAction",
    "invalidates": [
     "listOrders"
    ]
   },
   {
    "operationId": "createRefund",
    "contract": "orders",
    "purpose": "Refund an order, wholly or in part",
    "trigger": "onAction",
    "invalidates": [
     "listOrders"
    ]
   },
   {
    "operationId": "exchangeOrderLines",
    "contract": "orders",
    "purpose": "Exchange lines for different products or dates",
    "trigger": "onAction",
    "invalidates": [
     "listOrders"
    ]
   },
   {
    "operationId": "getOrderStatement",
    "contract": "orders",
    "purpose": "Full financial history of an order",
    "trigger": "onLoad"
   },
   {
    "operationId": "holdOrder",
    "contract": "orders",
    "purpose": "Park a sale and free the till",
    "trigger": "onAction",
    "invalidates": [
     "listOrders"
    ]
   },
   {
    "operationId": "listOrderRefunds",
    "contract": "orders",
    "purpose": "List refunds against an order",
    "trigger": "onLoad"
   },
   {
    "operationId": "modifyOrder",
    "contract": "orders",
    "purpose": "Add or remove lines on an existing order",
    "trigger": "onAction",
    "invalidates": [
     "listOrders"
    ]
   },
   {
    "operationId": "reprintOrder",
    "contract": "orders",
    "purpose": "Reprint or resend tickets",
    "trigger": "onAction",
    "invalidates": [
     "listOrders"
    ]
   },
   {
    "operationId": "rescheduleOrder",
    "contract": "orders",
    "purpose": "Move an order to another performance",
    "trigger": "onAction",
    "invalidates": [
     "listOrders"
    ]
   },
   {
    "operationId": "resumeOrder",
    "contract": "orders",
    "purpose": "Bring a parked sale back to a till",
    "trigger": "onAction",
    "invalidates": [
     "listOrders"
    ]
   },
   {
    "operationId": "voidOrder",
    "contract": "orders",
    "purpose": "Void an order",
    "trigger": "onAction",
    "invalidates": [
     "listOrders"
    ]
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "orderId",
     "from": "deepLink"
    }
   ],
   "coldEntry": "**A guest opening an order link weeks later.** Shows the order if it still resolves; if it was refunded or the performance passed, says which and offers the order list rather than an error.",
   "preloaded": [
    "Order.id",
    "Order.orderNumber",
    "Order.channel",
    "Order.venueId",
    "Order.scopePath"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-047"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 14 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "nameNote": "**Renamed 9 September 2026.** It was called *F&B Order Management*, which is BO-020's job and shares not one of this screen's fourteen operations. Its own purpose — fix an order that has gone wrong — is what it is called now.",
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
  "id": "BO-048",
  "name": "Retail Products",
  "module": "Orders & Money",
  "requiresModule": "retail",
  "wave": 2,
  "capability": "C00",
  "implementation": {
   "app": "venue-management-web",
   "route": "/venue-operations/retail-products",
   "component": "apps/venue-management-web/src/routes/venue-operations/RetailProductsDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "exitTo": [
    "BO-001",
    "BO-007",
    "BO-008",
    "BO-009"
   ],
   "inferred": true,
   "fromFlows": true,
   "transitions": [
    {
     "to": "BO-001",
     "trigger": "Queue Directory",
     "carries": [
      "eventId",
      "feedId",
      "queueId"
     ],
     "provenance": "derived — BO-001 declares entryState.params eventId, feedId, queueId, so an edge into it must carry them"
    },
    {
     "to": "BO-007",
     "trigger": "Product Directory",
     "carries": [
      "productId"
     ],
     "provenance": "derived — BO-007 declares entryState.params productId, so an edge into it must carry them"
    },
    {
     "to": "BO-008",
     "trigger": "Product Detail & Variants",
     "carries": [
      "productId",
      "venueId"
     ],
     "provenance": "derived — BO-008 declares entryState.params productId, venueId, so an edge into it must carry them"
    },
    {
     "to": "BO-009",
     "trigger": "Pricing Rules",
     "carries": [
      "priceListId"
     ],
     "provenance": "derived — BO-009 declares entryState.params priceListId, so an edge into it must carry them"
    },
    {
     "to": "GST-026",
     "trigger": "Guest tracks it in the app",
     "provenance": "flow F17 step 3→4",
     "operation": "listMerchandise",
     "crossesDevice": true,
     "back": false
    }
   ]
  },
  "notes": "Definition derived from the wireframe board on 14 August. CF-53 — 67 of these 73 had no definition at all. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual. **Cross-platform navigation removed 24 August**: GST-026. **A till does not navigate to a back office and a guest app does not navigate to either** — those are device handovers, and a flow declares them with `crossesDevice` rather than a screen pretending there is a link.",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listMerchandise` reads a population and nothing reads one of them; the detail is the row until a `get` exists",
  "purpose": "Manage what the shop sells.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every retail products",
       "bindsTo": "MerchandiseItem",
       "columns": [
        "MerchandiseItem.id",
        "MerchandiseItem.sku",
        "MerchandiseItem.barcode",
        "MerchandiseItem.name",
        "MerchandiseItem.outletId",
        "MerchandiseItem.categoryId",
        "MerchandiseItem.variantId",
        "MerchandiseItem.inventoryItemId",
        "MerchandiseItem.price",
        "MerchandiseItem.onHand",
        "MerchandiseItem.isReturnable",
        "MerchandiseItem.returnWindowDays"
       ],
       "operation": "listMerchandise",
       "provenance": "contract retail.yaml GET /merchandise"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected retail products",
       "bindsTo": "MerchandiseItem",
       "columns": [
        "MerchandiseItem.id",
        "MerchandiseItem.sku",
        "MerchandiseItem.barcode",
        "MerchandiseItem.name",
        "MerchandiseItem.outletId",
        "MerchandiseItem.categoryId",
        "MerchandiseItem.variantId",
        "MerchandiseItem.inventoryItemId",
        "MerchandiseItem.price",
        "MerchandiseItem.onHand",
        "MerchandiseItem.isReturnable",
        "MerchandiseItem.returnWindowDays",
        "MerchandiseItem.requiresSerialNumber",
        "MerchandiseItem.imageAssetRef",
        "MerchandiseItem.isActive"
       ],
       "operation": "listMerchandise",
       "provenance": "contract retail.yaml GET /merchandise"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Lookup",
       "operation": "lookupMerchandise",
       "provenance": "contract retail.yaml GET /merchandise/lookup"
      },
      {
       "kind": "secondaryButton",
       "label": "Create",
       "operation": "createMerchandise",
       "provenance": "contract retail.yaml POST /merchandise"
      },
      {
       "kind": "secondaryButton",
       "label": "Save changes",
       "operation": "updateMerchandise",
       "provenance": "contract retail.yaml PATCH /merchandise/{merchandiseId}"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "carried",
     "components": [
      {
       "kind": "detailPanel",
       "notes": "Structure from the wireframe board. Components not yet enumerated.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "dataTable",
       "derived": true,
       "impliedBy": "listMerchandise",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "searchField",
       "derived": true,
       "impliedBy": "lookupMerchandise",
       "label": "Search",
       "notes": "A search that returns nothing must say so differently from a search not yet run.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "createMerchandise",
       "label": "Create merchandise",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "createMerchandise",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The retail products list.",
   "error": "Could not load. Names which read failed and leaves the retail products untouched.",
   "emptyFirstRun": "No retail products yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the retail products are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listMerchandise",
    "contract": "retail",
    "purpose": "List merchandise",
    "trigger": "onLoad"
   },
   {
    "operationId": "lookupMerchandise",
    "contract": "retail",
    "purpose": "Price and stock check by barcode",
    "trigger": "onLoad"
   },
   {
    "operationId": "createMerchandise",
    "contract": "retail",
    "purpose": "Create a merchandise item",
    "trigger": "onAction",
    "invalidates": [
     "listMerchandise"
    ]
   },
   {
    "operationId": "updateMerchandise",
    "contract": "retail",
    "purpose": "Amend a merchandise item",
    "trigger": "onAction",
    "invalidates": [
     "listMerchandise"
    ]
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "merchandiseId",
     "from": "deepLink"
    }
   ],
   "coldEntry": "**A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know whether the record moved, closed or never existed, because those are three different next actions. **The scope is resolved from the session, never from the link**: a link cannot move somebody to a venue they do not hold. Arrives with `merchandiseId`.",
   "preloaded": [
    "MerchandiseItem.id",
    "MerchandiseItem.sku",
    "MerchandiseItem.barcode",
    "MerchandiseItem.name",
    "MerchandiseItem.outletId"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-048"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 4 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
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
  "id": "BO-051",
  "name": "Purchase Orders",
  "module": "Orders & Money",
  "requiresModule": "ticketing",
  "wave": 2,
  "capability": "C00",
  "implementation": {
   "app": "venue-management-web",
   "route": "/venue-operations/purchase-orders",
   "component": "apps/venue-management-web/src/routes/venue-operations/PurchaseOrdersDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "exitTo": [
    "BO-001",
    "BO-007",
    "BO-008",
    "BO-009"
   ],
   "inferred": true,
   "transitions": [
    {
     "to": "BO-001",
     "trigger": "Queue Directory",
     "carries": [
      "eventId",
      "feedId",
      "queueId"
     ],
     "provenance": "derived — BO-001 declares entryState.params eventId, feedId, queueId, so an edge into it must carry them"
    },
    {
     "to": "BO-007",
     "trigger": "Product Directory",
     "carries": [
      "productId"
     ],
     "provenance": "derived — BO-007 declares entryState.params productId, so an edge into it must carry them"
    },
    {
     "to": "BO-008",
     "trigger": "Product Detail & Variants",
     "carries": [
      "productId",
      "venueId"
     ],
     "provenance": "derived — BO-008 declares entryState.params productId, venueId, so an edge into it must carry them"
    },
    {
     "to": "BO-009",
     "trigger": "Pricing Rules",
     "carries": [
      "priceListId"
     ],
     "provenance": "derived — BO-009 declares entryState.params priceListId, so an edge into it must carry them"
    }
   ]
  },
  "notes": "Definition derived from the wireframe board on 14 August. CF-53 — 67 of these 73 had no definition at all. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual. **createRefund removed 18 August** — attached by module resemblance, not by what this screen does. A screen that does not handle money should not be able to move it (CF-87's class).",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listOrders` reads the population and `getOrder` reads one of them — list, select, act",
  "purpose": "Order more of what is running out.",
  "gaps": [
   {
    "operation": "getOrderStatement",
    "why": "**2 declared operations reach no component on this screen**: getOrderStatement, listOrderRefunds. Either the screen is missing what calls them, or the declaration is residue.",
    "source": "the screen's own declarations"
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
       "label": "Every purchase orders",
       "bindsTo": "OrderSummary",
       "columns": [
        "OrderSummary.id",
        "OrderSummary.orderNumber",
        "OrderSummary.status",
        "OrderSummary.grossAmount",
        "OrderSummary.refundedAmount",
        "OrderSummary.channel",
        "OrderSummary.lineCount"
       ],
       "operation": "listOrders",
       "provenance": "contract orders.yaml GET /orders"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected purchase orders",
       "bindsTo": "Order",
       "columns": [
        "Order.id",
        "Order.orderNumber",
        "Order.channel",
        "Order.venueId",
        "Order.scopePath",
        "Order.status",
        "Order.currency",
        "Order.currencyScale",
        "Order.grossAmount",
        "Order.taxAmount",
        "Order.netAmount",
        "Order.refundedAmount",
        "Order.totalPriceVariance",
        "Order.lines",
        "Order.payments",
        "Order.principalId"
       ],
       "operation": "getOrder",
       "provenance": "contract orders.yaml GET /orders/{orderId}"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Create",
       "operation": "createOrder",
       "provenance": "contract orders.yaml POST /orders"
      },
      {
       "kind": "secondaryButton",
       "label": "Apply",
       "operation": "applyManualDiscount",
       "provenance": "contract orders.yaml POST /orders/{orderId}/discounts"
      },
      {
       "kind": "secondaryButton",
       "label": "Exchange",
       "operation": "exchangeOrderLines",
       "provenance": "contract orders.yaml POST /orders/{orderId}/exchanges"
      },
      {
       "kind": "secondaryButton",
       "label": "Hold",
       "operation": "holdOrder",
       "provenance": "contract orders.yaml POST /orders/{orderId}/hold"
      },
      {
       "kind": "secondaryButton",
       "label": "Modify",
       "operation": "modifyOrder",
       "provenance": "contract orders.yaml POST /orders/{orderId}/modify"
      },
      {
       "kind": "secondaryButton",
       "label": "Reprint",
       "operation": "reprintOrder",
       "provenance": "contract orders.yaml POST /orders/{orderId}/reprints"
      },
      {
       "kind": "secondaryButton",
       "label": "Reschedule",
       "operation": "rescheduleOrder",
       "provenance": "contract orders.yaml POST /orders/{orderId}/reschedule"
      },
      {
       "kind": "secondaryButton",
       "label": "Resume",
       "operation": "resumeOrder",
       "provenance": "contract orders.yaml POST /orders/{orderId}/resume"
      },
      {
       "kind": "destructiveButton",
       "label": "Void",
       "operation": "voidOrder",
       "provenance": "contract orders.yaml POST /orders/{orderId}/voids"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "carried",
     "components": [
      {
       "kind": "detailPanel",
       "notes": "Structure from the wireframe board. Components not yet enumerated.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "dataTable",
       "derived": true,
       "impliedBy": "listOrders",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "createOrder",
       "label": "Create order",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "destructiveButton",
       "derived": true,
       "impliedBy": "voidOrder",
       "label": "Void order",
       "notes": "**Always confirms, never the default focus.** The consequence goes in the body — *cancel 3 orders worth AED 480* is a confirmation, *are you sure* is not.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "createOrder",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "confirmDialog",
       "derived": true,
       "label": "Confirm",
       "notes": "**The consequence goes in the body, not the title.** *Cancel 3 orders worth AED 480* is a confirmation; *are you sure* is not — and a dialog that cannot name what it destroys is a dialog somebody dismisses.\n\n**Added 31 August.** `confirmDialog` and `modal` were both in the component library and used **zero times across 492 screens**, while `destructiveButton` was used 39 times and its own entry reads *always requires confirmation*.",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "overlays": [
   {
    "id": "confirmVoidOrder",
    "component": "confirmDialog",
    "trigger": "Void",
    "body": "**Names what `voidOrder` changes and what it leaves alone**, in the consequence rather than the verb. A purchase orders this affects should be identified in the dialog, not just counted.",
    "provenance": "contract orders.yaml POST /orders/{orderId}/voids"
   }
  ],
  "states": {
   "loading": "The purchase orders list.",
   "error": "Could not load. Names which read failed and leaves the purchase orders untouched.",
   "emptyFirstRun": "No purchase orders yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the purchase orders are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listOrders",
    "contract": "orders",
    "purpose": "List orders",
    "trigger": "onLoad"
   },
   {
    "operationId": "getOrder",
    "contract": "orders",
    "purpose": "Read an order",
    "trigger": "onLoad"
   },
   {
    "operationId": "createOrder",
    "contract": "orders",
    "purpose": "Create an order",
    "trigger": "onAction",
    "invalidates": [
     "listOrders"
    ]
   },
   {
    "operationId": "applyManualDiscount",
    "contract": "orders",
    "purpose": "Apply a discount a cashier chose",
    "trigger": "onAction",
    "invalidates": [
     "listOrders"
    ]
   },
   {
    "operationId": "exchangeOrderLines",
    "contract": "orders",
    "purpose": "Exchange lines for different products or dates",
    "trigger": "onAction",
    "invalidates": [
     "listOrders"
    ]
   },
   {
    "operationId": "getOrderStatement",
    "contract": "orders",
    "purpose": "Full financial history of an order",
    "trigger": "onLoad"
   },
   {
    "operationId": "holdOrder",
    "contract": "orders",
    "purpose": "Park a sale and free the till",
    "trigger": "onAction",
    "invalidates": [
     "listOrders"
    ]
   },
   {
    "operationId": "listOrderRefunds",
    "contract": "orders",
    "purpose": "List refunds against an order",
    "trigger": "onLoad"
   },
   {
    "operationId": "modifyOrder",
    "contract": "orders",
    "purpose": "Add or remove lines on an existing order",
    "trigger": "onAction",
    "invalidates": [
     "listOrders"
    ]
   },
   {
    "operationId": "reprintOrder",
    "contract": "orders",
    "purpose": "Reprint or resend tickets",
    "trigger": "onAction",
    "invalidates": [
     "listOrders"
    ]
   },
   {
    "operationId": "rescheduleOrder",
    "contract": "orders",
    "purpose": "Move an order to another performance",
    "trigger": "onAction",
    "invalidates": [
     "listOrders"
    ]
   },
   {
    "operationId": "resumeOrder",
    "contract": "orders",
    "purpose": "Bring a parked sale back to a till",
    "trigger": "onAction",
    "invalidates": [
     "listOrders"
    ]
   },
   {
    "operationId": "voidOrder",
    "contract": "orders",
    "purpose": "Void an order",
    "trigger": "onAction",
    "invalidates": [
     "listOrders"
    ]
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "orderId",
     "from": "deepLink"
    }
   ],
   "coldEntry": "**A guest opening an order link weeks later.** Shows the order if it still resolves; if it was refunded or the performance passed, says which and offers the order list rather than an error.",
   "preloaded": [
    "Order.id",
    "Order.orderNumber",
    "Order.channel",
    "Order.venueId",
    "Order.scopePath"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-051"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 13 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
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
  "id": "BO-059",
  "name": "Sales Reports",
  "module": "Orders & Money",
  "requiresModule": "analytics",
  "wave": 1,
  "capability": "C00",
  "implementation": {
   "app": "venue-management-web",
   "route": "/venue-operations/sales-reports",
   "component": "apps/venue-management-web/src/routes/venue-operations/SalesReportsDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "exitTo": [
    "BO-001",
    "BO-007",
    "BO-008",
    "BO-009"
   ],
   "inferred": true,
   "transitions": [
    {
     "to": "BO-001",
     "trigger": "Queue Directory",
     "carries": [
      "eventId",
      "feedId",
      "queueId"
     ],
     "provenance": "derived — BO-001 declares entryState.params eventId, feedId, queueId, so an edge into it must carry them"
    },
    {
     "to": "BO-007",
     "trigger": "Product Directory",
     "carries": [
      "productId"
     ],
     "provenance": "derived — BO-007 declares entryState.params productId, so an edge into it must carry them"
    },
    {
     "to": "BO-008",
     "trigger": "Product Detail & Variants",
     "carries": [
      "productId",
      "venueId"
     ],
     "provenance": "derived — BO-008 declares entryState.params productId, venueId, so an edge into it must carry them"
    },
    {
     "to": "BO-009",
     "trigger": "Pricing Rules",
     "carries": [
      "priceListId"
     ],
     "provenance": "derived — BO-009 declares entryState.params priceListId, so an edge into it must carry them"
    }
   ]
  },
  "notes": "Definition derived from the wireframe board on 14 August. CF-53 — 67 of these 73 had no definition at all. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual.",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listReports` reads the population and `getFinancialReport` reads one of them — list, select, act",
  "purpose": "See what sold, through which channel.",
  "gaps": [
   {
    "operation": "getReport",
    "why": "**1 declared operation reach no component on this screen**: getReport. Either the screen is missing what calls them, or the declaration is residue.",
    "source": "the screen's own declarations"
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
       "label": "Every sales reports",
       "bindsTo": "ReportDefinition",
       "columns": [
        "ReportDefinition.name",
        "ReportDefinition.description",
        "ReportDefinition.category",
        "ReportDefinition.dataSource",
        "ReportDefinition.columns",
        "ReportDefinition.filters",
        "ReportDefinition.groupBy",
        "ReportDefinition.parameters",
        "ReportDefinition.requiredPermission",
        "ReportDefinition.maxDateRangeDays",
        "ReportDefinition.id",
        "ReportDefinition.isSystem"
       ],
       "operation": "listReports",
       "provenance": "contract reporting.yaml GET /reports"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected sales reports",
       "bindsTo": "FinancialReport",
       "columns": [
        "FinancialReport.report",
        "FinancialReport.fiscalPeriodId",
        "FinancialReport.legalEntityId",
        "FinancialReport.currency",
        "FinancialReport.currencyScale",
        "FinancialReport.generatedAt",
        "FinancialReport.sections"
       ],
       "operation": "getFinancialReport",
       "provenance": "contract finance.yaml GET /reports/financial"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Create",
       "operation": "createReport",
       "provenance": "contract reporting.yaml POST /reports"
      },
      {
       "kind": "secondaryButton",
       "label": "Ask",
       "operation": "askReportingQuestion",
       "provenance": "contract reporting.yaml POST /reports/ask"
      },
      {
       "kind": "destructiveButton",
       "label": "Delete",
       "operation": "deleteReport",
       "provenance": "contract reporting.yaml DELETE /reports/{reportId}"
      },
      {
       "kind": "secondaryButton",
       "label": "Run",
       "operation": "runReport",
       "provenance": "contract reporting.yaml POST /reports/{reportId}/run"
      },
      {
       "kind": "secondaryButton",
       "label": "Save",
       "operation": "saveNaturalLanguageQuery",
       "provenance": "contract reporting.yaml POST /reports/ask/{conversationId}/save"
      },
      {
       "kind": "secondaryButton",
       "label": "Save changes",
       "operation": "updateReport",
       "provenance": "contract reporting.yaml PUT /reports/{reportId}"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "carried",
     "components": [
      {
       "kind": "detailPanel",
       "notes": "Structure from the wireframe board. Components not yet enumerated.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "dataTable",
       "derived": true,
       "impliedBy": "listReports",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "createReport",
       "label": "Create report",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "destructiveButton",
       "derived": true,
       "impliedBy": "deleteReport",
       "label": "Delete report",
       "notes": "**Always confirms, never the default focus.** The consequence goes in the body — *cancel 3 orders worth AED 480* is a confirmation, *are you sure* is not.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "createReport",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "confirmDialog",
       "derived": true,
       "label": "Confirm",
       "notes": "**The consequence goes in the body, not the title.** *Cancel 3 orders worth AED 480* is a confirmation; *are you sure* is not — and a dialog that cannot name what it destroys is a dialog somebody dismisses.\n\n**Added 31 August.** `confirmDialog` and `modal` were both in the component library and used **zero times across 492 screens**, while `destructiveButton` was used 39 times and its own entry reads *always requires confirmation*.",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "overlays": [
   {
    "id": "confirmDeleteReport",
    "component": "confirmDialog",
    "trigger": "Delete",
    "body": "**Names what `deleteReport` changes and what it leaves alone**, in the consequence rather than the verb. A sales reports this affects should be identified in the dialog, not just counted.",
    "provenance": "contract reporting.yaml DELETE /reports/{reportId}"
   }
  ],
  "states": {
   "loading": "The sales reports list.",
   "error": "Could not load. Names which read failed and leaves the sales reports untouched.",
   "emptyFirstRun": "No sales reports yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the sales reports are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getFinancialReport",
    "contract": "finance",
    "purpose": "P&L, balance sheet or cash flow",
    "trigger": "onLoad"
   },
   {
    "operationId": "listReports",
    "contract": "reporting",
    "purpose": "List available report definitions",
    "trigger": "onLoad"
   },
   {
    "operationId": "createReport",
    "contract": "reporting",
    "purpose": "Create a custom report definition",
    "trigger": "onAction",
    "invalidates": [
     "listReports"
    ]
   },
   {
    "operationId": "askReportingQuestion",
    "contract": "reporting",
    "purpose": "Natural-language reporting query",
    "trigger": "onAction",
    "invalidates": [
     "listReports"
    ]
   },
   {
    "operationId": "deleteReport",
    "contract": "reporting",
    "purpose": "Retire a report definition",
    "trigger": "onAction",
    "invalidates": [
     "listReports"
    ]
   },
   {
    "operationId": "getReport",
    "contract": "reporting",
    "purpose": "Read a report definition",
    "trigger": "onLoad"
   },
   {
    "operationId": "runReport",
    "contract": "reporting",
    "purpose": "Run a report",
    "trigger": "onAction",
    "invalidates": [
     "listReports"
    ]
   },
   {
    "operationId": "saveNaturalLanguageQuery",
    "contract": "reporting",
    "purpose": "Save a natural-language answer as a report definition",
    "trigger": "onAction",
    "invalidates": [
     "listReports"
    ]
   },
   {
    "operationId": "updateReport",
    "contract": "reporting",
    "purpose": "Publish a new version of a definition",
    "trigger": "onAction",
    "invalidates": [
     "listReports"
    ]
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "conversationId",
     "from": "deepLink"
    },
    {
     "name": "reportId",
     "from": "deepLink"
    }
   ],
   "coldEntry": "A conversation link an agent opens from a notification. Resolves, or says it was closed and by whom.",
   "preloaded": [
    "FinancialReport.report",
    "FinancialReport.fiscalPeriodId",
    "FinancialReport.legalEntityId",
    "FinancialReport.currency",
    "FinancialReport.currencyScale"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-059"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 9 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
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
  "id": "BO-061",
  "name": "Scheduled Reports",
  "module": "Orders & Money",
  "requiresModule": "analytics",
  "wave": 3,
  "capability": "C00",
  "implementation": {
   "app": "venue-management-web",
   "route": "/venue-operations/scheduled-reports",
   "component": "apps/venue-management-web/src/routes/venue-operations/ScheduledReportsDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "exitTo": [
    "BO-001",
    "BO-007",
    "BO-008",
    "BO-009",
    "BO-060"
   ],
   "inferred": true,
   "entryFrom": [
    "BO-058"
   ],
   "transitions": [
    {
     "to": "BO-060",
     "trigger": "Attendance & Footfall",
     "provenance": "flow F107 step 2→3",
     "operation": "updateReport"
    },
    {
     "to": "BO-001",
     "trigger": "Queue Directory",
     "carries": [
      "eventId",
      "feedId",
      "queueId"
     ],
     "provenance": "derived — BO-001 declares entryState.params eventId, feedId, queueId, so an edge into it must carry them"
    },
    {
     "to": "BO-007",
     "trigger": "Product Directory",
     "carries": [
      "productId"
     ],
     "provenance": "derived — BO-007 declares entryState.params productId, so an edge into it must carry them"
    },
    {
     "to": "BO-008",
     "trigger": "Product Detail & Variants",
     "carries": [
      "productId",
      "venueId"
     ],
     "provenance": "derived — BO-008 declares entryState.params productId, venueId, so an edge into it must carry them"
    },
    {
     "to": "BO-009",
     "trigger": "Pricing Rules",
     "carries": [
      "priceListId"
     ],
     "provenance": "derived — BO-009 declares entryState.params priceListId, so an edge into it must carry them"
    }
   ]
  },
  "notes": "Definition derived from the wireframe board on 14 August. CF-53 — 67 of these 73 had no definition at all. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual.",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listReports` reads the population and `getFinancialReport` reads one of them — list, select, act",
  "purpose": "Send a report to somebody without them asking.",
  "gaps": [
   {
    "operation": "getReport",
    "why": "**1 declared operation reach no component on this screen**: getReport. Either the screen is missing what calls them, or the declaration is residue.",
    "source": "the screen's own declarations"
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
       "label": "Every scheduled reports",
       "bindsTo": "ReportDefinition",
       "columns": [
        "ReportDefinition.name",
        "ReportDefinition.description",
        "ReportDefinition.category",
        "ReportDefinition.dataSource",
        "ReportDefinition.columns",
        "ReportDefinition.filters",
        "ReportDefinition.groupBy",
        "ReportDefinition.parameters",
        "ReportDefinition.requiredPermission",
        "ReportDefinition.maxDateRangeDays",
        "ReportDefinition.id",
        "ReportDefinition.isSystem"
       ],
       "operation": "listReports",
       "provenance": "contract reporting.yaml GET /reports"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected scheduled reports",
       "bindsTo": "FinancialReport",
       "columns": [
        "FinancialReport.report",
        "FinancialReport.fiscalPeriodId",
        "FinancialReport.legalEntityId",
        "FinancialReport.currency",
        "FinancialReport.currencyScale",
        "FinancialReport.generatedAt",
        "FinancialReport.sections"
       ],
       "operation": "getFinancialReport",
       "provenance": "contract finance.yaml GET /reports/financial"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Create",
       "operation": "createReport",
       "provenance": "contract reporting.yaml POST /reports"
      },
      {
       "kind": "secondaryButton",
       "label": "Ask",
       "operation": "askReportingQuestion",
       "provenance": "contract reporting.yaml POST /reports/ask"
      },
      {
       "kind": "destructiveButton",
       "label": "Delete",
       "operation": "deleteReport",
       "provenance": "contract reporting.yaml DELETE /reports/{reportId}"
      },
      {
       "kind": "secondaryButton",
       "label": "Run",
       "operation": "runReport",
       "provenance": "contract reporting.yaml POST /reports/{reportId}/run"
      },
      {
       "kind": "secondaryButton",
       "label": "Save",
       "operation": "saveNaturalLanguageQuery",
       "provenance": "contract reporting.yaml POST /reports/ask/{conversationId}/save"
      },
      {
       "kind": "secondaryButton",
       "label": "Save changes",
       "operation": "updateReport",
       "provenance": "contract reporting.yaml PUT /reports/{reportId}"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "carried",
     "components": [
      {
       "kind": "detailPanel",
       "notes": "Structure from the wireframe board. Components not yet enumerated.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "dataTable",
       "derived": true,
       "impliedBy": "listReports",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "createReport",
       "label": "Create report",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "destructiveButton",
       "derived": true,
       "impliedBy": "deleteReport",
       "label": "Delete report",
       "notes": "**Always confirms, never the default focus.** The consequence goes in the body — *cancel 3 orders worth AED 480* is a confirmation, *are you sure* is not.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "createReport",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "confirmDialog",
       "derived": true,
       "label": "Confirm",
       "notes": "**The consequence goes in the body, not the title.** *Cancel 3 orders worth AED 480* is a confirmation; *are you sure* is not — and a dialog that cannot name what it destroys is a dialog somebody dismisses.\n\n**Added 31 August.** `confirmDialog` and `modal` were both in the component library and used **zero times across 492 screens**, while `destructiveButton` was used 39 times and its own entry reads *always requires confirmation*.",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "overlays": [
   {
    "id": "confirmDeleteReport",
    "component": "confirmDialog",
    "trigger": "Delete",
    "body": "**Names what `deleteReport` changes and what it leaves alone**, in the consequence rather than the verb. A scheduled reports this affects should be identified in the dialog, not just counted.",
    "provenance": "contract reporting.yaml DELETE /reports/{reportId}"
   }
  ],
  "states": {
   "loading": "The scheduled reports list.",
   "error": "Could not load. Names which read failed and leaves the scheduled reports untouched.",
   "emptyFirstRun": "No scheduled reports yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the scheduled reports are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getFinancialReport",
    "contract": "finance",
    "purpose": "P&L, balance sheet or cash flow",
    "trigger": "onLoad"
   },
   {
    "operationId": "listReports",
    "contract": "reporting",
    "purpose": "List available report definitions",
    "trigger": "onLoad"
   },
   {
    "operationId": "createReport",
    "contract": "reporting",
    "purpose": "Create a custom report definition",
    "trigger": "onAction",
    "invalidates": [
     "listReports"
    ]
   },
   {
    "operationId": "askReportingQuestion",
    "contract": "reporting",
    "purpose": "Natural-language reporting query",
    "trigger": "onAction",
    "invalidates": [
     "listReports"
    ]
   },
   {
    "operationId": "deleteReport",
    "contract": "reporting",
    "purpose": "Retire a report definition",
    "trigger": "onAction",
    "invalidates": [
     "listReports"
    ]
   },
   {
    "operationId": "getReport",
    "contract": "reporting",
    "purpose": "Read a report definition",
    "trigger": "onLoad"
   },
   {
    "operationId": "runReport",
    "contract": "reporting",
    "purpose": "Run a report",
    "trigger": "onAction",
    "invalidates": [
     "listReports"
    ]
   },
   {
    "operationId": "saveNaturalLanguageQuery",
    "contract": "reporting",
    "purpose": "Save a natural-language answer as a report definition",
    "trigger": "onAction",
    "invalidates": [
     "listReports"
    ]
   },
   {
    "operationId": "updateReport",
    "contract": "reporting",
    "purpose": "Publish a new version of a definition",
    "trigger": "onAction",
    "invalidates": [
     "listReports"
    ]
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "conversationId",
     "from": "deepLink"
    },
    {
     "name": "reportId",
     "from": "deepLink"
    }
   ],
   "coldEntry": "A conversation link an agent opens from a notification. Resolves, or says it was closed and by whom.",
   "preloaded": [
    "FinancialReport.report",
    "FinancialReport.fiscalPeriodId",
    "FinancialReport.legalEntityId",
    "FinancialReport.currency",
    "FinancialReport.currencyScale"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-061"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 9 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
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
  "id": "BO-062",
  "name": "Venue Profile",
  "module": "Orders & Money",
  "requiresModule": "ticketing",
  "wave": 1,
  "capability": "C00",
  "implementation": {
   "app": "venue-management-web",
   "route": "/venue-operations/venue-profile",
   "component": "apps/venue-management-web/src/routes/venue-operations/VenueProfileDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "exitTo": [
    "BO-001",
    "BO-007",
    "BO-008",
    "BO-009"
   ],
   "inferred": true,
   "transitions": [
    {
     "to": "BO-001",
     "trigger": "Queue Directory",
     "carries": [
      "eventId",
      "feedId",
      "queueId"
     ],
     "provenance": "derived — BO-001 declares entryState.params eventId, feedId, queueId, so an edge into it must carry them"
    },
    {
     "to": "BO-007",
     "trigger": "Product Directory",
     "carries": [
      "productId"
     ],
     "provenance": "derived — BO-007 declares entryState.params productId, so an edge into it must carry them"
    },
    {
     "to": "BO-008",
     "trigger": "Product Detail & Variants",
     "carries": [
      "productId",
      "venueId"
     ],
     "provenance": "derived — BO-008 declares entryState.params productId, venueId, so an edge into it must carry them"
    },
    {
     "to": "BO-009",
     "trigger": "Pricing Rules",
     "carries": [
      "priceListId"
     ],
     "provenance": "derived — BO-009 declares entryState.params priceListId, so an edge into it must carry them"
    }
   ]
  },
  "notes": "Definition derived from the wireframe board on 14 August. CF-53 — 67 of these 73 had no definition at all. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual.",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listDiningOutlets` reads the population and `getRefundPolicy` reads one of them — list, select, act",
  "purpose": "The facts every other surface reads.",
  "gaps": [
   {
    "operation": "listDeliveryLocations",
    "why": "**1 declared operation reach no component on this screen**: listDeliveryLocations. Either the screen is missing what calls them, or the declaration is residue.",
    "source": "the screen's own declarations"
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
       "label": "Every venue profile",
       "bindsTo": "DiningOutlet",
       "columns": [
        "DiningOutlet.outletId",
        "DiningOutlet.name",
        "DiningOutlet.kind",
        "DiningOutlet.zone",
        "DiningOutlet.cuisine",
        "DiningOutlet.isOpenNow",
        "DiningOutlet.opensAt",
        "DiningOutlet.closesAt",
        "DiningOutlet.orderingMethod",
        "DiningOutlet.estimatedWaitMinutes",
        "DiningOutlet.imageAssetRef",
        "DiningOutlet.menuId"
       ],
       "operation": "listDiningOutlets",
       "provenance": "contract fnb.yaml GET /venues/{venueId}/dining"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected venue profile",
       "bindsTo": "RefundPolicy",
       "columns": [
        "RefundPolicy.id",
        "RefundPolicy.venueId",
        "RefundPolicy.selfAuthoriseLimit",
        "RefundPolicy.requiresSecondUserAbove",
        "RefundPolicy.requiresApprovalAbove",
        "RefundPolicy.timeBands",
        "RefundPolicy.allowPartial",
        "RefundPolicy.refundWindowDays",
        "RefundPolicy.varianceThreshold"
       ],
       "operation": "getRefundPolicy",
       "provenance": "contract orders.yaml GET /venues/{venueId}/refund-policy"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Save changes",
       "operation": "setRefundPolicy",
       "provenance": "contract orders.yaml PUT /venues/{venueId}/refund-policy"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "carried",
     "components": [
      {
       "kind": "detailPanel",
       "notes": "Structure from the wireframe board. Components not yet enumerated.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "dataTable",
       "derived": true,
       "impliedBy": "listDiningOutlets",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "setRefundPolicy",
       "label": "Save refund policy",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "setRefundPolicy",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The venue profile list.",
   "error": "Could not load. Names which read failed and leaves the venue profile untouched.",
   "emptyFirstRun": "No venue profile yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the venue profile are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getRefundPolicy",
    "contract": "orders",
    "purpose": "Read a venue's refund policy",
    "trigger": "onLoad"
   },
   {
    "operationId": "listDiningOutlets",
    "contract": "fnb",
    "purpose": "Where a guest can eat, right now",
    "trigger": "onLoad"
   },
   {
    "operationId": "setRefundPolicy",
    "contract": "orders",
    "purpose": "Set a venue's refund policy",
    "trigger": "onAction",
    "invalidates": [
     "listDiningOutlets"
    ]
   },
   {
    "operationId": "listDeliveryLocations",
    "contract": "fnb",
    "purpose": "Where an order can be delivered",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "venueId",
     "from": "session"
    }
   ],
   "coldEntry": "Resolves from the session; a cold arrival is the ordinary case.",
   "preloaded": [
    "RefundPolicy.id",
    "RefundPolicy.venueId",
    "RefundPolicy.selfAuthoriseLimit",
    "RefundPolicy.requiresSecondUserAbove",
    "RefundPolicy.requiresApprovalAbove"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-062"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 4 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
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
 "acceptShiftVariance": {
  "method": "POST",
  "path": "/shifts/{shiftId}/accept-variance",
  "contract": "shift",
  "summary": "Accept an over/short beyond the threshold",
  "permission": "OVERSHORT_ACCEPT",
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
  "requestBody": null,
  "responds": "Shift"
 },
 "applyManualDiscount": {
  "method": "POST",
  "path": "/orders/{orderId}/discounts",
  "contract": "orders",
  "summary": "Apply a discount a cashier chose",
  "permission": "ORDER_DISCOUNT",
  "offlineCapable": true,
  "conflictPolicy": "append",
  "scopeLevel": "workstation",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "ManualDiscountRequest",
  "responds": "Order"
 },
 "approveShiftOpen": {
  "method": "POST",
  "path": "/shifts/{shiftId}/approve-open",
  "contract": "shift",
  "summary": "Approve a shift opening outside tolerance",
  "permission": "SHIFT_APPROVE_OPEN",
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
  "responds": "Shift"
 },
 "askReportingQuestion": {
  "method": "POST",
  "path": "/reports/ask",
  "contract": "reporting",
  "summary": "Natural-language reporting query",
  "permission": "REPORT_VIEW_VENUE",
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
  "responds": "NaturalLanguageAnswer"
 },
 "closeShift": {
  "method": "POST",
  "path": "/shifts/{shiftId}/close",
  "contract": "shift",
  "summary": "Blind close-out",
  "permission": "SHIFT_CLOSE",
  "offlineCapable": true,
  "conflictPolicy": "append",
  "scopeLevel": "workstation",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "CloseShiftRequest",
  "responds": "ShiftCloseResult"
 },
 "createCashMovement": {
  "method": "POST",
  "path": "/shifts/{shiftId}/cash-movements",
  "contract": "shift",
  "summary": "Record a cash lift or add",
  "permission": "CASH_LIFT",
  "offlineCapable": true,
  "conflictPolicy": "append",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "CreateCashMovementRequest",
  "responds": "CashMovement"
 },
 "createMerchandise": {
  "method": "POST",
  "path": "/merchandise",
  "contract": "retail",
  "summary": "Create a merchandise item",
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
  "requestBody": "CreateMerchandiseRequest",
  "responds": "MerchandiseItem"
 },
 "createOrder": {
  "method": "POST",
  "path": "/orders",
  "contract": "orders",
  "summary": "Create an order",
  "permission": "ORDER_CREATE",
  "offlineCapable": true,
  "conflictPolicy": "append",
  "scopeLevel": "workstation",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "CreateOrderRequest",
  "responds": "Order"
 },
 "createRefund": {
  "method": "POST",
  "path": "/orders/{orderId}/refunds",
  "contract": "orders",
  "summary": "Refund an order, wholly or in part",
  "permission": "ORDER_REFUND",
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
  "requestBody": "CreateRefundRequest",
  "responds": null
 },
 "createReport": {
  "method": "POST",
  "path": "/reports",
  "contract": "reporting",
  "summary": "Create a custom report definition",
  "permission": "REPORT_MANAGE",
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
  "requestBody": "CreateReportRequest",
  "responds": "ReportDefinition"
 },
 "deleteReport": {
  "method": "DELETE",
  "path": "/reports/{reportId}",
  "contract": "reporting",
  "summary": "Retire a report definition",
  "permission": "REPORT_MANAGE",
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
 "exchangeOrderLines": {
  "method": "POST",
  "path": "/orders/{orderId}/exchanges",
  "contract": "orders",
  "summary": "Exchange lines for different products or dates",
  "permission": "ORDER_EXCHANGE",
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
  "requestBody": "ExchangeOrderRequest",
  "responds": "OrderExchangeResult"
 },
 "getCurrentShift": {
  "method": "GET",
  "path": "/shifts/current",
  "contract": "shift",
  "summary": "The open or suspended shift on the session's workstation",
  "permission": "SHIFT_OPEN",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "workstation",
  "parameters": [],
  "requestBody": null,
  "responds": "Shift"
 },
 "getFinancialReport": {
  "method": "GET",
  "path": "/reports/financial",
  "contract": "finance",
  "summary": "P&L, balance sheet or cash flow",
  "permission": "REPORT_VIEW_VENUE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "report",
    "in": "query",
    "required": true
   },
   {
    "name": "fiscalPeriodId",
    "in": "query",
    "required": true
   },
   {
    "name": "legalEntityId",
    "in": "query",
    "required": null
   },
   {
    "name": "venueId",
    "in": "query",
    "required": null
   },
   {
    "name": "costCenterId",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "FinancialReport"
 },
 "getOrder": {
  "method": "GET",
  "path": "/orders/{orderId}",
  "contract": "orders",
  "summary": "Read an order",
  "permission": "ORDER_VIEW",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "Order"
 },
 "getOrderStatement": {
  "method": "GET",
  "path": "/orders/{orderId}/statement",
  "contract": "orders",
  "summary": "Full financial history of an order",
  "permission": "ORDER_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "OrderStatement"
 },
 "getRefundPolicy": {
  "method": "GET",
  "path": "/venues/{venueId}/refund-policy",
  "contract": "orders",
  "summary": "Read a venue's refund policy",
  "permission": "ORDER_VIEW",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "RefundPolicy"
 },
 "getReport": {
  "method": "GET",
  "path": "/reports/{reportId}",
  "contract": "reporting",
  "summary": "Read a report definition",
  "permission": "REPORT_VIEW_VENUE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "ReportDefinition"
 },
 "getSettlement": {
  "method": "GET",
  "path": "/settlements/{settlementId}",
  "contract": "finance",
  "summary": "Settlement detail with match results",
  "permission": "SETTLEMENT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "region",
  "parameters": [],
  "requestBody": null,
  "responds": "Settlement"
 },
 "getShift": {
  "method": "GET",
  "path": "/shifts/{shiftId}",
  "contract": "shift",
  "summary": "Read a shift",
  "permission": "REPORT_VIEW_WORKSTATION",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "Shift"
 },
 "getTrialBalance": {
  "method": "GET",
  "path": "/ledger/trial-balance",
  "contract": "finance",
  "summary": "Trial balance for a period",
  "permission": "LEDGER_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "region",
  "parameters": [
   {
    "name": "fiscalPeriodId",
    "in": "query",
    "required": true
   },
   {
    "name": "legalEntityId",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "TrialBalance"
 },
 "holdOrder": {
  "method": "POST",
  "path": "/orders/{orderId}/hold",
  "contract": "orders",
  "summary": "Park a sale and free the till",
  "permission": "ORDER_MODIFY",
  "offlineCapable": true,
  "conflictPolicy": "lastWriterWins",
  "scopeLevel": "workstation",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "Order"
 },
 "ingestSettlementFile": {
  "method": "POST",
  "path": "/settlements",
  "contract": "finance",
  "summary": "Ingest a provider settlement file",
  "permission": "SETTLEMENT_RECONCILE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "region",
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
 "listCashMovements": {
  "method": "GET",
  "path": "/shifts/{shiftId}/cash-movements",
  "contract": "shift",
  "summary": "Lifts, adds and the opening float",
  "permission": "REPORT_VIEW_WORKSTATION",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
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
  "responds": "CashMovement"
 },
 "listDeliveryLocations": {
  "method": "GET",
  "path": "/venues/{venueId}/delivery-locations",
  "contract": "fnb",
  "summary": "Where an order can be delivered",
  "permission": null,
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
    "name": "servingOutletId",
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
  "responds": "DeliveryLocation"
 },
 "listDiningOutlets": {
  "method": "GET",
  "path": "/venues/{venueId}/dining",
  "contract": "fnb",
  "summary": "Where a guest can eat, right now",
  "permission": null,
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "openNow",
    "in": "query",
    "required": null
   },
   {
    "name": "orderingMethod",
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
  "responds": "DiningOutlet"
 },
 "listLedgerEntries": {
  "method": "GET",
  "path": "/ledger/entries",
  "contract": "finance",
  "summary": "Query the ledger",
  "permission": "LEDGER_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "accountId",
    "in": "query",
    "required": null
   },
   {
    "name": "venueId",
    "in": "query",
    "required": null
   },
   {
    "name": "costCenterId",
    "in": "query",
    "required": null
   },
   {
    "name": "sourceType",
    "in": "query",
    "required": null
   },
   {
    "name": "sourceId",
    "in": "query",
    "required": null
   },
   {
    "name": "postedFrom",
    "in": "query",
    "required": null
   },
   {
    "name": "postedTo",
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
 "listMerchandise": {
  "method": "GET",
  "path": "/merchandise",
  "contract": "retail",
  "summary": "List merchandise",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "outletId",
    "in": "query",
    "required": null
   },
   {
    "name": "categoryId",
    "in": "query",
    "required": null
   },
   {
    "name": "inStockOnly",
    "in": "query",
    "required": null
   },
   {
    "name": "search",
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
 "listOrderRefunds": {
  "method": "GET",
  "path": "/orders/{orderId}/refunds",
  "contract": "orders",
  "summary": "List refunds against an order",
  "permission": "ORDER_VIEW",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
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
  "responds": "Refund"
 },
 "listOrders": {
  "method": "GET",
  "path": "/orders",
  "contract": "orders",
  "summary": "List orders",
  "permission": "ORDER_VIEW",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "venueId",
    "in": "query",
    "required": null
   },
   {
    "name": "principalId",
    "in": "query",
    "required": null
   },
   {
    "name": "shiftId",
    "in": "query",
    "required": null
   },
   {
    "name": "status",
    "in": "query",
    "required": null
   },
   {
    "name": "createdFrom",
    "in": "query",
    "required": null
   },
   {
    "name": "createdTo",
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
 "listReports": {
  "method": "GET",
  "path": "/reports",
  "contract": "reporting",
  "summary": "List available report definitions",
  "permission": "REPORT_VIEW_VENUE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "category",
    "in": "query",
    "required": null
   },
   {
    "name": "search",
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
 "listSettlementExceptions": {
  "method": "GET",
  "path": "/settlements/{settlementId}/exceptions",
  "contract": "finance",
  "summary": "Unmatched or mismatched settlement lines",
  "permission": "SETTLEMENT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "region",
  "parameters": [
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
 "listSettlements": {
  "method": "GET",
  "path": "/settlements",
  "contract": "finance",
  "summary": "List settlement batches",
  "permission": "SETTLEMENT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "region",
  "parameters": [
   {
    "name": "providerName",
    "in": "query",
    "required": null
   },
   {
    "name": "status",
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
 "listShifts": {
  "method": "GET",
  "path": "/shifts",
  "contract": "shift",
  "summary": "List shifts",
  "permission": "REPORT_VIEW_WORKSTATION",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "workstationId",
    "in": "query",
    "required": null
   },
   {
    "name": "status",
    "in": "query",
    "required": null
   },
   {
    "name": "openedFrom",
    "in": "query",
    "required": null
   },
   {
    "name": "openedTo",
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
 "lookupMerchandise": {
  "method": "GET",
  "path": "/merchandise/lookup",
  "contract": "retail",
  "summary": "Price and stock check by barcode",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "barcode",
    "in": "query",
    "required": null
   },
   {
    "name": "sku",
    "in": "query",
    "required": null
   },
   {
    "name": "includeSiblingOutlets",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "PriceCheck"
 },
 "modifyOrder": {
  "method": "POST",
  "path": "/orders/{orderId}/modify",
  "contract": "orders",
  "summary": "Add or remove lines on an existing order",
  "permission": "ORDER_MODIFY",
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
  "requestBody": "ModifyOrderRequest",
  "responds": "OrderModificationResult"
 },
 "openShift": {
  "method": "POST",
  "path": "/shifts",
  "contract": "shift",
  "summary": "Open a shift",
  "permission": "SHIFT_OPEN",
  "offlineCapable": true,
  "conflictPolicy": "append",
  "scopeLevel": "workstation",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "OpenShiftRequest",
  "responds": "Shift"
 },
 "recordNoSale": {
  "method": "POST",
  "path": "/shifts/{shiftId}/no-sale",
  "contract": "shift",
  "summary": "Open the drawer without a sale",
  "permission": "SHIFT_SUSPEND",
  "offlineCapable": true,
  "conflictPolicy": "append",
  "scopeLevel": "workstation",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "NoSaleEvent"
 },
 "reopenShift": {
  "method": "POST",
  "path": "/shifts/{shiftId}/reopen",
  "contract": "shift",
  "summary": "Reopen a shift closed in error",
  "permission": "SHIFT_REOPEN",
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
  "responds": "Shift"
 },
 "reprintOrder": {
  "method": "POST",
  "path": "/orders/{orderId}/reprints",
  "contract": "orders",
  "summary": "Reprint or resend tickets",
  "permission": "ORDER_REPRINT",
  "offlineCapable": true,
  "conflictPolicy": "append",
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
 "rescheduleOrder": {
  "method": "POST",
  "path": "/orders/{orderId}/reschedule",
  "contract": "orders",
  "summary": "Move an order to another performance",
  "permission": "ORDER_RESCHEDULE",
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
  "responds": "OrderExchangeResult"
 },
 "resolveSettlementException": {
  "method": "POST",
  "path": "/settlements/{settlementId}/exceptions",
  "contract": "finance",
  "summary": "Resolve a settlement exception",
  "permission": "SETTLEMENT_RECONCILE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "region",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "SettlementException"
 },
 "resumeOrder": {
  "method": "POST",
  "path": "/orders/{orderId}/resume",
  "contract": "orders",
  "summary": "Bring a parked sale back to a till",
  "permission": "ORDER_MODIFY",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "workstation",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "OrderResumeResult"
 },
 "resumeShift": {
  "method": "POST",
  "path": "/shifts/{shiftId}/resume",
  "contract": "shift",
  "summary": "Resume a suspended shift",
  "permission": "SHIFT_OPEN",
  "offlineCapable": true,
  "conflictPolicy": "append",
  "scopeLevel": "workstation",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "Shift"
 },
 "runReport": {
  "method": "POST",
  "path": "/reports/{reportId}/run",
  "contract": "reporting",
  "summary": "Run a report",
  "permission": "REPORT_VIEW_VENUE",
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
  "requestBody": "RunReportRequest",
  "responds": "ReportResult"
 },
 "saveNaturalLanguageQuery": {
  "method": "POST",
  "path": "/reports/ask/{conversationId}/save",
  "contract": "reporting",
  "summary": "Save a natural-language answer as a report definition",
  "permission": "REPORT_MANAGE",
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
  "responds": "ReportDefinition"
 },
 "setRefundPolicy": {
  "method": "PUT",
  "path": "/venues/{venueId}/refund-policy",
  "contract": "orders",
  "summary": "Set a venue's refund policy",
  "permission": "REGION_CONFIGURE",
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
  "requestBody": "RefundPolicy",
  "responds": "RefundPolicy"
 },
 "suspendShift": {
  "method": "POST",
  "path": "/shifts/{shiftId}/suspend",
  "contract": "shift",
  "summary": "Suspend a shift so another user can log in",
  "permission": "SHIFT_SUSPEND",
  "offlineCapable": true,
  "conflictPolicy": "append",
  "scopeLevel": "workstation",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "Shift"
 },
 "updateMerchandise": {
  "method": "PATCH",
  "path": "/merchandise/{merchandiseId}",
  "contract": "retail",
  "summary": "Amend a merchandise item",
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
  "requestBody": null,
  "responds": "MerchandiseItem"
 },
 "updateReport": {
  "method": "PUT",
  "path": "/reports/{reportId}",
  "contract": "reporting",
  "summary": "Publish a new version of a definition",
  "permission": "REPORT_MANAGE",
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
  "requestBody": "CreateReportRequest",
  "responds": "ReportDefinition"
 },
 "voidOrder": {
  "method": "POST",
  "path": "/orders/{orderId}/voids",
  "contract": "orders",
  "summary": "Void an order",
  "permission": "ORDER_VOID",
  "offlineCapable": true,
  "conflictPolicy": "append",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "Order"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "AccountType": {
  "type": "string",
  "enum": [
   "asset",
   "liability",
   "equity",
   "revenue",
   "expense"
  ]
 },
 "CashMovement": {
  "x-ticvai-persistence": "orders.cash_movement",
  "allOf": [
   {
    "$ref": "#/components/schemas/CreateCashMovementRequest"
   },
   {
    "type": "object",
    "required": [
     "shiftId",
     "authorisedByPrincipalId",
     "sequence"
    ],
    "properties": {
     "shiftId": {
      "type": "string"
     },
     "authorisedByPrincipalId": {
      "type": "string",
      "format": "uuid",
      "description": "The principal who authorised the movement, recorded for audit."
     },
     "sequence": {
      "type": "integer",
      "description": "Monotonic within the shift. Preserves order across an offline batch."
     },
     "syncedAt": {
      "type": "string",
      "format": "date-time",
      "nullable": true
     }
    }
   }
  ]
 },
 "CashMovementKind": {
  "type": "string",
  "enum": [
   "openingFloat",
   "lift",
   "add"
  ]
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
 "CloseShiftRequest": {
  "type": "object",
  "required": [
   "countedCash",
   "recordedAt"
  ],
  "properties": {
   "countedCash": {
    "$ref": "#/components/schemas/DenominationCount"
   },
   "nonCashDeclared": {
    "type": "array",
    "description": "Declared totals per non-cash tender, for reconciliation against captured payments.\n",
    "items": {
     "type": "object",
     "required": [
      "tender",
      "amount"
     ],
     "properties": {
      "tender": {
       "type": "string"
      },
      "amount": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      }
     }
    }
   },
   "notes": {
    "type": "string",
    "maxLength": 1000
   },
   "releaseHeldLeases": {
    "type": "boolean",
    "default": true,
    "description": "Return unsold inventory leases held by this workstation (ADR-0013 C103). Closing without releasing strands capacity until TTL expiry, which is visible at a gate during peak.\n"
   },
   "recordedAt": {
    "type": "string",
    "format": "date-time"
   }
  }
 },
 "CreateCashMovementRequest": {
  "type": "object",
  "required": [
   "id",
   "kind",
   "amount",
   "recordedAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$",
    "description": "Client-generated ULID."
   },
   "kind": {
    "$ref": "#/components/schemas/CashMovementKind"
   },
   "amount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "denominations": {
    "$ref": "#/components/schemas/DenominationCount"
   },
   "reference": {
    "type": "string",
    "maxLength": 64,
    "description": "Safe drop reference or bag number."
   },
   "reason": {
    "type": "string",
    "maxLength": 500
   },
   "recordedAt": {
    "type": "string",
    "format": "date-time"
   }
  }
 },
 "CreateMerchandiseRequest": {
  "x-ticvai-persistence": "none — request only",
  "type": "object",
  "required": [
   "sku",
   "name",
   "outletId",
   "variantId"
  ],
  "properties": {
   "sku": {
    "type": "string",
    "maxLength": 64
   },
   "barcode": {
    "type": "string",
    "maxLength": 128
   },
   "name": {
    "type": "string",
    "maxLength": 200
   },
   "outletId": {
    "type": "string",
    "format": "uuid"
   },
   "categoryId": {
    "type": "string",
    "format": "uuid"
   },
   "variantId": {
    "type": "string",
    "format": "uuid"
   },
   "inventoryItemId": {
    "type": "string",
    "format": "uuid"
   },
   "isReturnable": {
    "type": "boolean",
    "default": true
   },
   "returnWindowDays": {
    "type": "integer"
   },
   "requiresSerialNumber": {
    "type": "boolean",
    "default": false
   },
   "imageAssetRef": {
    "type": "string"
   }
  }
 },
 "CreateOrderLine": {
  "x-ticvai-persistence": "none — request only",
  "type": "object",
  "required": [
   "id",
   "variantId",
   "quantity",
   "quotedUnitPrice"
  ],
  "properties": {
   "id": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
   },
   "variantId": {
    "type": "string",
    "format": "uuid"
   },
   "performanceId": {
    "type": "string",
    "format": "uuid"
   },
   "inventoryHoldId": {
    "type": "string",
    "nullable": true,
    "description": "Lease the units were drawn from. Absent for uncontended products."
   },
   "seatIds": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Seated products only. Not available offline."
   },
   "quantity": {
    "type": "integer",
    "minimum": 1
   },
   "quotedUnitPrice": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "description": "What the client charged, from its local bundle."
   },
   "holderName": {
    "type": "string",
    "nullable": true
   },
   "dataMaskValues": {
    "type": "object",
    "additionalProperties": true
   }
  }
 },
 "CreateOrderRequest": {
  "type": "object",
  "required": [
   "id",
   "venueId",
   "channel",
   "lines",
   "recordedAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$",
    "description": "Client-generated ULID. Also the idempotency key."
   },
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "channel": {
    "$ref": "#/components/schemas/Channel"
   },
   "shiftId": {
    "type": "string"
   },
   "subjectId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Null for an anonymous sale. Identity and entitlement are separate."
   },
   "guestLinkId": {
    "type": "string",
    "nullable": true,
    "description": "Present where the guest is linked across cells."
   },
   "catalogueBundleVersion": {
    "type": "string",
    "description": "The bundle the client priced from. Lets the server explain a variance rather than merely report one.\n"
   },
   "lines": {
    "type": "array",
    "minItems": 1,
    "items": {
     "$ref": "#/components/schemas/CreateOrderLine"
    }
   },
   "recordedAt": {
    "type": "string",
    "format": "date-time"
   }
  }
 },
 "CreateRefundRequest": {
  "type": "object",
  "required": [
   "id",
   "amount",
   "reason",
   "recordedAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
   },
   "lineIds": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Omit to refund the whole order."
   },
   "amount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "reason": {
    "type": "string",
    "minLength": 3,
    "maxLength": 500
   },
   "secondaryAuthorisation": {
    "type": "object",
    "description": "Required above the venue's `requiresSecondUserAbove`. A second user — cashier or supervisor — names themselves. This is dual-authorisation, not escalation.\n",
    "required": [
     "principalId",
     "credential"
    ],
    "properties": {
     "principalId": {
      "type": "string",
      "format": "uuid"
     },
     "credential": {
      "type": "string",
      "maxLength": 512
     }
    }
   },
   "refundToOriginalTender": {
    "type": "boolean",
    "default": true
   },
   "alternateTender": {
    "$ref": "#/components/schemas/TenderKind"
   },
   "recordedAt": {
    "type": "string",
    "format": "date-time"
   }
  }
 },
 "CreateReportRequest": {
  "x-ticvai-persistence": "none — request only",
  "type": "object",
  "required": [
   "name",
   "category",
   "dataSource",
   "columns",
   "requiredPermission"
  ],
  "properties": {
   "name": {
    "type": "string",
    "maxLength": 200
   },
   "description": {
    "type": "string",
    "maxLength": 1000
   },
   "category": {
    "$ref": "#/components/schemas/ReportCategory"
   },
   "dataSource": {
    "$ref": "#/components/schemas/DataSource"
   },
   "columns": {
    "type": "array",
    "minItems": 1,
    "items": {
     "$ref": "#/components/schemas/ReportColumn"
    }
   },
   "filters": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/ReportFilter"
    }
   },
   "groupBy": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "parameters": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/ReportParameter"
    }
   },
   "requiredPermission": {
    "type": "string",
    "description": "Permission needed to run this report. **The author cannot assign one they do not hold** — otherwise a venue user could build themselves a tenant-wide view.\n"
   },
   "maxDateRangeDays": {
    "type": "integer",
    "nullable": true,
    "description": "Guards against a query spanning years of scan events."
   }
  }
 },
 "DataSource": {
  "type": "string",
  "description": "What a report may be built over. **A closed set, and that is the point** — a builder that accepts any table will happily produce a report over data nobody maintains.\n**Eight sources added 18 August** (BL-143), each because the matrix asks for a report the builder could not source. `stockCounts` and `waste`: 6.1.21 wants count variance and `stockMovements` records the movement rather than **the count that found the discrepancy**. `workstations`, `devices` and `principals`: 6.1.28 — **who did what at which till** is the question an auditor asks first and it had no source. `loyalty`: 6.1.37, points earned, burned and expiring. `reviews`: 6.1.46. `queueEntries`: **wait times are already measured and nothing could report on them.**\n**Adding a source is a decision, not an omission.** `principals`, `guests`, `loyalty` and `reviews` all name a person, and `REPORT_EXPORT_PII` gates them.\n",
  "enum": [
   "orders",
   "orderLines",
   "payments",
   "refunds",
   "shifts",
   "scanEvents",
   "entitlements",
   "products",
   "inventory",
   "stockMovements",
   "stockCounts",
   "waste",
   "workstations",
   "devices",
   "principals",
   "loyalty",
   "reviews",
   "queueEntries",
   "guests",
   "campaigns",
   "cases",
   "ledgerEntries",
   "workOrders",
   "approvals",
   "purchaseOrders",
   "receipts",
   "requisitions",
   "stockBatches",
   "resourceBookings",
   "delegations",
   "forms",
   "challenges",
   "wallets",
   "resaleListings"
  ]
 },
 "DeliveryLocation": {
  "type": "object",
  "x-ticvai-persistence": "fnb.delivery_location",
  "required": [
   "id",
   "venueId",
   "kind",
   "label",
   "isServiceable"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "kind": {
    "$ref": "#/components/schemas/DeliveryLocationKind"
   },
   "label": {
    "type": "string",
    "description": "What a runner is told. \"Cabana 12\", \"Row H Seat 4\", \"Lawn — north gate\"."
   },
   "zone": {
    "type": "string",
    "nullable": true
   },
   "tableId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Set where the location is a restaurant table, so it shares table state."
   },
   "seatId": {
    "type": "string",
    "nullable": true,
    "description": "Set where the seat is the address. References the seat map."
   },
   "servingOutletIds": {
    "type": "array",
    "description": "Which outlets deliver here. A cabana served by the pool bar and not the restaurant is normal, and a location nothing serves is not an address.\n",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "isServiceable": {
    "type": "boolean",
    "description": "False where the location exists but is not currently taking delivery — closed section, weather, no runner on shift.\n"
   },
   "unserviceableReason": {
    "type": "string",
    "nullable": true
   },
   "walkTimeMinutes": {
    "type": "integer",
    "nullable": true,
    "description": "From the serving outlet. Feeds the guest's estimate — a cabana eight minutes away is not the same promise as a table by the kitchen.\n"
   }
  }
 },
 "DeliveryLocationKind": {
  "type": "string",
  "description": "4.6.26. One concept, because a runner needs one instruction.",
  "enum": [
   "table",
   "seat",
   "cabana",
   "sunbed",
   "poolside",
   "box",
   "suite",
   "lawn",
   "collectionPoint",
   "namedLocation"
  ]
 },
 "DenominationCount": {
  "type": "array",
  "description": "**A count is a list of lines and the line is the row.** Until 24 August this array carried the persistence hint itself, so `orders.cash_count_line` derived a single column — `shift_id` — and a count line had no denomination, no quantity and no variance.\n**The array is the transport; `CashCountLine` is the row.**\n",
  "items": {
   "$ref": "#/components/schemas/CashCountLine"
  },
  "minItems": 1
 },
 "DiningOutlet": {
  "type": "object",
  "x-ticvai-persistence": "none — projection over outlet, menu and table state",
  "required": [
   "outletId",
   "name",
   "kind",
   "isOpenNow",
   "orderingMethod"
  ],
  "properties": {
   "outletId": {
    "type": "string",
    "format": "uuid"
   },
   "name": {
    "type": "string"
   },
   "kind": {
    "type": "string"
   },
   "zone": {
    "type": "string",
    "nullable": true
   },
   "cuisine": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "isOpenNow": {
    "type": "boolean"
   },
   "opensAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "closesAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "orderingMethod": {
    "$ref": "#/components/schemas/GuestOrderingMethod"
   },
   "estimatedWaitMinutes": {
    "type": "integer",
    "nullable": true,
    "description": "From current kitchen ticket volume, not a fixed figure. Null where the outlet has no KDS reporting — an invented wait time is worse than none.\n"
   },
   "imageAssetRef": {
    "type": "string",
    "nullable": true
   },
   "menuId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   }
  }
 },
 "ExchangeOrderRequest": {
  "type": "object",
  "required": [
   "id",
   "outgoingLineIds",
   "incomingLines",
   "recordedAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
   },
   "outgoingLineIds": {
    "type": "array",
    "minItems": 1,
    "items": {
     "type": "string"
    }
   },
   "incomingLines": {
    "type": "array",
    "minItems": 1,
    "items": {
     "$ref": "#/components/schemas/CreateOrderLine"
    }
   },
   "waiveFee": {
    "type": "boolean",
    "default": false
   },
   "reason": {
    "type": "string",
    "maxLength": 500
   },
   "recordedAt": {
    "type": "string",
    "format": "date-time"
   }
  }
 },
 "FieldType": {
  "type": "string",
  "enum": [
   "string",
   "integer",
   "decimal",
   "money",
   "boolean",
   "date",
   "dateTime",
   "uuid",
   "enum"
  ]
 },
 "FinancialReport": {
  "x-ticvai-persistence": "none — computed from replica",
  "type": "object",
  "required": [
   "report",
   "fiscalPeriodId",
   "currency",
   "generatedAt",
   "sections"
  ],
  "properties": {
   "report": {
    "type": "string"
   },
   "fiscalPeriodId": {
    "type": "string",
    "format": "uuid"
   },
   "legalEntityId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "currency": {
    "type": "string",
    "pattern": "^[A-Z]{3}$"
   },
   "currencyScale": {
    "type": "integer"
   },
   "generatedAt": {
    "type": "string",
    "format": "date-time"
   },
   "sections": {
    "type": "array",
    "items": {
     "type": "object",
     "required": [
      "name",
      "lines",
      "total"
     ],
     "properties": {
      "name": {
       "type": "string"
      },
      "lines": {
       "type": "array",
       "items": {
        "type": "object",
        "properties": {
         "label": {
          "type": "string"
         },
         "accountCode": {
          "type": "string",
          "nullable": true
         },
         "amount": {
          "$ref": "../shared/common.yaml#/components/schemas/Money"
         },
         "priorPeriodAmount": {
          "$ref": "../shared/common.yaml#/components/schemas/Money"
         }
        }
       }
      },
      "total": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      }
     }
    }
   }
  }
 },
 "GuestOrderingMethod": {
  "x-ticvai-persistence": "none — enum",
  "type": "string",
  "description": "How a guest may order at this outlet. Varies within one venue, so it is per outlet rather than a venue setting.\n",
  "enum": [
   "tableService",
   "appToTable",
   "appToCollect",
   "counterOnly",
   "notAvailable"
  ]
 },
 "ManualDiscountRequest": {
  "type": "object",
  "x-ticvai-persistence": "none — request only",
  "required": [
   "id",
   "reason",
   "recordedAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
   },
   "lineId": {
    "type": "string",
    "nullable": true,
    "description": "Omit to discount the order rather than a line."
   },
   "amount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "percentage": {
    "type": "number",
    "minimum": 0,
    "maximum": 100
   },
   "reason": {
    "type": "string",
    "minLength": 3,
    "maxLength": 300,
    "description": "Required, and free text rather than a code list. A cashier forced to pick the nearest reason picks the first one, and the register stops meaning anything.\n"
   },
   "reasonCode": {
    "type": "string",
    "nullable": true,
    "description": "Optional alongside the free text, where the venue maintains a list."
   },
   "approverPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Required above the venue threshold. May not be the requester."
   },
   "recordedAt": {
    "type": "string",
    "format": "date-time"
   }
  }
 },
 "MerchandiseItem": {
  "x-ticvai-persistence": "retail.merchandise",
  "type": "object",
  "required": [
   "id",
   "sku",
   "name",
   "outletId",
   "variantId",
   "price",
   "onHand",
   "isActive"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "sku": {
    "type": "string"
   },
   "barcode": {
    "type": "string",
    "nullable": true
   },
   "name": {
    "type": "string"
   },
   "outletId": {
    "type": "string",
    "format": "uuid"
   },
   "categoryId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "variantId": {
    "type": "string",
    "format": "uuid",
    "description": "The catalogue variant sold. Price and tax come from there."
   },
   "inventoryItemId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The stock item depleted on sale. Null means the item sells but never runs out, which is almost always a configuration error.\n"
   },
   "price": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "onHand": {
    "type": "number"
   },
   "isReturnable": {
    "type": "boolean",
    "default": true
   },
   "returnWindowDays": {
    "type": "integer",
    "nullable": true
   },
   "requiresSerialNumber": {
    "type": "boolean",
    "default": false
   },
   "imageAssetRef": {
    "type": "string",
    "nullable": true
   },
   "isActive": {
    "type": "boolean"
   }
  }
 },
 "ModifyOrderRequest": {
  "type": "object",
  "required": [
   "id",
   "recordedAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
   },
   "addLines": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/CreateOrderLine"
    }
   },
   "removeLineIds": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "reason": {
    "type": "string",
    "maxLength": 500
   },
   "recordedAt": {
    "type": "string",
    "format": "date-time"
   }
  }
 },
 "NaturalLanguageAnswer": {
  "x-ticvai-persistence": "none — computed",
  "type": "object",
  "required": [
   "conversationId",
   "question",
   "interpretation",
   "result",
   "confidence"
  ],
  "properties": {
   "conversationId": {
    "type": "string"
   },
   "question": {
    "type": "string"
   },
   "interpretation": {
    "type": "string",
    "description": "What the question was understood to mean, in plain language."
   },
   "generatedQuery": {
    "type": "object",
    "description": "The structured query produced — data source, columns, filters, grouping. Returned so the answer can be checked. An answer nobody can verify is worse than no answer.\n",
    "properties": {
     "dataSource": {
      "$ref": "#/components/schemas/DataSource"
     },
     "columns": {
      "type": "array",
      "items": {
       "$ref": "#/components/schemas/ReportColumn"
      }
     },
     "filters": {
      "type": "array",
      "items": {
       "$ref": "#/components/schemas/ReportFilter"
      }
     },
     "groupBy": {
      "type": "array",
      "items": {
       "type": "string"
      }
     }
    }
   },
   "result": {
    "$ref": "#/components/schemas/ReportResult"
   },
   "confidence": {
    "type": "number",
    "minimum": 0,
    "maximum": 1
   },
   "suggestedFollowUps": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "modelVersion": {
    "type": "string"
   },
   "tokensUsed": {
    "type": "integer"
   }
  }
 },
 "NoSaleEvent": {
  "type": "object",
  "x-ticvai-persistence": "orders.no_sale_event",
  "required": [
   "id",
   "shiftId",
   "reason",
   "principalId",
   "recordedAt"
  ],
  "properties": {
   "id": {
    "type": "string"
   },
   "shiftId": {
    "type": "string"
   },
   "workstationId": {
    "type": "string",
    "format": "uuid"
   },
   "reason": {
    "type": "string"
   },
   "note": {
    "type": "string",
    "nullable": true
   },
   "principalId": {
    "type": "string",
    "format": "uuid"
   },
   "recordedAt": {
    "type": "string",
    "format": "date-time"
   },
   "countThisShift": {
    "type": "integer",
    "description": "Running count. Returned so the terminal can show it — a cashier who can see they are on their ninth no-sale behaves differently from one who cannot.\n"
   }
  }
 },
 "OpenShiftRequest": {
  "type": "object",
  "required": [
   "workstationId",
   "openingFloat"
  ],
  "properties": {
   "workstationId": {
    "type": "string",
    "format": "uuid"
   },
   "openingFloat": {
    "$ref": "#/components/schemas/DenominationCount"
   },
   "depositBoxCode": {
    "type": "string",
    "maxLength": 64,
    "description": "Physical container assigned to this shift. Required where the venue configures deposit box allocation.\n"
   },
   "bagNumber": {
    "type": "string",
    "maxLength": 64,
    "description": "Required where the venue configures bag numbers as mandatory."
   },
   "recordedAt": {
    "type": "string",
    "format": "date-time",
    "description": "When the device recorded it. Differs from server receipt time for shifts opened offline.\n"
   }
  }
 },
 "Order": {
  "x-ticvai-persistence": "orders.sales_order + orders.order_line",
  "type": "object",
  "required": [
   "id",
   "venueId",
   "scopePath",
   "channel",
   "status",
   "currency",
   "currencyScale",
   "grossAmount",
   "taxAmount",
   "netAmount",
   "lines",
   "createdAt",
   "recordedAt"
  ],
  "properties": {
   "id": {
    "type": "string"
   },
   "orderNumber": {
    "type": "string"
   },
   "channel": {
    "allOf": [
     {
      "$ref": "#/components/schemas/OrderChannel"
     }
    ],
    "description": "Where it came from. Drives revenue attribution, promotion eligibility and the self-service adoption figures the operator will ask for within a month of launch.\n"
   },
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "scopePath": {
    "type": "string"
   },
   "status": {
    "$ref": "#/components/schemas/OrderStatus"
   },
   "currency": {
    "type": "string",
    "pattern": "^[A-Z]{3}$",
    "x-ticvai-persisted": false,
    "description": "**Resolved from the region, not stored** (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and cannot be anything else. **Kept on the wire , removed from the table** — a client should not walk a hierarchy to read a figure, and the  database should not hold nine million copies of AED. Four tables genuinely differ from their\n region and keep a stored currency: `orders.payment.tender_currency`, `inventory.supplier`, \n`ledger.account`, `control.partner_agreement`.\n"
   },
   "currencyScale": {
    "type": "integer",
    "minimum": 0,
    "maximum": 4,
    "x-ticvai-persisted": false,
    "description": "**Resolved from the region, not stored** (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and cannot be anything else — storing it per ro w is a copy of a fact that cannot differ. **Kept on the wire, removed from the table**: a cl ient reading a figure should not walk a hierarchy to know what it means, and the database sh ould not hold nine million copies of AED. Four tables genuinely differ from their region and\n keep a stored currency — `orders.payment.tender_currency`, `inventory.supplier`, `ledger.ac\ncount`, `control.partner_agreement`. **A guest paying USD at an AED venue is a real row; a w orkstation with its own currency is a misconfiguration.**\n"
   },
   "grossAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "taxAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "netAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "refundedAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "totalPriceVariance": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "description": "Sum across lines. Zero on a normal order."
   },
   "lines": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/OrderLine"
    }
   },
   "payments": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/Payment"
    }
   },
   "principalId": {
    "type": "string",
    "format": "uuid"
   },
   "workstationId": {
    "type": "string",
    "format": "uuid"
   },
   "shiftId": {
    "type": "string",
    "nullable": true
   },
   "subjectId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "createdAt": {
    "type": "string",
    "format": "date-time"
   },
   "recordedAt": {
    "type": "string",
    "format": "date-time"
   },
   "syncedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   }
  }
 },
 "OrderChannel": {
  "type": "string",
  "description": "Where the order originated. Added when guest self-ordering was contracted — an order a guest placed on their own phone is commercially and operationally different from one a cashier typed, and reporting that cannot separate them cannot answer whether self-ordering is working.\n",
  "enum": [
   "pos",
   "kiosk",
   "guestApp",
   "guestWeb",
   "callCentre",
   "partner",
   "api",
   "backOffice"
  ]
 },
 "OrderExchangeResult": {
  "x-ticvai-persistence": "none — computed",
  "type": "object",
  "required": [
   "orderId",
   "outgoingValue",
   "incomingValue",
   "difference"
  ],
  "properties": {
   "orderId": {
    "type": "string"
   },
   "outgoingValue": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "incomingValue": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "exchangeFee": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "difference": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "description": "Only the difference settles. The replacement is held before the original is released, never the other way round.\n"
   },
   "newLineIds": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "revokedEntitlementIds": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "issuedEntitlementIds": {
    "type": "array",
    "items": {
     "type": "string"
    }
   }
  }
 },
 "OrderLine": {
  "x-ticvai-persistence": "orders.order_line",
  "allOf": [
   {
    "$ref": "#/components/schemas/CreateOrderLine"
   },
   {
    "type": "object",
    "required": [
     "serverUnitPrice",
     "taxAmount",
     "netAmount",
     "grossAmount"
    ],
    "properties": {
     "serverUnitPrice": {
      "allOf": [
       {
        "$ref": "../shared/common.yaml#/components/schemas/Money"
       }
      ],
      "description": "What the server computed on ingest."
     },
     "priceVariance": {
      "allOf": [
       {
        "$ref": "../shared/common.yaml#/components/schemas/Money"
       }
      ],
      "description": "Server minus quoted. Non-zero means the quoted price was honoured and the difference posted to the variance account.\n"
     },
     "taxAmount": {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     },
     "netAmount": {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     },
     "grossAmount": {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     },
     "entitlementIds": {
      "type": "array",
      "items": {
       "type": "string"
      }
     },
     "crossRegionRightIds": {
      "type": "array",
      "items": {
       "type": "string"
      },
      "description": "Redemption rights propagated to other cells for this line."
     }
    }
   }
  ]
 },
 "OrderModificationResult": {
  "x-ticvai-persistence": "none — computed",
  "type": "object",
  "required": [
   "order",
   "balanceDue"
  ],
  "properties": {
   "order": {
    "$ref": "#/components/schemas/Order"
   },
   "addedValue": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "removedValue": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "balanceDue": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "description": "Positive means the guest pays; negative means a refund is due."
   },
   "refundId": {
    "type": "string",
    "nullable": true
   },
   "revokedEntitlementIds": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "issuedEntitlementIds": {
    "type": "array",
    "items": {
     "type": "string"
    }
   }
  }
 },
 "OrderResumeResult": {
  "type": "object",
  "x-ticvai-persistence": "none — computed",
  "required": [
   "order",
   "hasChanged"
  ],
  "properties": {
   "order": {
    "$ref": "#/components/schemas/Order"
   },
   "hasChanged": {
    "type": "boolean",
    "description": "True where anything moved while the sale was parked. The cashier decides — silently charging the old price loses money, silently charging the new one loses the guest.\n"
   },
   "changes": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "kind": {
       "type": "string",
       "enum": [
        "priceChanged",
        "promotionExpired",
        "promotionNowApplies",
        "soldOut",
        "seatHoldExpired",
        "productWithdrawn"
       ]
      },
      "lineId": {
       "type": "string"
      },
      "detail": {
       "type": "string"
      },
      "wasAmount": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      },
      "nowAmount": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      }
     }
    }
   }
  }
 },
 "OrderStatement": {
  "x-ticvai-persistence": "none — computed from order, payment, refund and ledger",
  "type": "object",
  "required": [
   "orderId",
   "orderNumber",
   "currency",
   "entries",
   "currentBalance"
  ],
  "properties": {
   "orderId": {
    "type": "string"
   },
   "orderNumber": {
    "type": "string"
   },
   "currency": {
    "type": "string",
    "pattern": "^[A-Z]{3}$",
    "x-ticvai-persisted": false,
    "description": "**Resolved from the region, not stored** (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and cannot be anything else. **Kept on the wire , removed from the table** — a client should not walk a hierarchy to read a figure, and the  database should not hold nine million copies of AED. Four tables genuinely differ from their\n region and keep a stored currency: `orders.payment.tender_currency`, `inventory.supplier`, \n`ledger.account`, `control.partner_agreement`.\n"
   },
   "currencyScale": {
    "type": "integer",
    "x-ticvai-persisted": false,
    "description": "**Resolved from the region, not stored** (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and cannot be anything else — storing it per ro w is a copy of a fact that cannot differ. **Kept on the wire, removed from the table**: a cl ient reading a figure should not walk a hierarchy to know what it means, and the database sh ould not hold nine million copies of AED. Four tables genuinely differ from their region and\n keep a stored currency — `orders.payment.tender_currency`, `inventory.supplier`, `ledger.ac\ncount`, `control.partner_agreement`. **A guest paying USD at an AED venue is a real row; a w orkstation with its own currency is a misconfiguration.**\n"
   },
   "entries": {
    "type": "array",
    "description": "Sequential. What an agent reads to a guest asking about a charge.",
    "items": {
     "type": "object",
     "required": [
      "kind",
      "amount",
      "runningBalance",
      "occurredAt"
     ],
     "properties": {
      "kind": {
       "type": "string",
       "enum": [
        "sale",
        "payment",
        "refund",
        "void",
        "modification",
        "exchange",
        "fee",
        "variance",
        "chargeback"
       ]
      },
      "description": {
       "type": "string"
      },
      "amount": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      },
      "runningBalance": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      },
      "referenceId": {
       "type": "string",
       "nullable": true
      },
      "principalId": {
       "type": "string",
       "format": "uuid",
       "nullable": true
      },
      "occurredAt": {
       "type": "string",
       "format": "date-time"
      }
     }
    }
   },
   "totalPaid": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "totalRefunded": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "currentBalance": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "description": "Positive means the guest owes; negative means a refund is outstanding."
   }
  }
 },
 "OrderStatus": {
  "type": "string",
  "enum": [
   "pending",
   "held",
   "paid",
   "partiallyPaid",
   "completed",
   "voided",
   "refunded",
   "partiallyRefunded",
   "failed"
  ],
  "description": "`held` is a parked sale — the cashier freed the till and the guest will return. It holds no inventory and expires, because a till that accumulates parked sales across a shift cannot be closed.\n"
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
 "Payment": {
  "x-ticvai-persistence": "orders.payment",
  "type": "object",
  "required": [
   "id",
   "orderId",
   "tender",
   "amount",
   "status",
   "recordedAt"
  ],
  "properties": {
   "id": {
    "type": "string"
   },
   "orderId": {
    "type": "string"
   },
   "tender": {
    "$ref": "#/components/schemas/TenderKind"
   },
   "tenderCurrency": {
    "type": "string",
    "pattern": "^[A-Z]{3}$",
    "description": "4.6.11. **What the guest actually handed over**, which is not always what the venue books. A tourist paying USD cash at a till is a foreign tender; the sale is still recorded in base currency.\nEqual to the base currency for almost every payment. **Present on all of them so the foreign-tender report has a source** — `getForeignTenderReport` promised *what was taken in which currency* and nothing recorded it until 18 August.\n"
   },
   "tenderAmount": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "description": "The amount in `tenderCurrency`, at that currency's own scale."
   },
   "fxRate": {
    "type": "number",
    "nullable": true,
    "description": "The rate applied, **stored on the payment rather than looked up later** (CF-37). A payment reconciled next month is reconciled at the rate of the day it was taken.\n"
   },
   "fxRateSource": {
    "type": "string",
    "nullable": true,
    "enum": [
     "manual",
     "feed",
     "cardScheme"
    ],
    "description": "4.2.8. Manual or fed on a schedule. **`cardScheme` is where the terminal did the conversion and told us** — dynamic currency conversion, the scheme's rate rather than ours.\n"
   },
   "changeCurrency": {
    "type": "string",
    "pattern": "^[A-Z]{3}$",
    "nullable": true,
    "description": "4.6.11 is deliberately asymmetric: **accept foreign currency, refund in local.** A till giving change in five currencies needs five floats and five counts, and the variance becomes unattributable.\n"
   },
   "amount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "changeAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "status": {
    "type": "string",
    "enum": [
     "authorised",
     "captured",
     "pendingConfirmation",
     "declined",
     "failed",
     "voided",
     "refunded"
    ]
   },
   "providerName": {
    "type": "string",
    "nullable": true
   },
   "providerReference": {
    "type": "string",
    "nullable": true
   },
   "lastInquiryAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "recordedAt": {
    "type": "string",
    "format": "date-time"
   },
   "syncedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   }
  }
 },
 "PriceCheck": {
  "x-ticvai-persistence": "none — computed",
  "type": "object",
  "required": [
   "merchandiseId",
   "name",
   "listPrice",
   "effectivePrice",
   "onHand"
  ],
  "properties": {
   "merchandiseId": {
    "type": "string",
    "format": "uuid"
   },
   "sku": {
    "type": "string"
   },
   "name": {
    "type": "string"
   },
   "listPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "effectivePrice": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "description": "After any live promotion."
   },
   "appliedPromotionCode": {
    "type": "string",
    "nullable": true
   },
   "onHand": {
    "type": "number"
   },
   "isAvailable": {
    "type": "boolean"
   },
   "siblingOutlets": {
    "type": "array",
    "description": "Stock elsewhere in the venue, so a colleague can be sent.",
    "items": {
     "type": "object",
     "properties": {
      "outletId": {
       "type": "string",
       "format": "uuid"
      },
      "outletName": {
       "type": "string"
      },
      "onHand": {
       "type": "number"
      }
     }
    }
   }
  }
 },
 "Refund": {
  "x-ticvai-persistence": "orders.refund",
  "type": "object",
  "required": [
   "id",
   "orderId",
   "amount",
   "status",
   "createdAt"
  ],
  "properties": {
   "id": {
    "type": "string"
   },
   "orderId": {
    "type": "string"
   },
   "fxRate": {
    "type": "number",
    "nullable": true,
    "readOnly": true,
    "description": "**The rate on the original payment, not today's** (BL-087, CF-118).\n`Payment` records `tenderCurrency`, `fxRate` and `fxRateSource` at the moment of sale, so the sale rate is always retrievable. **Refunding at today's rate repays a different amount of money than was taken** — a guest who paid 100 USD at 3.67 and is refunded at 3.72 gets back more AED than they gave, and the venue carries the difference on every refund.\nThe exposure runs both ways and neither direction is defensible: a guest short-changed by a moving rate has a complaint the venue cannot answer, because **the guest did nothing but wait.**\n"
   },
   "taxReversalEntryId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true,
    "description": "**A refund reverses the tax entry it created, and this is where that is stated rather than implied.** `reverseJournalEntry` and `calculateTax` both exist, so both halves were present and the obligation was assumed — **an implied obligation is one a developer can miss without failing anything.**\nNull only where the original sale carried no tax.\n"
   },
   "settleTo": {
    "type": "string",
    "enum": [
     "originalTender",
     "advanceBalance",
     "wireTransfer",
     "storeCredit"
    ],
    "default": "originalTender",
    "description": "BL-086. **A refund could only go back the way it came.** A guest whose card has expired, a partner settling by wire, a guest who would rather have the credit — three real cases with one answer.\n**`originalTender` stays the default** because refunding elsewhere is how money laundering works, and anything else needs a reason.\n"
   },
   "fxVariance": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "description": "Where the sale rate and the current rate differ, **the difference is booked as an FX variance rather than hidden in the refund**. `runFxRevaluation` already handles this class of movement and this is the same act at a smaller scale.\n"
   },
   "amount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "appliedPercentage": {
    "type": "number",
    "description": "From the venue's time bands, or an approver override."
   },
   "status": {
    "type": "string",
    "enum": [
     "pendingApproval",
     "pendingGateway",
     "completed",
     "declined",
     "failed"
    ]
   },
   "reason": {
    "type": "string"
   },
   "requestedByPrincipalId": {
    "type": "string",
    "format": "uuid"
   },
   "secondaryPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "approvedByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "ledgerEntryId": {
    "type": "string",
    "nullable": true,
    "description": "Written before the gateway is called."
   },
   "gatewayReference": {
    "type": "string",
    "nullable": true
   },
   "createdAt": {
    "type": "string",
    "format": "date-time"
   },
   "completedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   }
  }
 },
 "RefundPolicy": {
  "x-ticvai-persistence": "orders.refund_policy",
  "type": "object",
  "description": "Venue-configured. Thresholds are policy, not permission scope — venues run different policies and the permission model should not encode commercial rules.\n",
  "required": [
   "venueId",
   "selfAuthoriseLimit",
   "requiresApprovalAbove"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "description": "**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"
   },
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "selfAuthoriseLimit": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "description": "Up to this, a holder of ORDER_REFUND refunds alone. Zero means every refund needs a second authoriser.\n"
   },
   "requiresSecondUserAbove": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "description": "Above this, a second user — cashier OR supervisor — names themselves as audit control. Dual-authorisation, not escalation (2.12.3).\n"
   },
   "requiresApprovalAbove": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "description": "Above this, an ORDER_REFUND_APPROVE holder must approve."
   },
   "timeBands": {
    "type": "array",
    "description": "Refundable percentage by time before the performance. Evaluated most-specific first.\n",
    "items": {
     "type": "object",
     "required": [
      "hoursBefore",
      "percentage"
     ],
     "properties": {
      "hoursBefore": {
       "type": "integer",
       "minimum": 0
      },
      "percentage": {
       "type": "number",
       "minimum": 0,
       "maximum": 100
      }
     }
    }
   },
   "allowPartial": {
    "type": "boolean",
    "default": true
   },
   "refundWindowDays": {
    "type": "integer",
    "nullable": true
   },
   "varianceThreshold": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "description": "Price variance above this is an exception requiring review rather than a routine posting (CF-38). Venue-configured.\n"
   }
  }
 },
 "ReportCategory": {
  "type": "string",
  "enum": [
   "sales",
   "admission",
   "financial",
   "inventory",
   "guest",
   "operations",
   "marketing",
   "workforce",
   "compliance",
   "custom"
  ]
 },
 "ReportColumn": {
  "x-ticvai-persistence": "reporting.report_column",
  "type": "object",
  "required": [
   "field"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "description": "**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"
   },
   "field": {
    "type": "string"
   },
   "label": {
    "type": "string"
   },
   "aggregation": {
    "allOf": [
     {
      "$ref": "#/components/schemas/Aggregation"
     }
    ],
    "default": "none"
   },
   "sortOrder": {
    "type": "integer"
   },
   "sortDirection": {
    "type": "string",
    "enum": [
     "asc",
     "desc"
    ]
   },
   "format": {
    "type": "string",
    "nullable": true
   }
  }
 },
 "ReportDefinition": {
  "x-ticvai-persistence": "reporting.report_definition + reporting.report_column + reporting.report_filter",
  "allOf": [
   {
    "$ref": "#/components/schemas/CreateReportRequest"
   },
   {
    "type": "object",
    "required": [
     "id",
     "version",
     "isSystem",
     "isRetired",
     "createdAt"
    ],
    "properties": {
     "id": {
      "type": "string",
      "format": "uuid"
     },
     "version": {
      "type": "string"
     },
     "isSystem": {
      "type": "boolean",
      "description": "Shipped with the platform. Cannot be amended, only cloned."
     },
     "isRetired": {
      "type": "boolean"
     },
     "estimatedCost": {
      "type": "string",
      "enum": [
       "low",
       "medium",
       "high"
      ],
      "description": "Informs whether it may run inline or must be queued."
     },
     "createdByPrincipalId": {
      "type": "string",
      "format": "uuid",
      "nullable": true
     },
     "createdAt": {
      "type": "string",
      "format": "date-time"
     },
     "lastRunAt": {
      "type": "string",
      "format": "date-time",
      "nullable": true
     },
     "scopePath": {
      "type": "string",
      "description": "**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `venue` scope.**"
     }
    }
   }
  ]
 },
 "ReportFilter": {
  "x-ticvai-persistence": "reporting.report_filter",
  "type": "object",
  "required": [
   "field",
   "operator"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "description": "**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"
   },
   "field": {
    "type": "string"
   },
   "operator": {
    "type": "string",
    "enum": [
     "equals",
     "notEquals",
     "greaterThan",
     "lessThan",
     "between",
     "in",
     "notIn",
     "contains",
     "isNull",
     "isNotNull"
    ]
   },
   "value": {},
   "values": {
    "type": "array",
    "items": {}
   },
   "isParameter": {
    "type": "boolean",
    "default": false,
    "description": "Prompted at run time rather than fixed. Parameters narrow the result; they never widen scope.\n"
   }
  }
 },
 "ReportParameter": {
  "x-ticvai-persistence": "reporting.report_parameter",
  "type": "object",
  "required": [
   "key",
   "label",
   "type",
   "isRequired"
  ],
  "properties": {
   "key": {
    "type": "string"
   },
   "label": {
    "type": "string"
   },
   "type": {
    "$ref": "#/components/schemas/FieldType"
   },
   "isRequired": {
    "type": "boolean"
   },
   "defaultValue": {}
  }
 },
 "ReportResult": {
  "x-ticvai-persistence": "none — result set, cached in object storage",
  "type": "object",
  "required": [
   "executionId",
   "columns",
   "rows"
  ],
  "properties": {
   "executionId": {
    "type": "string"
   },
   "columns": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "key": {
       "type": "string"
      },
      "label": {
       "type": "string"
      },
      "type": {
       "$ref": "#/components/schemas/FieldType"
      }
     }
    }
   },
   "rows": {
    "type": "array",
    "items": {
     "type": "object",
     "additionalProperties": true
    }
   },
   "totals": {
    "type": "object",
    "additionalProperties": true
   },
   "rowCount": {
    "type": "integer"
   },
   "nextCursor": {
    "type": "string",
    "nullable": true
   },
   "generatedAt": {
    "type": "string",
    "format": "date-time"
   },
   "dataAsOf": {
    "type": "string",
    "format": "date-time",
    "description": "Replica position the result was read at. Reporting reads a lag-tolerant replica, so this may trail the primary by seconds — stating it prevents an argument about a figure that moved.\n"
   }
  }
 },
 "RunReportRequest": {
  "x-ticvai-persistence": "none — request only",
  "type": "object",
  "properties": {
   "parameters": {
    "type": "object",
    "additionalProperties": true
   },
   "venueId": {
    "type": "string",
    "format": "uuid",
    "description": "Narrows to one venue. Omitting it returns everything the caller's scope permits — it cannot be used to reach beyond that.\n"
   },
   "dateFrom": {
    "type": "string",
    "format": "date"
   },
   "dateTo": {
    "type": "string",
    "format": "date"
   },
   "forceAsync": {
    "type": "boolean",
    "default": false,
    "description": "Queue regardless of size, for a result to be collected later."
   }
  }
 },
 "Settlement": {
  "x-ticvai-persistence": "ledger.settlement",
  "type": "object",
  "required": [
   "id",
   "providerName",
   "periodStart",
   "periodEnd",
   "status",
   "ingestedAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "providerName": {
    "type": "string"
   },
   "periodStart": {
    "type": "string",
    "format": "date"
   },
   "periodEnd": {
    "type": "string",
    "format": "date"
   },
   "status": {
    "$ref": "#/components/schemas/SettlementStatus"
   },
   "lineCount": {
    "type": "integer"
   },
   "matchedCount": {
    "type": "integer"
   },
   "exceptionCount": {
    "type": "integer"
   },
   "providerGross": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "providerFees": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "providerNet": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "ledgerGross": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "difference": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "ingestedAt": {
    "type": "string",
    "format": "date-time"
   },
   "completedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "scopePath": {
    "type": "string",
    "description": "**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `region` scope.**"
   }
  }
 },
 "SettlementException": {
  "x-ticvai-persistence": "ledger.settlement_exception",
  "type": "object",
  "required": [
   "id",
   "settlementId",
   "kind",
   "providerReference",
   "amount"
  ],
  "properties": {
   "id": {
    "type": "string"
   },
   "settlementId": {
    "type": "string",
    "format": "uuid"
   },
   "kind": {
    "type": "string",
    "enum": [
     "unmatchedInProvider",
     "unmatchedInLedger",
     "amountMismatch",
     "duplicateInProvider",
     "feeUnexplained"
    ]
   },
   "providerReference": {
    "type": "string",
    "nullable": true
   },
   "paymentId": {
    "type": "string",
    "nullable": true
   },
   "amount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "expectedAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "resolution": {
    "type": "string",
    "nullable": true
   },
   "resolvedByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "resolvedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   }
  }
 },
 "SettlementStatus": {
  "type": "string",
  "enum": [
   "ingesting",
   "parsing",
   "matching",
   "matched",
   "hasExceptions",
   "resolved",
   "failed"
  ]
 },
 "Shift": {
  "x-ticvai-persistence": "orders.shift",
  "type": "object",
  "required": [
   "id",
   "workstationId",
   "venueId",
   "scopePath",
   "principalId",
   "status",
   "currency",
   "currencyScale",
   "openedAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$",
    "description": "Client-generated ULID. Also the idempotency key."
   },
   "workstationId": {
    "type": "string",
    "format": "uuid"
   },
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "scopePath": {
    "type": "string"
   },
   "principalId": {
    "type": "string",
    "format": "uuid",
    "description": "Who opened it. Cash reconciles to a person and a drawer."
   },
   "principalDisplayName": {
    "type": "string"
   },
   "incidents": {
    "type": "array",
    "description": "BL-097. **A till has exceptions and there was nowhere to write them** — a no-sale, a drawer opened without a transaction, a manager override, a guest dispute.\n**This is the log a cash-up investigation starts from**, and a shift that balances with four unexplained no-sales is not a shift that balanced.\n",
    "items": {
     "type": "object",
     "properties": {
      "kind": {
       "type": "string",
       "enum": [
        "noSale",
        "drawerOpen",
        "override",
        "voidAfterPayment",
        "guestDispute",
        "tillJam",
        "priceQuery",
        "other"
       ]
      },
      "at": {
       "type": "string",
       "format": "date-time"
      },
      "principalId": {
       "type": "string",
       "format": "uuid"
      },
      "note": {
       "type": "string",
       "nullable": true
      }
     }
    }
   },
   "status": {
    "$ref": "#/components/schemas/ShiftStatus"
   },
   "currency": {
    "type": "string",
    "pattern": "^[A-Z]{3}$",
    "x-ticvai-persisted": false,
    "description": "**Resolved from the region, not stored** (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and cannot be anything else. **Kept on the wire , removed from the table** — a client should not walk a hierarchy to read a figure, and the  database should not hold nine million copies of AED. Four tables genuinely differ from their\n region and keep a stored currency: `orders.payment.tender_currency`, `inventory.supplier`, \n`ledger.account`, `control.partner_agreement`.\n"
   },
   "currencyScale": {
    "type": "integer",
    "minimum": 0,
    "maximum": 4,
    "x-ticvai-persisted": false,
    "description": "**Resolved from the region, not stored** (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and cannot be anything else — storing it per ro w is a copy of a fact that cannot differ. **Kept on the wire, removed from the table**: a cl ient reading a figure should not walk a hierarchy to know what it means, and the database sh ould not hold nine million copies of AED. Four tables genuinely differ from their region and\n keep a stored currency — `orders.payment.tender_currency`, `inventory.supplier`, `ledger.ac\ncount`, `control.partner_agreement`. **A guest paying USD at an AED venue is a real row; a w orkstation with its own currency is a misconfiguration.**\n"
   },
   "depositBoxCode": {
    "type": "string",
    "nullable": true
   },
   "bagNumber": {
    "type": "string",
    "nullable": true
   },
   "openingFloat": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "salesTotal": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "refundsTotal": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "liftsTotal": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "heldLeaseCount": {
    "type": "integer",
    "description": "Inventory leases currently held by this workstation. Surfaced so an operator closing a shift can see what will be returned.\n"
   },
   "openedAt": {
    "type": "string",
    "format": "date-time"
   },
   "recordedAt": {
    "type": "string",
    "format": "date-time",
    "description": "When the device recorded the open. Differs from `openedAt` when offline."
   },
   "suspendedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "closedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "syncedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "description": "Null while the shift has unsynced operations."
   },
   "approvals": {
    "type": "array",
    "items": {
     "type": "object",
     "required": [
      "kind",
      "principalId",
      "at"
     ],
     "properties": {
      "kind": {
       "type": "string",
       "enum": [
        "open",
        "close",
        "variance"
       ]
      },
      "principalId": {
       "type": "string",
       "format": "uuid"
      },
      "at": {
       "type": "string",
       "format": "date-time"
      },
      "reason": {
       "type": "string"
      }
     }
    }
   }
  }
 },
 "ShiftCloseResult": {
  "x-ticvai-persistence": "none — computed",
  "type": "object",
  "required": [
   "shift",
   "expectedCash",
   "countedCash",
   "variance",
   "requiresAcceptance"
  ],
  "properties": {
   "shift": {
    "$ref": "#/components/schemas/Shift"
   },
   "expectedCash": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "countedCash": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "variance": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "description": "Counted minus expected. Negative is short."
   },
   "requiresAcceptance": {
    "type": "boolean",
    "description": "True when the variance exceeds the configured threshold."
   },
   "nonCashVariances": {
    "type": "array",
    "items": {
     "type": "object",
     "required": [
      "tender",
      "declared",
      "captured",
      "variance"
     ],
     "properties": {
      "tender": {
       "type": "string"
      },
      "declared": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      },
      "captured": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      },
      "variance": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      }
     }
    }
   }
  }
 },
 "ShiftStatus": {
  "type": "string",
  "enum": [
   "pendingApproval",
   "open",
   "suspended",
   "pendingVariance",
   "pendingClosure",
   "closed",
   "autoClosed"
  ]
 },
 "TenderKind": {
  "type": "string",
  "enum": [
   "cash",
   "card",
   "wallet",
   "voucher",
   "bankTransfer",
   "hotelCharge",
   "installment",
   "giftCard",
   "complimentary"
  ]
 },
 "TrialBalance": {
  "x-ticvai-persistence": "none — computed",
  "type": "object",
  "required": [
   "fiscalPeriodId",
   "isBalanced",
   "totalDebit",
   "totalCredit",
   "accounts"
  ],
  "properties": {
   "fiscalPeriodId": {
    "type": "string",
    "format": "uuid"
   },
   "isBalanced": {
    "type": "boolean",
    "description": "False indicates a defect, not a business condition. Double-entry cannot be unbalanced by legitimate activity.\n"
   },
   "totalDebit": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "totalCredit": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "accounts": {
    "type": "array",
    "items": {
     "type": "object",
     "required": [
      "accountId",
      "accountCode",
      "accountName",
      "debit",
      "credit",
      "balance"
     ],
     "properties": {
      "accountId": {
       "type": "string",
       "format": "uuid"
      },
      "accountCode": {
       "type": "string"
      },
      "accountName": {
       "type": "string"
      },
      "type": {
       "$ref": "#/components/schemas/AccountType"
      },
      "debit": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      },
      "credit": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      },
      "balance": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      }
     }
    }
   }
  }
 }
}
```
