# WS73 — Waiver, Consent & Digital Form Management board 2

**10 screens · 10 operations · 11 schemas · 2 permissions**

Platform P13 Venue CMS · ships as **venue-management** ·
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
  `MARKETING_MANAGE, MARKETING_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **0 of these operations work offline**
  
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `CMS-051` | Waiver Operations Command Center | commandCentre | 1 | 0 | — |
| `CMS-052` | Participant Waiver Status & Tracking | listDetail | 1 | 0 | — |
| `CMS-053` | Digital Signing & Collection Operations | listDetail | 1 | 0 | — |
| `CMS-054` | Minor, Guardian & Group Consent Management | listDetail | 1 | 0 | — |
| `CMS-055` | Waiver Verification & Validation Workspace | listDetail | 1 | 0 | — |
| `CMS-056` | Missing, Expired & Invalid Waiver Management | listDetail | 1 | 0 | — |
| `CMS-057` | On-Site Waiver & Exception Handling | configEditor | 1 | 0 | — |
| `CMS-058` | Compliance Evidence, Audit & Waiver Repository | listDetail | 1 | 0 | — |
| `CMS-059` | Waiver Analytics, Compliance & Operational Insights | listDetail | 1 | 0 | — |
| `CMS-060` | AI Waiver Compliance & Risk Intelligence Center | listDetail | 1 | 0 | — |

## Thin screens in this batch

**CMS-055, CMS-056, CMS-058, CMS-060 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "CMS-051",
  "name": "Waiver Operations Command Center",
  "module": "Policy",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Waiver, Consent & Digital Form Management_Reference.pdf",
   "board": "2",
   "number": "11.2.1",
   "page": 26
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/policy/waiver-operations-command-center-cms-051",
   "component": "apps/venue-management-web/src/routes/policy/WaiverOperationsCommandCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "CMS-001"
   ],
   "exitTo": [
    "CMS-001",
    "CMS-052",
    "CMS-053",
    "CMS-054",
    "CMS-055",
    "CMS-056",
    "CMS-057",
    "CMS-058",
    "CMS-059",
    "CMS-060"
   ],
   "inferred": false,
   "notes": "**The board's hub.** The workshop specified this module as boards of ten and opened each with a command centre; the other nine screens are that board's detail, so they are reached from here and return here.",
   "transitions": [
    {
     "to": "CMS-001",
     "trigger": "Tenant Workspace",
     "carries": [
      "tenantId"
     ],
     "provenance": "derived — CMS-001 declares entryState.params tenantId, so an edge into it must carry them"
    },
    {
     "to": "CMS-052",
     "trigger": "Works in Participant Waiver Status & Tracking",
     "provenance": "flow F182 step 1→2",
     "operation": "listWaiver"
    },
    {
     "to": "CMS-053",
     "trigger": "Works in Digital Signing & Collection Operations",
     "provenance": "flow F182 step 3→4",
     "operation": "listWaiver"
    },
    {
     "to": "CMS-054",
     "trigger": "Works in Minor, Guardian & Group Consent Management",
     "provenance": "flow F182 step 5→6",
     "operation": "listWaiver"
    },
    {
     "to": "CMS-055",
     "trigger": "Works in Waiver Verification & Validation Workspace",
     "provenance": "flow F182 step 7→8",
     "operation": "listWaiver"
    },
    {
     "to": "CMS-056",
     "trigger": "Works in Missing, Expired & Invalid Waiver Management",
     "provenance": "flow F182 step 9→10",
     "operation": "listWaiver"
    },
    {
     "to": "CMS-057",
     "trigger": "Works in On-Site Waiver & Exception Handling",
     "provenance": "flow F182 step 11→12",
     "operation": "listWaiver"
    },
    {
     "to": "CMS-058",
     "trigger": "Works in Compliance Evidence, Audit & Waiver Repository",
     "provenance": "flow F182 step 13→14",
     "operation": "listWaiver"
    },
    {
     "to": "CMS-059",
     "trigger": "Works in Waiver Analytics, Compliance & Operational Insights",
     "provenance": "flow F182 step 15→16",
     "operation": "listWaiver"
    },
    {
     "to": "CMS-060",
     "trigger": "Works in AI Waiver Compliance & Risk Intelligence Center",
     "provenance": "flow F182 step 17→18",
     "operation": "listWaiver"
    }
   ]
  },
  "density": "compact",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen both a metric directory (§Display) and a per-row directory (§Each record should show) — counts over a population, then the population",
  "purpose": "Provide Operations, Customer Service, Compliance and venue teams with a real-time overview of waiver completion across upcoming and active activities.",
  "purposeNote": "Operations can identify every upcoming activity affected by incomplete waiver requirements and prioritize corrective actions before customer arrival.",
  "layout": {
   "template": "dashboard",
   "regions": [
    {
     "name": "contentBody",
     "slot": "filters",
     "components": [
      {
       "kind": "searchField",
       "label": "Search waiver operations",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 26 §Filter by"
      },
      {
       "kind": "multiSelect",
       "label": "Filter by",
       "columns": [
        "Brand",
        "WaiverOperationsCommandCenterView.venue",
        "WaiverOperationsCommandCenterView.event",
        "WaiverOperationsCommandCenterView.product",
        "Waiver",
        "Date",
        "Status",
        "Participant Type",
        "Booking Channel"
       ],
       "notes": "The pack filters this screen by brand, venue, event, product, waiver, date and 3 more — which are present is a decision the pack already made.",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 26 §Filter by"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "Waivers Required",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 26 §Display",
       "bindsTo": "WaiverOperationsCommandCenterView.waiversRequired"
      },
      {
       "kind": "metricTile",
       "label": "Completed",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 26 §Display",
       "bindsTo": "WaiverOperationsCommandCenterView.completed"
      },
      {
       "kind": "metricTile",
       "label": "Pending",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 26 §Display",
       "bindsTo": "WaiverOperationsCommandCenterView.pending"
      },
      {
       "kind": "metricTile",
       "label": "Partially Completed",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 26 §Display",
       "bindsTo": "WaiverOperationsCommandCenterView.partiallyCompleted"
      },
      {
       "kind": "metricTile",
       "label": "Expiring",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 26 §Display",
       "bindsTo": "WaiverOperationsCommandCenterView.expiring"
      },
      {
       "kind": "metricTile",
       "label": "Invalid",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 26 §Display",
       "bindsTo": "WaiverOperationsCommandCenterView.invalid"
      },
      {
       "kind": "metricTile",
       "label": "Rejected",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 26 §Display",
       "bindsTo": "WaiverOperationsCommandCenterView.rejected"
      },
      {
       "kind": "metricTile",
       "label": "Guardian Consent Pending",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 26 §Display",
       "bindsTo": "WaiverOperationsCommandCenterView.guardianConsentPending"
      },
      {
       "kind": "metricTile",
       "label": "Upcoming Participants Missing Waiver",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 26 §Display",
       "bindsTo": "WaiverOperationsCommandCenterView.upcomingParticipantsMissingWaiver"
      },
      {
       "kind": "metricTile",
       "label": "Access Blocked",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 26 §Display",
       "bindsTo": "WaiverOperationsCommandCenterView.accessBlocked"
      },
      {
       "kind": "metricTile",
       "label": "Manual Exceptions",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 26 §Display",
       "bindsTo": "WaiverOperationsCommandCenterView.manualExceptions"
      },
      {
       "kind": "metricTile",
       "label": "Completion Rate",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 26 §Display",
       "bindsTo": "WaiverOperationsCommandCenterView.completionRate"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "moduleTiles",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every waiver operations",
       "columns": [
        "WaiverOperationsCommandCenterView.eventActivity",
        "WaiverOperationsCommandCenterView.venue",
        "WaiverOperationsCommandCenterView.dateTime",
        "WaiverOperationsCommandCenterView.participants",
        "WaiverOperationsCommandCenterView.waiversRequired",
        "WaiverOperationsCommandCenterView.completed",
        "WaiverOperationsCommandCenterView.missing",
        "WaiverOperationsCommandCenterView.completion",
        "WaiverOperationsCommandCenterView.guardianPending",
        "WaiverOperationsCommandCenterView.exceptions",
        "WaiverOperationsCommandCenterView.operationalRisk"
       ],
       "bindsTo": "WaiverOperationsCommandCenterView",
       "operation": "listWaiver",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 26 §Each record should show"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected waiver operations",
       "bindsTo": "WaiverOperationsCommandCenterView",
       "columns": [
        "WaiverOperationsCommandCenterView.eventActivity",
        "WaiverOperationsCommandCenterView.venue",
        "WaiverOperationsCommandCenterView.dateTime",
        "WaiverOperationsCommandCenterView.participants",
        "WaiverOperationsCommandCenterView.waiversRequired",
        "WaiverOperationsCommandCenterView.completed",
        "WaiverOperationsCommandCenterView.missing",
        "WaiverOperationsCommandCenterView.completion",
        "WaiverOperationsCommandCenterView.guardianPending",
        "WaiverOperationsCommandCenterView.exceptions",
        "WaiverOperationsCommandCenterView.operationalRisk"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Display by”, “Activity Status”, “Youth Attentio”, “Climbing”, “Session”.",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 26 §Each record should show"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The waiver operations list; the counts above it resolve separately.",
   "error": "Could not load. Names which read failed and leaves the waiver operations untouched.",
   "emptyFirstRun": "No waiver operations yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the waiver operations are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listWaiver",
    "contract": "marketing-crm",
    "purpose": "Waiver Operations Command Center",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P13 Venue CMS.dc.html#cms-051"
  },
  "apisNote": "Regenerated 9 September 2026 from Waiver, Consent & Digital Form Management_Reference.pdf page 26. 26 of 32 labels bound to a contract property; 32 of 55 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "_platform": {
   "code": "P13",
   "audience": "staff",
   "formFactor": "web",
   "shortName": "Venue CMS",
   "name": "Venue CMS — White Label",
   "app": "venue-management-web",
   "offlineCapable": false,
   "operator": "venue",
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P08",
     "P12",
     "P16"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "CMS-052",
  "name": "Participant Waiver Status & Tracking",
  "module": "Policy",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Waiver, Consent & Digital Form Management_Reference.pdf",
   "board": "2",
   "number": "11.2.2",
   "page": 28
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/policy/participant-waiver-status-tracking-cms-052",
   "component": "apps/venue-management-web/src/routes/policy/ParticipantWaiverStatusTracking.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "CMS-051"
   ],
   "exitTo": [
    "CMS-051"
   ],
   "inferred": false,
   "notes": "**Reached from CMS-051, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "CMS-051",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F182 step 2→3",
     "operation": "listParticipantWaiverStatus"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Provide a detailed operational record of the waiver requirements for each participant.",
  "purposeNote": "Staff can determine the complete waiver readiness of any participant from one screen.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "filters",
     "components": [
      {
       "kind": "searchField",
       "label": "Search participant waiver status",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 28 §Search by"
      },
      {
       "kind": "multiSelect",
       "label": "Filter by",
       "columns": [
        "ParticipantWaiverStatusTrackingView.participant",
        "ParticipantWaiverStatusTrackingView.booking",
        "ParticipantWaiverStatusTrackingView.ticket",
        "Email",
        "Mobile",
        "ParticipantWaiverStatusTrackingView.group",
        "Waiver ID"
       ],
       "notes": "The pack filters this screen by participant, booking, ticket, email, mobile, group and 1 more — which are present is a decision the pack already made.",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 28 §Search by"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every participant waiver status",
       "columns": [
        "ParticipantWaiverStatusTrackingView.participant",
        "ParticipantWaiverStatusTrackingView.participantId",
        "ParticipantWaiverStatusTrackingView.customerPurchaser",
        "ParticipantWaiverStatusTrackingView.booking",
        "ParticipantWaiverStatusTrackingView.ticket",
        "ParticipantWaiverStatusTrackingView.product",
        "ParticipantWaiverStatusTrackingView.event",
        "ParticipantWaiverStatusTrackingView.visitDate",
        "ParticipantWaiverStatusTrackingView.ageCategory",
        "ParticipantWaiverStatusTrackingView.group",
        "ParticipantWaiverStatusTrackingView.waiverRequirements",
        "ParticipantWaiverStatusTrackingView.completionStatus"
       ],
       "bindsTo": "ParticipantWaiverStatusTrackingView",
       "operation": "listParticipantWaiverStatus",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 28 §Display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected participant waiver status",
       "bindsTo": "ParticipantWaiverStatusTrackingView",
       "columns": [
        "ParticipantWaiverStatusTrackingView.participant",
        "ParticipantWaiverStatusTrackingView.participantId",
        "ParticipantWaiverStatusTrackingView.customerPurchaser",
        "ParticipantWaiverStatusTrackingView.booking",
        "ParticipantWaiverStatusTrackingView.ticket",
        "ParticipantWaiverStatusTrackingView.product",
        "ParticipantWaiverStatusTrackingView.event",
        "ParticipantWaiverStatusTrackingView.visitDate",
        "ParticipantWaiverStatusTrackingView.ageCategory",
        "ParticipantWaiverStatusTrackingView.group",
        "ParticipantWaiverStatusTrackingView.waiverRequirements",
        "ParticipantWaiverStatusTrackingView.completionStatus"
       ],
       "notes": null,
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 28 §Display"
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
       "notes": "**The pack separates these permissions and no action on the screen claims them yet:** Send Waiver, Resend, Open, View, Verify, Request Correction, Replace Signatory, Record Exception, View Audit History. Each needs attaching to the control it gates, or the screen needs the control.",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 28 §Authorized users can"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The participant waiver status list.",
   "error": "Could not load. Names which read failed and leaves the participant waiver status untouched.",
   "emptyFirstRun": "No participant waiver status yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the participant waiver status are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listParticipantWaiverStatus",
    "contract": "marketing-crm",
    "purpose": "Participant Waiver Status & Tracking",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "ParticipantWaiverStatusTrackingView.participant",
    "ParticipantWaiverStatusTrackingView.participantId",
    "ParticipantWaiverStatusTrackingView.customerPurchaser",
    "ParticipantWaiverStatusTrackingView.booking",
    "ParticipantWaiverStatusTrackingView.ticket",
    "ParticipantWaiverStatusTrackingView.product"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P13 Venue CMS.dc.html#cms-052"
  },
  "apisNote": "Regenerated 9 September 2026 from Waiver, Consent & Digital Form Management_Reference.pdf page 28. 16 of 19 labels bound to a contract property; 28 of 35 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "_platform": {
   "code": "P13",
   "audience": "staff",
   "formFactor": "web",
   "shortName": "Venue CMS",
   "name": "Venue CMS — White Label",
   "app": "venue-management-web",
   "offlineCapable": false,
   "operator": "venue",
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P08",
     "P12",
     "P16"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "CMS-053",
  "name": "Digital Signing & Collection Operations",
  "module": "Policy",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Waiver, Consent & Digital Form Management_Reference.pdf",
   "board": "2",
   "number": "11.2.3",
   "page": 29
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/policy/digital-signing-collection-operations-cms-053",
   "component": "apps/venue-management-web/src/routes/policy/DigitalSigningCollectionOperations.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "CMS-051"
   ],
   "exitTo": [
    "CMS-051"
   ],
   "inferred": false,
   "notes": "**Reached from CMS-051, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "CMS-051",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F182 step 4→5",
     "operation": "listDigitalSigningCollection"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Manage the actual distribution and completion of digital waivers.",
  "purposeNote": "channels.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 2 actions on this screen and the screen declares 1 operation.** Unserved: Email Link, SMS Link. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 29 §Support"
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
       "label": "Every digital signing collection",
       "columns": [
        "DigitalSigningCollectionOperationsView.sent",
        "DigitalSigningCollectionOperationsView.delivered",
        "DigitalSigningCollectionOperationsView.opened",
        "DigitalSigningCollectionOperationsView.started",
        "DigitalSigningCollectionOperationsView.completed",
        "DigitalSigningCollectionOperationsView.failed",
        "DigitalSigningCollectionOperationsView.expiredLinks"
       ],
       "bindsTo": "DigitalSigningCollectionOperationsView",
       "operation": "listDigitalSigningCollection",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 29 §Display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected digital signing collection",
       "bindsTo": "DigitalSigningCollectionOperationsView",
       "columns": [
        "DigitalSigningCollectionOperationsView.sent",
        "DigitalSigningCollectionOperationsView.delivered",
        "DigitalSigningCollectionOperationsView.opened",
        "DigitalSigningCollectionOperationsView.started",
        "DigitalSigningCollectionOperationsView.completed",
        "DigitalSigningCollectionOperationsView.failed",
        "DigitalSigningCollectionOperationsView.expiredLinks"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Link Issued”, “For groups”, “Waiver Completed”, “Security”.",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 29 §Display"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Email Link",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 29 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "SMS Link",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 29 §Support"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The digital signing collection list.",
   "error": "Could not load. Names which read failed and leaves the digital signing collection untouched.",
   "emptyFirstRun": "No digital signing collection yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the digital signing collection are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listDigitalSigningCollection",
    "contract": "marketing-crm",
    "purpose": "Digital Signing & Collection Operations",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "DigitalSigningCollectionOperationsView.sent",
    "DigitalSigningCollectionOperationsView.delivered",
    "DigitalSigningCollectionOperationsView.opened",
    "DigitalSigningCollectionOperationsView.started",
    "DigitalSigningCollectionOperationsView.completed",
    "DigitalSigningCollectionOperationsView.failed"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P13 Venue CMS.dc.html#cms-053"
  },
  "apisNote": "Regenerated 9 September 2026 from Waiver, Consent & Digital Form Management_Reference.pdf page 29. 7 of 7 labels bound to a contract property; 15 of 41 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "_platform": {
   "code": "P13",
   "audience": "staff",
   "formFactor": "web",
   "shortName": "Venue CMS",
   "name": "Venue CMS — White Label",
   "app": "venue-management-web",
   "offlineCapable": false,
   "operator": "venue",
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P08",
     "P12",
     "P16"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "CMS-054",
  "name": "Minor, Guardian & Group Consent Management",
  "module": "Policy",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Waiver, Consent & Digital Form Management_Reference.pdf",
   "board": "2",
   "number": "11.2.4",
   "page": 31
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/policy/minor-guardian-group-consent-management-cms-054",
   "component": "apps/venue-management-web/src/routes/policy/MinorGuardianGroupConsentManagement.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "CMS-051"
   ],
   "exitTo": [
    "CMS-051"
   ],
   "inferred": false,
   "notes": "**Reached from CMS-051, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "CMS-051",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F182 step 6→7",
     "operation": "listMinorGuardianGroup"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Manage complex consent relationships for minors and organized groups. This screen is particularly important for camps, academies, schools, family attractions and youth activities.",
  "purposeNote": "purchaser, participant and legal signatory as the same person.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 3 actions on this screen and the screen declares 1 operation.** Unserved: Send Guardian Links, Notify Group Leader, Export Missing List. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 31 §Allow"
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
       "label": "Every minor guardian group",
       "columns": [
        "MinorGuardianGroupConsentManagementView.organization",
        "MinorGuardianGroupConsentManagementView.groupLeader",
        "MinorGuardianGroupConsentManagementView.contact",
        "MinorGuardianGroupConsentManagementView.groupBooking",
        "MinorGuardianGroupConsentManagementView.responsibility",
        "MinorGuardianGroupConsentManagementView.permittedActions"
       ],
       "bindsTo": "MinorGuardianGroupConsentManagementView",
       "operation": "listMinorGuardianGroup",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 31 §Display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected minor guardian group",
       "bindsTo": "MinorGuardianGroupConsentManagementView",
       "columns": [
        "MinorGuardianGroupConsentManagementView.organization",
        "MinorGuardianGroupConsentManagementView.groupLeader",
        "MinorGuardianGroupConsentManagementView.contact",
        "MinorGuardianGroupConsentManagementView.groupBooking",
        "MinorGuardianGroupConsentManagementView.responsibility",
        "MinorGuardianGroupConsentManagementView.permittedActions"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Multiple Children”.",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 31 §Display"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Send Guardian Links",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 31 §Allow"
      },
      {
       "kind": "secondaryButton",
       "label": "Notify Group Leader",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 31 §Allow"
      },
      {
       "kind": "secondaryButton",
       "label": "Export Missing List",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 31 §Allow"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The minor guardian group list.",
   "error": "Could not load. Names which read failed and leaves the minor guardian group untouched.",
   "emptyFirstRun": "No minor guardian group yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the minor guardian group are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listMinorGuardianGroup",
    "contract": "marketing-crm",
    "purpose": "Minor, Guardian & Group Consent Management",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "MinorGuardianGroupConsentManagementView.organization",
    "MinorGuardianGroupConsentManagementView.groupLeader",
    "MinorGuardianGroupConsentManagementView.contact",
    "MinorGuardianGroupConsentManagementView.groupBooking",
    "MinorGuardianGroupConsentManagementView.responsibility",
    "MinorGuardianGroupConsentManagementView.permittedActions"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P13 Venue CMS.dc.html#cms-054"
  },
  "apisNote": "Regenerated 9 September 2026 from Waiver, Consent & Digital Form Management_Reference.pdf page 31. 6 of 6 labels bound to a contract property; 16 of 40 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "_platform": {
   "code": "P13",
   "audience": "staff",
   "formFactor": "web",
   "shortName": "Venue CMS",
   "name": "Venue CMS — White Label",
   "app": "venue-management-web",
   "offlineCapable": false,
   "operator": "venue",
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P08",
     "P12",
     "P16"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "CMS-055",
  "name": "Waiver Verification & Validation Workspace",
  "module": "Policy",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Waiver, Consent & Digital Form Management_Reference.pdf",
   "board": "2",
   "number": "11.2.5",
   "page": 33
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/policy/waiver-verification-validation-workspace-cms-055",
   "component": "apps/venue-management-web/src/routes/policy/WaiverVerificationValidationWorkspace.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "CMS-051"
   ],
   "exitTo": [
    "CMS-051"
   ],
   "inferred": false,
   "notes": "**Reached from CMS-051, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "CMS-051",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F182 step 8→9",
     "operation": "setWaiverVerificationValidation"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Provide authorized staff with a controlled process for reviewing waiver submissions that require verification.",
  "purposeNote": "Waivers requiring manual verification are reviewed consistently using governed validation criteria with complete reviewer accountability.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every waiver verification validation",
       "columns": [
        "WaiverVerificationValidationWorkspaceView.submissionId",
        "WaiverVerificationValidationWorkspaceView.participant",
        "WaiverVerificationValidationWorkspaceView.waiver",
        "WaiverVerificationValidationWorkspaceView.version",
        "WaiverVerificationValidationWorkspaceView.booking",
        "WaiverVerificationValidationWorkspaceView.signatory",
        "WaiverVerificationValidationWorkspaceView.submitted",
        "WaiverVerificationValidationWorkspaceView.verificationReason",
        "WaiverVerificationValidationWorkspaceView.risk",
        "WaiverVerificationValidationWorkspaceView.status"
       ],
       "bindsTo": "WaiverVerificationValidationWorkspaceView",
       "operation": "setWaiverVerificationValidation",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 33 §Display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected waiver verification validation",
       "bindsTo": "WaiverVerificationValidationWorkspaceView",
       "columns": [
        "WaiverVerificationValidationWorkspaceView.submissionId",
        "WaiverVerificationValidationWorkspaceView.participant",
        "WaiverVerificationValidationWorkspaceView.waiver",
        "WaiverVerificationValidationWorkspaceView.version",
        "WaiverVerificationValidationWorkspaceView.booking",
        "WaiverVerificationValidationWorkspaceView.signatory",
        "WaiverVerificationValidationWorkspaceView.submitted",
        "WaiverVerificationValidationWorkspaceView.verificationReason",
        "WaiverVerificationValidationWorkspaceView.risk",
        "WaiverVerificationValidationWorkspaceView.status"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Reviewer Actions”, “Human Governance”.",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 33 §Display"
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
       "provenance": "contract operation setWaiverVerificationValidation"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The waiver verification validation list.",
   "error": "Could not load. Names which read failed and leaves the waiver verification validation untouched.",
   "emptyFirstRun": "No waiver verification validation yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the waiver verification validation are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setWaiverVerificationValidation",
    "contract": "marketing-crm",
    "purpose": "Waiver Verification & Validation Workspace",
    "trigger": "onAction",
    "invalidates": [
     "setWaiverVerificationValidation"
    ]
   }
  ],
  "entryState": {
   "preloaded": [
    "WaiverVerificationValidationWorkspaceView.submissionId",
    "WaiverVerificationValidationWorkspaceView.participant",
    "WaiverVerificationValidationWorkspaceView.waiver",
    "WaiverVerificationValidationWorkspaceView.version",
    "WaiverVerificationValidationWorkspaceView.booking",
    "WaiverVerificationValidationWorkspaceView.signatory"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P13 Venue CMS.dc.html#cms-055"
  },
  "apisNote": "Regenerated 9 September 2026 from Waiver, Consent & Digital Form Management_Reference.pdf page 33. 10 of 10 labels bound to a contract property; 20 of 38 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "_platform": {
   "code": "P13",
   "audience": "staff",
   "formFactor": "web",
   "shortName": "Venue CMS",
   "name": "Venue CMS — White Label",
   "app": "venue-management-web",
   "offlineCapable": false,
   "operator": "venue",
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P08",
     "P12",
     "P16"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "CMS-056",
  "name": "Missing, Expired & Invalid Waiver Management",
  "module": "Policy",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Waiver, Consent & Digital Form Management_Reference.pdf",
   "board": "2",
   "number": "11.2.6",
   "page": 34
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/policy/missing-expired-invalid-waiver-management-cms-056",
   "component": "apps/venue-management-web/src/routes/policy/MissingExpiredInvalidWaiverManagement.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "CMS-051"
   ],
   "exitTo": [
    "CMS-051"
   ],
   "inferred": false,
   "notes": "**Reached from CMS-051, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "CMS-051",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F182 step 10→11",
     "operation": "listMissingExpiredInvalid"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Provide a dedicated exception workspace for waiver requirements preventing operational readiness.",
  "purposeNote": "Missing, invalid and expired waiver requirements are proactively identified and managed before they cause unnecessary admission or operational failures.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every missing expired invalid",
       "columns": [
        "MissingExpiredInvalidWaiverManagementView.participant",
        "MissingExpiredInvalidWaiverManagementView.booking",
        "MissingExpiredInvalidWaiverManagementView.event",
        "MissingExpiredInvalidWaiverManagementView.visitTime",
        "MissingExpiredInvalidWaiverManagementView.waiver",
        "MissingExpiredInvalidWaiverManagementView.problem",
        "MissingExpiredInvalidWaiverManagementView.timeRemaining",
        "MissingExpiredInvalidWaiverManagementView.accessImpact",
        "MissingExpiredInvalidWaiverManagementView.owner",
        "MissingExpiredInvalidWaiverManagementView.status"
       ],
       "bindsTo": "MissingExpiredInvalidWaiverManagementView",
       "operation": "listMissingExpiredInvalid",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 34 §Display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected missing expired invalid",
       "bindsTo": "MissingExpiredInvalidWaiverManagementView",
       "columns": [
        "MissingExpiredInvalidWaiverManagementView.participant",
        "MissingExpiredInvalidWaiverManagementView.booking",
        "MissingExpiredInvalidWaiverManagementView.event",
        "MissingExpiredInvalidWaiverManagementView.visitTime",
        "MissingExpiredInvalidWaiverManagementView.waiver",
        "MissingExpiredInvalidWaiverManagementView.problem",
        "MissingExpiredInvalidWaiverManagementView.timeRemaining",
        "MissingExpiredInvalidWaiverManagementView.accessImpact",
        "MissingExpiredInvalidWaiverManagementView.owner",
        "MissingExpiredInvalidWaiverManagementView.status"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Include”, “Highest priority should consider”, “Authorized staff can”.",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 34 §Display"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The missing expired invalid list.",
   "error": "Could not load. Names which read failed and leaves the missing expired invalid untouched.",
   "emptyFirstRun": "No missing expired invalid yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the missing expired invalid are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listMissingExpiredInvalid",
    "contract": "marketing-crm",
    "purpose": "Missing, Expired & Invalid Waiver Management",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "MissingExpiredInvalidWaiverManagementView.participant",
    "MissingExpiredInvalidWaiverManagementView.booking",
    "MissingExpiredInvalidWaiverManagementView.event",
    "MissingExpiredInvalidWaiverManagementView.visitTime",
    "MissingExpiredInvalidWaiverManagementView.waiver",
    "MissingExpiredInvalidWaiverManagementView.problem"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P13 Venue CMS.dc.html#cms-056"
  },
  "apisNote": "Regenerated 9 September 2026 from Waiver, Consent & Digital Form Management_Reference.pdf page 34. 10 of 10 labels bound to a contract property; 10 of 47 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "_platform": {
   "code": "P13",
   "audience": "staff",
   "formFactor": "web",
   "shortName": "Venue CMS",
   "name": "Venue CMS — White Label",
   "app": "venue-management-web",
   "offlineCapable": false,
   "operator": "venue",
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P08",
     "P12",
     "P16"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "CMS-057",
  "name": "On-Site Waiver & Exception Handling",
  "module": "Policy",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Waiver, Consent & Digital Form Management_Reference.pdf",
   "board": "2",
   "number": "11.2.7",
   "page": 36
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/policy/on-site-waiver-exception-handling-cms-057",
   "component": "apps/venue-management-web/src/routes/policy/OnSiteWaiverExceptionHandling.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "CMS-051"
   ],
   "exitTo": [
    "CMS-051"
   ],
   "inferred": false,
   "notes": "**Reached from CMS-051, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "CMS-051",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F182 step 12→13",
     "operation": "listSiteWaiverException"
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Depending on configuration) and no display directory — it is settings, not a population",
  "purpose": "Support customers who arrive at the venue without completing required waivers.",
  "purposeNote": "On-site staff can efficiently resolve legitimate waiver issues while preventing unauthorized bypass of mandatory consent requirements.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Send Mobile Link",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 36 §Depending on configuration"
      },
      {
       "kind": "textField",
       "label": "Display QR for Customer",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 36 §Depending on configuration"
      },
      {
       "kind": "selectField",
       "label": "Complete on Kiosk",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 36 §Depending on configuration"
      },
      {
       "kind": "textField",
       "label": "Complete on Staff Tablet",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 36 §Depending on configuration"
      },
      {
       "kind": "selectField",
       "label": "Contact Guardian",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 36 §Depending on configuration"
      },
      {
       "kind": "selectField",
       "label": "Re-Sign Updated Waiver",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 36 §Depending on configuration"
      },
      {
       "kind": "selectField",
       "label": "Request Supervisor Exception",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 36 §Depending on configuration"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The on-site waiver exception configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the on-site waiver exception untouched.",
   "emptyFirstRun": "No on-site waiver exception configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listSiteWaiverException",
    "contract": "marketing-crm",
    "purpose": "On-Site Waiver & Exception Handling",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P13 Venue CMS.dc.html#cms-057"
  },
  "apisNote": "Regenerated 9 September 2026 from Waiver, Consent & Digital Form Management_Reference.pdf page 36. 0 of 0 labels bound to a contract property; 7 of 40 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "_platform": {
   "code": "P13",
   "audience": "staff",
   "formFactor": "web",
   "shortName": "Venue CMS",
   "name": "Venue CMS — White Label",
   "app": "venue-management-web",
   "offlineCapable": false,
   "operator": "venue",
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P08",
     "P12",
     "P16"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "CMS-058",
  "name": "Compliance Evidence, Audit & Waiver Repository",
  "module": "Policy",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Waiver, Consent & Digital Form Management_Reference.pdf",
   "board": "2",
   "number": "11.2.8",
   "page": 38
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/policy/compliance-evidence-audit-waiver-repository-cms-058",
   "component": "apps/venue-management-web/src/routes/policy/ComplianceEvidenceAuditWaiverRepository.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "CMS-051"
   ],
   "exitTo": [
    "CMS-051"
   ],
   "inferred": false,
   "notes": "**Reached from CMS-051, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "CMS-051",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F182 step 14→15",
     "operation": "listComplianceEvidenceWaiver"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Maintain the complete evidentiary record of every waiver and consent transaction.",
  "purposeNote": "completed waiver at the relevant point in time.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 38"
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
       "label": "Search compliance evidence audit",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 38 §Search by"
      },
      {
       "kind": "multiSelect",
       "label": "Filter by",
       "columns": [
        "Participant",
        "Customer",
        "Ticket",
        "Booking",
        "Event",
        "Waiver",
        "Version",
        "Signatory",
        "Date",
        "Venue"
       ],
       "notes": "The pack filters this screen by participant, customer, ticket, booking, event, waiver and 4 more — which are present is a decision the pack already made.",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 38 §Search by"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The compliance evidence audit list.",
   "error": "Could not load. Names which read failed and leaves the compliance evidence audit untouched.",
   "emptyFirstRun": "No compliance evidence audit yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the compliance evidence audit are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listComplianceEvidenceWaiver",
    "contract": "marketing-crm",
    "purpose": "Compliance Evidence, Audit & Waiver Repository",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P13 Venue CMS.dc.html#cms-058"
  },
  "apisNote": "Regenerated 9 September 2026 from Waiver, Consent & Digital Form Management_Reference.pdf page 38. 0 of 10 labels bound to a contract property; 10 of 48 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "_platform": {
   "code": "P13",
   "audience": "staff",
   "formFactor": "web",
   "shortName": "Venue CMS",
   "name": "Venue CMS — White Label",
   "app": "venue-management-web",
   "offlineCapable": false,
   "operator": "venue",
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P08",
     "P12",
     "P16"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "CMS-059",
  "name": "Waiver Analytics, Compliance & Operational Insights",
  "module": "Policy",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Waiver, Consent & Digital Form Management_Reference.pdf",
   "board": "2",
   "number": "11.2.9",
   "page": 39
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/policy/waiver-analytics-compliance-operational-insights-cms-059",
   "component": "apps/venue-management-web/src/routes/policy/WaiverAnalyticsComplianceOperationalInsights.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "CMS-051"
   ],
   "exitTo": [
    "CMS-051"
   ],
   "inferred": false,
   "notes": "**Reached from CMS-051, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "CMS-051",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F182 step 16→17",
     "operation": "listWaiverComplianceOperational"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Analyze) and no metric row",
  "purpose": "Analyze waiver completion, customer behavior and operational effectiveness.",
  "purposeNote": "Management can understand waiver compliance and identify configuration or process improvements that reduce customer friction and on-site workload.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "filters",
     "components": [
      {
       "kind": "searchField",
       "label": "Search waiver analytics compliance",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 39 §Filter by"
      },
      {
       "kind": "multiSelect",
       "label": "Filter by",
       "columns": [
        "Waiver",
        "Version",
        "Product",
        "Event",
        "Venue",
        "Customer Type",
        "Participant Type",
        "Channel",
        "Language",
        "Group"
       ],
       "notes": "The pack filters this screen by waiver, version, product, event, venue, customer type and 4 more — which are present is a decision the pack already made.",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 39 §Filter by"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every waiver analytics compliance",
       "columns": [
        "WaiverAnalyticsComplianceOperationalInsightsView.waiversAssigned",
        "WaiverAnalyticsComplianceOperationalInsightsView.completionRate",
        "WaiverAnalyticsComplianceOperationalInsightsView.preArrivalCompletion",
        "WaiverAnalyticsComplianceOperationalInsightsView.onSiteCompletion",
        "WaiverAnalyticsComplianceOperationalInsightsView.averageCompletionTime",
        "WaiverAnalyticsComplianceOperationalInsightsView.guardianCompletionRate",
        "WaiverAnalyticsComplianceOperationalInsightsView.rejectionRate",
        "WaiverAnalyticsComplianceOperationalInsightsView.exceptionRate",
        "WaiverAnalyticsComplianceOperationalInsightsView.accessBlocks",
        "WaiverAnalyticsComplianceOperationalInsightsView.reminderEffectiveness",
        "WaiverAnalyticsComplianceOperationalInsightsView.checkInDelays",
        "WaiverAnalyticsComplianceOperationalInsightsView.staffInterventions",
        "WaiverAnalyticsComplianceOperationalInsightsView.onSiteCompletions",
        "WaiverAnalyticsComplianceOperationalInsightsView.exceptions"
       ],
       "bindsTo": "WaiverAnalyticsComplianceOperationalInsightsView",
       "operation": "listWaiverComplianceOperational",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 39 §Analyze"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected waiver analytics compliance",
       "bindsTo": "WaiverAnalyticsComplianceOperationalInsightsView",
       "columns": [
        "WaiverAnalyticsComplianceOperationalInsightsView.waiversAssigned",
        "WaiverAnalyticsComplianceOperationalInsightsView.completionRate",
        "WaiverAnalyticsComplianceOperationalInsightsView.preArrivalCompletion",
        "WaiverAnalyticsComplianceOperationalInsightsView.onSiteCompletion",
        "WaiverAnalyticsComplianceOperationalInsightsView.averageCompletionTime",
        "WaiverAnalyticsComplianceOperationalInsightsView.guardianCompletionRate",
        "WaiverAnalyticsComplianceOperationalInsightsView.rejectionRate",
        "WaiverAnalyticsComplianceOperationalInsightsView.exceptionRate",
        "WaiverAnalyticsComplianceOperationalInsightsView.accessBlocks",
        "WaiverAnalyticsComplianceOperationalInsightsView.reminderEffectiveness",
        "WaiverAnalyticsComplianceOperationalInsightsView.checkInDelays",
        "WaiverAnalyticsComplianceOperationalInsightsView.staffInterventions",
        "WaiverAnalyticsComplianceOperationalInsightsView.onSiteCompletions",
        "WaiverAnalyticsComplianceOperationalInsightsView.exceptions"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Visualize”, “Abandonment Analysis”, “Reminder Analysis”.",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 39 §Analyze"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The waiver analytics compliance list.",
   "error": "Could not load. Names which read failed and leaves the waiver analytics compliance untouched.",
   "emptyFirstRun": "No waiver analytics compliance yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the waiver analytics compliance are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listWaiverComplianceOperational",
    "contract": "marketing-crm",
    "purpose": "Waiver Analytics, Compliance & Operational Insights",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "WaiverAnalyticsComplianceOperationalInsightsView.waiversAssigned",
    "WaiverAnalyticsComplianceOperationalInsightsView.completionRate",
    "WaiverAnalyticsComplianceOperationalInsightsView.preArrivalCompletion",
    "WaiverAnalyticsComplianceOperationalInsightsView.onSiteCompletion",
    "WaiverAnalyticsComplianceOperationalInsightsView.averageCompletionTime",
    "WaiverAnalyticsComplianceOperationalInsightsView.guardianCompletionRate"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P13 Venue CMS.dc.html#cms-059"
  },
  "apisNote": "Regenerated 9 September 2026 from Waiver, Consent & Digital Form Management_Reference.pdf page 39. 14 of 24 labels bound to a contract property; 24 of 45 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "_platform": {
   "code": "P13",
   "audience": "staff",
   "formFactor": "web",
   "shortName": "Venue CMS",
   "name": "Venue CMS — White Label",
   "app": "venue-management-web",
   "offlineCapable": false,
   "operator": "venue",
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P08",
     "P12",
     "P16"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "CMS-060",
  "name": "AI Waiver Compliance & Risk Intelligence Center",
  "module": "Policy",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Waiver, Consent & Digital Form Management_Reference.pdf",
   "board": "2",
   "number": "11.2.10",
   "page": 41
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/policy/ai-waiver-compliance-risk-intelligence-center-cms-060",
   "component": "apps/venue-management-web/src/routes/policy/AiWaiverComplianceRiskIntelligenceCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "CMS-051"
   ],
   "exitTo": [
    "CMS-051"
   ],
   "inferred": false,
   "notes": "**Reached from CMS-051, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation."
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Provide an AI intelligence layer across the complete waiver lifecycle. This should combine Board 1 configuration data + Board 2 operational data.",
  "purposeNote": "while preserving human/legal governance over consent and exceptions. Board 2 — Final Screen Register",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 41"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 41"
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
       "kind": "banner",
       "label": "Permissions this screen separates",
       "notes": "**The pack separates these permissions and no action on the screen claims them yet:** “Which waiver version generates the most corrections?”. Each needs attaching to the control it gates, or the screen needs the control.",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 41 §Authorized users can ask"
      }
     ]
    },
    {
     "name": "contentBody",
     "components": [
      {
       "kind": "dataTable",
       "derived": true,
       "impliedBy": "listWaiverComplianceRisk",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The waiver compliance risk list.",
   "error": "Could not load. Names which read failed and leaves the waiver compliance risk untouched.",
   "emptyFirstRun": "No waiver compliance risk yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the waiver compliance risk are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listWaiverComplianceRisk",
    "contract": "marketing-crm",
    "purpose": "AI Waiver Compliance & Risk Intelligence Center",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "AiWaiverComplianceRiskIntelligenceCenterView.templates",
    "AiWaiverComplianceRiskIntelligenceCenterView.versions",
    "AiWaiverComplianceRiskIntelligenceCenterView.questions",
    "AiWaiverComplianceRiskIntelligenceCenterView.signatoryRules",
    "AiWaiverComplianceRiskIntelligenceCenterView.productAssociations"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P13 Venue CMS.dc.html#cms-060"
  },
  "apisNote": "Regenerated 9 September 2026 from Waiver, Consent & Digital Form Management_Reference.pdf page 41. 0 of 0 labels bound to a contract property; 1 of 87 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "_platform": {
   "code": "P13",
   "audience": "staff",
   "formFactor": "web",
   "shortName": "Venue CMS",
   "name": "Venue CMS — White Label",
   "app": "venue-management-web",
   "offlineCapable": false,
   "operator": "venue",
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P08",
     "P12",
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
 "listComplianceEvidenceWaiver": {
  "method": "GET",
  "path": "/compliance-evidence-waiver",
  "contract": "marketing-crm",
  "summary": "Compliance Evidence, Audit & Waiver Repository",
  "permission": "MARKETING_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "participant",
    "in": "query",
    "required": false
   },
   {
    "name": "customer",
    "in": "query",
    "required": false
   },
   {
    "name": "ticket",
    "in": "query",
    "required": false
   },
   {
    "name": "booking",
    "in": "query",
    "required": false
   },
   {
    "name": "event",
    "in": "query",
    "required": false
   },
   {
    "name": "waiver",
    "in": "query",
    "required": false
   },
   {
    "name": "version",
    "in": "query",
    "required": false
   },
   {
    "name": "signatory",
    "in": "query",
    "required": false
   }
  ],
  "requestBody": null,
  "responds": "ComplianceEvidenceAuditWaiverRepositoryView"
 },
 "listDigitalSigningCollection": {
  "method": "GET",
  "path": "/digital-signing-collection",
  "contract": "marketing-crm",
  "summary": "Digital Signing & Collection Operations",
  "permission": "MARKETING_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "DigitalSigningCollectionOperationsView"
 },
 "listMinorGuardianGroup": {
  "method": "GET",
  "path": "/minor-guardian-group",
  "contract": "marketing-crm",
  "summary": "Minor, Guardian & Group Consent Management",
  "permission": "MARKETING_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "MinorGuardianGroupConsentManagementView"
 },
 "listMissingExpiredInvalid": {
  "method": "GET",
  "path": "/missing-expired-invalid",
  "contract": "marketing-crm",
  "summary": "Missing, Expired & Invalid Waiver Management",
  "permission": "MARKETING_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "MissingExpiredInvalidWaiverManagementView"
 },
 "listParticipantWaiverStatus": {
  "method": "GET",
  "path": "/participant-waiver-statu",
  "contract": "marketing-crm",
  "summary": "Participant Waiver Status & Tracking",
  "permission": "MARKETING_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "email",
    "in": "query",
    "required": false
   },
   {
    "name": "mobile",
    "in": "query",
    "required": false
   },
   {
    "name": "waiverId",
    "in": "query",
    "required": false
   }
  ],
  "requestBody": null,
  "responds": "ParticipantWaiverStatusTrackingView"
 },
 "listSiteWaiverException": {
  "method": "GET",
  "path": "/site-waiver-exception",
  "contract": "marketing-crm",
  "summary": "On-Site Waiver & Exception Handling",
  "permission": "MARKETING_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "OnSiteWaiverExceptionHandlingView"
 },
 "listWaiver": {
  "method": "GET",
  "path": "/waiver",
  "contract": "marketing-crm",
  "summary": "Waiver Operations Command Center",
  "permission": "MARKETING_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "brand",
    "in": "query",
    "required": false
   },
   {
    "name": "waiver",
    "in": "query",
    "required": false
   },
   {
    "name": "date",
    "in": "query",
    "required": false
   },
   {
    "name": "status",
    "in": "query",
    "required": false
   },
   {
    "name": "participantType",
    "in": "query",
    "required": false
   },
   {
    "name": "bookingChannel",
    "in": "query",
    "required": false
   }
  ],
  "requestBody": null,
  "responds": "WaiverOperationsCommandCenterView"
 },
 "listWaiverComplianceOperational": {
  "method": "GET",
  "path": "/waiver-compliance-operational",
  "contract": "marketing-crm",
  "summary": "Waiver Analytics, Compliance & Operational Insights",
  "permission": "MARKETING_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "waiver",
    "in": "query",
    "required": false
   },
   {
    "name": "version",
    "in": "query",
    "required": false
   },
   {
    "name": "product",
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
    "name": "customerType",
    "in": "query",
    "required": false
   },
   {
    "name": "participantType",
    "in": "query",
    "required": false
   },
   {
    "name": "channel",
    "in": "query",
    "required": false
   }
  ],
  "requestBody": null,
  "responds": "WaiverAnalyticsComplianceOperationalInsightsView"
 },
 "listWaiverComplianceRisk": {
  "method": "GET",
  "path": "/waiver-compliance-risk",
  "contract": "marketing-crm",
  "summary": "AI Waiver Compliance & Risk Intelligence Center",
  "permission": "MARKETING_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "AiWaiverComplianceRiskIntelligenceCenterView"
 },
 "setWaiverVerificationValidation": {
  "method": "PUT",
  "path": "/waiver-verification-validation",
  "contract": "marketing-crm",
  "summary": "Waiver Verification & Validation Workspace",
  "permission": "MARKETING_MANAGE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": "WaiverVerificationValidationWorkspaceInput",
  "responds": "WaiverVerificationValidationWorkspaceView"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "AiWaiverComplianceRiskIntelligenceCenterView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over marketing-crm state, assembled at read time from tables that already exist",
  "description": "**What AI Waiver Compliance & Risk Intelligence Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "templates": {
    "type": "string",
    "description": "Templates"
   },
   "versions": {
    "type": "string",
    "description": "Versions"
   },
   "questions": {
    "type": "string",
    "description": "Questions"
   },
   "signatoryRules": {
    "type": "string",
    "description": "Signatory Rules"
   },
   "productAssociations": {
    "type": "string",
    "description": "Product Associations"
   },
   "participants": {
    "type": "string",
    "description": "Participants"
   },
   "completion": {
    "type": "string",
    "description": "Completion"
   },
   "verification": {
    "type": "string",
    "description": "Verification"
   },
   "exceptions": {
    "type": "string",
    "description": "Exceptions"
   },
   "accessBlocks": {
    "type": "string",
    "description": "Access Blocks"
   },
   "customerInteractions": {
    "type": "string",
    "description": "Customer Interactions"
   },
   "operationalTrends": {
    "type": "string",
    "description": "Operational Trends"
   },
   "missing": {
    "type": "string",
    "description": "missing"
   },
   "nextWeek": {
    "type": "string",
    "format": "date-time",
    "description": "next week"
   },
   "aWaiverIssue": {
    "type": "string",
    "description": "a waiver issue.”"
   },
   "requirements": {
    "type": "string",
    "description": "requirements"
   },
   "relationships": {
    "type": "string",
    "description": "relationships"
   },
   "area11CompleteStructure": {
    "type": "string",
    "description": "Area 11 — Complete Structure"
   }
  }
 },
 "ComplianceEvidenceAuditWaiverRepositoryView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over marketing-crm state, assembled at read time from tables that already exist",
  "description": "**What Compliance Evidence, Audit & Waiver Repository displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "waiverId": {
    "type": "string",
    "description": "Waiver ID"
   },
   "exactVersion": {
    "type": "string",
    "description": "Exact Version"
   },
   "signatoryType": {
    "type": "string",
    "description": "Signatory Type"
   },
   "submissionDate": {
    "type": "string",
    "format": "date-time",
    "description": "Submission Date"
   },
   "submissionTime": {
    "type": "string",
    "format": "date-time",
    "description": "Submission Time"
   },
   "responses": {
    "type": "string",
    "description": "Responses"
   },
   "acknowledgements": {
    "type": "string",
    "description": "Acknowledgements"
   },
   "signatureEvidence": {
    "type": "string",
    "description": "Signature Evidence"
   },
   "verification": {
    "type": "string",
    "description": "Verification"
   },
   "relatedBooking": {
    "type": "string",
    "description": "Related Booking"
   },
   "relatedTicket": {
    "type": "string",
    "description": "Related Ticket"
   },
   "applicableProduct": {
    "type": "string",
    "description": "Applicable Product"
   },
   "applicableEvent": {
    "type": "string",
    "description": "Applicable Event"
   },
   "auditEvents": {
    "type": "string",
    "description": "Audit Events"
   },
   "legalWording": {
    "type": "string",
    "description": "Legal wording"
   },
   "questions": {
    "type": "string",
    "description": "Questions"
   },
   "waiverVersion": {
    "type": "string",
    "description": "Waiver version"
   },
   "signatoryEvidence": {
    "type": "string",
    "description": "Signatory evidence"
   },
   "role": {
    "type": "string",
    "description": "Role"
   },
   "businessUnit": {
    "type": "string",
    "description": "Business Unit"
   },
   "legalEntity": {
    "type": "string",
    "description": "Legal Entity"
   },
   "dataSensitivity": {
    "type": "string",
    "description": "Data sensitivity"
   },
   "requirements": {
    "type": "string",
    "description": "requirements"
   }
  }
 },
 "DigitalSigningCollectionOperationsView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over marketing-crm state, assembled at read time from tables that already exist",
  "description": "**What Digital Signing & Collection Operations displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "emailLink": {
    "type": "string",
    "description": "Email Link"
   },
   "smsLink": {
    "type": "string",
    "description": "SMS Link"
   },
   "whatsappWhereIntegrated": {
    "type": "string",
    "description": "WhatsApp where integrated"
   },
   "b2cAccount": {
    "type": "string",
    "description": "B2C Account"
   },
   "mobileApp": {
    "type": "string",
    "description": "Mobile App"
   },
   "groupPortal": {
    "type": "string",
    "description": "Group Portal"
   },
   "qrCode": {
    "type": "string",
    "description": "QR Code"
   },
   "pos": {
    "type": "string",
    "description": "POS"
   },
   "kiosk": {
    "type": "string",
    "description": "Kiosk"
   },
   "staffAssistedDevice": {
    "type": "string",
    "description": "Staff-Assisted Device"
   },
   "sent": {
    "type": "string",
    "description": "Sent"
   },
   "delivered": {
    "type": "string",
    "description": "Delivered"
   },
   "opened": {
    "type": "string",
    "description": "Opened"
   },
   "started": {
    "type": "string",
    "description": "Started"
   },
   "completed": {
    "type": "string",
    "description": "Completed"
   },
   "failed": {
    "type": "integer",
    "description": "Failed"
   },
   "expiredLinks": {
    "type": "integer",
    "description": "Expired Links"
   },
   "singleMultiUse": {
    "type": "string",
    "description": "Single/Multi Use"
   },
   "authentication": {
    "type": "string",
    "description": "Authentication"
   },
   "participant": {
    "type": "string",
    "description": "Participant"
   },
   "booking": {
    "type": "string",
    "description": "Booking"
   },
   "waiverVersion": {
    "type": "string",
    "description": "Waiver Version"
   },
   "activityWaiverV32": {
    "type": "string",
    "description": "Activity Waiver v3.2"
   },
   "participantOmarAhmed": {
    "type": "string",
    "description": "Participant: Omar Ahmed"
   }
  }
 },
 "MinorGuardianGroupConsentManagementView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over marketing-crm state, assembled at read time from tables that already exist",
  "description": "**What Minor, Guardian & Group Consent Management displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "minor": {
    "type": "string",
    "description": "Minor"
   },
   "guardian": {
    "type": "string",
    "description": "Guardian"
   },
   "relationship": {
    "type": "string",
    "description": "Relationship"
   },
   "contact": {
    "type": "string",
    "description": "Contact"
   },
   "verificationStatus": {
    "type": "string",
    "description": "Verification Status"
   },
   "consentStatus": {
    "type": "string",
    "description": "Consent Status"
   },
   "signatureStatus": {
    "type": "string",
    "description": "Signature Status"
   },
   "oneGuardianOneMinor": {
    "type": "string",
    "description": "One Guardian → One Minor"
   },
   "oneGuardianMultipleMinors": {
    "type": "string",
    "description": "One Guardian → Multiple Minors"
   },
   "organization": {
    "type": "string",
    "description": "Organization"
   },
   "groupLeader": {
    "type": "string",
    "description": "Group Leader"
   },
   "groupBooking": {
    "type": "string",
    "description": "Group Booking"
   },
   "responsibility": {
    "type": "string",
    "description": "Responsibility"
   },
   "permittedActions": {
    "type": "integer",
    "description": "Permitted Actions"
   }
  }
 },
 "MissingExpiredInvalidWaiverManagementView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over marketing-crm state, assembled at read time from tables that already exist",
  "description": "**What Missing, Expired & Invalid Waiver Management displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "missingWaiver": {
    "type": "string",
    "description": "Missing Waiver"
   },
   "incomplete": {
    "type": "string",
    "description": "Incomplete"
   },
   "missingSignature": {
    "type": "string",
    "description": "Missing Signature"
   },
   "guardianMissing": {
    "type": "string",
    "description": "Guardian Missing"
   },
   "expired": {
    "type": "integer",
    "description": "Expired"
   },
   "wrongVersion": {
    "type": "string",
    "description": "Wrong Version"
   },
   "rejected": {
    "type": "integer",
    "description": "Rejected"
   },
   "verificationFailed": {
    "type": "integer",
    "description": "Verification Failed"
   },
   "participantMismatch": {
    "type": "string",
    "description": "Participant Mismatch"
   },
   "requiredCorrection": {
    "type": "string",
    "description": "Required Correction"
   },
   "participant": {
    "type": "string",
    "description": "Participant"
   },
   "booking": {
    "type": "string",
    "description": "Booking"
   },
   "event": {
    "type": "string",
    "description": "Event"
   },
   "visitTime": {
    "type": "string",
    "format": "date-time",
    "description": "Visit Time"
   },
   "waiver": {
    "type": "string",
    "description": "Waiver"
   },
   "problem": {
    "type": "string",
    "description": "Problem"
   },
   "timeRemaining": {
    "type": "string",
    "format": "date-time",
    "description": "Time Remaining"
   },
   "accessImpact": {
    "type": "string",
    "description": "Access Impact"
   },
   "owner": {
    "type": "string",
    "description": "Owner"
   },
   "status": {
    "type": "integer",
    "description": "Status"
   },
   "eventProximity": {
    "type": "string",
    "description": "Event proximity"
   },
   "mandatoryWaiver": {
    "type": "string",
    "description": "Mandatory waiver"
   },
   "accessBlocking": {
    "type": "string",
    "description": "Access blocking"
   },
   "minorGuardianIssue": {
    "type": "string",
    "description": "Minor/guardian issue"
   },
   "groupSize": {
    "type": "string",
    "description": "Group size"
   },
   "operationalImpact": {
    "type": "string",
    "description": "Operational impact"
   },
   "requestReSign": {
    "type": "string",
    "description": "Request Re-Sign"
   },
   "contactCustomer": {
    "type": "string",
    "description": "Contact Customer"
   },
   "contactGuardian": {
    "type": "string",
    "description": "Contact Guardian"
   },
   "requestVerification": {
    "type": "string",
    "description": "Request Verification"
   },
   "startExceptionWorkflow": {
    "type": "string",
    "description": "Start Exception Workflow"
   }
  }
 },
 "OnSiteWaiverExceptionHandlingView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over marketing-crm state, assembled at read time from tables that already exist",
  "description": "**What On-Site Waiver & Exception Handling displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "ticket": {
    "type": "string",
    "description": "Ticket"
   },
   "qr": {
    "type": "string",
    "description": "QR"
   },
   "booking": {
    "type": "string",
    "description": "Booking"
   },
   "customer": {
    "type": "string",
    "description": "Customer"
   },
   "participant": {
    "type": "string",
    "description": "Participant"
   },
   "group": {
    "type": "string",
    "description": "Group"
   },
   "membership": {
    "type": "string",
    "description": "Membership"
   },
   "displayQrForCustomer": {
    "type": "string",
    "description": "Display QR for Customer"
   },
   "completeOnKiosk": {
    "type": "string",
    "description": "Complete on Kiosk"
   },
   "completeOnStaffTablet": {
    "type": "string",
    "description": "Complete on Staff Tablet"
   },
   "contactGuardian": {
    "type": "string",
    "description": "Contact Guardian"
   },
   "reSignUpdatedWaiver": {
    "type": "string",
    "format": "date-time",
    "description": "Re-Sign Updated Waiver"
   },
   "requestSupervisorException": {
    "type": "string",
    "description": "Request Supervisor Exception"
   },
   "oneTime": {
    "type": "string",
    "format": "date-time",
    "description": "One-Time"
   },
   "ticketSpecific": {
    "type": "string",
    "description": "Ticket-Specific"
   },
   "activitySpecific": {
    "type": "string",
    "description": "Activity-Specific"
   },
   "timeLimited": {
    "type": "string",
    "format": "date-time",
    "description": "Time-Limited"
   },
   "signatureEvidenceExists": {
    "type": "string",
    "description": "signature/evidence exists"
   },
   "waiverStatusVerified": {
    "type": "string",
    "description": "Waiver Status → Verified"
   },
   "accessControlReceivesUpdatedEligibility": {
    "type": "string",
    "format": "date-time",
    "description": "Access Control receives updated eligibility"
   }
  }
 },
 "ParticipantWaiverStatusTrackingView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over marketing-crm state, assembled at read time from tables that already exist",
  "description": "**What Participant Waiver Status & Tracking displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "participant": {
    "type": "string",
    "description": "Participant"
   },
   "participantId": {
    "type": "string",
    "description": "Participant ID"
   },
   "customerPurchaser": {
    "type": "string",
    "description": "Customer/Purchaser"
   },
   "booking": {
    "type": "string",
    "description": "Booking"
   },
   "ticket": {
    "type": "string",
    "description": "Ticket"
   },
   "product": {
    "type": "string",
    "description": "Product"
   },
   "event": {
    "type": "string",
    "description": "Event"
   },
   "visitDate": {
    "type": "string",
    "format": "date-time",
    "description": "Visit Date"
   },
   "ageCategory": {
    "type": "string",
    "description": "Age Category"
   },
   "group": {
    "type": "string",
    "description": "Group"
   },
   "waiverRequirements": {
    "type": "integer",
    "description": "Waiver Requirements"
   },
   "completionStatus": {
    "type": "integer",
    "description": "Completion Status"
   },
   "requestCorrection": {
    "type": "string",
    "description": "Request Correction"
   },
   "recordException": {
    "type": "string",
    "description": "Record Exception"
   }
  }
 },
 "WaiverAnalyticsComplianceOperationalInsightsView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over marketing-crm state, assembled at read time from tables that already exist",
  "description": "**What Waiver Analytics, Compliance & Operational Insights displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "waiversAssigned": {
    "type": "string",
    "description": "Waivers Assigned"
   },
   "completionRate": {
    "type": "number",
    "description": "Completion Rate"
   },
   "preArrivalCompletion": {
    "type": "string",
    "description": "Pre-Arrival Completion"
   },
   "onSiteCompletion": {
    "type": "string",
    "description": "On-Site Completion"
   },
   "averageCompletionTime": {
    "type": "string",
    "format": "date-time",
    "description": "Average Completion Time"
   },
   "guardianCompletionRate": {
    "type": "number",
    "description": "Guardian Completion Rate"
   },
   "rejectionRate": {
    "type": "number",
    "description": "Rejection Rate"
   },
   "exceptionRate": {
    "type": "number",
    "description": "Exception Rate"
   },
   "accessBlocks": {
    "type": "string",
    "description": "Access Blocks"
   },
   "reminderEffectiveness": {
    "type": "string",
    "description": "Reminder Effectiveness"
   },
   "checkInDelays": {
    "type": "string",
    "description": "Check-in delays"
   },
   "staffInterventions": {
    "type": "string",
    "description": "Staff interventions"
   },
   "onSiteCompletions": {
    "type": "string",
    "description": "On-site completions"
   },
   "exceptions": {
    "type": "string",
    "description": "Exceptions"
   }
  }
 },
 "WaiverOperationsCommandCenterView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over marketing-crm state, assembled at read time from tables that already exist",
  "description": "**What Waiver Operations Command Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "waiversRequired": {
    "type": "boolean",
    "description": "Waivers Required"
   },
   "completed": {
    "type": "string",
    "description": "Completed"
   },
   "pending": {
    "type": "integer",
    "description": "Pending"
   },
   "partiallyCompleted": {
    "type": "string",
    "description": "Partially Completed"
   },
   "expiring": {
    "type": "string",
    "description": "Expiring"
   },
   "invalid": {
    "type": "string",
    "description": "Invalid"
   },
   "rejected": {
    "type": "integer",
    "description": "Rejected"
   },
   "guardianConsentPending": {
    "type": "integer",
    "description": "Guardian Consent Pending"
   },
   "upcomingParticipantsMissingWaiver": {
    "type": "string",
    "description": "Upcoming Participants Missing Waiver"
   },
   "accessBlocked": {
    "type": "string",
    "description": "Access Blocked"
   },
   "manualExceptions": {
    "type": "integer",
    "description": "Manual Exceptions"
   },
   "completionRate": {
    "type": "number",
    "description": "Completion Rate"
   },
   "today": {
    "type": "string",
    "description": "Today"
   },
   "tomorrow": {
    "type": "string",
    "description": "Tomorrow"
   },
   "thisWeek": {
    "type": "string",
    "description": "This Week"
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
   "activity": {
    "type": "string",
    "description": "Activity"
   },
   "group": {
    "type": "string",
    "description": "Group"
   },
   "booking": {
    "type": "string",
    "description": "Booking"
   },
   "waiverType": {
    "type": "string",
    "description": "Waiver Type"
   },
   "eventActivity": {
    "type": "string",
    "description": "Event/Activity"
   },
   "dateTime": {
    "type": "string",
    "format": "date-time",
    "description": "Date/Time"
   },
   "participants": {
    "type": "integer",
    "description": "Participants"
   },
   "missing": {
    "type": "string",
    "description": "Missing"
   },
   "completion": {
    "type": "number",
    "description": "Completion %"
   },
   "guardianPending": {
    "type": "integer",
    "description": "Guardian Pending"
   },
   "exceptions": {
    "type": "integer",
    "description": "Exceptions"
   },
   "operationalRisk": {
    "type": "string",
    "description": "Operational Risk"
   },
   "sEG": {
    "type": "string",
    "description": "s e g"
   },
   "youthAttentio": {
    "type": "string",
    "description": "Youth Attentio (the pack shows 180 174 6)"
   }
  }
 },
 "WaiverVerificationValidationWorkspaceInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures",
  "description": "**What Waiver Verification & Validation Workspace submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "requiredFieldsComplete": {
    "type": "string",
    "description": "Required Fields Complete"
   },
   "requiredQuestionsAnswered": {
    "type": "string",
    "description": "Required Questions Answered"
   },
   "requiredAcknowledgementsAccepted": {
    "type": "string",
    "description": "Required Acknowledgements Accepted"
   },
   "signaturePresent": {
    "type": "string",
    "description": "Signature Present"
   },
   "guardianRelationshipPresent": {
    "type": "string",
    "description": "Guardian Relationship Present"
   },
   "correctWaiverVersion": {
    "type": "string",
    "description": "Correct Waiver Version"
   },
   "participantMatch": {
    "type": "string",
    "description": "Participant Match"
   },
   "bookingMatch": {
    "type": "string",
    "description": "Booking Match"
   },
   "effectiveDateValid": {
    "type": "string",
    "format": "date-time",
    "description": "Effective Date Valid"
   },
   "requiredEvidencePresent": {
    "type": "string",
    "description": "Required Evidence Present"
   },
   "requestCorrection": {
    "type": "string",
    "description": "Request Correction"
   }
  }
 },
 "WaiverVerificationValidationWorkspaceView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over marketing-crm state, assembled at read time from tables that already exist",
  "description": "**What Waiver Verification & Validation Workspace displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "submissionId": {
    "type": "string",
    "description": "Submission ID"
   },
   "participant": {
    "type": "string",
    "description": "Participant"
   },
   "waiver": {
    "type": "string",
    "description": "Waiver"
   },
   "version": {
    "type": "string",
    "description": "Version"
   },
   "booking": {
    "type": "string",
    "description": "Booking"
   },
   "signatory": {
    "type": "string",
    "description": "Signatory"
   },
   "submitted": {
    "type": "string",
    "description": "Submitted"
   },
   "verificationReason": {
    "type": "string",
    "description": "Verification Reason"
   },
   "risk": {
    "type": "string",
    "description": "Risk"
   },
   "status": {
    "type": "integer",
    "description": "Status"
   },
   "requiredFieldsComplete": {
    "type": "string",
    "description": "Required Fields Complete"
   },
   "requiredQuestionsAnswered": {
    "type": "string",
    "description": "Required Questions Answered"
   },
   "requiredAcknowledgementsAccepted": {
    "type": "string",
    "description": "Required Acknowledgements Accepted"
   },
   "signaturePresent": {
    "type": "string",
    "description": "Signature Present"
   },
   "guardianRelationshipPresent": {
    "type": "string",
    "description": "Guardian Relationship Present"
   },
   "correctWaiverVersion": {
    "type": "string",
    "description": "Correct Waiver Version"
   },
   "participantMatch": {
    "type": "string",
    "description": "Participant Match"
   },
   "bookingMatch": {
    "type": "string",
    "description": "Booking Match"
   },
   "effectiveDateValid": {
    "type": "string",
    "format": "date-time",
    "description": "Effective Date Valid"
   },
   "requiredEvidencePresent": {
    "type": "string",
    "description": "Required Evidence Present"
   },
   "requestCorrection": {
    "type": "string",
    "description": "Request Correction"
   }
  }
 }
}
```
