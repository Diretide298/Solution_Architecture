# WS15 — Approval Workflows and Governance board 3

**10 screens · 5 operations · 8 schemas · 2 permissions**

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
  `APPROVAL_CONFIGURE, APPROVAL_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `ADM-329` | Approval Matrix Command Center | commandCentre | 1 | 0 | — |
| `ADM-330` | Approval Authority Matrix | configEditor | 1 | 0 | — |
| `ADM-331` | Organizational Hierarchy Routing | listDetail | 1 | 0 | — |
| `ADM-332` | Department-Based Approval Matrix | configEditor | 1 | 0 | — |
| `ADM-333` | Venue & Tenant Approval Matrix | listDetail | 1 | 0 | — |
| `ADM-334` | Value & Threshold Routing | listDetail | 1 | 0 | — |
| `ADM-335` | Risk-Based & Conditional Routing | listDetail | 1 | 0 | — |
| `ADM-336` | Approver Group & Decision Policy | listDetail | 1 | 0 | — |
| `ADM-337` | Routing Simulator & Conflict Detection | listDetail | 2 | 0 | — |
| `ADM-338` | AI Routing Advisor & Matrix Optimization | listDetail | 1 | 0 | — |

## Thin screens in this batch

**ADM-331, ADM-332, ADM-333, ADM-334, ADM-335, ADM-336, ADM-337, ADM-338 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "ADM-329",
  "name": "Approval Matrix Command Center",
  "module": "Platform",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Approval_Workflows_and_Governance_Reference.pdf",
   "board": "3",
   "number": "1",
   "page": 21
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/platform/approval-matrix-command-center-adm-329",
   "component": "apps/ticvai-web/src/routes/platform/ApprovalMatrixCommandCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-002"
   ],
   "exitTo": [
    "ADM-002",
    "ADM-330",
    "ADM-331",
    "ADM-332",
    "ADM-333",
    "ADM-334",
    "ADM-335",
    "ADM-336",
    "ADM-337",
    "ADM-338"
   ],
   "transitions": [
    {
     "to": "ADM-002",
     "trigger": "Back to Platform Dashboard",
     "provenance": "structural — pack board 3 wiring, 9 September 2026",
     "back": true
    },
    {
     "to": "ADM-338",
     "trigger": "AI Routing Advisor & Matrix Optimization",
     "provenance": "structural — pack board 3 wiring, 9 September 2026"
    },
    {
     "to": "ADM-330",
     "trigger": "Approval Authority Matrix",
     "provenance": "structural — pack board 3 wiring, 9 September 2026"
    },
    {
     "to": "ADM-331",
     "trigger": "Organizational Hierarchy Routing",
     "provenance": "structural — pack board 3 wiring, 9 September 2026"
    },
    {
     "to": "ADM-332",
     "trigger": "Department-Based Approval Matrix",
     "provenance": "structural — pack board 3 wiring, 9 September 2026"
    },
    {
     "to": "ADM-333",
     "trigger": "Venue & Tenant Approval Matrix",
     "provenance": "structural — pack board 3 wiring, 9 September 2026"
    },
    {
     "to": "ADM-334",
     "trigger": "Value & Threshold Routing",
     "provenance": "structural — pack board 3 wiring, 9 September 2026"
    },
    {
     "to": "ADM-335",
     "trigger": "Risk-Based & Conditional Routing",
     "provenance": "structural — pack board 3 wiring, 9 September 2026"
    },
    {
     "to": "ADM-336",
     "trigger": "Approver Group & Decision Policy",
     "provenance": "structural — pack board 3 wiring, 9 September 2026"
    },
    {
     "to": "ADM-337",
     "trigger": "Routing Simulator & Conflict Detection",
     "provenance": "structural — pack board 3 wiring, 9 September 2026"
    }
   ]
  },
  "density": "compact",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen a metric directory (§KPI Cards) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's",
  "purpose": "Provide administrators with a centralized overview of all approval matrices configured across TICVAI.",
  "layout": {
   "template": "dashboard",
   "regions": [
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "Active Approval Matrices",
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 21 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Approval Rules",
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 21 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Tenants Covered",
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 21 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Venues Covered",
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 21 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Departments Covered",
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 21 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Unassigned Rules",
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 21 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Routing Conflicts",
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 21 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Governance Warnings",
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 21 §KPI Cards"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The approval list; the counts above it resolve separately.",
   "error": "Could not load. Names which read failed and leaves the approval untouched.",
   "emptyFirstRun": "No approval yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the approval are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listApprovalMatrices",
    "contract": "approvals",
    "purpose": "Matrices in force",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "entryState": {
   "preloaded": [
    "Active Approval Matrices",
    "Approval Rules",
    "Tenants Covered",
    "Venues Covered",
    "Departments Covered",
    "Unassigned Rules"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-329",
   "workshopBoard": "wireframes/WS32 Approval Workflows and Governance Board 3.dc.html#adm-329"
  },
  "apisNote": "Regenerated 9 September 2026 from Approval_Workflows_and_Governance_Reference.pdf page 21. 0 of 0 labels bound to a contract property; 8 of 14 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-330",
  "name": "Approval Authority Matrix",
  "module": "Platform",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Approval_Workflows_and_Governance_Reference.pdf",
   "board": "3",
   "number": "2",
   "page": 22
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/platform/approval-authority-matrix-adm-330",
   "component": "apps/ticvai-web/src/routes/platform/ApprovalAuthorityMatrix.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-329"
   ],
   "exitTo": [
    "ADM-329"
   ],
   "transitions": [
    {
     "to": "ADM-329",
     "trigger": "Back to Approval Matrix Command Center",
     "provenance": "structural — pack board 3 wiring, 9 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configuration Dimensions) and no display directory — it is settings, not a population",
  "purpose": "Provide a visual table showing who can approve what and up to which authority level.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Role",
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 22 §Configuration Dimensions"
      },
      {
       "kind": "selectField",
       "label": "User",
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 22 §Configuration Dimensions"
      },
      {
       "kind": "selectField",
       "label": "Department",
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 22 §Configuration Dimensions"
      },
      {
       "kind": "selectField",
       "label": "Venue",
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 22 §Configuration Dimensions"
      },
      {
       "kind": "selectField",
       "label": "Tenant",
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 22 §Configuration Dimensions"
      },
      {
       "kind": "selectField",
       "label": "Business process",
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 22 §Configuration Dimensions"
      },
      {
       "kind": "selectField",
       "label": "Transaction value",
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 22 §Configuration Dimensions"
      },
      {
       "kind": "selectField",
       "label": "Percentage",
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 22 §Configuration Dimensions"
      },
      {
       "kind": "selectField",
       "label": "Risk level",
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 22 §Configuration Dimensions"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The approval authority configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the approval authority untouched.",
   "emptyFirstRun": "No approval authority configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setApprovalMatrix",
    "contract": "approvals",
    "purpose": "Authority by role and value",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listApprovalMatrices"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-330",
   "workshopBoard": "wireframes/WS32 Approval Workflows and Governance Board 3.dc.html#adm-330"
  },
  "apisNote": "Regenerated 9 September 2026 from Approval_Workflows_and_Governance_Reference.pdf page 22. 0 of 0 labels bound to a contract property; 9 of 17 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-331",
  "name": "Organizational Hierarchy Routing",
  "module": "Platform",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Approval_Workflows_and_Governance_Reference.pdf",
   "board": "3",
   "number": "3",
   "page": 23
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/platform/organizational-hierarchy-routing-adm-331",
   "component": "apps/ticvai-web/src/routes/platform/OrganizationalHierarchyRouting.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-329"
   ],
   "exitTo": [
    "ADM-329"
   ],
   "transitions": [
    {
     "to": "ADM-329",
     "trigger": "Back to Approval Matrix Command Center",
     "provenance": "structural — pack board 3 wiring, 9 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Configure approval routing based on the client's organizational hierarchy.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Approval_Workflows_and_Governance_Reference.pdf, page 23"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Approval_Workflows_and_Governance_Reference.pdf, page 23"
   }
  ],
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "components": [
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "setApprovalMatrix",
       "label": "Save approval matrix",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "setApprovalMatrix"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The organizational hierarchy routing list.",
   "error": "Could not load. Names which read failed and leaves the organizational hierarchy routing untouched.",
   "emptyFirstRun": "No organizational hierarchy routing yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the organizational hierarchy routing are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setApprovalMatrix",
    "contract": "approvals",
    "purpose": "Route up the hierarchy",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listApprovalMatrices"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-331",
   "workshopBoard": "wireframes/WS32 Approval Workflows and Governance Board 3.dc.html#adm-331"
  },
  "apisNote": "Regenerated 9 September 2026 from Approval_Workflows_and_Governance_Reference.pdf page 23. 0 of 0 labels bound to a contract property; 0 of 18 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-332",
  "name": "Department-Based Approval Matrix",
  "module": "Platform",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Approval_Workflows_and_Governance_Reference.pdf",
   "board": "3",
   "number": "4",
   "page": 24
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/platform/department-based-approval-matrix-adm-332",
   "component": "apps/ticvai-web/src/routes/platform/DepartmentBasedApprovalMatrix.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-329"
   ],
   "exitTo": [
    "ADM-329"
   ],
   "transitions": [
    {
     "to": "ADM-329",
     "trigger": "Back to Approval Matrix Command Center",
     "provenance": "structural — pack board 3 wiring, 9 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Critical configuration change) and no display directory — it is settings, not a population",
  "purpose": "Allow different departments to maintain different approval authority structures.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "→ IT Director",
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 24 §Critical configuration change"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "banner",
       "label": "Permissions this screen separates",
       "notes": "**The pack separates these permissions and no action on the screen claims them yet:** → Security Manager. Each needs attaching to the control it gates, or the screen needs the control.",
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 24 §Access permission modification"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The department-based approval configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the department-based approval untouched.",
   "emptyFirstRun": "No department-based approval configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setApprovalMatrix",
    "contract": "approvals",
    "purpose": "By department",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listApprovalMatrices"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-332",
   "workshopBoard": "wireframes/WS32 Approval Workflows and Governance Board 3.dc.html#adm-332"
  },
  "apisNote": "Regenerated 9 September 2026 from Approval_Workflows_and_Governance_Reference.pdf page 24. 0 of 0 labels bound to a contract property; 2 of 12 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-333",
  "name": "Venue & Tenant Approval Matrix",
  "module": "Platform",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Approval_Workflows_and_Governance_Reference.pdf",
   "board": "3",
   "number": "5",
   "page": 24
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/platform/venue-tenant-approval-matrix-adm-333",
   "component": "apps/ticvai-web/src/routes/platform/VenueTenantApprovalMatrix.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-329"
   ],
   "exitTo": [
    "ADM-329"
   ],
   "transitions": [
    {
     "to": "ADM-329",
     "trigger": "Back to Approval Matrix Command Center",
     "provenance": "structural — pack board 3 wiring, 9 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Allow approval policies to differ between TICVAI clients and between venues belonging to the same client.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Approval_Workflows_and_Governance_Reference.pdf, page 24"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Approval_Workflows_and_Governance_Reference.pdf, page 24"
   }
  ],
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "components": [
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "setApprovalMatrix",
       "label": "Save approval matrix",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "setApprovalMatrix"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The venue tenant approval list.",
   "error": "Could not load. Names which read failed and leaves the venue tenant approval untouched.",
   "emptyFirstRun": "No venue tenant approval yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the venue tenant approval are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setApprovalMatrix",
    "contract": "approvals",
    "purpose": "By venue and tenant",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listApprovalMatrices"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-333",
   "workshopBoard": "wireframes/WS32 Approval Workflows and Governance Board 3.dc.html#adm-333"
  },
  "apisNote": "Regenerated 9 September 2026 from Approval_Workflows_and_Governance_Reference.pdf page 24. 0 of 0 labels bound to a contract property; 0 of 10 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-334",
  "name": "Value & Threshold Routing",
  "module": "Platform",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Approval_Workflows_and_Governance_Reference.pdf",
   "board": "3",
   "number": "6",
   "page": 25
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/platform/value-threshold-routing-adm-334",
   "component": "apps/ticvai-web/src/routes/platform/ValueThresholdRouting.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-329"
   ],
   "exitTo": [
    "ADM-329"
   ],
   "transitions": [
    {
     "to": "ADM-329",
     "trigger": "Back to Approval Matrix Command Center",
     "provenance": "structural — pack board 3 wiring, 9 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Configure approval authority according to transaction value or percentage thresholds. Example — Refund",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Approval_Workflows_and_Governance_Reference.pdf, page 25"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Approval_Workflows_and_Governance_Reference.pdf, page 25"
   }
  ],
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "components": [
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "setApprovalMatrix",
       "label": "Save approval matrix",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "setApprovalMatrix"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The value threshold routing list.",
   "error": "Could not load. Names which read failed and leaves the value threshold routing untouched.",
   "emptyFirstRun": "No value threshold routing yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the value threshold routing are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setApprovalMatrix",
    "contract": "approvals",
    "purpose": "By value threshold",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listApprovalMatrices"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-334",
   "workshopBoard": "wireframes/WS32 Approval Workflows and Governance Board 3.dc.html#adm-334"
  },
  "apisNote": "Regenerated 9 September 2026 from Approval_Workflows_and_Governance_Reference.pdf page 25. 0 of 0 labels bound to a contract property; 0 of 9 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-335",
  "name": "Risk-Based & Conditional Routing",
  "module": "Platform",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Approval_Workflows_and_Governance_Reference.pdf",
   "board": "3",
   "number": "7",
   "page": 26
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/platform/risk-based-conditional-routing-adm-335",
   "component": "apps/ticvai-web/src/routes/platform/RiskBasedConditionalRouting.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-329"
   ],
   "exitTo": [
    "ADM-329"
   ],
   "transitions": [
    {
     "to": "ADM-329",
     "trigger": "Back to Approval Matrix Command Center",
     "provenance": "structural — pack board 3 wiring, 9 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Dynamically modify approval routing based on the risk or context of the request.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Approval_Workflows_and_Governance_Reference.pdf, page 26"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Approval_Workflows_and_Governance_Reference.pdf, page 26"
   }
  ],
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "components": [
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "setApprovalMatrix",
       "label": "Save approval matrix",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "setApprovalMatrix"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The risk-based conditional routing list.",
   "error": "Could not load. Names which read failed and leaves the risk-based conditional routing untouched.",
   "emptyFirstRun": "No risk-based conditional routing yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the risk-based conditional routing are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setApprovalMatrix",
    "contract": "approvals",
    "purpose": "By risk and condition",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listApprovalMatrices"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-335",
   "workshopBoard": "wireframes/WS32 Approval Workflows and Governance Board 3.dc.html#adm-335"
  },
  "apisNote": "Regenerated 9 September 2026 from Approval_Workflows_and_Governance_Reference.pdf page 26. 0 of 0 labels bound to a contract property; 0 of 22 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-336",
  "name": "Approver Group & Decision Policy",
  "module": "Platform",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Approval_Workflows_and_Governance_Reference.pdf",
   "board": "3",
   "number": "8",
   "page": 27
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/platform/approver-group-decision-policy-adm-336",
   "component": "apps/ticvai-web/src/routes/platform/ApproverGroupDecisionPolicy.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-329"
   ],
   "exitTo": [
    "ADM-329"
   ],
   "transitions": [
    {
     "to": "ADM-329",
     "trigger": "Back to Approval Matrix Command Center",
     "provenance": "structural — pack board 3 wiring, 9 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Define cases where approval authority belongs to multiple people rather than one individual.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Approval_Workflows_and_Governance_Reference.pdf, page 27"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Approval_Workflows_and_Governance_Reference.pdf, page 27"
   }
  ],
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "components": [
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "setApprovalControlPolicy",
       "label": "Save",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "setApprovalControlPolicy"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The approver group decision list.",
   "error": "Could not load. Names which read failed and leaves the approver group decision untouched.",
   "emptyFirstRun": "No approver group decision yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the approver group decision are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setApprovalControlPolicy",
    "contract": "approvals",
    "purpose": "Approver groups and decision policy",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listApprovalControlPolicies"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-336",
   "workshopBoard": "wireframes/WS32 Approval Workflows and Governance Board 3.dc.html#adm-336"
  },
  "apisNote": "Regenerated 9 September 2026 from Approval_Workflows_and_Governance_Reference.pdf page 27. 0 of 0 labels bound to a contract property; 0 of 11 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-337",
  "name": "Routing Simulator & Conflict Detection",
  "module": "Platform",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Approval_Workflows_and_Governance_Reference.pdf",
   "board": "3",
   "number": "9",
   "page": 27
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/platform/routing-simulator-conflict-detection-adm-337",
   "component": "apps/ticvai-web/src/routes/platform/RoutingSimulatorConflictDetection.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-329"
   ],
   "exitTo": [
    "ADM-329"
   ],
   "transitions": [
    {
     "to": "ADM-329",
     "trigger": "Back to Approval Matrix Command Center",
     "provenance": "structural — pack board 3 wiring, 9 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Allow administrators to test the complete approval matrix before deployment. This is particularly important because Board 3 can contain hundreds of combinations.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Approval_Workflows_and_Governance_Reference.pdf, page 27"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Approval_Workflows_and_Governance_Reference.pdf, page 27"
   }
  ],
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "components": [
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "evaluateApprovalRequirement",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "evaluateApprovalRequirement"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The routing simulator conflict list.",
   "error": "Could not load. Names which read failed and leaves the routing simulator conflict untouched.",
   "emptyFirstRun": "No routing simulator conflict yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the routing simulator conflict are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "evaluateApprovalRequirement",
    "contract": "approvals",
    "purpose": "Where would this route",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "simulateWorkflowTestingImpact",
    "contract": "approvals",
    "purpose": "Conflicts in the matrix",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-337",
   "workshopBoard": "wireframes/WS32 Approval Workflows and Governance Board 3.dc.html#adm-337"
  },
  "apisNote": "Regenerated 9 September 2026 from Approval_Workflows_and_Governance_Reference.pdf page 27. 0 of 0 labels bound to a contract property; 0 of 26 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-338",
  "name": "AI Routing Advisor & Matrix Optimization",
  "module": "Platform",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Approval_Workflows_and_Governance_Reference.pdf",
   "board": "3",
   "number": "10",
   "page": 28
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/platform/ai-routing-advisor-matrix-optimization-adm-338",
   "component": "apps/ticvai-web/src/routes/platform/AiRoutingAdvisorMatrixOptimization.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-329"
   ],
   "exitTo": [
    "ADM-329"
   ],
   "transitions": [
    {
     "to": "ADM-329",
     "trigger": "Back to Approval Matrix Command Center",
     "provenance": "structural — pack board 3 wiring, 9 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Use TICVAI AI to analyze approval behavior and recommend improvements to the approval matrix. The source requires AI risk assessment, priority scoring and escalation recommendations.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Approval_Workflows_and_Governance_Reference.pdf, page 28"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Approval_Workflows_and_Governance_Reference.pdf, page 28"
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
       "impliedBy": "listApprovalMatrices",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The routing advisor optimization list.",
   "error": "Could not load. Names which read failed and leaves the routing advisor optimization untouched.",
   "emptyFirstRun": "No routing advisor optimization yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the routing advisor optimization are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listApprovalMatrices",
    "contract": "approvals",
    "purpose": "The matrix being advised on",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-338",
   "workshopBoard": "wireframes/WS32 Approval Workflows and Governance Board 3.dc.html#adm-338"
  },
  "apisNote": "Regenerated 9 September 2026 from Approval_Workflows_and_Governance_Reference.pdf page 28. 0 of 0 labels bound to a contract property; 0 of 12 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
 "evaluateApprovalRequirement": {
  "method": "POST",
  "path": "/approval-requests/evaluate",
  "contract": "approvals",
  "summary": "Does this need approval, and from whom",
  "permission": "APPROVAL_VIEW",
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
  "responds": "ApprovalRequirement"
 },
 "listApprovalMatrices": {
  "method": "GET",
  "path": "/approval-matrices",
  "contract": "approvals",
  "summary": "What requires approval here",
  "permission": "APPROVAL_CONFIGURE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "kind",
    "in": "query",
    "required": null
   },
   {
    "name": "effective",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "ApprovalMatrix"
 },
 "setApprovalControlPolicy": {
  "method": "PUT",
  "path": "/approval-control-policies",
  "contract": "approvals",
  "summary": "Require a second, independent pair of eyes",
  "permission": "APPROVAL_CONFIGURE",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "ApprovalControlPolicy",
  "responds": "ApprovalControlPolicy"
 },
 "setApprovalMatrix": {
  "method": "PUT",
  "path": "/approval-matrices",
  "contract": "approvals",
  "summary": "Configure what requires approval",
  "permission": "APPROVAL_CONFIGURE",
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
  "requestBody": "ApprovalMatrix",
  "responds": "ApprovalMatrix"
 },
 "simulateWorkflowTestingImpact": {
  "method": "PUT",
  "path": "/workflow-testing-impact",
  "contract": "approvals",
  "summary": "Workflow Testing, Simulation & Impact Analysis",
  "permission": "APPROVAL_CONFIGURE",
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
  "requestBody": "WorkflowTestingSimulationImpactAnalysisInput",
  "responds": "WorkflowTestingSimulationImpactAnalysisView"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "ApprovalControlPolicy": {
  "type": "object",
  "x-ticvai-persistence": "approvals.control_policy",
  "description": "Approvals boards 6.2 and 6.3. **Which decisions one person may not take alone** — distinct from which roles one person may not hold, which is `identity.setSegregationRules`.\n",
  "required": [
   "code",
   "control"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "code": {
    "type": "string"
   },
   "name": {
    "type": "string"
   },
   "appliesToRequestKinds": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/ApprovalKind"
    }
   },
   "appliesAboveValue": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "control": {
    "type": "string",
    "enum": [
     "fourEyes",
     "dualControl",
     "separationFromRequester",
     "separationFromExecutor"
    ],
    "description": "**`fourEyes` is two different people; `dualControl` is two people from different groups.** The second is stronger and is what a finance auditor means, and collapsing them makes the stronger control unexpressible.\n"
   },
   "requiredApproverGroupIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "minimumApprovers": {
    "type": "integer",
    "default": 2
   },
   "requiresStepUp": {
    "type": "boolean",
    "default": false
   },
   "requiresSignature": {
    "type": "boolean",
    "default": false
   },
   "breakGlassAllowed": {
    "type": "boolean",
    "default": false,
    "description": "**Whether the control may be overridden in an emergency**, and if so it raises an alert rather than passing quietly. A control with no break-glass will be worked around by hand at three in the morning, which is worse.\n"
   },
   "scopePath": {
    "type": "string"
   },
   "isActive": {
    "type": "boolean",
    "default": true
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
 "ApprovalMatrix": {
  "type": "object",
  "x-ticvai-persistence": "approvals.matrix",
  "required": [
   "kind",
   "scopeLevel",
   "rules"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "kind": {
    "$ref": "#/components/schemas/ApprovalKind"
   },
   "scopeLevel": {
    "type": "string",
    "enum": [
     "tenant",
     "region",
     "venue"
    ]
   },
   "scopePath": {
    "type": "string",
    "readOnly": true
   },
   "version": {
    "type": "integer",
    "readOnly": true,
    "description": "11.1.80. **A request is decided by the rules it was raised under.** Changing the matrix mid-flight would mean an approver answering a question that changed while they read it.\n**(`kind`, `scopePath`, `version`) is unique**, and a stored version is never edited: a request's `matrixVersion` names exactly one rule set (decided 28 September, audit R129 (2)).\n"
   },
   "rules": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/ApprovalRule"
    }
   },
   "isActive": {
    "type": "boolean"
   }
  }
 },
 "ApprovalRequirement": {
  "type": "object",
  "x-ticvai-persistence": "none — computed",
  "description": "The answer to \"does this need approval\", returned before the action.",
  "required": [
   "isRequired"
  ],
  "properties": {
   "isRequired": {
    "type": "boolean"
   },
   "matchedRule": {
    "allOf": [
     {
      "$ref": "#/components/schemas/ApprovalRule"
     }
    ],
    "nullable": true
   },
   "matrixVersion": {
    "type": "integer",
    "nullable": true
   },
   "approvers": {
    "type": "array",
    "description": "Resolved, with delegations applied. **Named so the caller can say \"this needs Sara\"** rather than \"this needs approval\".\n",
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
      "level": {
       "type": "integer"
      },
      "isDelegate": {
       "type": "boolean"
      },
      "delegatedFrom": {
       "type": "string",
       "format": "uuid",
       "nullable": true
      }
     }
    }
   },
   "slaMinutes": {
    "type": "integer",
    "nullable": true
   },
   "noApproverAvailable": {
    "type": "boolean",
    "description": "**The case that must not fail silently.** A rule requiring a role nobody at this venue holds means the action is blocked forever, and the caller needs to know that now rather than after raising a request nobody can decide.\n"
   }
  }
 },
 "ApprovalRule": {
  "type": "object",
  "x-ticvai-persistence": "approvals.rule",
  "required": [
   "order",
   "approverRoleIds",
   "mode"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "description": "**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"
   },
   "order": {
    "type": "integer",
    "description": "**First match wins.** Explicit ordering is what makes a matrix reviewable — an unordered set of overlapping rules is one nobody can reason about.\n"
   },
   "minAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "maxAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "riskScoreAbove": {
    "type": "number",
    "nullable": true,
    "description": "11.1.12. **Not matched against the AI risk score** (29 September, build pass, group G2). The AI assessment on a request (`ApprovalRequest.aiAssessment`, from `ai.scoreApprovalRequest`) is context for the reviewer only (MoM 8 September: AI never influences approve or reject), and routing a request to more approvers because of it would be influence. A rule with this set matches only a `riskScore` the requesting contract passes in `attributes` from its own deterministic rules (a payment's rule score, for example). Using the AI score here needs the client to say so.\n"
   },
   "condition": {
    "type": "string",
    "nullable": true,
    "description": "11.1.13. Evaluated against the attributes the caller supplied.\n\n**No condition language is defined yet** (pull audit R104, 26 September): the grammar, the attributes it may name and how two conditions are compared for `unreachableRule` are an open decision, not something to infer from this field.\n"
   },
   "approverRoleIds": {
    "type": "array",
    "minItems": 1,
    "description": "Role ids from `identity.listRoles` (`Role.id`), which is where an editor gets the names to show and pick from. This contract stores the ids only.\n",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "approverScopeLevel": {
    "type": "string",
    "enum": [
     "venue",
     "department",
     "region",
     "tenant"
    ],
    "description": "11.1.39. Which organisational level the approver must sit at."
   },
   "mode": {
    "$ref": "#/components/schemas/ApprovalMode"
   },
   "levels": {
    "type": "integer",
    "default": 1,
    "description": "11.1.3. Multi-level chains ask each level in turn."
   },
   "requiresMfa": {
    "type": "boolean",
    "default": false
   },
   "requiresSignature": {
    "type": "boolean",
    "default": false
   },
   "slaMinutes": {
    "type": "integer",
    "nullable": true,
    "description": "11.1.14. Null means no SLA, which is different from a long one."
   },
   "escalateAfterMinutes": {
    "type": "integer",
    "nullable": true
   },
   "escalateToRoleIds": {
    "type": "array",
    "description": "Role ids from `identity.listRoles`, as `approverRoleIds`.",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "expiresAfterMinutes": {
    "type": "integer",
    "nullable": true,
    "description": "11.1.53. An unanswered request eventually stops waiting."
   },
   "externalProviderId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "11.1.65 (29 September). **This level is decided in an external workflow system** (`ApprovalExternalProvider`) rather than by a person in TICVAI. `approverRoleIds` stay required: they are who decides if the provider does not answer in time and its `onTimeout` is `fallBackToRoles`.\n"
   }
  }
 },
 "Money": {
  "type": "object",
  "x-ticvai-persistence-kind": "valueObject",
  "x-ticvai-persistence-column": "numeric(18,4)",
  "description": "**On the wire this is three fields; in the database it is one column.**\n24 August. Every column typed `Money` was landing as `jsonb` — 129 of them, including `orders.shift.opening_float`, `inventory.purchase_order.total` and `promotions.voucher.balance`. **`orders.cash_movement.amount` was `numeric(18,4)` because somebody hand-typed that one**, and the inconsistency is what made it visible.\n**A jsonb price cannot be summed in SQL.** Every total, variance and reconciliation moves into application code — and a shift variance computed in .NET against a ledger computed in Postgres is two answers to one question. That is F13 month-end and F98 takings-to-ledger, both walked, both assuming the arithmetic is in the database.\n**`currency` and `scale` are not stored per row.** ADR-0018 makes them region-scoped and not overridable below, so they resolve from the scope walk — storing AED against nine million rows in a UAE region is nine million copies of a fact that cannot differ. A row that needed its own currency would be a row in the wrong region.\n**They stay on the wire** because a client reading a figure should not have to walk a hierarchy to know what it means.\n",
  "required": [
   "amount",
   "currency",
   "scale"
  ],
  "properties": {
   "amount": {
    "type": "string",
    "description": "Decimal string, never a float. Up to 4 decimal places. **Persisted as `numeric(18,4)`** — the string is a transport choice, so a JavaScript client cannot round a fare in transit.\n",
    "pattern": "^-?\\d+(\\.\\d{1,4})?$"
   },
   "currency": {
    "type": "string",
    "description": "**Resolved from the region, not stored on the row** (ADR-0018). OMR uses 3 decimal places and AED uses 2 — a venue on a different scale from its region is a ledger that cannot consolidate.\n",
    "pattern": "^[A-Z]{3}$"
   },
   "scale": {
    "type": "integer",
    "description": "Resolved from the region alongside `currency`.",
    "minimum": 0,
    "maximum": 4
   }
  }
 },
 "WorkflowTestingSimulationImpactAnalysisInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; the outcome is recorded as approvals.workflow_version test results (data model for the agreed operations, 29 September)",
  "description": "**What Workflow Testing, Simulation & Impact Analysis submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "workflowId": {
    "type": "string",
    "description": "Workflow under test"
   },
   "testMode": {
    "type": "string",
    "enum": [
     "manualTestCase",
     "sampleTransaction",
     "historicalReplay",
     "scenarioSimulation",
     "batchTest"
    ],
    "description": "How the workflow is tested"
   },
   "version": {
    "type": "string",
    "description": "Version under test"
   },
   "compareWithVersion": {
    "type": "string",
    "description": "Existing version to compare against for regression"
   },
   "inputPayload": {
    "type": "string",
    "description": "Sample transaction as a JSON document, for manual and sample tests"
   },
   "replayFrom": {
    "type": "string",
    "format": "date",
    "description": "Historical replay start"
   },
   "replayTo": {
    "type": "string",
    "format": "date",
    "description": "Historical replay end"
   }
  },
  "required": [
   "workflowId",
   "testMode"
  ]
 },
 "WorkflowTestingSimulationImpactAnalysisView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — computed by simulation over approvals.workflow_version and the rules it calls; never executes actions (data model for the agreed operations, 29 September)",
  "description": "**What Workflow Testing, Simulation & Impact Analysis displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "workflowId": {
    "type": "string",
    "description": "Workflow under test"
   },
   "testMode": {
    "type": "string",
    "enum": [
     "manualTestCase",
     "sampleTransaction",
     "historicalReplay",
     "scenarioSimulation",
     "batchTest"
    ],
    "description": "How the workflow is tested"
   },
   "rulesEvaluated": {
    "type": "integer",
    "description": "Rules Evaluated"
   },
   "conditionsMatched": {
    "type": "integer",
    "description": "Conditions Matched"
   },
   "decisions": {
    "type": "integer",
    "description": "Decisions"
   },
   "approvalPath": {
    "type": "string",
    "description": "Approval Path"
   },
   "actions": {
    "type": "integer",
    "description": "Actions"
   },
   "notifications": {
    "type": "integer",
    "description": "Notifications"
   },
   "sla": {
    "type": "string",
    "description": "SLA"
   },
   "expectedOutcome": {
    "type": "string",
    "description": "Expected Outcome"
   },
   "version": {
    "type": "string",
    "description": "Version under test"
   },
   "compareWithVersion": {
    "type": "string",
    "description": "Existing version to compare against for regression"
   },
   "inputPayload": {
    "type": "string",
    "description": "Sample transaction as a JSON document, for manual and sample tests"
   },
   "replayFrom": {
    "type": "string",
    "format": "date",
    "description": "Historical replay start"
   },
   "replayTo": {
    "type": "string",
    "format": "date",
    "description": "Historical replay end"
   }
  },
  "required": [
   "workflowId",
   "testMode"
  ]
 }
}
```
