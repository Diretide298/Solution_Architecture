# WS76 — Digital Asset Management DAM board 3

**10 screens · 10 operations · 14 schemas · 6 permissions**

Platform P13 Venue CMS · ships as **venue-management** ·
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
  `ASSET_LIBRARY_APPROVE, ASSET_LIBRARY_MANAGE, ASSET_LIBRARY_SHARE, ASSET_LIBRARY_VIEW, PERMISSION_MANAGE, PERMISSION_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `CMS-081` | DAM Governance & Rights Command Center | listDetail | 2 | 0 | — |
| `CMS-082` | Asset Ownership & Responsibility Management | listDetail | 2 | 0 | — |
| `CMS-083` | Rights, License & Usage Policy Management | listDetail | 1 | 0 | — |
| `CMS-084` | Asset Approval Workflow Management | approvalInbox | 1 | 1 | — |
| `CMS-085` | Publication Eligibility & Governance Validation | listDetail | 1 | 0 | — |
| `CMS-086` | Role-Based Asset Access & Permission Management | listDetail | 2 | 0 | — |
| `CMS-087` | Secure Internal & External Sharing | listDetail | 1 | 1 | — |
| `CMS-088` | Rights Expiry, Renewal & Usage Impact | listDetail | 2 | 0 | — |
| `CMS-089` | Governance Audit Trail & Compliance Evidence | configEditor | 1 | 0 | — |
| `CMS-090` | Governance Risk, Compliance & AI Recommendations | listDetail | 1 | 0 | — |

## Thin screens in this batch

**CMS-082, CMS-083, CMS-085, CMS-086, CMS-089, CMS-090 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "CMS-081",
  "name": "DAM Governance & Rights Command Center",
  "module": "Media Library",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Digital Asset Management DAM.pdf",
   "board": "3",
   "number": "1",
   "page": 43
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/media-library/dam-governance-rights-command-center-cms-081",
   "component": "apps/venue-management-web/src/routes/media-library/DamGovernanceRightsCommandCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "CMS-001"
   ],
   "exitTo": [
    "CMS-001",
    "CMS-082",
    "CMS-083",
    "CMS-084",
    "CMS-085",
    "CMS-086",
    "CMS-087",
    "CMS-088",
    "CMS-089",
    "CMS-090"
   ],
   "transitions": [
    {
     "to": "CMS-001",
     "trigger": "Back to Tenant Workspace",
     "provenance": "structural — pack board 3 wiring, 11 September 2026",
     "back": true
    },
    {
     "to": "CMS-082",
     "trigger": "Asset Ownership & Responsibility Management",
     "provenance": "structural — pack board 3 wiring, 11 September 2026"
    },
    {
     "to": "CMS-083",
     "trigger": "Rights, License & Usage Policy Management",
     "provenance": "structural — pack board 3 wiring, 11 September 2026",
     "carries": [
      "assetId"
     ]
    },
    {
     "to": "CMS-084",
     "trigger": "Asset Approval Workflow Management",
     "provenance": "structural — pack board 3 wiring, 11 September 2026",
     "carries": [
      "assetId"
     ]
    },
    {
     "to": "CMS-085",
     "trigger": "Publication Eligibility & Governance Validation",
     "provenance": "structural — pack board 3 wiring, 11 September 2026",
     "carries": [
      "assetId"
     ]
    },
    {
     "to": "CMS-086",
     "trigger": "Role-Based Asset Access & Permission Management",
     "provenance": "structural — pack board 3 wiring, 11 September 2026"
    },
    {
     "to": "CMS-087",
     "trigger": "Secure Internal & External Sharing",
     "provenance": "structural — pack board 3 wiring, 11 September 2026"
    },
    {
     "to": "CMS-088",
     "trigger": "Rights Expiry, Renewal & Usage Impact",
     "provenance": "structural — pack board 3 wiring, 11 September 2026",
     "carries": [
      "assetId"
     ]
    },
    {
     "to": "CMS-089",
     "trigger": "Governance Audit Trail & Compliance Evidence",
     "provenance": "structural — pack board 3 wiring, 11 September 2026",
     "carries": [
      "assetId"
     ]
    },
    {
     "to": "CMS-090",
     "trigger": "Governance Risk, Compliance & AI Recommendations",
     "provenance": "structural — pack board 3 wiring, 11 September 2026"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display; Show) and no metric row",
  "purpose": "Provide DAM administrators, brand managers, legal/compliance teams, and content managers with one overview of asset governance.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 5 actions on this screen and the screen declares 0 operations.** Unserved: Approval Queue, Rights Review, Expiring Assets, External Shares, Governance Issues. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Digital Asset Management DAM.pdf, page 43 §Quick Actions"
   },
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Digital Asset Management DAM.pdf, page 43 §Display"
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
       "label": "Every dam governance rights",
       "columns": [
        "Active Assets",
        "Pending Approval",
        "Approved",
        "Pending",
        "Restricted",
        "Expired",
        "Blocked",
        "Critical Alerts"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Digital Asset Management DAM.pdf, page 43 §Display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected dam governance rights",
       "bindsTo": null,
       "columns": [
        "Active Assets",
        "Pending Approval",
        "Approved",
        "Pending",
        "Restricted",
        "Expired",
        "Blocked",
        "Critical Alerts"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Digital Asset Management”.",
       "provenance": "pack Digital Asset Management DAM.pdf, page 43 §Display"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Approval Queue",
       "provenance": "pack Digital Asset Management DAM.pdf, page 43 §Quick Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Rights Review",
       "provenance": "pack Digital Asset Management DAM.pdf, page 43 §Quick Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Expiring Assets",
       "provenance": "pack Digital Asset Management DAM.pdf, page 43 §Quick Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "External Shares",
       "provenance": "pack Digital Asset Management DAM.pdf, page 43 §Quick Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Governance Issues",
       "provenance": "pack Digital Asset Management DAM.pdf, page 43 §Quick Actions"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The dam governance rights list.",
   "error": "Could not load. Names which read failed and leaves the dam governance rights untouched.",
   "emptyFirstRun": "No dam governance rights yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the dam governance rights are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getExpiringRights",
    "contract": "assets",
    "purpose": "Rights about to lapse",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "getMediaUsageAnalytics",
    "contract": "assets",
    "purpose": "Governance coverage",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "entryState": {
   "preloaded": [
    "Active Assets",
    "Pending Approval",
    "Approved",
    "Pending",
    "Restricted",
    "Expired"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P13 Venue CMS.dc.html#cms-081",
   "workshopBoard": "wireframes/WS46 Digital Asset Management DAM Board 3.dc.html#cms-081"
  },
  "apisNote": "Regenerated 9 September 2026 from Digital Asset Management DAM.pdf page 43. 0 of 8 labels bound to a contract property; 13 of 27 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "_platform": {
   "code": "P13",
   "audience": "staff",
   "formFactor": "web",
   "shortName": "Venue CMS",
   "name": "Venue CMS — White Label",
   "app": "venue-management-web",
   "offlineCapable": false,
   "operator": "venue",
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P08",
     "P12",
     "P16"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "CMS-082",
  "name": "Asset Ownership & Responsibility Management",
  "module": "Media Library",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Digital Asset Management DAM.pdf",
   "board": "3",
   "number": "2",
   "page": 45
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/media-library/asset-ownership-responsibility-management-cms-082",
   "component": "apps/venue-management-web/src/routes/media-library/AssetOwnershipResponsibilityManagement.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "CMS-081"
   ],
   "exitTo": [
    "CMS-081"
   ],
   "transitions": [
    {
     "to": "CMS-081",
     "trigger": "Back to DAM Governance & Rights Command Center",
     "provenance": "structural — pack board 3 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Define who owns and is responsible for each digital asset from a business and operational perspective. This should be separate from the person who simply uploaded the file.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 1 actions on this screen and the screen declares 0 operations.** Unserved: Partner. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Digital Asset Management DAM.pdf, page 45 §Support"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Digital Asset Management DAM.pdf, page 45"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Digital Asset Management DAM.pdf, page 45"
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
       "label": "Partner",
       "provenance": "pack Digital Asset Management DAM.pdf, page 45 §Support"
      }
     ]
    },
    {
     "name": "contentBody",
     "components": [
      {
       "kind": "detailPanel",
       "derived": true,
       "impliedBy": "getMediaAsset",
       "notes": "One record, read-only."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "updateMediaAsset"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The asset ownership responsibility list.",
   "error": "Could not load. Names which read failed and leaves the asset ownership responsibility untouched.",
   "emptyFirstRun": "No asset ownership responsibility yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the asset ownership responsibility are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "updateMediaAsset",
    "contract": "assets",
    "purpose": "Set owner and responsibility",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "getMediaAsset",
    "contract": "assets",
    "purpose": "The asset being assigned",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P13 Venue CMS.dc.html#cms-082",
   "workshopBoard": "wireframes/WS46 Digital Asset Management DAM Board 3.dc.html#cms-082"
  },
  "apisNote": "Regenerated 9 September 2026 from Digital Asset Management DAM.pdf page 45. 0 of 0 labels bound to a contract property; 1 of 25 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "mediaId",
     "from": "navigation"
    }
   ]
  },
  "_platform": {
   "code": "P13",
   "audience": "staff",
   "formFactor": "web",
   "shortName": "Venue CMS",
   "name": "Venue CMS — White Label",
   "app": "venue-management-web",
   "offlineCapable": false,
   "operator": "venue",
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P08",
     "P12",
     "P16"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "CMS-083",
  "name": "Rights, License & Usage Policy Management",
  "module": "Media Library",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Digital Asset Management DAM.pdf",
   "board": "3",
   "number": "3",
   "page": 46
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/media-library/rights-license-usage-policy-management-cms-083",
   "component": "apps/venue-management-web/src/routes/media-library/RightsLicenseUsagePolicyManagement.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "CMS-081"
   ],
   "exitTo": [
    "CMS-081"
   ],
   "transitions": [
    {
     "to": "CMS-081",
     "trigger": "Back to DAM Governance & Rights Command Center",
     "provenance": "structural — pack board 3 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Define exactly how an asset is legally and commercially allowed to be used.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 2 actions on this screen and the screen declares 0 operations.** Unserved: Commercial use permitted, Non-commercial only. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Digital Asset Management DAM.pdf, page 46 §Support"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Digital Asset Management DAM.pdf, page 46"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Digital Asset Management DAM.pdf, page 46"
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
       "label": "Commercial use permitted",
       "provenance": "pack Digital Asset Management DAM.pdf, page 46 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Non-commercial only",
       "provenance": "pack Digital Asset Management DAM.pdf, page 46 §Support"
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
   "loading": "The rights license usage list.",
   "error": "Could not load. Names which read failed and leaves the rights license usage untouched.",
   "emptyFirstRun": "No rights license usage yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the rights license usage are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setMediaAssetRights",
    "contract": "assets",
    "purpose": "Licence, territory, channel and expiry",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "getMediaAsset",
     "getExpiringRights"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P13 Venue CMS.dc.html#cms-083",
   "workshopBoard": "wireframes/WS46 Digital Asset Management DAM Board 3.dc.html#cms-083"
  },
  "apisNote": "Regenerated 9 September 2026 from Digital Asset Management DAM.pdf page 46. 0 of 0 labels bound to a contract property; 2 of 31 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "assetId",
     "from": "navigation"
    }
   ]
  },
  "_platform": {
   "code": "P13",
   "audience": "staff",
   "formFactor": "web",
   "shortName": "Venue CMS",
   "name": "Venue CMS — White Label",
   "app": "venue-management-web",
   "offlineCapable": false,
   "operator": "venue",
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P08",
     "P12",
     "P16"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "CMS-084",
  "name": "Asset Approval Workflow Management",
  "module": "Media Library",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Digital Asset Management DAM.pdf",
   "board": "3",
   "number": "4",
   "page": 47
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/media-library/asset-approval-workflow-management-cms-084",
   "component": "apps/venue-management-web/src/routes/media-library/AssetApprovalWorkflowManagement.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "CMS-081"
   ],
   "exitTo": [
    "CMS-081"
   ],
   "transitions": [
    {
     "to": "CMS-081",
     "trigger": "Back to DAM Governance & Rights Command Center",
     "provenance": "structural — pack board 3 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "approvalInbox",
  "patternReason": "the pack lists Approve and Reject among this screen's own actions — every row is waiting for a decision, so the empty state is success rather than a prompt to create something",
  "purpose": "Provide configurable governance before an asset becomes approved for operational or public use.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 6 actions on this screen and the screen declares 0 operations.** Unserved: Approve, Reject, Request Changes, Delegate, Add Comment, Rejection. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Digital Asset Management DAM.pdf, page 47 §Actions"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Digital Asset Management DAM.pdf, page 47"
   }
  ],
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "actionBar",
     "slot": "decision",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Approve",
       "provenance": "pack Digital Asset Management DAM.pdf, page 47 §Actions"
      },
      {
       "kind": "destructiveButton",
       "label": "Reject",
       "provenance": "pack Digital Asset Management DAM.pdf, page 47 §Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Request Changes",
       "provenance": "pack Digital Asset Management DAM.pdf, page 47 §Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Delegate",
       "provenance": "pack Digital Asset Management DAM.pdf, page 47 §Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Add Comment",
       "provenance": "pack Digital Asset Management DAM.pdf, page 47 §Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Rejection",
       "provenance": "pack Digital Asset Management DAM.pdf, page 47 §Actions"
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
    "id": "confirmReject",
    "component": "confirmDialog",
    "trigger": "Reject",
    "body": "**Reject on a asset approval workflow is not reversible from this screen.** Names what it affects and what it leaves alone. The pack requires the decision to reach the audit trail, so the dialog states that it is recorded.",
    "provenance": "pack Digital Asset Management DAM.pdf, page 47 §Actions"
   }
  ],
  "states": {
   "loading": "The asset approval workflow list.",
   "error": "Could not load. Names which read failed and leaves the asset approval workflow untouched.",
   "emptyFirstRun": "**Nothing is waiting, which is the good outcome.** An empty queue means every request has been decided — this state offers no create action, because creating work is not what an empty inbox needs.",
   "emptyNoResults": "The filter narrowed it and the asset approval workflow are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setMediaAssetApproval",
    "contract": "assets",
    "purpose": "Submit, approve or reject",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "getMediaAsset",
     "searchMedia"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P13 Venue CMS.dc.html#cms-084",
   "workshopBoard": "wireframes/WS46 Digital Asset Management DAM Board 3.dc.html#cms-084"
  },
  "apisNote": "Regenerated 9 September 2026 from Digital Asset Management DAM.pdf page 47. 0 of 0 labels bound to a contract property; 6 of 21 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "assetId",
     "from": "navigation"
    }
   ]
  },
  "_platform": {
   "code": "P13",
   "audience": "staff",
   "formFactor": "web",
   "shortName": "Venue CMS",
   "name": "Venue CMS — White Label",
   "app": "venue-management-web",
   "offlineCapable": false,
   "operator": "venue",
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P08",
     "P12",
     "P16"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "CMS-085",
  "name": "Publication Eligibility & Governance Validation",
  "module": "Media Library",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Digital Asset Management DAM.pdf",
   "board": "3",
   "number": "5",
   "page": 48
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/media-library/publication-eligibility-governance-validation-cms-085",
   "component": "apps/venue-management-web/src/routes/media-library/PublicationEligibilityGovernanceValidation.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "CMS-081"
   ],
   "exitTo": [
    "CMS-081"
   ],
   "transitions": [
    {
     "to": "CMS-081",
     "trigger": "Back to DAM Governance & Rights Command Center",
     "provenance": "structural — pack board 3 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Determine whether an asset is actually eligible to be used or distributed. This screen is particularly important. An asset being technically available in DAM does not mean it should be publishable.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Digital Asset Management DAM.pdf, page 48"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Digital Asset Management DAM.pdf, page 48"
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
       "kind": "banner",
       "label": "Permissions this screen separates",
       "notes": "**The pack separates these permissions and no action on the screen claims them yet:** 🟢 B2C Allowed. Each needs attaching to the control it gates, or the screen needs the control.",
       "provenance": "pack Digital Asset Management DAM.pdf, page 48 §Channel Permission"
      }
     ]
    },
    {
     "name": "contentBody",
     "components": [
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "setMediaAssetApproval",
       "label": "Save media asset approval",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "setMediaAssetApproval"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The publication eligibility governance list.",
   "error": "Could not load. Names which read failed and leaves the publication eligibility governance untouched.",
   "emptyFirstRun": "No publication eligibility governance yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the publication eligibility governance are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setMediaAssetApproval",
    "contract": "assets",
    "purpose": "Publication eligibility, computed",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "getMediaAsset",
     "searchMedia"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P13 Venue CMS.dc.html#cms-085",
   "workshopBoard": "wireframes/WS46 Digital Asset Management DAM Board 3.dc.html#cms-085"
  },
  "apisNote": "Regenerated 9 September 2026 from Digital Asset Management DAM.pdf page 48. 0 of 0 labels bound to a contract property; 1 of 16 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "assetId",
     "from": "navigation"
    }
   ]
  },
  "_platform": {
   "code": "P13",
   "audience": "staff",
   "formFactor": "web",
   "shortName": "Venue CMS",
   "name": "Venue CMS — White Label",
   "app": "venue-management-web",
   "offlineCapable": false,
   "operator": "venue",
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P08",
     "P12",
     "P16"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "CMS-086",
  "name": "Role-Based Asset Access & Permission Management",
  "module": "Media Library",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Digital Asset Management DAM.pdf",
   "board": "3",
   "number": "6",
   "page": 49
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/media-library/role-based-asset-access-permission-management-cms-086",
   "component": "apps/venue-management-web/src/routes/media-library/RoleBasedAssetAccessPermissionManagement.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "CMS-081"
   ],
   "exitTo": [
    "CMS-081"
   ],
   "transitions": [
    {
     "to": "CMS-081",
     "trigger": "Back to DAM Governance & Rights Command Center",
     "provenance": "structural — pack board 3 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Control who can discover, view, edit, download, share, approve, or manage assets.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Digital Asset Management DAM.pdf, page 49"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Digital Asset Management DAM.pdf, page 49"
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
       "impliedBy": "listAccessPolicies",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      },
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "createAccessPolicy",
       "label": "Create access policy",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "createAccessPolicy"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The role-based asset access list.",
   "error": "Could not load. Names which read failed and leaves the role-based asset access untouched.",
   "emptyFirstRun": "No role-based asset access yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the role-based asset access are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listAccessPolicies",
    "contract": "identity",
    "purpose": "Who may see which assets",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "createAccessPolicy",
    "contract": "identity",
    "purpose": "Write an asset access policy",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P13 Venue CMS.dc.html#cms-086",
   "workshopBoard": "wireframes/WS46 Digital Asset Management DAM Board 3.dc.html#cms-086"
  },
  "apisNote": "Regenerated 9 September 2026 from Digital Asset Management DAM.pdf page 49. 0 of 0 labels bound to a contract property; 0 of 20 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "_platform": {
   "code": "P13",
   "audience": "staff",
   "formFactor": "web",
   "shortName": "Venue CMS",
   "name": "Venue CMS — White Label",
   "app": "venue-management-web",
   "offlineCapable": false,
   "operator": "venue",
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P08",
     "P12",
     "P16"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "CMS-087",
  "name": "Secure Internal & External Sharing",
  "module": "Media Library",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Digital Asset Management DAM.pdf",
   "board": "3",
   "number": "7",
   "page": 51
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/media-library/secure-internal-external-sharing-cms-087",
   "component": "apps/venue-management-web/src/routes/media-library/SecureInternalExternalSharing.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "CMS-081"
   ],
   "exitTo": [
    "CMS-081"
   ],
   "transitions": [
    {
     "to": "CMS-081",
     "trigger": "Back to DAM Governance & Rights Command Center",
     "provenance": "structural — pack board 3 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Allow controlled sharing without users manually downloading assets and sending uncontrolled copies.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 5 actions on this screen and the screen declares 0 operations.** Unserved: Copy Secure Link, Extend, Change Permission, Revoke, View Activity. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Digital Asset Management DAM.pdf, page 51 §Actions"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Digital Asset Management DAM.pdf, page 51"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Digital Asset Management DAM.pdf, page 51"
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
       "label": "Copy Secure Link",
       "provenance": "pack Digital Asset Management DAM.pdf, page 51 §Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Extend",
       "provenance": "pack Digital Asset Management DAM.pdf, page 51 §Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Change Permission",
       "provenance": "pack Digital Asset Management DAM.pdf, page 51 §Actions"
      },
      {
       "kind": "destructiveButton",
       "label": "Revoke",
       "provenance": "pack Digital Asset Management DAM.pdf, page 51 §Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "View Activity",
       "provenance": "pack Digital Asset Management DAM.pdf, page 51 §Actions"
      },
      {
       "kind": "banner",
       "label": "Permissions this screen separates",
       "notes": "**The pack separates these permissions and no action on the screen claims them yet:** View + Download Approved Renditions. Each needs attaching to the control it gates, or the screen needs the control.",
       "provenance": "pack Digital Asset Management DAM.pdf, page 51 §Permission"
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
    "id": "confirmRevoke",
    "component": "confirmDialog",
    "trigger": "Revoke",
    "body": "**Revoke on a secure internal external is not reversible from this screen.** Names what it affects and what it leaves alone. The pack requires the decision to reach the audit trail, so the dialog states that it is recorded.",
    "provenance": "pack Digital Asset Management DAM.pdf, page 51 §Actions"
   }
  ],
  "states": {
   "loading": "The secure internal external list.",
   "error": "Could not load. Names which read failed and leaves the secure internal external untouched.",
   "emptyFirstRun": "No secure internal external yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the secure internal external are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "createMediaShare",
    "contract": "assets",
    "purpose": "Share externally, on terms",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listMediaAssetAudit"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P13 Venue CMS.dc.html#cms-087",
   "workshopBoard": "wireframes/WS46 Digital Asset Management DAM Board 3.dc.html#cms-087"
  },
  "apisNote": "Regenerated 9 September 2026 from Digital Asset Management DAM.pdf page 51. 0 of 0 labels bound to a contract property; 6 of 13 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "_platform": {
   "code": "P13",
   "audience": "staff",
   "formFactor": "web",
   "shortName": "Venue CMS",
   "name": "Venue CMS — White Label",
   "app": "venue-management-web",
   "offlineCapable": false,
   "operator": "venue",
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P08",
     "P12",
     "P16"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "CMS-088",
  "name": "Rights Expiry, Renewal & Usage Impact",
  "module": "Media Library",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Digital Asset Management DAM.pdf",
   "board": "3",
   "number": "8",
   "page": 52
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/media-library/rights-expiry-renewal-usage-impact-cms-088",
   "component": "apps/venue-management-web/src/routes/media-library/RightsExpiryRenewalUsageImpact.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "CMS-081"
   ],
   "exitTo": [
    "CMS-081"
   ],
   "transitions": [
    {
     "to": "CMS-081",
     "trigger": "Back to DAM Governance & Rights Command Center",
     "provenance": "structural — pack board 3 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Show) and no metric row",
  "purpose": "Prevent expired assets from continuing to be used across TICVAI channels.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 6 actions on this screen and the screen declares 0 operations.** Unserved: Renew Rights, Upload Renewal Document, Change Expiry, Find Replacement, Notify Owner, Expiry Workflow. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Digital Asset Management DAM.pdf, page 52 §Actions"
   },
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Digital Asset Management DAM.pdf, page 52 §Show"
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
       "label": "Every rights expiry renewal",
       "columns": [
        "Expires in 7 Days",
        "Expires in 30 Days",
        "Expires in 60 Days",
        "Expired",
        "Example",
        "DAM-IMG-008421"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Digital Asset Management DAM.pdf, page 52 §Show"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected rights expiry renewal",
       "bindsTo": null,
       "columns": [
        "Expires in 7 Days",
        "Expires in 30 Days",
        "Expires in 60 Days",
        "Expired",
        "Example",
        "DAM-IMG-008421"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Rights expire”, “Impact”, “Owner notification”, “Digital Asset Management”, “Escalation”, “Expired”.",
       "provenance": "pack Digital Asset Management DAM.pdf, page 52 §Show"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Renew Rights",
       "provenance": "pack Digital Asset Management DAM.pdf, page 52 §Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Upload Renewal Document",
       "provenance": "pack Digital Asset Management DAM.pdf, page 52 §Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Change Expiry",
       "provenance": "pack Digital Asset Management DAM.pdf, page 52 §Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Find Replacement",
       "provenance": "pack Digital Asset Management DAM.pdf, page 52 §Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Notify Owner",
       "provenance": "pack Digital Asset Management DAM.pdf, page 52 §Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Expiry Workflow",
       "provenance": "pack Digital Asset Management DAM.pdf, page 52 §Actions"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The rights expiry renewal list.",
   "error": "Could not load. Names which read failed and leaves the rights expiry renewal untouched.",
   "emptyFirstRun": "No rights expiry renewal yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the rights expiry renewal are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getExpiringRights",
    "contract": "assets",
    "purpose": "What lapses, and what it would break",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "setMediaAssetRights",
    "contract": "assets",
    "purpose": "Renew",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "getMediaAsset",
     "getExpiringRights"
    ]
   }
  ],
  "entryState": {
   "preloaded": [
    "Expires in 7 Days",
    "Expires in 30 Days",
    "Expires in 60 Days",
    "Expired",
    "Example",
    "DAM-IMG-008421"
   ],
   "params": [
    {
     "name": "assetId",
     "from": "navigation"
    }
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P13 Venue CMS.dc.html#cms-088",
   "workshopBoard": "wireframes/WS46 Digital Asset Management DAM Board 3.dc.html#cms-088"
  },
  "apisNote": "Regenerated 9 September 2026 from Digital Asset Management DAM.pdf page 52. 0 of 6 labels bound to a contract property; 12 of 25 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "_platform": {
   "code": "P13",
   "audience": "staff",
   "formFactor": "web",
   "shortName": "Venue CMS",
   "name": "Venue CMS — White Label",
   "app": "venue-management-web",
   "offlineCapable": false,
   "operator": "venue",
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P08",
     "P12",
     "P16"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "CMS-089",
  "name": "Governance Audit Trail & Compliance Evidence",
  "module": "Media Library",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Digital Asset Management DAM.pdf",
   "board": "3",
   "number": "9",
   "page": 53
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/media-library/governance-audit-trail-compliance-evidence-cms-089",
   "component": "apps/venue-management-web/src/routes/media-library/GovernanceAuditTrailComplianceEvidence.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "CMS-081"
   ],
   "exitTo": [
    "CMS-081"
   ],
   "transitions": [
    {
     "to": "CMS-081",
     "trigger": "Back to DAM Governance & Rights Command Center",
     "provenance": "structural — pack board 3 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Asset Uploaded) and no display directory — it is settings, not a population",
  "purpose": "Provide complete traceability for asset governance.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 1 actions on this screen and the screen declares 0 operations.** Unserved: Action. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Digital Asset Management DAM.pdf, page 53 §Support"
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
       "label": "↓",
       "provenance": "pack Digital Asset Management DAM.pdf, page 53 §Asset Uploaded"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Action",
       "provenance": "pack Digital Asset Management DAM.pdf, page 53 §Support"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The governance audit trail configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the governance audit trail untouched.",
   "emptyFirstRun": "No governance audit trail configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [
   {
    "operationId": "listMediaAssetAudit",
    "contract": "assets",
    "purpose": "Edits and distribution together",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P13 Venue CMS.dc.html#cms-089",
   "workshopBoard": "wireframes/WS46 Digital Asset Management DAM Board 3.dc.html#cms-089"
  },
  "apisNote": "Regenerated 9 September 2026 from Digital Asset Management DAM.pdf page 53. 0 of 0 labels bound to a contract property; 2 of 31 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "assetId",
     "from": "navigation"
    }
   ]
  },
  "_platform": {
   "code": "P13",
   "audience": "staff",
   "formFactor": "web",
   "shortName": "Venue CMS",
   "name": "Venue CMS — White Label",
   "app": "venue-management-web",
   "offlineCapable": false,
   "operator": "venue",
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P08",
     "P12",
     "P16"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "CMS-090",
  "name": "Governance Risk, Compliance & AI Recommendations",
  "module": "Media Library",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Digital Asset Management DAM.pdf",
   "board": "3",
   "number": "10",
   "page": 54
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/media-library/governance-risk-compliance-ai-recommendations-cms-090",
   "component": "apps/venue-management-web/src/routes/media-library/GovernanceRiskComplianceAiRecommendations.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "CMS-081"
   ],
   "exitTo": [
    "CMS-081"
   ],
   "transitions": [
    {
     "to": "CMS-081",
     "trigger": "Back to DAM Governance & Rights Command Center",
     "provenance": "structural — pack board 3 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Provide a consolidated view of governance risks and use AI to help identify problems requiring human attention.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Digital Asset Management DAM.pdf, page 54 §Display"
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
       "label": "Every governance risk compliance",
       "columns": [
        "Assets Without Rights",
        "Expired Assets",
        "Rights Expiring",
        "Unapproved Assets",
        "Restricted Assets in Active Usage",
        "External Shares",
        "Long-Lived Shares",
        "Missing Evidence",
        "Approval SLA Breaches",
        "Risk Queue"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Digital Asset Management DAM.pdf, page 54 §Display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected governance risk compliance",
       "bindsTo": null,
       "columns": [
        "Assets Without Rights",
        "Expired Assets",
        "Rights Expiring",
        "Unapproved Assets",
        "Restricted Assets in Active Usage",
        "External Shares",
        "Long-Lived Shares",
        "Missing Evidence",
        "Approval SLA Breaches",
        "Risk Queue"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Asset Risk Usage Severity Action”, “Digital Asset Management”, “Human Governance”, “Approved”, “However”, “Therefore”.",
       "provenance": "pack Digital Asset Management DAM.pdf, page 54 §Display"
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
       "notes": "**The pack separates these permissions and no action on the screen claims them yet:** ↓. Each needs attaching to the control it gates, or the screen needs the control.",
       "provenance": "pack Digital Asset Management DAM.pdf, page 54 §Permission Check"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The governance risk compliance list.",
   "error": "Could not load. Names which read failed and leaves the governance risk compliance untouched.",
   "emptyFirstRun": "No governance risk compliance yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the governance risk compliance are still there. The pack's own statuses are 🟢 Valid — the state names which is selected.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getExpiringRights",
    "contract": "assets",
    "purpose": "Risk from lapsing rights",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "entryState": {
   "preloaded": [
    "Assets Without Rights",
    "Expired Assets",
    "Rights Expiring",
    "Unapproved Assets",
    "Restricted Assets in Active Usage",
    "External Shares"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P13 Venue CMS.dc.html#cms-090",
   "workshopBoard": "wireframes/WS46 Digital Asset Management DAM Board 3.dc.html#cms-090"
  },
  "apisNote": "Regenerated 9 September 2026 from Digital Asset Management DAM.pdf page 54. 0 of 10 labels bound to a contract property; 13 of 169 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "_platform": {
   "code": "P13",
   "audience": "staff",
   "formFactor": "web",
   "shortName": "Venue CMS",
   "name": "Venue CMS — White Label",
   "app": "venue-management-web",
   "offlineCapable": false,
   "operator": "venue",
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P08",
     "P12",
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
 "createAccessPolicy": {
  "method": "POST",
  "path": "/access-policies",
  "contract": "identity",
  "summary": "Write a policy without writing code",
  "permission": "PERMISSION_MANAGE",
  "offlineCapable": null,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "AccessPolicy",
  "responds": "AccessPolicy"
 },
 "createMediaShare": {
  "method": "POST",
  "path": "/media-shares",
  "contract": "assets",
  "summary": "Share assets with somebody outside the platform, on terms",
  "permission": "ASSET_LIBRARY_SHARE",
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
  "requestBody": "MediaShare",
  "responds": "MediaShare"
 },
 "getExpiringRights": {
  "method": "GET",
  "path": "/media/rights-expiring",
  "contract": "assets",
  "summary": "Assets whose licence is expiring or expired",
  "permission": "ASSET_LIBRARY_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "withinDays",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "ExpiringMedia"
 },
 "getMediaAsset": {
  "method": "GET",
  "path": "/media/{mediaId}",
  "contract": "assets",
  "summary": "Read an asset with derivatives and usage",
  "permission": "ASSET_LIBRARY_VIEW",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "MediaAssetDetail"
 },
 "getMediaUsageAnalytics": {
  "method": "GET",
  "path": "/media-usage",
  "contract": "assets",
  "summary": "Downloads, views, shares and library health",
  "permission": "ASSET_LIBRARY_VIEW",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": "from",
    "in": "query",
    "required": null
   },
   {
    "name": "to",
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
  "responds": "MediaUsageRow"
 },
 "listAccessPolicies": {
  "method": "GET",
  "path": "/access-policies",
  "contract": "identity",
  "summary": "Attribute-based access policies",
  "permission": "PERMISSION_VIEW",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "status",
    "in": "query",
    "required": null
   },
   {
    "name": "scopePath",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "AccessPolicy"
 },
 "listMediaAssetAudit": {
  "method": "GET",
  "path": "/media-assets/{assetId}/audit",
  "contract": "assets",
  "summary": "Who did what to this asset, and who received it",
  "permission": "ASSET_LIBRARY_VIEW",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "tenant",
  "parameters": [],
  "requestBody": null,
  "responds": "MediaAuditRecord"
 },
 "setMediaAssetApproval": {
  "method": "POST",
  "path": "/media-assets/{assetId}/approval",
  "contract": "assets",
  "summary": "Submit, approve, reject or publish an asset",
  "permission": "ASSET_LIBRARY_APPROVE",
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
  "responds": "MediaAssetApproval"
 },
 "setMediaAssetRights": {
  "method": "PUT",
  "path": "/media-assets/{assetId}/rights",
  "contract": "assets",
  "summary": "Licence, permitted use and expiry",
  "permission": "ASSET_LIBRARY_MANAGE",
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
  "requestBody": "MediaRights",
  "responds": "MediaRights"
 },
 "updateMediaAsset": {
  "method": "PATCH",
  "path": "/media/{mediaId}",
  "contract": "assets",
  "summary": "Amend metadata, tags or rights",
  "permission": "ASSET_LIBRARY_MANAGE",
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
  "responds": "MediaAsset"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "AccessCondition": {
  "type": "object",
  "description": "**One attribute, one operator, one value** — and the attribute names are an enum rather than free text, because a policy that reads `venu.type` silently never matches.\nThe enum is the matrix, row by row: user (3.3.7), employee (3.3.8), membership (3.3.9), accreditation (3.3.10), customer segment (3.3.11), resource classification (3.3.12), venue (3.3.13), attraction (3.3.14), device (3.3.15), day of week (3.3.16), season (3.3.17), event (3.3.18), capacity (3.3.19), occupancy (3.3.20), risk score (3.3.21), location (3.3.2) and time (3.3.3).\n",
  "required": [
   "attribute",
   "operator"
  ],
  "properties": {
   "attribute": {
    "type": "string",
    "enum": [
     "user.attribute",
     "employee.attribute",
     "employee.onShift",
     "membership.tier",
     "membership.status",
     "accreditation.type",
     "accreditation.status",
     "customer.segment",
     "resource.classification",
     "venue.attribute",
     "venue.id",
     "attraction.attribute",
     "device.kind",
     "device.id",
     "device.trusted",
     "time.ofDay",
     "time.dayOfWeek",
     "time.season",
     "time.withinOperatingHours",
     "event.id",
     "event.status",
     "capacity.utilisationPercent",
     "occupancy.level",
     "risk.score",
     "ticket.status",
     "location.scopePath"
    ]
   },
   "key": {
    "type": "string",
    "nullable": true,
    "description": "For the `*.attribute` forms — which attribute, by code."
   },
   "operator": {
    "type": "string",
    "enum": [
     "equals",
     "notEquals",
     "in",
     "notIn",
     "greaterThan",
     "lessThan",
     "between",
     "contains",
     "startsWith",
     "exists"
    ]
   },
   "value": {
    "nullable": true,
    "description": "The single comparand for `equals`, `notEquals`, `greaterThan`, `lessThan`, `contains` and `startsWith` — a string, number or boolean, by the attribute. Null for `exists`; `in`, `notIn` and `between` use `values`.\n"
   },
   "values": {
    "type": "array",
    "items": {
     "type": "string"
    }
   }
  }
 },
 "AccessPolicy": {
  "type": "object",
  "x-ticvai-persistence": "identity.access_policy",
  "description": "3.3. **Conditions and an effect, evaluated by one engine.** A role says who you are; a policy says under what circumstances that is enough.\n\n**Which of the two policy engines this is** (stated 29 September, build pass). The package has two: this one, and the access contract's `AccessDynamicPolicy` (`access.dynamic_policy`). **This one governs who may do what in the software**: a principal's permissions on operations and screens (`permissions` names them), narrowed or extended by who, where, when and on what device, and decided by `evaluateAccess`. **`AccessDynamicPolicy` governs who may pass which gate**: a guest's, holder's or employee's admission at an access point, decided in the gate's validation with results such as `requireId` or `requireSupervisor` that mean nothing to a permission check. A staff member's badge opening a staff door is a gate decision (access); the same staff member approving a refund is a permission decision (here). The overlap that remains is listed in the build readiness open items rather than merged in this pass.\n",
  "required": [
   "code",
   "name",
   "effect"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "description": "Assigned by the server on `createAccessPolicy`; the path names the policy on update."
   },
   "code": {
    "type": "string"
   },
   "name": {
    "type": "string"
   },
   "description": {
    "type": "string",
    "nullable": true
   },
   "isTemplate": {
    "type": "boolean",
    "default": false
   },
   "permissions": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "**Which permissions this policy speaks to.** A policy with an empty list speaks to all of them, which is powerful enough that it is worth being explicit about.\n"
   },
   "conditions": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/AccessCondition"
    }
   },
   "combining": {
    "type": "string",
    "enum": [
     "allMustMatch",
     "anyMayMatch"
    ],
    "default": "allMustMatch"
   },
   "effect": {
    "type": "string",
    "enum": [
     "permit",
     "deny"
    ],
    "description": "**Deny wins over permit when two policies disagree.** 3.3.32 asks for least-privilege, and a permit that can override a deny is not least-privilege by any reading — it is the union of every mistake anybody has made.\n"
   },
   "priority": {
    "type": "integer",
    "default": 0
   },
   "scopePath": {
    "type": "string",
    "description": "3.3.40 to 3.3.43. **Tenant, venue and cross-venue policies are one mechanism**, because `scope_path` is prefix-comparable — `uae.dubai` contains `uae.dubai.marina` — and inheritance is the prefix walk rather than a second table.\n"
   },
   "appliesToRoleIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "status": {
    "type": "string",
    "readOnly": true,
    "description": "**Moved only by `setAccessPolicyState`.** A policy is created as a `draft`, and a status sent in a create or update body is ignored — otherwise a write could skip the approval 3.3.26 requires.\n",
    "enum": [
     "draft",
     "pendingApproval",
     "active",
     "suspended",
     "retired"
    ]
   },
   "version": {
    "type": "integer",
    "default": 1,
    "readOnly": true,
    "description": "Set by the server; every `updateAccessPolicy` writes a new version."
   },
   "effectiveFrom": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "effectiveTo": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "delegatedAdminRoleIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    },
    "description": "3.3.35. **Who may edit this policy without being a platform administrator.** A venue manager tuning their own opening-hours rule should not need someone who can edit every tenant's.\n"
   }
  }
 },
 "ExpiringMedia": {
  "x-ticvai-persistence": "none — computed",
  "type": "object",
  "required": [
   "assetId",
   "filename",
   "validTo",
   "isExpired",
   "isInUse"
  ],
  "properties": {
   "assetId": {
    "type": "string",
    "format": "uuid"
   },
   "filename": {
    "type": "string"
   },
   "thumbnailUrl": {
    "type": "string",
    "nullable": true
   },
   "licensor": {
    "type": "string",
    "nullable": true
   },
   "validTo": {
    "type": "string",
    "format": "date"
   },
   "daysRemaining": {
    "type": "integer"
   },
   "isExpired": {
    "type": "boolean"
   },
   "isInUse": {
    "type": "boolean",
    "description": "True while `liveUsageCount` is above zero, that is, while live (published) content references the asset (audit R106 (10)). Drafts and collections do not count."
   },
   "liveUsageCount": {
    "type": "integer",
    "description": "References from live (published) content only (audit R106 (10)). Expired and live is the combination that matters."
   }
  }
 },
 "LocalisedText": {
  "x-ticvai-persistence": "none — jsonb column",
  "type": "object",
  "additionalProperties": {
   "type": "string"
  }
 },
 "MediaAsset": {
  "x-ticvai-persistence": "assets.media_asset",
  "type": "object",
  "required": [
   "id",
   "kind",
   "status",
   "filename",
   "contentType",
   "sizeBytes",
   "referenceCount",
   "createdAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "kind": {
    "$ref": "#/components/schemas/MediaKind"
   },
   "status": {
    "$ref": "#/components/schemas/MediaStatus"
   },
   "filename": {
    "type": "string"
   },
   "contentType": {
    "type": "string"
   },
   "sizeBytes": {
    "type": "integer"
   },
   "title": {
    "$ref": "#/components/schemas/LocalisedText"
   },
   "description": {
    "allOf": [
     {
      "$ref": "#/components/schemas/LocalisedText"
     }
    ],
    "description": "Set by `updateMediaAsset` and matched by `searchMedia`'s `search`. It was accepted and searched on before it had anywhere to be stored.\n"
   },
   "altText": {
    "allOf": [
     {
      "$ref": "#/components/schemas/LocalisedText"
     }
    ],
    "description": "Required before use in a guest-facing surface. WCAG 2.2 AA."
   },
   "width": {
    "type": "integer",
    "nullable": true
   },
   "height": {
    "type": "integer",
    "nullable": true
   },
   "durationSeconds": {
    "type": "number",
    "nullable": true
   },
   "customMetadata": {
    "type": "object",
    "nullable": true,
    "additionalProperties": true,
    "description": "BL-178. **`assets` is a strong contract and its metadata was fixed** — kind, title, alt text, dimensions, rights. A venue photographing four thousand products wants its own fields: shoot date, photographer, model release, season.\n**Free-form and searchable, not a schema.** Every venue would want a different one, and a fixed set would be wrong for all of them.\n"
   },
   "sharedWithTenantIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    },
    "description": "BL-178. **Cross-tenant sharing, and it is refused by default for a reason.** A brand operating three venues wants one logo library; two unrelated tenants sharing an asset store is the isolation breach ADR-0011 exists to prevent.\n**Only within one tenant's own scope tree.** A share naming a tenant outside it is refused rather than warned about — this is the one place where a permissive default would be a cross-tenant data leak.\n"
   },
   "tags": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "categoryId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The asset's category, one of `MediaTaxonomy.categories[].id`; null while unclassified. Set by `bulkUpdateMediaAssets` (`setCategoryId`) (decided 29 September, data model DM4).\n"
   },
   "venueId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "url": {
    "type": "string",
    "description": "Signed and expiring for private assets; stable CDN URL for public ones."
   },
   "thumbnailUrl": {
    "type": "string",
    "nullable": true
   },
   "referenceCount": {
    "type": "integer",
    "description": "How many surfaces reference this asset. Non-zero refuses deletion.\n"
   },
   "rights": {
    "$ref": "#/components/schemas/MediaRights"
   },
   "isRightsExpired": {
    "type": "boolean"
   },
   "version": {
    "type": "integer"
   },
   "uploadedByPrincipalId": {
    "type": "string",
    "format": "uuid"
   },
   "createdAt": {
    "type": "string",
    "format": "date-time"
   }
  }
 },
 "MediaAssetApproval": {
  "type": "object",
  "x-ticvai-persistence": "assets.approval",
  "description": "Boards 3.4 and 3.5. **Publication eligibility is computed from four facts.**",
  "properties": {
   "assetId": {
    "type": "string",
    "format": "uuid"
   },
   "state": {
    "type": "string",
    "enum": [
     "draft",
     "pendingApproval",
     "approved",
     "rejected",
     "published",
     "archived"
    ]
   },
   "eligibility": {
    "type": "array",
    "readOnly": true,
    "items": {
     "type": "object",
     "properties": {
      "check": {
       "type": "string",
       "enum": [
        "approved",
        "rightsCurrent",
        "renditionsReady",
        "classificationComplete"
       ]
      },
      "satisfied": {
       "type": "boolean"
      },
      "detail": {
       "type": "string",
       "nullable": true
      }
     }
    }
   },
   "approvedBy": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "comment": {
    "type": "string",
    "nullable": true
   },
   "at": {
    "type": "string",
    "format": "date-time"
   },
   "scopePath": {
    "type": "string"
   }
  }
 },
 "MediaAssetDetail": {
  "x-ticvai-persistence": "assets.media_asset",
  "allOf": [
   {
    "$ref": "#/components/schemas/MediaAsset"
   },
   {
    "type": "object",
    "properties": {
     "derivatives": {
      "type": "array",
      "description": "Generated from the original, never uploaded separately. A new breakpoint is a re-render rather than a re-upload of everything.\n",
      "items": {
       "type": "object",
       "properties": {
        "label": {
         "type": "string"
        },
        "width": {
         "type": "integer"
        },
        "height": {
         "type": "integer"
        },
        "sizeBytes": {
         "type": "integer"
        },
        "url": {
         "type": "string"
        }
       }
      }
     },
     "usage": {
      "type": "array",
      "description": "Every place this asset is referenced.",
      "items": {
       "$ref": "#/components/schemas/MediaUsage"
      }
     },
     "collections": {
      "type": "array",
      "items": {
       "type": "object",
       "properties": {
        "id": {
         "type": "string",
         "format": "uuid"
        },
        "name": {
         "type": "string"
        }
       }
      }
     },
     "previousVersions": {
      "type": "array",
      "items": {
       "type": "object",
       "properties": {
        "version": {
         "type": "integer"
        },
        "replacedAt": {
         "type": "string",
         "format": "date-time"
        },
        "replacedByPrincipalId": {
         "type": "string",
         "format": "uuid"
        }
       }
      }
     }
    }
   }
  ]
 },
 "MediaAuditRecord": {
  "type": "object",
  "x-ticvai-persistence": "assets.audit",
  "description": "Board 3.9. **Distribution as well as edits** — the question asked afterwards is who had it.\n",
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "assetId": {
    "type": "string",
    "format": "uuid"
   },
   "at": {
    "type": "string",
    "format": "date-time"
   },
   "action": {
    "type": "string",
    "enum": [
     "uploaded",
     "updated",
     "retagged",
     "versioned",
     "approved",
     "published",
     "shared",
     "downloaded",
     "delivered",
     "archived",
     "deleted"
    ]
   },
   "actorId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "recipient": {
    "type": "string",
    "nullable": true
   },
   "detail": {
    "type": "string",
    "nullable": true
   },
   "scopePath": {
    "type": "string"
   }
  }
 },
 "MediaKind": {
  "type": "string",
  "enum": [
   "image",
   "video",
   "audio",
   "document",
   "vector",
   "font",
   "archive"
  ]
 },
 "MediaRights": {
  "x-ticvai-persistence": "none — embedded in asset",
  "type": "object",
  "description": "Licensing terms. Tracked because an expired licence on a live surface is a legal exposure, not a housekeeping item.\n",
  "properties": {
   "licenceKind": {
    "type": "string",
    "enum": [
     "owned",
     "royaltyFree",
     "rightsManaged",
     "creativeCommons",
     "editorialOnly",
     "unknown"
    ]
   },
   "licensor": {
    "type": "string",
    "nullable": true
   },
   "licenceReference": {
    "type": "string",
    "nullable": true
   },
   "validFrom": {
    "type": "string",
    "format": "date",
    "nullable": true
   },
   "validTo": {
    "type": "string",
    "format": "date",
    "nullable": true
   },
   "permittedUses": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "web",
      "print",
      "socialMedia",
      "inVenue",
      "advertising",
      "internal"
     ]
    }
   },
   "attributionRequired": {
    "type": "boolean",
    "default": false
   },
   "attributionText": {
    "type": "string",
    "nullable": true
   },
   "permittedTerritories": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "ISO country or region codes. **Empty means unrestricted, which is a claim rather than an absence** — an unknown territory and a worldwide licence are not the same thing, and `licenceKind: unknown` is how the second is said.\n"
   },
   "permittedChannels": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Distribution channel codes, checked by `setMediaDistributionChannels`. Narrower than `permittedUses`, which describes the medium rather than the route.\n"
   },
   "modelReleaseHeld": {
    "type": "boolean",
    "default": false
   },
   "renewalOwner": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   }
  }
 },
 "MediaShare": {
  "type": "object",
  "x-ticvai-persistence": "assets.share",
  "description": "Board 3.7. **A licence grant with a link attached** — revocable, expiring and logged.",
  "required": [
   "assetIds",
   "expiresAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "assetIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "recipientEmail": {
    "type": "string",
    "nullable": true
   },
   "recipientOrganisation": {
    "type": "string",
    "nullable": true
   },
   "allowDownload": {
    "type": "boolean",
    "default": false
   },
   "allowedRenditions": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "passwordProtected": {
    "type": "boolean",
    "default": false
   },
   "expiresAt": {
    "type": "string",
    "format": "date-time"
   },
   "revokedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "url": {
    "type": "string",
    "readOnly": true
   },
   "openedCount": {
    "type": "integer",
    "readOnly": true
   },
   "scopePath": {
    "type": "string"
   }
  }
 },
 "MediaStatus": {
  "type": "string",
  "enum": [
   "processing",
   "ready",
   "quarantined",
   "failed",
   "archived"
  ]
 },
 "MediaUsage": {
  "x-ticvai-persistence": "assets.media_usage",
  "type": "object",
  "description": "One place an asset is used. **`surface: product` is written by catalogue** for each item of `Product.media` (decided 29 September, rev 3 23SEP-4): `referenceId` is the product id and `isLive` is true while the product is listed to guests, which is what stops an asset in use on a ticket card being archived from under it.\n",
  "required": [
   "surface",
   "referenceId"
  ],
  "properties": {
   "extractedText": {
    "type": "string",
    "description": "**Text pulled out of an uploaded document**, after extraction. The generic retrieval path for anything a tenant uploads — a PDF nobody can search is a PDF nobody reads.\n"
   },
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "description": "**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"
   },
   "surface": {
    "type": "string",
    "enum": [
     "tenantBranding",
     "homepageBanner",
     "promoBlock",
     "contentPage",
     "product",
     "event",
     "menuItem",
     "merchandise",
     "workOrder",
     "incident",
     "inspection",
     "campaign"
    ]
   },
   "referenceId": {
    "type": "string"
   },
   "label": {
    "type": "string"
   },
   "isLive": {
    "type": "boolean",
    "description": "True where the referencing surface is published to guests."
   }
  }
 },
 "MediaUsageRow": {
  "type": "object",
  "description": "Boards 1.10 and 4.9. **Assets never used is the number that justifies the library.**",
  "properties": {
   "key": {
    "type": "string"
   },
   "label": {
    "type": "string"
   },
   "assetCount": {
    "type": "integer"
   },
   "storageBytes": {
    "type": "integer"
   },
   "downloads": {
    "type": "integer"
   },
   "views": {
    "type": "integer"
   },
   "shares": {
    "type": "integer"
   },
   "neverUsedCount": {
    "type": "integer"
   },
   "unclassifiedCount": {
    "type": "integer"
   }
  }
 }
}
```
