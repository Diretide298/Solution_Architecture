# WS30 — Membership   Annual Pass Management board 2

**10 screens · 10 operations · 11 schemas · 2 permissions**

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
  `PLATFORM_CELL_MANAGE, PLATFORM_TENANT_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **0 of these operations work offline**
  
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `BO-294` | Member Operations Command Center | listDetail | 1 | 0 | — |
| `BO-295` | Member 360° Membership Account Workspace | listDetail | 1 | 0 | — |
| `BO-296` | Membership Activation, Assignment & Credential Management | listDetail | 1 | 0 | — |
| `BO-297` | Visit, Admission & Entitlement Usage Monitor | listDetail | 1 | 0 | — |
| `BO-298` | Membership Freeze, Suspension & Reactivation Management | configEditor | 1 | 1 | — |
| `BO-299` | Membership Upgrade, Downgrade & Product Migration Operations | listDetail | 1 | 1 | — |
| `BO-300` | Renewal Operations & Auto-Renewal Management | listDetail | 1 | 0 | — |
| `BO-301` | Member Exceptions, Overrides & Service Recovery | listDetail | 1 | 0 | — |
| `BO-302` | Member Lifecycle History, Audit & Case Timeline | listDetail | 1 | 0 | — |
| `BO-303` | Membership Analytics, Renewal Intelligence & AI Retention Center | commandCentre | 1 | 0 | — |

## Thin screens in this batch

**BO-297, BO-299, BO-300, BO-301, BO-302 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

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
     "carries": [
      "venueId"
     ],
     "provenance": "derived — BO-100 declares entryState.params venueId, so an edge into it must carry them"
    },
    {
     "to": "BO-295",
     "trigger": "Works in Member 360° Membership Account Workspace",
     "provenance": "flow F139 step 1→2",
     "operation": "listMember"
    },
    {
     "to": "BO-296",
     "trigger": "Works in Membership Activation, Assignment & Credential Management",
     "provenance": "flow F139 step 3→4",
     "operation": "listMember"
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
     "to": "BO-299",
     "trigger": "Works in Membership Upgrade, Downgrade & Product Migration Operations",
     "provenance": "flow F139 step 9→10",
     "operation": "listMember"
    },
    {
     "to": "BO-300",
     "trigger": "Works in Renewal Operations & Auto-Renewal Management",
     "provenance": "flow F139 step 11→12",
     "operation": "listMember"
    },
    {
     "to": "BO-301",
     "trigger": "Works in Member Exceptions, Overrides & Service Recovery",
     "provenance": "flow F139 step 13→14",
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
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Provide membership teams with a real-time operational dashboard for the complete active member population.",
  "purposeNote": "Membership operations teams can monitor and prioritize the complete member population from one centralized workspace.",
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
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every member operations",
       "columns": [
        "MemberOperationsCommandCenterView.activeMembers",
        "MemberOperationsCommandCenterView.newMembersToday",
        "MemberOperationsCommandCenterView.activatedToday",
        "MemberOperationsCommandCenterView.pendingActivation",
        "MemberOperationsCommandCenterView.expiringIn30Days",
        "MemberOperationsCommandCenterView.renewalDue",
        "MemberOperationsCommandCenterView.renewedThisMonth",
        "MemberOperationsCommandCenterView.renewalRate",
        "MemberOperationsCommandCenterView.suspendedMemberships",
        "MemberOperationsCommandCenterView.frozenMemberships",
        "MemberOperationsCommandCenterView.membershipExceptions",
        "MemberOperationsCommandCenterView.atRiskMembers",
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
        "MemberOperationsCommandCenterView.activeMembers",
        "MemberOperationsCommandCenterView.newMembersToday",
        "MemberOperationsCommandCenterView.activatedToday",
        "MemberOperationsCommandCenterView.pendingActivation",
        "MemberOperationsCommandCenterView.expiringIn30Days",
        "MemberOperationsCommandCenterView.renewalDue",
        "MemberOperationsCommandCenterView.renewedThisMonth",
        "MemberOperationsCommandCenterView.renewalRate",
        "MemberOperationsCommandCenterView.suspendedMemberships",
        "MemberOperationsCommandCenterView.frozenMemberships",
        "MemberOperationsCommandCenterView.membershipExceptions",
        "MemberOperationsCommandCenterView.atRiskMembers",
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
    "MemberOperationsCommandCenterView.activeMembers",
    "MemberOperationsCommandCenterView.newMembersToday",
    "MemberOperationsCommandCenterView.activatedToday",
    "MemberOperationsCommandCenterView.pendingActivation",
    "MemberOperationsCommandCenterView.expiringIn30Days",
    "MemberOperationsCommandCenterView.renewalDue"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-294"
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
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display; Show) and no metric row",
  "purpose": "Provide a complete operational view of an individual member and their membership contract. This should be the primary screen an authorized membership-service agent opens when helping a member.",
  "purposeNote": "Authorized users can understand the complete operational state of a membership without navigating across multiple modules.",
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
    "trigger": "onAction",
    "invalidates": [
     "setMemberMembershipAccount"
    ]
   }
  ],
  "entryState": {
   "preloaded": [
    "Member360MembershipAccountWorkspaceView.memberName",
    "Member360MembershipAccountWorkspaceView.customerId",
    "Member360MembershipAccountWorkspaceView.membershipId",
    "Member360MembershipAccountWorkspaceView.membershipProduct",
    "Member360MembershipAccountWorkspaceView.tier",
    "Member360MembershipAccountWorkspaceView.status"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-295"
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
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Manage the operational process that turns a purchased membership product into an active membership assigned to a specific individual.",
  "purposeNote": "Purchased memberships can be securely assigned, verified, activated and linked to appropriate credentials according to Board 1 rules.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 3 actions on this screen and the screen declares 1 operation.** Unserved: Review, Link, Escalate. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Membership___Annual_Pass_Management_Reference.pdf, page 24 §Actions depend on configuration"
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
       "label": "Review",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 24 §Actions depend on configuration"
      },
      {
       "kind": "secondaryButton",
       "label": "Link",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 24 §Actions depend on configuration"
      },
      {
       "kind": "secondaryButton",
       "label": "Escalate",
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
   }
  ],
  "entryState": {
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
   "board": "wireframes/P08 Venue Management.dc.html#bo-296"
  },
  "apisNote": "Regenerated 9 September 2026 from Membership___Annual_Pass_Management_Reference.pdf page 24. 6 of 6 labels bound to a contract property; 17 of 44 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display; Detect) and no metric row",
  "purpose": "Provide membership teams with complete visibility of how a member uses admission and other membership entitlements.",
  "purposeNote": "Authorized users can trace membership visits and benefit consumption while preserving the Access Control system as the authoritative admission-validation engine.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every visit admission entitlement",
       "columns": [
        "VisitAdmissionEntitlementUsageMonitorView.totalVisits",
        "VisitAdmissionEntitlementUsageMonitorView.visitsThisMonth",
        "VisitAdmissionEntitlementUsageMonitorView.lastVisit",
        "VisitAdmissionEntitlementUsageMonitorView.upcomingReservation",
        "VisitAdmissionEntitlementUsageMonitorView.guestTicketsUsed",
        "VisitAdmissionEntitlementUsageMonitorView.guestTicketsRemaining",
        "VisitAdmissionEntitlementUsageMonitorView.parkingUses",
        "VisitAdmissionEntitlementUsageMonitorView.benefitUsage",
        "VisitAdmissionEntitlementUsageMonitorView.noShows",
        "VisitAdmissionEntitlementUsageMonitorView.usageAboveLimit",
        "VisitAdmissionEntitlementUsageMonitorView.invalidReEntry",
        "VisitAdmissionEntitlementUsageMonitorView.benefitExhausted",
        "VisitAdmissionEntitlementUsageMonitorView.blackoutAttempt",
        "VisitAdmissionEntitlementUsageMonitorView.expiredMembershipUsage",
        "VisitAdmissionEntitlementUsageMonitorView.suspendedMembershipAttempt"
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
        "VisitAdmissionEntitlementUsageMonitorView.totalVisits",
        "VisitAdmissionEntitlementUsageMonitorView.visitsThisMonth",
        "VisitAdmissionEntitlementUsageMonitorView.lastVisit",
        "VisitAdmissionEntitlementUsageMonitorView.upcomingReservation",
        "VisitAdmissionEntitlementUsageMonitorView.guestTicketsUsed",
        "VisitAdmissionEntitlementUsageMonitorView.guestTicketsRemaining",
        "VisitAdmissionEntitlementUsageMonitorView.parkingUses",
        "VisitAdmissionEntitlementUsageMonitorView.benefitUsage",
        "VisitAdmissionEntitlementUsageMonitorView.noShows",
        "VisitAdmissionEntitlementUsageMonitorView.usageAboveLimit",
        "VisitAdmissionEntitlementUsageMonitorView.invalidReEntry",
        "VisitAdmissionEntitlementUsageMonitorView.benefitExhausted",
        "VisitAdmissionEntitlementUsageMonitorView.blackoutAttempt",
        "VisitAdmissionEntitlementUsageMonitorView.expiredMembershipUsage",
        "VisitAdmissionEntitlementUsageMonitorView.suspendedMembershipAttempt"
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
    "VisitAdmissionEntitlementUsageMonitorView.totalVisits",
    "VisitAdmissionEntitlementUsageMonitorView.visitsThisMonth",
    "VisitAdmissionEntitlementUsageMonitorView.lastVisit",
    "VisitAdmissionEntitlementUsageMonitorView.upcomingReservation",
    "VisitAdmissionEntitlementUsageMonitorView.guestTicketsUsed",
    "VisitAdmissionEntitlementUsageMonitorView.guestTicketsRemaining"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-297"
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
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 4 actions on this screen and the screen declares 1 operation.** Unserved: Suspend, Resume, Administrative Hold. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Membership___Annual_Pass_Management_Reference.pdf, page 27 §Support"
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
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 27 §Capture"
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
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-298"
  },
  "apisNote": "Regenerated 9 September 2026 from Membership___Annual_Pass_Management_Reference.pdf page 27. 0 of 0 labels bound to a contract property; 10 of 18 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Manage operational movement of an active member between membership products or tiers.",
  "purposeNote": "Memberships can move between tiers/products without losing historical, financial or entitlement integrity.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 1 actions on this screen and the screen declares 1 operation.** Unserved: End of Current Term. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Membership___Annual_Pass_Management_Reference.pdf, page 29 §Support"
   },
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
       "kind": "destructiveButton",
       "label": "End of Current Term",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 29 §Support"
      }
     ]
    },
    {
     "name": "contentBody",
     "components": [
      {
       "kind": "dataTable",
       "derived": true,
       "impliedBy": "listMembershipUpgradeDowngrade",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
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
   }
  ],
  "entryState": {
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
   "board": "wireframes/P08 Venue Management.dc.html#bo-299"
  },
  "apisNote": "Regenerated 9 September 2026 from Membership___Annual_Pass_Management_Reference.pdf page 29. 0 of 0 labels bound to a contract property; 1 of 34 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display; Track) and no metric row",
  "purpose": "Operationally manage memberships approaching expiry and execute the renewal policies configured in Board 1.",
  "purposeNote": "Membership teams can monitor and execute manual and automatic renewals while maintaining continuous and correctly versioned membership contracts.",
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
   }
  ],
  "entryState": {
   "preloaded": [
    "RenewalOperationsAutoRenewalManagementView.member",
    "RenewalOperationsAutoRenewalManagementView.membership",
    "RenewalOperationsAutoRenewalManagementView.tier",
    "RenewalOperationsAutoRenewalManagementView.expiry",
    "RenewalOperationsAutoRenewalManagementView.renewalWindow",
    "RenewalOperationsAutoRenewalManagementView.renewalPrice"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-300"
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
    "why": "**The pack names 3 actions on this screen and the screen declares 1 operation.** Unserved: Eligibility Override, Freeze Exception, Suspension Override. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Membership___Annual_Pass_Management_Reference.pdf, page 32 §Support"
   },
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
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 32 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Freeze Exception",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 32 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Suspension Override",
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
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-301"
  },
  "apisNote": "Regenerated 9 September 2026 from Membership___Annual_Pass_Management_Reference.pdf page 32. 0 of 0 labels bound to a contract property; 3 of 14 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Track) and no metric row",
  "purpose": "Maintain a complete historical record of everything that has happened to the membership from purchase to final expiry.",
  "purposeNote": "The entire membership lifecycle can be reconstructed chronologically with responsible users, systems, rules and related transactions.",
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
        "MemberLifecycleHistoryAuditCaseTimelineView.purchase",
        "MemberLifecycleHistoryAuditCaseTimelineView.assignment",
        "MemberLifecycleHistoryAuditCaseTimelineView.activation",
        "MemberLifecycleHistoryAuditCaseTimelineView.visits",
        "MemberLifecycleHistoryAuditCaseTimelineView.benefitUsage",
        "MemberLifecycleHistoryAuditCaseTimelineView.dependentChanges",
        "MemberLifecycleHistoryAuditCaseTimelineView.credentialChanges",
        "Freeze",
        "MemberLifecycleHistoryAuditCaseTimelineView.suspension",
        "MemberLifecycleHistoryAuditCaseTimelineView.reactivation",
        "Upgrade",
        "Downgrade",
        "MemberLifecycleHistoryAuditCaseTimelineView.renewal",
        "MemberLifecycleHistoryAuditCaseTimelineView.exceptions",
        "MemberLifecycleHistoryAuditCaseTimelineView.expiry",
        "MemberLifecycleHistoryAuditCaseTimelineView.cancellation"
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
        "MemberLifecycleHistoryAuditCaseTimelineView.purchase",
        "MemberLifecycleHistoryAuditCaseTimelineView.assignment",
        "MemberLifecycleHistoryAuditCaseTimelineView.activation",
        "MemberLifecycleHistoryAuditCaseTimelineView.visits",
        "MemberLifecycleHistoryAuditCaseTimelineView.benefitUsage",
        "MemberLifecycleHistoryAuditCaseTimelineView.dependentChanges",
        "MemberLifecycleHistoryAuditCaseTimelineView.credentialChanges",
        "Freeze",
        "MemberLifecycleHistoryAuditCaseTimelineView.suspension",
        "MemberLifecycleHistoryAuditCaseTimelineView.reactivation",
        "Upgrade",
        "Downgrade",
        "MemberLifecycleHistoryAuditCaseTimelineView.renewal",
        "MemberLifecycleHistoryAuditCaseTimelineView.exceptions",
        "MemberLifecycleHistoryAuditCaseTimelineView.expiry",
        "MemberLifecycleHistoryAuditCaseTimelineView.cancellation"
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
    "MemberLifecycleHistoryAuditCaseTimelineView.purchase",
    "MemberLifecycleHistoryAuditCaseTimelineView.assignment",
    "MemberLifecycleHistoryAuditCaseTimelineView.activation",
    "MemberLifecycleHistoryAuditCaseTimelineView.visits",
    "MemberLifecycleHistoryAuditCaseTimelineView.benefitUsage",
    "MemberLifecycleHistoryAuditCaseTimelineView.dependentChanges"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-302"
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
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen a metric directory (§Display; Forecast) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's",
  "purpose": "Turn membership operational data into actionable intelligence for retention, renewal, product optimization and member engagement.",
  "purposeNote": "Management can analyze membership performance and use governed AI intelligence to improve renewal, retention and membership-product performance. Board 2 — Final Screen Register # Backend Screen Core Responsibility 13.2. Member population",
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
       "bindsTo": "MembershipAnalyticsRenewalIntelligenceAiRetentionCenView.activeMembers"
      },
      {
       "kind": "metricTile",
       "label": "New Memberships",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 35 §Display",
       "bindsTo": "MembershipAnalyticsRenewalIntelligenceAiRetentionCenView.newMemberships"
      },
      {
       "kind": "metricTile",
       "label": "Renewal Rate",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 35 §Display",
       "bindsTo": "MembershipAnalyticsRenewalIntelligenceAiRetentionCenView.renewalRate"
      },
      {
       "kind": "metricTile",
       "label": "Churn Rate",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 35 §Display",
       "bindsTo": "MembershipAnalyticsRenewalIntelligenceAiRetentionCenView.churnRate"
      },
      {
       "kind": "metricTile",
       "label": "Auto-Renew Success",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 35 §Display",
       "bindsTo": "MembershipAnalyticsRenewalIntelligenceAiRetentionCenView.autoRenewSuccess"
      },
      {
       "kind": "metricTile",
       "label": "Average Membership Tenure",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 35 §Display",
       "bindsTo": "MembershipAnalyticsRenewalIntelligenceAiRetentionCenView.averageMembershipTenure"
      },
      {
       "kind": "metricTile",
       "label": "Average Visits per Member",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 35 §Display",
       "bindsTo": "MembershipAnalyticsRenewalIntelligenceAiRetentionCenView.averageVisitsPerMember"
      },
      {
       "kind": "metricTile",
       "label": "Revenue per Member",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 35 §Display",
       "bindsTo": "MembershipAnalyticsRenewalIntelligenceAiRetentionCenView.revenuePerMember"
      },
      {
       "kind": "metricTile",
       "label": "Membership Utilization",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 35 §Display",
       "bindsTo": "MembershipAnalyticsRenewalIntelligenceAiRetentionCenView.membershipUtilization"
      },
      {
       "kind": "metricTile",
       "label": "Benefit Utilization",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 35 §Display",
       "bindsTo": "MembershipAnalyticsRenewalIntelligenceAiRetentionCenView.benefitUtilization"
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
       "bindsTo": "MembershipAnalyticsRenewalIntelligenceAiRetentionCenView.freezeSuspensionRate"
      },
      {
       "kind": "metricTile",
       "label": "Expected Renewals",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 35 §Forecast",
       "bindsTo": "MembershipAnalyticsRenewalIntelligenceAiRetentionCenView.expectedRenewals"
      },
      {
       "kind": "metricTile",
       "label": "Expected Churn",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 35 §Forecast",
       "bindsTo": "MembershipAnalyticsRenewalIntelligenceAiRetentionCenView.expectedChurn"
      },
      {
       "kind": "metricTile",
       "label": "Renewal Revenue",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 35 §Forecast",
       "bindsTo": "MembershipAnalyticsRenewalIntelligenceAiRetentionCenView.renewalRevenue"
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
       "bindsTo": "MembershipAnalyticsRenewalIntelligenceAiRetentionCenView.membershipBaseGrowth"
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
    "MembershipAnalyticsRenewalIntelligenceAiRetentionCenView.activeMembers",
    "MembershipAnalyticsRenewalIntelligenceAiRetentionCenView.newMemberships",
    "MembershipAnalyticsRenewalIntelligenceAiRetentionCenView.renewalRate",
    "MembershipAnalyticsRenewalIntelligenceAiRetentionCenView.churnRate",
    "MembershipAnalyticsRenewalIntelligenceAiRetentionCenView.autoRenewSuccess",
    "MembershipAnalyticsRenewalIntelligenceAiRetentionCenView.averageMembershipTenure"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-303"
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
    "name": "status",
    "in": "query",
    "required": false
   },
   {
    "name": "memberType",
    "in": "query",
    "required": false
   },
   {
    "name": "activation",
    "in": "query",
    "required": false
   },
   {
    "name": "expiry",
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
    "name": "customerSegment",
    "in": "query",
    "required": false
   }
  ],
  "requestBody": null,
  "responds": "MemberOperationsCommandCenterView"
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
  "parameters": [],
  "requestBody": null,
  "responds": "MemberExceptionsOverridesServiceRecoveryView"
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
  "parameters": [],
  "requestBody": null,
  "responds": "MemberLifecycleHistoryAuditCaseTimelineView"
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
  "parameters": [],
  "requestBody": null,
  "responds": "MembershipActivationAssignmentCredentialManagementView"
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
  "parameters": [],
  "requestBody": null,
  "responds": "MembershipFreezeSuspensionReactivationManagementView"
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
    "name": "purchaseMonth",
    "in": "query",
    "required": false
   },
   {
    "name": "venue",
    "in": "query",
    "required": false
   },
   {
    "name": "acquisitionChannel",
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
   }
  ],
  "requestBody": null,
  "responds": "MembershipAnalyticsRenewalIntelligenceAiRetentionCenView"
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
  "parameters": [],
  "requestBody": null,
  "responds": "MembershipUpgradeDowngradeProductMigrationOperationsView"
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
  "parameters": [],
  "requestBody": null,
  "responds": "RenewalOperationsAutoRenewalManagementView"
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
  "parameters": [],
  "requestBody": null,
  "responds": "VisitAdmissionEntitlementUsageMonitorView"
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
  "parameters": [],
  "requestBody": "Member360MembershipAccountWorkspaceInput",
  "responds": "Member360MembershipAccountWorkspaceView"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "Member360MembershipAccountWorkspaceInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures",
  "description": "**What Member 360° Membership Account Workspace submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "payments": {
    "type": "string",
    "description": "Payments"
   },
   "renewals": {
    "type": "string",
    "description": "Renewals"
   },
   "upgrades": {
    "type": "string",
    "description": "Upgrades"
   },
   "refunds": {
    "type": "string",
    "description": "Refunds"
   },
   "membershipChanges": {
    "type": "string",
    "description": "Membership Changes"
   },
   "renew": {
    "type": "string",
    "description": "Renew"
   },
   "manageDependents": {
    "type": "string",
    "description": "Manage Dependents"
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
    "type": "integer",
    "description": "Status"
   },
   "activationDate": {
    "type": "string",
    "format": "date-time",
    "description": "Activation Date"
   },
   "expiryDate": {
    "type": "string",
    "format": "date-time",
    "description": "Expiry Date"
   },
   "renewalStatus": {
    "type": "integer",
    "description": "Renewal Status"
   },
   "primaryVenue": {
    "type": "string",
    "description": "Primary Venue"
   },
   "credentialStatus": {
    "type": "integer",
    "description": "Credential Status"
   },
   "primaryMember": {
    "type": "string",
    "description": "Primary Member"
   },
   "secondaryAdult": {
    "type": "string",
    "description": "Secondary Adult"
   },
   "dependents": {
    "type": "integer",
    "description": "Dependents"
   },
   "sharedBenefits": {
    "type": "integer",
    "description": "Shared Benefits"
   },
   "individualBenefits": {
    "type": "integer",
    "description": "Individual Benefits"
   },
   "membershipVersion": {
    "type": "string",
    "description": "Membership Version"
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
   "originalOrder": {
    "type": "string",
    "description": "Original Order"
   },
   "validity": {
    "type": "string",
    "description": "Validity"
   },
   "activationMethod": {
    "type": "string",
    "description": "Activation Method"
   },
   "renewalPolicy": {
    "type": "string",
    "description": "Renewal Policy"
   },
   "autoRenewStatus": {
    "type": "integer",
    "description": "Auto-Renew Status"
   },
   "fBBenefit": {
    "type": "string",
    "description": "F&B Benefit (the pack shows 10%)"
   },
   "retailBenefit": {
    "type": "string",
    "description": "Retail Benefit (the pack shows 10%)"
   },
   "payments": {
    "type": "string",
    "description": "Payments"
   },
   "renewals": {
    "type": "string",
    "description": "Renewals"
   },
   "upgrades": {
    "type": "string",
    "description": "Upgrades"
   },
   "refunds": {
    "type": "string",
    "description": "Refunds"
   },
   "membershipChanges": {
    "type": "string",
    "description": "Membership Changes"
   },
   "renew": {
    "type": "string",
    "description": "Renew"
   },
   "manageDependents": {
    "type": "string",
    "description": "Manage Dependents"
   }
  }
 },
 "MemberExceptionsOverridesServiceRecoveryView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over subscription state, assembled at read time from tables that already exist",
  "description": "**What Member Exceptions, Overrides & Service Recovery displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "eligibilityOverride": {
    "type": "string",
    "description": "Eligibility Override"
   },
   "activationExtension": {
    "type": "string",
    "description": "Activation Extension"
   },
   "expiryExtension": {
    "type": "string",
    "format": "date-time",
    "description": "Expiry Extension"
   },
   "complimentaryRenewal": {
    "type": "string",
    "description": "Complimentary Renewal"
   },
   "complimentaryBenefit": {
    "type": "string",
    "description": "Complimentary Benefit"
   },
   "entitlementAdjustment": {
    "type": "string",
    "description": "Entitlement Adjustment"
   },
   "suspensionOverride": {
    "type": "string",
    "description": "Suspension Override"
   },
   "replacementCredential": {
    "type": "string",
    "description": "Replacement Credential"
   },
   "renewalException": {
    "type": "string",
    "description": "Renewal Exception"
   },
   "dependentException": {
    "type": "string",
    "description": "Dependent Exception"
   },
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
    "type": "string",
    "description": "Supporting Documentation"
   },
   "financialImpact": {
    "type": "string",
    "description": "Financial Impact"
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
    "description": "Exception Type"
   },
   "value": {
    "type": "string",
    "description": "Value"
   },
   "duration": {
    "type": "string",
    "format": "date-time",
    "description": "Duration"
   },
   "membershipTier": {
    "type": "string",
    "description": "Membership Tier"
   }
  }
 },
 "MemberLifecycleHistoryAuditCaseTimelineView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over subscription state, assembled at read time from tables that already exist",
  "description": "**What Member Lifecycle History, Audit & Case Timeline displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "purchase": {
    "type": "string",
    "description": "Purchase"
   },
   "assignment": {
    "type": "string",
    "description": "Assignment"
   },
   "activation": {
    "type": "string",
    "description": "Activation"
   },
   "visits": {
    "type": "integer",
    "description": "Visits"
   },
   "benefitUsage": {
    "type": "string",
    "description": "Benefit Usage"
   },
   "dependentChanges": {
    "type": "integer",
    "description": "Dependent Changes"
   },
   "credentialChanges": {
    "type": "integer",
    "description": "Credential Changes"
   },
   "suspension": {
    "type": "string",
    "description": "Suspension"
   },
   "reactivation": {
    "type": "string",
    "description": "Reactivation"
   },
   "renewal": {
    "type": "string",
    "description": "Renewal"
   },
   "exceptions": {
    "type": "integer",
    "description": "Exceptions"
   },
   "expiry": {
    "type": "string",
    "format": "date-time",
    "description": "Expiry"
   },
   "cancellation": {
    "type": "string",
    "description": "Cancellation"
   },
   "forConfigurationSensitiveMemberChangesCapture": {
    "type": "string",
    "description": "For configuration-sensitive member changes capture"
   },
   "previousValueNewValue": {
    "type": "string",
    "description": "Previous Value → New Value"
   },
   "serviceRecovery": {
    "type": "string",
    "description": "Service Recovery"
   },
   "customer": {
    "type": "string",
    "description": "Customer"
   },
   "agent": {
    "type": "string",
    "description": "Agent"
   },
   "manager": {
    "type": "string",
    "description": "Manager"
   },
   "system": {
    "type": "string",
    "description": "System"
   },
   "api": {
    "type": "string",
    "description": "API"
   },
   "integration": {
    "type": "string",
    "description": "Integration"
   },
   "order": {
    "type": "string",
    "description": "Order"
   },
   "payment": {
    "type": "string",
    "description": "Payment"
   },
   "ticket": {
    "type": "string",
    "description": "Ticket"
   },
   "reservation": {
    "type": "string",
    "description": "Reservation"
   },
   "accessEvent": {
    "type": "string",
    "description": "Access Event"
   },
   "approval": {
    "type": "string",
    "description": "Approval"
   },
   "case": {
    "type": "string",
    "description": "Case"
   },
   "credential": {
    "type": "string",
    "description": "Credential"
   },
   "events": {
    "type": "string",
    "description": "events"
   },
   "customerService": {
    "type": "string",
    "description": "Customer Service"
   },
   "finance": {
    "type": "string",
    "description": "Finance"
   },
   "audit": {
    "type": "string",
    "description": "Audit"
   },
   "compliance": {
    "type": "string",
    "description": "Compliance"
   },
   "management": {
    "type": "string",
    "description": "Management"
   }
  }
 },
 "MemberOperationsCommandCenterView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over subscription state, assembled at read time from tables that already exist",
  "description": "**What Member Operations Command Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
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
    "type": "string",
    "description": "Activated Today"
   },
   "pendingActivation": {
    "type": "integer",
    "description": "Pending Activation"
   },
   "expiringIn30Days": {
    "type": "string",
    "description": "Expiring in 30 Days"
   },
   "renewalDue": {
    "type": "string",
    "description": "Renewal Due"
   },
   "renewedThisMonth": {
    "type": "string",
    "description": "Renewed This Month"
   },
   "renewalRate": {
    "type": "number",
    "description": "Renewal Rate"
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
    "description": "At-Risk Members"
   },
   "membershipId": {
    "type": "string",
    "description": "Membership ID"
   },
   "member": {
    "type": "string",
    "description": "Member"
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
    "format": "date-time",
    "description": "Activation Date"
   },
   "expiryDate": {
    "type": "string",
    "format": "date-time",
    "description": "Expiry Date"
   },
   "membershipStatus": {
    "type": "integer",
    "description": "Membership Status"
   },
   "usageLevel": {
    "type": "string",
    "description": "Usage Level"
   },
   "renewalStatus": {
    "type": "integer",
    "description": "Renewal Status"
   },
   "outstandingIssue": {
    "type": "string",
    "description": "Outstanding Issue"
   },
   "owner": {
    "type": "string",
    "description": "Owner"
   }
  }
 },
 "MembershipActivationAssignmentCredentialManagementView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over subscription state, assembled at read time from tables that already exist",
  "description": "**What Membership Activation, Assignment & Credential Management displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "awaitingMemberAssignment": {
    "type": "string",
    "description": "Awaiting Member Assignment"
   },
   "awaitingIdentityVerification": {
    "type": "string",
    "description": "Awaiting Identity Verification"
   },
   "awaitingDocumentVerification": {
    "type": "string",
    "description": "Awaiting Document Verification"
   },
   "awaitingActivation": {
    "type": "string",
    "description": "Awaiting Activation"
   },
   "activationFailed": {
    "type": "integer",
    "description": "Activation Failed"
   },
   "eligibility": {
    "type": "string",
    "description": "Eligibility"
   },
   "age": {
    "type": "string",
    "description": "Age"
   },
   "residency": {
    "type": "string",
    "description": "Residency"
   },
   "identity": {
    "type": "string",
    "description": "Identity"
   },
   "photograph": {
    "type": "string",
    "description": "Photograph"
   },
   "requiredDocuments": {
    "type": "string",
    "description": "Required Documents"
   },
   "dependentRelationship": {
    "type": "string",
    "description": "Dependent Relationship"
   },
   "termsAcceptance": {
    "type": "string",
    "description": "Terms Acceptance"
   },
   "purchaseDate": {
    "type": "string",
    "format": "date-time",
    "description": "Purchase Date"
   },
   "eligibleActivationDate": {
    "type": "string",
    "format": "date-time",
    "description": "Eligible Activation Date"
   },
   "activationDeadline": {
    "type": "string",
    "format": "date-time",
    "description": "Activation Deadline"
   },
   "selectedStartDate": {
    "type": "string",
    "format": "date-time",
    "description": "Selected Start Date"
   },
   "calculatedExpiry": {
    "type": "string",
    "format": "date-time",
    "description": "Calculated Expiry"
   },
   "activationMethod": {
    "type": "string",
    "description": "Activation Method"
   },
   "dynamicQr": {
    "type": "string",
    "description": "Dynamic QR"
   },
   "barcode": {
    "type": "string",
    "description": "Barcode"
   },
   "rfid": {
    "type": "string",
    "description": "RFID"
   },
   "nfc": {
    "type": "string",
    "description": "NFC"
   },
   "digitalMembershipCard": {
    "type": "string",
    "description": "Digital Membership Card"
   },
   "walletPass": {
    "type": "string",
    "description": "Wallet Pass"
   },
   "physicalCard": {
    "type": "string",
    "description": "Physical Card"
   },
   "reason": {
    "type": "string",
    "enum": [
     "eligibilityFailed",
     "missingDocumentation",
     "duplicateMembership",
     "credentialFailure",
     "configurationIssue"
    ],
    "description": "Vocabulary listed under Record reason."
   }
  }
 },
 "MembershipAnalyticsRenewalIntelligenceAiRetentionCenView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over subscription state, assembled at read time from tables that already exist",
  "description": "**What Membership Analytics, Renewal Intelligence & AI Retention Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
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
    "type": "string",
    "description": "Auto-Renew Success"
   },
   "averageMembershipTenure": {
    "type": "number",
    "description": "Average Membership Tenure"
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
   "visits": {
    "type": "string",
    "description": "Visits"
   },
   "benefitUsage": {
    "type": "string",
    "description": "Benefit Usage"
   },
   "guestTicketUsage": {
    "type": "string",
    "description": "Guest Ticket Usage"
   },
   "reservationBehavior": {
    "type": "string",
    "description": "Reservation Behavior"
   },
   "complaintsExceptions": {
    "type": "string",
    "description": "Complaints/Exceptions"
   },
   "renewal": {
    "type": "string",
    "description": "Renewal"
   },
   "visitsDown58": {
    "type": "number",
    "description": "Visits down 58%"
   },
   "noVisitsIn90Days": {
    "type": "string",
    "description": "No visits in 90 days"
   },
   "twoUnusedGuestBenefits": {
    "type": "string",
    "description": "Two unused guest benefits"
   },
   "previousRenewalOccurredLate": {
    "type": "string",
    "description": "Previous renewal occurred late"
   },
   "membershipExpiresIn21Days": {
    "type": "string",
    "format": "date-time",
    "description": "Membership expires in 21 days"
   },
   "expectedRenewals": {
    "type": "string",
    "description": "Expected Renewals"
   },
   "expectedChurn": {
    "type": "string",
    "description": "Expected Churn"
   },
   "renewalRevenue": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Renewal Revenue"
   },
   "membershipBaseGrowth": {
    "type": "string",
    "description": "Membership Base Growth"
   },
   "spend": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "spend?”"
   },
   "confidence": {
    "type": "string",
    "description": "Confidence"
   },
   "keyDrivers": {
    "type": "string",
    "description": "Key Drivers"
   },
   "modelVersion": {
    "type": "string",
    "description": "Model Version"
   },
   "dataFreshness": {
    "type": "string",
    "description": "Data Freshness"
   },
   "member360MembershipAccountWorkspace": {
    "type": "string",
    "description": "Member 360° Membership Account Workspace"
   },
   "backendScreenCoreResponsibility": {
    "type": "string",
    "description": "# Backend Screen Core Responsibility"
   },
   "entitlements": {
    "type": "string",
    "description": "entitlements"
   }
  }
 },
 "MembershipFreezeSuspensionReactivationManagementView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over subscription state, assembled at read time from tables that already exist",
  "description": "**What Membership Freeze, Suspension & Reactivation Management displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "reactivate": {
    "type": "string",
    "description": "Reactivate"
   },
   "administrativeHold": {
    "type": "string",
    "description": "Administrative Hold"
   },
   "policy": {
    "type": "string",
    "description": "policy"
   },
   "otherGovernedReason": {
    "type": "string",
    "description": "other governed reason"
   },
   "startDate": {
    "type": "string",
    "format": "date-time",
    "description": "Start Date"
   },
   "endDate": {
    "type": "string",
    "format": "date-time",
    "description": "End Date"
   },
   "duration": {
    "type": "string",
    "format": "date-time",
    "description": "Duration"
   },
   "reason": {
    "type": "string",
    "description": "Reason"
   },
   "requestedBy": {
    "type": "string",
    "description": "Requested By"
   },
   "approvedBy": {
    "type": "integer",
    "description": "Approved By"
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
    "description": "Current Membership"
   },
   "targetMembership": {
    "type": "string",
    "description": "Target Membership"
   },
   "customerQualification": {
    "type": "string",
    "description": "Customer Qualification"
   },
   "usage": {
    "type": "string",
    "description": "Usage"
   },
   "remainingValidity": {
    "type": "string",
    "description": "Remaining Validity"
   },
   "entitlements": {
    "type": "string",
    "description": "Entitlements"
   },
   "outstandingBalance": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Outstanding Balance"
   },
   "effectiveDate": {
    "type": "string",
    "format": "date-time",
    "description": "Effective Date"
   },
   "area11ForUpgradeConversionLogic": {
    "type": "number",
    "description": "Area 11 for upgrade/conversion logic"
   },
   "area10ForPriceDifference": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Area 10 for price difference"
   },
   "area12ForResultingOrderPayment": {
    "type": "string",
    "description": "Area 12 for resulting order/payment"
   },
   "immediately": {
    "type": "string",
    "description": "Immediately"
   },
   "nextVisit": {
    "type": "string",
    "format": "date-time",
    "description": "Next Visit"
   },
   "nextRenewal": {
    "type": "string",
    "format": "date-time",
    "description": "Next Renewal"
   },
   "fixedDate": {
    "type": "string",
    "format": "date-time",
    "description": "Fixed Date"
   },
   "endOfCurrentTerm": {
    "type": "string",
    "description": "End of Current Term"
   },
   "dD": {
    "type": "string",
    "description": "d d"
   },
   "guest": {
    "type": "string",
    "description": "Guest (the pack shows 2 6)"
   }
  }
 },
 "RenewalOperationsAutoRenewalManagementView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over subscription state, assembled at read time from tables that already exist",
  "description": "**What Renewal Operations & Auto-Renewal Management displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "renewalNotOpen": {
    "type": "integer",
    "description": "Renewal Not Open"
   },
   "renewalEligible": {
    "type": "string",
    "description": "Renewal Eligible"
   },
   "renewalInvitationSent": {
    "type": "string",
    "description": "Renewal Invitation Sent"
   },
   "renewalStarted": {
    "type": "string",
    "description": "Renewal Started"
   },
   "paymentPending": {
    "type": "integer",
    "description": "Payment Pending"
   },
   "renewed": {
    "type": "string",
    "description": "Renewed"
   },
   "autoRenewScheduled": {
    "type": "string",
    "format": "date-time",
    "description": "Auto-Renew Scheduled"
   },
   "autoRenewFailed": {
    "type": "integer",
    "description": "Auto-Renew Failed"
   },
   "gracePeriod": {
    "type": "string",
    "format": "date-time",
    "description": "Grace Period"
   },
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
    "format": "date-time",
    "description": "Expiry"
   },
   "renewalWindow": {
    "type": "string",
    "format": "date-time",
    "description": "Renewal Window"
   },
   "renewalPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Renewal Price"
   },
   "autoRenew": {
    "type": "string",
    "description": "Auto-Renew"
   },
   "paymentMethodStatus": {
    "type": "integer",
    "description": "Payment Method Status"
   },
   "eligibility": {
    "type": "string",
    "description": "Eligibility"
   },
   "renewalStatus": {
    "type": "integer",
    "description": "Renewal Status"
   },
   "currentStatus": {
    "type": "string",
    "description": "Current Status"
   },
   "outstandingIssues": {
    "type": "string",
    "description": "Outstanding Issues"
   },
   "pricing": {
    "type": "string",
    "description": "Pricing"
   },
   "paymentMethod": {
    "type": "string",
    "description": "Payment Method"
   },
   "consent": {
    "type": "boolean",
    "description": "Consent"
   },
   "membershipVersion": {
    "type": "string",
    "description": "Membership Version"
   },
   "accordingToBoard1Configuration": {
    "type": "string",
    "description": "according to Board 1 configuration"
   }
  }
 },
 "VisitAdmissionEntitlementUsageMonitorView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over subscription state, assembled at read time from tables that already exist",
  "description": "**What Visit, Admission & Entitlement Usage Monitor displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "totalVisits": {
    "type": "integer",
    "description": "Total Visits"
   },
   "visitsThisMonth": {
    "type": "string",
    "description": "Visits This Month"
   },
   "lastVisit": {
    "type": "string",
    "format": "date-time",
    "description": "Last Visit"
   },
   "upcomingReservation": {
    "type": "string",
    "description": "Upcoming Reservation"
   },
   "guestTicketsUsed": {
    "type": "string",
    "description": "Guest Tickets Used"
   },
   "guestTicketsRemaining": {
    "type": "string",
    "description": "Guest Tickets Remaining"
   },
   "parkingUses": {
    "type": "integer",
    "description": "Parking Uses"
   },
   "benefitUsage": {
    "type": "string",
    "description": "Benefit Usage"
   },
   "noShows": {
    "type": "integer",
    "description": "No-Shows"
   },
   "date": {
    "type": "string",
    "format": "date-time",
    "description": "Date"
   },
   "venue": {
    "type": "string",
    "description": "Venue"
   },
   "attraction": {
    "type": "string",
    "description": "Attraction"
   },
   "gate": {
    "type": "string",
    "description": "Gate"
   },
   "entryTime": {
    "type": "string",
    "format": "date-time",
    "description": "Entry Time"
   },
   "exitWhereAvailable": {
    "type": "string",
    "description": "Exit where available"
   },
   "credential": {
    "type": "string",
    "description": "Credential"
   },
   "reservation": {
    "type": "string",
    "description": "Reservation"
   },
   "validationResult": {
    "type": "string",
    "description": "Validation Result"
   },
   "guest": {
    "type": "string",
    "description": "Guest (the pack shows 4 2 2)"
   },
   "usageAboveLimit": {
    "type": "integer",
    "description": "Usage Above Limit"
   },
   "invalidReEntry": {
    "type": "string",
    "description": "Invalid Re-entry"
   },
   "benefitExhausted": {
    "type": "string",
    "description": "Benefit Exhausted"
   },
   "blackoutAttempt": {
    "type": "string",
    "description": "Blackout Attempt"
   },
   "expiredMembershipUsage": {
    "type": "integer",
    "description": "Expired Membership Usage"
   },
   "suspendedMembershipAttempt": {
    "type": "string",
    "description": "Suspended Membership Attempt"
   },
   "reason": {
    "type": "string",
    "description": "Reason"
   },
   "previousValue": {
    "type": "string",
    "description": "Previous Value"
   },
   "newValue": {
    "type": "integer",
    "description": "New Value"
   },
   "user": {
    "type": "string",
    "description": "User"
   },
   "approvalWhereRequired": {
    "type": "boolean",
    "description": "Approval where required"
   }
  }
 }
}
```
