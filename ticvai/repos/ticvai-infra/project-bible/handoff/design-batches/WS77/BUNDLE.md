# WS77 — Digital Asset Management DAM board 4

**10 screens · 0 operations · 0 schemas · 0 permissions**

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

- **Every control that can be refused must be gated.** 0 permissions apply here:
  ``. A control nobody can use must say so,
  not sit enabled and fail.
- **0 of these operations work offline**
  
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `CMS-091` | Asset Distribution & Delivery Command Center | listDetail | 0 | 0 | — |
| `CMS-092` | Asset Usage & Distribution Map | listDetail | 0 | 0 | — |
| `CMS-093` | Channel & Distribution Configuration | configEditor | 0 | 0 | — |
| `CMS-094` | Secure Delivery URL, CDN & Rendition Delivery | listDetail | 0 | 0 | — |
| `CMS-095` | Asset Replacement & Propagation Management | listDetail | 0 | 0 | — |
| `CMS-096` | Fallback, Expiry & Distribution Continuity | configEditor | 0 | 0 | — |
| `CMS-097` | DAM API & Integration Hub | listDetail | 0 | 0 | — |
| `CMS-098` | Delivery Monitoring & Integration Health | commandCentre | 0 | 0 | — |
| `CMS-099` | Asset Usage & Performance Analytics | commandCentre | 0 | 0 | — |
| `CMS-100` | Distribution Intelligence, AI Insights & Optimization | configEditor | 0 | 0 | — |

## Thin screens in this batch

**CMS-092, CMS-097, CMS-100 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "CMS-091",
  "name": "Asset Distribution & Delivery Command Center",
  "module": "Media Library",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Digital Asset Management DAM.pdf",
   "board": "4",
   "number": "1",
   "page": 62
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/media-library/asset-distribution-delivery-command-center-cms-091",
   "component": "apps/venue-management-web/src/routes/media-library/AssetDistributionDeliveryCommandCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "CMS-001"
   ],
   "exitTo": [
    "CMS-001",
    "CMS-092",
    "CMS-093",
    "CMS-094",
    "CMS-095",
    "CMS-096",
    "CMS-097",
    "CMS-098",
    "CMS-099",
    "CMS-100"
   ],
   "transitions": [
    {
     "to": "CMS-001",
     "trigger": "Back to Tenant Workspace",
     "provenance": "structural — pack board 4 wiring, 11 September 2026",
     "back": true
    },
    {
     "to": "CMS-092",
     "trigger": "Asset Usage & Distribution Map",
     "provenance": "structural — pack board 4 wiring, 11 September 2026"
    },
    {
     "to": "CMS-093",
     "trigger": "Channel & Distribution Configuration",
     "provenance": "structural — pack board 4 wiring, 11 September 2026"
    },
    {
     "to": "CMS-094",
     "trigger": "Secure Delivery URL, CDN & Rendition Delivery",
     "provenance": "structural — pack board 4 wiring, 11 September 2026"
    },
    {
     "to": "CMS-095",
     "trigger": "Asset Replacement & Propagation Management",
     "provenance": "structural — pack board 4 wiring, 11 September 2026"
    },
    {
     "to": "CMS-096",
     "trigger": "Fallback, Expiry & Distribution Continuity",
     "provenance": "structural — pack board 4 wiring, 11 September 2026"
    },
    {
     "to": "CMS-097",
     "trigger": "DAM API & Integration Hub",
     "provenance": "structural — pack board 4 wiring, 11 September 2026"
    },
    {
     "to": "CMS-098",
     "trigger": "Delivery Monitoring & Integration Health",
     "provenance": "structural — pack board 4 wiring, 11 September 2026"
    },
    {
     "to": "CMS-099",
     "trigger": "Asset Usage & Performance Analytics",
     "provenance": "structural — pack board 4 wiring, 11 September 2026"
    },
    {
     "to": "CMS-100",
     "trigger": "Distribution Intelligence, AI Insights & Optimization",
     "provenance": "structural — pack board 4 wiring, 11 September 2026"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display; Show) and no metric row",
  "purpose": "Provide a centralized operational overview of asset distribution across TICVAI and connected external channels.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 6 actions on this screen and the screen declares 0 operations.** Unserved: Distribution Map, Channel Management, Delivery Monitor, Replacement Center, API & Integration, Analytics. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Digital Asset Management DAM.pdf, page 62 §Quick Actions"
   },
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Digital Asset Management DAM.pdf, page 62 §Display"
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
       "label": "Every asset distribution delivery",
       "columns": [
        "Assets in Active Use",
        "Active Asset References",
        "Delivery Requests",
        "Active Channels",
        "CDN/Data Delivery",
        "Failed Deliveries",
        "Assets Requiring Replacement",
        "Expiring Assets in Active Use",
        "API Requests",
        "Delivery Availability %",
        "B2C Website",
        "Mobile App",
        "POS",
        "Kiosk",
        "Ticket Media",
        "Marketing",
        "Digital Signage",
        "Partner/API",
        "Delivery Health",
        "🟢 Healthy",
        "🟡 Degraded",
        "🔴 Failed",
        "⚪ Inactive",
        "Critical Alerts"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Digital Asset Management DAM.pdf, page 62 §Display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected asset distribution delivery",
       "bindsTo": null,
       "columns": [
        "Assets in Active Use",
        "Active Asset References",
        "Delivery Requests",
        "Active Channels",
        "CDN/Data Delivery",
        "Failed Deliveries",
        "Assets Requiring Replacement",
        "Expiring Assets in Active Use",
        "API Requests",
        "Delivery Availability %",
        "B2C Website",
        "Mobile App",
        "POS",
        "Kiosk",
        "Ticket Media",
        "Marketing",
        "Digital Signage",
        "Partner/API",
        "Delivery Health",
        "🟢 Healthy",
        "🟡 Degraded",
        "🔴 Failed",
        "⚪ Inactive",
        "Critical Alerts"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Digital Asset Management”, “Active Channels 28”.",
       "provenance": "pack Digital Asset Management DAM.pdf, page 62 §Display"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Distribution Map",
       "provenance": "pack Digital Asset Management DAM.pdf, page 62 §Quick Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Channel Management",
       "provenance": "pack Digital Asset Management DAM.pdf, page 62 §Quick Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Delivery Monitor",
       "provenance": "pack Digital Asset Management DAM.pdf, page 62 §Quick Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Replacement Center",
       "provenance": "pack Digital Asset Management DAM.pdf, page 62 §Quick Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "API & Integration",
       "provenance": "pack Digital Asset Management DAM.pdf, page 62 §Quick Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Analytics",
       "provenance": "pack Digital Asset Management DAM.pdf, page 62 §Quick Actions"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The asset distribution delivery list.",
   "error": "Could not load. Names which read failed and leaves the asset distribution delivery untouched.",
   "emptyFirstRun": "No asset distribution delivery yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the asset distribution delivery are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "entryState": {
   "preloaded": [
    "Assets in Active Use",
    "Active Asset References",
    "Delivery Requests",
    "Active Channels",
    "CDN/Data Delivery",
    "Failed Deliveries"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P13 Venue CMS.dc.html#cms-091"
  },
  "apisNote": "Regenerated 9 September 2026 from Digital Asset Management DAM.pdf page 62. 0 of 24 labels bound to a contract property; 30 of 39 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "CMS-092",
  "name": "Asset Usage & Distribution Map",
  "module": "Media Library",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Digital Asset Management DAM.pdf",
   "board": "4",
   "number": "2",
   "page": 64
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/media-library/asset-usage-distribution-map-cms-092",
   "component": "apps/venue-management-web/src/routes/media-library/AssetUsageDistributionMap.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "CMS-091"
   ],
   "exitTo": [
    "CMS-091"
   ],
   "transitions": [
    {
     "to": "CMS-091",
     "trigger": "Back to Asset Distribution & Delivery Command Center",
     "provenance": "structural — pack board 4 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Show) and no metric row",
  "purpose": "Show exactly where a digital asset is currently being used. This is one of the most important screens in the DAM.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Digital Asset Management DAM.pdf, page 64 §Show"
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
       "label": "Every asset usage distribution",
       "columns": [
        "TICVAI DAM Asset",
        "↓",
        "B2C Website — 5",
        "Mobile App — 4",
        "Kiosk — 3",
        "Ticket Media — 2",
        "Marketing Campaign — 3",
        "Digital Signage — 1"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Digital Asset Management DAM.pdf, page 64 §Show"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected asset usage distribution",
       "bindsTo": null,
       "columns": [
        "TICVAI DAM Asset",
        "↓",
        "B2C Website — 5",
        "Mobile App — 4",
        "Kiosk — 3",
        "Ticket Media — 2",
        "Marketing Campaign — 3",
        "Digital Signage — 1"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Dubai Park Hero”, “Usage Table”, “Reference Type”, “Follow Current Version”, “Critical Requirement”.",
       "provenance": "pack Digital Asset Management DAM.pdf, page 64 §Show"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The asset usage distribution list.",
   "error": "Could not load. Names which read failed and leaves the asset usage distribution untouched.",
   "emptyFirstRun": "No asset usage distribution yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the asset usage distribution are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "entryState": {
   "preloaded": [
    "TICVAI DAM Asset",
    "↓",
    "B2C Website — 5",
    "Mobile App — 4",
    "Kiosk — 3",
    "Ticket Media — 2"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P13 Venue CMS.dc.html#cms-092"
  },
  "apisNote": "Regenerated 9 September 2026 from Digital Asset Management DAM.pdf page 64. 0 of 8 labels bound to a contract property; 8 of 24 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "CMS-093",
  "name": "Channel & Distribution Configuration",
  "module": "Media Library",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Digital Asset Management DAM.pdf",
   "board": "4",
   "number": "3",
   "page": 65
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/media-library/channel-distribution-configuration-cms-093",
   "component": "apps/venue-management-web/src/routes/media-library/ChannelDistributionConfiguration.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "CMS-091"
   ],
   "exitTo": [
    "CMS-091"
   ],
   "transitions": [
    {
     "to": "CMS-091",
     "trigger": "Back to Asset Distribution & Delivery Command Center",
     "provenance": "structural — pack board 4 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population",
  "purpose": "Configure how DAM content can be consumed by different TICVAI modules and external channels.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Channel name",
       "provenance": "pack Digital Asset Management DAM.pdf, page 65 §Configure"
      },
      {
       "kind": "selectField",
       "label": "channel type",
       "provenance": "pack Digital Asset Management DAM.pdf, page 65 §Configure"
      },
      {
       "kind": "selectField",
       "label": "tenant",
       "provenance": "pack Digital Asset Management DAM.pdf, page 65 §Configure"
      },
      {
       "kind": "selectField",
       "label": "venue scope",
       "provenance": "pack Digital Asset Management DAM.pdf, page 65 §Configure"
      },
      {
       "kind": "selectField",
       "label": "allowed asset types",
       "provenance": "pack Digital Asset Management DAM.pdf, page 65 §Configure"
      },
      {
       "kind": "selectField",
       "label": "allowed categories",
       "provenance": "pack Digital Asset Management DAM.pdf, page 65 §Configure"
      },
      {
       "kind": "selectField",
       "label": "required approval",
       "provenance": "pack Digital Asset Management DAM.pdf, page 65 §Configure"
      },
      {
       "kind": "selectField",
       "label": "required rights",
       "provenance": "pack Digital Asset Management DAM.pdf, page 65 §Configure"
      },
      {
       "kind": "selectField",
       "label": "preferred rendition",
       "provenance": "pack Digital Asset Management DAM.pdf, page 65 §Configure"
      },
      {
       "kind": "selectField",
       "label": "fallback rendition",
       "provenance": "pack Digital Asset Management DAM.pdf, page 65 §Configure"
      },
      {
       "kind": "selectField",
       "label": "delivery method",
       "provenance": "pack Digital Asset Management DAM.pdf, page 65 §Configure"
      },
      {
       "kind": "selectField",
       "label": "caching policy",
       "provenance": "pack Digital Asset Management DAM.pdf, page 65 §Configure"
      },
      {
       "kind": "selectField",
       "label": "authentication requirement",
       "provenance": "pack Digital Asset Management DAM.pdf, page 65 §Configure"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The channel distribution configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the channel distribution untouched.",
   "emptyFirstRun": "No channel distribution configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P13 Venue CMS.dc.html#cms-093"
  },
  "apisNote": "Regenerated 9 September 2026 from Digital Asset Management DAM.pdf page 65. 0 of 0 labels bound to a contract property; 13 of 19 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "CMS-094",
  "name": "Secure Delivery URL, CDN & Rendition Delivery",
  "module": "Media Library",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Digital Asset Management DAM.pdf",
   "board": "4",
   "number": "4",
   "page": 66
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/media-library/secure-delivery-url-cdn-rendition-delivery-cms-094",
   "component": "apps/venue-management-web/src/routes/media-library/SecureDeliveryUrlCdnRenditionDelivery.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "CMS-091"
   ],
   "exitTo": [
    "CMS-091"
   ],
   "transitions": [
    {
     "to": "CMS-091",
     "trigger": "Back to Asset Distribution & Delivery Command Center",
     "provenance": "structural — pack board 4 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Provide optimized and controlled delivery of DAM assets without exposing private storage.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 3 actions on this screen and the screen declares 0 operations.** Unserved: configurable expiry, cache policy, revocation where applicable. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Digital Asset Management DAM.pdf, page 66 §Support"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Digital Asset Management DAM.pdf, page 66"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Digital Asset Management DAM.pdf, page 66"
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
       "label": "configurable expiry",
       "provenance": "pack Digital Asset Management DAM.pdf, page 66 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "cache policy",
       "provenance": "pack Digital Asset Management DAM.pdf, page 66 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "revocation where applicable",
       "provenance": "pack Digital Asset Management DAM.pdf, page 66 §Support"
      },
      {
       "kind": "banner",
       "label": "Permissions this screen separates",
       "notes": "**The pack separates these permissions and no action on the screen claims them yet:** ↓. Each needs attaching to the control it gates, or the screen needs the control.",
       "provenance": "pack Digital Asset Management DAM.pdf, page 66 §Permission / Eligibility Check"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The secure delivery url list.",
   "error": "Could not load. Names which read failed and leaves the secure delivery url untouched.",
   "emptyFirstRun": "No secure delivery url yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the secure delivery url are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P13 Venue CMS.dc.html#cms-094"
  },
  "apisNote": "Regenerated 9 September 2026 from Digital Asset Management DAM.pdf page 66. 0 of 0 labels bound to a contract property; 4 of 18 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "CMS-095",
  "name": "Asset Replacement & Propagation Management",
  "module": "Media Library",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Digital Asset Management DAM.pdf",
   "board": "4",
   "number": "5",
   "page": 67
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/media-library/asset-replacement-propagation-management-cms-095",
   "component": "apps/venue-management-web/src/routes/media-library/AssetReplacementPropagationManagement.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "CMS-091"
   ],
   "exitTo": [
    "CMS-091"
   ],
   "transitions": [
    {
     "to": "CMS-091",
     "trigger": "Back to Asset Distribution & Delivery Command Center",
     "provenance": "structural — pack board 4 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Safely manage replacement of assets that are outdated, expired, incorrect, rebranded, or otherwise no longer suitable.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 5 actions on this screen and the screen declares 0 operations.** Unserved: Replace Everywhere Eligible, Replace Selected Uses, Schedule Replacement, Keep Existing Version, Create Fallback. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Digital Asset Management DAM.pdf, page 67 §Support"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Digital Asset Management DAM.pdf, page 67"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Digital Asset Management DAM.pdf, page 67"
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
       "label": "Replace Everywhere Eligible",
       "provenance": "pack Digital Asset Management DAM.pdf, page 67 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Replace Selected Uses",
       "provenance": "pack Digital Asset Management DAM.pdf, page 67 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Schedule Replacement",
       "provenance": "pack Digital Asset Management DAM.pdf, page 67 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Keep Existing Version",
       "provenance": "pack Digital Asset Management DAM.pdf, page 67 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Create Fallback",
       "provenance": "pack Digital Asset Management DAM.pdf, page 67 §Support"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The asset replacement propagation list.",
   "error": "Could not load. Names which read failed and leaves the asset replacement propagation untouched.",
   "emptyFirstRun": "No asset replacement propagation yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the asset replacement propagation are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P13 Venue CMS.dc.html#cms-095"
  },
  "apisNote": "Regenerated 9 September 2026 from Digital Asset Management DAM.pdf page 67. 0 of 0 labels bound to a contract property; 5 of 18 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "CMS-096",
  "name": "Fallback, Expiry & Distribution Continuity",
  "module": "Media Library",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Digital Asset Management DAM.pdf",
   "board": "4",
   "number": "6",
   "page": 68
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/media-library/fallback-expiry-distribution-continuity-cms-096",
   "component": "apps/venue-management-web/src/routes/media-library/FallbackExpiryDistributionContinuity.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "CMS-091"
   ],
   "exitTo": [
    "CMS-091"
   ],
   "transitions": [
    {
     "to": "CMS-091",
     "trigger": "Back to Asset Distribution & Delivery Command Center",
     "provenance": "structural — pack board 4 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configured Fallback) and no display directory — it is settings, not a population",
  "purpose": "Ensure channels do not break when an asset becomes unavailable, expired, blocked, or fails delivery.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 12 actions on this screen and the screen declares 0 operations.** Unserved: Usage-Level Fallback, Asset archived, rights expired, approval revoked, rendition unavailable, asset restricted, delivery failure, version unavailable …. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Digital Asset Management DAM.pdf, page 68 §Support"
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
       "kind": "textField",
       "label": "DAM-IMG-009211 — Default Dubai Park Hero",
       "provenance": "pack Digital Asset Management DAM.pdf, page 68 §Configured Fallback"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Usage-Level Fallback",
       "provenance": "pack Digital Asset Management DAM.pdf, page 68 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Asset archived",
       "provenance": "pack Digital Asset Management DAM.pdf, page 68 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "rights expired",
       "provenance": "pack Digital Asset Management DAM.pdf, page 68 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "approval revoked",
       "provenance": "pack Digital Asset Management DAM.pdf, page 68 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "rendition unavailable",
       "provenance": "pack Digital Asset Management DAM.pdf, page 68 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "asset restricted",
       "provenance": "pack Digital Asset Management DAM.pdf, page 68 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "delivery failure",
       "provenance": "pack Digital Asset Management DAM.pdf, page 68 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "version unavailable",
       "provenance": "pack Digital Asset Management DAM.pdf, page 68 §Support"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The fallback expiry distribution configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the fallback expiry distribution untouched.",
   "emptyFirstRun": "No fallback expiry distribution configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P13 Venue CMS.dc.html#cms-096"
  },
  "apisNote": "Regenerated 9 September 2026 from Digital Asset Management DAM.pdf page 68. 0 of 0 labels bound to a contract property; 14 of 25 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "CMS-097",
  "name": "DAM API & Integration Hub",
  "module": "Media Library",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Digital Asset Management DAM.pdf",
   "board": "4",
   "number": "7",
   "page": 69
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/media-library/dam-api-integration-hub-cms-097",
   "component": "apps/venue-management-web/src/routes/media-library/DamApiIntegrationHub.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "CMS-091"
   ],
   "exitTo": [
    "CMS-091"
   ],
   "transitions": [
    {
     "to": "CMS-091",
     "trigger": "Back to Asset Distribution & Delivery Command Center",
     "provenance": "structural — pack board 4 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Provide controlled APIs and integration services for internal TICVAI modules and approved external systems.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 1 actions on this screen and the screen declares 0 operations.** Unserved: API credentials. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Digital Asset Management DAM.pdf, page 69 §Support appropriate"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Digital Asset Management DAM.pdf, page 69"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Digital Asset Management DAM.pdf, page 69"
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
       "label": "API credentials",
       "provenance": "pack Digital Asset Management DAM.pdf, page 69 §Support appropriate"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The dam api integration list.",
   "error": "Could not load. Names which read failed and leaves the dam api integration untouched.",
   "emptyFirstRun": "No dam api integration yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the dam api integration are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P13 Venue CMS.dc.html#cms-097"
  },
  "apisNote": "Regenerated 9 September 2026 from Digital Asset Management DAM.pdf page 69. 0 of 0 labels bound to a contract property; 1 of 13 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "CMS-098",
  "name": "Delivery Monitoring & Integration Health",
  "module": "Media Library",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Digital Asset Management DAM.pdf",
   "board": "4",
   "number": "8",
   "page": 70
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/media-library/delivery-monitoring-integration-health-cms-098",
   "component": "apps/venue-management-web/src/routes/media-library/DeliveryMonitoringIntegrationHealth.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "CMS-091"
   ],
   "exitTo": [
    "CMS-091"
   ],
   "transitions": [
    {
     "to": "CMS-091",
     "trigger": "Back to Asset Distribution & Delivery Command Center",
     "provenance": "structural — pack board 4 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen a metric directory (§Display; Detect) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's",
  "purpose": "Monitor the technical health of DAM delivery and connected integrations.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 11 actions on this screen and the screen declares 0 operations.** Unserved: View Consumer, Assign Replacement, Retry, View Logs, Notify Owner, Alerting, high error rate, delivery latency …. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Digital Asset Management DAM.pdf, page 70 §Actions"
   }
  ],
  "layout": {
   "template": "dashboard",
   "regions": [
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "Delivery Availability",
       "provenance": "pack Digital Asset Management DAM.pdf, page 70 §Display"
      },
      {
       "kind": "metricTile",
       "label": "Average Response Time",
       "provenance": "pack Digital Asset Management DAM.pdf, page 70 §Display"
      },
      {
       "kind": "metricTile",
       "label": "CDN Cache Hit %",
       "provenance": "pack Digital Asset Management DAM.pdf, page 70 §Display"
      },
      {
       "kind": "metricTile",
       "label": "API Success %",
       "provenance": "pack Digital Asset Management DAM.pdf, page 70 §Display"
      },
      {
       "kind": "metricTile",
       "label": "Failed Requests",
       "provenance": "pack Digital Asset Management DAM.pdf, page 70 §Display"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "View Consumer",
       "provenance": "pack Digital Asset Management DAM.pdf, page 70 §Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Assign Replacement",
       "provenance": "pack Digital Asset Management DAM.pdf, page 70 §Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Retry",
       "provenance": "pack Digital Asset Management DAM.pdf, page 70 §Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "View Logs",
       "provenance": "pack Digital Asset Management DAM.pdf, page 70 §Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Notify Owner",
       "provenance": "pack Digital Asset Management DAM.pdf, page 70 §Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Alerting",
       "provenance": "pack Digital Asset Management DAM.pdf, page 70 §Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "high error rate",
       "provenance": "pack Digital Asset Management DAM.pdf, page 70 §Support alerts for"
      },
      {
       "kind": "secondaryButton",
       "label": "delivery latency",
       "provenance": "pack Digital Asset Management DAM.pdf, page 70 §Support alerts for"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The delivery monitoring integration list; the counts above it resolve separately.",
   "error": "Could not load. Names which read failed and leaves the delivery monitoring integration untouched.",
   "emptyFirstRun": "No delivery monitoring integration yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the delivery monitoring integration are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P13 Venue CMS.dc.html#cms-098"
  },
  "apisNote": "Regenerated 9 September 2026 from Digital Asset Management DAM.pdf page 70. 0 of 0 labels bound to a contract property; 16 of 32 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "CMS-099",
  "name": "Asset Usage & Performance Analytics",
  "module": "Media Library",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Digital Asset Management DAM.pdf",
   "board": "4",
   "number": "9",
   "page": 71
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/media-library/asset-usage-performance-analytics-cms-099",
   "component": "apps/venue-management-web/src/routes/media-library/AssetUsagePerformanceAnalytics.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "CMS-091"
   ],
   "exitTo": [
    "CMS-091"
   ],
   "transitions": [
    {
     "to": "CMS-091",
     "trigger": "Back to Asset Distribution & Delivery Command Center",
     "provenance": "structural — pack board 4 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen both a metric directory (§Performance Metrics) and a per-row directory (§Display; Identify) — counts over a population, then the population",
  "purpose": "Show how digital assets are actually being consumed across TICVAI.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Digital Asset Management DAM.pdf, page 71 §Display"
   }
  ],
  "layout": {
   "template": "dashboard",
   "regions": [
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "impressions",
       "provenance": "pack Digital Asset Management DAM.pdf, page 71 §Performance Metrics"
      },
      {
       "kind": "metricTile",
       "label": "requests",
       "provenance": "pack Digital Asset Management DAM.pdf, page 71 §Performance Metrics"
      },
      {
       "kind": "metricTile",
       "label": "downloads",
       "provenance": "pack Digital Asset Management DAM.pdf, page 71 §Performance Metrics"
      },
      {
       "kind": "metricTile",
       "label": "delivery volume",
       "provenance": "pack Digital Asset Management DAM.pdf, page 71 §Performance Metrics"
      },
      {
       "kind": "metricTile",
       "label": "reuse count",
       "provenance": "pack Digital Asset Management DAM.pdf, page 71 §Performance Metrics"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "moduleTiles",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every asset usage performance",
       "columns": [
        "Assets Used",
        "Asset Requests",
        "Downloads"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Digital Asset Management DAM.pdf, page 71 §Display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected asset usage performance",
       "bindsTo": null,
       "columns": [
        "Assets Used",
        "Asset Requests",
        "Downloads"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Digital Asset Management”, “Asset Channels Requests Downloads Status”, “No usage in”, “Storage”, “Important”.",
       "provenance": "pack Digital Asset Management DAM.pdf, page 71 §Display"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The asset usage performance list; the counts above it resolve separately.",
   "error": "Could not load. Names which read failed and leaves the asset usage performance untouched.",
   "emptyFirstRun": "No asset usage performance yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the asset usage performance are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "entryState": {
   "preloaded": [
    "Assets Used",
    "Asset Requests",
    "Downloads",
    "impressions",
    "requests",
    "delivery volume"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P13 Venue CMS.dc.html#cms-099"
  },
  "apisNote": "Regenerated 9 September 2026 from Digital Asset Management DAM.pdf page 71. 0 of 3 labels bound to a contract property; 8 of 28 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "CMS-100",
  "name": "Distribution Intelligence, AI Insights & Optimization",
  "module": "Media Library",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Digital Asset Management DAM.pdf",
   "board": "4",
   "number": "10",
   "page": 73
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/media-library/distribution-intelligence-ai-insights-optimization-cms-100",
   "component": "apps/venue-management-web/src/routes/media-library/DistributionIntelligenceAiInsightsOptimization.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "CMS-091"
   ],
   "exitTo": [
    "CMS-091"
   ],
   "transitions": [
    {
     "to": "CMS-091",
     "trigger": "Back to Asset Distribution & Delivery Command Center",
     "provenance": "structural — pack board 4 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Select DAM Asset) and no display directory — it is settings, not a population",
  "purpose": "Provide intelligent recommendations across DAM distribution, usage, delivery, replacements, and integrations.",
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
       "provenance": "pack Digital Asset Management DAM.pdf, page 73 §Select DAM Asset"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The distribution intelligence insights configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the distribution intelligence insights untouched.",
   "emptyFirstRun": "No distribution intelligence insights configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P13 Venue CMS.dc.html#cms-100"
  },
  "apisNote": "Regenerated 9 September 2026 from Digital Asset Management DAM.pdf page 73. 0 of 0 labels bound to a contract property; 1 of 152 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
{}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{}
```
