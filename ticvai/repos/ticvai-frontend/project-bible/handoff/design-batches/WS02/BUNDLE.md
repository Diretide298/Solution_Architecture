# WS02 — Access Control board 2

**10 screens · 16 operations · 16 schemas · 4 permissions**

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

- **Every control that can be refused must be gated.** 4 permissions apply here:
  `ACCESS_POINT_CONFIGURE, PRODUCT_CONFIGURE, PRODUCT_VIEW, SCOPE_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `BO-154` | Access Rule Command Center | commandCentre | 3 | 0 | — |
| `BO-155` | Visual Access Rule Builder | listDetail | 1 | 0 | — |
| `BO-156` | Entry, Exit & Re-entry Rules | listDetail | 3 | 0 | — |
| `BO-157` | Anti-Passback & Journey Sequence | configEditor | 1 | 0 | — |
| `BO-158` | Access Validity & Time Rules | configEditor | 3 | 3 | — |
| `BO-159` | Entitlement Consumption Engine | listDetail | 2 | 0 | — |
| `BO-160` | Multi-Park & Crossover Rules | listDetail | 3 | 0 | — |
| `BO-161` | Guest, Companion & Eligibility Rules | configEditor | 3 | 1 | — |
| `BO-162` | Group Admission & Quantity Validation | listDetail | 1 | 0 | — |
| `BO-163` | Rule Simulation, Conflict Check & Publication | listDetail | 1 | 0 | — |

## Thin screens in this batch

**BO-155, BO-156, BO-157, BO-160, BO-162 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "BO-154",
  "name": "Access Rule Command Center",
  "module": "Access & Venue",
  "requiresModule": "access",
  "wave": 3,
  "source": {
   "pack": "Access Control Module_Reference.pdf",
   "board": "2",
   "number": "2.1",
   "page": 17
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/access-rule-command-center-bo-154",
   "component": "apps/venue-management-web/src/routes/access-venue/AccessRuleCommandCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-100"
   ],
   "exitTo": [
    "BO-100",
    "BO-155",
    "BO-156",
    "BO-157",
    "BO-158",
    "BO-159",
    "BO-160",
    "BO-161",
    "BO-162",
    "BO-163"
   ],
   "inferred": false,
   "notes": "**The board's hub.** The workshop specified this module as boards of ten and opened each with a command centre; the other nine screens are that board's detail, so they are reached from here and return here.",
   "transitions": [
    {
     "to": "BO-100",
     "trigger": "Venue Home",
     "provenance": "derived — BO-100 declares entryState.params  and BO-154 holds none of them, so the edge carries nothing and BO-100 opens cold"
    },
    {
     "to": "BO-155",
     "trigger": "Works in Visual Access Rule Builder",
     "provenance": "flow F112 step 1→2",
     "operation": "listAccessRule"
    },
    {
     "to": "BO-156",
     "trigger": "Works in Entry, Exit & Re-entry Rules",
     "provenance": "flow F112 step 3→4",
     "operation": "listAccessRule"
    },
    {
     "to": "BO-157",
     "trigger": "Works in Anti-Passback & Journey Sequence",
     "provenance": "flow F112 step 5→6",
     "operation": "listAccessRule"
    },
    {
     "to": "BO-158",
     "trigger": "Works in Access Validity & Time Rules",
     "provenance": "flow F112 step 7→8",
     "operation": "listAccessRule"
    },
    {
     "to": "BO-159",
     "trigger": "Works in Entitlement Consumption Engine",
     "provenance": "flow F112 step 9→10",
     "operation": "listAccessRule"
    },
    {
     "to": "BO-160",
     "trigger": "Works in Multi-Park & Crossover Rules",
     "provenance": "flow F112 step 11→12",
     "operation": "listAccessRule"
    },
    {
     "to": "BO-162",
     "trigger": "Works in Group Admission & Quantity Validation",
     "provenance": "flow F112 step 15→16",
     "operation": "listAccessRule"
    },
    {
     "to": "BO-163",
     "trigger": "Works in Rule Simulation, Conflict Check & Publication",
     "provenance": "flow F112 step 17→18",
     "operation": "listAccessRule"
    },
    {
     "to": "BO-161",
     "trigger": "Works in Guest, Companion & Eligibility Rules",
     "provenance": "flow F112 step 13→14",
     "operation": "listAccessRule",
     "carries": [
      "productId"
     ]
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Administrator can centrally find, understand, create, clone, modify and govern all admission rules.",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen both a metric directory (§Show) and a per-row directory (§Each rule displays) — counts over a population, then the population",
  "purpose": "Central configuration dashboard for all access and entitlement rules.",
  "layout": {
   "template": "dashboard",
   "regions": [
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "Active Access Rules",
       "provenance": "pack Access Control Module_Reference.pdf, page 17 §Show",
       "bindsTo": "AccessRuleCommandCenterViewSummary.activeAccessRules"
      },
      {
       "kind": "metricTile",
       "label": "Draft Rules",
       "provenance": "pack Access Control Module_Reference.pdf, page 17 §Show",
       "bindsTo": "AccessRuleCommandCenterViewSummary.draftRules"
      },
      {
       "kind": "metricTile",
       "label": "Scheduled Rules",
       "provenance": "pack Access Control Module_Reference.pdf, page 17 §Show",
       "bindsTo": "AccessRuleCommandCenterViewSummary.scheduledRules"
      },
      {
       "kind": "metricTile",
       "label": "Rules Pending Approval",
       "provenance": "pack Access Control Module_Reference.pdf, page 17 §Show",
       "bindsTo": "AccessRuleCommandCenterViewSummary.rulesPendingApproval"
      },
      {
       "kind": "metricTile",
       "label": "Venues Covered",
       "provenance": "pack Access Control Module_Reference.pdf, page 17 §Show",
       "bindsTo": "AccessRuleCommandCenterViewSummary.venuesCovered"
      },
      {
       "kind": "metricTile",
       "label": "Products/Tickets Covered",
       "provenance": "pack Access Control Module_Reference.pdf, page 17 §Show",
       "bindsTo": "AccessRuleCommandCenterViewSummary.productsTicketsCovered"
      },
      {
       "kind": "metricTile",
       "label": "Rules with Conflicts",
       "provenance": "pack Access Control Module_Reference.pdf, page 17 §Show",
       "bindsTo": "AccessRuleCommandCenterViewSummary.rulesWithConflicts"
      },
      {
       "kind": "metricTile",
       "label": "Rules Using Biometrics",
       "provenance": "pack Access Control Module_Reference.pdf, page 17 §Show",
       "bindsTo": "AccessRuleCommandCenterViewSummary.rulesUsingBiometrics"
      },
      {
       "kind": "metricTile",
       "label": "Rules Allowing Override",
       "provenance": "pack Access Control Module_Reference.pdf, page 17 §Show",
       "bindsTo": "AccessRuleCommandCenterViewSummary.rulesAllowingOverride"
      },
      {
       "kind": "metricTile",
       "label": "Offline-Compatible Rules",
       "provenance": "pack Access Control Module_Reference.pdf, page 17 §Show",
       "bindsTo": "AccessRuleCommandCenterViewSummary.offlineCompatibleRules"
      },
      {
       "kind": "metricTile",
       "label": "Recently Modified Rules",
       "provenance": "pack Access Control Module_Reference.pdf, page 17 §Show",
       "bindsTo": "AccessRuleCommandCenterViewSummary.recentlyModifiedRules"
      },
      {
       "kind": "metricTile",
       "label": "Upcoming Rule Changes",
       "provenance": "pack Access Control Module_Reference.pdf, page 17 §Show",
       "bindsTo": "AccessRuleCommandCenterViewSummary.upcomingRuleChanges"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "moduleTiles",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every access rule",
       "columns": [
        "Rule Applies To Location Validity Status"
       ],
       "bindsTo": "AccessRuleCommandCenterView",
       "operation": "listAccessRule",
       "provenance": "pack Access Control Module_Reference.pdf, page 17 §Each rule displays"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected access rule",
       "bindsTo": "AccessRuleCommandCenterView",
       "columns": [
        "Rule Applies To Location Validity Status"
       ],
       "notes": null,
       "provenance": "pack Access Control Module_Reference.pdf, page 17 §Each rule displays"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The access rule list; the counts above it resolve separately.",
   "error": "Could not load. Names which read failed and leaves the access rule untouched.",
   "emptyFirstRun": "No access rule yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the access rule are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listAccessRule",
    "contract": "access",
    "purpose": "Access Rule Command Center",
    "trigger": "onLoad"
   },
   {
    "operationId": "listAdmissionRules",
    "contract": "access",
    "purpose": "Every admission rule with its scope",
    "trigger": "onLoad",
    "provenance": "decided 29 September, VM close-out (venue management and configuration)"
   },
   {
    "operationId": "createAdmissionRules",
    "contract": "access",
    "purpose": "Create an access rule (admission profile)",
    "trigger": "onAction",
    "provenance": "decided 29 September, VM close-out (venue management and configuration)",
    "invalidates": [
     "listAccessRule",
     "listAdmissionRules"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-154",
   "workshopBoard": "wireframes/WS19 Access Control Board 2.dc.html#bo-154"
  },
  "apisNote": "Regenerated 9 September 2026 from Access Control Module_Reference.pdf page 17. 12 of 13 labels bound to a contract property; 13 of 27 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-155",
  "name": "Visual Access Rule Builder",
  "module": "Access & Venue",
  "requiresModule": "access",
  "wave": 3,
  "source": {
   "pack": "Access Control Module_Reference.pdf",
   "board": "2",
   "number": "2.2",
   "page": 18
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/visual-access-rule-builder-bo-155",
   "component": "apps/venue-management-web/src/routes/access-venue/VisualAccessRuleBuilder.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-154"
   ],
   "exitTo": [
    "BO-154"
   ],
   "inferred": false,
   "notes": "**Reached from BO-154, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-154",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F112 step 2→3",
     "operation": "setVisualAccessRule"
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Complex admission rules can be configured without code or vendor development.",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Provide a no-code rule engine. This is where TICVAI should become significantly easier to configure than traditional access-control systems.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Access Control Module_Reference.pdf, page 18"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Access Control Module_Reference.pdf, page 18"
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
       "provenance": "contract operation setVisualAccessRule"
      }
     ]
    },
    {
     "name": "contentBody",
     "components": [
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "setVisualAccessRule"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The visual access rule list.",
   "error": "Could not load. Names which read failed and leaves the visual access rule untouched.",
   "emptyFirstRun": "No visual access rule yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the visual access rule are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setVisualAccessRule",
    "contract": "access",
    "purpose": "Visual Access Rule Builder",
    "trigger": "onAction"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-155",
   "workshopBoard": "wireframes/WS19 Access Control Board 2.dc.html#bo-155"
  },
  "apisNote": "Regenerated 9 September 2026 from Access Control Module_Reference.pdf page 18. 0 of 0 labels bound to a contract property; 0 of 22 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-156",
  "name": "Entry, Exit & Re-entry Rules",
  "module": "Access & Venue",
  "requiresModule": "access",
  "wave": 3,
  "source": {
   "pack": "Access Control Module_Reference.pdf",
   "board": "2",
   "number": "2.3",
   "page": 19
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/entry-exit-re-entry-rules-bo-156",
   "component": "apps/venue-management-web/src/routes/access-venue/EntryExitReEntryRules.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-154"
   ],
   "exitTo": [
    "BO-154"
   ],
   "inferred": false,
   "notes": "**Reached from BO-154, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-154",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F112 step 4→5",
     "operation": "listEntryExitRule"
    }
   ]
  },
  "density": "compact",
  "purposeNote": "The complete entry → exit → re-entry lifecycle can be configured independently by ticket/product/access policy.",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Configure admission quantity and journey sequencing. The source matrix explicitly requires configurable quantities for entry, exit and same-day re-entry, anti- passback intervals, required exit before re-entry, and required entry before exit.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Access Control Module_Reference.pdf, page 19"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Access Control Module_Reference.pdf, page 19"
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
       "impliedBy": "listEntryExitRule",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Save admission rules",
       "operation": "updateAdmissionRules",
       "provenance": "contract access.yaml PUT /admission-rules/{profileId} (decided 29 September, VM close-out)"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The entry exit re-entry list.",
   "error": "Could not load. Names which read failed and leaves the entry exit re-entry untouched.",
   "emptyFirstRun": "No entry exit re-entry yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the entry exit re-entry are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listEntryExitRule",
    "contract": "access",
    "purpose": "Entry, Exit & Re-entry Rules",
    "trigger": "onLoad"
   },
   {
    "operationId": "listAdmissionRules",
    "contract": "access",
    "purpose": "The admission profiles whose entry, exit and re-entry rules are edited here",
    "trigger": "onLoad",
    "provenance": "decided 29 September, VM close-out (venue management and configuration)"
   },
   {
    "operationId": "updateAdmissionRules",
    "contract": "access",
    "purpose": "Save entry, exit and re-entry limits (maxReentries, requiresExitBeforeReentry)",
    "trigger": "onAction",
    "provenance": "decided 29 September, VM close-out (venue management and configuration)",
    "invalidates": [
     "listEntryExitRule",
     "listAdmissionRules"
    ]
   }
  ],
  "entryState": {
   "preloaded": [
    "EntryExitReEntryRulesView.entryMode"
   ],
   "params": [
    {
     "name": "profileId",
     "from": "navigation"
    }
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-156",
   "workshopBoard": "wireframes/WS19 Access Control Board 2.dc.html#bo-156"
  },
  "apisNote": "Regenerated 9 September 2026 from Access Control Module_Reference.pdf page 19. 0 of 0 labels bound to a contract property; 0 of 24 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-157",
  "name": "Anti-Passback & Journey Sequence",
  "module": "Access & Venue",
  "requiresModule": "access",
  "wave": 3,
  "source": {
   "pack": "Access Control Module_Reference.pdf",
   "board": "2",
   "number": "2.4",
   "page": 20
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/anti-passback-journey-sequence-bo-157",
   "component": "apps/venue-management-web/src/routes/access-venue/AntiPassbackJourneySequence.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-154"
   ],
   "exitTo": [
    "BO-154"
   ],
   "inferred": false,
   "notes": "**Reached from BO-154, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-154",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F112 step 6→7",
     "operation": "listAntiPassbackJourney"
    }
   ]
  },
  "density": "compact",
  "purposeNote": "The system prevents credential sharing and invalid journey sequences while allowing configurable operational exceptions.",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure required sequences such as) and no display directory — it is settings, not a population",
  "purpose": "Prevent credential sharing and impossible access sequences.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "textField",
       "label": "ENTRY → EXIT → RE-ENTRY",
       "provenance": "pack Access Control Module_Reference.pdf, page 20 §Configure required sequences such as"
      },
      {
       "kind": "textField",
       "label": "PARK A → CROSSOVER → PARK B",
       "provenance": "pack Access Control Module_Reference.pdf, page 20 §Configure required sequences such as"
      },
      {
       "kind": "textField",
       "label": "MAIN ENTRY → ATTRACTION ENTRY",
       "provenance": "pack Access Control Module_Reference.pdf, page 20 §Configure required sequences such as"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The anti-passback journey sequence configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the anti-passback journey sequence untouched.",
   "emptyFirstRun": "No anti-passback journey sequence configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listAntiPassbackJourney",
    "contract": "access",
    "purpose": "Anti-Passback & Journey Sequence",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-157",
   "workshopBoard": "wireframes/WS19 Access Control Board 2.dc.html#bo-157"
  },
  "apisNote": "Regenerated 9 September 2026 from Access Control Module_Reference.pdf page 20. 0 of 0 labels bound to a contract property; 3 of 23 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-158",
  "name": "Access Validity & Time Rules",
  "module": "Access & Venue",
  "requiresModule": "access",
  "wave": 3,
  "source": {
   "pack": "Access Control Module_Reference.pdf",
   "board": "2",
   "number": "2.5",
   "page": 21
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/access-validity-time-rules-bo-158",
   "component": "apps/venue-management-web/src/routes/access-venue/AccessValidityTimeRules.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-154"
   ],
   "exitTo": [
    "BO-154"
   ],
   "inferred": false,
   "notes": "**Reached from BO-154, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-154",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F112 step 8→9",
     "operation": "listAccessValidityTime"
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Access validity can be controlled by dates, relative periods, calendars and precise time windows.",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population",
  "purpose": "Determine when access is permitted.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "weekdays",
       "provenance": "pack Access Control Module_Reference.pdf, page 21 §Configure"
      },
      {
       "kind": "selectField",
       "label": "weekends",
       "provenance": "pack Access Control Module_Reference.pdf, page 21 §Configure"
      },
      {
       "kind": "selectField",
       "label": "peak dates",
       "provenance": "pack Access Control Module_Reference.pdf, page 21 §Configure"
      },
      {
       "kind": "selectField",
       "label": "off-peak dates",
       "provenance": "pack Access Control Module_Reference.pdf, page 21 §Configure"
      },
      {
       "kind": "selectField",
       "label": "holidays",
       "provenance": "pack Access Control Module_Reference.pdf, page 21 §Configure"
      },
      {
       "kind": "selectField",
       "label": "seasons",
       "provenance": "pack Access Control Module_Reference.pdf, page 21 §Configure"
      },
      {
       "kind": "selectField",
       "label": "event dates",
       "provenance": "pack Access Control Module_Reference.pdf, page 21 §Configure"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "From / To",
       "provenance": "pack Access Control Module_Reference.pdf, page 21 §Support"
      },
      {
       "kind": "destructiveButton",
       "label": "End of Day",
       "provenance": "pack Access Control Module_Reference.pdf, page 21 §Support"
      },
      {
       "kind": "destructiveButton",
       "label": "End of Week",
       "provenance": "pack Access Control Module_Reference.pdf, page 21 §Support"
      },
      {
       "kind": "destructiveButton",
       "label": "End of Month",
       "provenance": "pack Access Control Module_Reference.pdf, page 21 §Support"
      },
      {
       "kind": "primaryButton",
       "label": "Save admission rules",
       "operation": "updateAdmissionRules",
       "provenance": "contract access.yaml PUT /admission-rules/{profileId} (decided 29 September, VM close-out)"
      }
     ]
    }
   ]
  },
  "overlays": [
   {
    "id": "confirmEndOfDay",
    "component": "confirmDialog",
    "trigger": "End of Day",
    "body": "**End of Day on a access validity time is not reversible from this screen.** Names what it affects and what it leaves alone. The pack requires the decision to reach the audit trail, so the dialog states that it is recorded.",
    "provenance": "pack Access Control Module_Reference.pdf, page 21 §Support"
   },
   {
    "id": "confirmEndOfWeek",
    "component": "confirmDialog",
    "trigger": "End of Week",
    "body": "**End of Week on a access validity time is not reversible from this screen.** Names what it affects and what it leaves alone. The pack requires the decision to reach the audit trail, so the dialog states that it is recorded.",
    "provenance": "pack Access Control Module_Reference.pdf, page 21 §Support"
   },
   {
    "id": "confirmEndOfMonth",
    "component": "confirmDialog",
    "trigger": "End of Month",
    "body": "**End of Month on a access validity time is not reversible from this screen.** Names what it affects and what it leaves alone. The pack requires the decision to reach the audit trail, so the dialog states that it is recorded.",
    "provenance": "pack Access Control Module_Reference.pdf, page 21 §Support"
   }
  ],
  "states": {
   "loading": "The access validity time configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the access validity time untouched.",
   "emptyFirstRun": "No access validity time configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listAccessValidityTime",
    "contract": "access",
    "purpose": "Access Validity & Time Rules",
    "trigger": "onLoad"
   },
   {
    "operationId": "listAdmissionRules",
    "contract": "access",
    "purpose": "The admission profiles whose validity windows are edited here",
    "trigger": "onLoad",
    "provenance": "decided 29 September, VM close-out (venue management and configuration)"
   },
   {
    "operationId": "updateAdmissionRules",
    "contract": "access",
    "purpose": "Save the admission window (openMinutesBefore, closeMinutesAfter, maxDurationMinutes)",
    "trigger": "onAction",
    "provenance": "decided 29 September, VM close-out (venue management and configuration)",
    "invalidates": [
     "listAccessValidityTime",
     "listAdmissionRules"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-158",
   "workshopBoard": "wireframes/WS19 Access Control Board 2.dc.html#bo-158"
  },
  "apisNote": "Regenerated 9 September 2026 from Access Control Module_Reference.pdf page 21. 0 of 0 labels bound to a contract property; 11 of 25 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here. **Pack actions reconciled 29 September (VM close-out):** From / To, End of Day, End of Week, End of Month are choices sent by `updateAdmissionRules` (validity.anchor / validity.endOf once AdmissionRules gains the validity block (VM handoff)).",
  "entryState": {
   "params": [
    {
     "name": "profileId",
     "from": "navigation"
    }
   ]
  },
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
  "id": "BO-159",
  "name": "Entitlement Consumption Engine",
  "module": "Access & Venue",
  "requiresModule": "access",
  "wave": 3,
  "source": {
   "pack": "Access Control Module_Reference.pdf",
   "board": "2",
   "number": "2.6",
   "page": 22
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/entitlement-consumption-engine-bo-159",
   "component": "apps/venue-management-web/src/routes/access-venue/EntitlementConsumptionEngine.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-154"
   ],
   "exitTo": [
    "BO-154"
   ],
   "inferred": false,
   "notes": "**Reached from BO-154, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-154",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F112 step 10→11",
     "operation": "listEntitlementConsumption"
    }
   ]
  },
  "density": "compact",
  "purposeNote": "A validation event can consume the correct entitlement and immediately calculate the remaining balance.",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Determine what gets consumed when access is granted. This is critical because one credential may represent several different entitlements. The matrix specifically describes a single QR capable of carrying park admission, ride entitlement, meal voucher, coupon, photo voucher and re-entry rights.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Access Control Module_Reference.pdf, page 22"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Access Control Module_Reference.pdf, page 22"
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
       "label": "Attraction Admission",
       "provenance": "pack Access Control Module_Reference.pdf, page 22 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Voucher",
       "provenance": "pack Access Control Module_Reference.pdf, page 22 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Event",
       "provenance": "pack Access Control Module_Reference.pdf, page 22 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Experience",
       "provenance": "pack Access Control Module_Reference.pdf, page 22 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Membership benefit",
       "provenance": "pack Access Control Module_Reference.pdf, page 22 §Support"
      },
      {
       "kind": "primaryButton",
       "label": "Save consumption rule",
       "operation": "setEntitlementConsumption",
       "provenance": "contract access.yaml PUT /entitlement-consumption (decided 29 September, VM close-out)"
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
   "loading": "The entitlement consumption list.",
   "error": "Could not load. Names which read failed and leaves the entitlement consumption untouched.",
   "emptyFirstRun": "No entitlement consumption yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the entitlement consumption are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listEntitlementConsumption",
    "contract": "access",
    "purpose": "Entitlement Consumption Engine",
    "trigger": "onLoad"
   },
   {
    "operationId": "setEntitlementConsumption",
    "contract": "access",
    "purpose": "Save consumption rule",
    "trigger": "onAction"
   }
  ],
  "entryState": {
   "preloaded": [
    "EntitlementConsumptionEngineView.entitlementType"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-159",
   "workshopBoard": "wireframes/WS19 Access Control Board 2.dc.html#bo-159"
  },
  "apisNote": "Regenerated 9 September 2026 from Access Control Module_Reference.pdf page 22. 0 of 0 labels bound to a contract property; 5 of 27 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here. **Pack actions reconciled 29 September (VM close-out):** still owed by a contract change: `setEntitlementConsumption`.",
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
  "id": "BO-160",
  "name": "Multi-Park & Crossover Rules",
  "module": "Access & Venue",
  "requiresModule": "access",
  "wave": 3,
  "source": {
   "pack": "Access Control Module_Reference.pdf",
   "board": "2",
   "number": "2.7",
   "page": 23
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/multi-park-crossover-rules-bo-160",
   "component": "apps/venue-management-web/src/routes/access-venue/MultiParkCrossoverRules.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-154"
   ],
   "exitTo": [
    "BO-154"
   ],
   "inferred": false,
   "notes": "**Reached from BO-154, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-154",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F112 step 12→13",
     "operation": "listMultiParkCrossover"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Configure complex access between multiple parks/venues. The matrix specifically requires multi-park access on different days, same-day crossover, park-specific entry quantities and conditional access based on previous park admission.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Access Control Module_Reference.pdf, page 23"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Access Control Module_Reference.pdf, page 23"
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
       "impliedBy": "listMultiParkCrossover2",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Save admission rules",
       "operation": "updateAdmissionRules",
       "provenance": "contract access.yaml PUT /admission-rules/{profileId} (decided 29 September, VM close-out)"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The multi-park crossover rules list.",
   "error": "Could not load. Names which read failed and leaves the multi-park crossover rules untouched.",
   "emptyFirstRun": "No multi-park crossover rules yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the multi-park crossover rules are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listMultiParkCrossover",
    "contract": "access",
    "purpose": "Multi-Park & Crossover Rules",
    "trigger": "onLoad"
   },
   {
    "operationId": "listAdmissionRules",
    "contract": "access",
    "purpose": "The admission profiles that carry crossover rules",
    "trigger": "onLoad",
    "provenance": "decided 29 September, VM close-out (venue management and configuration)"
   },
   {
    "operationId": "updateAdmissionRules",
    "contract": "access",
    "purpose": "Save which parks a profile admits to (allowedAccessPointIds, scopePath)",
    "trigger": "onAction",
    "provenance": "decided 29 September, VM close-out (venue management and configuration)",
    "invalidates": [
     "listMultiParkCrossover2",
     "listMultiParkCrossover",
     "listAdmissionRules"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-160",
   "workshopBoard": "wireframes/WS19 Access Control Board 2.dc.html#bo-160"
  },
  "apisNote": "Regenerated 9 September 2026 from Access Control Module_Reference.pdf page 23. 0 of 0 labels bound to a contract property; 0 of 3 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "profileId",
     "from": "navigation"
    }
   ]
  },
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
  "id": "BO-161",
  "name": "Guest, Companion & Eligibility Rules",
  "module": "Access & Venue",
  "requiresModule": "access",
  "wave": 3,
  "source": {
   "pack": "Access Control Module_Reference.pdf",
   "board": "2",
   "number": "2.8",
   "page": 24
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/guest-companion-eligibility-rules-bo-161",
   "component": "apps/venue-management-web/src/routes/access-venue/GuestCompanionEligibilityRules.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-154"
   ],
   "exitTo": [
    "BO-154"
   ],
   "inferred": false,
   "notes": "**Reached from BO-154, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-154",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F112 step 14→15",
     "operation": "listGuestCompanionEligibility"
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Access rules can consider guest category, linked persons and companion requirements.",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population",
  "purpose": "Apply access conditions based on guest characteristics and relationships.",
  "gaps": [
   {
    "operation": null,
    "why": "**Seven pack categories are not age categories and are not carried** (decided 28 September, audit R275 (b): the guest categories map onto the age rules). POD, POD Companion, Nanny, VIP, Member, Staff and Accreditation are ticket, credential or entitlement types, not eligibility by age; no contract rule gives them an eligibility meaning. If the client needs one of them as an access condition, it is a new rule, not a field here.",
    "source": "pack Access Control Module_Reference.pdf, page 24 §Configure"
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
       "kind": "detailPanel",
       "label": "The age rule",
       "bindsTo": "ProductEligibilityRule",
       "columns": [
        "ProductEligibilityRule.minAgeYears",
        "ProductEligibilityRule.maxAgeYears",
        "ProductEligibilityRule.accompaniedBelowAge",
        "ProductEligibilityRule.guardianSignatureAgeFrom",
        "ProductEligibilityRule.guardianSignatureAgeTo",
        "ProductEligibilityRule.minHeightCm",
        "ProductEligibilityRule.maxHeightCm",
        "ProductEligibilityRule.heightBandsCm"
       ],
       "operation": "getProductEligibilityRule",
       "notes": "**The guest categories are the age bands** (decided 28 September, audit R275 (b)) — Infant under 3, Child 3–12, Junior 13–17, Adult 18–59, Senior 60+ (`EligibilityDeclaration.ageBand`). A product admits the bands its `minAgeYears`/`maxAgeYears` cover; height stays its own limit.",
       "provenance": "contract catalogue.yaml GET /products/{productId}/eligibility-rule"
      },
      {
       "kind": "selectField",
       "label": "Infant",
       "operation": "setProductEligibilityRule",
       "notes": "Age band infant (under 3). Admitted when the rule's age range includes it (audit R275 (b)).",
       "provenance": "contract catalogue.yaml PUT /products/{productId}/eligibility-rule"
      },
      {
       "kind": "selectField",
       "label": "Child",
       "operation": "setProductEligibilityRule",
       "notes": "Age band child (3–12). Admitted when the rule's age range includes it (audit R275 (b)).",
       "provenance": "contract catalogue.yaml PUT /products/{productId}/eligibility-rule"
      },
      {
       "kind": "selectField",
       "label": "Junior",
       "operation": "setProductEligibilityRule",
       "notes": "Age band junior (13–17). Admitted when the rule's age range includes it (audit R275 (b)).",
       "provenance": "contract catalogue.yaml PUT /products/{productId}/eligibility-rule"
      },
      {
       "kind": "selectField",
       "label": "Adult",
       "operation": "setProductEligibilityRule",
       "notes": "Age band adult (18–59). Admitted when the rule's age range includes it (audit R275 (b)).",
       "provenance": "contract catalogue.yaml PUT /products/{productId}/eligibility-rule"
      },
      {
       "kind": "selectField",
       "label": "Senior",
       "operation": "setProductEligibilityRule",
       "notes": "Age band senior (60+). Admitted when the rule's age range includes it (audit R275 (b)).",
       "provenance": "contract catalogue.yaml PUT /products/{productId}/eligibility-rule"
      },
      {
       "kind": "numberField",
       "label": "Accompanied below age",
       "operation": "setProductEligibilityRule",
       "notes": "**Child Ticket + Assigned Adult Ticket** from the pack — a guest below this age must be accompanied (`accompaniedBelowAge`) (audit R275 (b)).",
       "provenance": "contract catalogue.yaml PUT /products/{productId}/eligibility-rule"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Save age rule",
       "operation": "setProductEligibilityRule",
       "provenance": "contract catalogue.yaml PUT /products/{productId}/eligibility-rule"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The guest companion eligibility configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the guest companion eligibility untouched.",
   "emptyFirstRun": "No guest companion eligibility configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getProductEligibilityRule",
    "contract": "catalogue",
    "purpose": "A product's age, height and supervision limits",
    "trigger": "onLoad"
   },
   {
    "operationId": "setProductEligibilityRule",
    "contract": "catalogue",
    "purpose": "Set age, height and supervision limits",
    "trigger": "onAction"
   },
   {
    "operationId": "listGuestCompanionEligibility",
    "contract": "access",
    "purpose": "Guest, Companion & Eligibility Rules",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-161",
   "workshopBoard": "wireframes/WS19 Access Control Board 2.dc.html#bo-161"
  },
  "apisNote": "Regenerated 9 September 2026 from Access Control Module_Reference.pdf page 24. 0 of 0 labels bound to a contract property; 12 of 27 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "productId",
     "from": "navigation"
    }
   ]
  },
  "overlays": [
   {
    "id": "formSetProductEligibilityRule",
    "component": "modal",
    "trigger": "Save age rule",
    "body": "**Collects what `setProductEligibilityRule` sends before it is called.** The guest categories are the age bands, so the categories chosen become `minAgeYears` and `maxAgeYears`; `accompaniedBelowAge`, the guardian-signature ages, `waiverRequired`, `swimAbility` and the height limits are optional (decided 28 September, audit R275 (b)). Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "ProductEligibilityRule",
    "confirm": {
     "label": "Save age rule",
     "operation": "setProductEligibilityRule"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "minAgeYears",
      "maxAgeYears",
      "accompaniedBelowAge",
      "guardianSignatureAgeFrom",
      "guardianSignatureAgeTo",
      "minHeightCm",
      "maxHeightCm",
      "heightBandsCm",
      "waiverRequired",
      "swimAbility"
     ]
    },
    "provenance": "contract catalogue.yaml PUT /products/{productId}/eligibility-rule"
   }
  ],
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
  "id": "BO-162",
  "name": "Group Admission & Quantity Validation",
  "module": "Access & Venue",
  "requiresModule": "access",
  "wave": 3,
  "source": {
   "pack": "Access Control Module_Reference.pdf",
   "board": "2",
   "number": "2.9",
   "page": 25
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/group-admission-quantity-validation-bo-162",
   "component": "apps/venue-management-web/src/routes/access-venue/GroupAdmissionQuantityValidation.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-154"
   ],
   "exitTo": [
    "BO-154"
   ],
   "inferred": false,
   "notes": "**Reached from BO-154, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-154",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F112 step 16→17",
     "operation": "listGroupAdmissionQuantity"
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Large groups can be admitted quickly without scanning every guest individually when the configured product permits group admission.",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Handle B2B groups, school groups, tour groups and family/group tickets efficiently. The matrix specifically calls for faster admission for large B2B groups and the ability for one QR/group ticket to represent multiple admissions.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Access Control Module_Reference.pdf, page 25"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Access Control Module_Reference.pdf, page 25"
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
       "impliedBy": "listGroupAdmissionQuantity",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The group admission quantity list.",
   "error": "Could not load. Names which read failed and leaves the group admission quantity untouched.",
   "emptyFirstRun": "No group admission quantity yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the group admission quantity are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listGroupAdmissionQuantity",
    "contract": "access",
    "purpose": "Group Admission & Quantity Validation",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": []
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-162",
   "workshopBoard": "wireframes/WS19 Access Control Board 2.dc.html#bo-162"
  },
  "apisNote": "Regenerated 9 September 2026 from Access Control Module_Reference.pdf page 25. 0 of 0 labels bound to a contract property; 0 of 21 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-163",
  "name": "Rule Simulation, Conflict Check & Publication",
  "module": "Access & Venue",
  "requiresModule": "access",
  "wave": 3,
  "source": {
   "pack": "Access Control Module_Reference.pdf",
   "board": "2",
   "number": "2.10",
   "page": 26
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/rule-simulation-conflict-check-publication-bo-163",
   "component": "apps/venue-management-web/src/routes/access-venue/RuleSimulationConflictCheckPublication.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-154"
   ],
   "exitTo": [
    "BO-154"
   ],
   "inferred": false,
   "notes": "**Reached from BO-154, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation."
  },
  "density": "compact",
  "purposeNote": "Every access rule can be simulated, validated, approved, versioned, published and rolled back with a complete audit trail. Board 2 — Final Screen Structure # Backend Screen Core Responsibility 2.1 Access Rule Command Center Central access-rule management # Backend Screen Core Responsibility 2.2 Visual Access Rule Builder No-code admission logic 2.3 Entry, Exit & Re-entry Rules Admission quantities and lifecycle 2.4 Anti-Passback & Journey Sequence Sharing prevention and sequence control 2.5 Access Validity & Time Rules Dates, calendars, time and expiry 2.6 Entitlement Consumption Engine Consum",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "No access rule should reach a live gate without being tested.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Access Control Module_Reference.pdf, page 26"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Access Control Module_Reference.pdf, page 26"
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
       "label": "Rule V1.0",
       "provenance": "pack Access Control Module_Reference.pdf, page 26 §Support versioning"
      },
      {
       "kind": "secondaryButton",
       "label": "Rule V1.1",
       "provenance": "pack Access Control Module_Reference.pdf, page 26 §Support versioning"
      },
      {
       "kind": "secondaryButton",
       "label": "Rule V2.0",
       "provenance": "pack Access Control Module_Reference.pdf, page 26 §Support versioning"
      },
      {
       "kind": "publishGate",
       "label": "What publishing changes",
       "notes": "**Names what goes live, where, and from when.** A publish with no stated consequence is one somebody presses meaning to save.",
       "provenance": "authored — required by check-screens for publishRuleConflictCheck"
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
   "loading": "The rule simulation conflict list.",
   "error": "Could not load. Names which read failed and leaves the rule simulation conflict untouched.",
   "emptyFirstRun": "No rule simulation conflict yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the rule simulation conflict are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "publishRuleConflictCheck",
    "contract": "access",
    "purpose": "Rule Simulation, Conflict Check & Publication",
    "trigger": "onAction"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-163",
   "workshopBoard": "wireframes/WS19 Access Control Board 2.dc.html#bo-163"
  },
  "apisNote": "Regenerated 9 September 2026 from Access Control Module_Reference.pdf page 26. 0 of 0 labels bound to a contract property; 3 of 59 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
 "createAdmissionRules": {
  "method": "POST",
  "path": "/admission-rules",
  "contract": "access",
  "summary": "Create an admission profile",
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
  "requestBody": "AdmissionRules",
  "responds": "AdmissionRules"
 },
 "getProductEligibilityRule": {
  "method": "GET",
  "path": "/products/{productId}/eligibility-rule",
  "contract": "catalogue",
  "summary": "Who may take part: age, height, supervision",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "productId",
    "in": "path",
    "required": true
   }
  ],
  "requestBody": null,
  "responds": "ProductEligibilityRule"
 },
 "listAccessRule": {
  "method": "GET",
  "path": "/access-rule",
  "contract": "access",
  "summary": "Access Rule Command Center",
  "permission": "SCOPE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "venue",
    "in": "query",
    "required": false
   },
   {
    "name": "park",
    "in": "query",
    "required": false
   },
   {
    "name": "attraction",
    "in": "query",
    "required": false
   },
   {
    "name": "product",
    "in": "query",
    "required": false
   },
   {
    "name": "credential",
    "in": "query",
    "required": false
   },
   {
    "name": "ruleType",
    "in": "query",
    "required": false
   },
   {
    "name": "status",
    "in": "query",
    "required": false
   },
   {
    "name": "date",
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
 "listAccessValidityTime": {
  "method": "GET",
  "path": "/access-validity-time",
  "contract": "access",
  "summary": "Access Validity & Time Rules",
  "permission": "SCOPE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "AccessValidityTimeRulesView"
 },
 "listAdmissionRules": {
  "method": "GET",
  "path": "/admission-rules",
  "contract": "access",
  "summary": "List admission profiles",
  "permission": "SCOPE_VIEW",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
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
 "listAntiPassbackJourney": {
  "method": "GET",
  "path": "/anti-passback-journey",
  "contract": "access",
  "summary": "Anti-Passback & Journey Sequence",
  "permission": "SCOPE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "AntiPassbackJourneySequenceView"
 },
 "listEntitlementConsumption": {
  "method": "GET",
  "path": "/entitlement-consumption",
  "contract": "access",
  "summary": "Entitlement Consumption Engine",
  "permission": "SCOPE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "EntitlementConsumptionEngineView"
 },
 "listEntryExitRule": {
  "method": "GET",
  "path": "/entry-exit-rule",
  "contract": "access",
  "summary": "Entry, Exit & Re-entry Rules",
  "permission": "SCOPE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "EntryExitReEntryRulesView"
 },
 "listGroupAdmissionQuantity": {
  "method": "GET",
  "path": "/group-admission-quantity",
  "contract": "access",
  "summary": "Group Admission & Quantity Validation",
  "permission": "SCOPE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "GroupAdmissionQuantityValidationView"
 },
 "listGuestCompanionEligibility": {
  "method": "GET",
  "path": "/guest-companion-eligibility",
  "contract": "access",
  "summary": "Guest, Companion & Eligibility Rules",
  "permission": "SCOPE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "GuestCompanionEligibilityRulesView"
 },
 "listMultiParkCrossover": {
  "method": "GET",
  "path": "/multi-park-crossover",
  "contract": "access",
  "summary": "Multi-Park & Crossover Rules",
  "permission": "SCOPE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "MultiParkCrossoverRulesView"
 },
 "publishRuleConflictCheck": {
  "method": "PUT",
  "path": "/rule-conflict-check",
  "contract": "access",
  "summary": "Rule Simulation, Conflict Check & Publication",
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
  "requestBody": "RuleSimulationConflictCheckPublicationInput",
  "responds": "RuleSimulationConflictCheckPublicationView"
 },
 "setEntitlementConsumption": {
  "method": "PUT",
  "path": "/entitlement-consumption",
  "contract": "access",
  "summary": "Save an entitlement consumption rule",
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
  "requestBody": "EntitlementConsumptionEngineInput",
  "responds": "EntitlementConsumptionEngineView"
 },
 "setProductEligibilityRule": {
  "method": "PUT",
  "path": "/products/{productId}/eligibility-rule",
  "contract": "catalogue",
  "summary": "Set age, height and supervision limits",
  "permission": "PRODUCT_CONFIGURE",
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
    "name": "productId",
    "in": "path",
    "required": true
   }
  ],
  "requestBody": "ProductEligibilityRule",
  "responds": "ProductEligibilityRule"
 },
 "setVisualAccessRule": {
  "method": "PUT",
  "path": "/visual-access-rule",
  "contract": "access",
  "summary": "Visual Access Rule Builder",
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
  "requestBody": "VisualAccessRuleBuilderInput",
  "responds": "VisualAccessRuleBuilderView"
 },
 "updateAdmissionRules": {
  "method": "PUT",
  "path": "/admission-rules/{profileId}",
  "contract": "access",
  "summary": "Update an admission profile",
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
  "requestBody": "AdmissionRules",
  "responds": "AdmissionRules"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "AccessValidityTimeRulesView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Access Validity & Time Rules displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "ruleId": {
    "type": "string"
   },
   "validityBasis": {
    "type": "string",
    "enum": [
     "fixedRange",
     "daysAfterSale",
     "daysAfterActivation",
     "daysAfterFirstUse",
     "endOfDay",
     "endOfWeek",
     "endOfMonth",
     "endOfYear"
    ]
   },
   "dayTypes": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "weekdays",
      "weekends",
      "peakDates",
      "offPeakDates",
      "holidays",
      "seasons",
      "eventDates"
     ]
    },
    "description": "Calendar day types on which access is allowed"
   },
   "blackoutDates": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "ISO dates on which access is refused"
   },
   "name": {
    "type": "string"
   },
   "validFrom": {
    "type": "string",
    "format": "date-time"
   },
   "validTo": {
    "type": "string",
    "format": "date-time"
   },
   "validityDays": {
    "type": "integer",
    "description": "N for the relative bases"
   },
   "timeWindowStart": {
    "type": "string",
    "description": "Local time HH:MM, e.g. 09:00"
   },
   "timeWindowEnd": {
    "type": "string",
    "description": "Local time HH:MM, e.g. 13:00"
   },
   "admissionToleranceMinutes": {
    "type": "integer"
   },
   "gracePeriodMinutes": {
    "type": "integer"
   },
   "noShowExpiryMinutes": {
    "type": "integer",
    "description": "Credential expires this long after its admission/performance time if unused"
   }
  },
  "required": [
   "ruleId",
   "validityBasis"
  ]
 },
 "AdmissionRules": {
  "x-ticvai-persistence": "access.admission_rules",
  "type": "object",
  "required": [
   "id",
   "code",
   "name",
   "openMinutesBefore",
   "closeMinutesAfter"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "description": "**Server-assigned.** Ignored in a `createAdmissionRules` or `updateAdmissionRules` body; on update the profile is the one the path names.\n"
   },
   "code": {
    "type": "string",
    "maxLength": 64
   },
   "perProductRules": {
    "allOf": [
     {
      "$ref": "#/components/schemas/PerProductRuleList"
     }
    ],
    "description": "BL-059. **Transaction rules were per profile and a ticket type could not state its own.** An annual pass allowing one entry per day and a single ticket allowing one entry ever are different rules, and forcing a profile per product multiplies profiles instead.\n"
   },
   "name": {
    "type": "string",
    "maxLength": 200
   },
   "openMinutesBefore": {
    "type": "integer",
    "description": "How long before a performance validation opens."
   },
   "closeMinutesAfter": {
    "type": "integer"
   },
   "maxDurationMinutes": {
    "type": "integer",
    "nullable": true
   },
   "requiresExitBeforeReentry": {
    "type": "boolean",
    "default": false
   },
   "maxReentries": {
    "type": "integer",
    "nullable": true
   },
   "entryLimit": {
    "type": "object",
    "description": "**How many times the credential may enter** (decided 29 September, VM close-out). Pack 'Access Control Module' p.19 (BO-156, Entry, Exit & Re-entry Rules). Absent means `unlimited`.",
    "required": [
     "mode"
    ],
    "properties": {
     "mode": {
      "type": "string",
      "enum": [
       "unlimited",
       "once",
       "nTimes",
       "nPerDay",
       "nPerPeriod"
      ],
      "default": "unlimited"
     },
     "count": {
      "type": "integer",
      "minimum": 1,
      "description": "N for nTimes, nPerDay and nPerPeriod; required for those modes (`422` without it)"
     },
     "periodDays": {
      "type": "integer",
      "minimum": 1,
      "description": "The period for nPerPeriod"
     }
    }
   },
   "exitScan": {
    "type": "string",
    "enum": [
     "required",
     "optional",
     "none"
    ],
    "default": "optional",
    "description": "(decided 29 September, VM close-out) `required`: re-entry needs a recorded exit. `optional`: exits run in free rotation and headcount is inferred. `none`: the exit has no reader."
   },
   "maxExits": {
    "type": "integer",
    "minimum": 0,
    "nullable": true,
    "description": "Null is unlimited (decided 29 September, VM close-out)"
   },
   "reEntryWindowMinutes": {
    "type": "integer",
    "minimum": 1,
    "nullable": true,
    "description": "Minutes after an exit within which re-entry is allowed; null is any time the credential is valid (decided 29 September, VM close-out)"
   },
   "sameDayOnly": {
    "type": "boolean",
    "default": true,
    "description": "Re-entry only on the day of the exit (decided 29 September, VM close-out)"
   },
   "designatedAccessPointIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    },
    "description": "Re-entry only through these access points; empty is any allowed access point (decided 29 September, VM close-out)"
   },
   "validity": {
    "type": "object",
    "description": "**When the credential is valid** (decided 29 September, VM close-out). Pack 'Access Control Module' p.21 (BO-158, Access Validity & Time Rules). The admission window above still applies inside it.",
    "required": [
     "anchor"
    ],
    "properties": {
     "anchor": {
      "type": "string",
      "enum": [
       "fixedRange",
       "afterSale",
       "afterActivation",
       "afterFirstUse"
      ],
      "description": "fixedRange uses from and to; the others count days from the event"
     },
     "days": {
      "type": "integer",
      "minimum": 1,
      "description": "N days after the anchor; required unless the anchor is fixedRange"
     },
     "from": {
      "type": "string",
      "format": "date"
     },
     "to": {
      "type": "string",
      "format": "date",
      "description": "Inclusive. Must not be before from (`422`)"
     },
     "endOf": {
      "type": "string",
      "enum": [
       "day",
       "week",
       "month",
       "year"
      ],
      "nullable": true,
      "description": "Validity runs to the end of the day, week, month or year the relative period ends in"
     },
     "daysOfWeek": {
      "type": "array",
      "items": {
       "type": "string",
       "enum": [
        "mon",
        "tue",
        "wed",
        "thu",
        "fri",
        "sat",
        "sun"
       ]
      },
      "description": "Empty is every day"
     },
     "dayTypes": {
      "type": "array",
      "items": {
       "type": "string",
       "enum": [
        "peakDates",
        "offPeakDates",
        "holidays",
        "seasons",
        "eventDates"
       ]
      },
      "description": "Calendar day types on which access is allowed; empty is every day type"
     },
     "blackoutDates": {
      "type": "array",
      "items": {
       "type": "string",
       "format": "date"
      },
      "description": "Dates on which access is refused whatever else allows it"
     }
    }
   },
   "crossover": {
    "type": "object",
    "nullable": true,
    "description": "**Crossover between parks** (decided 29 September, VM close-out). Pack 'Access Control Module' p.23 (BO-160, Multi-Park & Crossover Rules); BO-220 uses the same block. Null means the profile admits to one park only.",
    "required": [
     "allowedParkOrgUnitIds"
    ],
    "properties": {
     "allowedParkOrgUnitIds": {
      "type": "array",
      "minItems": 2,
      "items": {
       "type": "string",
       "format": "uuid"
      }
     },
     "parkOrder": {
      "type": "array",
      "items": {
       "type": "string",
       "format": "uuid"
      },
      "description": "Required order of parks, if any; empty is any order"
     },
     "sameDayOnly": {
      "type": "boolean",
      "default": true
     },
     "differentDayAccess": {
      "type": "boolean",
      "default": false
     },
     "dayPattern": {
      "type": "string",
      "enum": [
       "consecutiveFromFirstScan",
       "flexibleWithinValidity"
      ],
      "default": "flexibleWithinValidity"
     },
     "maxParkEntries": {
      "type": "integer",
      "minimum": 1,
      "nullable": true,
      "description": "Null is unlimited"
     },
     "crossoverQuantity": {
      "type": "integer",
      "minimum": 1,
      "nullable": true,
      "description": "How many crossovers; null is unlimited"
     },
     "crossoverAfterTime": {
      "type": "string",
      "pattern": "^([01][0-9]|2[0-3]):[0-5][0-9]$",
      "nullable": true,
      "description": "Earliest venue-local time HH:MM a crossover is allowed"
     },
     "prerequisiteParkOrgUnitId": {
      "type": "string",
      "format": "uuid",
      "nullable": true,
      "description": "The park that must be entered first"
     },
     "reEntryAfterCrossover": {
      "type": "boolean",
      "default": false
     }
    }
   },
   "allowedAccessPointIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    },
    "description": "Empty means any access point in the venue."
   },
   "reEntryVerification": {
    "type": "string",
    "enum": [
     "credentialOnly",
     "credentialUvStamp",
     "credentialFace",
     "credentialOperator",
     "custom"
    ],
    "default": "credentialOnly",
    "description": "What a re-entering guest must show besides the credential, as `listEntryTemporaryExit` returns it (added 29 September, data-model close-out DM1)."
   },
   "ruleConditions": {
    "type": "object",
    "nullable": true,
    "description": "The visual rule builder body `setVisualAccessRule` writes: `appliesTo` (products or credential types), `conditions`, `logic` (AND / OR / NOT over the conditions), `decision` (allow, deny, referToOperator, overrideEligible) and `consequences`. **One `jsonb` column on the rule row**, read with the rule and never queried on its own; the locations stay in `access.entry_rule_point` (added 29 September, data-model close-out DM1)."
   },
   "scopePath": {
    "type": "string",
    "description": "**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `venue` scope.**"
   }
  }
 },
 "AntiPassbackJourneySequenceView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Anti-Passback & Journey Sequence displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "ruleId": {
    "type": "string"
   },
   "scope": {
    "type": "string",
    "enum": [
     "credential",
     "guest",
     "gate",
     "attraction",
     "park",
     "venue"
    ],
    "description": "Level the anti-passback check applies at"
   },
   "name": {
    "type": "string"
   },
   "windowMinutes": {
    "type": "integer",
    "description": "Anti-passback time window"
   },
   "requiredSequence": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Ordered steps, e.g. entry, exit, reEntry"
   },
   "violationResponses": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Any of deny, warning, referToOperator, requireSupervisor, allowOverride, triggerSecurityAlert"
   }
  },
  "required": [
   "ruleId",
   "scope"
  ]
 },
 "EntitlementConsumptionEngineInput": {
  "type": "object",
  "x-ticvai-persistence": "none — request only; the write configures the rules the matching View reads back (decided 29 September, VM close-out)",
  "description": "**What Entitlement Consumption Engine submits** (decided 29 September, VM close-out). The writable fields of its View; the figures the screen computes are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "required": [
   "name",
   "entitlementType"
  ],
  "properties": {
   "ruleId": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$",
    "description": "Absent creates a rule"
   },
   "name": {
    "type": "string",
    "maxLength": 200
   },
   "credentialType": {
    "type": "string",
    "description": "Credential or product type the rule applies to"
   },
   "entitlementType": {
    "type": "string",
    "enum": [
     "parkAdmission",
     "attractionAdmission",
     "ride",
     "fastPass",
     "meal",
     "voucher",
     "photo",
     "locker",
     "event",
     "experience",
     "reEntry",
     "membershipBenefit",
     "custom"
    ]
   },
   "consumptionOrder": {
    "type": "integer",
    "minimum": 1,
    "default": 1,
    "description": "Where one scan could consume several entitlements, lower is consumed first"
   },
   "consumptionPerValidation": {
    "type": "integer",
    "minimum": 1,
    "default": 1,
    "description": "Units one scan consumes"
   },
   "quantity": {
    "type": "integer",
    "minimum": 1,
    "description": "Units the entitlement carries; ignored when unlimited"
   },
   "unlimited": {
    "type": "boolean",
    "default": false
   },
   "onePerAttraction": {
    "type": "boolean",
    "default": false
   },
   "attractionIds": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Empty means every attraction the entitlement covers"
   }
  }
 },
 "EntitlementConsumptionEngineView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Entitlement Consumption Engine displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "credentialType": {
    "type": "string",
    "description": "Credential or product type the rule applies to (decided 29 September, VM close-out)"
   },
   "consumptionOrder": {
    "type": "integer",
    "minimum": 1,
    "description": "Where one scan could consume several entitlements, lower is consumed first (decided 29 September, VM close-out)"
   },
   "ruleId": {
    "type": "string"
   },
   "entitlementType": {
    "type": "string",
    "enum": [
     "parkAdmission",
     "attractionAdmission",
     "ride",
     "fastPass",
     "meal",
     "voucher",
     "photo",
     "locker",
     "event",
     "experience",
     "reEntry",
     "membershipBenefit",
     "custom"
    ]
   },
   "quantity": {
    "type": "integer",
    "description": "Quantity (the pack shows 3)"
   },
   "consumptionPerValidation": {
    "type": "integer",
    "description": "Consumption per validation (the pack shows 1)"
   },
   "name": {
    "type": "string"
   },
   "unlimited": {
    "type": "boolean",
    "description": "No quantity limit, e.g. Gold Fast Pass"
   },
   "attractionIds": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Attractions where it may be consumed"
   },
   "onePerAttraction": {
    "type": "boolean",
    "description": "At most one use per attraction"
   }
  },
  "required": [
   "ruleId",
   "entitlementType"
  ]
 },
 "EntryExitReEntryRulesView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Entry, Exit & Re-entry Rules displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "ruleId": {
    "type": "string"
   },
   "entryMode": {
    "type": "string",
    "enum": [
     "unlimited",
     "once",
     "nTimes",
     "nPerDay",
     "nPerPeriod"
    ]
   },
   "exitScan": {
    "type": "string",
    "enum": [
     "required",
     "optional"
    ],
    "description": "Optional means exits run in free rotation and headcount is inferred"
   },
   "exitMode": {
    "type": "string",
    "enum": [
     "unlimited",
     "limited"
    ]
   },
   "reEntryAllowed": {
    "type": "boolean",
    "description": "Allowed / Not Allowed"
   },
   "maximumReEntries": {
    "type": "integer",
    "description": "Maximum re-entries"
   },
   "sameDayOnly": {
    "type": "boolean",
    "description": "Same-day only"
   },
   "designatedGateRequired": {
    "type": "boolean",
    "description": "Designated gate required"
   },
   "exitRequiredFirst": {
    "type": "boolean",
    "description": "Exit required first"
   },
   "reEntryWindow": {
    "type": "integer",
    "description": "Minutes after exit within which re-entry is allowed"
   },
   "name": {
    "type": "string"
   },
   "appliesTo": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Tickets, products or access policies the rule governs"
   },
   "entryLimit": {
    "type": "integer",
    "description": "N for nTimes, nPerDay, nPerPeriod"
   },
   "entryPeriod": {
    "type": "string",
    "description": "ISO 8601 duration for nPerPeriod"
   },
   "exitLimit": {
    "type": "integer"
   }
  },
  "required": [
   "ruleId",
   "entryMode"
  ]
 },
 "GroupAdmissionQuantityValidationView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Group Admission & Quantity Validation displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "ruleId": {
    "type": "string"
   },
   "allowedGroupModes": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "entireGroup",
      "partialGroup",
      "multipleWaves",
      "leaderGuests",
      "singleQrMultiEntry",
      "individualChildTicketsUnderGroup",
      "prevalidatedB2bManifest"
     ]
    }
   },
   "name": {
    "type": "string"
   },
   "productIds": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Group products the rule covers"
   },
   "maxGroupSize": {
    "type": "integer"
   }
  },
  "required": [
   "ruleId",
   "allowedGroupModes"
  ]
 },
 "GuestCompanionEligibilityRulesView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Guest, Companion & Eligibility Rules displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "ruleId": {
    "type": "string"
   },
   "guestCategory": {
    "type": "string",
    "enum": [
     "adult",
     "child",
     "junior",
     "senior",
     "pod",
     "podCompanion",
     "nanny",
     "vip",
     "member",
     "staff",
     "accreditation",
     "customerSegment"
    ]
   },
   "name": {
    "type": "string"
   },
   "requiredCompanionCategory": {
    "type": "string",
    "description": "Category of the qualifying companion, e.g. adult"
   },
   "companionVerification": {
    "type": "string",
    "enum": [
     "linkedTicket",
     "companionBiometric"
    ]
   },
   "verifyAt": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "admission",
      "exit",
      "attraction"
     ]
    },
    "description": "Where the companion is checked (decided 29 September, VM close-out)"
   },
   "attractionIds": {
    "type": "array",
    "items": {
     "type": "string"
    }
   }
  },
  "required": [
   "ruleId",
   "guestCategory"
  ]
 },
 "MultiParkCrossoverRulesView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Multi-Park & Crossover Rules displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "ruleId": {
    "type": "string"
   },
   "allowedParks": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "allowed parks"
   },
   "parkOrder": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Required park order, if any"
   },
   "sameDayCrossover": {
    "type": "boolean",
    "description": "same-day crossover"
   },
   "differentDayAccess": {
    "type": "boolean",
    "description": "different-day access"
   },
   "numberOfParkEntries": {
    "type": "integer",
    "description": "number of park entries"
   },
   "crossoverQuantity": {
    "type": "integer",
    "description": "crossover quantity"
   },
   "crossoverTime": {
    "type": "string",
    "description": "Earliest local time HH:MM a crossover is allowed"
   },
   "prerequisitePark": {
    "type": "string",
    "description": "prerequisite park"
   },
   "reEntryAfterCrossover": {
    "type": "boolean",
    "description": "re-entry after crossover"
   },
   "name": {
    "type": "string"
   },
   "dayPattern": {
    "type": "string",
    "enum": [
     "consecutiveFromFirstScan",
     "flexibleWithinValidity"
    ]
   }
  },
  "required": [
   "ruleId",
   "allowedParks"
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
 "PerProductRuleList": {
  "type": "array",
  "x-ticvai-persistence-kind": "valueObject",
  "x-ticvai-persistence-column": "jsonb",
  "description": "**One `jsonb` column on the profile row** (`access.admission_rules.per_product_rules`). The rules are read with the profile and a rule is never queried on its own, so a child table would add a join for nothing.\n",
  "items": {
   "type": "object",
   "properties": {
    "productId": {
     "type": "string",
     "format": "uuid"
    },
    "entriesPerDay": {
     "type": "integer",
     "nullable": true
    },
    "minimumGapMinutes": {
     "type": "integer",
     "nullable": true,
     "description": "**Anti-passback in minutes rather than a boolean.** A guest leaving for lunch and returning in forty minutes is normal; the same scan twice in ten seconds is a card being passed back over a fence.\n"
    },
    "allowedAccessPointIds": {
     "type": "array",
     "items": {
      "type": "string",
      "format": "uuid"
     }
    },
    "biometricPolicy": {
     "allOf": [
      {
       "$ref": "#/components/schemas/BiometricPolicy"
      }
     ],
     "description": "BL-105, 3.2.9. **The biometric check is a property of the product, not of the venue** — memberships checked, day tickets not. It sits here rather than on the profile because `perProductRules` is already where a ticket type states its own terms, and a profile per product would multiply profiles to carry one flag.\n**Absent means `disabled`**, and `disabled` is the answer for every product until somebody chooses otherwise. **Inert while `VenueSettings.biometrics.isEnabled` is false**, so a rules profile copied to another venue cannot begin capturing faces there.\n"
    },
    "maxPassesPerBiometricIdentity": {
     "type": "integer",
     "nullable": true,
     "minimum": 1,
     "description": "BL-096, 2.14.7. **The annual-pass quota, keyed to biometric identity.** `enrolFacePass` already answers 409 where a face is on another annual pass; the constant behind that refusal was one and was invisible. **Null means unlimited** and is the answer for every product that is not an annual pass — a quota applied where nobody asked for one turns a family sharing a day ticket into a fraud alert.\n"
    }
   }
  }
 },
 "ProductEligibilityRule": {
  "type": "object",
  "x-ticvai-persistence": "catalogue.product_eligibility_rule",
  "description": "Participation limits for one product. Absent means anyone may take part, and `getProductEligibilityRule` returns that absence as this schema with every limit null, never as a `404`.",
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "productId": {
    "type": "string",
    "readOnly": true
   },
   "minAgeYears": {
    "type": "integer",
    "minimum": 0,
    "nullable": true
   },
   "maxAgeYears": {
    "type": "integer",
    "minimum": 0,
    "nullable": true
   },
   "minHeightCm": {
    "type": "integer",
    "minimum": 50,
    "maximum": 250,
    "nullable": true
   },
   "maxHeightCm": {
    "type": "integer",
    "minimum": 50,
    "maximum": 250,
    "nullable": true
   },
   "heightBandsCm": {
    "type": "array",
    "items": {
     "type": "integer"
    },
    "default": [
     120,
     140
    ],
    "description": "Band edges the guest chooses between, e.g. under 1.20 m, 1.20–1.40 m, 1.40 m and over."
   },
   "accompaniedBelowAge": {
    "type": "integer",
    "nullable": true,
    "description": "Under this age an adult must be present, e.g. 8 at the kids club."
   },
   "guardianSignatureAgeFrom": {
    "type": "integer",
    "nullable": true
   },
   "guardianSignatureAgeTo": {
    "type": "integer",
    "nullable": true,
    "description": "Ages needing a guardian's signature, e.g. 12–15 on a thrill ride."
   },
   "waiverRequired": {
    "type": "boolean",
    "default": false
   },
   "swimAbility": {
    "type": "string",
    "enum": [
     "notRequired",
     "confident"
    ],
    "default": "notRequired",
    "deprecated": true,
    "description": "**Superseded for the guest's answer** (decided 29 September, rev 3 REV3-26): the swim question is a consent, not a data field. A venue attaches *Are you able to swim?* as a consent question (`Product.consentQuestionIds`), with its own text, version and whether it is asked per person or once per booking, and the answer is a consent record. Kept so existing rules read; a new product should use a consent question instead.\n"
   },
   "refundableIfIneligibleAtGate": {
    "type": "boolean",
    "default": false
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "**The partition key** (ADR-0005). Operations write it at `venue` scope."
   }
  }
 },
 "RuleSimulationConflictCheckPublicationInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures",
  "description": "**What Rule Simulation, Conflict Check & Publication submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "step": {
    "type": "string",
    "enum": [
     "simulate",
     "validate",
     "schedule",
     "publish",
     "rollBack"
    ]
   },
   "ruleVersionId": {
    "type": "string",
    "description": "Rule version being simulated or published"
   },
   "credentialId": {
    "type": "string",
    "description": "Credential used for the virtual scan"
   },
   "accessPointId": {
    "type": "string"
   },
   "simulatedAt": {
    "type": "string",
    "format": "date-time"
   },
   "previousJourney": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Prior scans assumed for the simulation"
   },
   "decision": {
    "type": "string",
    "enum": [
     "allow",
     "deny",
     "referToOperator",
     "overrideEligible"
    ]
   },
   "decisionTrace": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Each condition checked and whether it passed"
   },
   "failedRuleId": {
    "type": "string"
   },
   "conflicts": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Conflicts found (advisory)"
   },
   "scheduledAt": {
    "type": "string",
    "format": "date-time"
   }
  },
  "required": [
   "ruleVersionId",
   "step"
  ]
 },
 "RuleSimulationConflictCheckPublicationView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Rule Simulation, Conflict Check & Publication displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "step": {
    "type": "string",
    "enum": [
     "simulate",
     "validate",
     "schedule",
     "publish",
     "rollBack"
    ]
   },
   "ruleVersionId": {
    "type": "string",
    "description": "Rule version being simulated or published"
   },
   "credentialId": {
    "type": "string",
    "description": "Credential used for the virtual scan"
   },
   "accessPointId": {
    "type": "string"
   },
   "simulatedAt": {
    "type": "string",
    "format": "date-time"
   },
   "previousJourney": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Prior scans assumed for the simulation"
   },
   "decision": {
    "type": "string",
    "enum": [
     "allow",
     "deny",
     "referToOperator",
     "overrideEligible"
    ]
   },
   "decisionTrace": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Each condition checked and whether it passed"
   },
   "failedRuleId": {
    "type": "string"
   },
   "conflicts": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Conflicts found (advisory)"
   },
   "scheduledAt": {
    "type": "string",
    "format": "date-time"
   }
  },
  "required": [
   "ruleVersionId",
   "step"
  ]
 },
 "VisualAccessRuleBuilderInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures",
  "description": "**What Visual Access Rule Builder submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "decision": {
    "type": "string",
    "enum": [
     "allow",
     "deny",
     "referToOperator",
     "overrideEligible"
    ],
    "description": "THEN"
   },
   "name": {
    "type": "string"
   },
   "ruleId": {
    "type": "string"
   },
   "logic": {
    "type": "string",
    "description": "Boolean expression combining the conditions with AND / OR / NOT"
   },
   "appliesTo": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Products or credential types (WHEN)"
   },
   "locationIds": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Venue, park, zone, attraction or gate IDs (AT)"
   },
   "conditions": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Conditions (IF), e.g. visitDate = today, remainingEntries > 0"
   },
   "consequences": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Actions performed on the decision, e.g. consumeEntry, incrementAttendance"
   }
  },
  "required": [
   "ruleId",
   "name",
   "decision"
  ]
 },
 "VisualAccessRuleBuilderView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Visual Access Rule Builder displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "decision": {
    "type": "string",
    "enum": [
     "allow",
     "deny",
     "referToOperator",
     "overrideEligible"
    ],
    "description": "THEN"
   },
   "name": {
    "type": "string"
   },
   "ruleId": {
    "type": "string"
   },
   "logic": {
    "type": "string",
    "description": "Boolean expression combining the conditions with AND / OR / NOT"
   },
   "appliesTo": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Products or credential types (WHEN)"
   },
   "locationIds": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Venue, park, zone, attraction or gate IDs (AT)"
   },
   "conditions": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Conditions (IF), e.g. visitDate = today, remainingEntries > 0"
   },
   "consequences": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Actions performed on the decision, e.g. consumeEntry, incrementAttendance"
   }
  },
  "required": [
   "ruleId",
   "name",
   "decision"
  ]
 }
}
```
