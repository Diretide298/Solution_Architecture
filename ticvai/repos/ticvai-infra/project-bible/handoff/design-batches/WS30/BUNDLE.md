# WS30 — Membership   Annual Pass Management board 2

**10 screens · 19 operations · 31 schemas · 6 permissions**

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

- **Every control that can be refused must be gated.** 6 permissions apply here:
  `APPROVAL_REQUEST, GUEST_MANAGE, ORDER_MODIFY, PLATFORM_CELL_MANAGE, PLATFORM_TENANT_VIEW, PRODUCT_CONFIGURE`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `BO-294` | Member Operations Command Center | listDetail | 1 | 0 | — |
| `BO-295` | Member 360° Membership Account Workspace | listDetail | 2 | 0 | — |
| `BO-296` | Membership Activation, Assignment & Credential Management | listDetail | 2 | 0 | — |
| `BO-297` | Visit, Admission & Entitlement Usage Monitor | listDetail | 1 | 0 | — |
| `BO-298` | Membership Freeze, Suspension & Reactivation Management | configEditor | 4 | 1 | — |
| `BO-299` | Membership Upgrade, Downgrade & Product Migration Operations | listDetail | 2 | 1 | — |
| `BO-300` | Renewal Operations & Auto-Renewal Management | listDetail | 2 | 0 | — |
| `BO-301` | Member Exceptions, Overrides & Service Recovery | listDetail | 5 | 0 | — |
| `BO-302` | Member Lifecycle History, Audit & Case Timeline | listDetail | 1 | 0 | — |
| `BO-303` | Membership Analytics, Renewal Intelligence & AI Retention Center | commandCentre | 1 | 0 | — |

## Thin screens in this batch

**BO-300, BO-302 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "BO-294",
  "name": "Member Operations Command Center",
  "module": "Sell",
  "requiresModule": "membership",
  "wave": 3,
  "source": {
   "pack": "Membership___Annual_Pass_Management_Reference.pdf",
   "board": "2",
   "number": "13.2.1",
   "page": 21
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/sell/member-operations-command-center-bo-294",
   "component": "apps/venue-management-web/src/routes/sell/MemberOperationsCommandCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-100"
   ],
   "exitTo": [
    "BO-100",
    "BO-295",
    "BO-296",
    "BO-297",
    "BO-298",
    "BO-299",
    "BO-300",
    "BO-301",
    "BO-302",
    "BO-303"
   ],
   "inferred": false,
   "notes": "**The board's hub.** The workshop specified this module as boards of ten and opened each with a command centre; the other nine screens are that board's detail, so they are reached from here and return here.",
   "transitions": [
    {
     "to": "BO-100",
     "trigger": "Venue Home",
     "provenance": "derived — BO-100 declares entryState.params  and BO-294 holds none of them, so the edge carries nothing and BO-100 opens cold"
    },
    {
     "to": "BO-297",
     "trigger": "Works in Visit, Admission & Entitlement Usage Monitor",
     "provenance": "flow F139 step 5→6",
     "operation": "listMember"
    },
    {
     "to": "BO-298",
     "trigger": "Works in Membership Freeze, Suspension & Reactivation Management",
     "provenance": "flow F139 step 7→8",
     "operation": "listMember"
    },
    {
     "to": "BO-302",
     "trigger": "Works in Member Lifecycle History, Audit & Case Timeline",
     "provenance": "flow F139 step 15→16",
     "operation": "listMember"
    },
    {
     "to": "BO-303",
     "trigger": "Works in Membership Analytics, Renewal Intelligence & AI Retention Center",
     "provenance": "flow F139 step 17→18",
     "operation": "listMember"
    },
    {
     "to": "BO-295",
     "trigger": "Works in Member 360° Membership Account Workspace",
     "provenance": "flow F139 step 1→2",
     "operation": "listMember",
     "carries": [
      "membershipId"
     ]
    },
    {
     "to": "BO-296",
     "trigger": "Works in Membership Activation, Assignment & Credential Management",
     "provenance": "flow F139 step 3→4",
     "operation": "listMember",
     "carries": [
      "membershipId"
     ]
    },
    {
     "to": "BO-299",
     "trigger": "Works in Membership Upgrade, Downgrade & Product Migration Operations",
     "provenance": "flow F139 step 9→10",
     "operation": "listMember",
     "carries": [
      "membershipId"
     ]
    },
    {
     "to": "BO-300",
     "trigger": "Works in Renewal Operations & Auto-Renewal Management",
     "provenance": "flow F139 step 11→12",
     "operation": "listMember",
     "carries": [
      "membershipId"
     ]
    },
    {
     "to": "BO-301",
     "trigger": "Works in Member Exceptions, Overrides & Service Recovery",
     "provenance": "flow F139 step 13→14",
     "operation": "listMember",
     "carries": [
      "membershipId"
     ]
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Membership operations teams can monitor and prioritize the complete member population from one centralized workspace.",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Provide membership teams with a real-time operational dashboard for the complete active member population.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "filters",
     "components": [
      {
       "kind": "searchField",
       "label": "Search member operations",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 21 §Filter by"
      },
      {
       "kind": "multiSelect",
       "label": "Filter by",
       "columns": [
        "MemberOperationsCommandCenterView.venue",
        "Product",
        "MemberOperationsCommandCenterView.tier",
        "Status",
        "Member Type",
        "Activation",
        "Expiry",
        "Renewal",
        "Usage",
        "Customer Segment",
        "Acquisition Channel"
       ],
       "notes": "The pack filters this screen by venue, product, tier, status, member type, activation and 5 more — which are present is a decision the pack already made.",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 21 §Filter by"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "Active Members",
       "bindsTo": "MemberOperationsCommandCenterSummary.activeMembers",
       "operation": "listMember",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "New Members Today",
       "bindsTo": "MemberOperationsCommandCenterSummary.newMembersToday",
       "operation": "listMember",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Activated Today",
       "bindsTo": "MemberOperationsCommandCenterSummary.activatedToday",
       "operation": "listMember",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Pending Activation",
       "bindsTo": "MemberOperationsCommandCenterSummary.pendingActivation",
       "operation": "listMember",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Expiring in 30 Days",
       "bindsTo": "MemberOperationsCommandCenterSummary.expiringIn30Days",
       "operation": "listMember",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Renewal due",
       "bindsTo": "MemberOperationsCommandCenterSummary.renewalDue",
       "operation": "listMember",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Renewed This Month",
       "bindsTo": "MemberOperationsCommandCenterSummary.renewedThisMonth",
       "operation": "listMember",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Renewal rate",
       "bindsTo": "MemberOperationsCommandCenterSummary.renewalRate",
       "operation": "listMember",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Suspended Memberships",
       "bindsTo": "MemberOperationsCommandCenterSummary.suspendedMemberships",
       "operation": "listMember",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Frozen Memberships",
       "bindsTo": "MemberOperationsCommandCenterSummary.frozenMemberships",
       "operation": "listMember",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Membership Exceptions",
       "bindsTo": "MemberOperationsCommandCenterSummary.membershipExceptions",
       "operation": "listMember",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "At risk members",
       "bindsTo": "MemberOperationsCommandCenterSummary.atRiskMembers",
       "operation": "listMember",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every member operations",
       "columns": [
        "MemberOperationsCommandCenterView.membershipId",
        "MemberOperationsCommandCenterView.member",
        "MemberOperationsCommandCenterView.membershipProduct",
        "MemberOperationsCommandCenterView.tier",
        "MemberOperationsCommandCenterView.venue",
        "MemberOperationsCommandCenterView.activationDate",
        "MemberOperationsCommandCenterView.expiryDate",
        "MemberOperationsCommandCenterView.membershipStatus",
        "MemberOperationsCommandCenterView.usageLevel",
        "MemberOperationsCommandCenterView.renewalStatus",
        "MemberOperationsCommandCenterView.outstandingIssue",
        "MemberOperationsCommandCenterView.owner"
       ],
       "bindsTo": "MemberOperationsCommandCenterView",
       "operation": "listMember",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 21 §Display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected member operations",
       "bindsTo": "MemberOperationsCommandCenterView",
       "columns": [
        "MemberOperationsCommandCenterView.membershipId",
        "MemberOperationsCommandCenterView.member",
        "MemberOperationsCommandCenterView.membershipProduct",
        "MemberOperationsCommandCenterView.tier",
        "MemberOperationsCommandCenterView.venue",
        "MemberOperationsCommandCenterView.activationDate",
        "MemberOperationsCommandCenterView.expiryDate",
        "MemberOperationsCommandCenterView.membershipStatus",
        "MemberOperationsCommandCenterView.usageLevel",
        "MemberOperationsCommandCenterView.renewalStatus",
        "MemberOperationsCommandCenterView.outstandingIssue",
        "MemberOperationsCommandCenterView.owner"
       ],
       "notes": null,
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 21 §Display"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The member operations list.",
   "error": "Could not load. Names which read failed and leaves the member operations untouched.",
   "emptyFirstRun": "No member operations yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the member operations are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listMember",
    "contract": "subscription",
    "purpose": "Member Operations Command Center",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "MemberOperationsCommandCenterSummary.activeMembers",
    "MemberOperationsCommandCenterSummary.newMembersToday",
    "MemberOperationsCommandCenterSummary.activatedToday",
    "MemberOperationsCommandCenterSummary.pendingActivation",
    "MemberOperationsCommandCenterSummary.expiringIn30Days",
    "MemberOperationsCommandCenterSummary.renewalDue"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-294",
   "workshopBoard": "wireframes/WS83 Membership   Annual Pass Management Board 2.dc.html#bo-294"
  },
  "apisNote": "Regenerated 9 September 2026 from Membership___Annual_Pass_Management_Reference.pdf page 21. 26 of 35 labels bound to a contract property; 35 of 46 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-295",
  "name": "Member 360° Membership Account Workspace",
  "module": "Sell",
  "requiresModule": "membership",
  "wave": 3,
  "source": {
   "pack": "Membership___Annual_Pass_Management_Reference.pdf",
   "board": "2",
   "number": "13.2.2",
   "page": 22
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/sell/member-360-membership-account-workspace-bo-295",
   "component": "apps/venue-management-web/src/routes/sell/Member360MembershipAccountWorkspace.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-294"
   ],
   "exitTo": [
    "BO-294"
   ],
   "inferred": false,
   "notes": "**Reached from BO-294, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-294",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F139 step 2→3",
     "operation": "setMemberMembershipAccount"
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Authorized users can understand the complete operational state of a membership without navigating across multiple modules.",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display; Show) and no metric row",
  "purpose": "Provide a complete operational view of an individual member and their membership contract. This should be the primary screen an authorized membership-service agent opens when helping a member.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every member 360° membership",
       "columns": [
        "Member360MembershipAccountWorkspaceView.memberName",
        "Member360MembershipAccountWorkspaceView.customerId",
        "Member360MembershipAccountWorkspaceView.membershipId",
        "Member360MembershipAccountWorkspaceView.membershipProduct",
        "Member360MembershipAccountWorkspaceView.tier",
        "Member360MembershipAccountWorkspaceView.status",
        "Member360MembershipAccountWorkspaceView.activationDate",
        "Member360MembershipAccountWorkspaceView.expiryDate",
        "Member360MembershipAccountWorkspaceView.renewalStatus",
        "Member360MembershipAccountWorkspaceView.primaryVenue",
        "Member360MembershipAccountWorkspaceView.credentialStatus",
        "Member360MembershipAccountWorkspaceView.primaryMember",
        "Member360MembershipAccountWorkspaceView.secondaryAdult",
        "Member360MembershipAccountWorkspaceView.dependents",
        "Member360MembershipAccountWorkspaceView.sharedBenefits",
        "Member360MembershipAccountWorkspaceView.individualBenefits",
        "Member360MembershipAccountWorkspaceView.membershipVersion",
        "Member360MembershipAccountWorkspaceView.purchaseDate",
        "Member360MembershipAccountWorkspaceView.purchaseChannel",
        "Member360MembershipAccountWorkspaceView.originalOrder",
        "Member360MembershipAccountWorkspaceView.validity",
        "Member360MembershipAccountWorkspaceView.activationMethod",
        "Member360MembershipAccountWorkspaceView.renewalPolicy",
        "Member360MembershipAccountWorkspaceView.autoRenewStatus"
       ],
       "bindsTo": "Member360MembershipAccountWorkspaceView",
       "operation": "setMemberMembershipAccount",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 22 §Display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected member 360° membership",
       "bindsTo": "Member360MembershipAccountWorkspaceView",
       "columns": [
        "Member360MembershipAccountWorkspaceView.memberName",
        "Member360MembershipAccountWorkspaceView.customerId",
        "Member360MembershipAccountWorkspaceView.membershipId",
        "Member360MembershipAccountWorkspaceView.membershipProduct",
        "Member360MembershipAccountWorkspaceView.tier",
        "Member360MembershipAccountWorkspaceView.status",
        "Member360MembershipAccountWorkspaceView.activationDate",
        "Member360MembershipAccountWorkspaceView.expiryDate",
        "Member360MembershipAccountWorkspaceView.renewalStatus",
        "Member360MembershipAccountWorkspaceView.primaryVenue",
        "Member360MembershipAccountWorkspaceView.credentialStatus",
        "Member360MembershipAccountWorkspaceView.primaryMember",
        "Member360MembershipAccountWorkspaceView.secondaryAdult",
        "Member360MembershipAccountWorkspaceView.dependents",
        "Member360MembershipAccountWorkspaceView.sharedBenefits",
        "Member360MembershipAccountWorkspaceView.individualBenefits",
        "Member360MembershipAccountWorkspaceView.membershipVersion",
        "Member360MembershipAccountWorkspaceView.purchaseDate",
        "Member360MembershipAccountWorkspaceView.purchaseChannel",
        "Member360MembershipAccountWorkspaceView.originalOrder",
        "Member360MembershipAccountWorkspaceView.validity",
        "Member360MembershipAccountWorkspaceView.activationMethod",
        "Member360MembershipAccountWorkspaceView.renewalPolicy",
        "Member360MembershipAccountWorkspaceView.autoRenewStatus"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Guest Tickets”, “Free Parking”, “F&B Benefit”, “Retail Benefit”, “Link to”.",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 22 §Display"
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
       "provenance": "contract operation setMemberMembershipAccount"
      },
      {
       "kind": "banner",
       "label": "Permissions this screen separates",
       "notes": "**The pack separates these permissions and no action on the screen claims them yet:** Activate, Freeze, Suspend, Resume, Renew, Replace Credential, Add Note, Review Eligibility, Manage Dependents. Each needs attaching to the control it gates, or the screen needs the control.",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 22 §Subject to permission"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The member 360° membership list.",
   "error": "Could not load. Names which read failed and leaves the member 360° membership untouched.",
   "emptyFirstRun": "No member 360° membership yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the member 360° membership are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setMemberMembershipAccount",
    "contract": "subscription",
    "purpose": "Member 360° Membership Account Workspace",
    "trigger": "onAction"
   },
   {
    "operationId": "recordBenefitUsage",
    "contract": "identity",
    "purpose": "Consume a member benefit by hand",
    "trigger": "onAction",
    "provenance": "decided 29 September, VM close-out (venue management and configuration)"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "membershipId",
     "from": "navigation"
    }
   ],
   "preloaded": [
    "Member360MembershipAccountWorkspaceView.memberName",
    "Member360MembershipAccountWorkspaceView.customerId",
    "Member360MembershipAccountWorkspaceView.membershipId",
    "Member360MembershipAccountWorkspaceView.membershipProduct",
    "Member360MembershipAccountWorkspaceView.tier",
    "Member360MembershipAccountWorkspaceView.status"
   ],
   "coldEntry": "Opened from BO-294 with the membership picked there. Opened cold (a bookmark or a refresh), it shows the list to pick from rather than an empty record, and says plainly if the membership no longer exists."
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-295",
   "workshopBoard": "wireframes/WS83 Membership   Annual Pass Management Board 2.dc.html#bo-295"
  },
  "apisNote": "Regenerated 9 September 2026 from Membership___Annual_Pass_Management_Reference.pdf page 22. 24 of 24 labels bound to a contract property; 33 of 51 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-296",
  "name": "Membership Activation, Assignment & Credential Management",
  "module": "Sell",
  "requiresModule": "membership",
  "wave": 3,
  "source": {
   "pack": "Membership___Annual_Pass_Management_Reference.pdf",
   "board": "2",
   "number": "13.2.3",
   "page": 24
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/sell/membership-activation-assignment-credential-management-bo-296",
   "component": "apps/venue-management-web/src/routes/sell/MembershipActivationAssignmentCredentialManageme.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-294"
   ],
   "exitTo": [
    "BO-294"
   ],
   "inferred": false,
   "notes": "**Reached from BO-294, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-294",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F139 step 4→5",
     "operation": "listMembershipActivationCredential"
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Purchased memberships can be securely assigned, verified, activated and linked to appropriate credentials according to Board 1 rules.",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Manage the operational process that turns a purchased membership product into an active membership assigned to a specific individual.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every membership activation credential",
       "columns": [
        "MembershipActivationAssignmentCredentialManagementView.purchaseDate",
        "MembershipActivationAssignmentCredentialManagementView.eligibleActivationDate",
        "MembershipActivationAssignmentCredentialManagementView.activationDeadline",
        "MembershipActivationAssignmentCredentialManagementView.selectedStartDate",
        "MembershipActivationAssignmentCredentialManagementView.calculatedExpiry",
        "MembershipActivationAssignmentCredentialManagementView.activationMethod"
       ],
       "bindsTo": "MembershipActivationAssignmentCredentialManagementView",
       "operation": "listMembershipActivationCredential",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 24 §Display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected membership activation credential",
       "bindsTo": "MembershipActivationAssignmentCredentialManagementView",
       "columns": [
        "MembershipActivationAssignmentCredentialManagementView.purchaseDate",
        "MembershipActivationAssignmentCredentialManagementView.eligibleActivationDate",
        "MembershipActivationAssignmentCredentialManagementView.activationDeadline",
        "MembershipActivationAssignmentCredentialManagementView.selectedStartDate",
        "MembershipActivationAssignmentCredentialManagementView.calculatedExpiry",
        "MembershipActivationAssignmentCredentialManagementView.activationMethod"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Show memberships”, “Purchased Membership”, “Associate membership with”, “Record reason”.",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 24 §Display"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Block",
       "operation": "resolveMembershipActivation",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 24 §Actions depend on configuration"
      },
      {
       "kind": "secondaryButton",
       "label": "Review",
       "operation": "resolveMembershipActivation",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 24 §Actions depend on configuration"
      },
      {
       "kind": "secondaryButton",
       "label": "Replace",
       "operation": "resolveMembershipActivation",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 24 §Actions depend on configuration"
      },
      {
       "kind": "secondaryButton",
       "label": "Link",
       "operation": "resolveMembershipActivation",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 24 §Actions depend on configuration"
      },
      {
       "kind": "secondaryButton",
       "label": "Escalate",
       "operation": "resolveMembershipActivation",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 24 §Actions depend on configuration"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The membership activation credential list.",
   "error": "Could not load. Names which read failed and leaves the membership activation credential untouched.",
   "emptyFirstRun": "No membership activation credential yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the membership activation credential are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listMembershipActivationCredential",
    "contract": "subscription",
    "purpose": "Membership Activation, Assignment & Credential Management",
    "trigger": "onLoad"
   },
   {
    "operationId": "resolveMembershipActivation",
    "contract": "orders",
    "purpose": "Act on activation",
    "trigger": "onAction"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "membershipId",
     "from": "navigation"
    }
   ],
   "preloaded": [
    "MembershipActivationAssignmentCredentialManagementView.purchaseDate",
    "MembershipActivationAssignmentCredentialManagementView.eligibleActivationDate",
    "MembershipActivationAssignmentCredentialManagementView.activationDeadline",
    "MembershipActivationAssignmentCredentialManagementView.selectedStartDate",
    "MembershipActivationAssignmentCredentialManagementView.calculatedExpiry",
    "MembershipActivationAssignmentCredentialManagementView.activationMethod"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-296",
   "workshopBoard": "wireframes/WS83 Membership   Annual Pass Management Board 2.dc.html#bo-296"
  },
  "apisNote": "Regenerated 9 September 2026 from Membership___Annual_Pass_Management_Reference.pdf page 24. 6 of 6 labels bound to a contract property; 19 of 44 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here. **Pack actions reconciled 29 September (VM close-out):** still owed by a contract change: `resolveMembershipActivation`.",
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
  "id": "BO-297",
  "name": "Visit, Admission & Entitlement Usage Monitor",
  "module": "Sell",
  "requiresModule": "membership",
  "wave": 3,
  "source": {
   "pack": "Membership___Annual_Pass_Management_Reference.pdf",
   "board": "2",
   "number": "13.2.4",
   "page": 26
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/sell/visit-admission-entitlement-usage-monitor-bo-297",
   "component": "apps/venue-management-web/src/routes/sell/VisitAdmissionEntitlementUsageMonitor.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-294"
   ],
   "exitTo": [
    "BO-294"
   ],
   "inferred": false,
   "notes": "**Reached from BO-294, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-294",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F139 step 6→7",
     "operation": "listVisitAdmissionEntitlement"
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Authorized users can trace membership visits and benefit consumption while preserving the Access Control system as the authoritative admission-validation engine.",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display; Detect) and no metric row",
  "purpose": "Provide membership teams with complete visibility of how a member uses admission and other membership entitlements.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "Total Visits",
       "bindsTo": "VisitAdmissionEntitlementUsageMonitorSummary.totalVisits",
       "operation": "listVisitAdmissionEntitlement",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Visits This Month",
       "bindsTo": "VisitAdmissionEntitlementUsageMonitorSummary.visitsThisMonth",
       "operation": "listVisitAdmissionEntitlement",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Last Visit",
       "bindsTo": "VisitAdmissionEntitlementUsageMonitorSummary.lastVisit",
       "operation": "listVisitAdmissionEntitlement",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Upcoming Reservation start",
       "bindsTo": "VisitAdmissionEntitlementUsageMonitorSummary.upcomingReservation",
       "operation": "listVisitAdmissionEntitlement",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Guest Tickets Used",
       "bindsTo": "VisitAdmissionEntitlementUsageMonitorSummary.guestTicketsUsed",
       "operation": "listVisitAdmissionEntitlement",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Guest Tickets Remaining",
       "bindsTo": "VisitAdmissionEntitlementUsageMonitorSummary.guestTicketsRemaining",
       "operation": "listVisitAdmissionEntitlement",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Parking Uses",
       "bindsTo": "VisitAdmissionEntitlementUsageMonitorSummary.parkingUses",
       "operation": "listVisitAdmissionEntitlement",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Benefit usage",
       "bindsTo": "VisitAdmissionEntitlementUsageMonitorSummary.benefitUsage",
       "operation": "listVisitAdmissionEntitlement",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "No-Shows",
       "bindsTo": "VisitAdmissionEntitlementUsageMonitorSummary.noShows",
       "operation": "listVisitAdmissionEntitlement",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every visit admission entitlement",
       "columns": [
        "VisitAdmissionEntitlementUsageMonitorView.validationResult"
       ],
       "bindsTo": "VisitAdmissionEntitlementUsageMonitorView",
       "operation": "listVisitAdmissionEntitlement",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 26 §Display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected visit admission entitlement",
       "bindsTo": "VisitAdmissionEntitlementUsageMonitorView",
       "columns": [
        "VisitAdmissionEntitlementUsageMonitorView.validationResult"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Benefit”, “Guest”, “Parking 18 Unlimited”, “Manual Adjustment”, “Require”.",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 26 §Display"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The visit admission entitlement list.",
   "error": "Could not load. Names which read failed and leaves the visit admission entitlement untouched.",
   "emptyFirstRun": "No visit admission entitlement yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the visit admission entitlement are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listVisitAdmissionEntitlement",
    "contract": "subscription",
    "purpose": "Visit, Admission & Entitlement Usage Monitor",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "VisitAdmissionEntitlementUsageMonitorSummary.totalVisits",
    "VisitAdmissionEntitlementUsageMonitorSummary.visitsThisMonth",
    "VisitAdmissionEntitlementUsageMonitorSummary.lastVisit",
    "VisitAdmissionEntitlementUsageMonitorSummary.upcomingReservation",
    "VisitAdmissionEntitlementUsageMonitorSummary.guestTicketsUsed",
    "VisitAdmissionEntitlementUsageMonitorSummary.guestTicketsRemaining"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-297",
   "workshopBoard": "wireframes/WS83 Membership   Annual Pass Management Board 2.dc.html#bo-297"
  },
  "apisNote": "Regenerated 9 September 2026 from Membership___Annual_Pass_Management_Reference.pdf page 26. 15 of 15 labels bound to a contract property; 24 of 39 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-298",
  "name": "Membership Freeze, Suspension & Reactivation Management",
  "module": "Sell",
  "requiresModule": "membership",
  "wave": 3,
  "source": {
   "pack": "Membership___Annual_Pass_Management_Reference.pdf",
   "board": "2",
   "number": "13.2.5",
   "page": 27
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/sell/membership-freeze-suspension-reactivation-management-bo-298",
   "component": "apps/venue-management-web/src/routes/sell/MembershipFreezeSuspensionReactivationManagement.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-294"
   ],
   "exitTo": [
    "BO-294"
   ],
   "inferred": false,
   "notes": "**Reached from BO-294, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-294",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F139 step 8→9",
     "operation": "listMembershipFreezeSuspension"
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Freeze Configuration Consumption; Capture) and no display directory — it is settings, not a population",
  "purpose": "Manage temporary interruption of membership rights without necessarily terminating the membership contract.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Start Date",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 27 §Capture"
      },
      {
       "kind": "selectField",
       "label": "End Date",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 27 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Duration",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 27 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Reason",
       "notes": "The freeze reasons of `freezeEntitlement`: travelling, injury, personal, seasonal, other. **Choosing Other makes Note required** (decided 28 September, audit R222).",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 27 §Capture"
      },
      {
       "kind": "textField",
       "label": "Note",
       "notes": "**Required, at least 3 characters, when the reason is Other** — the form will not submit without it, and `freezeEntitlement` refuses 400 (decided 28 September, audit R222). Optional for every other reason.",
       "provenance": "contract catalogue.yaml POST /entitlements/{entitlementId}/freeze"
      },
      {
       "kind": "selectField",
       "label": "Requested By",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 27 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Approved By",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 27 §Capture"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Freeze",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 27 §Support"
      },
      {
       "kind": "destructiveButton",
       "label": "Suspend",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 27 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Resume",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 27 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Reactivate",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 27 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Administrative Hold",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 27 §Support"
      }
     ]
    }
   ]
  },
  "overlays": [
   {
    "id": "confirmSuspend",
    "component": "confirmDialog",
    "trigger": "Suspend",
    "body": "**Suspend on a membership freeze suspension is not reversible from this screen.** Names what it affects and what it leaves alone. The pack requires the decision to reach the audit trail, so the dialog states that it is recorded.",
    "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 27 §Support"
   }
  ],
  "states": {
   "loading": "The membership freeze suspension configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the membership freeze suspension untouched.",
   "emptyFirstRun": "No membership freeze suspension configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listMembershipFreezeSuspension",
    "contract": "subscription",
    "purpose": "Membership Freeze, Suspension & Reactivation Management",
    "trigger": "onLoad"
   },
   {
    "operationId": "freezeEntitlement",
    "contract": "catalogue",
    "purpose": "Pause a membership at the guest's request",
    "trigger": "onAction",
    "provenance": "decided 29 September, VM close-out (venue management and configuration)"
   },
   {
    "operationId": "reinstateEntitlement",
    "contract": "catalogue",
    "purpose": "Lift a suspension",
    "trigger": "onAction",
    "provenance": "decided 29 September, VM close-out (venue management and configuration)"
   },
   {
    "operationId": "suspendEntitlement",
    "contract": "catalogue",
    "purpose": "Suspend or reactivate the membership entitlement (isSuspended, reason)",
    "trigger": "onAction",
    "provenance": "decided 29 September, VM close-out (venue management and configuration): serves the pack action(s) Suspend, Administrative Hold, Reactivate; Resume"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "entitlementId",
     "from": "navigation"
    }
   ],
   "coldEntry": "Opened from BO-294 with the membership entitlement picked there. Opened cold (a bookmark or a refresh), it shows the list to pick from rather than an empty record, and says plainly if the membership entitlement no longer exists."
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-298",
   "workshopBoard": "wireframes/WS83 Membership   Annual Pass Management Board 2.dc.html#bo-298"
  },
  "apisNote": "Regenerated 9 September 2026 from Membership___Annual_Pass_Management_Reference.pdf page 27. 0 of 0 labels bound to a contract property; 11 of 18 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here. **Pack actions reconciled 29 September (VM close-out):** Suspend, Administrative Hold, Reactivate: `suspendEntitlement`; Resume: `freezeEntitlement`.",
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
  "id": "BO-299",
  "name": "Membership Upgrade, Downgrade & Product Migration Operations",
  "module": "Sell",
  "requiresModule": "membership",
  "wave": 3,
  "source": {
   "pack": "Membership___Annual_Pass_Management_Reference.pdf",
   "board": "2",
   "number": "13.2.6",
   "page": 29
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/sell/membership-upgrade-downgrade-product-migration-operation-bo-299",
   "component": "apps/venue-management-web/src/routes/sell/MembershipUpgradeDowngradeProductMigrationOperat.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-294"
   ],
   "exitTo": [
    "BO-294"
   ],
   "inferred": false,
   "notes": "**Reached from BO-294, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-294",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F139 step 10→11",
     "operation": "listMembershipUpgradeDowngrade"
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Memberships can move between tiers/products without losing historical, financial or entitlement integrity.",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Manage operational movement of an active member between membership products or tiers.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Membership___Annual_Pass_Management_Reference.pdf, page 29"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Membership___Annual_Pass_Management_Reference.pdf, page 29"
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
       "label": "Next Visit",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 29 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Next Renewal",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 29 §Support"
      },
      {
       "kind": "destructiveButton",
       "label": "End of Current Term",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 29 §Support"
      },
      {
       "kind": "primaryButton",
       "label": "Migrate membership",
       "operation": "migrateMembership",
       "provenance": "contract orders.yaml POST /memberships/{membershipId}/migrations (decided 29 September, VM close-out)"
      }
     ]
    },
    {
     "name": "contentBody",
     "components": []
    }
   ]
  },
  "overlays": [
   {
    "id": "confirmEndOfCurrentTerm",
    "component": "confirmDialog",
    "trigger": "End of Current Term",
    "body": "**End of Current Term on a membership upgrade downgrade is not reversible from this screen.** Names what it affects and what it leaves alone. The pack requires the decision to reach the audit trail, so the dialog states that it is recorded.",
    "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 29 §Support"
   }
  ],
  "states": {
   "loading": "The membership upgrade downgrade list.",
   "error": "Could not load. Names which read failed and leaves the membership upgrade downgrade untouched.",
   "emptyFirstRun": "No membership upgrade downgrade yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the membership upgrade downgrade are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listMembershipUpgradeDowngrade",
    "contract": "subscription",
    "purpose": "Membership Upgrade, Downgrade & Product Migration Operations",
    "trigger": "onLoad"
   },
   {
    "operationId": "migrateMembership",
    "contract": "orders",
    "purpose": "Migrate membership",
    "trigger": "onAction"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "membershipId",
     "from": "navigation"
    }
   ],
   "preloaded": [
    "MembershipUpgradeDowngradeProductMigrationOperationsView.currentMembership",
    "MembershipUpgradeDowngradeProductMigrationOperationsView.targetMembership",
    "MembershipUpgradeDowngradeProductMigrationOperationsView.customerQualification",
    "MembershipUpgradeDowngradeProductMigrationOperationsView.usage",
    "MembershipUpgradeDowngradeProductMigrationOperationsView.remainingValidity"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-299",
   "workshopBoard": "wireframes/WS83 Membership   Annual Pass Management Board 2.dc.html#bo-299"
  },
  "apisNote": "Regenerated 9 September 2026 from Membership___Annual_Pass_Management_Reference.pdf page 29. 0 of 0 labels bound to a contract property; 3 of 34 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here. **Pack actions reconciled 29 September (VM close-out):** still owed by a contract change: `migrateMembership`.",
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
  "id": "BO-300",
  "name": "Renewal Operations & Auto-Renewal Management",
  "module": "Sell",
  "requiresModule": "membership",
  "wave": 3,
  "source": {
   "pack": "Membership___Annual_Pass_Management_Reference.pdf",
   "board": "2",
   "number": "13.2.7",
   "page": 30
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/sell/renewal-operations-auto-renewal-management-bo-300",
   "component": "apps/venue-management-web/src/routes/sell/RenewalOperationsAutoRenewalManagement.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-294"
   ],
   "exitTo": [
    "BO-294"
   ],
   "inferred": false,
   "notes": "**Reached from BO-294, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-294",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F139 step 12→13",
     "operation": "listRenewalAuto"
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Membership teams can monitor and execute manual and automatic renewals while maintaining continuous and correctly versioned membership contracts.",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display; Track) and no metric row",
  "purpose": "Operationally manage memberships approaching expiry and execute the renewal policies configured in Board 1.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every renewal operations auto-renewal",
       "columns": [
        "RenewalOperationsAutoRenewalManagementView.member",
        "RenewalOperationsAutoRenewalManagementView.membership",
        "RenewalOperationsAutoRenewalManagementView.tier",
        "RenewalOperationsAutoRenewalManagementView.expiry",
        "RenewalOperationsAutoRenewalManagementView.renewalWindow",
        "RenewalOperationsAutoRenewalManagementView.renewalPrice",
        "RenewalOperationsAutoRenewalManagementView.autoRenew",
        "RenewalOperationsAutoRenewalManagementView.paymentMethodStatus",
        "RenewalOperationsAutoRenewalManagementView.eligibility",
        "RenewalOperationsAutoRenewalManagementView.renewalStatus"
       ],
       "bindsTo": "RenewalOperationsAutoRenewalManagementView",
       "operation": "listRenewalAuto",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 30 §Display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected renewal operations auto-renewal",
       "bindsTo": "RenewalOperationsAutoRenewalManagementView",
       "columns": [
        "RenewalOperationsAutoRenewalManagementView.member",
        "RenewalOperationsAutoRenewalManagementView.membership",
        "RenewalOperationsAutoRenewalManagementView.tier",
        "RenewalOperationsAutoRenewalManagementView.expiry",
        "RenewalOperationsAutoRenewalManagementView.renewalWindow",
        "RenewalOperationsAutoRenewalManagementView.renewalPrice",
        "RenewalOperationsAutoRenewalManagementView.autoRenew",
        "RenewalOperationsAutoRenewalManagementView.paymentMethodStatus",
        "RenewalOperationsAutoRenewalManagementView.eligibility",
        "RenewalOperationsAutoRenewalManagementView.renewalStatus"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Segment members into”, “Validate”, “Final failure”, “Renewal Grace”, “Renewal Continuity”, “Current expiry”.",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 30 §Display"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The renewal operations auto-renewal list.",
   "error": "Could not load. Names which read failed and leaves the renewal operations auto-renewal untouched.",
   "emptyFirstRun": "No renewal operations auto-renewal yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the renewal operations auto-renewal are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listRenewalAuto",
    "contract": "subscription",
    "purpose": "Renewal Operations & Auto-Renewal Management",
    "trigger": "onLoad"
   },
   {
    "operationId": "renewMembership",
    "contract": "orders",
    "purpose": "Renew a membership now, manually",
    "trigger": "onAction",
    "provenance": "decided 29 September, VM close-out (venue management and configuration)"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "membershipId",
     "from": "navigation"
    }
   ],
   "preloaded": [
    "RenewalOperationsAutoRenewalManagementView.member",
    "RenewalOperationsAutoRenewalManagementView.membership",
    "RenewalOperationsAutoRenewalManagementView.tier",
    "RenewalOperationsAutoRenewalManagementView.expiry",
    "RenewalOperationsAutoRenewalManagementView.renewalWindow",
    "RenewalOperationsAutoRenewalManagementView.renewalPrice"
   ],
   "coldEntry": "Opened from BO-294 with the membership picked there. Opened cold (a bookmark or a refresh), it shows the list to pick from rather than an empty record, and says plainly if the membership no longer exists."
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-300",
   "workshopBoard": "wireframes/WS83 Membership   Annual Pass Management Board 2.dc.html#bo-300"
  },
  "apisNote": "Regenerated 9 September 2026 from Membership___Annual_Pass_Management_Reference.pdf page 30. 10 of 10 labels bound to a contract property; 10 of 41 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-301",
  "name": "Member Exceptions, Overrides & Service Recovery",
  "module": "Sell",
  "requiresModule": "membership",
  "wave": 3,
  "source": {
   "pack": "Membership___Annual_Pass_Management_Reference.pdf",
   "board": "2",
   "number": "13.2.8",
   "page": 32
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/sell/member-exceptions-overrides-service-recovery-bo-301",
   "component": "apps/venue-management-web/src/routes/sell/MemberExceptionsOverridesServiceRecovery.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-294"
   ],
   "exitTo": [
    "BO-294"
   ],
   "inferred": false,
   "notes": "**Reached from BO-294, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-294",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F139 step 14→15",
     "operation": "listMemberExceptionOverride"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Provide controlled handling of member-specific situations that fall outside normal membership policy.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Membership___Annual_Pass_Management_Reference.pdf, page 32"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Membership___Annual_Pass_Management_Reference.pdf, page 32"
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
       "label": "Eligibility Override",
       "operation": "createMemberException",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 32 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Expiry Extension",
       "operation": "createMemberException",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 32 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Complimentary Renewal",
       "operation": "createMemberException",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 32 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Complimentary Benefit",
       "operation": "createMemberException",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 32 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Entitlement Adjustment",
       "operation": "createMemberException",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 32 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Freeze Exception",
       "operation": "createMemberException",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 32 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Suspension Override",
       "operation": "createMemberException",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 32 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Replacement Credential",
       "operation": "createMemberException",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 32 §Support"
      }
     ]
    },
    {
     "name": "contentBody",
     "components": []
    }
   ]
  },
  "states": {
   "loading": "The member exceptions overrides list.",
   "error": "Could not load. Names which read failed and leaves the member exceptions overrides untouched.",
   "emptyFirstRun": "No member exceptions overrides yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the member exceptions overrides are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listMemberExceptionOverride",
    "contract": "subscription",
    "purpose": "Member Exceptions, Overrides & Service Recovery",
    "trigger": "onLoad"
   },
   {
    "operationId": "createApprovalRequest",
    "contract": "approvals",
    "purpose": "Raise the approval a member exception needs",
    "trigger": "onAction",
    "provenance": "decided 29 September, VM close-out (venue management and configuration)"
   },
   {
    "operationId": "freezeEntitlement",
    "contract": "catalogue",
    "purpose": "Grant a freeze as an exception",
    "trigger": "onAction",
    "provenance": "decided 29 September, VM close-out (venue management and configuration)"
   },
   {
    "operationId": "reinstateEntitlement",
    "contract": "catalogue",
    "purpose": "Override a suspension",
    "trigger": "onAction",
    "provenance": "decided 29 September, VM close-out (venue management and configuration)"
   },
   {
    "operationId": "createMemberException",
    "contract": "orders",
    "purpose": "Record exception",
    "trigger": "onAction"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "membershipId",
     "from": "navigation"
    },
    {
     "name": "entitlementId",
     "from": "navigation"
    }
   ],
   "coldEntry": "Opened from BO-294 with the membership entitlement picked there. Opened cold (a bookmark or a refresh), it shows the list to pick from rather than an empty record, and says plainly if the membership entitlement no longer exists."
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-301",
   "workshopBoard": "wireframes/WS83 Membership   Annual Pass Management Board 2.dc.html#bo-301"
  },
  "apisNote": "Regenerated 9 September 2026 from Membership___Annual_Pass_Management_Reference.pdf page 32. 0 of 0 labels bound to a contract property; 9 of 14 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here. **Pack actions reconciled 29 September (VM close-out):** still owed by a contract change: `createMemberException`.",
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
  "id": "BO-302",
  "name": "Member Lifecycle History, Audit & Case Timeline",
  "module": "Sell",
  "requiresModule": "membership",
  "wave": 3,
  "source": {
   "pack": "Membership___Annual_Pass_Management_Reference.pdf",
   "board": "2",
   "number": "13.2.9",
   "page": 33
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/sell/member-lifecycle-history-audit-case-timeline-bo-302",
   "component": "apps/venue-management-web/src/routes/sell/MemberLifecycleHistoryAuditCaseTimeline.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-294"
   ],
   "exitTo": [
    "BO-294"
   ],
   "inferred": false,
   "notes": "**Reached from BO-294, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-294",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F139 step 16→17",
     "operation": "listMemberLifecycleCase"
    }
   ]
  },
  "density": "compact",
  "purposeNote": "The entire membership lifecycle can be reconstructed chronologically with responsible users, systems, rules and related transactions.",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Track) and no metric row",
  "purpose": "Maintain a complete historical record of everything that has happened to the membership from purchase to final expiry.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every member lifecycle history",
       "columns": [
        "MemberLifecycleHistoryAuditCaseTimelineView.eventType",
        "Freeze",
        "Upgrade",
        "Downgrade"
       ],
       "bindsTo": "MemberLifecycleHistoryAuditCaseTimelineView",
       "operation": "listMemberLifecycleCase",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 33 §Track"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected member lifecycle history",
       "bindsTo": "MemberLifecycleHistoryAuditCaseTimelineView",
       "columns": [
        "MemberLifecycleHistoryAuditCaseTimelineView.eventType",
        "Freeze",
        "Upgrade",
        "Downgrade"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Before/After Audit”, “Expiry”, “Reason”, “Record”, “Link to”, “Case Notes”.",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 33 §Track"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The member lifecycle history list.",
   "error": "Could not load. Names which read failed and leaves the member lifecycle history untouched.",
   "emptyFirstRun": "No member lifecycle history yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the member lifecycle history are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listMemberLifecycleCase",
    "contract": "subscription",
    "purpose": "Member Lifecycle History, Audit & Case Timeline",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "MemberLifecycleHistoryAuditCaseTimelineView.eventType"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-302",
   "workshopBoard": "wireframes/WS83 Membership   Annual Pass Management Board 2.dc.html#bo-302"
  },
  "apisNote": "Regenerated 9 September 2026 from Membership___Annual_Pass_Management_Reference.pdf page 33. 13 of 16 labels bound to a contract property; 16 of 56 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-303",
  "name": "Membership Analytics, Renewal Intelligence & AI Retention Center",
  "module": "Sell",
  "requiresModule": "membership",
  "wave": 3,
  "source": {
   "pack": "Membership___Annual_Pass_Management_Reference.pdf",
   "board": "2",
   "number": "13.2.10",
   "page": 35
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/sell/membership-analytics-renewal-intelligence-ai-retention-c-bo-303",
   "component": "apps/venue-management-web/src/routes/sell/MembershipAnalyticsRenewalIntelligenceAiRetentio.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-294"
   ],
   "exitTo": [
    "BO-294"
   ],
   "inferred": false,
   "notes": "**Reached from BO-294, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation."
  },
  "density": "compact",
  "purposeNote": "Management can analyze membership performance and use governed AI intelligence to improve renewal, retention and membership-product performance. Board 2 — Final Screen Register # Backend Screen Core Responsibility 13.2. Member population",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen a metric directory (§Display; Forecast) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's",
  "purpose": "Turn membership operational data into actionable intelligence for retention, renewal, product optimization and member engagement.",
  "layout": {
   "template": "dashboard",
   "regions": [
    {
     "name": "contentBody",
     "slot": "filters",
     "components": [
      {
       "kind": "searchField",
       "label": "Search membership analytics renewal",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 35 §Analyze by"
      },
      {
       "kind": "multiSelect",
       "label": "Filter by",
       "columns": [
        "Membership Product",
        "Tier",
        "Purchase Month",
        "Venue",
        "Acquisition Channel",
        "Customer Segment",
        "Geography",
        "Renewal Cohort"
       ],
       "notes": "The pack filters this screen by membership product, tier, purchase month, venue, acquisition channel, customer segment and 2 more — which are present is a decision the pack already made.",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 35 §Analyze by"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "Active Members",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 35 §Display",
       "bindsTo": "MembershipAnalyticsRenewalIntelligenceAiRetentionCenSummary.activeMembers"
      },
      {
       "kind": "metricTile",
       "label": "New Memberships",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 35 §Display",
       "bindsTo": "MembershipAnalyticsRenewalIntelligenceAiRetentionCenSummary.newMemberships"
      },
      {
       "kind": "metricTile",
       "label": "Renewal Rate",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 35 §Display",
       "bindsTo": "MembershipAnalyticsRenewalIntelligenceAiRetentionCenSummary.renewalRate"
      },
      {
       "kind": "metricTile",
       "label": "Churn Rate",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 35 §Display",
       "bindsTo": "MembershipAnalyticsRenewalIntelligenceAiRetentionCenSummary.churnRate"
      },
      {
       "kind": "metricTile",
       "label": "Auto-Renew Success",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 35 §Display",
       "bindsTo": "MembershipAnalyticsRenewalIntelligenceAiRetentionCenSummary.autoRenewSuccess"
      },
      {
       "kind": "metricTile",
       "label": "Average Membership Tenure",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 35 §Display",
       "bindsTo": "MembershipAnalyticsRenewalIntelligenceAiRetentionCenSummary.averageMembershipTenure"
      },
      {
       "kind": "metricTile",
       "label": "Average Visits per Member",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 35 §Display",
       "bindsTo": "MembershipAnalyticsRenewalIntelligenceAiRetentionCenSummary.averageVisitsPerMember"
      },
      {
       "kind": "metricTile",
       "label": "Revenue per Member",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 35 §Display",
       "bindsTo": "MembershipAnalyticsRenewalIntelligenceAiRetentionCenSummary.revenuePerMember"
      },
      {
       "kind": "metricTile",
       "label": "Membership Utilization",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 35 §Display",
       "bindsTo": "MembershipAnalyticsRenewalIntelligenceAiRetentionCenSummary.membershipUtilization"
      },
      {
       "kind": "metricTile",
       "label": "Benefit Utilization",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 35 §Display",
       "bindsTo": "MembershipAnalyticsRenewalIntelligenceAiRetentionCenSummary.benefitUtilization"
      },
      {
       "kind": "metricTile",
       "label": "Upgrade Rate",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 35 §Display"
      },
      {
       "kind": "metricTile",
       "label": "Freeze/Suspension Rate",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 35 §Display",
       "bindsTo": "MembershipAnalyticsRenewalIntelligenceAiRetentionCenSummary.freezeSuspensionRate"
      },
      {
       "kind": "metricTile",
       "label": "Expected Renewals",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 35 §Forecast",
       "bindsTo": "MembershipAnalyticsRenewalIntelligenceAiRetentionCenSummary.expectedRenewals"
      },
      {
       "kind": "metricTile",
       "label": "Expected Churn",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 35 §Forecast",
       "bindsTo": "MembershipAnalyticsRenewalIntelligenceAiRetentionCenSummary.expectedChurn"
      },
      {
       "kind": "metricTile",
       "label": "Renewal Revenue",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 35 §Forecast",
       "bindsTo": "MembershipAnalyticsRenewalIntelligenceAiRetentionCenSummary.renewalRevenue"
      },
      {
       "kind": "metricTile",
       "label": "Upgrade Revenue",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 35 §Forecast"
      },
      {
       "kind": "metricTile",
       "label": "Membership Base Growth",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 35 §Forecast",
       "bindsTo": "MembershipAnalyticsRenewalIntelligenceAiRetentionCenSummary.membershipBaseGrowth"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The membership analytics renewal list; the counts above it resolve separately.",
   "error": "Could not load. Names which read failed and leaves the membership analytics renewal untouched.",
   "emptyFirstRun": "No membership analytics renewal yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the membership analytics renewal are still there. The pack's own statuses are 5 Management — the state names which is selected.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listMembershipRenewalRetention",
    "contract": "subscription",
    "purpose": "Membership Analytics, Renewal Intelligence & AI Retention Center",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "MembershipAnalyticsRenewalIntelligenceAiRetentionCenSummary.activeMembers",
    "MembershipAnalyticsRenewalIntelligenceAiRetentionCenSummary.newMemberships",
    "MembershipAnalyticsRenewalIntelligenceAiRetentionCenSummary.renewalRate",
    "MembershipAnalyticsRenewalIntelligenceAiRetentionCenSummary.churnRate",
    "MembershipAnalyticsRenewalIntelligenceAiRetentionCenSummary.autoRenewSuccess",
    "MembershipAnalyticsRenewalIntelligenceAiRetentionCenSummary.averageMembershipTenure"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-303",
   "workshopBoard": "wireframes/WS83 Membership   Annual Pass Management Board 2.dc.html#bo-303"
  },
  "apisNote": "Regenerated 9 September 2026 from Membership___Annual_Pass_Management_Reference.pdf page 35. 15 of 23 labels bound to a contract property; 27 of 105 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
 "createApprovalRequest": {
  "method": "POST",
  "path": "/approval-requests",
  "contract": "approvals",
  "summary": "Raise a request",
  "permission": "APPROVAL_REQUEST",
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
  "requestBody": "CreateApprovalRequest",
  "responds": "ApprovalRequest"
 },
 "createMemberException": {
  "method": "POST",
  "path": "/memberships/{membershipId}/exceptions",
  "contract": "orders",
  "summary": "Record a member exception, override or service-recovery act",
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
  "requestBody": "MemberExceptionInput",
  "responds": "MemberExceptionView"
 },
 "freezeEntitlement": {
  "method": "POST",
  "path": "/entitlements/{entitlementId}/freeze",
  "contract": "catalogue",
  "summary": "Pause a membership at the guest's request",
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
  "responds": "Entitlement"
 },
 "listMember": {
  "method": "GET",
  "path": "/member",
  "contract": "subscription",
  "summary": "Member Operations Command Center",
  "permission": "PLATFORM_TENANT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
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
    "name": "status",
    "in": "query",
    "required": false
   },
   {
    "name": "activation",
    "in": "query",
    "required": false
   },
   {
    "name": "renewal",
    "in": "query",
    "required": false
   },
   {
    "name": "usage",
    "in": "query",
    "required": false
   },
   {
    "name": "memberType",
    "in": "query",
    "required": false
   },
   {
    "name": "expiringWithinDays",
    "in": "query",
    "required": false
   },
   {
    "name": "venue",
    "in": "query",
    "required": false
   },
   {
    "name": "tier",
    "in": "query",
    "required": false
   },
   {
    "name": "acquisitionChannel",
    "in": "query",
    "required": false
   },
   {
    "name": "atRisk",
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
 "listMemberExceptionOverride": {
  "method": "GET",
  "path": "/member-exception-override",
  "contract": "subscription",
  "summary": "Member Exceptions, Overrides & Service Recovery",
  "permission": "PLATFORM_TENANT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": "exceptionType",
    "in": "query",
    "required": false
   },
   {
    "name": "approvalStatus",
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
 "listMemberLifecycleCase": {
  "method": "GET",
  "path": "/member-lifecycle-case",
  "contract": "subscription",
  "summary": "Member Lifecycle History, Audit & Case Timeline",
  "permission": "PLATFORM_TENANT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": "membershipId",
    "in": "query",
    "required": false
   },
   {
    "name": "eventType",
    "in": "query",
    "required": false
   },
   {
    "name": "actorType",
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
 "listMembershipActivationCredential": {
  "method": "GET",
  "path": "/membership-activation-credential",
  "contract": "subscription",
  "summary": "Membership Activation, Assignment & Credential Management",
  "permission": "PLATFORM_TENANT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": "queueStage",
    "in": "query",
    "required": false
   },
   {
    "name": "membershipProduct",
    "in": "query",
    "required": false
   },
   {
    "name": "venue",
    "in": "query",
    "required": false
   },
   {
    "name": "search",
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
 "listMembershipFreezeSuspension": {
  "method": "GET",
  "path": "/membership-freeze-suspension",
  "contract": "subscription",
  "summary": "Membership Freeze, Suspension & Reactivation Management",
  "permission": "PLATFORM_TENANT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": "interruptionType",
    "in": "query",
    "required": false
   },
   {
    "name": "membershipId",
    "in": "query",
    "required": false
   },
   {
    "name": "activeOnly",
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
 "listMembershipRenewalRetention": {
  "method": "GET",
  "path": "/membership-renewal-retention",
  "contract": "subscription",
  "summary": "Membership Analytics, Renewal Intelligence & AI Retention Center",
  "permission": "PLATFORM_TENANT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": "membershipProduct",
    "in": "query",
    "required": false
   },
   {
    "name": "tier",
    "in": "query",
    "required": false
   },
   {
    "name": "venue",
    "in": "query",
    "required": false
   },
   {
    "name": "customerSegment",
    "in": "query",
    "required": false
   },
   {
    "name": "geography",
    "in": "query",
    "required": false
   },
   {
    "name": "renewalCohort",
    "in": "query",
    "required": false
   },
   {
    "name": "purchaseMonth",
    "in": "query",
    "required": false
   },
   {
    "name": "acquisitionChannel",
    "in": "query",
    "required": false
   },
   {
    "name": "churnFlag",
    "in": "query",
    "required": false
   },
   {
    "name": "maxRenewalProbability",
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
 "listMembershipUpgradeDowngrade": {
  "method": "GET",
  "path": "/membership-upgrade-downgrade",
  "contract": "subscription",
  "summary": "Membership Upgrade, Downgrade & Product Migration Operations",
  "permission": "PLATFORM_TENANT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": "movementType",
    "in": "query",
    "required": false
   },
   {
    "name": "membershipProduct",
    "in": "query",
    "required": false
   },
   {
    "name": "bulkMigrationId",
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
 "listRenewalAuto": {
  "method": "GET",
  "path": "/renewal-auto",
  "contract": "subscription",
  "summary": "Renewal Operations & Auto-Renewal Management",
  "permission": "PLATFORM_TENANT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": "renewalStatus",
    "in": "query",
    "required": false
   },
   {
    "name": "membershipProduct",
    "in": "query",
    "required": false
   },
   {
    "name": "tier",
    "in": "query",
    "required": false
   },
   {
    "name": "autoRenew",
    "in": "query",
    "required": false
   },
   {
    "name": "expiringFrom",
    "in": "query",
    "required": false
   },
   {
    "name": "expiringTo",
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
 "listVisitAdmissionEntitlement": {
  "method": "GET",
  "path": "/visit-admission-entitlement",
  "contract": "subscription",
  "summary": "Visit, Admission & Entitlement Usage Monitor",
  "permission": "PLATFORM_TENANT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": "membershipId",
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
    "name": "venue",
    "in": "query",
    "required": false
   },
   {
    "name": "validationResult",
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
 "migrateMembership": {
  "method": "POST",
  "path": "/memberships/{membershipId}/migrations",
  "contract": "orders",
  "summary": "Upgrade, downgrade or migrate an active membership to another product",
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
  "requestBody": "MembershipMigrationInput",
  "responds": "MembershipMigrationView"
 },
 "recordBenefitUsage": {
  "method": "POST",
  "path": "/memberships/{membershipId}/benefit-usage",
  "contract": "identity",
  "summary": "Consume a benefit",
  "permission": "GUEST_MANAGE",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "membershipId",
    "in": "path",
    "required": true
   },
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "IdentityBenefitUsage",
  "responds": "IdentityBenefitUsage"
 },
 "reinstateEntitlement": {
  "method": "POST",
  "path": "/entitlements/{entitlementId}/reinstate",
  "contract": "catalogue",
  "summary": "Lift a suspension",
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
  "responds": "Entitlement"
 },
 "renewMembership": {
  "method": "POST",
  "path": "/memberships/{membershipId}/renewals",
  "contract": "orders",
  "summary": "Renew a membership",
  "permission": "ORDER_MODIFY",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "membershipId",
    "in": "path",
    "required": true
   },
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "OrdersMembershipRenewal",
  "responds": "OrdersMembershipRenewal"
 },
 "resolveMembershipActivation": {
  "method": "POST",
  "path": "/memberships/{membershipId}/activation/resolve",
  "contract": "orders",
  "summary": "Act on a membership in the activation queue",
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
  "requestBody": "MembershipActivationActionInput",
  "responds": "MembershipActivationView"
 },
 "setMemberMembershipAccount": {
  "method": "PUT",
  "path": "/member-membership-account",
  "contract": "subscription",
  "summary": "Member 360° Membership Account Workspace",
  "permission": "PLATFORM_CELL_MANAGE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "Member360MembershipAccountWorkspaceInput",
  "responds": "Member360MembershipAccountWorkspaceView"
 },
 "suspendEntitlement": {
  "method": "POST",
  "path": "/entitlements/{entitlementId}/suspend",
  "contract": "catalogue",
  "summary": "Suspend or reinstate an entitlement",
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
  "requestBody": null,
  "responds": null
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "ApprovalDecision": {
  "type": "object",
  "x-ticvai-persistence": "approvals.decision",
  "required": [
   "level",
   "principalId",
   "decision",
   "decidedAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "description": "**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"
   },
   "level": {
    "type": "integer"
   },
   "principalId": {
    "type": "string",
    "format": "uuid"
   },
   "displayName": {
    "type": "string"
   },
   "isDelegate": {
    "type": "boolean"
   },
   "delegatedFrom": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "decision": {
    "type": "string",
    "enum": [
     "approve",
     "reject"
    ]
   },
   "comment": {
    "type": "string",
    "nullable": true
   },
   "reason": {
    "type": "string",
    "nullable": true
   },
   "usedMfa": {
    "type": "boolean"
   },
   "signatureRef": {
    "type": "string",
    "nullable": true
   },
   "decidedAt": {
    "type": "string",
    "format": "date-time"
   }
  }
 },
 "ApprovalKind": {
  "type": "string",
  "description": "11.1.7 and 11.1.30–11.1.37. **The first four already exist as bespoke implementations** and this contract is what they collapse into.\n**Which actions route here — decided 28 September, audit R144.** Finance and procurement acts go through this engine to a **finance approver**: closing a fiscal period (`periodClose`), reopening one (`periodReopen`), cancelling a purchase order (`purchaseOrderCancel`) and closing one short (`purchaseOrderShortClose`). The tenant default matrix for each of these names the finance approver role; a venue may tighten it and never loosen it. Starting a release rollout routes through `releasePromotion` to the platform release manager (a holder of `PLATFORM_RELEASE_PROMOTE`). **Not every `requiresApproval` goes here:** reopening a shift, recounting a stock count and a retail return above the venue threshold take a supervisor's step-up on the same device instead, and never raise a request.\n**Catalogue change requests route through `productChange` and `pricingChange`** (decided 29 September, writers pass): a product change and a price or pricing change raised in `catalogue` ask for approval under these two kinds, so a venue can route product edits and price edits to different approvers.\n",
  "enum": [
   "refund",
   "priceOverride",
   "discountOverride",
   "complimentaryTicket",
   "membershipCancellation",
   "accessPermissionChange",
   "configurationChange",
   "aiRecommendation",
   "releasePromotion",
   "requisition",
   "stockWriteOff",
   "journalEntry",
   "periodClose",
   "periodReopen",
   "purchaseOrderCancel",
   "purchaseOrderShortClose",
   "tenantMigration",
   "productChange",
   "pricingChange"
  ]
 },
 "ApprovalMode": {
  "type": "string",
  "description": "11.1.43–11.1.46. **Sequential** asks one at a time, **parallel** asks everyone at once, **consensus** needs all of them, **majority** needs more than half.\nParallel and consensus differ in when it completes: parallel completes on the first approval, consensus waits for all. Conflating them is how a four-eyes rule turns into a one-eye rule.\n",
  "enum": [
   "sequential",
   "parallel",
   "consensus",
   "majority"
  ]
 },
 "ApprovalRequest": {
  "type": "object",
  "x-ticvai-persistence": "approvals.request",
  "required": [
   "id",
   "kind",
   "status",
   "requestedByPrincipalId",
   "requestedAt"
  ],
  "properties": {
   "id": {
    "type": "string"
   },
   "kind": {
    "$ref": "#/components/schemas/ApprovalKind"
   },
   "rerouteOnNoApprover": {
    "type": "boolean",
    "default": true,
    "description": "BL-154. **An approver on leave is an approval that waits for them to come back.** Reroutes to the next in the chain rather than stalling — `workforce` already knows who is on leave, and an approval queue nobody is watching is the thing that stops a venue.\n"
   },
   "outOfOfficeDelegateId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "allowEmailApproval": {
    "type": "boolean",
    "default": false,
    "description": "**Approving from an email link with no second factor is the weakest path in the system**, so it is off by default and available only below a configured value.\n"
   },
   "reopenedFrom": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "**Reopening a decided approval creates a new one that points back.** Editing a decision in place destroys the record of what was originally approved, which is the only thing an audit wants.\n"
   },
   "status": {
    "$ref": "#/components/schemas/ApprovalStatus"
   },
   "subjectContract": {
    "type": "string"
   },
   "subjectType": {
    "type": "string"
   },
   "subjectId": {
    "type": "string"
   },
   "scopePath": {
    "type": "string"
   },
   "summary": {
    "type": "string"
   },
   "amount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "justification": {
    "type": "string",
    "nullable": true
   },
   "requestedByPrincipalId": {
    "type": "string",
    "format": "uuid"
   },
   "matrixVersion": {
    "type": "integer"
   },
   "mode": {
    "$ref": "#/components/schemas/ApprovalMode"
   },
   "currentLevel": {
    "type": "integer"
   },
   "totalLevels": {
    "type": "integer"
   },
   "pendingApprovers": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "principalId": {
       "type": "string",
       "format": "uuid"
      },
      "displayName": {
       "type": "string"
      },
      "isDelegate": {
       "type": "boolean"
      }
     }
    }
   },
   "decisions": {
    "type": "array",
    "description": "Every decision at every level, in order. **Immutable once the request completes** (11.1.56) — an approval is evidence, and amending one is a different fact.\n",
    "items": {
     "$ref": "#/components/schemas/ApprovalDecision"
    }
   },
   "escalations": {
    "type": "array",
    "description": "11.1.48. Who was asked, when, and why it moved up. **Escalation adds an approver rather than replacing one**, so the original stays in the record.\n",
    "items": {
     "type": "object",
     "properties": {
      "at": {
       "type": "string",
       "format": "date-time"
      },
      "reason": {
       "type": "string"
      },
      "fromLevel": {
       "type": "integer"
      },
      "toLevel": {
       "type": "integer"
      },
      "wasAutomatic": {
       "type": "boolean"
      }
     }
    }
   },
   "resubmittedFromId": {
    "type": "string",
    "nullable": true
   },
   "reopenedFromId": {
    "type": "string",
    "nullable": true
   },
   "slaDueAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "slaBreached": {
    "type": "boolean"
   },
   "expiresAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "requestedAt": {
    "type": "string",
    "format": "date-time"
   },
   "completedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "aiAssessment": {
    "type": "object",
    "nullable": true,
    "readOnly": true,
    "description": "**AI context for the reviewer, never an input to the decision** (11.1.73 to 11.1.75; MoM 8 September; 29 September, build pass, group G2). Written by approvals from `ai.scoreApprovalRequest` on submit and on each SLA tick; null where AI is off or has not answered. Shown on the request labelled as AI; orders the inbox only when `sort=aiPriority` is asked for.",
    "properties": {
     "riskScore": {
      "type": "integer",
      "minimum": 0,
      "maximum": 100
     },
     "riskBand": {
      "type": "string",
      "enum": [
       "low",
       "medium",
       "high",
       "critical"
      ]
     },
     "priorityScore": {
      "type": "integer",
      "minimum": 0,
      "maximum": 100
     },
     "escalationSuggestion": {
      "type": "object",
      "description": "A suggestion a person may act on through `escalateApprovalRequest`, or the tenant's own SLA policy may; nothing escalates because of it.",
      "properties": {
       "action": {
        "type": "string",
        "enum": [
         "escalate",
         "addBackupApprover",
         "none"
        ]
       },
       "reason": {
        "type": "string",
        "nullable": true
       }
      }
     },
     "signals": {
      "type": "array",
      "maxItems": 10,
      "description": "The signals behind the scores, largest first, as `ai.AiApprovalRequestScore.signals`.",
      "items": {
       "type": "object",
       "properties": {
        "code": {
         "type": "string"
        },
        "contribution": {
         "type": "number"
        },
        "detail": {
         "type": "string",
         "nullable": true
        }
       }
      }
     },
     "scoreId": {
      "type": "string",
      "format": "uuid",
      "description": "The `ai.approval_request_score` row it was copied from; `ai.getApprovalRequestScore` gives the full context. Not a foreign key (the score lives in the AI service)."
     },
     "decisionRecordId": {
      "type": "string",
      "description": "The ai decision record, for the audit of what the AI said and why."
     },
     "assessedAt": {
      "type": "string",
      "format": "date-time"
     }
    }
   }
  }
 },
 "ApprovalStatus": {
  "type": "string",
  "enum": [
   "draft",
   "pending",
   "escalated",
   "returned",
   "informationRequested",
   "approved",
   "rejected",
   "withdrawn",
   "expired",
   "cancelled"
  ]
 },
 "CreateApprovalRequest": {
  "type": "object",
  "x-ticvai-persistence": "none — request only",
  "required": [
   "id",
   "kind",
   "subjectContract",
   "subjectType",
   "subjectId",
   "scopePath",
   "summary"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "kind": {
    "$ref": "#/components/schemas/ApprovalKind"
   },
   "subjectContract": {
    "type": "string",
    "description": "Which contract owns the thing being approved."
   },
   "subjectType": {
    "type": "string"
   },
   "subjectId": {
    "type": "string",
    "description": "**A reference, never a copy.** A copy goes stale between raising and deciding, and an approver reading a stale copy approves something that no longer exists.\n"
   },
   "scopePath": {
    "type": "string"
   },
   "summary": {
    "type": "string",
    "maxLength": 300,
    "description": "What the approver sees in their queue before opening it."
   },
   "amount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "attributes": {
    "type": "object",
    "additionalProperties": true
   },
   "justification": {
    "type": "string",
    "maxLength": 1000
   },
   "isDraft": {
    "type": "boolean",
    "default": false,
    "description": "True saves the request at `draft` without routing it; `submitApprovalRequest` sends it later (decided 28 September, audit R129).\n"
   }
  }
 },
 "Entitlement": {
  "type": "object",
  "x-ticvai-persistence": "access.entitlement",
  "description": "**What a guest actually holds.** Found missing on 18 August by the schema audit — 33 tables in `orders`, seven in `access`, and none of them stored an issued ticket.\nThe package sold products, defined `EntitlementTemplate`, recorded `ScanEvent.ticketId`, transferred `ticket_transfer.ticketIds` and issued `wallet_pass.entitlementId` — **five artefacts referring to a thing that did not exist.** `validateAccess` read the *template* and never the instance, and `suspendEntitlement` suspended the template, **which would have suspended it for every guest who held one.**\n**The template is the definition and this is the instance.** A template says *an annual pass admits once a day for a year*; this says *this guest's annual pass, bought on 3 March, used eleven times, frozen for two weeks in July, valid until 2 March.*\n",
  "required": [
   "id",
   "templateId",
   "productId",
   "orderId",
   "subjectId",
   "status",
   "validFrom",
   "validTo"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "description": "A UUIDv7, matching `TicketStatus.ticketId` — **stable for the life of the ticket and independent of the media carrying it.** A guest whose wristband broke keeps the same entitlement with a new `mediaCode`.\n**This is the ticket id.** Wherever an operation takes a `ticketId` or `ticketIds` — `lookupTicket`, `listScans`, `ScanEvent`, the offline package and `transferOrderTickets` — it is this value. An order line's `entitlementIds` are the ticket ids of that line.\n"
   },
   "templateId": {
    "type": "string",
    "format": "uuid",
    "description": "The definition it was issued against. **Pinned at issue** — a template edited next month must not change what this guest bought.\n"
   },
   "productId": {
    "type": "string",
    "format": "uuid"
   },
   "orderId": {
    "type": "string",
    "format": "uuid",
    "description": "The order's id, a UUIDv7 as in `/orders/{orderId}` (`orders.sales_order.id`)."
   },
   "orderLineId": {
    "type": "string",
    "format": "uuid"
   },
   "subjectId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Who holds it. **Null is legitimate** — a ticket bought as a gift or sold at a till to somebody who gave no details has no subject until it is claimed.\n"
   },
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "scopePath": {
    "type": "string"
   },
   "mediaCode": {
    "type": "string",
    "description": "What is scanned — a QR payload, a wristband serial, a card number. **Rotatable without reissuing**, because a guest whose wristband broke should not need a new ticket.\n"
   },
   "status": {
    "$ref": "../spine/orders.yaml#/components/schemas/EntitlementStatus"
   },
   "statusNote": {
    "type": "string",
    "nullable": true,
    "description": "**Not `TicketStatus` — that is a validation result with a misleading name**, computed at scan time and carrying `isValid` and `isInsideVenue`. The lifecycle is `orders.EntitlementStatus`, and `states/entitlement-status.yaml` has modelled it since before this table existed.\n**Which is the finding in one line: the package had the lifecycle, the state model and the validation result, and no row to hang them on.**\n"
   },
   "validFrom": {
    "type": "string",
    "format": "date-time"
   },
   "validTo": {
    "type": "string",
    "format": "date-time",
    "description": "**Resolved at issue from the template, then owned here.** A freeze extends it, a reissue replaces it, and neither reaches back to the template.\n**What the pre-expiry notice is measured from** (29 September, build pass, group G2; 5.5.30). A daily run in access publishes `entitlement.expiringSoon` once per entitlement and `validTo` when an entitlement in `issued` or `partiallyConsumed` comes within its template's `expiryNoticeDays` (`catalogue.EntitlementTemplate`), and not for one bought inside that window. Marketing turns it into the reminder (a `MessageTrigger` on the event, or a triggered campaign on `entitlementExpiring`); access only says the date is near. A freeze or renewal that moves `validTo` raises the next notice once.\n"
   },
   "entriesUsed": {
    "type": "integer",
    "default": 0,
    "readOnly": true,
    "x-ticvai-derived": "onWrite",
    "description": "**The number `validateAccess` decrements and nothing was decrementing.** A ten-entry pass with no counter is a ten-entry pass that admits forever.\n**Maintained on write**, in the same transaction as the admitting `access.scan_event` row: by `validateAccess`, `validateGroupAccess` (by the count admitted) and `syncScans` for each replayed admission the server accepts. A replayed scan the server downgrades to `denied` does not count.\n"
   },
   "entriesAllowed": {
    "type": "integer",
    "nullable": true
   },
   "lastEntryAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true,
    "x-ticvai-derived": "onWrite",
    "description": "`recordedAt` of the latest admission counted in `entriesUsed`, written by the same writes. A scan replayed late with an earlier `recordedAt` does not move it back.\n"
   },
   "frozenDays": {
    "type": "integer",
    "default": 0,
    "readOnly": true,
    "x-ticvai-derived": "onWrite",
    "description": "Days added by a freeze. **Maintained on write** by the freeze operation (`freezeEntitlement`), in the same write that extends `validTo` by those days. **Held here rather than computed from a freeze log**, because a gate has to answer in under 300ms and cannot replay a history to decide validity.\n"
   },
   "suspendedReason": {
    "type": "string",
    "nullable": true
   },
   "freezeReason": {
    "type": "string",
    "nullable": true,
    "enum": [
     "travelling",
     "injury",
     "personal",
     "seasonal",
     "other"
    ],
    "description": "The `reason` of the latest `freezeEntitlement` (audit R222). Null when never frozen."
   },
   "freezeNote": {
    "type": "string",
    "nullable": true,
    "maxLength": 500,
    "description": "The `note` the latest `freezeEntitlement` took, required there when `reason` is `other` (decided 28 September, audit R222). Kept so the quarterly review of `other` notes has something to read."
   },
   "isNameBound": {
    "type": "boolean",
    "default": false
   },
   "holderName": {
    "type": "string",
    "nullable": true
   },
   "sharedWithSubjectIds": {
    "type": "array",
    "description": "`shareEntitlement`. **The owner keeps it and a second person may present it** — the asymmetry that stops a shared family pass becoming a resale chain.\n",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "issuedVia": {
    "type": "string",
    "enum": [
     "sale",
     "invitation",
     "reissue",
     "transfer",
     "resale",
     "membership",
     "groupBooking"
    ],
    "description": "**How it came to exist, and it matters to finance.** A sold entitlement carries deferred revenue; an invitation carries a marketing cost; a reissue carries neither.\n"
   },
   "supersedesEntitlementId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "For a reissue or a resale. **The chain is traceable** — a ticket appearing from nowhere is indistinguishable from a fraudulent one.\n"
   },
   "walletValueId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Where the template carries stored value. **A `retail.Wallet` bound to the entitlement, not a balance on it** (CF-126).\n"
   },
   "facePassEnrolmentId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true,
    "x-ticvai-persisted": false,
    "x-ticvai-derived": "onRead",
    "description": "The active `facePass` enrolment on this entitlement (`FacePassEnrolment.id`), or null when none is. **Computed on read from `pii.subject_biometric` and not stored here** — the PII split keeps the biometric on its own side, and this carries only its id. It is how a screen holding a pass finds the enrolment `getFacePassEnrolment` and `revokeFacePass` take.\n"
   }
  }
 },
 "IdentityBenefitUsage": {
  "type": "object",
  "x-ticvai-persistence": "identity.benefit_usage",
  "description": "**Taken from the backend workbook, 20 September.** Tracks each use of a customer's membership benefit and the remaining allowance.",
  "required": [
   "customerMembershipId",
   "membershipBenefitId",
   "quantity",
   "usedAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "customerMembershipId": {
    "type": "string",
    "format": "uuid"
   },
   "membershipBenefitId": {
    "type": "string",
    "format": "uuid"
   },
   "quantity": {
    "type": "number"
   },
   "sourceType": {
    "type": "string",
    "maxLength": 30,
    "nullable": true
   },
   "sourceOrderId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "usedAt": {
    "type": "string",
    "format": "date-time"
   },
   "remainingQuantity": {
    "type": "number",
    "nullable": true,
    "readOnly": true,
    "description": "Written on the row by the server when the usage is recorded; ignored in a request."
   },
   "notes": {
    "type": "string",
    "maxLength": 500,
    "nullable": true
   }
  }
 },
 "Member360MembershipAccountWorkspaceInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures",
  "description": "**What Member 360° Membership Account Workspace submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "membershipId": {
    "type": "string",
    "description": "Membership ID the action applies to"
   },
   "action": {
    "type": "string",
    "enum": [
     "activate",
     "freeze",
     "suspend",
     "resume",
     "renew",
     "replaceCredential",
     "addNote",
     "reviewEligibility",
     "manageDependents"
    ],
    "description": "Operational Action (pack pp.23-24)"
   },
   "reason": {
    "type": "string",
    "description": "Reason; required for freeze, suspend and resume",
    "nullable": true
   },
   "note": {
    "type": "string",
    "description": "Case note text, for addNote",
    "nullable": true
   },
   "effectiveDate": {
    "type": "string",
    "format": "date",
    "description": "Effective date, e.g. freeze start",
    "nullable": true
   },
   "endDate": {
    "type": "string",
    "format": "date",
    "description": "Freeze end date",
    "nullable": true
   }
  }
 },
 "Member360MembershipAccountWorkspaceView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over subscription state, assembled at read time from tables that already exist",
  "description": "**What Member 360° Membership Account Workspace displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "memberName": {
    "type": "string",
    "description": "Member Name"
   },
   "customerId": {
    "type": "string",
    "description": "Customer ID"
   },
   "membershipId": {
    "type": "string",
    "description": "Membership ID"
   },
   "membershipProduct": {
    "type": "string",
    "description": "Membership Product"
   },
   "tier": {
    "type": "string",
    "description": "Tier"
   },
   "status": {
    "type": "string",
    "description": "Status: one of the membership lifecycle values active, frozen, suspended, expired or cancelled (shape follows catalogue GuestMembership.status; states/guest-membership-status.yaml): frozen is the member's pause and extends validity, suspended is a sanction and does not"
   },
   "activationDate": {
    "type": "string",
    "format": "date",
    "description": "Activation Date",
    "nullable": true
   },
   "expiryDate": {
    "type": "string",
    "format": "date",
    "description": "Expiry Date",
    "nullable": true
   },
   "renewalStatus": {
    "type": "string",
    "description": "Renewal Status: renewalNotOpen, renewalEligible, renewalInvitationSent, renewalStarted, paymentPending, renewed, autoRenewScheduled, autoRenewFailed, gracePeriod or expiredWithoutRenewal (pack p.30 Renewal Pipeline)"
   },
   "primaryVenue": {
    "type": "string",
    "description": "Primary Venue"
   },
   "credentialStatus": {
    "type": "string",
    "description": "Credential Status: notIssued, active, disabled or replaced"
   },
   "primaryMember": {
    "type": "string",
    "description": "Primary Member"
   },
   "secondaryAdult": {
    "type": "string",
    "description": "Secondary Adult name",
    "nullable": true
   },
   "dependents": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "customerId": {
       "type": "string"
      },
      "name": {
       "type": "string"
      },
      "role": {
       "type": "string",
       "enum": [
        "primaryMember",
        "secondaryAdult",
        "dependent",
        "child",
        "guardian",
        "authorizedManager"
       ]
      }
     }
    },
    "description": "Dependents on the membership"
   },
   "sharedBenefits": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "entitlementType": {
       "type": "string",
       "enum": [
        "unlimitedAdmission",
        "limitedAdmissions",
        "attractionAccess",
        "eventAccess",
        "zoneAccess",
        "fastTrack",
        "priorityEntry",
        "guestTickets",
        "parking",
        "fnbBenefit",
        "retailBenefit",
        "rentalBenefit",
        "specialEventAccess",
        "bookingPrivileges",
        "other"
       ]
      },
      "allocation": {
       "type": "integer",
       "nullable": true,
       "description": "Empty for unlimited"
      },
      "used": {
       "type": "integer"
      },
      "remaining": {
       "type": "integer",
       "nullable": true,
       "description": "Empty for unlimited"
      },
      "value": {
       "type": "string",
       "nullable": true,
       "description": "Display value of a discount benefit, from its pricing rule"
      }
     }
    },
    "description": "Shared Benefits with allocation, used and remaining"
   },
   "individualBenefits": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "entitlementType": {
       "type": "string",
       "enum": [
        "unlimitedAdmission",
        "limitedAdmissions",
        "attractionAccess",
        "eventAccess",
        "zoneAccess",
        "fastTrack",
        "priorityEntry",
        "guestTickets",
        "parking",
        "fnbBenefit",
        "retailBenefit",
        "rentalBenefit",
        "specialEventAccess",
        "bookingPrivileges",
        "other"
       ]
      },
      "allocation": {
       "type": "integer",
       "nullable": true,
       "description": "Empty for unlimited"
      },
      "used": {
       "type": "integer"
      },
      "remaining": {
       "type": "integer",
       "nullable": true,
       "description": "Empty for unlimited"
      },
      "value": {
       "type": "string",
       "nullable": true,
       "description": "Display value of a discount benefit, from its pricing rule"
      }
     }
    },
    "description": "Individual Benefits with allocation, used and remaining"
   },
   "membershipVersion": {
    "type": "integer",
    "description": "Membership Version the contract is on"
   },
   "purchaseDate": {
    "type": "string",
    "format": "date",
    "description": "Purchase Date"
   },
   "purchaseChannel": {
    "$ref": "../shared/common.yaml#/components/schemas/SalesChannel",
    "description": "Purchase Channel"
   },
   "originalOrder": {
    "type": "string",
    "description": "Original Order id"
   },
   "validity": {
    "type": "string",
    "enum": [
     "fixedCalendar",
     "durationFromPurchase",
     "durationFromActivation",
     "seasonBased",
     "customPeriod"
    ],
    "description": "Validity method"
   },
   "activationMethod": {
    "type": "string",
    "enum": [
     "immediateOnPurchase",
     "fixedStartDate",
     "firstVisit",
     "manualActivation",
     "customerActivation",
     "membershipCardCollection",
     "identityVerification",
     "configuredTrigger"
    ],
    "description": "Activation Method"
   },
   "renewalPolicy": {
    "type": "string",
    "description": "Renewal Policy: the product's renewal modes, e.g. customerSelfService and autoRenewal"
   },
   "autoRenewStatus": {
    "type": "string",
    "description": "Auto-Renew Status: off, optedIn, scheduled or failed; only the member's explicit opt-in sets optedIn"
   },
   "frozenDays": {
    "type": "integer",
    "description": "Days lost to a freeze and added back to the expiry (follows catalogue GuestMembership.frozenDays)"
   },
   "relatedTransactions": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "kind": {
       "type": "string",
       "enum": [
        "order",
        "payment",
        "renewal",
        "upgrade",
        "refund",
        "membershipChange"
       ]
      },
      "id": {
       "type": "string"
      },
      "occurredAt": {
       "type": "string",
       "format": "date-time"
      }
     }
    },
    "description": "Related Transactions (pack p.23)"
   },
   "aiSummary": {
    "type": "string",
    "description": "AI Member Summary, advisory",
    "nullable": true
   }
  }
 },
 "MemberExceptionInput": {
  "type": "object",
  "x-ticvai-persistence": "none — request only",
  "description": "What `createMemberException` takes. The eight kinds are the pack's own labels on BO-301 (decided 29 September, readiness close-out).\n",
  "required": [
   "kind",
   "reason"
  ],
  "properties": {
   "kind": {
    "type": "string",
    "description": "The exception kind (decided 29 September, readiness close-out). `complimentaryRenewal` and `complimentaryBenefit` move money and need an approved `approvalRequestId`.",
    "enum": [
     "eligibilityOverride",
     "expiryExtension",
     "complimentaryRenewal",
     "complimentaryBenefit",
     "entitlementAdjustment",
     "freezeException",
     "suspensionOverride",
     "replacementCredential"
    ]
   },
   "reason": {
    "type": "string",
    "minLength": 3,
    "maxLength": 500
   },
   "approvalRequestId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The approved request in `approvals`. Required for `complimentaryRenewal` and `complimentaryBenefit`."
   },
   "extendDays": {
    "type": "integer",
    "minimum": 1,
    "maximum": 366,
    "nullable": true,
    "description": "Required for `expiryExtension`."
   },
   "benefitId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The plan benefit (`catalogue.membership_benefit`). Required for `complimentaryBenefit` and `entitlementAdjustment`."
   },
   "quantity": {
    "type": "integer",
    "minimum": 1,
    "nullable": true,
    "description": "How many of the benefit. Required with `benefitId`."
   }
  }
 },
 "MemberExceptionView": {
  "type": "object",
  "x-ticvai-persistence": "orders.member_exception",
  "description": "**One exception made to a membership, and who made it.** Written by `createMemberException` (decided 29 September, readiness close-out); the audit trail a membership that behaves outside its plan is explained from.\n",
  "required": [
   "id",
   "membershipId",
   "kind",
   "reason",
   "recordedAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "membershipId": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "description": "The membership in the path."
   },
   "kind": {
    "type": "string",
    "enum": [
     "eligibilityOverride",
     "expiryExtension",
     "complimentaryRenewal",
     "complimentaryBenefit",
     "entitlementAdjustment",
     "freezeException",
     "suspensionOverride",
     "replacementCredential"
    ]
   },
   "reason": {
    "type": "string",
    "maxLength": 500
   },
   "approvalRequestId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "extendDays": {
    "type": "integer",
    "nullable": true
   },
   "benefitId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "quantity": {
    "type": "integer",
    "nullable": true
   },
   "newExpiryAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true,
    "description": "With `expiryExtension` or `complimentaryRenewal`, the membership's expiry after the exception."
   },
   "recordedBy": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "description": "The principal who made the exception."
   },
   "recordedAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   }
  }
 },
 "MemberExceptionsOverridesServiceRecoveryView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over subscription state, assembled at read time from tables that already exist",
  "description": "**What Member Exceptions, Overrides & Service Recovery displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "member": {
    "type": "string",
    "description": "Member"
   },
   "membership": {
    "type": "string",
    "description": "Membership"
   },
   "requestedAction": {
    "type": "string",
    "description": "Requested Action"
   },
   "standardPolicyResult": {
    "type": "string",
    "description": "Standard Policy Result"
   },
   "requestedException": {
    "type": "string",
    "description": "Requested Exception"
   },
   "reason": {
    "type": "string",
    "description": "Reason"
   },
   "supportingDocumentation": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Supporting Documentation: document ids"
   },
   "financialImpact": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "nullable": true,
    "description": "Financial Impact of the exception"
   },
   "entitlementImpact": {
    "type": "string",
    "description": "Entitlement Impact"
   },
   "requestor": {
    "type": "string",
    "description": "Requestor"
   },
   "exceptionType": {
    "type": "string",
    "enum": [
     "eligibilityOverride",
     "activationExtension",
     "expiryExtension",
     "complimentaryRenewal",
     "complimentaryBenefit",
     "entitlementAdjustment",
     "freezeException",
     "suspensionOverride",
     "replacementCredential",
     "renewalException",
     "dependentException"
    ],
    "description": "Exception Type (pack p.32)"
   },
   "exceptionValue": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "nullable": true,
    "description": "Value used for approval routing"
   },
   "durationDays": {
    "type": "integer",
    "description": "Duration in days, for extensions",
    "nullable": true
   },
   "membershipTier": {
    "type": "string",
    "description": "Membership Tier"
   },
   "exceptionId": {
    "type": "string",
    "description": "Exception ID"
   },
   "approvalStatus": {
    "type": "string",
    "description": "Approval status: pending, approved, rejected or applied"
   },
   "approver": {
    "type": "string",
    "description": "Approver; must differ from the requestor for high-value exceptions",
    "nullable": true
   },
   "remedy": {
    "type": "string",
    "enum": [
     "extendMembership",
     "guestTicket",
     "complimentaryVisit",
     "feeWaiver",
     "benefitCredit",
     "renewalDiscount",
     "alternativeEntitlement"
    ],
    "description": "Service Recovery remedy (pack p.33)",
    "nullable": true
   },
   "aiSuggestion": {
    "type": "string",
    "description": "AI suggestion, advisory",
    "nullable": true
   }
  }
 },
 "MemberLifecycleHistoryAuditCaseTimelineView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over subscription state, assembled at read time from tables that already exist",
  "description": "**What Member Lifecycle History, Audit & Case Timeline displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "eventId": {
    "type": "string",
    "description": "Event id"
   },
   "membershipId": {
    "type": "string",
    "description": "Membership ID"
   },
   "occurredAt": {
    "type": "string",
    "format": "date-time",
    "description": "When it happened"
   },
   "eventType": {
    "type": "string",
    "enum": [
     "purchase",
     "assignment",
     "activation",
     "visit",
     "benefitUsage",
     "dependentChange",
     "credentialChange",
     "freeze",
     "suspension",
     "reactivation",
     "upgrade",
     "downgrade",
     "renewal",
     "exception",
     "expiry",
     "cancellation",
     "caseNote"
    ],
    "description": "Event (pack pp.33-34)"
   },
   "field": {
    "type": "string",
    "description": "Changed field for configuration-sensitive changes, e.g. expiry",
    "nullable": true
   },
   "previousValue": {
    "type": "string",
    "description": "Previous Value",
    "nullable": true
   },
   "newValue": {
    "type": "string",
    "description": "New Value",
    "nullable": true
   },
   "reason": {
    "type": "string",
    "description": "Reason",
    "nullable": true
   },
   "actorType": {
    "type": "string",
    "enum": [
     "customer",
     "agent",
     "manager",
     "system",
     "api",
     "integration"
    ],
    "description": "Actor (pack p.34)"
   },
   "actorName": {
    "type": "string",
    "description": "Actor name or id",
    "nullable": true
   },
   "relatedTransactions": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "kind": {
       "type": "string",
       "enum": [
        "order",
        "payment",
        "ticket",
        "reservation",
        "accessEvent",
        "approval",
        "case",
        "credential"
       ]
      },
      "id": {
       "type": "string"
      }
     }
    },
    "description": "Related Transactions (pack p.34)"
   },
   "note": {
    "type": "string",
    "description": "Case note text, for caseNote events",
    "nullable": true
   }
  }
 },
 "MemberOperationsCommandCenterSummary": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection; the headline tiles over the list, computed at read time for the filters in force",
  "description": "**The headline figures on Member Operations Command Center.** The pack's KPI cards, split out of the row (decided 29 September, readiness close-out): a count describes the list, not each item in it.",
  "properties": {
   "activeMembers": {
    "type": "integer",
    "description": "Active Members"
   },
   "newMembersToday": {
    "type": "integer",
    "description": "New Members Today"
   },
   "activatedToday": {
    "type": "integer",
    "description": "Activated Today"
   },
   "pendingActivation": {
    "type": "integer",
    "description": "Pending Activation"
   },
   "expiringIn30Days": {
    "type": "integer",
    "description": "Expiring in 30 Days"
   },
   "renewalDue": {
    "type": "integer",
    "description": "Renewal Due: memberships inside their renewal window and not yet renewed"
   },
   "renewedThisMonth": {
    "type": "integer",
    "description": "Renewed This Month"
   },
   "renewalRate": {
    "type": "number",
    "description": "Renewal Rate: percentage of memberships that expired in the last 12 months and were renewed (decided 29 September, readiness close-out)"
   },
   "suspendedMemberships": {
    "type": "integer",
    "description": "Suspended Memberships"
   },
   "frozenMemberships": {
    "type": "integer",
    "description": "Frozen Memberships"
   },
   "membershipExceptions": {
    "type": "integer",
    "description": "Membership Exceptions"
   },
   "atRiskMembers": {
    "type": "integer",
    "description": "At-Risk Members: includes annual-pass holders with no visit in the last 90 days, flagged for churn follow-up (MoM 8 Sep)"
   },
   "operationalAlerts": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Operational Alerts (pack p.21), e.g. memberships expiring within seven days, purchases unactivated over 30 days, dependents needing eligibility review"
   },
   "aiInsights": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "AI Assistance: advisory observations only; never applied automatically (pack AI sections)"
   }
  }
 },
 "MemberOperationsCommandCenterView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over subscription state, assembled at read time from tables that already exist",
  "description": "**What Member Operations Command Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "membershipId": {
    "type": "string",
    "description": "Membership ID"
   },
   "member": {
    "type": "string",
    "description": "Member name"
   },
   "membershipProduct": {
    "type": "string",
    "description": "Membership Product"
   },
   "tier": {
    "type": "string",
    "description": "Tier"
   },
   "venue": {
    "type": "string",
    "description": "Venue"
   },
   "activationDate": {
    "type": "string",
    "format": "date",
    "description": "Activation Date",
    "nullable": true
   },
   "expiryDate": {
    "type": "string",
    "format": "date",
    "description": "Expiry Date",
    "nullable": true
   },
   "membershipStatus": {
    "type": "string",
    "description": "Membership Status: one of the membership lifecycle values active, frozen, suspended, expired or cancelled (shape follows catalogue GuestMembership.status; states/guest-membership-status.yaml): frozen is the member's pause and extends validity, suspended is a sanction and does not; empty until activated (see activationStage)",
    "nullable": true
   },
   "usageLevel": {
    "type": "string",
    "enum": [
     "none",
     "low",
     "regular",
     "high"
    ],
    "description": "Usage Level over the last 90 days: none = no visit, low = 1-2 visits, regular = 3-9, high = 10 or more (decided 29 September, readiness close-out)"
   },
   "renewalStatus": {
    "type": "string",
    "description": "Renewal Status: renewalNotOpen, renewalEligible, renewalInvitationSent, renewalStarted, paymentPending, renewed, autoRenewScheduled, autoRenewFailed, gracePeriod or expiredWithoutRenewal (pack p.30 Renewal Pipeline)"
   },
   "outstandingIssue": {
    "type": "string",
    "description": "Outstanding Issue, e.g. dependent eligibility review or failed payment",
    "nullable": true
   },
   "owner": {
    "type": "string",
    "description": "Owner"
   },
   "customerId": {
    "type": "string",
    "description": "Customer ID of the member (CRM profile)"
   },
   "activationStage": {
    "type": "string",
    "enum": [
     "purchased",
     "pendingAssignment",
     "pendingActivation",
     "activated"
    ],
    "description": "Activation stage before the lifecycle starts (pack p.21: Purchased, Pending Assignment, Pending Activation)"
   },
   "atRisk": {
    "type": "boolean",
    "description": "Flagged at risk, e.g. no visit in the last 90 days (MoM 8 Sep)"
   }
  }
 },
 "MembershipActivationActionInput": {
  "type": "object",
  "x-ticvai-persistence": "none — request only",
  "description": "What `resolveMembershipActivation` takes (decided 29 September, readiness close-out).",
  "required": [
   "action"
  ],
  "properties": {
   "action": {
    "type": "string",
    "description": "The activation-queue action (decided 29 September, readiness close-out).",
    "enum": [
     "activate",
     "block",
     "review",
     "replace",
     "link",
     "escalate"
    ]
   },
   "credentialId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The credential being replaced. Required for `replace`."
   },
   "mediaCode": {
    "type": "string",
    "maxLength": 100,
    "nullable": true,
    "description": "The new media's code. Required for `replace`."
   },
   "subjectId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The guest the membership is linked to. Required for `link`."
   },
   "reason": {
    "type": "string",
    "minLength": 3,
    "maxLength": 500,
    "nullable": true,
    "description": "Required for `block` and `escalate`."
   }
  }
 },
 "MembershipActivationAssignmentCredentialManagementView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over subscription state, assembled at read time from tables that already exist",
  "description": "**What Membership Activation, Assignment & Credential Management displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "purchaseDate": {
    "type": "string",
    "format": "date",
    "description": "Purchase Date"
   },
   "eligibleActivationDate": {
    "type": "string",
    "format": "date",
    "description": "Eligible Activation Date"
   },
   "activationDeadline": {
    "type": "string",
    "format": "date",
    "description": "Activation Deadline; an unactivated membership expires here",
    "nullable": true
   },
   "selectedStartDate": {
    "type": "string",
    "format": "date",
    "description": "Selected Start Date",
    "nullable": true
   },
   "calculatedExpiry": {
    "type": "string",
    "format": "date",
    "description": "Calculated Expiry",
    "nullable": true
   },
   "activationMethod": {
    "type": "string",
    "enum": [
     "immediateOnPurchase",
     "fixedStartDate",
     "firstVisit",
     "manualActivation",
     "customerActivation",
     "membershipCardCollection",
     "identityVerification",
     "configuredTrigger"
    ],
    "description": "Activation Method"
   },
   "failureReason": {
    "type": "string",
    "enum": [
     "eligibilityFailed",
     "missingDocumentation",
     "duplicateMembership",
     "credentialFailure",
     "configurationIssue"
    ],
    "description": "Vocabulary listed under Record reason."
   },
   "membershipId": {
    "type": "string",
    "description": "Membership ID"
   },
   "membershipProduct": {
    "type": "string",
    "description": "Membership product name"
   },
   "purchaserCustomerId": {
    "type": "string",
    "description": "Customer who bought it"
   },
   "memberCustomerId": {
    "type": "string",
    "description": "Customer it is assigned to; empty until assigned",
    "nullable": true
   },
   "queueStage": {
    "type": "string",
    "enum": [
     "awaitingMemberAssignment",
     "awaitingIdentityVerification",
     "awaitingDocumentVerification",
     "awaitingActivation",
     "activationFailed"
    ],
    "description": "Activation Queue stage (pack p.24)"
   },
   "requiredChecks": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "check": {
       "type": "string",
       "enum": [
        "eligibility",
        "age",
        "residency",
        "identity",
        "photograph",
        "requiredDocuments",
        "dependentRelationship",
        "termsAcceptance"
       ]
      },
      "result": {
       "type": "string",
       "enum": [
        "pending",
        "passed",
        "failed",
        "notRequired"
       ]
      }
     }
    },
    "description": "Required Checks per Board 1 configuration (pack p.24)"
   },
   "credentialTypes": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "dynamicQr",
      "barcode",
      "rfid",
      "nfc",
      "digitalMembershipCard",
      "walletPass",
      "physicalCard"
     ]
    },
    "description": "Credential Assignment (pack p.25)"
   },
   "duplicateOf": {
    "type": "string",
    "description": "Duplicate Membership Detection: the membership ID the customer already holds",
    "nullable": true
   },
   "duplicateAction": {
    "type": "string",
    "enum": [
     "block",
     "review",
     "replace",
     "link",
     "escalate"
    ],
    "description": "Configured action on a duplicate",
    "nullable": true
   }
  }
 },
 "MembershipActivationView": {
  "type": "object",
  "x-ticvai-persistence": "orders.membership_activation_action",
  "description": "**One action taken on a membership in the activation queue.** Written by `resolveMembershipActivation` (decided 29 September, readiness close-out).\n",
  "required": [
   "id",
   "membershipId",
   "action",
   "recordedAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "membershipId": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "action": {
    "type": "string",
    "enum": [
     "activate",
     "block",
     "review",
     "replace",
     "link",
     "escalate"
    ]
   },
   "credentialId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "mediaCode": {
    "type": "string",
    "maxLength": 100,
    "nullable": true
   },
   "subjectId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "reason": {
    "type": "string",
    "maxLength": 500,
    "nullable": true
   },
   "membershipStatus": {
    "type": "string",
    "maxLength": 30,
    "readOnly": true,
    "description": "The membership's status after the action."
   },
   "recordedBy": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "recordedAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   }
  }
 },
 "MembershipAnalyticsRenewalIntelligenceAiRetentionCenSummary": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection; the headline tiles over the list, computed at read time for the filters in force",
  "description": "**The headline figures on Membership Analytics, Renewal Intelligence & AI Retention Center.** The pack's KPI cards, split out of the row (decided 29 September, readiness close-out): a count describes the list, not each item in it.",
  "properties": {
   "activeMembers": {
    "type": "integer",
    "description": "Active Members"
   },
   "newMemberships": {
    "type": "integer",
    "description": "New Memberships"
   },
   "renewalRate": {
    "type": "number",
    "description": "Renewal Rate"
   },
   "churnRate": {
    "type": "number",
    "description": "Churn Rate"
   },
   "autoRenewSuccess": {
    "type": "number",
    "description": "Auto-Renew Success: percentage of auto-renew attempts that succeeded"
   },
   "averageMembershipTenure": {
    "type": "number",
    "description": "Average Membership Tenure in months"
   },
   "averageVisitsPerMember": {
    "type": "number",
    "description": "Average Visits per Member"
   },
   "revenuePerMember": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Revenue per Member"
   },
   "membershipUtilization": {
    "type": "number",
    "description": "Membership Utilization"
   },
   "benefitUtilization": {
    "type": "number",
    "description": "Benefit Utilization"
   },
   "freezeSuspensionRate": {
    "type": "number",
    "description": "Freeze/Suspension Rate"
   },
   "expectedRenewals": {
    "type": "integer",
    "description": "Expected Renewals in the forecast period"
   },
   "expectedChurn": {
    "type": "integer",
    "description": "Expected Churn in the forecast period"
   },
   "renewalRevenue": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Renewal Revenue"
   },
   "membershipBaseGrowth": {
    "type": "number",
    "description": "Membership Base Growth, percent"
   },
   "upgradeRate": {
    "type": "number",
    "description": "Upgrade Rate, percent (pack p.35)"
   },
   "upgradeRevenue": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "description": "Upgrade Revenue forecast (pack p.37)"
   },
   "renewalFunnel": {
    "type": "object",
    "description": "Renewal Funnel (pack p.36)",
    "properties": {
     "eligibleForRenewal": {
      "type": "integer"
     },
     "contacted": {
      "type": "integer"
     },
     "renewalStarted": {
      "type": "integer"
     },
     "paymentAttempted": {
      "type": "integer"
     },
     "renewed": {
      "type": "integer"
     },
     "failed": {
      "type": "integer"
     },
     "expired": {
      "type": "integer"
     }
    }
   }
  }
 },
 "MembershipAnalyticsRenewalIntelligenceAiRetentionCenView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over subscription state, assembled at read time from tables that already exist",
  "description": "**What Membership Analytics, Renewal Intelligence & AI Retention Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "visits": {
    "type": "integer",
    "description": "Visits in the current term"
   },
   "benefitUsage": {
    "type": "number",
    "description": "Benefit usage, percent of allocation used"
   },
   "guestTicketUsage": {
    "type": "integer",
    "description": "Guest tickets used this term"
   },
   "complaintsExceptions": {
    "type": "integer",
    "description": "Complaints/Exceptions this term"
   },
   "confidence": {
    "type": "number",
    "description": "Confidence of the prediction, 0-1"
   },
   "keyDrivers": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Key Drivers, e.g. visits down 58%, no visits in 90 days"
   },
   "modelVersion": {
    "type": "string",
    "description": "Model Version"
   },
   "dataFreshness": {
    "type": "string",
    "format": "date-time",
    "description": "Data Freshness: when the inputs were last refreshed"
   },
   "membershipId": {
    "type": "string",
    "description": "Membership ID"
   },
   "memberName": {
    "type": "string",
    "description": "Member name"
   },
   "membershipProduct": {
    "type": "string",
    "description": "Membership product"
   },
   "tier": {
    "type": "string",
    "description": "Tier",
    "nullable": true
   },
   "expiryDate": {
    "type": "string",
    "format": "date",
    "description": "Expiry date"
   },
   "lastVisitDate": {
    "type": "string",
    "format": "date",
    "description": "Last visit",
    "nullable": true
   },
   "renewalProbability": {
    "type": "number",
    "description": "Member Renewal Probability, 0-1 (advisory)"
   },
   "churnFlag": {
    "type": "boolean",
    "description": "No visit in the last 90 days: flagged for churn follow-up (MoM 8 Sep)"
   },
   "recommendedActions": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "renewalReminder",
      "benefitReminder",
      "membershipEducation",
      "upgradeOffer",
      "retentionOffer",
      "serviceFollowUp"
     ]
    },
    "description": "Recommended Actions (pack p.36), advisory"
   }
  }
 },
 "MembershipFreezeSuspensionReactivationManagementView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over subscription state, assembled at read time from tables that already exist",
  "description": "**What Membership Freeze, Suspension & Reactivation Management displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "startDate": {
    "type": "string",
    "format": "date",
    "description": "Start Date"
   },
   "endDate": {
    "type": "string",
    "format": "date",
    "description": "End Date; empty for open-ended suspension",
    "nullable": true
   },
   "durationDays": {
    "type": "integer",
    "description": "Duration in days",
    "nullable": true
   },
   "reason": {
    "type": "string",
    "description": "Reason in the requester's words"
   },
   "requestedBy": {
    "type": "string",
    "description": "Requested By (member, agent or system)"
   },
   "approvedBy": {
    "type": "string",
    "description": "Approved By",
    "nullable": true
   },
   "membershipId": {
    "type": "string",
    "description": "Membership ID"
   },
   "memberName": {
    "type": "string",
    "description": "Member name"
   },
   "interruptionType": {
    "type": "string",
    "enum": [
     "freeze",
     "suspension",
     "administrativeHold"
    ],
    "description": "Freeze (member's permitted pause), Suspension (administrative restriction) or Administrative Hold (pack p.27)"
   },
   "suspensionReason": {
    "type": "string",
    "enum": [
     "paymentIssue",
     "membershipMisuse",
     "credentialMisuse",
     "eligibilityIssue",
     "chargeback",
     "administrativeReview",
     "other"
    ],
    "description": "Suspension Reason (pack p.28)",
    "nullable": true
   },
   "validityTreatment": {
    "type": "string",
    "enum": [
     "extendExpiry",
     "doNotExtend"
    ],
    "description": "Validity Treatment (pack p.28). Default extendExpiry for a freeze and doNotExtend for a suspension, as the membership state model sets"
   },
   "newExpiryDate": {
    "type": "string",
    "format": "date",
    "description": "Expiry after the extension, when validityTreatment is extendExpiry",
    "nullable": true
   },
   "entitlementTreatment": {
    "type": "object",
    "description": "Entitlement Treatment during the interruption (pack p.28). Defaults: admission, reservations, benefits and credential blocked; renewal allowed during a freeze and blocked during a suspension (decided 29 September, readiness close-out)",
    "properties": {
     "admissionBlocked": {
      "type": "boolean"
     },
     "reservationsRestricted": {
      "type": "boolean"
     },
     "benefitsRestricted": {
      "type": "boolean"
     },
     "renewalAllowed": {
      "type": "boolean"
     },
     "credentialDisabled": {
      "type": "boolean"
     }
    }
   },
   "interruptionStatus": {
    "type": "string",
    "description": "Interruption status: scheduled, active, ended or cancelled"
   }
  }
 },
 "MembershipMigrationInput": {
  "type": "object",
  "x-ticvai-persistence": "none — request only",
  "description": "What `migrateMembership` takes (decided 29 September, readiness close-out).",
  "required": [
   "targetProductId",
   "direction",
   "effectiveTiming"
  ],
  "properties": {
   "targetProductId": {
    "type": "string",
    "format": "uuid",
    "description": "The membership product it moves to."
   },
   "direction": {
    "type": "string",
    "description": "Which way it moves (decided 29 September, readiness close-out).",
    "enum": [
     "upgrade",
     "downgrade",
     "migration"
    ]
   },
   "effectiveTiming": {
    "type": "string",
    "description": "When the move takes effect (decided 29 September, readiness close-out).",
    "enum": [
     "immediate",
     "nextVisit",
     "nextRenewal",
     "endOfCurrentTerm"
    ]
   },
   "proRata": {
    "type": "boolean",
    "default": false,
    "description": "Charge or credit the difference for the remaining term."
   }
  }
 },
 "MembershipMigrationView": {
  "type": "object",
  "x-ticvai-persistence": "orders.membership_migration",
  "description": "**One move of a membership to another product.** Written by `migrateMembership` (decided 29 September, readiness close-out).\n",
  "required": [
   "id",
   "membershipId",
   "fromProductId",
   "targetProductId",
   "direction",
   "effectiveTiming",
   "status"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "membershipId": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "fromProductId": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "targetProductId": {
    "type": "string",
    "format": "uuid"
   },
   "direction": {
    "type": "string",
    "enum": [
     "upgrade",
     "downgrade",
     "migration"
    ]
   },
   "effectiveTiming": {
    "type": "string",
    "enum": [
     "immediate",
     "nextVisit",
     "nextRenewal",
     "endOfCurrentTerm"
    ]
   },
   "proRata": {
    "type": "boolean"
   },
   "proRataAmount": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "nullable": true,
    "readOnly": true,
    "description": "With `proRata`, the difference charged (positive) or credited (negative)."
   },
   "orderId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true,
    "description": "The order the pro-rata difference went through."
   },
   "effectiveAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true,
    "description": "When it took, or will take, effect. Null for `nextVisit` until the visit."
   },
   "status": {
    "type": "string",
    "readOnly": true,
    "enum": [
     "scheduled",
     "applied"
    ]
   },
   "createdAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   }
  }
 },
 "MembershipUpgradeDowngradeProductMigrationOperationsView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over subscription state, assembled at read time from tables that already exist",
  "description": "**What Membership Upgrade, Downgrade & Product Migration Operations displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "currentMembership": {
    "type": "string",
    "description": "Current Membership product and tier"
   },
   "targetMembership": {
    "type": "string",
    "description": "Target Membership product and tier"
   },
   "customerQualification": {
    "type": "string",
    "enum": [
     "eligible",
     "notEligible",
     "reviewRequired"
    ],
    "description": "Customer Qualification for the target"
   },
   "usage": {
    "type": "integer",
    "description": "Usage: visits in the current term"
   },
   "remainingValidity": {
    "type": "integer",
    "description": "Remaining Validity in days"
   },
   "entitlementComparison": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "entitlementType": {
       "type": "string",
       "enum": [
        "unlimitedAdmission",
        "limitedAdmissions",
        "attractionAccess",
        "eventAccess",
        "zoneAccess",
        "fastTrack",
        "priorityEntry",
        "guestTickets",
        "parking",
        "fnbBenefit",
        "retailBenefit",
        "rentalBenefit",
        "specialEventAccess",
        "bookingPrivileges",
        "other"
       ]
      },
      "current": {
       "type": "string"
      },
      "target": {
       "type": "string"
      }
     }
    },
    "description": "Entitlement Comparison (pack pp.29-30)"
   },
   "outstandingBalance": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "nullable": true,
    "description": "Outstanding Balance on the member's account"
   },
   "effectiveDate": {
    "type": "string",
    "format": "date",
    "description": "Effective date, for effectiveTiming fixedDate or once resolved",
    "nullable": true
   },
   "membershipId": {
    "type": "string",
    "description": "Membership ID"
   },
   "memberName": {
    "type": "string",
    "description": "Member name"
   },
   "movementType": {
    "type": "string",
    "enum": [
     "upgrade",
     "downgrade",
     "migration"
    ],
    "description": "Upgrade, downgrade or product migration"
   },
   "effectiveTiming": {
    "type": "string",
    "enum": [
     "immediately",
     "nextVisit",
     "nextRenewal",
     "fixedDate",
     "endOfCurrentTerm"
    ],
    "description": "Effective Date option (pack p.29)"
   },
   "proRataCredit": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "nullable": true,
    "description": "Pro-rata credit for the unused part of the current term, calculated by pricing (MoM 1 Sep §4.9)"
   },
   "priceDifference": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "nullable": true,
    "description": "Balance to charge after the credit, calculated by pricing (Area 10)"
   },
   "consumedBenefitTreatment": {
    "type": "string",
    "enum": [
     "reset",
     "carryForward",
     "adjust"
    ],
    "description": "Consumed Benefits (pack p.30): per the target product's rules"
   },
   "orderId": {
    "type": "string",
    "description": "Resulting order (Area 12)",
    "nullable": true
   },
   "bulkMigrationId": {
    "type": "string",
    "description": "Bulk Migration batch, when part of one (pack p.30)",
    "nullable": true
   },
   "requestStatus": {
    "type": "string",
    "description": "Request status: quoted, pendingPayment, scheduled, completed or cancelled"
   }
  }
 },
 "OrdersMembershipRenewal": {
  "type": "object",
  "x-ticvai-persistence": "orders.membership_renewal",
  "description": "**Taken from the backend workbook, 20 September.** Stores membership renewal transactions and the result of each renewal attempt.",
  "required": [
   "customerMembershipId",
   "entitlementTemplateId",
   "type",
   "status",
   "attemptedAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "customerMembershipId": {
    "type": "string",
    "format": "uuid",
    "description": "The membership in the path. Taken from the path on `renewMembership`."
   },
   "entitlementTemplateId": {
    "type": "string",
    "format": "uuid"
   },
   "orderId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true,
    "description": "The order the renewal charged through. Set by the server."
   },
   "type": {
    "type": "string",
    "maxLength": 30
   },
   "status": {
    "type": "string",
    "maxLength": 30,
    "readOnly": true
   },
   "previousExpiryAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true
   },
   "newExpiryAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true,
    "description": "Computed from the entitlement template's term and grace period."
   },
   "attemptedAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   },
   "completedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true
   },
   "failureReason": {
    "type": "string",
    "maxLength": 500,
    "nullable": true,
    "readOnly": true
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
 "RenewalOperationsAutoRenewalManagementSummary": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection; the headline tiles over the list, computed at read time for the filters in force",
  "description": "**The headline figures on Renewal Operations & Auto-Renewal Management.** The pack's KPI cards, split out of the row (decided 29 September, readiness close-out): a count describes the list, not each item in it.",
  "properties": {
   "renewalNotOpen": {
    "type": "integer",
    "description": "Renewal Not Open"
   },
   "renewalEligible": {
    "type": "integer",
    "description": "Renewal Eligible"
   },
   "renewalInvitationSent": {
    "type": "integer",
    "description": "Renewal Invitation Sent"
   },
   "renewalStarted": {
    "type": "integer",
    "description": "Renewal Started"
   },
   "paymentPending": {
    "type": "integer",
    "description": "Payment Pending"
   },
   "renewed": {
    "type": "integer",
    "description": "Renewed"
   },
   "autoRenewScheduled": {
    "type": "integer",
    "description": "Auto-Renew Scheduled"
   },
   "autoRenewFailed": {
    "type": "integer",
    "description": "Auto-Renew Failed"
   },
   "gracePeriod": {
    "type": "integer",
    "description": "Grace Period"
   },
   "expiredWithoutRenewal": {
    "type": "integer",
    "description": "Expired Without Renewal"
   }
  }
 },
 "RenewalOperationsAutoRenewalManagementView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over subscription state, assembled at read time from tables that already exist",
  "description": "**What Renewal Operations & Auto-Renewal Management displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "member": {
    "type": "string",
    "description": "Member"
   },
   "membership": {
    "type": "string",
    "description": "Membership"
   },
   "tier": {
    "type": "string",
    "description": "Tier"
   },
   "expiry": {
    "type": "string",
    "format": "date",
    "description": "Expiry"
   },
   "renewalWindow": {
    "type": "object",
    "description": "Renewal Window",
    "properties": {
     "opens": {
      "type": "string",
      "format": "date"
     },
     "closes": {
      "type": "string",
      "format": "date"
     }
    }
   },
   "renewalPrice": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "nullable": true,
    "description": "Renewal Price from pricing (Area 10)"
   },
   "autoRenew": {
    "type": "boolean",
    "description": "Auto-Renew: the member has explicitly opted in"
   },
   "paymentMethodStatus": {
    "type": "string",
    "description": "Payment Method Status: none, valid, expiringSoon, expired or failed"
   },
   "eligibility": {
    "type": "string",
    "enum": [
     "eligible",
     "notEligible",
     "reviewRequired"
    ],
    "description": "Eligibility for renewal"
   },
   "renewalStatus": {
    "type": "string",
    "description": "Renewal Status: renewalNotOpen, renewalEligible, renewalInvitationSent, renewalStarted, paymentPending, renewed, autoRenewScheduled, autoRenewFailed, gracePeriod or expiredWithoutRenewal (pack p.30 Renewal Pipeline)"
   },
   "membershipStatus": {
    "type": "string",
    "description": "Current membership status: one of the membership lifecycle values active, frozen, suspended, expired or cancelled (shape follows catalogue GuestMembership.status; states/guest-membership-status.yaml): frozen is the member's pause and extends validity, suspended is a sanction and does not"
   },
   "outstandingIssues": {
    "type": "string",
    "description": "Outstanding Issues",
    "nullable": true
   },
   "autoRenewConsentAt": {
    "type": "string",
    "format": "date-time",
    "description": "Consent: when the member accepted the auto-renewal terms; empty means no consent and auto-renew will not run",
    "nullable": true
   },
   "membershipVersion": {
    "type": "integer",
    "description": "Membership Version the renewal will be on"
   },
   "membershipId": {
    "type": "string",
    "description": "Membership ID"
   },
   "preNotificationSentAt": {
    "type": "string",
    "format": "date-time",
    "description": "Pre-renewal reminder sent",
    "nullable": true
   },
   "paymentAttempts": {
    "type": "integer",
    "description": "Auto-renew payment attempts so far"
   },
   "nextAttemptAt": {
    "type": "string",
    "format": "date-time",
    "description": "Next scheduled payment attempt",
    "nullable": true
   }
  }
 },
 "VisitAdmissionEntitlementUsageMonitorSummary": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection; the headline tiles over the list, computed at read time for the filters in force",
  "description": "**The headline figures on Visit, Admission & Entitlement Usage Monitor.** The pack's KPI cards, split out of the row (decided 29 September, readiness close-out): a count describes the list, not each item in it.",
  "properties": {
   "totalVisits": {
    "type": "integer",
    "description": "Total Visits"
   },
   "visitsThisMonth": {
    "type": "integer",
    "description": "Visits This Month"
   },
   "lastVisit": {
    "type": "string",
    "format": "date-time",
    "description": "Last Visit",
    "nullable": true
   },
   "upcomingReservation": {
    "type": "string",
    "format": "date-time",
    "description": "Upcoming Reservation start",
    "nullable": true
   },
   "guestTicketsUsed": {
    "type": "integer",
    "description": "Guest Tickets Used"
   },
   "guestTicketsRemaining": {
    "type": "integer",
    "description": "Guest Tickets Remaining",
    "nullable": true
   },
   "parkingUses": {
    "type": "integer",
    "description": "Parking Uses"
   },
   "benefitUsage": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "entitlementType": {
       "type": "string",
       "enum": [
        "unlimitedAdmission",
        "limitedAdmissions",
        "attractionAccess",
        "eventAccess",
        "zoneAccess",
        "fastTrack",
        "priorityEntry",
        "guestTickets",
        "parking",
        "fnbBenefit",
        "retailBenefit",
        "rentalBenefit",
        "specialEventAccess",
        "bookingPrivileges",
        "other"
       ]
      },
      "allocation": {
       "type": "integer",
       "nullable": true,
       "description": "Empty for unlimited"
      },
      "used": {
       "type": "integer"
      },
      "remaining": {
       "type": "integer",
       "nullable": true,
       "description": "Empty for unlimited"
      },
      "value": {
       "type": "string",
       "nullable": true,
       "description": "Display value of a discount benefit, from its pricing rule"
      }
     }
    },
    "description": "Entitlement Consumption (pack p.26): allocation, used and remaining per benefit"
   },
   "noShows": {
    "type": "integer",
    "description": "No-Shows"
   },
   "usageExceptions": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "code": {
       "type": "string",
       "enum": [
        "usageAboveLimit",
        "invalidReEntry",
        "benefitExhausted",
        "blackoutAttempt",
        "expiredMembershipUsage",
        "suspendedMembershipAttempt"
       ]
      },
      "count": {
       "type": "integer"
      }
     }
    },
    "description": "Usage Exceptions (pack pp.26-27) counted over the filtered visits"
   },
   "aiInsights": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "AI Assistance: advisory observations only; never applied automatically (pack AI sections)"
   }
  }
 },
 "VisitAdmissionEntitlementUsageMonitorView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over subscription state, assembled at read time from tables that already exist",
  "description": "**What Visit, Admission & Entitlement Usage Monitor displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "date": {
    "type": "string",
    "format": "date",
    "description": "Date of the visit"
   },
   "venue": {
    "type": "string",
    "description": "Venue"
   },
   "attraction": {
    "type": "string",
    "description": "Attraction",
    "nullable": true
   },
   "gate": {
    "type": "string",
    "description": "Gate",
    "nullable": true
   },
   "entryTime": {
    "type": "string",
    "format": "date-time",
    "description": "Entry Time"
   },
   "exitTime": {
    "type": "string",
    "format": "date-time",
    "description": "Exit time where the venue records exits",
    "nullable": true
   },
   "credential": {
    "type": "string",
    "description": "Credential presented (credential id)"
   },
   "reservation": {
    "type": "string",
    "description": "Reservation id, where the visit was booked",
    "nullable": true
   },
   "validationResult": {
    "type": "string",
    "enum": [
     "admitted",
     "usageAboveLimit",
     "invalidReEntry",
     "benefitExhausted",
     "blackoutAttempt",
     "expiredMembershipUsage",
     "suspendedMembershipAttempt"
    ],
    "description": "Validation Result from Access Control"
   },
   "membershipId": {
    "type": "string",
    "description": "Membership ID"
   },
   "visitId": {
    "type": "string",
    "description": "Visit (access event) id"
   }
  }
 }
}
```
