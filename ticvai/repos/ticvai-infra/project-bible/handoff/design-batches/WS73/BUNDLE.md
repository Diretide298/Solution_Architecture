# WS73 — Waiver, Consent & Digital Form Management board 2

**10 screens · 10 operations · 7 schemas · 3 permissions**

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

- **Every control that can be refused must be gated.** 3 permissions apply here:
  `GUEST_MANAGE, GUEST_VIEW, GUEST_VIEW_PII`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
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
     "provenance": "derived — CMS-001 declares entryState.params  and CMS-051 holds none of them, so the edge carries nothing and CMS-001 opens cold"
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
  "purposeNote": "Operations can identify every upcoming activity affected by incomplete waiver requirements and prioritize corrective actions before customer arrival.",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen both a metric directory (§Display) and a per-row directory (§Each record should show) — counts over a population, then the population",
  "purpose": "Provide Operations, Customer Service, Compliance and venue teams with a real-time overview of waiver completion across upcoming and active activities.",
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
        "WaiverOperationsCommandCenterView.upcomingActivities[].eventActivity",
        "WaiverOperationsCommandCenterView.upcomingActivities[].venue",
        "WaiverOperationsCommandCenterView.upcomingActivities[].dateTime",
        "WaiverOperationsCommandCenterView.upcomingActivities[].participants",
        "WaiverOperationsCommandCenterView.upcomingActivities[].waiversRequired",
        "WaiverOperationsCommandCenterView.upcomingActivities[].completed",
        "WaiverOperationsCommandCenterView.upcomingActivities[].missing",
        "WaiverOperationsCommandCenterView.upcomingActivities[].completion",
        "WaiverOperationsCommandCenterView.upcomingActivities[].guardianPending",
        "WaiverOperationsCommandCenterView.upcomingActivities[].exceptions",
        "WaiverOperationsCommandCenterView.upcomingActivities[].operationalRisk"
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
        "WaiverOperationsCommandCenterView.upcomingActivities[].eventActivity",
        "WaiverOperationsCommandCenterView.upcomingActivities[].venue",
        "WaiverOperationsCommandCenterView.upcomingActivities[].dateTime",
        "WaiverOperationsCommandCenterView.upcomingActivities[].participants",
        "WaiverOperationsCommandCenterView.upcomingActivities[].waiversRequired",
        "WaiverOperationsCommandCenterView.upcomingActivities[].completed",
        "WaiverOperationsCommandCenterView.upcomingActivities[].missing",
        "WaiverOperationsCommandCenterView.upcomingActivities[].completion",
        "WaiverOperationsCommandCenterView.upcomingActivities[].guardianPending",
        "WaiverOperationsCommandCenterView.upcomingActivities[].exceptions",
        "WaiverOperationsCommandCenterView.upcomingActivities[].operationalRisk"
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
   "board": "wireframes/P13 Venue CMS.dc.html#cms-051",
   "workshopBoard": "wireframes/WS185 Waiver, Consent & Digital Form Management Board 2.dc.html#cms-051"
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
  "purposeNote": "Staff can determine the complete waiver readiness of any participant from one screen.",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Provide a detailed operational record of the waiver requirements for each participant.",
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
   "board": "wireframes/P13 Venue CMS.dc.html#cms-052",
   "workshopBoard": "wireframes/WS185 Waiver, Consent & Digital Form Management Board 2.dc.html#cms-052"
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
  "purposeNote": "channels.",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Manage the actual distribution and completion of digital waivers.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 5 actions on this screen and the screen declares 1 operation.** Unserved: Email Link, SMS Link, WhatsApp where integrated, POS, Staff-Assisted Device. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
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
      },
      {
       "kind": "secondaryButton",
       "label": "WhatsApp where integrated",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 29 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "POS",
       "provenance": "pack Waiver, Consent & Digital Form Management_Reference.pdf, page 29 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Staff-Assisted Device",
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
   "board": "wireframes/P13 Venue CMS.dc.html#cms-053",
   "workshopBoard": "wireframes/WS185 Waiver, Consent & Digital Form Management Board 2.dc.html#cms-053"
  },
  "apisNote": "Regenerated 9 September 2026 from Waiver, Consent & Digital Form Management_Reference.pdf page 29. 7 of 7 labels bound to a contract property; 18 of 41 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "purposeNote": "purchaser, participant and legal signatory as the same person.",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Manage complex consent relationships for minors and organized groups. This screen is particularly important for camps, academies, schools, family attractions and youth activities.",
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
        "MinorGuardianGroupConsentManagementView.group.organization",
        "MinorGuardianGroupConsentManagementView.group.groupLeader",
        "MinorGuardianGroupConsentManagementView.group.contact",
        "MinorGuardianGroupConsentManagementView.group.groupBooking",
        "MinorGuardianGroupConsentManagementView.group.responsibility",
        "MinorGuardianGroupConsentManagementView.group.permittedActions"
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
        "MinorGuardianGroupConsentManagementView.group.organization",
        "MinorGuardianGroupConsentManagementView.group.groupLeader",
        "MinorGuardianGroupConsentManagementView.group.contact",
        "MinorGuardianGroupConsentManagementView.group.groupBooking",
        "MinorGuardianGroupConsentManagementView.group.responsibility",
        "MinorGuardianGroupConsentManagementView.group.permittedActions"
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
    "MinorGuardianGroupConsentManagementView.guardians[].contact"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P13 Venue CMS.dc.html#cms-054",
   "workshopBoard": "wireframes/WS185 Waiver, Consent & Digital Form Management Board 2.dc.html#cms-054"
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
  "purposeNote": "Waivers requiring manual verification are reviewed consistently using governed validation criteria with complete reviewer accountability.",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Provide authorized staff with a controlled process for reviewing waiver submissions that require verification.",
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
    "trigger": "onAction"
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
   "board": "wireframes/P13 Venue CMS.dc.html#cms-055",
   "workshopBoard": "wireframes/WS185 Waiver, Consent & Digital Form Management Board 2.dc.html#cms-055"
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
  "purposeNote": "Missing, invalid and expired waiver requirements are proactively identified and managed before they cause unnecessary admission or operational failures.",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Provide a dedicated exception workspace for waiver requirements preventing operational readiness.",
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
        "MissingExpiredInvalidWaiverManagementView.timeRemainingSeconds",
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
        "MissingExpiredInvalidWaiverManagementView.timeRemainingSeconds",
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
   "board": "wireframes/P13 Venue CMS.dc.html#cms-056",
   "workshopBoard": "wireframes/WS185 Waiver, Consent & Digital Form Management Board 2.dc.html#cms-056"
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
  "purposeNote": "On-site staff can efficiently resolve legitimate waiver issues while preventing unauthorized bypass of mandatory consent requirements.",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Depending on configuration) and no display directory — it is settings, not a population",
  "purpose": "Support customers who arrive at the venue without completing required waivers.",
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
   "board": "wireframes/P13 Venue CMS.dc.html#cms-057",
   "workshopBoard": "wireframes/WS185 Waiver, Consent & Digital Form Management Board 2.dc.html#cms-057"
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
  "purposeNote": "completed waiver at the relevant point in time.",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Maintain the complete evidentiary record of every waiver and consent transaction.",
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
   "board": "wireframes/P13 Venue CMS.dc.html#cms-058",
   "workshopBoard": "wireframes/WS185 Waiver, Consent & Digital Form Management Board 2.dc.html#cms-058"
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
  "purposeNote": "Management can understand waiver compliance and identify configuration or process improvements that reduce customer friction and on-site workload.",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Analyze) and no metric row",
  "purpose": "Analyze waiver completion, customer behavior and operational effectiveness.",
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
        "WaiverAnalyticsComplianceOperationalInsightsView.averageCompletionSeconds",
        "WaiverAnalyticsComplianceOperationalInsightsView.guardianCompletionRate",
        "WaiverAnalyticsComplianceOperationalInsightsView.rejectionRate",
        "WaiverAnalyticsComplianceOperationalInsightsView.exceptionRate",
        "WaiverAnalyticsComplianceOperationalInsightsView.accessBlocks",
        "WaiverAnalyticsComplianceOperationalInsightsView.reminderEffectiveness",
        "WaiverAnalyticsComplianceOperationalInsightsView.checkInDelays",
        "WaiverAnalyticsComplianceOperationalInsightsView.staffInterventions",
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
        "WaiverAnalyticsComplianceOperationalInsightsView.averageCompletionSeconds",
        "WaiverAnalyticsComplianceOperationalInsightsView.guardianCompletionRate",
        "WaiverAnalyticsComplianceOperationalInsightsView.rejectionRate",
        "WaiverAnalyticsComplianceOperationalInsightsView.exceptionRate",
        "WaiverAnalyticsComplianceOperationalInsightsView.accessBlocks",
        "WaiverAnalyticsComplianceOperationalInsightsView.reminderEffectiveness",
        "WaiverAnalyticsComplianceOperationalInsightsView.checkInDelays",
        "WaiverAnalyticsComplianceOperationalInsightsView.staffInterventions",
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
    "WaiverAnalyticsComplianceOperationalInsightsView.guardianCompletionRate"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P13 Venue CMS.dc.html#cms-059",
   "workshopBoard": "wireframes/WS185 Waiver, Consent & Digital Form Management Board 2.dc.html#cms-059"
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
  "purposeNote": "while preserving human/legal governance over consent and exceptions. Board 2 — Final Screen Register",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Provide an AI intelligence layer across the complete waiver lifecycle. This should combine Board 1 configuration data + Board 2 operational data.",
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
   "board": "wireframes/P13 Venue CMS.dc.html#cms-060",
   "workshopBoard": "wireframes/WS185 Waiver, Consent & Digital Form Management Board 2.dc.html#cms-060"
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
  "permission": "GUEST_VIEW_PII",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "participantSubjectId",
    "in": "query",
    "required": false
   },
   {
    "name": "customerSubjectId",
    "in": "query",
    "required": false
   },
   {
    "name": "signatorySubjectId",
    "in": "query",
    "required": false
   },
   {
    "name": "ticketId",
    "in": "query",
    "required": false
   },
   {
    "name": "orderId",
    "in": "query",
    "required": false
   },
   {
    "name": "eventId",
    "in": "query",
    "required": false
   },
   {
    "name": "formId",
    "in": "query",
    "required": false
   },
   {
    "name": "formVersion",
    "in": "query",
    "required": false
   },
   {
    "name": "venueId",
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
 "listDigitalSigningCollection": {
  "method": "GET",
  "path": "/digital-signing-collection",
  "contract": "marketing-crm",
  "summary": "Digital Signing & Collection Operations",
  "permission": "GUEST_VIEW",
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
    "name": "venueId",
    "in": "query",
    "required": false
   },
   {
    "name": "formId",
    "in": "query",
    "required": false
   },
   {
    "name": "performanceId",
    "in": "query",
    "required": false
   },
   {
    "name": "groupBookingId",
    "in": "query",
    "required": false
   },
   {
    "name": "orderId",
    "in": "query",
    "required": false
   },
   {
    "name": "method",
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
   }
  ],
  "requestBody": null,
  "responds": "DigitalSigningCollectionOperationsView"
 },
 "listMinorGuardianGroup": {
  "method": "GET",
  "path": "/minor-guardian-group",
  "contract": "marketing-crm",
  "summary": "Minor, Guardian & Group Consent Management",
  "permission": "GUEST_VIEW_PII",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "groupBookingId",
    "in": "query",
    "required": false
   },
   {
    "name": "guardianSubjectId",
    "in": "query",
    "required": false
   },
   {
    "name": "orderId",
    "in": "query",
    "required": false
   },
   {
    "name": "performanceId",
    "in": "query",
    "required": false
   },
   {
    "name": "consentStatus",
    "in": "query",
    "required": false
   },
   {
    "name": "visitFrom",
    "in": "query",
    "required": false
   },
   {
    "name": "visitTo",
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
 "listMissingExpiredInvalid": {
  "method": "GET",
  "path": "/missing-expired-invalid",
  "contract": "marketing-crm",
  "summary": "Missing, Expired & Invalid Waiver Management",
  "permission": "GUEST_VIEW_PII",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "problem",
    "in": "query",
    "required": false
   },
   {
    "name": "status",
    "in": "query",
    "required": false
   },
   {
    "name": "accessImpact",
    "in": "query",
    "required": false
   },
   {
    "name": "ownerStaffId",
    "in": "query",
    "required": false
   },
   {
    "name": "performanceId",
    "in": "query",
    "required": false
   },
   {
    "name": "groupBookingId",
    "in": "query",
    "required": false
   },
   {
    "name": "venueId",
    "in": "query",
    "required": false
   },
   {
    "name": "visitFrom",
    "in": "query",
    "required": false
   },
   {
    "name": "visitTo",
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
 "listParticipantWaiverStatus": {
  "method": "GET",
  "path": "/participant-waiver-statu",
  "contract": "marketing-crm",
  "summary": "Participant Waiver Status & Tracking",
  "permission": "GUEST_VIEW_PII",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "q",
    "in": "query",
    "required": false
   },
   {
    "name": "participantSubjectId",
    "in": "query",
    "required": false
   },
   {
    "name": "orderId",
    "in": "query",
    "required": false
   },
   {
    "name": "ticketId",
    "in": "query",
    "required": false
   },
   {
    "name": "groupBookingId",
    "in": "query",
    "required": false
   },
   {
    "name": "formId",
    "in": "query",
    "required": false
   },
   {
    "name": "performanceId",
    "in": "query",
    "required": false
   },
   {
    "name": "visitFrom",
    "in": "query",
    "required": false
   },
   {
    "name": "visitTo",
    "in": "query",
    "required": false
   },
   {
    "name": "completionStatus",
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
 "listSiteWaiverException": {
  "method": "GET",
  "path": "/site-waiver-exception",
  "contract": "marketing-crm",
  "summary": "On-Site Waiver & Exception Handling",
  "permission": "GUEST_VIEW_PII",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "ticketId",
    "in": "query",
    "required": false
   },
   {
    "name": "mediaCode",
    "in": "query",
    "required": false
   },
   {
    "name": "orderId",
    "in": "query",
    "required": false
   },
   {
    "name": "customerSubjectId",
    "in": "query",
    "required": false
   },
   {
    "name": "participantSubjectId",
    "in": "query",
    "required": false
   },
   {
    "name": "groupBookingId",
    "in": "query",
    "required": false
   },
   {
    "name": "membershipId",
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
 "listWaiver": {
  "method": "GET",
  "path": "/waiver",
  "contract": "marketing-crm",
  "summary": "Waiver Operations Command Center",
  "permission": "GUEST_VIEW",
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
    "name": "brandId",
    "in": "query",
    "required": false
   },
   {
    "name": "venueId",
    "in": "query",
    "required": false
   },
   {
    "name": "eventId",
    "in": "query",
    "required": false
   },
   {
    "name": "productId",
    "in": "query",
    "required": false
   },
   {
    "name": "formId",
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
   },
   {
    "name": "breakdownBy",
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
  "permission": "GUEST_VIEW",
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
    "name": "formId",
    "in": "query",
    "required": false
   },
   {
    "name": "formVersion",
    "in": "query",
    "required": false
   },
   {
    "name": "productId",
    "in": "query",
    "required": false
   },
   {
    "name": "eventId",
    "in": "query",
    "required": false
   },
   {
    "name": "venueId",
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
   },
   {
    "name": "language",
    "in": "query",
    "required": false
   },
   {
    "name": "groupBookingId",
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
  "permission": "GUEST_VIEW",
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
    "name": "venueId",
    "in": "query",
    "required": false
   },
   {
    "name": "forecastDate",
    "in": "query",
    "required": false
   },
   {
    "name": "category",
    "in": "query",
    "required": false
   }
  ],
  "requestBody": null,
  "responds": "AiWaiverComplianceRiskIntelligenceCenterView"
 },
 "setWaiverVerificationValidation": {
  "method": "PUT",
  "path": "/waiver-verification-validation",
  "contract": "marketing-crm",
  "summary": "Record a reviewer's verification decision on a waiver submission",
  "permission": "GUEST_MANAGE",
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
  "x-ticvai-persistence": "none — projection over marketing.form_definition + marketing.form_definition_field, marketing.waiver_requirement (new), marketing.waiver_requirement_event (new), marketing.form_submission, marketing.waiver_verification (new), marketing.waiver_exception (new) and catalogue product associations; predictions computed at read time",
  "description": "Waiver risks, recommendations and the readiness forecast. Advisory only.",
  "required": [
   "risks",
   "recommendations"
  ],
  "properties": {
   "templates": {
    "type": "integer",
    "minimum": 0,
    "description": "Waiver forms analysed (published or scheduled)."
   },
   "versions": {
    "type": "integer",
    "minimum": 0,
    "description": "Form versions in effect or scheduled."
   },
   "questions": {
    "type": "integer",
    "minimum": 0,
    "description": "Questions across those versions."
   },
   "signatoryRules": {
    "type": "integer",
    "minimum": 0
   },
   "productAssociations": {
    "type": "integer",
    "minimum": 0
   },
   "risks": {
    "type": "array",
    "maxItems": 100,
    "items": {
     "type": "object",
     "required": [
      "category",
      "severity",
      "message"
     ],
     "properties": {
      "category": {
       "type": "string",
       "enum": [
        "operational",
        "configuration",
        "version",
        "customerExperience"
       ]
      },
      "severity": {
       "type": "string",
       "enum": [
        "high",
        "medium",
        "low"
       ]
      },
      "source": {
       "type": "string",
       "enum": [
        "rule",
        "ai"
       ],
       "description": "`rule` for a deterministic check, `ai` for a prediction."
      },
      "message": {
       "type": "string",
       "maxLength": 500
      },
      "subjectType": {
       "type": "string",
       "nullable": true,
       "enum": [
        "performance",
        "product",
        "form",
        "formVersion",
        "groupBooking"
       ]
      },
      "subjectId": {
       "type": "string",
       "nullable": true
      },
      "affectedParticipants": {
       "type": "integer",
       "minimum": 0,
       "nullable": true
      }
     }
    }
   },
   "recommendations": {
    "type": "array",
    "maxItems": 50,
    "items": {
     "type": "object",
     "required": [
      "message",
      "action"
     ],
     "properties": {
      "message": {
       "type": "string",
       "maxLength": 500
      },
      "action": {
       "type": "string",
       "enum": [
        "sendTargetedReminders",
        "reorderFormSections",
        "reviewMobileLayout",
        "updateVersionAssociation",
        "addReminderTrigger",
        "enableAccessBlocking",
        "other"
       ]
      },
      "operationId": {
       "type": "string",
       "nullable": true,
       "description": "The operation that would carry it out, e.g. `actOnWaiverRequirements`, `setMessageTrigger`, `setDigitalWaiverForm`."
      },
      "riskIndex": {
       "type": "integer",
       "minimum": 0,
       "nullable": true,
       "description": "Index into `risks` of the risk it answers."
      }
     }
    }
   },
   "forecast": {
    "type": "object",
    "nullable": true,
    "required": [
     "forDate",
     "readinessRate"
    ],
    "properties": {
     "forDate": {
      "type": "string",
      "format": "date"
     },
     "readinessRate": {
      "type": "number",
      "minimum": 0,
      "maximum": 1,
      "description": "Predicted share of participants ready at arrival."
     },
     "potentialUnresolved": {
      "type": "integer",
      "minimum": 0
     },
     "highRisk": {
      "type": "integer",
      "minimum": 0
     }
    }
   }
  }
 },
 "DigitalSigningCollectionOperationsView": {
  "type": "object",
  "x-ticvai-persistence": "none — projection over marketing.waiver_requirement (new), marketing.waiver_requirement_event (new), marketing.message_dispatch and marketing.form_submission",
  "description": "Waiver link distribution and completion for the filters given.",
  "required": [
   "sent",
   "delivered",
   "opened",
   "started",
   "completed",
   "failed",
   "expiredLinks",
   "byMethod",
   "journey"
  ],
  "properties": {
   "sent": {
    "type": "integer",
    "minimum": 0
   },
   "delivered": {
    "type": "integer",
    "minimum": 0
   },
   "opened": {
    "type": "integer",
    "minimum": 0
   },
   "started": {
    "type": "integer",
    "minimum": 0
   },
   "completed": {
    "type": "integer",
    "minimum": 0
   },
   "failed": {
    "type": "integer",
    "minimum": 0,
    "description": "Links whose message could not be delivered on any channel."
   },
   "expiredLinks": {
    "type": "integer",
    "minimum": 0,
    "description": "Links that expired unused, or were refused because already used."
   },
   "completionRate": {
    "type": "number",
    "minimum": 0,
    "maximum": 1,
    "description": "`completed` / `sent`."
   },
   "byMethod": {
    "type": "array",
    "description": "One entry per delivery method used in the window.",
    "items": {
     "type": "object",
     "required": [
      "method",
      "sent",
      "completed"
     ],
     "properties": {
      "method": {
       "type": "string",
       "enum": [
        "email",
        "sms",
        "whatsapp",
        "guestWeb",
        "guestApp",
        "groupPortal",
        "qrCode",
        "pos",
        "kiosk",
        "staffAssistedDevice"
       ]
      },
      "sent": {
       "type": "integer",
       "minimum": 0
      },
      "completed": {
       "type": "integer",
       "minimum": 0
      },
      "completionRate": {
       "type": "number",
       "minimum": 0,
       "maximum": 1
      }
     }
    }
   },
   "journey": {
    "type": "array",
    "description": "How many requirements reached each stage of the signing journey, in journey order.",
    "items": {
     "type": "object",
     "required": [
      "stage",
      "count"
     ],
     "properties": {
      "stage": {
       "type": "string",
       "enum": [
        "linkIssued",
        "participantIdentified",
        "waiverLoaded",
        "questionsCompleted",
        "acknowledgementsAccepted",
        "signatureCaptured",
        "submissionValidated",
        "evidenceStored"
       ]
      },
      "count": {
       "type": "integer",
       "minimum": 0
      }
     }
    }
   },
   "recentCompletions": {
    "type": "array",
    "maxItems": 50,
    "items": {
     "type": "object",
     "required": [
      "requirementId",
      "participantSubjectId",
      "formName",
      "formVersion",
      "completedAt"
     ],
     "properties": {
      "requirementId": {
       "type": "string",
       "format": "uuid"
      },
      "participantSubjectId": {
       "type": "string",
       "format": "uuid",
       "description": "The name is not returned here (GUEST_VIEW); `listParticipantWaiverStatus` resolves it under GUEST_VIEW_PII."
      },
      "booking": {
       "type": "string",
       "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
      },
      "formName": {
       "type": "string"
      },
      "formVersion": {
       "type": "integer",
       "minimum": 1
      },
      "method": {
       "type": "string",
       "nullable": true
      },
      "completedAt": {
       "type": "string",
       "format": "date-time"
      }
     }
    }
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
 "WaiverAnalyticsComplianceOperationalInsightsView": {
  "type": "object",
  "x-ticvai-persistence": "none — projection over marketing.waiver_requirement (new), marketing.waiver_requirement_event (new), marketing.form_submission, marketing.waiver_verification (new), marketing.waiver_exception (new), marketing.message_dispatch and access validation outcomes",
  "description": "Waiver analytics for the filters given; aggregate only.",
  "required": [
   "waiversAssigned",
   "completionRate",
   "funnel"
  ],
  "properties": {
   "waiversAssigned": {
    "type": "integer",
    "minimum": 0
   },
   "completionRate": {
    "type": "number",
    "minimum": 0,
    "maximum": 1
   },
   "preArrivalCompletion": {
    "type": "integer",
    "minimum": 0,
    "description": "Requirements completed before the participant arrived."
   },
   "onSiteCompletion": {
    "type": "integer",
    "minimum": 0,
    "description": "Requirements completed on site (kiosk, POS, staff-assisted device, on-site QR)."
   },
   "averageCompletionSeconds": {
    "type": "integer",
    "minimum": 0,
    "nullable": true,
    "description": "Mean time from opening the link to submitting."
   },
   "guardianCompletionRate": {
    "type": "number",
    "minimum": 0,
    "maximum": 1
   },
   "rejectionRate": {
    "type": "number",
    "minimum": 0,
    "maximum": 1
   },
   "exceptionRate": {
    "type": "number",
    "minimum": 0,
    "maximum": 1
   },
   "accessBlocks": {
    "type": "integer",
    "minimum": 0,
    "description": "Access attempts refused with `waiverRequired`."
   },
   "checkInDelays": {
    "type": "integer",
    "minimum": 0,
    "description": "Check-ins held while a waiver was completed or resolved on site."
   },
   "staffInterventions": {
    "type": "integer",
    "minimum": 0,
    "description": "Staff actions taken on requirements (sends, corrections, verifications, exceptions)."
   },
   "exceptions": {
    "type": "integer",
    "minimum": 0,
    "description": "Exceptions approved."
   },
   "reminderEffectiveness": {
    "type": "array",
    "description": "Completion after each reminder, by how long before the activity it was sent.",
    "items": {
     "type": "object",
     "required": [
      "hoursBeforeActivity",
      "sent",
      "completedAfter"
     ],
     "properties": {
      "hoursBeforeActivity": {
       "type": "integer",
       "minimum": 0
      },
      "sent": {
       "type": "integer",
       "minimum": 0
      },
      "completedAfter": {
       "type": "integer",
       "minimum": 0
      },
      "completionRate": {
       "type": "number",
       "minimum": 0,
       "maximum": 1
      }
     }
    }
   },
   "funnel": {
    "type": "array",
    "description": "In funnel order.",
    "items": {
     "type": "object",
     "required": [
      "stage",
      "count"
     ],
     "properties": {
      "stage": {
       "type": "string",
       "enum": [
        "assigned",
        "sent",
        "delivered",
        "opened",
        "started",
        "signed",
        "verified"
       ]
      },
      "count": {
       "type": "integer",
       "minimum": 0
      }
     }
    }
   },
   "abandonment": {
    "type": "array",
    "maxItems": 50,
    "description": "Where people leave the form, highest abandonment first.",
    "items": {
     "type": "object",
     "required": [
      "formId",
      "formVersion",
      "section",
      "abandonmentRate"
     ],
     "properties": {
      "formId": {
       "type": "string",
       "format": "uuid"
      },
      "formVersion": {
       "type": "integer",
       "minimum": 1
      },
      "section": {
       "type": "string",
       "description": "The section or field key where the session ended."
      },
      "deviceClass": {
       "type": "string",
       "enum": [
        "mobile",
        "desktop",
        "tablet",
        "kiosk"
       ]
      },
      "abandoned": {
       "type": "integer",
       "minimum": 0
      },
      "abandonmentRate": {
       "type": "number",
       "minimum": 0,
       "maximum": 1
      }
     }
    }
   },
   "insights": {
    "type": "array",
    "maxItems": 20,
    "description": "Advisory findings.",
    "items": {
     "type": "object",
     "required": [
      "message"
     ],
     "properties": {
      "message": {
       "type": "string",
       "maxLength": 500
      }
     }
    }
   }
  }
 },
 "WaiverOperationsCommandCenterView": {
  "type": "object",
  "x-ticvai-persistence": "none — projection over marketing.waiver_requirement (new), marketing.form_definition, marketing.form_submission, marketing.waiver_signature, marketing.waiver_verification (new), marketing.waiver_exception (new), orders.order_line, orders.group_booking and catalogue.performance",
  "description": "Waiver readiness for the filters given. Counts are of participant waiver requirements for activities in the window unless the name says otherwise.",
  "required": [
   "waiversRequired",
   "completed",
   "pending",
   "completionRate",
   "byPeriod",
   "breakdown",
   "upcomingActivities"
  ],
  "properties": {
   "waiversRequired": {
    "type": "integer",
    "minimum": 0,
    "description": "Requirements assigned, excluding `superseded`."
   },
   "completed": {
    "type": "integer",
    "minimum": 0,
    "description": "Requirements `completed` or `verified`."
   },
   "pending": {
    "type": "integer",
    "minimum": 0,
    "description": "Requirements `assigned`, `sent` or `opened`, not yet started."
   },
   "partiallyCompleted": {
    "type": "integer",
    "minimum": 0,
    "description": "Requirements `inProgress`, and participants with some but not all waivers complete."
   },
   "expiring": {
    "type": "integer",
    "minimum": 0,
    "description": "Completed requirements whose acceptance (`FormSubmission.expiresAt`) ends before the activity starts."
   },
   "invalid": {
    "type": "integer",
    "minimum": 0,
    "description": "Requirements `expired`, or completed against a superseded version."
   },
   "rejected": {
    "type": "integer",
    "minimum": 0
   },
   "guardianConsentPending": {
    "type": "integer",
    "minimum": 0,
    "description": "Minor participants whose guardian has not yet signed."
   },
   "upcomingParticipantsMissingWaiver": {
    "type": "integer",
    "minimum": 0,
    "description": "Participants with at least one mandatory requirement not complete."
   },
   "accessBlocked": {
    "type": "integer",
    "minimum": 0,
    "description": "Participants whose ticket download, activation, check-in or access is currently blocked by a waiver."
   },
   "manualExceptions": {
    "type": "integer",
    "minimum": 0,
    "description": "Approved exceptions (`setWaiverException`) in force."
   },
   "completionRate": {
    "type": "number",
    "minimum": 0,
    "maximum": 1,
    "description": "`completed` / `waiversRequired`."
   },
   "byPeriod": {
    "type": "array",
    "description": "Today, tomorrow and this week, in that order, whatever the window.",
    "items": {
     "type": "object",
     "required": [
      "period",
      "waiversRequired",
      "completed",
      "missing"
     ],
     "properties": {
      "period": {
       "type": "string",
       "enum": [
        "today",
        "tomorrow",
        "thisWeek"
       ]
      },
      "waiversRequired": {
       "type": "integer",
       "minimum": 0
      },
      "completed": {
       "type": "integer",
       "minimum": 0
      },
      "missing": {
       "type": "integer",
       "minimum": 0
      }
     }
    }
   },
   "breakdown": {
    "type": "array",
    "maxItems": 100,
    "description": "One entry per value of `breakdownBy`, lowest completion first.",
    "items": {
     "type": "object",
     "required": [
      "key",
      "label",
      "waiversRequired",
      "completed",
      "completionRate"
     ],
     "properties": {
      "key": {
       "type": "string",
       "description": "The id of the venue, event, product, performance, group booking, booking or waiver form."
      },
      "label": {
       "type": "string"
      },
      "waiversRequired": {
       "type": "integer",
       "minimum": 0
      },
      "completed": {
       "type": "integer",
       "minimum": 0
      },
      "missing": {
       "type": "integer",
       "minimum": 0
      },
      "completionRate": {
       "type": "number",
       "minimum": 0,
       "maximum": 1
      }
     }
    }
   },
   "upcomingActivities": {
    "type": "array",
    "maxItems": 100,
    "description": "Performances in the window, most at risk first, then by `dateTime`.",
    "items": {
     "type": "object",
     "required": [
      "performanceId",
      "eventActivity",
      "dateTime",
      "participants",
      "waiversRequired",
      "completed",
      "missing",
      "completion",
      "operationalRisk"
     ],
     "properties": {
      "performanceId": {
       "type": "string",
       "format": "uuid"
      },
      "eventId": {
       "type": "string",
       "format": "uuid"
      },
      "eventActivity": {
       "type": "string",
       "description": "The event or activity name."
      },
      "venueId": {
       "type": "string",
       "format": "uuid"
      },
      "venue": {
       "type": "string",
       "description": "The venue name."
      },
      "dateTime": {
       "type": "string",
       "format": "date-time",
       "description": "When the performance starts."
      },
      "participants": {
       "type": "integer",
       "minimum": 0
      },
      "waiversRequired": {
       "type": "integer",
       "minimum": 0
      },
      "completed": {
       "type": "integer",
       "minimum": 0
      },
      "missing": {
       "type": "integer",
       "minimum": 0
      },
      "completion": {
       "type": "number",
       "minimum": 0,
       "maximum": 1,
       "description": "The performance's waiver readiness (the pack's Readiness Score)."
      },
      "guardianPending": {
       "type": "integer",
       "minimum": 0
      },
      "exceptions": {
       "type": "integer",
       "minimum": 0
      },
      "admissionAtRisk": {
       "type": "boolean",
       "description": "At least one missing requirement is configured to block check-in or access."
      },
      "operationalRisk": {
       "type": "string",
       "enum": [
        "ready",
        "attention",
        "critical"
       ],
       "description": "`critical` when a missing requirement would block admission; `attention` when anything is missing; otherwise `ready`."
      }
     }
    }
   },
   "insights": {
    "type": "array",
    "maxItems": 20,
    "description": "Advisory predictions, e.g. participants unlikely to complete before arrival without another reminder. Never change a status.",
    "items": {
     "type": "object",
     "required": [
      "message"
     ],
     "properties": {
      "performanceId": {
       "type": "string",
       "format": "uuid",
       "nullable": true
      },
      "predictedIncomplete": {
       "type": "integer",
       "minimum": 0,
       "nullable": true
      },
      "message": {
       "type": "string",
       "maxLength": 500
      }
     }
    }
   }
  }
 },
 "WaiverVerificationValidationWorkspaceInput": {
  "type": "object",
  "x-ticvai-persistence": "marketing.waiver_verification",
  "description": "A reviewer's decision on one waiver submission. The automatic checks are the server's and are not sent; the reviewer records the checks only a person can make.",
  "required": [
   "submissionId",
   "result"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "submissionId": {
    "type": "string",
    "format": "uuid",
    "description": "The `FormSubmission` reviewed; the natural key."
   },
   "result": {
    "type": "string",
    "enum": [
     "verified",
     "rejected",
     "correctionRequired",
     "escalated"
    ]
   },
   "participantMatch": {
    "type": "boolean",
    "nullable": true,
    "description": "The reviewer confirmed the signed participant is the booked participant."
   },
   "bookingMatch": {
    "type": "boolean",
    "nullable": true
   },
   "guardianRelationshipPresent": {
    "type": "boolean",
    "nullable": true,
    "description": "The reviewer confirmed the signatory's guardianship under the configured policy."
   },
   "requiredEvidencePresent": {
    "type": "boolean",
    "nullable": true,
    "description": "Any supporting document the form requires was seen."
   },
   "reasonCode": {
    "type": "string",
    "nullable": true,
    "enum": [
     "signatoryNotAuthorised",
     "participantMismatch",
     "wrongVersion",
     "incompleteAnswers",
     "evidenceMissing",
     "suspectedFraud",
     "other"
    ]
   },
   "note": {
    "type": "string",
    "maxLength": 2000,
    "nullable": true,
    "description": "Required for `rejected`, `correctionRequired`, `escalated`, and for changing an earlier decision."
   },
   "escalatedTo": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The staff member the review is escalated to; required for `escalated`."
   },
   "reviewedBy": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "reviewedAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "**The partition key** (ADR-0005)."
   },
   "updatedAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   }
  }
 },
 "WaiverVerificationValidationWorkspaceView": {
  "type": "object",
  "x-ticvai-persistence": "none — projection over marketing.form_submission, marketing.waiver_signature, marketing.form_definition, marketing.waiver_verification (new) and marketing.waiver_requirement (new); names from pii.subject",
  "description": "One waiver submission in the verification queue, with its automatic checks, the reviewer's findings and any anomalies flagged.",
  "required": [
   "submissionId",
   "participant",
   "waiver",
   "version",
   "submitted",
   "status",
   "checks"
  ],
  "properties": {
   "submissionId": {
    "type": "string",
    "format": "uuid"
   },
   "requirementId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "participant": {
    "type": "object",
    "properties": {
     "subjectId": {
      "type": "string",
      "format": "uuid"
     },
     "name": {
      "type": "string"
     },
     "age": {
      "type": "integer",
      "minimum": 0,
      "nullable": true
     }
    }
   },
   "waiver": {
    "type": "object",
    "properties": {
     "formId": {
      "type": "string",
      "format": "uuid"
     },
     "name": {
      "type": "string"
     }
    }
   },
   "version": {
    "type": "integer",
    "minimum": 1,
    "description": "The form version signed."
   },
   "booking": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$",
    "nullable": true
   },
   "signatory": {
    "type": "object",
    "properties": {
     "subjectId": {
      "type": "string",
      "format": "uuid"
     },
     "name": {
      "type": "string"
     },
     "signatoryType": {
      "type": "string",
      "enum": [
       "participant",
       "guardian",
       "organisationRepresentative"
      ]
     }
    }
   },
   "submitted": {
    "type": "string",
    "format": "date-time",
    "description": "`FormSubmission.submittedAt`, the device time of signing."
   },
   "verificationReason": {
    "type": "string",
    "enum": [
     "configuredManualReview",
     "automaticCheckFailed",
     "minorSignedAsAdult",
     "guardianDiscrepancy",
     "participantMismatch",
     "evidenceRequired",
     "aiAnomaly",
     "sampleReview"
    ]
   },
   "risk": {
    "type": "string",
    "enum": [
     "low",
     "medium",
     "high"
    ]
   },
   "status": {
    "type": "string",
    "enum": [
     "automaticallyValidated",
     "pendingManualVerification",
     "verified",
     "correctionRequired",
     "rejected",
     "escalated"
    ]
   },
   "checks": {
    "type": "object",
    "description": "Each check the form's configuration applies; null when it does not apply. The first seven are evaluated by the server, the last three recorded by the reviewer.",
    "properties": {
     "requiredFieldsComplete": {
      "type": "boolean",
      "nullable": true
     },
     "requiredQuestionsAnswered": {
      "type": "boolean",
      "nullable": true
     },
     "requiredAcknowledgementsAccepted": {
      "type": "boolean",
      "nullable": true
     },
     "signaturePresent": {
      "type": "boolean",
      "nullable": true
     },
     "correctWaiverVersion": {
      "type": "boolean",
      "nullable": true
     },
     "effectiveDateValid": {
      "type": "boolean",
      "nullable": true,
      "description": "The version signed was in effect at signing and the acceptance covers the visit."
     },
     "guardianRelationshipPresent": {
      "type": "boolean",
      "nullable": true,
      "description": "Evaluated from `GuestRelationship` where recorded, otherwise the reviewer's."
     },
     "participantMatch": {
      "type": "boolean",
      "nullable": true
     },
     "bookingMatch": {
      "type": "boolean",
      "nullable": true
     },
     "requiredEvidencePresent": {
      "type": "boolean",
      "nullable": true
     }
    }
   },
   "anomalies": {
    "type": "array",
    "description": "Advisory flags for the reviewer; never a decision.",
    "items": {
     "type": "object",
     "required": [
      "code",
      "message"
     ],
     "properties": {
      "code": {
       "type": "string",
       "enum": [
        "minorSignedAsAdult",
        "guardianSurnameDiffers",
        "signatoryIsMinor",
        "signedAfterActivity",
        "duplicateSubmission",
        "other"
       ]
      },
      "message": {
       "type": "string",
       "maxLength": 500
      },
      "source": {
       "type": "string",
       "enum": [
        "rule",
        "ai"
       ]
      }
     }
    }
   },
   "reviewedBy": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "reviewedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "note": {
    "type": "string",
    "nullable": true
   }
  }
 }
}
```
