# P02-engagement-support-01 — P02 · Engagement & Support (1 of 2)

**10 screens · 30 operations · 77 schemas · 4 permissions**

Platform P02 Guest App · ships as **guest** ·
guest audience · mobileApp ·
offline-capable

## Who this is for

**guest on mobileApp.** Everything below is how you know what is
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
  `AI_USE, CASE_MANAGE, PRODUCT_VIEW, TENANT_CONFIGURE`. A control nobody can use must say so,
  not sit enabled and fail.
- **9 of these operations work offline**: getTenantAppStatus, getVisitPlan, getWaitTimes, listCatalogueBundles, listContentPages, listFaqs, listMyNotifications, listProducts
  — and the rest do not. A surface that looks the same online and off is lying.
- **Offline, every screen shows one banner, the same on web and app:** *"You're offline. Connect to the internet to book, pay, order or join a queue."* The moment the connection drops, on every screen, above the screen's own content. By itself as soon as the connection is back, with a short "Back online" confirmation. **It never** Covers what is already on screen, or appears for a server error — that is the screen's own error state, and a guest told they are offline when the venue is down reconnects for nothing. Each screen's `states.offline` says what stays on screen and what waits.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `GST-030` | In-Venue Notifications | configEditor | 3 | 0 | — |
| `GST-031` | AI Concierge – Home | statusTracker | 5 | 4 | — |
| `GST-032` | AI Concierge – Chat | statusTracker | 9 | 6 | — |
| `GST-033` | AI Concierge – Contextual Help | configEditor | 1 | 0 | — |
| `GST-035` | Feedback & Ratings | configEditor | 2 | 1 | — |
| `GST-040` | Help & Support | commandCentre | 6 | 2 | — |
| `GST-051` | Plan | multiStepForm | 4 | 0 | — |
| `GST-052` | Suggested Itineraries | listDetail | 3 | 0 | — |
| `GST-053` | Your Plan | listDetail | 7 | 0 | — |
| `GST-054` | AI Planner | listDetail | 6 | 0 | yes |

## Thin screens in this batch

**GST-033, GST-052 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "GST-030",
  "name": "In-Venue Notifications",
  "module": "Engagement & Support",
  "requiresModule": "fnb",
  "wave": 2,
  "capability": "C61",
  "implementation": {
   "app": "guest-app",
   "route": "/general/in-venue-notifications",
   "component": "apps/guest-app/src/routes/general/InVenueNotificationsDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "GST-001",
    "GST-025"
   ],
   "inferred": true,
   "exitTo": [
    "GST-001",
    "GST-002",
    "GST-031"
   ],
   "fromFlows": true,
   "transitions": [
    {
     "to": "GST-001",
     "trigger": "Home – Default",
     "provenance": "derived — GST-001 declares entryState.params  and GST-030 holds none of them. The edge carries nothing: GST-030 is opened from GST-001, so this edge is the way back and GST-001 keeps its own state"
    },
    {
     "to": "GST-031",
     "trigger": "AI Concierge – Home",
     "carries": [
      "outletId"
     ],
     "provenance": "derived — GST-031 declares entryState.params conversationId, outletId and GST-030 holds outletId, so an edge into it carries them"
    }
   ]
  },
  "notes": "States derived from the screen pattern on 17 August, not individually considered. Purpose derived from the screen name and its operations on 17 August, not from a requirement. **Back in the first release** (decided 29 September, rev 3 GAP-C1): the notifications feed is needed in the first release, which reverses audit R242's deferral of this screen. The `deferred` block is removed and the screen returns to `wave: 2`, where it sat before R242. Queue calls and order status still also show on the queue and order screens, which poll.",
  "density": "comfortable",
  "pattern": "configEditor",
  "patternReason": "`listMyNotifications` reads the feed (decided 29 September, rev 3 GAP-C1); the location-session claim stays a form on the same screen, so the pattern is kept until the screen is redrawn",
  "purpose": "Work with in-venue notifications for this venue.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Claim location session",
       "operation": "claimLocationSession",
       "provenance": "contract fnb.yaml POST /location-sessions"
      },
      {
       "kind": "secondaryButton",
       "label": "Mark all as read",
       "operation": "markMyNotificationsRead",
       "notes": "Sends `{all: true}`. Only the guest's own notifications are marked.",
       "provenance": "contract marketing-crm.yaml POST /me/notifications/read"
      }
     ]
    },
    {
     "name": "contentBody",
     "components": [
      {
       "kind": "textField",
       "label": "Location code",
       "operation": "claimLocationSession",
       "provenance": "contract fnb.yaml POST /location-sessions"
      },
      {
       "kind": "textField",
       "label": "Seat reference",
       "operation": "claimLocationSession",
       "provenance": "contract fnb.yaml POST /location-sessions"
      },
      {
       "kind": "numberField",
       "label": "Party size",
       "operation": "claimLocationSession",
       "provenance": "contract fnb.yaml POST /location-sessions"
      },
      {
       "kind": "cardList",
       "label": "Notifications",
       "bindsTo": "GuestNotification",
       "operation": "listMyNotifications",
       "notes": "**Newest first, unread ones marked.** Each card shows the kind, title, body and when it was queued; tapping one opens its `deepLink` (an order, a queue ticket, a booking) and marks it read. `unreadCount` is the badge on the tab. Sends `?venueId=` for the venue the guest picked.",
       "provenance": "contract marketing-crm.yaml GET /me/notifications (decided 29 September, rev 3 GAP-C1)"
      },
      {
       "kind": "toggle",
       "label": "Unread only",
       "operation": "listMyNotifications",
       "notes": "Sends `?unreadOnly=` to `listMyNotifications`.",
       "provenance": "contract marketing-crm.yaml GET /me/notifications"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The notification feed.",
   "error": "Could not load. Names which read failed and leaves the in-venue notifications untouched.",
   "emptyFirstRun": "**No notifications yet.** Queue calls, order updates and venue notices appear here as the venue sends them.",
   "offline": "**The offline banner shows.** Notices already received stay listed. New queue calls and order updates arrive once the connection is back, and the banner is the warning that they may be late.",
   "emptyNoResults": "**No unread notifications.** Names the Unread only filter and offers to show all; the read ones are still there."
  },
  "apis": [
   {
    "operationId": "claimLocationSession",
    "contract": "fnb",
    "purpose": "From the flow it appears in",
    "trigger": "onAction"
   },
   {
    "operationId": "listMyNotifications",
    "contract": "marketing-crm",
    "purpose": "The guest's notification feed, newest first: queue calls, order ready, booking changes, venue alerts (decided 29 September, rev 3 GAP-C1)",
    "trigger": "onLoad"
   },
   {
    "operationId": "markMyNotificationsRead",
    "contract": "marketing-crm",
    "purpose": "Mark the opened notifications, or all of them, read",
    "trigger": "onAction"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "client-verified",
   "board": "wireframes/P02 Guest App.dc.html#gst-030",
   "prototype": {
    "file": "sources/designs/guest-rev3-28-september/TICVAI Guest Booking Mobile v2.dc.html",
    "rev": "rev 3",
    "verified": "2026-09-28",
    "match": "exact",
    "view": "DEFERRED (R242), still in the prototype: Account → All screens → Wave 2 → In-venue notifications; At-venue tab → Alerts",
    "differences": "The YAML defers this (no in-app notification feed in the first release), but the prototype still shows a feed and an Alerts tab, so the client will expect it."
   }
  },
  "apisNote": "Rebuilt 9 September 2026 from the 1 operation this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "_platform": {
   "code": "P02",
   "audience": "guest",
   "formFactor": "mobileApp",
   "shortName": "Guest App",
   "name": "Guest App — Mobile",
   "offlineCapable": true,
   "offlineBanner": {
    "kind": "banner",
    "state": "warning",
    "message": "You're offline. Connect to the internet to book, pay, order or join a queue.",
    "shows": "The moment the connection drops, on every screen, above the screen's own content.",
    "clears": "By itself as soon as the connection is back, with a short \"Back online\" confirmation.",
    "never": "Covers what is already on screen, or appears for a server error — that is the screen's own error state, and a guest told they are offline when the venue is down reconnects for nothing.",
    "provenance": "Decided 12 September 2026 — guest web and guest app behave identically offline and say so with the same banner."
   },
   "app": "guest-app",
   "operator": "guest",
   "targetApp": {
    "app": "guest",
    "name": "TICVAI Guest",
    "shell": "mobile",
    "siblings": [
     "P01",
     "P05"
    ],
    "note": "**One guest product in three shells.** Web, mobile and kiosk share 73–91% of their operations; the kiosk is the same product in a fixed frame with no keyboard, and is deliberately narrower rather than different.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "GST-031",
  "name": "AI Concierge – Home",
  "module": "Engagement & Support",
  "requiresModule": "fnb",
  "wave": 2,
  "capability": "AI-02",
  "implementation": {
   "app": "guest-app",
   "route": "/general/ai-concierge-home",
   "component": "apps/guest-app/src/routes/general/AiConciergeHomeDashboard.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "GST-001"
   ],
   "inferred": true,
   "exitTo": [
    "GST-001",
    "GST-002",
    "GST-032"
   ],
   "fromFlows": true,
   "transitions": [
    {
     "to": "GST-001",
     "trigger": "Home – Default",
     "provenance": "derived — GST-001 declares entryState.params  and GST-031 holds none of them. The edge carries nothing: GST-031 is opened from GST-001, so this edge is the way back and GST-001 keeps its own state"
    },
    {
     "to": "GST-032",
     "trigger": "AI Concierge – Chat",
     "carries": [
      "conversationId"
     ],
     "provenance": "derived — GST-032 declares entryState.params conversationId, messageId, orderId and GST-031 holds conversationId, so an edge into it carries them"
    }
   ]
  },
  "notes": "States derived from the screen pattern on 17 August, not individually considered. Purpose derived from the screen name and its operations on 17 August, not from a requirement. **Guest concierge confirmed in Phase 1 on 17 August (CF-14), charged per token and bounded by `AiPolicy.guestCapabilityScope`.** Still degrades to the manual planner rather than to an error. **Cross-surface parity, 31 August**: added createAiConversation, handoverToAgent, requestSuggestion. **A guest does not know which surface they are on** — the same named screen on web and app now calls the same guest-callable operations.\n\n**Rev 3 (decided 29 September).** The concierge shows as mascot art when `BookingFlowConfig.conciergeMascot` is on (default), otherwise a plain button (CFG-5).",
  "density": "comfortable",
  "pattern": "statusTracker",
  "patternReason": "`getGuestMenu` reads one record and nothing reads a population — the screen is about that one thing",
  "purpose": "The screen this app sits on. Everything else is entered from here and returns to it.",
  "layout": {
   "template": "detail",
   "regions": [
    {
     "name": "contentBody",
     "slot": "record",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The guest menu",
       "bindsTo": "GuestMenu",
       "columns": [
        "GuestMenu.outletId",
        "GuestMenu.menuId",
        "GuestMenu.name",
        "GuestMenu.inForceUntil",
        "GuestMenu.currency",
        "GuestMenu.currencyScale",
        "GuestMenu.sections"
       ],
       "operation": "getGuestMenu",
       "provenance": "contract fnb.yaml GET /outlets/{outletId}/guest-menu"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Send AI message",
       "operation": "sendAiMessage",
       "provenance": "contract ai.yaml POST /conversations/{conversationId}/messages"
      },
      {
       "kind": "secondaryButton",
       "label": "Create AI conversation",
       "operation": "createAiConversation",
       "provenance": "contract ai.yaml POST /conversations"
      },
      {
       "kind": "secondaryButton",
       "label": "Handover to agent",
       "operation": "handoverToAgent",
       "provenance": "contract marketing-crm.yaml POST /conversations/{conversationId}/handover"
      },
      {
       "kind": "secondaryButton",
       "label": "Request suggestion",
       "operation": "requestSuggestion",
       "provenance": "contract ai.yaml POST /ai/suggestions"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The concierge home, read by `getGuestMenu`.",
   "error": "Could not load. Names which read failed and leaves the concierge home untouched.",
   "emptyFirstRun": "No concierge home yet. Offers Create AI conversation (`createAiConversation`).",
   "emptyNoAccess": "Shown when the caller lacks `AI_USE`, which `sendAiMessage` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "offline": "**Not available, and the offline banner says why.** The assistant needs the connection; conversations already loaded stay readable."
  },
  "apis": [
   {
    "operationId": "getGuestMenu",
    "contract": "fnb",
    "purpose": "From the flow it appears in",
    "trigger": "onLoad"
   },
   {
    "operationId": "sendAiMessage",
    "contract": "ai",
    "purpose": "Ask",
    "trigger": "onAction"
   },
   {
    "operationId": "createAiConversation",
    "contract": "ai",
    "purpose": "Open a conversation",
    "trigger": "onAction"
   },
   {
    "operationId": "handoverToAgent",
    "contract": "marketing-crm",
    "purpose": "Pass an assistant conversation to a person",
    "trigger": "onAction"
   },
   {
    "operationId": "requestSuggestion",
    "contract": "ai",
    "purpose": "A suggestion of kind prepPlan, upsell or waitTime from the concierge; an itinerary (guest-allowed since 29 September) is asked on the Plan tab (GST-054), not here",
    "trigger": "onAction"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "conversationId",
     "from": "deepLink"
    },
    {
     "name": "outletId",
     "from": "deepLink"
    }
   ],
   "coldEntry": "A conversation link an agent opens from a notification. Resolves, or says it was closed and by whom."
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "designed",
   "board": "wireframes/P02 Guest App.dc.html#gst-031",
   "prototype": {
    "file": "sources/designs/guest-rev3-29-september/TICVAI Mobile App v4.dc.html",
    "rev": "Mobile App v4, 29 September 2026",
    "match": "none",
    "note": "Mobile App v4 has no view for this screen. Drawn by Claude Code on 30 September 2026 in the v4 look (the frame on this screen's board, wireframes/frames/gst-031.html, and #GST-031 in handoff/design-batches/apps/1-guest-app/return/TICVAI Guest App.dc.html). NOT client-verified: awaiting the client's design reviewer. Build the layout from that frame and this definition. Mobile v2 (28 September, superseded by v4) showed it at: Account → All screens → Wave 2 → AI concierge – home (exact)."
   },
   "source": "Claude Code, 30 September 2026, drawn in the Mobile App v4 look",
   "note": "**Drawn by Claude Code on 30 September 2026 in the Mobile App v4 look; not client-verified, awaiting the client's design reviewer.** `provenance: designed` because the accepted vocabulary has no value for an agent-drawn frame; it is the value the eight Claude Design frames of 29 September carry. Gaps the operations leave are in handoff/design-batches/apps/1-guest-app/return/FINDINGS.md."
  },
  "apisNote": "Rebuilt 9 September 2026 from the 5 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "overlays": [
   {
    "id": "formSendAiMessage",
    "component": "modal",
    "trigger": "Send AI message",
    "body": "**Collects what `sendAiMessage` sends before it is called.** Required: `content`. Optional: `collectionIds`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Send AI message",
     "operation": "sendAiMessage"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "content",
      "collectionIds"
     ]
    },
    "provenance": "client-verified"
   },
   {
    "id": "formCreateAiConversation",
    "component": "modal",
    "trigger": "Create AI conversation",
    "body": "**Collects what `createAiConversation` sends before it is called.** Required: `module`. Optional: `locale`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Create AI conversation",
     "operation": "createAiConversation"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "module",
      "locale"
     ]
    },
    "provenance": "client-verified"
   },
   {
    "id": "formHandoverToAgent",
    "component": "modal",
    "trigger": "Handover to agent",
    "body": "**Collects what `handoverToAgent` sends before it is called.** Required: `reason`. Optional: `summary`, `preferredQueueId`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Handover to agent",
     "operation": "handoverToAgent"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "reason",
      "summary",
      "preferredQueueId"
     ]
    },
    "provenance": "client-verified"
   },
   {
    "id": "formRequestSuggestion",
    "component": "modal",
    "trigger": "Request suggestion",
    "body": "**Collects what `requestSuggestion` sends before it is called.** Required: `kind`, offered as `prepPlan`, `upsell` or `waitTime` only — no `scenario`; an itinerary is asked on the Plan tab (GST-054, since 29 September). Optional: `subjectRef`, `horizon`, `context`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Request suggestion",
     "operation": "requestSuggestion"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "kind",
      "subjectRef",
      "horizon",
      "context"
     ]
    },
    "provenance": "client-verified"
   }
  ],
  "_platform": {
   "code": "P02",
   "audience": "guest",
   "formFactor": "mobileApp",
   "shortName": "Guest App",
   "name": "Guest App — Mobile",
   "offlineCapable": true,
   "offlineBanner": {
    "kind": "banner",
    "state": "warning",
    "message": "You're offline. Connect to the internet to book, pay, order or join a queue.",
    "shows": "The moment the connection drops, on every screen, above the screen's own content.",
    "clears": "By itself as soon as the connection is back, with a short \"Back online\" confirmation.",
    "never": "Covers what is already on screen, or appears for a server error — that is the screen's own error state, and a guest told they are offline when the venue is down reconnects for nothing.",
    "provenance": "Decided 12 September 2026 — guest web and guest app behave identically offline and say so with the same banner."
   },
   "app": "guest-app",
   "operator": "guest",
   "targetApp": {
    "app": "guest",
    "name": "TICVAI Guest",
    "shell": "mobile",
    "siblings": [
     "P01",
     "P05"
    ],
    "note": "**One guest product in three shells.** Web, mobile and kiosk share 73–91% of their operations; the kiosk is the same product in a fixed frame with no keyboard, and is deliberately narrower rather than different.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "GST-032",
  "name": "AI Concierge – Chat",
  "module": "Engagement & Support",
  "requiresModule": "ticketing",
  "wave": 2,
  "capability": "AI-02",
  "implementation": {
   "app": "guest-app",
   "route": "/general/ai-concierge-chat",
   "component": "apps/guest-app/src/routes/general/AiConciergeChatDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "GST-001"
   ],
   "inferred": true,
   "exitTo": [
    "GST-001",
    "GST-002",
    "GST-033"
   ],
   "fromFlows": true,
   "transitions": [
    {
     "to": "GST-001",
     "trigger": "Home – Default",
     "provenance": "derived — GST-001 declares entryState.params  and GST-032 holds none of them. The edge carries nothing: GST-032 is opened from GST-001, so this edge is the way back and GST-001 keeps its own state"
    },
    {
     "to": "GST-033",
     "trigger": "AI Concierge – Contextual Help",
     "carries": [
      "conversationId"
     ],
     "provenance": "derived — GST-033 declares entryState.params conversationId and GST-032 holds conversationId, so an edge into it carries them"
    }
   ]
  },
  "notes": "States derived from the screen pattern on 17 August, not individually considered. Purpose derived from the screen name and its operations on 17 August, not from a requirement. **Guest concierge confirmed in Phase 1 on 17 August (CF-14), charged per token and bounded by `AiPolicy.guestCapabilityScope`.** Still degrades to the manual planner rather than to an error.",
  "density": "comfortable",
  "pattern": "statusTracker",
  "patternReason": "`getGuestOrderStatus` reads one record and nothing reads a population — the screen is about that one thing",
  "purpose": "Add ai concierge – chat for this venue.",
  "layout": {
   "template": "detail",
   "regions": [
    {
     "name": "contentBody",
     "slot": "record",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The guest order status",
       "bindsTo": "GuestOrderStatus",
       "columns": [
        "GuestOrderStatus.orderId",
        "GuestOrderStatus.orderNumber",
        "GuestOrderStatus.status",
        "GuestOrderStatus.estimatedReadyAt",
        "GuestOrderStatus.isReadyForCollection",
        "GuestOrderStatus.lines"
       ],
       "operation": "getGuestOrderStatus",
       "provenance": "contract fnb.yaml GET /guest-orders/{orderId}"
      },
      {
       "kind": "detailPanel",
       "label": "The cart",
       "bindsTo": "Cart",
       "columns": [
        "Cart.id",
        "Cart.token",
        "Cart.venueId",
        "Cart.channel",
        "Cart.subjectId",
        "Cart.status",
        "Cart.lines",
        "Cart.conflicts",
        "Cart.subtotal",
        "Cart.discountTotal",
        "Cart.taxTotal",
        "Cart.total",
        "Cart.appliedPromotionIds",
        "Cart.expiresAt",
        "Cart.extensionsUsed",
        "Cart.maxExtensions"
       ],
       "operation": "getCart",
       "provenance": "contract orders.yaml GET /carts/{cartId}"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Create guest F&B order",
       "operation": "createGuestFnbOrder",
       "provenance": "contract fnb.yaml POST /guest-orders"
      },
      {
       "kind": "secondaryButton",
       "label": "Add cart line",
       "operation": "addCartLine",
       "provenance": "contract orders.yaml POST /carts/{cartId}/lines"
      },
      {
       "kind": "secondaryButton",
       "label": "Checkout cart",
       "operation": "checkoutCart",
       "provenance": "contract orders.yaml POST /carts/{cartId}/checkout"
      },
      {
       "kind": "secondaryButton",
       "label": "Send AI message",
       "operation": "sendAiMessage",
       "provenance": "contract ai.yaml POST /conversations/{conversationId}/messages"
      },
      {
       "kind": "secondaryButton",
       "label": "Send conversation message",
       "operation": "sendConversationMessage",
       "provenance": "contract marketing-crm.yaml POST /conversations/{conversationId}/messages"
      },
      {
       "kind": "secondaryButton",
       "label": "Handover to agent",
       "operation": "handoverToAgent",
       "provenance": "contract marketing-crm.yaml POST /conversations/{conversationId}/handover"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The concierge chat, read by `getGuestOrderStatus`.",
   "error": "Could not load. Names which read failed and leaves the concierge chat untouched.",
   "emptyFirstRun": "No concierge chat yet. Offers Create guest F&B order (`createGuestFnbOrder`).",
   "emptyNoAccess": "Shown when the caller lacks `AI_USE`, which `sendAiMessage` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "offline": "**Not available, and the offline banner says why.** The assistant needs the connection; conversations already loaded stay readable."
  },
  "apis": [
   {
    "operationId": "createGuestFnbOrder",
    "contract": "fnb",
    "purpose": "From the flow it appears in",
    "trigger": "onAction"
   },
   {
    "operationId": "getGuestOrderStatus",
    "contract": "fnb",
    "purpose": "Track an order",
    "trigger": "onLoad"
   },
   {
    "operationId": "getCart",
    "contract": "orders",
    "purpose": "The cart, priced and checked, right now",
    "trigger": "onLoad"
   },
   {
    "operationId": "addCartLine",
    "contract": "orders",
    "purpose": "Add something",
    "trigger": "onAction"
   },
   {
    "operationId": "checkoutCart",
    "contract": "orders",
    "purpose": "Turn the cart into an order",
    "trigger": "onAction"
   },
   {
    "operationId": "sendAiMessage",
    "contract": "ai",
    "purpose": "Ask",
    "trigger": "onAction"
   },
   {
    "operationId": "sendConversationMessage",
    "contract": "marketing-crm",
    "purpose": "Say something, as a guest or an agent",
    "trigger": "onAction"
   },
   {
    "operationId": "handoverToAgent",
    "contract": "marketing-crm",
    "purpose": "Pass an assistant conversation to a person",
    "trigger": "onAction"
   },
   {
    "operationId": "recordAnswerFeedback",
    "contract": "ai",
    "purpose": "Say whether an answer helped",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "cartId",
     "from": "session"
    },
    {
     "name": "conversationId",
     "from": "deepLink"
    },
    {
     "name": "orderId",
     "from": "deepLink"
    },
    {
     "name": "messageId",
     "from": "navigation"
    }
   ],
   "coldEntry": "A conversation link an agent opens from a notification. Resolves, or says it was closed and by whom. **A guest opening an order link weeks later.** Shows the order if it still resolves; if it was refunded or the performance passed, says which and offers the order list rather than an error."
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "designed",
   "board": "wireframes/P02 Guest App.dc.html#gst-032",
   "prototype": {
    "file": "sources/designs/guest-rev3-29-september/TICVAI Mobile App v4.dc.html",
    "rev": "Mobile App v4, 29 September 2026",
    "match": "none",
    "note": "Mobile App v4 has no view for this screen. Drawn by Claude Code on 30 September 2026 in the v4 look (the frame on this screen's board, wireframes/frames/gst-032.html, and #GST-032 in handoff/design-batches/apps/1-guest-app/return/TICVAI Guest App.dc.html). NOT client-verified: awaiting the client's design reviewer. Build the layout from that frame and this definition. Mobile v2 (28 September, superseded by v4) showed it at: Account → All screens → Wave 2 → AI concierge – chat (exact)."
   },
   "source": "Claude Code, 30 September 2026, drawn in the Mobile App v4 look",
   "note": "**Drawn by Claude Code on 30 September 2026 in the Mobile App v4 look; not client-verified, awaiting the client's design reviewer.** `provenance: designed` because the accepted vocabulary has no value for an agent-drawn frame; it is the value the eight Claude Design frames of 29 September carry. Gaps the operations leave are in handoff/design-batches/apps/1-guest-app/return/FINDINGS.md."
  },
  "apisNote": "Rebuilt 9 September 2026 from the 8 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "overlays": [
   {
    "id": "formCreateGuestFnbOrder",
    "component": "modal",
    "trigger": "Create guest F&B order",
    "body": "**Collects what `createGuestFnbOrder` sends before it is called.** Required: `id`, `lines`, `quotedTotal`, `recordedAt`. Optional: `locationSessionId`, `outletId`, `fulfilment`, `paymentMethod`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "CreateGuestOrderRequest",
    "confirm": {
     "label": "Create guest F&B order",
     "operation": "createGuestFnbOrder"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "lines",
      "quotedTotal",
      "recordedAt",
      "locationSessionId",
      "outletId",
      "fulfilment",
      "paymentMethod"
     ]
    },
    "provenance": "client-verified"
   },
   {
    "id": "formAddCartLine",
    "component": "modal",
    "trigger": "Add cart line",
    "body": "**Collects what `addCartLine` sends before it is called.** Required: `variantId`, `quantity`. Optional: `performanceId`, `seatIds`, `parentLineId`, `attributes`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "AddCartLineRequest",
    "confirm": {
     "label": "Add cart line",
     "operation": "addCartLine"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "variantId",
      "quantity",
      "performanceId",
      "seatIds",
      "parentLineId",
      "attributes"
     ]
    },
    "provenance": "client-verified"
   },
   {
    "id": "formCheckoutCart",
    "component": "modal",
    "trigger": "Checkout cart",
    "body": "**Collects what `checkoutCart` sends before it is called.** Nothing in the body is required. Optional: `subjectId`, `attendees`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Checkout cart",
     "operation": "checkoutCart"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "subjectId",
      "attendees"
     ]
    },
    "provenance": "client-verified"
   },
   {
    "id": "formSendAiMessage",
    "component": "modal",
    "trigger": "Send AI message",
    "body": "**Collects what `sendAiMessage` sends before it is called.** Required: `content`. Optional: `collectionIds`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Send AI message",
     "operation": "sendAiMessage"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "content",
      "collectionIds"
     ]
    },
    "provenance": "client-verified"
   },
   {
    "id": "formSendConversationMessage",
    "component": "modal",
    "trigger": "Send conversation message",
    "body": "**Collects what `sendConversationMessage` sends before it is called.** Required: `body`. Optional: `attachments`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Send conversation message",
     "operation": "sendConversationMessage"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "body",
      "attachments"
     ]
    },
    "provenance": "client-verified"
   },
   {
    "id": "formHandoverToAgent",
    "component": "modal",
    "trigger": "Handover to agent",
    "body": "**Collects what `handoverToAgent` sends before it is called.** Required: `reason`. Optional: `summary`, `preferredQueueId`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Handover to agent",
     "operation": "handoverToAgent"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "reason",
      "summary",
      "preferredQueueId"
     ]
    },
    "provenance": "client-verified"
   }
  ],
  "_platform": {
   "code": "P02",
   "audience": "guest",
   "formFactor": "mobileApp",
   "shortName": "Guest App",
   "name": "Guest App — Mobile",
   "offlineCapable": true,
   "offlineBanner": {
    "kind": "banner",
    "state": "warning",
    "message": "You're offline. Connect to the internet to book, pay, order or join a queue.",
    "shows": "The moment the connection drops, on every screen, above the screen's own content.",
    "clears": "By itself as soon as the connection is back, with a short \"Back online\" confirmation.",
    "never": "Covers what is already on screen, or appears for a server error — that is the screen's own error state, and a guest told they are offline when the venue is down reconnects for nothing.",
    "provenance": "Decided 12 September 2026 — guest web and guest app behave identically offline and say so with the same banner."
   },
   "app": "guest-app",
   "operator": "guest",
   "targetApp": {
    "app": "guest",
    "name": "TICVAI Guest",
    "shell": "mobile",
    "siblings": [
     "P01",
     "P05"
    ],
    "note": "**One guest product in three shells.** Web, mobile and kiosk share 73–91% of their operations; the kiosk is the same product in a fixed frame with no keyboard, and is deliberately narrower rather than different.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "GST-033",
  "name": "AI Concierge – Contextual Help",
  "module": "Engagement & Support",
  "requiresModule": "ai",
  "wave": 2,
  "capability": "AI-02",
  "implementation": {
   "app": "guest-app",
   "route": "/general/ai-concierge-contextual-help",
   "component": "apps/guest-app/src/routes/general/AiConciergeContextualHelpDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "GST-001"
   ],
   "inferred": true,
   "exitTo": [
    "GST-001",
    "GST-002"
   ],
   "fromFlows": true,
   "transitions": [
    {
     "to": "GST-001",
     "trigger": "Home – Default",
     "provenance": "derived — GST-001 declares entryState.params  and GST-033 holds none of them. The edge carries nothing: GST-033 is opened from GST-001, so this edge is the way back and GST-001 keeps its own state"
    }
   ]
  },
  "notes": "States derived from the screen pattern on 17 August, not individually considered. Purpose derived from the screen name and its operations on 17 August, not from a requirement. **Guest concierge confirmed in Phase 1 on 17 August (CF-14), charged per token and bounded by `AiPolicy.guestCapabilityScope`.** Still degrades to the manual planner rather than to an error. **createPayment removed 18 August** — attached by module resemblance, not by what this screen does. A screen that does not handle money should not be able to move it (CF-87's class). **Navigation repointed to P15 on 20 August** — the F&B screens it linked to moved out of the back office when the client board was adopted. **Cross-platform navigation removed 24 August**: BO-020. **A till does not navigate to a back office and a guest app does not navigate to either** — those are device handovers, and a flow declares them with `crossesDevice` rather than a screen pretending there is a link.",
  "density": "comfortable",
  "pattern": "configEditor",
  "patternReason": "the screen declares only writes (`sendAiMessage`) and no read of a population — it is settings, not a list",
  "purpose": "Answer a question without needing a person.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Send AI message",
       "operation": "sendAiMessage",
       "provenance": "contract ai.yaml POST /conversations/{conversationId}/messages"
      }
     ]
    },
    {
     "name": "contentBody",
     "components": [
      {
       "kind": "textField",
       "label": "Content",
       "operation": "sendAiMessage",
       "notes": "Required.",
       "provenance": "contract ai.yaml POST /conversations/{conversationId}/messages"
      },
      {
       "kind": "multiSelect",
       "label": "Collection ids",
       "operation": "sendAiMessage",
       "provenance": "contract ai.yaml POST /conversations/{conversationId}/messages"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The saved concierge contextual help.",
   "error": "Could not load. Names which read failed and leaves the concierge contextual help untouched.",
   "emptyFirstRun": "No concierge contextual help configured. The form opens empty and `sendAiMessage` saves the first one; it says what the platform does in the meantime.",
   "emptyNoAccess": "Shown when the caller lacks `AI_USE`, which `sendAiMessage` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "offline": "**Not available, and the offline banner says why.** The assistant needs the connection; conversations already loaded stay readable."
  },
  "apis": [
   {
    "operationId": "sendAiMessage",
    "contract": "ai",
    "purpose": "Ask",
    "trigger": "onAction"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "conversationId",
     "from": "deepLink"
    }
   ],
   "coldEntry": "A conversation link an agent opens from a notification. Resolves, or says it was closed and by whom."
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "client-verified",
   "board": "wireframes/P02 Guest App.dc.html#gst-033",
   "prototype": {
    "file": "sources/designs/guest-rev3-28-september/TICVAI Guest Booking Mobile v2.dc.html",
    "rev": "rev 3",
    "verified": "2026-09-28",
    "match": "exact",
    "view": "Account → All screens → Wave 2 → AI concierge – contextual help"
   }
  },
  "apisNote": "Rebuilt 9 September 2026 from the 1 operation this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "_platform": {
   "code": "P02",
   "audience": "guest",
   "formFactor": "mobileApp",
   "shortName": "Guest App",
   "name": "Guest App — Mobile",
   "offlineCapable": true,
   "offlineBanner": {
    "kind": "banner",
    "state": "warning",
    "message": "You're offline. Connect to the internet to book, pay, order or join a queue.",
    "shows": "The moment the connection drops, on every screen, above the screen's own content.",
    "clears": "By itself as soon as the connection is back, with a short \"Back online\" confirmation.",
    "never": "Covers what is already on screen, or appears for a server error — that is the screen's own error state, and a guest told they are offline when the venue is down reconnects for nothing.",
    "provenance": "Decided 12 September 2026 — guest web and guest app behave identically offline and say so with the same banner."
   },
   "app": "guest-app",
   "operator": "guest",
   "targetApp": {
    "app": "guest",
    "name": "TICVAI Guest",
    "shell": "mobile",
    "siblings": [
     "P01",
     "P05"
    ],
    "note": "**One guest product in three shells.** Web, mobile and kiosk share 73–91% of their operations; the kiosk is the same product in a fixed frame with no keyboard, and is deliberately narrower rather than different.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "GST-035",
  "name": "Feedback & Ratings",
  "module": "Engagement & Support",
  "requiresModule": "marketing",
  "wave": 3,
  "capability": "C62",
  "implementation": {
   "app": "guest-app",
   "route": "/general/feedback-and-ratings",
   "component": "apps/guest-app/src/routes/general/FeedbackAndRatingsList.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "GST-001"
   ],
   "inferred": true,
   "exitTo": [
    "GST-001",
    "GST-002"
   ],
   "transitions": [
    {
     "to": "GST-001",
     "trigger": "Home – Default",
     "provenance": "derived — GST-001 declares entryState.params  and GST-035 holds none of them. The edge carries nothing: GST-035 is opened from GST-001, so this edge is the way back and GST-001 keeps its own state"
    }
   ]
  },
  "notes": "States derived from the screen pattern on 17 August, not individually considered. Purpose derived from the screen name and its operations on 17 August, not from a requirement. **Guest case operations wired 24 August.** **No case operation was guest-callable** — a guest could raise nothing and read nothing, and `check-screens` refused the staff-permissioned ones on a guest surface. `listMyCases`, `raiseMyCase` and `replyToMyCase` are scoped to the caller rather than filtered by a subject parameter.",
  "density": "comfortable",
  "pattern": "configEditor",
  "patternReason": "the screen declares only writes (`submitReview`, `raiseMyCase`) and no read of a population — it is settings, not a list",
  "purpose": "Work with feedback & ratings for this venue.",
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
       "bindsTo": "SubmitReviewRequest.id",
       "provenance": "contract marketing-crm.yaml POST /reviews"
      },
      {
       "kind": "textField",
       "label": "subjectId",
       "bindsTo": "SubmitReviewRequest.subjectId",
       "provenance": "contract marketing-crm.yaml POST /reviews"
      },
      {
       "kind": "textField",
       "label": "venueId",
       "bindsTo": "SubmitReviewRequest.venueId",
       "provenance": "contract marketing-crm.yaml POST /reviews"
      },
      {
       "kind": "textField",
       "label": "relatedOrderId",
       "bindsTo": "SubmitReviewRequest.relatedOrderId",
       "provenance": "contract marketing-crm.yaml POST /reviews"
      },
      {
       "kind": "textField",
       "label": "rating",
       "bindsTo": "SubmitReviewRequest.rating",
       "provenance": "contract marketing-crm.yaml POST /reviews"
      },
      {
       "kind": "textField",
       "label": "body",
       "bindsTo": "SubmitReviewRequest.body",
       "provenance": "contract marketing-crm.yaml POST /reviews"
      },
      {
       "kind": "textField",
       "label": "aspects",
       "bindsTo": "SubmitReviewRequest.aspects",
       "provenance": "contract marketing-crm.yaml POST /reviews"
      },
      {
       "kind": "textField",
       "label": "recordedAt",
       "bindsTo": "SubmitReviewRequest.recordedAt",
       "provenance": "contract marketing-crm.yaml POST /reviews"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Submit review",
       "operation": "submitReview",
       "provenance": "contract marketing-crm.yaml POST /reviews"
      },
      {
       "kind": "secondaryButton",
       "label": "Raise my case",
       "operation": "raiseMyCase",
       "provenance": "contract marketing-crm.yaml POST /my/cases"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The saved feedback ratings.",
   "error": "Could not load. Names which read failed and leaves the feedback ratings untouched.",
   "emptyFirstRun": "No feedback ratings configured. The form opens empty and `submitReview` saves the first one; it says what the platform does in the meantime.",
   "offline": "**The offline banner shows.** What was already loaded stays on screen, marked with its age. Anything that spends money, holds capacity or changes the account waits for the connection, and its button says so rather than failing."
  },
  "apis": [
   {
    "operationId": "submitReview",
    "contract": "marketing-crm",
    "purpose": "from page inventory",
    "trigger": "onAction"
   },
   {
    "operationId": "raiseMyCase",
    "contract": "marketing-crm",
    "purpose": "Report something — lost property, a complaint, a question",
    "trigger": "onAction"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "client-verified",
   "board": "wireframes/P02 Guest App.dc.html#gst-035",
   "prototype": {
    "file": "sources/designs/guest-rev3-28-september/TICVAI Guest Booking Mobile v2.dc.html",
    "rev": "rev 3",
    "verified": "2026-09-28",
    "match": "exact",
    "view": "Account → All screens → Wave 3 → Feedback & ratings"
   }
  },
  "apisNote": "Rebuilt 9 September 2026 from the 2 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "overlays": [
   {
    "id": "formRaiseMyCase",
    "component": "modal",
    "trigger": "Raise my case",
    "body": "**Collects what `raiseMyCase` sends before it is called.** Required: `id`, `kind`, `summary`, `recordedAt`. Optional: `detail`, `venueId`, `orderRef`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Raise my case",
     "operation": "raiseMyCase"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "kind",
      "summary",
      "recordedAt",
      "detail",
      "venueId",
      "orderRef"
     ]
    },
    "provenance": "client-verified"
   }
  ],
  "_platform": {
   "code": "P02",
   "audience": "guest",
   "formFactor": "mobileApp",
   "shortName": "Guest App",
   "name": "Guest App — Mobile",
   "offlineCapable": true,
   "offlineBanner": {
    "kind": "banner",
    "state": "warning",
    "message": "You're offline. Connect to the internet to book, pay, order or join a queue.",
    "shows": "The moment the connection drops, on every screen, above the screen's own content.",
    "clears": "By itself as soon as the connection is back, with a short \"Back online\" confirmation.",
    "never": "Covers what is already on screen, or appears for a server error — that is the screen's own error state, and a guest told they are offline when the venue is down reconnects for nothing.",
    "provenance": "Decided 12 September 2026 — guest web and guest app behave identically offline and say so with the same banner."
   },
   "app": "guest-app",
   "operator": "guest",
   "targetApp": {
    "app": "guest",
    "name": "TICVAI Guest",
    "shell": "mobile",
    "siblings": [
     "P01",
     "P05"
    ],
    "note": "**One guest product in three shells.** Web, mobile and kiosk share 73–91% of their operations; the kiosk is the same product in a fixed frame with no keyboard, and is deliberately narrower rather than different.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "GST-040",
  "name": "Help & Support",
  "module": "Engagement & Support",
  "requiresModule": "marketing",
  "wave": 2,
  "capability": "C17",
  "implementation": {
   "app": "guest-app",
   "route": "/general/help-and-support",
   "component": "apps/guest-app/src/routes/general/HelpAndSupportDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "GST-001"
   ],
   "inferred": true,
   "exitTo": [
    "GST-001",
    "GST-002"
   ],
   "transitions": [
    {
     "to": "GST-001",
     "trigger": "Home – Default",
     "provenance": "derived — GST-001 declares entryState.params  and GST-040 holds none of them. The edge carries nothing: GST-040 is opened from GST-001, so this edge is the way back and GST-001 keeps its own state"
    },
    {
     "to": "WEB-034",
     "trigger": "They report something lost",
     "provenance": "flow F54 step 2→3",
     "crossesDevice": true,
     "back": false,
     "carries": [
      "caseId"
     ]
    }
   ]
  },
  "notes": "States derived from the screen pattern on 17 August, not individually considered. Purpose derived from the screen name and its operations on 17 August, not from a requirement. **Guest case operations wired 24 August.** **No case operation was guest-callable** — a guest could raise nothing and read nothing, and `check-screens` refused the staff-permissioned ones on a guest surface. `listMyCases`, `raiseMyCase` and `replyToMyCase` are scoped to the caller rather than filtered by a subject parameter.\n\n**Rev 3 (decided 29 September).** The Help screen shows app status and a public *What's new* (GAP-B2).",
  "density": "comfortable",
  "pattern": "commandCentre",
  "patternReason": "3 independent reads and no read of one record — the screen watches a population rather than working one",
  "purpose": "Answer a question without needing a person.",
  "layout": {
   "template": "dashboard",
   "regions": [
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "Faqs",
       "bindsTo": "FaqCategory",
       "operation": "listFaqs",
       "provenance": "contract white-label.yaml GET /tenant-config/faqs"
      },
      {
       "kind": "metricTile",
       "label": "Content pages",
       "bindsTo": "ContentPage",
       "operation": "listContentPages",
       "provenance": "contract white-label.yaml GET /tenant-config/pages"
      },
      {
       "kind": "metricTile",
       "label": "My cases",
       "bindsTo": "Case",
       "operation": "listMyCases",
       "provenance": "contract marketing-crm.yaml GET /my/cases"
      },
      {
       "kind": "dataTable",
       "label": "Every faq category",
       "bindsTo": "FaqCategory",
       "columns": [
        "FaqCategory.code",
        "FaqCategory.name",
        "FaqCategory.sortOrder",
        "FaqCategory.entries",
        "FaqCategory.scopePath"
       ],
       "operation": "listFaqs",
       "provenance": "contract white-label.yaml GET /tenant-config/faqs"
      },
      {
       "kind": "cardList",
       "label": "What's new",
       "notes": "Public, localised release notes from `getTenantAppStatus` `whatsNew`, newest first, at most 10; the staff-only `recentChanges` stays staff only.",
       "operation": "getTenantAppStatus",
       "provenance": "decided 29 September, rev 3 GAP-B2"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Raise my case",
       "operation": "raiseMyCase",
       "provenance": "contract marketing-crm.yaml POST /my/cases"
      },
      {
       "kind": "secondaryButton",
       "label": "Reply to my case",
       "operation": "replyToMyCase",
       "provenance": "contract marketing-crm.yaml POST /my/cases/{caseId}/messages"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The help support figures; each tile loads on its own.",
   "error": "Could not load. Names which read failed and leaves the help support untouched.",
   "emptyFirstRun": "No help support yet. Offers Raise my case (`raiseMyCase`).",
   "emptyNoResults": "Never shown: `listFaqs` takes no filter, so an empty list is always the first-run state above.",
   "emptyNoAccess": "Shown when the caller lacks `TENANT_CONFIGURE`, which `listFaqs` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "offline": "**The offline banner shows.** Help already loaded stays readable, marked with its age. **Raising a case is disabled offline** — it needs the connection (decided 28 September, audit R148) — and the screen says how to reach staff in person instead: the guest services desk, or any member of staff."
  },
  "apis": [
   {
    "operationId": "listFaqs",
    "contract": "white-label",
    "purpose": "List FAQs",
    "trigger": "onLoad"
   },
   {
    "operationId": "listContentPages",
    "contract": "white-label",
    "purpose": "List custom content pages",
    "trigger": "onLoad"
   },
   {
    "operationId": "listMyCases",
    "contract": "marketing-crm",
    "purpose": "The cases this guest raised",
    "trigger": "onLoad"
   },
   {
    "operationId": "raiseMyCase",
    "contract": "marketing-crm",
    "purpose": "Report something — lost property, a complaint, a question",
    "trigger": "onAction",
    "invalidates": [
     "listFaqs"
    ]
   },
   {
    "operationId": "replyToMyCase",
    "contract": "marketing-crm",
    "purpose": "Reply on a case the guest raised",
    "trigger": "onAction",
    "invalidates": [
     "listFaqs"
    ]
   },
   {
    "operationId": "getTenantAppStatus",
    "contract": "white-label",
    "purpose": "App status and the public *What's new*",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "caseId",
     "from": "deepLink",
     "optional": true
    }
   ],
   "coldEntry": "A case opened from a notification or the list. **Optional** — the ordinary way in is to raise a new one, not to open an old one."
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "client-verified",
   "board": "wireframes/P02 Guest App.dc.html#gst-040",
   "prototype": {
    "file": "sources/designs/guest-rev3-28-september/TICVAI Guest Booking Mobile v2.dc.html",
    "rev": "rev 3",
    "verified": "2026-09-28",
    "match": "exact",
    "view": "Account → All screens → Wave 2 → Help & support"
   }
  },
  "apisNote": "Rebuilt 9 September 2026 from the 5 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "overlays": [
   {
    "id": "formRaiseMyCase",
    "component": "modal",
    "trigger": "Raise my case",
    "body": "**Collects what `raiseMyCase` sends before it is called.** Required: `id`, `kind`, `summary`, `recordedAt`. Optional: `detail`, `venueId`, `orderRef`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Raise my case",
     "operation": "raiseMyCase"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "kind",
      "summary",
      "recordedAt",
      "detail",
      "venueId",
      "orderRef"
     ]
    },
    "provenance": "client-verified"
   },
   {
    "id": "formReplyToMyCase",
    "component": "modal",
    "trigger": "Reply to my case",
    "body": "**Collects what `replyToMyCase` sends before it is called.** Required: `message`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Reply to my case",
     "operation": "replyToMyCase"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "message"
     ]
    },
    "provenance": "client-verified"
   }
  ],
  "_platform": {
   "code": "P02",
   "audience": "guest",
   "formFactor": "mobileApp",
   "shortName": "Guest App",
   "name": "Guest App — Mobile",
   "offlineCapable": true,
   "offlineBanner": {
    "kind": "banner",
    "state": "warning",
    "message": "You're offline. Connect to the internet to book, pay, order or join a queue.",
    "shows": "The moment the connection drops, on every screen, above the screen's own content.",
    "clears": "By itself as soon as the connection is back, with a short \"Back online\" confirmation.",
    "never": "Covers what is already on screen, or appears for a server error — that is the screen's own error state, and a guest told they are offline when the venue is down reconnects for nothing.",
    "provenance": "Decided 12 September 2026 — guest web and guest app behave identically offline and say so with the same banner."
   },
   "app": "guest-app",
   "operator": "guest",
   "targetApp": {
    "app": "guest",
    "name": "TICVAI Guest",
    "shell": "mobile",
    "siblings": [
     "P01",
     "P05"
    ],
    "note": "**One guest product in three shells.** Web, mobile and kiosk share 73–91% of their operations; the kiosk is the same product in a fixed frame with no keyboard, and is deliberately narrower rather than different.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "GST-051",
  "name": "Plan",
  "module": "Engagement & Support",
  "requiresModule": "ticketing",
  "wave": 1,
  "capability": "AI-35",
  "implementation": {
   "app": "guest-app",
   "route": "/general/plan-your-adventure-start",
   "component": "apps/guest-app/src/routes/general/PlanYourAdventureStartDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "isEntryPoint": true,
   "inferred": false,
   "uses": [
    "appTabs"
   ],
   "entryFrom": [
    "GST-001",
    "GST-053"
   ],
   "exitTo": [
    "GST-053",
    "GST-052",
    "GST-001"
   ],
   "transitions": [
    {
     "to": "GST-053",
     "trigger": "Make my plan",
     "control": "primaryButton#makeMyPlan",
     "operation": "generateVisitPlan",
     "carries": [
      "planId"
     ],
     "onFailure": [
      {
       "when": "nothing suits the party",
       "to": "GST-051",
       "note": "Says which answer ruled everything out."
      }
     ],
     "provenance": "decided 29 September 2026, MOB-6; v4 prototype plan → planResult"
    },
    {
     "to": "GST-052",
     "trigger": "Take a ready-made plan",
     "provenance": "decided 29 September 2026, MOB-6"
    },
    {
     "to": "GST-001",
     "trigger": "Home tab",
     "provenance": "decided 29 September 2026, MOB-1"
    }
   ]
  },
  "notes": "Minuted 10 Aug §4.9. Benchmarked against Skidata. Tied to a ticket purchase and saved as a personal visit profile. **Out of the first release** (decided 28 September, audit R187): the itinerary planner is deferred and this screen is `wave: 4` with a `deferred` block. Kept, not deleted, for the release that builds it.\n\n**Rev 3 (decided 29 September).** Had stayed in wave 4 (GAP-C3); superseded the same day by the re-plan below.\n\n**Brought into Block A on 29 September** (Chinmay, the 29 September re-plan, MOB-6): a rules-based planner with the AI planner agent on top. This supersedes audit R187, the deferral half of R209 and rev 3 GAP-C3; the `deferred` block is removed and the screen is wave 1.\n\n**Mobile v4 role (MOB-6): the Plan tab root, \"Plan\".** Inputs: party size, heights (or ages), dates, pace (packed, balanced or relaxed), interests and cuisine. The rules planner (`generateVisitPlan`) runs with no AI. The tab is hidden when the venue turns module `visitPlanner` off.\n\n**Multi-venue intelligence (client meeting 30 September, MoM 4.7, Allam; agreed by Chinmay).** In a multi-venue tenant each chosen day is at one park, and the planner uses **only the rides, dining and retail that exist at that park**: a cuisine or shop preference is checked against that park's own points, never assumed of every park (only one park has the Indian restaurant, so *Indian* places lunch there on that park's day and nowhere else). Retail and kiosk shops are now planner options alongside F&B (the gap a Softlabs teammate flagged). Contract: venue-map `generateVisitPlan` `dayVenues`, `retailTags`, `VisitPlan.unmatchedPreferences`.",
  "density": "comfortable",
  "pattern": "multiStepForm",
  "patternReason": "The v4 prototype asks six questions one at a time (who, heights, days, pace, likes, food) and ends on *Make my plan*",
  "purpose": "The Plan tab: tell the venue who is coming, when, at what pace and what you like, and get a day-by-day plan.",
  "layout": {
   "template": "wizard",
   "regions": [
    {
     "name": "progress",
     "slot": "progress",
     "components": [
      {
       "kind": "progressIndicator",
       "label": "Plan your visit · n of 6",
       "notes": "Six questions; Heights is skipped when no children are coming.",
       "provenance": "decided 29 September 2026, MOB-6"
      }
     ]
    },
    {
     "name": "fields",
     "slot": "fields",
     "components": [
      {
       "kind": "numberField",
       "label": "Adults",
       "notes": "Age 12 and over, at least 1, at most 8.",
       "provenance": "decided 29 September 2026, MOB-6"
      },
      {
       "kind": "numberField",
       "label": "Children",
       "notes": "Age 3 to 11, 0-8.",
       "provenance": "decided 29 September 2026, MOB-6"
      },
      {
       "kind": "selectField",
       "label": "How tall are the children?",
       "operation": "listProducts",
       "notes": "Per child: under 1.0 m, 1.0-1.2 m, 1.2-1.4 m, 1.4 m and over (or an age where the venue sets age rules). Rides over a child's limit are left out, from `ProductEligibilityRule`.",
       "provenance": "decided 29 September 2026, MOB-6"
      },
      {
       "kind": "multiSelect",
       "label": "Which days are you visiting?",
       "notes": "Up to three days; each day gets its own park at a multi-park venue.",
       "provenance": "decided 29 September 2026, MOB-6"
      },
      {
       "kind": "selectField",
       "label": "Which park each day?",
       "bindsTo": "TenantAppStatus.venues",
       "operation": "getTenantAppStatus",
       "notes": "**Only in a multi-venue tenant** (more than one entry in `getTenantAppStatus.venues`); hidden otherwise. One choice per chosen day, defaulting to the venue picked on Home; sent as `VisitPlanRequest.dayVenues`. **Each day is then planned from that park's own rides, dining and shops only** (client meeting 30 September, MoM 4.7).",
       "provenance": "decided 30 September 2026, client meeting MoM 4.7 (Allam)"
      },
      {
       "kind": "selectField",
       "label": "How busy should each day be?",
       "notes": "Packed, Balanced or Relaxed.",
       "provenance": "decided 29 September 2026, MOB-6"
      },
      {
       "kind": "multiSelect",
       "label": "What are you most interested in?",
       "operation": "listProducts",
       "notes": "Interest tags from the venue's points (`VenuePoint.interestTags`): thrill rides, family rides, shows, water, shopping.",
       "provenance": "decided 29 September 2026, MOB-6"
      },
      {
       "kind": "multiSelect",
       "label": "Any shops you'd like to visit?",
       "notes": "**Shown when Shopping is chosen above** (client meeting 30 September, MoM 4.7: retail and kiosk shops join F&B in the planner). Options are the `retailTags` of the shops and retail kiosks of the chosen parks (souvenirs, toys, apparel ...); sent as `VisitPlanRequest.retailTags`. A shop stop is planned only at a shop or kiosk of that day's park.",
       "provenance": "decided 30 September 2026, client meeting MoM 4.7 (Allam)"
      },
      {
       "kind": "selectField",
       "label": "What would you like for lunch?",
       "notes": "**Cuisines from the dining points of the chosen parks only** (`VenuePoint.cuisineTags` of restaurants, cafes and food kiosks; client meeting 30 September, MoM 4.7). Lunch is planned at a restaurant **of that day's park** that serves it, never another park's. In a multi-venue plan each cuisine names the park(s) that serve it (*Indian · Summit Peaks only*), so the guest sees before planning that it will not be on every day.",
       "provenance": "decided 29 September 2026, MOB-6; decided 30 September 2026, client meeting MoM 4.7 (Allam)"
      }
     ]
    },
    {
     "name": "submit",
     "slot": "submit",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Make my plan",
       "operation": "generateVisitPlan",
       "notes": "Calls `generateVisitPlan`: the rules planner, no AI. Opens Your Plan (GST-053).",
       "provenance": "decided 29 September 2026, MOB-6"
      },
      {
       "kind": "secondaryButton",
       "label": "Take a ready-made plan",
       "notes": "Opens Suggested Itineraries (GST-052).",
       "provenance": "decided 29 September 2026, MOB-6"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The plan builds in place; the inputs stay on screen.",
   "error": "Could not load the plan. Names what failed; the inputs are kept so trying again costs nothing.",
   "emptyFirstRun": "No plan yet: the first question is shown. Nothing is saved until *Make my plan*.",
   "emptyNoResults": "Nothing suits the whole party on that day (for example every ride is over a child's height): says so and offers to change the answers.",
   "preferenceNotAtVenue": "**A preference no chosen park can meet** (client meeting 30 September, MoM 4.7): a cuisine or shop tag with no matching point at any park of the plan is marked on its chip (*Not at the parks you chose*) before *Make my plan*; the plan is still made without it, never with a restaurant or shop from a park the party is not visiting. Where another park of the tenant has it, the chip says which, and choosing that park for a day brings it in.",
   "emptyNoAccess": "A guest holds no permission. A plan that is not theirs says so without saying whose it is; a signed-out guest can still build a plan and is asked to sign in only to save or book it.",
   "offline": "**The offline banner shows.** What was already loaded stays on screen, marked with its age. Anything that spends money, holds capacity or changes the account waits for the connection, and its button says so rather than failing."
  },
  "apis": [
   {
    "operationId": "getWaitTimes",
    "contract": "queue",
    "purpose": "Wait times across a venue",
    "trigger": "onLoad"
   },
   {
    "operationId": "listProducts",
    "contract": "catalogue",
    "purpose": "List products",
    "trigger": "onLoad"
   },
   {
    "operationId": "generateVisitPlan",
    "contract": "venue-map",
    "purpose": "Build a rules plan from the inputs (party, heights, dates, park per day, pace, interests, shops, cuisine); each day from its own park's points only",
    "trigger": "onAction",
    "provenance": "decided 29 September 2026, MOB-6; decided 30 September 2026, client meeting MoM 4.7 (Allam)"
   },
   {
    "operationId": "getTenantAppStatus",
    "contract": "white-label",
    "purpose": "The tenant's active venues, for the park-per-day choice in a multi-venue tenant",
    "trigger": "onLoad",
    "provenance": "decided 30 September 2026, client meeting MoM 4.7 (Allam)"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "venueId",
     "from": "session"
    }
   ],
   "coldEntry": "The Plan tab; a cold arrival is the ordinary case and starts at the first question."
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "client-verified",
   "board": "wireframes/P02 Guest App.dc.html#gst-051",
   "prototype": {
    "file": "sources/designs/guest-rev3-30-september/TICVAI Mobile App v4.dc.html",
    "rev": "mobile v4 (30 September build)",
    "verified": "2026-10-01",
    "match": "exact",
    "view": "Plan tab (Plan your visit · 1 of 6)"
   }
  },
  "apisNote": "Rebuilt 9 September 2026 from the 2 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "_platform": {
   "code": "P02",
   "audience": "guest",
   "formFactor": "mobileApp",
   "shortName": "Guest App",
   "name": "Guest App — Mobile",
   "offlineCapable": true,
   "offlineBanner": {
    "kind": "banner",
    "state": "warning",
    "message": "You're offline. Connect to the internet to book, pay, order or join a queue.",
    "shows": "The moment the connection drops, on every screen, above the screen's own content.",
    "clears": "By itself as soon as the connection is back, with a short \"Back online\" confirmation.",
    "never": "Covers what is already on screen, or appears for a server error — that is the screen's own error state, and a guest told they are offline when the venue is down reconnects for nothing.",
    "provenance": "Decided 12 September 2026 — guest web and guest app behave identically offline and say so with the same banner."
   },
   "app": "guest-app",
   "operator": "guest",
   "targetApp": {
    "app": "guest",
    "name": "TICVAI Guest",
    "shell": "mobile",
    "siblings": [
     "P01",
     "P05"
    ],
    "note": "**One guest product in three shells.** Web, mobile and kiosk share 73–91% of their operations; the kiosk is the same product in a fixed frame with no keyboard, and is deliberately narrower rather than different.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "GST-052",
  "name": "Suggested Itineraries",
  "module": "Engagement & Support",
  "requiresModule": "ticketing",
  "wave": 1,
  "capability": "AI-35",
  "implementation": {
   "app": "guest-app",
   "route": "/general/suggested-itineraries",
   "component": "apps/guest-app/src/routes/general/SuggestedItinerariesDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "inferred": false,
   "entryFrom": [
    "GST-001",
    "GST-051"
   ],
   "exitTo": [
    "GST-053",
    "GST-051",
    "GST-001"
   ],
   "transitions": [
    {
     "to": "GST-053",
     "trigger": "Use this plan",
     "operation": "generateVisitPlan",
     "carries": [
      "planId"
     ],
     "provenance": "decided 29 September 2026, MOB-6"
    },
    {
     "to": "GST-051",
     "trigger": "Make my own",
     "provenance": "decided 29 September 2026, MOB-6"
    },
    {
     "to": "GST-001",
     "trigger": "Home tab",
     "provenance": "decided 29 September 2026, MOB-1"
    }
   ]
  },
  "notes": "Minuted 10 Aug §4.9. ** wired 24 August.** The board drew four bespoke AI endpoints for itinerary planning; **one operation with a kind answers all of them** (ADR-0028), and recording the outcome is what lets a model replace the heuristic later. **`recordSuggestionOutcome` removed from the guest surface.** `check-screens` refused it and was right: **a guest does not record an outcome — the platform observes what they did.** A guest app that self-reports whether it took the advice is a training label the guest could forge, and the observation belongs server-side where the plan and the visit can be compared. **Out of the first release** (decided 28 September, audit R187): the itinerary planner is deferred and this screen is `wave: 4` with a `deferred` block. Kept, not deleted, for the release that builds it. **Itinerary suggestion removed 28 September** (decided 28 September, audit R209): the planner is deferred (R187) and `requestSuggestion` refuses a guest anything but prepPlan, upsell and waitTime, so this screen no longer asks for a day plan.\n\n**Rev 3 (decided 29 September).** Had stayed in wave 4 (GAP-C3); superseded the same day by the re-plan below.\n\n**Brought into Block A on 29 September** (Chinmay, the 29 September re-plan, MOB-6): a rules-based planner with the AI planner agent on top. This supersedes audit R187, the deferral half of R209 and rev 3 GAP-C3; the `deferred` block is removed and the screen is wave 1.\n\n**Mobile v4 role (MOB-6): ready-made day plans per venue** the guest can take; each is rules-built by `generateVisitPlan` from preset inputs, then edited on GST-053.",
  "density": "comfortable",
  "pattern": "listDetail",
  "patternReason": "`listProducts` reads a population and nothing reads one of them; the detail is the row until a `get` exists",
  "purpose": "Ready-made day plans for this venue that a guest can take instead of answering questions.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "cardList",
       "label": "Ready-made plans",
       "operation": "listProducts",
       "notes": "The venue's preset plans (e.g. *Thrill day*, *Family day*, *Relaxed day*), each a set of planner inputs; **Use this plan** runs `generateVisitPlan` with those inputs and the guest's party size and date. Rules-built, not AI: seeded, not learned, on day one.",
       "provenance": "decided 29 September 2026, MOB-6"
      },
      {
       "kind": "dataTable",
       "label": "Every bundle",
       "operation": "listCatalogueBundles",
       "notes": "Bundles a preset plan can include (e.g. Fast Track).",
       "provenance": "contract catalogue.yaml GET /catalogue/bundles"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Use this plan",
       "operation": "generateVisitPlan",
       "notes": "Opens Your Plan (GST-053).",
       "provenance": "decided 29 September 2026, MOB-6"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The plan builds in place; the inputs stay on screen.",
   "error": "Could not load the plan. Names what failed; the inputs are kept so trying again costs nothing.",
   "emptyFirstRun": "The venue has no ready-made plans: says so and offers *Make my own* (GST-051).",
   "emptyNoResults": "Nothing suits the whole party on that day (for example every ride is over a child's height): says so and offers to change the answers.",
   "emptyNoAccess": "A guest holds no permission. A plan that is not theirs says so without saying whose it is; a signed-out guest can still build a plan and is asked to sign in only to save or book it.",
   "offline": "**The offline banner shows.** What was already loaded stays on screen, marked with its age. Anything that spends money, holds capacity or changes the account waits for the connection, and its button says so rather than failing."
  },
  "apis": [
   {
    "operationId": "listProducts",
    "contract": "catalogue",
    "purpose": "List products",
    "trigger": "onLoad"
   },
   {
    "operationId": "listCatalogueBundles",
    "contract": "catalogue",
    "purpose": "List published bundles",
    "trigger": "onLoad"
   },
   {
    "operationId": "generateVisitPlan",
    "contract": "venue-map",
    "purpose": "Build a rules plan from the inputs (party, heights, dates, pace, interests, cuisine)",
    "trigger": "onAction",
    "provenance": "decided 29 September 2026, MOB-6"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "venueId",
     "from": "session"
    }
   ],
   "coldEntry": "Lists the venue's ready-made plans; nothing is needed upstream."
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "designed",
   "board": "wireframes/P02 Guest App.dc.html#gst-052",
   "prototype": {
    "file": "sources/designs/guest-rev3-29-september/TICVAI Mobile App v4.dc.html",
    "rev": "Mobile App v4, 29 September 2026",
    "match": "none",
    "note": "Mobile App v4 has no view for this screen. Drawn by Claude Code on 30 September 2026 in the v4 look (the frame on this screen's board, wireframes/frames/gst-052.html, and #GST-052 in handoff/design-batches/apps/1-guest-app/return/TICVAI Guest App.dc.html). NOT client-verified: awaiting the client's design reviewer. Build the layout from that frame and this definition. Mobile v2 (28 September, superseded by v4) showed it at: Account → All screens → Wave 3 → Suggested itineraries (exact). What v2 did differently: Mobile v4 draws no ready-made plans list: its Plan tab goes straight to the questions. Built from this definition in the v4 style."
   },
   "source": "Claude Code, 30 September 2026, drawn in the Mobile App v4 look",
   "note": "**Drawn by Claude Code on 30 September 2026 in the Mobile App v4 look; not client-verified, awaiting the client's design reviewer.** `provenance: designed` because the accepted vocabulary has no value for an agent-drawn frame; it is the value the eight Claude Design frames of 29 September carry. Gaps the operations leave are in handoff/design-batches/apps/1-guest-app/return/FINDINGS.md."
  },
  "apisNote": "Rebuilt 9 September 2026 from the 3 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "_platform": {
   "code": "P02",
   "audience": "guest",
   "formFactor": "mobileApp",
   "shortName": "Guest App",
   "name": "Guest App — Mobile",
   "offlineCapable": true,
   "offlineBanner": {
    "kind": "banner",
    "state": "warning",
    "message": "You're offline. Connect to the internet to book, pay, order or join a queue.",
    "shows": "The moment the connection drops, on every screen, above the screen's own content.",
    "clears": "By itself as soon as the connection is back, with a short \"Back online\" confirmation.",
    "never": "Covers what is already on screen, or appears for a server error — that is the screen's own error state, and a guest told they are offline when the venue is down reconnects for nothing.",
    "provenance": "Decided 12 September 2026 — guest web and guest app behave identically offline and say so with the same banner."
   },
   "app": "guest-app",
   "operator": "guest",
   "targetApp": {
    "app": "guest",
    "name": "TICVAI Guest",
    "shell": "mobile",
    "siblings": [
     "P01",
     "P05"
    ],
    "note": "**One guest product in three shells.** Web, mobile and kiosk share 73–91% of their operations; the kiosk is the same product in a fixed frame with no keyboard, and is deliberately narrower rather than different.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "GST-053",
  "name": "Your Plan",
  "module": "Engagement & Support",
  "requiresModule": "ticketing",
  "wave": 1,
  "capability": "C02",
  "implementation": {
   "app": "guest-app",
   "route": "/general/build-your-own-itinerary",
   "component": "apps/guest-app/src/routes/general/BuildYourOwnItineraryDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "inferred": false,
   "entryFrom": [
    "GST-051",
    "GST-052",
    "GST-054"
   ],
   "exitTo": [
    "GST-041",
    "GST-054",
    "GST-051",
    "GST-048",
    "GST-059",
    "GST-001"
   ],
   "transitions": [
    {
     "to": "GST-041",
     "trigger": "Book this plan",
     "control": "primaryButton#bookThisPlan",
     "operation": "bookVisitPlan",
     "carries": [
      "cartId"
     ],
     "onFailure": [
      {
       "when": "an item sold out since the plan was made",
       "to": "GST-053",
       "note": "Names it and offers a swap; the rest of the plan is kept."
      }
     ],
     "provenance": "decided 29 September 2026, MOB-6; v4 prototype Book this plan"
    },
    {
     "to": "GST-054",
     "trigger": "Refine with the AI planner",
     "carries": [
      "planId"
     ],
     "provenance": "decided 29 September 2026, MOB-6"
    },
    {
     "to": "GST-051",
     "trigger": "Change answers",
     "provenance": "decided 29 September 2026, MOB-6"
    },
    {
     "to": "GST-048",
     "trigger": "More add-ons",
     "carries": [
      "cartId"
     ],
     "provenance": "decided 29 September 2026, MOB-6"
    },
    {
     "to": "GST-059",
     "trigger": "On the day: follow the plan",
     "carries": [
      "planId"
     ],
     "provenance": "decided 29 September 2026, MOB-6"
    },
    {
     "to": "GST-001",
     "trigger": "Home tab",
     "provenance": "decided 29 September 2026, MOB-1"
    }
   ]
  },
  "notes": "Minuted 10 Aug §4.9. **Group sharing agreed** — an in-app QR a friend scans to join the itinerary (Chinmay raised, Qossai confirmed). **Out of the first release** (decided 28 September, audit R187): the itinerary planner is deferred and this screen is `wave: 4` with a `deferred` block. Kept, not deleted, for the release that builds it.\n\n**Rev 3 (decided 29 September).** Had stayed in wave 4 (GAP-C3); superseded the same day by the re-plan below.\n\n**Brought into Block A on 29 September** (Chinmay, the 29 September re-plan, MOB-6): a rules-based planner with the AI planner agent on top. This supersedes audit R187, the deferral half of R209 and rev 3 GAP-C3; the `deferred` block is removed and the screen is wave 1.\n\n**Mobile v4 role (MOB-6): \"Your Plan\".** Per-day itinerary with swap, remove, add and undo (`updateVisitPlan` is versioned), add-ons such as Fast Track, and **Book this plan** → GST-041.\n\n**Multi-venue intelligence (client meeting 30 September, MoM 4.7, Allam).** Each day tab is one park, and every item on it (rides, dining, and now retail: shops and kiosks) is at that park; a preference the park cannot meet shows as *Not at this park* rather than being filled from another park.",
  "density": "comfortable",
  "pattern": "listDetail",
  "patternReason": "`listProducts` reads the population and `getCart` reads one of them — list, select, act",
  "purpose": "The plan, day by day: swap, remove or add items, undo, add Fast Track, then book the whole plan.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "selectField",
       "label": "Day tabs",
       "bindsTo": "VisitPlan",
       "operation": "getVisitPlan",
       "notes": "Day 1 · Fri 2 Oct · Summit Peaks … one tab per chosen day; the park is the day's `VisitPlan.days[].venueId` (client meeting 30 September, MoM 4.7).",
       "provenance": "decided 29 September 2026, MOB-6"
      },
      {
       "kind": "timeline",
       "label": "The day",
       "bindsTo": "VisitPlanItem",
       "operation": "getVisitPlan",
       "notes": "Arrive, then each timed item (ride, show, lunch at a restaurant serving the chosen cuisine, a shop or kiosk stop) with its place and zone; Fast Track marked on the rides it covers. **Every item is at the day's park** (`VisitPlanItem.venueId`; client meeting 30 September, MoM 4.7): retail stops (`kind` `shop`: shops and retail kiosks) sit beside meals, both from that park's own points.",
       "provenance": "decided 29 September 2026, MOB-6; decided 30 September 2026, client meeting MoM 4.7 (Allam)"
      },
      {
       "kind": "secondaryButton",
       "label": "Swap",
       "operation": "listVisitPlanAlternatives",
       "notes": "Opens the swap sheet of candidates that suit everyone (`listVisitPlanAlternatives`); choosing one saves a new version. Candidates come only from the day's park (client meeting 30 September, MoM 4.7); a meal swaps to that park's dining, a shop to its shops and kiosks.",
       "provenance": "decided 29 September 2026, MOB-6"
      },
      {
       "kind": "destructiveButton",
       "label": "Remove",
       "operation": "updateVisitPlan",
       "notes": "Removes the item (not arrival or lunch); a new version, so Undo brings it back.",
       "provenance": "decided 29 September 2026, MOB-6"
      },
      {
       "kind": "secondaryButton",
       "label": "+ Add something",
       "operation": "listVisitPlanAlternatives",
       "notes": "The same sheet, adding to the day.",
       "provenance": "decided 29 September 2026, MOB-6"
      },
      {
       "kind": "secondaryButton",
       "label": "Undo changes",
       "operation": "updateVisitPlan",
       "notes": "Returns the day to the previous version of the plan.",
       "provenance": "decided 29 September 2026, MOB-6"
      },
      {
       "kind": "banner",
       "label": "Left out for your group",
       "operation": "getVisitPlan",
       "notes": "Items left out because of a child's height, with the limit (e.g. *Freefall Tower (needs 1.40 m)*), and a must-see at none of the chosen parks (`notAtVenue`).",
       "provenance": "decided 29 September 2026, MOB-6"
      },
      {
       "kind": "banner",
       "label": "Not at this park",
       "bindsTo": "VisitPlan.unmatchedPreferences",
       "operation": "getVisitPlan",
       "notes": "**Per day, what the day's park could not offer** (client meeting 30 September, MoM 4.7): e.g. *No Indian restaurant at Summit Peaks. Indian food is at Aqua Park (day 2).* Names the other park from `availableAtVenueIds`, or says no park has it. Lunch that day is at the park's best other restaurant, marked as such. Hidden when every preference is met.",
       "provenance": "decided 30 September 2026, client meeting MoM 4.7 (Allam)"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "toggle",
       "label": "Add Fast Track",
       "operation": "updateVisitPlan",
       "notes": "An add-on from the plan's `addOnSuggestions` (the product GST-048 sells), priced per guest, with the queuing time it saves.",
       "provenance": "decided 29 September 2026, MOB-6"
      },
      {
       "kind": "detailPanel",
       "label": "Estimated total",
       "operation": "getVisitPlan",
       "notes": "Estimated price for the group and days; the guest confirms dates and tickets in the basket.",
       "provenance": "decided 29 September 2026, MOB-6"
      },
      {
       "kind": "detailPanel",
       "label": "The wait time",
       "operation": "getWaitTimes",
       "notes": "Live waits beside the rides on today's plan.",
       "provenance": "contract queue.yaml GET /queues/wait-times"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Book this plan",
       "operation": "bookVisitPlan",
       "notes": "`bookVisitPlan` turns the plan and add-ons into cart lines and returns the cart; lands on the basket (GST-041).",
       "provenance": "decided 29 September 2026, MOB-6"
      },
      {
       "kind": "secondaryButton",
       "label": "Refine with the AI planner",
       "notes": "Opens GST-054 when the venue has AI on.",
       "provenance": "decided 29 September 2026, MOB-6"
      },
      {
       "kind": "secondaryButton",
       "label": "Change answers",
       "notes": "Back to the questions (GST-051).",
       "provenance": "decided 29 September 2026, MOB-6"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The plan builds in place; the inputs stay on screen.",
   "error": "Could not load the plan. Names what failed; the inputs are kept so trying again costs nothing.",
   "emptyFirstRun": "No plan yet: offers the questions (GST-051) or a ready-made plan (GST-052).",
   "emptyNoResults": "Nothing suits the whole party on that day (for example every ride is over a child's height): says so and offers to change the answers.",
   "preferenceNotAtVenue": "**A day whose park cannot meet a preference** (client meeting 30 September, MoM 4.7): the day is shown in full with the *Not at this park* banner naming the cuisine or shop and where it is instead; nothing from another park is placed. *Change answers* (GST-051) lets the guest move that day to the park that has it. An empty swap sheet says the day's park has no other option of that kind, not that none exists anywhere.",
   "emptyNoAccess": "A guest holds no permission. A plan that is not theirs says so without saying whose it is; a signed-out guest can still build a plan and is asked to sign in only to save or book it.",
   "offline": "**The offline banner shows.** What was already loaded stays on screen, marked with its age. Anything that spends money, holds capacity or changes the account waits for the connection, and its button says so rather than failing."
  },
  "apis": [
   {
    "operationId": "getCart",
    "contract": "orders",
    "purpose": "The cart, priced and checked, right now",
    "trigger": "onLoad"
   },
   {
    "operationId": "listProducts",
    "contract": "catalogue",
    "purpose": "List products",
    "trigger": "onLoad"
   },
   {
    "operationId": "getWaitTimes",
    "contract": "queue",
    "purpose": "Wait times across a venue",
    "trigger": "onLoad"
   },
   {
    "operationId": "getVisitPlan",
    "contract": "venue-map",
    "purpose": "The plan: days, timed items and add-on suggestions, at its current version",
    "trigger": "onLoad",
    "provenance": "decided 29 September 2026, MOB-6"
   },
   {
    "operationId": "updateVisitPlan",
    "contract": "venue-map",
    "purpose": "Swap, remove, add or undo: each change is a new version, so undo goes back one",
    "trigger": "onAction",
    "provenance": "decided 29 September 2026, MOB-6"
   },
   {
    "operationId": "listVisitPlanAlternatives",
    "contract": "venue-map",
    "purpose": "Swap candidates for one item that suit everyone in the party",
    "trigger": "onAction",
    "provenance": "decided 29 September 2026, MOB-6"
   },
   {
    "operationId": "bookVisitPlan",
    "contract": "venue-map",
    "purpose": "Book this plan: turns the plan (and chosen add-ons) into cart lines and returns the cart",
    "trigger": "onAction",
    "provenance": "decided 29 September 2026, MOB-6"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "planId",
     "from": "GST-051",
     "optional": false
    },
    {
     "name": "venueId",
     "from": "session"
    },
    {
     "name": "itemId",
     "from": "navigation",
     "optional": true
    },
    {
     "name": "cartId",
     "from": "session"
    }
   ],
   "coldEntry": "A saved plan opened from a link or the Plan tab. A plan whose dates have passed says so and offers to plan again; a plan that is not this guest's is refused without saying whose it is. `itemId` is the plan item the guest taps Swap on, picked on this screen."
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "client-verified",
   "board": "wireframes/P02 Guest App.dc.html#gst-053",
   "prototype": {
    "file": "sources/designs/guest-rev3-30-september/TICVAI Mobile App v4.dc.html",
    "rev": "mobile v4 (30 September build)",
    "verified": "2026-10-01",
    "match": "exact",
    "view": "Plan tab → the six questions → Make my plan (Your plan)"
   }
  },
  "apisNote": "Rebuilt 9 September 2026 from the 4 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "_platform": {
   "code": "P02",
   "audience": "guest",
   "formFactor": "mobileApp",
   "shortName": "Guest App",
   "name": "Guest App — Mobile",
   "offlineCapable": true,
   "offlineBanner": {
    "kind": "banner",
    "state": "warning",
    "message": "You're offline. Connect to the internet to book, pay, order or join a queue.",
    "shows": "The moment the connection drops, on every screen, above the screen's own content.",
    "clears": "By itself as soon as the connection is back, with a short \"Back online\" confirmation.",
    "never": "Covers what is already on screen, or appears for a server error — that is the screen's own error state, and a guest told they are offline when the venue is down reconnects for nothing.",
    "provenance": "Decided 12 September 2026 — guest web and guest app behave identically offline and say so with the same banner."
   },
   "app": "guest-app",
   "operator": "guest",
   "targetApp": {
    "app": "guest",
    "name": "TICVAI Guest",
    "shell": "mobile",
    "siblings": [
     "P01",
     "P05"
    ],
    "note": "**One guest product in three shells.** Web, mobile and kiosk share 73–91% of their operations; the kiosk is the same product in a fixed frame with no keyboard, and is deliberately narrower rather than different.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "GST-054",
  "name": "AI Planner",
  "module": "Engagement & Support",
  "requiresModule": "ai",
  "wave": 1,
  "capability": "AI-35",
  "implementation": {
   "app": "guest-app",
   "route": "/general/ai-optimized-itinerary",
   "component": "apps/guest-app/src/routes/general/AiOptimizedItineraryDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "inferred": false,
   "entryFrom": [
    "GST-053"
   ],
   "exitTo": [
    "GST-053",
    "GST-059",
    "GST-001"
   ],
   "transitions": [
    {
     "to": "GST-053",
     "trigger": "Back to your plan",
     "carries": [
      "planId"
     ],
     "provenance": "decided 29 September 2026, MOB-6"
    },
    {
     "to": "GST-059",
     "trigger": "They follow it through the day",
     "carries": [
      "planId"
     ],
     "provenance": "decided 29 September 2026, MOB-6"
    },
    {
     "to": "GST-001",
     "trigger": "Home tab",
     "provenance": "decided 29 September 2026, MOB-1"
    }
   ]
  },
  "notes": "Minuted 10 Aug §4.9. **The AI half is Wave 2** — the manual planner must work without it (CF-41). **Guest concierge confirmed in Phase 1 on 17 August (CF-14), charged per token and bounded by `AiPolicy.guestCapabilityScope`.** Still degrades to the manual planner rather than to an error. ** wired 24 August.** The board drew four bespoke AI endpoints for itinerary planning; **one operation with a kind answers all of them** (ADR-0028), and recording the outcome is what lets a model replace the heuristic later. **`recordSuggestionOutcome` removed from the guest surface.** `check-screens` refused it and was right: **a guest does not record an outcome — the platform observes what they did.** A guest app that self-reports whether it took the advice is a training label the guest could forge, and the observation belongs server-side where the plan and the visit can be compared. **Out of the first release** (decided 28 September, audit R187): the itinerary planner is deferred and this screen is `wave: 4` with a `deferred` block. Kept, not deleted, for the release that builds it. **Itinerary suggestion removed 28 September** (decided 28 September, audit R209): the planner is deferred (R187) and `requestSuggestion` refuses a guest anything but prepPlan, upsell and waitTime, so this screen no longer asks for a day plan.\n\n**Rev 3 (decided 29 September).** Had stayed in wave 4 (GAP-C3); superseded the same day by the re-plan below.\n\n**Brought into Block A on 29 September** (Chinmay, the 29 September re-plan, MOB-6): a rules-based planner with the AI planner agent on top. This supersedes audit R187, the deferral half of R209 and rev 3 GAP-C3; the `deferred` block is removed and the screen is wave 1.\n\n**Mobile v4 role (MOB-6): \"AI Planner\".** The agent refines the rules plan by chat; its tools are the plan operations, and `requestSuggestion` gains the guest-allowed kind `itinerary` (what R209 said to add if the planner ships). AI writes only `ai.*` stores; the plan change itself is `updateVisitPlan`. **The rules plan never fails over to an error**: with AI off, not licensed or failing, the guest keeps the rules plan and the Plan tab works in full.\n\n**Grounding (client meeting 30 September, MoM 4.7, Allam).** The agent's candidates are only the rides, dining and retail (shops and kiosks) of each day's own park, as the plan operations return them; `updateVisitPlan` refuses a point from another park (`point-not-at-day-venue`) as the backstop.",
  "density": "comfortable",
  "pattern": "listDetail",
  "patternReason": "`listProducts` reads the population and `getWaitTimes` reads one of them — list, select, act",
  "purpose": "Ask the planner in your own words to change the plan; it refines the rules plan, and the rules plan stays if AI is unavailable.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "timeline",
       "label": "Your plan",
       "bindsTo": "VisitPlanItem",
       "operation": "getVisitPlan",
       "notes": "The current plan version, updated as the agent changes it.",
       "provenance": "decided 29 September 2026, MOB-6"
      },
      {
       "kind": "assistantPanel",
       "label": "Ask the planner",
       "operation": "sendAiMessage",
       "notes": "e.g. *More shows, fewer coasters on day 2*. The agent calls `requestSuggestion` kind `itinerary` and applies the result with `updateVisitPlan`; Undo on GST-053 reverts it. **Grounded in each day's park** (client meeting 30 September, MoM 4.7): it proposes only rides, dining and shops (kiosks included) that the plan operations return for that day's venue; asked for something the park lacks (*Indian food on day 1*), it says the park has none and names the park that does, and never places another park's restaurant or shop.",
       "provenance": "decided 29 September 2026, MOB-6"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "banner",
       "label": "Planner unavailable",
       "operation": "getVisitPlan",
       "notes": "**The rules plan never fails over to an error**: with AI off, not licensed or failing, the guest keeps the rules plan and the Plan tab works in full. Shown when AI is off for the venue, the tenant has no AI licence, or the call fails or times out.",
       "provenance": "decided 29 September 2026, MOB-6"
      },
      {
       "kind": "detailPanel",
       "label": "The wait time",
       "operation": "getWaitTimes",
       "notes": "Live waits the agent plans around.",
       "provenance": "contract queue.yaml GET /queues/wait-times"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Apply this change",
       "operation": "updateVisitPlan",
       "notes": "Saves the agent's proposal as a new plan version.",
       "provenance": "decided 29 September 2026, MOB-6"
      },
      {
       "kind": "secondaryButton",
       "label": "Back to your plan",
       "notes": "GST-053.",
       "provenance": "decided 29 September 2026, MOB-6"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The plan builds in place; the inputs stay on screen.",
   "error": "Could not load the plan. Names what failed; the inputs are kept so trying again costs nothing.",
   "emptyFirstRun": "No conversation yet: the plan is shown with example requests.",
   "emptyNoResults": "Nothing suits the whole party on that day (for example every ride is over a child's height): says so and offers to change the answers.",
   "emptyNoAccess": "A guest holds no permission. A plan that is not theirs says so without saying whose it is; a signed-out guest can still build a plan and is asked to sign in only to save or book it.",
   "offline": "**The offline banner shows.** What was already loaded stays on screen, marked with its age. Anything that spends money, holds capacity or changes the account waits for the connection, and its button says so rather than failing.",
   "aiUnavailable": "**Falls back to the rules plan, never to an error** (MOB-6): the plan from `getVisitPlan` stays on screen with a short note, and the guest carries on editing it on GST-053."
  },
  "apis": [
   {
    "operationId": "getWaitTimes",
    "contract": "queue",
    "purpose": "Wait times across a venue",
    "trigger": "onLoad"
   },
   {
    "operationId": "sendAiMessage",
    "contract": "ai",
    "purpose": "Chat with the planner agent; its tools are the plan operations, so a change it makes is a new plan version",
    "trigger": "onAction",
    "invalidates": [
     "listProducts"
    ]
   },
   {
    "operationId": "getVisitPlan",
    "contract": "venue-map",
    "purpose": "The plan: days, timed items and add-on suggestions, at its current version",
    "trigger": "onLoad",
    "provenance": "decided 29 September 2026, MOB-6"
   },
   {
    "operationId": "updateVisitPlan",
    "contract": "venue-map",
    "purpose": "Swap, remove, add or undo: each change is a new version, so undo goes back one",
    "trigger": "onAction",
    "provenance": "decided 29 September 2026, MOB-6"
   },
   {
    "operationId": "createAiConversation",
    "contract": "ai",
    "purpose": "Open the planner conversation for this plan",
    "trigger": "onLoad",
    "provenance": "decided 29 September 2026, MOB-6"
   },
   {
    "operationId": "requestSuggestion",
    "contract": "ai",
    "purpose": "A suggestion of kind `itinerary` (guest-allowed since 29 September): the planner agent's proposal for the plan, applied through `updateVisitPlan`",
    "trigger": "onAction",
    "provenance": "decided 29 September 2026, MOB-6"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "planId",
     "from": "GST-053"
    },
    {
     "name": "conversationId",
     "from": "deepLink",
     "optional": true
    },
    {
     "name": "venueId",
     "from": "session"
    }
   ],
   "coldEntry": "A planner link from a notification: opens the plan and its conversation, or the plan alone if the conversation was closed."
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "client-verified",
   "board": "wireframes/P02 Guest App.dc.html#gst-054",
   "prototype": {
    "file": "sources/designs/guest-rev3-30-september/TICVAI Mobile App v4.dc.html",
    "rev": "mobile v4 (30 September build)",
    "verified": "2026-10-01",
    "match": "partial",
    "view": "Ask Sahli (the assistant chat; v4 has no plan-specific chat)",
    "differences": "v4 draws the rules plan and a general assistant chat; it has no plan-specific chat. Built from this definition."
   }
  },
  "apisNote": "Rebuilt 9 September 2026 from the 4 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "machine": {
   "key": "plannerMode",
   "initial": "rulesPlan",
   "provenance": "decided 29 September 2026, MOB-6; BRIEF decision 1: the rules planner with the AI planner agent on top",
   "states": {
    "rulesPlan": {
     "operation": "getVisitPlan",
     "note": "The rules plan is shown; the chat is open."
    },
    "refining": {
     "operation": "sendAiMessage",
     "note": "The agent is working on a request."
    },
    "proposed": {
     "operation": "requestSuggestion",
     "note": "A change is proposed, not yet saved."
    },
    "aiUnavailable": {
     "note": "**The rules plan never fails over to an error**: with AI off, not licensed or failing, the guest keeps the rules plan and the Plan tab works in full.",
     "retryTo": "rulesPlan"
    }
   },
   "transitions": [
    {
     "from": "rulesPlan",
     "on": "Send",
     "to": "refining"
    },
    {
     "from": "refining",
     "on": "proposal returned",
     "to": "proposed"
    },
    {
     "from": "proposed",
     "on": "Apply this change",
     "to": "rulesPlan",
     "note": "updateVisitPlan saves a new version."
    },
    {
     "from": "proposed",
     "on": "Discard",
     "to": "rulesPlan"
    },
    {
     "from": "refining",
     "on": "AI off, refused or timed out",
     "to": "aiUnavailable"
    },
    {
     "from": "rulesPlan",
     "on": "AI off for the venue",
     "to": "aiUnavailable"
    }
   ]
  },
  "_platform": {
   "code": "P02",
   "audience": "guest",
   "formFactor": "mobileApp",
   "shortName": "Guest App",
   "name": "Guest App — Mobile",
   "offlineCapable": true,
   "offlineBanner": {
    "kind": "banner",
    "state": "warning",
    "message": "You're offline. Connect to the internet to book, pay, order or join a queue.",
    "shows": "The moment the connection drops, on every screen, above the screen's own content.",
    "clears": "By itself as soon as the connection is back, with a short \"Back online\" confirmation.",
    "never": "Covers what is already on screen, or appears for a server error — that is the screen's own error state, and a guest told they are offline when the venue is down reconnects for nothing.",
    "provenance": "Decided 12 September 2026 — guest web and guest app behave identically offline and say so with the same banner."
   },
   "app": "guest-app",
   "operator": "guest",
   "targetApp": {
    "app": "guest",
    "name": "TICVAI Guest",
    "shell": "mobile",
    "siblings": [
     "P01",
     "P05"
    ],
    "note": "**One guest product in three shells.** Web, mobile and kiosk share 73–91% of their operations; the kiosk is the same product in a fixed frame with no keyboard, and is deliberately narrower rather than different.",
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
 "addCartLine": {
  "method": "POST",
  "path": "/carts/{cartId}/lines",
  "contract": "orders",
  "summary": "Add something",
  "permission": null,
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
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "AddCartLineRequest",
  "responds": "Cart"
 },
 "bookVisitPlan": {
  "method": "POST",
  "path": "/visit-plans/{planId}/booking",
  "contract": "venue-map",
  "summary": "Book this plan — turn it into cart lines",
  "permission": null,
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
  "responds": "VisitPlanBooking"
 },
 "checkoutCart": {
  "method": "POST",
  "path": "/carts/{cartId}/checkout",
  "contract": "orders",
  "summary": "Turn the cart into an order",
  "permission": null,
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
  "responds": "Order"
 },
 "claimLocationSession": {
  "method": "POST",
  "path": "/location-sessions",
  "contract": "fnb",
  "summary": "Tell the platform where the guest is",
  "permission": null,
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
  "responds": "LocationSession"
 },
 "createAiConversation": {
  "method": "POST",
  "path": "/conversations",
  "contract": "ai",
  "summary": "Open a conversation",
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
  "responds": "AiConversation"
 },
 "createGuestFnbOrder": {
  "method": "POST",
  "path": "/guest-orders",
  "contract": "fnb",
  "summary": "A guest orders food",
  "permission": null,
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
  "requestBody": "CreateGuestOrderRequest",
  "responds": "GuestOrderResult"
 },
 "generateVisitPlan": {
  "method": "POST",
  "path": "/visit-plans",
  "contract": "venue-map",
  "summary": "Build a visit plan from the party, the dates and what they like",
  "permission": null,
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
  "requestBody": "VisitPlanRequest",
  "responds": "VisitPlan"
 },
 "getCart": {
  "method": "GET",
  "path": "/carts/{cartId}",
  "contract": "orders",
  "summary": "The cart, priced and checked, right now",
  "permission": null,
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
  "responds": "Cart"
 },
 "getGuestMenu": {
  "method": "GET",
  "path": "/outlets/{outletId}/guest-menu",
  "contract": "fnb",
  "summary": "The menu a guest sees",
  "permission": null,
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "at",
    "in": "query",
    "required": null
   },
   {
    "name": "language",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "GuestMenu"
 },
 "getGuestOrderStatus": {
  "method": "GET",
  "path": "/guest-orders/{orderId}",
  "contract": "fnb",
  "summary": "Track an order",
  "permission": null,
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "GuestOrderStatus"
 },
 "getTenantAppStatus": {
  "method": "GET",
  "path": "/tenant-config/status",
  "contract": "white-label",
  "summary": "App status and recent changes",
  "permission": null,
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [],
  "requestBody": null,
  "responds": "TenantAppStatus"
 },
 "getVisitPlan": {
  "method": "GET",
  "path": "/visit-plans/{planId}",
  "contract": "venue-map",
  "summary": "A visit plan, at its current version or an earlier one",
  "permission": null,
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "version",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "VisitPlan"
 },
 "getWaitTimes": {
  "method": "GET",
  "path": "/queues/wait-times",
  "contract": "queue",
  "summary": "Wait times across a venue",
  "permission": null,
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "venueId",
    "in": "query",
    "required": true
   },
   {
    "name": "category",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "WaitTime"
 },
 "handoverToAgent": {
  "method": "POST",
  "path": "/conversations/{conversationId}/handover",
  "contract": "marketing-crm",
  "summary": "Pass an assistant conversation to a person",
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
  "responds": "Conversation"
 },
 "listCatalogueBundles": {
  "method": "GET",
  "path": "/catalogue/bundles",
  "contract": "catalogue",
  "summary": "List published catalogue bundles",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "BundleSummary"
 },
 "listContentPages": {
  "method": "GET",
  "path": "/tenant-config/pages",
  "contract": "white-label",
  "summary": "List custom content pages",
  "permission": "TENANT_CONFIGURE",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": "status",
    "in": "query",
    "required": null
   },
   {
    "name": "categoryCode",
    "in": "query",
    "required": null
   },
   {
    "name": "slug",
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
 "listFaqs": {
  "method": "GET",
  "path": "/tenant-config/faqs",
  "contract": "white-label",
  "summary": "List FAQs",
  "permission": "TENANT_CONFIGURE",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [],
  "requestBody": null,
  "responds": "FaqCategory"
 },
 "listMyCases": {
  "method": "GET",
  "path": "/my/cases",
  "contract": "marketing-crm",
  "summary": "The cases this guest raised",
  "permission": null,
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
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
 "listMyNotifications": {
  "method": "GET",
  "path": "/me/notifications",
  "contract": "marketing-crm",
  "summary": "The signed-in guest's notification feed",
  "permission": null,
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
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
   },
   {
    "name": "unreadOnly",
    "in": "query",
    "required": null
   },
   {
    "name": "venueId",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "Page"
 },
 "listProducts": {
  "method": "GET",
  "path": "/products",
  "contract": "catalogue",
  "summary": "List products",
  "permission": "PRODUCT_VIEW",
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
    "name": "kind",
    "in": "query",
    "required": null
   },
   {
    "name": "isSellable",
    "in": "query",
    "required": null
   },
   {
    "name": "categoryId",
    "in": "query",
    "required": null
   },
   {
    "name": "segmentTag",
    "in": "query",
    "required": null
   },
   {
    "name": "guidedAnswerIds",
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
 "listVisitPlanAlternatives": {
  "method": "GET",
  "path": "/visit-plans/{planId}/items/{itemId}/alternatives",
  "contract": "venue-map",
  "summary": "What could take this item's place",
  "permission": null,
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
 "markMyNotificationsRead": {
  "method": "POST",
  "path": "/me/notifications/read",
  "contract": "marketing-crm",
  "summary": "Mark the signed-in guest's notifications read",
  "permission": null,
  "offlineCapable": true,
  "conflictPolicy": "lastWriterWins",
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
 "raiseMyCase": {
  "method": "POST",
  "path": "/my/cases",
  "contract": "marketing-crm",
  "summary": "Report something — lost property, a complaint, a question",
  "permission": null,
  "offlineCapable": false,
  "conflictPolicy": "append",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "Case"
 },
 "recordAnswerFeedback": {
  "method": "POST",
  "path": "/messages/{messageId}/feedback",
  "contract": "ai",
  "summary": "Say whether an answer helped",
  "permission": "AI_USE",
  "offlineCapable": false,
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
  "responds": "AiAnswerFeedback"
 },
 "replyToMyCase": {
  "method": "POST",
  "path": "/my/cases/{caseId}/messages",
  "contract": "marketing-crm",
  "summary": "Reply on a case the guest raised",
  "permission": null,
  "offlineCapable": false,
  "conflictPolicy": "append",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "CaseDetail"
 },
 "requestSuggestion": {
  "method": "POST",
  "path": "/ai/suggestions",
  "contract": "ai",
  "summary": "Ask for an answer, however it is currently produced",
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
  "responds": "Suggestion"
 },
 "sendAiMessage": {
  "method": "POST",
  "path": "/conversations/{conversationId}/messages",
  "contract": "ai",
  "summary": "Ask",
  "permission": "AI_USE",
  "offlineCapable": false,
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
  "responds": "AiMessage"
 },
 "sendConversationMessage": {
  "method": "POST",
  "path": "/conversations/{conversationId}/messages",
  "contract": "marketing-crm",
  "summary": "Say something, as a guest or an agent",
  "permission": "CASE_MANAGE",
  "offlineCapable": false,
  "conflictPolicy": "append",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "ConversationMessage"
 },
 "submitReview": {
  "method": "POST",
  "path": "/reviews",
  "contract": "marketing-crm",
  "summary": "Submit a review",
  "permission": null,
  "offlineCapable": false,
  "conflictPolicy": "append",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "SubmitReviewRequest",
  "responds": "Review"
 },
 "updateVisitPlan": {
  "method": "PUT",
  "path": "/visit-plans/{planId}",
  "contract": "venue-map",
  "summary": "Swap, remove, add, move or undo, as a new version",
  "permission": null,
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
  "requestBody": "VisitPlanUpdate",
  "responds": "VisitPlan"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "AddCartLineRequest": {
  "type": "object",
  "x-ticvai-persistence": "none — request only",
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
    "format": "uuid"
   },
   "bookedWindow": {
    "$ref": "#/components/schemas/BookedWindow"
   },
   "recommendationId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The `trackingId` of the ai `decideRecommendations` item this line came from (29 September, build, AI system design 2.2 A step 8), so a purchase is attributed to the recommendation that led to it rather than guessed. Optional; sent by a page or till that shows the engine's recommendations. Not validated against the engine: an unknown id only fails to attribute.\n"
   },
   "tableReservationId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "A table deposit line (decided 29 September, rev 3 REV3-8b): the `fnb.TableReservation` in `awaitingDeposit` this pays for, sent with `variantId` set to the booking's `deposit.variantId` and `quantity` 1. The price is the booking's `deposit.amount`. A booking that is not awaiting a deposit is refused 422 `depositNotDue`.\n"
   },
   "seatIds": {
    "type": "array",
    "maxItems": 50,
    "description": "At most `VenueSettings.seating.maxSeatsPerGuestOrder` seats per booking on a guest channel (default 10, bounds 1 to 50, decided 29 September, rev 3 REV3-7); at most 10 per sale on staff and POS (audit R080 (c)). Over the limit is 422 `seatLimitExceeded`.",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "resourceHoldId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "A `resources.ResourceHold` on a resource the guest picked on a venue map (decided 29 September, rev 3 REV3-15); `variantId` is the placed resource's price-band variant and `quantity` is 1. The hold is the line's capacity; no inventory lease is taken."
   },
   "parentLineId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "For an add-on attaching to a ticket already in the cart. **Removing the parent removes the child** — a locker with no admission is not a sale.\n"
   },
   "attributes": {
    "$ref": "#/components/schemas/OrderLineAttributes"
   }
  }
 },
 "AiAnswerFeedback": {
  "type": "object",
  "x-ticvai-persistence": "ai.answer_feedback",
  "description": "**What a person thought of an answer** (AIC-062). One label per message per person; it feeds the golden sets and the knowledge-gap list, never an online update (design 3.5).",
  "required": [
   "messageId",
   "rating"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "messageId": {
    "type": "string",
    "format": "uuid",
    "x-ticvai-references": "ai.message"
   },
   "conversationId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "x-ticvai-references": "ai.conversation"
   },
   "rating": {
    "type": "string",
    "enum": [
     "helpful",
     "notHelpful"
    ]
   },
   "reason": {
    "type": "string",
    "enum": [
     "wrong",
     "outdated",
     "incomplete",
     "notGrounded",
     "unsafe",
     "other"
    ],
    "nullable": true
   },
   "comment": {
    "type": "string",
    "nullable": true,
    "maxLength": 1000
   },
   "audience": {
    "type": "string",
    "enum": [
     "staff",
     "guest"
    ],
    "readOnly": true
   },
   "principalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true,
    "x-ticvai-references": "identity.principal"
   },
   "subjectId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true,
    "description": "The guest, where the audience is `guest`."
   },
   "createdAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."
   }
  }
 },
 "AiConversation": {
  "type": "object",
  "x-ticvai-persistence": "ai.conversation",
  "required": [
   "id",
   "principalId",
   "module",
   "startedAt"
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
   "scopePath": {
    "type": "string"
   },
   "module": {
    "$ref": "../shared/common.yaml#/components/schemas/ModuleKey"
   },
   "locale": {
    "type": "string"
   },
   "messageCount": {
    "type": "integer"
   },
   "startedAt": {
    "type": "string",
    "format": "date-time"
   },
   "lastMessageAt": {
    "type": "string",
    "format": "date-time"
   }
  }
 },
 "AiMaturity": {
  "type": "object",
  "x-ticvai-persistence": "none — embedded as jsonb on ai.suggestion and ai.forecast_version",
  "description": "**Where an answer stands, on every answer** (29 September, AI functions review; baseline then learn). The customer sees a stage badge and a \"Based on\" chip, never a bare percentage (design 5.6), and \"Limited historical data\" while the starting pattern carries more than half the weight.",
  "required": [
   "stage",
   "basedOn"
  ],
  "properties": {
   "stage": {
    "type": "string",
    "enum": [
     "starting",
     "learning",
     "established",
     "learned"
    ],
    "description": "`starting`: the baseline (venue AI settings, the starting pattern for the venue type, the UAE calendar, weather). `learning`: own data carries short-range patterns (about 4 weeks). `established`: own level and trend lead, the baseline fills gaps such as a holiday not yet seen (about 3 months, or at once with 12+ months imported). `learned`: a model trained on this tenant's data, promoted by an admin (AI-D16)."
   },
   "basedOn": {
    "type": "string",
    "description": "The \"Based on\" line, in words, e.g. *Based on: your venue profile, UAE calendar, weather, 23 days of your sales*. Always present."
   },
   "sources": {
    "type": "array",
    "items": {
     "type": "object",
     "required": [
      "source"
     ],
     "properties": {
      "source": {
       "type": "string",
       "enum": [
        "venueSettings",
        "startingPattern",
        "calendar",
        "weather",
        "bookingsOnHand",
        "ownHistory",
        "importedHistory",
        "configuration",
        "trainedModel"
       ]
      },
      "detail": {
       "type": "string",
       "nullable": true,
       "description": "e.g. *23 days*, *water park pattern v3*, *Eid al-Adha 2027*."
      },
      "observations": {
       "type": "integer",
       "nullable": true
      }
     }
    }
   },
   "ownDataShare": {
    "type": "number",
    "minimum": 0,
    "maximum": 1,
    "description": "The weight own data carries, `n / (k + n)`. Below 0.5 the answer is marked \"Limited historical data\"."
   },
   "limitedHistory": {
    "type": "boolean"
   },
   "nextStage": {
    "type": "object",
    "nullable": true,
    "description": "What the next stage needs, e.g. *8 more Saturdays of sales*, or *an admin promotion*.",
    "properties": {
     "stage": {
      "type": "string",
      "enum": [
       "learning",
       "established",
       "learned"
      ]
     },
     "needs": {
      "type": "string"
     },
     "expectedBy": {
      "type": "string",
      "format": "date",
      "nullable": true
     }
    }
   }
  }
 },
 "AiMessage": {
  "type": "object",
  "x-ticvai-persistence": "ai.message",
  "required": [
   "id",
   "conversationId",
   "role",
   "content",
   "createdAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "conversationId": {
    "type": "string",
    "format": "uuid"
   },
   "role": {
    "type": "string",
    "enum": [
     "user",
     "assistant",
     "system"
    ]
   },
   "content": {
    "type": "string"
   },
   "sources": {
    "$ref": "#/components/schemas/AiSourceList"
   },
   "confidence": {
    "type": "number",
    "nullable": true,
    "description": "8.1.5, 8.3.67. **Nullable on purpose** — a provider that does not report confidence must yield null rather than an invented number, and an interface showing 0.9 because the code defaulted it is worse than showing nothing.\n"
   },
   "rationale": {
    "type": "string",
    "nullable": true,
    "description": "8.3.68, 8.3.69."
   },
   "proposedAction": {
    "allOf": [
     {
      "$ref": "#/components/schemas/ProposedAction"
     }
    ],
    "nullable": true,
    "description": "Present where the answer suggests a change. **A draft, never applied here.**"
   },
   "traceId": {
    "type": "string"
   },
   "provider": {
    "$ref": "#/components/schemas/AiProviderKind"
   },
   "model": {
    "type": "string"
   },
   "promptTokens": {
    "type": "integer"
   },
   "completionTokens": {
    "type": "integer"
   },
   "latencyMs": {
    "type": "integer"
   },
   "createdAt": {
    "type": "string",
    "format": "date-time"
   }
  }
 },
 "AiProviderKind": {
  "type": "string",
  "enum": [
   "openai",
   "gemini",
   "anthropic",
   "azureOpenai",
   "localLlm",
   "openaiCompatible"
  ],
  "description": "`openaiCompatible` (added 29 September, AI design 3.3): a customer endpoint that speaks the OpenAI API, taken with no custom development (AIC-009). Any other protocol needs an adapter.\n"
 },
 "AiSourceList": {
  "type": "array",
  "x-ticvai-persistence-kind": "valueObject",
  "x-ticvai-persistence-column": "jsonb",
  "description": "**The sources an answer was grounded in, stored with the answer** (8.3.70). One `jsonb` column on the row that carries it — `ai.message.sources` and `ai.activity.sources` — because the grounding audit reads the list as it was when the answer was given, and a source is never queried on its own.\n",
  "items": {
   "$ref": "#/components/schemas/AiSource"
  }
 },
 "AllergenCode": {
  "type": "string",
  "description": "**The fourteen declarable allergens, as one closed list.** Every allergen field in this contract uses it — the menu claim, the ticket line, a substitution's delta, a modifier option, the label on a bag — so a declared set and an actual set compare without anybody normalising case or synonyms. It was the `Allergen.contains` enum; the other fields were free text.\n",
  "enum": [
   "gluten",
   "crustaceans",
   "eggs",
   "fish",
   "peanuts",
   "soybeans",
   "milk",
   "nuts",
   "celery",
   "mustard",
   "sesame",
   "sulphites",
   "lupin",
   "molluscs"
  ]
 },
 "AppAvailability": {
  "type": "string",
  "description": "**The sold-out or closed signal (decided 28 September, audit R073).** `open` is the normal state. `soldOut` shows WEB-029's sold-out state across the app while browsing still works; `closed` shows the closed state (a weather closure, a private event). Neither refuses a request on its own: it is what the guest is told, and a sale is still refused by availability where it applies. Set with `setMaintenanceMode`.\n",
  "enum": [
   "open",
   "soldOut",
   "closed"
  ],
  "default": "open"
 },
 "BookedWindow": {
  "type": "object",
  "nullable": true,
  "x-ticvai-persistence": "none — embedded as window_starts_at and window_ends_at on orders.cart_line and orders.order_line",
  "description": "**The booked time window of an hourly product, such as a meeting room** (decided 29 September, rev 3 REV3-13: meeting rooms by the hour are in scope). The guest picks a date, a length and a start time from `resources.listProductStartTimes`; the length is the product's `length` variant (1 hour, 2 hours, half day, full day), priced per variant, so the price is the variant's. **`endsAt` minus `startsAt` must equal the chosen variant's length** (its `length` dimension value's `durationMinutes`), or the line is refused 422 `windowLengthMismatch`. Required on a product with `catalogue.Product.requiresTimeWindow` true and refused on any other (`windowRequired`, `windowNotAllowed`). The room itself is not named here: the window holds capacity of the room type, and `resources.allocateResources` picks the room at checkout (26 August minute: a guest books a meeting room product, never a raw room).\n",
  "required": [
   "startsAt",
   "endsAt"
  ],
  "properties": {
   "startsAt": {
    "type": "string",
    "format": "date-time"
   },
   "endsAt": {
    "type": "string",
    "format": "date-time",
    "description": "After `startsAt`, on the same venue day."
   }
  }
 },
 "BundleSummary": {
  "x-ticvai-persistence": "none — projection over bundle",
  "type": "object",
  "description": "One published catalogue bundle — the signed snapshot terminals pull (ADR-0013). Not `promotions.Bundle`, which is a sellable product made of other products.",
  "required": [
   "version",
   "venueId",
   "publishedAt",
   "publishedBy",
   "contentHash",
   "staleAfter",
   "sizeBytes"
  ],
  "properties": {
   "version": {
    "type": "string"
   },
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "publishedAt": {
    "type": "string",
    "format": "date-time"
   },
   "publishedBy": {
    "type": "string",
    "format": "uuid"
   },
   "contentHash": {
    "type": "string"
   },
   "signatureKeyId": {
    "type": "string",
    "description": "Key that signed this bundle. A terminal offline across a key rotation needs a grace window, or it cannot verify the next bundle.\n"
   },
   "staleAfter": {
    "type": "string",
    "format": "date-time"
   },
   "sizeBytes": {
    "type": "integer"
   },
   "note": {
    "type": "string"
   },
   "appliedByWorkstations": {
    "type": "integer"
   }
  }
 },
 "Cart": {
  "type": "object",
  "x-ticvai-persistence": "orders.cart",
  "required": [
   "id",
   "venueId",
   "channel",
   "status",
   "lines"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "token": {
    "type": "string",
    "readOnly": true,
    "description": "**How an anonymous guest returns to their cart**, including from a recovery email. Rotated on claim, so a link shared before signing in does not reach the account after.\n"
   },
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "channel": {
    "$ref": "../shared/common.yaml#/components/schemas/SalesChannel"
   },
   "subjectId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Null while anonymous. Set by `claimCart`."
   },
   "status": {
    "$ref": "#/components/schemas/CartStatus"
   },
   "lines": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/CartLine"
    }
   },
   "conflicts": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/CartConflict"
    }
   },
   "consentQuestions": {
    "type": "array",
    "readOnly": true,
    "description": "**The consent questions this cart's products and flow ask** (decided 29 September, rev 3 REV3-26), computed on read at their current version as **the union of each line's published booking flow's `white-label.BookingFlow.settings.consentQuestionIds`** (the flow `getPublishedBookingFlow` resolves for the line's product: product, then category, then the venue's flow for the kind; moved from `BookingFlowConfig`, 29 September W12) **and every line's `catalogue.Product.consentQuestionIds`, each question once**: the flow's first, in its order, then each product's in cart-line order, a question already listed not repeated (its `lineIds` gain the line). The client asks them, in the order given, and sends the answers to `marketing.recordConsentAnswers`; `answered` then turns true. One or several, as the venue chose. `checkoutCart` refuses while a required one is unanswered.\n",
    "items": {
     "allOf": [
      {
       "$ref": "../satellite/marketing-crm.yaml#/components/schemas/ConsentQuestion"
      },
      {
       "type": "object",
       "properties": {
        "lineIds": {
         "type": "array",
         "description": "The cart lines that ask it. Empty for a question the flow asks.",
         "items": {
          "type": "string",
          "format": "uuid"
         }
        },
        "answered": {
         "type": "boolean",
         "description": "Every person (for `perPerson`) or the booking (for `perBooking`) has an answer."
        }
       }
      }
     ]
    }
   },
   "subtotal": {
    "x-ticvai-column": "net_amount",
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "discountTotal": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "taxTotal": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "total": {
    "x-ticvai-column": "gross_amount",
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "appliedPromotionIds": {
    "type": "array",
    "description": "**Re-evaluated on every read.** A promotion that expired while the cart sat must not still be applied at checkout, and a promotion that became applicable should be.\n",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "couponCodes": {
    "type": "array",
    "readOnly": true,
    "description": "The promo codes the guest entered through `applyCartPromoCode` (decided 28 September, audit R073 (e)). **Sent as `couponCodes` on every promotions evaluation of this cart**, so a code is re-checked on each read like any promotion; a code that stops qualifying stays listed here and its promotion drops out of `appliedPromotionIds`.\n",
    "items": {
     "type": "string",
     "maxLength": 100
    }
   },
   "expiresAt": {
    "type": "string",
    "format": "date-time",
    "description": "The earliest lease expiry in the cart, or the cart's own window where it holds none."
   },
   "extensionsUsed": {
    "type": "integer",
    "readOnly": true
   },
   "maxExtensions": {
    "type": "integer",
    "readOnly": true
   },
   "locale": {
    "type": "string"
   },
   "createdAt": {
    "type": "string",
    "format": "date-time"
   },
   "updatedAt": {
    "type": "string",
    "format": "date-time"
   }
  }
 },
 "CartConflict": {
  "type": "object",
  "x-ticvai-persistence": "none — computed on read",
  "description": "2.9.5. Golf at 13:00 and karting at 13:00 for the same guest. **A prompt, not a refusal** — a party of four may legitimately split, and refusing would be wrong more often than right.\n",
  "properties": {
   "kind": {
    "type": "string",
    "enum": [
     "overlappingTime",
     "sameSessionDifferentVenue",
     "exceedsPartySize",
     "requiresPrerequisite",
     "consentBlocksBooking"
    ]
   },
   "lineIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "message": {
    "type": "string"
   },
   "isBlocking": {
    "type": "boolean",
    "description": "Most are not. `requiresPrerequisite` is — an add-on with no ticket to attach to cannot be sold. So is `consentBlocksBooking`: a consent question answered with the answer the venue set to block the booking (decided 29 September, rev 3 REV3-26).\n"
   }
  }
 },
 "CartLine": {
  "type": "object",
  "x-ticvai-persistence": "orders.cart_line",
  "required": [
   "id",
   "variantId",
   "quantity"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "variantId": {
    "type": "string",
    "format": "uuid"
   },
   "productName": {
    "type": "string",
    "readOnly": true
   },
   "quantity": {
    "type": "integer",
    "minimum": 1
   },
   "performanceId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "bookedWindow": {
    "$ref": "#/components/schemas/BookedWindow"
   },
   "recommendationId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The `trackingId` of the ai `decideRecommendations` item this line came from (29 September, build, AI system design 2.2 A step 8), so a purchase is attributed to the recommendation that led to it rather than guessed. Set from `addCartLine`; checkout copies it to the order line.\n"
   },
   "tableReservationId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Set on a table deposit line only (decided 29 September, rev 3 REV3-8b): the `fnb.TableReservation` this line secures. Priced from the deposit the booking snapshotted, not from the variant. Becomes an `orders.deposit` row at checkout, not revenue. A table booking with no deposit never has a line (rev 3 REV3-8).\n"
   },
   "seatIds": {
    "type": "array",
    "maxItems": 50,
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "resourceHoldId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The `resources.ResourceHold` this line buys (decided 29 September, rev 3 REV3-15). While set, `leaseExpiresAt` is the hold's `expiresAt` and `inventoryHoldId` is null."
   },
   "attributes": {
    "$ref": "#/components/schemas/OrderLineAttributes"
   },
   "parentLineId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The line this add-on is attached to, from `AddCartLineRequest.parentLineId`. Kept on the line because **removing the parent removes the child**, and `removeCartLine` has to be able to find the children.\n"
   },
   "overridePrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "overrideReason": {
    "type": "string",
    "nullable": true,
    "enum": [
     "priceMatch",
     "serviceRecovery",
     "negotiated",
     "damagedGoods",
     "staffSale",
     "error"
    ],
    "description": "BL-085. **An operator could apply an approved discount and not enter a price.** A price match against a competitor and a service-recovery gesture are not discounts off a list — they are a number somebody decided.\n**Escalated above a configured threshold, and the reason is a closed set**: a free-text override reason is an override nobody can report on, and this is the field an auditor reads first.\n"
   },
   "feeKind": {
    "type": "string",
    "nullable": true,
    "enum": [
     "booking",
     "transaction",
     "service",
     "delivery",
     "convenience",
     "cancellation"
    ],
    "description": "**A fee is a line, not an adjustment.** `orders` already separates a service charge from a tip for the reason that applies here: **a guest is entitled to see what they are being charged for**, and a fee folded into the ticket price is a fee nobody can question.\nItemised at checkout, taxed on its own code, and refundable separately — **a cancellation fee is usually the one thing not refunded**, which only works if it is its own line.\n"
   },
   "unitPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "lineTotal": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "inventoryHoldId": {
    "type": "string",
    "nullable": true,
    "description": "The capacity held for this line — a `catalogue.InventoryHold.id`, typed as that id is. **Null for a product with no capacity** — a t-shirt needs stock, not a lease.\n"
   },
   "leaseExpiresAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "description": "Shown to the guest. *\"Your seats are held for 6 minutes\"* is better than discovering it at checkout.\n"
   },
   "isAvailable": {
    "type": "boolean",
    "readOnly": true,
    "description": "Re-checked on every read. **A line can become unavailable while the cart sits** — a lease expiring is not the same as the product selling out, and both land here.\n"
   }
  }
 },
 "CartStatus": {
  "type": "string",
  "enum": [
   "active",
   "expiring",
   "expired",
   "abandoned",
   "checkedOut"
  ]
 },
 "Case": {
  "x-ticvai-persistence": "marketing.case",
  "x-ticvai-retired-columns": [
   "guest_name",
   "subject",
   "is_sla_breached"
  ],
  "type": "object",
  "required": [
   "id",
   "caseNumber",
   "subject",
   "status",
   "priority",
   "createdAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "description": "Created on the device (`CreateCaseRequest.id`, `raiseMyCase`), so a UUIDv7."
   },
   "caseNumber": {
    "type": "string",
    "readOnly": true,
    "description": "**Server-assigned: the venue prefix plus a sequence per venue** (decided 28 September, audit R152). Not gapless; only tax invoices are gapless, per legal entity. Assigned when the case reaches the server, so a retry with the same `id` keeps its number.\n"
   },
   "subjectId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "guestName": {
    "type": "string",
    "nullable": true,
    "readOnly": true,
    "x-ticvai-persisted": false,
    "description": "**Resolved from `pii.subject` when the case is read, never stored on the case.** A name copied onto a case row is personal data outside the erasable store (ADR-0023), and it had no source anyway — no request carries it. Returned only to callers holding `GUEST_VIEW_PII`, as `searchGuests` does.\n"
   },
   "subject": {
    "type": "string",
    "x-ticvai-column": "title",
    "description": "**The case's one-line title**, not a person. Stored as `title` so the table does not hold `subject` beside `subject_id`; the wire keeps `subject` because screens bind it.\n"
   },
   "kind": {
    "allOf": [
     {
      "$ref": "#/components/schemas/CaseKind"
     }
    ],
    "nullable": true,
    "description": "What the guest said it was about, where the guest raised it."
   },
   "channel": {
    "allOf": [
     {
      "$ref": "#/components/schemas/MessageChannel"
     }
    ],
    "description": "How the guest reached the venue — `CreateCaseRequest.channel`, or `inApp` for a case raised through `raiseMyCase`."
   },
   "recordedAt": {
    "type": "string",
    "format": "date-time",
    "description": "Device time the case was raised — the start of the SLA clock."
   },
   "syncedAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true,
    "description": "Server time the case arrived. Equal to `recordedAt` for a case raised online."
   },
   "categoryId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "queueId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The `ServiceQueue` the case waits in, set by routing (`CaseRoutingRule.queueId`). Null once routed straight to an agent. (decided 29 September, data model for the agreed operations)"
   },
   "membershipId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The identity membership this case concerns (`identity.customer_membership`); member case notes are cases with this set. (decided 29 September, coordinator decision DM4, writers pass)"
   },
   "status": {
    "$ref": "#/components/schemas/CaseStatus"
   },
   "priority": {
    "$ref": "#/components/schemas/CasePriority"
   },
   "assignedToPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "venueId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "relatedOrderId": {
    "type": "string",
    "nullable": true
   },
   "slaDueAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "isSlaBreached": {
    "type": "boolean",
    "readOnly": true,
    "x-ticvai-persisted": false,
    "description": "**Computed when read, never stored.** True once the case has been open longer than its SLA allows — the time from `recordedAt` to `resolvedAt` (or to now, while unresolved), less `slaPausedSeconds`, is past the target that set `slaDueAt`. A stored flag would need a job to flip it at the moment of breach, and no such job is designed; `listCases?breachedSla` filters on the same computation.\n"
   },
   "slaPausedSeconds": {
    "type": "integer",
    "description": "Accrued only while awaiting the guest. Waiting on an internal team does not pause the clock.\n"
   },
   "escalationCount": {
    "type": "integer"
   },
   "createdAt": {
    "type": "string",
    "format": "date-time"
   },
   "resolvedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   }
  }
 },
 "CaseDetail": {
  "x-ticvai-persistence": "marketing.case",
  "allOf": [
   {
    "$ref": "#/components/schemas/Case"
   },
   {
    "type": "object",
    "properties": {
     "description": {
      "type": "string"
     },
     "resolutionNote": {
      "type": "string",
      "nullable": true
     },
     "messages": {
      "type": "array",
      "items": {
       "$ref": "#/components/schemas/CaseMessage"
      }
     }
    }
   }
  ]
 },
 "CaseKind": {
  "type": "string",
  "description": "**What the guest says the case is about**, in their words rather than the venue's taxonomy — `raiseMyCase` asks for it and `categoryId` is what staff file it under. Stored on the case, because a lost-property report that forgets it was one cannot be routed to the lost and found desk.\n**`other` only with a note (decided 28 September, audit R222).** A case raised as `other` must carry a non-empty `detail` (`raiseMyCase`), or it is refused with 400; the notes are reviewed quarterly to add the real kinds they reveal.\n",
  "enum": [
   "lostProperty",
   "complaint",
   "question",
   "accessibility",
   "refundRequest",
   "other"
  ]
 },
 "CaseMessage": {
  "x-ticvai-persistence": "marketing.case_message",
  "type": "object",
  "required": [
   "id",
   "body",
   "isInternal",
   "authorKind",
   "recordedAt"
  ],
  "properties": {
   "resolution": {
    "type": "string",
    "description": "**What was actually done about it.** Indexed for retrieval: an agent facing a complaint benefits more from how the last one was resolved than from a policy. Without this column `marketing.case` can only embed its subject line.\n"
   },
   "id": {
    "type": "string"
   },
   "body": {
    "type": "string"
   },
   "isInternal": {
    "type": "boolean"
   },
   "authorKind": {
    "type": "string",
    "enum": [
     "agent",
     "guest",
     "system",
     "ai"
    ]
   },
   "authorPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "channel": {
    "$ref": "#/components/schemas/MessageChannel"
   },
   "attachmentRefs": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "recordedAt": {
    "type": "string",
    "format": "date-time",
    "description": "Device time — `addCaseMessage` is offline-capable."
   },
   "syncedAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true,
    "description": "Server time the message arrived."
   }
  }
 },
 "CasePriority": {
  "type": "string",
  "enum": [
   "low",
   "normal",
   "high",
   "urgent"
  ]
 },
 "CaseStatus": {
  "type": "string",
  "enum": [
   "open",
   "inProgress",
   "awaitingGuest",
   "escalated",
   "resolved",
   "closed"
  ]
 },
 "Channel": {
  "type": "string",
  "enum": [
   "pos",
   "kiosk",
   "web",
   "mobile",
   "b2b",
   "ota",
   "callCentre"
  ]
 },
 "ContentPage": {
  "x-ticvai-persistence": "whitelabel.content_page",
  "type": "object",
  "required": [
   "id",
   "slug",
   "title",
   "body",
   "status"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "slug": {
    "type": "string",
    "pattern": "^[a-z0-9-]+$"
   },
   "title": {
    "$ref": "#/components/schemas/LocalisedText"
   },
   "body": {
    "$ref": "#/components/schemas/LocalisedRichText"
   },
   "isEnabled": {
    "type": "boolean",
    "default": true,
    "description": "BL-005. **Enablement is not publication.** A published page that is disabled exists, keeps its URL and its history, and does not render — which is what a tenant wants when a section is seasonal.\n**Unpublishing loses the version; disabling does not.** Collapsing them means a venue turning off its water-park section for winter has to republish it every spring.\n"
   },
   "status": {
    "allOf": [
     {
      "$ref": "#/components/schemas/ContentStatus"
     }
    ],
    "readOnly": true,
    "description": "Created as `draft`, published by `publishTenantConfig`, archived through `updateContentPage` (`states/content.yaml`)."
   },
   "iconAssetRef": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "categoryCode": {
    "type": "string",
    "nullable": true
   },
   "sortOrder": {
    "type": "integer"
   },
   "isReferenced": {
    "type": "boolean",
    "readOnly": true,
    "x-ticvai-derived": "onWrite",
    "description": "True when navigation or the homepage links to this page. Blocks deletion. Maintained by `setNavigation` and `setHomepageLayout` in the same transaction as the links they write."
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `tenant` scope.**"
   }
  }
 },
 "ContentStatus": {
  "type": "string",
  "enum": [
   "draft",
   "published",
   "archived"
  ]
 },
 "Conversation": {
  "type": "object",
  "x-ticvai-persistence": "marketing.conversation",
  "description": "22.8. **A conversation is not a case.** A case is a ticket measured in hours; a conversation is a live session measured in seconds, with somebody waiting. A conversation may create a case; it is not one.\n",
  "required": [
   "id",
   "channel",
   "state"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "telephony": {
    "type": "object",
    "nullable": true,
    "description": "BL-083. **`ConversationChannel` included `voice` with nothing behind it** — the model anticipated telephony and stopped at the enum.\n**Not an integration, a binding.** Genesys, Avaya, Amazon Connect, Teams and 3CX all do call control themselves; what the platform needs is the call bound to the guest and the case, so **an agent who answers already knows who is calling and what about.**\n",
    "properties": {
     "providerCallId": {
      "type": "string"
     },
     "direction": {
      "type": "string",
      "enum": [
       "inbound",
       "outbound",
       "transferred"
      ]
     },
     "fromNumberMasked": {
      "type": "string",
      "nullable": true,
      "description": "**Masked, and it is still personal data.** A phone number identifies a person more reliably than a name does.\n"
     },
     "recordingRef": {
      "type": "string",
      "nullable": true,
      "description": "Held by the provider, referenced here. **Recording consent is jurisdictional and the platform does not assume it** — a reference with no consent record is a recording nobody may play.\n"
     },
     "agentState": {
      "type": "string",
      "enum": [
       "available",
       "onCall",
       "wrapUp",
       "away",
       "offline"
      ],
      "nullable": true
     }
    }
   },
   "assistSessionId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "BL-094. **`startKioskAssist` recorded a staff member helping a guest and `createCase` recorded a service interaction, and neither referenced the other** — so the traceability 2.13.20 asks for had no link to follow.\n**The link is here rather than on the assist session**, because a case may span several assists and an assist belongs to at most one case.\n"
   },
   "channel": {
    "$ref": "#/components/schemas/ConversationChannel"
   },
   "state": {
    "$ref": "#/components/schemas/ConversationState"
   },
   "subjectId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "22.8.3. Resolved from phone, email, membership number or a signed-in session. **A conversation with none of those stays anonymous rather than being guessed at.**\n"
   },
   "venueId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "assignedPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "queueId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "queuePosition": {
    "type": "integer",
    "nullable": true,
    "readOnly": true,
    "x-ticvai-derived": "onRead",
    "description": "Place among the unclaimed conversations in `queueId`, from the live agent queue (audit R149). Null once claimed."
   },
   "estimatedWaitSeconds": {
    "type": "integer",
    "nullable": true,
    "readOnly": true,
    "x-ticvai-derived": "onRead",
    "description": "From the live agent queue — the conversations ahead divided across that queue's agents online now (audit R149). Null once claimed."
   },
   "handoverReason": {
    "type": "string",
    "nullable": true,
    "enum": [
     "guestRequested",
     "assistantRefused",
     "assistantFailed",
     "outOfScope",
     "negativeSentiment",
     "complexIntent",
     "paymentIssue"
    ]
   },
   "handoverSummary": {
    "type": "string",
    "nullable": true,
    "description": "**The assistant's own account of what the guest wants**, so an agent opens with context rather than reading a transcript while somebody waits.\n"
   },
   "sentiment": {
    "type": "string",
    "nullable": true,
    "enum": [
     "positive",
     "neutral",
     "negative",
     "escalating"
    ],
    "description": "22.8.16. **`escalating` is a routing signal**, not a report line."
   },
   "intent": {
    "type": "string",
    "nullable": true,
    "description": "22.8.13. What the guest appears to want, used for routing."
   },
   "locale": {
    "type": "string"
   },
   "caseId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "22.8.12. Where the conversation raised one."
   },
   "messages": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/ConversationMessage"
    }
   },
   "firstResponseSeconds": {
    "type": "integer",
    "nullable": true,
    "readOnly": true
   },
   "startedAt": {
    "type": "string",
    "format": "date-time"
   },
   "closedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "outcome": {
    "type": "string",
    "nullable": true,
    "enum": [
     "resolved",
     "caseRaised",
     "abandonedByGuest",
     "timedOut",
     "spam"
    ]
   }
  }
 },
 "ConversationChannel": {
  "type": "string",
  "enum": [
   "webChat",
   "inAppChat",
   "whatsapp",
   "sms",
   "email",
   "kiosk",
   "voice"
  ]
 },
 "ConversationMessage": {
  "type": "object",
  "x-ticvai-persistence": "marketing.conversation_message + marketing.conversation_message_attachment",
  "required": [
   "id",
   "sender",
   "body",
   "sentAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "sender": {
    "type": "string",
    "enum": [
     "guest",
     "agent",
     "assistant",
     "system"
    ],
    "description": "**Resolved, never declared.** The assistant is labelled as one — a guest talking to a bot that presents as a person is a complaint waiting for the moment they find out.\n"
   },
   "senderPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "body": {
    "type": "string"
   },
   "attachments": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "assetId": {
       "type": "string",
       "format": "uuid"
      },
      "kind": {
       "type": "string",
       "enum": [
        "image",
        "video",
        "document",
        "ticket",
        "qr",
        "paymentLink"
       ]
      }
     }
    }
   },
   "aiInteractionId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Where the assistant sent it. **Links the message to its tokens and cost**, so a conversation's spend is attributable (CF-14).\n"
   },
   "sentAt": {
    "type": "string",
    "format": "date-time"
   },
   "readAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   }
  }
 },
 "ConversationState": {
  "type": "string",
  "description": "**`withAssistant` and `queued` are different, and the second has a person waiting.** Merging them makes the service level unmeasurable, because time with a bot is not time in a queue.\n",
  "enum": [
   "withAssistant",
   "queued",
   "withAgent",
   "waitingOnGuest",
   "resolved",
   "abandoned",
   "timedOut"
  ]
 },
 "CreateGuestOrderLine": {
  "x-ticvai-persistence": "none — request only",
  "type": "object",
  "required": [
   "id",
   "menuItemId",
   "quantity"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "menuItemId": {
    "type": "string",
    "format": "uuid"
   },
   "quantity": {
    "type": "integer",
    "minimum": 1,
    "maximum": 20
   },
   "modifierOptionIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "note": {
    "type": "string",
    "maxLength": 200,
    "description": "Free text to the kitchen. Allergy notes belong here and are surfaced prominently on the ticket.\n"
   }
  }
 },
 "CreateGuestOrderRequest": {
  "type": "object",
  "required": [
   "id",
   "lines",
   "quotedTotal",
   "recordedAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "locationSessionId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "From `claimLocationSession`. Where the order is going. Required for delivery to a table, seat, cabana or named location. Absent for collection, where the outlet is named instead.\n"
   },
   "outletId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Required for collection. Ignored where a location session is supplied — the session names its outlet."
   },
   "fulfilment": {
    "allOf": [
     {
      "$ref": "#/components/schemas/GuestOrderFulfilment"
     }
    ],
    "nullable": true,
    "description": "Required for takeaway and address delivery; refused with 422 when it breaks the outlet's `FnbDeliveryPolicy`."
   },
   "lines": {
    "type": "array",
    "minItems": 1,
    "items": {
     "$ref": "#/components/schemas/CreateGuestOrderLine"
    }
   },
   "quotedTotal": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "description": "What the guest was shown. Checked against the server's recomputation — a guest is never trusted with a price, and a mismatch is refused rather than silently corrected in either direction.\n"
   },
   "paymentMethod": {
    "type": "string",
    "enum": [
     "card",
     "wallet",
     "roomCharge",
     "addToTab"
    ]
   },
   "recordedAt": {
    "type": "string",
    "format": "date-time"
   }
  }
 },
 "DeliveryLocationKind": {
  "type": "string",
  "description": "4.6.26. One concept, because a runner needs one instruction.",
  "enum": [
   "table",
   "seat",
   "cabana",
   "sunbed",
   "poolside",
   "box",
   "suite",
   "lawn",
   "collectionPoint",
   "namedLocation"
  ]
 },
 "FaqCategory": {
  "x-ticvai-persistence": "whitelabel.faq_category + whitelabel.faq_entry",
  "type": "object",
  "required": [
   "code",
   "name",
   "entries"
  ],
  "properties": {
   "code": {
    "type": "string"
   },
   "name": {
    "$ref": "#/components/schemas/LocalisedText"
   },
   "sortOrder": {
    "type": "integer"
   },
   "entries": {
    "type": "array",
    "items": {
     "type": "object",
     "required": [
      "id",
      "question",
      "answer"
     ],
     "properties": {
      "id": {
       "type": "string",
       "format": "uuid"
      },
      "question": {
       "$ref": "#/components/schemas/LocalisedText"
      },
      "answer": {
       "$ref": "#/components/schemas/LocalisedRichText"
      },
      "sortOrder": {
       "type": "integer"
      },
      "isPublished": {
       "type": "boolean"
      }
     }
    }
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `tenant` scope.**"
   }
  }
 },
 "FnbOrderStatus": {
  "type": "string",
  "description": "The full lifecycle from 4.6.35. Nine states, not six — the earlier enum collapsed `accepted` into `placed` and had no `collected` or `delivered` at all, which made collection and delivery indistinguishable from a server putting a plate down.\n`accepted` matters because an outlet may refuse: past last orders, out of a key ingredient, or simply too far behind. A guest whose order sat in `placed` for ten minutes and was then rejected has a worse experience than one refused immediately.\n",
  "enum": [
   "ordered",
   "accepted",
   "inPreparation",
   "ready",
   "served",
   "collected",
   "delivered",
   "cancelled",
   "refunded"
  ]
 },
 "GuestListing": {
  "type": "string",
  "enum": [
   "bookable",
   "infoOnly",
   "hidden"
  ],
  "default": "bookable",
  "description": "**How a product appears to a guest** (decided 29 September, rev 3 REV3-14). `bookable`: listed and searched while it is on sale, and added to the basket. `infoOnly`: listed and searched with its details, photo and `notBookableLabel` whether or not it is on sale, and **never added to a basket** (`addCartLine` refuses it with `409`); the screen opens its details instead. `hidden`: never listed or searched for a guest, and reachable only where a staff channel sells it. Independent of `isSellable`, which says whether a channel may sell it at all.\n"
 },
 "GuestMenu": {
  "type": "object",
  "x-ticvai-persistence": "none — projection over menu, item and availability",
  "required": [
   "outletId",
   "menuId",
   "name",
   "inForceUntil",
   "sections"
  ],
  "properties": {
   "outletId": {
    "type": "string",
    "format": "uuid"
   },
   "menuId": {
    "type": "string",
    "format": "uuid"
   },
   "name": {
    "type": "string"
   },
   "inForceUntil": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "description": "When this menu stops applying. The client shows it, because a guest browsing breakfast at 10:55 should know.\n"
   },
   "currency": {
    "type": "string",
    "pattern": "^[A-Z]{3}$"
   },
   "currencyScale": {
    "type": "integer"
   },
   "sections": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "name": {
       "type": "string"
      },
      "sortOrder": {
       "type": "integer"
      },
      "items": {
       "type": "array",
       "items": {
        "type": "object",
        "required": [
         "menuItemId",
         "name",
         "price",
         "isAvailable",
         "allergens"
        ],
        "properties": {
         "menuItemId": {
          "type": "string",
          "format": "uuid"
         },
         "name": {
          "type": "string"
         },
         "description": {
          "type": "string",
          "nullable": true
         },
         "price": {
          "$ref": "../shared/common.yaml#/components/schemas/Money"
         },
         "imageAssetRef": {
          "type": "string",
          "nullable": true
         },
         "isAvailable": {
          "type": "boolean",
          "description": "Marked, not removed. A guest who saw a dish yesterday and cannot find it today assumes the app is broken; \"sold out\" is an answer.\n"
         },
         "unavailableReason": {
          "type": "string",
          "nullable": true
         },
         "allergens": {
          "type": "array",
          "description": "Always present. Not a field a tenant may choose to omit.",
          "items": {
           "$ref": "#/components/schemas/AllergenCode"
          }
         },
         "preparationMinutes": {
          "type": "integer",
          "nullable": true
         },
         "modifierGroups": {
          "type": "array",
          "items": {
           "$ref": "#/components/schemas/ModifierGroup"
          }
         }
        }
       }
      }
     }
    }
   }
  }
 },
 "GuestNotification": {
  "type": "object",
  "description": "One in-app message as the guest sees it. A view of `marketing.message_dispatch`, channel `inApp`.",
  "required": [
   "id",
   "title",
   "queuedAt",
   "read"
  ],
  "properties": {
   "id": {
    "type": "string"
   },
   "kind": {
    "type": "string",
    "enum": [
     "queueCall",
     "orderReady",
     "bookingChange",
     "venueAlert",
     "offer",
     "other"
    ]
   },
   "title": {
    "$ref": "#/components/schemas/LocalisedText"
   },
   "body": {
    "$ref": "#/components/schemas/LocalisedText"
   },
   "venueId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "deepLink": {
    "type": "string",
    "nullable": true,
    "description": "Where tapping the notification leads in the app (an order, a queue ticket, a booking)."
   },
   "queuedAt": {
    "type": "string",
    "format": "date-time"
   },
   "read": {
    "type": "boolean"
   }
  }
 },
 "GuestOrderFulfilment": {
  "type": "object",
  "x-ticvai-persistence": "fnb.order_fulfilment",
  "description": "How a guest's order leaves the kitchen: collected, delivered to an address, or taken to a place in the venue.",
  "required": [
   "mode"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "orderId": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "x-ticvai-column": "service_order_id",
    "description": "The guest order this fulfils (`FnbOrder.id`). Set by the server from the order it arrives with."
   },
   "mode": {
    "type": "string",
    "enum": [
     "collection",
     "delivery",
     "inVenue"
    ],
    "description": "`collection` from a counter, `delivery` to an address outside the venue, `inVenue` to a table, seat, cabana or named location (the location session). `GuestOrderResult.fulfilment` reports the same choice."
   },
   "collectionAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "windowStart": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "windowEnd": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "deliveryAddress": {
    "type": "object",
    "nullable": true,
    "properties": {
     "building": {
      "type": "string",
      "maxLength": 200
     },
     "unit": {
      "type": "string",
      "maxLength": 60,
      "nullable": true
     },
     "emirate": {
      "type": "string",
      "maxLength": 60
     },
     "directions": {
      "type": "string",
      "maxLength": 500,
      "nullable": true
     }
    }
   },
   "deliveryFee": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "readOnly": true,
    "nullable": true
   },
   "cutlery": {
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
 "GuestOrderResult": {
  "type": "object",
  "x-ticvai-persistence": "none — projection over fnb_order",
  "required": [
   "orderId",
   "orderNumber",
   "status",
   "total"
  ],
  "properties": {
   "orderId": {
    "type": "string"
   },
   "orderNumber": {
    "type": "string",
    "description": "Short and readable. It gets called out across a counter."
   },
   "fulfilment": {
    "type": "string",
    "enum": [
     "collect",
     "deliverToLocation",
     "tableService",
     "deliverToAddress"
    ],
    "description": "How the order reaches the guest, in the request's terms: `collect` is `GuestOrderFulfilment.mode` `collection`; `deliverToAddress` is `delivery`; `inVenue` is `tableService` where the location session is a table and `deliverToLocation` for a seat, cabana or named location. `KitchenTicket.serviceMode` is the kitchen's view and uses `ServiceMode`."
   },
   "deliveryLabel": {
    "type": "string",
    "nullable": true,
    "description": "Where it is going, as a runner would read it."
   },
   "status": {
    "$ref": "#/components/schemas/FnbOrderStatus"
   },
   "total": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "estimatedReadyAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "collectionPoint": {
    "type": "string",
    "nullable": true
   },
   "tableLabel": {
    "type": "string",
    "nullable": true
   }
  }
 },
 "GuestOrderStatus": {
  "type": "object",
  "x-ticvai-persistence": "none — projection over kitchen_ticket",
  "required": [
   "orderId",
   "status",
   "lines"
  ],
  "properties": {
   "orderId": {
    "type": "string"
   },
   "orderNumber": {
    "type": "string"
   },
   "status": {
    "$ref": "#/components/schemas/FnbOrderStatus"
   },
   "estimatedReadyAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "isReadyForCollection": {
    "type": "boolean"
   },
   "lines": {
    "type": "array",
    "description": "Per-line status. A guest waiting on one dish should see which.",
    "items": {
     "type": "object",
     "properties": {
      "name": {
       "type": "string"
      },
      "quantity": {
       "type": "integer"
      },
      "status": {
       "$ref": "#/components/schemas/KitchenTicketStatus"
      }
     }
    }
   }
  }
 },
 "KitchenTicketStatus": {
  "type": "string",
  "enum": [
   "received",
   "preparing",
   "ready",
   "served",
   "recalled",
   "cancelled"
  ]
 },
 "LocalisedRichText": {
  "x-ticvai-persistence": "none — jsonb column",
  "type": "object",
  "description": "Keyed by language code. Values are sanitised HTML.",
  "additionalProperties": {
   "type": "string"
  }
 },
 "LocalisedText": {
  "x-ticvai-persistence": "none — jsonb column",
  "type": "object",
  "additionalProperties": {
   "type": "string"
  }
 },
 "LocationSession": {
  "type": "object",
  "x-ticvai-persistence": "fnb.location_session",
  "required": [
   "id",
   "locationId",
   "kind",
   "label",
   "expiresAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "locationId": {
    "type": "string",
    "format": "uuid"
   },
   "kind": {
    "$ref": "#/components/schemas/DeliveryLocationKind"
   },
   "label": {
    "type": "string"
   },
   "outletId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The outlet serving this location. Where several serve it, the guest chooses and this is set on the first order.\n"
   },
   "visitId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The table visit this session orders onto, where the location is a table. Absent for a cabana or a seat, which have no visit concept — the order stands alone.\n"
   },
   "joinedExistingVisit": {
    "type": "boolean"
   },
   "subjectId": {
    "type": "string",
    "format": "uuid"
   },
   "expiresAt": {
    "type": "string",
    "format": "date-time",
    "description": "Sessions expire so a guest who leaves cannot order to a lounger now occupied by someone else.\n"
   }
  }
 },
 "MessageChannel": {
  "type": "string",
  "enum": [
   "email",
   "sms",
   "whatsapp",
   "push",
   "inApp",
   "post"
  ]
 },
 "MinimumAppVersion": {
  "x-ticvai-persistence": "none — embedded in tenant_config",
  "type": "object",
  "nullable": true,
  "description": "**The oldest guest app build still allowed to run (decided 28 September, audit R073).** A guest app whose own version is below the one for its platform shows the forced-upgrade screen (GST-047) and nothing else. Null, or a platform left null, forces nothing. Live at once through `setMaintenanceMode`, because an upgrade that must wait for a publish is not forced.\n",
  "properties": {
   "ios": {
    "type": "string",
    "nullable": true,
    "pattern": "^\\d+\\.\\d+\\.\\d+$"
   },
   "android": {
    "type": "string",
    "nullable": true,
    "pattern": "^\\d+\\.\\d+\\.\\d+$"
   }
  }
 },
 "ModifierGroup": {
  "x-ticvai-persistence": "fnb.modifier_group + fnb.modifier_option",
  "type": "object",
  "description": "**An F&B modifier is a choice added to a dish at the moment of ordering** — *no onions*, *extra cheese*, *cooked medium*. **It is not an Attribute**, the axis that generates catalogue variants (naming-and-style §3 lists *Modifier* as a banned synonym for that), and the two must not be merged: a variant is a different product with its own stock, a modifier is an instruction on a line with at most a price delta.\n",
  "required": [
   "id",
   "code",
   "name",
   "minSelections",
   "maxSelections",
   "options"
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
   "minSelections": {
    "type": "integer",
    "minimum": 0,
    "description": "Greater than zero makes the group required."
   },
   "maxSelections": {
    "type": "integer",
    "minimum": 1
   },
   "options": {
    "type": "array",
    "minItems": 1,
    "items": {
     "type": "object",
     "required": [
      "id",
      "name",
      "priceDelta"
     ],
     "properties": {
      "id": {
       "type": "string",
       "format": "uuid"
      },
      "name": {
       "type": "string"
      },
      "priceDelta": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      },
      "isDefault": {
       "type": "boolean"
      },
      "isAvailable": {
       "type": "boolean"
      },
      "allergens": {
       "type": "array",
       "description": "What choosing this option adds to the dish. `attachModifierGroup` refuses a group that adds one the item does not declare, and `verifyAllergens` reports it as `via` `modifier`.",
       "items": {
        "$ref": "#/components/schemas/AllergenCode"
       }
      }
     }
    }
   },
   "scopePath": {
    "type": "string",
    "description": "**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `venue` scope.**"
   }
  }
 },
 "ModuleKey": {
  "$ref": "../shared/common.yaml#/components/schemas/ModuleKey"
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
 "OrderChannel": {
  "type": "string",
  "description": "Where the order originated. Added when guest self-ordering was contracted — an order a guest placed on their own phone is commercially and operationally different from one a cashier typed, and reporting that cannot separate them cannot answer whether self-ordering is working.\n",
  "enum": [
   "pos",
   "kiosk",
   "guestApp",
   "guestWeb",
   "callCentre",
   "partner",
   "api",
   "backOffice"
  ]
 },
 "OrderLine": {
  "x-ticvai-persistence": "orders.order_line + orders.order_line_eligibility + orders.order_line_discount",
  "x-ticvai-retired-columns": [
   "promotion_id",
   "name",
   "reason"
  ],
  "allOf": [
   {
    "$ref": "#/components/schemas/CreateOrderLine"
   },
   {
    "type": "object",
    "required": [
     "serverUnitPrice",
     "taxAmount",
     "netAmount",
     "grossAmount"
    ],
    "properties": {
     "serverUnitPrice": {
      "allOf": [
       {
        "$ref": "../shared/common.yaml#/components/schemas/Money"
       }
      ],
      "description": "What the server computed on ingest."
     },
     "priceVariance": {
      "allOf": [
       {
        "$ref": "../shared/common.yaml#/components/schemas/Money"
       }
      ],
      "description": "Server minus quoted. Non-zero means the quoted price was honoured and the difference posted to the variance account.\n"
     },
     "taxAmount": {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     },
     "netAmount": {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     },
     "grossAmount": {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     },
     "entitlementIds": {
      "type": "array",
      "description": "The entitlements this line issued. **These are the ticket ids** — `transferOrderTickets.ticketIds` and `reprintOrder.reissuedTicketIds` take and return them.",
      "items": {
       "type": "string",
       "format": "uuid"
      }
     },
     "crossRegionRightIds": {
      "type": "array",
      "items": {
       "type": "string"
      },
      "description": "Redemption rights propagated to other cells for this line."
     },
     "reprintCount": {
      "type": "integer",
      "minimum": 0,
      "default": 0,
      "readOnly": true,
      "description": "How many times this line's tickets were reprinted or resent. `reprintOrder` increments it; repeated reprints are the signal worth surfacing."
     },
     "venueId": {
      "type": "string",
      "format": "uuid",
      "readOnly": true,
      "description": "The order's venue, copied onto the line (ADR-0044's own example; system-design review SD-008, 29 September) so a line is scoped and partitionable without its order."
     },
     "discounts": {
      "type": "array",
      "readOnly": true,
      "description": "**The discounts applied to this line, one row each** (system-design review SD-008, 29 September). Until then a discount object was flattened into the line as `promotion_id NOT NULL`, so a line with no promotion could not be inserted. A line with no discount has none.",
      "items": {
       "$ref": "#/components/schemas/OrderLineDiscount"
      }
     }
    }
   }
  ]
 },
 "OrderLineAttributes": {
  "type": "object",
  "nullable": true,
  "additionalProperties": true,
  "x-ticvai-persistence": "none — embedded as attributes (jsonb) on orders.cart_line and orders.order_line",
  "description": "Open attributes of a line, kept from the cart to the order line. **`transport` is the one with a defined shape** (decided 29 September, rev 3 REV3-21); other keys are free.\n",
  "properties": {
   "transport": {
    "$ref": "#/components/schemas/TransportLineAttributes"
   }
  }
 },
 "OrderStatus": {
  "type": "string",
  "enum": [
   "pending",
   "held",
   "paid",
   "partiallyPaid",
   "completed",
   "voided",
   "refunded",
   "partiallyRefunded",
   "failed"
  ],
  "description": "`held` is a parked sale — the cashier freed the till and the guest will return. It holds no inventory and expires, because a till that accumulates parked sales across a shift cannot be closed.\n"
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
 "Product": {
  "x-ticvai-persistence": "catalogue.product",
  "type": "object",
  "required": [
   "id",
   "code",
   "name",
   "kind",
   "venueId",
   "scopePath",
   "isSellable",
   "hasVariants"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "code": {
    "type": "string",
    "maxLength": 64
   },
   "familyKey": {
    "type": "string",
    "maxLength": 64,
    "pattern": "^[A-Za-z0-9_-]+$",
    "nullable": true,
    "x-ticvai-unique": "venue",
    "description": "**The same product at another location** (decided 29 September, rev 3 REV3-18). Optional. A tenant that sells one attraction at several venues gives each venue's product the same key, e.g. `aquarium-entry`; the key names the family across the tenant and each venue has at most one product in it, so a second product at the same venue with the key is refused with `409 duplicate-code`. **What it is for:** when a guest changes location on the booking screen (the 'Booking at' switcher, `BookingFlowConfig.locationSwitcher`), lines whose product shares a `familyKey` with a product at the new venue are carried over to that product, with times and prices refreshed; every other line is cleared. Null means the product belongs to no family and its lines always clear on a switch. Compared case-insensitively, like `code`.\n"
   },
   "name": {
    "type": "string",
    "maxLength": 200
   },
   "description": {
    "type": "string"
   },
   "kind": {
    "$ref": "#/components/schemas/ProductKind"
   },
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "scopePath": {
    "type": "string"
   },
   "createdByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "description": "1.4.18. **The approval gate refuses an approver who is the author, and nothing recorded either.** `SeatBlock`, `DelegatedAccess` and `ManualDiscountRequest` all carry this and the product passing through approval did not.\n"
   },
   "approvedByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true
   },
   "responsibleDepartmentId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Who owns this product commercially. A scope node at `department` level."
   },
   "onSaleFrom": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "description": "1.4.8. **A seasonal product should not need somebody awake at midnight.** Archiving already runs on a timer in this contract, so the machinery exists; `effectiveFrom` appears on tax codes, FX rates and white-label policies and not here.\n"
   },
   "onSaleTo": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "description": "Retires the product automatically. **Retirement is not deletion** — the product stops selling and every order that referenced it still resolves.\n"
   },
   "categoryId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "**Taken from their `fnb.product` and `retail.product`, 20 September.** `catalogue.product_category` has existed since 20 August with two operations and nothing could be filed under it — a merchandise hierarchy with a tree and no leaves. Their per-domain product tables both carried this column and ours did not.\n"
   },
   "lifecycleState": {
    "$ref": "#/components/schemas/ProductLifecycleState"
   },
   "isSellable": {
    "type": "boolean",
    "readOnly": true,
    "description": "True only when live **and** carried by a published bundle. Approval and publication are different acts.\n**Derived, never set.** It changes when `transitionProductLifecycle` moves the product and when `publishBundle` carries it, so `updateProduct` does not take it — `withdraw` is how a product stops selling.\n"
   },
   "isStockTracked": {
    "type": "boolean",
    "default": false,
    "description": "**Taken from their `fnb.product`, 20 September.** Whether a sale decrements stock, which is not what `isSellable` asks. A ticket is sellable and tracks no stock; a bottle of water is both. Without it, an F&B sale cannot tell inventory whether to move.\n"
   },
   "hasVariants": {
    "type": "boolean"
   },
   "variantCount": {
    "type": "integer"
   },
   "segmentTags": {
    "type": "array",
    "description": "7.3.5. **A channel and a segment tag are mandatory and nothing required either.** A catalogue that cannot be filtered by segment is a catalogue nobody can report on.\n**Hierarchical, not flat** — `family/with-toddlers` narrows `family` without duplicating it, which is how the promotions engine already treats scope.\n**A level is a tag under `level/`** (decided 29 September, rev 3 REV3-19): `level/beginner`, `level/intermediate`, `level/advanced`, `level/expert` (proposed codes, client to correct). A guest screen filters on it with `listProducts` `segmentTag`, and the words a guest reads beside each option come from `ProductCategory.description`, not from the tag.\n",
    "items": {
     "type": "string"
    }
   },
   "codeSchema": {
    "type": "string",
    "readOnly": true,
    "description": "7.3.4 specifies `[ParkCode]-[ProductType]-[Variant]`. **`Product.code` existed and nothing required a format**, so a venue with three thousand products had three thousand conventions.\nThe tenant sets the pattern and the platform generates against it. **Validation is the point, not the string** — a code typed by hand is a code that will not sort.\n"
   },
   "channels": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/Channel"
    }
   },
   "entitlementTemplateId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "What the buyer receives. Null for products that grant nothing — F&B and retail. Identity and entitlement are separate concerns.\n"
   },
   "blockedOffline": {
    "type": "boolean",
    "description": "True for seated and retail. Seated because a seat map is not a count; retail because stock depletes in real time.\n"
   },
   "dataMaskValues": {
    "type": "object",
    "additionalProperties": true,
    "description": "Custom fields. JSONB-backed, defined by the venue's data mask."
   },
   "guestListing": {
    "$ref": "#/components/schemas/GuestListing"
   },
   "notBookableLabel": {
    "allOf": [
     {
      "$ref": "#/components/schemas/LocalisedText"
     }
    ],
    "nullable": true,
    "description": "The label a guest reads on an `infoOnly` product, e.g. *Info only* or *Not bookable online; ask at the desk* (decided 29 September, rev 3 REV3-14). Each value at most 60 characters. Null means the guest screen shows its default wording. Ignored unless `guestListing` is `infoOnly`.\n"
   },
   "salesContact": {
    "allOf": [
     {
      "$ref": "#/components/schemas/ProductSalesContact"
     }
    ],
    "nullable": true,
    "description": "**Who a guest contacts to book a view-only product** (decided 29 September, W3), e.g. a training course listed with full details and no Book button. Shown as *Call sales* and *Email sales* on an `infoOnly` product. Null means the venue's own contact (white-label `getTenantAppStatus.contact`). Ignored unless `guestListing` is `infoOnly`.\n"
   },
   "bookingFlowId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "**The booking flow this product is sold through** (decided 29 September, W8 and W12): a white-label `BookingFlow` of the venue, which orders the guest's steps (for a workshop, the product first and then the date and time). Null means the category's flow (`ProductCategory.bookingFlowId`), and failing that the venue's flow for the product's `kind`. Written by `createProduct` and `updateProduct`, which refuse an id that is not a flow of the venue with `422`.\n"
   },
   "displayTags": {
    "type": "array",
    "maxItems": 6,
    "items": {
     "$ref": "#/components/schemas/ProductDisplayTag"
    },
    "description": "**Short facts a guest reads on the ticket card and under *Read more***: *2 Hours*, *Min 1.10 m*, *Free adult entry*, *Valid 90 days*, *Emirates ID* (decided 29 September, 23SEP-3). Not `segmentTags`, which are for reporting and segmentation and which a guest never reads.\n**Derived on read when none are set.** When the venue has written no tags, a read returns tags derived from the product's duration (`clock`), entitlement validity (`calendar`) and the eligibility rule's `minHeightCm` (`height`), each marked `derived: true`; they are never stored. Once the venue writes any tag, only what it wrote is returned. Whether the guest screen shows them is `BookingFlowConfig.ticketTags` (white-label).\n"
   },
   "media": {
    "type": "array",
    "maxItems": 20,
    "items": {
     "$ref": "#/components/schemas/ProductMedia"
    },
    "description": "**The product's own photos and video** (decided 29 September, 23SEP-4). *Read more* opens on the `isPrimary` item, and a listing shows each product's primary image, so two tickets in one category no longer share the category's picture (`ProductCategory.imageAssetId`).\nEvery `assetId` names an asset of the asset library (`assets.yaml` `MediaAsset`) in status `ready` whose kind matches `kind`; anything else is a `422`. **Exactly one item is `isPrimary`** when the list is not empty, and an `assetId` appears once; otherwise `400`. Setting the list records each reference as asset usage (`MediaUsage` with `surface: product`, `referenceId` the product id, `isLive` true while the product is listed to guests), which is what stops a used asset being archived from under the product.\n"
   },
   "consentQuestionIds": {
    "type": "array",
    "maxItems": 10,
    "uniqueItems": true,
    "items": {
     "type": "string",
     "format": "uuid"
    },
    "description": "**The consent questions a guest answers when booking this product**, in the order they are asked (decided 29 September, rev 3 REV3-26): *Are you able to swim?*, *Do you hold a scuba certification?*, *I accept the risk*. Each id names a consent question defined in marketing-crm (`ConsentQuestion`), which owns the text, its version and whether it is asked per person or once per booking; the answer is stored there as a consent record (question version, answer, who answered, when). **One question or several, as the venue chooses.** A flow can carry its own list too (`white-label.BookingFlow.settings.consentQuestionIds`, on the product's published booking flow as `getPublishedBookingFlow` resolves it: product, then category, then the venue's flow for the kind; moved from `BookingFlowConfig` 29 September, W12); a booking asks the union of the flow's questions and those of every product in the cart, each question once (`orders.Cart.consentQuestions`). An id that names no active consent question of the tenant is a `422`.\n"
   },
   "requiresTimeWindow": {
    "type": "boolean",
    "default": false,
    "description": "**True for a space sold by the hour**, e.g. a meeting room type (decided 29 September, rev 3 REV3-13). The product is the room type (*focus pod*, *majlis*, *boardroom*, *auditorium*), never a named room; its lengths are a `length` axis (`setProductAttributes`) whose values carry `durationMinutes`, and each length is a variant priced on its own in the price list, so price is the room rate for that length. The cart line carries the booked start and end (orders), the end being the start plus the chosen variant's `durationMinutes`; `resources.listProductStartTimes` supplies the start times for a variant and a date and `allocateResources` picks the room from the product's resource requirements (`setExperienceResourceRequirements`) at checkout. True requires every active variant to have a `durationMinutes`; otherwise `422`.\n"
   },
   "productOwnerPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The product owner (29 September, data model DM3), set with `setProductContextOwnership`. `responsibleDepartmentId` is the owning department."
   },
   "operationalContact": {
    "type": "string",
    "maxLength": 200,
    "nullable": true,
    "description": "A principal id or a name, as the context screen takes it."
   },
   "businessUnitId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "legalEntityId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "A `ledger.legal_entity`, read through finance."
   },
   "attractionId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "siteId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "locationId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "brandId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The brand, as the context screen names it (a catalogue brand category)."
   },
   "marketCode": {
    "type": "string",
    "maxLength": 40,
    "nullable": true
   },
   "salesTerritory": {
    "type": "string",
    "maxLength": 100,
    "nullable": true
   }
  }
 },
 "ProductDisplayTag": {
  "x-ticvai-persistence": "none — jsonb column on catalogue.product",
  "type": "object",
  "required": [
   "kind",
   "label"
  ],
  "description": "One short fact on a ticket card (decided 29 September, 23SEP-3). `kind` picks the icon.",
  "properties": {
   "kind": {
    "type": "string",
    "enum": [
     "clock",
     "height",
     "free",
     "calendar",
     "id"
    ],
    "description": "`clock` a duration, `height` a height rule, `free` something included free, `calendar` a validity, `id` a document the guest must bring."
   },
   "label": {
    "allOf": [
     {
      "$ref": "#/components/schemas/LocalisedText"
     }
    ],
    "description": "What the guest reads, e.g. *2 Hours*. Each language value at most 40 characters."
   },
   "derived": {
    "type": "boolean",
    "readOnly": true,
    "default": false,
    "description": "True on a tag the server derived on read because the venue set none. Never sent."
   }
  }
 },
 "ProductKind": {
  "type": "string",
  "description": "**`openDated` added 24 August** from the client's *Create Ticket Flow* board, which names six main ticket types and this was the one with no kind: **valid on any date within an eligible range, rather than for a named performance or a fixed date.**\nThe mechanism already existed — `access.entitlement` carries `valid_from`, `valid_to`, `entries_allowed` and `frozen_days`, which is exactly an open-dated pass. **What was missing was the product saying it is one**, so a catalogue could not offer it and a report could not count it.\n**`datedAdmission` is a different thing and the two were being conflated**: dated is *this Tuesday*, open-dated is *any Tuesday between March and June*. A guest buying the second and being sold the first has bought the wrong ticket.\n**Transport uses two existing kinds, not a new one** (decided 29 September, rev 3 REV3-21). A one-way trip is `timedAdmission`: `transport.createTransportRoute` creates the route's product with one variant per passenger type, and each departure is a performance. A multi-trip or unlimited pass is `openDated`: `transport.createTransportPassType` creates it, with `EntitlementTemplate.entriesAllowed` = the pass's trips (null for unlimited), the validity = `validityDays`, and `EntitlementTemplate.transportRestriction` naming the station pair the pass was bought for, so `access` refuses it on another journey. The sale path is unchanged: both are cart lines, priced by `transport.quoteTransportFare` (orders `TransportLineAttributes`).\n",
  "enum": [
   "admission",
   "timedAdmission",
   "datedAdmission",
   "openDated",
   "seated",
   "membership",
   "bundle",
   "fnb",
   "retail",
   "rental",
   "addOn",
   "giftCard"
  ]
 },
 "ProductLifecycleState": {
  "type": "string",
  "enum": [
   "draft",
   "inReview",
   "approved",
   "live",
   "withdrawn",
   "archived"
  ]
 },
 "ProductMedia": {
  "x-ticvai-persistence": "catalogue.product_media",
  "type": "object",
  "required": [
   "assetId",
   "kind",
   "isPrimary"
  ],
  "description": "One photo or video of a product, referencing the asset library (decided 29 September, 23SEP-4). One row per product and asset, so the asset library can answer which products use an asset.\n",
  "properties": {
   "assetId": {
    "type": "string",
    "format": "uuid",
    "description": "A `MediaAsset` of `assets.yaml`, in status `ready`."
   },
   "kind": {
    "type": "string",
    "enum": [
     "image",
     "video"
    ]
   },
   "isPrimary": {
    "type": "boolean",
    "default": false,
    "description": "The item *Read more* opens on and a listing shows. Exactly one per product."
   },
   "displayOrder": {
    "type": "integer",
    "default": 100
   },
   "altText": {
    "allOf": [
     {
      "$ref": "#/components/schemas/LocalisedText"
     }
    ],
    "nullable": true
   }
  }
 },
 "ProductSalesContact": {
  "x-ticvai-persistence": "none — jsonb column on catalogue.product",
  "type": "object",
  "description": "Who to contact to book a view-only product (decided 29 September, W3). At least one of `phone` or `email`.\n",
  "minProperties": 1,
  "properties": {
   "phone": {
    "type": "string",
    "maxLength": 32,
    "nullable": true
   },
   "email": {
    "type": "string",
    "format": "email",
    "maxLength": 254,
    "nullable": true
   },
   "note": {
    "allOf": [
     {
      "$ref": "#/components/schemas/LocalisedText"
     }
    ],
    "nullable": true,
    "description": "A line shown under the contact, e.g. *Group courses are booked by phone*. At most 200 characters per language."
   }
  }
 },
 "ProposedAction": {
  "type": "object",
  "x-ticvai-persistence": "ai.proposed_action",
  "required": [
   "id",
   "kind",
   "targetContract",
   "targetOperation",
   "payload",
   "status"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "interactionId": {
    "type": "string",
    "format": "uuid"
   },
   "kind": {
    "type": "string",
    "enum": [
     "pricing",
     "promotion",
     "operational",
     "financial",
     "configuration",
     "content",
     "audience"
    ],
    "description": "`content` (a marketing or storefront draft from `proposeMarketingContent`) and `audience` (a lookalike segment from `proposeLookalikeSegment`) added 29 September (build); both are applied by a person in the owning screen."
   },
   "targetContract": {
    "type": "string",
    "description": "Which contract would perform it. The assistant never performs it itself."
   },
   "targetOperation": {
    "type": "string"
   },
   "payload": {
    "type": "object",
    "additionalProperties": true,
    "description": "The request body a person would submit, ready to review. **Open on purpose: its shape is the request body of `targetOperation` in `targetContract`**, and it is validated against that operation, not restated here.\n"
   },
   "summary": {
    "type": "string"
   },
   "status": {
    "type": "string",
    "description": "**Expiry (decided 28 September, audit R213)**: a `proposed` action expires 7 days after `proposedAt`; an `approved` action not applied expires 24 hours after `decidedAt`. Both are proposed values, client to correct, and `expiresAt` carries the one that applies.\n",
    "enum": [
     "proposed",
     "approved",
     "rejected",
     "applied",
     "expired"
    ]
   },
   "expiresAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true,
    "x-ticvai-derived": "onWrite",
    "description": "When the expiry timer moves this action to `expired` — `proposedAt` plus 7 days while `proposed`, `decidedAt` plus 24 hours once `approved`, null once `rejected`, `applied` or `expired` (audit R213)."
   },
   "approvalLevel": {
    "type": "integer",
    "minimum": 1,
    "maximum": 2,
    "description": "8.3.65. Multi-level, because a discount and a pricing change differ in authority. **Two levels (decided 28 September, audit R213)**: `2` for anything touching prices or permissions (every `pricing` and `promotion` action, and any other whose payload sets a price, a discount, a role or a permission grant), which needs a manager other than the requester; `1` for everything else, which the requester approves themselves.\n"
   },
   "decidedByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "decisionReason": {
    "type": "string",
    "nullable": true,
    "description": "Required on rejection. **The only signal the assistant is proposing badly**, and without it a poor model degrades silently.\n"
   },
   "proposedAt": {
    "type": "string",
    "format": "date-time"
   },
   "decidedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "**Added 29 September (AI design 3.1):** `ai.proposed_action` had no policy — its only references were nullable. The scope it was proposed at, and the partition key row-level security reads.\n"
   },
   "planId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true,
    "x-ticvai-references": "ai.action_plan",
    "description": "The plan this action presents for a decision (AI design 2.2 D, 3.8)."
   },
   "approvalRequestId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true,
    "description": "The `approvals` request deciding a tier 2 or matrix-caught action (AI design 2.3)."
   },
   "changeSetHash": {
    "type": "string",
    "nullable": true,
    "readOnly": true,
    "description": "Hash of the change set approved; execution refuses a plan whose hash differs (AIC-181)."
   }
  }
 },
 "QueueStatus": {
  "type": "string",
  "enum": [
   "open",
   "paused",
   "closed",
   "atCapacity"
  ]
 },
 "Review": {
  "x-ticvai-persistence": "marketing.review",
  "allOf": [
   {
    "$ref": "#/components/schemas/SubmitReviewRequest"
   },
   {
    "type": "object",
    "required": [
     "status"
    ],
    "properties": {
     "status": {
      "type": "string",
      "enum": [
       "pendingModeration",
       "published",
       "hidden",
       "rejected"
      ]
     },
     "response": {
      "type": "string",
      "nullable": true
     },
     "responseIsPublic": {
      "type": "boolean"
     },
     "respondedByPrincipalId": {
      "type": "string",
      "format": "uuid",
      "nullable": true
     },
     "openedCaseId": {
      "type": "string",
      "nullable": true,
      "description": "Case raised automatically where the rating fell below the venue's threshold. Feedback that goes nowhere is worse than no feedback mechanism.\n"
     }
    }
   }
  ]
 },
 "SubmitReviewRequest": {
  "x-ticvai-persistence": "none — request only",
  "type": "object",
  "required": [
   "id",
   "rating",
   "venueId",
   "recordedAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "subjectId": {
    "type": "string",
    "format": "uuid"
   },
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "relatedOrderId": {
    "type": "string"
   },
   "rating": {
    "type": "integer",
    "minimum": 1,
    "maximum": 5
   },
   "body": {
    "type": "string",
    "maxLength": 5000
   },
   "aspects": {
    "type": "array",
    "description": "Aspect chips — the closed set the description always named.",
    "uniqueItems": true,
    "items": {
     "type": "string",
     "enum": [
      "exhibitions",
      "staff",
      "cleanliness",
      "food",
      "value"
     ]
    }
   },
   "recordedAt": {
    "type": "string",
    "format": "date-time"
   }
  }
 },
 "Suggestion": {
  "type": "object",
  "x-ticvai-persistence": "ai.suggestion",
  "description": "One answer to one question, with its reasoning and its confidence. **Built 24 August so that machine learning can be swapped in without touching a screen.**\n**A suggestion is never an action.** It proposes; `ProposedAction` and its approval path decide. A model that can order stock is a model that will order stock wrongly at three in the morning.\n**`inputs` is recorded, not just referenced.** A suggestion that cannot be reproduced cannot be defended to a finance controller asking why the system said to order four hundred.\n",
  "required": [
   "id",
   "kind",
   "basis",
   "maturity",
   "producedAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "kind": {
    "$ref": "#/components/schemas/SuggestionKind"
   },
   "basis": {
    "$ref": "#/components/schemas/SuggestionBasis"
   },
   "scopePath": {
    "type": "string"
   },
   "subjectRef": {
    "type": "string",
    "nullable": true,
    "description": "What it is about — a product, an outlet, an item, a party."
   },
   "value": {
    "type": "object",
    "additionalProperties": true,
    "description": "The suggestion itself. Shape depends on `kind`."
   },
   "confidence": {
    "type": "number",
    "nullable": true,
    "minimum": 0,
    "maximum": 1,
    "description": "**Null for a heuristic and that is honest.** A rule has no confidence — dressing one up with 0.85 is the fastest way to make a manager trust a number that means nothing.\n"
   },
   "explanation": {
    "type": "string",
    "description": "**Plain words, always present, whatever the basis.** *Because covers are up 12% on this day last year* — a suggestion a manager cannot explain to their own boss is a suggestion they will not action.\n"
   },
   "inputs": {
    "type": "object",
    "additionalProperties": true,
    "description": "What went in. **Recorded so the answer can be reproduced** — and so that when a model replaces the rule, the two can be run against the same inputs and compared.\n"
   },
   "producerRef": {
    "type": "string",
    "description": "The rule name or the model id and version. **A model version is part of the record**: *the model said so* is not an answer to *which model, when*.\n"
   },
   "maturity": {
    "$ref": "#/components/schemas/AiMaturity"
   },
   "producedAt": {
    "type": "string",
    "format": "date-time"
   },
   "expiresAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "description": "**A demand forecast for Saturday is worthless on Sunday.** An expired suggestion is hidden rather than shown stale.\n"
   }
  }
 },
 "SuggestionBasis": {
  "type": "string",
  "description": "**How the answer was reached, and this is the field the whole design exists for.**\nA venue must be able to see that today's price suggestion is a margin rule and next quarter's is a trained model — **the same operation, the same screen, a different basis** — and a screen that cannot say which is a screen that asks a manager to trust arithmetic it will not show.\n**Swapping a heuristic for a model is a provider change, not a contract change.** That is the point of the abstraction: the frontend, the audit record and the outcome capture all stay exactly as they are.\n",
  "enum": [
   "heuristic",
   "statistical",
   "model",
   "hybrid",
   "manual"
  ]
 },
 "SuggestionKind": {
  "type": "string",
  "description": "What is being suggested. **A closed set, and the reason it is closed is the swap.** Every entry here is a question a venue asks that a model could answer better than a rule — and each one starts as a heuristic and becomes a model when there is data.\n**Six of these were drawn as their own endpoints on the client F&B boards** — `suggestPrice`, `simulateScenario`, `simulateSlaPolicy`, `suggestRequisition`, `suggestReplenishment`, `publishDemandPlan`. **Building six endpoints means six places to change when a model changes**, and the model will change more often than the venue's question does.\n**What each kind is based on, and when the venue's own data takes over. Proposed, client to correct (decided 28 September, audit R213; re-read 29 September, AI functions review).** The figure after each rule is **the point where own data takes over from the baseline, not a refusal**: below it the kind answers from the baseline (venue AI settings, the starting pattern for the venue type, the UAE calendar, the weather) with `maturity.stage` `starting`, and between it and about three months it blends the two (`learning`). The day-one baseline per kind: `replenishment`, `requisition`, `prepPlan`, `staffing`, `demandForecast` and `scenario` from the baseline forecast (typical attendance from the venue AI settings x the venue-type month curve x the calendar x weather, bookings on hand as a floor); `menuEngineering` ranked by margin with popularity marked learning; `slaTarget` a standard default; `waitTime` people ahead / configured capacity; `upsell` the relationship map and business priority; `segmentation` known guest attributes; `anomaly` the venue's configured thresholds and actual against the forecast's low end; `sendTime` the channel's typical hour; `wasteRisk` shelf life and par against the forecast; `queueBalancing` configured capacity per queue. Only a missing setting refuses (422 `AiMissingSettingProblem`).\n- `price`: unit cost plus the category's target margin, held inside the price band. Minimum: a current cost, no history.\n- `replenishment`: par level minus on-hand plus expected use over the supplier lead time. Minimum: 14 days of stock movements.\n- `requisition`: the next service's prep-plan ingredient needs minus kitchen stock. Minimum: 14 days of sales.\n- `demandForecast`: the average of the same weekday over the last 8 weeks, adjusted by admissions already booked. Minimum: 8 weeks of sales.\n- `prepPlan`: forecast covers for the service times each item's share of the last 4 same weekdays. Minimum: 4 weeks of sales.\n- `menuEngineering`: each item placed by popularity against margin, over 90 days. Minimum: 90 days of sales.\n- `staffing`: forecast demand divided by the role's standard covers per staff hour. Minimum: 8 weeks of sales (the forecast it rests on).\n- `slaTarget`: the 80th percentile of actual times over the last 30 days. Minimum: 30 days of timed events.\n- `waitTime`: people ahead divided by the throughput of the last 30 minutes. Minimum: 30 minutes of throughput today.\n- `upsell`: the item most often bought with the basket's items over 90 days. Minimum: 90 days of orders.\n- `segmentation`: recency, frequency and spend scores over 12 months. Minimum: 90 days of orders.\n- `anomaly`: a value outside three standard deviations of the same weekday over 8 weeks. Minimum: 8 weeks of the measure.\n- `scenario`: the demand forecast re-run with the stated changes. Minimum: as `demandForecast`.\n- `sendTime` (added 29 September): per recipient, the hour inside `context.sendWindow` in which they have most often opened or clicked over the last 90 days (marketing-crm attribution touches), and where `context.channel` is `best`, the consented channel with the highest engagement. A recipient with fewer than three touches gets their segment's modal hour, and one with none the window's start. Asked with `subjectRef` a segment id or `context.subjectIds` (at most 10,000). `value` is `{recommendations: [{subjectId, sendAt, channel, basisTouches}]}`. Minimum: 90 days of message touches at the scope.\n- `wasteRisk` (added 29 September): per item at an outlet or store location, planned production and stock on hand minus forecast demand over the item's shelf life, plus batches expiring inside the horizon (`inventory.listExpiringBatches`). `value` is `{items: [{itemRef, quantityAtRisk, valueAtCost, expiresAt, recommendedAction (reducePrep, promote, transfer, useInRecipe), transferTo}]}`. Minimum: 14 days of recorded waste and of sales.\n- `queueBalancing` (added 29 September): per queue or attraction at `subjectRef` (a venue) over `horizon`, the forecast wait (the `queue` forecast definition) against throughput capacity, a recommended virtual-queue return-slot allocation by queue type, and guest redirection from over-used to under-used attractions. `value` is `{queues: [{queueId, forecastWaitMinutes, capacityPerHour, returnSlotsPerInterval, redirectTo}]}`. Minimum: 14 days of queue readings.\n- `itinerary` (added 29 September, MOB-6, guest-allowed): refines a `venue-map` visit plan the guest owns. `subjectRef` is the plan id; `value` is `{planId, baseVersion, changes, rationale}`, applied with `updateVisitPlan` as the guest. Minimum: none; the rules plan is the baseline. Every change names a point or performance of that day's venue only, rides, dining and retail alike (30 September client meeting, MoM 4.7).\n",
  "enum": [
   "price",
   "replenishment",
   "requisition",
   "demandForecast",
   "prepPlan",
   "menuEngineering",
   "staffing",
   "slaTarget",
   "waitTime",
   "upsell",
   "segmentation",
   "anomaly",
   "scenario",
   "sendTime",
   "wasteRisk",
   "queueBalancing",
   "itinerary"
  ]
 },
 "TenantAppStatus": {
  "x-ticvai-persistence": "none — computed",
  "type": "object",
  "description": "Computed on read. The published fields come from the current `ConfigVersion`, the maintenance fields from the tenant's `tenant_config` row (`setMaintenanceMode`), and the draft fields from the working draft. **Fields marked staff only are left out of a response to a caller without a staff session** (`getTenantAppStatus`).\n",
  "required": [
   "tenantId",
   "isPublished",
   "isInMaintenance"
  ],
  "properties": {
   "tenantId": {
    "type": "string",
    "format": "uuid"
   },
   "isPublished": {
    "type": "boolean",
    "x-ticvai-derived": "onRead",
    "description": "True once any version has been published."
   },
   "publishedVersion": {
    "type": "string",
    "nullable": true
   },
   "publishedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "draftVersion": {
    "type": "string",
    "description": "Staff only."
   },
   "hasUnpublishedChanges": {
    "type": "boolean",
    "x-ticvai-derived": "onRead",
    "description": "Staff only. The working draft differs from the current version's `snapshot`."
   },
   "activeModuleCount": {
    "type": "integer",
    "x-ticvai-derived": "onRead",
    "description": "Staff only. `ModuleEnablement` rows with `isEnabled` true."
   },
   "licensedModuleCount": {
    "type": "integer",
    "x-ticvai-derived": "onRead",
    "description": "Staff only. `ModuleEnablement` rows with `isLicensed` true."
   },
   "activePageCount": {
    "type": "integer",
    "x-ticvai-derived": "onRead",
    "description": "Staff only. Content pages that are `published` and enabled."
   },
   "isInMaintenance": {
    "type": "boolean"
   },
   "maintenanceMessage": {
    "$ref": "#/components/schemas/LocalisedText"
   },
   "expectedBackAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "minimumAppVersion": {
    "$ref": "#/components/schemas/MinimumAppVersion"
   },
   "contact": {
    "$ref": "#/components/schemas/VenueContact"
   },
   "availability": {
    "$ref": "#/components/schemas/AppAvailability"
   },
   "availabilityMessage": {
    "allOf": [
     {
      "$ref": "#/components/schemas/LocalisedText"
     }
    ],
    "nullable": true,
    "description": "What the sold-out or closed screen says (WEB-029). Null shows the default wording."
   },
   "venues": {
    "type": "array",
    "maxItems": 200,
    "x-ticvai-derived": "onRead",
    "description": "**Public: the venues a guest can pick** (decided 28 September, audit R267; schema named 29 September, readiness close-out, our build plan). The source of the venue picker on WEB-001 and GST-001, returned with or without a session. **Published only**: a venue is listed when its scope node is active (`tenancy.OrgUnit.isActive`) and it is in the tenant's current published `ConfigVersion`; a venue added or reactivated since the last publish appears after the next publish, and a draft never reaches a guest. Ordered by `name`. Empty when nothing is published.\n",
    "items": {
     "type": "object",
     "required": [
      "venueId",
      "name"
     ],
     "properties": {
      "venueId": {
       "type": "string",
       "format": "uuid",
       "description": "**The venue's scope node** (`tenancy.OrgUnit.id`, level venue): what every guest screen that declares `venueId` `from: session` reads once the guest picks it."
      },
      "name": {
       "type": "string",
       "maxLength": 200,
       "description": "The venue's name (`tenancy.OrgUnit.name`)."
      },
      "city": {
       "type": "string",
       "maxLength": 120,
       "nullable": true,
       "description": "Shown under the name so two venues with similar names can be told apart."
      },
      "openingHoursToday": {
       "type": "object",
       "nullable": true,
       "description": "Today's opening hours in the venue's time zone, from `tenancy.VenueSettings` opening hours. Null when the venue is closed today or has none set.",
       "properties": {
        "opens": {
         "type": "string",
         "pattern": "^([01][0-9]|2[0-3]):[0-5][0-9]$"
        },
        "closes": {
         "type": "string",
         "pattern": "^([01][0-9]|2[0-3]):[0-5][0-9]$"
        }
       }
      }
     }
    }
   },
   "whatsNew": {
    "type": "array",
    "maxItems": 10,
    "x-ticvai-derived": "onRead",
    "description": "**Public: the guest \"what's new\"** (decided 29 September, rev 3 GAP-B2). Newest first, at most 10, from `platform-ops.Release.guestReleaseNotes` of the releases the tenant's cell has received; a release with no guest notes is skipped. Returned with or without a staff session.\n",
    "items": {
     "type": "object",
     "required": [
      "version",
      "publishedAt",
      "notes"
     ],
     "properties": {
      "version": {
       "type": "string",
       "description": "The release version."
      },
      "publishedAt": {
       "type": "string",
       "format": "date-time",
       "description": "When the release reached the tenant's cell."
      },
      "notes": {
       "$ref": "#/components/schemas/LocalisedText"
      }
     }
    }
   },
   "recentChanges": {
    "type": "array",
    "description": "Staff only. Names the principal behind each change, so it never reaches a public response.",
    "items": {
     "type": "object",
     "properties": {
      "area": {
       "type": "string"
      },
      "description": {
       "type": "string"
      },
      "principalId": {
       "type": "string",
       "format": "uuid"
      },
      "at": {
       "type": "string",
       "format": "date-time"
      }
     }
    }
   }
  }
 },
 "VenueContact": {
  "x-ticvai-persistence": "none — embedded in tenant_config",
  "type": "object",
  "nullable": true,
  "description": "How a guest reaches the venue: WEB-028 Contact & Venue Information, and the screen shown on an error or when the app cannot help (decided 28 September, audit R073). Public, because nothing here is personal.\n",
  "properties": {
   "phone": {
    "type": "string",
    "nullable": true
   },
   "email": {
    "type": "string",
    "format": "email",
    "nullable": true
   },
   "whatsapp": {
    "type": "string",
    "nullable": true
   },
   "address": {
    "allOf": [
     {
      "$ref": "#/components/schemas/LocalisedText"
     }
    ],
    "nullable": true
   },
   "openingHours": {
    "allOf": [
     {
      "$ref": "#/components/schemas/LocalisedText"
     }
    ],
    "nullable": true,
    "description": "Prose, as the guest reads it. The bookable hours are the catalogue's."
   }
  }
 },
 "VisitPlan": {
  "type": "object",
  "x-ticvai-persistence": "venuemap.visit_plan",
  "description": "**A guest's visit plan** (29 September, MOB-6): the Plan tab. One row per plan; its items are `venuemap.visit_plan_item` rows carrying the version they belong to, so every earlier version stays readable and undo is a new version equal to an old one. **Owned by the guest session**, like a cart: `subjectId` when signed in, `sessionRef` for an anonymous device session, claimed on sign-in.\n",
  "required": [
   "id",
   "venueId",
   "status",
   "version",
   "days"
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
    "type": "string",
    "readOnly": true,
    "description": "Derived from `venueId`."
   },
   "subjectId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true,
    "x-ticvai-references": "marketing.guest_profile",
    "description": "The signed-in guest. From the session, never from the body."
   },
   "sessionRef": {
    "type": "string",
    "nullable": true,
    "readOnly": true,
    "description": "The anonymous device session that owns the plan until sign-in."
   },
   "status": {
    "type": "string",
    "enum": [
     "draft",
     "booked",
     "archived"
    ],
    "readOnly": true,
    "description": "`booked` after `bookVisitPlan`; a booked plan is read-only. `archived` after its last date."
   },
   "version": {
    "type": "integer",
    "minimum": 1,
    "readOnly": true,
    "description": "The current version. Every `updateVisitPlan` adds one."
   },
   "source": {
    "type": "string",
    "enum": [
     "rules",
     "preset",
     "aiAgent"
    ],
    "readOnly": true,
    "description": "What produced the current version: the rules planner, a preset, or the AI planner agent acting for the guest. **The guest sees which**, as every AI answer says what it is based on.\n"
   },
   "inputs": {
    "$ref": "#/components/schemas/VisitPlanRequest"
   },
   "mapVersion": {
    "type": "integer",
    "readOnly": true,
    "description": "The published map version the plan was laid out on."
   },
   "cartId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true,
    "x-ticvai-references": "orders.cart",
    "description": "The cart `bookVisitPlan` filled."
   },
   "excluded": {
    "type": "array",
    "readOnly": true,
    "description": "**What was left out and why**, e.g. a coaster excluded because one of the party is under its 120 cm minimum. Shown on GST-053, so the planner never looks as if it forgot.\n",
    "items": {
     "type": "object",
     "properties": {
      "pointId": {
       "type": "string",
       "format": "uuid"
      },
      "productId": {
       "type": "string",
       "format": "uuid",
       "nullable": true
      },
      "reason": {
       "type": "string",
       "enum": [
        "heightRule",
        "ageRule",
        "closedOnDate",
        "notInInterests",
        "noTime",
        "notAtVenue"
       ],
       "description": "`notAtVenue` (30 September, MoM 4.7): a must-include point that is at none of the plan's venues, so no day could hold it.\n"
      }
     }
    }
   },
   "unmatchedPreferences": {
    "type": "array",
    "readOnly": true,
    "x-ticvai-persisted": false,
    "x-ticvai-derived": "onRead",
    "description": "**A preference a day's venue cannot meet is said, never faked** (30 September client meeting, MoM 4.7, Allam's requirement). One entry per day and preference that no point of that day's venue matches: a cuisine (`cuisineTags`), a shop (`retailTags`) or an interest (`interestTags`). `availableAtVenueIds` names the tenant's other active venues whose published map does match, so GST-053 and WEB-050 can say *Indian food is at the other park (day 2)* instead of quietly placing a restaurant the party cannot reach. Empty when every preference is met on every day. Worked out on read for the version read (a swap can meet or lose a preference), never stored.\n",
    "items": {
     "type": "object",
     "required": [
      "date",
      "venueId",
      "preference",
      "tag"
     ],
     "properties": {
      "date": {
       "type": "string",
       "format": "date"
      },
      "venueId": {
       "type": "string",
       "format": "uuid",
       "description": "The day's venue, which has no match."
      },
      "preference": {
       "type": "string",
       "enum": [
        "cuisine",
        "retail",
        "interest"
       ]
      },
      "tag": {
       "type": "string",
       "maxLength": 30
      },
      "availableAtVenueIds": {
       "type": "array",
       "items": {
        "type": "string",
        "format": "uuid"
       },
       "description": "Other active venues of the tenant where the tag is matched. Empty when none is."
      }
     }
    }
   },
   "days": {
    "type": "array",
    "readOnly": true,
    "description": "One per date, in order. The items of the version read.",
    "items": {
     "type": "object",
     "required": [
      "date",
      "venueId",
      "items"
     ],
     "properties": {
      "date": {
       "type": "string",
       "format": "date"
      },
      "venueId": {
       "type": "string",
       "format": "uuid",
       "description": "**The venue this day is planned at** (30 September, MoM 4.7): `VisitPlanRequest.dayVenues` for the date, else `venueId`. Every item of the day is at this venue.\n"
      },
      "opensAt": {
       "type": "string",
       "nullable": true
      },
      "closesAt": {
       "type": "string",
       "nullable": true
      },
      "items": {
       "type": "array",
       "items": {
        "$ref": "#/components/schemas/VisitPlanItem"
       }
      }
     }
    }
   },
   "createdAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   },
   "updatedAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   }
  }
 },
 "VisitPlanAlternative": {
  "type": "object",
  "x-ticvai-persistence": "none — computed on read",
  "description": "One candidate for a swap (29 September, MOB-6).",
  "required": [
   "kind",
   "venueId",
   "startsAt",
   "reason"
  ],
  "properties": {
   "kind": {
    "type": "string",
    "enum": [
     "attraction",
     "show",
     "meal",
     "shop",
     "rest"
    ]
   },
   "venueId": {
    "type": "string",
    "format": "uuid",
    "description": "The item's day venue; an alternative is never from another venue (30 September, MoM 4.7)."
   },
   "pointId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "productId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "performanceId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "name": {
    "type": "string"
   },
   "startsAt": {
    "type": "string",
    "format": "date-time"
   },
   "durationMinutes": {
    "type": "integer"
   },
   "walkMinutes": {
    "type": "integer",
    "nullable": true
   },
   "expectedWaitMinutes": {
    "type": "integer",
    "nullable": true
   },
   "matchedInterests": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "reason": {
    "type": "string",
    "description": "Why it is offered, in words the sheet shows, e.g. *Same thrill level, 4 minutes closer*."
   }
  }
 },
 "VisitPlanBooking": {
  "type": "object",
  "x-ticvai-persistence": "none — computed; the lines are orders.cart_line rows",
  "description": "What `bookVisitPlan` returns (29 September, MOB-6): the cart handoff.",
  "required": [
   "planId",
   "cartId",
   "added",
   "notAdded"
  ],
  "properties": {
   "planId": {
    "type": "string",
    "format": "uuid"
   },
   "cartId": {
    "type": "string",
    "format": "uuid"
   },
   "added": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "itemId": {
       "type": "string",
       "format": "uuid"
      },
      "cartLineId": {
       "type": "string",
       "format": "uuid"
      },
      "leaseExpiresAt": {
       "type": "string",
       "format": "date-time",
       "nullable": true
      }
     }
    }
   },
   "notAdded": {
    "type": "array",
    "description": "Items that could not be added, with the `addCartLine` refusal each met.",
    "items": {
     "type": "object",
     "properties": {
      "itemId": {
       "type": "string",
       "format": "uuid"
      },
      "reason": {
       "type": "string",
       "description": "The orders `CartProblem` code, e.g. `soldOutForSession`, `productInfoOnly`, `seatLimitExceeded`."
      }
     }
    }
   },
   "freeItems": {
    "type": "integer",
    "description": "Stops that need nothing bought."
   }
  }
 },
 "VisitPlanItem": {
  "type": "object",
  "x-ticvai-persistence": "venuemap.visit_plan_item",
  "description": "**One timed stop on a plan day** (29 September, MOB-6). Rows are kept per `planVersion`: a change writes the day's items again under the new version, and an older version's rows are never updated.\n",
  "required": [
   "id",
   "planId",
   "planVersion",
   "date",
   "sequence",
   "kind",
   "startsAt",
   "endsAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "planId": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "x-ticvai-references": "venuemap.visit_plan"
   },
   "planVersion": {
    "type": "integer",
    "minimum": 1,
    "readOnly": true
   },
   "date": {
    "type": "string",
    "format": "date"
   },
   "sequence": {
    "type": "integer",
    "minimum": 1
   },
   "kind": {
    "type": "string",
    "enum": [
     "attraction",
     "show",
     "meal",
     "shop",
     "rest",
     "travel"
    ],
    "description": "`meal` is a stop at a dining point (restaurant, cafe or food kiosk); `shop` is a retail stop at a shop or a retail kiosk (30 September client meeting, MoM 4.7: retail is placed from the day venue's own points, as dining is).\n"
   },
   "venueId": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "x-ticvai-persisted": false,
    "x-ticvai-derived": "onRead",
    "description": "**The venue of this stop** (30 September client meeting, MoM 4.7): always the day's venue, and the venue whose map `pointId` is on. Carried on the item so the screens, `bookVisitPlan` and the AI planner agent read it rather than infer it. **Worked out on read, not stored**: from the plan's `inputs` (`dayVenues` for the item's date, else `venueId`). A stored `venue_id` would move the item rows from the plan's own row-level policy to a venue policy and hide a second park's items from the guest who owns the plan.\n"
   },
   "pointId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "x-ticvai-references": "venuemap.point"
   },
   "productId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "x-ticvai-references": "catalogue.product",
    "description": "What is bought for this stop, where it is bought. Null for a free stop."
   },
   "bundleId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "x-ticvai-references": "promotions.bundle",
    "description": "A meal combo or package, from the point's `featuredOffer`."
   },
   "performanceId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "x-ticvai-references": "catalogue.performance"
   },
   "startsAt": {
    "type": "string",
    "format": "date-time"
   },
   "endsAt": {
    "type": "string",
    "format": "date-time"
   },
   "walkMinutesBefore": {
    "type": "integer",
    "minimum": 0,
    "nullable": true
   },
   "expectedWaitMinutes": {
    "type": "integer",
    "minimum": 0,
    "nullable": true,
    "description": "The typical wait at that hour when the plan was laid out; GST-059 replaces it with the live one."
   },
   "addOnSuggestion": {
    "type": "object",
    "nullable": true,
    "description": "A suggested add-on for this stop, e.g. Fast Track where the wait is long. Never added by itself.",
    "properties": {
     "productId": {
      "type": "string",
      "format": "uuid"
     },
     "reason": {
      "type": "string"
     }
    }
   },
   "addOnAccepted": {
    "type": "boolean",
    "default": false
   },
   "pinned": {
    "type": "boolean",
    "default": false,
    "description": "The guest fixed this stop; a re-lay moves other stops around it."
   },
   "note": {
    "type": "string",
    "nullable": true,
    "maxLength": 200
   }
  }
 },
 "VisitPlanRequest": {
  "type": "object",
  "x-ticvai-persistence": "none — request only; kept as `inputs` on venuemap.visit_plan",
  "description": "What `generateVisitPlan` takes (29 September, MOB-6): the Plan tab's form on GST-051 and WEB-050.\n",
  "required": [
   "venueId",
   "dates",
   "party"
  ],
  "properties": {
   "venueId": {
    "type": "string",
    "format": "uuid",
    "description": "The venue the guest picked in the app (GST-001 / WEB-001), which scopes the plan. Every date is planned at this venue unless `dayVenues` puts it somewhere else.\n"
   },
   "dayVenues": {
    "type": "array",
    "maxItems": 7,
    "description": "**Which venue on which date, in a multi-venue tenant** (30 September client meeting, MoM 4.7, Allam's requirement). One entry per date that is not at `venueId`; each date of `dates` at most once. Each venue must be an active venue of the caller's tenant (the options `getTenantAppStatus.venues` lists), else 422 `venue-not-in-tenant`. **Each day is then planned from that venue's own published map only**: its rides, its dining and its retail points, never another venue's.\n",
    "items": {
     "type": "object",
     "required": [
      "date",
      "venueId"
     ],
     "properties": {
      "date": {
       "type": "string",
       "format": "date"
      },
      "venueId": {
       "type": "string",
       "format": "uuid"
      }
     }
    }
   },
   "dates": {
    "type": "array",
    "minItems": 1,
    "maxItems": 7,
    "items": {
     "type": "string",
     "format": "date"
    }
   },
   "party": {
    "type": "array",
    "minItems": 1,
    "maxItems": 20,
    "description": "One entry per person. **Height where the guest knows it, age otherwise**: height is what ride eligibility rules test, and an age band is the fallback the rule may also state. Nothing here identifies a person.\n",
    "items": {
     "type": "object",
     "properties": {
      "heightCm": {
       "type": "integer",
       "minimum": 40,
       "maximum": 230,
       "nullable": true
      },
      "ageYears": {
       "type": "integer",
       "minimum": 0,
       "maximum": 120,
       "nullable": true
      }
     }
    }
   },
   "pace": {
    "type": "string",
    "enum": [
     "packed",
     "relaxed"
    ],
    "default": "relaxed"
   },
   "interestTags": {
    "type": "array",
    "maxItems": 12,
    "description": "The same closed list as `VenuePoint.interestTags`.",
    "items": {
     "type": "string"
    }
   },
   "cuisineTags": {
    "type": "array",
    "maxItems": 8,
    "description": "Matched per day against the `cuisineTags` of that day's venue's dining points only (30 September, MoM 4.7). A cuisine no dining point of the day's venue serves is not forced into the day; it is reported in `VisitPlan.unmatchedPreferences`.\n",
    "items": {
     "type": "string"
    }
   },
   "retailTags": {
    "type": "array",
    "maxItems": 8,
    "description": "**Shops the party would like to visit** (30 September client meeting, MoM 4.7: retail and kiosk shops join F&B as venue-linked planner options), e.g. `souvenirs`, `toys`, `apparel`, `essentials`. Matched per day against `VenuePoint.retailTags` of that day's venue's shops and retail kiosks; an unmatched tag is reported, as a cuisine is.\n",
    "items": {
     "type": "string",
     "maxLength": 30
    }
   },
   "mustIncludePointIds": {
    "type": "array",
    "maxItems": 10,
    "description": "Placed on a day whose venue has the point. A point at none of the plan's venues is listed in `VisitPlan.excluded` with `notAtVenue`, never placed on another venue's day.\n",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "preset": {
    "type": "string",
    "nullable": true,
    "enum": [
     "highlights",
     "family",
     "thrillSeeker",
     "waterDay",
     "relaxed",
     "showsAndDining"
    ],
    "description": "A ready-made day plan (GST-052 Suggested Itineraries): the preset fixes the interests and the pace, and the party still decides eligibility.\n"
   },
   "presetKey": {
    "type": "string",
    "nullable": true,
    "maxLength": 64,
    "pattern": "^[a-z][a-zA-Z0-9]*$",
    "description": "The ready-made plan the guest took on GST-052 (30 September, second wave of the 29 September pass, MOB-6): one of the built-in `preset` keys above, or a key of a ready-made plan the venue defines. **The same rules planner runs**: the preset only supplies interests, pace and must-include points, and the party still decides eligibility. When both `preset` and `presetKey` are sent they must name the same plan; `presetKey` is the field new clients send. An unknown key is refused 422 `unknown-preset`.\n"
   },
   "startTime": {
    "type": "string",
    "nullable": true,
    "pattern": "^([01][0-9]|2[0-3]):[0-5][0-9]$",
    "description": "When the party arrives. Null means opening time."
   },
   "locale": {
    "type": "string",
    "nullable": true
   }
  }
 },
 "VisitPlanUpdate": {
  "type": "object",
  "x-ticvai-persistence": "none — request only; lands as a new version of venuemap.visit_plan_item rows",
  "description": "What `updateVisitPlan` takes (29 September, MOB-6).",
  "required": [
   "baseVersion",
   "changes"
  ],
  "properties": {
   "baseVersion": {
    "type": "integer",
    "minimum": 1
   },
   "changes": {
    "type": "array",
    "minItems": 1,
    "maxItems": 20,
    "items": {
     "type": "object",
     "required": [
      "op"
     ],
     "properties": {
      "op": {
       "type": "string",
       "enum": [
        "swap",
        "remove",
        "add",
        "move",
        "pin",
        "acceptAddOn",
        "declineAddOn",
        "revertTo"
       ]
      },
      "itemId": {
       "type": "string",
       "format": "uuid",
       "nullable": true
      },
      "date": {
       "type": "string",
       "format": "date",
       "nullable": true
      },
      "pointId": {
       "type": "string",
       "format": "uuid",
       "nullable": true
      },
      "performanceId": {
       "type": "string",
       "format": "uuid",
       "nullable": true
      },
      "startsAt": {
       "type": "string",
       "format": "date-time",
       "nullable": true
      },
      "version": {
       "type": "integer",
       "nullable": true,
       "description": "For `revertTo`, the earlier version to restore (undo)."
      }
     }
    }
   }
  }
 },
 "WaitTime": {
  "x-ticvai-persistence": "none — computed from readings and throughput",
  "type": "object",
  "required": [
   "queueId",
   "waitMinutes",
   "source",
   "asOf",
   "isStale"
  ],
  "properties": {
   "queueId": {
    "type": "string",
    "format": "uuid"
   },
   "queueName": {
    "$ref": "#/components/schemas/LocalisedText"
   },
   "attractionProductId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "attractionCategoryId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The catalogue `ProductCategory` the attraction product is filed under — the value the `category` filter on `getWaitTimes` matches. Read from catalogue, not stored here.\n"
   },
   "status": {
    "$ref": "#/components/schemas/QueueStatus"
   },
   "waitMinutes": {
    "type": "integer",
    "nullable": true,
    "description": "Null where the queue is closed or no estimate is available."
   },
   "source": {
    "$ref": "#/components/schemas/WaitTimeSource"
   },
   "isStale": {
    "type": "boolean",
    "description": "The underlying feed has gone quiet past its expected interval. The figure is shown with a caveat rather than frozen and presented as current, and it is not hidden (decided 28 September, audit R080 (b)): the screen shows `waitMinutes` with its `asOf` and a stale marker.\n"
   },
   "heightRequirementCm": {
    "type": "integer",
    "nullable": true
   },
   "zone": {
    "type": "string",
    "nullable": true
   },
   "asOf": {
    "type": "string",
    "format": "date-time",
    "description": "When the figure was produced — the queue's `waitTimeAsOf`."
   }
  }
 },
 "WaitTimeSource": {
  "type": "string",
  "description": "Where the estimate came from. Surfaced so an operator knows whether a figure is measured or guessed.\n",
  "enum": [
   "sensor",
   "throughput",
   "manual",
   "unavailable"
  ]
 }
}
```
