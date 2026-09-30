# WS178 — TICVAI Finance Backend Structure Reference v1.0 board 1

**1 screens · 5 operations · 13 schemas · 2 permissions**

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

- **Every control that can be refused must be gated.** 2 permissions apply here:
  `LEDGER_VIEW, REPORT_VIEW_VENUE`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `BO-1081` | Finance Dashboard | listDetail | 5 | 0 | — |

## Thin screens in this batch

**BO-1081 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "BO-1081",
  "name": "Finance Dashboard",
  "module": "Orders & Money",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "TICVAI Finance Backend Structure Reference v1.0.pdf",
   "board": "1",
   "number": "1",
   "page": 106
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/orders-money/finance-dashboard-bo-1081",
   "component": "apps/venue-management-web/src/routes/orders-money/FinanceDashboard.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-100"
   ],
   "exitTo": [
    "BO-100"
   ],
   "transitions": [
    {
     "to": "BO-100",
     "trigger": "Back to Venue Home",
     "provenance": "structural — pack board 1 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Finance Dashboard",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack TICVAI Finance Backend Structure Reference v1.0.pdf, page 106"
   }
  ],
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "filters",
     "components": [
      {
       "kind": "searchField",
       "label": "Search finance",
       "provenance": "pack TICVAI Finance Backend Structure Reference v1.0.pdf, page 106 §Global filters"
      },
      {
       "kind": "multiSelect",
       "label": "Filter by",
       "columns": [
        "Company: UAE01",
        "Site: All Sites",
        "Attraction: All",
        "Currency: AED",
        "Period: August 2026"
       ],
       "notes": "The pack filters this screen by company: uae01, site: all sites, attraction: all, currency: aed, period: august 2026 — which are present is a decision the pack already made.",
       "provenance": "pack TICVAI Finance Backend Structure Reference v1.0.pdf, page 106 §Global filters"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The finance list.",
   "error": "Could not load. Names which read failed and leaves the finance untouched.",
   "emptyFirstRun": "No finance yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the finance are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getKpiValues",
    "contract": "reporting",
    "purpose": "Finance KPIs against target",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "getUnifiedReconciliation",
    "contract": "finance",
    "purpose": "Where the money stands",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "listTaxInvoices",
    "contract": "finance",
    "purpose": "List tax invoices",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "listCreditMemos",
    "contract": "finance",
    "purpose": "List credit memos",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "listEInvoiceTransmissions",
    "contract": "finance",
    "purpose": "E-invoicing transmission log and failures",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-1081",
   "workshopBoard": "wireframes/WS163 TICVAI Finance Backend Structure Reference v1.0 Board 1.dc.html#bo-1081"
  },
  "apisNote": "Regenerated 9 September 2026 from TICVAI Finance Backend Structure Reference v1.0.pdf page 106. 0 of 5 labels bound to a contract property; 5 of 28 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
 "getKpiValues": {
  "method": "GET",
  "path": "/kpi-values",
  "contract": "reporting",
  "summary": "Current values, against target, with movement",
  "permission": "REPORT_VIEW_VENUE",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "kpiIds",
    "in": "query",
    "required": null
   },
   {
    "name": "kpiCodes",
    "in": "query",
    "required": null
   },
   {
    "name": "scopePath",
    "in": "query",
    "required": null
   },
   {
    "name": "period",
    "in": "query",
    "required": null
   },
   {
    "name": "compareTo",
    "in": "query",
    "required": null
   },
   {
    "name": "interval",
    "in": "query",
    "required": null
   },
   {
    "name": "groupBy",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "KpiValue"
 },
 "getUnifiedReconciliation": {
  "method": "GET",
  "path": "/reconciliation/unified",
  "contract": "finance",
  "summary": "Every money source against the ledger, in one view",
  "permission": "LEDGER_VIEW",
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
   }
  ],
  "requestBody": null,
  "responds": "UnifiedReconciliation"
 },
 "listCreditMemos": {
  "method": "GET",
  "path": "/credit-memos",
  "contract": "finance",
  "summary": "Credit memos issued, newest first",
  "permission": "LEDGER_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "region",
  "parameters": [
   {
    "name": "taxInvoiceId",
    "in": "query",
    "required": null
   },
   {
    "name": "refundId",
    "in": "query",
    "required": null
   },
   {
    "name": "legalEntityId",
    "in": "query",
    "required": null
   },
   {
    "name": "issuedFrom",
    "in": "query",
    "required": null
   },
   {
    "name": "issuedTo",
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
 "listEInvoiceTransmissions": {
  "method": "GET",
  "path": "/e-invoicing/transmissions",
  "contract": "finance",
  "summary": "What was sent to the e-invoicing provider, and what came back",
  "permission": "LEDGER_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "region",
  "parameters": [
   {
    "name": "legalEntityId",
    "in": "query",
    "required": null
   },
   {
    "name": "status",
    "in": "query",
    "required": null
   },
   {
    "name": "documentId",
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
 "listTaxInvoices": {
  "method": "GET",
  "path": "/tax-invoices",
  "contract": "finance",
  "summary": "Tax invoices issued, newest first",
  "permission": "LEDGER_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "region",
  "parameters": [
   {
    "name": "orderId",
    "in": "query",
    "required": null
   },
   {
    "name": "legalEntityId",
    "in": "query",
    "required": null
   },
   {
    "name": "invoiceType",
    "in": "query",
    "required": null
   },
   {
    "name": "status",
    "in": "query",
    "required": null
   },
   {
    "name": "issuedFrom",
    "in": "query",
    "required": null
   },
   {
    "name": "issuedTo",
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
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "FinCreditMemo": {
  "x-ticvai-persistence": "ledger.credit_memo + ledger.credit_memo_line",
  "type": "object",
  "description": "5.7.94. **A tax credit note against one tax invoice**, with its own series. Never edited.",
  "required": [
   "id",
   "creditMemoNumber",
   "taxInvoiceId",
   "kind",
   "reason",
   "legalEntityId",
   "issuedAt",
   "currency",
   "netAmount",
   "taxAmount",
   "grossAmount",
   "lines"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "creditMemoNumber": {
    "type": "string",
    "readOnly": true,
    "description": "Server-assigned from the legal entity's credit memo series, in sequence without gaps."
   },
   "taxInvoiceId": {
    "type": "string",
    "format": "uuid"
   },
   "taxInvoiceNumber": {
    "type": "string",
    "readOnly": true
   },
   "kind": {
    "type": "string",
    "enum": [
     "full",
     "partial"
    ]
   },
   "reason": {
    "type": "string",
    "enum": [
     "refund",
     "cancellation",
     "priceAdjustment",
     "returnOfGoods",
     "billingError",
     "other"
    ]
   },
   "refundId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "cancelledOrderId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "legalEntityId": {
    "type": "string",
    "format": "uuid"
   },
   "buyerSubjectId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "issuedAt": {
    "type": "string",
    "format": "date-time"
   },
   "currency": {
    "type": "string",
    "pattern": "^[A-Z]{3}$"
   },
   "netAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "taxAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "grossAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "taxAmountInLegalCurrency": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "note": {
    "type": "string",
    "nullable": true
   },
   "renditionAssetId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true
   },
   "eInvoiceStatus": {
    "$ref": "#/components/schemas/FinEInvoiceTransmissionStatus"
   },
   "issuedByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true
   },
   "lines": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/FinCreditMemoLine"
    }
   },
   "scopePath": {
    "type": "string",
    "readOnly": true
   }
  }
 },
 "FinCreditMemoLine": {
  "type": "object",
  "required": [
   "invoiceLineNumber",
   "netAmount",
   "taxAmount",
   "grossAmount"
  ],
  "properties": {
   "invoiceLineNumber": {
    "type": "integer",
    "minimum": 1
   },
   "description": {
    "type": "string",
    "maxLength": 500
   },
   "quantity": {
    "type": "number",
    "nullable": true
   },
   "netAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "taxRate": {
    "type": "number"
   },
   "taxCategory": {
    "$ref": "#/components/schemas/FinTaxCategory"
   },
   "taxAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "grossAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   }
  }
 },
 "FinEInvoiceTransmission": {
  "x-ticvai-persistence": "ledger.einvoice_transmission",
  "type": "object",
  "description": "6.1.1. One attempt to send one tax document to the provider, and its answer.",
  "required": [
   "id",
   "documentKind",
   "documentId",
   "legalEntityId",
   "status",
   "createdAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "documentKind": {
    "type": "string",
    "enum": [
     "taxInvoice",
     "creditMemo"
    ]
   },
   "documentId": {
    "type": "string",
    "format": "uuid"
   },
   "documentNumber": {
    "type": "string"
   },
   "legalEntityId": {
    "type": "string",
    "format": "uuid"
   },
   "providerId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "mode": {
    "type": "string",
    "enum": [
     "test",
     "live"
    ]
   },
   "status": {
    "$ref": "#/components/schemas/FinEInvoiceTransmissionStatus"
   },
   "payloadHash": {
    "type": "string",
    "nullable": true,
    "description": "SHA-256 of the document as sent, so a resend can be shown to be the same document."
   },
   "providerMessageId": {
    "type": "string",
    "nullable": true
   },
   "attempt": {
    "type": "integer",
    "minimum": 1
   },
   "errorCodes": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "errorMessage": {
    "type": "string",
    "nullable": true
   },
   "sentAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "answeredAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "createdAt": {
    "type": "string",
    "format": "date-time"
   },
   "scopePath": {
    "type": "string",
    "readOnly": true
   }
  }
 },
 "FinEInvoiceTransmissionStatus": {
  "type": "string",
  "description": "6.1.1. `notRequired` where the legal entity's provider is `disabled` or absent.",
  "enum": [
   "notRequired",
   "queued",
   "sent",
   "accepted",
   "rejected",
   "failed"
  ]
 },
 "FinTaxCategory": {
  "type": "string",
  "description": "How a line is treated for VAT. Taken from the tax code the line was posted with.",
  "enum": [
   "standardRated",
   "zeroRated",
   "exempt",
   "outOfScope",
   "reverseCharge"
  ]
 },
 "FinTaxInvoice": {
  "x-ticvai-persistence": "ledger.tax_invoice + ledger.tax_invoice_line",
  "type": "object",
  "description": "5.7.93, 5.10.3. **A guest tax invoice, as issued, never edited.** Corrections are credit memos. The supplier block is a snapshot of the legal entity at issue, so a later change of address does not change a document already given to a guest.",
  "required": [
   "id",
   "invoiceNumber",
   "invoiceType",
   "status",
   "legalEntityId",
   "issuedAt",
   "supplyDate",
   "currency",
   "netAmount",
   "taxAmount",
   "grossAmount",
   "lines"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "invoiceNumber": {
    "type": "string",
    "readOnly": true,
    "description": "Server-assigned from the legal entity's series for the document kind, in sequence and without gaps, e.g. `INV-2026-000123`. Never reused."
   },
   "invoiceType": {
    "$ref": "#/components/schemas/FinTaxInvoiceType"
   },
   "status": {
    "$ref": "#/components/schemas/FinTaxInvoiceStatus"
   },
   "legalEntityId": {
    "type": "string",
    "format": "uuid"
   },
   "templateId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "venueId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "orderIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "supplierName": {
    "type": "string"
   },
   "supplierAddress": {
    "type": "string",
    "nullable": true
   },
   "supplierTaxRegistrationNumber": {
    "type": "string",
    "nullable": true
   },
   "buyerSubjectId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The guest the orders belong to; the key a guest's own reads filter on."
   },
   "buyerName": {
    "type": "string",
    "nullable": true
   },
   "buyerAddress": {
    "type": "string",
    "nullable": true
   },
   "buyerCountryCode": {
    "type": "string",
    "pattern": "^[A-Z]{2}$",
    "nullable": true
   },
   "buyerTaxRegistrationNumber": {
    "type": "string",
    "nullable": true
   },
   "customerAccountId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "issuedAt": {
    "type": "string",
    "format": "date-time"
   },
   "supplyDate": {
    "type": "string",
    "format": "date",
    "description": "The date of supply where it differs from the issue date (the latest order's payment date on a consolidated invoice). A day in the region's time zone."
   },
   "currency": {
    "type": "string",
    "pattern": "^[A-Z]{3}$"
   },
   "netAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "discountAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "taxAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "grossAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "taxAmountInLegalCurrency": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "The tax in the legal entity's currency (AED in the UAE) where the invoice currency differs, at the rate the orders were stored at."
   },
   "creditedAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "languages": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "supersedesInvoiceId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "renditionAssetId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true,
    "description": "The PDF rendered at issue; read through getTaxDocumentRendition."
   },
   "eInvoiceStatus": {
    "$ref": "#/components/schemas/FinEInvoiceTransmissionStatus"
   },
   "issuedByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true,
    "description": "Null where the platform issued it."
   },
   "lines": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/FinTaxInvoiceLine"
    }
   },
   "taxSummary": {
    "type": "array",
    "x-ticvai-persisted": false,
    "description": "VAT per rate and category, summed from the lines for the response.",
    "items": {
     "type": "object",
     "properties": {
      "taxCategory": {
       "$ref": "#/components/schemas/FinTaxCategory"
      },
      "taxRate": {
       "type": "number"
      },
      "taxableAmount": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      },
      "taxAmount": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      }
     }
    }
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "**The partition key** (ADR-0005). Written at the scope of the venue the orders were sold at, or the region for a consolidated invoice across venues."
   }
  }
 },
 "FinTaxInvoiceLine": {
  "type": "object",
  "description": "One line as it was sold and taxed. Amounts are in the invoice currency.",
  "required": [
   "lineNumber",
   "description",
   "quantity",
   "netAmount",
   "taxAmount",
   "grossAmount",
   "taxCategory"
  ],
  "properties": {
   "lineNumber": {
    "type": "integer",
    "minimum": 1
   },
   "orderId": {
    "type": "string",
    "format": "uuid"
   },
   "orderLineId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "description": {
    "type": "string",
    "maxLength": 500
   },
   "quantity": {
    "type": "number"
   },
   "unitPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "discountAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "netAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "taxCodeId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "taxRate": {
    "type": "number",
    "minimum": 0,
    "maximum": 100
   },
   "taxCategory": {
    "$ref": "#/components/schemas/FinTaxCategory"
   },
   "taxAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "grossAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "creditedAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   }
  }
 },
 "FinTaxInvoiceStatus": {
  "type": "string",
  "description": "`issued` until a credit memo is issued against it; `superseded` where a full invoice replaced a simplified one for the same supply (only if the law allows it; see issueTaxInvoice).",
  "enum": [
   "issued",
   "partiallyCredited",
   "fullyCredited",
   "superseded"
  ]
 },
 "FinTaxInvoiceType": {
  "type": "string",
  "description": "5.7.93. `simplified` for one order with no recipient details, `full` for one order with them, `consolidated` for several paid orders of one buyer on one invoice.",
  "enum": [
   "simplified",
   "full",
   "consolidated"
  ]
 },
 "KpiValue": {
  "type": "object",
  "description": "BI board 10.3. **Value, target, variance, direction and freshness in one read.**",
  "properties": {
   "kpiId": {
    "type": "string",
    "format": "uuid"
   },
   "code": {
    "type": "string"
   },
   "bucketStart": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "description": "The start of the bucket this value covers, when `getKpiValues` was asked for an `interval`; null otherwise."
   },
   "groupKey": {
    "type": "string",
    "nullable": true,
    "description": "The value of the `groupBy` dimension this row is for (a status, a category code, a tier); null when no `groupBy` was asked."
   },
   "name": {
    "type": "string"
   },
   "scopePath": {
    "type": "string"
   },
   "period": {
    "type": "string"
   },
   "value": {
    "$ref": "#/components/schemas/MetricValue"
   },
   "target": {
    "allOf": [
     {
      "$ref": "#/components/schemas/MetricValue"
     }
    ],
    "nullable": true
   },
   "comparison": {
    "allOf": [
     {
      "$ref": "#/components/schemas/MetricValue"
     }
    ],
    "nullable": true
   },
   "variancePercent": {
    "type": "number",
    "nullable": true
   },
   "direction": {
    "type": "string",
    "enum": [
     "up",
     "down",
     "flat"
    ]
   },
   "status": {
    "type": "string",
    "enum": [
     "green",
     "amber",
     "red",
     "noTarget"
    ]
   },
   "asOf": {
    "type": "string",
    "format": "date-time"
   },
   "stale": {
    "type": "boolean",
    "description": "**True when the pipeline behind it has not refreshed.** A number nobody flagged as stale is a number somebody will act on.\n"
   }
  }
 },
 "MetricValue": {
  "x-ticvai-persistence-column": "numeric(18,4)",
  "description": "**A reading of a metric or KPI, or a threshold on one.** A `Money` where the metric is money-valued — `MetricSource` lists those in `x-ticvai-money-valued`, and a KPI is when its `unit` is `currency` — and a plain number otherwise. naming-and-style 5.1: money is never a float, at any layer.\nStored as `numeric(18,4)` either way: a money value stores its amount, and currency and scale resolve from the scope as they do for every `Money`.\n",
  "oneOf": [
   {
    "type": "number"
   },
   {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   }
  ]
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
 "UnifiedReconciliation": {
  "type": "object",
  "description": "4.2.19. **Four sources and the variances between them.** A view showing each balanced against itself has not reconciled anything.\n",
  "properties": {
   "from": {
    "type": "string",
    "format": "date",
    "description": "A day in the region's time zone, local midnight to local midnight."
   },
   "to": {
    "type": "string",
    "format": "date",
    "description": "A day in the region's time zone, local midnight to local midnight."
   },
   "sources": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "source": {
       "type": "string",
       "enum": [
        "pos",
        "gateway",
        "bank",
        "wallet",
        "ledger"
       ]
      },
      "providerName": {
       "type": "string",
       "nullable": true
      },
      "total": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      },
      "transactionCount": {
       "type": "integer"
      }
     }
    }
   },
   "variances": {
    "type": "array",
    "description": "**Where two sources disagree, named.** A discrepancy is usually the gap between two of them rather than inside one, and *\"out by 240\"* without saying between what is not actionable.\n",
    "items": {
     "type": "object",
     "properties": {
      "between": {
       "type": "array",
       "description": "The two sources that disagree, as named in `sources[].source`.",
       "minItems": 2,
       "maxItems": 2,
       "items": {
        "type": "string",
        "enum": [
         "pos",
         "gateway",
         "bank",
         "wallet",
         "ledger"
        ]
       }
      },
      "amount": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      },
      "likelyCause": {
       "type": "string",
       "nullable": true
      }
     }
    }
   }
  }
 }
}
```
