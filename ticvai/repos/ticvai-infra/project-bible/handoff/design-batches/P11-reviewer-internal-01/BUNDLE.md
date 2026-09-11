# P11-reviewer-internal-01 — P11 · Reviewer (Internal)

**3 screens · 3 operations · 7 schemas · 2 permissions**

Platform P11 Accreditation Web · ships as **ticvai-control** ·
public audience · web ·
online only

## Who this is for

**public on web.** Everything below is how you know what is
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
  `APPROVAL_DECIDE, APPROVAL_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **0 of these operations work offline**
  
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `ACC-006` | Reviewer Queue | approvalInbox | 1 | 0 | — |
| `ACC-007` | Reviewer Application Detail | approvalInbox | 2 | 2 | — |
| `ACC-008` | Credential Register | listDetail | 1 | 1 | — |

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "ACC-006",
  "name": "Reviewer Queue",
  "module": "Reviewer (Internal)",
  "wave": 3,
  "requiresModule": "accreditation",
  "pattern": "approvalInbox",
  "density": "compact",
  "purpose": "Work the queue of applications waiting on a decision, oldest-due first, and approve the straightforward ones without opening them.\n",
  "apis": [
   {
    "operationId": "listApprovalRequests",
    "contract": "approvals",
    "purpose": "Accreditation applications awaiting a decision",
    "trigger": "onLoad"
   }
  ],
  "gaps": [
   {
    "operation": "getWaitTimes",
    "removed": true,
    "why": "**Removed 9 September.** The screen declared `getWaitTimes`, which is the guest app's ride-queue read. A reviewer queue and a virtual queue share a word and nothing else — the fourth instance of a name collision in this package after `release`, `generatedPack` and `provenance`.\n",
    "source": "frame claude-design/Accreditation Board.dc.html#acc-006"
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
       "label": "Applicant or outlet",
       "notes": "Searches holder name and organisation. **Not \"find a record\".**"
      },
      {
       "kind": "selectField",
       "label": "Performance",
       "notes": "All performances, or one. A reviewer usually works one night at a time.",
       "provenance": "frame claude-design/Accreditation Board.dc.html#acc-006"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "queue",
     "components": [
      {
       "kind": "dataTable",
       "label": "Queue",
       "bindsTo": "ApprovalRequest[]",
       "columns": [
        "ApprovalRequest.summary",
        "ApprovalRequest.requestedAt",
        "ApprovalRequest.slaDueAt",
        "ApprovalRequest.status"
       ],
       "notes": "**Due first, and how long it has waited.** `slaDueAt` is the sort, not `requestedAt` — an application for tonight outranks one submitted earlier for next month. Rows carry the signals a reviewer decides on: *no press card, no commission*, *commission letter attached*, *accredited last season*.\n",
       "provenance": "frame claude-design/Accreditation Board.dc.html#acc-006"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "item",
     "components": [
      {
       "kind": "detailPanel",
       "label": "Selected application",
       "bindsTo": "ApprovalRequest",
       "notes": "Enough to approve without opening `ACC-007`.",
       "provenance": "frame claude-design/Accreditation Board.dc.html#acc-006"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "decision",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Approve",
       "permission": "APPROVAL_DECIDE"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The queue.",
   "emptyFirstRun": "**An empty queue is success, not a broken screen.** Nothing is waiting — says so as reassurance, and says when the next applications are expected.\n",
   "emptyNoResults": "Nothing matches this filter. The queue itself is not empty.",
   "emptyNoAccess": "You do not review for this programme.",
   "error": "Could not load the queue. **No decision is lost** — nothing was in flight."
  },
  "entryState": {
   "params": [
    {
     "name": "programmeId",
     "from": "session"
    }
   ],
   "preloaded": [],
   "coldEntry": "Opens on the reviewer's own programmes, due-first."
  },
  "navigation": {
   "entryFrom": [
    "ACC-001"
   ],
   "exitTo": [
    "ACC-007",
    "ACC-008"
   ],
   "transitions": [
    {
     "to": "ACC-007",
     "trigger": "Reviewer Application Detail",
     "carries": [
      "requestId"
     ],
     "provenance": "derived — ACC-007 declares entryState.params requestId, so an edge into it must carry them"
    },
    {
     "to": "ACC-008",
     "trigger": "Credential Register",
     "carries": [
      "programmeId"
     ],
     "provenance": "derived — ACC-008 declares entryState.params programmeId, so an edge into it must carry them"
    }
   ]
  },
  "implementation": {
   "app": "accreditation-web",
   "route": "/reviewer-internal/reviewer-queue",
   "component": "apps/accreditation-web/src/routes/reviewer-internal/ReviewerQueueList.tsx",
   "status": "notStarted"
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P11 Accreditation Web.dc.html#acc-006"
  },
  "resolvedQuestions": [
   "Unblocked by the 7 September workshop (TICVAI_MoM_2026-09-07_Accreditation_Entitlements_VirtualQueue), which this question said did not exist. Decided there - identity documents are OCR'd to auto-populate the form, and the extracted data is stored as structured fields rather than only the image, because expiry tracking and renewal prompts cannot read a scan; uniqueness is enforced on passport and Emirates ID and a duplicate submission is blocked; the web portal is primary with the mobile app a secondary route for individual applicants. And one decision removes screens rather than adding them - accreditation- holder monitoring is to be a filtered view inside general entitlement monitoring, not a separate system. Capability and API mapping can now be done; 74 pages of ACCREDITATION.pdf are also in the design corpus and no operation has been drafted from them yet."
  ],
  "_platform": {
   "code": "P11",
   "audience": "public",
   "formFactor": "web",
   "shortName": "Accreditation Web",
   "name": "Accreditation Web — Applications",
   "offlineCapable": false,
   "app": "accreditation-web",
   "operator": "public",
   "targetApp": {
    "app": "ticvai-control",
    "name": "TICVAI Control",
    "shell": "web",
    "siblings": [
     "P09",
     "P10",
     "P14",
     "P17"
    ],
    "note": "**TICVAI operates all five**, whoever signs in. The partner portal, the accreditation intake, the developer portal and the sign-up are outward faces of the control plane, not separate products — but their users are not TICVAI staff, and the permission model has to hold that line. **P17 added 11 September 2026**: a prospect buying TICVAI has no tenant and no cell, so the control plane is the only thing that can serve them.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "ACC-007",
  "name": "Reviewer Application Detail",
  "module": "Reviewer (Internal)",
  "wave": 3,
  "requiresModule": "accreditation",
  "pattern": "approvalInbox",
  "density": "compact",
  "purpose": "Everything the decision needs about one application, in one place, so the reviewer does not open another screen to decide.\n",
  "apis": [
   {
    "operationId": "listApprovalRequests",
    "contract": "approvals",
    "purpose": "The application under review",
    "trigger": "onLoad"
   },
   {
    "operationId": "decideApprovalRequest",
    "contract": "approvals",
    "purpose": "Approve or refuse, with a reason",
    "trigger": "onAction",
    "invalidates": [
     "listApprovalRequests",
     "listAccreditationBadges"
    ]
   }
  ],
  "gaps": [
   {
    "operation": "getApprovalRequest",
    "why": "The screen shows one application and the only read is a list. **A detail screen that fetches a collection to find one row is a detail screen that gets slower as the queue grows.**\n",
    "source": "contract approvals.yaml"
   }
  ],
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "item",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The application",
       "bindsTo": "ApprovalRequest",
       "notes": "Role, outlet, press card, commission — **including the ones that are absent**, stated as *Not stated* and *None attached* rather than left blank. A blank field and a declared absence look identical and only one is information.\n",
       "provenance": "frame claude-design/Accreditation Board.dc.html#acc-007"
      },
      {
       "kind": "detailPanel",
       "label": "History with this venue",
       "notes": "**Accredited before, and conditions breached.** This is the field the decision usually turns on and the one a reviewer would otherwise go looking for.\n",
       "provenance": "frame claude-design/Accreditation Board.dc.html#acc-007"
      },
      {
       "kind": "banner",
       "label": "Decision due",
       "bindsTo": "ApprovalRequest.slaDueAt",
       "provenance": "frame claude-design/Accreditation Board.dc.html#acc-007"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "decision",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Approve",
       "permission": "APPROVAL_DECIDE"
      },
      {
       "kind": "destructiveButton",
       "label": "Refuse",
       "permission": "APPROVAL_DECIDE"
      }
     ]
    }
   ]
  },
  "overlays": [
   {
    "id": "refuse",
    "component": "confirmDialog",
    "trigger": "Refuse",
    "body": "**Captures the reason, and says the applicant will read it.** `ApprovalDecision.reason` is part of the record; a refusal with no reason produces an appeal by telephone.\n",
    "bindsTo": "ApprovalDecision.reason",
    "provenance": "authored, from pattern approvalInbox"
   },
   {
    "id": "approveWithConditions",
    "component": "drawer",
    "trigger": "Approve",
    "body": "Coverage granted may be narrower than coverage requested — *stalls, not pit*. **The badge renders what is granted**, so the two screens must agree.\n",
    "provenance": "frame claude-design/Accreditation Board.dc.html#acc-005"
   }
  ],
  "states": {
   "loading": "The application.",
   "error": "**A failed decision is not a made decision.** Says the decision was not recorded and leaves the buttons live.\n",
   "emptyNoAccess": "You do not review for this programme.",
   "emptyNoResults": "This application was decided by somebody else while it was open. Shows the decision.",
   "emptyFirstRun": "Nothing selected. The queue is where a reviewer starts."
  },
  "entryState": {
   "params": [
    {
     "name": "requestId",
     "from": "ACC-006"
    }
   ],
   "preloaded": [
    "summary",
    "requestedAt",
    "slaDueAt"
   ],
   "coldEntry": "Reached from the queue, or from a link in a reviewer's email. Opened cold it loads the application, or says it has already been decided and by whom.\n"
  },
  "navigation": {
   "entryFrom": [
    "ACC-002",
    "ACC-006"
   ],
   "exitTo": [
    "ACC-005",
    "ACC-006",
    "ACC-008"
   ],
   "transitions": [
    {
     "to": "ACC-005",
     "trigger": "The badge is issued",
     "provenance": "flow F23 step 2→3"
    },
    {
     "to": "ACC-006",
     "trigger": "Reviewer Queue",
     "carries": [
      "programmeId"
     ],
     "provenance": "derived — ACC-006 declares entryState.params programmeId, so an edge into it must carry them"
    },
    {
     "to": "ACC-008",
     "trigger": "Credential Register",
     "carries": [
      "programmeId"
     ],
     "provenance": "derived — ACC-008 declares entryState.params programmeId, so an edge into it must carry them"
    }
   ]
  },
  "implementation": {
   "app": "accreditation-web",
   "route": "/reviewer-internal/reviewer-application-detail",
   "component": "apps/accreditation-web/src/routes/reviewer-internal/ReviewerApplicationDetail.tsx",
   "status": "notStarted"
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P11 Accreditation Web.dc.html#acc-007"
  },
  "resolvedQuestions": [
   "Unblocked by the 7 September workshop (TICVAI_MoM_2026-09-07_Accreditation_Entitlements_VirtualQueue), which this question said did not exist. Decided there - identity documents are OCR'd to auto-populate the form, and the extracted data is stored as structured fields rather than only the image, because expiry tracking and renewal prompts cannot read a scan; uniqueness is enforced on passport and Emirates ID and a duplicate submission is blocked; the web portal is primary with the mobile app a secondary route for individual applicants. And one decision removes screens rather than adding them - accreditation- holder monitoring is to be a filtered view inside general entitlement monitoring, not a separate system. Capability and API mapping can now be done; 74 pages of ACCREDITATION.pdf are also in the design corpus and no operation has been drafted from them yet."
  ],
  "_platform": {
   "code": "P11",
   "audience": "public",
   "formFactor": "web",
   "shortName": "Accreditation Web",
   "name": "Accreditation Web — Applications",
   "offlineCapable": false,
   "app": "accreditation-web",
   "operator": "public",
   "targetApp": {
    "app": "ticvai-control",
    "name": "TICVAI Control",
    "shell": "web",
    "siblings": [
     "P09",
     "P10",
     "P14",
     "P17"
    ],
    "note": "**TICVAI operates all five**, whoever signs in. The partner portal, the accreditation intake, the developer portal and the sign-up are outward faces of the control plane, not separate products — but their users are not TICVAI staff, and the permission model has to hold that line. **P17 added 11 September 2026**: a prospect buying TICVAI has no tenant and no cell, so the control plane is the only thing that can serve them.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "ACC-008",
  "name": "Credential Register",
  "module": "Reviewer (Internal)",
  "wave": 3,
  "requiresModule": "accreditation",
  "pattern": "listDetail",
  "density": "compact",
  "purpose": "Every credential issued this season, who holds it, where it is valid, and whether it has been used — and revoke one when it has to be revoked.\n",
  "purposeNote": "**Rewritten 9 September.** The purpose read *\"Get a guest into the app, fast, on a device that may be shared\"*, which is a login screen's purpose on a credential register. Found independently by Claude Design on the drawn frame and by this pass.\n",
  "apis": [
   {
    "operationId": "listAccreditationBadges",
    "contract": "approvals",
    "purpose": "Credentials issued for this programme",
    "trigger": "onLoad"
   }
  ],
  "gaps": [
   {
    "operation": "revokeAccreditationBadge",
    "why": "The register offers **Revoke** and nothing performs it. `AccreditationBadge.state` and `revokedReason` exist to record the outcome, so the schema is ready and the operation is not.\n",
    "source": "contract approvals.yaml AccreditationBadge.revokedReason"
   },
   {
    "field": "AccreditationBadge.lastUsedAt",
    "why": "The register shows a **last used** column and the schema has no such field. *Not yet* is the value that matters — a credential issued and never presented is the one to ask about.\n",
    "source": "frame claude-design/Accreditation Board.dc.html#acc-008"
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
       "label": "Holder or reference"
      },
      {
       "kind": "selectField",
       "label": "Season",
       "notes": "Defaults to the current season. **A register scoped to all time is a register nobody reads.**",
       "provenance": "frame claude-design/Accreditation Board.dc.html#acc-008"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Credential register",
       "bindsTo": "AccreditationBadge[]",
       "columns": [
        "AccreditationBadge.holderName",
        "AccreditationBadge.zones",
        "AccreditationBadge.issuedAt",
        "AccreditationBadge.state"
       ],
       "notes": "Holder, valid for, issued, last used. **Revoked rows stay visible and read as revoked** — removing them from the register is how a revoked badge gets re-issued by mistake.\n",
       "provenance": "frame claude-design/Accreditation Board.dc.html#acc-008"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "Credential",
       "bindsTo": "AccreditationBadge",
       "provenance": "frame claude-design/Accreditation Board.dc.html#acc-008"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "destructiveButton",
       "label": "Revoke",
       "permission": "APPROVAL_DECIDE"
      },
      {
       "kind": "secondaryButton",
       "label": "Export",
       "notes": "The register is what a venue hands to a security team before a performance.",
       "provenance": "frame claude-design/Accreditation Board.dc.html#acc-008"
      }
     ]
    }
   ]
  },
  "overlays": [
   {
    "id": "confirmRevoke",
    "component": "confirmDialog",
    "trigger": "Revoke",
    "body": "**Names the holder and what stops working, and captures the reason.** A revocation takes somebody's access to a building they may already be standing outside.\n",
    "bindsTo": "AccreditationBadge.revokedReason",
    "provenance": "authored, from pattern listDetail"
   }
  ],
  "states": {
   "loading": "The register.",
   "emptyFirstRun": "No credentials issued yet this season. Points at the queue.",
   "emptyNoResults": "Nothing matches. The register is not empty.",
   "emptyNoAccess": "You do not administer credentials for this programme.",
   "error": "Could not load. **No credential is affected** by a failed read."
  },
  "entryState": {
   "params": [
    {
     "name": "programmeId",
     "from": "session"
    }
   ],
   "preloaded": [],
   "coldEntry": "Opens on the current season."
  },
  "navigation": {
   "entryFrom": [
    "ACC-006",
    "ACC-007"
   ],
   "exitTo": [
    "ACC-006",
    "ACC-007"
   ],
   "transitions": [
    {
     "to": "ACC-006",
     "trigger": "Reviewer Queue",
     "carries": [
      "programmeId"
     ],
     "provenance": "derived — ACC-006 declares entryState.params programmeId, so an edge into it must carry them"
    },
    {
     "to": "ACC-007",
     "trigger": "Reviewer Application Detail",
     "carries": [
      "requestId"
     ],
     "provenance": "derived — ACC-007 declares entryState.params requestId, so an edge into it must carry them"
    }
   ]
  },
  "implementation": {
   "app": "accreditation-web",
   "route": "/reviewer-internal/credential-register",
   "component": "apps/accreditation-web/src/routes/reviewer-internal/CredentialRegisterList.tsx",
   "status": "notStarted"
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P11 Accreditation Web.dc.html#acc-008"
  },
  "resolvedQuestions": [
   "Unblocked by the 7 September workshop (TICVAI_MoM_2026-09-07_Accreditation_Entitlements_VirtualQueue), which this question said did not exist. Decided there - identity documents are OCR'd to auto-populate the form, and the extracted data is stored as structured fields rather than only the image, because expiry tracking and renewal prompts cannot read a scan; uniqueness is enforced on passport and Emirates ID and a duplicate submission is blocked; the web portal is primary with the mobile app a secondary route for individual applicants. And one decision removes screens rather than adding them - accreditation- holder monitoring is to be a filtered view inside general entitlement monitoring, not a separate system. Capability and API mapping can now be done; 74 pages of ACCREDITATION.pdf are also in the design corpus and no operation has been drafted from them yet."
  ],
  "_platform": {
   "code": "P11",
   "audience": "public",
   "formFactor": "web",
   "shortName": "Accreditation Web",
   "name": "Accreditation Web — Applications",
   "offlineCapable": false,
   "app": "accreditation-web",
   "operator": "public",
   "targetApp": {
    "app": "ticvai-control",
    "name": "TICVAI Control",
    "shell": "web",
    "siblings": [
     "P09",
     "P10",
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
 "decideApprovalRequest": {
  "method": "POST",
  "path": "/approval-requests/{requestId}/decide",
  "contract": "approvals",
  "summary": "Approve or reject",
  "permission": "APPROVAL_DECIDE",
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
  "responds": "ApprovalRequest"
 },
 "listAccreditationBadges": {
  "method": "GET",
  "path": "/accreditation-badges",
  "contract": "approvals",
  "summary": "Badges issued and their state",
  "permission": "APPROVAL_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "AccreditationBadge"
 },
 "listApprovalRequests": {
  "method": "GET",
  "path": "/approval-requests",
  "contract": "approvals",
  "summary": "Requests awaiting a decision, or already decided",
  "permission": "APPROVAL_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "assignedToMe",
    "in": "query",
    "required": null
   },
   {
    "name": "raisedByMe",
    "in": "query",
    "required": null
   },
   {
    "name": "status",
    "in": "query",
    "required": null
   },
   {
    "name": "kind",
    "in": "query",
    "required": null
   },
   {
    "name": "breachingWithinMinutes",
    "in": "query",
    "required": null
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
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "AccreditationBadge": {
  "type": "object",
  "x-ticvai-persistence": "approvals.accreditation_badge",
  "description": "**Drafted 4 September.** The credential an approved application produces. **Its lifetime is not the approval's** - a badge is revoked, lost or expires while the decision that authorised it still stands.",
  "required": [
   "id"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "approvalRequestId": {
    "type": "string",
    "format": "uuid"
   },
   "holderName": {
    "type": "string"
   },
   "zones": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Where this badge admits, which is the whole point of it."
   },
   "state": {
    "type": "string",
    "enum": [
     "issued",
     "collected",
     "suspended",
     "revoked",
     "expired"
    ]
   },
   "issuedAt": {
    "type": "string",
    "format": "date-time"
   },
   "expiresAt": {
    "type": "string",
    "format": "date-time"
   },
   "revokedReason": {
    "type": "string"
   }
  }
 },
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
  "description": "11.1.7 and 11.1.30–11.1.37. **The first four already exist as bespoke implementations** and this contract is what they collapse into.\n",
  "enum": [
   "refund",
   "priceOverride",
   "discountOverride",
   "complimentaryTicket",
   "membershipCancellation",
   "accessPermissionChange",
   "configurationChange",
   "aiRecommendation",
   "shiftVariance",
   "releasePromotion",
   "requisition",
   "stockWriteOff",
   "journalEntry",
   "periodReopen",
   "tenantMigration"
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
   }
  }
 },
 "ApprovalStatus": {
  "type": "string",
  "enum": [
   "draft",
   "pending",
   "escalated",
   "approved",
   "rejected",
   "withdrawn",
   "expired",
   "cancelled"
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
 }
}
```
