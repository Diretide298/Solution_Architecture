# P06-operations-04 — P06 · Operations (4 of 5)

**10 screens · 25 operations · 33 schemas · 9 permissions**

Platform P06 Venue Staff App · ships as **venue-staff-mobile** ·
staff audience · mobileApp ·
offline-capable

## Who this is for

**staff on mobileApp.** Everything below is how you know what is
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

- **Every control that can be refused must be gated.** 9 permissions apply here:
  `AI_USE, ANNOUNCEMENT_PUBLISH, ASSET_LIBRARY_VIEW, DEVICE_CONFIGURE, DEVICE_VIEW, ORDER_CREATE, ORDER_MODIFY, ORDER_VIEW, WORKFORCE_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **12 of these operations work offline**: acknowledgeAnnouncement, addTip, createPayment, getCurrentSession, getMediaAsset, getMediaEntitlements, listAnnouncements, listDevices
  — and the rest do not. A surface that looks the same online and off is lying.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `EMP-035` | Payment on device | configEditor | 4 | 2 | — |
| `EMP-036` | Issue media | statusTracker | 3 | 1 | — |
| `EMP-037` | Notifications | listDetail | 8 | 1 | — |
| `EMP-039` | Announcements | listDetail | 4 | 1 | — |
| `EMP-038` | Broadcast to team | listDetail | 4 | 1 | — |
| `EMP-040` | Knowledge base | configEditor | 1 | 0 | — |
| `EMP-041` | Training | listDetail | 2 | 1 | — |
| `EMP-042` | Profile | listDetail | 6 | 3 | — |
| `EMP-043` | Device settings | listDetail | 2 | 1 | — |
| `EMP-044` | Accessibility | listDetail | 0 | 0 | — |

## Thin screens in this batch

**EMP-036, EMP-041, EMP-044 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "EMP-035",
  "name": "Payment on device",
  "module": "Operations",
  "requiresModule": "ticketing",
  "wave": 2,
  "capability": "C00",
  "implementation": {
   "app": "venue-staff-app",
   "route": "/operations/payment-on-device",
   "component": "apps/venue-staff-app/src/routes/operations/PaymentOnDeviceDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "exitTo": [
    "EMP-001",
    "EMP-002",
    "EMP-003",
    "EMP-036"
   ],
   "inferred": false,
   "entryFrom": [
    "EMP-034"
   ],
   "notes": "**Reached from EMP-034** — payment follows the sale that needs it. Stated on 4 September: this screen exited to the hubs and nothing exited to it, so it was outside the navigation graph entirely.",
   "transitions": [
    {
     "to": "EMP-036",
     "trigger": "Media is issued on the spot",
     "provenance": "flow F66 step 2→3"
    },
    {
     "to": "EMP-001",
     "trigger": "Sign in",
     "provenance": "derived — EMP-001 declares entryState.params challengeId and EMP-035 holds none of them, so the edge carries nothing and EMP-001 opens cold"
    },
    {
     "to": "EMP-002",
     "trigger": "Select venue & role",
     "provenance": "derived — EMP-002 declares entryState.params  and EMP-035 holds none of them, so the edge carries nothing and EMP-002 opens cold"
    },
    {
     "to": "EMP-003",
     "trigger": "Home — on duty",
     "provenance": "derived — EMP-003 declares entryState.params incidentId and EMP-035 holds none of them, so the edge carries nothing and EMP-003 opens cold"
    }
   ]
  },
  "notes": "Definition derived from the wireframe board on 14 August. Components, states and operations still to be written. Card on a handheld. **Tender currency equals base currency** — a staff member taking payment away from a till has no float and cannot accept foreign cash.",
  "density": "comfortable",
  "pattern": "configEditor",
  "patternReason": "the screen declares only writes (`createPayment`, `inquirePaymentStatus`, `addTip`) and no read of a population — it is settings, not a list",
  "purpose": "Take a card payment on the handheld.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "textField",
       "label": "id",
       "bindsTo": "CreatePaymentRequest.id",
       "provenance": "contract orders.yaml POST /payments"
      },
      {
       "kind": "textField",
       "label": "orderId",
       "bindsTo": "CreatePaymentRequest.orderId",
       "provenance": "contract orders.yaml POST /payments"
      },
      {
       "kind": "textField",
       "label": "tender",
       "bindsTo": "CreatePaymentRequest.tender",
       "provenance": "contract orders.yaml POST /payments"
      },
      {
       "kind": "textField",
       "label": "amount",
       "bindsTo": "CreatePaymentRequest.amount",
       "provenance": "contract orders.yaml POST /payments"
      },
      {
       "kind": "textField",
       "label": "tenderedAmount",
       "bindsTo": "CreatePaymentRequest.tenderAmount",
       "provenance": "contract orders.yaml POST /payments"
      },
      {
       "kind": "textField",
       "label": "walletAuthorisationId",
       "bindsTo": "CreatePaymentRequest.walletAuthorisationId",
       "provenance": "contract orders.yaml POST /payments"
      },
      {
       "kind": "textField",
       "label": "deviceId",
       "bindsTo": "CreatePaymentRequest.deviceId",
       "provenance": "contract orders.yaml POST /payments"
      },
      {
       "kind": "textField",
       "label": "recordedAt",
       "bindsTo": "CreatePaymentRequest.recordedAt",
       "provenance": "contract orders.yaml POST /payments"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Create payment",
       "operation": "createPayment",
       "provenance": "contract orders.yaml POST /payments"
      },
      {
       "kind": "secondaryButton",
       "label": "Inquire payment status",
       "operation": "inquirePaymentStatus",
       "provenance": "contract orders.yaml POST /payments/{paymentId}/inquiry"
      },
      {
       "kind": "secondaryButton",
       "label": "Add tip",
       "operation": "addTip",
       "provenance": "contract orders.yaml POST /payments/{paymentId}/tip"
      },
      {
       "kind": "secondaryButton",
       "label": "Capture payment",
       "operation": "capturePayment",
       "provenance": "contract orders.yaml POST /payments/{paymentId}/capture"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The saved payment device.",
   "error": "Could not load. Names which read failed and leaves the payment device untouched.",
   "emptyFirstRun": "No payment device configured. The form opens empty and `createPayment` saves the first one; it says what the platform does in the meantime.",
   "emptyNoAccess": "Shown when the caller lacks `ORDER_CREATE`, which `createPayment` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "offline": "Not available for card"
  },
  "apis": [
   {
    "operationId": "createPayment",
    "contract": "orders",
    "purpose": "Take a payment against an order",
    "trigger": "onAction"
   },
   {
    "operationId": "inquirePaymentStatus",
    "contract": "orders",
    "purpose": "Ask the provider what actually happened",
    "trigger": "onAction"
   },
   {
    "operationId": "addTip",
    "contract": "orders",
    "purpose": "Record a tip against a payment",
    "trigger": "onAction"
   },
   {
    "operationId": "capturePayment",
    "contract": "orders",
    "purpose": "Capture a previously authorised payment",
    "trigger": "onAction"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "paymentId",
     "from": "deepLink"
    }
   ],
   "coldEntry": "**A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know whether the record moved, closed or never existed, because those are three different next actions. **The scope is resolved from the session, never from the link**: a link cannot move somebody to a venue they do not hold. Arrives with `paymentId`."
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P06 Venue Staff App.dc.html#emp-035"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 4 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "overlays": [
   {
    "id": "formAddTip",
    "component": "modal",
    "trigger": "Add tip",
    "body": "**Collects what `addTip` sends before it is called.** Required: `amount`, `source`, `recordedAt`. Optional: `allocateToPrincipalId`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Add tip",
     "operation": "addTip"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "amount",
      "source",
      "recordedAt",
      "allocateToPrincipalId"
     ]
    },
    "provenance": "contract orders.yaml POST /payments/{paymentId}/tip"
   },
   {
    "id": "formCapturePayment",
    "component": "modal",
    "trigger": "Capture payment",
    "body": "**Collects what `capturePayment` sends before it is called.** Required: `amount`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Capture payment",
     "operation": "capturePayment"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "amount"
     ]
    },
    "provenance": "contract orders.yaml POST /payments/{paymentId}/capture"
   }
  ],
  "_platform": {
   "code": "P06",
   "audience": "staff",
   "formFactor": "mobileApp",
   "shortName": "Venue Staff App",
   "name": "Venue Staff App — Operations",
   "app": "venue-staff-app",
   "offlineCapable": true,
   "operator": "venue",
   "targetApp": {
    "app": "venue-staff-mobile",
    "name": "TICVAI Venue Staff",
    "shell": "mobile",
    "siblings": [
     "P07"
    ],
    "note": "**Both offline-capable, both carried rather than sat at.** They cannot fold into venue management, which is online desktop web, and they share 69% with each other.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "EMP-036",
  "name": "Issue media",
  "module": "Operations",
  "requiresModule": "ticketing",
  "wave": 2,
  "capability": "C00",
  "implementation": {
   "app": "venue-staff-app",
   "route": "/operations/issue-media",
   "component": "apps/venue-staff-app/src/routes/operations/IssueMediaDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "exitTo": [
    "EMP-001",
    "EMP-002",
    "EMP-003"
   ],
   "inferred": false,
   "entryFrom": [
    "EMP-034",
    "EMP-035"
   ],
   "notes": "**Reached from EMP-034** — media is issued for the sale that bought it. Stated on 4 September: this screen exited to the hubs and nothing exited to it, so it was outside the navigation graph entirely.",
   "transitions": [
    {
     "to": "EMP-001",
     "trigger": "Sign in",
     "provenance": "derived — EMP-001 declares entryState.params challengeId and EMP-036 holds none of them, so the edge carries nothing and EMP-001 opens cold"
    },
    {
     "to": "EMP-002",
     "trigger": "Select venue & role",
     "provenance": "derived — EMP-002 declares entryState.params  and EMP-036 holds none of them, so the edge carries nothing and EMP-002 opens cold"
    },
    {
     "to": "EMP-003",
     "trigger": "Home — on duty",
     "provenance": "derived — EMP-003 declares entryState.params incidentId and EMP-036 holds none of them, so the edge carries nothing and EMP-003 opens cold"
    }
   ]
  },
  "notes": "Definition derived from the wireframe board on 14 August. Components, states and operations still to be written. **9 assets operations removed 18 August (CF-114).** The whole media contract was attached to this screen. **A till adding an item to a ticket does not manage a media library** — it reads the asset it needs and nothing else. Same shape as CF-87, one level up: that attached sibling operations, this attached a whole contract.",
  "density": "comfortable",
  "pattern": "statusTracker",
  "patternReason": "`getMediaEntitlements` reads one record and nothing reads a population — the screen is about that one thing",
  "purpose": "Give the guest something the gate can read.",
  "layout": {
   "template": "detail",
   "regions": [
    {
     "name": "contentBody",
     "slot": "record",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The media entitlements",
       "bindsTo": "MediaEntitlements",
       "columns": [
        "MediaEntitlements.mediaCode",
        "MediaEntitlements.mediaKind",
        "MediaEntitlements.subjectId",
        "MediaEntitlements.isValid",
        "MediaEntitlements.invalidReason",
        "MediaEntitlements.canAcceptMore",
        "MediaEntitlements.entitlements"
       ],
       "operation": "getMediaEntitlements",
       "provenance": "contract orders.yaml GET /media/{mediaCode}/entitlements"
      },
      {
       "kind": "detailPanel",
       "label": "The media asset",
       "bindsTo": "MediaAssetDetail",
       "columns": [
        "MediaAssetDetail.id",
        "MediaAssetDetail.kind",
        "MediaAssetDetail.status",
        "MediaAssetDetail.filename",
        "MediaAssetDetail.contentType",
        "MediaAssetDetail.sizeBytes",
        "MediaAssetDetail.title",
        "MediaAssetDetail.description",
        "MediaAssetDetail.altText",
        "MediaAssetDetail.width",
        "MediaAssetDetail.height",
        "MediaAssetDetail.durationSeconds",
        "MediaAssetDetail.customMetadata",
        "MediaAssetDetail.sharedWithTenantIds",
        "MediaAssetDetail.tags",
        "MediaAssetDetail.venueId"
       ],
       "operation": "getMediaAsset",
       "provenance": "contract assets.yaml GET /media/{mediaId}"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Append entitlement to media",
       "operation": "appendEntitlementToMedia",
       "provenance": "contract orders.yaml POST /media/{mediaCode}/entitlements"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The issue media, read by `getMediaEntitlements`.",
   "error": "Could not load. Names which read failed and leaves the issue media untouched.",
   "emptyFirstRun": "No issue media yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table.",
   "emptyNoAccess": "Shown when the caller lacks `ORDER_VIEW`, which `getMediaEntitlements` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "offline": "Issues from the local range allocated at shift start"
  },
  "apis": [
   {
    "operationId": "getMediaEntitlements",
    "contract": "orders",
    "purpose": "What is already on this media",
    "trigger": "onLoad"
   },
   {
    "operationId": "appendEntitlementToMedia",
    "contract": "orders",
    "purpose": "Add something to a ticket the guest already holds",
    "trigger": "onAction"
   },
   {
    "operationId": "getMediaAsset",
    "contract": "assets",
    "purpose": "Read an asset with derivatives and usage",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "mediaCode",
     "from": "deepLink"
    },
    {
     "name": "mediaId",
     "from": "deepLink"
    }
   ],
   "coldEntry": "**A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know whether the record moved, closed or never existed, because those are three different next actions. **The scope is resolved from the session, never from the link**: a link cannot move somebody to a venue they do not hold. Arrives with `mediaCode`, `mediaId`."
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P06 Venue Staff App.dc.html#emp-036"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 3 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "overlays": [
   {
    "id": "formAppendEntitlementToMedia",
    "component": "modal",
    "trigger": "Append entitlement to media",
    "body": "**Collects what `appendEntitlementToMedia` sends before it is called.** Required: `id`, `lines`, `recordedAt`. Optional: `paymentMethod`, `note`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "AppendEntitlementRequest",
    "confirm": {
     "label": "Append entitlement to media",
     "operation": "appendEntitlementToMedia"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "lines",
      "recordedAt",
      "paymentMethod",
      "note"
     ]
    },
    "provenance": "contract orders.yaml POST /media/{mediaCode}/entitlements"
   }
  ],
  "_platform": {
   "code": "P06",
   "audience": "staff",
   "formFactor": "mobileApp",
   "shortName": "Venue Staff App",
   "name": "Venue Staff App — Operations",
   "app": "venue-staff-app",
   "offlineCapable": true,
   "operator": "venue",
   "targetApp": {
    "app": "venue-staff-mobile",
    "name": "TICVAI Venue Staff",
    "shell": "mobile",
    "siblings": [
     "P07"
    ],
    "note": "**Both offline-capable, both carried rather than sat at.** They cannot fold into venue management, which is online desktop web, and they share 69% with each other.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "EMP-037",
  "name": "Notifications",
  "module": "Operations",
  "requiresModule": "core",
  "wave": 1,
  "capability": "C00",
  "implementation": {
   "app": "venue-staff-app",
   "route": "/operations/notifications",
   "component": "apps/venue-staff-app/src/routes/operations/NotificationsDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "exitTo": [
    "EMP-001",
    "EMP-002",
    "EMP-003"
   ],
   "inferred": false,
   "entryFrom": [
    "EMP-003"
   ],
   "notes": "**Reached from EMP-003** — the screen the device sits on between tasks. Stated on 4 September: this screen exited to the hubs and nothing exited to it, so it was outside the navigation graph entirely.",
   "transitions": [
    {
     "to": "EMP-001",
     "trigger": "Sign in",
     "provenance": "derived — EMP-001 declares entryState.params challengeId and EMP-037 holds none of them, so the edge carries nothing and EMP-001 opens cold"
    },
    {
     "to": "EMP-002",
     "trigger": "Select venue & role",
     "provenance": "derived — EMP-002 declares entryState.params  and EMP-037 holds none of them, so the edge carries nothing and EMP-002 opens cold"
    },
    {
     "to": "EMP-003",
     "trigger": "Home — on duty",
     "provenance": "derived — EMP-003 declares entryState.params incidentId and EMP-037 holds none of them, so the edge carries nothing and EMP-003 opens cold"
    }
   ]
  },
  "notes": "Definition derived from the wireframe board on 14 August. Components, states and operations still to be written.",
  "density": "comfortable",
  "pattern": "listDetail",
  "patternReason": "`listAnnouncements` reads the population and `getAnnouncementReach` reads one of them — list, select, act",
  "purpose": "Tell the right person the right thing.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "toggle",
       "label": "Unacknowledged only",
       "operation": "listAnnouncements",
       "notes": "Sends `?unacknowledgedOnly=` to `listAnnouncements`.",
       "provenance": "contract workforce.yaml GET /announcements"
      },
      {
       "kind": "dataTable",
       "label": "Every announcement",
       "bindsTo": "Announcement",
       "columns": [
        "Announcement.id",
        "Announcement.title",
        "Announcement.body",
        "Announcement.kind",
        "Announcement.venueIds",
        "Announcement.departmentIds",
        "Announcement.roleIds",
        "Announcement.requiresAcknowledgement",
        "Announcement.expiresAt",
        "Announcement.publishedByPrincipalId",
        "Announcement.publishedAt",
        "Announcement.locale"
       ],
       "operation": "listAnnouncements",
       "provenance": "contract workforce.yaml GET /announcements"
      },
      {
       "kind": "publishGate",
       "impliedBy": "publishAnnouncement",
       "notes": "Declares `publishAnnouncement`. **The gate names what the publish will affect before it happens** — a disabled Publish with no reason is the state operators escalate.\n",
       "provenance": "carried from the previous definition"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected announcement",
       "bindsTo": "Announcement",
       "columns": [
        "Announcement.id",
        "Announcement.title",
        "Announcement.body",
        "Announcement.kind",
        "Announcement.venueIds",
        "Announcement.departmentIds",
        "Announcement.roleIds",
        "Announcement.requiresAcknowledgement",
        "Announcement.expiresAt",
        "Announcement.publishedByPrincipalId",
        "Announcement.publishedAt",
        "Announcement.locale"
       ],
       "operation": "listAnnouncements",
       "provenance": "contract workforce.yaml GET /announcements"
      },
      {
       "kind": "detailPanel",
       "label": "The announcement reach",
       "bindsTo": "AnnouncementReach",
       "columns": [
        "AnnouncementReach.announcementId",
        "AnnouncementReach.targeted",
        "AnnouncementReach.delivered",
        "AnnouncementReach.acknowledged",
        "AnnouncementReach.outstanding"
       ],
       "operation": "getAnnouncementReach",
       "provenance": "contract workforce.yaml GET /announcements/{announcementId}/reach"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Acknowledge announcement",
       "operation": "acknowledgeAnnouncement",
       "provenance": "contract workforce.yaml POST /announcements/{announcementId}/acknowledge"
      },
      {
       "kind": "secondaryButton",
       "label": "Publish announcement",
       "operation": "publishAnnouncement",
       "provenance": "contract workforce.yaml POST /announcements"
      },
      {
       "kind": "publishGate",
       "label": "What publishing changes",
       "notes": "**Names what goes live, where, and from when.** A publish with no stated consequence is one somebody presses meaning to save.",
       "provenance": "authored — required by check-screens"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The notifications list.",
   "error": "Could not load. Names which read failed and leaves the notifications untouched.",
   "emptyFirstRun": "No notifications yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table.",
   "emptyNoResults": "Nothing matches the filter on unacknowledgedOnly and the notifications are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Shown when the caller lacks `WORKFORCE_VIEW`, which `listAnnouncements` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "offline": "Cached, with age. Acknowledgements queue"
  },
  "apis": [
   {
    "operationId": "listAnnouncements",
    "contract": "workforce",
    "purpose": "What staff have been told",
    "trigger": "onLoad"
   },
   {
    "operationId": "acknowledgeAnnouncement",
    "contract": "workforce",
    "purpose": "Confirm you have read it",
    "trigger": "onAction",
    "invalidates": [
     "listAnnouncements"
    ]
   },
   {
    "operationId": "getAnnouncementReach",
    "contract": "workforce",
    "purpose": "Who has acknowledged, and who has not",
    "trigger": "onAction"
   },
   {
    "operationId": "publishAnnouncement",
    "contract": "workforce",
    "purpose": "Tell staff something",
    "trigger": "onAction",
    "invalidates": [
     "listAnnouncements"
    ]
   },
   {
    "operationId": "listStaffConversations",
    "contract": "workforce",
    "purpose": "My conversations with colleagues, unread first",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "listStaffMessages",
    "contract": "workforce",
    "purpose": "Open a conversation",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "sendStaffMessage",
    "contract": "workforce",
    "purpose": "Message a colleague or a small group",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "markStaffConversationRead",
    "contract": "workforce",
    "purpose": "Mark a conversation read",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "announcementId",
     "from": "deepLink"
    },
    {
     "name": "conversationId",
     "from": "navigation"
    }
   ],
   "coldEntry": "**A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know whether the record moved, closed or never existed, because those are three different next actions. **The scope is resolved from the session, never from the link**: a link cannot move somebody to a venue they do not hold. Arrives with `announcementId`.",
   "preloaded": [
    "Announcement.id",
    "Announcement.title",
    "Announcement.body",
    "Announcement.kind",
    "Announcement.venueIds"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P06 Venue Staff App.dc.html#emp-037"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 4 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "overlays": [
   {
    "id": "formPublishAnnouncement",
    "component": "modal",
    "trigger": "Publish announcement",
    "body": "**Collects what `publishAnnouncement` sends before it is called.** Required: `title`, `body`, `kind`, `publishedAt`. Optional: `id`, `venueIds`, `departmentIds`, `roleIds`, `requiresAcknowledgement`, `expiresAt`, `publishedByPrincipalId`, `locale`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "Announcement",
    "confirm": {
     "label": "Publish announcement",
     "operation": "publishAnnouncement"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "title",
      "body",
      "kind",
      "publishedAt",
      "id",
      "venueIds",
      "departmentIds",
      "roleIds",
      "requiresAcknowledgement",
      "expiresAt",
      "publishedByPrincipalId",
      "locale"
     ]
    },
    "provenance": "contract workforce.yaml POST /announcements"
   }
  ],
  "_platform": {
   "code": "P06",
   "audience": "staff",
   "formFactor": "mobileApp",
   "shortName": "Venue Staff App",
   "name": "Venue Staff App — Operations",
   "app": "venue-staff-app",
   "offlineCapable": true,
   "operator": "venue",
   "targetApp": {
    "app": "venue-staff-mobile",
    "name": "TICVAI Venue Staff",
    "shell": "mobile",
    "siblings": [
     "P07"
    ],
    "note": "**Both offline-capable, both carried rather than sat at.** They cannot fold into venue management, which is online desktop web, and they share 69% with each other.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "EMP-039",
  "name": "Announcements",
  "module": "Operations",
  "requiresModule": "core",
  "wave": 2,
  "capability": "C00",
  "implementation": {
   "app": "venue-staff-app",
   "route": "/operations/announcements",
   "component": "apps/venue-staff-app/src/routes/operations/AnnouncementsDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "exitTo": [
    "EMP-001",
    "EMP-002",
    "EMP-003"
   ],
   "inferred": false,
   "entryFrom": [
    "EMP-003"
   ],
   "notes": "**Reached from EMP-003** — the screen the device sits on between tasks. Stated on 4 September: this screen exited to the hubs and nothing exited to it, so it was outside the navigation graph entirely.",
   "transitions": [
    {
     "to": "EMP-001",
     "trigger": "Sign in",
     "provenance": "derived — EMP-001 declares entryState.params challengeId and EMP-039 holds none of them, so the edge carries nothing and EMP-001 opens cold"
    },
    {
     "to": "EMP-002",
     "trigger": "Select venue & role",
     "provenance": "derived — EMP-002 declares entryState.params  and EMP-039 holds none of them, so the edge carries nothing and EMP-002 opens cold"
    },
    {
     "to": "EMP-003",
     "trigger": "Home — on duty",
     "provenance": "derived — EMP-003 declares entryState.params incidentId and EMP-039 holds none of them, so the edge carries nothing and EMP-003 opens cold"
    }
   ]
  },
  "notes": "Definition derived from the wireframe board on 14 August. Components, states and operations still to be written.",
  "density": "comfortable",
  "pattern": "listDetail",
  "patternReason": "`listAnnouncements` reads the population and `getAnnouncementReach` reads one of them — list, select, act",
  "purpose": "Read what the venue told everybody.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "toggle",
       "label": "Unacknowledged only",
       "operation": "listAnnouncements",
       "notes": "Sends `?unacknowledgedOnly=` to `listAnnouncements`.",
       "provenance": "contract workforce.yaml GET /announcements"
      },
      {
       "kind": "dataTable",
       "label": "Every announcement",
       "bindsTo": "Announcement",
       "columns": [
        "Announcement.id",
        "Announcement.title",
        "Announcement.body",
        "Announcement.kind",
        "Announcement.venueIds",
        "Announcement.departmentIds",
        "Announcement.roleIds",
        "Announcement.requiresAcknowledgement",
        "Announcement.expiresAt",
        "Announcement.publishedByPrincipalId",
        "Announcement.publishedAt",
        "Announcement.locale"
       ],
       "operation": "listAnnouncements",
       "provenance": "contract workforce.yaml GET /announcements"
      },
      {
       "kind": "publishGate",
       "impliedBy": "publishAnnouncement",
       "notes": "Declares `publishAnnouncement`. **The gate names what the publish will affect before it happens** — a disabled Publish with no reason is the state operators escalate.\n",
       "provenance": "carried from the previous definition"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected announcement",
       "bindsTo": "Announcement",
       "columns": [
        "Announcement.id",
        "Announcement.title",
        "Announcement.body",
        "Announcement.kind",
        "Announcement.venueIds",
        "Announcement.departmentIds",
        "Announcement.roleIds",
        "Announcement.requiresAcknowledgement",
        "Announcement.expiresAt",
        "Announcement.publishedByPrincipalId",
        "Announcement.publishedAt",
        "Announcement.locale"
       ],
       "operation": "listAnnouncements",
       "provenance": "contract workforce.yaml GET /announcements"
      },
      {
       "kind": "detailPanel",
       "label": "The announcement reach",
       "bindsTo": "AnnouncementReach",
       "columns": [
        "AnnouncementReach.announcementId",
        "AnnouncementReach.targeted",
        "AnnouncementReach.delivered",
        "AnnouncementReach.acknowledged",
        "AnnouncementReach.outstanding"
       ],
       "operation": "getAnnouncementReach",
       "provenance": "contract workforce.yaml GET /announcements/{announcementId}/reach"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Acknowledge announcement",
       "operation": "acknowledgeAnnouncement",
       "provenance": "contract workforce.yaml POST /announcements/{announcementId}/acknowledge"
      },
      {
       "kind": "secondaryButton",
       "label": "Publish announcement",
       "operation": "publishAnnouncement",
       "provenance": "contract workforce.yaml POST /announcements"
      },
      {
       "kind": "publishGate",
       "label": "What publishing changes",
       "notes": "**Names what goes live, where, and from when.** A publish with no stated consequence is one somebody presses meaning to save.",
       "provenance": "authored — required by check-screens"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The announcements list.",
   "error": "Could not load. Names which read failed and leaves the announcements untouched.",
   "emptyFirstRun": "No announcements yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table.",
   "emptyNoResults": "Nothing matches the filter on unacknowledgedOnly and the announcements are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Shown when the caller lacks `WORKFORCE_VIEW`, which `listAnnouncements` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "offline": "Cached. **Acknowledgement queues** — an emergency acknowledgement needing a network does not arrive when it matters"
  },
  "apis": [
   {
    "operationId": "listAnnouncements",
    "contract": "workforce",
    "purpose": "What staff have been told",
    "trigger": "onLoad"
   },
   {
    "operationId": "acknowledgeAnnouncement",
    "contract": "workforce",
    "purpose": "Confirm you have read it",
    "trigger": "onAction",
    "invalidates": [
     "listAnnouncements"
    ]
   },
   {
    "operationId": "getAnnouncementReach",
    "contract": "workforce",
    "purpose": "Who has acknowledged, and who has not",
    "trigger": "onAction"
   },
   {
    "operationId": "publishAnnouncement",
    "contract": "workforce",
    "purpose": "Tell staff something",
    "trigger": "onAction",
    "invalidates": [
     "listAnnouncements"
    ]
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "announcementId",
     "from": "deepLink"
    }
   ],
   "coldEntry": "**A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know whether the record moved, closed or never existed, because those are three different next actions. **The scope is resolved from the session, never from the link**: a link cannot move somebody to a venue they do not hold. Arrives with `announcementId`.",
   "preloaded": [
    "Announcement.id",
    "Announcement.title",
    "Announcement.body",
    "Announcement.kind",
    "Announcement.venueIds"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P06 Venue Staff App.dc.html#emp-039"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 4 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "overlays": [
   {
    "id": "formPublishAnnouncement",
    "component": "modal",
    "trigger": "Publish announcement",
    "body": "**Collects what `publishAnnouncement` sends before it is called.** Required: `title`, `body`, `kind`, `publishedAt`. Optional: `id`, `venueIds`, `departmentIds`, `roleIds`, `requiresAcknowledgement`, `expiresAt`, `publishedByPrincipalId`, `locale`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "Announcement",
    "confirm": {
     "label": "Publish announcement",
     "operation": "publishAnnouncement"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "title",
      "body",
      "kind",
      "publishedAt",
      "id",
      "venueIds",
      "departmentIds",
      "roleIds",
      "requiresAcknowledgement",
      "expiresAt",
      "publishedByPrincipalId",
      "locale"
     ]
    },
    "provenance": "contract workforce.yaml POST /announcements"
   }
  ],
  "_platform": {
   "code": "P06",
   "audience": "staff",
   "formFactor": "mobileApp",
   "shortName": "Venue Staff App",
   "name": "Venue Staff App — Operations",
   "app": "venue-staff-app",
   "offlineCapable": true,
   "operator": "venue",
   "targetApp": {
    "app": "venue-staff-mobile",
    "name": "TICVAI Venue Staff",
    "shell": "mobile",
    "siblings": [
     "P07"
    ],
    "note": "**Both offline-capable, both carried rather than sat at.** They cannot fold into venue management, which is online desktop web, and they share 69% with each other.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "EMP-038",
  "name": "Broadcast to team",
  "module": "Operations",
  "requiresModule": "core",
  "wave": 2,
  "capability": "C00",
  "implementation": {
   "app": "venue-staff-app",
   "route": "/operations/broadcast-to-team",
   "component": "apps/venue-staff-app/src/routes/operations/BroadcastToTeamDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "exitTo": [
    "EMP-001",
    "EMP-002",
    "EMP-003"
   ],
   "inferred": false,
   "entryFrom": [
    "EMP-003"
   ],
   "notes": "**Reached from EMP-003** — the screen the device sits on between tasks. Stated on 4 September: this screen exited to the hubs and nothing exited to it, so it was outside the navigation graph entirely.",
   "transitions": [
    {
     "to": "EMP-001",
     "trigger": "Sign in",
     "provenance": "derived — EMP-001 declares entryState.params challengeId and EMP-038 holds none of them, so the edge carries nothing and EMP-001 opens cold"
    },
    {
     "to": "EMP-002",
     "trigger": "Select venue & role",
     "provenance": "derived — EMP-002 declares entryState.params  and EMP-038 holds none of them, so the edge carries nothing and EMP-002 opens cold"
    },
    {
     "to": "EMP-003",
     "trigger": "Home — on duty",
     "provenance": "derived — EMP-003 declares entryState.params incidentId and EMP-038 holds none of them, so the edge carries nothing and EMP-003 opens cold"
    }
   ]
  },
  "notes": "Definition derived from the wireframe board on 14 August. Components, states and operations still to be written.",
  "density": "comfortable",
  "pattern": "listDetail",
  "patternReason": "`listAnnouncements` reads the population and `getAnnouncementReach` reads one of them — list, select, act",
  "purpose": "Reach everybody on shift at once.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "toggle",
       "label": "Unacknowledged only",
       "operation": "listAnnouncements",
       "notes": "Sends `?unacknowledgedOnly=` to `listAnnouncements`.",
       "provenance": "contract workforce.yaml GET /announcements"
      },
      {
       "kind": "dataTable",
       "label": "Every announcement",
       "bindsTo": "Announcement",
       "columns": [
        "Announcement.id",
        "Announcement.title",
        "Announcement.body",
        "Announcement.kind",
        "Announcement.venueIds",
        "Announcement.departmentIds",
        "Announcement.roleIds",
        "Announcement.requiresAcknowledgement",
        "Announcement.expiresAt",
        "Announcement.publishedByPrincipalId",
        "Announcement.publishedAt",
        "Announcement.locale"
       ],
       "operation": "listAnnouncements",
       "provenance": "contract workforce.yaml GET /announcements"
      },
      {
       "kind": "publishGate",
       "impliedBy": "publishAnnouncement",
       "notes": "Declares `publishAnnouncement`. **The gate names what the publish will affect before it happens** — a disabled Publish with no reason is the state operators escalate.\n",
       "provenance": "carried from the previous definition"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected announcement",
       "bindsTo": "Announcement",
       "columns": [
        "Announcement.id",
        "Announcement.title",
        "Announcement.body",
        "Announcement.kind",
        "Announcement.venueIds",
        "Announcement.departmentIds",
        "Announcement.roleIds",
        "Announcement.requiresAcknowledgement",
        "Announcement.expiresAt",
        "Announcement.publishedByPrincipalId",
        "Announcement.publishedAt",
        "Announcement.locale"
       ],
       "operation": "listAnnouncements",
       "provenance": "contract workforce.yaml GET /announcements"
      },
      {
       "kind": "detailPanel",
       "label": "The announcement reach",
       "bindsTo": "AnnouncementReach",
       "columns": [
        "AnnouncementReach.announcementId",
        "AnnouncementReach.targeted",
        "AnnouncementReach.delivered",
        "AnnouncementReach.acknowledged",
        "AnnouncementReach.outstanding"
       ],
       "operation": "getAnnouncementReach",
       "provenance": "contract workforce.yaml GET /announcements/{announcementId}/reach"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Publish announcement",
       "operation": "publishAnnouncement",
       "provenance": "contract workforce.yaml POST /announcements",
       "notes": "Kind `emergency` needs ANNOUNCEMENT_EMERGENCY, not ANNOUNCEMENT_PUBLISH; without it the emergency kind is not offered and a publish is refused 403 `emergency-permission-required` (decided 28 September, audit R091 (1))."
      },
      {
       "kind": "secondaryButton",
       "label": "Acknowledge announcement",
       "operation": "acknowledgeAnnouncement",
       "provenance": "contract workforce.yaml POST /announcements/{announcementId}/acknowledge"
      },
      {
       "kind": "publishGate",
       "label": "What publishing changes",
       "notes": "**Names what goes live, where, and from when.** A publish with no stated consequence is one somebody presses meaning to save.",
       "provenance": "authored — required by check-screens"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The broadcast team list.",
   "error": "Could not load. Names which read failed and leaves the broadcast team untouched.",
   "emptyFirstRun": "No broadcast team yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table.",
   "emptyNoResults": "Nothing matches the filter on unacknowledgedOnly and the broadcast team are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Shown when the caller lacks `WORKFORCE_VIEW`, which `getAnnouncementReach` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "offline": "Queues, and states that it has not gone yet"
  },
  "apis": [
   {
    "operationId": "publishAnnouncement",
    "contract": "workforce",
    "purpose": "Tell staff something",
    "trigger": "onAction",
    "invalidates": [
     "listAnnouncements"
    ]
   },
   {
    "operationId": "getAnnouncementReach",
    "contract": "workforce",
    "purpose": "Who has acknowledged, and who has not",
    "trigger": "onAction"
   },
   {
    "operationId": "acknowledgeAnnouncement",
    "contract": "workforce",
    "purpose": "Confirm you have read it",
    "trigger": "onAction",
    "invalidates": [
     "listAnnouncements"
    ]
   },
   {
    "operationId": "listAnnouncements",
    "contract": "workforce",
    "purpose": "What staff have been told",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "announcementId",
     "from": "deepLink"
    }
   ],
   "coldEntry": "**A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know whether the record moved, closed or never existed, because those are three different next actions. **The scope is resolved from the session, never from the link**: a link cannot move somebody to a venue they do not hold. Arrives with `announcementId`.",
   "preloaded": [
    "Announcement.id",
    "Announcement.title",
    "Announcement.body",
    "Announcement.kind",
    "Announcement.venueIds"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P06 Venue Staff App.dc.html#emp-038"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 4 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "overlays": [
   {
    "id": "formPublishAnnouncement",
    "component": "modal",
    "trigger": "Publish announcement",
    "body": "**Collects what `publishAnnouncement` sends before it is called.** Required: `title`, `body`, `kind`, `publishedAt`. Optional: `id`, `venueIds`, `departmentIds`, `roleIds`, `requiresAcknowledgement`, `expiresAt`, `publishedByPrincipalId`, `locale`. **An `emergency` kind requires ANNOUNCEMENT_EMERGENCY** (audit R091 (1)). Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "Announcement",
    "confirm": {
     "label": "Publish announcement",
     "operation": "publishAnnouncement"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "title",
      "body",
      "kind",
      "publishedAt",
      "id",
      "venueIds",
      "departmentIds",
      "roleIds",
      "requiresAcknowledgement",
      "expiresAt",
      "publishedByPrincipalId",
      "locale"
     ]
    },
    "provenance": "contract workforce.yaml POST /announcements"
   }
  ],
  "_platform": {
   "code": "P06",
   "audience": "staff",
   "formFactor": "mobileApp",
   "shortName": "Venue Staff App",
   "name": "Venue Staff App — Operations",
   "app": "venue-staff-app",
   "offlineCapable": true,
   "operator": "venue",
   "targetApp": {
    "app": "venue-staff-mobile",
    "name": "TICVAI Venue Staff",
    "shell": "mobile",
    "siblings": [
     "P07"
    ],
    "note": "**Both offline-capable, both carried rather than sat at.** They cannot fold into venue management, which is online desktop web, and they share 69% with each other.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "EMP-040",
  "name": "Knowledge base",
  "module": "Operations",
  "requiresModule": "ai",
  "wave": 2,
  "capability": "C00",
  "implementation": {
   "app": "venue-staff-app",
   "route": "/operations/knowledge-base",
   "component": "apps/venue-staff-app/src/routes/operations/KnowledgeBaseDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "exitTo": [
    "EMP-001",
    "EMP-002",
    "EMP-003",
    "EMP-041"
   ],
   "inferred": false,
   "entryFrom": [
    "EMP-003",
    "EMP-020"
   ],
   "notes": "**Reached from EMP-003** — the screen the device sits on between tasks. Stated on 4 September: this screen exited to the hubs and nothing exited to it, so it was outside the navigation graph entirely.",
   "transitions": [
    {
     "to": "EMP-001",
     "trigger": "Sign in",
     "provenance": "derived — EMP-001 declares entryState.params challengeId and EMP-040 holds none of them, so the edge carries nothing and EMP-001 opens cold"
    },
    {
     "to": "EMP-002",
     "trigger": "Select venue & role",
     "provenance": "derived — EMP-002 declares entryState.params  and EMP-040 holds none of them, so the edge carries nothing and EMP-002 opens cold"
    },
    {
     "to": "EMP-003",
     "trigger": "Home — on duty",
     "provenance": "derived — EMP-003 declares entryState.params incidentId and EMP-040 holds none of them, so the edge carries nothing and EMP-003 opens cold"
    }
   ]
  },
  "notes": "Definition derived from the wireframe board on 14 August. Components, states and operations still to be written.",
  "density": "comfortable",
  "pattern": "configEditor",
  "patternReason": "the screen declares only writes (`semanticSearch`) and no read of a population — it is settings, not a list",
  "purpose": "Look up the rule rather than guess it.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Semantic search",
       "operation": "semanticSearch",
       "provenance": "contract ai.yaml POST /search"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "carried",
     "components": [
      {
       "kind": "searchField",
       "label": "Query",
       "operation": "semanticSearch",
       "notes": "Required.",
       "provenance": "contract ai.yaml POST /search"
      },
      {
       "kind": "multiSelect",
       "label": "Kinds",
       "operation": "semanticSearch",
       "provenance": "contract ai.yaml POST /search"
      },
      {
       "kind": "numberField",
       "label": "Limit",
       "operation": "semanticSearch",
       "provenance": "contract ai.yaml POST /search"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The saved knowledge base.",
   "error": "Could not load. Names which read failed and leaves the knowledge base untouched.",
   "emptyFirstRun": "No knowledge base configured. The form opens empty and `semanticSearch` saves the first one; it says what the platform does in the meantime.",
   "emptyNoAccess": "Shown when the caller lacks `AI_USE`, which `semanticSearch` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "offline": "**Cached articles only**, with a note that newer ones may exist"
  },
  "apis": [
   {
    "operationId": "semanticSearch",
    "contract": "ai",
    "purpose": "Search meaning, not words",
    "trigger": "onAction"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P06 Venue Staff App.dc.html#emp-040"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 1 operation this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "_platform": {
   "code": "P06",
   "audience": "staff",
   "formFactor": "mobileApp",
   "shortName": "Venue Staff App",
   "name": "Venue Staff App — Operations",
   "app": "venue-staff-app",
   "offlineCapable": true,
   "operator": "venue",
   "targetApp": {
    "app": "venue-staff-mobile",
    "name": "TICVAI Venue Staff",
    "shell": "mobile",
    "siblings": [
     "P07"
    ],
    "note": "**Both offline-capable, both carried rather than sat at.** They cannot fold into venue management, which is online desktop web, and they share 69% with each other.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "EMP-041",
  "name": "Training",
  "module": "Operations",
  "requiresModule": "ai",
  "wave": 3,
  "capability": "C00",
  "implementation": {
   "app": "venue-staff-app",
   "route": "/operations/training",
   "component": "apps/venue-staff-app/src/routes/operations/TrainingDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "exitTo": [
    "EMP-001",
    "EMP-002",
    "EMP-003"
   ],
   "inferred": false,
   "entryFrom": [
    "EMP-040"
   ],
   "notes": "**Reached from EMP-040** — training is reached from the knowledge it extends. Stated on 4 September: this screen exited to the hubs and nothing exited to it, so it was outside the navigation graph entirely.",
   "transitions": [
    {
     "to": "EMP-001",
     "trigger": "Sign in",
     "provenance": "derived — EMP-001 declares entryState.params challengeId and EMP-041 holds none of them, so the edge carries nothing and EMP-001 opens cold"
    },
    {
     "to": "EMP-002",
     "trigger": "Select venue & role",
     "provenance": "derived — EMP-002 declares entryState.params  and EMP-041 holds none of them, so the edge carries nothing and EMP-002 opens cold"
    },
    {
     "to": "EMP-003",
     "trigger": "Home — on duty",
     "provenance": "derived — EMP-003 declares entryState.params incidentId and EMP-041 holds none of them, so the edge carries nothing and EMP-003 opens cold"
    }
   ]
  },
  "notes": "Definition derived from the wireframe board on 14 August. Components, states and operations still to be written.",
  "density": "comfortable",
  "pattern": "listDetail",
  "patternReason": "`listTrainingRecords` reads a population and nothing reads one of them; the detail is the row until a `get` exists",
  "purpose": "Do the module that unlocks the role.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every training",
       "bindsTo": "TrainingRecord",
       "columns": [
        "TrainingRecord.id",
        "TrainingRecord.principalId",
        "TrainingRecord.courseName",
        "TrainingRecord.required",
        "TrainingRecord.completedAt",
        "TrainingRecord.expiresAt",
        "TrainingRecord.state",
        "TrainingRecord.evidenceRef"
       ],
       "operation": "listTrainingRecords",
       "provenance": "contract workforce.yaml GET /training-records"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected training",
       "bindsTo": "TrainingRecord",
       "columns": [
        "TrainingRecord.id",
        "TrainingRecord.principalId",
        "TrainingRecord.courseName",
        "TrainingRecord.required",
        "TrainingRecord.completedAt",
        "TrainingRecord.expiresAt",
        "TrainingRecord.state",
        "TrainingRecord.evidenceRef"
       ],
       "operation": "listTrainingRecords",
       "provenance": "contract workforce.yaml GET /training-records"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Semantic search",
       "operation": "semanticSearch",
       "provenance": "contract ai.yaml POST /search"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The training list.",
   "error": "Could not load. Names which read failed and leaves the training untouched.",
   "emptyFirstRun": "No training yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table.",
   "emptyNoResults": "Never shown: `listTrainingRecords` takes no filter, so an empty list is always the first-run state above.",
   "emptyNoAccess": "Shown when the caller lacks `WORKFORCE_VIEW`, which `listTrainingRecords` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "offline": "Cached progress; completions queue"
  },
  "apis": [
   {
    "operationId": "semanticSearch",
    "contract": "ai",
    "purpose": "Search meaning, not words",
    "trigger": "onAction",
    "invalidates": [
     "listTrainingRecords"
    ]
   },
   {
    "operationId": "listTrainingRecords",
    "contract": "workforce",
    "purpose": "Training completed and what is expiring",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "TrainingRecord.id",
    "TrainingRecord.principalId",
    "TrainingRecord.courseName",
    "TrainingRecord.required",
    "TrainingRecord.completedAt"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P06 Venue Staff App.dc.html#emp-041"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 2 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "overlays": [
   {
    "id": "formSemanticSearch",
    "component": "modal",
    "trigger": "Semantic search",
    "body": "**Collects what `semanticSearch` sends before it is called.** Required: `query`. Optional: `kinds`, `limit`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Semantic search",
     "operation": "semanticSearch"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "query",
      "kinds",
      "limit"
     ]
    },
    "provenance": "contract ai.yaml POST /search"
   }
  ],
  "_platform": {
   "code": "P06",
   "audience": "staff",
   "formFactor": "mobileApp",
   "shortName": "Venue Staff App",
   "name": "Venue Staff App — Operations",
   "app": "venue-staff-app",
   "offlineCapable": true,
   "operator": "venue",
   "targetApp": {
    "app": "venue-staff-mobile",
    "name": "TICVAI Venue Staff",
    "shell": "mobile",
    "siblings": [
     "P07"
    ],
    "note": "**Both offline-capable, both carried rather than sat at.** They cannot fold into venue management, which is online desktop web, and they share 69% with each other.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "EMP-042",
  "name": "Profile",
  "module": "Operations",
  "requiresModule": "core",
  "wave": 1,
  "capability": "C00",
  "implementation": {
   "app": "venue-staff-app",
   "route": "/operations/profile",
   "component": "apps/venue-staff-app/src/routes/operations/ProfileDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "exitTo": [
    "EMP-001",
    "EMP-002",
    "EMP-003"
   ],
   "inferred": false,
   "entryFrom": [
    "EMP-003"
   ],
   "notes": "**Reached from EMP-003** — the screen the device sits on between tasks. Stated on 4 September: this screen exited to the hubs and nothing exited to it, so it was outside the navigation graph entirely.",
   "transitions": [
    {
     "to": "EMP-001",
     "trigger": "Sign in",
     "provenance": "derived — EMP-001 declares entryState.params challengeId and EMP-042 holds none of them, so the edge carries nothing and EMP-001 opens cold"
    },
    {
     "to": "EMP-002",
     "trigger": "Select venue & role",
     "provenance": "derived — EMP-002 declares entryState.params  and EMP-042 holds none of them, so the edge carries nothing and EMP-002 opens cold"
    },
    {
     "to": "EMP-003",
     "trigger": "Home — on duty",
     "provenance": "derived — EMP-003 declares entryState.params incidentId and EMP-042 holds none of them, so the edge carries nothing and EMP-003 opens cold"
    }
   ]
  },
  "notes": "Definition derived from the wireframe board on 14 August. Components, states and operations still to be written. **Removed 24 August**: forceLogout, listActiveSessions, revokeAllSessions. **Bulk-attach residue** — the 18 August defect that put identical operation sets on unrelated screens. A till does not cancel a performance, a staff app does not create roles, and **a scanner does not run a cash shift.**",
  "density": "comfortable",
  "pattern": "listDetail",
  "patternReason": "`listMfaMethods` reads the population and `getCurrentSession` reads one of them — list, select, act",
  "purpose": "Change what this person controls about themselves.",
  "gaps": [
   {
    "operation": "listSsoProviders",
    "why": "**1 declared operation reaches no component on this screen**: listSsoProviders. Either the screen is missing what calls them, or the declaration is residue.",
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
       "label": "Every MFA method",
       "bindsTo": "MfaMethod",
       "columns": [
        "MfaMethod.id",
        "MfaMethod.kind",
        "MfaMethod.label",
        "MfaMethod.maskedTarget",
        "MfaMethod.isActive",
        "MfaMethod.isPrimary",
        "MfaMethod.enrolledAt",
        "MfaMethod.lastUsedAt"
       ],
       "operation": "listMfaMethods",
       "provenance": "contract identity.yaml GET /auth/mfa/methods"
      },
      {
       "kind": "dataTable",
       "label": "Every SSO provider",
       "bindsTo": "SsoProvider",
       "columns": [
        "SsoProvider.id",
        "SsoProvider.displayName",
        "SsoProvider.protocol",
        "SsoProvider.iconAssetRef",
        "SsoProvider.isEnforced",
        "SsoProvider.scopePath"
       ],
       "operation": "listSsoProviders",
       "provenance": "contract identity.yaml GET /auth/sso/providers"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected MFA method",
       "bindsTo": "MfaMethod",
       "columns": [
        "MfaMethod.id",
        "MfaMethod.kind",
        "MfaMethod.label",
        "MfaMethod.maskedTarget",
        "MfaMethod.isActive",
        "MfaMethod.isPrimary",
        "MfaMethod.enrolledAt",
        "MfaMethod.lastUsedAt"
       ],
       "operation": "listMfaMethods",
       "provenance": "contract identity.yaml GET /auth/mfa/methods"
      },
      {
       "kind": "detailPanel",
       "label": "The session",
       "bindsTo": "Session",
       "columns": [
        "Session.sessionId",
        "Session.principalId",
        "Session.roleId",
        "Session.displayName",
        "Session.scope",
        "Session.effectivePermissions",
        "Session.permissionsByScope",
        "Session.saleBoardId",
        "Session.workstation",
        "Session.openedAt",
        "Session.expiresAt"
       ],
       "operation": "getCurrentSession",
       "provenance": "contract identity.yaml GET /auth/session"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Add a sign-in method",
       "operation": "enrolMfaMethod",
       "provenance": "contract identity.yaml POST /auth/mfa/methods",
       "notes": "Offers only an authenticator app (`totp`) and email (`emailOtp`, the fallback); any other kind is refused 422 `mfa-kind-not-allowed` (decided 28 September, audit R126 (5))."
      },
      {
       "kind": "secondaryButton",
       "label": "Verify the new method",
       "operation": "verifyMfaEnrolment",
       "provenance": "contract identity.yaml POST /auth/mfa/methods/{methodId}",
       "notes": "The method is not active until a code from it is verified."
      },
      {
       "kind": "destructiveButton",
       "label": "Remove this method",
       "operation": "removeMfaMethod",
       "provenance": "contract identity.yaml DELETE /auth/mfa/methods/{methodId}",
       "notes": "Removing the last active method is refused 409 while the person holds a permission that requires MFA (ROLE_MANAGE, LEDGER_APPROVE, or one the tenant added) (decided 28 September, audit R135)."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The profile list.",
   "error": "Could not load. Names which read failed and leaves the profile untouched.",
   "emptyFirstRun": "No profile yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table.",
   "emptyNoResults": "Never shown: `listMfaMethods` takes no filter, so an empty list is always the first-run state above.",
   "offline": "Cached"
  },
  "apis": [
   {
    "operationId": "getCurrentSession",
    "contract": "identity",
    "purpose": "Current session and effective permissions",
    "trigger": "onLoad"
   },
   {
    "operationId": "listMfaMethods",
    "contract": "identity",
    "purpose": "Enrolled MFA methods",
    "trigger": "onLoad"
   },
   {
    "operationId": "enrolMfaMethod",
    "contract": "identity",
    "purpose": "Start enrolling an authenticator app, or email as the fallback (audit R126 (5), R135)",
    "trigger": "onAction",
    "invalidates": [
     "listMfaMethods"
    ]
   },
   {
    "operationId": "verifyMfaEnrolment",
    "contract": "identity",
    "purpose": "Activate the new method with a code from it",
    "trigger": "onAction",
    "invalidates": [
     "listMfaMethods"
    ]
   },
   {
    "operationId": "removeMfaMethod",
    "contract": "identity",
    "purpose": "Remove a method; the last one is refused 409 while a permission requiring MFA is held (audit R135)",
    "trigger": "onAction",
    "invalidates": [
     "listMfaMethods"
    ]
   },
   {
    "operationId": "listSsoProviders",
    "contract": "identity",
    "purpose": "Identity providers configured for this tenant",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "sessionId",
     "from": "session"
    },
    {
     "name": "methodId",
     "from": "navigation"
    }
   ],
   "coldEntry": "Resolves from the session; a cold arrival is the ordinary case.",
   "preloaded": [
    "MfaMethod.id",
    "MfaMethod.kind",
    "MfaMethod.label",
    "MfaMethod.maskedTarget",
    "MfaMethod.isActive"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P06 Venue Staff App.dc.html#emp-042"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 4 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "overlays": [
   {
    "id": "formEnrolMfaMethod",
    "component": "modal",
    "trigger": "Add a sign-in method",
    "body": "**Collects what `enrolMfaMethod` sends before it is called.** Required: `kind`, offered as authenticator app (`totp`) or email (`emailOtp`) only (audit R126 (5)). Optional: `target`, the email address for the email method. The response carries the secret and QR code for an authenticator app. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "MfaEnrolment",
    "confirm": {
     "label": "Add method",
     "operation": "enrolMfaMethod"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "kind",
      "target"
     ]
    },
    "provenance": "contract identity.yaml POST /auth/mfa/methods"
   },
   {
    "id": "formVerifyMfaEnrolment",
    "component": "modal",
    "trigger": "Verify the new method",
    "body": "**Collects what `verifyMfaEnrolment` sends before it is called.** Required: `code`. The method is active only after this. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Verify",
     "operation": "verifyMfaEnrolment"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "code"
     ]
    },
    "provenance": "contract identity.yaml POST /auth/mfa/methods/{methodId}"
   },
   {
    "id": "confirmRemoveMfaMethod",
    "component": "confirmDialog",
    "trigger": "Remove this method",
    "body": "**Names the method being removed.** Removing the last active method is refused 409 while the person holds a permission in `PasswordPolicy.mfaRequiredForPermissions`, and the dialog says so before the call rather than after (decided 28 September, audit R135).",
    "confirm": {
     "label": "Remove method",
     "operation": "removeMfaMethod"
    },
    "dismiss": {
     "label": "Keep it",
     "discards": []
    },
    "provenance": "contract identity.yaml DELETE /auth/mfa/methods/{methodId}"
   }
  ],
  "_platform": {
   "code": "P06",
   "audience": "staff",
   "formFactor": "mobileApp",
   "shortName": "Venue Staff App",
   "name": "Venue Staff App — Operations",
   "app": "venue-staff-app",
   "offlineCapable": true,
   "operator": "venue",
   "targetApp": {
    "app": "venue-staff-mobile",
    "name": "TICVAI Venue Staff",
    "shell": "mobile",
    "siblings": [
     "P07"
    ],
    "note": "**Both offline-capable, both carried rather than sat at.** They cannot fold into venue management, which is online desktop web, and they share 69% with each other.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "EMP-043",
  "name": "Device settings",
  "module": "Operations",
  "requiresModule": "marketing",
  "wave": 1,
  "capability": "C00",
  "implementation": {
   "app": "venue-staff-app",
   "route": "/operations/device-settings",
   "component": "apps/venue-staff-app/src/routes/operations/DeviceSettingsDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "exitTo": [
    "EMP-001",
    "EMP-002",
    "EMP-003",
    "EMP-018",
    "EMP-044",
    "EMP-045"
   ],
   "inferred": false,
   "entryFrom": [
    "EMP-003"
   ],
   "notes": "**Reached from EMP-003** — the screen the device sits on between tasks. Stated on 4 September: this screen exited to the hubs and nothing exited to it, so it was outside the navigation graph entirely.",
   "transitions": [
    {
     "to": "EMP-018",
     "trigger": "It pulls its offline package",
     "provenance": "flow F71 step 1→2",
     "operation": "listDevices"
    },
    {
     "to": "EMP-001",
     "trigger": "Sign in",
     "provenance": "derived — EMP-001 declares entryState.params challengeId and EMP-043 holds none of them, so the edge carries nothing and EMP-001 opens cold"
    },
    {
     "to": "EMP-002",
     "trigger": "Select venue & role",
     "provenance": "derived — EMP-002 declares entryState.params  and EMP-043 holds none of them, so the edge carries nothing and EMP-002 opens cold"
    },
    {
     "to": "EMP-003",
     "trigger": "Home — on duty",
     "provenance": "derived — EMP-003 declares entryState.params incidentId and EMP-043 holds none of them, so the edge carries nothing and EMP-003 opens cold"
    }
   ]
  },
  "notes": "Definition derived from the wireframe board on 14 August. Components, states and operations still to be written. **Removed 24 August**: listGuestDevices, adjustLoyaltyPoints, getConsentHistory, getGuestConsents, getGuestLoyalty, getGuestProfile, getWishlist. **Bulk-attach residue, found by walking a journey.** A device-settings screen does not read guest loyalty, a venue map does not set a refund policy, a shift summary does not close the shift, and **a rota a steward can rewrite is not a rota.** **Removed 24 August**: mergeGuestProfiles, searchGuests, updateGuestProfile. **Bulk-attach residue.** A device-settings screen does not merge guest profiles, a rota view does not author the rota, a shift summary does not open a shift, and **authority notification belongs where the incident is raised, not where it is read.**",
  "density": "comfortable",
  "pattern": "listDetail",
  "patternReason": "`listDevices` reads a population and nothing reads one of them; the detail is the row until a `get` exists",
  "purpose": "Set how this handheld behaves.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "textField",
       "label": "Workstation id",
       "operation": "listDevices",
       "notes": "Sends `?workstationId=` to `listDevices`.",
       "provenance": "contract tenancy.yaml GET /devices"
      },
      {
       "kind": "textField",
       "label": "Kind",
       "operation": "listDevices",
       "notes": "Sends `?kind=` to `listDevices`.",
       "provenance": "contract tenancy.yaml GET /devices"
      },
      {
       "kind": "dataTable",
       "label": "Every registered device",
       "bindsTo": "RegisteredDevice",
       "columns": [
        "RegisteredDevice.id",
        "RegisteredDevice.kind",
        "RegisteredDevice.driver",
        "RegisteredDevice.identifier",
        "RegisteredDevice.workstationId",
        "RegisteredDevice.model",
        "RegisteredDevice.pushToken",
        "RegisteredDevice.pushPlatform",
        "RegisteredDevice.pushFailureCount",
        "RegisteredDevice.offlineScope",
        "RegisteredDevice.firmwareVersion",
        "RegisteredDevice.isRequired"
       ],
       "operation": "listDevices",
       "provenance": "contract tenancy.yaml GET /devices"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected registered device",
       "bindsTo": "RegisteredDevice",
       "columns": [
        "RegisteredDevice.id",
        "RegisteredDevice.kind",
        "RegisteredDevice.driver",
        "RegisteredDevice.identifier",
        "RegisteredDevice.workstationId",
        "RegisteredDevice.model",
        "RegisteredDevice.pushToken",
        "RegisteredDevice.pushPlatform",
        "RegisteredDevice.pushFailureCount",
        "RegisteredDevice.offlineScope",
        "RegisteredDevice.firmwareVersion",
        "RegisteredDevice.isRequired",
        "RegisteredDevice.status",
        "RegisteredDevice.batteryPercent",
        "RegisteredDevice.lastCheckedAt",
        "RegisteredDevice.health"
       ],
       "operation": "listDevices",
       "provenance": "contract tenancy.yaml GET /devices"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Register device",
       "operation": "registerDevice",
       "provenance": "contract tenancy.yaml POST /devices"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The device settings list.",
   "error": "Could not load. Names which read failed and leaves the device settings untouched.",
   "emptyFirstRun": "No device settings yet. Offers Register device (`registerDevice`); distinct from a filter that matched nothing.",
   "emptyNoResults": "Nothing matches the filter on workstationId, kind and the device settings are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Shown when the caller lacks `DEVICE_VIEW`, which `listDevices` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "offline": "**Fully offline** — device settings are local by definition"
  },
  "apis": [
   {
    "operationId": "listDevices",
    "contract": "tenancy",
    "purpose": "List registered devices",
    "trigger": "onLoad"
   },
   {
    "operationId": "registerDevice",
    "contract": "tenancy",
    "purpose": "Register a device",
    "trigger": "onAction",
    "invalidates": [
     "listDevices"
    ]
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "subjectId",
     "from": "session"
    }
   ],
   "coldEntry": "Resolves from the session; a cold arrival is the ordinary case.",
   "preloaded": [
    "RegisteredDevice.id",
    "RegisteredDevice.kind",
    "RegisteredDevice.driver",
    "RegisteredDevice.identifier",
    "RegisteredDevice.workstationId"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P06 Venue Staff App.dc.html#emp-043"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 2 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "overlays": [
   {
    "id": "formRegisterDevice",
    "component": "modal",
    "trigger": "Register device",
    "body": "**Collects what `registerDevice` sends before it is called.** Required: `id`, `kind`, `driver`, `workstationId`. Optional: `identifier`, `model`, `pushToken`, `pushPlatform`, `pushFailureCount`, `offlineScope`, `firmwareVersion`, `isRequired`, `status`, `batteryPercent`, `lastCheckedAt`, `health` and 5 more. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "RegisteredDevice",
    "confirm": {
     "label": "Register device",
     "operation": "registerDevice"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "kind",
      "driver",
      "workstationId",
      "identifier",
      "model",
      "pushToken",
      "pushPlatform",
      "pushFailureCount",
      "offlineScope",
      "firmwareVersion",
      "isRequired",
      "status",
      "batteryPercent",
      "lastCheckedAt",
      "health",
      "lastHeartbeatAt",
      "capabilities"
     ]
    },
    "provenance": "contract tenancy.yaml POST /devices"
   }
  ],
  "_platform": {
   "code": "P06",
   "audience": "staff",
   "formFactor": "mobileApp",
   "shortName": "Venue Staff App",
   "name": "Venue Staff App — Operations",
   "app": "venue-staff-app",
   "offlineCapable": true,
   "operator": "venue",
   "targetApp": {
    "app": "venue-staff-mobile",
    "name": "TICVAI Venue Staff",
    "shell": "mobile",
    "siblings": [
     "P07"
    ],
    "note": "**Both offline-capable, both carried rather than sat at.** They cannot fold into venue management, which is online desktop web, and they share 69% with each other.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "EMP-044",
  "name": "Accessibility",
  "module": "Operations",
  "requiresModule": "core",
  "wave": 2,
  "capability": "C00",
  "implementation": {
   "app": "venue-staff-app",
   "route": "/operations/accessibility",
   "component": "apps/venue-staff-app/src/routes/operations/AccessibilityDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "exitTo": [
    "EMP-001",
    "EMP-002",
    "EMP-003"
   ],
   "inferred": false,
   "entryFrom": [
    "EMP-043"
   ],
   "notes": "**Reached from EMP-043** — accessibility is a device setting. Stated on 4 September: this screen exited to the hubs and nothing exited to it, so it was outside the navigation graph entirely.",
   "transitions": [
    {
     "to": "EMP-001",
     "trigger": "Sign in",
     "provenance": "derived — EMP-001 declares entryState.params challengeId and EMP-044 holds none of them, so the edge carries nothing and EMP-001 opens cold"
    },
    {
     "to": "EMP-002",
     "trigger": "Select venue & role",
     "provenance": "derived — EMP-002 declares entryState.params  and EMP-044 holds none of them, so the edge carries nothing and EMP-002 opens cold"
    },
    {
     "to": "EMP-003",
     "trigger": "Home — on duty",
     "provenance": "derived — EMP-003 declares entryState.params incidentId and EMP-044 holds none of them, so the edge carries nothing and EMP-003 opens cold"
    }
   ]
  },
  "notes": "Definition derived from the wireframe board on 14 August. Components, states and operations still to be written.",
  "density": "comfortable",
  "pattern": "listDetail",
  "patternReason": "**the screen's operations choose no pattern** — no list, no get, no write that groups. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Make the app usable in the conditions it is used in.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen declares no operation the contracts recognise.** Nothing fills it, nothing it does is committed anywhere, and its shape below is a default rather than a reading.",
    "source": "the screen's own declarations"
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
   "loading": "—",
   "error": "—",
   "emptyFirstRun": "—",
   "offline": "**Fully offline.** Accessibility settings are device-local and must never depend on a network"
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P06 Venue Staff App.dc.html#emp-044"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 0 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "_platform": {
   "code": "P06",
   "audience": "staff",
   "formFactor": "mobileApp",
   "shortName": "Venue Staff App",
   "name": "Venue Staff App — Operations",
   "app": "venue-staff-app",
   "offlineCapable": true,
   "operator": "venue",
   "targetApp": {
    "app": "venue-staff-mobile",
    "name": "TICVAI Venue Staff",
    "shell": "mobile",
    "siblings": [
     "P07"
    ],
    "note": "**Both offline-capable, both carried rather than sat at.** They cannot fold into venue management, which is online desktop web, and they share 69% with each other.",
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
 "acknowledgeAnnouncement": {
  "method": "POST",
  "path": "/announcements/{announcementId}/acknowledge",
  "contract": "workforce",
  "summary": "Confirm you have read it",
  "permission": "WORKFORCE_VIEW",
  "offlineCapable": true,
  "conflictPolicy": "append",
  "scopeLevel": "venue",
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
 "addTip": {
  "method": "POST",
  "path": "/payments/{paymentId}/tip",
  "contract": "orders",
  "summary": "Record a tip against a payment",
  "permission": "ORDER_MODIFY",
  "offlineCapable": true,
  "conflictPolicy": "append",
  "scopeLevel": "workstation",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "Payment"
 },
 "appendEntitlementToMedia": {
  "method": "POST",
  "path": "/media/{mediaCode}/entitlements",
  "contract": "orders",
  "summary": "Add something to a ticket the guest already holds",
  "permission": "ORDER_CREATE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "workstation",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "AppendEntitlementRequest",
  "responds": "AppendEntitlementResult"
 },
 "capturePayment": {
  "method": "POST",
  "path": "/payments/{paymentId}/capture",
  "contract": "orders",
  "summary": "Capture a previously authorised payment",
  "permission": "ORDER_CREATE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "workstation",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "Payment"
 },
 "createPayment": {
  "method": "POST",
  "path": "/payments",
  "contract": "orders",
  "summary": "Take a payment against an order",
  "permission": "ORDER_CREATE",
  "offlineCapable": true,
  "conflictPolicy": "append",
  "scopeLevel": "workstation",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "CreatePaymentRequest",
  "responds": "Payment"
 },
 "enrolMfaMethod": {
  "method": "POST",
  "path": "/auth/mfa/methods",
  "contract": "identity",
  "summary": "Enrol an MFA method",
  "permission": null,
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
  "responds": "MfaEnrolment"
 },
 "getAnnouncementReach": {
  "method": "GET",
  "path": "/announcements/{announcementId}/reach",
  "contract": "workforce",
  "summary": "Who has acknowledged, and who has not",
  "permission": "WORKFORCE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "AnnouncementReach"
 },
 "getCurrentSession": {
  "method": "GET",
  "path": "/auth/session",
  "contract": "identity",
  "summary": "Current session and effective permissions",
  "permission": null,
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "workstation",
  "parameters": [],
  "requestBody": null,
  "responds": "Session"
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
 "getMediaEntitlements": {
  "method": "GET",
  "path": "/media/{mediaCode}/entitlements",
  "contract": "orders",
  "summary": "What is already on this media",
  "permission": "ORDER_VIEW",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "MediaEntitlements"
 },
 "inquirePaymentStatus": {
  "method": "POST",
  "path": "/payments/{paymentId}/inquiry",
  "contract": "orders",
  "summary": "Ask the provider what actually happened",
  "permission": "ORDER_CREATE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "workstation",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "Payment"
 },
 "listAnnouncements": {
  "method": "GET",
  "path": "/announcements",
  "contract": "workforce",
  "summary": "What staff have been told",
  "permission": "WORKFORCE_VIEW",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "unacknowledgedOnly",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "Announcement"
 },
 "listDevices": {
  "method": "GET",
  "path": "/devices",
  "contract": "tenancy",
  "summary": "List registered devices",
  "permission": "DEVICE_VIEW",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "workstationId",
    "in": "query",
    "required": null
   },
   {
    "name": "kind",
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
 "listSsoProviders": {
  "method": "GET",
  "path": "/auth/sso/providers",
  "contract": "identity",
  "summary": "Identity providers configured for this tenant",
  "permission": null,
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [],
  "requestBody": null,
  "responds": "SsoProvider"
 },
 "listStaffConversations": {
  "method": "GET",
  "path": "/staff-conversations",
  "contract": "workforce",
  "summary": "The caller's staff conversations, newest activity first",
  "permission": "WORKFORCE_VIEW",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "unreadOnly",
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
 "listStaffMessages": {
  "method": "GET",
  "path": "/staff-conversations/{conversationId}/messages",
  "contract": "workforce",
  "summary": "Messages in one staff conversation, newest first",
  "permission": "WORKFORCE_VIEW",
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
 "listTrainingRecords": {
  "method": "GET",
  "path": "/training-records",
  "contract": "workforce",
  "summary": "Training completed and what is expiring",
  "permission": "WORKFORCE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "TrainingRecord"
 },
 "markStaffConversationRead": {
  "method": "POST",
  "path": "/staff-conversations/{conversationId}/read",
  "contract": "workforce",
  "summary": "Mark a staff conversation read up to a message",
  "permission": "WORKFORCE_VIEW",
  "offlineCapable": true,
  "conflictPolicy": "append",
  "scopeLevel": "venue",
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
 "publishAnnouncement": {
  "method": "POST",
  "path": "/announcements",
  "contract": "workforce",
  "summary": "Tell staff something",
  "permission": "ANNOUNCEMENT_PUBLISH",
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
  "requestBody": "Announcement",
  "responds": "Announcement"
 },
 "registerDevice": {
  "method": "POST",
  "path": "/devices",
  "contract": "tenancy",
  "summary": "Register a device",
  "permission": "DEVICE_CONFIGURE",
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
  "requestBody": "RegisteredDevice",
  "responds": "RegisteredDevice"
 },
 "removeMfaMethod": {
  "method": "DELETE",
  "path": "/auth/mfa/methods/{methodId}",
  "contract": "identity",
  "summary": "Remove an MFA method",
  "permission": null,
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
  "responds": null
 },
 "semanticSearch": {
  "method": "POST",
  "path": "/search",
  "contract": "ai",
  "summary": "Search meaning, not words",
  "permission": "AI_USE",
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
  "responds": "SearchResult"
 },
 "sendStaffMessage": {
  "method": "POST",
  "path": "/staff-messages",
  "contract": "workforce",
  "summary": "Send a message to a colleague or a small group",
  "permission": "WORKFORCE_VIEW",
  "offlineCapable": true,
  "conflictPolicy": "append",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "WorkforceSendStaffMessageRequest",
  "responds": "WorkforceStaffMessage"
 },
 "verifyMfaEnrolment": {
  "method": "POST",
  "path": "/auth/mfa/methods/{methodId}",
  "contract": "identity",
  "summary": "Complete enrolment",
  "permission": null,
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
  "responds": "MfaMethod"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "Announcement": {
  "type": "object",
  "x-ticvai-persistence": "workforce.announcement",
  "required": [
   "title",
   "body",
   "kind",
   "publishedAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "title": {
    "type": "string",
    "maxLength": 140
   },
   "body": {
    "type": "string",
    "maxLength": 4000
   },
   "kind": {
    "$ref": "#/components/schemas/AnnouncementKind"
   },
   "venueIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "departmentIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "roleIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "requiresAcknowledgement": {
    "type": "boolean"
   },
   "deliveryChannels": {
    "type": "array",
    "description": "How it reaches people (29 September, build, 18.1.5). `inApp` always; `push` to the targeted people's registered staff phones (tenancy `RegisteredDevice`, kind `mobileHandset`). `emergency` is sent by both whatever is set here.\n",
    "items": {
     "type": "string",
     "enum": [
      "inApp",
      "push"
     ]
    },
    "default": [
     "inApp",
     "push"
    ]
   },
   "expiresAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "publishedByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "publishedAt": {
    "type": "string",
    "format": "date-time"
   },
   "locale": {
    "type": "string",
    "nullable": true
   }
  }
 },
 "AnnouncementKind": {
  "type": "string",
  "description": "`emergency` is not a louder `operational`. It overrides the home screen, bypasses quiet hours, requires acknowledgement, and carries a separate permission.\n",
  "enum": [
   "operational",
   "safety",
   "emergency",
   "hr",
   "celebration"
  ]
 },
 "AnnouncementReach": {
  "type": "object",
  "x-ticvai-persistence": "none — computed from workforce.announcement_receipt",
  "properties": {
   "announcementId": {
    "type": "string",
    "format": "uuid"
   },
   "targeted": {
    "type": "integer"
   },
   "delivered": {
    "type": "integer"
   },
   "acknowledged": {
    "type": "integer"
   },
   "outstanding": {
    "type": "array",
    "description": "**The list that matters.** For an operational notice it measures whether anyone read it; during an emergency it is the roll call.\n",
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
      "onShift": {
       "type": "boolean"
      }
     }
    }
   }
  }
 },
 "AppendEntitlementRequest": {
  "type": "object",
  "x-ticvai-persistence": "none — request only",
  "required": [
   "id",
   "lines",
   "recordedAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "description": "Client-generated UUIDv7 of the new order this creates, and its idempotency key — it must equal the `Idempotency-Key` header."
   },
   "lines": {
    "type": "array",
    "minItems": 1,
    "items": {
     "type": "object",
     "required": [
      "variantId",
      "quantity"
     ],
     "properties": {
      "variantId": {
       "type": "string",
       "format": "uuid"
      },
      "quantity": {
       "type": "integer",
       "minimum": 1
      },
      "performanceId": {
       "type": "string",
       "format": "uuid",
       "nullable": true
      }
     }
    }
   },
   "paymentMethod": {
    "type": "string",
    "enum": [
     "card",
     "cash",
     "wallet",
     "giftCard",
     "chargeToAccount"
    ]
   },
   "note": {
    "type": "string",
    "maxLength": 300
   },
   "recordedAt": {
    "type": "string",
    "format": "date-time"
   }
  }
 },
 "AppendEntitlementResult": {
  "type": "object",
  "x-ticvai-persistence": "none — computed",
  "required": [
   "order",
   "media"
  ],
  "properties": {
   "order": {
    "allOf": [
     {
      "$ref": "#/components/schemas/Order"
     }
    ],
    "description": "A **new** order. The original is untouched — it was paid, receipted and possibly reported on, and editing it would move yesterday's revenue.\n"
   },
   "media": {
    "allOf": [
     {
      "$ref": "#/components/schemas/MediaEntitlements"
     }
    ],
    "description": "The full set now on the media, so the cashier can say what the QR does."
   },
   "addedEntitlementIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   }
  }
 },
 "CreatePaymentRequest": {
  "type": "object",
  "required": [
   "id",
   "orderId",
   "tender",
   "amount",
   "recordedAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "description": "Client-generated UUIDv7 of the payment, and its idempotency key — it must equal the `Idempotency-Key` header."
   },
   "orderId": {
    "type": "string",
    "format": "uuid"
   },
   "tender": {
    "$ref": "#/components/schemas/TenderKind"
   },
   "amount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "tenderCurrency": {
    "type": "string",
    "pattern": "^[A-Z]{3}$",
    "nullable": true,
    "description": "The currency the guest handed over, where it is not the venue's — becomes `Payment.tenderCurrency`. Omit for a payment in the venue's own currency."
   },
   "tenderAmount": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "description": "**What the guest handed over**, in `tenderCurrency` — becomes `Payment.tenderAmount`, one name for one concept (renamed from `tenderedAmount` on 26 September). For cash, change is the difference.\n"
   },
   "walletAuthorisationId": {
    "type": "string",
    "nullable": true,
    "description": "Cross-cell wallet hold, where the guest's home cell is elsewhere."
   },
   "walletHoldId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "For a `wallet` tender, the hold `wallet.holdWalletFunds` placed (SD-027). Capture debits it; the order service writes no wallet table."
   },
   "returnUrl": {
    "type": "string",
    "format": "uri",
    "nullable": true,
    "description": "Where the provider returns the guest after a 3-D Secure challenge or hosted page (SD-034). Required for a card payment from the guest web or app."
   },
   "terminalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The card terminal to instruct, for a card payment at a till (ECR flow, SD-034)."
   },
   "deviceId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "recordedAt": {
    "type": "string",
    "format": "date-time"
   }
  }
 },
 "DeviceCapability": {
  "type": "string",
  "description": "BL-179. **Something a driver reports, not something the platform provides.** The list grows as vendors are added, which is ADR-0015's whole position: adding a vendor is a driver plus configuration rather than a core change.\n**`genderClassification` is here because `VenueSettings.segregatedAccess. genderVerification` already offers `deviceAssisted` and nothing answered it** — a switch with no driver behind it. Where a venue's access hardware performs the check and the venue chooses to use it, the result is **advisory to the steward and never decisive at the turnstile** (`ValidationResult.advisory`). 3.2.45 asks for rejection; the package deviates deliberately and CF-130 records why.\n",
  "enum": [
   "genderClassification"
  ]
 },
 "DeviceKind": {
  "type": "string",
  "enum": [
   "receiptPrinter",
   "ticketPrinter",
   "labelPrinter",
   "cashDrawer",
   "barcodeScanner",
   "rfidReader",
   "nfcReader",
   "cardReader",
   "idReader",
   "biometricReader",
   "accessReader",
   "paymentTerminal",
   "customerDisplay",
   "signageDisplay",
   "kitchenDisplay",
   "turnstileController",
   "wristbandEncoder",
   "signaturePad",
   "scale",
   "camera",
   "mobileHandset"
  ],
  "description": "`mobileHandset` (18.1.5, added 29 September): a staff phone or tablet running the staff app, registered for push and bound to no workstation.\n"
 },
 "EntitlementStatus": {
  "type": "string",
  "description": "**What the storage layer holds, and what a guest is shown.** `MediaEntitlements` carried only `isValid` and a reason string — a boolean cannot distinguish a ticket that was used from one that expired, was refunded, or was transferred to somebody else, and those are four different conversations at a gate.\nAdded 17 August. `states/entitlement.yaml` had modelled these six since 14 August and the contract had no enum behind it, which the state checker reported correctly for three days.\n",
  "enum": [
   "issued",
   "partiallyConsumed",
   "fullyConsumed",
   "expired",
   "cancelled",
   "surrendered"
  ]
 },
 "ExchangeRateDecimal": {
  "type": "string",
  "x-ticvai-persistence-kind": "valueObject",
  "x-ticvai-persistence-column": "numeric(18,6)",
  "description": "**An exchange rate: a decimal string, never a float**, for the reason `Money.amount` is one — a JavaScript client must not round a rate in transit. **Six decimal places**, the precision `finance.FxRate.rate` asks for, and stored at that precision.\n",
  "pattern": "^\\d+(\\.\\d{1,6})?$"
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
 "MediaEntitlements": {
  "type": "object",
  "x-ticvai-persistence": "none — projection over entitlement and scan history",
  "required": [
   "mediaCode",
   "isValid",
   "entitlements"
  ],
  "properties": {
   "mediaCode": {
    "type": "string"
   },
   "mediaKind": {
    "type": "string",
    "enum": [
     "qr",
     "wristband",
     "card",
     "nfc",
     "mobilePass"
    ]
   },
   "subjectId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "isValid": {
    "type": "boolean"
   },
   "invalidReason": {
    "type": "string",
    "nullable": true
   },
   "canAcceptMore": {
    "type": "boolean",
    "description": "False where the media has been surrendered, expired or blocked. A cashier should know before taking money, not after.\n"
   },
   "entitlements": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "entitlementId": {
       "type": "string",
       "format": "uuid"
      },
      "name": {
       "type": "string"
      },
      "kind": {
       "type": "string",
       "enum": [
        "admission",
        "locker",
        "fnb",
        "retail",
        "parking",
        "rental",
        "experience",
        "membership"
       ]
      },
      "orderId": {
       "type": "string",
       "format": "uuid"
      },
      "addedAt": {
       "type": "string",
       "format": "date-time"
      },
      "status": {
       "allOf": [
        {
         "$ref": "#/components/schemas/EntitlementStatus"
        }
       ],
       "description": "**Replaced `isRedeemed` on 17 August.** A boolean could not distinguish a ticket that was used from one that expired, was refunded, or was transferred — four different conversations at a gate, and the steward could see only \"not valid\".\n"
      },
      "entriesUsed": {
       "type": "integer"
      },
      "entriesAllowed": {
       "type": "integer",
       "nullable": true
      },
      "redeemedAt": {
       "type": "string",
       "format": "date-time",
       "nullable": true
      },
      "transferredToSubjectId": {
       "type": "string",
       "format": "uuid",
       "nullable": true
      },
      "validTo": {
       "type": "string",
       "format": "date-time",
       "nullable": true
      }
     }
    }
   }
  }
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
 "MfaEnrolment": {
  "x-ticvai-persistence": "none — transient",
  "type": "object",
  "required": [
   "methodId",
   "kind"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "description": "**Added 20 August.** The table had no key at all — no id, no parent and no natural key, so **no row could be addressed, updated or deleted.** The response schema returned everything a caller needs and not the row's own identity, which is the difference between an API response and a table.\n"
   },
   "methodId": {
    "type": "string",
    "format": "uuid"
   },
   "kind": {
    "$ref": "#/components/schemas/MfaKind"
   },
   "secret": {
    "type": "string",
    "nullable": true,
    "description": "TOTP shared secret. Returned once, at enrolment, and never again."
   },
   "qrCodeUri": {
    "type": "string",
    "nullable": true
   },
   "recoveryCodes": {
    "type": "array",
    "description": "Returned once, in this enrolment response (`enrolMfaMethod` writes them, hashed, to `identity.mfa_recovery_code`). Not retrievable afterwards — `verifyMfaEnrolment` does not return them.\n",
    "items": {
     "type": "string"
    }
   },
   "expiresAt": {
    "type": "string",
    "format": "date-time"
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
 "Order": {
  "x-ticvai-persistence": "orders.sales_order + orders.order_line",
  "type": "object",
  "required": [
   "id",
   "venueId",
   "scopePath",
   "channel",
   "status",
   "currency",
   "currencyScale",
   "grossAmount",
   "taxAmount",
   "netAmount",
   "lines",
   "createdAt",
   "recordedAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "description": "The client UUIDv7 from `CreateOrderRequest.id`."
   },
   "orderNumber": {
    "type": "string",
    "readOnly": true,
    "description": "The number a guest reads and a cashier types. **Server-assigned: the venue prefix and a sequence per venue**, for example `DXB1-000123` (decided 28 September, audit R152). A till holds a reserved range of the venue sequence, so an order taken offline gets its number on the till and keeps it through `syncOrders`. **Not gapless**: an unused reserved range leaves a gap, and that is allowed. Only tax invoices are gapless, per legal entity. The receipt carries this number.\n"
   },
   "channel": {
    "allOf": [
     {
      "$ref": "#/components/schemas/OrderChannel"
     }
    ],
    "description": "Where it came from. Drives revenue attribution, promotion eligibility and the self-service adoption figures the operator will ask for within a month of launch.\n"
   },
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "scopePath": {
    "type": "string"
   },
   "status": {
    "$ref": "#/components/schemas/OrderStatus"
   },
   "currency": {
    "type": "string",
    "pattern": "^[A-Z]{3}$",
    "x-ticvai-persisted": false,
    "description": "**Resolved from the region, not stored** (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and cannot be anything else. **Kept on the wire , removed from the table** — a client should not walk a hierarchy to read a figure, and the  database should not hold nine million copies of AED. Four tables genuinely differ from their\n region and keep a stored currency: `orders.payment.tender_currency`, `inventory.supplier`, \n`ledger.account`, `control.partner_agreement`.\n"
   },
   "currencyScale": {
    "type": "integer",
    "minimum": 0,
    "maximum": 4,
    "x-ticvai-persisted": false,
    "description": "**Resolved from the region, not stored** (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and cannot be anything else — storing it per ro w is a copy of a fact that cannot differ. **Kept on the wire, removed from the table**: a cl ient reading a figure should not walk a hierarchy to know what it means, and the database sh ould not hold nine million copies of AED. Four tables genuinely differ from their region and\n keep a stored currency — `orders.payment.tender_currency`, `inventory.supplier`, `ledger.ac\ncount`, `control.partner_agreement`. **A guest paying USD at an AED venue is a real row; a w orkstation with its own currency is a misconfiguration.**\n"
   },
   "grossAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "taxAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "netAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "refundedAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "droppedPromotions": {
    "type": "array",
    "readOnly": true,
    "x-ticvai-persisted": false,
    "description": "**Promotions left off this order at checkout because their budget cap would have been exceeded** (decided 28 September, audit R101 (8)). Empty when none was dropped. Returned by `checkoutCart` and `createOrder`, not stored.\n",
    "items": {
     "type": "object",
     "required": [
      "promotionId"
     ],
     "properties": {
      "promotionId": {
       "type": "string",
       "format": "uuid"
      },
      "name": {
       "type": "string"
      },
      "reason": {
       "type": "string",
       "enum": [
        "budgetCapReached"
       ]
      }
     }
    }
   },
   "totalPriceVariance": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "description": "Sum across lines. Zero on a normal order."
   },
   "lines": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/OrderLine"
    }
   },
   "payments": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/Payment"
    }
   },
   "principalId": {
    "type": "string",
    "format": "uuid"
   },
   "workstationId": {
    "type": "string",
    "format": "uuid"
   },
   "shiftId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "subjectId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "holdLabel": {
    "type": "string",
    "maxLength": 60,
    "nullable": true,
    "readOnly": true,
    "description": "The `label` a cashier gave when parking it with `holdOrder` — how they find it again. Null on an order never held."
   },
   "heldUntil": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true,
    "description": "When a held order expires and is voided (states/order.yaml), from `holdOrder`'s `holdUntil`. Null on an order not currently held."
   },
   "createdAt": {
    "type": "string",
    "format": "date-time"
   },
   "recordedAt": {
    "type": "string",
    "format": "date-time"
   },
   "syncedAt": {
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
 "Payment": {
  "x-ticvai-persistence": "orders.payment",
  "type": "object",
  "required": [
   "id",
   "orderId",
   "tender",
   "amount",
   "status",
   "recordedAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "orderId": {
    "type": "string",
    "format": "uuid"
   },
   "tender": {
    "$ref": "#/components/schemas/TenderKind"
   },
   "tenderCurrency": {
    "type": "string",
    "pattern": "^[A-Z]{3}$",
    "description": "4.6.11. **What the guest actually handed over**, which is not always what the venue books. A tourist paying USD cash at a till is a foreign tender; the sale is still recorded in base currency.\nEqual to the base currency for almost every payment. **Present on all of them so the foreign-tender report has a source** — `getForeignTenderReport` promised *what was taken in which currency* and nothing recorded it until 18 August.\n"
   },
   "tenderAmount": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "description": "The amount in `tenderCurrency`, at that currency's own scale."
   },
   "fxRate": {
    "allOf": [
     {
      "$ref": "#/components/schemas/ExchangeRateDecimal"
     }
    ],
    "nullable": true,
    "description": "The rate applied, **stored on the payment rather than looked up later** (CF-37). A payment reconciled next month is reconciled at the rate of the day it was taken.\n"
   },
   "fxRateSource": {
    "type": "string",
    "nullable": true,
    "enum": [
     "manual",
     "feed",
     "cardScheme"
    ],
    "description": "4.2.8. Manual or fed on a schedule. **`cardScheme` is where the terminal did the conversion and told us** — dynamic currency conversion, the scheme's rate rather than ours.\n"
   },
   "changeCurrency": {
    "type": "string",
    "pattern": "^[A-Z]{3}$",
    "nullable": true,
    "description": "4.6.11 is deliberately asymmetric: **accept foreign currency, refund in local.** A till giving change in five currencies needs five floats and five counts, and the variance becomes unattributable.\n"
   },
   "amount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "changeAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "status": {
    "type": "string",
    "enum": [
     "authorised",
     "captured",
     "pendingConfirmation",
     "declined",
     "failed",
     "voided",
     "refunded"
    ]
   },
   "providerName": {
    "type": "string",
    "nullable": true
   },
   "providerReference": {
    "type": "string",
    "nullable": true,
    "description": "The provider's own id for the charge (Stripe PaymentIntent, NI order reference). What `payments.receivePaymentProviderWebhook` matches an incoming event on (SD-034)."
   },
   "providerIdempotencyKey": {
    "type": "string",
    "nullable": true,
    "readOnly": true,
    "description": "The idempotency key sent to the provider, which is this payment's `id` (SD-034, 29 September). A retried provider call cannot charge twice."
   },
   "terminalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The card terminal a till payment ran on (ECR flow, SD-034)."
   },
   "nextAction": {
    "type": "object",
    "nullable": true,
    "x-ticvai-persisted": false,
    "description": "**What the caller does while the payment is `pendingConfirmation`** (SD-034, 29 September). `redirect`: send the browser to `url` (3-D Secure challenge or hosted page); the provider returns the guest to `returnUrl` and the result arrives by webhook. `terminal`: the card terminal has been instructed; wait for its result. Null once the payment has an outcome.",
    "properties": {
     "kind": {
      "type": "string",
      "enum": [
       "redirect",
       "terminal"
      ]
     },
     "url": {
      "type": "string",
      "format": "uri",
      "nullable": true
     },
     "expiresAt": {
      "type": "string",
      "format": "date-time",
      "nullable": true
     }
    }
   },
   "lastInquiryAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "recordedAt": {
    "type": "string",
    "format": "date-time"
   },
   "syncedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   }
  }
 },
 "RegisteredDevice": {
  "x-ticvai-persistence": "platform.device",
  "type": "object",
  "description": "**The device register of record** (decided 29 September, build pass). Identity, enrolment, credential, firmware and push registration for every device in the estate live on this row. `access.access_device` places access-control devices in the gate topology and repeats serial, versions, health and lifecycle; the two are not merged yet, and where they disagree this row wins.\n",
  "required": [
   "id",
   "kind",
   "driver"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "kind": {
    "$ref": "#/components/schemas/DeviceKind"
   },
   "driver": {
    "type": "string",
    "description": "Built to an open standard where one exists — ESC/POS, UnifiedPOS, OSDP. Adding a vendor is a driver plus configuration, not a core change (ADR-0015).\n"
   },
   "identifier": {
    "type": "string",
    "nullable": true
   },
   "workstationId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Required for every kind except `mobileHandset`, which is bound to no workstation (18.1.5, 29 September); `registerDevice` refuses either mistake with `422`.\n"
   },
   "model": {
    "type": "string",
    "nullable": true
   },
   "pushToken": {
    "type": "string",
    "format": "password",
    "nullable": true,
    "writeOnly": true,
    "description": "BL-163. **Guest devices register for push and staff devices did not** — `registerGuestDevice` exists with a token, platform and failure count, and a scanner that cannot be told anything is a scanner somebody has to walk to.\nWrite-only, and marked `writeOnly`: accepted by `registerDevice` and never returned by `listDevices` or `getDevice`. **A push token is a credential**, and the rule that no surface holds a provider key applies here too.\n"
   },
   "pushPlatform": {
    "type": "string",
    "nullable": true,
    "enum": [
     "ios",
     "android",
     "web",
     "windows"
    ]
   },
   "pushFailureCount": {
    "type": "integer",
    "default": 0,
    "readOnly": true,
    "description": "**Consecutive failures.** A token that has failed repeatedly is a device that was wiped or reassigned, and continuing to push to it is how a notification queue fills with nothing.\n"
   },
   "offlineScope": {
    "type": "string",
    "nullable": true,
    "enum": [
     "none",
     "readOnly",
     "sellAndScan",
     "fullVenue"
    ],
    "description": "BL-163. **What this device may do with no connection**, which was unstated for the staff app while `venue-pos` and `venue-scanner` had it settled.\n**`fullVenue` on a personal handset is a decision, not a default** — a device that can do everything offline is a device that carries the whole venue's data in somebody's pocket.\n"
   },
   "firmwareVersion": {
    "type": "string",
    "nullable": true,
    "readOnly": true,
    "description": "As the device last reported it on its heartbeat."
   },
   "isRequired": {
    "type": "boolean",
    "description": "True blocks shift open when the device is unreachable."
   },
   "status": {
    "type": "string",
    "readOnly": true,
    "enum": [
     "online",
     "offline",
     "error",
     "consumableLow",
     "needsAttention",
     "unknown"
    ],
    "description": "What the device last said on its heartbeat; `unknown` until it has."
   },
   "batteryPercent": {
    "type": "integer",
    "nullable": true,
    "readOnly": true,
    "minimum": 0,
    "maximum": 100,
    "description": "Board 1 of the client's POS design set, 20 August. **A wristband encoder at 8% is a gate that stops working in an hour**, and nothing in the package carried it.\n**Null where the device has no battery**, which is most of them — a receipt printer reporting 100% forever is worse than one reporting nothing.\n"
   },
   "lastCheckedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true,
    "description": "**Distinct from `lastHeartbeatAt`.** A heartbeat is the workstation saying the device is attached; a check is the device answering. **A printer with no paper heartbeats perfectly**, which is why the client's board shows both columns.\n"
   },
   "health": {
    "type": "string",
    "enum": [
     "healthy",
     "warning",
     "degraded",
     "offline",
     "unknown"
    ],
    "default": "unknown",
    "readOnly": true,
    "description": "**Derived, not reported.** Computed from heartbeat age, battery, firmware currency and error rate — a device does not know whether it is healthy, and asking it produces a fleet that is 100% healthy and 12% broken.\n"
   },
   "lastHeartbeatAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true
   },
   "capabilities": {
    "type": "array",
    "readOnly": true,
    "items": {
     "$ref": "#/components/schemas/DeviceCapability"
    },
    "description": "BL-179. **What this driver reports it can do, beyond reading media.** ADR-0015 is standards-first — the device does what the device does — and until now a venue could switch on a feature that depended on hardware without anything being able to say whether the hardware was there.\n**A capability absent is a capability unavailable**, not a capability assumed. A venue setting that requires one is refused where no device in scope reports it, rather than silently doing nothing at the gate.\n"
   },
   "enrolmentState": {
    "type": "string",
    "enum": [
     "registered",
     "enrolled",
     "provisioned",
     "active",
     "deactivated",
     "retired"
    ],
    "default": "registered",
    "readOnly": true,
    "description": "BL-160. **Where the device is in its life, which is not the same question as whether it is answering.** `enrolDevice` has taken the whole matrix — registered, enrolled, provisioned, active, deactivated, retired — since 16.1.2, and until now there was no column for it to land in, so the operation read this table and wrote nothing.\n**Distinct from `status` and from `health`.** `status` is what the device last said and `health` is what we computed from it; a decommissioned turnstile still sitting on the network is `online` and `retired` at once, and neither column contradicts the other. **A device that is `retired` is refused at the gate whatever its status says.**\nThe transition itself — who moved it, from what, and why — is a `tenancy.device_audit` record. It is not repeated here, because the latest transition stored in two places is one place to go stale.\n"
   },
   "retiredAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true,
    "description": "**Set when `enrolmentState` reaches `retired`, and null otherwise.** Derivable from `tenancy.device_audit`, and kept as a column for the same reason `maintenance.asset.retired_on` is one: a retirement date you reconstruct from an audit log is a date nobody filters a fleet by.\n"
   },
   "configurationProfileId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true,
    "description": "**The profile this device was provisioned with.** `enrolDevice` has accepted one since 16.1.3 and there was nowhere to keep it, so the answer to *\"what is this reader configured as\"* lived only in the request that set it.\n"
   }
  }
 },
 "SearchResult": {
  "type": "object",
  "x-ticvai-persistence": "none — computed",
  "properties": {
   "kind": {
    "type": "string"
   },
   "id": {
    "type": "string"
   },
   "title": {
    "type": "string"
   },
   "excerpt": {
    "type": "string"
   },
   "relevance": {
    "type": "number"
   },
   "collectionId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "scopePath": {
    "type": "string"
   },
   "assetId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "For kind `media`, the asset (29 September, build; 23.1.6)."
   },
   "mediaType": {
    "type": "string",
    "nullable": true,
    "enum": [
     "image",
     "video",
     "audio",
     "document"
    ]
   },
   "matchedOn": {
    "type": "string",
    "nullable": true,
    "enum": [
     "title",
     "description",
     "tags",
     "aiDescription"
    ],
    "description": "Which text the match came from, so a wrong hit can be traced to a wrong tag."
   }
  }
 },
 "Session": {
  "type": "object",
  "required": [
   "sessionId",
   "principalId",
   "roleId",
   "scope",
   "effectivePermissions",
   "saleBoardId"
  ],
  "properties": {
   "sessionId": {
    "type": "string",
    "format": "uuid"
   },
   "principalId": {
    "type": "string",
    "format": "uuid"
   },
   "roleId": {
    "type": "string",
    "format": "uuid"
   },
   "displayName": {
    "type": "string"
   },
   "scope": {
    "type": "array",
    "description": "Scope nodes this session may act within, resolved once at login from the ltree hierarchy with deny-overrides-allow. Clients filter navigation against this — they never compute it.\n",
    "items": {
     "$ref": "../shared/common.yaml#/components/schemas/ScopeRef"
    }
   },
   "effectivePermissions": {
    "allOf": [
     {
      "$ref": "../shared/permissions.yaml#/components/schemas/PermissionSet"
     }
    ],
    "description": "Flattened set across all granted scopes, after deny resolution. Convenience for coarse checks. Anything scope-sensitive must use `permissionsByScope`.\n"
   },
   "permissionsByScope": {
    "type": "array",
    "description": "Permissions effective at each granted scope path. Clients filter navigation on this and never compute permissions themselves.\n",
    "items": {
     "$ref": "../shared/permissions.yaml#/components/schemas/ScopedPermissions"
    }
   },
   "saleBoardId": {
    "type": "string",
    "format": "uuid",
    "description": "Landing surface, derived from the WORKSTATION, not the role (12 Aug 2026 §3). Ticketing, F&B or Retail board.\n"
   },
   "workstation": {
    "$ref": "#/components/schemas/WorkstationContext"
   },
   "openedAt": {
    "type": "string",
    "format": "date-time"
   },
   "expiresAt": {
    "type": "string",
    "format": "date-time"
   }
  }
 },
 "SsoProtocol": {
  "type": "string",
  "enum": [
   "oidc",
   "saml2"
  ]
 },
 "SsoProvider": {
  "x-ticvai-persistence": "identity.sso_provider",
  "type": "object",
  "required": [
   "id",
   "displayName",
   "protocol"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "displayName": {
    "type": "string"
   },
   "protocol": {
    "$ref": "#/components/schemas/SsoProtocol"
   },
   "iconAssetRef": {
    "type": "string",
    "nullable": true
   },
   "isEnforced": {
    "type": "boolean",
    "description": "True disables password login for principals covered by this provider."
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `tenant` scope**; the server sets it and ignores it in a request."
   }
  }
 },
 "TenderKind": {
  "type": "string",
  "description": "`wallet` is a **digital wallet** (Apple Pay, Google Pay and the like, taken through the gateway), the value the guest channels accept beside `card` (decided 28 September, audit R080 (a)). **The stored-value TICVAI wallet is a separate tender**: it is spent through `authoriseStoredValue` and `captureStoredValue` (`StoredValueKind` `wallet`), never as this value, so the client can see which of the two the decision meant.\n",
  "enum": [
   "cash",
   "card",
   "wallet",
   "voucher",
   "bankTransfer",
   "hotelCharge",
   "installment",
   "giftCard",
   "complimentary"
  ]
 },
 "TrainingRecord": {
  "type": "object",
  "x-ticvai-persistence": "workforce.training_record",
  "description": "**Drafted 4 September.** One person, one course, one outcome. **The field that matters is the expiry** - a lapsed food-safety or first-aid certificate is a person who may not work a station, and a list without it is a list nobody can roster from.",
  "required": [
   "id"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "principalId": {
    "type": "string",
    "format": "uuid"
   },
   "courseName": {
    "type": "string"
   },
   "required": {
    "type": "boolean"
   },
   "completedAt": {
    "type": "string",
    "format": "date-time"
   },
   "expiresAt": {
    "type": "string",
    "format": "date-time"
   },
   "state": {
    "type": "string",
    "enum": [
     "notStarted",
     "inProgress",
     "passed",
     "failed",
     "expired"
    ]
   },
   "evidenceRef": {
    "type": "string"
   }
  }
 },
 "WorkforceSendStaffMessageRequest": {
  "type": "object",
  "x-ticvai-persistence": "none — request only",
  "required": [
   "id",
   "body",
   "sentAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "description": "Client-generated UUIDv7; a replay of the same id returns the stored message."
   },
   "conversationId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "An existing conversation the caller is in. Absent means `recipientPrincipalIds`."
   },
   "recipientPrincipalIds": {
    "type": "array",
    "maxItems": 49,
    "items": {
     "type": "string",
     "format": "uuid"
    },
    "description": "Colleagues to message when there is no `conversationId`. One reuses the direct conversation; several start a group."
   },
   "title": {
    "type": "string",
    "maxLength": 120,
    "nullable": true,
    "description": "A new group's title; ignored otherwise."
   },
   "body": {
    "type": "string",
    "minLength": 1,
    "maxLength": 2000
   },
   "attachmentAssetId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "sentAt": {
    "type": "string",
    "format": "date-time"
   }
  }
 },
 "WorkforceStaffConversation": {
  "type": "object",
  "x-ticvai-persistence": "workforce.staff_conversation",
  "description": "**One direct or group conversation between staff of a venue** (18.9.5 Internal Messaging; decided 29 September, build pass). Created by `sendStaffMessage` the first time colleagues are messaged; its participants are `workforce.staff_conversation_participant` rows. Announcements stay the one-to-many channel; this is the one-to-one and small-group one.",
  "required": [
   "id",
   "venueId",
   "kind",
   "createdByPrincipalId",
   "createdAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "scopePath": {
    "type": "string"
   },
   "kind": {
    "type": "string",
    "enum": [
     "direct",
     "group"
    ],
    "description": "A direct conversation has exactly two participants and at most one exists per pair."
   },
   "title": {
    "type": "string",
    "maxLength": 120,
    "nullable": true,
    "description": "Group conversations only; null on a direct one."
   },
   "createdByPrincipalId": {
    "type": "string",
    "format": "uuid"
   },
   "createdAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   },
   "lastMessageAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true
   }
  }
 },
 "WorkforceStaffConversationSummary": {
  "type": "object",
  "x-ticvai-persistence": "none — projection over workforce.staff_conversation, its participants and its latest message, for the caller",
  "description": "One row of `listStaffConversations`, as the caller sees it.",
  "required": [
   "conversation",
   "unreadCount"
  ],
  "properties": {
   "conversation": {
    "$ref": "#/components/schemas/WorkforceStaffConversation"
   },
   "participants": {
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
      "onShift": {
       "type": "boolean"
      }
     }
    }
   },
   "lastMessage": {
    "allOf": [
     {
      "$ref": "#/components/schemas/WorkforceStaffMessage"
     }
    ],
    "nullable": true
   },
   "unreadCount": {
    "type": "integer",
    "minimum": 0
   }
  }
 },
 "WorkforceStaffMessage": {
  "type": "object",
  "x-ticvai-persistence": "workforce.staff_message",
  "description": "One message in a staff conversation (decided 29 September, build pass). Never edited through the API, so a conversation reads the same to everyone in it afterwards.",
  "required": [
   "id",
   "staffConversationId",
   "senderPrincipalId",
   "body",
   "sentAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "description": "The client-generated UUIDv7 from the send, the key an offline replay deduplicates on."
   },
   "staffConversationId": {
    "type": "string",
    "format": "uuid"
   },
   "senderPrincipalId": {
    "type": "string",
    "format": "uuid"
   },
   "body": {
    "type": "string",
    "maxLength": 2000
   },
   "attachmentAssetId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "A photo or file, held as a media asset."
   },
   "sentAt": {
    "type": "string",
    "format": "date-time",
    "description": "When the sender sent it, which for a message queued offline is before it arrived."
   },
   "receivedAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true,
    "nullable": true
   }
  }
 },
 "WorkstationContext": {
  "type": "object",
  "required": [
   "id",
   "code",
   "venueId",
   "regionId"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "code": {
    "type": "string"
   },
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "regionId": {
    "type": "string",
    "format": "uuid"
   },
   "accessPointId": {
    "type": "string",
    "format": "uuid",
    "description": "Inherited from the workstation, never selected by the operator."
   },
   "devices": {
    "type": "array",
    "items": {
     "type": "object",
     "required": [
      "kind",
      "driver"
     ],
     "properties": {
      "kind": {
       "type": "string",
       "enum": [
        "receiptPrinter",
        "ticketPrinter",
        "cashDrawer",
        "barcodeScanner",
        "rfidReader",
        "paymentTerminal",
        "customerDisplay"
       ]
      },
      "driver": {
       "type": "string"
      },
      "identifier": {
       "type": "string"
      }
     }
    }
   },
   "currency": {
    "type": "string",
    "pattern": "^[A-Z]{3}$"
   },
   "currencyScale": {
    "type": "integer",
    "minimum": 0,
    "maximum": 4
   },
   "timezone": {
    "type": "string"
   },
   "cellName": {
    "type": "string",
    "description": "The cell serving this workstation's region. One cell per tenant per region (ADR-0014). A client uses this only for diagnostics and telemetry tagging — never for routing, which the Control Plane resolves.\n"
   },
   "deploymentProfile": {
    "type": "string",
    "enum": [
     "terminalLocal",
     "venueEdge",
     "thin"
    ],
    "description": "Whether this surface reads catalogue locally (ADR-0013). Determines which flows the client enables offline.\n"
   }
  }
 }
}
```
