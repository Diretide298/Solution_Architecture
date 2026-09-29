# WS61 — Ticket Media   Credential Management board 3

**10 screens · 16 operations · 17 schemas · 7 permissions**

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

- **Every control that can be refused must be gated.** 7 permissions apply here:
  `ACCESS_POINT_CONFIGURE, AUDIT_VIEW, ORDER_EXCHANGE, ORDER_REPRINT, REPORT_VIEW_VENUE, SCOPE_VIEW, TICKET_LOOKUP`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `BO-354` | Credential Operations Command Center | commandCentre | 1 | 0 | — |
| `BO-355` | Virtual Ticket & Credential 360° Workspace | commandCentre | 1 | 0 | — |
| `BO-356` | Credential Generation & Issuance Monitor | listDetail | 5 | 0 | — |
| `BO-357` | Credential Delivery & Distribution Operations | listDetail | 2 | 0 | — |
| `BO-358` | Media Binding, Activation & Assignment Operations | listDetail | 1 | 0 | — |
| `BO-359` | Credential Replacement, Reissue, Revocation & Recovery | configEditor | 2 | 0 | — |
| `BO-360` | Failed Generation, Delivery & Credential Exception Management | listDetail | 2 | 0 | — |
| `BO-361` | Credential Usage & Cross-Media Traceability | configEditor | 1 | 0 | — |
| `BO-362` | Credential Security, Audit & Operational Evidence | listDetail | 1 | 0 | — |
| `BO-363` | Ticket Media Analytics & AI Operations Intelligence | listDetail | 1 | 0 | — |

## Thin screens in this batch

**BO-362 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "BO-354",
  "name": "Credential Operations Command Center",
  "module": "Access & Venue",
  "requiresModule": "access",
  "wave": 3,
  "source": {
   "pack": "Ticket_Media___Credential_Management_Reference.pdf",
   "board": "3",
   "number": "15.3.1",
   "page": 41
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/credential-operations-command-center-bo-354",
   "component": "apps/venue-management-web/src/routes/access-venue/CredentialOperationsCommandCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-100"
   ],
   "exitTo": [
    "BO-100",
    "BO-355",
    "BO-356",
    "BO-357",
    "BO-358",
    "BO-359",
    "BO-360",
    "BO-361",
    "BO-362",
    "BO-363"
   ],
   "inferred": false,
   "notes": "**The board's hub.** The workshop specified this module as boards of ten and opened each with a command centre; the other nine screens are that board's detail, so they are reached from here and return here.",
   "transitions": [
    {
     "to": "BO-100",
     "trigger": "Venue Home",
     "provenance": "derived — BO-100 declares entryState.params  and BO-354 holds none of them, so the edge carries nothing and BO-100 opens cold"
    },
    {
     "to": "BO-355",
     "trigger": "Works in Virtual Ticket & Credential 360° Workspace",
     "provenance": "flow F170 step 1→2",
     "operation": "listCredential"
    },
    {
     "to": "BO-356",
     "trigger": "Works in Credential Generation & Issuance Monitor",
     "provenance": "flow F170 step 3→4",
     "operation": "listCredential"
    },
    {
     "to": "BO-358",
     "trigger": "Works in Media Binding, Activation & Assignment Operations",
     "provenance": "flow F170 step 7→8",
     "operation": "listCredential"
    },
    {
     "to": "BO-360",
     "trigger": "Works in Failed Generation, Delivery & Credential Exception Management",
     "provenance": "flow F170 step 11→12",
     "operation": "listCredential"
    },
    {
     "to": "BO-361",
     "trigger": "Works in Credential Usage & Cross-Media Traceability",
     "provenance": "flow F170 step 13→14",
     "operation": "listCredential"
    },
    {
     "to": "BO-362",
     "trigger": "Works in Credential Security, Audit & Operational Evidence",
     "provenance": "flow F170 step 15→16",
     "operation": "listCredential"
    },
    {
     "to": "BO-363",
     "trigger": "Works in Ticket Media Analytics & AI Operations Intelligence",
     "provenance": "flow F170 step 17→18",
     "operation": "listCredential"
    },
    {
     "to": "BO-357",
     "trigger": "Works in Credential Delivery & Distribution Operations",
     "provenance": "flow F170 step 5→6",
     "operation": "listCredential",
     "carries": [
      "credentialId"
     ]
    },
    {
     "to": "BO-359",
     "trigger": "Works in Credential Replacement, Reissue, Revocation & Recovery",
     "provenance": "flow F170 step 9→10",
     "operation": "listCredential",
     "carries": [
      "credentialId"
     ]
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Operations can understand the health, status and exceptions of all issued credentials from one central workspace.",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen both a metric directory (§Display) and a per-row directory (§Each record should show) — counts over a population, then the population",
  "purpose": "Provide Operations, Ticketing, Customer Service and Technical teams with a real-time command center covering all issued credential media. This is the operational starting point for Area 15.",
  "layout": {
   "template": "dashboard",
   "regions": [
    {
     "name": "contentBody",
     "slot": "filters",
     "components": [
      {
       "kind": "searchField",
       "label": "Search credential operations",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 41 §Filter by"
      },
      {
       "kind": "multiSelect",
       "label": "Filter by",
       "columns": [
        "Brand",
        "Venue",
        "CredentialOperationsCommandCenterView.event",
        "CredentialOperationsCommandCenterView.product",
        "Date",
        "Media",
        "CredentialOperationsCommandCenterView.provider",
        "Status",
        "Channel",
        "CredentialOperationsCommandCenterView.exception",
        "Customer"
       ],
       "notes": "The pack filters this screen by brand, venue, event, product, date, media and 5 more — which are present is a decision the pack already made.",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 41 §Filter by"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "Virtual Tickets Issued",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 41 §Display",
       "bindsTo": "CredentialOperationsCommandCenterViewSummary.virtualTicketsIssued"
      },
      {
       "kind": "metricTile",
       "label": "Credentials Generated",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 41 §Display",
       "bindsTo": "CredentialOperationsCommandCenterViewSummary.credentialsGenerated"
      },
      {
       "kind": "metricTile",
       "label": "Active Credentials",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 41 §Display",
       "bindsTo": "CredentialOperationsCommandCenterViewSummary.activeCredentials"
      },
      {
       "kind": "metricTile",
       "label": "Pending Generation",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 41 §Display",
       "bindsTo": "CredentialOperationsCommandCenterViewSummary.pendingGeneration"
      },
      {
       "kind": "metricTile",
       "label": "Pending Delivery",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 41 §Display",
       "bindsTo": "CredentialOperationsCommandCenterViewSummary.pendingDelivery"
      },
      {
       "kind": "metricTile",
       "label": "Pending Binding",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 41 §Display",
       "bindsTo": "CredentialOperationsCommandCenterViewSummary.pendingBinding"
      },
      {
       "kind": "metricTile",
       "label": "Pending Activation",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 41 §Display",
       "bindsTo": "CredentialOperationsCommandCenterViewSummary.pendingActivation"
      },
      {
       "kind": "metricTile",
       "label": "Suspended",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 41 §Display",
       "bindsTo": "CredentialOperationsCommandCenterViewSummary.suspended"
      },
      {
       "kind": "metricTile",
       "label": "Revoked",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 41 §Display",
       "bindsTo": "CredentialOperationsCommandCenterViewSummary.revoked"
      },
      {
       "kind": "metricTile",
       "label": "Expired",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 41 §Display",
       "bindsTo": "CredentialOperationsCommandCenterViewSummary.expired"
      },
      {
       "kind": "metricTile",
       "label": "Failed Generation",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 41 §Display",
       "bindsTo": "CredentialOperationsCommandCenterViewSummary.failedGeneration"
      },
      {
       "kind": "metricTile",
       "label": "Failed Delivery",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 41 §Display",
       "bindsTo": "CredentialOperationsCommandCenterViewSummary.failedDelivery"
      },
      {
       "kind": "metricTile",
       "label": "Synchronization Exceptions",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 41 §Display",
       "bindsTo": "CredentialOperationsCommandCenterViewSummary.synchronizationExceptions"
      },
      {
       "kind": "metricTile",
       "label": "Multi-Media Virtual Tickets",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 41 §Display",
       "bindsTo": "CredentialOperationsCommandCenterViewSummary.multiMediaVirtualTickets"
      },
      {
       "kind": "metricTile",
       "label": "Virtual Tickets Without Active Media",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 41 §Display"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "moduleTiles",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every credential operations",
       "columns": [
        "CredentialOperationsCommandCenterView.virtualTicketId",
        "CredentialOperationsCommandCenterView.credentialId",
        "CredentialOperationsCommandCenterView.mediaType",
        "CredentialOperationsCommandCenterView.customerParticipant",
        "CredentialOperationsCommandCenterView.product",
        "CredentialOperationsCommandCenterView.event",
        "CredentialOperationsCommandCenterView.credentialStatus",
        "CredentialOperationsCommandCenterView.deliveryStatus",
        "CredentialOperationsCommandCenterView.activationStatus",
        "CredentialOperationsCommandCenterView.bindingStatus",
        "CredentialOperationsCommandCenterView.provider",
        "CredentialOperationsCommandCenterView.lastActivity",
        "CredentialOperationsCommandCenterView.exception",
        "CredentialOperationsCommandCenterView.owner"
       ],
       "bindsTo": "CredentialOperationsCommandCenterView",
       "operation": "listCredential",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 41 §Each record should show"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected credential operations",
       "bindsTo": "CredentialOperationsCommandCenterView",
       "columns": [
        "CredentialOperationsCommandCenterView.virtualTicketId",
        "CredentialOperationsCommandCenterView.credentialId",
        "CredentialOperationsCommandCenterView.mediaType",
        "CredentialOperationsCommandCenterView.customerParticipant",
        "CredentialOperationsCommandCenterView.product",
        "CredentialOperationsCommandCenterView.event",
        "CredentialOperationsCommandCenterView.credentialStatus",
        "CredentialOperationsCommandCenterView.deliveryStatus",
        "CredentialOperationsCommandCenterView.activationStatus",
        "CredentialOperationsCommandCenterView.bindingStatus",
        "CredentialOperationsCommandCenterView.provider",
        "CredentialOperationsCommandCenterView.lastActivity",
        "CredentialOperationsCommandCenterView.exception",
        "CredentialOperationsCommandCenterView.owner"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Display credentials by”, “Provide indicators such as”.",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 41 §Each record should show"
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
       "notes": "**The pack separates these permissions and no action on the screen claims them yet:** Open Virtual Ticket, Generate Credential, Resend, Activate, Suspend Media, Replace, Revoke, Diagnose, View History. Each needs attaching to the control it gates, or the screen needs the control.",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 41 §Authorized users can"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The credential operations list; the counts above it resolve separately.",
   "error": "Could not load. Names which read failed and leaves the credential operations untouched.",
   "emptyFirstRun": "No credential operations yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the credential operations are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listCredential",
    "contract": "access",
    "purpose": "Credential Operations Command Center",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-354",
   "workshopBoard": "wireframes/WS167 Ticket Media   Credential Management Board 3.dc.html#bo-354"
  },
  "apisNote": "Regenerated 9 September 2026 from Ticket_Media___Credential_Management_Reference.pdf page 41. 32 of 39 labels bound to a contract property; 49 of 72 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-355",
  "name": "Virtual Ticket & Credential 360° Workspace",
  "module": "Access & Venue",
  "requiresModule": "access",
  "wave": 3,
  "source": {
   "pack": "Ticket_Media___Credential_Management_Reference.pdf",
   "board": "3",
   "number": "15.3.2",
   "page": 43
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/virtual-ticket-credential-360-workspace-bo-355",
   "component": "apps/venue-management-web/src/routes/access-venue/VirtualTicketCredential360Workspace.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-354"
   ],
   "exitTo": [
    "BO-354"
   ],
   "inferred": false,
   "notes": "**Reached from BO-354, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-354",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F170 step 2→3",
     "operation": "setVirtualTicketCredential"
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Staff can view and manage the complete multi-media credential history of a Virtual Ticket without treating each credential as a separate ticket.",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen both a metric directory (§Display; Identify) and a per-row directory (§For each media show) — counts over a population, then the population",
  "purpose": "Provide a complete operational view of one Virtual Ticket and every media credential currently or historically associated with it. This is one of the most important operational screens.",
  "layout": {
   "template": "dashboard",
   "regions": [
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "Virtual Ticket ID",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 43 §Display",
       "bindsTo": "VirtualTicketCredential360WorkspaceView.virtualTicketId"
      },
      {
       "kind": "metricTile",
       "label": "Ticket Holder",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 43 §Display",
       "bindsTo": "VirtualTicketCredential360WorkspaceView.ticketHolder"
      },
      {
       "kind": "metricTile",
       "label": "Participant",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 43 §Display",
       "bindsTo": "VirtualTicketCredential360WorkspaceView.participant"
      },
      {
       "kind": "metricTile",
       "label": "Product",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 43 §Display",
       "bindsTo": "VirtualTicketCredential360WorkspaceView.product"
      },
      {
       "kind": "metricTile",
       "label": "Event",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 43 §Display",
       "bindsTo": "VirtualTicketCredential360WorkspaceView.event"
      },
      {
       "kind": "metricTile",
       "label": "Performance",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 43 §Display",
       "bindsTo": "VirtualTicketCredential360WorkspaceView.performance"
      },
      {
       "kind": "metricTile",
       "label": "Venue",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 43 §Display",
       "bindsTo": "VirtualTicketCredential360WorkspaceView.venue"
      },
      {
       "kind": "metricTile",
       "label": "Seat",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 43 §Display",
       "bindsTo": "VirtualTicketCredential360WorkspaceView.seat"
      },
      {
       "kind": "metricTile",
       "label": "Order",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 43 §Display",
       "bindsTo": "VirtualTicketCredential360WorkspaceView.order"
      },
      {
       "kind": "metricTile",
       "label": "Ticket Status",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 43 §Display",
       "bindsTo": "VirtualTicketCredential360WorkspaceView.ticketStatus"
      },
      {
       "kind": "metricTile",
       "label": "Usage Status",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 43 §Display",
       "bindsTo": "VirtualTicketCredential360WorkspaceView.usageStatus"
      },
      {
       "kind": "metricTile",
       "label": "Validity",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 43 §Display",
       "bindsTo": "VirtualTicketCredential360WorkspaceView.validity"
      },
      {
       "kind": "metricTile",
       "label": "Entitlements",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 43 §Display",
       "bindsTo": "VirtualTicketCredential360WorkspaceView.entitlements"
      },
      {
       "kind": "metricTile",
       "label": "Primary",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 43 §Identify",
       "bindsTo": "VirtualTicketCredential360WorkspaceView.mediaRole"
      },
      {
       "kind": "metricTile",
       "label": "Secondary",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 43 §Identify",
       "bindsTo": "VirtualTicketCredential360WorkspaceView.mediaRole"
      },
      {
       "kind": "metricTile",
       "label": "Fallback",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 43 §Identify",
       "bindsTo": "VirtualTicketCredential360WorkspaceView.mediaRole"
      },
      {
       "kind": "metricTile",
       "label": "Temporary",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 43 §Identify",
       "bindsTo": "VirtualTicketCredential360WorkspaceView.mediaRole"
      },
      {
       "kind": "metricTile",
       "label": "Revoked historical media",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 43 §Identify",
       "bindsTo": "VirtualTicketCredential360WorkspaceView.mediaRole"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "moduleTiles",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every virtual ticket credential",
       "columns": [
        "VirtualTicketCredential360WorkspaceView.bindingId",
        "VirtualTicketCredential360WorkspaceView.mediaType",
        "VirtualTicketCredential360WorkspaceView.provider",
        "VirtualTicketCredential360WorkspaceView.issued",
        "VirtualTicketCredential360WorkspaceView.delivered",
        "VirtualTicketCredential360WorkspaceView.activated",
        "Valid From/To",
        "VirtualTicketCredential360WorkspaceView.lastUpdate",
        "Last presentation/use",
        "VirtualTicketCredential360WorkspaceView.deviceReferenceWhereAppropriate",
        "VirtualTicketCredential360WorkspaceView.status"
       ],
       "bindsTo": "VirtualTicketCredential360WorkspaceView",
       "operation": "setVirtualTicketCredential",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 43 §For each media show"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected virtual ticket credential",
       "bindsTo": "VirtualTicketCredential360WorkspaceView",
       "columns": [
        "VirtualTicketCredential360WorkspaceView.bindingId",
        "VirtualTicketCredential360WorkspaceView.mediaType",
        "VirtualTicketCredential360WorkspaceView.provider",
        "VirtualTicketCredential360WorkspaceView.issued",
        "VirtualTicketCredential360WorkspaceView.delivered",
        "VirtualTicketCredential360WorkspaceView.activated",
        "Valid From/To",
        "VirtualTicketCredential360WorkspaceView.lastUpdate",
        "Last presentation/use",
        "VirtualTicketCredential360WorkspaceView.deviceReferenceWhereAppropriate",
        "VirtualTicketCredential360WorkspaceView.status"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Credential Wallet”, “Media Status”, “Dynamic QR Active”, “Apple Wallet Active”, “Old RFID RF-88410”, “Provide one chronological timeline”.",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 43 §For each media show"
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
       "provenance": "contract operation setVirtualTicketCredential"
      },
      {
       "kind": "banner",
       "label": "Permissions this screen separates",
       "notes": "**The pack separates these permissions and no action on the screen claims them yet:** Generate Additional Media, Bind RFID, Add Wallet Pass, Initiate Face Enrollment, Replace Media, Suspend, Revoke, Resend, Refresh, Diagnose. Each needs attaching to the control it gates, or the screen needs the control.",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 43 §Depending on permission"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The virtual ticket credential list; the counts above it resolve separately.",
   "error": "Could not load. Names which read failed and leaves the virtual ticket credential untouched.",
   "emptyFirstRun": "No virtual ticket credential yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the virtual ticket credential are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setVirtualTicketCredential",
    "contract": "access",
    "purpose": "Virtual Ticket & Credential 360° Workspace",
    "trigger": "onAction"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-355",
   "workshopBoard": "wireframes/WS167 Ticket Media   Credential Management Board 3.dc.html#bo-355"
  },
  "apisNote": "Regenerated 9 September 2026 from Ticket_Media___Credential_Management_Reference.pdf page 43. 27 of 29 labels bound to a contract property; 39 of 53 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-356",
  "name": "Credential Generation & Issuance Monitor",
  "module": "Access & Venue",
  "requiresModule": "access",
  "wave": 3,
  "source": {
   "pack": "Ticket_Media___Credential_Management_Reference.pdf",
   "board": "3",
   "number": "15.3.3",
   "page": 45
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/credential-generation-issuance-monitor-bo-356",
   "component": "apps/venue-management-web/src/routes/access-venue/CredentialGenerationIssuanceMonitor.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-354"
   ],
   "exitTo": [
    "BO-354"
   ],
   "inferred": false,
   "notes": "**Reached from BO-354, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-354",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F170 step 4→5",
     "operation": "listCredentialGenerationIssuance"
    }
   ]
  },
  "density": "compact",
  "purposeNote": "operational visibility into successful and failed issuance.",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Show; Display) and no metric row",
  "purpose": "Manage and monitor generation of credential instances from approved Board 2 media templates.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every credential generation issuance",
       "columns": [
        "→ Bound → Ready → Delivered",
        "CredentialGenerationIssuanceMonitorView.requestId",
        "CredentialGenerationIssuanceMonitorView.virtualTicket",
        "CredentialGenerationIssuanceMonitorView.media",
        "CredentialGenerationIssuanceMonitorView.template",
        "CredentialGenerationIssuanceMonitorView.templateVersion",
        "CredentialGenerationIssuanceMonitorView.product",
        "CredentialGenerationIssuanceMonitorView.customer",
        "Trigger",
        "CredentialGenerationIssuanceMonitorView.provider",
        "CredentialGenerationIssuanceMonitorView.requestedAt",
        "CredentialGenerationIssuanceMonitorView.generatedAt",
        "CredentialGenerationIssuanceMonitorView.status",
        "CredentialGenerationIssuanceMonitorView.error"
       ],
       "bindsTo": "CredentialGenerationIssuanceMonitorView",
       "operation": "listCredentialGenerationIssuance",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 45 §Show"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected credential generation issuance",
       "bindsTo": "CredentialGenerationIssuanceMonitorView",
       "columns": [
        "→ Bound → Ready → Delivered",
        "CredentialGenerationIssuanceMonitorView.requestId",
        "CredentialGenerationIssuanceMonitorView.virtualTicket",
        "CredentialGenerationIssuanceMonitorView.media",
        "CredentialGenerationIssuanceMonitorView.template",
        "CredentialGenerationIssuanceMonitorView.templateVersion",
        "CredentialGenerationIssuanceMonitorView.product",
        "CredentialGenerationIssuanceMonitorView.customer",
        "Trigger",
        "CredentialGenerationIssuanceMonitorView.provider",
        "CredentialGenerationIssuanceMonitorView.requestedAt",
        "CredentialGenerationIssuanceMonitorView.generatedAt",
        "CredentialGenerationIssuanceMonitorView.status",
        "CredentialGenerationIssuanceMonitorView.error"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Generation Sources”, “Template Resolution”, “Bulk Generation”, “Failures may include”.",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 45 §Show"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Automatic Retry",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 45 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Manual Retry",
       "operation": "retryCredentialGeneration",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 45 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Retry Selected",
       "operation": "retryCredentialGeneration",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 45 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Retry All Eligible",
       "operation": "retryCredentialGeneration",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 45 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Escalate",
       "operation": "resolveCredentialException",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 45 §Support"
      },
      {
       "kind": "primaryButton",
       "label": "Save retry policy",
       "operation": "setCredentialIssuanceRetryPolicy",
       "provenance": "contract access.yaml PUT /credential-issuance-retry-policy (decided 29 September, VM close-out)"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The credential generation issuance list.",
   "error": "Could not load. Names which read failed and leaves the credential generation issuance untouched.",
   "emptyFirstRun": "No credential generation issuance yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the credential generation issuance are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listCredentialGenerationIssuance",
    "contract": "access",
    "purpose": "Credential Generation & Issuance Monitor",
    "trigger": "onLoad"
   },
   {
    "operationId": "getCredentialIssuanceRetryPolicy",
    "contract": "access",
    "purpose": "The retry policy the monitor applies",
    "trigger": "onLoad"
   },
   {
    "operationId": "setCredentialIssuanceRetryPolicy",
    "contract": "access",
    "purpose": "Save retry policy",
    "trigger": "onAction"
   },
   {
    "operationId": "retryCredentialGeneration",
    "contract": "access",
    "purpose": "Retry",
    "trigger": "onAction"
   },
   {
    "operationId": "resolveCredentialException",
    "contract": "access",
    "purpose": "Escalate",
    "trigger": "onAction"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "exceptionId",
     "from": "navigation"
    }
   ],
   "preloaded": [
    "→ Bound → Ready → Delivered",
    "CredentialGenerationIssuanceMonitorView.requestId",
    "CredentialGenerationIssuanceMonitorView.virtualTicket",
    "CredentialGenerationIssuanceMonitorView.media",
    "CredentialGenerationIssuanceMonitorView.template",
    "CredentialGenerationIssuanceMonitorView.templateVersion"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-356",
   "workshopBoard": "wireframes/WS167 Ticket Media   Credential Management Board 3.dc.html#bo-356"
  },
  "apisNote": "Regenerated 9 September 2026 from Ticket_Media___Credential_Management_Reference.pdf page 45. 12 of 14 labels bound to a contract property; 19 of 57 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here. **Pack actions reconciled 29 September (VM close-out):** still owed by a contract change: `setCredentialIssuanceRetryPolicy`, `resolveCredentialException`, `retryCredentialGeneration`.",
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
  "id": "BO-357",
  "name": "Credential Delivery & Distribution Operations",
  "module": "Access & Venue",
  "requiresModule": "access",
  "wave": 3,
  "source": {
   "pack": "Ticket_Media___Credential_Management_Reference.pdf",
   "board": "3",
   "number": "15.3.4",
   "page": 47
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/credential-delivery-distribution-operations-bo-357",
   "component": "apps/venue-management-web/src/routes/access-venue/CredentialDeliveryDistributionOperations.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-354"
   ],
   "exitTo": [
    "BO-354"
   ],
   "inferred": false,
   "notes": "**Reached from BO-354, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-354",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F170 step 6→7",
     "operation": "listCredentialDeliveryDistribution"
    }
   ]
  },
  "density": "compact",
  "purposeNote": "delivery tracking.",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Show) and no metric row",
  "purpose": "Manage how generated ticket media are delivered or made available to customers, participants and operational staff.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every credential delivery distribution",
       "columns": [
        "CredentialDeliveryDistributionOperationsView.virtualTicket",
        "CredentialDeliveryDistributionOperationsView.media",
        "CredentialDeliveryDistributionOperationsView.recipient",
        "CredentialDeliveryDistributionOperationsView.channel",
        "CredentialDeliveryDistributionOperationsView.destination",
        "CredentialDeliveryDistributionOperationsView.sentAt",
        "CredentialDeliveryDistributionOperationsView.deliveredAt",
        "CredentialDeliveryDistributionOperationsView.openedDownloaded",
        "CredentialDeliveryDistributionOperationsView.attempt",
        "CredentialDeliveryDistributionOperationsView.status"
       ],
       "bindsTo": "CredentialDeliveryDistributionOperationsView",
       "operation": "listCredentialDeliveryDistribution",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 47 §Show"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected credential delivery distribution",
       "bindsTo": "CredentialDeliveryDistributionOperationsView",
       "columns": [
        "CredentialDeliveryDistributionOperationsView.virtualTicket",
        "CredentialDeliveryDistributionOperationsView.media",
        "CredentialDeliveryDistributionOperationsView.recipient",
        "CredentialDeliveryDistributionOperationsView.channel",
        "CredentialDeliveryDistributionOperationsView.destination",
        "CredentialDeliveryDistributionOperationsView.sentAt",
        "CredentialDeliveryDistributionOperationsView.deliveredAt",
        "CredentialDeliveryDistributionOperationsView.openedDownloaded",
        "CredentialDeliveryDistributionOperationsView.attempt",
        "CredentialDeliveryDistributionOperationsView.status"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Alternative states”, “Where allowed, support”.",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 47 §Show"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "SMS Link",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 47 §Support as applicable"
      },
      {
       "kind": "secondaryButton",
       "label": "WhatsApp integration",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 47 §Support as applicable"
      },
      {
       "kind": "secondaryButton",
       "label": "Download",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 47 §Support as applicable"
      },
      {
       "kind": "secondaryButton",
       "label": "Apple Wallet",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 47 §Support as applicable"
      },
      {
       "kind": "secondaryButton",
       "label": "Google Wallet",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 47 §Support as applicable"
      },
      {
       "kind": "secondaryButton",
       "label": "POS",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 47 §Support as applicable"
      },
      {
       "kind": "secondaryButton",
       "label": "API",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 47 §Support as applicable"
      },
      {
       "kind": "secondaryButton",
       "label": "Physical Collection",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 47 §Support as applicable"
      },
      {
       "kind": "primaryButton",
       "label": "Send credential",
       "operation": "deliverCredential",
       "permission": "ORDER_REPRINT",
       "notes": "Re-sending a credential is a digital reprint: needs ORDER_REPRINT, not gate configuration rights (K1).",
       "provenance": "contract access.yaml POST /credentials/{credentialId}/deliveries (decided 29 September, VM close-out)"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The credential delivery distribution list.",
   "error": "Could not load. Names which read failed and leaves the credential delivery distribution untouched.",
   "emptyFirstRun": "No credential delivery distribution yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the credential delivery distribution are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission: reading needs SCOPE_VIEW; **sending a credential needs ORDER_REPRINT** (K1, 29 September), and the Send action is hidden without it. Never an empty table."
  },
  "apis": [
   {
    "operationId": "listCredentialDeliveryDistribution",
    "contract": "access",
    "purpose": "Credential Delivery & Distribution Operations",
    "trigger": "onLoad"
   },
   {
    "operationId": "deliverCredential",
    "contract": "access",
    "purpose": "Send credential",
    "trigger": "onAction"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "credentialId",
     "from": "navigation"
    }
   ],
   "preloaded": [
    "CredentialDeliveryDistributionOperationsView.virtualTicket",
    "CredentialDeliveryDistributionOperationsView.media",
    "CredentialDeliveryDistributionOperationsView.recipient",
    "CredentialDeliveryDistributionOperationsView.channel",
    "CredentialDeliveryDistributionOperationsView.destination",
    "CredentialDeliveryDistributionOperationsView.sentAt"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-357",
   "workshopBoard": "wireframes/WS167 Ticket Media   Credential Management Board 3.dc.html#bo-357"
  },
  "apisNote": "Regenerated 9 September 2026 from Ticket_Media___Credential_Management_Reference.pdf page 47. 10 of 10 labels bound to a contract property; 29 of 50 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here. **Pack actions reconciled 29 September (VM close-out):** still owed by a contract change: `deliverCredential`.",
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
  "id": "BO-358",
  "name": "Media Binding, Activation & Assignment Operations",
  "module": "Access & Venue",
  "requiresModule": "access",
  "wave": 3,
  "source": {
   "pack": "Ticket_Media___Credential_Management_Reference.pdf",
   "board": "3",
   "number": "15.3.5",
   "page": 48
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/media-binding-activation-assignment-operations-bo-358",
   "component": "apps/venue-management-web/src/routes/access-venue/MediaBindingActivationAssignmentOperations.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-354"
   ],
   "exitTo": [
    "BO-354"
   ],
   "inferred": false,
   "notes": "**Reached from BO-354, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-354",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F170 step 8→9",
     "operation": "setMediaBindingActivation"
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Operational staff can securely assign and activate supported physical, digital and biometric credential media against the correct Virtual Ticket.",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Manage credentials that require operational assignment or activation after ticket issuance.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every media binding activation",
       "columns": [
        "MediaBindingActivationAssignmentOperationsView.virtualTicket",
        "MediaBindingActivationAssignmentOperationsView.customer",
        "MediaBindingActivationAssignmentOperationsView.product",
        "MediaBindingActivationAssignmentOperationsView.existingMedia",
        "MediaBindingActivationAssignmentOperationsView.credentialIdUid",
        "MediaBindingActivationAssignmentOperationsView.provider",
        "MediaBindingActivationAssignmentOperationsView.activationMode",
        "MediaBindingActivationAssignmentOperationsView.validity",
        "MediaBindingActivationAssignmentOperationsView.bindingRule"
       ],
       "bindsTo": "MediaBindingActivationAssignmentOperationsView",
       "operation": "setMediaBindingActivation",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 48 §Display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected media binding activation",
       "bindsTo": "MediaBindingActivationAssignmentOperationsView",
       "columns": [
        "MediaBindingActivationAssignmentOperationsView.virtualTicket",
        "MediaBindingActivationAssignmentOperationsView.customer",
        "MediaBindingActivationAssignmentOperationsView.product",
        "MediaBindingActivationAssignmentOperationsView.existingMedia",
        "MediaBindingActivationAssignmentOperationsView.credentialIdUid",
        "MediaBindingActivationAssignmentOperationsView.provider",
        "MediaBindingActivationAssignmentOperationsView.activationMode",
        "MediaBindingActivationAssignmentOperationsView.validity",
        "MediaBindingActivationAssignmentOperationsView.bindingRule"
       ],
       "notes": "The pack groups this record's detail under its own headings: “This is especially important for”, “Scan Virtual Ticket QR”, “Scan Wristband UID”, “Resolve Virtual Ticket”, “Bind”, “Activate”.",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 48 §Display"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Scan",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 48 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Batch assignment",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 48 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Encoder assignment",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 48 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Activate Now",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 48 §Allow"
      },
      {
       "kind": "secondaryButton",
       "label": "Schedule",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 48 §Allow"
      },
      {
       "kind": "secondaryButton",
       "label": "Activate on First Use",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 48 §Allow"
      },
      {
       "kind": "secondaryButton",
       "label": "Activate on Collection",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 48 §Allow"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The media binding activation list.",
   "error": "Could not load. Names which read failed and leaves the media binding activation untouched.",
   "emptyFirstRun": "No media binding activation yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the media binding activation are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setMediaBindingActivation",
    "contract": "access",
    "purpose": "Media Binding, Activation & Assignment Operations",
    "trigger": "onAction"
   }
  ],
  "entryState": {
   "preloaded": [
    "MediaBindingActivationAssignmentOperationsView.virtualTicket",
    "MediaBindingActivationAssignmentOperationsView.customer",
    "MediaBindingActivationAssignmentOperationsView.product",
    "MediaBindingActivationAssignmentOperationsView.existingMedia",
    "MediaBindingActivationAssignmentOperationsView.credentialIdUid"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-358",
   "workshopBoard": "wireframes/WS167 Ticket Media   Credential Management Board 3.dc.html#bo-358"
  },
  "apisNote": "Regenerated 9 September 2026 from Ticket_Media___Credential_Management_Reference.pdf page 48. 10 of 10 labels bound to a contract property; 18 of 40 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here. **Pack actions reconciled 29 September (VM close-out):** Scan, Batch assignment, Encoder assignment, Activate Now, Schedule, Activate on First Use, Activate on Collection are choices sent by `setMediaBindingActivation`.",
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
  "id": "BO-359",
  "name": "Credential Replacement, Reissue, Revocation & Recovery",
  "module": "Access & Venue",
  "requiresModule": "access",
  "wave": 3,
  "source": {
   "pack": "Ticket_Media___Credential_Management_Reference.pdf",
   "board": "3",
   "number": "15.3.6",
   "page": 50
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/credential-replacement-reissue-revocation-recovery-bo-359",
   "component": "apps/venue-management-web/src/routes/access-venue/CredentialReplacementReissueRevocationRecovery.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-354"
   ],
   "exitTo": [
    "BO-354"
   ],
   "inferred": false,
   "notes": "**Reached from BO-354, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-354",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F170 step 10→11",
     "operation": "listCredentialReplacementReissue"
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Ticket and without losing historical traceability.",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure/reference) and no display directory — it is settings, not a population",
  "purpose": "Manage operational credential changes while preserving the underlying Virtual Ticket.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Immediate old-media revocation",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 50 §Configure/reference"
      },
      {
       "kind": "selectField",
       "label": "Grace period",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 50 §Configure/reference"
      },
      {
       "kind": "selectField",
       "label": "Maximum replacements",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 50 §Configure/reference"
      },
      {
       "kind": "selectField",
       "label": "Identity verification",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 50 §Configure/reference"
      },
      {
       "kind": "selectField",
       "label": "Supervisor approval",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 50 §Configure/reference"
      },
      {
       "kind": "selectField",
       "label": "Reason codes",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 50 §Configure/reference"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Customer changed phone",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 50 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Wristband replacement",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 50 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Wallet replacement",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 50 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Incorrect assignment",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 50 §Support"
      },
      {
       "kind": "primaryButton",
       "label": "Replace credential",
       "operation": "replaceCredential",
       "permission": "ORDER_EXCHANGE",
       "notes": "Needs ORDER_EXCHANGE, as reissueEntitlement, with step-up (mfa) on confirm (K1).",
       "provenance": "contract access.yaml POST /credentials/{credentialId}/replace (decided 29 September, VM close-out)"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The credential replacement reissue configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the credential replacement reissue untouched.",
   "emptyFirstRun": "No credential replacement reissue configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission: reading needs SCOPE_VIEW; **replacing a credential needs ORDER_EXCHANGE with step-up (mfa)** (K1, 29 September), and the Replace action is hidden without it. Never an empty table."
  },
  "apis": [
   {
    "operationId": "listCredentialReplacementReissue",
    "contract": "access",
    "purpose": "Credential Replacement, Reissue, Revocation & Recovery",
    "trigger": "onLoad"
   },
   {
    "operationId": "replaceCredential",
    "contract": "access",
    "purpose": "Replace credential",
    "trigger": "onAction"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "credentialId",
     "from": "navigation"
    }
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-359",
   "workshopBoard": "wireframes/WS167 Ticket Media   Credential Management Board 3.dc.html#bo-359"
  },
  "apisNote": "Regenerated 9 September 2026 from Ticket_Media___Credential_Management_Reference.pdf page 50. 0 of 0 labels bound to a contract property; 10 of 37 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here. **Pack actions reconciled 29 September (VM close-out):** still owed by a contract change: `replaceCredential`.",
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
  "id": "BO-360",
  "name": "Failed Generation, Delivery & Credential Exception Management",
  "module": "Access & Venue",
  "requiresModule": "access",
  "wave": 3,
  "source": {
   "pack": "Ticket_Media___Credential_Management_Reference.pdf",
   "board": "3",
   "number": "15.3.7",
   "page": 51
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/failed-generation-delivery-credential-exception-manageme-bo-360",
   "component": "apps/venue-management-web/src/routes/access-venue/FailedGenerationDeliveryCredentialExceptionManag.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-354"
   ],
   "exitTo": [
    "BO-354"
   ],
   "inferred": false,
   "notes": "**Reached from BO-354, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-354",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F170 step 12→13",
     "operation": "listFailedGenerationDelivery"
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Credential failures are centrally identified, prioritized and resolved before unnecessarily impacting customer admission or fulfillment.",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Provide one dedicated operational queue for credential-related failures.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every failed generation delivery",
       "columns": [
        "FailedGenerationDeliveryCredentialExceptionManagemenView.severity",
        "FailedGenerationDeliveryCredentialExceptionManagemenView.virtualTicket",
        "FailedGenerationDeliveryCredentialExceptionManagemenView.credential",
        "FailedGenerationDeliveryCredentialExceptionManagemenView.media",
        "FailedGenerationDeliveryCredentialExceptionManagemenView.customer",
        "FailedGenerationDeliveryCredentialExceptionManagemenView.event",
        "FailedGenerationDeliveryCredentialExceptionManagemenView.failure",
        "FailedGenerationDeliveryCredentialExceptionManagemenView.time",
        "FailedGenerationDeliveryCredentialExceptionManagemenView.operationalImpact",
        "Retry Status",
        "FailedGenerationDeliveryCredentialExceptionManagemenView.owner"
       ],
       "bindsTo": "FailedGenerationDeliveryCredentialExceptionManagemenView",
       "operation": "listFailedGenerationDelivery",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 51 §Display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected failed generation delivery",
       "bindsTo": "FailedGenerationDeliveryCredentialExceptionManagemenView",
       "columns": [
        "FailedGenerationDeliveryCredentialExceptionManagemenView.severity",
        "FailedGenerationDeliveryCredentialExceptionManagemenView.virtualTicket",
        "FailedGenerationDeliveryCredentialExceptionManagemenView.credential",
        "FailedGenerationDeliveryCredentialExceptionManagemenView.media",
        "FailedGenerationDeliveryCredentialExceptionManagemenView.customer",
        "FailedGenerationDeliveryCredentialExceptionManagemenView.event",
        "FailedGenerationDeliveryCredentialExceptionManagemenView.failure",
        "FailedGenerationDeliveryCredentialExceptionManagemenView.time",
        "FailedGenerationDeliveryCredentialExceptionManagemenView.operationalImpact",
        "Retry Status",
        "FailedGenerationDeliveryCredentialExceptionManagemenView.owner"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Include”, “Consider”.",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 51 §Display"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Retry",
       "operation": "resolveCredentialException",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 51 §Allow"
      },
      {
       "kind": "secondaryButton",
       "label": "Regenerate",
       "operation": "resolveCredentialException",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 51 §Allow"
      },
      {
       "kind": "secondaryButton",
       "label": "Use Fallback",
       "operation": "resolveCredentialException",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 51 §Allow"
      },
      {
       "kind": "secondaryButton",
       "label": "Escalate",
       "operation": "resolveCredentialException",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 51 §Allow"
      },
      {
       "kind": "secondaryButton",
       "label": "Assign Owner",
       "operation": "resolveCredentialException",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 51 §Allow"
      },
      {
       "kind": "secondaryButton",
       "label": "Open Technical Case",
       "operation": "resolveCredentialException",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 51 §Allow"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The failed generation delivery list.",
   "error": "Could not load. Names which read failed and leaves the failed generation delivery untouched.",
   "emptyFirstRun": "No failed generation delivery yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the failed generation delivery are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listFailedGenerationDelivery",
    "contract": "access",
    "purpose": "Failed Generation, Delivery & Credential Exception Management",
    "trigger": "onLoad"
   },
   {
    "operationId": "resolveCredentialException",
    "contract": "access",
    "purpose": "Resolve",
    "trigger": "onAction"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "exceptionId",
     "from": "navigation"
    }
   ],
   "preloaded": [
    "FailedGenerationDeliveryCredentialExceptionManagemenView.severity",
    "FailedGenerationDeliveryCredentialExceptionManagemenView.virtualTicket",
    "FailedGenerationDeliveryCredentialExceptionManagemenView.credential",
    "FailedGenerationDeliveryCredentialExceptionManagemenView.media",
    "FailedGenerationDeliveryCredentialExceptionManagemenView.customer",
    "FailedGenerationDeliveryCredentialExceptionManagemenView.event"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-360",
   "workshopBoard": "wireframes/WS167 Ticket Media   Credential Management Board 3.dc.html#bo-360"
  },
  "apisNote": "Regenerated 9 September 2026 from Ticket_Media___Credential_Management_Reference.pdf page 51. 10 of 11 labels bound to a contract property; 17 of 48 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here. **Pack actions reconciled 29 September (VM close-out):** still owed by a contract change: `resolveCredentialException`.",
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
  "id": "BO-361",
  "name": "Credential Usage & Cross-Media Traceability",
  "module": "Access & Venue",
  "requiresModule": "access",
  "wave": 3,
  "source": {
   "pack": "Ticket_Media___Credential_Management_Reference.pdf",
   "board": "3",
   "number": "15.3.8",
   "page": 53
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/credential-usage-cross-media-traceability-bo-361",
   "component": "apps/venue-management-web/src/routes/access-venue/CredentialUsageCrossMediaTraceability.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-354"
   ],
   "exitTo": [
    "BO-354"
   ],
   "inferred": false,
   "notes": "**Reached from BO-354, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-354",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F170 step 14→15",
     "operation": "listCredentialUsageCross"
    }
   ]
  },
  "density": "compact",
  "purposeNote": "authoritative admission decision engine.",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Capture/reference) and no display directory — it is settings, not a population",
  "purpose": "Provide end-to-end visibility into how the different media attached to one Virtual Ticket have been presented or used. This screen is for credential traceability, while Area 16 remains responsible for the actual access-control decision.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Virtual Ticket",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 53 §Capture/reference"
      },
      {
       "kind": "selectField",
       "label": "Credential",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 53 §Capture/reference"
      },
      {
       "kind": "selectField",
       "label": "Media",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 53 §Capture/reference"
      },
      {
       "kind": "selectField",
       "label": "Presentation timestamp",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 53 §Capture/reference"
      },
      {
       "kind": "selectField",
       "label": "Location",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 53 §Capture/reference"
      },
      {
       "kind": "selectField",
       "label": "Device",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 53 §Capture/reference"
      },
      {
       "kind": "selectField",
       "label": "External system",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 53 §Capture/reference"
      },
      {
       "kind": "selectField",
       "label": "Transaction type",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 53 §Capture/reference"
      },
      {
       "kind": "selectField",
       "label": "Result",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 53 §Capture/reference"
      },
      {
       "kind": "selectField",
       "label": "Entitlement impact",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 53 §Capture/reference"
      },
      {
       "kind": "selectField",
       "label": "Synchronization status",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 53 §Capture/reference"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "What happened to the master entitlement?",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 53 §Allow administrators to understand"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The credential usage cross-media configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the credential usage cross-media untouched.",
   "emptyFirstRun": "No credential usage cross-media configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listCredentialUsageCross",
    "contract": "access",
    "purpose": "Credential Usage & Cross-Media Traceability",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-361",
   "workshopBoard": "wireframes/WS167 Ticket Media   Credential Management Board 3.dc.html#bo-361"
  },
  "apisNote": "Regenerated 9 September 2026 from Ticket_Media___Credential_Management_Reference.pdf page 53. 0 of 0 labels bound to a contract property; 12 of 33 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here. **Pack actions reconciled 29 September (VM close-out):** What happened to the master entitlement? dropped (sentence fragment (question heading)).",
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
  "id": "BO-362",
  "name": "Credential Security, Audit & Operational Evidence",
  "module": "Access & Venue",
  "requiresModule": "access",
  "wave": 3,
  "source": {
   "pack": "Ticket_Media___Credential_Management_Reference.pdf",
   "board": "3",
   "number": "15.3.9",
   "page": 54
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/credential-security-audit-operational-evidence-bo-362",
   "component": "apps/venue-management-web/src/routes/access-venue/CredentialSecurityAuditOperationalEvidence.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-354"
   ],
   "exitTo": [
    "BO-354"
   ],
   "inferred": false,
   "notes": "**Reached from BO-354, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-354",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F170 step 16→17",
     "operation": "listCredentialSecurityOperational"
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Every significant credential lifecycle action is traceable with sufficient evidence to reconstruct who did what, when, why and to which Virtual Ticket.",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Identify) and no metric row",
  "purpose": "Maintain complete evidence of credential creation and lifecycle activity.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every credential security audit",
       "columns": [
        "CredentialSecurityAuditOperationalEvidenceView.anomalyFlags"
       ],
       "bindsTo": "CredentialSecurityAuditOperationalEvidenceView",
       "operation": "listCredentialSecurityOperational",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 54 §Identify"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected credential security audit",
       "bindsTo": "CredentialSecurityAuditOperationalEvidenceView",
       "columns": [
        "CredentialSecurityAuditOperationalEvidenceView.anomalyFlags"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Record”, “RFID-1001”, “Access Control”, “Evidence Export”.",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 54 §Identify"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The credential security audit list.",
   "error": "Could not load. Names which read failed and leaves the credential security audit untouched.",
   "emptyFirstRun": "No credential security audit yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the credential security audit are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listCredentialSecurityOperational",
    "contract": "access",
    "purpose": "Credential Security, Audit & Operational Evidence",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "CredentialSecurityAuditOperationalEvidenceView.anomalyFlags"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-362",
   "workshopBoard": "wireframes/WS167 Ticket Media   Credential Management Board 3.dc.html#bo-362"
  },
  "apisNote": "Regenerated 9 September 2026 from Ticket_Media___Credential_Management_Reference.pdf page 54. 6 of 6 labels bound to a contract property; 21 of 55 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-363",
  "name": "Ticket Media Analytics & AI Operations Intelligence",
  "module": "Access & Venue",
  "requiresModule": "access",
  "wave": 3,
  "source": {
   "pack": "Ticket_Media___Credential_Management_Reference.pdf",
   "board": "3",
   "number": "15.3.10",
   "page": 56
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/ticket-media-analytics-ai-operations-intelligence-bo-363",
   "component": "apps/venue-management-web/src/routes/access-venue/TicketMediaAnalyticsAiOperationsIntelligence.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-354"
   ],
   "exitTo": [
    "BO-354"
   ],
   "inferred": false,
   "notes": "**Reached from BO-354, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation."
  },
  "density": "compact",
  "purposeNote": "and operational performance without transferring authoritative ticket or security decisions to generative AI. Board 3 — Final Screen Register",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Analyze; Compare) and no metric row",
  "purpose": "Provide management and operations with analytics and AI intelligence across Virtual Tickets and credential media. This should be a serious operational intelligence layer—not simply a chatbot.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "filters",
     "components": [
      {
       "kind": "searchField",
       "label": "Search ticket media analytics",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 56 §Analyze by"
      },
      {
       "kind": "multiSelect",
       "label": "Filter by",
       "columns": [
        "Brand",
        "Venue",
        "Event",
        "Product",
        "Channel",
        "Media",
        "Provider",
        "Device",
        "Customer segment",
        "Time period"
       ],
       "notes": "The pack filters this screen by brand, venue, event, product, channel, media and 4 more — which are present is a decision the pack already made.",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 56 §Analyze by"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every ticket media analytics",
       "columns": [
        "TicketMediaAnalyticsAiOperationsIntelligenceView.credentialsGenerated",
        "TicketMediaAnalyticsAiOperationsIntelligenceView.generationSuccess",
        "TicketMediaAnalyticsAiOperationsIntelligenceView.deliverySuccess",
        "TicketMediaAnalyticsAiOperationsIntelligenceView.activation",
        "TicketMediaAnalyticsAiOperationsIntelligenceView.walletAdoption",
        "TicketMediaAnalyticsAiOperationsIntelligenceView.rfidAdoption",
        "TicketMediaAnalyticsAiOperationsIntelligenceView.faceCredentialAdoption",
        "TicketMediaAnalyticsAiOperationsIntelligenceView.multiMediaAdoption",
        "TicketMediaAnalyticsAiOperationsIntelligenceView.replacementRate",
        "TicketMediaAnalyticsAiOperationsIntelligenceView.revocationRate",
        "TicketMediaAnalyticsAiOperationsIntelligenceView.generationFailure",
        "TicketMediaAnalyticsAiOperationsIntelligenceView.deliveryFailure",
        "TicketMediaAnalyticsAiOperationsIntelligenceView.averageGenerationTime",
        "TicketMediaAnalyticsAiOperationsIntelligenceView.averageResolutionTime",
        "TicketMediaAnalyticsAiOperationsIntelligenceView.mediaUsageDistribution",
        "TicketMediaAnalyticsAiOperationsIntelligenceView.providerUptime",
        "TicketMediaAnalyticsAiOperationsIntelligenceView.generationFailures",
        "TicketMediaAnalyticsAiOperationsIntelligenceView.encodingFailures",
        "TicketMediaAnalyticsAiOperationsIntelligenceView.deliveryFailures",
        "TicketMediaAnalyticsAiOperationsIntelligenceView.synchronizationDelay",
        "TicketMediaAnalyticsAiOperationsIntelligenceView.replacementFrequency"
       ],
       "bindsTo": "TicketMediaAnalyticsAiOperationsIntelligenceView",
       "operation": "listTicketMedia",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 56 §Analyze"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected ticket media analytics",
       "bindsTo": "TicketMediaAnalyticsAiOperationsIntelligenceView",
       "columns": [
        "TicketMediaAnalyticsAiOperationsIntelligenceView.credentialsGenerated",
        "TicketMediaAnalyticsAiOperationsIntelligenceView.generationSuccess",
        "TicketMediaAnalyticsAiOperationsIntelligenceView.deliverySuccess",
        "TicketMediaAnalyticsAiOperationsIntelligenceView.activation",
        "TicketMediaAnalyticsAiOperationsIntelligenceView.walletAdoption",
        "TicketMediaAnalyticsAiOperationsIntelligenceView.rfidAdoption",
        "TicketMediaAnalyticsAiOperationsIntelligenceView.faceCredentialAdoption",
        "TicketMediaAnalyticsAiOperationsIntelligenceView.multiMediaAdoption",
        "TicketMediaAnalyticsAiOperationsIntelligenceView.replacementRate",
        "TicketMediaAnalyticsAiOperationsIntelligenceView.revocationRate",
        "TicketMediaAnalyticsAiOperationsIntelligenceView.generationFailure",
        "TicketMediaAnalyticsAiOperationsIntelligenceView.deliveryFailure",
        "TicketMediaAnalyticsAiOperationsIntelligenceView.averageGenerationTime",
        "TicketMediaAnalyticsAiOperationsIntelligenceView.averageResolutionTime",
        "TicketMediaAnalyticsAiOperationsIntelligenceView.mediaUsageDistribution",
        "TicketMediaAnalyticsAiOperationsIntelligenceView.providerUptime",
        "TicketMediaAnalyticsAiOperationsIntelligenceView.generationFailures",
        "TicketMediaAnalyticsAiOperationsIntelligenceView.encodingFailures",
        "TicketMediaAnalyticsAiOperationsIntelligenceView.deliveryFailures",
        "TicketMediaAnalyticsAiOperationsIntelligenceView.synchronizationDelay",
        "TicketMediaAnalyticsAiOperationsIntelligenceView.replacementFrequency"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Eligible customers”, “Backend Screen”, “Credential Operations Command Center”, “Operational exceptions”, “ONE VIRTUAL TICKET”.",
       "provenance": "pack Ticket_Media___Credential_Management_Reference.pdf, page 56 §Analyze"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The ticket media analytics list.",
   "error": "Could not load. Names which read failed and leaves the ticket media analytics untouched.",
   "emptyFirstRun": "No ticket media analytics yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the ticket media analytics are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listTicketMedia",
    "contract": "access",
    "purpose": "Ticket Media Analytics & AI Operations Intelligence",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "TicketMediaAnalyticsAiOperationsIntelligenceView.credentialsGenerated",
    "TicketMediaAnalyticsAiOperationsIntelligenceView.generationSuccess",
    "TicketMediaAnalyticsAiOperationsIntelligenceView.deliverySuccess",
    "TicketMediaAnalyticsAiOperationsIntelligenceView.activation",
    "TicketMediaAnalyticsAiOperationsIntelligenceView.walletAdoption",
    "TicketMediaAnalyticsAiOperationsIntelligenceView.rfidAdoption"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-363",
   "workshopBoard": "wireframes/WS167 Ticket Media   Credential Management Board 3.dc.html#bo-363"
  },
  "apisNote": "Regenerated 9 September 2026 from Ticket_Media___Credential_Management_Reference.pdf page 56. 21 of 31 labels bound to a contract property; 31 of 133 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
 "deliverCredential": {
  "method": "POST",
  "path": "/credentials/{credentialId}/deliveries",
  "contract": "access",
  "summary": "Send a credential over a channel",
  "permission": "ORDER_REPRINT",
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
  "requestBody": "CredentialDeliveryInput",
  "responds": "CredentialDeliveryDistributionOperationsView"
 },
 "getCredentialIssuanceRetryPolicy": {
  "method": "GET",
  "path": "/credential-issuance-retry-policy",
  "contract": "access",
  "summary": "Read the credential issuance retry policy",
  "permission": "SCOPE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "CredentialIssuanceRetryPolicyView"
 },
 "listCredential": {
  "method": "GET",
  "path": "/credential",
  "contract": "access",
  "summary": "Credential Operations Command Center",
  "permission": "SCOPE_VIEW",
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
    "name": "venue",
    "in": "query",
    "required": false
   },
   {
    "name": "date",
    "in": "query",
    "required": false
   },
   {
    "name": "media",
    "in": "query",
    "required": false
   },
   {
    "name": "status",
    "in": "query",
    "required": false
   },
   {
    "name": "channel",
    "in": "query",
    "required": false
   },
   {
    "name": "customer",
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
    "name": "provider",
    "in": "query",
    "required": false
   },
   {
    "name": "exception",
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
 "listCredentialDeliveryDistribution": {
  "method": "GET",
  "path": "/credential-delivery-distribution",
  "contract": "access",
  "summary": "Credential Delivery & Distribution Operations",
  "permission": "SCOPE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "channel",
    "in": "query",
    "required": false
   },
   {
    "name": "status",
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
 "listCredentialGenerationIssuance": {
  "method": "GET",
  "path": "/credential-generation-issuance",
  "contract": "access",
  "summary": "Credential Generation & Issuance Monitor",
  "permission": "SCOPE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "status",
    "in": "query",
    "required": false
   },
   {
    "name": "trigger",
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
 "listCredentialReplacementReissue": {
  "method": "GET",
  "path": "/credential-replacement-reissue",
  "contract": "access",
  "summary": "Credential Replacement, Reissue, Revocation & Recovery",
  "permission": "SCOPE_VIEW",
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
  "responds": "CredentialReplacementReissueRevocationRecoveryView"
 },
 "listCredentialSecurityOperational": {
  "method": "GET",
  "path": "/credential-security-operational",
  "contract": "access",
  "summary": "Credential Security, Audit & Operational Evidence",
  "permission": "AUDIT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "virtualTicket",
    "in": "query",
    "required": false
   },
   {
    "name": "action",
    "in": "query",
    "required": false
   },
   {
    "name": "actor",
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
 "listCredentialUsageCross": {
  "method": "GET",
  "path": "/credential-usage-cross",
  "contract": "access",
  "summary": "Credential Usage & Cross-Media Traceability",
  "permission": "TICKET_LOOKUP",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "virtualTicket",
    "in": "query",
    "required": false
   },
   {
    "name": "media",
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
 "listFailedGenerationDelivery": {
  "method": "GET",
  "path": "/failed-generation-delivery",
  "contract": "access",
  "summary": "Failed Generation, Delivery & Credential Exception Management",
  "permission": "SCOPE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "severity",
    "in": "query",
    "required": false
   },
   {
    "name": "failureType",
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
 "listTicketMedia": {
  "method": "GET",
  "path": "/ticket-media",
  "contract": "access",
  "summary": "Ticket Media Analytics & AI Operations Intelligence",
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
    "name": "brand",
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
    "name": "product",
    "in": "query",
    "required": false
   },
   {
    "name": "channel",
    "in": "query",
    "required": false
   },
   {
    "name": "media",
    "in": "query",
    "required": false
   },
   {
    "name": "provider",
    "in": "query",
    "required": false
   },
   {
    "name": "device",
    "in": "query",
    "required": false
   },
   {
    "name": "customerSegment",
    "in": "query",
    "required": false
   },
   {
    "name": "timePeriod",
    "in": "query",
    "required": false
   }
  ],
  "requestBody": null,
  "responds": "TicketMediaAnalyticsAiOperationsIntelligenceView"
 },
 "replaceCredential": {
  "method": "POST",
  "path": "/credentials/{credentialId}/replace",
  "contract": "access",
  "summary": "Replace a credential's media",
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
  "requestBody": "CredentialReplacementInput",
  "responds": "CredentialOperationsCommandCenterView"
 },
 "resolveCredentialException": {
  "method": "POST",
  "path": "/credential-exceptions/{exceptionId}/resolve",
  "contract": "access",
  "summary": "Act on a credential exception",
  "permission": "ACCESS_POINT_CONFIGURE",
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
  "requestBody": "CredentialExceptionActionInput",
  "responds": "FailedGenerationDeliveryCredentialExceptionManagemenView"
 },
 "retryCredentialGeneration": {
  "method": "POST",
  "path": "/credential-generation-issuance/retry",
  "contract": "access",
  "summary": "Retry failed credential generation",
  "permission": "ACCESS_POINT_CONFIGURE",
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
  "requestBody": "CredentialGenerationRetryInput",
  "responds": "CredentialGenerationRetryResult"
 },
 "setCredentialIssuanceRetryPolicy": {
  "method": "PUT",
  "path": "/credential-issuance-retry-policy",
  "contract": "access",
  "summary": "Set the credential issuance retry policy",
  "permission": "ACCESS_POINT_CONFIGURE",
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
  "requestBody": "CredentialIssuanceRetryPolicyInput",
  "responds": "CredentialIssuanceRetryPolicyView"
 },
 "setMediaBindingActivation": {
  "method": "PUT",
  "path": "/media-binding-activation",
  "contract": "access",
  "summary": "Media Binding, Activation & Assignment Operations",
  "permission": "ACCESS_POINT_CONFIGURE",
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
  "requestBody": "MediaBindingActivationAssignmentOperationsInput",
  "responds": "MediaBindingActivationAssignmentOperationsView"
 },
 "setVirtualTicketCredential": {
  "method": "PUT",
  "path": "/virtual-ticket-credential",
  "contract": "access",
  "summary": "Virtual Ticket & Credential 360° Workspace",
  "permission": "ACCESS_POINT_CONFIGURE",
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
  "requestBody": "VirtualTicketCredential360WorkspaceInput",
  "responds": "VirtualTicketCredential360WorkspaceView"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "CredentialDeliveryDistributionOperationsView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Credential Delivery & Distribution Operations displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "virtualTicket": {
    "type": "string",
    "description": "Virtual Ticket"
   },
   "media": {
    "type": "string",
    "description": "Media"
   },
   "recipient": {
    "type": "string",
    "description": "Recipient"
   },
   "channel": {
    "type": "string",
    "enum": [
     "email",
     "smsLink",
     "whatsapp",
     "b2cAccount",
     "mobileApp",
     "download",
     "appleWallet",
     "googleWallet",
     "pos",
     "boxOffice",
     "kiosk",
     "groupPortal",
     "api",
     "physicalCollection"
    ],
    "description": "Delivery channel"
   },
   "destination": {
    "type": "string",
    "description": "Destination, masked"
   },
   "sentAt": {
    "type": "string",
    "format": "date-time",
    "description": "Sent At"
   },
   "deliveredAt": {
    "type": "string",
    "format": "date-time",
    "description": "Delivered At"
   },
   "openedDownloaded": {
    "type": "string",
    "format": "date-time",
    "description": "When opened or downloaded"
   },
   "attempt": {
    "type": "integer",
    "description": "Attempt"
   },
   "status": {
    "type": "string",
    "enum": [
     "notRequired",
     "pending",
     "sent",
     "delivered",
     "openedDownloaded",
     "completed",
     "failed",
     "bounced",
     "expired",
     "cancelled"
    ],
    "description": "Delivery status"
   },
   "recipientRole": {
    "type": "string",
    "enum": [
     "purchaser",
     "ticketHolder",
     "participant",
     "guardian",
     "groupLeader",
     "authorizedRecipient"
    ],
    "description": "Who the credential was delivered to"
   }
  }
 },
 "CredentialDeliveryInput": {
  "type": "object",
  "x-ticvai-persistence": "none — request only (decided 29 September, VM close-out)",
  "description": "Send, or send again, one credential over one channel (decided 29 September, VM close-out).",
  "required": [
   "id",
   "channel"
  ],
  "properties": {
   "id": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$",
    "description": "Client-generated delivery attempt id"
   },
   "channel": {
    "type": "string",
    "enum": [
     "email",
     "smsLink",
     "whatsapp",
     "download",
     "appleWallet",
     "googleWallet",
     "pos",
     "api",
     "physicalCollection"
    ]
   },
   "recipient": {
    "type": "string",
    "maxLength": 320,
    "description": "Email address, phone number or collection point; empty sends to the recipient already on the credential"
   },
   "recipientRole": {
    "type": "string",
    "enum": [
     "purchaser",
     "ticketHolder",
     "participant",
     "guardian",
     "groupLeader",
     "authorizedRecipient"
    ],
    "default": "ticketHolder"
   },
   "note": {
    "type": "string",
    "maxLength": 300
   }
  }
 },
 "CredentialExceptionActionInput": {
  "type": "object",
  "x-ticvai-persistence": "none — request only (decided 29 September, VM close-out)",
  "description": "One action on a credential exception in the failure queue (decided 29 September, VM close-out).",
  "required": [
   "action"
  ],
  "properties": {
   "action": {
    "type": "string",
    "enum": [
     "retry",
     "regenerate",
     "useFallback",
     "escalate",
     "assignOwner",
     "openTechnicalCase"
    ]
   },
   "ownerId": {
    "type": "string",
    "description": "Required for assignOwner and escalate"
   },
   "fallbackMediaKind": {
    "type": "string",
    "enum": [
     "qr",
     "pdf",
     "printedTicket",
     "rfidCard",
     "wristband"
    ],
    "description": "Required for useFallback"
   },
   "note": {
    "type": "string",
    "maxLength": 500
   }
  }
 },
 "CredentialGenerationRetryInput": {
  "type": "object",
  "x-ticvai-persistence": "none — request only (decided 29 September, VM close-out)",
  "description": "Retry failed credential generation, for selected requests or every eligible one (decided 29 September, VM close-out).",
  "required": [
   "scope"
  ],
  "properties": {
   "scope": {
    "type": "string",
    "enum": [
     "selected",
     "allEligible"
    ]
   },
   "requestIds": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "maxItems": 500,
    "description": "The failed generation requests (`CredentialGenerationIssuanceMonitorView.requestId`); required for selected"
   }
  }
 },
 "CredentialGenerationRetryResult": {
  "type": "object",
  "x-ticvai-persistence": "none — computed (decided 29 September, VM close-out)",
  "description": "What a retry queued and what it skipped (decided 29 September, VM close-out).",
  "required": [
   "queued",
   "skipped"
  ],
  "properties": {
   "queued": {
    "type": "integer"
   },
   "skipped": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "requestId": {
       "type": "string"
      },
      "reason": {
       "type": "string",
       "enum": [
        "notFailed",
        "alreadyQueued",
        "notRetryable"
       ]
      }
     }
    }
   }
  }
 },
 "CredentialIssuanceRetryPolicyInput": {
  "type": "object",
  "x-ticvai-persistence": "none — request only (decided 29 September, VM close-out)",
  "description": "The tenant's automatic retry policy for failed credential generation (decided 29 September, VM close-out). Proposed defaults are ours (our build plan).",
  "required": [
   "automaticRetry"
  ],
  "properties": {
   "automaticRetry": {
    "type": "boolean",
    "default": true
   },
   "maxAttempts": {
    "type": "integer",
    "minimum": 1,
    "maximum": 10,
    "default": 3
   },
   "backoffMinutes": {
    "type": "integer",
    "minimum": 1,
    "maximum": 240,
    "default": 5,
    "description": "Wait before the first retry; doubles on each attempt"
   },
   "escalateAfterAttempts": {
    "type": "integer",
    "minimum": 1,
    "maximum": 10,
    "default": 3,
    "description": "After this many failures the request becomes a credential exception with an owner; not more than maxAttempts"
   }
  }
 },
 "CredentialIssuanceRetryPolicyView": {
  "type": "object",
  "x-ticvai-persistence": "access.credential_issuance_retry_policy",
  "description": "The automatic retry policy in force, one per venue (decided 29 September, VM close-out).",
  "required": [
   "venueId",
   "automaticRetry",
   "maxAttempts",
   "backoffMinutes",
   "escalateAfterAttempts"
  ],
  "properties": {
   "venueId": {
    "type": "string"
   },
   "automaticRetry": {
    "type": "boolean",
    "default": true
   },
   "maxAttempts": {
    "type": "integer",
    "minimum": 1,
    "maximum": 10,
    "default": 3
   },
   "backoffMinutes": {
    "type": "integer",
    "minimum": 1,
    "maximum": 240,
    "default": 5
   },
   "escalateAfterAttempts": {
    "type": "integer",
    "minimum": 1,
    "maximum": 10,
    "default": 3
   },
   "updatedAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   },
   "scopePath": {
    "type": "string",
    "description": "The partition key (ADR-0005). Written at venue scope"
   }
  }
 },
 "CredentialOperationsCommandCenterView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Credential Operations Command Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "virtualTicketId": {
    "type": "string",
    "description": "Virtual Ticket ID"
   },
   "credentialId": {
    "type": "string",
    "description": "Credential ID"
   },
   "mediaType": {
    "type": "string",
    "description": "Media Type"
   },
   "customerParticipant": {
    "type": "string",
    "description": "Customer / Participant"
   },
   "product": {
    "type": "string",
    "description": "Product"
   },
   "event": {
    "type": "string",
    "description": "Event"
   },
   "credentialStatus": {
    "type": "string",
    "enum": [
     "pendingGeneration",
     "generated",
     "pendingActivation",
     "active",
     "suspended",
     "revoked",
     "expired",
     "failed"
    ],
    "description": "Credential status"
   },
   "deliveryStatus": {
    "type": "string",
    "enum": [
     "notRequired",
     "pending",
     "sent",
     "delivered",
     "openedDownloaded",
     "completed",
     "failed",
     "bounced",
     "expired",
     "cancelled"
    ],
    "description": "Delivery status (15.3.4)"
   },
   "activationStatus": {
    "type": "string",
    "enum": [
     "pending",
     "scheduled",
     "active",
     "notRequired"
    ],
    "description": "Activation status"
   },
   "bindingStatus": {
    "type": "string",
    "enum": [
     "pending",
     "bound",
     "unbound",
     "failed"
    ],
    "description": "Binding status"
   },
   "provider": {
    "type": "string",
    "description": "Provider"
   },
   "lastActivity": {
    "type": "string",
    "format": "date-time",
    "description": "Last Activity"
   },
   "exception": {
    "type": "string",
    "description": "Exception"
   },
   "owner": {
    "type": "string",
    "description": "Owner"
   }
  }
 },
 "CredentialReplacementInput": {
  "type": "object",
  "x-ticvai-persistence": "none — request only (decided 29 September, VM close-out)",
  "description": "Replace the media of a credential while the Virtual Ticket stays the same (decided 29 September, VM close-out).",
  "required": [
   "reason"
  ],
  "properties": {
   "reason": {
    "type": "string",
    "enum": [
     "lost",
     "stolen",
     "damaged",
     "compromised",
     "customerChangedPhone",
     "rfidFailure",
     "wristbandReplacement",
     "qrCompromise",
     "walletReplacement",
     "faceReEnrollment",
     "incorrectAssignment"
    ]
   },
   "newMediaKind": {
    "type": "string",
    "description": "Media type of the replacement (`MediaTypeTechnologyLibraryView.mediaType`); empty keeps the current kind"
   },
   "newMediaCode": {
    "type": "string",
    "description": "Code of the new physical media where one is encoded at the counter"
   },
   "approvalRequestId": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$",
    "description": "The granted approval, where the replacement rule requires one"
   },
   "note": {
    "type": "string",
    "maxLength": 500
   }
  }
 },
 "CredentialReplacementReissueRevocationRecoveryView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Credential Replacement, Reissue, Revocation & Recovery displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "reason": {
    "type": "string",
    "enum": [
     "lost",
     "stolen",
     "damaged",
     "compromised",
     "customerChangedPhone",
     "rfidFailure",
     "wristbandReplacement",
     "qrCompromise",
     "walletReplacement",
     "faceReEnrollment",
     "incorrectAssignment"
    ],
    "description": "Replacement reason this policy covers"
   },
   "immediateOldMediaRevocation": {
    "type": "boolean",
    "description": "Immediate old-media revocation"
   },
   "gracePeriod": {
    "type": "string",
    "description": "ISO 8601 duration, e.g. PT30M"
   },
   "maximumReplacements": {
    "type": "integer",
    "description": "Maximum replacements"
   },
   "identityVerification": {
    "type": "boolean",
    "description": "Identity verification"
   },
   "supervisorApproval": {
    "type": "boolean",
    "description": "Supervisor approval"
   },
   "reasonCodes": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Reason codes"
   },
   "recoveryAllowed": {
    "type": "boolean",
    "description": "A suspended credential may be restored under this policy"
   }
  },
  "required": [
   "reason"
  ]
 },
 "FailedGenerationDeliveryCredentialExceptionManagemenView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Failed Generation, Delivery & Credential Exception Management displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "exceptionId": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$",
    "description": "The key `resolveCredentialException` acts on (decided 29 September, VM close-out)"
   },
   "lastAction": {
    "type": "string",
    "enum": [
     "retry",
     "regenerate",
     "useFallback",
     "escalate",
     "assignOwner",
     "openTechnicalCase"
    ],
    "description": "The last action taken through `resolveCredentialException`"
   },
   "failureType": {
    "type": "string",
    "enum": [
     "generationFailed",
     "bindingFailed",
     "activationFailed",
     "deliveryFailed",
     "walletFailure",
     "rfidEncodingFailure",
     "duplicateCredential",
     "invalidToken",
     "providerFailure",
     "synchronizationFailure",
     "missingTemplate",
     "missingRequiredData",
     "expiredCredential",
     "mappingFailure",
     "unknownCredential"
    ],
    "description": "Failure category"
   },
   "severity": {
    "type": "string",
    "enum": [
     "low",
     "medium",
     "high",
     "critical"
    ],
    "description": "Severity, weighted by event proximity, arrival time, affected tickets, fallback availability, VIP and access impact"
   },
   "virtualTicket": {
    "type": "string",
    "description": "Virtual Ticket"
   },
   "credential": {
    "type": "string",
    "description": "Credential"
   },
   "media": {
    "type": "string",
    "description": "Media"
   },
   "customer": {
    "type": "string",
    "description": "Customer"
   },
   "event": {
    "type": "string",
    "description": "Event"
   },
   "failure": {
    "type": "string",
    "description": "Failure"
   },
   "time": {
    "type": "string",
    "format": "date-time",
    "description": "Time"
   },
   "operationalImpact": {
    "type": "string",
    "description": "Operational Impact"
   },
   "owner": {
    "type": "string",
    "description": "Owner"
   },
   "retryStatus": {
    "type": "string",
    "description": "Retry status"
   }
  }
 },
 "MediaBindingActivationAssignmentOperationsInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures",
  "description": "**What Media Binding, Activation & Assignment Operations submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "credentialIdUid": {
    "type": "string",
    "description": "Credential ID or UID read from the medium; for face, the biometric provider reference"
   },
   "virtualTicketId": {
    "type": "string",
    "description": "Virtual Ticket the medium is bound to"
   },
   "mediaKind": {
    "type": "string",
    "enum": [
     "rfid",
     "nfc",
     "wristband",
     "physicalCard",
     "faceRecognition",
     "temporaryCredential"
    ],
    "description": "Medium being bound"
   },
   "captureMethod": {
    "type": "string",
    "enum": [
     "scan",
     "tap",
     "manualLookup",
     "batchAssignment",
     "encoderAssignment"
    ],
    "description": "How the medium was read or assigned"
   },
   "activationMode": {
    "type": "string",
    "enum": [
     "activateNow",
     "schedule",
     "activateOnFirstUse",
     "activateOnCollection",
     "temporaryActivation"
    ],
    "description": "When the bound medium becomes active"
   },
   "provider": {
    "type": "string",
    "description": "Provider"
   },
   "scheduledAt": {
    "type": "string",
    "format": "date-time",
    "description": "Activation time when scheduled"
   }
  },
  "required": [
   "virtualTicketId",
   "mediaKind",
   "credentialIdUid"
  ]
 },
 "MediaBindingActivationAssignmentOperationsView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Media Binding, Activation & Assignment Operations displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "virtualTicketId": {
    "type": "string",
    "description": "Virtual Ticket the medium is bound to"
   },
   "mediaKind": {
    "type": "string",
    "enum": [
     "rfid",
     "nfc",
     "wristband",
     "physicalCard",
     "faceRecognition",
     "temporaryCredential"
    ],
    "description": "Medium being bound"
   },
   "virtualTicket": {
    "type": "string",
    "description": "Virtual Ticket"
   },
   "customer": {
    "type": "string",
    "description": "Customer"
   },
   "product": {
    "type": "string",
    "description": "Product"
   },
   "existingMedia": {
    "type": "string",
    "description": "Existing Media"
   },
   "credentialIdUid": {
    "type": "string",
    "description": "Credential ID / UID"
   },
   "provider": {
    "type": "string",
    "description": "Provider"
   },
   "activationMode": {
    "type": "string",
    "enum": [
     "activateNow",
     "schedule",
     "activateOnFirstUse",
     "activateOnCollection",
     "temporaryActivation"
    ],
    "description": "When the bound medium becomes active"
   },
   "validity": {
    "type": "string",
    "description": "Validity"
   },
   "bindingRule": {
    "type": "string",
    "description": "Binding Rule"
   },
   "captureMethod": {
    "type": "string",
    "enum": [
     "scan",
     "tap",
     "manualLookup",
     "batchAssignment",
     "encoderAssignment"
    ],
    "description": "How the medium was read or assigned"
   },
   "scheduledAt": {
    "type": "string",
    "format": "date-time",
    "description": "Activation time when scheduled"
   }
  },
  "required": [
   "virtualTicketId",
   "mediaKind",
   "credentialIdUid"
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
 "TicketMediaAnalyticsAiOperationsIntelligenceView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Ticket Media Analytics & AI Operations Intelligence displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "credentialsGenerated": {
    "type": "integer",
    "description": "Credentials Generated"
   },
   "generationSuccess": {
    "type": "number",
    "description": "Generation Success %"
   },
   "deliverySuccess": {
    "type": "number",
    "description": "Delivery Success %"
   },
   "activation": {
    "type": "number",
    "description": "Activation %"
   },
   "walletAdoption": {
    "type": "number",
    "description": "Percent"
   },
   "rfidAdoption": {
    "type": "number",
    "description": "Percent"
   },
   "faceCredentialAdoption": {
    "type": "number",
    "description": "Percent"
   },
   "multiMediaAdoption": {
    "type": "number",
    "description": "Percent"
   },
   "replacementRate": {
    "type": "number",
    "description": "Replacement Rate"
   },
   "revocationRate": {
    "type": "number",
    "description": "Revocation Rate"
   },
   "generationFailure": {
    "type": "number",
    "description": "Generation Failure %"
   },
   "deliveryFailure": {
    "type": "number",
    "description": "Delivery Failure %"
   },
   "averageGenerationTime": {
    "type": "number",
    "description": "Seconds"
   },
   "averageResolutionTime": {
    "type": "number",
    "description": "Seconds"
   },
   "mediaUsageDistribution": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Share of eligible customers per media type; may exceed 100% in total"
   },
   "providerUptime": {
    "type": "number",
    "description": "Percent"
   },
   "generationFailures": {
    "type": "integer",
    "description": "Generation failures"
   },
   "encodingFailures": {
    "type": "integer",
    "description": "Encoding failures"
   },
   "deliveryFailures": {
    "type": "integer",
    "description": "Delivery failures"
   },
   "synchronizationDelay": {
    "type": "number",
    "description": "Seconds"
   },
   "replacementFrequency": {
    "type": "number",
    "description": "Replacement frequency"
   },
   "credentialFailureRisk": {
    "type": "string",
    "description": "Predicted; advisory"
   },
   "deliveryFailureProbability": {
    "type": "number",
    "description": "Predicted, 0 to 1; advisory"
   },
   "mediaDemandForUpcomingEvents": {
    "type": "string",
    "description": "Media demand for upcoming events"
   },
   "rfidWristbandStockRequirements": {
    "type": "string",
    "description": "RFID/wristband stock requirements"
   },
   "operationalWorkload": {
    "type": "string",
    "description": "Operational workload"
   },
   "likelyOnSiteReplacementVolumes": {
    "type": "integer",
    "description": "Predicted; advisory"
   }
  }
 },
 "VirtualTicketCredential360WorkspaceInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table covers these fields** — the closest is access.entitlement at 9%, so this is not an update to anything the package stores today and no new table has been decided",
  "description": "**What Virtual Ticket & Credential 360° Workspace submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.\n\n**The pack defines this as a record**, under *For each media show* - one of only 13 drafted writes that does. That is the client writing a row rather than a screen, and it is where the table conversation should start.",
  "properties": {
   "virtualTicketId": {
    "type": "string",
    "description": "Virtual Ticket ID"
   },
   "mediaRole": {
    "type": "string",
    "enum": [
     "primary",
     "secondary",
     "fallback",
     "temporary",
     "revokedHistorical"
    ],
    "description": "Role of the medium on the ticket"
   },
   "bindingId": {
    "type": "string",
    "description": "Binding ID"
   },
   "mediaType": {
    "type": "string",
    "description": "Media type"
   },
   "provider": {
    "type": "string",
    "description": "Provider"
   },
   "issued": {
    "type": "string",
    "format": "date-time",
    "description": "Issued"
   },
   "delivered": {
    "type": "string",
    "format": "date-time",
    "description": "Delivered"
   },
   "activated": {
    "type": "string",
    "format": "date-time",
    "description": "Activated"
   },
   "validFrom": {
    "type": "string",
    "format": "date-time",
    "description": "Valid From"
   },
   "validTo": {
    "type": "string",
    "format": "date-time",
    "description": "Valid To"
   },
   "lastUpdate": {
    "type": "string",
    "format": "date-time",
    "description": "Last update"
   },
   "lastPresentation": {
    "type": "string",
    "format": "date-time",
    "description": "Last presentation"
   },
   "lastUse": {
    "type": "string",
    "format": "date-time",
    "description": "Last use"
   },
   "deviceReferenceWhereAppropriate": {
    "type": "string",
    "description": "Device/reference where appropriate"
   },
   "status": {
    "type": "string",
    "enum": [
     "pending",
     "active",
     "suspended",
     "revoked",
     "expired"
    ],
    "description": "Medium status"
   }
  },
  "x-ticvai-record-definition": "For each media show",
  "required": [
   "virtualTicketId"
  ]
 },
 "VirtualTicketCredential360WorkspaceView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Virtual Ticket & Credential 360° Workspace displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "virtualTicketId": {
    "type": "string",
    "description": "Virtual Ticket ID"
   },
   "ticketHolder": {
    "type": "string",
    "description": "Ticket Holder"
   },
   "participant": {
    "type": "string",
    "description": "Participant"
   },
   "product": {
    "type": "string",
    "description": "Product"
   },
   "event": {
    "type": "string",
    "description": "Event"
   },
   "performance": {
    "type": "string",
    "description": "Performance"
   },
   "venue": {
    "type": "string",
    "description": "Venue"
   },
   "seat": {
    "type": "string",
    "description": "Seat"
   },
   "order": {
    "type": "string",
    "description": "Order"
   },
   "ticketStatus": {
    "type": "string",
    "enum": [
     "created",
     "pendingFulfillment",
     "active",
     "partiallyUsed",
     "used",
     "expired",
     "suspended",
     "cancelled",
     "voided",
     "reissuedSuperseded",
     "refunded",
     "transferred",
     "blocked"
    ],
    "description": "Virtual Ticket status"
   },
   "usageStatus": {
    "type": "string",
    "enum": [
     "unused",
     "partiallyUsed",
     "used"
    ],
    "description": "Usage status"
   },
   "validity": {
    "type": "string",
    "description": "Validity"
   },
   "entitlements": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Entitlements on the ticket"
   },
   "mediaRole": {
    "type": "string",
    "enum": [
     "primary",
     "secondary",
     "fallback",
     "temporary",
     "revokedHistorical"
    ],
    "description": "Role of the medium on the ticket"
   },
   "bindingId": {
    "type": "string",
    "description": "Binding ID"
   },
   "mediaType": {
    "type": "string",
    "description": "Media type"
   },
   "provider": {
    "type": "string",
    "description": "Provider"
   },
   "issued": {
    "type": "string",
    "format": "date-time",
    "description": "Issued"
   },
   "delivered": {
    "type": "string",
    "format": "date-time",
    "description": "Delivered"
   },
   "activated": {
    "type": "string",
    "format": "date-time",
    "description": "Activated"
   },
   "validFrom": {
    "type": "string",
    "format": "date-time",
    "description": "Valid From"
   },
   "validTo": {
    "type": "string",
    "format": "date-time",
    "description": "Valid To"
   },
   "lastUpdate": {
    "type": "string",
    "format": "date-time",
    "description": "Last update"
   },
   "lastPresentation": {
    "type": "string",
    "format": "date-time",
    "description": "Last presentation"
   },
   "lastUse": {
    "type": "string",
    "format": "date-time",
    "description": "Last use"
   },
   "deviceReferenceWhereAppropriate": {
    "type": "string",
    "description": "Device/reference where appropriate"
   },
   "status": {
    "type": "string",
    "enum": [
     "pending",
     "active",
     "suspended",
     "revoked",
     "expired"
    ],
    "description": "Medium status"
   }
  },
  "required": [
   "virtualTicketId"
  ]
 }
}
```
