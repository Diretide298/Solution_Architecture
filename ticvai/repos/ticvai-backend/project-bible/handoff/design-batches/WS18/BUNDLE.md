# WS18 — Approval Workflows and Governance board 6

**10 screens · 16 operations · 16 schemas · 6 permissions**

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

- **Every control that can be refused must be gated.** 6 permissions apply here:
  `APPROVAL_CONFIGURE, APPROVAL_DECIDE, APPROVAL_VIEW, ROLE_MANAGE, TENANT_CONFIGURE, TENANT_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `ADM-339` | Governance & Compliance Command Center | commandCentre | 2 | 0 | — |
| `ADM-340` | Segregation of Duties Policy Manager | configEditor | 1 | 0 | — |
| `ADM-341` | Four-Eyes & Dual-Control Policy | configEditor | 2 | 0 | — |
| `ADM-342` | Authentication & MFA Policy Manager | listDetail | 6 | 0 | — |
| `ADM-343` | Sensitive Action Confirmation | configEditor | 2 | 0 | — |
| `ADM-344` | Digital Signature Management | configEditor | 1 | 0 | — |
| `ADM-345` | Immutable Approval Record & Tamper Detection | listDetail | 1 | 0 | — |
| `ADM-346` | Approval Record Retention Policy | configEditor | 3 | 0 | — |
| `ADM-347` | Regulatory Audit & Evidence Center | listDetail | 1 | 0 | — |
| `ADM-348` | Governance Risk & AI Compliance Advisor | listDetail | 1 | 0 | — |

## Thin screens in this batch

**ADM-340, ADM-345, ADM-347, ADM-348 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

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
  "apis": [
   {
    "operationId": "listApprovalControlPolicies",
    "contract": "approvals",
    "purpose": "Controls in force",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "getApprovalAnalytics",
    "contract": "approvals",
    "purpose": "Governance posture",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
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
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-339",
   "workshopBoard": "wireframes/WS35 Approval Workflows and Governance Board 6.dc.html#adm-339"
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
      },
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "setSegregationRules",
       "label": "Save segregation rules",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "setSegregationRules"
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
  "apis": [
   {
    "operationId": "setSegregationRules",
    "contract": "identity",
    "purpose": "Which roles may not be held together",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-340",
   "workshopBoard": "wireframes/WS35 Approval Workflows and Governance Board 6.dc.html#adm-340"
  },
  "apisNote": "Regenerated 9 September 2026 from Approval_Workflows_and_Governance_Reference.pdf page 51. 0 of 0 labels bound to a contract property; 1 of 14 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "apis": [
   {
    "operationId": "setApprovalControlPolicy",
    "contract": "approvals",
    "purpose": "Four-eyes and dual control",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listApprovalControlPolicies"
    ]
   },
   {
    "operationId": "listApprovalControlPolicies",
    "contract": "approvals",
    "purpose": "What is already required",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-341",
   "workshopBoard": "wireframes/WS35 Approval Workflows and Governance Board 6.dc.html#adm-341"
  },
  "apisNote": "Regenerated 9 September 2026 from Approval_Workflows_and_Governance_Reference.pdf page 52. 0 of 0 labels bound to a contract property; 7 of 11 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Define the authentication strength required before an approver can execute sensitive approval decisions. The source requires authentication before approval actions and supports MFA for sensitive approvals.",
  "gaps": [
   {
    "operation": "setPasswordPolicy",
    "why": "**`setPasswordPolicy` replaces the whole policy and nothing reads it.** identity has no `getPasswordPolicy`, so this screen cannot show the tenant's current `mfaRequiredForPermissions` (or the rest of the policy it must send back unchanged). Handed to the contracts group (audit R135).",
    "source": "contract identity.yaml PUT /password-policy"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Approval_Workflows_and_Governance_Reference.pdf, page 53"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Approval_Workflows_and_Governance_Reference.pdf, page 53"
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
       "provenance": "contract operation setStepUpPolicy"
      }
     ]
    },
    {
     "name": "contentBody",
     "components": [
      {
       "kind": "dataTable",
       "derived": true,
       "impliedBy": "listStepUpPolicies",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "setStepUpPolicy"
      },
      {
       "kind": "multiSelect",
       "label": "Permissions that require MFA",
       "bindsTo": "PasswordPolicy",
       "columns": [
        "PasswordPolicy.mfaRequiredForPermissions"
       ],
       "operation": "setPasswordPolicy",
       "notes": "**MFA is required by permission (decided 28 September, audit R135).** A principal holding any permission listed here must present a second factor at sign-in and keep an active method. The floor — `ROLE_MANAGE`, `LEDGER_APPROVE` and every `PLATFORM_*` permission — is shown locked: the tenant may add permissions and never drop a floor entry (`setPasswordPolicy` refuses such a body with 400).",
       "provenance": "contract identity.yaml PUT /password-policy"
      },
      {
       "kind": "primaryButton",
       "label": "Save MFA requirement",
       "operation": "setPasswordPolicy",
       "notes": "**Staff factors only.** Guest two-step verification is not set here: it is a per-venue option in Venue Management (`VenueSettings.identity.guestTwoStep`, BO-065), off unless the venue enables it (decided 29 September, rev 3 GAP-B1, superseding the second part of audit R167).",
       "provenance": "contract identity.yaml PUT /password-policy"
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
    "operationId": "setPasswordPolicy",
    "contract": "identity",
    "purpose": "Which permissions require MFA (`mfaRequiredForPermissions`) — add above the floor, never drop (decided 28 September, audit R135)",
    "trigger": "onAction"
   },
   {
    "operationId": "listMfaMethods",
    "contract": "identity",
    "purpose": "Which methods approvers have enrolled, because a policy demanding a factor nobody holds locks the action",
    "trigger": "onLoad"
   },
   {
    "operationId": "getGuestVerificationPolicy",
    "contract": "identity",
    "purpose": "The tenant's guest identity-verification workflow",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "setGuestVerificationPolicy",
    "contract": "identity",
    "purpose": "Set which verifications guests must pass, and when",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-342",
   "workshopBoard": "wireframes/WS35 Approval Workflows and Governance Board 6.dc.html#adm-342"
  },
  "apisNote": "Regenerated 9 September 2026 from Approval_Workflows_and_Governance_Reference.pdf page 53. 0 of 0 labels bound to a contract property; 0 of 20 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "apis": [
   {
    "operationId": "setStepUpPolicy",
    "contract": "approvals",
    "purpose": "Which actions need re-authentication",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listStepUpPolicies"
    ]
   },
   {
    "operationId": "listStepUpPolicies",
    "contract": "approvals",
    "purpose": "Policies in force",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-343",
   "workshopBoard": "wireframes/WS35 Approval Workflows and Governance Board 6.dc.html#adm-343"
  },
  "apisNote": "Regenerated 9 September 2026 from Approval_Workflows_and_Governance_Reference.pdf page 53. 0 of 0 labels bound to a contract property; 6 of 17 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "apis": [
   {
    "operationId": "signApprovalDecision",
    "contract": "approvals",
    "purpose": "Signature methods in use",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "getApprovalRecord"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-344",
   "workshopBoard": "wireframes/WS35 Approval Workflows and Governance Board 6.dc.html#adm-344"
  },
  "apisNote": "Regenerated 9 September 2026 from Approval_Workflows_and_Governance_Reference.pdf page 54. 0 of 0 labels bound to a contract property; 8 of 19 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "requestId",
     "from": "navigation"
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
  "apis": [
   {
    "operationId": "getApprovalRecord",
    "contract": "approvals",
    "purpose": "Chained records, verified on read",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "entryState": {
   "preloaded": [
    "Record Integrity: VERIFIED ✓",
    "🔴 Potential Tamper Event Detected",
    "Record affected",
    "User/service",
    "Date/time",
    "attempted action"
   ],
   "params": [
    {
     "name": "requestId",
     "from": "navigation"
    }
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-345",
   "workshopBoard": "wireframes/WS35 Approval Workflows and Governance Board 6.dc.html#adm-345"
  },
  "apisNote": "Regenerated 9 September 2026 from Approval_Workflows_and_Governance_Reference.pdf page 55. 0 of 9 labels bound to a contract property; 9 of 25 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "apis": [
   {
    "operationId": "setApprovalRetentionPolicy",
    "contract": "approvals",
    "purpose": "How long records are kept",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "getApprovalRecord"
    ]
   },
   {
    "operationId": "listDataRetentionSettings",
    "contract": "tenancy",
    "purpose": "Retention period per data class",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "setDataRetentionSetting",
    "contract": "tenancy",
    "purpose": "Set a class's period (approvalRecord, aiDecisionRecords)",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-346",
   "workshopBoard": "wireframes/WS35 Approval Workflows and Governance Board 6.dc.html#adm-346"
  },
  "apisNote": "Regenerated 9 September 2026 from Approval_Workflows_and_Governance_Reference.pdf page 56. 0 of 0 labels bound to a contract property; 8 of 16 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "dataClass",
     "from": "navigation"
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
  "apis": [
   {
    "operationId": "createApprovalEvidencePackage",
    "contract": "approvals",
    "purpose": "Assemble what an auditor asked for",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-347",
   "workshopBoard": "wireframes/WS35 Approval Workflows and Governance Board 6.dc.html#adm-347"
  },
  "apisNote": "Regenerated 9 September 2026 from Approval_Workflows_and_Governance_Reference.pdf page 57. 0 of 12 labels bound to a contract property; 12 of 17 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "apis": [
   {
    "operationId": "getApprovalAnalytics",
    "contract": "approvals",
    "purpose": "Risk and compliance posture",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-348",
   "workshopBoard": "wireframes/WS35 Approval Workflows and Governance Board 6.dc.html#adm-348"
  },
  "apisNote": "Regenerated 9 September 2026 from Approval_Workflows_and_Governance_Reference.pdf page 58. 0 of 0 labels bound to a contract property; 0 of 14 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
 "createApprovalEvidencePackage": {
  "method": "POST",
  "path": "/approval-evidence-packages",
  "contract": "approvals",
  "summary": "Assemble what an auditor asked for",
  "permission": "APPROVAL_VIEW",
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
  "requestBody": null,
  "responds": null
 },
 "getApprovalAnalytics": {
  "method": "GET",
  "path": "/approval-analytics",
  "contract": "approvals",
  "summary": "Volumes, times, rejections and bottlenecks",
  "permission": "APPROVAL_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "from",
    "in": "query",
    "required": null
   },
   {
    "name": "groupBy",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "ApprovalAnalytics"
 },
 "getApprovalRecord": {
  "method": "GET",
  "path": "/approval-requests/{requestId}/record",
  "contract": "approvals",
  "summary": "The immutable decision record, and whether it is intact",
  "permission": "APPROVAL_VIEW",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "ApprovalRecord"
 },
 "getGuestVerificationPolicy": {
  "method": "GET",
  "path": "/guest-verification-policy",
  "contract": "identity",
  "summary": "The tenant's guest identity-verification workflow",
  "permission": "TENANT_CONFIGURE",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "tenant",
  "parameters": [],
  "requestBody": null,
  "responds": "IdentityGuestVerificationPolicy"
 },
 "listApprovalControlPolicies": {
  "method": "GET",
  "path": "/approval-control-policies",
  "contract": "approvals",
  "summary": "Segregation of duties, four-eyes and dual control",
  "permission": "APPROVAL_VIEW",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "tenant",
  "parameters": [],
  "requestBody": null,
  "responds": "ApprovalControlPolicy"
 },
 "listDataRetentionSettings": {
  "method": "GET",
  "path": "/data-retention-settings",
  "contract": "tenancy",
  "summary": "How long the tenant keeps each class of data",
  "permission": "TENANT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": "dataClass",
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
 "setApprovalRetentionPolicy": {
  "method": "PUT",
  "path": "/approval-retention",
  "contract": "approvals",
  "summary": "How long decision records are kept, and what survives",
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
  "requestBody": "ApprovalRetentionPolicy",
  "responds": "ApprovalRetentionPolicy"
 },
 "setDataRetentionSetting": {
  "method": "PUT",
  "path": "/data-retention-settings/{dataClass}",
  "contract": "tenancy",
  "summary": "Set how long the tenant keeps one class of data",
  "permission": "TENANT_CONFIGURE",
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
  "requestBody": "TenantDataRetentionSetting",
  "responds": "TenantDataRetentionSetting"
 },
 "setGuestVerificationPolicy": {
  "method": "PUT",
  "path": "/guest-verification-policy",
  "contract": "identity",
  "summary": "Set which verifications a guest must pass, and when",
  "permission": "TENANT_CONFIGURE",
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
  "requestBody": "IdentityGuestVerificationPolicy",
  "responds": "IdentityGuestVerificationPolicy"
 },
 "setPasswordPolicy": {
  "method": "PUT",
  "path": "/password-policy",
  "contract": "identity",
  "summary": "Length, breach check, lockout and step-up",
  "permission": "TENANT_CONFIGURE",
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
  "requestBody": "PasswordPolicy",
  "responds": "PasswordPolicy"
 },
 "setSegregationRules": {
  "method": "PUT",
  "path": "/segregation-rules",
  "contract": "identity",
  "summary": "Which permissions may not be held together",
  "permission": "ROLE_MANAGE",
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
  "requestBody": null,
  "responds": "SegregationRule"
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
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "StepUpPolicy",
  "responds": "StepUpPolicy"
 },
 "signApprovalDecision": {
  "method": "POST",
  "path": "/approval-requests/{requestId}/signature",
  "contract": "approvals",
  "summary": "Sign a decision, so it can be proved later",
  "permission": "APPROVAL_DECIDE",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "ApprovalSignature"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "ApprovalAnalytics": {
  "type": "object",
  "x-ticvai-persistence": "none — aggregated from approvals.request",
  "properties": {
   "from": {
    "type": "string",
    "format": "date"
   },
   "to": {
    "type": "string",
    "format": "date"
   },
   "groupBy": {
    "type": "string",
    "description": "The grouping asked for, as the `groupBy` query parameter; each row's `key` is one value of it.",
    "enum": [
     "kind",
     "approver",
     "venue",
     "day",
     "week"
    ]
   },
   "rows": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "key": {
       "type": "string"
      },
      "raised": {
       "type": "integer"
      },
      "approved": {
       "type": "integer"
      },
      "rejected": {
       "type": "integer"
      },
      "withdrawn": {
       "type": "integer"
      },
      "expired": {
       "type": "integer",
       "description": "**Requests nobody answered.** Usually a routing defect rather than a busy approver, and the number that says the matrix names the wrong person.\n"
      },
      "escalated": {
       "type": "integer"
      },
      "slaBreached": {
       "type": "integer"
      },
      "medianMinutes": {
       "type": "number"
      },
      "p95Minutes": {
       "type": "number"
      }
     }
    }
   }
  }
 },
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
 "ApprovalRecord": {
  "type": "object",
  "x-ticvai-persistence": "approvals.decision_record",
  "description": "Approvals boards 4.10 and 6.6. **Tamper evidence, not tamper prevention** — each record chains to the one before it, so a changed entry breaks every hash after it.\n",
  "properties": {
   "requestId": {
    "type": "string",
    "format": "uuid"
   },
   "sequence": {
    "type": "integer"
   },
   "recordedAt": {
    "type": "string",
    "format": "date-time"
   },
   "decision": {
    "type": "string"
   },
   "decidedBy": {
    "type": "string",
    "format": "uuid"
   },
   "comment": {
    "type": "string",
    "nullable": true
   },
   "policyVersions": {
    "type": "array",
    "description": "**What the rules were at the time**, because they have changed since.",
    "items": {
     "type": "object",
     "properties": {
      "policyId": {
       "type": "string",
       "format": "uuid"
      },
      "version": {
       "type": "integer"
      }
     }
    }
   },
   "payloadHash": {
    "type": "string"
   },
   "previousRecordHash": {
    "type": "string",
    "nullable": true
   },
   "recordHash": {
    "type": "string"
   },
   "signatures": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/ApprovalSignature"
    }
   },
   "integrity": {
    "type": "string",
    "readOnly": true,
    "enum": [
     "intact",
     "broken",
     "unverifiable"
    ],
    "description": "**Verified on read.** A tamper check nobody runs reports the breach years late."
   },
   "scopePath": {
    "type": "string"
   }
  }
 },
 "ApprovalRetentionPolicy": {
  "type": "object",
  "x-ticvai-persistence": "approvals.retention_policy",
  "description": "Approvals board 6.7. **Approval records outlive what they approved.**",
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "appliesToRequestKinds": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/ApprovalKind"
    }
   },
   "retainYears": {
    "type": "integer",
    "nullable": true,
    "description": "**Null takes the tenant's `approvalRecord` retention setting** (tenancy `setDataRetentionSetting`; decided 29 September, all data retention is tenant configuration). A value here applies to the request kinds this policy names and may only lengthen what the tenant setting keeps.\n"
   },
   "retainSignatures": {
    "type": "boolean",
    "default": true
   },
   "retainAttachments": {
    "type": "boolean",
    "default": false
   },
   "onExpiry": {
    "type": "string",
    "enum": [
     "delete",
     "anonymise",
     "archive"
    ],
    "default": "archive"
   },
   "overridesPrivacyDeletion": {
    "type": "boolean",
    "default": true,
    "description": "**Can extend, never shorten, what privacy retention would delete.** The interaction is decided once here instead of argued per data-subject request.\n"
   },
   "legalBasis": {
    "type": "string",
    "nullable": true
   },
   "scopePath": {
    "type": "string"
   }
  }
 },
 "ApprovalSignature": {
  "type": "object",
  "x-ticvai-persistence": "approvals.signature",
  "description": "Approvals board 6.5. **What is signed is the request as it stood at the moment of decision**, so a later edit breaks its own signature.\n",
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "requestId": {
    "type": "string",
    "format": "uuid"
   },
   "signedBy": {
    "type": "string",
    "format": "uuid"
   },
   "signedAt": {
    "type": "string",
    "format": "date-time"
   },
   "method": {
    "type": "string",
    "enum": [
     "platformKey",
     "uaePass",
     "externalCertificate",
     "drawnSignature"
    ]
   },
   "payloadHash": {
    "type": "string"
   },
   "signature": {
    "type": "string"
   },
   "certificateSubject": {
    "type": "string",
    "nullable": true
   },
   "stepUpVerified": {
    "type": "boolean",
    "default": false
   },
   "scopePath": {
    "type": "string"
   }
  }
 },
 "IdentityGuestVerificationPolicy": {
  "type": "object",
  "x-ticvai-persistence": "identity.guest_verification_policy",
  "description": "**The tenant's configurable identity workflow for guests** (5.3.21; decided 29 September, build pass). Which verifications registration needs, which moments need a verified ID document, what is accepted and who reviews it. Proposed defaults are ours (our build plan).",
  "required": [
   "registrationRequires"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "The tenant, written by the server (`x-ticvai-config-scope: tenant`)."
   },
   "registrationRequires": {
    "type": "array",
    "description": "Verifications a new account must pass before it is usable. Proposed default `[mobileOtp]`.",
    "items": {
     "type": "string",
     "enum": [
      "email",
      "mobileOtp"
     ]
    }
   },
   "idDocumentRequiredFor": {
    "type": "array",
    "description": "The moments that need a verified ID document. Empty (the default) asks for none.",
    "items": {
     "type": "string",
     "enum": [
      "accountCreation",
      "ageRestrictedPurchase",
      "residentPricing",
      "accountRecovery",
      "walletTopUpAboveLimit"
     ]
    }
   },
   "walletTopUpLimit": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "acceptedDocumentKinds": {
    "type": "array",
    "description": "Proposed default passport, emiratesId, nationalId.",
    "items": {
     "type": "string",
     "enum": [
      "passport",
      "emiratesId",
      "nationalId",
      "drivingLicence",
      "residencePermit",
      "other"
     ]
    }
   },
   "uaePassSatisfiesIdDocument": {
    "type": "boolean",
    "default": true,
    "description": "A guest signed in with UAE Pass (`guestUaePassLogin`) counts as ID-verified, since the national identity has already checked the person."
   },
   "socialLoginCountsAsEmailVerified": {
    "type": "boolean",
    "default": true
   },
   "selfieRequired": {
    "type": "boolean",
    "default": false
   },
   "reviewMode": {
    "type": "string",
    "enum": [
     "manual",
     "provider",
     "providerThenManual"
    ],
    "default": "manual",
    "description": "Who checks a document. `provider` and `providerThenManual` need the client's verification provider (make-or-break on `setGuestVerificationPolicy`)."
   },
   "documentImageRetention": {
    "type": "string",
    "enum": [
     "deleteOnDecision",
     "keepUntilDocumentExpiry"
    ],
    "default": "deleteOnDecision",
    "description": "How long the scan is kept. The outcome and the hashed number are kept either way."
   },
   "maxResubmissions": {
    "type": "integer",
    "minimum": 0,
    "maximum": 10,
    "default": 3
   },
   "updatedAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   }
  }
 },
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
 "PasswordPolicy": {
  "type": "object",
  "x-ticvai-persistence": "identity.password_policy",
  "description": "BL-144. **Written by `setPasswordPolicy`, which returns it**, at tenant scope. Before BL-144 the package had no password policy, no lockout and no forced change at first logon anywhere.\n**Modelled on NIST SP 800-63B rather than on habit.** Length beats composition, and forced rotation on a schedule makes passwords worse — people increment a digit. Rotation is here because some tenants are contractually required to have it, **not because it helps.**\n",
  "required": [
   "id",
   "scopePath",
   "minLength"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "description": "Assigned by the server. Required in the response only; ignored if a request sends it."
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "**The partition key** (ADR-0005), written by the server from the caller's tenant (`x-ticvai-config-scope: tenant`). Required in the response only; ignored if a request sends it."
   },
   "minLength": {
    "type": "integer",
    "default": 12,
    "minimum": 8,
    "description": "A tenant may raise the length and never set it below 8 (decided 28 September, audit R126 (7))."
   },
   "requireBreachCheck": {
    "type": "boolean",
    "default": true,
    "description": "**The single most effective rule.** Refusing a password known to be breached stops more account takeovers than every composition rule combined.\n"
   },
   "maxAgeDays": {
    "type": "integer",
    "nullable": true,
    "description": "**Null is the recommended value.** Forced rotation produces `Summer2026!` becoming `Summer2027!`, and it is offered because some tenants are contractually obliged to have it rather than because it works.\n"
   },
   "recoveryMethods": {
    "type": "array",
    "description": "BL-132. **A guest locked out had no path back** — lockout existed and recovery did not, which turns a forgotten password into a support call.\n**Ordered by strength, and the venue chooses which it offers.** Email is weakest and universal; a verified phone is stronger; an in-person check at a desk is strongest and only available to a guest who is already at the venue.\n",
    "items": {
     "type": "string",
     "enum": [
      "email",
      "sms",
      "securityQuestions",
      "inPersonVerification",
      "supportAssisted"
     ]
    }
   },
   "maxConcurrentSessions": {
    "type": "integer",
    "nullable": true,
    "description": "BL-145. **Null, and that is the decision.** A staff principal has one live session, full stop: ADR-0004 keeps a server-side session registry (the `sid` claim, `ActiveSession`), and §3.1.3 refuses a second sign-in rather than counting towards a limit (confirmed 28 September, audit R184). A number here would only ever mean 1.\nThe requirement asked for it configurable. **Configurable to null is still an answer.**\n"
   },
   "deviceRestriction": {
    "type": "object",
    "nullable": true,
    "description": "BL-146. **Device, browser, IP and location restriction on access.** Applies to staff principals, not guests — a guest restricted to one device is a guest who cannot use their new phone.\n**Warn before block by default.** An IP restriction that blocks silently is a venue manager locked out on the day their ISP rotates an address.\n",
    "properties": {
     "allowedIpRanges": {
      "type": "array",
      "items": {
       "type": "string"
      }
     },
     "allowedCountries": {
      "type": "array",
      "items": {
       "type": "string"
      }
     },
     "requireRegisteredDevice": {
      "type": "boolean",
      "default": false
     },
     "onViolation": {
      "type": "string",
      "enum": [
       "warn",
       "requireStepUp",
       "block"
      ],
      "default": "requireStepUp"
     }
    }
   },
   "lockoutAfterAttempts": {
    "type": "integer",
    "default": 10
   },
   "lockoutMinutes": {
    "type": "integer",
    "default": 15,
    "description": "**A temporary lockout, not a permanent one.** Permanent lockout on failed attempts is a denial-of-service anybody can run against a known username.\n"
   },
   "forceChangeOnFirstLogon": {
    "type": "boolean",
    "default": true
   },
   "reusePreventionCount": {
    "type": "integer",
    "default": 5,
    "minimum": 0,
    "maximum": 24,
    "description": "**How many previous credentials a staff member may not reuse** — the last 5 unless the tenant sets another (decided 28 September, audit R132). `changeOwnCredential` refuses a match with `422`.\n"
   },
   "mfaRequiredForPermissions": {
    "type": "array",
    "description": "**Step-up rather than blanket MFA.** Requiring it for a refund approval and not for reading a rota is what stops people sharing devices to avoid it.\n**MFA is required by permission, not by role** (decided 28 September, audit R135). A principal holding any permission listed here must keep an active method (`removeMfaMethod` refuses to remove the last one). **The default is the platform floor**: `ROLE_MANAGE`, `LEDGER_APPROVE` and every `PLATFORM_*` permission. A tenant may add to the list and never remove a floor entry; a body that drops one is refused `400`.\n",
    "items": {
     "$ref": "../shared/permissions.yaml#/components/schemas/Permission"
    },
    "default": [
     "ROLE_MANAGE",
     "LEDGER_APPROVE",
     "PLATFORM_TENANT_VIEW",
     "PLATFORM_TENANT_MANAGE",
     "PLATFORM_TENANT_TERMINATE",
     "PLATFORM_TENANT_ACCESS",
     "PLATFORM_PLAN_MANAGE",
     "PLATFORM_CELL_VIEW",
     "PLATFORM_CELL_MANAGE",
     "PLATFORM_BILLING_VIEW",
     "PLATFORM_BILLING_MANAGE",
     "PLATFORM_RELEASE_VIEW",
     "PLATFORM_RELEASE_MANAGE",
     "PLATFORM_RELEASE_PROMOTE",
     "PLATFORM_MIGRATION_VIEW",
     "PLATFORM_MIGRATION_APPLY"
    ]
   }
  }
 },
 "SegregationRule": {
  "type": "object",
  "x-ticvai-persistence": "identity.segregation_rule",
  "description": "BL-147, 3.3.31 and 11.1.24. **The package enforced segregation of duties in exactly one place** — the product lifecycle guard requiring the approver not be the author — and there was no general rule.\n**A conflict is between two permissions held by one principal**, and the check runs at grant time rather than at use time: **discovering the conflict when somebody exercises it means the conflict already existed.**\n",
  "required": [
   "id",
   "permissionA",
   "permissionB",
   "severity"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "description": "Assigned by the server. Required in the response only; ignored if a request sends it."
   },
   "name": {
    "type": "string"
   },
   "permissionA": {
    "type": "string"
   },
   "permissionB": {
    "type": "string"
   },
   "severity": {
    "type": "string",
    "enum": [
     "block",
     "requireApproval",
     "warn"
    ]
   },
   "rationale": {
    "type": "string",
    "description": "**Why these two conflict, in words an auditor reads.** A rule with no rationale is a rule somebody removes when it becomes inconvenient.\n"
   },
   "scopeSensitive": {
    "type": "boolean",
    "default": true,
    "description": "**Whether the two permissions must overlap in scope to conflict**, and this is not `scopePath` below — that one is the partition key and says where the rule *row* lives (ADR-0005), not where the *conflict* applies.\n**True, and it should rarely be false.** `ACCREDITATION_ISSUE` at Yas Island beside `ACCREDITATION_MANAGE` at Warner Bros is two jobs at two sites; flagging it is a control crying wolf, and the first thing a venue does with one of those is switch it off. The comparison walks `scopePath` prefixes the same way `resolvePermissions` already does — `uae.dubai` contains `uae.dubai.marina`, so one is an overlap and two siblings are not.\n**False is for conflicts that are genuinely estate-wide**, such as holding both sides of a financial reconciliation anywhere at all.\n"
   },
   "allowWithCompensatingControl": {
    "type": "boolean",
    "default": false,
    "description": "**A small venue cannot always separate duties**, and pretending otherwise means the rule gets disabled entirely. A named compensating control is better than no rule.\n"
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `tenant` scope**; the server sets it and ignores it in a request."
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
 },
 "TenantDataRetentionClass": {
  "type": "string",
  "description": "**The data classes a tenant sets a retention period for** (decided 29 September, Chinmay: all data retention is tenant configuration, one setting per class). Defaults are ADR-0047's and the AI system design's (section 8, decision 5); a legal limit is the only thing the platform enforces.\n| Class | Default | Counted from | Legal limit (refused) | |---|---|---|---| | `guestProfile` | 5 years | last activity | none | | `paymentRecord` | 10 years | created | at least 10 years (4.3.4) | | `financialRecord` | 7 years | created | at least 7 years (6.1.78) | | `auditRecord` | 2 years (authorisation and device audit) | created | none | | `approvalRecord` | 7 years (approvals board 6.7) | decided | none | | `complianceInspection` | 7 years | created | none | | `faceTagBiometric` | 7 days | ticket expiry | make-or-break | | `facePassBiometric` | follows `guestProfile` | last activity | make-or-break | | `aiPrompts` | 90 days (prompts and responses) | created | none | | `aiConversations` | 90 days | last activity | none | | `aiDecisionRecords` | follows `auditRecord` (decision records and the approvals of AI actions) | decided | none | | `aiMetadataIndex` | always follows `aiDecisionRecords` (summaries, entities, embeddings) | created | none |\n**ADR-0047's floors and ceilings that are not law are defaults now, not refusals** (the audit floor of one year, the proposed seven-year guest-profile ceiling, the Face Tag thirty-day ceiling). Platform-owned copies — the burst environment copy, a decommissioned cell — are not tenant data classes and are not here.\n",
  "enum": [
   "guestProfile",
   "paymentRecord",
   "financialRecord",
   "auditRecord",
   "approvalRecord",
   "complianceInspection",
   "faceTagBiometric",
   "facePassBiometric",
   "aiPrompts",
   "aiConversations",
   "aiDecisionRecords",
   "aiMetadataIndex"
  ]
 },
 "TenantDataRetentionSetting": {
  "type": "object",
  "x-ticvai-persistence": "tenancy.data_retention_setting",
  "description": "**One tenant's retention period for one data class** (decided 29 September, Chinmay). One row per tenant and class, written by `setDataRetentionSetting`; a class with no row takes the platform default. The limit and default fields are the platform's catalogue, computed for the response and not stored on the row.\n",
  "required": [
   "dataClass"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "dataClass": {
    "allOf": [
     {
      "$ref": "#/components/schemas/TenantDataRetentionClass"
     }
    ],
    "x-ticvai-unique": "tenant",
    "description": "One row per class per tenant. On a write it comes from the path; a body value is ignored."
   },
   "retainAmount": {
    "type": "integer",
    "nullable": true,
    "minimum": 0,
    "description": "The tenant's period. Null with no `followsDataClass` means the platform default applies. Zero means the data is not kept past the transaction that produced it.\n"
   },
   "retainUnit": {
    "type": "string",
    "nullable": true,
    "enum": [
     "days",
     "months",
     "years"
    ],
    "description": "Required with `retainAmount`."
   },
   "followsDataClass": {
    "allOf": [
     {
      "$ref": "#/components/schemas/TenantDataRetentionClass"
     }
    ],
    "nullable": true,
    "description": "Keep this class for as long as another class is kept. Set by default for `aiDecisionRecords` (follows `auditRecord`), `facePassBiometric` (follows `guestProfile`) and `aiMetadataIndex` (follows `aiDecisionRecords`, and cannot be changed).\n"
   },
   "onExpiry": {
    "type": "string",
    "enum": [
     "archive",
     "anonymise",
     "delete"
    ],
    "default": "archive",
    "description": "ADR-0047's stages. `archive` moves the data to the archive instance, from where it is erased on the class's own schedule; derived stores (the AI index, search) purge at archive, not later.\n"
   },
   "anchor": {
    "type": "string",
    "readOnly": true,
    "x-ticvai-persisted": false,
    "enum": [
     "createdAt",
     "lastActivity",
     "decidedAt",
     "ticketExpiry"
    ],
    "description": "What the period is counted from. Fixed per class by the platform."
   },
   "effectiveAmount": {
    "type": "integer",
    "readOnly": true,
    "x-ticvai-persisted": false,
    "description": "The period actually applied, after follows and defaults are resolved."
   },
   "effectiveUnit": {
    "type": "string",
    "readOnly": true,
    "x-ticvai-persisted": false,
    "enum": [
     "days",
     "months",
     "years"
    ]
   },
   "isDefault": {
    "type": "boolean",
    "readOnly": true,
    "x-ticvai-persisted": false,
    "description": "True when the tenant has not set this class and the platform default applies."
   },
   "defaultAmount": {
    "type": "integer",
    "nullable": true,
    "readOnly": true,
    "x-ticvai-persisted": false
   },
   "defaultUnit": {
    "type": "string",
    "nullable": true,
    "readOnly": true,
    "x-ticvai-persisted": false,
    "enum": [
     "days",
     "months",
     "years"
    ]
   },
   "legalMinimumAmount": {
    "type": "integer",
    "nullable": true,
    "readOnly": true,
    "x-ticvai-persisted": false,
    "description": "A floor the law sets. A shorter period is refused (`422`)."
   },
   "legalMaximumAmount": {
    "type": "integer",
    "nullable": true,
    "readOnly": true,
    "x-ticvai-persisted": false,
    "description": "A maximum the law sets. A longer period is refused (`422`). Null for every class until the biometric make-or-break is answered."
   },
   "legalLimitUnit": {
    "type": "string",
    "nullable": true,
    "readOnly": true,
    "x-ticvai-persisted": false,
    "enum": [
     "days",
     "months",
     "years"
    ]
   },
   "legalBasis": {
    "type": "string",
    "nullable": true,
    "readOnly": true,
    "x-ticvai-persisted": false,
    "description": "The law or requirement the limit comes from, e.g. `4.3.4`."
   },
   "updatedAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   },
   "updatedByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "The tenant. Retention is set at tenant scope only."
   }
  }
 }
}
```
