# WS18 — Approval Workflows and Governance board 6

**10 screens · 3 operations · 4 schemas · 1 permissions**

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

- **Every control that can be refused must be gated.** 1 permissions apply here:
  `APPROVAL_CONFIGURE`. A control nobody can use must say so,
  not sit enabled and fail.
- **0 of these operations work offline**
  
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `ADM-339` | Governance & Compliance Command Center | commandCentre | 0 | 0 | — |
| `ADM-340` | Segregation of Duties Policy Manager | configEditor | 0 | 0 | — |
| `ADM-341` | Four-Eyes & Dual-Control Policy | configEditor | 0 | 0 | — |
| `ADM-342` | Authentication & MFA Policy Manager | listDetail | 3 | 0 | — |
| `ADM-343` | Sensitive Action Confirmation | configEditor | 0 | 0 | — |
| `ADM-344` | Digital Signature Management | configEditor | 0 | 0 | — |
| `ADM-345` | Immutable Approval Record & Tamper Detection | listDetail | 0 | 0 | — |
| `ADM-346` | Approval Record Retention Policy | configEditor | 0 | 0 | — |
| `ADM-347` | Regulatory Audit & Evidence Center | listDetail | 0 | 0 | — |
| `ADM-348` | Governance Risk & AI Compliance Advisor | listDetail | 0 | 0 | — |

## Thin screens in this batch

**ADM-340, ADM-342, ADM-345, ADM-347, ADM-348 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "ADM-339",
  "name": "Governance & Compliance Command Center",
  "module": "Platform",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Approval_Workflows_and_Governance_Reference.pdf",
   "board": "6",
   "number": "1",
   "page": 50
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/platform/governance-compliance-command-center-adm-339",
   "component": "apps/ticvai-web/src/routes/platform/GovernanceComplianceCommandCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-002"
   ],
   "exitTo": [
    "ADM-002",
    "ADM-340",
    "ADM-341",
    "ADM-342",
    "ADM-343",
    "ADM-344",
    "ADM-345",
    "ADM-346",
    "ADM-347",
    "ADM-348"
   ],
   "transitions": [
    {
     "to": "ADM-002",
     "trigger": "Back to Platform Dashboard",
     "provenance": "structural — pack board 6 wiring, 9 September 2026",
     "back": true
    },
    {
     "to": "ADM-348",
     "trigger": "Governance Risk & AI Compliance Advisor",
     "provenance": "structural — pack board 6 wiring, 9 September 2026"
    },
    {
     "to": "ADM-340",
     "trigger": "Segregation of Duties Policy Manager",
     "provenance": "structural — pack board 6 wiring, 9 September 2026"
    },
    {
     "to": "ADM-341",
     "trigger": "Four-Eyes & Dual-Control Policy",
     "provenance": "structural — pack board 6 wiring, 9 September 2026"
    },
    {
     "to": "ADM-342",
     "trigger": "Authentication & MFA Policy Manager",
     "provenance": "structural — pack board 6 wiring, 9 September 2026"
    },
    {
     "to": "ADM-343",
     "trigger": "Sensitive Action Confirmation",
     "provenance": "structural — pack board 6 wiring, 9 September 2026"
    },
    {
     "to": "ADM-344",
     "trigger": "Digital Signature Management",
     "provenance": "structural — pack board 6 wiring, 9 September 2026"
    },
    {
     "to": "ADM-345",
     "trigger": "Immutable Approval Record & Tamper Detection",
     "provenance": "structural — pack board 6 wiring, 9 September 2026"
    },
    {
     "to": "ADM-346",
     "trigger": "Approval Record Retention Policy",
     "provenance": "structural — pack board 6 wiring, 9 September 2026"
    },
    {
     "to": "ADM-347",
     "trigger": "Regulatory Audit & Evidence Center",
     "provenance": "structural — pack board 6 wiring, 9 September 2026"
    }
   ]
  },
  "density": "compact",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen a metric directory (§KPI Cards) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's",
  "purpose": "Provide administrators, auditors and security teams with an overview of approval governance health across the organization.",
  "layout": {
   "template": "dashboard",
   "regions": [
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "Governance Compliance %",
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 50 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "SoD Conflicts",
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 50 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Four-Eyes Protected Actions",
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 50 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "MFA-Protected Approvals",
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 50 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Digital Signatures",
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 50 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Tamper Alerts",
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 50 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Retention Exceptions",
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 50 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Audit Findings",
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 50 §KPI Cards"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The governance compliance list; the counts above it resolve separately.",
   "error": "Could not load. Names which read failed and leaves the governance compliance untouched.",
   "emptyFirstRun": "No governance compliance yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the governance compliance are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "entryState": {
   "preloaded": [
    "Governance Compliance %",
    "SoD Conflicts",
    "Four-Eyes Protected Actions",
    "MFA-Protected Approvals",
    "Digital Signatures",
    "Tamper Alerts"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-339"
  },
  "apisNote": "Regenerated 9 September 2026 from Approval_Workflows_and_Governance_Reference.pdf page 50. 0 of 0 labels bound to a contract property; 8 of 20 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-340",
  "name": "Segregation of Duties Policy Manager",
  "module": "Platform",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Approval_Workflows_and_Governance_Reference.pdf",
   "board": "6",
   "number": "2",
   "page": 51
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/platform/segregation-of-duties-policy-manager-adm-340",
   "component": "apps/ticvai-web/src/routes/platform/SegregationOfDutiesPolicyManager.tsx",
   "status": "notStarted"
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Price Configuration User) and no display directory — it is settings, not a population",
  "purpose": "Define combinations of actions that the same person must not be allowed to perform. The matrix explicitly states that users shall be prevented from approving their own requests.",
  "gaps": [
   {
    "operation": null,
    "why": "**Segregation of Duties Policy Manager declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either the write operations are missing or this screen is a view of something another screen builds.",
    "source": "contract — the screen's declared operations"
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
       "label": "=R",
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 51 §Price Configuration User"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The segregation duties policy configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the segregation duties policy untouched.",
   "emptyFirstRun": "No segregation duties policy configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-340"
  },
  "apisNote": "Regenerated 9 September 2026 from Approval_Workflows_and_Governance_Reference.pdf page 51. 0 of 0 labels bound to a contract property; 1 of 14 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "navigation": {
   "entryFrom": [
    "ADM-339"
   ],
   "exitTo": [
    "ADM-339"
   ],
   "transitions": [
    {
     "to": "ADM-339",
     "trigger": "Back to Governance & Compliance Command Center",
     "provenance": "structural — pack board 6 wiring, 9 September 2026",
     "back": true
    }
   ]
  },
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
  "id": "ADM-341",
  "name": "Four-Eyes & Dual-Control Policy",
  "module": "Platform",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Approval_Workflows_and_Governance_Reference.pdf",
   "board": "6",
   "number": "3",
   "page": 52
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/platform/four-eyes-dual-control-policy-adm-341",
   "component": "apps/ticvai-web/src/routes/platform/FourEyesDualControlPolicy.tsx",
   "status": "notStarted"
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Administrators should configure) and no display directory — it is settings, not a population",
  "purpose": "Configure sensitive actions requiring approval from at least two independent authorized persons. The source explicitly requires dual approval capability for sensitive operations.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "textField",
       "label": "Two different users required",
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 52 §Administrators should configure"
      },
      {
       "kind": "selectField",
       "label": "Different roles required",
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 52 §Administrators should configure"
      },
      {
       "kind": "textField",
       "label": "Different departments if required",
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 52 §Administrators should configure"
      },
      {
       "kind": "textField",
       "label": "No delegated duplicate identity",
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 52 §Administrators should configure"
      },
      {
       "kind": "selectField",
       "label": "Minimum authority level",
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 52 §Administrators should configure"
      },
      {
       "kind": "textField",
       "label": "Sequential or parallel approval",
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 52 §Administrators should configure"
      },
      {
       "kind": "selectField",
       "label": "Both approvals mandatory",
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 52 §Administrators should configure"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The four-eyes dual- policy configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the four-eyes dual- policy untouched.",
   "emptyFirstRun": "No four-eyes dual- policy configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-341"
  },
  "apisNote": "Regenerated 9 September 2026 from Approval_Workflows_and_Governance_Reference.pdf page 52. 0 of 0 labels bound to a contract property; 7 of 11 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "navigation": {
   "entryFrom": [
    "ADM-339"
   ],
   "exitTo": [
    "ADM-339"
   ],
   "transitions": [
    {
     "to": "ADM-339",
     "trigger": "Back to Governance & Compliance Command Center",
     "provenance": "structural — pack board 6 wiring, 9 September 2026",
     "back": true
    }
   ]
  },
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
  "id": "ADM-342",
  "name": "Authentication & MFA Policy Manager",
  "module": "Platform",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Approval_Workflows_and_Governance_Reference.pdf",
   "board": "6",
   "number": "4",
   "page": 53
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/platform/authentication-mfa-policy-manager-adm-342",
   "component": "apps/ticvai-web/src/routes/platform/AuthenticationMfaPolicyManager.tsx",
   "status": "notStarted"
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Define the authentication strength required before an approver can execute sensitive approval decisions. The source requires authentication before approval actions and supports MFA for sensitive approvals.",
  "gaps": [],
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "components": [
      {
       "kind": "dataTable",
       "derived": true,
       "impliedBy": "listMfaMethods",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      },
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "setStepUpPolicy",
       "label": "Save step up policy",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "setStepUpPolicy"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The authentication mfa policy list.",
   "error": "Could not load. Names which read failed and leaves the authentication mfa policy untouched.",
   "emptyFirstRun": "No authentication mfa policy yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the authentication mfa policy are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listStepUpPolicies",
    "contract": "approvals",
    "purpose": "Every action that can demand a second factor, its contract floor, and what is in force here",
    "trigger": "onLoad"
   },
   {
    "operationId": "setStepUpPolicy",
    "contract": "approvals",
    "purpose": "Raise the strength required before an action may be executed",
    "trigger": "onAction",
    "invalidates": [
     "listStepUpPolicies"
    ]
   },
   {
    "operationId": "listMfaMethods",
    "contract": "identity",
    "purpose": "Which methods approvers have enrolled, because a policy demanding a factor nobody holds locks the action",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-342"
  },
  "apisNote": "**Wired on 10 September 2026.** This screen came from the workshop pack `Approval_Workflows_and_Governance` board 6 and declared no operation at all - its own `gaps` entry read *the name promises authoring and the contract offers none*. It now reads and raises `StepUpPolicy`.\n\n**`listMfaMethods` is here for a reason that is easy to miss.** A policy demanding `mfa` on an action whose approvers have enrolled no method does not secure the action, it stops it - and the person who finds out is an approver with a decision in front of them.",
  "navigation": {
   "entryFrom": [
    "ADM-339"
   ],
   "exitTo": [
    "ADM-339"
   ],
   "transitions": [
    {
     "to": "ADM-339",
     "trigger": "Back to Governance & Compliance Command Center",
     "provenance": "structural — pack board 6 wiring, 9 September 2026",
     "back": true
    }
   ]
  },
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
  "id": "ADM-343",
  "name": "Sensitive Action Confirmation",
  "module": "Platform",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Approval_Workflows_and_Governance_Reference.pdf",
   "board": "6",
   "number": "5",
   "page": 53
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/platform/sensitive-action-confirmation-adm-343",
   "component": "apps/ticvai-web/src/routes/platform/SensitiveActionConfirmation.tsx",
   "status": "notStarted"
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configuration) and no display directory — it is settings, not a population",
  "purpose": "Configure the final confirmation requirements before a sensitive approval becomes binding. The source specifically requires confirmation before execution of sensitive approvals.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Action",
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 53 §Configuration"
      },
      {
       "kind": "selectField",
       "label": "Amount",
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 53 §Configuration"
      },
      {
       "kind": "selectField",
       "label": "Risk",
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 53 §Configuration"
      },
      {
       "kind": "selectField",
       "label": "department",
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 53 §Configuration"
      },
      {
       "kind": "selectField",
       "label": "venue",
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 53 §Configuration"
      },
      {
       "kind": "selectField",
       "label": "tenant",
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 53 §Configuration"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The sensitive action confirmation configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the sensitive action confirmation untouched.",
   "emptyFirstRun": "No sensitive action confirmation configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-343"
  },
  "apisNote": "Regenerated 9 September 2026 from Approval_Workflows_and_Governance_Reference.pdf page 53. 0 of 0 labels bound to a contract property; 6 of 17 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "navigation": {
   "entryFrom": [
    "ADM-339"
   ],
   "exitTo": [
    "ADM-339"
   ],
   "transitions": [
    {
     "to": "ADM-339",
     "trigger": "Back to Governance & Compliance Command Center",
     "provenance": "structural — pack board 6 wiring, 9 September 2026",
     "back": true
    }
   ]
  },
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
  "id": "ADM-344",
  "name": "Digital Signature Management",
  "module": "Platform",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Approval_Workflows_and_Governance_Reference.pdf",
   "board": "6",
   "number": "6",
   "page": 54
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/platform/digital-signature-management-adm-344",
   "component": "apps/ticvai-web/src/routes/platform/DigitalSignatureManagement.tsx",
   "status": "notStarted"
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population",
  "purpose": "Manage workflows where approval decisions require a digital signature. The matrix explicitly requires digital-signature support for sensitive approvals.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Workflow requiring signature",
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 54 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Approval stage",
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 54 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Signer role",
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 54 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Signature requirement",
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 54 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Certificate information",
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 54 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Timestamp",
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 54 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Signature validation status",
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 54 §Configure"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The digital signature configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the digital signature untouched.",
   "emptyFirstRun": "No digital signature configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-344"
  },
  "apisNote": "Regenerated 9 September 2026 from Approval_Workflows_and_Governance_Reference.pdf page 54. 0 of 0 labels bound to a contract property; 8 of 19 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "navigation": {
   "entryFrom": [
    "ADM-339"
   ],
   "exitTo": [
    "ADM-339"
   ],
   "transitions": [
    {
     "to": "ADM-339",
     "trigger": "Back to Governance & Compliance Command Center",
     "provenance": "structural — pack board 6 wiring, 9 September 2026",
     "back": true
    }
   ]
  },
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
  "id": "ADM-345",
  "name": "Immutable Approval Record & Tamper Detection",
  "module": "Platform",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Approval_Workflows_and_Governance_Reference.pdf",
   "board": "6",
   "number": "7",
   "page": 55
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/platform/immutable-approval-record-tamper-detection-adm-345",
   "component": "apps/ticvai-web/src/routes/platform/ImmutableApprovalRecordTamperDetection.tsx",
   "status": "notStarted"
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Protect completed approval records from unauthorized modification. The matrix requires completed approval records to be immutable and requires detection of unauthorized modification attempts.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Approval_Workflows_and_Governance_Reference.pdf, page 55 §Display"
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
       "label": "Every immutable approval record",
       "columns": [
        "Record Integrity: VERIFIED ✓",
        "🔴 Potential Tamper Event Detected",
        "Record affected",
        "User/service",
        "Date/time",
        "attempted action",
        "source",
        "severity",
        "investigation status"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 55 §Display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected immutable approval record",
       "bindsTo": null,
       "columns": [
        "Record Integrity: VERIFIED ✓",
        "🔴 Potential Tamper Event Detected",
        "Record affected",
        "User/service",
        "Date/time",
        "attempted action",
        "source",
        "severity",
        "investigation status"
       ],
       "notes": "The pack groups this record's detail under its own headings: “APR-10543”, “Integrity Information”.",
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 55 §Display"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The immutable approval record list.",
   "error": "Could not load. Names which read failed and leaves the immutable approval record untouched.",
   "emptyFirstRun": "No immutable approval record yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the immutable approval record are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "entryState": {
   "preloaded": [
    "Record Integrity: VERIFIED ✓",
    "🔴 Potential Tamper Event Detected",
    "Record affected",
    "User/service",
    "Date/time",
    "attempted action"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-345"
  },
  "apisNote": "Regenerated 9 September 2026 from Approval_Workflows_and_Governance_Reference.pdf page 55. 0 of 9 labels bound to a contract property; 9 of 25 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "navigation": {
   "entryFrom": [
    "ADM-339"
   ],
   "exitTo": [
    "ADM-339"
   ],
   "transitions": [
    {
     "to": "ADM-339",
     "trigger": "Back to Governance & Compliance Command Center",
     "provenance": "structural — pack board 6 wiring, 9 September 2026",
     "back": true
    }
   ]
  },
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
  "id": "ADM-346",
  "name": "Approval Record Retention Policy",
  "module": "Platform",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Approval_Workflows_and_Governance_Reference.pdf",
   "board": "6",
   "number": "8",
   "page": 56
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/platform/approval-record-retention-policy-adm-346",
   "component": "apps/ticvai-web/src/routes/platform/ApprovalRecordRetentionPolicy.tsx",
   "status": "notStarted"
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configuration) and no display directory — it is settings, not a population",
  "purpose": "Define how long approval and governance records shall be retained. The matrix explicitly requires configurable approval record-retention policies.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Retention duration",
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 56 §Configuration"
      },
      {
       "kind": "selectField",
       "label": "Tenant",
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 56 §Configuration"
      },
      {
       "kind": "selectField",
       "label": "Country / jurisdiction",
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 56 §Configuration"
      },
      {
       "kind": "selectField",
       "label": "Record category",
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 56 §Configuration"
      },
      {
       "kind": "selectField",
       "label": "Workflow",
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 56 §Configuration"
      },
      {
       "kind": "selectField",
       "label": "Effective date",
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 56 §Configuration"
      },
      {
       "kind": "selectField",
       "label": "archival behavior",
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 56 §Configuration"
      },
      {
       "kind": "selectField",
       "label": "disposal behavior",
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 56 §Configuration"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The approval record retention configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the approval record retention untouched.",
   "emptyFirstRun": "No approval record retention configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-346"
  },
  "apisNote": "Regenerated 9 September 2026 from Approval_Workflows_and_Governance_Reference.pdf page 56. 0 of 0 labels bound to a contract property; 8 of 16 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "navigation": {
   "entryFrom": [
    "ADM-339"
   ],
   "exitTo": [
    "ADM-339"
   ],
   "transitions": [
    {
     "to": "ADM-339",
     "trigger": "Back to Governance & Compliance Command Center",
     "provenance": "structural — pack board 6 wiring, 9 September 2026",
     "back": true
    }
   ]
  },
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
  "id": "ADM-347",
  "name": "Regulatory Audit & Evidence Center",
  "module": "Platform",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Approval_Workflows_and_Governance_Reference.pdf",
   "board": "6",
   "number": "9",
   "page": 57
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/platform/regulatory-audit-evidence-center-adm-347",
   "component": "apps/ticvai-web/src/routes/platform/RegulatoryAuditEvidenceCenter.tsx",
   "status": "notStarted"
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Provide internal and external auditors with controlled access to complete approval evidence. The source specifically requires approval records suitable for regulatory audits.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Approval_Workflows_and_Governance_Reference.pdf, page 57"
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
       "label": "Search regulatory audit evidence",
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 57 §Search by"
      },
      {
       "kind": "multiSelect",
       "label": "Filter by",
       "columns": [
        "Request",
        "Transaction",
        "Customer",
        "Approver",
        "Requester",
        "Workflow",
        "Venue",
        "Department",
        "Date",
        "approval outcome",
        "risk",
        "value"
       ],
       "notes": "The pack filters this screen by request, transaction, customer, approver, requester, workflow and 6 more — which are present is a decision the pack already made.",
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 57 §Search by"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The regulatory audit evidence list.",
   "error": "Could not load. Names which read failed and leaves the regulatory audit evidence untouched.",
   "emptyFirstRun": "No regulatory audit evidence yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the regulatory audit evidence are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-347"
  },
  "apisNote": "Regenerated 9 September 2026 from Approval_Workflows_and_Governance_Reference.pdf page 57. 0 of 12 labels bound to a contract property; 12 of 17 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "navigation": {
   "entryFrom": [
    "ADM-339"
   ],
   "exitTo": [
    "ADM-339"
   ],
   "transitions": [
    {
     "to": "ADM-339",
     "trigger": "Back to Governance & Compliance Command Center",
     "provenance": "structural — pack board 6 wiring, 9 September 2026",
     "back": true
    }
   ]
  },
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
  "id": "ADM-348",
  "name": "Governance Risk & AI Compliance Advisor",
  "module": "Platform",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Approval_Workflows_and_Governance_Reference.pdf",
   "board": "6",
   "number": "10",
   "page": 58
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/platform/governance-risk-ai-compliance-advisor-adm-348",
   "component": "apps/ticvai-web/src/routes/platform/GovernanceRiskAiComplianceAdvisor.tsx",
   "status": "notStarted"
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Use AI to identify unusual governance patterns, potential policy weaknesses and compliance risks. This screen should assist compliance teams rather than automatically change governance policies.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Approval_Workflows_and_Governance_Reference.pdf, page 58"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Approval_Workflows_and_Governance_Reference.pdf, page 58"
   }
  ],
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "components": []
    }
   ]
  },
  "states": {
   "loading": "The governance risk compliance list.",
   "error": "Could not load. Names which read failed and leaves the governance risk compliance untouched.",
   "emptyFirstRun": "No governance risk compliance yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the governance risk compliance are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-348"
  },
  "apisNote": "Regenerated 9 September 2026 from Approval_Workflows_and_Governance_Reference.pdf page 58. 0 of 0 labels bound to a contract property; 0 of 14 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "navigation": {
   "entryFrom": [
    "ADM-339"
   ],
   "exitTo": [
    "ADM-339"
   ],
   "transitions": [
    {
     "to": "ADM-339",
     "trigger": "Back to Governance & Compliance Command Center",
     "provenance": "structural — pack board 6 wiring, 9 September 2026",
     "back": true
    }
   ]
  },
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
 "listMfaMethods": {
  "method": "GET",
  "path": "/auth/mfa/methods",
  "contract": "identity",
  "summary": "Enrolled MFA methods",
  "permission": null,
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [],
  "requestBody": null,
  "responds": "MfaMethod"
 },
 "listStepUpPolicies": {
  "method": "GET",
  "path": "/step-up-policies",
  "contract": "approvals",
  "summary": "What needs a second factor here",
  "permission": "APPROVAL_CONFIGURE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": "effective",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "StepUpPolicy"
 },
 "setStepUpPolicy": {
  "method": "PUT",
  "path": "/step-up-policies",
  "contract": "approvals",
  "summary": "Raise what needs a second factor",
  "permission": "APPROVAL_CONFIGURE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [],
  "requestBody": "StepUpPolicy",
  "responds": "StepUpPolicy"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "MfaKind": {
  "type": "string",
  "enum": [
   "totp",
   "smsOtp",
   "emailOtp",
   "biometric",
   "hardwareToken"
  ]
 },
 "MfaMethod": {
  "x-ticvai-persistence": "identity.mfa_method",
  "type": "object",
  "required": [
   "id",
   "kind",
   "isActive",
   "enrolledAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "kind": {
    "$ref": "#/components/schemas/MfaKind"
   },
   "label": {
    "type": "string",
    "nullable": true
   },
   "maskedTarget": {
    "type": "string",
    "nullable": true,
    "description": "Partially masked destination, so a person can tell two methods apart."
   },
   "isActive": {
    "type": "boolean"
   },
   "isPrimary": {
    "type": "boolean"
   },
   "enrolledAt": {
    "type": "string",
    "format": "date-time"
   },
   "lastUsedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   }
  }
 },
 "StepUpPolicy": {
  "x-ticvai-persistence": "approvals.step_up_policy",
  "type": "object",
  "required": [
   "operationId",
   "required"
  ],
  "properties": {
   "operationId": {
    "type": "string",
    "description": "The action governed. Names an operation, never a screen."
   },
   "required": {
    "allOf": [
     {
      "$ref": "#/components/schemas/StepUpStrength"
     }
    ],
    "description": "The strength in force at this scope."
   },
   "contractFloor": {
    "allOf": [
     {
      "$ref": "#/components/schemas/StepUpStrength"
     }
    ],
    "description": "What `x-ticvai-step-up` sets on the operation. Read only, and the value `required` may not go below.\n"
   },
   "scopeLevel": {
    "type": "string",
    "enum": [
     "tenant",
     "region",
     "venue"
    ],
    "description": "Where this rule was set, not where it applies."
   },
   "reason": {
    "type": "string",
    "maxLength": 512,
    "description": "Why it was raised. **An unexplained control is one somebody removes** the first time it is inconvenient.\n"
   },
   "setBy": {
    "type": "string",
    "format": "uuid"
   },
   "setAt": {
    "type": "string",
    "format": "date-time"
   }
  }
 },
 "StepUpStrength": {
  "type": "string",
  "description": "**Ordered, weakest first, and that ordering is what makes *raise only* checkable.** `pin` is a supervisor PIN captured in place — `roles.yaml` already resolves escalation that way and it is right for an action taken several times a shift. `mfa` is a challenge against an enrolled method and is right for an action taken a few times a month.\n",
  "enum": [
   "none",
   "pin",
   "mfa"
  ]
 }
}
```
