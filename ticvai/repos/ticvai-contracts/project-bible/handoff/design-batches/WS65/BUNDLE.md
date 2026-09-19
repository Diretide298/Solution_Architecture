# WS65 — Ticket Upgrade, Exchange & Conversion board 1

**10 screens · 10 operations · 13 schemas · 2 permissions**

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
| `ADM-308` | Upgrade & Conversion Command Center | commandCentre | 1 | 0 | — |
| `ADM-309` | Upgrade & Conversion Path Builder | listDetail | 1 | 0 | — |
| `ADM-310` | Upgrade Eligibility & Qualification Rules | configEditor | 1 | 0 | — |
| `ADM-311` | Upgrade Timing, Usage & Ticket Status Rules | configEditor | 1 | 0 | — |
| `ADM-312` | Upgrade Financial Treatment & Price Difference Rules | configEditor | 1 | 0 | — |
| `ADM-313` | Pro-Rata, Residual Value & Entitlement Credit Configuration | listDetail | 1 | 0 | — |
| `ADM-314` | Person-Type, Product & Entitlement Conversion Rules | listDetail | 1 | 0 | — |
| `ADM-315` | Bulk, Group & Assisted Upgrade Operations | configEditor | 1 | 0 | — |
| `ADM-316` | Upgrade Execution, Credential Regeneration & Channel Controls | configEditor | 1 | 0 | — |
| `ADM-317` | Upgrade History, Exception Management & Audit Explorer | listDetail | 1 | 0 | — |

## Thin screens in this batch

**ADM-309, ADM-313, ADM-314 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "ADM-308",
  "name": "Upgrade & Conversion Command Center",
  "module": "Commercial",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Ticket Upgrade, Exchange & Conversion_Reference.pdf",
   "board": "1",
   "number": "11.1.1",
   "page": 3
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/upgrade-conversion-command-center-adm-308",
   "component": "apps/ticvai-web/src/routes/commercial/UpgradeConversionCommandCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-002"
   ],
   "exitTo": [
    "ADM-002",
    "ADM-309",
    "ADM-310",
    "ADM-311",
    "ADM-312",
    "ADM-313",
    "ADM-314",
    "ADM-315",
    "ADM-316",
    "ADM-317"
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
     "to": "ADM-309",
     "trigger": "Works in Upgrade & Conversion Path Builder",
     "provenance": "flow F174 step 1→2",
     "operation": "listUpgradeConversion"
    },
    {
     "to": "ADM-310",
     "trigger": "Works in Upgrade Eligibility & Qualification Rules",
     "provenance": "flow F174 step 3→4",
     "operation": "listUpgradeConversion"
    },
    {
     "to": "ADM-311",
     "trigger": "Works in Upgrade Timing, Usage & Ticket Status Rules",
     "provenance": "flow F174 step 5→6",
     "operation": "listUpgradeConversion"
    },
    {
     "to": "ADM-312",
     "trigger": "Works in Upgrade Financial Treatment & Price Difference Rules",
     "provenance": "flow F174 step 7→8",
     "operation": "listUpgradeConversion"
    },
    {
     "to": "ADM-313",
     "trigger": "Works in Pro-Rata, Residual Value & Entitlement Credit Configuration",
     "provenance": "flow F174 step 9→10",
     "operation": "listUpgradeConversion"
    },
    {
     "to": "ADM-314",
     "trigger": "Works in Person-Type, Product & Entitlement Conversion Rules",
     "provenance": "flow F174 step 11→12",
     "operation": "listUpgradeConversion"
    },
    {
     "to": "ADM-315",
     "trigger": "Works in Bulk, Group & Assisted Upgrade Operations",
     "provenance": "flow F174 step 13→14",
     "operation": "listUpgradeConversion"
    },
    {
     "to": "ADM-316",
     "trigger": "Works in Upgrade Execution, Credential Regeneration & Channel Controls",
     "provenance": "flow F174 step 15→16",
     "operation": "listUpgradeConversion"
    },
    {
     "to": "ADM-317",
     "trigger": "Works in Upgrade History, Exception Management & Audit Explorer",
     "provenance": "flow F174 step 17→18",
     "operation": "listUpgradeConversion"
    }
   ]
  },
  "density": "compact",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen both a metric directory (§Display) and a per-row directory (§Each configuration displays) — counts over a population, then the population",
  "purpose": "Provide administrators and operations teams with one centralized view of all ticket upgrade, exchange and conversion configurations and operational activity.",
  "purposeNote": "Authorized users can monitor the complete upgrade and conversion configuration portfolio and operational activity from one workspace.",
  "layout": {
   "template": "dashboard",
   "regions": [
    {
     "name": "contentBody",
     "slot": "filters",
     "components": [
      {
       "kind": "searchField",
       "label": "Search upgrade conversion",
       "provenance": "pack Ticket Upgrade, Exchange & Conversion_Reference.pdf, page 3 §Filter by"
      },
      {
       "kind": "multiSelect",
       "label": "Filter by",
       "columns": [
        "UpgradeConversionCommandCenterView.venue",
        "Event",
        "Product",
        "UpgradeConversionCommandCenterView.transactionType",
        "UpgradeConversionCommandCenterView.channel",
        "Customer Segment",
        "Rule Status",
        "Effective Date"
       ],
       "notes": "The pack filters this screen by venue, event, product, transaction type, channel, customer segment and 2 more — which are present is a decision the pack already made.",
       "provenance": "pack Ticket Upgrade, Exchange & Conversion_Reference.pdf, page 3 §Filter by"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "Active Upgrade Paths",
       "provenance": "pack Ticket Upgrade, Exchange & Conversion_Reference.pdf, page 3 §Display",
       "bindsTo": "UpgradeConversionCommandCenterView.activeUpgradePaths"
      },
      {
       "kind": "metricTile",
       "label": "Active Conversion Rules",
       "provenance": "pack Ticket Upgrade, Exchange & Conversion_Reference.pdf, page 3 §Display",
       "bindsTo": "UpgradeConversionCommandCenterView.activeConversionRules"
      },
      {
       "kind": "metricTile",
       "label": "Products Eligible for Upgrade",
       "provenance": "pack Ticket Upgrade, Exchange & Conversion_Reference.pdf, page 3 §Display",
       "bindsTo": "UpgradeConversionCommandCenterView.productsEligibleForUpgrade"
      },
      {
       "kind": "metricTile",
       "label": "Products Excluded",
       "provenance": "pack Ticket Upgrade, Exchange & Conversion_Reference.pdf, page 3 §Display",
       "bindsTo": "UpgradeConversionCommandCenterView.productsExcluded"
      },
      {
       "kind": "metricTile",
       "label": "Upgrades Today",
       "provenance": "pack Ticket Upgrade, Exchange & Conversion_Reference.pdf, page 3 §Display",
       "bindsTo": "UpgradeConversionCommandCenterView.upgradesToday"
      },
      {
       "kind": "metricTile",
       "label": "Conversions Today",
       "provenance": "pack Ticket Upgrade, Exchange & Conversion_Reference.pdf, page 3 §Display",
       "bindsTo": "UpgradeConversionCommandCenterView.conversionsToday"
      },
      {
       "kind": "metricTile",
       "label": "Upgrade Revenue",
       "provenance": "pack Ticket Upgrade, Exchange & Conversion_Reference.pdf, page 3 §Display"
      },
      {
       "kind": "metricTile",
       "label": "Pending Exceptions",
       "provenance": "pack Ticket Upgrade, Exchange & Conversion_Reference.pdf, page 3 §Display",
       "bindsTo": "UpgradeConversionCommandCenterView.pendingExceptions"
      },
      {
       "kind": "metricTile",
       "label": "Failed Conversions",
       "provenance": "pack Ticket Upgrade, Exchange & Conversion_Reference.pdf, page 3 §Display",
       "bindsTo": "UpgradeConversionCommandCenterView.failedConversions"
      },
      {
       "kind": "metricTile",
       "label": "Expiring Rules",
       "provenance": "pack Ticket Upgrade, Exchange & Conversion_Reference.pdf, page 3 §Display",
       "bindsTo": "UpgradeConversionCommandCenterView.expiringRules"
      },
      {
       "kind": "metricTile",
       "label": "Configuration Conflicts",
       "provenance": "pack Ticket Upgrade, Exchange & Conversion_Reference.pdf, page 3 §Display",
       "bindsTo": "UpgradeConversionCommandCenterView.configurationConflicts"
      },
      {
       "kind": "metricTile",
       "label": "Manual Overrides",
       "provenance": "pack Ticket Upgrade, Exchange & Conversion_Reference.pdf, page 3 §Display",
       "bindsTo": "UpgradeConversionCommandCenterView.manualOverrides"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "moduleTiles",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every upgrade conversion",
       "columns": [
        "UpgradeConversionCommandCenterView.ruleId",
        "UpgradeConversionCommandCenterView.ruleName",
        "UpgradeConversionCommandCenterView.sourceProduct",
        "UpgradeConversionCommandCenterView.targetProduct",
        "UpgradeConversionCommandCenterView.transactionType",
        "UpgradeConversionCommandCenterView.venue",
        "UpgradeConversionCommandCenterView.channel",
        "UpgradeConversionCommandCenterView.effectivePeriod",
        "UpgradeConversionCommandCenterView.financialMethod",
        "UpgradeConversionCommandCenterView.approvalRequirement",
        "UpgradeConversionCommandCenterView.status",
        "UpgradeConversionCommandCenterView.owner"
       ],
       "bindsTo": "UpgradeConversionCommandCenterView",
       "operation": "listUpgradeConversion",
       "provenance": "pack Ticket Upgrade, Exchange & Conversion_Reference.pdf, page 3 §Each configuration displays"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected upgrade conversion",
       "bindsTo": "UpgradeConversionCommandCenterView",
       "columns": [
        "UpgradeConversionCommandCenterView.ruleId",
        "UpgradeConversionCommandCenterView.ruleName",
        "UpgradeConversionCommandCenterView.sourceProduct",
        "UpgradeConversionCommandCenterView.targetProduct",
        "UpgradeConversionCommandCenterView.transactionType",
        "UpgradeConversionCommandCenterView.venue",
        "UpgradeConversionCommandCenterView.channel",
        "UpgradeConversionCommandCenterView.effectivePeriod",
        "UpgradeConversionCommandCenterView.financialMethod",
        "UpgradeConversionCommandCenterView.approvalRequirement",
        "UpgradeConversionCommandCenterView.status",
        "UpgradeConversionCommandCenterView.owner"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Upgrade”, “Downgrade”, “Exchange”, “Conversion”, “Person-Type Conversion”, “Product Conversion”.",
       "provenance": "pack Ticket Upgrade, Exchange & Conversion_Reference.pdf, page 3 §Each configuration displays"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The upgrade conversion list; the counts above it resolve separately.",
   "error": "Could not load. Names which read failed and leaves the upgrade conversion untouched.",
   "emptyFirstRun": "No upgrade conversion yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the upgrade conversion are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listUpgradeConversion",
    "contract": "orders",
    "purpose": "Upgrade & Conversion Command Center",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-308"
  },
  "apisNote": "Regenerated 9 September 2026 from Ticket Upgrade, Exchange & Conversion_Reference.pdf page 3. 26 of 31 labels bound to a contract property; 32 of 45 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-309",
  "name": "Upgrade & Conversion Path Builder",
  "module": "Commercial",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Ticket Upgrade, Exchange & Conversion_Reference.pdf",
   "board": "1",
   "number": "11.1.2",
   "page": 5
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/upgrade-conversion-path-builder-adm-309",
   "component": "apps/ticvai-web/src/routes/commercial/UpgradeConversionPathBuilder.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-308"
   ],
   "exitTo": [
    "ADM-308"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-308, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-308",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F174 step 2→3",
     "operation": "setUpgradeConversionPath"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Define exactly which products/tickets may be converted into which other products. This becomes the central conversion relationship engine.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Ticket Upgrade, Exchange & Conversion_Reference.pdf, page 5"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Ticket Upgrade, Exchange & Conversion_Reference.pdf, page 5"
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
       "provenance": "contract operation setUpgradeConversionPath"
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
       "impliedBy": "setUpgradeConversionPath"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The upgrade conversion path list.",
   "error": "Could not load. Names which read failed and leaves the upgrade conversion path untouched.",
   "emptyFirstRun": "No upgrade conversion path yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the upgrade conversion path are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setUpgradeConversionPath",
    "contract": "orders",
    "purpose": "Upgrade & Conversion Path Builder",
    "trigger": "onAction",
    "invalidates": [
     "setUpgradeConversionPath"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-309"
  },
  "apisNote": "Regenerated 9 September 2026 from Ticket Upgrade, Exchange & Conversion_Reference.pdf page 5. 0 of 0 labels bound to a contract property; 0 of 4 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-310",
  "name": "Upgrade Eligibility & Qualification Rules",
  "module": "Commercial",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Ticket Upgrade, Exchange & Conversion_Reference.pdf",
   "board": "1",
   "number": "11.1.3",
   "page": 7
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/upgrade-eligibility-qualification-rules-adm-310",
   "component": "apps/ticvai-web/src/routes/commercial/UpgradeEligibilityQualificationRules.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-308"
   ],
   "exitTo": [
    "ADM-308"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-308, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-308",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F174 step 4→5",
     "operation": "listUpgradeEligibilityQualification"
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure eligibility for) and no display directory — it is settings, not a population",
  "purpose": "Determine whether a particular ticket/customer/transaction qualifies for a configured upgrade or conversion path. A path existing does not automatically mean every ticket can use it.",
  "purposeNote": "customer, time and transaction conditions.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Valid",
       "provenance": "pack Ticket Upgrade, Exchange & Conversion_Reference.pdf, page 7 §Configure eligibility for"
      },
      {
       "kind": "selectField",
       "label": "Unused",
       "provenance": "pack Ticket Upgrade, Exchange & Conversion_Reference.pdf, page 7 §Configure eligibility for"
      },
      {
       "kind": "selectField",
       "label": "Partially Used",
       "provenance": "pack Ticket Upgrade, Exchange & Conversion_Reference.pdf, page 7 §Configure eligibility for"
      },
      {
       "kind": "selectField",
       "label": "Used",
       "provenance": "pack Ticket Upgrade, Exchange & Conversion_Reference.pdf, page 7 §Configure eligibility for"
      },
      {
       "kind": "selectField",
       "label": "Expired",
       "provenance": "pack Ticket Upgrade, Exchange & Conversion_Reference.pdf, page 7 §Configure eligibility for"
      },
      {
       "kind": "selectField",
       "label": "Cancelled",
       "provenance": "pack Ticket Upgrade, Exchange & Conversion_Reference.pdf, page 7 §Configure eligibility for"
      },
      {
       "kind": "selectField",
       "label": "Suspended",
       "provenance": "pack Ticket Upgrade, Exchange & Conversion_Reference.pdf, page 7 §Configure eligibility for"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The upgrade eligibility qualification configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the upgrade eligibility qualification untouched.",
   "emptyFirstRun": "No upgrade eligibility qualification configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listUpgradeEligibilityQualification",
    "contract": "orders",
    "purpose": "Upgrade Eligibility & Qualification Rules",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-310"
  },
  "apisNote": "Regenerated 9 September 2026 from Ticket Upgrade, Exchange & Conversion_Reference.pdf page 7. 0 of 0 labels bound to a contract property; 7 of 43 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-311",
  "name": "Upgrade Timing, Usage & Ticket Status Rules",
  "module": "Commercial",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Ticket Upgrade, Exchange & Conversion_Reference.pdf",
   "board": "1",
   "number": "11.1.4",
   "page": 9
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/upgrade-timing-usage-ticket-status-rules-adm-311",
   "component": "apps/ticvai-web/src/routes/commercial/UpgradeTimingUsageTicketStatusRules.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-308"
   ],
   "exitTo": [
    "ADM-308"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-308, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-308",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F174 step 6→7",
     "operation": "listUpgradeTimingUsage"
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure treatment of; Configure; Configure whether) and no display directory — it is settings, not a population",
  "purpose": "Define how ticket lifecycle state affects upgrade and conversion behavior. This deserves its own screen because a ticket may already have been partially consumed.",
  "purposeNote": "Upgrade and conversion rules correctly account for ticket lifecycle, usage and remaining entitlement before allowing a transaction.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 1 actions on this screen and the screen declares 1 operation.** Unserved: Grace Period. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Ticket Upgrade, Exchange & Conversion_Reference.pdf, page 9 §Support"
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
       "label": "Used Admissions",
       "provenance": "pack Ticket Upgrade, Exchange & Conversion_Reference.pdf, page 9 §Configure treatment of"
      },
      {
       "kind": "selectField",
       "label": "Unused Admissions",
       "provenance": "pack Ticket Upgrade, Exchange & Conversion_Reference.pdf, page 9 §Configure treatment of"
      },
      {
       "kind": "selectField",
       "label": "Remaining Days",
       "provenance": "pack Ticket Upgrade, Exchange & Conversion_Reference.pdf, page 9 §Configure treatment of"
      },
      {
       "kind": "selectField",
       "label": "Remaining Stored Value",
       "provenance": "pack Ticket Upgrade, Exchange & Conversion_Reference.pdf, page 9 §Configure treatment of"
      },
      {
       "kind": "selectField",
       "label": "Remaining Benefits",
       "provenance": "pack Ticket Upgrade, Exchange & Conversion_Reference.pdf, page 9 §Configure treatment of"
      },
      {
       "kind": "selectField",
       "label": "Invalidate",
       "provenance": "pack Ticket Upgrade, Exchange & Conversion_Reference.pdf, page 9 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Supersede",
       "provenance": "pack Ticket Upgrade, Exchange & Conversion_Reference.pdf, page 9 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Retain for History",
       "provenance": "pack Ticket Upgrade, Exchange & Conversion_Reference.pdf, page 9 §Configure"
      },
      {
       "kind": "textField",
       "label": "Link to New Ticket",
       "provenance": "pack Ticket Upgrade, Exchange & Conversion_Reference.pdf, page 9 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Partially Retain Entitlement",
       "provenance": "pack Ticket Upgrade, Exchange & Conversion_Reference.pdf, page 9 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Never Eligible",
       "provenance": "pack Ticket Upgrade, Exchange & Conversion_Reference.pdf, page 9 §Configure whether"
      },
      {
       "kind": "textField",
       "label": "Eligible Within Grace Period",
       "provenance": "pack Ticket Upgrade, Exchange & Conversion_Reference.pdf, page 9 §Configure whether"
      },
      {
       "kind": "selectField",
       "label": "Supervisor Exception Allowed",
       "provenance": "pack Ticket Upgrade, Exchange & Conversion_Reference.pdf, page 9 §Configure whether"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Grace Period",
       "provenance": "pack Ticket Upgrade, Exchange & Conversion_Reference.pdf, page 9 §Support"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The upgrade timing usage configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the upgrade timing usage untouched.",
   "emptyFirstRun": "No upgrade timing usage configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listUpgradeTimingUsage",
    "contract": "orders",
    "purpose": "Upgrade Timing, Usage & Ticket Status Rules",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-311"
  },
  "apisNote": "Regenerated 9 September 2026 from Ticket Upgrade, Exchange & Conversion_Reference.pdf page 9. 0 of 0 labels bound to a contract property; 14 of 32 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-312",
  "name": "Upgrade Financial Treatment & Price Difference Rules",
  "module": "Commercial",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Ticket Upgrade, Exchange & Conversion_Reference.pdf",
   "board": "1",
   "number": "11.1.5",
   "page": 10
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/upgrade-financial-treatment-price-difference-rules-adm-312",
   "component": "apps/ticvai-web/src/routes/commercial/UpgradeFinancialTreatmentPriceDifferenceRules.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-308"
   ],
   "exitTo": [
    "ADM-308"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-308, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-308",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F174 step 8→9",
     "operation": "listUpgradeFinancialTreatment"
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure whether target pricing uses; Configure whether existing) and no display directory — it is settings, not a population",
  "purpose": "Define how the financial relationship between the old and new product should be treated.",
  "purposeNote": "Area 11 can define upgrade financial policies while all monetary calculations are resolved consistently through TICVAI's central pricing engine.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Current Selling Price",
       "provenance": "pack Ticket Upgrade, Exchange & Conversion_Reference.pdf, page 10 §Configure whether target pricing uses"
      },
      {
       "kind": "selectField",
       "label": "Original-Date Price",
       "provenance": "pack Ticket Upgrade, Exchange & Conversion_Reference.pdf, page 10 §Configure whether target pricing uses"
      },
      {
       "kind": "selectField",
       "label": "Upgrade-Specific Rate",
       "provenance": "pack Ticket Upgrade, Exchange & Conversion_Reference.pdf, page 10 §Configure whether target pricing uses"
      },
      {
       "kind": "selectField",
       "label": "Contracted Rate",
       "provenance": "pack Ticket Upgrade, Exchange & Conversion_Reference.pdf, page 10 §Configure whether target pricing uses"
      },
      {
       "kind": "selectField",
       "label": "Membership Rate",
       "provenance": "pack Ticket Upgrade, Exchange & Conversion_Reference.pdf, page 10 §Configure whether target pricing uses"
      },
      {
       "kind": "selectField",
       "label": "Fixed Upgrade Price",
       "provenance": "pack Ticket Upgrade, Exchange & Conversion_Reference.pdf, page 10 §Configure whether target pricing uses"
      },
      {
       "kind": "selectField",
       "label": "Promotion",
       "provenance": "pack Ticket Upgrade, Exchange & Conversion_Reference.pdf, page 10 §Configure whether existing"
      },
      {
       "kind": "selectField",
       "label": "Membership Discount",
       "provenance": "pack Ticket Upgrade, Exchange & Conversion_Reference.pdf, page 10 §Configure whether existing"
      },
      {
       "kind": "selectField",
       "label": "Voucher",
       "provenance": "pack Ticket Upgrade, Exchange & Conversion_Reference.pdf, page 10 §Configure whether existing"
      },
      {
       "kind": "selectField",
       "label": "Corporate Discount",
       "provenance": "pack Ticket Upgrade, Exchange & Conversion_Reference.pdf, page 10 §Configure whether existing"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The upgrade financial treatment configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the upgrade financial treatment untouched.",
   "emptyFirstRun": "No upgrade financial treatment configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listUpgradeFinancialTreatment",
    "contract": "orders",
    "purpose": "Upgrade Financial Treatment & Price Difference Rules",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-312"
  },
  "apisNote": "Regenerated 9 September 2026 from Ticket Upgrade, Exchange & Conversion_Reference.pdf page 10. 0 of 0 labels bound to a contract property; 10 of 37 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-313",
  "name": "Pro-Rata, Residual Value & Entitlement Credit Configuration",
  "module": "Commercial",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Ticket Upgrade, Exchange & Conversion_Reference.pdf",
   "board": "1",
   "number": "11.1.6",
   "page": 12
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/pro-rata-residual-value-entitlement-credit-configuration-adm-313",
   "component": "apps/ticvai-web/src/routes/commercial/ProRataResidualValueEntitlementCreditConfigurati.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-308"
   ],
   "exitTo": [
    "ADM-308"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-308, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-308",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F174 step 10→11",
     "operation": "setProRataResidual"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Handle complex upgrades where part of the original product has already been consumed.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Ticket Upgrade, Exchange & Conversion_Reference.pdf, page 12"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Ticket Upgrade, Exchange & Conversion_Reference.pdf, page 12"
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
       "provenance": "contract operation setProRataResidual"
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
       "impliedBy": "setProRataResidual"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The pro-rata residual value list.",
   "error": "Could not load. Names which read failed and leaves the pro-rata residual value untouched.",
   "emptyFirstRun": "No pro-rata residual value yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the pro-rata residual value are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setProRataResidual",
    "contract": "orders",
    "purpose": "Pro-Rata, Residual Value & Entitlement Credit Configuration",
    "trigger": "onAction",
    "invalidates": [
     "setProRataResidual"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-313"
  },
  "apisNote": "Regenerated 9 September 2026 from Ticket Upgrade, Exchange & Conversion_Reference.pdf page 12. 0 of 0 labels bound to a contract property; 0 of 12 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-314",
  "name": "Person-Type, Product & Entitlement Conversion Rules",
  "module": "Commercial",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Ticket Upgrade, Exchange & Conversion_Reference.pdf",
   "board": "1",
   "number": "11.1.7",
   "page": 14
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/person-type-product-entitlement-conversion-rules-adm-314",
   "component": "apps/ticvai-web/src/routes/commercial/PersonTypeProductEntitlementConversionRules.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-308"
   ],
   "exitTo": [
    "ADM-308"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-308, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-308",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F174 step 12→13",
     "operation": "listPersonTypeProduct"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Handle conversions that change more than simply the commercial level of a ticket.",
  "purposeNote": "structures while preserving eligibility and consumption integrity.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Ticket Upgrade, Exchange & Conversion_Reference.pdf, page 14"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Ticket Upgrade, Exchange & Conversion_Reference.pdf, page 14"
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
       "impliedBy": "listPersonTypeProduct",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The person-type product entitlement list.",
   "error": "Could not load. Names which read failed and leaves the person-type product entitlement untouched.",
   "emptyFirstRun": "No person-type product entitlement yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the person-type product entitlement are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listPersonTypeProduct",
    "contract": "orders",
    "purpose": "Person-Type, Product & Entitlement Conversion Rules",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "PersonTypeProductEntitlementConversionRulesView.childAdult",
    "PersonTypeProductEntitlementConversionRulesView.juniorAdult",
    "PersonTypeProductEntitlementConversionRulesView.seniorAdult",
    "PersonTypeProductEntitlementConversionRulesView.residentTourist",
    "PersonTypeProductEntitlementConversionRulesView.standardMember"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-314"
  },
  "apisNote": "Regenerated 9 September 2026 from Ticket Upgrade, Exchange & Conversion_Reference.pdf page 14. 0 of 0 labels bound to a contract property; 0 of 29 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-315",
  "name": "Bulk, Group & Assisted Upgrade Operations",
  "module": "Commercial",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Ticket Upgrade, Exchange & Conversion_Reference.pdf",
   "board": "1",
   "number": "11.1.8",
   "page": 16
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/bulk-group-assisted-upgrade-operations-adm-315",
   "component": "apps/ticvai-web/src/routes/commercial/BulkGroupAssistedUpgradeOperations.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-308"
   ],
   "exitTo": [
    "ADM-308"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-308, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-308",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F174 step 14→15",
     "operation": "listBulkGroupAssisted"
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Select by; Configure) and no display directory — it is settings, not a population",
  "purpose": "Support operational upgrades involving multiple tickets rather than requiring staff to process each individually.",
  "purposeNote": "Authorized operations teams can safely process large group and bulk upgrades with eligibility, financial and exception validation before execution.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 1 actions on this screen and the screen declares 1 operation.** Unserved: Change Person Type. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Ticket Upgrade, Exchange & Conversion_Reference.pdf, page 16 §Support"
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
       "label": "Order",
       "provenance": "pack Ticket Upgrade, Exchange & Conversion_Reference.pdf, page 16 §Select by"
      },
      {
       "kind": "selectField",
       "label": "Reservation",
       "provenance": "pack Ticket Upgrade, Exchange & Conversion_Reference.pdf, page 16 §Select by"
      },
      {
       "kind": "selectField",
       "label": "Group",
       "provenance": "pack Ticket Upgrade, Exchange & Conversion_Reference.pdf, page 16 §Select by"
      },
      {
       "kind": "selectField",
       "label": "Event",
       "provenance": "pack Ticket Upgrade, Exchange & Conversion_Reference.pdf, page 16 §Select by"
      },
      {
       "kind": "selectField",
       "label": "Performance",
       "provenance": "pack Ticket Upgrade, Exchange & Conversion_Reference.pdf, page 16 §Select by"
      },
      {
       "kind": "selectField",
       "label": "Ticket Type",
       "provenance": "pack Ticket Upgrade, Exchange & Conversion_Reference.pdf, page 16 §Select by"
      },
      {
       "kind": "selectField",
       "label": "Seat Section",
       "provenance": "pack Ticket Upgrade, Exchange & Conversion_Reference.pdf, page 16 §Select by"
      },
      {
       "kind": "selectField",
       "label": "Customer Segment",
       "provenance": "pack Ticket Upgrade, Exchange & Conversion_Reference.pdf, page 16 §Select by"
      },
      {
       "kind": "textField",
       "label": "Process eligible tickets and exclude failures",
       "provenance": "pack Ticket Upgrade, Exchange & Conversion_Reference.pdf, page 16 §Configure"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Change Person Type",
       "provenance": "pack Ticket Upgrade, Exchange & Conversion_Reference.pdf, page 16 §Support"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The bulk group assisted configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the bulk group assisted untouched.",
   "emptyFirstRun": "No bulk group assisted configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listBulkGroupAssisted",
    "contract": "orders",
    "purpose": "Bulk, Group & Assisted Upgrade Operations",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-315"
  },
  "apisNote": "Regenerated 9 September 2026 from Ticket Upgrade, Exchange & Conversion_Reference.pdf page 16. 0 of 0 labels bound to a contract property; 10 of 37 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-316",
  "name": "Upgrade Execution, Credential Regeneration & Channel Controls",
  "module": "Commercial",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Ticket Upgrade, Exchange & Conversion_Reference.pdf",
   "board": "1",
   "number": "11.1.9",
   "page": 18
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/upgrade-execution-credential-regeneration-channel-contro-adm-316",
   "component": "apps/ticvai-web/src/routes/commercial/UpgradeExecutionCredentialRegenerationChannelCon.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-308"
   ],
   "exitTo": [
    "ADM-308"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-308, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-308",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F174 step 16→17",
     "operation": "createUpgradeCredentialRegeneration"
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Depending on configuration) and no display directory — it is settings, not a population",
  "purpose": "Control what happens operationally once an upgrade or conversion is approved and financially completed.",
  "purposeNote": "Completed upgrades correctly update tickets, entitlements, credentials, access rights, financial records and applicable sales channels as one controlled transaction.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Regenerate QR",
       "provenance": "pack Ticket Upgrade, Exchange & Conversion_Reference.pdf, page 18 §Depending on configuration"
      },
      {
       "kind": "selectField",
       "label": "Invalidate Old QR",
       "provenance": "pack Ticket Upgrade, Exchange & Conversion_Reference.pdf, page 18 §Depending on configuration"
      },
      {
       "kind": "selectField",
       "label": "Update Dynamic QR",
       "provenance": "pack Ticket Upgrade, Exchange & Conversion_Reference.pdf, page 18 §Depending on configuration"
      },
      {
       "kind": "selectField",
       "label": "Update RFID",
       "provenance": "pack Ticket Upgrade, Exchange & Conversion_Reference.pdf, page 18 §Depending on configuration"
      },
      {
       "kind": "selectField",
       "label": "Update NFC",
       "provenance": "pack Ticket Upgrade, Exchange & Conversion_Reference.pdf, page 18 §Depending on configuration"
      },
      {
       "kind": "selectField",
       "label": "Update Wallet Pass",
       "provenance": "pack Ticket Upgrade, Exchange & Conversion_Reference.pdf, page 18 §Depending on configuration"
      },
      {
       "kind": "selectField",
       "label": "Reissue Ticket",
       "provenance": "pack Ticket Upgrade, Exchange & Conversion_Reference.pdf, page 18 §Depending on configuration"
      },
      {
       "kind": "selectField",
       "label": "Preserve Existing Credential",
       "provenance": "pack Ticket Upgrade, Exchange & Conversion_Reference.pdf, page 18 §Depending on configuration"
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
       "provenance": "contract operation createUpgradeCredentialRegeneration"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The upgrade execution credential configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the upgrade execution credential untouched.",
   "emptyFirstRun": "No upgrade execution credential configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "createUpgradeCredentialRegeneration",
    "contract": "orders",
    "purpose": "Upgrade Execution, Credential Regeneration & Channel Controls",
    "trigger": "onAction",
    "invalidates": [
     "createUpgradeCredentialRegeneration"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-316"
  },
  "apisNote": "Regenerated 9 September 2026 from Ticket Upgrade, Exchange & Conversion_Reference.pdf page 18. 0 of 0 labels bound to a contract property; 8 of 49 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-317",
  "name": "Upgrade History, Exception Management & Audit Explorer",
  "module": "Commercial",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Ticket Upgrade, Exchange & Conversion_Reference.pdf",
   "board": "1",
   "number": "11.1.10",
   "page": 20
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/upgrade-history-exception-management-audit-explorer-adm-317",
   "component": "apps/ticvai-web/src/routes/commercial/UpgradeHistoryExceptionManagementAuditExplorer.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-308"
   ],
   "exitTo": [
    "ADM-308"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-308, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation."
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Provide complete operational and financial traceability for every upgrade, downgrade, exchange and conversion.",
  "purposeNote": "Every upgrade/conversion transaction and exception can be fully reconstructed across commercial, financial, ticketing, credential and user activity. Board 1 — Final Screen Register # Backend Screen Core Responsibility 11.1.1 Upgrade & Conversion Command Center Central operations",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "filters",
     "components": [
      {
       "kind": "searchField",
       "label": "Search upgrade history exception",
       "provenance": "pack Ticket Upgrade, Exchange & Conversion_Reference.pdf, page 20 §Search by"
      },
      {
       "kind": "multiSelect",
       "label": "Filter by",
       "columns": [
        "Ticket",
        "UpgradeHistoryExceptionManagementAuditExplorerView.order",
        "UpgradeHistoryExceptionManagementAuditExplorerView.customer",
        "Event",
        "Product",
        "UpgradeHistoryExceptionManagementAuditExplorerView.agent",
        "UpgradeHistoryExceptionManagementAuditExplorerView.channel",
        "UpgradeHistoryExceptionManagementAuditExplorerView.transactionType",
        "Date",
        "Exception"
       ],
       "notes": "The pack filters this screen by ticket, order, customer, event, product, agent and 4 more — which are present is a decision the pack already made.",
       "provenance": "pack Ticket Upgrade, Exchange & Conversion_Reference.pdf, page 20 §Search by"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every upgrade history exception",
       "columns": [
        "UpgradeHistoryExceptionManagementAuditExplorerView.eligibilityOverride",
        "UpgradeHistoryExceptionManagementAuditExplorerView.financialOverride",
        "UpgradeHistoryExceptionManagementAuditExplorerView.expiredTicketException",
        "UpgradeHistoryExceptionManagementAuditExplorerView.manualCredit",
        "UpgradeHistoryExceptionManagementAuditExplorerView.complimentaryUpgrade",
        "UpgradeHistoryExceptionManagementAuditExplorerView.failedCredentialUpdate",
        "UpgradeHistoryExceptionManagementAuditExplorerView.failedPaymentReconciliation",
        "UpgradeHistoryExceptionManagementAuditExplorerView.channelSynchronizationFailure"
       ],
       "bindsTo": "UpgradeHistoryExceptionManagementAuditExplorerView",
       "operation": "listUpgradeException",
       "provenance": "pack Ticket Upgrade, Exchange & Conversion_Reference.pdf, page 20 §Display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected upgrade history exception",
       "bindsTo": "UpgradeHistoryExceptionManagementAuditExplorerView",
       "columns": [
        "UpgradeHistoryExceptionManagementAuditExplorerView.eligibilityOverride",
        "UpgradeHistoryExceptionManagementAuditExplorerView.financialOverride",
        "UpgradeHistoryExceptionManagementAuditExplorerView.expiredTicketException",
        "UpgradeHistoryExceptionManagementAuditExplorerView.manualCredit",
        "UpgradeHistoryExceptionManagementAuditExplorerView.complimentaryUpgrade",
        "UpgradeHistoryExceptionManagementAuditExplorerView.failedCredentialUpdate",
        "UpgradeHistoryExceptionManagementAuditExplorerView.failedPaymentReconciliation",
        "UpgradeHistoryExceptionManagementAuditExplorerView.channelSynchronizationFailure"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Store”, “Standard Admission”, “Manual Override”, “Require”, “Source-to-target”, “Controls”.",
       "provenance": "pack Ticket Upgrade, Exchange & Conversion_Reference.pdf, page 20 §Display"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The upgrade history exception list.",
   "error": "Could not load. Names which read failed and leaves the upgrade history exception untouched.",
   "emptyFirstRun": "No upgrade history exception yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the upgrade history exception are still there. The pack's own statuses are controls — the state names which is selected.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listUpgradeException",
    "contract": "orders",
    "purpose": "Upgrade History, Exception Management & Audit Explorer",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "UpgradeHistoryExceptionManagementAuditExplorerView.eligibilityOverride",
    "UpgradeHistoryExceptionManagementAuditExplorerView.financialOverride",
    "UpgradeHistoryExceptionManagementAuditExplorerView.expiredTicketException",
    "UpgradeHistoryExceptionManagementAuditExplorerView.manualCredit",
    "UpgradeHistoryExceptionManagementAuditExplorerView.complimentaryUpgrade",
    "UpgradeHistoryExceptionManagementAuditExplorerView.failedCredentialUpdate"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-317"
  },
  "apisNote": "Regenerated 9 September 2026 from Ticket Upgrade, Exchange & Conversion_Reference.pdf page 20. 13 of 18 labels bound to a contract property; 23 of 88 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
 "createUpgradeCredentialRegeneration": {
  "method": "POST",
  "path": "/upgrade-credential-regeneration",
  "contract": "orders",
  "summary": "Upgrade Execution, Credential Regeneration & Channel Controls",
  "permission": "ORDER_CREATE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": "UpgradeExecutionCredentialRegenerationChannelControlInput",
  "responds": "UpgradeExecutionCredentialRegenerationChannelControlView"
 },
 "listBulkGroupAssisted": {
  "method": "GET",
  "path": "/bulk-group-assisted",
  "contract": "orders",
  "summary": "Bulk, Group & Assisted Upgrade Operations",
  "permission": "ORDER_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "BulkGroupAssistedUpgradeOperationsView"
 },
 "listPersonTypeProduct": {
  "method": "GET",
  "path": "/person-type-product",
  "contract": "orders",
  "summary": "Person-Type, Product & Entitlement Conversion Rules",
  "permission": "ORDER_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "PersonTypeProductEntitlementConversionRulesView"
 },
 "listUpgradeConversion": {
  "method": "GET",
  "path": "/upgrade-conversion",
  "contract": "orders",
  "summary": "Upgrade & Conversion Command Center",
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
    "name": "customerSegment",
    "in": "query",
    "required": false
   },
   {
    "name": "ruleStatus",
    "in": "query",
    "required": false
   },
   {
    "name": "effectiveDate",
    "in": "query",
    "required": false
   }
  ],
  "requestBody": null,
  "responds": "UpgradeConversionCommandCenterView"
 },
 "listUpgradeEligibilityQualification": {
  "method": "GET",
  "path": "/upgrade-eligibility-qualification",
  "contract": "orders",
  "summary": "Upgrade Eligibility & Qualification Rules",
  "permission": "ORDER_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "UpgradeEligibilityQualificationRulesView"
 },
 "listUpgradeException": {
  "method": "GET",
  "path": "/upgrade-exception",
  "contract": "orders",
  "summary": "Upgrade History, Exception Management & Audit Explorer",
  "permission": "ORDER_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "ticket",
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
    "name": "date",
    "in": "query",
    "required": false
   },
   {
    "name": "exception",
    "in": "query",
    "required": false
   }
  ],
  "requestBody": null,
  "responds": "UpgradeHistoryExceptionManagementAuditExplorerView"
 },
 "listUpgradeFinancialTreatment": {
  "method": "GET",
  "path": "/upgrade-financial-treatment",
  "contract": "orders",
  "summary": "Upgrade Financial Treatment & Price Difference Rules",
  "permission": "ORDER_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "UpgradeFinancialTreatmentPriceDifferenceRulesView"
 },
 "listUpgradeTimingUsage": {
  "method": "GET",
  "path": "/upgrade-timing-usage",
  "contract": "orders",
  "summary": "Upgrade Timing, Usage & Ticket Status Rules",
  "permission": "ORDER_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "UpgradeTimingUsageTicketStatusRulesView"
 },
 "setProRataResidual": {
  "method": "PUT",
  "path": "/pro-rata-residual",
  "contract": "orders",
  "summary": "Pro-Rata, Residual Value & Entitlement Credit Configuration",
  "permission": "ORDER_CREATE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": "ProRataResidualValueEntitlementCreditConfigurationInput",
  "responds": "ProRataResidualValueEntitlementCreditConfigurationView"
 },
 "setUpgradeConversionPath": {
  "method": "PUT",
  "path": "/upgrade-conversion-path",
  "contract": "orders",
  "summary": "Upgrade & Conversion Path Builder",
  "permission": "ORDER_CREATE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": "UpgradeConversionPathBuilderInput",
  "responds": "UpgradeConversionPathBuilderView"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "BulkGroupAssistedUpgradeOperationsView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over orders state, assembled at read time from tables that already exist",
  "description": "**What Bulk, Group & Assisted Upgrade Operations displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "byType": {
    "type": "string",
    "enum": [
     "order",
     "reservation",
     "group",
     "event",
     "performance",
     "ticketType",
     "seatSection",
     "customerSegment"
    ],
    "description": "Vocabulary listed under Select by."
   },
   "changePersonType": {
    "type": "string",
    "description": "Change Person Type"
   },
   "selected150Tickets": {
    "type": "string",
    "description": "Selected: 150 Tickets"
   },
   "eligible142": {
    "type": "string",
    "description": "Eligible: 142"
   },
   "notEligible8": {
    "type": "string",
    "description": "Not Eligible: 8"
   }
  }
 },
 "PersonTypeProductEntitlementConversionRulesView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over orders state, assembled at read time from tables that already exist",
  "description": "**What Person-Type, Product & Entitlement Conversion Rules displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "childAdult": {
    "type": "string",
    "description": "Child → Adult"
   },
   "juniorAdult": {
    "type": "string",
    "description": "Junior → Adult"
   },
   "seniorAdult": {
    "type": "string",
    "description": "Senior → Adult"
   },
   "residentTourist": {
    "type": "string",
    "description": "Resident → Tourist"
   },
   "standardMember": {
    "type": "string",
    "description": "Standard → Member"
   },
   "customPersonTypes": {
    "type": "string",
    "description": "Custom Person Types"
   },
   "differenceCalculatedThroughArea10": {
    "type": "string",
    "description": "Difference calculated through Area 10"
   },
   "andIdentify": {
    "type": "string",
    "description": "and identify"
   },
   "retained": {
    "type": "string",
    "description": "Retained"
   },
   "replaced": {
    "type": "string",
    "description": "Replaced"
   },
   "added": {
    "type": "string",
    "description": "Added"
   },
   "removed": {
    "type": "string",
    "description": "Removed"
   },
   "alreadyConsumed": {
    "type": "string",
    "description": "Already Consumed"
   },
   "age": {
    "type": "string",
    "description": "Age"
   },
   "membership": {
    "type": "string",
    "description": "Membership"
   },
   "residency": {
    "type": "string",
    "description": "Residency"
   },
   "corporateAssociation": {
    "type": "string",
    "description": "Corporate Association"
   },
   "identityVerification": {
    "type": "string",
    "description": "Identity Verification"
   },
   "otherEligibilityRules": {
    "type": "string",
    "description": "Other eligibility rules"
   }
  }
 },
 "ProRataResidualValueEntitlementCreditConfigurationInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures",
  "description": "**What Pro-Rata, Residual Value & Entitlement Credit Configuration submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "multiDayPasses": {
    "type": "string",
    "description": "Multi-Day Passes"
   },
   "memberships": {
    "type": "string",
    "description": "Memberships"
   },
   "annualPasses": {
    "type": "string",
    "description": "Annual Passes"
   },
   "multiAttractionProducts": {
    "type": "string",
    "description": "Multi-Attraction Products"
   },
   "packages": {
    "type": "string",
    "description": "Packages"
   },
   "storedEntitlements": {
    "type": "string",
    "description": "Stored Entitlements"
   },
   "remainingDaysOriginalDays": {
    "type": "string",
    "description": "Remaining Days / Original Days"
   },
   "remainingUsesTotalUses": {
    "type": "string",
    "description": "Remaining Uses / Total Uses"
   },
   "remainingCommercialValue": {
    "type": "string",
    "description": "Remaining Commercial Value"
   },
   "valueOfUnconsumedBenefits": {
    "type": "string",
    "description": "Value of unconsumed benefits"
   },
   "configuredCommercialAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Configured commercial amount"
   }
  }
 },
 "ProRataResidualValueEntitlementCreditConfigurationView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over orders state, assembled at read time from tables that already exist",
  "description": "**What Pro-Rata, Residual Value & Entitlement Credit Configuration displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "multiDayPasses": {
    "type": "string",
    "description": "Multi-Day Passes"
   },
   "memberships": {
    "type": "string",
    "description": "Memberships"
   },
   "annualPasses": {
    "type": "string",
    "description": "Annual Passes"
   },
   "multiAttractionProducts": {
    "type": "string",
    "description": "Multi-Attraction Products"
   },
   "packages": {
    "type": "string",
    "description": "Packages"
   },
   "storedEntitlements": {
    "type": "string",
    "description": "Stored Entitlements"
   },
   "remainingDaysOriginalDays": {
    "type": "string",
    "description": "Remaining Days / Original Days"
   },
   "remainingUsesTotalUses": {
    "type": "string",
    "description": "Remaining Uses / Total Uses"
   },
   "remainingCommercialValue": {
    "type": "string",
    "description": "Remaining Commercial Value"
   },
   "valueOfUnconsumedBenefits": {
    "type": "string",
    "description": "Value of unconsumed benefits"
   },
   "configuredCommercialAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Configured commercial amount"
   }
  }
 },
 "UpgradeConversionCommandCenterView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over orders state, assembled at read time from tables that already exist",
  "description": "**What Upgrade & Conversion Command Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "activeUpgradePaths": {
    "type": "integer",
    "description": "Active Upgrade Paths"
   },
   "activeConversionRules": {
    "type": "integer",
    "description": "Active Conversion Rules"
   },
   "productsEligibleForUpgrade": {
    "type": "string",
    "description": "Products Eligible for Upgrade"
   },
   "productsExcluded": {
    "type": "string",
    "description": "Products Excluded"
   },
   "upgradesToday": {
    "type": "string",
    "description": "Upgrades Today"
   },
   "conversionsToday": {
    "type": "string",
    "description": "Conversions Today"
   },
   "pendingExceptions": {
    "type": "integer",
    "description": "Pending Exceptions"
   },
   "failedConversions": {
    "type": "integer",
    "description": "Failed Conversions"
   },
   "expiringRules": {
    "type": "integer",
    "description": "Expiring Rules"
   },
   "configurationConflicts": {
    "type": "integer",
    "description": "Configuration Conflicts"
   },
   "manualOverrides": {
    "type": "integer",
    "description": "Manual Overrides"
   },
   "ruleId": {
    "type": "string",
    "description": "Rule ID"
   },
   "ruleName": {
    "type": "string",
    "description": "Rule Name"
   },
   "sourceProduct": {
    "type": "string",
    "description": "Source Product"
   },
   "targetProduct": {
    "type": "string",
    "description": "Target Product"
   },
   "transactionType": {
    "type": "string",
    "description": "Transaction Type"
   },
   "venue": {
    "type": "string",
    "description": "Venue"
   },
   "channel": {
    "type": "string",
    "description": "Channel"
   },
   "effectivePeriod": {
    "type": "string",
    "format": "date-time",
    "description": "Effective Period"
   },
   "financialMethod": {
    "type": "string",
    "description": "Financial Method"
   },
   "approvalRequirement": {
    "type": "string",
    "description": "Approval Requirement"
   },
   "status": {
    "type": "string",
    "description": "Status"
   },
   "owner": {
    "type": "string",
    "description": "Owner"
   },
   "standardPremium": {
    "type": "string",
    "description": "Standard → Premium"
   },
   "premiumStandard": {
    "type": "string",
    "description": "Premium → Standard"
   },
   "eventAEventB": {
    "type": "string",
    "description": "Event A → Event B"
   },
   "dayTicketAnnualPass": {
    "type": "string",
    "description": "Day Ticket → Annual Pass"
   },
   "childAdult": {
    "type": "string",
    "description": "Child → Adult"
   },
   "generalAdmissionCombinationTicket": {
    "type": "string",
    "description": "General Admission → Combination Ticket"
   }
  }
 },
 "UpgradeConversionPathBuilderInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures",
  "description": "**What Upgrade & Conversion Path Builder submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {}
 },
 "UpgradeConversionPathBuilderView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over orders state, assembled at read time from tables that already exist",
  "description": "**What Upgrade & Conversion Path Builder displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "note": {
    "type": "string"
   }
  }
 },
 "UpgradeEligibilityQualificationRulesView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over orders state, assembled at read time from tables that already exist",
  "description": "**What Upgrade Eligibility & Qualification Rules displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "ticketStatus": {
    "type": "string",
    "description": "Ticket Status"
   },
   "product": {
    "type": "string",
    "description": "Product"
   },
   "ticketType": {
    "type": "string",
    "description": "Ticket Type"
   },
   "event": {
    "type": "string",
    "description": "Event"
   },
   "performance": {
    "type": "string",
    "description": "Performance"
   },
   "visitDate": {
    "type": "string",
    "format": "date-time",
    "description": "Visit Date"
   },
   "timeslot": {
    "type": "string",
    "description": "Timeslot"
   },
   "customerType": {
    "type": "string",
    "description": "Customer Type"
   },
   "customerSegment": {
    "type": "string",
    "description": "Customer Segment"
   },
   "membership": {
    "type": "string",
    "description": "Membership"
   },
   "loyaltyTier": {
    "type": "string",
    "description": "Loyalty Tier"
   },
   "channel": {
    "type": "string",
    "description": "Channel"
   },
   "venue": {
    "type": "string",
    "description": "Venue"
   },
   "location": {
    "type": "string",
    "description": "Location"
   },
   "purchaseDate": {
    "type": "string",
    "format": "date-time",
    "description": "Purchase Date"
   },
   "purchaseChannel": {
    "type": "string",
    "description": "Purchase Channel"
   },
   "originalPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Original Price"
   },
   "promotionUsed": {
    "type": "string",
    "description": "Promotion Used"
   },
   "usageStatus": {
    "type": "string",
    "description": "Usage Status"
   },
   "valid": {
    "type": "string",
    "description": "Valid"
   },
   "unused": {
    "type": "string",
    "description": "Unused"
   },
   "partiallyUsed": {
    "type": "string",
    "description": "Partially Used"
   },
   "used": {
    "type": "string",
    "description": "Used"
   },
   "expired": {
    "type": "integer",
    "description": "Expired"
   },
   "cancelled": {
    "type": "integer",
    "description": "Cancelled"
   },
   "suspended": {
    "type": "string",
    "description": "Suspended"
   },
   "vipUpgradeEligible": {
    "type": "string",
    "description": "VIP Upgrade Eligible"
   },
   "vipUpgradeNotAvailable": {
    "type": "string",
    "description": "VIP Upgrade Not Available"
   },
   "previousUpgrade": {
    "type": "string",
    "description": "Previous Upgrade"
   },
   "previousConversion": {
    "type": "number",
    "description": "Previous Conversion"
   },
   "redemptionHistory": {
    "type": "string",
    "description": "Redemption History"
   },
   "withReason": {
    "type": "string",
    "description": "with reason"
   }
  }
 },
 "UpgradeExecutionCredentialRegenerationChannelControlInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures",
  "description": "**What Upgrade Execution, Credential Regeneration & Channel Controls submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "regenerateQr": {
    "type": "string",
    "description": "Regenerate QR"
   },
   "invalidateOldQr": {
    "type": "string",
    "description": "Invalidate Old QR"
   },
   "preserveExistingCredential": {
    "type": "string",
    "description": "Preserve Existing Credential"
   },
   "newEntitlement": {
    "type": "integer",
    "description": "New Entitlement"
   },
   "newAccessRights": {
    "type": "integer",
    "description": "New Access Rights"
   },
   "newZone": {
    "type": "integer",
    "description": "New Zone"
   },
   "newDate": {
    "type": "string",
    "format": "date-time",
    "description": "New Date"
   },
   "newPerformance": {
    "type": "integer",
    "description": "New Performance"
   },
   "oldCredentialInvalidation": {
    "type": "string",
    "description": "Old Credential Invalidation"
   },
   "b2cSelfService": {
    "type": "string",
    "description": "B2C Self-Service"
   },
   "mobileApp": {
    "type": "string",
    "description": "Mobile App"
   },
   "pos": {
    "type": "string",
    "description": "POS"
   },
   "callCenter": {
    "type": "string",
    "description": "Call Center"
   },
   "boxOffice": {
    "type": "string",
    "description": "Box Office"
   },
   "kiosk": {
    "type": "string",
    "description": "Kiosk"
   },
   "b2b": {
    "type": "string",
    "description": "B2B"
   },
   "reseller": {
    "type": "string",
    "description": "Reseller"
   },
   "api": {
    "type": "string",
    "description": "API"
   },
   "standardPremiumOnly": {
    "type": "string",
    "description": "Standard → Premium only"
   },
   "allAuthorizedPaths": {
    "type": "string",
    "description": "All authorized paths"
   },
   "updatedTicket": {
    "type": "string",
    "format": "date-time",
    "description": "Updated Ticket"
   },
   "updatedReceipt": {
    "type": "string",
    "format": "date-time",
    "description": "Updated Receipt"
   },
   "updatedInvoice": {
    "type": "string",
    "format": "date-time",
    "description": "Updated Invoice"
   },
   "confirmationEmail": {
    "type": "string",
    "description": "Confirmation Email"
   },
   "smsWhatsappWhereConfigured": {
    "type": "string",
    "description": "SMS/WhatsApp where configured"
   },
   "walletPassUpdate": {
    "type": "string",
    "description": "Wallet Pass Update"
   },
   "entitlementStatesInconsistent": {
    "type": "string",
    "description": "entitlement states inconsistent"
   }
  }
 },
 "UpgradeExecutionCredentialRegenerationChannelControlView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over orders state, assembled at read time from tables that already exist",
  "description": "**What Upgrade Execution, Credential Regeneration & Channel Controls displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "regenerateQr": {
    "type": "string",
    "description": "Regenerate QR"
   },
   "invalidateOldQr": {
    "type": "string",
    "description": "Invalidate Old QR"
   },
   "preserveExistingCredential": {
    "type": "string",
    "description": "Preserve Existing Credential"
   },
   "newEntitlement": {
    "type": "integer",
    "description": "New Entitlement"
   },
   "newAccessRights": {
    "type": "integer",
    "description": "New Access Rights"
   },
   "newZone": {
    "type": "integer",
    "description": "New Zone"
   },
   "newDate": {
    "type": "string",
    "format": "date-time",
    "description": "New Date"
   },
   "newPerformance": {
    "type": "integer",
    "description": "New Performance"
   },
   "oldCredentialInvalidation": {
    "type": "string",
    "description": "Old Credential Invalidation"
   },
   "b2cSelfService": {
    "type": "string",
    "description": "B2C Self-Service"
   },
   "mobileApp": {
    "type": "string",
    "description": "Mobile App"
   },
   "pos": {
    "type": "string",
    "description": "POS"
   },
   "callCenter": {
    "type": "string",
    "description": "Call Center"
   },
   "boxOffice": {
    "type": "string",
    "description": "Box Office"
   },
   "kiosk": {
    "type": "string",
    "description": "Kiosk"
   },
   "b2b": {
    "type": "string",
    "description": "B2B"
   },
   "reseller": {
    "type": "string",
    "description": "Reseller"
   },
   "api": {
    "type": "string",
    "description": "API"
   },
   "standardPremiumOnly": {
    "type": "string",
    "description": "Standard → Premium only"
   },
   "allAuthorizedPaths": {
    "type": "string",
    "description": "All authorized paths"
   },
   "updatedTicket": {
    "type": "string",
    "format": "date-time",
    "description": "Updated Ticket"
   },
   "updatedReceipt": {
    "type": "string",
    "format": "date-time",
    "description": "Updated Receipt"
   },
   "updatedInvoice": {
    "type": "string",
    "format": "date-time",
    "description": "Updated Invoice"
   },
   "confirmationEmail": {
    "type": "string",
    "description": "Confirmation Email"
   },
   "smsWhatsappWhereConfigured": {
    "type": "string",
    "description": "SMS/WhatsApp where configured"
   },
   "walletPassUpdate": {
    "type": "string",
    "description": "Wallet Pass Update"
   },
   "entitlementStatesInconsistent": {
    "type": "string",
    "description": "entitlement states inconsistent"
   }
  }
 },
 "UpgradeFinancialTreatmentPriceDifferenceRulesView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over orders state, assembled at read time from tables that already exist",
  "description": "**What Upgrade Financial Treatment & Price Difference Rules displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "basedOnRemainingValidity": {
    "type": "string",
    "description": "Based on remaining validity"
   },
   "basedOnRemainingEntitlement": {
    "type": "string",
    "description": "Based on remaining entitlement"
   },
   "customerPaysFullTargetPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Customer pays full target price"
   },
   "currentSellingPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Current Selling Price"
   },
   "originalDatePrice": {
    "type": "string",
    "format": "date-time",
    "description": "Original-Date Price"
   },
   "upgradeSpecificRate": {
    "type": "number",
    "description": "Upgrade-Specific Rate"
   },
   "contractedRate": {
    "type": "number",
    "description": "Contracted Rate"
   },
   "membershipRate": {
    "type": "number",
    "description": "Membership Rate"
   },
   "fixedUpgradePrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Fixed Upgrade Price"
   },
   "thisIsImportant": {
    "type": "string",
    "description": "This is important"
   },
   "configuredRate": {
    "type": "number",
    "description": "configured rate?"
   },
   "promotion": {
    "type": "string",
    "description": "Promotion"
   },
   "membershipDiscount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Membership Discount"
   },
   "voucher": {
    "type": "string",
    "description": "Voucher"
   },
   "corporateDiscount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Corporate Discount"
   },
   "targetPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Target Price"
   },
   "credit": {
    "type": "string",
    "description": "Credit"
   },
   "priceDifference": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Price Difference"
   },
   "discount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Discount"
   },
   "fees": {
    "type": "string",
    "description": "Fees"
   },
   "tax": {
    "type": "string",
    "description": "Tax"
   },
   "rounding": {
    "type": "string",
    "description": "Rounding"
   },
   "finalAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Final Amount"
   }
  }
 },
 "UpgradeHistoryExceptionManagementAuditExplorerView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over orders state, assembled at read time from tables that already exist",
  "description": "**What Upgrade History, Exception Management & Audit Explorer displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "transactionId": {
    "type": "string",
    "description": "Transaction ID"
   },
   "originalTicket": {
    "type": "string",
    "description": "Original Ticket"
   },
   "newTicket": {
    "type": "integer",
    "description": "New Ticket"
   },
   "sourceProduct": {
    "type": "string",
    "description": "Source Product"
   },
   "targetProduct": {
    "type": "string",
    "description": "Target Product"
   },
   "customer": {
    "type": "string",
    "description": "Customer"
   },
   "order": {
    "type": "string",
    "description": "Order"
   },
   "transactionType": {
    "type": "string",
    "description": "Transaction Type"
   },
   "originalValue": {
    "type": "string",
    "description": "Original Value"
   },
   "eligibleCredit": {
    "type": "string",
    "description": "Eligible Credit"
   },
   "priceDifference": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Price Difference"
   },
   "fees": {
    "type": "string",
    "description": "Fees"
   },
   "tax": {
    "type": "string",
    "description": "Tax"
   },
   "paymentRefund": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Payment/Refund"
   },
   "channel": {
    "type": "string",
    "description": "Channel"
   },
   "agent": {
    "type": "string",
    "description": "Agent"
   },
   "dateTime": {
    "type": "string",
    "format": "date-time",
    "description": "Date/Time"
   },
   "rule": {
    "type": "string",
    "description": "Rule"
   },
   "status": {
    "type": "string",
    "description": "Status"
   },
   "withEachTransactionLinked": {
    "type": "string",
    "description": "with each transaction linked"
   },
   "eligibilityOverride": {
    "type": "string",
    "description": "Eligibility Override"
   },
   "financialOverride": {
    "type": "string",
    "description": "Financial Override"
   },
   "expiredTicketException": {
    "type": "integer",
    "description": "Expired Ticket Exception"
   },
   "manualCredit": {
    "type": "string",
    "description": "Manual Credit"
   },
   "complimentaryUpgrade": {
    "type": "string",
    "description": "Complimentary Upgrade"
   },
   "failedCredentialUpdate": {
    "type": "integer",
    "description": "Failed Credential Update"
   },
   "failedPaymentReconciliation": {
    "type": "integer",
    "description": "Failed Payment Reconciliation"
   },
   "channelSynchronizationFailure": {
    "type": "string",
    "description": "Channel Synchronization Failure"
   },
   "reason": {
    "type": "string",
    "description": "Reason"
   },
   "user": {
    "type": "string",
    "description": "User"
   },
   "role": {
    "type": "string",
    "description": "Role"
   },
   "approval": {
    "type": "string",
    "description": "Approval"
   },
   "supportingNote": {
    "type": "string",
    "description": "Supporting Note"
   },
   "timestamp": {
    "type": "string",
    "format": "date-time",
    "description": "Timestamp"
   },
   "relationships": {
    "type": "string",
    "description": "relationships"
   },
   "controls": {
    "type": "string",
    "description": "controls"
   },
   "architectureForExample": {
    "type": "string",
    "description": "architecture—for example"
   },
   "eventAEventB": {
    "type": "string",
    "description": "Event A → Event B"
   }
  }
 },
 "UpgradeTimingUsageTicketStatusRulesView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over orders state, assembled at read time from tables that already exist",
  "description": "**What Upgrade Timing, Usage & Ticket Status Rules displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "beforeFirstUse": {
    "type": "string",
    "description": "Before First Use"
   },
   "afterFirstUse": {
    "type": "string",
    "description": "After First Use"
   },
   "partiallyConsumed": {
    "type": "string",
    "description": "Partially Consumed"
   },
   "beforeVisit": {
    "type": "string",
    "description": "Before Visit"
   },
   "duringVisit": {
    "type": "string",
    "description": "During Visit"
   },
   "afterVisit": {
    "type": "string",
    "description": "After Visit"
   },
   "beforeExpiry": {
    "type": "string",
    "format": "date-time",
    "description": "Before Expiry"
   },
   "gracePeriod": {
    "type": "string",
    "format": "date-time",
    "description": "Grace Period"
   },
   "exampleAttractionUpgrade": {
    "type": "string",
    "description": "Example — Attraction Upgrade"
   },
   "andAlreadyVisitedAttractionA": {
    "type": "string",
    "description": "and already visited Attraction A"
   },
   "product": {
    "type": "string",
    "description": "product"
   },
   "usedAdmissions": {
    "type": "string",
    "description": "Used Admissions"
   },
   "unusedAdmissions": {
    "type": "string",
    "description": "Unused Admissions"
   },
   "remainingDays": {
    "type": "string",
    "description": "Remaining Days"
   },
   "remainingStoredValue": {
    "type": "string",
    "description": "Remaining Stored Value"
   },
   "remainingBenefits": {
    "type": "string",
    "description": "Remaining Benefits"
   },
   "invalidate": {
    "type": "string",
    "description": "Invalidate"
   },
   "supersede": {
    "type": "string",
    "description": "Supersede"
   },
   "retainForHistory": {
    "type": "string",
    "description": "Retain for History"
   },
   "partiallyRetainEntitlement": {
    "type": "string",
    "description": "Partially Retain Entitlement"
   },
   "neverEligible": {
    "type": "string",
    "description": "Never Eligible"
   },
   "eligibleWithinGracePeriod": {
    "type": "string",
    "format": "date-time",
    "description": "Eligible Within Grace Period"
   },
   "supervisorExceptionAllowed": {
    "type": "boolean",
    "description": "Supervisor Exception Allowed"
   }
  }
 }
}
```
