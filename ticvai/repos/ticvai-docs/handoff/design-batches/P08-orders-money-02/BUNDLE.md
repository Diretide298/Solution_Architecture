# P08-orders-money-02 — P08 · Orders & Money (2 of 3)

**10 screens · 60 operations · 63 schemas · 29 permissions**

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

- **Every control that can be refused must be gated.** 29 permissions apply here:
  `CASH_LIFT, CASH_NO_SALE, LEDGER_VIEW, ORDER_CREATE, ORDER_DISCOUNT, ORDER_EXCHANGE, ORDER_MODIFY, ORDER_REFUND, ORDER_REPRINT, ORDER_RESCHEDULE, ORDER_VIEW, ORDER_VOID`…. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `BO-040` | Variance Approval | approvalInbox | 13 | 9 | — |
| `BO-041` | Cash Movements | approvalInbox | 5 | 2 | — |
| `BO-042` | Banking & Safe | approvalInbox | 5 | 1 | — |
| `BO-043` | Daily Reconciliation | listDetail | 7 | 2 | — |
| `BO-047` | Order Corrections & Exceptions | listDetail | 14 | 9 | — |
| `BO-048` | Retail Products | listDetail | 4 | 2 | — |
| `BO-059` | Sales Reports | listDetail | 9 | 6 | — |
| `BO-061` | Scheduled Reports | listDetail | 5 | 3 | — |
| `BO-062` | Venue Profile | listDetail | 4 | 1 | — |
| `BO-065` | Venue Configuration | listDetail | 6 | 2 | — |

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
    "BO-008",
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
     "to": "BO-008",
     "trigger": "Product Detail & Variants",
     "provenance": "derived — BO-008 declares entryState.params productId, variantId, version and BO-040 holds none of them, so the edge carries nothing and BO-008 opens cold"
    }
   ]
  },
  "notes": "Definition derived from the wireframe board on 14 August. CF-53 — 67 of these 73 had no definition at all. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual.",
  "density": "compact",
  "pattern": "approvalInbox",
  "patternReason": "`approveShiftOpen` decides items that `listShifts` queues — every row is waiting for a person, so the empty state is success",
  "purpose": "Accept or refuse a till that did not balance.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "queue",
     "components": [
      {
       "kind": "textField",
       "label": "Workstation id",
       "operation": "listShifts",
       "notes": "Sends `?workstationId=` to `listShifts`.",
       "provenance": "contract shift.yaml GET /shifts"
      },
      {
       "kind": "textField",
       "label": "Status",
       "operation": "listShifts",
       "notes": "Sends `?status=` to `listShifts`.",
       "provenance": "contract shift.yaml GET /shifts"
      },
      {
       "kind": "datePicker",
       "label": "Opened from",
       "operation": "listShifts",
       "notes": "Sends `?openedFrom=` to `listShifts`.",
       "provenance": "contract shift.yaml GET /shifts"
      },
      {
       "kind": "datePicker",
       "label": "Opened to",
       "operation": "listShifts",
       "notes": "Sends `?openedTo=` to `listShifts`.",
       "provenance": "contract shift.yaml GET /shifts"
      },
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
      },
      {
       "kind": "dataTable",
       "label": "Every cash movement",
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
        "CashMovement.depositBoxId",
        "CashMovement.witnessPrincipalId",
        "CashMovement.withdrawalReason",
        "CashMovement.authorisedByPrincipalId"
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
       "label": "The selected shift",
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
      },
      {
       "kind": "detailPanel",
       "label": "The shift",
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
       "operation": "getShift",
       "provenance": "contract shift.yaml GET /shifts/{shiftId}"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "decision",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Accept shift variance",
       "operation": "acceptShiftVariance",
       "provenance": "contract shift.yaml POST /shifts/{shiftId}/accept-variance"
      },
      {
       "kind": "secondaryButton",
       "label": "Approve shift open",
       "operation": "approveShiftOpen",
       "provenance": "contract shift.yaml POST /shifts/{shiftId}/approve-open"
      },
      {
       "kind": "destructiveButton",
       "label": "Close shift",
       "operation": "closeShift",
       "provenance": "contract shift.yaml POST /shifts/{shiftId}/close"
      },
      {
       "kind": "secondaryButton",
       "label": "Create cash movement",
       "operation": "createCashMovement",
       "provenance": "contract shift.yaml POST /shifts/{shiftId}/cash-movements"
      },
      {
       "kind": "secondaryButton",
       "label": "Open shift",
       "operation": "openShift",
       "provenance": "contract shift.yaml POST /shifts"
      },
      {
       "kind": "secondaryButton",
       "label": "Record no sale",
       "operation": "recordNoSale",
       "provenance": "contract shift.yaml POST /shifts/{shiftId}/no-sale"
      },
      {
       "kind": "secondaryButton",
       "label": "Reopen shift",
       "operation": "reopenShift",
       "provenance": "contract shift.yaml POST /shifts/{shiftId}/reopen"
      },
      {
       "kind": "secondaryButton",
       "label": "Resume shift",
       "operation": "resumeShift",
       "provenance": "contract shift.yaml POST /shifts/{shiftId}/resume"
      },
      {
       "kind": "destructiveButton",
       "label": "Suspend shift",
       "operation": "suspendShift",
       "provenance": "contract shift.yaml POST /shifts/{shiftId}/suspend"
      }
     ]
    }
   ]
  },
  "overlays": [
   {
    "id": "confirmCloseShift",
    "component": "confirmDialog",
    "trigger": "Close shift",
    "body": "**Names what `closeShift` changes and what it leaves alone**, in the consequence rather than the verb. A variance approval this affects should be identified in the dialog, not just counted. **Collects what `closeShift` sends before it is called.** Required: `countedCash`, `recordedAt`. Optional: `nonCashDeclared`, `notes`, `releaseHeldLeases`.",
    "provenance": "contract shift.yaml POST /shifts/{shiftId}/close",
    "bindsTo": "CloseShiftRequest"
   },
   {
    "id": "confirmSuspendShift",
    "component": "confirmDialog",
    "trigger": "Suspend shift",
    "body": "**Names what `suspendShift` changes and what it leaves alone**, in the consequence rather than the verb. A variance approval this affects should be identified in the dialog, not just counted. **Collects what `suspendShift` sends before it is called.** Required: `recordedAt`. Optional: `reason`.",
    "provenance": "contract shift.yaml POST /shifts/{shiftId}/suspend"
   },
   {
    "id": "formAcceptShiftVariance",
    "component": "modal",
    "trigger": "Accept shift variance",
    "body": "**Collects what `acceptShiftVariance` sends before it is called.** Required: `reason`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Accept shift variance",
     "operation": "acceptShiftVariance"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "reason"
     ]
    },
    "provenance": "contract shift.yaml POST /shifts/{shiftId}/accept-variance"
   },
   {
    "id": "formApproveShiftOpen",
    "component": "modal",
    "trigger": "Approve shift open",
    "body": "**Collects what `approveShiftOpen` sends before it is called.** Required: `reason`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Approve shift open",
     "operation": "approveShiftOpen"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "reason"
     ]
    },
    "provenance": "contract shift.yaml POST /shifts/{shiftId}/approve-open"
   },
   {
    "id": "formCreateCashMovement",
    "component": "modal",
    "trigger": "Create cash movement",
    "body": "**Collects what `createCashMovement` sends before it is called.** Required: `id`, `kind`, `amount`, `recordedAt`. Optional: `denominations`, `reference`, `reason`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "CreateCashMovementRequest",
    "confirm": {
     "label": "Create cash movement",
     "operation": "createCashMovement"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "kind",
      "amount",
      "recordedAt",
      "denominations",
      "reference",
      "reason"
     ]
    },
    "provenance": "contract shift.yaml POST /shifts/{shiftId}/cash-movements"
   },
   {
    "id": "formOpenShift",
    "component": "modal",
    "trigger": "Open shift",
    "body": "**Collects what `openShift` sends before it is called.** Required: `workstationId`, `openingFloat`. Optional: `depositBoxCode`, `bagNumber`, `recordedAt`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "OpenShiftRequest",
    "confirm": {
     "label": "Open shift",
     "operation": "openShift"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "workstationId",
      "openingFloat",
      "depositBoxCode",
      "bagNumber",
      "recordedAt"
     ]
    },
    "provenance": "contract shift.yaml POST /shifts"
   },
   {
    "id": "formRecordNoSale",
    "component": "modal",
    "trigger": "Record no sale",
    "body": "**Collects what `recordNoSale` sends before it is called.** Required: `id`, `reason`, `recordedAt`. Optional: `note`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Record no sale",
     "operation": "recordNoSale"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "reason",
      "recordedAt",
      "note"
     ]
    },
    "provenance": "contract shift.yaml POST /shifts/{shiftId}/no-sale"
   },
   {
    "id": "formReopenShift",
    "component": "modal",
    "trigger": "Reopen shift",
    "body": "**Collects what `reopenShift` sends before it is called.** Required: `reason` and `supervisorStepUp` — a supervisor who did not close the shift enters their staff PIN on this device (`principalId`, `credential`) (decided 28 September, audit R144). A refusal names which: the supervisor is the closer (403 approver-is-closer) or the PIN was refused (403 supervisor-step-up-refused). Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Reopen shift",
     "operation": "reopenShift"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "reason",
      "supervisorStepUp"
     ]
    },
    "provenance": "contract shift.yaml POST /shifts/{shiftId}/reopen"
   },
   {
    "id": "formResumeShift",
    "component": "modal",
    "trigger": "Resume shift",
    "body": "**Collects what `resumeShift` sends before it is called.** Required: `recordedAt`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Resume shift",
     "operation": "resumeShift"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "recordedAt"
     ]
    },
    "provenance": "contract shift.yaml POST /shifts/{shiftId}/resume"
   }
  ],
  "states": {
   "loading": "The variance approval list.",
   "error": "Could not load. Names which read failed and leaves the variance approval untouched.",
   "emptyFirstRun": "**Nothing is waiting, which is the good outcome.** An empty queue means every item has been decided; it offers no create action, because creating work is not what it needs.",
   "emptyNoResults": "Nothing matches the filter on workstationId, status, openedFrom, openedTo and the variance approval are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Shown when the caller lacks `REPORT_VIEW_WORKSTATION`, which `listShifts` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
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
    "BO-008"
   ],
   "inferred": true,
   "transitions": [
    {
     "to": "BO-008",
     "trigger": "Product Detail & Variants",
     "provenance": "derived — BO-008 declares entryState.params productId, variantId, version and BO-041 holds none of them, so the edge carries nothing and BO-008 opens cold"
    }
   ]
  },
  "notes": "Definition derived from the wireframe board on 14 August. CF-53 — 67 of these 73 had no definition at all. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual. **Kept separate from BO-042, each with its own operations (decided 28 September, audit R276)** — the two carried the same thirteen shift operations. This screen keeps cash lifts, adds and no-sales (`listCashMovements`, `createCashMovement`, `recordNoSale`) with the shift they belong to; opening, suspending, closing and reopening shifts stay on BO-039 and BO-040, and banking and safe drops are BO-042.",
  "density": "compact",
  "pattern": "approvalInbox",
  "patternReason": "`listCashMovements` queues a shift's lifts, adds and no-sales for review; the reviewer records a correcting lift or add with `createCashMovement` — every row is looked at, so the empty state is success",
  "purpose": "Track money in and out of a drawer that is not a sale.",
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
      },
      {
       "kind": "dataTable",
       "label": "Every shift",
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
       "label": "The selected cash movement",
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
        "CashMovement.depositBoxId",
        "CashMovement.witnessPrincipalId",
        "CashMovement.withdrawalReason",
        "CashMovement.authorisedByPrincipalId",
        "CashMovement.sequence",
        "CashMovement.syncedAt"
       ],
       "operation": "listCashMovements",
       "provenance": "contract shift.yaml GET /shifts/{shiftId}/cash-movements"
      },
      {
       "kind": "detailPanel",
       "label": "The shift",
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
       "operation": "getShift",
       "provenance": "contract shift.yaml GET /shifts/{shiftId}"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "decision",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Create cash movement",
       "operation": "createCashMovement",
       "provenance": "contract shift.yaml POST /shifts/{shiftId}/cash-movements"
      },
      {
       "kind": "secondaryButton",
       "label": "Record no sale",
       "operation": "recordNoSale",
       "provenance": "contract shift.yaml POST /shifts/{shiftId}/no-sale"
      }
     ]
    }
   ]
  },
  "overlays": [
   {
    "id": "formCreateCashMovement",
    "component": "modal",
    "trigger": "Create cash movement",
    "body": "**Collects what `createCashMovement` sends before it is called.** Required: `id`, `kind`, `amount`, `recordedAt`. Optional: `denominations`, `reference`, `reason`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "CreateCashMovementRequest",
    "confirm": {
     "label": "Create cash movement",
     "operation": "createCashMovement"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "kind",
      "amount",
      "recordedAt",
      "denominations",
      "reference",
      "reason"
     ]
    },
    "provenance": "contract shift.yaml POST /shifts/{shiftId}/cash-movements"
   },
   {
    "id": "formRecordNoSale",
    "component": "modal",
    "trigger": "Record no sale",
    "body": "**Collects what `recordNoSale` sends before it is called.** Required: `id`, `reason`, `recordedAt`. Optional: `note`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Record no sale",
     "operation": "recordNoSale"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "reason",
      "recordedAt",
      "note"
     ]
    },
    "provenance": "contract shift.yaml POST /shifts/{shiftId}/no-sale"
   }
  ],
  "states": {
   "loading": "The cash movements list.",
   "error": "Could not load. Names which read failed and leaves the cash movements untouched.",
   "emptyFirstRun": "**Nothing is waiting, which is the good outcome.** An empty queue means every item has been decided; it offers no create action, because creating work is not what it needs.",
   "emptyNoResults": "Never shown: `listCashMovements` takes no filter, so an empty list is always the first-run state above.",
   "emptyNoAccess": "Shown when the caller lacks `REPORT_VIEW_WORKSTATION`, which `listCashMovements` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
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
    "operationId": "recordNoSale",
    "contract": "shift",
    "purpose": "Open the drawer without a sale",
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
    "CashMovement.id",
    "CashMovement.kind",
    "CashMovement.amount",
    "CashMovement.denominations",
    "CashMovement.reference"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-041"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 13 operations this screen declares (5 after the 28 September split from BO-042, audit R276), not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
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
    "BO-008"
   ],
   "inferred": true,
   "transitions": [
    {
     "to": "BO-008",
     "trigger": "Product Detail & Variants",
     "provenance": "derived — BO-008 declares entryState.params productId, variantId, version and BO-042 holds none of them, so the edge carries nothing and BO-008 opens cold"
    }
   ]
  },
  "notes": "Definition derived from the wireframe board on 14 August. CF-53 — 67 of these 73 had no definition at all. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual. **Kept separate from BO-041, each with its own operations (decided 28 September, audit R276)** — the two carried the same thirteen shift operations. This screen moves cash out of the tills — `listDepositBoxes` and `withdrawFromDepositBox` with reason banking or safeDrop — and reads the lifts that result; cash lifts and adds at a till are BO-041, and the shift lifecycle stays on BO-039 and BO-040.",
  "density": "compact",
  "pattern": "approvalInbox",
  "patternReason": "`listDepositBoxes` queues the boxes holding cash; a supervisor takes cash out of each for banking or the safe with `withdrawFromDepositBox` — every open box is waiting for a person, so the empty state is success",
  "purpose": "Move the day’s cash out of the tills.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "queue",
     "components": [
      {
       "kind": "dataTable",
       "label": "Deposit boxes holding cash",
       "bindsTo": "DepositBox",
       "columns": [
        "DepositBox.cashierName",
        "DepositBox.workstationId",
        "DepositBox.shiftId",
        "DepositBox.status",
        "DepositBox.openingFloat",
        "DepositBox.withdrawnTotal"
       ],
       "operation": "listDepositBoxes",
       "notes": "Sends `?openOnly=true` to `listDepositBoxes`. A box being counted (`closing`, `closed`, `reconciled`) takes nothing out and is shown without the action.",
       "provenance": "contract shift.yaml GET /deposit-boxes"
      },
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
      },
      {
       "kind": "dataTable",
       "label": "Every shift",
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
       "label": "The selected cash movement",
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
        "CashMovement.depositBoxId",
        "CashMovement.witnessPrincipalId",
        "CashMovement.withdrawalReason",
        "CashMovement.authorisedByPrincipalId",
        "CashMovement.sequence",
        "CashMovement.syncedAt"
       ],
       "operation": "listCashMovements",
       "provenance": "contract shift.yaml GET /shifts/{shiftId}/cash-movements"
      },
      {
       "kind": "detailPanel",
       "label": "The shift",
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
       "operation": "getShift",
       "provenance": "contract shift.yaml GET /shifts/{shiftId}"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "decision",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Bank or safe-drop cash",
       "operation": "withdrawFromDepositBox",
       "provenance": "contract shift.yaml POST /deposit-boxes/{boxId}/withdraw"
      }
     ]
    }
   ]
  },
  "overlays": [
   {
    "id": "formWithdrawFromDepositBox",
    "component": "modal",
    "trigger": "Bank or safe-drop cash",
    "body": "**Collects what `withdrawFromDepositBox` sends before it is called.** Required: `id`, `amount`, `witnessPrincipalId` (the cashier the cash came from), `recordedAt`. Optional: `reason` (banking, safeDrop, changeOrder, other), `note`. The lift reduces the box's expected close figure, so it is never a variance. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Bank or safe-drop cash",
     "operation": "withdrawFromDepositBox"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "amount",
      "witnessPrincipalId",
      "reason",
      "note",
      "recordedAt"
     ]
    },
    "provenance": "contract shift.yaml POST /deposit-boxes/{boxId}/withdraw"
   }
  ],
  "states": {
   "loading": "The banking safe list.",
   "error": "Could not load. Names which read failed and leaves the banking safe untouched.",
   "emptyFirstRun": "**Nothing is waiting, which is the good outcome.** An empty queue means every item has been decided; it offers no create action, because creating work is not what it needs.",
   "emptyNoResults": "Never shown: `listCashMovements` takes no filter, so an empty list is always the first-run state above.",
   "emptyNoAccess": "Shown when the caller lacks `REPORT_VIEW_WORKSTATION`, which `listCashMovements` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listDepositBoxes",
    "contract": "shift",
    "purpose": "Cash boxes and who holds them — the cash to move out of the tills (audit R276)",
    "trigger": "onLoad"
   },
   {
    "operationId": "withdrawFromDepositBox",
    "contract": "shift",
    "purpose": "Take cash out of a box for banking or the safe",
    "trigger": "onAction",
    "invalidates": [
     "listDepositBoxes",
     "listCashMovements"
    ]
   },
   {
    "operationId": "listCashMovements",
    "contract": "shift",
    "purpose": "Lifts, adds and the opening float",
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
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "shiftId",
     "from": "session"
    },
    {
     "name": "boxId",
     "from": "navigation"
    }
   ],
   "coldEntry": "Resolves from the session; a cold arrival is the ordinary case.",
   "preloaded": [
    "CashMovement.id",
    "CashMovement.kind",
    "CashMovement.amount",
    "CashMovement.denominations",
    "CashMovement.reference"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-042"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 13 operations this screen declares (split from BO-041 on 28 September, audit R276), not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
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
    "BO-008",
    "BO-074"
   ],
   "inferred": true,
   "transitions": [
    {
     "to": "BO-008",
     "trigger": "Product Detail & Variants",
     "provenance": "derived — BO-008 declares entryState.params productId, variantId, version and BO-043 holds none of them, so the edge carries nothing and BO-008 opens cold"
    },
    {
     "to": "BO-074",
     "trigger": "Chart of Accounts",
     "provenance": "flow F98 step 1→2",
     "carries": [
      "accountId"
     ]
    }
   ]
  },
  "notes": "Definition derived from the wireframe board on 14 August. CF-53 — 67 of these 73 had no definition at all. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual.",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listSettlements` reads the population and `getTrialBalance` reads one of them — list, select, act",
  "purpose": "Prove the day balances before anyone goes home.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "textField",
       "label": "Provider name",
       "operation": "listSettlements",
       "notes": "Sends `?providerName=` to `listSettlements`.",
       "provenance": "contract finance.yaml GET /settlements"
      },
      {
       "kind": "textField",
       "label": "Status",
       "operation": "listSettlements",
       "notes": "Sends `?status=` to `listSettlements`.",
       "provenance": "contract finance.yaml GET /settlements"
      },
      {
       "kind": "dataTable",
       "label": "Every settlement",
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
      },
      {
       "kind": "dataTable",
       "label": "Every posting",
       "bindsTo": "Posting",
       "columns": [
        "Posting.id",
        "Posting.journalEntryId",
        "Posting.accountId",
        "Posting.accountCode",
        "Posting.debit",
        "Posting.credit",
        "Posting.venueId",
        "Posting.costCenterId",
        "Posting.source",
        "Posting.sourceId",
        "Posting.description",
        "Posting.postedAt"
       ],
       "operation": "listLedgerEntries",
       "provenance": "contract finance.yaml GET /ledger/entries"
      },
      {
       "kind": "dataTable",
       "label": "Every settlement exception",
       "bindsTo": "SettlementException",
       "columns": [
        "SettlementException.id",
        "SettlementException.settlementId",
        "SettlementException.kind",
        "SettlementException.providerReference",
        "SettlementException.paymentId",
        "SettlementException.amount",
        "SettlementException.expectedAmount",
        "SettlementException.resolution",
        "SettlementException.note",
        "SettlementException.resolvedByPrincipalId",
        "SettlementException.resolvedAt"
       ],
       "operation": "listSettlementExceptions",
       "provenance": "contract finance.yaml GET /settlements/{settlementId}/exceptions"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected settlement",
       "bindsTo": "Settlement",
       "columns": [
        "Settlement.id",
        "Settlement.currencyCode",
        "Settlement.providerName",
        "Settlement.periodStart",
        "Settlement.periodEnd",
        "Settlement.fileReference",
        "Settlement.format",
        "Settlement.status",
        "Settlement.lineCount",
        "Settlement.matchedCount",
        "Settlement.exceptionCount",
        "Settlement.providerGross",
        "Settlement.providerFees",
        "Settlement.providerNet",
        "Settlement.ledgerGross",
        "Settlement.difference"
       ],
       "operation": "getSettlement",
       "provenance": "contract finance.yaml GET /settlements/{settlementId}"
      },
      {
       "kind": "detailPanel",
       "label": "The trial balance",
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
       "label": "Ingest settlement file",
       "operation": "ingestSettlementFile",
       "provenance": "contract finance.yaml POST /settlements"
      },
      {
       "kind": "secondaryButton",
       "label": "Resolve settlement exception",
       "operation": "resolveSettlementException",
       "provenance": "contract finance.yaml POST /settlements/{settlementId}/exceptions"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The daily reconciliation list.",
   "error": "Could not load. Names which read failed and leaves the daily reconciliation untouched.",
   "emptyFirstRun": "No daily reconciliation yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table.",
   "emptyNoResults": "Nothing matches the filter on providerName, status and the daily reconciliation are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Shown when the caller lacks `LEDGER_VIEW`, which `getTrialBalance` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
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
    "trigger": "onAction"
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
    "trigger": "onAction"
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
    "Settlement.id",
    "Settlement.currencyCode",
    "Settlement.providerName",
    "Settlement.periodStart",
    "Settlement.periodEnd"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-043"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 7 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "overlays": [
   {
    "id": "formIngestSettlementFile",
    "component": "modal",
    "trigger": "Ingest settlement file",
    "body": "**Collects what `ingestSettlementFile` sends before it is called.** Required: `providerName`, `periodStart`, `periodEnd`, `fileReference`. Optional: `format`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Ingest settlement file",
     "operation": "ingestSettlementFile"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "providerName",
      "periodStart",
      "periodEnd",
      "fileReference",
      "format"
     ]
    },
    "provenance": "contract finance.yaml POST /settlements"
   },
   {
    "id": "formResolveSettlementException",
    "component": "modal",
    "trigger": "Resolve settlement exception",
    "body": "**Collects what `resolveSettlementException` sends before it is called.** Required: `exceptionId`, `resolution`, `note`. Optional: `matchedPaymentId`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Resolve settlement exception",
     "operation": "resolveSettlementException"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "exceptionId",
      "resolution",
      "note",
      "matchedPaymentId"
     ]
    },
    "provenance": "contract finance.yaml POST /settlements/{settlementId}/exceptions"
   }
  ],
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
    "BO-008"
   ],
   "inferred": true,
   "transitions": [
    {
     "to": "BO-008",
     "trigger": "Product Detail & Variants",
     "provenance": "derived — BO-008 declares entryState.params productId, variantId, version and BO-047 holds none of them, so the edge carries nothing and BO-008 opens cold"
    }
   ]
  },
  "notes": "Definition derived from the wireframe board on 14 August. CF-53 — 67 of these 73 had no definition at all. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual.",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listOrders` reads the population and `getOrder` reads one of them — list, select, act",
  "purpose": "Fix an order that has gone wrong.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "textField",
       "label": "Venue id",
       "operation": "listOrders",
       "notes": "Sends `?venueId=` to `listOrders`.",
       "provenance": "contract orders.yaml GET /orders"
      },
      {
       "kind": "textField",
       "label": "Principal id",
       "operation": "listOrders",
       "notes": "Sends `?principalId=` to `listOrders`.",
       "provenance": "contract orders.yaml GET /orders"
      },
      {
       "kind": "textField",
       "label": "Shift id",
       "operation": "listOrders",
       "notes": "Sends `?shiftId=` to `listOrders`.",
       "provenance": "contract orders.yaml GET /orders"
      },
      {
       "kind": "textField",
       "label": "Status",
       "operation": "listOrders",
       "notes": "Sends `?status=` to `listOrders`.",
       "provenance": "contract orders.yaml GET /orders"
      },
      {
       "kind": "datePicker",
       "label": "Created from",
       "operation": "listOrders",
       "notes": "Sends `?createdFrom=` to `listOrders`.",
       "provenance": "contract orders.yaml GET /orders"
      },
      {
       "kind": "datePicker",
       "label": "Created to",
       "operation": "listOrders",
       "notes": "Sends `?createdTo=` to `listOrders`.",
       "provenance": "contract orders.yaml GET /orders"
      },
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
      },
      {
       "kind": "dataTable",
       "label": "Every refund",
       "bindsTo": "Refund",
       "columns": [
        "Refund.id",
        "Refund.orderId",
        "Refund.batchId",
        "Refund.fxRate",
        "Refund.taxReversalEntryId",
        "Refund.settleTo",
        "Refund.fxVariance",
        "Refund.amount",
        "Refund.appliedPercentage",
        "Refund.status",
        "Refund.reason",
        "Refund.requestedByPrincipalId"
       ],
       "operation": "listOrderRefunds",
       "provenance": "contract orders.yaml GET /orders/{orderId}/refunds"
      },
      {
       "kind": "confirmDialog",
       "derived": true,
       "label": "Confirm",
       "notes": "**The consequence goes in the body, not the title.** *Cancel 3 orders worth AED 480* is a confirmation; *are you sure* is not — and a dialog that cannot name what it destroys is a dialog somebody dismisses.\n\n**Added 31 August.** `confirmDialog` and `modal` were both in the component library and used **zero times across 492 screens**, while `destructiveButton` was used 39 times and its own entry reads *always requires confirmation*.",
       "provenance": "carried from the previous definition"
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
       "bindsTo": "OrderSummary",
       "columns": [
        "OrderSummary.id",
        "OrderSummary.orderNumber",
        "OrderSummary.status",
        "OrderSummary.grossAmount",
        "OrderSummary.refundedAmount",
        "OrderSummary.channel",
        "OrderSummary.lineCount",
        "OrderSummary.principalId",
        "OrderSummary.holdLabel",
        "OrderSummary.heldUntil"
       ],
       "operation": "listOrders",
       "provenance": "contract orders.yaml GET /orders"
      },
      {
       "kind": "detailPanel",
       "label": "The order statement",
       "bindsTo": "OrderStatement",
       "columns": [
        "OrderStatement.orderId",
        "OrderStatement.orderNumber",
        "OrderStatement.currency",
        "OrderStatement.currencyScale",
        "OrderStatement.entries",
        "OrderStatement.totalPaid",
        "OrderStatement.totalRefunded",
        "OrderStatement.currentBalance"
       ],
       "operation": "getOrderStatement",
       "provenance": "contract orders.yaml GET /orders/{orderId}/statement"
      },
      {
       "kind": "detailPanel",
       "label": "The order",
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
       "label": "Create order",
       "operation": "createOrder",
       "provenance": "contract orders.yaml POST /orders"
      },
      {
       "kind": "secondaryButton",
       "label": "Apply manual discount",
       "operation": "applyManualDiscount",
       "provenance": "contract orders.yaml POST /orders/{orderId}/discounts"
      },
      {
       "kind": "secondaryButton",
       "label": "Create refund",
       "operation": "createRefund",
       "provenance": "contract orders.yaml POST /orders/{orderId}/refunds"
      },
      {
       "kind": "secondaryButton",
       "label": "Exchange order lines",
       "operation": "exchangeOrderLines",
       "provenance": "contract orders.yaml POST /orders/{orderId}/exchanges"
      },
      {
       "kind": "secondaryButton",
       "label": "Hold order",
       "operation": "holdOrder",
       "provenance": "contract orders.yaml POST /orders/{orderId}/hold"
      },
      {
       "kind": "secondaryButton",
       "label": "Modify order",
       "operation": "modifyOrder",
       "provenance": "contract orders.yaml POST /orders/{orderId}/modify"
      },
      {
       "kind": "secondaryButton",
       "label": "Reprint order",
       "operation": "reprintOrder",
       "provenance": "contract orders.yaml POST /orders/{orderId}/reprints"
      },
      {
       "kind": "secondaryButton",
       "label": "Reschedule order",
       "operation": "rescheduleOrder",
       "provenance": "contract orders.yaml POST /orders/{orderId}/reschedule"
      },
      {
       "kind": "secondaryButton",
       "label": "Resume order",
       "operation": "resumeOrder",
       "provenance": "contract orders.yaml POST /orders/{orderId}/resume"
      },
      {
       "kind": "destructiveButton",
       "label": "Void order",
       "operation": "voidOrder",
       "provenance": "contract orders.yaml POST /orders/{orderId}/voids"
      }
     ]
    }
   ]
  },
  "overlays": [
   {
    "id": "confirmVoidOrder",
    "component": "confirmDialog",
    "trigger": "Void order",
    "body": "**Names what `voidOrder` changes and what it leaves alone**, in the consequence rather than the verb. A order this affects should be identified in the dialog, not just counted. **Collects what `voidOrder` sends before it is called.** Required: `id`, `reason`, `recordedAt`. `reason` is the void reason list (`VoidReason`: guestChangedMind, enteredInError, itemUnavailable, qualityIssue, duplicate, other); **choosing Other makes `note` required** (decided 28 September, audit R125 (4), R222).",
    "provenance": "contract orders.yaml POST /orders/{orderId}/voids"
   },
   {
    "id": "formCreateOrder",
    "component": "modal",
    "trigger": "Create order",
    "body": "**Collects what `createOrder` sends before it is called.** Required: `id`, `venueId`, `channel`, `lines`, `recordedAt`. Optional: `shiftId`, `subjectId`, `guestLinkId`, `catalogueBundleVersion`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "CreateOrderRequest",
    "confirm": {
     "label": "Create order",
     "operation": "createOrder"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "venueId",
      "channel",
      "lines",
      "recordedAt",
      "shiftId",
      "subjectId",
      "guestLinkId",
      "catalogueBundleVersion"
     ]
    },
    "provenance": "contract orders.yaml POST /orders"
   },
   {
    "id": "formApplyManualDiscount",
    "component": "modal",
    "trigger": "Apply manual discount",
    "body": "**Collects what `applyManualDiscount` sends before it is called.** Required: `id`, `reason`, `recordedAt`. Optional: `lineId`, `amount`, `percentage`, `reasonCode`, `approverPrincipalId`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "ManualDiscountRequest",
    "confirm": {
     "label": "Apply manual discount",
     "operation": "applyManualDiscount"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "reason",
      "recordedAt",
      "lineId",
      "amount",
      "percentage",
      "reasonCode",
      "approverPrincipalId"
     ]
    },
    "provenance": "contract orders.yaml POST /orders/{orderId}/discounts"
   },
   {
    "id": "formCreateRefund",
    "component": "modal",
    "trigger": "Create refund",
    "body": "**Collects what `createRefund` sends before it is called.** Required: `id`, `amount`, `reason`, `recordedAt`. Optional: `lineIds`, `secondaryAuthorisation`, `refundToOriginalTender`, `alternateTender`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "CreateRefundRequest",
    "confirm": {
     "label": "Create refund",
     "operation": "createRefund"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "amount",
      "reason",
      "recordedAt",
      "lineIds",
      "secondaryAuthorisation",
      "refundToOriginalTender",
      "alternateTender"
     ]
    },
    "provenance": "contract orders.yaml POST /orders/{orderId}/refunds"
   },
   {
    "id": "formExchangeOrderLines",
    "component": "modal",
    "trigger": "Exchange order lines",
    "body": "**Collects what `exchangeOrderLines` sends before it is called.** Required: `id`, `outgoingLineIds`, `incomingLines`, `recordedAt`. Optional: `waiveFee`, `reason`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "ExchangeOrderRequest",
    "confirm": {
     "label": "Exchange order lines",
     "operation": "exchangeOrderLines"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "outgoingLineIds",
      "incomingLines",
      "recordedAt",
      "waiveFee",
      "reason"
     ]
    },
    "provenance": "contract orders.yaml POST /orders/{orderId}/exchanges"
   },
   {
    "id": "formHoldOrder",
    "component": "modal",
    "trigger": "Hold order",
    "body": "**Collects what `holdOrder` sends before it is called.** Required: `recordedAt`. Optional: `label`, `holdUntil`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Hold order",
     "operation": "holdOrder"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "recordedAt",
      "label",
      "holdUntil"
     ]
    },
    "provenance": "contract orders.yaml POST /orders/{orderId}/hold"
   },
   {
    "id": "formModifyOrder",
    "component": "modal",
    "trigger": "Modify order",
    "body": "**Collects what `modifyOrder` sends before it is called.** Required: `id`, `recordedAt`. Optional: `addLines`, `removeLineIds`, `reason`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "ModifyOrderRequest",
    "confirm": {
     "label": "Modify order",
     "operation": "modifyOrder"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "recordedAt",
      "addLines",
      "removeLineIds",
      "reason"
     ]
    },
    "provenance": "contract orders.yaml POST /orders/{orderId}/modify"
   },
   {
    "id": "formReprintOrder",
    "component": "modal",
    "trigger": "Reprint order",
    "body": "**Collects what `reprintOrder` sends before it is called.** Required: `delivery`, `recordedAt`. Optional: `destination`, `lineIds`, `reason`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Reprint order",
     "operation": "reprintOrder"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "delivery",
      "recordedAt",
      "destination",
      "lineIds",
      "reason"
     ]
    },
    "provenance": "contract orders.yaml POST /orders/{orderId}/reprints"
   },
   {
    "id": "formRescheduleOrder",
    "component": "modal",
    "trigger": "Reschedule order",
    "body": "**Collects what `rescheduleOrder` sends before it is called.** Required: `targetPerformanceId`, `recordedAt`. Optional: `lineIds`, `waiveFee`, `reason`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Reschedule order",
     "operation": "rescheduleOrder"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "targetPerformanceId",
      "recordedAt",
      "lineIds",
      "waiveFee",
      "reason"
     ]
    },
    "provenance": "contract orders.yaml POST /orders/{orderId}/reschedule"
   }
  ],
  "states": {
   "loading": "The order list.",
   "error": "Could not load. Names which read failed and leaves the order untouched.",
   "emptyFirstRun": "No order yet. Offers Create order (`createOrder`); distinct from a filter that matched nothing.",
   "emptyNoResults": "Nothing matches the filter on venueId, principalId, shiftId, status, createdFrom, createdTo and the order are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Shown when the caller lacks `ORDER_VIEW`, which `listOrders` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
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
    "trigger": "onAction"
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
    "trigger": "onAction"
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
    "trigger": "onAction"
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
    "OrderSummary.id",
    "OrderSummary.orderNumber",
    "OrderSummary.status",
    "OrderSummary.grossAmount",
    "OrderSummary.refundedAmount"
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
    "BO-008"
   ],
   "inferred": true,
   "fromFlows": true,
   "transitions": [
    {
     "to": "BO-008",
     "trigger": "Product Detail & Variants",
     "provenance": "derived — BO-008 declares entryState.params productId, variantId, version and BO-048 holds none of them, so the edge carries nothing and BO-008 opens cold"
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
       "kind": "textField",
       "label": "Outlet id",
       "operation": "listMerchandise",
       "notes": "Sends `?outletId=` to `listMerchandise`.",
       "provenance": "contract retail.yaml GET /merchandise"
      },
      {
       "kind": "textField",
       "label": "Category id",
       "operation": "listMerchandise",
       "notes": "Sends `?categoryId=` to `listMerchandise`.",
       "provenance": "contract retail.yaml GET /merchandise"
      },
      {
       "kind": "toggle",
       "label": "In stock only",
       "operation": "listMerchandise",
       "notes": "Sends `?inStockOnly=` to `listMerchandise`.",
       "provenance": "contract retail.yaml GET /merchandise"
      },
      {
       "kind": "searchField",
       "label": "Search",
       "operation": "listMerchandise",
       "notes": "Sends `?search=` to `listMerchandise`.",
       "provenance": "contract retail.yaml GET /merchandise"
      },
      {
       "kind": "dataTable",
       "label": "Every merchandise",
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
      },
      {
       "kind": "searchField",
       "derived": true,
       "impliedBy": "lookupMerchandise",
       "label": "Search",
       "notes": "A search that returns nothing must say so differently from a search not yet run.",
       "provenance": "carried from the previous definition"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected merchandise",
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
       "label": "Lookup merchandise",
       "operation": "lookupMerchandise",
       "provenance": "contract retail.yaml GET /merchandise/lookup"
      },
      {
       "kind": "secondaryButton",
       "label": "Create merchandise",
       "operation": "createMerchandise",
       "provenance": "contract retail.yaml POST /merchandise"
      },
      {
       "kind": "secondaryButton",
       "label": "Save merchandise",
       "operation": "updateMerchandise",
       "provenance": "contract retail.yaml PATCH /merchandise/{merchandiseId}"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The retail products list.",
   "error": "Could not load. Names which read failed and leaves the retail products untouched.",
   "emptyFirstRun": "No retail products yet. Offers Create merchandise (`createMerchandise`); distinct from a filter that matched nothing.",
   "emptyNoResults": "Nothing matches the filter on outletId, categoryId, inStockOnly, search and the retail products are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Shown when the caller lacks `PRODUCT_VIEW`, which `listMerchandise` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
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
    "trigger": "onAction"
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
  "overlays": [
   {
    "id": "formCreateMerchandise",
    "component": "modal",
    "trigger": "Create merchandise",
    "body": "**Collects what `createMerchandise` sends before it is called.** Required: `sku`, `name`, `outletId`, `variantId`. Optional: `barcode`, `description`, `categoryId`, `inventoryItemId`, `isReturnable`, `returnWindowDays`, `requiresSerialNumber`, `imageAssetRef`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "CreateMerchandiseRequest",
    "confirm": {
     "label": "Create merchandise",
     "operation": "createMerchandise"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "sku",
      "name",
      "outletId",
      "variantId",
      "barcode",
      "description",
      "categoryId",
      "inventoryItemId",
      "isReturnable",
      "returnWindowDays",
      "requiresSerialNumber",
      "imageAssetRef"
     ]
    },
    "provenance": "contract retail.yaml POST /merchandise"
   },
   {
    "id": "formUpdateMerchandise",
    "component": "modal",
    "trigger": "Save merchandise",
    "body": "**Collects what `updateMerchandise` sends before it is called.** Nothing in the body is required. Optional: `name`, `description`, `barcode`, `categoryId`, `inventoryItemId`, `imageAssetRef`, `isReturnable`, `returnWindowDays`, `requiresSerialNumber`, `isActive`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Save merchandise",
     "operation": "updateMerchandise"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "name",
      "description",
      "barcode",
      "categoryId",
      "inventoryItemId",
      "imageAssetRef",
      "isReturnable",
      "returnWindowDays",
      "requiresSerialNumber",
      "isActive"
     ]
    },
    "provenance": "contract retail.yaml PATCH /merchandise/{merchandiseId}"
   }
  ],
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
    "BO-008"
   ],
   "inferred": true,
   "transitions": [
    {
     "to": "BO-008",
     "trigger": "Product Detail & Variants",
     "provenance": "derived — BO-008 declares entryState.params productId, variantId, version and BO-059 holds none of them, so the edge carries nothing and BO-008 opens cold"
    }
   ]
  },
  "notes": "Definition derived from the wireframe board on 14 August. CF-53 — 67 of these 73 had no definition at all. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual.",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listReports` reads the population and `getFinancialReport` reads one of them — list, select, act",
  "purpose": "See what sold, through which channel.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "textField",
       "label": "Category",
       "operation": "listReports",
       "notes": "Sends `?category=` to `listReports`.",
       "provenance": "contract reporting.yaml GET /reports"
      },
      {
       "kind": "searchField",
       "label": "Search",
       "operation": "listReports",
       "notes": "Sends `?search=` to `listReports`.",
       "provenance": "contract reporting.yaml GET /reports"
      },
      {
       "kind": "dataTable",
       "label": "Every report definition",
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
      },
      {
       "kind": "confirmDialog",
       "derived": true,
       "label": "Confirm",
       "notes": "**The consequence goes in the body, not the title.** *Cancel 3 orders worth AED 480* is a confirmation; *are you sure* is not — and a dialog that cannot name what it destroys is a dialog somebody dismisses.\n\n**Added 31 August.** `confirmDialog` and `modal` were both in the component library and used **zero times across 492 screens**, while `destructiveButton` was used 39 times and its own entry reads *always requires confirmation*.",
       "provenance": "carried from the previous definition"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected report definition",
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
        "ReportDefinition.isSystem",
        "ReportDefinition.isRetired",
        "ReportDefinition.estimatedCost",
        "ReportDefinition.createdByPrincipalId",
        "ReportDefinition.lastRunAt"
       ],
       "operation": "getReport",
       "provenance": "contract reporting.yaml GET /reports/{reportId}"
      },
      {
       "kind": "detailPanel",
       "label": "The financial report",
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
       "label": "Create report",
       "operation": "createReport",
       "provenance": "contract reporting.yaml POST /reports"
      },
      {
       "kind": "secondaryButton",
       "label": "Ask reporting question",
       "operation": "askReportingQuestion",
       "provenance": "contract reporting.yaml POST /reports/ask"
      },
      {
       "kind": "destructiveButton",
       "label": "Delete report",
       "operation": "deleteReport",
       "provenance": "contract reporting.yaml DELETE /reports/{reportId}"
      },
      {
       "kind": "secondaryButton",
       "label": "Run report",
       "operation": "runReport",
       "notes": "**Runs the seeded report `salesByChannel`** — net sales per sales channel for the period (proposed, client to correct; decided 28 September, audit R282). `reportId` is the venue's seeded definition with that code, listed on `listSeededReports`.",
       "provenance": "contract reporting.yaml POST /reports/{reportId}/run"
      },
      {
       "kind": "secondaryButton",
       "label": "Save natural language query",
       "operation": "saveNaturalLanguageQuery",
       "provenance": "contract reporting.yaml POST /reports/ask/{conversationId}/save"
      },
      {
       "kind": "secondaryButton",
       "label": "Save report",
       "operation": "updateReport",
       "provenance": "contract reporting.yaml PUT /reports/{reportId}"
      }
     ]
    }
   ]
  },
  "overlays": [
   {
    "id": "confirmDeleteReport",
    "component": "confirmDialog",
    "trigger": "Delete report",
    "body": "**Names what `deleteReport` changes and what it leaves alone**, in the consequence rather than the verb. A sales reports this affects should be identified in the dialog, not just counted.",
    "provenance": "contract reporting.yaml DELETE /reports/{reportId}"
   },
   {
    "id": "formCreateReport",
    "component": "modal",
    "trigger": "Create report",
    "body": "**Collects what `createReport` sends before it is called.** Required: `name`, `category`, `dataSource`, `columns`, `requiredPermission`. Optional: `description`, `filters`, `groupBy`, `parameters`, `maxDateRangeDays`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "CreateReportRequest",
    "confirm": {
     "label": "Create report",
     "operation": "createReport"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "name",
      "category",
      "dataSource",
      "columns",
      "requiredPermission",
      "description",
      "filters",
      "groupBy",
      "parameters",
      "maxDateRangeDays"
     ]
    },
    "provenance": "contract reporting.yaml POST /reports"
   },
   {
    "id": "formAskReportingQuestion",
    "component": "modal",
    "trigger": "Ask reporting question",
    "body": "**Collects what `askReportingQuestion` sends before it is called.** Required: `question`. Optional: `conversationId`, `venueId`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Ask reporting question",
     "operation": "askReportingQuestion"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "question",
      "conversationId",
      "venueId"
     ]
    },
    "provenance": "contract reporting.yaml POST /reports/ask"
   },
   {
    "id": "formRunReport",
    "component": "modal",
    "trigger": "Run report",
    "body": "**Collects what `runReport` sends before it is called.** Nothing in the body is required. Optional: `parameters`, `venueId`, `dateFrom`, `dateTo`, `forceAsync`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "RunReportRequest",
    "confirm": {
     "label": "Run report",
     "operation": "runReport"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "parameters",
      "venueId",
      "dateFrom",
      "dateTo",
      "forceAsync"
     ]
    },
    "provenance": "contract reporting.yaml POST /reports/{reportId}/run"
   },
   {
    "id": "formSaveNaturalLanguageQuery",
    "component": "modal",
    "trigger": "Save natural language query",
    "body": "**Collects what `saveNaturalLanguageQuery` sends before it is called.** Required: `name`. Optional: `category`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Save natural language query",
     "operation": "saveNaturalLanguageQuery"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "name",
      "category"
     ]
    },
    "provenance": "contract reporting.yaml POST /reports/ask/{conversationId}/save"
   },
   {
    "id": "formUpdateReport",
    "component": "modal",
    "trigger": "Save report",
    "body": "**Collects what `updateReport` sends before it is called.** Required: `name`, `category`, `dataSource`, `columns`, `requiredPermission`. Optional: `description`, `filters`, `groupBy`, `parameters`, `maxDateRangeDays`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "CreateReportRequest",
    "confirm": {
     "label": "Save report",
     "operation": "updateReport"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "name",
      "category",
      "dataSource",
      "columns",
      "requiredPermission",
      "description",
      "filters",
      "groupBy",
      "parameters",
      "maxDateRangeDays"
     ]
    },
    "provenance": "contract reporting.yaml PUT /reports/{reportId}"
   }
  ],
  "states": {
   "loading": "The sales reports list.",
   "error": "Could not load. Names which read failed and leaves the sales reports untouched.",
   "emptyFirstRun": "No sales reports yet. Offers Create report (`createReport`); distinct from a filter that matched nothing.",
   "emptyNoResults": "Nothing matches the filter on category, search and the sales reports are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Shown when the caller lacks `REPORT_VIEW_VENUE`, which `getFinancialReport` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
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
    "trigger": "onAction"
   },
   {
    "operationId": "runReport",
    "contract": "reporting",
    "purpose": "Run the seeded report `salesByChannel` (proposed, audit R282)",
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
    "ReportDefinition.name",
    "ReportDefinition.description",
    "ReportDefinition.category",
    "ReportDefinition.dataSource",
    "ReportDefinition.columns"
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
    "BO-008",
    "BO-060"
   ],
   "inferred": true,
   "entryFrom": [
    "BO-058"
   ],
   "transitions": [
    {
     "to": "BO-008",
     "trigger": "Product Detail & Variants",
     "provenance": "derived — BO-008 declares entryState.params productId, variantId, version and BO-061 holds none of them, so the edge carries nothing and BO-008 opens cold"
    },
    {
     "to": "BO-060",
     "trigger": "Attendance & Footfall",
     "provenance": "flow F107 step 2→3",
     "carries": [
      "reportId"
     ]
    }
   ]
  },
  "notes": "Definition derived from the wireframe board on 14 August. CF-53 — 67 of these 73 had no definition at all. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual. **Rebound 28 September to report schedules (audit R254, R261)** — the screen carried report-definition and natural-language operations (`askReportingQuestion`, `saveNaturalLanguageQuery`, `getFinancialReport`, `deleteReport` and five more) that serve BO-058 and BO-060; it now lists, creates, changes and deletes schedules and shows each schedule's delivery history.",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listReportSchedules` reads the population and `listReportExecutions` reads the delivery history of the selected one — list, select, act",
  "purpose": "Send a report to somebody without them asking.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every report schedule",
       "bindsTo": "ReportSchedule",
       "columns": [
        "ReportSchedule.name",
        "ReportSchedule.reportId",
        "ReportSchedule.cadence",
        "ReportSchedule.recipients",
        "ReportSchedule.format",
        "ReportSchedule.isPaused",
        "ReportSchedule.lastRunAt",
        "ReportSchedule.lastRunStatus",
        "ReportSchedule.nextRunAt",
        "ReportSchedule.consecutiveFailures"
       ],
       "operation": "listReportSchedules",
       "provenance": "contract reporting.yaml GET /report-schedules"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Delivery history",
       "bindsTo": "ReportExecution",
       "columns": [
        "ReportExecution.requestedAt",
        "ReportExecution.completedAt",
        "ReportExecution.status",
        "ReportExecution.rowCount",
        "ReportExecution.error",
        "ReportExecution.expiresAt"
       ],
       "operation": "listReportExecutions",
       "notes": "Sends `?reportId=` of the selected schedule to `listReportExecutions`; each run the schedule made is a row, with its status and any error, so a recipient who says they never got it can be answered.",
       "provenance": "contract reporting.yaml GET /report-executions"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Create report schedule",
       "operation": "createReportSchedule",
       "provenance": "contract reporting.yaml POST /report-schedules"
      },
      {
       "kind": "secondaryButton",
       "label": "Save report schedule",
       "operation": "updateReportSchedule",
       "provenance": "contract reporting.yaml PATCH /report-schedules/{scheduleId}"
      },
      {
       "kind": "destructiveButton",
       "label": "Delete report schedule",
       "operation": "deleteReportSchedule",
       "provenance": "contract reporting.yaml DELETE /report-schedules/{scheduleId}"
      }
     ]
    }
   ]
  },
  "overlays": [
   {
    "id": "formCreateReportSchedule",
    "component": "modal",
    "trigger": "Create report schedule",
    "body": "**Collects what `createReportSchedule` sends before it is called.** Required: `reportId`, `cadence`, `recipients`, `format`. Optional: `name`, `parameters`, `includePersonalData`, `skipIfEmpty`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "CreateReportScheduleRequest",
    "confirm": {
     "label": "Create report schedule",
     "operation": "createReportSchedule"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "reportId",
      "name",
      "cadence",
      "parameters",
      "recipients",
      "format",
      "includePersonalData",
      "skipIfEmpty"
     ]
    },
    "provenance": "contract reporting.yaml POST /report-schedules"
   },
   {
    "id": "formUpdateReportSchedule",
    "component": "modal",
    "trigger": "Save report schedule",
    "body": "**Collects what `updateReportSchedule` sends before it is called.** At least one of `isPaused`, `cadence`, `recipients`, `format`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Save report schedule",
     "operation": "updateReportSchedule"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "isPaused",
      "cadence",
      "recipients",
      "format"
     ]
    },
    "provenance": "contract reporting.yaml PATCH /report-schedules/{scheduleId}"
   },
   {
    "id": "confirmDeleteReportSchedule",
    "component": "confirmDialog",
    "trigger": "Delete report schedule",
    "body": "**Names the schedule and who stops receiving it.** Deleting stops future deliveries; the delivery history already made stays.",
    "provenance": "contract reporting.yaml DELETE /report-schedules/{scheduleId}"
   }
  ],
  "states": {
   "loading": "The report schedules.",
   "error": "Could not load. Names which read failed and leaves the schedules untouched.",
   "emptyFirstRun": "No report schedules yet. Offers Create report schedule (`createReportSchedule`).",
   "emptyNoResults": "Never shown: `listReportSchedules` takes no filter here, so an empty list is always the first-run state above.",
   "emptyNoAccess": "Shown when the caller lacks `REPORT_VIEW_VENUE`, which `listReportSchedules` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listReportSchedules",
    "contract": "reporting",
    "purpose": "Every scheduled delivery",
    "trigger": "onLoad"
   },
   {
    "operationId": "createReportSchedule",
    "contract": "reporting",
    "purpose": "Schedule a report to recipients",
    "trigger": "onAction",
    "invalidates": [
     "listReportSchedules"
    ]
   },
   {
    "operationId": "updateReportSchedule",
    "contract": "reporting",
    "purpose": "Pause, change cadence, recipients or format",
    "trigger": "onAction",
    "invalidates": [
     "listReportSchedules"
    ]
   },
   {
    "operationId": "deleteReportSchedule",
    "contract": "reporting",
    "purpose": "Stop a scheduled delivery",
    "trigger": "onAction",
    "invalidates": [
     "listReportSchedules"
    ]
   },
   {
    "operationId": "listReportExecutions",
    "contract": "reporting",
    "purpose": "Delivery history of a schedule",
    "trigger": "onAction"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "reportId",
     "from": "deepLink",
     "optional": true
    },
    {
     "name": "scheduleId",
     "from": "navigation"
    }
   ],
   "coldEntry": "A link to a report's schedules. Opens the list filtered to that report, or says the report no longer exists.",
   "preloaded": [
    "ReportSchedule.name",
    "ReportSchedule.reportId",
    "ReportSchedule.cadence"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-061"
  },
  "apisNote": "Rebuilt 28 September 2026 on report schedules (audit R254, R261). The 9 report-definition and natural-language operations bound on 9 September served BO-058/BO-060, not scheduling, and were removed.",
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
    "BO-008"
   ],
   "inferred": true,
   "transitions": [
    {
     "to": "BO-008",
     "trigger": "Product Detail & Variants",
     "provenance": "derived — BO-008 declares entryState.params productId, variantId, version and BO-062 holds none of them, so the edge carries nothing and BO-008 opens cold"
    }
   ]
  },
  "notes": "Definition derived from the wireframe board on 14 August. CF-53 — 67 of these 73 had no definition at all. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual.",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listDiningOutlets` reads the population and `getRefundPolicy` reads one of them — list, select, act",
  "purpose": "The facts every other surface reads.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "toggle",
       "label": "Open now",
       "operation": "listDiningOutlets",
       "notes": "Sends `?openNow=` to `listDiningOutlets`.",
       "provenance": "contract fnb.yaml GET /venues/{venueId}/dining"
      },
      {
       "kind": "textField",
       "label": "Ordering method",
       "operation": "listDiningOutlets",
       "notes": "Sends `?orderingMethod=` to `listDiningOutlets`.",
       "provenance": "contract fnb.yaml GET /venues/{venueId}/dining"
      },
      {
       "kind": "dataTable",
       "label": "Every dining outlet",
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
      },
      {
       "kind": "dataTable",
       "label": "Every delivery location",
       "bindsTo": "DeliveryLocation",
       "columns": [
        "DeliveryLocation.id",
        "DeliveryLocation.venueId",
        "DeliveryLocation.kind",
        "DeliveryLocation.label",
        "DeliveryLocation.zone",
        "DeliveryLocation.tableId",
        "DeliveryLocation.seatId",
        "DeliveryLocation.servingOutletIds",
        "DeliveryLocation.isServiceable",
        "DeliveryLocation.unserviceableReason",
        "DeliveryLocation.walkTimeMinutes"
       ],
       "operation": "listDeliveryLocations",
       "provenance": "contract fnb.yaml GET /venues/{venueId}/delivery-locations"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected dining outlet",
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
      },
      {
       "kind": "detailPanel",
       "label": "The refund policy",
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
       "label": "Save refund policy",
       "operation": "setRefundPolicy",
       "provenance": "contract orders.yaml PUT /venues/{venueId}/refund-policy"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The venue profile list.",
   "error": "Could not load. Names which read failed and leaves the venue profile untouched.",
   "emptyFirstRun": "No venue profile yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table.",
   "emptyNoResults": "Nothing matches the filter on openNow, orderingMethod and the venue profile are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Shown when the caller lacks `ORDER_VIEW`, which `getRefundPolicy` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
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
    "DiningOutlet.outletId",
    "DiningOutlet.name",
    "DiningOutlet.kind",
    "DiningOutlet.zone",
    "DiningOutlet.cuisine"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-062"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 4 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "overlays": [
   {
    "id": "formSetRefundPolicy",
    "component": "modal",
    "trigger": "Save refund policy",
    "body": "**Collects what `setRefundPolicy` sends before it is called.** Required: `venueId`, `selfAuthoriseLimit`, `requiresApprovalAbove`. Optional: `id`, `requiresSecondUserAbove`, `timeBands`, `allowPartial`, `refundWindowDays`, `varianceThreshold`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "RefundPolicy",
    "confirm": {
     "label": "Save refund policy",
     "operation": "setRefundPolicy"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "venueId",
      "selfAuthoriseLimit",
      "requiresApprovalAbove",
      "id",
      "requiresSecondUserAbove",
      "timeBands",
      "allowPartial",
      "refundWindowDays",
      "varianceThreshold"
     ]
    },
    "provenance": "contract orders.yaml PUT /venues/{venueId}/refund-policy"
   }
  ],
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
  "id": "BO-065",
  "name": "Venue Configuration",
  "module": "Orders & Money",
  "requiresModule": "ticketing",
  "wave": 1,
  "capability": "C00",
  "implementation": {
   "app": "venue-management-web",
   "route": "/venue-operations/venue-configuration",
   "component": "apps/venue-management-web/src/routes/venue-operations/VenueConfigurationDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "exitTo": [
    "BO-008"
   ],
   "inferred": true,
   "transitions": [
    {
     "to": "BO-008",
     "trigger": "Product Detail & Variants",
     "provenance": "derived — BO-008 declares entryState.params productId, variantId, version and BO-065 holds none of them, so the edge carries nothing and BO-008 opens cold"
    }
   ]
  },
  "notes": "Definition derived from the wireframe board on 14 August. CF-53 — 67 of these 73 had no definition at all. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual.",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listDiningOutlets` reads the population and `getRefundPolicy` reads one of them — list, select, act",
  "purpose": "Set the venue-level values everything inherits from.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "toggle",
       "label": "Open now",
       "operation": "listDiningOutlets",
       "notes": "Sends `?openNow=` to `listDiningOutlets`.",
       "provenance": "contract fnb.yaml GET /venues/{venueId}/dining"
      },
      {
       "kind": "textField",
       "label": "Ordering method",
       "operation": "listDiningOutlets",
       "notes": "Sends `?orderingMethod=` to `listDiningOutlets`.",
       "provenance": "contract fnb.yaml GET /venues/{venueId}/dining"
      },
      {
       "kind": "dataTable",
       "label": "Every dining outlet",
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
      },
      {
       "kind": "dataTable",
       "label": "Every delivery location",
       "bindsTo": "DeliveryLocation",
       "columns": [
        "DeliveryLocation.id",
        "DeliveryLocation.venueId",
        "DeliveryLocation.kind",
        "DeliveryLocation.label",
        "DeliveryLocation.zone",
        "DeliveryLocation.tableId",
        "DeliveryLocation.seatId",
        "DeliveryLocation.servingOutletIds",
        "DeliveryLocation.isServiceable",
        "DeliveryLocation.unserviceableReason",
        "DeliveryLocation.walkTimeMinutes"
       ],
       "operation": "listDeliveryLocations",
       "provenance": "contract fnb.yaml GET /venues/{venueId}/delivery-locations"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected dining outlet",
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
      },
      {
       "kind": "detailPanel",
       "label": "The refund policy",
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
      },
      {
       "kind": "toggle",
       "label": "Guest two-step verification",
       "bindsTo": "VenueSettings.identity.guestTwoStep.enabled",
       "operation": "setVenueSettings",
       "notes": "**A venue option, off unless the venue enables it** (decided 29 September, rev 3 GAP-B1, per venue, superseding the second part of audit R167 \"no guest MFA\"; guests still never use enterprise SSO). On, a guest of this venue may enrol an authenticator app with email codes as the fallback, and an enrolled guest is asked for it at sign-in here. A guest's enrolment is one per tenant, so it is never asked at a venue that has this off. Left empty, the venue inherits the tenant default.",
       "provenance": "contract tenancy.yaml PUT /venues/{venueId}/settings"
      },
      {
       "kind": "multiSelect",
       "label": "Actions that ask again",
       "bindsTo": "VenueSettings.identity.guestTwoStep.stepUpActions",
       "operation": "setVenueSettings",
       "notes": "The guest actions at this venue that ask an enrolled guest for the factor again, whatever the age of the session: change contact details, change password, manage payment methods, transfer tickets, delete account. Proposed default all but transfer tickets, client to correct (rev 3 GAP-B1).",
       "provenance": "contract tenancy.yaml PUT /venues/{venueId}/settings"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Save refund policy",
       "operation": "setRefundPolicy",
       "provenance": "contract orders.yaml PUT /venues/{venueId}/refund-policy"
      },
      {
       "kind": "secondaryButton",
       "label": "Save venue settings",
       "operation": "setVenueSettings",
       "provenance": "contract tenancy.yaml PUT /venues/{venueId}/settings"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The venue list.",
   "error": "Could not load. Names which read failed and leaves the venue untouched.",
   "emptyFirstRun": "No venue yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table.",
   "emptyNoResults": "Nothing matches the filter on openNow, orderingMethod and the venue are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Shown when the caller lacks `ORDER_VIEW`, which `getRefundPolicy` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
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
   },
   {
    "operationId": "setVenueSettings",
    "contract": "tenancy",
    "purpose": "Save the venue's configuration",
    "trigger": "onAction",
    "invalidates": [
     "listDiningOutlets"
    ]
   },
   {
    "operationId": "getVenueSettings",
    "contract": "tenancy",
    "purpose": "The venue's settings, with the tenant default each empty one inherits",
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
    "DiningOutlet.outletId",
    "DiningOutlet.name",
    "DiningOutlet.kind",
    "DiningOutlet.zone",
    "DiningOutlet.cuisine"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-065"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 5 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "overlays": [
   {
    "id": "formSetRefundPolicy",
    "component": "modal",
    "trigger": "Save refund policy",
    "body": "**Collects what `setRefundPolicy` sends before it is called.** Required: `venueId`, `selfAuthoriseLimit`, `requiresApprovalAbove`. Optional: `id`, `requiresSecondUserAbove`, `timeBands`, `allowPartial`, `refundWindowDays`, `varianceThreshold`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "RefundPolicy",
    "confirm": {
     "label": "Save refund policy",
     "operation": "setRefundPolicy"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "venueId",
      "selfAuthoriseLimit",
      "requiresApprovalAbove",
      "id",
      "requiresSecondUserAbove",
      "timeBands",
      "allowPartial",
      "refundWindowDays",
      "varianceThreshold"
     ]
    },
    "provenance": "contract orders.yaml PUT /venues/{venueId}/refund-policy"
   },
   {
    "id": "formSetVenueSettings",
    "component": "modal",
    "trigger": "Save venue settings",
    "body": "**Collects what `setVenueSettings` sends before it is called.** Nothing in the body is required. Optional: `id`, `venueId`, `currencyCode`, `currencyScale`, `supportHours`, `quietHours`, `biometrics`, `segregatedAccess`, `alerting`, and **the configured limits** — `displayCurrencies`, the cart, resale, exchange, reschedule and reservation limits, `shiftVarianceThreshold`, and the `catalogue`, `inventory`, `seating`, `promotions`, `fnb`, `queue` and `reporting` groups (decided 28 September, audit R094), and `identity`, which carries guest two-step verification for this venue (decided 29 September, rev 3 GAP-B1). `seating.maxSeatsPerGuestOrder` is set on BO-1063. **A limit left empty inherits the tenant default** (null = inherit); each field shows the default it would inherit. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "VenueSettings",
    "confirm": {
     "label": "Save venue settings",
     "operation": "setVenueSettings"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "venueId",
      "currencyCode",
      "currencyScale",
      "supportHours",
      "quietHours",
      "biometrics",
      "segregatedAccess",
      "alerting",
      "displayCurrencies",
      "catalogue",
      "inventory",
      "seating",
      "promotions",
      "fnb",
      "queue",
      "reporting",
      "identity"
     ]
    },
    "provenance": "contract tenancy.yaml PUT /venues/{venueId}/settings"
   }
  ],
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
  "offlineCapable": false,
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
 "createReportSchedule": {
  "method": "POST",
  "path": "/report-schedules",
  "contract": "reporting",
  "summary": "Schedule a report",
  "permission": "REPORT_SCHEDULE",
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
  "requestBody": "CreateReportScheduleRequest",
  "responds": "ReportSchedule"
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
 "deleteReportSchedule": {
  "method": "DELETE",
  "path": "/report-schedules/{scheduleId}",
  "contract": "reporting",
  "summary": "Delete a schedule",
  "permission": "REPORT_SCHEDULE",
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
  "summary": "Financial statements, revenue and tax summaries",
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
 "getVenueSettings": {
  "method": "GET",
  "path": "/venues/{venueId}/settings",
  "contract": "tenancy",
  "summary": "Operational settings for this venue",
  "permission": "TENANT_VIEW",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "VenueSettings"
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
  "responds": "Page"
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
  "responds": "Page"
 },
 "listDepositBoxes": {
  "method": "GET",
  "path": "/deposit-boxes",
  "contract": "shift",
  "summary": "Cash boxes and who holds them",
  "permission": "SHIFT_OPEN",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "openOnly",
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
  "responds": "Page"
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
  "responds": "Page"
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
 "listReportExecutions": {
  "method": "GET",
  "path": "/report-executions",
  "contract": "reporting",
  "summary": "List executions",
  "permission": "REPORT_VIEW_VENUE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "reportId",
    "in": "query",
    "required": null
   },
   {
    "name": "status",
    "in": "query",
    "required": null
   },
   {
    "name": "mineOnly",
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
 "listReportSchedules": {
  "method": "GET",
  "path": "/report-schedules",
  "contract": "reporting",
  "summary": "List scheduled reports",
  "permission": "REPORT_VIEW_VENUE",
  "offlineCapable": false,
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
    "name": "venueId",
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
   },
   {
    "name": "outletId",
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
  "offlineCapable": false,
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
  "summary": "Open the Deposit Box without a sale",
  "permission": "CASH_NO_SALE",
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
 "setVenueSettings": {
  "method": "PUT",
  "path": "/venues/{venueId}/settings",
  "contract": "tenancy",
  "summary": "Set support hours, quiet hours, segregated access and alerting",
  "permission": "TENANT_CONFIGURE",
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
  "requestBody": "VenueSettings",
  "responds": "VenueSettings"
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
 "updateReportSchedule": {
  "method": "PATCH",
  "path": "/report-schedules/{scheduleId}",
  "contract": "reporting",
  "summary": "Amend, pause or resume a schedule",
  "permission": "REPORT_SCHEDULE",
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
  "responds": "ReportSchedule"
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
 },
 "withdrawFromDepositBox": {
  "method": "POST",
  "path": "/deposit-boxes/{boxId}/withdraw",
  "contract": "shift",
  "summary": "A supervisor takes cash out mid-shift",
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
  "requestBody": null,
  "responds": "DepositBox"
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
 "Cadence": {
  "x-ticvai-persistence": "none — embedded in schedule",
  "type": "object",
  "description": "**What each frequency needs (decided 28 September, audit R158).** `daily`: `timeOfDay`. `weekly`: `dayOfWeek` and `timeOfDay`. `monthly`: `dayOfMonth` and `timeOfDay`, a day past the month's end running on its last day. `quarterly`: `dayOfMonth` and `timeOfDay`, in the first month of each quarter. `onShiftClose` and `onPeriodClose`: nothing else, they run on the event. A field a frequency needs and does not have, or one it does not take, is the 400 on `createReportSchedule`. **Times are in the venue's time zone.**\n",
  "required": [
   "frequency"
  ],
  "properties": {
   "frequency": {
    "type": "string",
    "enum": [
     "daily",
     "weekly",
     "monthly",
     "quarterly",
     "onShiftClose",
     "onPeriodClose"
    ]
   },
   "dayOfWeek": {
    "type": "integer",
    "minimum": 0,
    "maximum": 6
   },
   "dayOfMonth": {
    "type": "integer",
    "minimum": 1,
    "maximum": 31
   },
   "timeOfDay": {
    "type": "string",
    "pattern": "^([01]\\d|2[0-3]):[0-5]\\d$"
   },
   "timeZone": {
    "type": "string",
    "readOnly": true,
    "description": "Always the venue's time zone (decided 28 September, audit R158), returned so a reader knows which. Not taken on a write."
   }
  }
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
      "type": "string",
      "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
     },
     "depositBoxId": {
      "type": "string",
      "format": "uuid",
      "nullable": true,
      "description": "The box the cash moved in or out of. Set on every lift `withdrawFromDepositBox` records (26 September, pull audit R099).\n"
     },
     "witnessPrincipalId": {
      "type": "string",
      "format": "uuid",
      "nullable": true,
      "description": "The cashier who countersigned a withdrawal. Null on other movements."
     },
     "withdrawalReason": {
      "allOf": [
       {
        "$ref": "#/components/schemas/WithdrawalReason"
       }
      ],
      "nullable": true
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
  ],
  "description": "`openingFloat` is written by `openShift`; `lift` by `createCashMovement` and by `withdrawFromDepositBox`, which is a lift from one cashier's box; `add` by `createCashMovement`.\n"
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
    "type": "array",
    "minItems": 1,
    "description": "**The cashier's blind count, one line per denomination counted** (decided 29 September, readiness close-out; our build plan). The server writes each line as one `CashCountLine` (`countKind` close) against the shift, taking the face value from `platform.denomination`. A denomination may appear once; a repeat is refused with 422 `duplicate-denomination`.\n",
    "items": {
     "$ref": "#/components/schemas/CountedDenominationLine"
    }
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
 "CountedDenominationLine": {
  "type": "object",
  "x-ticvai-persistence": "none — request only; lands as `CashCountLine` rows",
  "description": "**One line of a cash count as the cashier types it: which note or coin, how many, and what they come to** (decided 29 September, readiness close-out; our build plan). The shape of the blind count on close (`closeShift`) and of the count columns on the till screens (POS-007, POS-011). It is the request side of `CashCountLine`, which is the stored row and adds the shift, the count kind, who counted and when.\n**`total` is shown to the cashier and checked, not trusted**: the server recomputes `count` times the denomination's face value and refuses a line whose `total` disagrees with 422 `count-total-mismatch`. An inactive or unknown denomination is refused with 422 `unknown-denomination`.\n",
  "required": [
   "denominationId",
   "count"
  ],
  "properties": {
   "denominationId": {
    "type": "string",
    "format": "uuid",
    "description": "References `platform.denomination` (`Denomination.id`) — face value, kind and counting order live there."
   },
   "count": {
    "type": "integer",
    "minimum": 0,
    "maximum": 100000,
    "description": "**How many of this note or coin were counted.** Zero is a line, not an omission: a denomination counted and found empty."
   },
   "total": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "description": "`count` times the face value, in the denomination's currency. Optional on the way in (the server computes it) and checked when sent.\n"
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
    "$ref": "#/components/schemas/DenominationCount",
    "x-ticvai-persisted": false,
    "description": "**Stored as `orders.cash_count_line` rows** with `countKind: movement` and this movement's `cashMovementId`, not as a column. The jsonb blob this used to land in is what `Denomination` was created to replace (26 September, pull audit R099).\n"
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
   "description": {
    "type": "string",
    "description": "What the item is, in the guest's words. Indexed for guest-app search."
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
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$",
    "description": "Client-generated ULID of the line. `lineIds` everywhere in this contract are these."
   },
   "variantId": {
    "type": "string",
    "format": "uuid"
   },
   "performanceId": {
    "type": "string",
    "format": "uuid"
   },
   "bookedWindow": {
    "$ref": "#/components/schemas/BookedWindow"
   },
   "inventoryHoldId": {
    "type": "string",
    "nullable": true,
    "description": "Lease the units were drawn from — a `catalogue.InventoryHold.id`. Absent for uncontended products."
   },
   "seatIds": {
    "type": "array",
    "maxItems": 50,
    "items": {
     "type": "string",
     "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
    },
    "description": "Seated products only, as `seating.Seat.id`. Not available offline. **At most `VenueSettings.seating.maxSeatsPerGuestOrder` seats per booking on a guest channel** (default 10, bounds 1 to 50, decided 29 September, rev 3 REV3-7); **at most 10 per sale on staff and POS** (audit R080 (c)), across all the lines of one order for one performance. `createOrder` refuses more with 422 `seatLimitExceeded` (problem type `seat-limit-exceeded`)."
   },
   "resourceHoldId": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$",
    "nullable": true,
    "description": "A `resources.ResourceHold` on a resource the guest picked on a venue map (decided 29 September, rev 3 REV3-15); `variantId` is the placed resource's price-band variant. `createOrder` converts the hold into a `ResourceBooking` without releasing it. Not available offline."
   },
   "attributes": {
    "$ref": "#/components/schemas/OrderLineAttributes"
   },
   "quantity": {
    "type": "integer",
    "minimum": 1
   },
   "eligibilityDeclaration": {
    "type": "array",
    "nullable": true,
    "x-ticvai-note": "One row per declared guest in `orders.order_line_eligibility` (named on `OrderLine`), because an array of objects is a child table's rows, not a column.\n",
    "items": {
     "type": "object",
     "properties": {
      "ageBand": {
       "type": "string",
       "enum": [
        "infant",
        "child",
        "junior",
        "adult",
        "senior"
       ],
       "description": "Infant under 3, child 3–12, junior 13–17, adult 18–59, senior 60+."
      },
      "ageYears": {
       "type": "integer",
       "nullable": true
      },
      "heightBandIndex": {
       "type": "integer",
       "nullable": true
      },
      "confidentSwimmer": {
       "type": "boolean",
       "nullable": true,
       "description": "**Derived, kept for the gate check** (decided 29 September, rev 3 REV3-26). The swim question is a consent: the answer is a `marketing.BookingConsentRecord` of kind `swim`, and this is filled from it (true for a `yes` covering this person, whether answered for them or once for the booking). A value sent that contradicts the record is ignored and the record wins. No longer the place a swim answer is captured.\n"
      },
      "guardianSigned": {
       "type": "boolean"
      }
     }
    },
    "description": "What was declared for each guest on this line, kept as the record staff check at the gate."
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
    "additionalProperties": true,
    "description": "**Deliberately open.** Custom fields keyed by the venue's data mask: the field definitions travel in the catalogue bundle (`catalogue.CatalogueBundle.payload`), so the keys are the venue's to define, as on `catalogue`'s own `dataMaskValues`.\n"
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
    "description": "Client-generated ULID. Also the idempotency key: it must equal the `Idempotency-Key` header, and a replay or a mismatch follows `IdempotencyKey` in `shared/common.yaml`. Offline replay through `syncOrders` carries no header, and this id alone deduplicates there.\n"
   },
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "channel": {
    "$ref": "#/components/schemas/Channel"
   },
   "shiftId": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
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
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$",
    "description": "Client-generated ULID of the refund, and its idempotency key — it must equal the `Idempotency-Key` header."
   },
   "lineIds": {
    "type": "array",
    "items": {
     "type": "string",
     "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
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
      "maxLength": 512,
      "description": "The second person's staff PIN, as they sign in at a till with it. **A PIN, never a password** (decided 28 September, audit R123 (7))."
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
    "$ref": "../shared/permissions.yaml#/components/schemas/Permission",
    "description": "Permission needed to run this report, from the shared `Permission` vocabulary. **The author cannot assign one they do not hold** — otherwise a venue user could build themselves a tenant-wide view.\n"
   },
   "maxDateRangeDays": {
    "type": "integer",
    "nullable": true,
    "minimum": 1,
    "default": 366,
    "description": "Guards against a query spanning years of scan events. **When a report sets none, 366 days applies (decided 28 September, audit R158)**, so `runReport`'s date-range 400 always has a limit."
   }
  }
 },
 "CreateReportScheduleRequest": {
  "x-ticvai-persistence": "none — request only",
  "type": "object",
  "required": [
   "reportId",
   "cadence",
   "recipients",
   "format"
  ],
  "properties": {
   "reportId": {
    "type": "string",
    "format": "uuid"
   },
   "name": {
    "type": "string",
    "maxLength": 200
   },
   "cadence": {
    "$ref": "#/components/schemas/Cadence"
   },
   "parameters": {
    "type": "object",
    "additionalProperties": true,
    "description": "As `RunReportRequest.parameters` — keyed by the report's `ReportParameter.key`, applied to every run."
   },
   "recipients": {
    "type": "array",
    "minItems": 1,
    "items": {
     "$ref": "#/components/schemas/Recipient"
    }
   },
   "format": {
    "$ref": "#/components/schemas/ExportFormat"
   },
   "includePersonalData": {
    "type": "boolean",
    "default": false
   },
   "skipIfEmpty": {
    "type": "boolean",
    "default": true,
    "description": "An empty report every morning trains people to ignore the report."
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
 "DenominationCount": {
  "type": "array",
  "description": "**A count is a list of lines and the line is the row.** Until 24 August this array carried the persistence hint itself, so `orders.cash_count_line` derived a single column — `shift_id` — and a count line had no denomination, no quantity and no variance.\n**The array is the transport; `CashCountLine` is the row.**\n",
  "items": {
   "$ref": "#/components/schemas/CashCountLine"
  },
  "minItems": 1
 },
 "DepositBox": {
  "type": "object",
  "x-ticvai-persistence": "orders.deposit_box + orders.deposit_box_opening_denomination + orders.deposit_box_foreign_holding",
  "description": "5.8. **Allocated to a cashier, not to a workstation.** A cashier moving between tills takes their float with them, which is what makes a variance attributable to a person.\n**`openingDenominations` and `foreignHoldings` are child rows** (26 September, pull audit R099): `orders.deposit_box_opening_denomination` and `orders.deposit_box_foreign_holding`, one row per item, keyed to the box. Until then the contract carried both and the table had nowhere to put either.\n",
  "required": [
   "cashierPrincipalId",
   "venueId",
   "openingFloat"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "cashierPrincipalId": {
    "type": "string",
    "format": "uuid"
   },
   "cashierName": {
    "type": "string",
    "readOnly": true
   },
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "workstationId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Where it is being used now. **Changes during a shift; the box does not.**"
   },
   "shiftId": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$",
    "nullable": true,
    "description": "The shift trading from this box. A ULID, as `Shift.id` is."
   },
   "status": {
    "$ref": "#/components/schemas/DepositBoxStatus"
   },
   "openingFloat": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "openingDenominations": {
    "type": "array",
    "description": "5.8.3. **Either this or a total** — a supervisor handing over a counted bag should not have to re-count it into fields. POS-001 offered only denominations until 14 August.\n",
    "items": {
     "type": "object",
     "required": [
      "denominationId",
      "count"
     ],
     "properties": {
      "denominationId": {
       "type": "string",
       "format": "uuid",
       "description": "References `platform.denomination`, as `CashCountLine.denominationId` does. Until 26 September this was `denomination: number` — a face value as a JSON float, which naming-and-style 5.1 forbids and which could disagree with the note it named (pull audit R122).\n"
      },
      "count": {
       "type": "integer",
       "minimum": 0
      }
     }
    }
   },
   "withdrawnTotal": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "readOnly": true,
    "description": "**Reduces the expected close figure.** Cash skimmed for banking is not a shortfall, and a system that treats it as one makes every busy cashier look short.\n"
   },
   "foreignHoldings": {
    "type": "array",
    "description": "4.6.11 and 6.1.10. **Foreign cash accepted at this till, counted separately by currency.** A till taking USD and EUR alongside AED has three counts and three variances — collapsing them into a base-currency total makes a variance unattributable to the currency that caused it.\n**No opening float in a foreign currency and no change given in one.** Foreign cash only ever comes in, which is what keeps this to one number per currency rather than a full reconciliation each.\n",
    "items": {
     "type": "object",
     "required": [
      "currency",
      "countedAmount"
     ],
     "properties": {
      "currency": {
       "type": "string",
       "pattern": "^[A-Z]{3}$",
       "description": "**Stored, because it is the one thing that is not the region's.** A foreign holding is by definition cash in a currency the till does not trade in, so it cannot resolve from the region (ADR-0018) the way the box's own amounts do; it is the key of the row, one per currency per box. The amounts on this item are in this currency.\n"
      },
      "expectedAmount": {
       "allOf": [
        {
         "$ref": "../shared/common.yaml#/components/schemas/Money"
        }
       ],
       "description": "The sum of tenders taken in this currency during the shift."
      },
      "countedAmount": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      },
      "variance": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      },
      "baseEquivalent": {
       "allOf": [
        {
         "$ref": "../shared/common.yaml#/components/schemas/Money"
        }
       ],
       "description": "**At the rates on the payments, not today's.** A shift closed on Friday and reviewed on Monday is reviewed at Friday's rates (CF-37).\n"
      }
     }
    }
   },
   "expectedTotal": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "countedTotal": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "variance": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "closedByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "**Flagged where it is not the holder.** A box closed without its holder present is allowed — the cash is counted by somebody, and who counted it is the record.\n"
   },
   "allocatedAt": {
    "type": "string",
    "format": "date-time",
    "description": "When the device recorded the allocation. `allocateDepositBox` is offline-capable, so for a box allocated offline this differs from the server's receipt time.\n"
   },
   "closedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   }
  }
 },
 "DepositBoxStatus": {
  "type": "string",
  "enum": [
   "allocated",
   "open",
   "suspended",
   "closing",
   "closed",
   "reconciled"
  ]
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
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$",
    "description": "Client-generated ULID of this exchange, and its idempotency key — it must equal the `Idempotency-Key` header."
   },
   "outgoingLineIds": {
    "type": "array",
    "minItems": 1,
    "items": {
     "type": "string",
     "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
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
 "ExecutionStatus": {
  "type": "string",
  "enum": [
   "queued",
   "running",
   "completed",
   "failed",
   "cancelled",
   "expired"
  ]
 },
 "ExportFormat": {
  "type": "string",
  "enum": [
   "csv",
   "xlsx",
   "pdf",
   "json"
  ]
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
    "$ref": "#/components/schemas/FinancialReportKind"
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
          "allOf": [
           {
            "$ref": "../shared/common.yaml#/components/schemas/Money"
           }
          ],
          "description": "The same line for **the same period last year** (decided 28 September, audit R127 (3)). Absent where that period did not exist."
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
 "FinancialReportKind": {
  "type": "string",
  "description": "The report `getFinancialReport` returns. One vocabulary for the query and the response.",
  "enum": [
   "profitAndLoss",
   "balanceSheet",
   "cashFlow",
   "revenueByVenue",
   "revenueByProduct",
   "taxSummary"
  ]
 },
 "GeneratedQuery": {
  "x-ticvai-persistence": "none — embedded; stored whole in `reporting.natural_language_query`",
  "type": "object",
  "description": "The structured query a natural-language question produced — data source, columns, filters, grouping. Named on 26 September so the answer and the kept copy are one shape.\n",
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
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$",
    "description": "Client-generated ULID of this discount, and its idempotency key — it must equal the `Idempotency-Key` header."
   },
   "lineId": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$",
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
   "description": {
    "type": "string",
    "description": "What the item is, in the guest's words. Indexed for guest-app search.\n"
   },
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
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "x-ticvai-column": "list_price"
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
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$",
    "description": "Client-generated ULID **of this modification, not of the order** — the order is the path's `orderId`. It is the modification's idempotency key and must equal the `Idempotency-Key` header.\n"
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
     "type": "string",
     "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
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
    "$ref": "#/components/schemas/GeneratedQuery",
    "description": "The structured query produced — data source, columns, filters, grouping. Returned so the answer can be checked. An answer nobody can verify is worse than no answer. **Also kept, as `NaturalLanguageQuery`**, for `saveNaturalLanguageQuery`.\n"
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
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
   },
   "shiftId": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
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
    "description": "When the device recorded it. `openShift` is online-only (F32), so this differs from server receipt time only by transit; it is kept because the shift's other device writes are ordered against it.\n"
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
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$",
    "description": "The client ULID from `CreateOrderRequest.id`."
   },
   "orderNumber": {
    "type": "string",
    "readOnly": true,
    "description": "The number a guest reads and a cashier types. **Server-assigned: the venue prefix and a sequence per venue**, for example `DXB1-000123` (decided 28 September, audit R152). A till holds a reserved range of the venue sequence, so an order taken offline gets its number on the till and keeps it through `syncOrders`. **Not gapless**: an unused reserved range leaves a gap, and that is allowed. Only tax invoices are gapless, per legal entity. The receipt carries this number.\n"
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
   "droppedPromotions": {
    "type": "array",
    "readOnly": true,
    "x-ticvai-persisted": false,
    "description": "**Promotions left off this order at checkout because their budget cap would have been exceeded** (decided 28 September, audit R101 (8)). Empty when none was dropped. Returned by `checkoutCart` and `createOrder`, not stored.\n",
    "items": {
     "type": "object",
     "required": [
      "promotionId"
     ],
     "properties": {
      "promotionId": {
       "type": "string",
       "format": "uuid"
      },
      "name": {
       "type": "string"
      },
      "reason": {
       "type": "string",
       "enum": [
        "budgetCapReached"
       ]
      }
     }
    }
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
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$",
    "nullable": true
   },
   "subjectId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "holdLabel": {
    "type": "string",
    "maxLength": 60,
    "nullable": true,
    "readOnly": true,
    "description": "The `label` a cashier gave when parking it with `holdOrder` — how they find it again. Null on an order never held."
   },
   "heldUntil": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true,
    "description": "When a held order expires and is voided (states/order.yaml), from `holdOrder`'s `holdUntil`. Null on an order not currently held."
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
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
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
     "type": "string",
     "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
    }
   },
   "revokedEntitlementIds": {
    "type": "array",
    "items": {
     "type": "string",
     "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
    }
   },
   "issuedEntitlementIds": {
    "type": "array",
    "items": {
     "type": "string",
     "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
    }
   }
  }
 },
 "OrderLine": {
  "x-ticvai-persistence": "orders.order_line + orders.order_line_eligibility",
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
      "description": "The entitlements this line issued. **These are the ticket ids** — `transferOrderTickets.ticketIds` and `reprintOrder.reissuedTicketIds` take and return them.",
      "items": {
       "type": "string",
       "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
      }
     },
     "crossRegionRightIds": {
      "type": "array",
      "items": {
       "type": "string"
      },
      "description": "Redemption rights propagated to other cells for this line."
     },
     "reprintCount": {
      "type": "integer",
      "minimum": 0,
      "default": 0,
      "readOnly": true,
      "description": "How many times this line's tickets were reprinted or resent. `reprintOrder` increments it; repeated reprints are the signal worth surfacing."
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
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$",
    "nullable": true
   },
   "revokedEntitlementIds": {
    "type": "array",
    "items": {
     "type": "string",
     "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
    }
   },
   "issuedEntitlementIds": {
    "type": "array",
    "items": {
     "type": "string",
     "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
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
       "type": "string",
       "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
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
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
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
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
   },
   "orderId": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
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
    "allOf": [
     {
      "$ref": "#/components/schemas/ExchangeRateDecimal"
     }
    ],
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
   "outletId": {
    "type": "string",
    "format": "uuid",
    "description": "The outlet whose price and stock this is: the asking workstation's outlet, or `outletId` for a caller with none (decided 28 September, audit R215).\n"
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
 "Recipient": {
  "x-ticvai-persistence": "reporting.schedule_recipient",
  "type": "object",
  "description": "One recipient of a schedule. **A row of `reporting.schedule_recipient`, a child of `reporting.schedule`** — `ReportSchedule` declares the pair, which is what gives the table its `schedule_id`. Pull audit 26 September: declared on its own, the table had no column tying a recipient to its schedule.\n",
  "required": [
   "kind",
   "address"
  ],
  "properties": {
   "kind": {
    "type": "string",
    "enum": [
     "principal",
     "email",
     "sftp",
     "webhook"
    ]
   },
   "address": {
    "type": "string"
   },
   "principalId": {
    "type": "string",
    "format": "uuid"
   }
  }
 },
 "RefundPolicy": {
  "x-ticvai-persistence": "orders.refund_policy + orders.refund_policy_time_band",
  "type": "object",
  "description": "Venue-configured. Thresholds are policy, not permission scope — venues run different policies and the permission model should not encode commercial rules.\n**The three thresholds must ascend** (decided 28 September, audit R123 (6)): `selfAuthoriseLimit` <= `requiresSecondUserAbove` <= `requiresApprovalAbove`, where the second is set. `setRefundPolicy` refuses a policy that does not with 422 `refund-thresholds-not-ascending`.\n",
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
    "format": "uuid",
    "readOnly": true,
    "description": "The venue in the path. Not taken from a `setRefundPolicy` body."
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
    "nullable": true,
    "minimum": 0,
    "description": "Days after purchase within which a refund may be made. 0 is allowed and means the day of purchase only; null means no window (decided 28 September, audit R123 (6))."
   },
   "varianceThreshold": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "description": "Price variance above this is an exception requiring review rather than a routine posting (CF-38). Venue-configured.\n**A venue setting with a tenant default** (decided 28 September, audit R094). **Proposed default, client to correct (audit R094): AED 5.00 per order line.**\n"
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
      "type": "string",
      "description": "The current version. Assigned by the server on each publish; earlier ones are kept as `ReportDefinitionVersion`."
     },
     "isSystem": {
      "type": "boolean",
      "description": "Shipped with the platform — seeded at provisioning (BL-053, `SeededReport`). **Clone-only (decided 28 September, audit R096)**: `updateReport` and `deleteReport` refuse it with 409 `system-report`; a venue changes a copy made with `createReport`.\n"
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
   "value": {
    "description": "**Open on purpose; its type is the field's.** One value, of the `FieldType` that `listReportFields` gives for `field` — a string, number, boolean, or a date, date-time or uuid as a string. Absent for `in`, `notIn`, `between`, `isNull` and `isNotNull`.\n"
   },
   "values": {
    "type": "array",
    "description": "The values for `in` and `notIn`, or exactly two (from, to) for `between`. Each of the field's `FieldType`, as `value`.",
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
   "defaultValue": {
    "description": "Open on purpose. A value of this parameter's `type`, used when a run supplies none."
   }
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
    "description": "**Open on purpose; the shape is `columns`.** Each row is keyed by `columns[].key`, and each value is of that column's `type` — money as a `Money`, dates, date-times and uuids as strings. A report's columns are chosen at run time, so no fixed schema can name them.\n",
    "items": {
     "type": "object",
     "additionalProperties": true
    }
   },
   "totals": {
    "type": "object",
    "additionalProperties": true,
    "description": "Aggregated columns only, keyed and typed as a row is."
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
 "ReportSchedule": {
  "x-ticvai-persistence": "reporting.schedule + reporting.schedule_recipient",
  "allOf": [
   {
    "$ref": "#/components/schemas/CreateReportScheduleRequest"
   },
   {
    "type": "object",
    "required": [
     "id",
     "ownerPrincipalId",
     "isPaused",
     "createdAt"
    ],
    "properties": {
     "id": {
      "type": "string",
      "format": "uuid"
     },
     "ownerPrincipalId": {
      "type": "string",
      "format": "uuid",
      "description": "The schedule runs under this principal's permissions, not the recipients'. A standing grant of whatever the owner can see.\n"
     },
     "isPaused": {
      "type": "boolean"
     },
     "lastRunAt": {
      "type": "string",
      "format": "date-time",
      "nullable": true
     },
     "lastRunStatus": {
      "$ref": "#/components/schemas/ExecutionStatus"
     },
     "nextRunAt": {
      "type": "string",
      "format": "date-time",
      "nullable": true
     },
     "consecutiveFailures": {
      "type": "integer"
     },
     "createdAt": {
      "type": "string",
      "format": "date-time"
     }
    }
   }
  ]
 },
 "RunReportRequest": {
  "x-ticvai-persistence": "none — request only",
  "type": "object",
  "properties": {
   "parameters": {
    "type": "object",
    "additionalProperties": true,
    "description": "**Open on purpose; its shape is the report's.** Keyed by `ReportParameter.key` of the definition being run, each value of that parameter's `type`. An `isRequired` parameter with no value here and no `defaultValue` is the `400` `runReport` lists.\n"
   },
   "venueId": {
    "type": "string",
    "format": "uuid",
    "description": "Narrows to one venue. Omitting it returns everything the caller's scope permits — it cannot be used to reach beyond that.\n"
   },
   "dateFrom": {
    "type": "string",
    "format": "date",
    "description": "Defaults to today in the venue's time zone when not sent (decided 28 September, audit R158)."
   },
   "dateTo": {
    "type": "string",
    "format": "date",
    "description": "Defaults to today in the venue's time zone when not sent (audit R158)."
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
   "currencyCode": {
    "type": "string",
    "pattern": "^[A-Z]{3}$",
    "description": "**A settlement has no account, so nothing else denominates it.** A posting takes its currency from `ledger.account.currency` and a payment from `tenderCurrency`, but a settlement is a provider file for a period: `providerGross`, `ledgerGross` and `difference` are bare amounts, and a provider file in one currency against a ledger in another computes a difference that means nothing. Added 20 September, when a venue became able to trade outside its region's currency.\n"
   },
   "providerName": {
    "type": "string"
   },
   "venueId": {
    "type": "string",
    "format": "uuid",
    "description": "The venue this settlement is for. **Reconciled daily per venue** (decided 28 September, audit R110 (b)), so `periodStart` and `periodEnd` are the same day."
   },
   "periodStart": {
    "type": "string",
    "format": "date",
    "description": "A day in the region's time zone, local midnight to local midnight."
   },
   "periodEnd": {
    "type": "string",
    "format": "date",
    "description": "A day in the region's time zone, local midnight to local midnight."
   },
   "fileReference": {
    "type": "string",
    "format": "uuid",
    "description": "The `MediaAsset` holding the provider file, as given to `ingestSettlementFile`. **Kept on the row because parsing is asynchronous**: the job that parses the file reads it from here.\n"
   },
   "format": {
    "type": "string",
    "nullable": true,
    "enum": [
     "csv",
     "fixedWidth",
     "xml",
     "json"
    ],
    "description": "The file format given at ingest. Null when none was given."
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
    "readOnly": true,
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
    "type": "string",
    "format": "uuid",
    "description": "Server-created when parsing finds the exception, so a UUID (naming-and-style 4)."
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
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$",
    "nullable": true
   },
   "amount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "expectedAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "resolution": {
    "allOf": [
     {
      "$ref": "#/components/schemas/SettlementResolution"
     }
    ],
    "nullable": true,
    "description": "Null while the exception is open."
   },
   "note": {
    "type": "string",
    "nullable": true,
    "description": "The `note` given to `resolveSettlementException`, stored with the resolution."
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
 "SettlementResolution": {
  "type": "string",
  "description": "How a settlement exception was explained. One vocabulary for the request and the stored exception.",
  "enum": [
   "matchedManually",
   "writeOff",
   "disputeRaised",
   "providerError",
   "timingDifference"
  ]
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
  "x-ticvai-persistence": "orders.pos_shift + orders.pos_shift_approval + orders.pos_shift_incident",
  "description": "**`approvals` and `incidents` are child rows** (26 September, pull audit R099): `orders.pos_shift_approval` and `orders.pos_shift_incident`, one row per item, keyed to the shift. Until then the contract carried both and `orders.pos_shift` had nowhere to put either.\n",
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
    "x-ticvai-column": "gross_sales_amount",
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "What the till took in sales, as the guest paid it — tax included."
   },
   "refundsTotal": {
    "x-ticvai-column": "gross_refunded_amount",
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "What the till paid back, as the guest was refunded it — tax included."
   },
   "liftsTotal": {
    "x-ticvai-column": "lifted_amount",
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Cash taken out mid-shift by lifts and withdrawals. Cash, so neither gross nor net."
   },
   "expectedCash": {
    "x-ticvai-column": "expected_cash_amount",
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "readOnly": true,
    "nullable": true,
    "description": "26 September, pull audit R207. **The figure the blind count was measured against**, revealed once the count is in — null until then. Until this date only `ShiftCloseResult` carried it, returned once by `closeShift`, so BO-040 could not show the over/short it exists to accept.\n"
   },
   "countedCash": {
    "x-ticvai-column": "counted_cash_amount",
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "readOnly": true,
    "nullable": true,
    "description": "What the close count found. Null until the shift is counted."
   },
   "variance": {
    "x-ticvai-column": "variance_amount",
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "readOnly": true,
    "nullable": true,
    "description": "Counted minus expected, as `ShiftCloseResult.variance`. Negative is short."
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
    "description": "When the device recorded the open. `openedAt` is the server's time."
   },
   "suspendedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "suspendReason": {
    "type": "string",
    "maxLength": 200,
    "nullable": true,
    "description": "The `reason` given to `suspendShift`. Cleared on resume."
   },
   "closedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "closedByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Who submitted the close count. `reopenShift` refuses an approver who is this principal, and until 26 September there was nothing to compare against (pull audit R099).\n"
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
       ],
       "description": "`open` from `approveShiftOpen`, `close` from `approveShiftClose`, `variance` from `acceptShiftVariance`.\n"
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
    "description": "True when the variance exceeds the venue's `shiftVarianceThreshold` (audit R094). The shift is then `pendingVariance` and only `acceptShiftVariance` finalises it (audit R080 (e)).\n"
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
  "description": "`wallet` is a **digital wallet** (Apple Pay, Google Pay and the like, taken through the gateway), the value the guest channels accept beside `card` (decided 28 September, audit R080 (a)). **The stored-value TICVAI wallet is a separate tender**: it is spent through `authoriseStoredValue` and `captureStoredValue` (`StoredValueKind` `wallet`), never as this value, so the client can see which of the two the decision meant.\n",
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
 },
 "VenueSettings": {
  "type": "object",
  "x-ticvai-persistence": "platform.venue_settings",
  "description": "**Venue-level operational configuration that no other level can answer.**\nRegion owns currency, tax regime and fiscal year (ADR-0011). Venue owns the things that vary between two venues in one region — **opening hours, support hours, and what the local law requires of the gate.**\n**And the configured limits** (decided 28 September, audit R094): every limit the contracts call *configured* is a field here, from `displayCurrencies` and `cartLeaseSeconds` down to the grouped `catalogue`, `inventory`, `seating`, `promotions`, `fnb`, `queue`, `reporting`, `marketing` and `identity` settings. **Each has a tenant-level default**: the tenant sets it once with `setVenueSettingsDefaults`, a venue overrides it within the field's bounds, and a null field here inherits it. Each field's `default` is the proposed tenant default, marked proposed, client to correct (audit R094); `docs/active/configured-limits-proposal.md` is the sheet the client corrects, and where the two differ this contract is what runs.\n",
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "description": "**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"
   },
   "venueId": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "description": "From the path of `setVenueSettings`."
   },
   "currencyCode": {
    "type": "string",
    "pattern": "^[A-Z]{3}$",
    "nullable": true,
    "readOnly": true,
    "description": "**`readOnly` is the freeze.** `setVenueSettings` takes this whole schema as its request body, so without it any settings save could rewrite the currency of a venue that had already traded — which is the one thing ADR-0018's amendment forbids. It is set when the venue is provisioned, defaulted from the region, and changed only by an operation whose precondition is that the venue has not yet traded.\n**The venue's trading currency, defaulted from its region and frozen once the venue has traded** (ADR-0018, amended 20 September). Currency was a region-only fact, grouped with tax rates on the reasoning that *\"a venue cannot choose its VAT\"* -- true of tax and over-applied to currency, because a free-zone unit, a duty-free shop and a cruise terminal genuinely trade in a currency their region does not.\n**This column exists because the freeze needs somewhere to live.** A venue that resolved purely from its region would silently follow a region currency change after it had already traded, and every dated artefact beneath it -- a price list is a `validFrom`/`validTo` range -- would render retrospectively wrong. Null means \"resolve from the region\", which is the answer for every venue that has not overridden.\n"
   },
   "currencyScale": {
    "type": "integer",
    "minimum": 0,
    "maximum": 4,
    "nullable": true,
    "readOnly": true,
    "description": "**Scale travels with currency** (ADR-0008), and so does the freeze. OMR is three decimal places because Oman says so; overriding the currency without the scale gets rounding wrong. Set together or not at all.\n"
   },
   "supportHours": {
    "type": "object",
    "description": "CF-100. **A venue decides whether its support desk is 24/7 or bounded, and the platform does not.** This was recorded as an open question for eleven days and was never one — the code is identical either way, and what was missing was somewhere to put the answer.\n",
    "properties": {
     "mode": {
      "type": "string",
      "enum": [
       "alwaysOn",
       "businessHours",
       "custom",
       "none"
      ]
     },
     "timezone": {
      "type": "string",
      "description": "IANA zone the `windows` are read in. Absent, they are read in the region's `timeZone`, like every other wall-clock time in this contract.\n"
     },
     "windows": {
      "type": "array",
      "items": {
       "type": "object",
       "properties": {
        "day": {
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
        "from": {
         "type": "string",
         "description": "Wall-clock time the desk opens."
        },
        "to": {
         "type": "string",
         "description": "Wall-clock time the desk closes."
        }
       }
      }
     },
     "outOfHoursMessage": {
      "type": "string",
      "nullable": true
     }
    }
   },
   "quietHours": {
    "type": "object",
    "nullable": true,
    "description": "**When the platform does not send.** A wallet low-balance alert at 3am is a complaint, and journeys and message triggers both respect this.\n**Operational messages ignore it** — a queue-turn alert is why a guest is holding the phone.\n",
    "properties": {
     "from": {
      "type": "string",
      "description": "Wall-clock time sending stops",
      "in the region's time zone.": null
     },
     "to": {
      "type": "string",
      "description": "Wall-clock time sending resumes",
      "in the region's time zone.": null
     }
    }
   },
   "biometrics": {
    "type": "object",
    "nullable": true,
    "description": "CF-35, BL-096, BL-105, BL-106. **The venue-level master switch, and the one place a person is asked whether the paperwork exists.** Biometric data is sensitive under PDPL (Federal Decree-Law 45/2021) — heightened protection, explicit consent, and an Article 21 assessment before the processing rather than after it.\n**Nothing below this switch operates while it is off.** `AdmissionRules` may carry a `biometricPolicy` per ticket type and those rules are inert until a venue enables biometrics here, which means a profile copied between venues cannot start capturing faces at the destination.\n**Venue level because that is where the assessment is filed.** Region owns tax and currency; the DPIA, the consent notice and the hardware are a venue's.\n",
    "properties": {
     "isEnabled": {
      "type": "boolean",
      "default": false,
      "description": "**Off by default, and turning it on is refused without the two fields below.** `setVenueSettings` answers 422 rather than accepting an enable it cannot evidence — **a DPIA nobody can name is a DPIA nobody did**, and the point of the refusal is that the person switching this on is asked at the moment they switch it on rather than by an auditor a year later.\n"
     },
     "dpiaReference": {
      "type": "string",
      "nullable": true,
      "maxLength": 200,
      "description": "**The venue's own reference for its Article 21 assessment.** The platform does not hold the document and does not judge it; it records that one was named, by whom, and when — which is what an audit asks for and what the venue can produce.\n"
     },
     "consentNoticeAcknowledgedAt": {
      "type": "string",
      "format": "date-time",
      "nullable": true,
      "description": "**When somebody confirmed the consent forms are in place at the point of capture.** A guest consenting in an app is a record; a guest consenting at a ticket counter is a notice somebody has to have printed and a question somebody has to have asked.\n"
     },
     "acknowledgedByPrincipalId": {
      "type": "string",
      "format": "uuid",
      "nullable": true,
      "readOnly": true,
      "description": "**Who confirmed it.** An acknowledgement with no name behind it cannot be followed up, and this is the field that makes the switch an act rather than a setting. Recorded by the server as the caller whose save carried the acknowledgement, so it cannot name somebody else.\n"
     },
     "faceTagPurgeMinutesAfterClose": {
      "type": "integer",
      "nullable": true,
      "default": 0,
      "description": "BL-106. **How long a same-visit Face Tag survives past the close of the operating day**, and zero is the default because that is what 3.2.44 describes. A non-zero value is an operational allowance for a late reconciliation, not a retention period — **`facePass` ignores this entirely** and is bounded by its entitlement.\n"
     }
    }
   },
   "segregatedAccess": {
    "type": "object",
    "nullable": true,
    "description": "CF-130. **Configured at venue level because it changes by region and the venue is where it is known** — a Ladies Night, a family session, a prayer-time closure.\n**The platform does not infer gender.** 3.2.45 asks for automatic gender recognition and 3.2.46 for rule-based facial recognition validation, and neither is built. Two reasons, and the second is the one that decided it:\n**A Ladies Night ticket is already gendered at the point of sale**, so the gate checks the entitlement the platform issued rather than the face in front of it — deterministic, auditable, and already contracted through `admissionRules`.\n**And these events are staffed.** A steward at the entrance is making the judgment anyway, and a classifier that overrules a person who can see more than it can is a machine and a human disagreeing while a guest waits.\n**`genderVerification` is a switch, not an implementation.** Where a venue's access hardware offers the capability and the venue chooses to use it, this turns it on — following ADR-0015's standards-first driver model, where the device does what the device does. **Not everything needs to be built.**\n",
    "properties": {
     "isEnabled": {
      "type": "boolean",
      "default": false
     },
     "appliesToAccessPointIds": {
      "type": "array",
      "items": {
       "type": "string",
       "format": "uuid"
      }
     },
     "schedule": {
      "type": "array",
      "items": {
       "type": "object",
       "properties": {
        "day": {
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
        "from": {
         "type": "string",
         "description": "Wall-clock time",
         "in the region's time zone.": null
        },
        "to": {
         "type": "string",
         "description": "Wall-clock time",
         "in the region's time zone.": null
        },
        "admits": {
         "type": "string",
         "enum": [
          "all",
          "women",
          "womenAndChildren",
          "families",
          "members"
         ]
        }
       }
      }
     },
     "entitlementGated": {
      "type": "boolean",
      "default": true,
      "readOnly": true,
      "description": "**Always true, and stated rather than assumed.** The gate admits on the entitlement. Everything below is advisory on top of that, and nothing replaces it.\n"
     },
     "genderVerification": {
      "type": "string",
      "enum": [
       "off",
       "staffAssisted",
       "deviceAssisted"
      ],
      "default": "off",
      "description": "`off` — the entitlement decides and a steward handles exceptions. **The default, and what is contracted.**\n`staffAssisted` — the steward's screen shows the ticket type so they can ask. No inference anywhere.\n`deviceAssisted` — **the venue's access hardware performs the check, not the platform.** Available only where the driver reports the capability, and the result is **advisory to the steward rather than decisive at the turnstile** (3.2.45 asks for rejection; this deviates deliberately).\n"
     },
     "overrideRateAlertThreshold": {
      "type": "number",
      "nullable": true,
      "description": "Where `deviceAssisted` is on. **An override rate near zero means the steward has stopped deciding**, and that is the number that says whether the human safeguard is working or decorative.\n"
     }
    }
   },
   "alerting": {
    "type": "object",
    "description": "CF-134. **On-platform notification, marked as read.** Six contracts detect their own trouble and none told a person.\n**The panel is the default and email or WhatsApp only where the matrix names them** — an operational alert that arrives by email is an alert nobody sees in time.\n",
    "properties": {
     "channel": {
      "type": "string",
      "enum": [
       "dashboardPanel",
       "dashboardAndEmail",
       "dashboardAndWhatsapp"
      ],
      "default": "dashboardPanel"
     },
     "acknowledgementRequired": {
      "type": "boolean",
      "default": true
     },
     "escalateAfterMinutes": {
      "type": "integer",
      "nullable": true
     }
    }
   },
   "displayCurrencies": {
    "type": "array",
    "nullable": true,
    "description": "**Which currencies this venue shows guests** (decided 28 September, audit R120 (a)). ISO 4217 codes, each one its region holds an `FxRate` for; the rate itself stays per region and is never set here. `finance.listFxRates` with `venueId` narrows the region's rates to these. Null or empty shows the trading currency only. A code the region has no rate for is refused `400`.\n",
    "items": {
     "type": "string",
     "pattern": "^[A-Z]{3}$"
    }
   },
   "cartLeaseSeconds": {
    "type": "integer",
    "nullable": true,
    "minimum": 30,
    "maximum": 3600,
    "default": 900,
    "description": "**How long a cart holds capacity** (decided 28 September, audit R169): 15 minutes, the default `catalogue.acquireInventoryHold` takes for `ttlSeconds`. Proposed, client to correct (audit R094).\n"
   },
   "cartHoldExtensionMinutes": {
    "type": "integer",
    "nullable": true,
    "minimum": 1,
    "maximum": 30,
    "default": 5,
    "description": "How long one `orders.extendCart` extension adds. Proposed, client to correct (audit R094)."
   },
   "cartMaxExtensions": {
    "type": "integer",
    "nullable": true,
    "minimum": 0,
    "maximum": 5,
    "default": 1,
    "description": "How many extensions a cart may take before `extensionCapReached` (`Cart.maxExtensions`). Proposed, client to correct (audit R094)."
   },
   "resaleCutoffHours": {
    "type": "integer",
    "nullable": true,
    "minimum": 0,
    "maximum": 168,
    "default": 24,
    "description": "Hours before the performance after which a ticket can no longer be listed for resale (`orders.createResaleListing`). Proposed, client to correct (audit R094)."
   },
   "exchangeCutoffHours": {
    "type": "integer",
    "nullable": true,
    "minimum": 0,
    "maximum": 720,
    "default": 24,
    "description": "Hours before the original performance after which lines can no longer be exchanged (`orders.exchangeOrderLines`, `outsideExchangeWindow`). Proposed, client to correct (audit R094)."
   },
   "rescheduleCutoffHours": {
    "type": "integer",
    "nullable": true,
    "minimum": 0,
    "maximum": 720,
    "default": 24,
    "description": "Hours before the original performance after which an order can no longer be rescheduled (`orders.rescheduleOrder`, `outsideRescheduleWindow`). Proposed, client to correct (audit R094)."
   },
   "reservationMaxExtensions": {
    "type": "integer",
    "nullable": true,
    "minimum": 0,
    "maximum": 5,
    "default": 1,
    "description": "How many times `orders.extendReservation` may extend one reservation. Proposed, client to correct (audit R094)."
   },
   "shiftVarianceThreshold": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "nullable": true,
    "description": "Over or short at shift close beyond which the shift waits in `pendingVariance` for `shift.acceptShiftVariance`. **Proposed tenant default AED 20.00, bounds 0 to 1,000 in the venue currency; client finance to correct (audit R094).**\n"
   },
   "catalogue": {
    "type": "object",
    "nullable": true,
    "properties": {
     "maxVariantsPerProduct": {
      "type": "integer",
      "nullable": true,
      "minimum": 1,
      "maximum": 2000,
      "default": 200,
      "description": "Variants one product may generate from its attributes (`setProductAttributes` refuses above it). Proposed, client to correct (audit R094)."
     },
     "waitlistOfferHoldMinutes": {
      "type": "integer",
      "nullable": true,
      "minimum": 1,
      "maximum": 1440,
      "default": 30,
      "description": "How long a waitlist offer holds the released capacity for the guest it was offered to. Proposed, client to correct (audit R094)."
     },
     "bulkPriceChangeEscalationPercent": {
      "type": "number",
      "nullable": true,
      "minimum": 0,
      "maximum": 100,
      "default": 10,
      "description": "A `bulkChangePrices` run changing any price by more than this percentage needs `PRICE_CONFIGURE` (audit R197). Proposed, client to correct (audit R094)."
     },
     "bulkPriceChangeEscalationCount": {
      "type": "integer",
      "nullable": true,
      "minimum": 1,
      "default": 50,
      "description": "A `bulkChangePrices` run touching more prices than this needs `PRICE_CONFIGURE` (audit R197). Proposed, client to correct (audit R094)."
     }
    }
   },
   "inventory": {
    "type": "object",
    "nullable": true,
    "properties": {
     "overReceiptTolerancePercent": {
      "type": "number",
      "nullable": true,
      "minimum": 0,
      "maximum": 25,
      "default": 5,
      "description": "Percent above the outstanding ordered quantity a goods receipt line may record (`createGoodsReceipt`). Proposed, client to correct (audit R094)."
     },
     "countVarianceTolerancePercent": {
      "type": "number",
      "nullable": true,
      "minimum": 0,
      "maximum": 25,
      "default": 2,
      "description": "Percent difference between counted and expected quantity before a count line is an exception (`getCountVariance`). Proposed, client to correct (audit R094)."
     },
     "countVarianceApprovalAmount": {
      "allOf": [
       {
        "$ref": "../shared/common.yaml#/components/schemas/Money"
       }
      ],
      "nullable": true,
      "description": "Total variance value of a count above which posting it needs approval (`postStockCount`). **Proposed tenant default 1,000.00 in the venue currency, client finance to correct (audit R094).**\n"
     }
    }
   },
   "seating": {
    "type": "object",
    "nullable": true,
    "properties": {
     "seatHoldExtensionSeconds": {
      "type": "integer",
      "nullable": true,
      "minimum": 60,
      "maximum": 1800,
      "default": 300,
      "description": "What one `extendSeatHold` adds. No hold outlives 30 minutes in all (audit R169). Proposed, client to correct (audit R094)."
     },
     "seatHoldMaxExtensions": {
      "type": "integer",
      "nullable": true,
      "minimum": 0,
      "maximum": 5,
      "default": 2,
      "description": "How many times a seat hold may be extended. Proposed, client to correct (audit R094). A resource hold on a venue map (`resources.extendResourceHold`) uses the same two bounds (decided 29 September, rev 3 REV3-15)."
     },
     "maxSeatsPerGuestOrder": {
      "type": "integer",
      "nullable": true,
      "minimum": 1,
      "maximum": 50,
      "default": 10,
      "description": "**Seats one guest may take in one booking on a guest channel** (Guest Web, Guest App), decided 29 September, rev 3 REV3-7. `seating.createSeatHold` counts the seats in the request plus the seats the same guest already holds on the same performance, and refuses above this with `422` `seat-limit-exceeded`, naming the limit. Default 10, bounds 1 to 50; a venue sets its own in Venue Management. Staff and POS sales keep 10 per sale (audit R080 (c)) and do not read this field.\n"
     }
    }
   },
   "promotions": {
    "type": "object",
    "nullable": true,
    "properties": {
     "maxDiscountPercent": {
      "type": "number",
      "nullable": true,
      "minimum": 0,
      "maximum": 100,
      "default": 30,
      "description": "The largest discount one promotion may give (`createPromotion` refuses above it). Proposed, client to correct (audit R094)."
     },
     "nearZeroLinePrice": {
      "allOf": [
       {
        "$ref": "../shared/common.yaml#/components/schemas/Money"
       }
      ],
      "nullable": true,
      "description": "Net line price below which a stacked combination is flagged near-zero in `analysePromotionConflicts` (audit R096 (5)); a warning, not a refusal. **Proposed tenant default AED 1.00, client to correct (audit R094).**\n"
     }
    }
   },
   "fnb": {
    "type": "object",
    "nullable": true,
    "properties": {
     "recallWindowMinutes": {
      "type": "integer",
      "nullable": true,
      "minimum": 0,
      "maximum": 60,
      "default": 10,
      "description": "Minutes after a bump during which `recallKitchenTicket` still recalls; after it the act is a refire. Proposed, client to correct (audit R094)."
     },
     "compEscalationAmount": {
      "allOf": [
       {
        "$ref": "../shared/common.yaml#/components/schemas/Money"
       }
      ],
      "nullable": true,
      "description": "Line value above which `compItem` needs `ORDER_DISCOUNT` (audit R197). **Proposed tenant default AED 100.00, client to correct (audit R094).**\n"
     },
     "foodSafetyLeadPrincipalId": {
      "type": "string",
      "format": "uuid",
      "nullable": true,
      "description": "**The venue's food-safety lead**, to whom `escalateCorrectiveAction` sends every escalation (decided 28 September, audit R096 (9)). A venue fact, so it has no tenant default; while it is null an escalation is refused `409 no-food-safety-lead`.\n"
     }
    }
   },
   "queue": {
    "type": "object",
    "nullable": true,
    "properties": {
     "crossQueueLimit": {
      "type": "integer",
      "nullable": true,
      "minimum": 1,
      "maximum": 10,
      "default": 2,
      "description": "Virtual queues one guest party may wait in at once (`joinQueue`, `crossQueueLimitReached`). Proposed, client to correct (audit R094)."
     }
    }
   },
   "reporting": {
    "type": "object",
    "nullable": true,
    "properties": {
     "inlineRunRowLimit": {
      "type": "integer",
      "nullable": true,
      "minimum": 1000,
      "maximum": 100000,
      "default": 5000,
      "description": "Estimated rows above which `runReport` answers `202` and runs in the background. Proposed, client to correct (audit R094)."
     },
     "dashboardRefreshBudgetPerMinute": {
      "type": "integer",
      "nullable": true,
      "minimum": 1,
      "default": 24,
      "description": "Tile refreshes per minute, summed over a dashboard's tiles, that `createDashboard` allows. Proposed, client to correct (audit R094)."
     }
    }
   },
   "marketing": {
    "type": "object",
    "nullable": true,
    "properties": {
     "attributionWindowDays": {
      "type": "integer",
      "nullable": true,
      "minimum": 1,
      "maximum": 30,
      "default": 7,
      "description": "Days after a campaign touch within which a booking is attributed to it (`getCampaignPerformance`). Proposed, client to correct (audit R094)."
     }
    }
   },
   "identity": {
    "type": "object",
    "nullable": true,
    "properties": {
     "guestOtpMaxAttempts": {
      "type": "integer",
      "nullable": true,
      "minimum": 3,
      "maximum": 10,
      "default": 5,
      "description": "Wrong entries allowed per guest one-time code before `verifyGuestOtp` invalidates it. A guest code is tenant-scoped, so the tenant default is the value used. Proposed, client to correct (audit R094).\n"
     },
     "guestTwoStep": {
      "type": "object",
      "nullable": true,
      "description": "**Guest two-step verification: a venue option, off unless the venue enables it in Venue Management** (decided 29 September, rev 3 GAP-B1, per venue, superseding the second part of audit R167, \"no guest MFA\"; an earlier draft of the same day put it on the tenant's `PasswordPolicy`, which no longer carries it). **The guest's enrolment stays tenant-wide**: one guest account across the tenant's venues, so a method enrolled once is used in every venue that has this on, and is never asked in a venue that has it off. Identity learns the venue from `venueId` on the guest sign-in (`verifyGuestOtp`, `guestPasswordLogin`, `guestSocialLogin`, `guestUaePassLogin`) and on `createMfaChallenge`: the venue the guest app or booking is in; with no venue given, an enrolled guest is asked when any venue of the tenant has it on. Guests may enrol `totp` with `emailOtp` as the fallback, as staff do (audit R126 (5)); it is never forced. Guests still never use enterprise SSO (R167, first part). A null inherits the tenant default set with `setVenueSettingsDefaults`.\n",
      "properties": {
       "enabled": {
        "type": "boolean",
        "default": false,
        "description": "Off unless the venue enables it. While no venue of the tenant has it on, guests cannot enrol (`enrolMfaMethod` answers 403 `guest-two-step-disabled`)."
       },
       "stepUpActions": {
        "type": "array",
        "uniqueItems": true,
        "description": "The guest actions in this venue that ask an enrolled guest for the factor again, whatever the age of the session. The service performing the action passes this venue to `createMfaChallenge`. Proposed, client to correct (rev 3 GAP-B1).\n",
        "items": {
         "type": "string",
         "enum": [
          "changeContactDetails",
          "changePassword",
          "managePaymentMethods",
          "transferTickets",
          "deleteAccount"
         ]
        },
        "default": [
         "changeContactDetails",
         "changePassword",
         "managePaymentMethods",
         "deleteAccount"
        ]
       }
      }
     }
    }
   }
  }
 },
 "WithdrawalReason": {
  "type": "string",
  "description": "Why a supervisor took cash out of a box. Set only on lifts `withdrawFromDepositBox` records.",
  "enum": [
   "banking",
   "safeDrop",
   "changeOrder",
   "other"
  ]
 }
}
```
