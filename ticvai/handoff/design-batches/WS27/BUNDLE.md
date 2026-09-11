# WS27 — Group Sales   Corporate Booking Management board 1

**10 screens · 10 operations · 14 schemas · 2 permissions**

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
| `BO-264` | Group Sales Command Center | commandCentre | 1 | 0 | — |
| `BO-265` | Group Enquiry & Opportunity Capture | configEditor | 1 | 0 | — |
| `BO-266` | Group Customer & Organization Profile | listDetail | 1 | 0 | — |
| `BO-267` | Group Requirements, Availability & Capacity Planner | listDetail | 1 | 0 | — |
| `BO-268` | Group Package & Experience Builder | listDetail | 1 | 0 | — |
| `BO-269` | Group Quotation Builder & Proposal Generation | configEditor | 1 | 0 | — |
| `BO-270` | Quote Revision, Negotiation & Version Management | configEditor | 1 | 0 | — |
| `BO-271` | Group Discount, Exception & Approval Workflow | listDetail | 1 | 0 | — |
| `BO-272` | Quote-to-Booking Conversion & Confirmation | listDetail | 1 | 0 | — |
| `BO-273` | Group Booking 360° & Handover Workspace | listDetail | 1 | 0 | — |

## Thin screens in this batch

**BO-266, BO-267, BO-268, BO-271, BO-272, BO-273 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "BO-264",
  "name": "Group Sales Command Center",
  "module": "Sell",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Group_Sales___Corporate_Booking_Management_Reference.pdf",
   "board": "1",
   "number": "9.1.1",
   "page": 4
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/sell/group-sales-command-center-bo-264",
   "component": "apps/venue-management-web/src/routes/sell/GroupSalesCommandCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-100"
   ],
   "exitTo": [
    "BO-100",
    "BO-265",
    "BO-266",
    "BO-267",
    "BO-268",
    "BO-269",
    "BO-270",
    "BO-271",
    "BO-272",
    "BO-273"
   ],
   "inferred": false,
   "notes": "**The board's hub.** The workshop specified this module as boards of ten and opened each with a command centre; the other nine screens are that board's detail, so they are reached from here and return here.",
   "transitions": [
    {
     "to": "BO-100",
     "trigger": "Venue Home",
     "carries": [
      "venueId"
     ],
     "provenance": "derived — BO-100 declares entryState.params venueId, so an edge into it must carry them"
    },
    {
     "to": "BO-265",
     "trigger": "Works in Group Enquiry & Opportunity Capture",
     "provenance": "flow F136 step 1→2",
     "operation": "listGroupSale"
    },
    {
     "to": "BO-266",
     "trigger": "Works in Group Customer & Organization Profile",
     "provenance": "flow F136 step 3→4",
     "operation": "listGroupSale"
    },
    {
     "to": "BO-267",
     "trigger": "Works in Group Requirements, Availability & Capacity Planner",
     "provenance": "flow F136 step 5→6",
     "operation": "listGroupSale"
    },
    {
     "to": "BO-268",
     "trigger": "Works in Group Package & Experience Builder",
     "provenance": "flow F136 step 7→8",
     "operation": "listGroupSale"
    },
    {
     "to": "BO-269",
     "trigger": "Works in Group Quotation Builder & Proposal Generation",
     "provenance": "flow F136 step 9→10",
     "operation": "listGroupSale"
    },
    {
     "to": "BO-270",
     "trigger": "Works in Quote Revision, Negotiation & Version Management",
     "provenance": "flow F136 step 11→12",
     "operation": "listGroupSale"
    },
    {
     "to": "BO-271",
     "trigger": "Works in Group Discount, Exception & Approval Workflow",
     "provenance": "flow F136 step 13→14",
     "operation": "listGroupSale"
    },
    {
     "to": "BO-272",
     "trigger": "Works in Quote-to-Booking Conversion & Confirmation",
     "provenance": "flow F136 step 15→16",
     "operation": "listGroupSale"
    },
    {
     "to": "BO-273",
     "trigger": "Works in Group Booking 360° & Handover Workspace",
     "provenance": "flow F136 step 17→18",
     "operation": "listGroupSale"
    }
   ]
  },
  "density": "compact",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen both a metric directory (§Display; Show) and a per-row directory (§Each opportunity should display) — counts over a population, then the population",
  "purpose": "Provide the Group Sales team with a centralized commercial workspace showing the entire group-sales pipeline.",
  "purposeNote": "The Group Sales team can manage its complete direct-sales pipeline and immediately identify opportunities requiring commercial action.",
  "layout": {
   "template": "dashboard",
   "regions": [
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "New Enquiries",
       "provenance": "pack Group_Sales___Corporate_Booking_Management_Reference.pdf, page 4 §Display",
       "bindsTo": "GroupSalesCommandCenterView.newEnquiries"
      },
      {
       "kind": "metricTile",
       "label": "Open Opportunities",
       "provenance": "pack Group_Sales___Corporate_Booking_Management_Reference.pdf, page 4 §Display"
      },
      {
       "kind": "metricTile",
       "label": "Quotations Outstanding",
       "provenance": "pack Group_Sales___Corporate_Booking_Management_Reference.pdf, page 4 §Display",
       "bindsTo": "GroupSalesCommandCenterView.quotationsOutstanding"
      },
      {
       "kind": "metricTile",
       "label": "Quotes Awaiting Approval",
       "provenance": "pack Group_Sales___Corporate_Booking_Management_Reference.pdf, page 4 §Display",
       "bindsTo": "GroupSalesCommandCenterView.quotesAwaitingApproval"
      },
      {
       "kind": "metricTile",
       "label": "Confirmed Groups",
       "provenance": "pack Group_Sales___Corporate_Booking_Management_Reference.pdf, page 4 §Display",
       "bindsTo": "GroupSalesCommandCenterView.confirmedGroups"
      },
      {
       "kind": "metricTile",
       "label": "Expected Guests",
       "provenance": "pack Group_Sales___Corporate_Booking_Management_Reference.pdf, page 4 §Display",
       "bindsTo": "GroupSalesCommandCenterView.expectedGuests"
      },
      {
       "kind": "metricTile",
       "label": "Pipeline Value",
       "provenance": "pack Group_Sales___Corporate_Booking_Management_Reference.pdf, page 4 §Display",
       "bindsTo": "GroupSalesCommandCenterView.pipelineValue"
      },
      {
       "kind": "metricTile",
       "label": "Confirmed Revenue",
       "provenance": "pack Group_Sales___Corporate_Booking_Management_Reference.pdf, page 4 §Display",
       "bindsTo": "GroupSalesCommandCenterView.confirmedRevenue"
      },
      {
       "kind": "metricTile",
       "label": "Conversion Rate",
       "provenance": "pack Group_Sales___Corporate_Booking_Management_Reference.pdf, page 4 §Display",
       "bindsTo": "GroupSalesCommandCenterView.conversionRate"
      },
      {
       "kind": "metricTile",
       "label": "Average Group Value",
       "provenance": "pack Group_Sales___Corporate_Booking_Management_Reference.pdf, page 4 §Display",
       "bindsTo": "GroupSalesCommandCenterView.averageGroupValue"
      },
      {
       "kind": "metricTile",
       "label": "Expiring Quotes",
       "provenance": "pack Group_Sales___Corporate_Booking_Management_Reference.pdf, page 4 §Display",
       "bindsTo": "GroupSalesCommandCenterView.expiringQuotes"
      },
      {
       "kind": "metricTile",
       "label": "Sales Target Achievement",
       "provenance": "pack Group_Sales___Corporate_Booking_Management_Reference.pdf, page 4 §Display",
       "bindsTo": "GroupSalesCommandCenterView.salesTargetAchievement"
      },
      {
       "kind": "metricTile",
       "label": "Follow-ups due",
       "provenance": "pack Group_Sales___Corporate_Booking_Management_Reference.pdf, page 4 §Show",
       "bindsTo": "GroupSalesCommandCenterView.followUpsDue"
      },
      {
       "kind": "metricTile",
       "label": "Quotes expiring",
       "provenance": "pack Group_Sales___Corporate_Booking_Management_Reference.pdf, page 4 §Show",
       "bindsTo": "GroupSalesCommandCenterView.quotesExpiring"
      },
      {
       "kind": "metricTile",
       "label": "Customer responses",
       "provenance": "pack Group_Sales___Corporate_Booking_Management_Reference.pdf, page 4 §Show",
       "bindsTo": "GroupSalesCommandCenterView.customerResponses"
      },
      {
       "kind": "metricTile",
       "label": "Approval requests",
       "provenance": "pack Group_Sales___Corporate_Booking_Management_Reference.pdf, page 4 §Show",
       "bindsTo": "GroupSalesCommandCenterView.approvalRequests"
      },
      {
       "kind": "metricTile",
       "label": "Deposits pending",
       "provenance": "pack Group_Sales___Corporate_Booking_Management_Reference.pdf, page 4 §Show",
       "bindsTo": "GroupSalesCommandCenterView.depositsPending"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "moduleTiles",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every group sales",
       "columns": [
        "GroupSalesCommandCenterView.enquiryId",
        "GroupSalesCommandCenterView.organizationCustomer",
        "GroupSalesCommandCenterView.groupType",
        "GroupSalesCommandCenterView.eventAttraction",
        "GroupSalesCommandCenterView.visitDate",
        "GroupSalesCommandCenterView.guestCount",
        "GroupSalesCommandCenterView.salesOwner",
        "GroupSalesCommandCenterView.estimatedValue",
        "GroupSalesCommandCenterView.quoteStatus",
        "GroupSalesCommandCenterView.probability",
        "GroupSalesCommandCenterView.nextAction",
        "GroupSalesCommandCenterView.expectedCloseDate"
       ],
       "bindsTo": "GroupSalesCommandCenterView",
       "operation": "listGroupSale",
       "provenance": "pack Group_Sales___Corporate_Booking_Management_Reference.pdf, page 4 §Each opportunity should display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected group sales",
       "bindsTo": "GroupSalesCommandCenterView",
       "columns": [
        "GroupSalesCommandCenterView.enquiryId",
        "GroupSalesCommandCenterView.organizationCustomer",
        "GroupSalesCommandCenterView.groupType",
        "GroupSalesCommandCenterView.eventAttraction",
        "GroupSalesCommandCenterView.visitDate",
        "GroupSalesCommandCenterView.guestCount",
        "GroupSalesCommandCenterView.salesOwner",
        "GroupSalesCommandCenterView.estimatedValue",
        "GroupSalesCommandCenterView.quoteStatus",
        "GroupSalesCommandCenterView.probability",
        "GroupSalesCommandCenterView.nextAction",
        "GroupSalesCommandCenterView.expectedCloseDate"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Visualize”, “High Priority Opportunity”.",
       "provenance": "pack Group_Sales___Corporate_Booking_Management_Reference.pdf, page 4 §Each opportunity should display"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The group sales list; the counts above it resolve separately.",
   "error": "Could not load. Names which read failed and leaves the group sales untouched.",
   "emptyFirstRun": "No group sales yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the group sales are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listGroupSale",
    "contract": "orders",
    "purpose": "Group Sales Command Center",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-264"
  },
  "apisNote": "Regenerated 9 September 2026 from Group_Sales___Corporate_Booking_Management_Reference.pdf page 4. 28 of 28 labels bound to a contract property; 29 of 38 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-265",
  "name": "Group Enquiry & Opportunity Capture",
  "module": "Sell",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Group_Sales___Corporate_Booking_Management_Reference.pdf",
   "board": "1",
   "number": "9.1.2",
   "page": 5
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/sell/group-enquiry-opportunity-capture-bo-265",
   "component": "apps/venue-management-web/src/routes/sell/GroupEnquiryOpportunityCapture.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-264"
   ],
   "exitTo": [
    "BO-264"
   ],
   "inferred": false,
   "notes": "**Reached from BO-264, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-264",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F136 step 2→3",
     "operation": "listGroupEnquiryOpportunity"
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Capture; Configure) and no display directory — it is settings, not a population",
  "purpose": "Capture a new group-sales enquiry and convert it into a structured sales opportunity.",
  "purposeNote": "Every group-sales request can be captured as a structured, owned and trackable opportunity without requiring a booking to exist yet.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 3 actions on this screen and the screen declares 1 operation.** Unserved: Sales Team, Campaign, Existing Customer. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Group_Sales___Corporate_Booking_Management_Reference.pdf, page 5 §Support"
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
       "label": "Enquiry ID",
       "provenance": "pack Group_Sales___Corporate_Booking_Management_Reference.pdf, page 5 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Customer/Organization",
       "provenance": "pack Group_Sales___Corporate_Booking_Management_Reference.pdf, page 5 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Contact",
       "provenance": "pack Group_Sales___Corporate_Booking_Management_Reference.pdf, page 5 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Group Type",
       "provenance": "pack Group_Sales___Corporate_Booking_Management_Reference.pdf, page 5 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Requested Venue",
       "provenance": "pack Group_Sales___Corporate_Booking_Management_Reference.pdf, page 5 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Requested Event/Experience",
       "provenance": "pack Group_Sales___Corporate_Booking_Management_Reference.pdf, page 5 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Preferred Date",
       "provenance": "pack Group_Sales___Corporate_Booking_Management_Reference.pdf, page 5 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Alternative Date",
       "provenance": "pack Group_Sales___Corporate_Booking_Management_Reference.pdf, page 5 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Preferred Time",
       "provenance": "pack Group_Sales___Corporate_Booking_Management_Reference.pdf, page 5 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Estimated Guests",
       "provenance": "pack Group_Sales___Corporate_Booking_Management_Reference.pdf, page 5 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Adults",
       "provenance": "pack Group_Sales___Corporate_Booking_Management_Reference.pdf, page 5 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Children",
       "provenance": "pack Group_Sales___Corporate_Booking_Management_Reference.pdf, page 5 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Students",
       "provenance": "pack Group_Sales___Corporate_Booking_Management_Reference.pdf, page 5 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Staff/Teachers",
       "provenance": "pack Group_Sales___Corporate_Booking_Management_Reference.pdf, page 5 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Special Requirements",
       "provenance": "pack Group_Sales___Corporate_Booking_Management_Reference.pdf, page 5 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Budget",
       "provenance": "pack Group_Sales___Corporate_Booking_Management_Reference.pdf, page 5 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Notes",
       "provenance": "pack Group_Sales___Corporate_Booking_Management_Reference.pdf, page 5 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Sales Owner",
       "provenance": "pack Group_Sales___Corporate_Booking_Management_Reference.pdf, page 5 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Sales Team",
       "provenance": "pack Group_Sales___Corporate_Booking_Management_Reference.pdf, page 5 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Priority",
       "provenance": "pack Group_Sales___Corporate_Booking_Management_Reference.pdf, page 5 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Expected Value",
       "provenance": "pack Group_Sales___Corporate_Booking_Management_Reference.pdf, page 5 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Probability",
       "provenance": "pack Group_Sales___Corporate_Booking_Management_Reference.pdf, page 5 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Expected Close Date",
       "provenance": "pack Group_Sales___Corporate_Booking_Management_Reference.pdf, page 5 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Lead Source",
       "provenance": "pack Group_Sales___Corporate_Booking_Management_Reference.pdf, page 5 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Campaign",
       "provenance": "pack Group_Sales___Corporate_Booking_Management_Reference.pdf, page 5 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Next Action",
       "provenance": "pack Group_Sales___Corporate_Booking_Management_Reference.pdf, page 5 §Configure"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Sales Team",
       "provenance": "pack Group_Sales___Corporate_Booking_Management_Reference.pdf, page 5 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Campaign",
       "provenance": "pack Group_Sales___Corporate_Booking_Management_Reference.pdf, page 5 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Existing Customer",
       "provenance": "pack Group_Sales___Corporate_Booking_Management_Reference.pdf, page 5 §Support"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The group enquiry opportunity configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the group enquiry opportunity untouched.",
   "emptyFirstRun": "No group enquiry opportunity configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listGroupEnquiryOpportunity",
    "contract": "orders",
    "purpose": "Group Enquiry & Opportunity Capture",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-265"
  },
  "apisNote": "Regenerated 9 September 2026 from Group_Sales___Corporate_Booking_Management_Reference.pdf page 5. 0 of 0 labels bound to a contract property; 29 of 43 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-266",
  "name": "Group Customer & Organization Profile",
  "module": "Sell",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Group_Sales___Corporate_Booking_Management_Reference.pdf",
   "board": "1",
   "number": "9.1.3",
   "page": 6
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/sell/group-customer-organization-profile-bo-266",
   "component": "apps/venue-management-web/src/routes/sell/GroupCustomerOrganizationProfile.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-264"
   ],
   "exitTo": [
    "BO-264"
   ],
   "inferred": false,
   "notes": "**Reached from BO-264, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-264",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F136 step 4→5",
     "operation": "listGroupCustomerOrganization"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Show) and no metric row",
  "purpose": "Maintain the customer or organization buying directly from TICVAI.",
  "purposeNote": "Sales teams can see the complete relationship with a group customer while maintaining one governed customer record across TICVAI.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every group customer organization",
       "columns": [
        "GroupCustomerOrganizationProfileView.previousEnquiries",
        "GroupCustomerOrganizationProfileView.previousQuotations",
        "GroupCustomerOrganizationProfileView.confirmedBookings",
        "GroupCustomerOrganizationProfileView.totalGuests",
        "GroupCustomerOrganizationProfileView.revenue",
        "GroupCustomerOrganizationProfileView.cancellationHistory",
        "GroupCustomerOrganizationProfileView.outstandingBalance",
        "GroupCustomerOrganizationProfileView.futureBookings"
       ],
       "bindsTo": "GroupCustomerOrganizationProfileView",
       "operation": "listGroupCustomerOrganization",
       "provenance": "pack Group_Sales___Corporate_Booking_Management_Reference.pdf, page 6 §Show"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected group customer organization",
       "bindsTo": "GroupCustomerOrganizationProfileView",
       "columns": [
        "GroupCustomerOrganizationProfileView.previousEnquiries",
        "GroupCustomerOrganizationProfileView.previousQuotations",
        "GroupCustomerOrganizationProfileView.confirmedBookings",
        "GroupCustomerOrganizationProfileView.totalGuests",
        "GroupCustomerOrganizationProfileView.revenue",
        "GroupCustomerOrganizationProfileView.cancellationHistory",
        "GroupCustomerOrganizationProfileView.outstandingBalance",
        "GroupCustomerOrganizationProfileView.futureBookings"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Maintain”, “CRM Integration”.",
       "provenance": "pack Group_Sales___Corporate_Booking_Management_Reference.pdf, page 6 §Show"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The group customer organization list.",
   "error": "Could not load. Names which read failed and leaves the group customer organization untouched.",
   "emptyFirstRun": "No group customer organization yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the group customer organization are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listGroupCustomerOrganization",
    "contract": "orders",
    "purpose": "Group Customer & Organization Profile",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "GroupCustomerOrganizationProfileView.previousEnquiries",
    "GroupCustomerOrganizationProfileView.previousQuotations",
    "GroupCustomerOrganizationProfileView.confirmedBookings",
    "GroupCustomerOrganizationProfileView.totalGuests",
    "GroupCustomerOrganizationProfileView.revenue",
    "GroupCustomerOrganizationProfileView.cancellationHistory"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-266"
  },
  "apisNote": "Regenerated 9 September 2026 from Group_Sales___Corporate_Booking_Management_Reference.pdf page 6. 8 of 8 labels bound to a contract property; 19 of 42 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-267",
  "name": "Group Requirements, Availability & Capacity Planner",
  "module": "Sell",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Group_Sales___Corporate_Booking_Management_Reference.pdf",
   "board": "1",
   "number": "9.1.4",
   "page": 8
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/sell/group-requirements-availability-capacity-planner-bo-267",
   "component": "apps/venue-management-web/src/routes/sell/GroupRequirementsAvailabilityCapacityPlanner.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-264"
   ],
   "exitTo": [
    "BO-264"
   ],
   "inferred": false,
   "notes": "**Reached from BO-264, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-264",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F136 step 6→7",
     "operation": "listGroupRequirementAvailability"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Determine whether TICVAI can accommodate the requested group before preparing a quotation.",
  "purposeNote": "Sales teams can validate admission, schedule and required resource availability before making a commercial commitment to the customer.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every group requirements availability",
       "columns": [
        "GroupRequirementsAvailabilityCapacityPlannerView.eventCapacity",
        "GroupRequirementsAvailabilityCapacityPlannerView.availableCapacity",
        "GroupRequirementsAvailabilityCapacityPlannerView.existingGroups",
        "GroupRequirementsAvailabilityCapacityPlannerView.publicSales",
        "GroupRequirementsAvailabilityCapacityPlannerView.operationalHolds",
        "GroupRequirementsAvailabilityCapacityPlannerView.resourceAvailability",
        "GroupRequirementsAvailabilityCapacityPlannerView.timeslotAvailability"
       ],
       "bindsTo": "GroupRequirementsAvailabilityCapacityPlannerView",
       "operation": "listGroupRequirementAvailability",
       "provenance": "pack Group_Sales___Corporate_Booking_Management_Reference.pdf, page 8 §Display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected group requirements availability",
       "bindsTo": "GroupRequirementsAvailabilityCapacityPlannerView",
       "columns": [
        "GroupRequirementsAvailabilityCapacityPlannerView.eventCapacity",
        "GroupRequirementsAvailabilityCapacityPlannerView.availableCapacity",
        "GroupRequirementsAvailabilityCapacityPlannerView.existingGroups",
        "GroupRequirementsAvailabilityCapacityPlannerView.publicSales",
        "GroupRequirementsAvailabilityCapacityPlannerView.operationalHolds",
        "GroupRequirementsAvailabilityCapacityPlannerView.resourceAvailability",
        "GroupRequirementsAvailabilityCapacityPlannerView.timeslotAvailability"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Calendar View”, “Capacity Reservation”, “Resource Dependencies”.",
       "provenance": "pack Group_Sales___Corporate_Booking_Management_Reference.pdf, page 8 §Display"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The group requirements availability list.",
   "error": "Could not load. Names which read failed and leaves the group requirements availability untouched.",
   "emptyFirstRun": "No group requirements availability yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the group requirements availability are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listGroupRequirementAvailability",
    "contract": "orders",
    "purpose": "Group Requirements, Availability & Capacity Planner",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "GroupRequirementsAvailabilityCapacityPlannerView.eventCapacity",
    "GroupRequirementsAvailabilityCapacityPlannerView.availableCapacity",
    "GroupRequirementsAvailabilityCapacityPlannerView.existingGroups",
    "GroupRequirementsAvailabilityCapacityPlannerView.publicSales",
    "GroupRequirementsAvailabilityCapacityPlannerView.operationalHolds",
    "GroupRequirementsAvailabilityCapacityPlannerView.resourceAvailability"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-267"
  },
  "apisNote": "Regenerated 9 September 2026 from Group_Sales___Corporate_Booking_Management_Reference.pdf page 8. 7 of 7 labels bound to a contract property; 22 of 43 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-268",
  "name": "Group Package & Experience Builder",
  "module": "Sell",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Group_Sales___Corporate_Booking_Management_Reference.pdf",
   "board": "1",
   "number": "9.1.5",
   "page": 9
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/sell/group-package-experience-builder-bo-268",
   "component": "apps/venue-management-web/src/routes/sell/GroupPackageExperienceBuilder.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-264"
   ],
   "exitTo": [
    "BO-264"
   ],
   "inferred": false,
   "notes": "**Reached from BO-264, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-264",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F136 step 8→9",
     "operation": "setGroupPackageExperience"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Show) and no metric row",
  "purpose": "Build a complete commercial package tailored to the group's requirements.",
  "purposeNote": "Sales teams can build a multi-product group package while consuming approved TICVAI products, pricing and resources rather than manually calculating the offer outside the platform.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every group package experience",
       "columns": [
        "GroupPackageExperienceBuilderView.standardPrice",
        "GroupPackageExperienceBuilderView.groupRate",
        "GroupPackageExperienceBuilderView.discount",
        "GroupPackageExperienceBuilderView.complimentaryQuantity",
        "GroupPackageExperienceBuilderView.addOnPrice",
        "GroupPackageExperienceBuilderView.tax",
        "GroupPackageExperienceBuilderView.fees",
        "GroupPackageExperienceBuilderView.packageTotal",
        "GroupPackageExperienceBuilderView.pricePerGuest"
       ],
       "bindsTo": "GroupPackageExperienceBuilderView",
       "operation": "setGroupPackageExperience",
       "provenance": "pack Group_Sales___Corporate_Booking_Management_Reference.pdf, page 9 §Show"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected group package experience",
       "bindsTo": "GroupPackageExperienceBuilderView",
       "columns": [
        "GroupPackageExperienceBuilderView.standardPrice",
        "GroupPackageExperienceBuilderView.groupRate",
        "GroupPackageExperienceBuilderView.discount",
        "GroupPackageExperienceBuilderView.complimentaryQuantity",
        "GroupPackageExperienceBuilderView.addOnPrice",
        "GroupPackageExperienceBuilderView.tax",
        "GroupPackageExperienceBuilderView.fees",
        "GroupPackageExperienceBuilderView.packageTotal",
        "GroupPackageExperienceBuilderView.pricePerGuest"
       ],
       "notes": "The pack groups this record's detail under its own headings: “School Discovery Package”, “Package Templates”.",
       "provenance": "pack Group_Sales___Corporate_Booking_Management_Reference.pdf, page 9 §Show"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Group Ticket",
       "provenance": "pack Group_Sales___Corporate_Booking_Management_Reference.pdf, page 9 §Allow combinations of"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The group package experience list.",
   "error": "Could not load. Names which read failed and leaves the group package experience untouched.",
   "emptyFirstRun": "No group package experience yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the group package experience are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setGroupPackageExperience",
    "contract": "orders",
    "purpose": "Group Package & Experience Builder",
    "trigger": "onAction",
    "invalidates": [
     "setGroupPackageExperience"
    ]
   }
  ],
  "entryState": {
   "preloaded": [
    "GroupPackageExperienceBuilderView.standardPrice",
    "GroupPackageExperienceBuilderView.groupRate",
    "GroupPackageExperienceBuilderView.discount",
    "GroupPackageExperienceBuilderView.complimentaryQuantity",
    "GroupPackageExperienceBuilderView.addOnPrice",
    "GroupPackageExperienceBuilderView.tax"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-268"
  },
  "apisNote": "Regenerated 9 September 2026 from Group_Sales___Corporate_Booking_Management_Reference.pdf page 9. 9 of 9 labels bound to a contract property; 10 of 44 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-269",
  "name": "Group Quotation Builder & Proposal Generation",
  "module": "Sell",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Group_Sales___Corporate_Booking_Management_Reference.pdf",
   "board": "1",
   "number": "9.1.6",
   "page": 11
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/sell/group-quotation-builder-proposal-generation-bo-269",
   "component": "apps/venue-management-web/src/routes/sell/GroupQuotationBuilderProposalGeneration.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-264"
   ],
   "exitTo": [
    "BO-264"
   ],
   "inferred": false,
   "notes": "**Reached from BO-264, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-264",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F136 step 10→11",
     "operation": "setGroupQuotationProposal"
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Capture; Where configured, customer can) and no display directory — it is settings, not a population",
  "purpose": "Turn the configured group package into a professional customer quotation.",
  "purposeNote": "Sales teams can generate a controlled, branded and auditable group quotation directly from the approved package configuration.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Quote Number",
       "provenance": "pack Group_Sales___Corporate_Booking_Management_Reference.pdf, page 11 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Opportunity",
       "provenance": "pack Group_Sales___Corporate_Booking_Management_Reference.pdf, page 11 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Customer",
       "provenance": "pack Group_Sales___Corporate_Booking_Management_Reference.pdf, page 11 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Contact",
       "provenance": "pack Group_Sales___Corporate_Booking_Management_Reference.pdf, page 11 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Quote Date",
       "provenance": "pack Group_Sales___Corporate_Booking_Management_Reference.pdf, page 11 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Valid Until",
       "provenance": "pack Group_Sales___Corporate_Booking_Management_Reference.pdf, page 11 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Visit Date",
       "provenance": "pack Group_Sales___Corporate_Booking_Management_Reference.pdf, page 11 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Guest Count",
       "provenance": "pack Group_Sales___Corporate_Booking_Management_Reference.pdf, page 11 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Currency",
       "provenance": "pack Group_Sales___Corporate_Booking_Management_Reference.pdf, page 11 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Sales Owner",
       "provenance": "pack Group_Sales___Corporate_Booking_Management_Reference.pdf, page 11 §Capture"
      },
      {
       "kind": "textField",
       "label": "Accept / Reject / Request Changes",
       "provenance": "pack Group_Sales___Corporate_Booking_Management_Reference.pdf, page 11 §Where configured, customer can"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Save changes",
       "provenance": "contract operation setGroupQuotationProposal"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The group quotation proposal configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the group quotation proposal untouched.",
   "emptyFirstRun": "No group quotation proposal configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setGroupQuotationProposal",
    "contract": "orders",
    "purpose": "Group Quotation Builder & Proposal Generation",
    "trigger": "onAction",
    "invalidates": [
     "setGroupQuotationProposal"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-269"
  },
  "apisNote": "Regenerated 9 September 2026 from Group_Sales___Corporate_Booking_Management_Reference.pdf page 11. 0 of 0 labels bound to a contract property; 11 of 36 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-270",
  "name": "Quote Revision, Negotiation & Version Management",
  "module": "Sell",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Group_Sales___Corporate_Booking_Management_Reference.pdf",
   "board": "1",
   "number": "9.1.7",
   "page": 12
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/sell/quote-revision-negotiation-version-management-bo-270",
   "component": "apps/venue-management-web/src/routes/sell/QuoteRevisionNegotiationVersionManagement.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-264"
   ],
   "exitTo": [
    "BO-264"
   ],
   "inferred": false,
   "notes": "**Reached from BO-264, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-264",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F136 step 12→13",
     "operation": "listQuoteRevisionNegotiation"
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Capture) and no display directory — it is settings, not a population",
  "purpose": "Manage the commercial negotiation process without losing historical versions.",
  "purposeNote": "Every quotation revision and negotiation decision is retained with complete commercial history and impact visibility.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Customer Request",
       "provenance": "pack Group_Sales___Corporate_Booking_Management_Reference.pdf, page 12 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Internal Response",
       "provenance": "pack Group_Sales___Corporate_Booking_Management_Reference.pdf, page 12 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Price Change",
       "provenance": "pack Group_Sales___Corporate_Booking_Management_Reference.pdf, page 12 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Quantity Change",
       "provenance": "pack Group_Sales___Corporate_Booking_Management_Reference.pdf, page 12 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Package Change",
       "provenance": "pack Group_Sales___Corporate_Booking_Management_Reference.pdf, page 12 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Terms Change",
       "provenance": "pack Group_Sales___Corporate_Booking_Management_Reference.pdf, page 12 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Date",
       "provenance": "pack Group_Sales___Corporate_Booking_Management_Reference.pdf, page 12 §Capture"
      },
      {
       "kind": "selectField",
       "label": "User",
       "provenance": "pack Group_Sales___Corporate_Booking_Management_Reference.pdf, page 12 §Capture"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The quote revision negotiation configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the quote revision negotiation untouched.",
   "emptyFirstRun": "No quote revision negotiation configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listQuoteRevisionNegotiation",
    "contract": "orders",
    "purpose": "Quote Revision, Negotiation & Version Management",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-270"
  },
  "apisNote": "Regenerated 9 September 2026 from Group_Sales___Corporate_Booking_Management_Reference.pdf page 12. 0 of 0 labels bound to a contract property; 8 of 26 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-271",
  "name": "Group Discount, Exception & Approval Workflow",
  "module": "Sell",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Group_Sales___Corporate_Booking_Management_Reference.pdf",
   "board": "1",
   "number": "9.1.8",
   "page": 13
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/sell/group-discount-exception-approval-workflow-bo-271",
   "component": "apps/venue-management-web/src/routes/sell/GroupDiscountExceptionApprovalWorkflow.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-264"
   ],
   "exitTo": [
    "BO-264"
   ],
   "inferred": false,
   "notes": "**Reached from BO-264, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-264",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F136 step 14→15",
     "operation": "approveGroupDiscountException"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Govern non-standard group pricing and commercial exceptions before a quote is committed.",
  "purposeNote": "No quotation containing a controlled commercial exception can be issued or accepted without the appropriate approval.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Group_Sales___Corporate_Booking_Management_Reference.pdf, page 13"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Group_Sales___Corporate_Booking_Management_Reference.pdf, page 13"
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
       "label": "Approve",
       "provenance": "contract operation approveGroupDiscountException"
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
       "impliedBy": "approveGroupDiscountException"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The group discount exception list.",
   "error": "Could not load. Names which read failed and leaves the group discount exception untouched.",
   "emptyFirstRun": "No group discount exception yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the group discount exception are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "approveGroupDiscountException",
    "contract": "orders",
    "purpose": "Group Discount, Exception & Approval Workflow",
    "trigger": "onAction",
    "invalidates": [
     "approveGroupDiscountException"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-271"
  },
  "apisNote": "Regenerated 9 September 2026 from Group_Sales___Corporate_Booking_Management_Reference.pdf page 13. 0 of 0 labels bound to a contract property; 0 of 38 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-272",
  "name": "Quote-to-Booking Conversion & Confirmation",
  "module": "Sell",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Group_Sales___Corporate_Booking_Management_Reference.pdf",
   "board": "1",
   "number": "9.1.9",
   "page": 15
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/sell/quote-to-booking-conversion-confirmation-bo-272",
   "component": "apps/venue-management-web/src/routes/sell/QuoteToBookingConversionConfirmation.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-264"
   ],
   "exitTo": [
    "BO-264"
   ],
   "inferred": false,
   "notes": "**Reached from BO-264, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-264",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F136 step 16→17",
     "operation": "listQuoteBookingConversion"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Convert an accepted quotation into a confirmed TICVAI group booking without re-entering the commercial configuration.",
  "purposeNote": "An approved and accepted quotation can become a confirmed group booking while preserving the exact commercial agreement and without duplicate data entry.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Group_Sales___Corporate_Booking_Management_Reference.pdf, page 15"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Group_Sales___Corporate_Booking_Management_Reference.pdf, page 15"
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
       "impliedBy": "listQuoteBookingConversion",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The quote-to-booking conversion confirmation list.",
   "error": "Could not load. Names which read failed and leaves the quote-to-booking conversion confirmation untouched.",
   "emptyFirstRun": "No quote-to-booking conversion confirmation yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the quote-to-booking conversion confirmation are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listQuoteBookingConversion",
    "contract": "orders",
    "purpose": "Quote-to-Booking Conversion & Confirmation",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "QuoteToBookingConversionConfirmationView.quoteRemainsValid",
    "QuoteToBookingConversionConfirmationView.capacityRemainsAvailable",
    "QuoteToBookingConversionConfirmationView.resourcesRemainAvailable",
    "QuoteToBookingConversionConfirmationView.priceRemainsApproved",
    "QuoteToBookingConversionConfirmationView.approvalRemainsValid"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-272"
  },
  "apisNote": "Regenerated 9 September 2026 from Group_Sales___Corporate_Booking_Management_Reference.pdf page 15. 0 of 0 labels bound to a contract property; 0 of 38 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-273",
  "name": "Group Booking 360° & Handover Workspace",
  "module": "Sell",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Group_Sales___Corporate_Booking_Management_Reference.pdf",
   "board": "1",
   "number": "9.1.10",
   "page": 16
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/sell/group-booking-360-handover-workspace-bo-273",
   "component": "apps/venue-management-web/src/routes/sell/GroupBooking360HandoverWorkspace.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-264"
   ],
   "exitTo": [
    "BO-264"
   ],
   "inferred": false,
   "notes": "**Reached from BO-264, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation."
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display; Show) and no metric row",
  "purpose": "Provide a consolidated view of the completed sales journey and hand the confirmed group cleanly from Sales to Operations. 360° Header Board 1 ended when the quotation was accepted and converted into a confirmed group booking. Board 2 takes over from confirmation until the group visit is completed and financially closed.",
  "purposeNote": "Once a group sale is confirmed, Sales can hand over a complete and structured booking to Operations without relying on emails, spreadsheets or manual re-entry. Board 1 — Final Screen Register",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every group booking 360°",
       "columns": [
        "GroupBooking360HandoverWorkspaceView.arrival",
        "GroupBooking360HandoverWorkspaceView.groupCheckIn",
        "GroupBooking360HandoverWorkspaceView.guides",
        "GroupBooking360HandoverWorkspaceView.catering",
        "GroupBooking360HandoverWorkspaceView.accessibility",
        "GroupBooking360HandoverWorkspaceView.transport",
        "GroupBooking360HandoverWorkspaceView.parking",
        "GroupBooking360HandoverWorkspaceView.specialInstructions",
        "GroupBooking360HandoverWorkspaceView.resources",
        "GroupBooking360HandoverWorkspaceView.originalEnquiry",
        "GroupBooking360HandoverWorkspaceView.opportunity",
        "GroupBooking360HandoverWorkspaceView.finalQuote",
        "GroupBooking360HandoverWorkspaceView.discount",
        "GroupBooking360HandoverWorkspaceView.approval",
        "GroupBooking360HandoverWorkspaceView.agreedPrice",
        "GroupBooking360HandoverWorkspaceView.deposit",
        "GroupBooking360HandoverWorkspaceView.balance",
        "GroupBooking360HandoverWorkspaceView.products",
        "GroupBooking360HandoverWorkspaceView.tickets",
        "GroupBooking360HandoverWorkspaceView.dateTime",
        "GroupBooking360HandoverWorkspaceView.capacity",
        "GroupBooking360HandoverWorkspaceView.seatingWhereApplicable",
        "GroupBooking360HandoverWorkspaceView.packageComponents",
        "GroupBooking360HandoverWorkspaceView.organization",
        "GroupBooking360HandoverWorkspaceView.mainContact",
        "GroupBooking360HandoverWorkspaceView.financeContact",
        "GroupBooking360HandoverWorkspaceView.eventDayContact"
       ],
       "bindsTo": "GroupBooking360HandoverWorkspaceView",
       "operation": "setGroupBookingHandover",
       "provenance": "pack Group_Sales___Corporate_Booking_Management_Reference.pdf, page 16 §Display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected group booking 360°",
       "bindsTo": "GroupBooking360HandoverWorkspaceView",
       "columns": [
        "GroupBooking360HandoverWorkspaceView.arrival",
        "GroupBooking360HandoverWorkspaceView.groupCheckIn",
        "GroupBooking360HandoverWorkspaceView.guides",
        "GroupBooking360HandoverWorkspaceView.catering",
        "GroupBooking360HandoverWorkspaceView.accessibility",
        "GroupBooking360HandoverWorkspaceView.transport",
        "GroupBooking360HandoverWorkspaceView.parking",
        "GroupBooking360HandoverWorkspaceView.specialInstructions",
        "GroupBooking360HandoverWorkspaceView.resources",
        "GroupBooking360HandoverWorkspaceView.originalEnquiry",
        "GroupBooking360HandoverWorkspaceView.opportunity",
        "GroupBooking360HandoverWorkspaceView.finalQuote",
        "GroupBooking360HandoverWorkspaceView.discount",
        "GroupBooking360HandoverWorkspaceView.approval",
        "GroupBooking360HandoverWorkspaceView.agreedPrice",
        "GroupBooking360HandoverWorkspaceView.deposit",
        "GroupBooking360HandoverWorkspaceView.balance",
        "GroupBooking360HandoverWorkspaceView.products",
        "GroupBooking360HandoverWorkspaceView.tickets",
        "GroupBooking360HandoverWorkspaceView.dateTime",
        "GroupBooking360HandoverWorkspaceView.capacity",
        "GroupBooking360HandoverWorkspaceView.seatingWhereApplicable",
        "GroupBooking360HandoverWorkspaceView.packageComponents",
        "GroupBooking360HandoverWorkspaceView.organization",
        "GroupBooking360HandoverWorkspaceView.mainContact",
        "GroupBooking360HandoverWorkspaceView.financeContact",
        "GroupBooking360HandoverWorkspaceView.eventDayContact"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Backend Screen Primary Responsibility”, “Enquiry/opportunity”, “Multi-product package”, “Group Quotation Builder & Proposal”, “Quote Revision, Negotiation & Version”, “Group Discount, Exception & Approval”.",
       "provenance": "pack Group_Sales___Corporate_Booking_Management_Reference.pdf, page 16 §Display"
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
       "provenance": "contract operation setGroupBookingHandover"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The group booking 360° list.",
   "error": "Could not load. Names which read failed and leaves the group booking 360° untouched.",
   "emptyFirstRun": "No group booking 360° yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the group booking 360° are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setGroupBookingHandover",
    "contract": "orders",
    "purpose": "Group Booking 360° & Handover Workspace",
    "trigger": "onAction",
    "invalidates": [
     "setGroupBookingHandover"
    ]
   }
  ],
  "entryState": {
   "preloaded": [
    "GroupBooking360HandoverWorkspaceView.arrival",
    "GroupBooking360HandoverWorkspaceView.groupCheckIn",
    "GroupBooking360HandoverWorkspaceView.guides",
    "GroupBooking360HandoverWorkspaceView.catering",
    "GroupBooking360HandoverWorkspaceView.accessibility",
    "GroupBooking360HandoverWorkspaceView.transport"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-273"
  },
  "apisNote": "Regenerated 9 September 2026 from Group_Sales___Corporate_Booking_Management_Reference.pdf page 16. 27 of 27 labels bound to a contract property; 27 of 90 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
 "approveGroupDiscountException": {
  "method": "PUT",
  "path": "/group-discount-exception",
  "contract": "orders",
  "summary": "Group Discount, Exception & Approval Workflow",
  "permission": "ORDER_CREATE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": "GroupDiscountExceptionApprovalWorkflowInput",
  "responds": "GroupDiscountExceptionApprovalWorkflowView"
 },
 "listGroupCustomerOrganization": {
  "method": "GET",
  "path": "/group-customer-organization",
  "contract": "orders",
  "summary": "Group Customer & Organization Profile",
  "permission": "ORDER_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "GroupCustomerOrganizationProfileView"
 },
 "listGroupEnquiryOpportunity": {
  "method": "GET",
  "path": "/group-enquiry-opportunity",
  "contract": "orders",
  "summary": "Group Enquiry & Opportunity Capture",
  "permission": "ORDER_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "GroupEnquiryOpportunityCaptureView"
 },
 "listGroupRequirementAvailability": {
  "method": "GET",
  "path": "/group-requirement-availability",
  "contract": "orders",
  "summary": "Group Requirements, Availability & Capacity Planner",
  "permission": "ORDER_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "GroupRequirementsAvailabilityCapacityPlannerView"
 },
 "listGroupSale": {
  "method": "GET",
  "path": "/group-sale",
  "contract": "orders",
  "summary": "Group Sales Command Center",
  "permission": "ORDER_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "GroupSalesCommandCenterView"
 },
 "listQuoteBookingConversion": {
  "method": "GET",
  "path": "/quote-booking-conversion",
  "contract": "orders",
  "summary": "Quote-to-Booking Conversion & Confirmation",
  "permission": "ORDER_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "QuoteToBookingConversionConfirmationView"
 },
 "listQuoteRevisionNegotiation": {
  "method": "GET",
  "path": "/quote-revision-negotiation",
  "contract": "orders",
  "summary": "Quote Revision, Negotiation & Version Management",
  "permission": "ORDER_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "QuoteRevisionNegotiationVersionManagementView"
 },
 "setGroupBookingHandover": {
  "method": "PUT",
  "path": "/group-booking-handover",
  "contract": "orders",
  "summary": "Group Booking 360° & Handover Workspace",
  "permission": "ORDER_CREATE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": "GroupBooking360HandoverWorkspaceInput",
  "responds": "GroupBooking360HandoverWorkspaceView"
 },
 "setGroupPackageExperience": {
  "method": "PUT",
  "path": "/group-package-experience",
  "contract": "orders",
  "summary": "Group Package & Experience Builder",
  "permission": "ORDER_CREATE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": "GroupPackageExperienceBuilderInput",
  "responds": "GroupPackageExperienceBuilderView"
 },
 "setGroupQuotationProposal": {
  "method": "PUT",
  "path": "/group-quotation-proposal",
  "contract": "orders",
  "summary": "Group Quotation Builder & Proposal Generation",
  "permission": "ORDER_CREATE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": "GroupQuotationBuilderProposalGenerationInput",
  "responds": "GroupQuotationBuilderProposalGenerationView"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "GroupBooking360HandoverWorkspaceInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures",
  "description": "**What Group Booking 360° & Handover Workspace submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "notes": {
    "type": "string",
    "description": "Notes"
   },
   "tasks": {
    "type": "string",
    "description": "Tasks"
   },
   "attachments": {
    "type": "string",
    "description": "Attachments"
   },
   "departmentAssignments": {
    "type": "string",
    "description": "Department assignments"
   },
   "internalMentions": {
    "type": "string",
    "description": "Internal mentions"
   },
   "handoverAcknowledgment": {
    "type": "string",
    "description": "Handover acknowledgment"
   },
   "creation": {
    "type": "string",
    "description": "creation"
   },
   "groupRequirementsAvailabilityCapacity": {
    "type": "integer",
    "description": "Group Requirements, Availability & Capacity"
   },
   "servicesTheGroup": {
    "type": "string",
    "description": "services the group"
   },
   "reconciliationPerformanceAi": {
    "type": "string",
    "description": "Reconciliation → Performance & AI"
   }
  }
 },
 "GroupBooking360HandoverWorkspaceView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over orders state, assembled at read time from tables that already exist",
  "description": "**What Group Booking 360° & Handover Workspace displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "arrival": {
    "type": "string",
    "description": "Arrival"
   },
   "groupCheckIn": {
    "type": "string",
    "description": "Group Check-In"
   },
   "guides": {
    "type": "integer",
    "description": "Guides"
   },
   "catering": {
    "type": "string",
    "description": "Catering"
   },
   "accessibility": {
    "type": "string",
    "description": "Accessibility"
   },
   "transport": {
    "type": "string",
    "description": "Transport"
   },
   "parking": {
    "type": "string",
    "description": "Parking"
   },
   "specialInstructions": {
    "type": "integer",
    "description": "Special Instructions"
   },
   "resources": {
    "type": "integer",
    "description": "Resources"
   },
   "originalEnquiry": {
    "type": "string",
    "description": "Original Enquiry"
   },
   "opportunity": {
    "type": "string",
    "description": "Opportunity"
   },
   "finalQuote": {
    "type": "string",
    "description": "Final Quote"
   },
   "discount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Discount"
   },
   "approval": {
    "type": "string",
    "description": "Approval"
   },
   "agreedPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Agreed Price"
   },
   "deposit": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Deposit"
   },
   "balance": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Balance"
   },
   "products": {
    "type": "integer",
    "description": "Products"
   },
   "tickets": {
    "type": "integer",
    "description": "Tickets"
   },
   "dateTime": {
    "type": "string",
    "format": "date-time",
    "description": "Date/time"
   },
   "capacity": {
    "type": "integer",
    "description": "Capacity"
   },
   "seatingWhereApplicable": {
    "type": "string",
    "description": "Seating where applicable"
   },
   "packageComponents": {
    "type": "integer",
    "description": "Package components"
   },
   "organization": {
    "type": "string",
    "description": "Organization"
   },
   "mainContact": {
    "type": "string",
    "description": "Main Contact"
   },
   "financeContact": {
    "type": "string",
    "description": "Finance Contact"
   },
   "eventDayContact": {
    "type": "string",
    "description": "Event-Day Contact"
   },
   "notes": {
    "type": "string",
    "description": "Notes"
   },
   "tasks": {
    "type": "string",
    "description": "Tasks"
   },
   "attachments": {
    "type": "string",
    "description": "Attachments"
   },
   "departmentAssignments": {
    "type": "string",
    "description": "Department assignments"
   },
   "internalMentions": {
    "type": "string",
    "description": "Internal mentions"
   },
   "handoverAcknowledgment": {
    "type": "string",
    "description": "Handover acknowledgment"
   },
   "creation": {
    "type": "string",
    "description": "creation"
   },
   "groupRequirementsAvailabilityCapacity": {
    "type": "integer",
    "description": "Group Requirements, Availability & Capacity"
   },
   "servicesTheGroup": {
    "type": "string",
    "description": "services the group"
   },
   "reconciliationPerformanceAi": {
    "type": "string",
    "description": "Reconciliation → Performance & AI"
   }
  }
 },
 "GroupCustomerOrganizationProfileView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over orders state, assembled at read time from tables that already exist",
  "description": "**What Group Customer & Organization Profile displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "school": {
    "type": "string",
    "description": "School"
   },
   "university": {
    "type": "string",
    "description": "University"
   },
   "company": {
    "type": "string",
    "description": "Company"
   },
   "government": {
    "type": "string",
    "description": "Government"
   },
   "sportsClub": {
    "type": "string",
    "description": "Sports Club"
   },
   "association": {
    "type": "string",
    "description": "Association"
   },
   "tourGroup": {
    "type": "string",
    "description": "Tour Group"
   },
   "privateGroup": {
    "type": "string",
    "description": "Private Group"
   },
   "eventOrganizer": {
    "type": "string",
    "description": "Event Organizer"
   },
   "charity": {
    "type": "string",
    "description": "Charity"
   },
   "organizationName": {
    "type": "string",
    "description": "Organization Name"
   },
   "customerId": {
    "type": "string",
    "description": "Customer ID"
   },
   "organizationType": {
    "type": "string",
    "description": "Organization Type"
   },
   "registrationDetailsWhereApplicable": {
    "type": "string",
    "description": "Registration Details where applicable"
   },
   "country": {
    "type": "string",
    "description": "Country"
   },
   "city": {
    "type": "string",
    "description": "City"
   },
   "address": {
    "type": "string",
    "description": "Address"
   },
   "taxVatInformation": {
    "type": "string",
    "description": "Tax/VAT Information"
   },
   "preferredLanguage": {
    "type": "string",
    "description": "Preferred Language"
   },
   "billingDetails": {
    "type": "string",
    "description": "Billing Details"
   },
   "accountOwner": {
    "type": "string",
    "description": "Account Owner"
   },
   "primaryContact": {
    "type": "string",
    "description": "Primary Contact"
   },
   "bookingContact": {
    "type": "string",
    "description": "Booking Contact"
   },
   "financeContact": {
    "type": "string",
    "description": "Finance Contact"
   },
   "eventDayContact": {
    "type": "string",
    "description": "Event-Day Contact"
   },
   "decisionMaker": {
    "type": "string",
    "description": "Decision Maker"
   },
   "previousEnquiries": {
    "type": "integer",
    "description": "Previous enquiries"
   },
   "previousQuotations": {
    "type": "integer",
    "description": "Previous quotations"
   },
   "confirmedBookings": {
    "type": "integer",
    "description": "Confirmed bookings"
   },
   "totalGuests": {
    "type": "integer",
    "description": "Total guests"
   },
   "revenue": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Revenue"
   },
   "cancellationHistory": {
    "type": "string",
    "description": "Cancellation history"
   },
   "outstandingBalance": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Outstanding balance"
   },
   "futureBookings": {
    "type": "integer",
    "description": "Future bookings"
   }
  }
 },
 "GroupDiscountExceptionApprovalWorkflowInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table covers these fields** — the closest is orders.cash_movement at 5%, so this is not an update to anything the package stores today and no new table has been decided",
  "description": "**What Group Discount, Exception & Approval Workflow submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "standardGroupDiscount10": {
    "type": "number",
    "description": "Standard Group Discount: 10%"
   },
   "requested18": {
    "type": "number",
    "description": "Requested: 18%"
   },
   "approvalRequiredCommercialDirector": {
    "type": "string",
    "description": "Approval required — Commercial Director"
   },
   "discount": {
    "type": "number",
    "description": "Discount %"
   },
   "transactionValue": {
    "type": "string",
    "description": "Transaction value"
   },
   "margin": {
    "type": "number",
    "description": "Margin"
   },
   "customerType": {
    "type": "string",
    "description": "Customer type"
   },
   "venue": {
    "type": "string",
    "description": "Venue"
   },
   "event": {
    "type": "string",
    "description": "Event"
   },
   "salesUser": {
    "type": "string",
    "description": "Sales user"
   },
   "risk": {
    "type": "string",
    "description": "Risk"
   },
   "customer": {
    "type": "string",
    "description": "Customer"
   },
   "opportunity": {
    "type": "string",
    "description": "Opportunity"
   },
   "quote": {
    "type": "string",
    "description": "Quote"
   },
   "standardPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Standard Price"
   },
   "proposedPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Proposed Price"
   },
   "marginImpact": {
    "type": "number",
    "description": "Margin Impact"
   },
   "historicalCustomerValue": {
    "type": "string",
    "description": "Historical Customer Value"
   },
   "reason": {
    "type": "string",
    "description": "Reason"
   },
   "capacityImpact": {
    "type": "integer",
    "description": "Capacity Impact"
   }
  }
 },
 "GroupDiscountExceptionApprovalWorkflowView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over orders state, assembled at read time from tables that already exist",
  "description": "**What Group Discount, Exception & Approval Workflow displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "standardGroupDiscount10": {
    "type": "number",
    "description": "Standard Group Discount: 10%"
   },
   "requested18": {
    "type": "number",
    "description": "Requested: 18%"
   },
   "approvalRequiredCommercialDirector": {
    "type": "string",
    "description": "Approval required — Commercial Director"
   },
   "discount": {
    "type": "number",
    "description": "Discount %"
   },
   "transactionValue": {
    "type": "string",
    "description": "Transaction value"
   },
   "margin": {
    "type": "number",
    "description": "Margin"
   },
   "customerType": {
    "type": "string",
    "description": "Customer type"
   },
   "venue": {
    "type": "string",
    "description": "Venue"
   },
   "event": {
    "type": "string",
    "description": "Event"
   },
   "salesUser": {
    "type": "string",
    "description": "Sales user"
   },
   "risk": {
    "type": "string",
    "description": "Risk"
   },
   "customer": {
    "type": "string",
    "description": "Customer"
   },
   "opportunity": {
    "type": "string",
    "description": "Opportunity"
   },
   "quote": {
    "type": "string",
    "description": "Quote"
   },
   "standardPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Standard Price"
   },
   "proposedPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Proposed Price"
   },
   "marginImpact": {
    "type": "number",
    "description": "Margin Impact"
   },
   "historicalCustomerValue": {
    "type": "string",
    "description": "Historical Customer Value"
   },
   "reason": {
    "type": "string",
    "description": "Reason"
   },
   "capacityImpact": {
    "type": "integer",
    "description": "Capacity Impact"
   }
  }
 },
 "GroupEnquiryOpportunityCaptureView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over orders state, assembled at read time from tables that already exist",
  "description": "**What Group Enquiry & Opportunity Capture displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "website": {
    "type": "string",
    "description": "Website"
   },
   "phone": {
    "type": "string",
    "description": "Phone"
   },
   "email": {
    "type": "string",
    "description": "Email"
   },
   "walkIn": {
    "type": "string",
    "description": "Walk-in"
   },
   "salesTeam": {
    "type": "string",
    "description": "Sales Team"
   },
   "crm": {
    "type": "string",
    "description": "CRM"
   },
   "referral": {
    "type": "string",
    "description": "Referral"
   },
   "campaign": {
    "type": "string",
    "description": "Campaign"
   },
   "existingCustomer": {
    "type": "string",
    "description": "Existing Customer"
   },
   "manualEntry": {
    "type": "string",
    "description": "Manual Entry"
   },
   "enquiryId": {
    "type": "string",
    "description": "Enquiry ID"
   },
   "customerOrganization": {
    "type": "string",
    "description": "Customer/Organization"
   },
   "contact": {
    "type": "string",
    "description": "Contact"
   },
   "groupType": {
    "type": "string",
    "description": "Group Type"
   },
   "requestedVenue": {
    "type": "string",
    "description": "Requested Venue"
   },
   "requestedEvent": {
    "type": "string",
    "description": "Requested Event"
   },
   "requestedExperience": {
    "type": "string",
    "description": "Requested Experience"
   },
   "preferredDate": {
    "type": "string",
    "format": "date-time",
    "description": "Preferred Date"
   },
   "alternativeDate": {
    "type": "string",
    "format": "date-time",
    "description": "Alternative Date"
   },
   "preferredTime": {
    "type": "string",
    "format": "date-time",
    "description": "Preferred Time"
   },
   "estimatedGuests": {
    "type": "string",
    "description": "Estimated Guests"
   },
   "adults": {
    "type": "string",
    "description": "Adults"
   },
   "children": {
    "type": "string",
    "description": "Children"
   },
   "students": {
    "type": "string",
    "description": "Students"
   },
   "staffTeachers": {
    "type": "string",
    "description": "Staff/Teachers"
   },
   "specialRequirements": {
    "type": "string",
    "description": "Special Requirements"
   },
   "budget": {
    "type": "string",
    "description": "Budget"
   },
   "notes": {
    "type": "string",
    "description": "Notes"
   },
   "salesOwner": {
    "type": "string",
    "description": "Sales Owner"
   },
   "priority": {
    "type": "string",
    "description": "Priority"
   },
   "expectedValue": {
    "type": "string",
    "description": "Expected Value"
   },
   "probability": {
    "type": "string",
    "description": "Probability"
   },
   "expectedCloseDate": {
    "type": "string",
    "format": "date-time",
    "description": "Expected Close Date"
   },
   "leadSource": {
    "type": "string",
    "description": "Lead Source"
   },
   "nextAction": {
    "type": "string",
    "format": "date-time",
    "description": "Next Action"
   }
  }
 },
 "GroupPackageExperienceBuilderInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures",
  "description": "**What Group Package & Experience Builder submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "admissionTickets": {
    "type": "string",
    "description": "Admission Tickets"
   },
   "groupTicket": {
    "type": "string",
    "description": "Group Ticket"
   },
   "guidedTour": {
    "type": "string",
    "description": "Guided Tour"
   },
   "reservedSeating": {
    "type": "string",
    "description": "Reserved Seating"
   },
   "fB": {
    "type": "string",
    "description": "F&B"
   },
   "mealVoucher": {
    "type": "string",
    "description": "Meal Voucher"
   },
   "merchandise": {
    "type": "string",
    "description": "Merchandise"
   },
   "transportation": {
    "type": "string",
    "description": "Transportation"
   },
   "parking": {
    "type": "string",
    "description": "Parking"
   },
   "workshop": {
    "type": "string",
    "description": "Workshop"
   },
   "educationProgram": {
    "type": "string",
    "description": "Education Program"
   },
   "meetingRoom": {
    "type": "string",
    "description": "Meeting Room"
   },
   "vipExperience": {
    "type": "string",
    "description": "VIP Experience"
   },
   "addOns": {
    "type": "string",
    "description": "Add-ons"
   },
   "rentalResources": {
    "type": "string",
    "description": "Rental Resources"
   },
   "educationalWorkshop": {
    "type": "string",
    "description": "Educational Workshop"
   },
   "schoolPackage": {
    "type": "string",
    "description": "School Package"
   },
   "corporatePackage": {
    "type": "string",
    "description": "Corporate Package"
   },
   "birthdayPackage": {
    "type": "string",
    "description": "Birthday Package"
   },
   "vipGroupPackage": {
    "type": "string",
    "description": "VIP Group Package"
   },
   "conferencePackage": {
    "type": "string",
    "description": "Conference Package"
   }
  }
 },
 "GroupPackageExperienceBuilderView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over orders state, assembled at read time from tables that already exist",
  "description": "**What Group Package & Experience Builder displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "admissionTickets": {
    "type": "string",
    "description": "Admission Tickets"
   },
   "groupTicket": {
    "type": "string",
    "description": "Group Ticket"
   },
   "guidedTour": {
    "type": "string",
    "description": "Guided Tour"
   },
   "reservedSeating": {
    "type": "string",
    "description": "Reserved Seating"
   },
   "fB": {
    "type": "string",
    "description": "F&B"
   },
   "mealVoucher": {
    "type": "string",
    "description": "Meal Voucher"
   },
   "merchandise": {
    "type": "string",
    "description": "Merchandise"
   },
   "transportation": {
    "type": "string",
    "description": "Transportation"
   },
   "parking": {
    "type": "string",
    "description": "Parking"
   },
   "workshop": {
    "type": "string",
    "description": "Workshop"
   },
   "educationProgram": {
    "type": "string",
    "description": "Education Program"
   },
   "meetingRoom": {
    "type": "string",
    "description": "Meeting Room"
   },
   "vipExperience": {
    "type": "string",
    "description": "VIP Experience"
   },
   "addOns": {
    "type": "string",
    "description": "Add-ons"
   },
   "rentalResources": {
    "type": "string",
    "description": "Rental Resources"
   },
   "educationalWorkshop": {
    "type": "string",
    "description": "Educational Workshop"
   },
   "standardPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Standard Price"
   },
   "groupRate": {
    "type": "number",
    "description": "Group Rate"
   },
   "discount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Discount"
   },
   "complimentaryQuantity": {
    "type": "integer",
    "description": "Complimentary Quantity"
   },
   "addOnPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Add-on Price"
   },
   "tax": {
    "type": "string",
    "description": "Tax"
   },
   "fees": {
    "type": "integer",
    "description": "Fees"
   },
   "packageTotal": {
    "type": "string",
    "description": "Package Total"
   },
   "pricePerGuest": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Price Per Guest"
   },
   "schoolPackage": {
    "type": "string",
    "description": "School Package"
   },
   "corporatePackage": {
    "type": "string",
    "description": "Corporate Package"
   },
   "birthdayPackage": {
    "type": "string",
    "description": "Birthday Package"
   },
   "vipGroupPackage": {
    "type": "string",
    "description": "VIP Group Package"
   },
   "conferencePackage": {
    "type": "string",
    "description": "Conference Package"
   }
  }
 },
 "GroupQuotationBuilderProposalGenerationInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table covers these fields** — the closest is orders.cart at 3%, so this is not an update to anything the package stores today and no new table has been decided",
  "description": "**What Group Quotation Builder & Proposal Generation submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.\n\n**The pack defines this as a record**, under *For each line* - one of only 13 drafted writes that does. That is the client writing a row rather than a screen, and it is where the table conversation should start.",
  "properties": {
   "quoteNumber": {
    "type": "string",
    "description": "Quote Number"
   },
   "opportunity": {
    "type": "string",
    "description": "Opportunity"
   },
   "customer": {
    "type": "string",
    "description": "Customer"
   },
   "contact": {
    "type": "string",
    "description": "Contact"
   },
   "quoteDate": {
    "type": "string",
    "format": "date-time",
    "description": "Quote Date"
   },
   "validUntil": {
    "type": "string",
    "description": "Valid Until"
   },
   "visitDate": {
    "type": "string",
    "format": "date-time",
    "description": "Visit Date"
   },
   "guestCount": {
    "type": "integer",
    "description": "Guest Count"
   },
   "currency": {
    "type": "string",
    "description": "Currency"
   },
   "salesOwner": {
    "type": "string",
    "description": "Sales Owner"
   },
   "productService": {
    "type": "string",
    "description": "Product/Service"
   },
   "description": {
    "type": "string",
    "description": "Description"
   },
   "quantity": {
    "type": "integer",
    "description": "Quantity"
   },
   "standardRate": {
    "type": "number",
    "description": "Standard Rate"
   },
   "groupRate": {
    "type": "number",
    "description": "Group Rate"
   },
   "discount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Discount"
   },
   "tax": {
    "type": "string",
    "description": "Tax"
   },
   "fee": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Fee"
   },
   "total": {
    "type": "integer",
    "description": "Total"
   },
   "quoteValidity": {
    "type": "string",
    "description": "Quote validity"
   },
   "depositRequirement": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Deposit requirement"
   },
   "paymentSchedule": {
    "type": "string",
    "description": "Payment schedule"
   },
   "cancellationPolicy": {
    "type": "string",
    "description": "Cancellation policy"
   },
   "amendmentConditions": {
    "type": "string",
    "description": "Amendment conditions"
   },
   "guestCountDeadline": {
    "type": "string",
    "format": "date-time",
    "description": "Guest-count deadline"
   },
   "operationalTerms": {
    "type": "string",
    "description": "Operational terms"
   },
   "email": {
    "type": "string",
    "description": "Email"
   },
   "pdf": {
    "type": "string",
    "description": "PDF"
   },
   "customerPortal": {
    "type": "string",
    "description": "Customer portal"
   },
   "secureDigitalLink": {
    "type": "string",
    "description": "Secure digital link"
   }
  },
  "x-ticvai-record-definition": "For each line"
 },
 "GroupQuotationBuilderProposalGenerationView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over orders state, assembled at read time from tables that already exist",
  "description": "**What Group Quotation Builder & Proposal Generation displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "quoteNumber": {
    "type": "string",
    "description": "Quote Number"
   },
   "opportunity": {
    "type": "string",
    "description": "Opportunity"
   },
   "customer": {
    "type": "string",
    "description": "Customer"
   },
   "contact": {
    "type": "string",
    "description": "Contact"
   },
   "quoteDate": {
    "type": "string",
    "format": "date-time",
    "description": "Quote Date"
   },
   "validUntil": {
    "type": "string",
    "description": "Valid Until"
   },
   "visitDate": {
    "type": "string",
    "format": "date-time",
    "description": "Visit Date"
   },
   "guestCount": {
    "type": "integer",
    "description": "Guest Count"
   },
   "currency": {
    "type": "string",
    "description": "Currency"
   },
   "salesOwner": {
    "type": "string",
    "description": "Sales Owner"
   },
   "productService": {
    "type": "string",
    "description": "Product/Service"
   },
   "description": {
    "type": "string",
    "description": "Description"
   },
   "quantity": {
    "type": "integer",
    "description": "Quantity"
   },
   "standardRate": {
    "type": "number",
    "description": "Standard Rate"
   },
   "groupRate": {
    "type": "number",
    "description": "Group Rate"
   },
   "discount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Discount"
   },
   "tax": {
    "type": "string",
    "description": "Tax"
   },
   "fee": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Fee"
   },
   "total": {
    "type": "integer",
    "description": "Total"
   },
   "quoteValidity": {
    "type": "string",
    "description": "Quote validity"
   },
   "depositRequirement": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Deposit requirement"
   },
   "paymentSchedule": {
    "type": "string",
    "description": "Payment schedule"
   },
   "cancellationPolicy": {
    "type": "string",
    "description": "Cancellation policy"
   },
   "amendmentConditions": {
    "type": "string",
    "description": "Amendment conditions"
   },
   "guestCountDeadline": {
    "type": "string",
    "format": "date-time",
    "description": "Guest-count deadline"
   },
   "operationalTerms": {
    "type": "string",
    "description": "Operational terms"
   },
   "email": {
    "type": "string",
    "description": "Email"
   },
   "pdf": {
    "type": "string",
    "description": "PDF"
   },
   "customerPortal": {
    "type": "string",
    "description": "Customer portal"
   },
   "secureDigitalLink": {
    "type": "string",
    "description": "Secure digital link"
   }
  }
 },
 "GroupRequirementsAvailabilityCapacityPlannerView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over orders state, assembled at read time from tables that already exist",
  "description": "**What Group Requirements, Availability & Capacity Planner displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "venue": {
    "type": "string",
    "description": "Venue"
   },
   "eventAttraction": {
    "type": "string",
    "description": "Event/Attraction"
   },
   "date": {
    "type": "string",
    "format": "date-time",
    "description": "Date"
   },
   "alternativeDates": {
    "type": "string",
    "description": "Alternative Dates"
   },
   "arrivalTime": {
    "type": "string",
    "format": "date-time",
    "description": "Arrival Time"
   },
   "departureTime": {
    "type": "string",
    "format": "date-time",
    "description": "Departure Time"
   },
   "groupSize": {
    "type": "string",
    "description": "Group Size"
   },
   "guestCategories": {
    "type": "string",
    "description": "Guest Categories"
   },
   "accessibilityRequirements": {
    "type": "string",
    "description": "Accessibility Requirements"
   },
   "seatingRequirement": {
    "type": "string",
    "description": "Seating Requirement"
   },
   "resources": {
    "type": "string",
    "description": "Resources"
   },
   "guides": {
    "type": "string",
    "description": "Guides"
   },
   "catering": {
    "type": "string",
    "description": "Catering"
   },
   "transportation": {
    "type": "string",
    "description": "Transportation"
   },
   "addOns": {
    "type": "string",
    "description": "Add-ons"
   },
   "eventCapacity": {
    "type": "integer",
    "description": "Event Capacity"
   },
   "availableCapacity": {
    "type": "integer",
    "description": "Available Capacity"
   },
   "existingGroups": {
    "type": "integer",
    "description": "Existing Groups"
   },
   "publicSales": {
    "type": "integer",
    "description": "Public Sales"
   },
   "operationalHolds": {
    "type": "integer",
    "description": "Operational Holds"
   },
   "resourceAvailability": {
    "type": "string",
    "description": "Resource Availability"
   },
   "timeslotAvailability": {
    "type": "string",
    "description": "Timeslot Availability"
   },
   "proposal": {
    "type": "string",
    "description": "proposal"
   },
   "rooms": {
    "type": "string",
    "description": "Rooms"
   },
   "equipment": {
    "type": "string",
    "description": "Equipment"
   },
   "vehicles": {
    "type": "string",
    "description": "Vehicles"
   },
   "meetingSpaces": {
    "type": "string",
    "description": "Meeting spaces"
   },
   "cateringCapacity": {
    "type": "integer",
    "description": "Catering capacity"
   }
  }
 },
 "GroupSalesCommandCenterView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over orders state, assembled at read time from tables that already exist",
  "description": "**What Group Sales Command Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "newEnquiries": {
    "type": "integer",
    "description": "New Enquiries"
   },
   "quotationsOutstanding": {
    "type": "string",
    "description": "Quotations Outstanding"
   },
   "quotesAwaitingApproval": {
    "type": "string",
    "description": "Quotes Awaiting Approval"
   },
   "confirmedGroups": {
    "type": "integer",
    "description": "Confirmed Groups"
   },
   "expectedGuests": {
    "type": "integer",
    "description": "Expected Guests"
   },
   "pipelineValue": {
    "type": "string",
    "description": "Pipeline Value"
   },
   "confirmedRevenue": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Confirmed Revenue"
   },
   "conversionRate": {
    "type": "number",
    "description": "Conversion Rate"
   },
   "averageGroupValue": {
    "type": "number",
    "description": "Average Group Value"
   },
   "expiringQuotes": {
    "type": "integer",
    "description": "Expiring Quotes"
   },
   "salesTargetAchievement": {
    "type": "string",
    "description": "Sales Target Achievement"
   },
   "enquiryId": {
    "type": "string",
    "description": "Enquiry ID"
   },
   "organizationCustomer": {
    "type": "string",
    "description": "Organization/Customer"
   },
   "groupType": {
    "type": "string",
    "description": "Group Type"
   },
   "eventAttraction": {
    "type": "string",
    "description": "Event/Attraction"
   },
   "visitDate": {
    "type": "string",
    "format": "date-time",
    "description": "Visit Date"
   },
   "guestCount": {
    "type": "integer",
    "description": "Guest Count"
   },
   "salesOwner": {
    "type": "string",
    "description": "Sales Owner"
   },
   "estimatedValue": {
    "type": "string",
    "description": "Estimated Value"
   },
   "quoteStatus": {
    "type": "string",
    "description": "Quote Status"
   },
   "probability": {
    "type": "string",
    "description": "Probability"
   },
   "nextAction": {
    "type": "string",
    "format": "date-time",
    "description": "Next Action"
   },
   "expectedCloseDate": {
    "type": "string",
    "format": "date-time",
    "description": "Expected Close Date"
   },
   "followUpsDue": {
    "type": "string",
    "description": "Follow-ups due"
   },
   "quotesExpiring": {
    "type": "string",
    "description": "Quotes expiring"
   },
   "customerResponses": {
    "type": "integer",
    "description": "Customer responses"
   },
   "approvalRequests": {
    "type": "integer",
    "description": "Approval requests"
   },
   "depositsPending": {
    "type": "integer",
    "description": "Deposits pending"
   }
  }
 },
 "QuoteRevisionNegotiationVersionManagementView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over orders state, assembled at read time from tables that already exist",
  "description": "**What Quote Revision, Negotiation & Version Management displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "v2": {
    "type": "string",
    "description": "v2"
   },
   "v3Accepted": {
    "type": "string",
    "description": "v3 — Accepted"
   },
   "v1V2V3": {
    "type": "string",
    "description": "v1 v2 v3"
   },
   "nt": {
    "type": "string",
    "description": "nt"
   },
   "customerRequest": {
    "type": "string",
    "description": "Customer Request"
   },
   "internalResponse": {
    "type": "string",
    "description": "Internal Response"
   },
   "priceChange": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Price Change"
   },
   "quantityChange": {
    "type": "integer",
    "description": "Quantity Change"
   },
   "packageChange": {
    "type": "string",
    "description": "Package Change"
   },
   "termsChange": {
    "type": "string",
    "description": "Terms Change"
   },
   "date": {
    "type": "string",
    "format": "date-time",
    "description": "Date"
   },
   "user": {
    "type": "string",
    "description": "User"
   }
  }
 },
 "QuoteToBookingConversionConfirmationView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over orders state, assembled at read time from tables that already exist",
  "description": "**What Quote-to-Booking Conversion & Confirmation displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "quoteRemainsValid": {
    "type": "string",
    "description": "Quote remains valid"
   },
   "capacityRemainsAvailable": {
    "type": "integer",
    "description": "Capacity remains available"
   },
   "resourcesRemainAvailable": {
    "type": "string",
    "description": "Resources remain available"
   },
   "priceRemainsApproved": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Price remains approved"
   },
   "approvalRemainsValid": {
    "type": "string",
    "description": "Approval remains valid"
   },
   "customerDetailsComplete": {
    "type": "string",
    "description": "Customer details complete"
   },
   "paymentDepositRuleConfigured": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Payment/deposit rule configured"
   },
   "guestCountValid": {
    "type": "integer",
    "description": "Guest count valid"
   },
   "groupBookingId": {
    "type": "string",
    "description": "Group Booking ID"
   },
   "ticvaiOrder": {
    "type": "string",
    "description": "TICVAI Order"
   },
   "customer": {
    "type": "string",
    "description": "Customer"
   },
   "visitEvent": {
    "type": "string",
    "description": "Visit/Event"
   },
   "products": {
    "type": "string",
    "description": "Products"
   },
   "quantity": {
    "type": "integer",
    "description": "Quantity"
   },
   "agreedPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Agreed Price"
   },
   "paymentSchedule": {
    "type": "string",
    "description": "Payment Schedule"
   },
   "operationalRequirements": {
    "type": "string",
    "description": "Operational Requirements"
   },
   "salesOwner": {
    "type": "string",
    "description": "Sales Owner"
   },
   "applicable": {
    "type": "string",
    "description": "applicable"
   },
   "bookingConfirmation": {
    "type": "string",
    "description": "Booking Confirmation"
   },
   "paymentInstructions": {
    "type": "string",
    "description": "Payment Instructions"
   },
   "depositRequest": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Deposit Request"
   },
   "customerPortalLinkWhereApplicable": {
    "type": "string",
    "description": "Customer Portal Link where applicable"
   },
   "nextSteps": {
    "type": "string",
    "format": "date-time",
    "description": "Next Steps"
   }
  }
 }
}
```
