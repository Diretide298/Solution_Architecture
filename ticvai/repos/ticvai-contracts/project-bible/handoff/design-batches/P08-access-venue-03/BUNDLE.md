# P08-access-venue-03 — P08 · Access & Venue (3 of 3)

**5 screens · 12 operations · 9 schemas · 7 permissions**

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

- **Every control that can be refused must be gated.** 7 permissions apply here:
  `ORDER_CREATE, REPORT_VIEW_VENUE, RESOURCE_BOOK, RESOURCE_MANAGE, RESOURCE_VIEW, SCOPE_VIEW, TENANT_CONFIGURE`. A control nobody can use must say so,
  not sit enabled and fail.
- **6 of these operations work offline**: checkInResource, checkOutResource, getSessionManifest, getVenueSettings, listAccessPoints, reorderSessionManifest
  — and the rest do not. A surface that looks the same online and off is lying.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `BO-096` | Resource Calendar | statusTracker | 2 | 0 | — |
| `BO-097` | Check Out & Check In | configEditor | 4 | 0 | — |
| `BO-098` | Qualifications | configEditor | 1 | 0 | — |
| `BO-099` | Session Manifest | statusTracker | 2 | 0 | — |
| `BO-103` | Access & Venue | listDetail | 3 | 0 | — |

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "BO-096",
  "name": "Resource Calendar",
  "module": "Access & Venue",
  "requiresModule": "resources",
  "wave": 2,
  "implementation": {
   "app": "venue-management-web",
   "route": "/resources/calendar",
   "component": "apps/venue-management-web/src/routes/resources/ResourceCalendar.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-095"
   ],
   "exitTo": [
    "BO-097"
   ],
   "transitions": [
    {
     "to": "BO-097",
     "trigger": "The guest arrives;",
     "provenance": "flow F25 step 3→4",
     "operation": "bookResource"
    }
   ]
  },
  "notes": "CF-125. **Conflict detection before assignment is the whole point** — two bookings on one cabana is a guest arriving to find somebody in their chair, and it must be impossible rather than unlikely.",
  "density": "compact",
  "pattern": "statusTracker",
  "patternReason": "`getResourceAvailability` reads one record and nothing reads a population — the screen is about that one thing",
  "purpose": "See what is free, and book it without double-booking.",
  "layout": {
   "template": "detail",
   "regions": [
    {
     "name": "contentBody",
     "slot": "record",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected resource calendar",
       "bindsTo": "ResourceAvailability",
       "columns": [
        "ResourceAvailability.resourceId",
        "ResourceAvailability.freeWindows",
        "ResourceAvailability.blockedWindows"
       ],
       "operation": "getResourceAvailability",
       "provenance": "contract resources.yaml GET /resources/{resourceId}/availability"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Book",
       "operation": "bookResource",
       "provenance": "contract resources.yaml POST /resource-bookings"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "carried",
     "components": [
      {
       "kind": "timeline",
       "bindsTo": "ResourceAvailability",
       "notes": "Setup and teardown render as their own bands, not as part of the booking — **a 30-minute turnaround is invisible if it is drawn inside the booking**",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "primaryButton",
       "label": "Book",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "banner",
       "notes": "Conflicts, named with times. *Not available* on something a guest can see is not an answer",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "Calendar grid; today renders first",
   "error": "Could not load availability. **Do not book blind** — a booking made against a stale calendar is the double-booking this screen exists to prevent.",
   "emptyFirstRun": "Nothing booked in this window. **Free is the default state and it is worth showing plainly** — an empty calendar at a venue that takes bookings is either a quiet week or a resource nobody knows exists.",
   "emptyNoResults": "No availability in this window. The response says why — booked, setup, teardown, maintenance or closed — because **wait and look elsewhere are different answers**.",
   "emptyNoAccess": "You do not have RESOURCE_VIEW."
  },
  "apis": [
   {
    "operationId": "getResourceAvailability",
    "contract": "resources",
    "purpose": "Free windows",
    "trigger": "onLoad"
   },
   {
    "operationId": "bookResource",
    "contract": "resources",
    "purpose": "Reserve",
    "trigger": "onAction"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "resourceId",
     "from": "BO-095"
    }
   ],
   "coldEntry": "Resolves from the session; a cold arrival is the ordinary case."
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-096"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 2 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
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
  "id": "BO-097",
  "name": "Check Out & Check In",
  "module": "Access & Venue",
  "requiresModule": "resources",
  "wave": 2,
  "implementation": {
   "app": "venue-management-web",
   "route": "/resources/check-out",
   "component": "apps/venue-management-web/src/routes/resources/ResourceCheckOutForm.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-095",
    "BO-096"
   ],
   "exitTo": [
    "BO-095",
    "BO-096"
   ],
   "inferred": false,
   "notes": "**Returns to BO-095, BO-096.** Stated on 4 September: this screen declared where it is reached from and no way to leave, so whoever landed on it was stuck. The return path is the same edge travelled the other way, not a guess about the product.",
   "transitions": [
    {
     "to": "BO-096",
     "trigger": "Resource Calendar",
     "carries": [
      "resourceId"
     ],
     "provenance": "derived — BO-096 declares entryState.params resourceId, so an edge into it must carry them"
    }
   ]
  },
  "notes": "CF-125, CF-126. **The deposit is held, not taken** — a deposit taken and refunded is two transactions and a fee. **Damage routes the resource to maintenance directly**, because routing through available leaves a window where the next guest books a broken item. **The deposit operations are declared here because this screen calls them** — F25 named them at steps 4 and 5 and the screen did not, which the flow checker refused. **A step calling an operation its screen does not declare is one of the two out of step**, and in this case it was the screen.",
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the screen declares only writes (`checkOutResource`, `checkInResource`, `authoriseStoredValue`) and no read of a population — it is settings, not a list",
  "purpose": "Hand it over with a deposit, take it back, settle.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "textField",
       "label": "amount",
       "bindsTo": "Money.amount",
       "provenance": "contract resources.yaml POST /resource-bookings/{bookingId}/check-out"
      },
      {
       "kind": "textField",
       "label": "currency",
       "bindsTo": "Money.currency",
       "provenance": "contract resources.yaml POST /resource-bookings/{bookingId}/check-out"
      },
      {
       "kind": "textField",
       "label": "scale",
       "bindsTo": "Money.scale",
       "provenance": "contract resources.yaml POST /resource-bookings/{bookingId}/check-out"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Check",
       "operation": "checkOutResource",
       "provenance": "contract resources.yaml POST /resource-bookings/{bookingId}/check-out"
      },
      {
       "kind": "secondaryButton",
       "label": "Check",
       "operation": "checkInResource",
       "provenance": "contract resources.yaml POST /resource-bookings/{bookingId}/check-in"
      },
      {
       "kind": "secondaryButton",
       "label": "Authorise",
       "operation": "authoriseStoredValue",
       "provenance": "contract orders.yaml POST /stored-value/authorisations"
      },
      {
       "kind": "secondaryButton",
       "label": "Release hold",
       "operation": "relinquishStoredValue",
       "provenance": "contract orders.yaml POST /stored-value/authorisations/{authorisationId}/release"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "carried",
     "components": [
      {
       "kind": "textField",
       "label": "Condition note",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "fileUpload",
       "label": "Condition photos",
       "notes": "Taken on the way out, not only on the way back",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "primaryButton",
       "label": "Check out",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "secondaryButton",
       "label": "Check in",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The booking and its condition history",
   "error": "Could not load. **Check-out and check-in work offline** — the deposit hold reconciles on sync.",
   "emptyFirstRun": "Nothing is out. **The list a poolside attendant checks at close** — anything still here at the end of the day is a conversation.",
   "emptyNoAccess": "You do not have RESOURCE_BOOK.",
   "offline": "Queued locally. The deposit is authorised on sync, and **the condition note taken now is the only defence against a dispute later**."
  },
  "apis": [
   {
    "operationId": "checkOutResource",
    "contract": "resources",
    "purpose": "Hand over",
    "trigger": "onAction"
   },
   {
    "operationId": "checkInResource",
    "contract": "resources",
    "purpose": "Take back",
    "trigger": "onAction"
   },
   {
    "operationId": "authoriseStoredValue",
    "contract": "orders",
    "purpose": "Hold the deposit",
    "trigger": "onAction"
   },
   {
    "operationId": "relinquishStoredValue",
    "contract": "orders",
    "purpose": "Release it",
    "trigger": "onAction"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "authorisationId",
     "from": "deepLink"
    },
    {
     "name": "bookingId",
     "from": "deepLink"
    }
   ],
   "coldEntry": "**A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know whether the record moved, closed or never existed, because those are three different next actions. **The scope is resolved from the session, never from the link**: a link cannot move somebody to a venue they do not hold. Arrives with `authorisationId`, `bookingId`."
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-097"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 4 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
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
  "id": "BO-098",
  "name": "Qualifications",
  "module": "Access & Venue",
  "requiresModule": "resources",
  "wave": 2,
  "implementation": {
   "app": "venue-management-web",
   "route": "/resources/qualifications",
   "component": "apps/venue-management-web/src/routes/resources/QualificationList.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-095"
   ],
   "exitTo": [
    "BO-095"
   ],
   "inferred": false,
   "notes": "**Returns to BO-095.** Stated on 4 September: this screen declared where it is reached from and no way to leave, so whoever landed on it was stuck. The return path is the same edge travelled the other way, not a guess about the product."
  },
  "notes": "CF-125. **Expiry is the field that makes this worth having** — a certification with no expiry is one nobody renews.",
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the screen declares only writes (`setResourceQualifications`) and no read of a population — it is settings, not a list",
  "purpose": "What a person is certified to do, and until when.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "textField",
       "label": "code",
       "bindsTo": "Qualification.code",
       "provenance": "contract resources.yaml PUT /resources/{resourceId}/qualifications"
      },
      {
       "kind": "textField",
       "label": "name",
       "bindsTo": "Qualification.name",
       "provenance": "contract resources.yaml PUT /resources/{resourceId}/qualifications"
      },
      {
       "kind": "textField",
       "label": "issuedAt",
       "bindsTo": "Qualification.issuedAt",
       "provenance": "contract resources.yaml PUT /resources/{resourceId}/qualifications"
      },
      {
       "kind": "textField",
       "label": "expiresAt",
       "bindsTo": "Qualification.expiresAt",
       "provenance": "contract resources.yaml PUT /resources/{resourceId}/qualifications"
      },
      {
       "kind": "textField",
       "label": "issuer",
       "bindsTo": "Qualification.issuer",
       "provenance": "contract resources.yaml PUT /resources/{resourceId}/qualifications"
      },
      {
       "kind": "textField",
       "label": "documentAssetId",
       "bindsTo": "Qualification.documentAssetId",
       "provenance": "contract resources.yaml PUT /resources/{resourceId}/qualifications"
      },
      {
       "kind": "textField",
       "label": "scopePath",
       "bindsTo": "Qualification.scopePath",
       "provenance": "contract resources.yaml PUT /resources/{resourceId}/qualifications"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Save changes",
       "operation": "setResourceQualifications",
       "provenance": "contract resources.yaml PUT /resources/{resourceId}/qualifications"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "carried",
     "components": [
      {
       "kind": "dataTable",
       "bindsTo": "Qualification[]",
       "notes": "Sorted by expiry, not by name — **a lifeguard certificate that lapsed last month is a safety failure, not a data-quality one**",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "banner",
       "notes": "Expired qualifications held by staff on today rota",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "Qualifications with their expiry",
   "error": "Could not load.",
   "emptyFirstRun": "No qualifications recorded. **A role is not a skill** — 1.2.36 requires the check before assignment, not after.",
   "emptyNoAccess": "You do not have RESOURCE_MANAGE."
  },
  "apis": [
   {
    "operationId": "setResourceQualifications",
    "contract": "resources",
    "purpose": "Set qualifications",
    "trigger": "onAction"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "resourceId",
     "from": "BO-095"
    }
   ],
   "coldEntry": "Resolves from the session; a cold arrival is the ordinary case."
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-098"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 1 operation this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
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
  "id": "BO-099",
  "name": "Session Manifest",
  "module": "Access & Venue",
  "requiresModule": "resources",
  "wave": 2,
  "implementation": {
   "app": "venue-management-web",
   "route": "/resources/session-manifest",
   "component": "apps/venue-management-web/src/routes/resources/SessionManifest.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-096"
   ],
   "exitTo": [
    "BO-096"
   ],
   "inferred": false,
   "notes": "**Returns to BO-096.** Stated on 4 September: this screen declared where it is reached from and no way to leave, so whoever landed on it was stuck. The return path is the same edge travelled the other way, not a guess about the product.",
   "transitions": [
    {
     "to": "BO-096",
     "trigger": "Resource Calendar",
     "carries": [
      "resourceId"
     ],
     "provenance": "derived — BO-096 declares entryState.params resourceId, so an edge into it must carry them"
    }
   ]
  },
  "notes": "CF-125, CF-129. Distinct from duration, which variants already handle.",
  "density": "compact",
  "pattern": "statusTracker",
  "patternReason": "`getSessionManifest` reads one record and nothing reads a population — the screen is about that one thing",
  "purpose": "Who is in a session, in what order.",
  "layout": {
   "template": "detail",
   "regions": [
    {
     "name": "contentBody",
     "slot": "record",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected session manifest",
       "bindsTo": "SessionParticipant",
       "columns": [
        "SessionParticipant.id",
        "SessionParticipant.sessionId",
        "SessionParticipant.subjectId",
        "SessionParticipant.position",
        "SessionParticipant.experienceLevel",
        "SessionParticipant.packageName",
        "SessionParticipant.notes",
        "SessionParticipant.hasSignedWaiver"
       ],
       "operation": "getSessionManifest",
       "provenance": "contract resources.yaml GET /sessions/{sessionId}/manifest"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Reorder",
       "operation": "reorderSessionManifest",
       "provenance": "contract resources.yaml PUT /sessions/{sessionId}/manifest"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "carried",
     "components": [
      {
       "kind": "dataTable",
       "bindsTo": "SessionParticipant[]",
       "notes": "Drag to reorder. **The running order is operational** — an instructor takes beginners first, and booking order puts one between two advanced riders",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "banner",
       "notes": "Unsigned waivers, named. **An instructor about to start does not want to discover one at the water edge**",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "Participants in running order",
   "error": "Could not load the manifest.",
   "emptyFirstRun": "Nobody booked into this session yet.",
   "emptyNoResults": "No participants match.",
   "emptyNoAccess": "You do not have RESOURCE_VIEW.",
   "offline": "The cached manifest. **An instructor at the water edge needs this more than anyone**, and that is where the signal is worst."
  },
  "apis": [
   {
    "operationId": "getSessionManifest",
    "contract": "resources",
    "purpose": "The manifest",
    "trigger": "onLoad"
   },
   {
    "operationId": "reorderSessionManifest",
    "contract": "resources",
    "purpose": "Change the order",
    "trigger": "onAction"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "sessionId",
     "from": "session"
    }
   ],
   "coldEntry": "Resolves from the session; a cold arrival is the ordinary case."
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-099"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 2 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
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
  "id": "BO-103",
  "name": "Access & Venue",
  "module": "Access & Venue",
  "requiresModule": "core",
  "wave": 1,
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue",
   "component": "apps/venue-management-web/src/routes/home/AccessVenueList.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-100"
   ],
   "exitTo": [
    "BO-001",
    "BO-002",
    "BO-003",
    "BO-004",
    "BO-005",
    "BO-006",
    "BO-030",
    "BO-031",
    "BO-032",
    "BO-033",
    "BO-034",
    "BO-035",
    "BO-038",
    "BO-069",
    "BO-071",
    "BO-072",
    "BO-092",
    "BO-093",
    "BO-094",
    "BO-095",
    "BO-096",
    "BO-097",
    "BO-098",
    "BO-099"
   ],
   "transitions": [
    {
     "to": "BO-001",
     "trigger": "Queue Directory",
     "carries": [
      "eventId",
      "feedId",
      "queueId"
     ],
     "provenance": "derived — BO-001 declares entryState.params eventId, feedId, queueId, so an edge into it must carry them"
    },
    {
     "to": "BO-002",
     "trigger": "Queue Configuration",
     "carries": [
      "performanceId",
      "queueId"
     ],
     "provenance": "derived — BO-002 declares entryState.params performanceId, queueId, so an edge into it must carry them"
    },
    {
     "to": "BO-003",
     "trigger": "Queue Integration Setup",
     "carries": [
      "feedId",
      "orderId",
      "venueId"
     ],
     "provenance": "derived — BO-003 declares entryState.params feedId, orderId, venueId, so an edge into it must carry them"
    },
    {
     "to": "BO-004",
     "trigger": "Manual Wait Time Entry",
     "carries": [
      "queueId",
      "refundId"
     ],
     "provenance": "derived — BO-004 declares entryState.params queueId, refundId, so an edge into it must carry them"
    },
    {
     "to": "BO-005",
     "trigger": "Queue Monitor",
     "carries": [
      "campaignId",
      "queueId"
     ],
     "provenance": "derived — BO-005 declares entryState.params campaignId, queueId, so an edge into it must carry them"
    },
    {
     "to": "BO-006",
     "trigger": "Parking Configuration",
     "carries": [
      "accessPointId"
     ],
     "provenance": "derived — BO-006 declares entryState.params accessPointId, so an edge into it must carry them"
    },
    {
     "to": "BO-030",
     "trigger": "Work Order Verification",
     "carries": [
      "venueId",
      "workOrderId"
     ],
     "provenance": "derived — BO-030 declares entryState.params venueId, workOrderId, so an edge into it must carry them"
    },
    {
     "to": "BO-031",
     "trigger": "Asset Register",
     "carries": [
      "assetId",
      "venueId"
     ],
     "provenance": "derived — BO-031 declares entryState.params assetId, venueId, so an edge into it must carry them"
    },
    {
     "to": "BO-032",
     "trigger": "Admission Profiles",
     "carries": [
      "profileId"
     ],
     "provenance": "derived — BO-032 declares entryState.params profileId, so an edge into it must carry them"
    },
    {
     "to": "BO-033",
     "trigger": "Blacklist Management",
     "carries": [
      "mediaCode"
     ],
     "provenance": "derived — BO-033 declares entryState.params mediaCode, so an edge into it must carry them"
    },
    {
     "to": "BO-038",
     "trigger": "Reconciliation Queue",
     "carries": [
      "queueId"
     ],
     "provenance": "derived — BO-038 declares entryState.params queueId, so an edge into it must carry them"
    },
    {
     "to": "BO-069",
     "trigger": "Asset Register",
     "carries": [
      "assetId",
      "gameId"
     ],
     "provenance": "derived — BO-069 declares entryState.params assetId, gameId, so an edge into it must carry them"
    },
    {
     "to": "BO-071",
     "trigger": "Planned Maintenance",
     "carries": [
      "roleId"
     ],
     "provenance": "derived — BO-071 declares entryState.params roleId, so an edge into it must carry them"
    },
    {
     "to": "BO-072",
     "trigger": "Incident Log",
     "carries": [
      "incidentId"
     ],
     "provenance": "derived — BO-072 declares entryState.params incidentId, so an edge into it must carry them"
    },
    {
     "to": "BO-093",
     "trigger": "Map Import & Labelling",
     "carries": [
      "mapId"
     ],
     "provenance": "derived — BO-093 declares entryState.params mapId, so an edge into it must carry them"
    },
    {
     "to": "BO-094",
     "trigger": "Map Editor & Publish",
     "carries": [
      "mapId",
      "pathId"
     ],
     "provenance": "derived — BO-094 declares entryState.params mapId, pathId, so an edge into it must carry them"
    },
    {
     "to": "BO-096",
     "trigger": "Resource Calendar",
     "carries": [
      "resourceId"
     ],
     "provenance": "derived — BO-096 declares entryState.params resourceId, so an edge into it must carry them"
    },
    {
     "to": "BO-097",
     "trigger": "Check Out & Check In",
     "carries": [
      "authorisationId",
      "bookingId"
     ],
     "provenance": "derived — BO-097 declares entryState.params authorisationId, bookingId, so an edge into it must carry them"
    },
    {
     "to": "BO-098",
     "trigger": "Qualifications",
     "carries": [
      "resourceId"
     ],
     "provenance": "derived — BO-098 declares entryState.params resourceId, so an edge into it must carry them"
    },
    {
     "to": "BO-099",
     "trigger": "Session Manifest",
     "carries": [
      "sessionId"
     ],
     "provenance": "derived — BO-099 declares entryState.params sessionId, so an edge into it must carry them"
    }
   ]
  },
  "notes": "Section landing. **24 screens reach the entry point through here** — before 20 August they reached it through nothing. **Given its section's own operations on 4 September.** It sat on `getVenueSettings` alone, which made it identical to every other section landing page — a hub that shows nothing of its section is a menu item, not a screen.",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listAccessPoints` reads the population and `getVenueSettings` reads one of them — list, select, act",
  "purpose": "Everything in access & venue, and what in it needs attention.",
  "gaps": [
   {
    "operation": "listScans",
    "why": "**1 declared operation reach no component on this screen**: listScans. Either the screen is missing what calls them, or the declaration is residue.",
    "source": "the screen's own declarations"
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
       "label": "Every access venue",
       "bindsTo": "AccessPoint",
       "columns": [
        "AccessPoint.id",
        "AccessPoint.code",
        "AccessPoint.name",
        "AccessPoint.venueId",
        "AccessPoint.scopePath",
        "AccessPoint.externalCredentialSources",
        "AccessPoint.scanAnomalyRules",
        "AccessPoint.operatingMode",
        "AccessPoint.vehicleLocationCapture",
        "AccessPoint.mode",
        "AccessPoint.direction",
        "AccessPoint.antiPassbackEnabled"
       ],
       "operation": "listAccessPoints",
       "provenance": "contract access.yaml GET /access-points"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected access venue",
       "bindsTo": "VenueSettings",
       "columns": [
        "VenueSettings.id",
        "VenueSettings.venueId",
        "VenueSettings.supportHours",
        "VenueSettings.quietHours",
        "VenueSettings.segregatedAccess",
        "VenueSettings.alerting"
       ],
       "operation": "getVenueSettings",
       "provenance": "contract tenancy.yaml GET /venues/{venueId}/settings"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "carried",
     "components": [
      {
       "kind": "cardList",
       "bindsTo": "screens",
       "notes": "24 screens, each with what needs attention.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "searchField",
       "label": "Search access & venue",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The list, with counts.",
   "error": "Could not load. Venue Home is still reachable.",
   "emptyFirstRun": "**Nothing configured in access & venue yet.** The action is the first thing to set up, not a blank list.",
   "emptyNoResults": "Nothing matches the filter.",
   "emptyNoAccess": "You do not have permission for access & venue. **Said plainly** — an empty section reads as broken."
  },
  "apis": [
   {
    "operationId": "getVenueSettings",
    "contract": "tenancy",
    "purpose": "What is enabled here",
    "trigger": "onLoad"
   },
   {
    "operationId": "listAccessPoints",
    "contract": "access",
    "purpose": "Gates and lanes in this venue",
    "trigger": "onLoad"
   },
   {
    "operationId": "listScans",
    "contract": "access",
    "purpose": "Admissions as they happen",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "venueId",
     "from": "session"
    }
   ],
   "coldEntry": "**Resolves from the session, so a cold arrival is the ordinary case** — a manager bookmarks the back office and opens it every morning. A principal with more than one venue is asked which before the page renders, rather than shown the first one.",
   "preloaded": [
    "VenueSettings.id",
    "VenueSettings.venueId",
    "VenueSettings.supportHours",
    "VenueSettings.quietHours",
    "VenueSettings.segregatedAccess"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-103"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 3 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
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
 "authoriseStoredValue": {
  "method": "POST",
  "path": "/stored-value/authorisations",
  "contract": "orders",
  "summary": "Hold a balance on any stored-value instrument",
  "permission": "ORDER_CREATE",
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
  "responds": "StoredValueAuthorisation"
 },
 "bookResource": {
  "method": "POST",
  "path": "/resource-bookings",
  "contract": "resources",
  "summary": "Reserve a specific resource for a window",
  "permission": "RESOURCE_BOOK",
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
  "responds": "ResourceBooking"
 },
 "checkInResource": {
  "method": "POST",
  "path": "/resource-bookings/{bookingId}/check-in",
  "contract": "resources",
  "summary": "Take it back, and settle the deposit",
  "permission": "RESOURCE_BOOK",
  "offlineCapable": true,
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
  "responds": "ResourceBooking"
 },
 "checkOutResource": {
  "method": "POST",
  "path": "/resource-bookings/{bookingId}/check-out",
  "contract": "resources",
  "summary": "Hand it over, with a deposit against it",
  "permission": "RESOURCE_BOOK",
  "offlineCapable": true,
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
  "responds": "ResourceBooking"
 },
 "getResourceAvailability": {
  "method": "GET",
  "path": "/resources/{resourceId}/availability",
  "contract": "resources",
  "summary": "When it is free, with conflicts already resolved",
  "permission": "RESOURCE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "from",
    "in": "query",
    "required": true
   },
   {
    "name": "to",
    "in": "query",
    "required": true
   }
  ],
  "requestBody": null,
  "responds": "ResourceAvailability"
 },
 "getSessionManifest": {
  "method": "GET",
  "path": "/sessions/{sessionId}/manifest",
  "contract": "resources",
  "summary": "Who is in a session, in what order",
  "permission": "RESOURCE_VIEW",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "SessionParticipant"
 },
 "getVenueSettings": {
  "method": "GET",
  "path": "/venues/{venueId}/settings",
  "contract": "tenancy",
  "summary": "Operational settings for this venue",
  "permission": "TENANT_CONFIGURE",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "VenueSettings"
 },
 "listAccessPoints": {
  "method": "GET",
  "path": "/access-points",
  "contract": "access",
  "summary": "List access points",
  "permission": "SCOPE_VIEW",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "venueId",
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
 "listScans": {
  "method": "GET",
  "path": "/access/scans",
  "contract": "access",
  "summary": "List scan events",
  "permission": "REPORT_VIEW_VENUE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "accessPointId",
    "in": "query",
    "required": null
   },
   {
    "name": "ticketId",
    "in": "query",
    "required": null
   },
   {
    "name": "outcome",
    "in": "query",
    "required": null
   },
   {
    "name": "recordedFrom",
    "in": "query",
    "required": null
   },
   {
    "name": "recordedTo",
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
 "relinquishStoredValue": {
  "method": "POST",
  "path": "/stored-value/authorisations/{authorisationId}/release",
  "contract": "orders",
  "summary": "Give a hold back",
  "permission": "ORDER_CREATE",
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
  "responds": "StoredValueAuthorisation"
 },
 "reorderSessionManifest": {
  "method": "PUT",
  "path": "/sessions/{sessionId}/manifest",
  "contract": "resources",
  "summary": "Change the running order",
  "permission": "RESOURCE_BOOK",
  "offlineCapable": true,
  "conflictPolicy": "lastWriterWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "SessionParticipant"
 },
 "setResourceQualifications": {
  "method": "PUT",
  "path": "/resources/{resourceId}/qualifications",
  "contract": "resources",
  "summary": "What a person resource is certified to do, and until when",
  "permission": "RESOURCE_MANAGE",
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
  "responds": "Qualification"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
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
 "Qualification": {
  "type": "object",
  "x-ticvai-persistence": "resources.qualification",
  "description": "1.2.36. **A role is not a skill**, and the check happens before assignment rather than after.\n",
  "required": [
   "code",
   "name"
  ],
  "properties": {
   "code": {
    "type": "string"
   },
   "name": {
    "type": "string"
   },
   "issuedAt": {
    "type": "string",
    "format": "date",
    "nullable": true
   },
   "expiresAt": {
    "type": "string",
    "format": "date",
    "nullable": true,
    "description": "**The field that makes this worth having.** A certification with no expiry is one nobody renews, and a lifeguard certificate that lapsed last month is a safety failure rather than a data-quality one.\n"
   },
   "issuer": {
    "type": "string",
    "nullable": true
   },
   "documentAssetId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "scopePath": {
    "type": "string",
    "description": "**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `venue` scope.**"
   }
  }
 },
 "ResourceAvailability": {
  "type": "object",
  "description": "**Free windows, with setup and teardown already subtracted.** A client computing this from bookings will forget the turnaround.\n",
  "properties": {
   "resourceId": {
    "type": "string",
    "format": "uuid"
   },
   "freeWindows": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "from": {
       "type": "string",
       "format": "date-time"
      },
      "to": {
       "type": "string",
       "format": "date-time"
      }
     }
    }
   },
   "blockedWindows": {
    "type": "array",
    "description": "**With a reason, because they are not the same.** Booked and under repair need different responses from an operator looking for something free — wait, or look elsewhere.\n",
    "items": {
     "type": "object",
     "properties": {
      "from": {
       "type": "string",
       "format": "date-time"
      },
      "to": {
       "type": "string",
       "format": "date-time"
      },
      "reason": {
       "type": "string",
       "enum": [
        "booked",
        "setup",
        "teardown",
        "maintenance",
        "blackout",
        "closed"
       ]
      }
     }
    }
   }
  }
 },
 "ResourceBooking": {
  "type": "object",
  "x-ticvai-persistence": "resources.booking",
  "required": [
   "id",
   "resourceId",
   "from",
   "to",
   "status"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "resourceId": {
    "type": "string",
    "format": "uuid"
   },
   "subjectId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "orderId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "from": {
    "type": "string",
    "format": "date-time"
   },
   "to": {
    "type": "string",
    "format": "date-time"
   },
   "status": {
    "type": "string",
    "enum": [
     "reserved",
     "checkedOut",
     "returned",
     "overdue",
     "cancelled",
     "noShow"
    ]
   },
   "recurrenceGroupId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Ties the occurrences of a recurring booking. **Cancelling one week does not cancel the series**, and cancelling the series is a separate act with a separate confirmation.\n"
   },
   "depositAuthorisationId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The hold, through `orders.authoriseStoredValue` (CF-126). **A deposit taken and refunded is two transactions and a fee; held and released is neither.**\n"
   },
   "checkedOutAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "dueBackAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "returnedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "conditionOut": {
    "type": "string",
    "nullable": true
   },
   "conditionIn": {
    "type": "string",
    "nullable": true
   }
  }
 },
 "SessionParticipant": {
  "type": "object",
  "x-ticvai-persistence": "resources.session_participant",
  "description": "1.3.44. **The running order is operational.** An instructor takes beginners first, and a manifest sorted by booking time puts one between two advanced riders.\n",
  "required": [
   "id",
   "sessionId",
   "subjectId",
   "position"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "sessionId": {
    "type": "string",
    "format": "uuid"
   },
   "subjectId": {
    "type": "string",
    "format": "uuid"
   },
   "position": {
    "type": "integer"
   },
   "experienceLevel": {
    "type": "string",
    "enum": [
     "firstTime",
     "beginner",
     "intermediate",
     "advanced"
    ],
    "nullable": true
   },
   "packageName": {
    "type": "string",
    "nullable": true
   },
   "notes": {
    "type": "string",
    "nullable": true
   },
   "hasSignedWaiver": {
    "type": "boolean",
    "readOnly": true,
    "description": "2.15.9. **Shown on the manifest because that is where it is acted on** — an instructor about to start does not want to discover an unsigned waiver at the water's edge.\n"
   }
  }
 },
 "StoredValueAuthorisation": {
  "type": "object",
  "x-ticvai-persistence": "orders.stored_value_authorisation",
  "description": "A hold against any stored-value instrument. **Two-phase by necessity, not by preference** — an arcade machine, a kitchen and a gate all take time between committing to a spend and knowing it succeeded, and a balance that cannot be held is a balance that gets double-spent or refunded by hand.\n",
  "required": [
   "id",
   "kind",
   "instrumentId",
   "amount",
   "status"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "kind": {
    "$ref": "#/components/schemas/StoredValueKind"
   },
   "instrumentId": {
    "type": "string",
    "format": "uuid",
    "description": "The wallet, card, voucher or position being held against."
   },
   "amount": {
    "$ref": "#/components/schemas/Money"
   },
   "status": {
    "type": "string",
    "enum": [
     "held",
     "partiallyCaptured",
     "captured",
     "released",
     "expired"
    ],
    "description": "**Mirrors `cross-region.WalletAuthorisation` exactly**, which is the point — one lifecycle rather than six.\n"
   },
   "capturedAmount": {
    "$ref": "#/components/schemas/Money"
   },
   "expiresAt": {
    "type": "string",
    "format": "date-time",
    "description": "**Released automatically.** A hold nobody releases is a guest whose balance is short with no explanation, and the arcade is where that happens most.\n"
   },
   "reference": {
    "type": "string",
    "description": "What the hold is for — an order, a play, a table visit."
   },
   "scopePath": {
    "type": "string",
    "description": "**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `venue` scope.**"
   }
  }
 },
 "StoredValueKind": {
  "type": "string",
  "description": "**Six things in this package hold a balance and behave the same way** — a wallet, a gift card, a game card, a voucher, a loyalty position and a prepaid entitlement. They were built separately across three sessions and each grew its own balance, bonus balance, status, blocked reason and expiry (CF-126).\n**The concern is not tidiness. Only one of the six could hold an authorisation.** `authoriseWalletSpend` / `captureWalletAuthorisation` / `relinquishWalletAuthorisation` gave two-phase spend to the retail wallet alone, so **a guest with 200 game credits starting a play the machine then failed had no held balance** — the credits were either taken or not, with no third state.\nThe entities stay distinct because their lifecycles genuinely differ — a gift card activates at a till, a loyalty position never expires the same way. **What is shared is the spend mechanism**, and this enum is what lets it be shared.\n",
  "enum": [
   "wallet",
   "giftCard",
   "gameCard",
   "voucher",
   "loyalty",
   "prepaidEntitlement"
  ]
 },
 "VenueSettings": {
  "type": "object",
  "x-ticvai-persistence": "platform.venue_settings",
  "description": "**Venue-level operational configuration that no other level can answer.**\nRegion owns currency, tax regime and fiscal year (ADR-0011). Venue owns the things that vary between two venues in one region — **opening hours, support hours, and what the local law requires of the gate.**\n",
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "description": "**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"
   },
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "supportHours": {
    "type": "object",
    "description": "CF-100. **A venue decides whether its support desk is 24/7 or bounded, and the platform does not.** This was recorded as an open question for eleven days and was never one — the code is identical either way, and what was missing was somewhere to put the answer.\n",
    "properties": {
     "mode": {
      "type": "string",
      "enum": [
       "alwaysOn",
       "businessHours",
       "custom",
       "none"
      ]
     },
     "timezone": {
      "type": "string"
     },
     "windows": {
      "type": "array",
      "items": {
       "type": "object",
       "properties": {
        "day": {
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
        "from": {
         "type": "string"
        },
        "to": {
         "type": "string"
        }
       }
      }
     },
     "outOfHoursMessage": {
      "type": "string",
      "nullable": true
     }
    }
   },
   "quietHours": {
    "type": "object",
    "nullable": true,
    "description": "**When the platform does not send.** A wallet low-balance alert at 3am is a complaint, and journeys and message triggers both respect this.\n**Operational messages ignore it** — a queue-turn alert is why a guest is holding the phone.\n",
    "properties": {
     "from": {
      "type": "string"
     },
     "to": {
      "type": "string"
     }
    }
   },
   "segregatedAccess": {
    "type": "object",
    "nullable": true,
    "description": "CF-130. **Configured at venue level because it changes by region and the venue is where it is known** — a Ladies Night, a family session, a prayer-time closure.\n**The platform does not infer gender.** 3.2.45 asks for automatic gender recognition and 3.2.46 for rule-based facial recognition validation, and neither is built. Two reasons, and the second is the one that decided it:\n**A Ladies Night ticket is already gendered at the point of sale**, so the gate checks the entitlement the platform issued rather than the face in front of it — deterministic, auditable, and already contracted through `admissionRules`.\n**And these events are staffed.** A steward at the entrance is making the judgment anyway, and a classifier that overrules a person who can see more than it can is a machine and a human disagreeing while a guest waits.\n**`genderVerification` is a switch, not an implementation.** Where a venue's access hardware offers the capability and the venue chooses to use it, this turns it on — following ADR-0015's standards-first driver model, where the device does what the device does. **Not everything needs to be built.**\n",
    "properties": {
     "isEnabled": {
      "type": "boolean",
      "default": false
     },
     "appliesToAccessPointIds": {
      "type": "array",
      "items": {
       "type": "string",
       "format": "uuid"
      }
     },
     "schedule": {
      "type": "array",
      "items": {
       "type": "object",
       "properties": {
        "day": {
         "type": "string"
        },
        "from": {
         "type": "string"
        },
        "to": {
         "type": "string"
        },
        "admits": {
         "type": "string",
         "enum": [
          "all",
          "women",
          "womenAndChildren",
          "families",
          "members"
         ]
        }
       }
      }
     },
     "entitlementGated": {
      "type": "boolean",
      "default": true,
      "readOnly": true,
      "description": "**Always true, and stated rather than assumed.** The gate admits on the entitlement. Everything below is advisory on top of that, and nothing replaces it.\n"
     },
     "genderVerification": {
      "type": "string",
      "enum": [
       false,
       "staffAssisted",
       "deviceAssisted"
      ],
      "default": false,
      "description": "`off` — the entitlement decides and a steward handles exceptions. **The default, and what is contracted.**\n`staffAssisted` — the steward's screen shows the ticket type so they can ask. No inference anywhere.\n`deviceAssisted` — **the venue's access hardware performs the check, not the platform.** Available only where the driver reports the capability, and the result is **advisory to the steward rather than decisive at the turnstile** (3.2.45 asks for rejection; this deviates deliberately).\n"
     },
     "overrideRateAlertThreshold": {
      "type": "number",
      "nullable": true,
      "description": "Where `deviceAssisted` is on. **An override rate near zero means the steward has stopped deciding**, and that is the number that says whether the human safeguard is working or decorative.\n"
     }
    }
   },
   "alerting": {
    "type": "object",
    "description": "CF-134. **On-platform notification, marked as read.** Six contracts detect their own trouble and none told a person.\n**The panel is the default and email or WhatsApp only where the matrix names them** — an operational alert that arrives by email is an alert nobody sees in time.\n",
    "properties": {
     "channel": {
      "type": "string",
      "enum": [
       "dashboardPanel",
       "dashboardAndEmail",
       "dashboardAndWhatsapp"
      ],
      "default": "dashboardPanel"
     },
     "acknowledgementRequired": {
      "type": "boolean",
      "default": true
     },
     "escalateAfterMinutes": {
      "type": "integer",
      "nullable": true
     }
    }
   }
  }
 }
}
```
