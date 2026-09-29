# P10-reports-settlement-01 — P10 · Reports & Settlement

**3 screens · 16 operations · 26 schemas · 6 permissions**

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

- **Every control that can be refused must be gated.** 6 permissions apply here:
  `PARTNER_MANAGE, PARTNER_VIEW, REPORT_MANAGE, REPORT_VIEW_VENUE, SETTLEMENT_RECONCILE, SETTLEMENT_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `PTR-014` | Settlement & Payment History | listDetail | 5 | 2 | — |
| `PTR-017` | Commission Statement | listDetail | 2 | 0 | — |
| `PTR-018` | Reports & Sales Performance | listDetail | 9 | 6 | — |

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "PTR-014",
  "name": "Settlement & Payment History",
  "module": "Reports & Settlement",
  "requiresModule": "partner",
  "wave": 3,
  "capability": "C50",
  "implementation": {
   "app": "partner-web",
   "route": "/general/settlement-and-payment-history",
   "component": "apps/partner-web/src/routes/general/SettlementAndPaymentHistoryList.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "PTR-001"
   ],
   "inferred": true,
   "exitTo": [
    "PTR-003"
   ],
   "transitions": [
    {
     "to": "PTR-003",
     "trigger": "Profile & Company Details",
     "provenance": "derived — PTR-003 declares entryState.params  and PTR-014 holds none of them, so the edge carries nothing and PTR-003 opens cold"
    }
   ]
  },
  "notes": "States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual. Purpose derived from the screen name and its operations on 17 August, not from a requirement.",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listSettlements` reads the population and `getSettlement` reads one of them — list, select, act",
  "purpose": "Take the money, and be unambiguous about whether it worked.",
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
        "Settlement.ledgerGross",
        "Settlement.difference",
        "Settlement.ingestedAt",
        "Settlement.completedAt",
        "Settlement.scopePath"
       ],
       "operation": "getSettlement",
       "provenance": "contract finance.yaml GET /settlements/{settlementId}"
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
   "loading": "The settlement payment history list.",
   "error": "Could not load. Names which read failed and leaves the settlement payment history untouched.",
   "emptyFirstRun": "No settlement payment history yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table.",
   "emptyNoResults": "Nothing matches the filter on providerName, status and the settlement payment history are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Shown when the caller lacks `SETTLEMENT_VIEW`, which `listSettlements` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listSettlements",
    "contract": "finance",
    "purpose": "from page inventory",
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
   "coldEntry": "**A partner link resolves within that partner's own scope and refuses outside it.** A forwarded link between partners must not open another partner's record. If the target is gone the screen says so and offers the partner's own list. Arrives with `settlementId`.",
   "preloaded": [
    "Settlement.id",
    "Settlement.providerName",
    "Settlement.periodStart",
    "Settlement.periodEnd",
    "Settlement.status"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P10 Partner Web.dc.html#ptr-014"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 5 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
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
  "id": "PTR-017",
  "name": "Commission Statement",
  "module": "Reports & Settlement",
  "requiresModule": "partner",
  "wave": 3,
  "implementation": {
   "app": "partner-web",
   "route": "/general/commission-statement",
   "component": "apps/partner-web/src/routes/general/CommissionStatementDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "PTR-001"
   ],
   "inferred": true,
   "exitTo": [
    "PTR-003"
   ],
   "transitions": [
    {
     "to": "PTR-003",
     "trigger": "Profile & Company Details",
     "provenance": "derived — PTR-003 declares entryState.params  and PTR-017 holds none of them, so the edge carries nothing and PTR-003 opens cold"
    }
   ]
  },
  "notes": "States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual. Purpose derived from the screen name and its operations on 17 August, not from a requirement.",
  "openQuestions": [
   "No contract — commission not modelled"
  ],
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listPartnerAgreements` reads the population and `getCommissionStatement` reads one of them — list, select, act",
  "purpose": "Answer a question about commission with numbers someone can check.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "numberField",
       "label": "Expiring within days",
       "operation": "listPartnerAgreements",
       "notes": "Sends `?expiringWithinDays=` to `listPartnerAgreements`.",
       "provenance": "contract subscription.yaml GET /partner-agreements"
      },
      {
       "kind": "textField",
       "label": "Status",
       "operation": "listPartnerAgreements",
       "notes": "Sends `?status=` to `listPartnerAgreements`.",
       "provenance": "contract subscription.yaml GET /partner-agreements"
      },
      {
       "kind": "dataTable",
       "label": "Every partner agreement",
       "bindsTo": "PartnerAgreement",
       "columns": [
        "PartnerAgreement.id",
        "PartnerAgreement.partnerId",
        "PartnerAgreement.partnerName",
        "PartnerAgreement.status",
        "PartnerAgreement.rateMode",
        "PartnerAgreement.commissionPercent",
        "PartnerAgreement.volumeTiers",
        "PartnerAgreement.volumeWindow",
        "PartnerAgreement.seasonalRates",
        "PartnerAgreement.segmentTier",
        "PartnerAgreement.brandingAssetId",
        "PartnerAgreement.storefrontSubdomain"
       ],
       "operation": "listPartnerAgreements",
       "provenance": "contract subscription.yaml GET /partner-agreements"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected partner agreement",
       "bindsTo": "PartnerAgreement",
       "columns": [
        "PartnerAgreement.id",
        "PartnerAgreement.partnerId",
        "PartnerAgreement.partnerName",
        "PartnerAgreement.status",
        "PartnerAgreement.rateMode",
        "PartnerAgreement.commissionPercent",
        "PartnerAgreement.volumeTiers",
        "PartnerAgreement.volumeWindow",
        "PartnerAgreement.seasonalRates",
        "PartnerAgreement.segmentTier",
        "PartnerAgreement.brandingAssetId",
        "PartnerAgreement.storefrontSubdomain",
        "PartnerAgreement.sponsorship",
        "PartnerAgreement.netRates",
        "PartnerAgreement.creditTermDays",
        "PartnerAgreement.acceptedByPrincipalId"
       ],
       "operation": "listPartnerAgreements",
       "provenance": "contract subscription.yaml GET /partner-agreements"
      },
      {
       "kind": "detailPanel",
       "label": "The commission statement",
       "bindsTo": "CommissionStatement",
       "columns": [
        "CommissionStatement.agreementId",
        "CommissionStatement.partnerName",
        "CommissionStatement.from",
        "CommissionStatement.to",
        "CommissionStatement.currency",
        "CommissionStatement.grossSales",
        "CommissionStatement.refunds",
        "CommissionStatement.netSales",
        "CommissionStatement.commissionEarned",
        "CommissionStatement.amountDue",
        "CommissionStatement.lines"
       ],
       "operation": "getCommissionStatement",
       "provenance": "contract subscription.yaml GET /partner-agreements/{agreementId}/commission-statement"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The commission statement list.",
   "error": "Could not load. Names which read failed and leaves the commission statement untouched.",
   "emptyFirstRun": "No commission statement yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table.",
   "emptyNoResults": "Nothing matches the filter on expiringWithinDays, status and the commission statement are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Shown when the caller lacks `PARTNER_VIEW`, which `getCommissionStatement` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getCommissionStatement",
    "contract": "subscription",
    "purpose": "What the partner earned and what is owed",
    "trigger": "onAction"
   },
   {
    "operationId": "listPartnerAgreements",
    "contract": "subscription",
    "purpose": "Commercial agreements with B2B partners",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "agreementId",
     "from": "deepLink"
    }
   ],
   "coldEntry": "**A partner link resolves within that partner's own scope and refuses outside it.** A forwarded link between partners must not open another partner's record. If the target is gone the screen says so and offers the partner's own list. Arrives with `agreementId`.",
   "preloaded": [
    "PartnerAgreement.id",
    "PartnerAgreement.partnerId",
    "PartnerAgreement.partnerName",
    "PartnerAgreement.status",
    "PartnerAgreement.rateMode"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P10 Partner Web.dc.html#ptr-017"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 2 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
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
  "id": "PTR-018",
  "name": "Reports & Sales Performance",
  "module": "Reports & Settlement",
  "requiresModule": "partner",
  "wave": 3,
  "capability": "C21",
  "implementation": {
   "app": "partner-web",
   "route": "/general/reports-and-sales-performance",
   "component": "apps/partner-web/src/routes/general/ReportsAndSalesPerformanceDashboard.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "PTR-001"
   ],
   "inferred": true,
   "exitTo": [
    "PTR-003"
   ],
   "transitions": [
    {
     "to": "PTR-003",
     "trigger": "Profile & Company Details",
     "provenance": "derived — PTR-003 declares entryState.params  and PTR-018 holds none of them, so the edge carries nothing and PTR-003 opens cold"
    }
   ]
  },
  "notes": "States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual. Purpose derived from the screen name and its operations on 17 August, not from a requirement.",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listReports` reads the population and `getFinancialReport` reads one of them — list, select, act",
  "purpose": "Answer a question about reports with numbers someone can check.",
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
       "label": "Run report",
       "operation": "runReport",
       "provenance": "contract reporting.yaml POST /reports/{reportId}/run"
      },
      {
       "kind": "secondaryButton",
       "label": "Ask reporting question",
       "operation": "askReportingQuestion",
       "provenance": "contract reporting.yaml POST /reports/ask"
      },
      {
       "kind": "secondaryButton",
       "label": "Create report",
       "operation": "createReport",
       "provenance": "contract reporting.yaml POST /reports"
      },
      {
       "kind": "destructiveButton",
       "label": "Delete report",
       "operation": "deleteReport",
       "provenance": "contract reporting.yaml DELETE /reports/{reportId}"
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
    "body": "**Names what `deleteReport` changes and what it leaves alone**, in the consequence rather than the verb. A reports sales performance this affects should be identified in the dialog, not just counted.",
    "provenance": "contract reporting.yaml DELETE /reports/{reportId}"
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
   "loading": "The reports sales performance list.",
   "error": "Could not load. Names which read failed and leaves the reports sales performance untouched.",
   "emptyFirstRun": "No reports sales performance yet. Offers Create report (`createReport`); distinct from a filter that matched nothing.",
   "emptyNoResults": "Nothing matches the filter on category, search and the reports sales performance are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Shown when the caller lacks `REPORT_VIEW_VENUE`, which `getFinancialReport` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "runReport",
    "contract": "reporting",
    "purpose": "from page inventory",
    "trigger": "onAction"
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
    "operationId": "createReport",
    "contract": "reporting",
    "purpose": "Create a custom report definition",
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
    "operationId": "getFinancialReport",
    "contract": "finance",
    "purpose": "P&L, balance sheet or cash flow",
    "trigger": "onLoad"
   },
   {
    "operationId": "getReport",
    "contract": "reporting",
    "purpose": "Read a report definition",
    "trigger": "onAction"
   },
   {
    "operationId": "listReports",
    "contract": "reporting",
    "purpose": "List available report definitions",
    "trigger": "onLoad"
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
   "board": "wireframes/P10 Partner Web.dc.html#ptr-018"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 9 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
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
 "getCommissionStatement": {
  "method": "GET",
  "path": "/partner-agreements/{agreementId}/commission-statement",
  "contract": "subscription",
  "summary": "What the partner earned and what is owed",
  "permission": "PARTNER_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": "from",
    "in": "query",
    "required": null
   },
   {
    "name": "to",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "CommissionStatement"
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
 "listPartnerAgreements": {
  "method": "GET",
  "path": "/partner-agreements",
  "contract": "subscription",
  "summary": "Commercial agreements with B2B partners",
  "permission": "PARTNER_MANAGE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": "expiringWithinDays",
    "in": "query",
    "required": null
   },
   {
    "name": "status",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "PartnerAgreement"
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
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "CommissionStatement": {
  "type": "object",
  "x-ticvai-persistence": "none — aggregated from orders and control.partner_agreement",
  "properties": {
   "agreementId": {
    "type": "string",
    "format": "uuid"
   },
   "partnerName": {
    "type": "string"
   },
   "from": {
    "type": "string",
    "format": "date"
   },
   "to": {
    "type": "string",
    "format": "date"
   },
   "currency": {
    "type": "string"
   },
   "grossSales": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "refunds": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "netSales": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "commissionEarned": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "amountDue": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "lines": {
    "type": "array",
    "description": "**Reconcilable order by order.** A statement a partner cannot check line by line is a statement they will dispute, and the dispute costs more than the detail.\n",
    "items": {
     "type": "object",
     "properties": {
      "orderId": {
       "type": "string",
       "format": "uuid"
      },
      "orderNumber": {
       "type": "string"
      },
      "soldAt": {
       "type": "string",
       "format": "date-time"
      },
      "agreementVersion": {
       "type": "integer",
       "description": "The version in force at the time of that sale, not the current one."
      },
      "gross": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      },
      "commission": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      },
      "isRefunded": {
       "type": "boolean"
      }
     }
    }
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
 "DataSource": {
  "type": "string",
  "description": "What a report may be built over. **A closed set, and that is the point** — a builder that accepts any table will happily produce a report over data nobody maintains.\n**Eight sources added 18 August** (BL-143), each because the matrix asks for a report the builder could not source. `stockCounts` and `waste`: 6.1.21 wants count variance and `stockMovements` records the movement rather than **the count that found the discrepancy**. `workstations`, `devices` and `principals`: 6.1.28 — **who did what at which till** is the question an auditor asks first and it had no source. `loyalty`: 6.1.37, points earned, burned and expiring. `reviews`: 6.1.46. `queueEntries`: **wait times are already measured and nothing could report on them.**\n**Adding a source is a decision, not an omission.** `principals`, `guests`, `loyalty` and `reviews` all name a person, and `REPORT_EXPORT_PII` gates them.\n\n**`forecastPoints` added 29 September** (8.2.55, build pass, group G2): the points of published AI forecast versions; see `x-ticvai-forecast-points`.\n\n**Three accreditation sources added 29 September** (12.1.50, build pass): `accreditationApplications`, `accreditationHolders` and `accreditationCredentials`, over `accreditation.application`, `accreditation.holder` and `accreditation.credential`. They are what the accreditation KPIs and any accreditation report or export (`exportReportResult`, csv or xlsx) are built over. **All three name a person**, and `REPORT_EXPORT_PII` gates them as it gates `guests`.\n",
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
   "resaleListings",
   "accreditationApplications",
   "accreditationHolders",
   "accreditationCredentials",
   "forecastPoints"
  ],
  "x-ticvai-forecast-points": "**`forecastPoints` added 29 September (build pass, group G2; 8.2.55)**: one row per forecast point (`ai.forecast_point`) of a **published** forecast version (`ai.forecast_version` status `published`), with the definition it belongs to (`ai.forecast_definition`: subject, grain, unit), the period, the dimension key and the p10, p50 and p90 values. Draft, awaiting-approval and superseded versions are not reachable, and scenario points (`scenarioId` set) only with the scenario named as a filter: **a forecast leaves the platform as the one somebody published**. It is how a forecast is exported (`runReport` then `exportReportResult`, csv or xlsx), scheduled or put on a dashboard. Names no person, so `REPORT_EXPORT` is enough. Read from the reporting replica of the AI log database (design 2.4), never from the model service.\n"
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
   },
   "compiledSql": {
    "type": "string",
    "nullable": true,
    "description": "The SQL the semantic spec compiled to, exactly as run on the analytical replica (29 September, design 5.7). The replica's row-level security applies beneath it, so it does not need to carry the caller's scope. Null on queries kept before the semantic compile.\n"
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
   "reliability"
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
    "description": "What the question was understood to mean, in plain language. When the question is outside the semantic model, the \"not available yet\" sentence."
   },
   "semanticSpec": {
    "allOf": [
     {
      "$ref": "#/components/schemas/ReportingSemanticQuerySpec"
     }
    ],
    "nullable": true,
    "description": "What the model returned instead of SQL (design 2.2 E, 5.7): metric, dimensions, filters, period, comparison, as validated against the semantic model. Null when the question is outside it. **Also kept**, on `NaturalLanguageQuery`, so a follow-up edits it.\n"
   },
   "generatedQuery": {
    "allOf": [
     {
      "$ref": "#/components/schemas/GeneratedQuery"
     }
    ],
    "nullable": true,
    "description": "The query the spec compiled to: data source, columns, filters, grouping, and the compiled SQL in `compiledSql`. Returned so the answer can be checked. An answer nobody can verify is worse than no answer. **Also kept, as `NaturalLanguageQuery`**, for `saveNaturalLanguageQuery`. Null when the question is outside the semantic model.\n"
   },
   "result": {
    "allOf": [
     {
      "$ref": "#/components/schemas/ReportResult"
     }
    ],
    "nullable": true,
    "description": "Null when the question is outside the semantic model."
   },
   "dataAsOf": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "description": "Replica position the answer was read at, the result's `dataAsOf`, stated beside the answer so a figure that moved is not argued about. Null when nothing was run."
   },
   "reliability": {
    "$ref": "#/components/schemas/ReportingAnswerReliability"
   },
   "unavailableReason": {
    "allOf": [
     {
      "$ref": "#/components/schemas/ReportingUnavailableReason"
     }
    ],
    "nullable": true,
    "description": "Set only when `reliability` is `insufficientEvidence` because the question is outside the semantic model (\"not available yet\"); names which part is not modelled."
   },
   "confidence": {
    "type": "number",
    "minimum": 0,
    "maximum": 1,
    "deprecated": true,
    "description": "Superseded by `reliability` on 29 September (design 5.6, never a bare percentage for analytics). Returned for one release, then removed."
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
 "PartnerAgreement": {
  "type": "object",
  "x-ticvai-persistence": "control.partner_agreement",
  "x-ticvai-retired-columns": [
   "partner_name"
  ],
  "required": [
   "partnerId",
   "rateMode",
   "validFrom"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "partnerId": {
    "x-ticvai-references": "control.partner",
    "type": "string",
    "format": "uuid",
    "description": "The partner (control.partner) this agreement is with. The agreement carries the terms; control.partner carries who the partner is and whether it may trade. **Resolves to control.partner**, not to platform.tenant as the naming convention guessed before the partner master existed (decided 29 September, writers pass; DM4)"
   },
   "partnerName": {
    "type": "string",
    "readOnly": true,
    "x-ticvai-persisted": false,
    "description": "The partner's trading name, **read from control.partner.trading_name** (Partner.tradingName) when the agreement is returned and never stored on the agreement, so a renamed partner cannot show two names (decided 29 September, writers pass; DM4)"
   },
   "version": {
    "type": "integer",
    "readOnly": true,
    "description": "**Amending creates a version.** An order placed last week was placed under last week's rate, and settlement must be able to say which.\n"
   },
   "status": {
    "$ref": "#/components/schemas/PartnerAgreementStatus"
   },
   "rateMode": {
    "$ref": "#/components/schemas/PartnerRateMode"
   },
   "commissionPercent": {
    "type": "number",
    "nullable": true
   },
   "volumeTiers": {
    "type": "array",
    "deprecated": true,
    "x-ticvai-persisted": false,
    "description": "**Retired: the tiers are rows of control.partner_rate_volume_band** (`PartnerRate.volumeBands`, written by setPartnerRateNet), one set per rate row, so a tier can differ by product, venue or channel. Accepted and ignored on write; not returned once the bands exist. `volumeWindow` below still says over which window the bands count (decided 29 September, writers pass; DM4).\n\n2.7.57. **A tier that changes at a threshold needs the sale to look back at cumulative volume, and nothing did.** Flat net rates and per-channel price lists cover the simple case and stop there.\n**The window is the argument, not the tier.** A partner who sells 400 in January and 400 in February is either a 400-tier partner twice or an 800-tier partner once, and the two are different money. `volumeWindow` says which.\n",
    "items": {
     "type": "object",
     "required": [
      "fromUnits",
      "commissionPercent"
     ],
     "properties": {
      "fromUnits": {
       "type": "integer"
      },
      "commissionPercent": {
       "type": "number"
      },
      "appliesRetrospectively": {
       "type": "boolean",
       "default": false,
       "description": "**Whether crossing a tier reprices what came before it.** Retrospective is what a partner assumes and prospective is what a venue budgets for — it has to be stated.\n"
      }
     }
    }
   },
   "volumeWindow": {
    "type": "string",
    "nullable": true,
    "enum": [
     "calendarMonth",
     "calendarQuarter",
     "calendarYear",
     "agreementYear",
     "rolling12Months"
    ]
   },
   "seasonalRates": {
    "type": "array",
    "deprecated": true,
    "x-ticvai-persisted": false,
    "description": "**Retired: a seasonal rate is a control.partner_rate row** with `seasonalRate: true` and its own `effectiveFrom`/`effectiveTo` (`PartnerRate`, written by setPartnerRateNet); the most specific row in force wins. Accepted and ignored on write (decided 29 September, writers pass; DM4).\n\nRates that change by date range. **Separate from the volume tier because they compound** — a peak-season rate at a high volume tier is both, and a single rate table cannot say so.\n",
    "items": {
     "type": "object",
     "properties": {
      "from": {
       "type": "string",
       "format": "date"
      },
      "to": {
       "type": "string",
       "format": "date"
      },
      "commissionPercent": {
       "type": "number"
      }
     }
    }
   },
   "segmentTier": {
    "type": "string",
    "nullable": true
   },
   "brandingAssetId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "2.7.x, BL-078. **A reseller selling a venue's tickets under their own brand is a second scope level white-label does not have** — `BrandIdentity` and `setTheme` are tenant-scoped throughout.\n**Co-branding rather than replacement.** The venue's identity stays on the ticket because the ticket admits to the venue; the partner's sits beside it.\n"
   },
   "storefrontSubdomain": {
    "type": "string",
    "nullable": true
   },
   "sponsorship": {
    "type": "object",
    "nullable": true,
    "description": "BL-050. **Sponsorship inventory is sellable capacity of a different kind** — logo placements, hospitality allocations, naming rights. It is closer to a partner agreement than to a product: **a sponsor buys a relationship for a season, not a ticket for a date.**\nModelled here rather than as a `ProductKind` because the commercial terms — the term, the exclusivity, the settlement — are the agreement's, and duplicating them onto a product would mean two places to disagree.\n",
    "properties": {
     "placements": {
      "type": "array",
      "items": {
       "type": "object",
       "properties": {
        "surface": {
         "type": "string",
         "enum": [
          "signage",
          "ticketFace",
          "appBanner",
          "emailFooter",
          "venueNaming",
          "zoneNaming",
          "uniform",
          "printedMap"
         ]
        },
        "quantity": {
         "type": "integer"
        },
        "exclusive": {
         "type": "boolean",
         "default": false,
         "description": "**Exclusivity is the expensive word.** A sponsor paying for category exclusivity has bought the absence of a competitor, and a second agreement breaching it is a legal problem rather than a scheduling one.\n"
        }
       }
      }
     },
     "hospitalityAllocation": {
      "type": "integer",
      "nullable": true,
      "description": "Tickets or cabanas included. **Issued as invitations, not sales** — no revenue attaches."
     },
     "categoryExclusivity": {
      "type": "string",
      "nullable": true
     }
    }
   },
   "netRates": {
    "type": "array",
    "deprecated": true,
    "x-ticvai-persisted": false,
    "description": "**Retired: net rates are rows of control.partner_rate** (`PartnerRate` with `pricingModel: netRate`, `netRate` and the `maxDiscountPercent` guardrail), written by setPartnerRateNet. Per product or category; absent means the commission applies across the catalogue. Accepted and ignored on write (decided 29 September, writers pass; DM4)",
    "items": {
     "type": "object",
     "properties": {
      "productId": {
       "type": "string",
       "format": "uuid",
       "nullable": true
      },
      "categoryId": {
       "type": "string",
       "format": "uuid",
       "nullable": true
      },
      "netPrice": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      },
      "maxDiscountPercent": {
       "type": "number",
       "nullable": true,
       "description": "1.6.10. **What the partner may not undercut.** A reseller selling below the venue's own price damages the direct channel, and the venue usually cares more about that than the margin.\n"
      }
     }
    }
   },
   "creditTermDays": {
    "type": "integer",
    "description": "2.7.36. Net 30, net 60. Drives when an invoice becomes overdue."
   },
   "acceptedByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "BL-079. **Electronic acceptance against a version**, following the `signatureRef` precedent. An agreement accepted with no version recorded is an agreement nobody can produce in a dispute.\n"
   },
   "acceptedVersion": {
    "type": "integer",
    "nullable": true
   },
   "acceptedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "signatureRef": {
    "type": "string",
    "nullable": true
   },
   "corporateAllocations": {
    "type": "array",
    "deprecated": true,
    "x-ticvai-persisted": false,
    "description": "**Retired: allocations are rows of control.partner_allocation** (`PartnerAllocation`, written by setPartnerAllocations and read by listCommercialAllocationQuota); used quantity is counted from orders against the row, not stored. Accepted and ignored on write (decided 29 September, writers pass; DM4).\n\nBL-035. **`PartnerAgreement` covered commercial terms and not allocations.** A corporate account with fifty places for its staff is the same structure as a reseller with fifty to sell, and **the difference is that a corporate member does not pay.**\n",
    "items": {
     "type": "object",
     "properties": {
      "productId": {
       "type": "string",
       "format": "uuid"
      },
      "quantity": {
       "type": "integer"
      },
      "usedQuantity": {
       "type": "integer",
       "readOnly": true
      },
      "perMemberLimit": {
       "type": "integer",
       "nullable": true
      },
      "validTo": {
       "type": "string",
       "format": "date",
       "nullable": true
      }
     }
    }
   },
   "settlementCurrency": {
    "type": "string",
    "pattern": "^[A-Z]{3}$",
    "description": "**The currency this partner is billed and settles in**, which is often not the venue's. A UK tour operator selling a Dubai attraction is invoiced in GBP against sales booked in AED, and the difference is somebody's exposure.\n**`creditLimit` and `netRates` are expressed in this currency**, not the venue's — a limit in the wrong currency is a limit that moves with the exchange rate.\n"
   },
   "fxPolicy": {
    "type": "string",
    "enum": [
     "rateAtSale",
     "rateAtInvoice",
     "fixedRate"
    ],
    "default": "rateAtSale",
    "description": "**Which rate converts a sale into the settlement currency, and it is a commercial term.** `rateAtSale` puts the movement on the partner; `rateAtInvoice` puts it on the venue; `fixedRate` puts it on whoever guessed wrong when the agreement was signed.\n**Not a default to leave alone** — on a monthly statement across a moving rate the three produce materially different numbers, and the partner will have assumed one of them.\n"
   },
   "fixedRate": {
    "type": "number",
    "nullable": true,
    "description": "Where `fxPolicy` is `fixedRate`. **An amendment creates a version** so an old statement stays readable."
   },
   "creditLimit": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "allowedChannels": {
    "type": "array",
    "items": {
     "$ref": "../shared/common.yaml#/components/schemas/SalesChannel"
    }
   },
   "allowedVenueIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "requiresApprovalAboveValue": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "nullable": true,
    "description": "2.7.39. Routes through `approvals` rather than a second mechanism here."
   },
   "validFrom": {
    "type": "string",
    "format": "date"
   },
   "validTo": {
    "type": "string",
    "format": "date",
    "nullable": true,
    "description": "2.7.37. **An agreement that lapses silently keeps selling at rates nobody agreed to**, discovered at settlement rather than at sale. Null means open-ended, which should be rare and deliberate.\n"
   },
   "expiryAlertDays": {
    "type": "integer",
    "default": 30
   },
   "approvalRequestId": {
    "type": "string",
    "nullable": true,
    "readOnly": true
   },
   "notes": {
    "type": "string"
   },
   "agreementName": {
    "type": "string",
    "nullable": true,
    "description": "Agreement name (decided 29 September, data model DM4)"
   },
   "agreementType": {
    "type": "string",
    "nullable": true,
    "description": "Agreement type code, seeded with reseller, ota, travelTrade, corporate, wholesale, affiliate, distribution, apiCommercial (pack p.26) (decided 29 September, data model DM4)"
   },
   "contractReference": {
    "type": "string",
    "nullable": true,
    "description": "Contract reference (decided 29 September, data model DM4)"
   },
   "legalEntityId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The contracting legal entity (ledger.legal_entity) (decided 29 September, data model DM4)"
   },
   "brandId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Brand the agreement covers; empty for every brand of the tenant (decided 29 September, data model DM4)"
   },
   "territory": {
    "type": "string",
    "nullable": true,
    "description": "Territory (decided 29 September, data model DM4)"
   },
   "commercialOwnerPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Commercial owner, a staff principal (decided 29 September, data model DM4)"
   },
   "financeOwnerPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Finance owner, a staff principal (decided 29 September, data model DM4)"
   },
   "pricingBasis": {
    "type": "string",
    "enum": [
     "retailPrice",
     "netRate",
     "discountFromRetail",
     "markup",
     "derivedRate"
    ],
    "nullable": true,
    "description": "Pricing basis (pack p.27 pricing models); the rows are `control.partner_rate` (decided 29 September, data model DM4)"
   },
   "paymentModel": {
    "type": "string",
    "enum": [
     "creditAccount",
     "prepaid",
     "payPerTransaction"
    ],
    "nullable": true,
    "description": "Payment model, the three confirmed at MoM 5 Aug and MoM 31 Aug 4.4: creditAccount (sells to an approved credit ceiling, invoiced periodically), prepaid (pre-funded wallet drawn down per sale) or payPerTransaction (card at each sale). Held here once; the billing screen reads and sets this column (decided 29 September, data model DM4)"
   },
   "renewalType": {
    "type": "string",
    "enum": [
     "manual",
     "auto"
    ],
    "nullable": true,
    "description": "Renewal type (decided 29 September, data model DM4)"
   },
   "renewalNoticeDays": {
    "type": "integer",
    "minimum": 0,
    "nullable": true,
    "description": "Renewal notice period in days (decided 29 September, data model DM4)"
   },
   "renegotiationRequired": {
    "type": "boolean",
    "default": false,
    "description": "Renegotiation required before renewal (decided 29 September, data model DM4)"
   },
   "renewalRequiresApproval": {
    "type": "boolean",
    "description": "Renewal needs approval (decided 29 September, data model DM4)"
   },
   "minimumCommitment": {
    "type": "integer",
    "minimum": 0,
    "nullable": true,
    "description": "Minimum commitment: tickets over the agreement term (decided 29 September, data model DM4)"
   },
   "salesTarget": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "nullable": true,
    "description": "Sales target over the agreement term (decided 29 September, data model DM4)"
   },
   "agreementValue": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "nullable": true,
    "description": "Agreement value (MoM 31 Aug 4.4: each agreement captures term/value) (decided 29 September, data model DM4)"
   },
   "commissionTerms": {
    "type": "string",
    "nullable": true,
    "description": "Commission terms as written in the contract; the rules that compute it are `control.partner_commission_rule` (decided 29 September, data model DM4)"
   },
   "creditTerms": {
    "type": "string",
    "nullable": true,
    "description": "Credit terms as written in the contract (decided 29 September, data model DM4)"
   },
   "allocationTerms": {
    "type": "string",
    "nullable": true,
    "description": "Allocation terms as written in the contract; the allocations are `control.partner_allocation` (decided 29 September, data model DM4)"
   },
   "cancellationConditions": {
    "type": "string",
    "nullable": true,
    "description": "Cancellation conditions (decided 29 September, data model DM4)"
   },
   "refundConditions": {
    "type": "string",
    "nullable": true,
    "description": "Refund conditions (pack p.26) (decided 29 September, data model DM4)"
   },
   "bookingRestrictions": {
    "type": "string",
    "nullable": true,
    "description": "Booking restrictions as written in the contract; the enforced limits are `control.partner_booking_limit` (decided 29 September, data model DM4)"
   },
   "settlementTerms": {
    "type": "string",
    "nullable": true,
    "description": "Settlement terms (decided 29 September, data model DM4)"
   },
   "scopePath": {
    "type": "string",
    "description": "The partition key (ADR-0005), written at `tenant` scope, as every control.partner_* row carries it, so row-level security scopes the agreement the same way (decided 29 September, writers pass; DM4)"
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
 "PartnerRateMode": {
  "type": "string",
  "description": "**Alternatives, not both.** A partner buys at a net rate and keeps the margin, or sells at face value and is paid commission. Both is being paid twice for the same sale.\n",
  "enum": [
   "netRate",
   "commission"
  ]
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
 "ReportingAnswerReliability": {
  "type": "string",
  "description": "**How far an analytics answer can be relied on** (decided 29 September, AI system design 5.6): a category, never a bare percentage. `grounded`: every figure comes from a result of the compiled spec. `partial`: part of the question was answered and the rest was not modelled. `conflictingSources`: the result and a cited source disagree. `insufficientEvidence`: the question could not be answered, including \"not available yet\" outside the semantic model. The same four values as `ai.yaml`'s assistant answers.\n",
  "enum": [
   "grounded",
   "partial",
   "conflictingSources",
   "insufficientEvidence"
  ]
 },
 "ReportingSemanticQuerySpec": {
  "x-ticvai-persistence": "none — embedded; stored whole in `reporting.natural_language_query`",
  "type": "object",
  "description": "**A question in the semantic model's own vocabulary** (decided 29 September, AI system design 2.2 E and 5.7). What the model returns for a live-number question instead of SQL, and what `runSemanticQuery` takes. Every code is a `SemanticModel` field code or a KPI code; Reporting validates the spec against the published model and compiles it deterministically, so the same spec compiles to the same SQL for the same model version.\n",
  "required": [
   "metric",
   "period"
  ],
  "properties": {
   "metric": {
    "type": "string",
    "description": "A measure field code in the `SemanticModel`, or a `KpiDefinition.code`. The governed definition the dashboards use, so the number matches them."
   },
   "dimensions": {
    "type": "array",
    "maxItems": 5,
    "description": "Field codes to group by. Each must be reachable from the metric's dataset through a relationship the semantic model declares.",
    "items": {
     "type": "string"
    }
   },
   "filters": {
    "type": "array",
    "items": {
     "type": "object",
     "required": [
      "field",
      "operator"
     ],
     "properties": {
      "field": {
       "type": "string",
       "description": "A `SemanticModel` field code."
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
        "isNull",
        "isNotNull"
       ]
      },
      "values": {
       "type": "array",
       "description": "**Open on purpose; typed by the field.** One value for the comparison operators, exactly two (from, to) for `between`, any number for `in` and `notIn`, none for `isNull` and `isNotNull`.\n",
       "items": {}
      }
     }
    }
   },
   "period": {
    "type": "string",
    "description": "ISO 8601 interval in the venue's time zone, e.g. `2026-09-21/2026-09-27`, the form `explainMetricChange` takes."
   },
   "comparison": {
    "type": "string",
    "nullable": true,
    "description": "As `getKpiValues` `compareTo`. With one, each row carries the metric for the comparison beside the current value.",
    "enum": [
     "previousPeriod",
     "samePeriodLastYear",
     "target",
     "benchmark"
    ]
   },
   "semanticModelVersion": {
    "type": "integer",
    "readOnly": true,
    "description": "The `SemanticModel.version` the spec was validated and compiled against. Set by Reporting."
   }
  }
 },
 "ReportingUnavailableReason": {
  "type": "string",
  "description": "Which part of a question is outside the semantic model, so the answer is \"not available yet\" (design 5.7). A metric or field the caller may not see is reported as not modelled, so the reason does not reveal that it exists.",
  "enum": [
   "metricNotModelled",
   "dimensionNotModelled",
   "filterNotModelled",
   "comparisonNotAvailable",
   "periodOutsideHistory"
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
 }
}
```
