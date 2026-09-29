# WS27 — Group Sales   Corporate Booking Management board 1

**10 screens · 15 operations · 22 schemas · 4 permissions**

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

- **Every control that can be refused must be gated.** 4 permissions apply here:
  `ORDER_CREATE, ORDER_MODIFY, ORDER_VIEW, PRODUCT_CONFIGURE`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `BO-264` | Group Sales Command Center | commandCentre | 2 | 0 | — |
| `BO-265` | Group Enquiry & Opportunity Capture | configEditor | 2 | 0 | — |
| `BO-266` | Group Customer & Organization Profile | listDetail | 2 | 0 | — |
| `BO-267` | Group Requirements, Availability & Capacity Planner | listDetail | 1 | 0 | — |
| `BO-268` | Group Package & Experience Builder | listDetail | 1 | 0 | — |
| `BO-269` | Group Quotation Builder & Proposal Generation | configEditor | 1 | 0 | — |
| `BO-270` | Quote Revision, Negotiation & Version Management | configEditor | 1 | 0 | — |
| `BO-271` | Group Discount, Exception & Approval Workflow | listDetail | 1 | 0 | — |
| `BO-272` | Quote-to-Booking Conversion & Confirmation | listDetail | 3 | 0 | — |
| `BO-273` | Group Booking 360° & Handover Workspace | listDetail | 1 | 0 | — |

## Thin screens in this batch

**BO-267, BO-271, BO-272, BO-273 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

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
     "provenance": "derived — BO-100 declares entryState.params  and BO-264 holds none of them, so the edge carries nothing and BO-100 opens cold"
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
  "purposeNote": "The Group Sales team can manage its complete direct-sales pipeline and immediately identify opportunities requiring commercial action.",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen both a metric directory (§Display; Show) and a per-row directory (§Each opportunity should display) — counts over a population, then the population",
  "purpose": "Provide the Group Sales team with a centralized commercial workspace showing the entire group-sales pipeline.",
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
    "operationId": "listGroupSale2",
    "contract": "orders",
    "purpose": "Group Sales Analytics & AI Intelligence Center",
    "trigger": "onLoad"
   },
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
   "board": "wireframes/P08 Venue Management.dc.html#bo-264",
   "workshopBoard": "wireframes/WS68 Group Sales   Corporate Booking Management Board 1.dc.html#bo-264"
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
  "purposeNote": "Every group-sales request can be captured as a structured, owned and trackable opportunity without requiring a booking to exist yet.",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Capture; Configure) and no display directory — it is settings, not a population",
  "purpose": "Capture a new group-sales enquiry and convert it into a structured sales opportunity.",
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
      },
      {
       "kind": "secondaryButton",
       "label": "Manual Entry",
       "provenance": "pack Group_Sales___Corporate_Booking_Management_Reference.pdf, page 5 §Support"
      },
      {
       "kind": "primaryButton",
       "label": "Capture enquiry",
       "operation": "createGroupEnquiry",
       "provenance": "contract orders.yaml POST /group-enquiry-opportunity (decided 29 September, VM close-out)"
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
   },
   {
    "operationId": "createGroupEnquiry",
    "contract": "orders",
    "purpose": "Capture enquiry",
    "trigger": "onAction"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-265",
   "workshopBoard": "wireframes/WS68 Group Sales   Corporate Booking Management Board 1.dc.html#bo-265"
  },
  "apisNote": "Regenerated 9 September 2026 from Group_Sales___Corporate_Booking_Management_Reference.pdf page 5. 0 of 0 labels bound to a contract property; 30 of 43 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here. **Pack actions reconciled 29 September (VM close-out):** still owed by a contract change: `createGroupEnquiry`.",
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
  "purposeNote": "Sales teams can see the complete relationship with a group customer while maintaining one governed customer record across TICVAI.",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Show) and no metric row",
  "purpose": "Maintain the customer or organization buying directly from TICVAI.",
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
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Event Organizer",
       "provenance": "pack Group_Sales___Corporate_Booking_Management_Reference.pdf, page 6 §Support"
      },
      {
       "kind": "primaryButton",
       "label": "Save organisation profile",
       "operation": "setGroupCustomerOrganization",
       "provenance": "contract orders.yaml PUT /group-customer-organization (decided 29 September, VM close-out)"
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
   },
   {
    "operationId": "setGroupCustomerOrganization",
    "contract": "orders",
    "purpose": "Save organisation profile",
    "trigger": "onAction"
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
   "board": "wireframes/P08 Venue Management.dc.html#bo-266",
   "workshopBoard": "wireframes/WS68 Group Sales   Corporate Booking Management Board 1.dc.html#bo-266"
  },
  "apisNote": "Regenerated 9 September 2026 from Group_Sales___Corporate_Booking_Management_Reference.pdf page 6. 8 of 8 labels bound to a contract property; 20 of 42 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here. **Pack actions reconciled 29 September (VM close-out):** still owed by a contract change: `setGroupCustomerOrganization`.",
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
  "purposeNote": "Sales teams can validate admission, schedule and required resource availability before making a commercial commitment to the customer.",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Determine whether TICVAI can accommodate the requested group before preparing a quotation.",
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
   "board": "wireframes/P08 Venue Management.dc.html#bo-267",
   "workshopBoard": "wireframes/WS68 Group Sales   Corporate Booking Management Board 1.dc.html#bo-267"
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
  "purposeNote": "Sales teams can build a multi-product group package while consuming approved TICVAI products, pricing and resources rather than manually calculating the offer outside the platform.",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Show) and no metric row",
  "purpose": "Build a complete commercial package tailored to the group's requirements.",
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
      },
      {
       "kind": "secondaryButton",
       "label": "Meal Voucher",
       "provenance": "pack Group_Sales___Corporate_Booking_Management_Reference.pdf, page 9 §Allow combinations of"
      },
      {
       "kind": "secondaryButton",
       "label": "VIP Experience",
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
    "trigger": "onAction"
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
   "board": "wireframes/P08 Venue Management.dc.html#bo-268",
   "workshopBoard": "wireframes/WS68 Group Sales   Corporate Booking Management Board 1.dc.html#bo-268"
  },
  "apisNote": "Regenerated 9 September 2026 from Group_Sales___Corporate_Booking_Management_Reference.pdf page 9. 9 of 9 labels bound to a contract property; 12 of 44 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here. **Pack actions reconciled 29 September (VM close-out):** Meal Voucher, VIP Experience are choices sent by `setGroupPackageExperience`.",
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
  "purposeNote": "Sales teams can generate a controlled, branded and auditable group quotation directly from the approved package configuration.",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Capture; Where configured, customer can) and no display directory — it is settings, not a population",
  "purpose": "Turn the configured group package into a professional customer quotation.",
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
    "trigger": "onAction"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-269",
   "workshopBoard": "wireframes/WS68 Group Sales   Corporate Booking Management Board 1.dc.html#bo-269"
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
  "purposeNote": "Every quotation revision and negotiation decision is retained with complete commercial history and impact visibility.",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Capture) and no display directory — it is settings, not a population",
  "purpose": "Manage the commercial negotiation process without losing historical versions.",
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
   "board": "wireframes/P08 Venue Management.dc.html#bo-270",
   "workshopBoard": "wireframes/WS68 Group Sales   Corporate Booking Management Board 1.dc.html#bo-270"
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
  "purposeNote": "No quotation containing a controlled commercial exception can be issued or accepted without the appropriate approval.",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Govern non-standard group pricing and commercial exceptions before a quote is committed.",
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
    "trigger": "onAction"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-271",
   "workshopBoard": "wireframes/WS68 Group Sales   Corporate Booking Management Board 1.dc.html#bo-271"
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
  "purposeNote": "An approved and accepted quotation can become a confirmed group booking while preserving the exact commercial agreement and without duplicate data entry.",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Convert an accepted quotation into a confirmed TICVAI group booking without re-entering the commercial configuration.",
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
      },
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "createGroupBooking",
       "label": "Create group booking",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "createGroupBooking"
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
   },
   {
    "operationId": "createGroupBooking",
    "contract": "orders",
    "purpose": "Convert the accepted quote into a group booking",
    "trigger": "onAction",
    "provenance": "decided 29 September, VM close-out (venue management and configuration)",
    "invalidates": [
     "listQuoteBookingConversion"
    ]
   },
   {
    "operationId": "updateGroupBooking",
    "contract": "orders",
    "purpose": "Confirm numbers or the leader on the converted booking",
    "trigger": "onAction",
    "provenance": "decided 29 September, VM close-out (venue management and configuration)",
    "invalidates": [
     "listQuoteBookingConversion"
    ]
   }
  ],
  "entryState": {
   "preloaded": [],
   "params": [
    {
     "name": "groupBookingId",
     "from": "navigation"
    }
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-272",
   "workshopBoard": "wireframes/WS68 Group Sales   Corporate Booking Management Board 1.dc.html#bo-272"
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
  "purposeNote": "Once a group sale is confirmed, Sales can hand over a complete and structured booking to Operations without relying on emails, spreadsheets or manual re-entry. Board 1 — Final Screen Register",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display; Show) and no metric row",
  "purpose": "Provide a consolidated view of the completed sales journey and hand the confirmed group cleanly from Sales to Operations. 360° Header Board 1 ended when the quotation was accepted and converted into a confirmed group booking. Board 2 takes over from confirmation until the group visit is completed and financially closed.",
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
        "GroupBooking360HandoverWorkspaceView.seating",
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
        "GroupBooking360HandoverWorkspaceView.seating",
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
    "trigger": "onAction"
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
   "board": "wireframes/P08 Venue Management.dc.html#bo-273",
   "workshopBoard": "wireframes/WS68 Group Sales   Corporate Booking Management Board 1.dc.html#bo-273"
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
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "GroupDiscountExceptionApprovalWorkflowInput",
  "responds": "GroupDiscountExceptionApprovalWorkflowView"
 },
 "createGroupBooking": {
  "method": "POST",
  "path": "/group-bookings",
  "contract": "orders",
  "summary": "Turn an order into a group booking",
  "permission": "ORDER_CREATE",
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
  "requestBody": "CreateGroupBookingRequest",
  "responds": "GroupBooking"
 },
 "createGroupEnquiry": {
  "method": "POST",
  "path": "/group-enquiry-opportunity",
  "contract": "orders",
  "summary": "Capture a group enquiry",
  "permission": "ORDER_CREATE",
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
  "requestBody": "GroupEnquiryInput",
  "responds": "GroupEnquiryOpportunityView"
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
 "listGroupSale2": {
  "method": "GET",
  "path": "/group-sale-2",
  "contract": "orders",
  "summary": "Group Sales Analytics & AI Intelligence Center",
  "permission": "ORDER_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "customerType",
    "in": "query",
    "required": false
   },
   {
    "name": "organization",
    "in": "query",
    "required": false
   },
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
    "name": "salesOwner",
    "in": "query",
    "required": false
   },
   {
    "name": "groupType",
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
    "name": "campaign",
    "in": "query",
    "required": false
   },
   {
    "name": "market",
    "in": "query",
    "required": false
   }
  ],
  "requestBody": null,
  "responds": "GroupSalesAnalyticsAiIntelligenceCenterView"
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
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "GroupBooking360HandoverWorkspaceInput",
  "responds": "GroupBooking360HandoverWorkspaceView"
 },
 "setGroupCustomerOrganization": {
  "method": "PUT",
  "path": "/group-customer-organization",
  "contract": "orders",
  "summary": "Save a group customer organisation's profile",
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
  "requestBody": "GroupCustomerOrganizationInput",
  "responds": "GroupCustomerOrganizationView"
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
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
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
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "GroupQuotationBuilderProposalGenerationInput",
  "responds": "GroupQuotationBuilderProposalGenerationView"
 },
 "updateGroupBooking": {
  "method": "PATCH",
  "path": "/group-bookings/{groupBookingId}",
  "contract": "orders",
  "summary": "Confirm numbers, change the leader or cancel a group",
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
  "requestBody": "UpdateGroupBookingRequest",
  "responds": "GroupBooking"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "CreateGroupBookingRequest": {
  "type": "object",
  "description": "Request only. Persisted as `GroupBooking`.",
  "required": [
   "orderId",
   "leaderSubjectId",
   "expectedSize"
  ],
  "properties": {
   "kind": {
    "type": "string",
    "enum": [
     "general",
     "school",
     "corporate",
     "party"
    ],
    "default": "general"
   },
   "packageProductId": {
    "type": "string",
    "nullable": true,
    "description": "The school-trip format or party package."
   },
   "yearGroup": {
    "type": "string",
    "maxLength": 40,
    "nullable": true
   },
   "accessAndDietaryNeeds": {
    "type": "string",
    "maxLength": 1000,
    "nullable": true
   },
   "celebrantName": {
    "type": "string",
    "maxLength": 120,
    "nullable": true,
    "description": "The birthday child."
   },
   "celebrantTurningAge": {
    "type": "integer",
    "minimum": 1,
    "maximum": 18,
    "nullable": true
   },
   "allergiesAndRequests": {
    "type": "string",
    "maxLength": 1000,
    "nullable": true
   },
   "finalHeadcountDueBy": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "orderId": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
   },
   "leaderSubjectId": {
    "type": "string",
    "format": "uuid",
    "description": "The person who pays, is called if the coach is late, and collects the names."
   },
   "organisationName": {
    "type": "string",
    "maxLength": 200,
    "nullable": true
   },
   "expectedSize": {
    "type": "integer",
    "minimum": 2
   },
   "minimumSize": {
    "type": "integer",
    "minimum": 1,
    "nullable": true
   },
   "attendeeCaptureRequired": {
    "type": "boolean",
    "default": false
   },
   "attendeeCaptureDueBy": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   }
  }
 },
 "GroupBooking": {
  "type": "object",
  "x-ticvai-persistence": "orders.group_booking",
  "description": "BL-028. **`BO-026 Group Bookings` ran on generic order operations** — no group size, no quota, no leader, no per-attendee capture.\n**The leader is the point.** A school booking forty places has one person who pays, one who is called if the coach is late, and forty who need names collecting — and a generic order has one guest.\n",
  "required": [
   "id",
   "orderId",
   "leaderSubjectId",
   "expectedSize",
   "status"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "kind": {
    "type": "string",
    "enum": [
     "general",
     "school",
     "corporate",
     "party"
    ],
    "default": "general"
   },
   "packageProductId": {
    "type": "string",
    "nullable": true,
    "description": "The school-trip format or party package."
   },
   "yearGroup": {
    "type": "string",
    "maxLength": 40,
    "nullable": true
   },
   "accessAndDietaryNeeds": {
    "type": "string",
    "maxLength": 1000,
    "nullable": true
   },
   "celebrantName": {
    "type": "string",
    "maxLength": 120,
    "nullable": true,
    "description": "The birthday child."
   },
   "celebrantTurningAge": {
    "type": "integer",
    "minimum": 1,
    "maximum": 18,
    "nullable": true
   },
   "allergiesAndRequests": {
    "type": "string",
    "maxLength": 1000,
    "nullable": true
   },
   "finalHeadcountDueBy": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "quoteSentAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true
   },
   "riskAssessmentSentAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true
   },
   "preferredDate": {
    "type": "string",
    "format": "date",
    "nullable": true,
    "description": "The date the guest asked for on `requestGroupBooking` — what its `409 dateUnavailable` is checked against. Null for a group a member of staff built from an order."
   },
   "orderId": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
   },
   "leaderSubjectId": {
    "type": "string",
    "format": "uuid"
   },
   "organisationName": {
    "type": "string",
    "nullable": true
   },
   "expectedSize": {
    "type": "integer"
   },
   "confirmedSize": {
    "type": "integer",
    "nullable": true
   },
   "minimumSize": {
    "type": "integer",
    "nullable": true,
    "description": "**Below which the group rate does not apply.** A booking for forty that arrives as twelve is a pricing question somebody has to answer at the gate, and stating the threshold means answering it at booking instead.\n"
   },
   "attendeeCaptureRequired": {
    "type": "boolean",
    "default": false,
    "description": "**Whether names are needed before admission.** A school trip usually needs them and a corporate day out usually does not, and the difference is a safeguarding requirement rather than a preference.\n"
   },
   "attendeeCaptureDueBy": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "status": {
    "type": "string",
    "enum": [
     "provisional",
     "confirmed",
     "namesPending",
     "complete",
     "cancelled"
    ]
   }
  }
 },
 "GroupBooking360HandoverWorkspaceInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; lands in the handover columns of `orders.group_visit_plan` (DM5, 29 September)",
  "description": "**What Group Booking 360° & Handover Workspace submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "notes": {
    "type": "string",
    "description": "Notes"
   },
   "attachments": {
    "type": "string",
    "description": "Attachments"
   },
   "handoverAcknowledgment": {
    "type": "string",
    "description": "Handover acknowledgment"
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
   "attachments": {
    "type": "string",
    "description": "Attachments"
   },
   "handoverAcknowledgment": {
    "type": "string",
    "description": "Handover acknowledgment"
   },
   "seating": {
    "type": "string",
    "description": "Seating where applicable"
   }
  }
 },
 "GroupCustomerOrganizationInput": {
  "type": "object",
  "x-ticvai-persistence": "none — request only",
  "description": "What `setGroupCustomerOrganization` takes (decided 29 September, readiness close-out).",
  "required": [
   "name",
   "organisationType"
  ],
  "properties": {
   "organisationId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Null creates the organisation; an id replaces that profile."
   },
   "name": {
    "type": "string",
    "maxLength": 200
   },
   "organisationType": {
    "type": "string",
    "description": "What kind of buyer this is (decided 29 September, readiness close-out).",
    "enum": [
     "school",
     "corporate",
     "travelAgent",
     "eventOrganizer",
     "association",
     "government",
     "other"
    ]
   },
   "contacts": {
    "type": "array",
    "items": {
     "type": "object",
     "required": [
      "role",
      "name"
     ],
     "properties": {
      "role": {
       "type": "string",
       "enum": [
        "primary",
        "booking",
        "finance",
        "eventDay",
        "decisionMaker"
       ]
      },
      "name": {
       "type": "string",
       "maxLength": 120
      },
      "email": {
       "type": "string",
       "format": "email",
       "nullable": true
      },
      "phone": {
       "type": "string",
       "maxLength": 30,
       "nullable": true
      }
     }
    }
   },
   "billingDetails": {
    "type": "object",
    "nullable": true,
    "properties": {
     "billingName": {
      "type": "string",
      "maxLength": 200
     },
     "billingEmail": {
      "type": "string",
      "format": "email",
      "nullable": true
     },
     "address": {
      "type": "string",
      "maxLength": 500,
      "nullable": true
     }
    }
   },
   "taxDetails": {
    "type": "object",
    "nullable": true,
    "properties": {
     "taxRegistrationNumber": {
      "type": "string",
      "maxLength": 50,
      "nullable": true
     },
     "taxCountry": {
      "type": "string",
      "pattern": "^[A-Z]{2}$",
      "nullable": true
     }
    }
   }
  }
 },
 "GroupCustomerOrganizationProfileView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over orders state, assembled at read time from tables that already exist",
  "description": "**What Group Customer & Organization Profile displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "organizationName": {
    "type": "string",
    "description": "Organization Name"
   },
   "customerId": {
    "type": "string",
    "description": "Customer ID"
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
   },
   "registrationDetails": {
    "type": "string",
    "description": "Registration Details where applicable"
   },
   "organizationType": {
    "type": "string",
    "enum": [
     "school",
     "university",
     "company",
     "government",
     "sportsClub",
     "association",
     "tourGroup",
     "privateGroup",
     "eventOrganizer",
     "charity"
    ],
    "description": "Organisation type (configurable; MoM 31 Aug)."
   }
  }
 },
 "GroupCustomerOrganizationView": {
  "type": "object",
  "x-ticvai-persistence": "orders.group_customer_organization + orders.group_customer_organization_contact",
  "description": "**The organisation a group buys under.** Saved by `setGroupCustomerOrganization` (decided 29 September, readiness close-out); `listGroupCustomerOrganization` is the screen's projection over these.\n",
  "required": [
   "id",
   "name",
   "organisationType"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "name": {
    "type": "string",
    "maxLength": 200
   },
   "organisationType": {
    "type": "string",
    "enum": [
     "school",
     "corporate",
     "travelAgent",
     "eventOrganizer",
     "association",
     "government",
     "other"
    ]
   },
   "contacts": {
    "type": "array",
    "items": {
     "type": "object",
     "required": [
      "role",
      "name"
     ],
     "properties": {
      "role": {
       "type": "string",
       "enum": [
        "primary",
        "booking",
        "finance",
        "eventDay",
        "decisionMaker"
       ]
      },
      "name": {
       "type": "string",
       "maxLength": 120
      },
      "email": {
       "type": "string",
       "format": "email",
       "nullable": true
      },
      "phone": {
       "type": "string",
       "maxLength": 30,
       "nullable": true
      }
     }
    }
   },
   "billingDetails": {
    "type": "object",
    "nullable": true,
    "properties": {
     "billingName": {
      "type": "string",
      "maxLength": 200
     },
     "billingEmail": {
      "type": "string",
      "format": "email",
      "nullable": true
     },
     "address": {
      "type": "string",
      "maxLength": 500,
      "nullable": true
     }
    }
   },
   "taxDetails": {
    "type": "object",
    "nullable": true,
    "properties": {
     "taxRegistrationNumber": {
      "type": "string",
      "maxLength": 50,
      "nullable": true
     },
     "taxCountry": {
      "type": "string",
      "pattern": "^[A-Z]{2}$",
      "nullable": true
     }
    }
   },
   "updatedAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   }
  }
 },
 "GroupDiscountExceptionApprovalWorkflowInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; the decision lands in the discount columns of `orders.group_quote` (DM5, 29 September)",
  "description": "**What Group Discount, Exception & Approval Workflow submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
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
   },
   "decision": {
    "type": "string",
    "enum": [
     "approve",
     "reject",
     "returnForChange"
    ],
    "description": "Approver decision"
   },
   "comment": {
    "type": "string",
    "description": "Comment"
   }
  }
 },
 "GroupDiscountExceptionApprovalWorkflowView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over orders state, assembled at read time from tables that already exist",
  "description": "**What Group Discount, Exception & Approval Workflow displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
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
   },
   "decision": {
    "type": "string",
    "enum": [
     "approve",
     "reject",
     "returnForChange"
    ],
    "description": "Approver decision"
   }
  }
 },
 "GroupEnquiryInput": {
  "type": "object",
  "x-ticvai-persistence": "none — request only",
  "description": "What `createGroupEnquiry` takes (decided 29 September, readiness close-out).",
  "required": [
   "source",
   "contact",
   "groupSize"
  ],
  "properties": {
   "source": {
    "type": "string",
    "description": "Where the enquiry came from (decided 29 September, readiness close-out).",
    "enum": [
     "website",
     "salesTeam",
     "campaign",
     "existingCustomer",
     "partner",
     "manualEntry"
    ]
   },
   "organisationId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "An organisation already on file; null when the enquirer is not yet one."
   },
   "contact": {
    "type": "object",
    "required": [
     "name"
    ],
    "properties": {
     "name": {
      "type": "string",
      "maxLength": 120
     },
     "email": {
      "type": "string",
      "format": "email",
      "nullable": true
     },
     "phone": {
      "type": "string",
      "maxLength": 30,
      "nullable": true
     },
     "organisationName": {
      "type": "string",
      "maxLength": 200,
      "nullable": true,
      "description": "Who they are, when `organisationId` is null."
     }
    }
   },
   "groupSize": {
    "type": "integer",
    "minimum": 1
   },
   "preferredDates": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "date"
    }
   },
   "requirements": {
    "type": "string",
    "maxLength": 2000,
    "nullable": true
   },
   "salesOwnerPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The opportunity's owner. **An enquiry is the opportunity** (DM5, 29 September); the pipeline fields live on it rather than on a second table that would copy it."
   },
   "priority": {
    "type": "string",
    "nullable": true,
    "enum": [
     "low",
     "normal",
     "high"
    ]
   },
   "expectedValue": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "nullable": true
   },
   "probability": {
    "type": "integer",
    "nullable": true,
    "minimum": 0,
    "maximum": 100,
    "description": "Percent."
   },
   "expectedCloseDate": {
    "type": "string",
    "format": "date",
    "nullable": true
   },
   "nextActionAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   }
  }
 },
 "GroupEnquiryOpportunityCaptureView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over orders state, assembled at read time from tables that already exist",
  "description": "**What Group Enquiry & Opportunity Capture displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
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
   "nextAction": {
    "type": "string",
    "format": "date-time",
    "description": "Next Action"
   },
   "leadSource": {
    "type": "string",
    "enum": [
     "website",
     "phone",
     "email",
     "walkIn",
     "salesTeam",
     "crm",
     "referral",
     "campaign",
     "existingCustomer",
     "manualEntry"
    ],
    "description": "Where the enquiry came from."
   }
  }
 },
 "GroupEnquiryOpportunityView": {
  "type": "object",
  "x-ticvai-persistence": "orders.group_enquiry",
  "description": "**One captured group enquiry.** Written by `createGroupEnquiry` (decided 29 September, readiness close-out); `listGroupEnquiryOpportunity` is the screen's projection over these.\n",
  "required": [
   "id",
   "source",
   "contact",
   "groupSize",
   "createdAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "source": {
    "type": "string",
    "enum": [
     "website",
     "salesTeam",
     "campaign",
     "existingCustomer",
     "partner",
     "manualEntry"
    ]
   },
   "organisationId": {
    "x-ticvai-references": "orders.group_customer_organization",
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "contact": {
    "type": "object",
    "properties": {
     "name": {
      "type": "string",
      "maxLength": 120
     },
     "email": {
      "type": "string",
      "format": "email",
      "nullable": true
     },
     "phone": {
      "type": "string",
      "maxLength": 30,
      "nullable": true
     },
     "organisationName": {
      "type": "string",
      "maxLength": 200,
      "nullable": true
     }
    }
   },
   "groupSize": {
    "type": "integer",
    "minimum": 1
   },
   "preferredDates": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "date"
    }
   },
   "requirements": {
    "type": "string",
    "maxLength": 2000,
    "nullable": true
   },
   "salesOwnerPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The opportunity's owner. **An enquiry is the opportunity** (DM5, 29 September); the pipeline fields live on it rather than on a second table that would copy it."
   },
   "priority": {
    "type": "string",
    "nullable": true,
    "enum": [
     "low",
     "normal",
     "high"
    ]
   },
   "expectedValue": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "nullable": true
   },
   "probability": {
    "type": "integer",
    "nullable": true,
    "minimum": 0,
    "maximum": 100,
    "description": "Percent."
   },
   "expectedCloseDate": {
    "type": "string",
    "format": "date",
    "nullable": true
   },
   "nextActionAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "createdBy": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "createdAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   }
  }
 },
 "GroupPackageExperienceBuilderInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; lands in the package columns of `orders.group_quote` (DM5, 29 September)",
  "description": "**What Group Package & Experience Builder submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "componentTypes": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "admissionTickets",
      "groupTicket",
      "guidedTour",
      "reservedSeating",
      "fB",
      "mealVoucher",
      "merchandise",
      "transportation",
      "parking",
      "workshop",
      "educationProgram",
      "meetingRoom",
      "vipExperience",
      "addOns",
      "rentalResources",
      "educationalWorkshop"
     ]
    },
    "description": "What the package combines."
   },
   "template": {
    "type": "string",
    "enum": [
     "schoolPackage",
     "corporatePackage",
     "birthdayPackage",
     "vipGroupPackage",
     "conferencePackage"
    ],
    "description": "Reusable package template."
   },
   "packageName": {
    "type": "string",
    "description": "Package name"
   },
   "guestCount": {
    "type": "integer",
    "description": "Guests"
   },
   "components": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Products and services in the package"
   }
  }
 },
 "GroupPackageExperienceBuilderView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over orders state, assembled at read time from tables that already exist",
  "description": "**What Group Package & Experience Builder displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
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
   "componentTypes": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "admissionTickets",
      "groupTicket",
      "guidedTour",
      "reservedSeating",
      "fB",
      "mealVoucher",
      "merchandise",
      "transportation",
      "parking",
      "workshop",
      "educationProgram",
      "meetingRoom",
      "vipExperience",
      "addOns",
      "rentalResources",
      "educationalWorkshop"
     ]
    },
    "description": "What the package combines."
   },
   "template": {
    "type": "string",
    "enum": [
     "schoolPackage",
     "corporatePackage",
     "birthdayPackage",
     "vipGroupPackage",
     "conferencePackage"
    ],
    "description": "Reusable package template."
   },
   "packageName": {
    "type": "string",
    "description": "Package name"
   },
   "guestCount": {
    "type": "integer",
    "description": "Guests"
   },
   "components": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Products and services in the package"
   }
  }
 },
 "GroupQuotationBuilderProposalGenerationInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; lands in `orders.group_quote` and its `orders.group_quote_line` rows (DM5, 29 September)",
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
   "deliveryFormats": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "email",
      "pdf",
      "secureDigitalLink",
      "customerPortal"
     ]
    },
    "description": "How the proposal is delivered."
   },
   "lines": {
    "type": "array",
    "description": "Quote lines",
    "items": {
     "type": "object",
     "properties": {
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
       "$ref": "../shared/common.yaml#/components/schemas/Money",
       "description": "Standard rate"
      },
      "groupRate": {
       "$ref": "../shared/common.yaml#/components/schemas/Money",
       "description": "Group rate"
      },
      "discount": {
       "$ref": "../shared/common.yaml#/components/schemas/Money",
       "description": "Discount"
      },
      "tax": {
       "$ref": "../shared/common.yaml#/components/schemas/Money",
       "description": "Tax"
      },
      "fee": {
       "$ref": "../shared/common.yaml#/components/schemas/Money",
       "description": "Fee"
      },
      "total": {
       "$ref": "../shared/common.yaml#/components/schemas/Money",
       "description": "Total"
      }
     }
    }
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
   "deliveryFormats": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "email",
      "pdf",
      "secureDigitalLink",
      "customerPortal"
     ]
    },
    "description": "How the proposal is delivered."
   },
   "lines": {
    "type": "array",
    "description": "Quote lines",
    "items": {
     "type": "object",
     "properties": {
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
       "$ref": "../shared/common.yaml#/components/schemas/Money",
       "description": "Standard rate"
      },
      "groupRate": {
       "$ref": "../shared/common.yaml#/components/schemas/Money",
       "description": "Group rate"
      },
      "discount": {
       "$ref": "../shared/common.yaml#/components/schemas/Money",
       "description": "Discount"
      },
      "tax": {
       "$ref": "../shared/common.yaml#/components/schemas/Money",
       "description": "Tax"
      },
      "fee": {
       "$ref": "../shared/common.yaml#/components/schemas/Money",
       "description": "Fee"
      },
      "total": {
       "$ref": "../shared/common.yaml#/components/schemas/Money",
       "description": "Total"
      }
     }
    }
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
   "cateringCapacity": {
    "type": "integer",
    "description": "Catering capacity"
   },
   "resourceChecks": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "rooms",
      "equipment",
      "vehicles",
      "meetingSpaces"
     ]
    },
    "description": "Resource Management checks run for the request."
   }
  }
 },
 "GroupSalesAnalyticsAiIntelligenceCenterView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over orders state, assembled at read time from tables that already exist",
  "description": "**What Group Sales Analytics & AI Intelligence Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "enquiries": {
    "type": "string",
    "description": "Enquiries"
   },
   "quotes": {
    "type": "string",
    "description": "Quotes"
   },
   "conversionRate": {
    "type": "number",
    "description": "Conversion Rate"
   },
   "groupBookings": {
    "type": "string",
    "description": "Group Bookings"
   },
   "guests": {
    "type": "string",
    "description": "Guests"
   },
   "revenue": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Revenue"
   },
   "averageGroupSize": {
    "type": "number",
    "description": "Average Group Size"
   },
   "averageBookingValue": {
    "type": "number",
    "description": "Average Booking Value"
   },
   "discount": {
    "type": "number",
    "description": "Discount %"
   },
   "revenuePerGuest": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Revenue per Guest"
   },
   "cancellationRate": {
    "type": "number",
    "description": "Cancellation Rate"
   },
   "noShowRate": {
    "type": "number",
    "description": "No-Show Rate"
   },
   "outstandingReceivables": {
    "type": "string",
    "description": "Outstanding Receivables"
   },
   "repeatCustomerRate": {
    "type": "number",
    "description": "Repeat Customer Rate"
   },
   "additionalGroups": {
    "type": "string",
    "description": "Additional groups"
   },
   "capacityUtilization": {
    "type": "integer",
    "description": "Capacity utilization"
   },
   "discountCost": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Discount cost"
   },
   "expectedContribution": {
    "type": "string",
    "description": "Expected contribution"
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
   },
   "quoteNumber": {
    "type": "string",
    "description": "Quote number"
   },
   "version": {
    "type": "integer",
    "description": "Version"
   },
   "versionStatus": {
    "type": "string",
    "enum": [
     "draft",
     "sent",
     "superseded",
     "accepted",
     "rejected"
    ],
    "description": "Version status"
   }
  }
 },
 "QuoteToBookingConversionConfirmationView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over orders state, assembled at read time from tables that already exist",
  "description": "**What Quote-to-Booking Conversion & Confirmation displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "groupBookingId": {
    "type": "string",
    "description": "Group Booking ID"
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
   "nextSteps": {
    "type": "string",
    "format": "date-time",
    "description": "Next Steps"
   },
   "orderId": {
    "type": "string",
    "description": "TICVAI Order"
   },
   "customerPortalLink": {
    "type": "string",
    "description": "Customer Portal Link where applicable"
   },
   "failedChecks": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "quoteExpired",
      "capacityUnavailable",
      "resourcesUnavailable",
      "priceNotApproved",
      "approvalInvalid",
      "customerDetailsIncomplete",
      "depositRuleMissing",
      "guestCountInvalid"
     ]
    },
    "description": "Conversion checks that fail; empty means the quote converts."
   }
  }
 },
 "UpdateGroupBookingRequest": {
  "type": "object",
  "description": "Request only. Every field optional; absent means unchanged.",
  "properties": {
   "packageProductId": {
    "type": "string",
    "nullable": true,
    "description": "The school-trip format or party package."
   },
   "yearGroup": {
    "type": "string",
    "maxLength": 40,
    "nullable": true
   },
   "accessAndDietaryNeeds": {
    "type": "string",
    "maxLength": 1000,
    "nullable": true
   },
   "celebrantName": {
    "type": "string",
    "maxLength": 120,
    "nullable": true,
    "description": "The birthday child."
   },
   "celebrantTurningAge": {
    "type": "integer",
    "minimum": 1,
    "maximum": 18,
    "nullable": true
   },
   "allergiesAndRequests": {
    "type": "string",
    "maxLength": 1000,
    "nullable": true
   },
   "finalHeadcountDueBy": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "leaderSubjectId": {
    "type": "string",
    "format": "uuid"
   },
   "organisationName": {
    "type": "string",
    "maxLength": 200,
    "nullable": true
   },
   "expectedSize": {
    "type": "integer",
    "minimum": 2
   },
   "confirmedSize": {
    "type": "integer",
    "minimum": 0
   },
   "minimumSize": {
    "type": "integer",
    "minimum": 1,
    "nullable": true
   },
   "attendeeCaptureRequired": {
    "type": "boolean"
   },
   "attendeeCaptureDueBy": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "status": {
    "type": "string",
    "enum": [
     "confirmed",
     "namesPending",
     "complete",
     "cancelled"
    ]
   }
  }
 }
}
```
