# P11-reviewer-internal-01 — P11 · Reviewer (Internal)

**3 screens · 6 operations · 4 schemas · 2 permissions**

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
  `ACCREDITATION_APPROVE, ACCREDITATION_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `ACC-006` | Reviewer Queue | approvalInbox | 1 | 0 | — |
| `ACC-007` | Reviewer Application Detail | approvalInbox | 4 | 2 | — |
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
    "operationId": "listAccreditationApplications",
    "contract": "accreditation",
    "purpose": "Applications awaiting review, oldest first",
    "trigger": "onLoad",
    "provenance": "readiness close-out, 29 September 2026"
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
      "documentId"
     ],
     "provenance": "derived — ACC-007 declares entryState.params applicationId, documentId and ACC-006 holds documentId, so an edge into it carries them"
    },
    {
     "to": "ACC-008",
     "trigger": "Credential Register",
     "provenance": "derived — ACC-008 declares entryState.params  and ACC-006 holds none of them. The edge carries nothing: ACC-008 needs nothing to open"
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
    "operationId": "decideAccreditationApplication",
    "contract": "accreditation",
    "purpose": "Approve, reject or return for information",
    "trigger": "onAction",
    "provenance": "readiness close-out, 29 September 2026"
   },
   {
    "operationId": "getAccreditationApplication",
    "contract": "accreditation",
    "purpose": "The application under review",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "listAccreditationDocuments",
    "contract": "accreditation",
    "purpose": "The application's documents (applicationId), each with its state",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "verifyAccreditationDocument",
    "contract": "accreditation",
    "purpose": "Verify or refuse each document",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
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
     "name": "applicationId",
     "from": "ACC-006"
    },
    {
     "name": "documentId",
     "from": "navigation"
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
     "to": "ACC-006",
     "trigger": "Reviewer Queue",
     "provenance": "derived — ACC-006 declares entryState.params  and ACC-007 holds none of them. The edge carries nothing: ACC-007 is opened from ACC-006, so this edge is the way back and ACC-006 keeps its own state"
    },
    {
     "to": "ACC-008",
     "trigger": "Credential Register",
     "provenance": "derived — ACC-008 declares entryState.params  and ACC-007 holds none of them. The edge carries nothing: ACC-008 needs nothing to open"
    },
    {
     "to": "ACC-005",
     "trigger": "The badge is issued",
     "provenance": "flow F23 step 2→3",
     "carries": [
      "holderId"
     ]
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
    "operationId": "listAccreditationCredentials",
    "contract": "accreditation",
    "purpose": "Every credential issued, with its validity",
    "trigger": "onLoad",
    "provenance": "readiness close-out, 29 September 2026"
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
     "provenance": "derived — ACC-006 declares entryState.params  and ACC-008 holds none of them. The edge carries nothing: ACC-008 is opened from ACC-006, so this edge is the way back and ACC-006 keeps its own state"
    },
    {
     "to": "ACC-007",
     "trigger": "Reviewer Application Detail",
     "provenance": "derived — ACC-007 declares entryState.params applicationId, documentId and ACC-008 holds none of them. The edge carries nothing: ACC-008 is opened from ACC-007, so this edge is the way back and ACC-007 keeps its own state"
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
 "decideAccreditationApplication": {
  "method": "POST",
  "path": "/accreditation-applications/{applicationId}/decide",
  "contract": "accreditation",
  "summary": "Approve, reject, return for more, or escalate",
  "permission": "ACCREDITATION_APPROVE",
  "offlineCapable": null,
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
  "responds": "AccreditationApplication"
 },
 "getAccreditationApplication": {
  "method": "GET",
  "path": "/accreditation-applications/{applicationId}",
  "contract": "accreditation",
  "summary": "One application, with where each requirement stands",
  "permission": "ACCREDITATION_VIEW",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "AccreditationApplication"
 },
 "listAccreditationApplications": {
  "method": "GET",
  "path": "/accreditation-applications",
  "contract": "accreditation",
  "summary": "Applications, by state and programme",
  "permission": "ACCREDITATION_VIEW",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "programmeId",
    "in": "query",
    "required": null
   },
   {
    "name": "status",
    "in": "query",
    "required": null
   },
   {
    "name": "applicantType",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "AccreditationApplication"
 },
 "listAccreditationCredentials": {
  "method": "GET",
  "path": "/accreditation-credentials",
  "contract": "accreditation",
  "summary": "Badges and digital credentials issued",
  "permission": "ACCREDITATION_VIEW",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "holderId",
    "in": "query",
    "required": null
   },
   {
    "name": "status",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "AccreditationCredential"
 },
 "listAccreditationDocuments": {
  "method": "GET",
  "path": "/accreditation-documents",
  "contract": "accreditation",
  "summary": "Documents supplied, by holder, application, requirement or state",
  "permission": "ACCREDITATION_VIEW",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "applicationId",
    "in": "query",
    "required": null
   },
   {
    "name": "holderId",
    "in": "query",
    "required": null
   },
   {
    "name": "requirementCode",
    "in": "query",
    "required": null
   },
   {
    "name": "status",
    "in": "query",
    "required": null
   },
   {
    "name": "expiringWithinDays",
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
 },
 "verifyAccreditationDocument": {
  "method": "POST",
  "path": "/accreditation-documents/{documentId}/verify",
  "contract": "accreditation",
  "summary": "Accept or refuse a submitted document",
  "permission": "ACCREDITATION_APPROVE",
  "offlineCapable": null,
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
  "responds": "AccreditationDocument"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "AccreditationApplication": {
  "type": "object",
  "x-ticvai-persistence": "accreditation.application",
  "description": "Board 1.3. **Usually submitted by an organisation on behalf of its people.**",
  "required": [
   "programmeId"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "reference": {
    "type": "string"
   },
   "programmeId": {
    "type": "string",
    "format": "uuid"
   },
   "categoryCode": {
    "type": "string",
    "nullable": true
   },
   "applicantType": {
    "type": "string"
   },
   "submittedByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "organisationId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "subject": {
    "type": "object",
    "additionalProperties": true,
    "description": "Name, date of birth, nationality, contact — shaped by the requirements matrix."
   },
   "requirementStatus": {
    "type": "array",
    "readOnly": true,
    "items": {
     "type": "object",
     "properties": {
      "requirementCode": {
       "type": "string"
      },
      "satisfied": {
       "type": "boolean"
      },
      "documentId": {
       "type": "string",
       "format": "uuid",
       "nullable": true
      }
     }
    }
   },
   "status": {
    "type": "string",
    "enum": [
     "draft",
     "submitted",
     "underReview",
     "informationRequested",
     "approved",
     "rejected",
     "withdrawn",
     "expired"
    ]
   },
   "decisionReason": {
    "type": "string",
    "nullable": true
   },
   "missingRequirements": {
    "type": "array",
    "readOnly": true,
    "description": "The requirement codes a reviewer returned the application for, or rejected it over — what the applicant must change before resubmitting",
    "items": {
     "type": "string"
    }
   },
   "decisionDueAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true,
    "description": "When a decision is due — the approvals request's SLA. **A date, not a queue position**"
   },
   "approvalRequestId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "holderId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "renewsHolderId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true,
    "description": "12.1.37. Set by `renewAccreditation`; approval extends this holder rather than creating one"
   },
   "resubmissionOfApplicationId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true,
    "description": "12.1.33. The rejected application this one resubmits, so the rejection stays in the record"
   },
   "resubmissionNote": {
    "type": "string",
    "maxLength": 1000,
    "nullable": true,
    "readOnly": true,
    "description": "What the applicant changed, from `resubmitAccreditationApplication`"
   },
   "submittedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "decidedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "scopePath": {
    "type": "string"
   }
  }
 },
 "AccreditationCredential": {
  "type": "object",
  "x-ticvai-persistence": "accreditation.credential",
  "description": "Board 4. **Not the accreditation** — reissuing one re-vets nobody.",
  "required": [
   "holderId",
   "kind"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "holderId": {
    "type": "string",
    "format": "uuid"
   },
   "kind": {
    "type": "string",
    "enum": [
     "printedBadge",
     "mobileCredential",
     "qr",
     "nfcCard",
     "rfidCard",
     "wristband"
    ]
   },
   "symbology": {
    "type": "string",
    "nullable": true,
    "description": "12.1.22. **How `encodedIdentifier` is carried**, so a reader and a badge renderer agree: `qr` for a QR credential and the default for a `mobileCredential`, a barcode where a printed badge carries one, `nfcNdef` or `rfidEpc` for an encoded card, `none` where nothing is encoded.\n",
    "enum": [
     "qr",
     "dataMatrix",
     "pdf417",
     "aztec",
     "code128",
     "nfcNdef",
     "rfidEpc",
     "none"
    ]
   },
   "serialNumber": {
    "type": "string",
    "nullable": true
   },
   "encodedIdentifier": {
    "type": "string",
    "nullable": true
   },
   "badgeTemplateId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "issuedAt": {
    "type": "string",
    "format": "date-time"
   },
   "issuedBy": {
    "type": "string",
    "format": "uuid"
   },
   "activatedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "status": {
    "type": "string",
    "enum": [
     "pendingPrint",
     "issued",
     "active",
     "lost",
     "replaced",
     "revoked",
     "expired"
    ]
   },
   "replacesCredentialId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "replacementCount": {
    "type": "integer",
    "default": 0
   },
   "scopePath": {
    "type": "string"
   }
  }
 },
 "AccreditationDocument": {
  "type": "object",
  "x-ticvai-persistence": "accreditation.document",
  "description": "Board 2.5. **Submitted against a named requirement, not into a folder.**",
  "required": [
   "requirementCode",
   "assetId"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "holderId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "applicationId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "requirementCode": {
    "type": "string"
   },
   "assetId": {
    "type": "string",
    "format": "uuid"
   },
   "submittedAt": {
    "type": "string",
    "format": "date-time"
   },
   "status": {
    "type": "string",
    "enum": [
     "submitted",
     "verified",
     "rejected",
     "expired"
    ]
   },
   "verifiedBy": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "verifiedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "rejectionReason": {
    "type": "string",
    "nullable": true
   },
   "expiresAt": {
    "type": "string",
    "format": "date",
    "nullable": true,
    "description": "**An insurance certificate valid until March accredits somebody until March**, whatever the programme says.\n"
   },
   "scopePath": {
    "type": "string"
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
 }
}
```
