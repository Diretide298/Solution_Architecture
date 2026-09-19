# P02-engagement-support-01 — P02 · Engagement & Support (1 of 2)

**10 screens · 21 operations · 45 schemas · 4 permissions**

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
- **6 of these operations work offline**: getWaitTimes, listCatalogueBundles, listContentPages, listFaqs, listProducts, raiseMyCase
  — and the rest do not. A surface that looks the same online and off is lying.
- **Offline, every screen shows one banner, the same on web and app:** *"You're offline. Connect to the internet to book, pay, order or join a queue."* The moment the connection drops, on every screen, above the screen's own content. By itself as soon as the connection is back, with a short "Back online" confirmation. **It never** Covers what is already on screen, or appears for a server error — that is the screen's own error state, and a guest told they are offline when the venue is down reconnects for nothing. Each screen's `states.offline` says what stays on screen and what waits.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `GST-030` | In-Venue Notifications | configEditor | 1 | 0 | — |
| `GST-031` | AI Concierge – Home | statusTracker | 5 | 0 | — |
| `GST-032` | AI Concierge – Chat | statusTracker | 8 | 0 | — |
| `GST-033` | AI Concierge – Contextual Help | configEditor | 1 | 0 | — |
| `GST-035` | Feedback & Ratings | configEditor | 2 | 0 | — |
| `GST-040` | Help & Support | commandCentre | 5 | 0 | — |
| `GST-051` | Plan Your Adventure – Start | listDetail | 2 | 0 | — |
| `GST-052` | Suggested Itineraries | listDetail | 3 | 0 | — |
| `GST-053` | Build Your Own Itinerary | listDetail | 4 | 0 | — |
| `GST-054` | AI Optimized Itinerary | listDetail | 4 | 0 | — |

## Thin screens in this batch

**GST-030, GST-033, GST-051, GST-052, GST-053 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

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
    "GST-003",
    "GST-031"
   ],
   "fromFlows": true,
   "transitions": [
    {
     "to": "GST-001",
     "trigger": "Home – Default",
     "carries": [
      "subjectId"
     ],
     "provenance": "derived — GST-001 declares entryState.params subjectId, so an edge into it must carry them"
    },
    {
     "to": "GST-003",
     "trigger": "Event & Attraction Listing",
     "carries": [
      "eventId"
     ],
     "provenance": "derived — GST-003 declares entryState.params eventId, so an edge into it must carry them"
    },
    {
     "to": "GST-031",
     "trigger": "AI Concierge – Home",
     "carries": [
      "conversationId",
      "outletId"
     ],
     "provenance": "derived — GST-031 declares entryState.params conversationId, outletId, so an edge into it must carry them"
    }
   ]
  },
  "notes": "States derived from the screen pattern on 17 August, not individually considered. Purpose derived from the screen name and its operations on 17 August, not from a requirement.",
  "openQuestions": [
   "Inventory cites `GET /notifications` — no matching operation. Written before the contracts existed."
  ],
  "density": "comfortable",
  "pattern": "configEditor",
  "patternReason": "the screen declares only writes (`claimLocationSession`) and no read of a population — it is settings, not a list",
  "purpose": "Work with in-venue notifications for this venue.",
  "gaps": [
   {
    "operation": "claimLocationSession",
    "why": "**`claimLocationSession` declares no request body shape**, so nothing says what this editor edits. The fields cannot be derived and the screen needs the contract before it needs a designer.",
    "source": "contract fnb.yaml POST /location-sessions"
   }
  ],
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Claim",
       "operation": "claimLocationSession",
       "provenance": "contract fnb.yaml POST /location-sessions"
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
       "impliedBy": "claimLocationSession"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The saved in-venue notifications.",
   "error": "Could not load. Names which read failed and leaves the in-venue notifications untouched.",
   "emptyFirstRun": "No in-venue notifications configured. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "offline": "**The offline banner shows.** Notices already received stay listed. New queue calls and order updates arrive once the connection is back, and the banner is the warning that they may be late."
  },
  "apis": [
   {
    "operationId": "claimLocationSession",
    "contract": "fnb",
    "purpose": "From the flow it appears in",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P02 Guest App.dc.html#gst-030"
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
    "GST-003",
    "GST-032"
   ],
   "fromFlows": true,
   "transitions": [
    {
     "to": "GST-001",
     "trigger": "Home – Default",
     "carries": [
      "subjectId"
     ],
     "provenance": "derived — GST-001 declares entryState.params subjectId, so an edge into it must carry them"
    },
    {
     "to": "GST-003",
     "trigger": "Event & Attraction Listing",
     "carries": [
      "eventId"
     ],
     "provenance": "derived — GST-003 declares entryState.params eventId, so an edge into it must carry them"
    },
    {
     "to": "GST-032",
     "trigger": "AI Concierge – Chat",
     "carries": [
      "cartId",
      "conversationId",
      "orderId"
     ],
     "provenance": "derived — GST-032 declares entryState.params cartId, conversationId, orderId, so an edge into it must carry them"
    }
   ]
  },
  "notes": "States derived from the screen pattern on 17 August, not individually considered. Purpose derived from the screen name and its operations on 17 August, not from a requirement. **Guest concierge confirmed in Phase 1 on 17 August (CF-14), charged per token and bounded by `AiPolicy.guestCapabilityScope`.** Still degrades to the manual planner rather than to an error. **Cross-surface parity, 31 August**: added createAiConversation, handoverToAgent, requestSuggestion. **A guest does not know which surface they are on** — the same named screen on web and app now calls the same guest-callable operations.",
  "openQuestions": [
   "Inventory cites `POST /ai/concierge` — no matching operation. Written before the contracts existed."
  ],
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
       "label": "The selected concierge home",
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
       "label": "Send",
       "operation": "sendAiMessage",
       "provenance": "contract ai.yaml POST /conversations/{conversationId}/messages"
      },
      {
       "kind": "secondaryButton",
       "label": "Create",
       "operation": "createAiConversation",
       "provenance": "contract ai.yaml POST /conversations"
      },
      {
       "kind": "secondaryButton",
       "label": "Handover",
       "operation": "handoverToAgent",
       "provenance": "contract marketing-crm.yaml POST /conversations/{conversationId}/handover"
      },
      {
       "kind": "secondaryButton",
       "label": "Request",
       "operation": "requestSuggestion",
       "provenance": "contract ai.yaml POST /ai/suggestions"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The concierge home list.",
   "error": "Could not load. Names which read failed and leaves the concierge home untouched.",
   "emptyFirstRun": "No concierge home yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the concierge home are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
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
    "purpose": "requestSuggestion",
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
   "provenance": "generated",
   "board": "wireframes/P02 Guest App.dc.html#gst-031"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 5 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
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
    "GST-003",
    "GST-033"
   ],
   "fromFlows": true,
   "transitions": [
    {
     "to": "GST-001",
     "trigger": "Home – Default",
     "carries": [
      "subjectId"
     ],
     "provenance": "derived — GST-001 declares entryState.params subjectId, so an edge into it must carry them"
    },
    {
     "to": "GST-003",
     "trigger": "Event & Attraction Listing",
     "carries": [
      "eventId"
     ],
     "provenance": "derived — GST-003 declares entryState.params eventId, so an edge into it must carry them"
    },
    {
     "to": "GST-033",
     "trigger": "AI Concierge – Contextual Help",
     "carries": [
      "conversationId"
     ],
     "provenance": "derived — GST-033 declares entryState.params conversationId, so an edge into it must carry them"
    }
   ]
  },
  "notes": "States derived from the screen pattern on 17 August, not individually considered. Purpose derived from the screen name and its operations on 17 August, not from a requirement. **Guest concierge confirmed in Phase 1 on 17 August (CF-14), charged per token and bounded by `AiPolicy.guestCapabilityScope`.** Still degrades to the manual planner rather than to an error.",
  "openQuestions": [
   "Inventory cites `POST /ai/concierge` — no matching operation. Written before the contracts existed."
  ],
  "density": "comfortable",
  "pattern": "statusTracker",
  "patternReason": "`getGuestOrderStatus` reads one record and nothing reads a population — the screen is about that one thing",
  "purpose": "Add ai concierge – chat for this venue.",
  "gaps": [
   {
    "operation": "getCart",
    "why": "**1 declared operation reach no component on this screen**: getCart. Either the screen is missing what calls them, or the declaration is residue.",
    "source": "the screen's own declarations"
   }
  ],
  "layout": {
   "template": "detail",
   "regions": [
    {
     "name": "contentBody",
     "slot": "record",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected concierge chat",
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
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Create",
       "operation": "createGuestFnbOrder",
       "provenance": "contract fnb.yaml POST /guest-orders"
      },
      {
       "kind": "secondaryButton",
       "label": "Add",
       "operation": "addCartLine",
       "provenance": "contract orders.yaml POST /carts/{cartId}/lines"
      },
      {
       "kind": "secondaryButton",
       "label": "Checkout",
       "operation": "checkoutCart",
       "provenance": "contract orders.yaml POST /carts/{cartId}/checkout"
      },
      {
       "kind": "secondaryButton",
       "label": "Send",
       "operation": "sendAiMessage",
       "provenance": "contract ai.yaml POST /conversations/{conversationId}/messages"
      },
      {
       "kind": "secondaryButton",
       "label": "Send",
       "operation": "sendConversationMessage",
       "provenance": "contract marketing-crm.yaml POST /conversations/{conversationId}/messages"
      },
      {
       "kind": "secondaryButton",
       "label": "Handover",
       "operation": "handoverToAgent",
       "provenance": "contract marketing-crm.yaml POST /conversations/{conversationId}/handover"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The concierge chat list.",
   "error": "Could not load. Names which read failed and leaves the concierge chat untouched.",
   "emptyFirstRun": "No concierge chat yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the concierge chat are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "offline": "**Not available, and the offline banner says why.** The assistant needs the connection; conversations already loaded stay readable."
  },
  "apis": [
   {
    "operationId": "createGuestFnbOrder",
    "contract": "fnb",
    "purpose": "From the flow it appears in",
    "trigger": "onLoad"
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
    }
   ],
   "coldEntry": "A conversation link an agent opens from a notification. Resolves, or says it was closed and by whom. **A guest opening an order link weeks later.** Shows the order if it still resolves; if it was refunded or the performance passed, says which and offers the order list rather than an error."
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P02 Guest App.dc.html#gst-032"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 8 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
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
    "GST-002",
    "GST-003"
   ],
   "fromFlows": true,
   "transitions": [
    {
     "to": "GST-001",
     "trigger": "Home – Default",
     "carries": [
      "subjectId"
     ],
     "provenance": "derived — GST-001 declares entryState.params subjectId, so an edge into it must carry them"
    },
    {
     "to": "GST-003",
     "trigger": "Event & Attraction Listing",
     "carries": [
      "eventId"
     ],
     "provenance": "derived — GST-003 declares entryState.params eventId, so an edge into it must carry them"
    }
   ]
  },
  "notes": "States derived from the screen pattern on 17 August, not individually considered. Purpose derived from the screen name and its operations on 17 August, not from a requirement. **Guest concierge confirmed in Phase 1 on 17 August (CF-14), charged per token and bounded by `AiPolicy.guestCapabilityScope`.** Still degrades to the manual planner rather than to an error. **createPayment removed 18 August** — attached by module resemblance, not by what this screen does. A screen that does not handle money should not be able to move it (CF-87's class). **Navigation repointed to P15 on 20 August** — the F&B screens it linked to moved out of the back office when the client board was adopted. **Cross-platform navigation removed 24 August**: BO-020. **A till does not navigate to a back office and a guest app does not navigate to either** — those are device handovers, and a flow declares them with `crossesDevice` rather than a screen pretending there is a link.",
  "openQuestions": [
   "Inventory cites `POST /ai/concierge` — no matching operation. Written before the contracts existed."
  ],
  "density": "comfortable",
  "pattern": "configEditor",
  "patternReason": "the screen declares only writes (`sendAiMessage`) and no read of a population — it is settings, not a list",
  "purpose": "Answer a question without needing a person.",
  "gaps": [
   {
    "operation": "sendAiMessage",
    "why": "**`sendAiMessage` declares no request body shape**, so nothing says what this editor edits. The fields cannot be derived and the screen needs the contract before it needs a designer.",
    "source": "contract ai.yaml POST /conversations/{conversationId}/messages"
   }
  ],
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Send",
       "operation": "sendAiMessage",
       "provenance": "contract ai.yaml POST /conversations/{conversationId}/messages"
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
       "impliedBy": "sendAiMessage"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The saved concierge contextual help.",
   "error": "Could not load. Names which read failed and leaves the concierge contextual help untouched.",
   "emptyFirstRun": "No concierge contextual help configured. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
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
   "provenance": "generated",
   "board": "wireframes/P02 Guest App.dc.html#gst-033"
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
    "GST-002",
    "GST-003"
   ],
   "transitions": [
    {
     "to": "GST-001",
     "trigger": "Home – Default",
     "carries": [
      "subjectId"
     ],
     "provenance": "derived — GST-001 declares entryState.params subjectId, so an edge into it must carry them"
    },
    {
     "to": "GST-003",
     "trigger": "Event & Attraction Listing",
     "carries": [
      "eventId"
     ],
     "provenance": "derived — GST-003 declares entryState.params eventId, so an edge into it must carry them"
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
       "label": "Submit",
       "operation": "submitReview",
       "provenance": "contract marketing-crm.yaml POST /reviews"
      },
      {
       "kind": "secondaryButton",
       "label": "Raise",
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
   "emptyFirstRun": "No feedback ratings configured. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "offline": "**The offline banner shows.** What was already loaded stays on screen, marked with its age. Anything that spends money, holds capacity or changes the account waits for the connection, and its button says so rather than failing."
  },
  "apis": [
   {
    "operationId": "submitReview",
    "contract": "marketing-crm",
    "purpose": "from page inventory",
    "trigger": "onLoad"
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
   "provenance": "generated",
   "board": "wireframes/P02 Guest App.dc.html#gst-035"
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
    "GST-002",
    "GST-003"
   ],
   "transitions": [
    {
     "to": "GST-001",
     "trigger": "Home – Default",
     "carries": [
      "subjectId"
     ],
     "provenance": "derived — GST-001 declares entryState.params subjectId, so an edge into it must carry them"
    },
    {
     "to": "GST-003",
     "trigger": "Event & Attraction Listing",
     "carries": [
      "eventId"
     ],
     "provenance": "derived — GST-003 declares entryState.params eventId, so an edge into it must carry them"
    },
    {
     "to": "WEB-034",
     "trigger": "They report something lost",
     "provenance": "flow F54 step 2→3",
     "crossesDevice": true,
     "back": false
    }
   ]
  },
  "notes": "States derived from the screen pattern on 17 August, not individually considered. Purpose derived from the screen name and its operations on 17 August, not from a requirement. **Guest case operations wired 24 August.** **No case operation was guest-callable** — a guest could raise nothing and read nothing, and `check-screens` refused the staff-permissioned ones on a guest surface. `listMyCases`, `raiseMyCase` and `replyToMyCase` are scoped to the caller rather than filtered by a subject parameter.",
  "openQuestions": [
   "Inventory cites `GET /support` — no matching operation. Written before the contracts existed."
  ],
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
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every help support",
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
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Raise",
       "operation": "raiseMyCase",
       "provenance": "contract marketing-crm.yaml POST /my/cases"
      },
      {
       "kind": "secondaryButton",
       "label": "Reply",
       "operation": "replyToMyCase",
       "provenance": "contract marketing-crm.yaml POST /my/cases/{caseId}/messages"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The help support list.",
   "error": "Could not load. Names which read failed and leaves the help support untouched.",
   "emptyFirstRun": "No help support yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the help support are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "offline": "**The offline banner shows.** What was already loaded stays on screen, marked with its age. Anything that spends money, holds capacity or changes the account waits for the connection, and its button says so rather than failing."
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
   "provenance": "generated",
   "board": "wireframes/P02 Guest App.dc.html#gst-040"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 5 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
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
  "name": "Plan Your Adventure – Start",
  "module": "Engagement & Support",
  "requiresModule": "queue",
  "wave": 3,
  "capability": "AI-35",
  "implementation": {
   "app": "guest-app",
   "route": "/general/plan-your-adventure-start",
   "component": "apps/guest-app/src/routes/general/PlanYourAdventureStartDetail.tsx",
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
    "GST-003",
    "GST-052"
   ],
   "transitions": [
    {
     "to": "GST-052",
     "trigger": "Suggested itineraries are offered",
     "provenance": "flow F49 step 1→2",
     "operation": "listProducts"
    },
    {
     "to": "GST-001",
     "trigger": "Home – Default",
     "carries": [
      "subjectId"
     ],
     "provenance": "derived — GST-001 declares entryState.params subjectId, so an edge into it must carry them"
    },
    {
     "to": "GST-003",
     "trigger": "Event & Attraction Listing",
     "carries": [
      "eventId"
     ],
     "provenance": "derived — GST-003 declares entryState.params eventId, so an edge into it must carry them"
    }
   ]
  },
  "notes": "Minuted 10 Aug §4.9. Benchmarked against Skidata. Tied to a ticket purchase and saved as a personal visit profile.",
  "openQuestions": [
   "Inventory cites `POST /ai/itinerary` — no matching operation. Written before the contracts existed."
  ],
  "density": "comfortable",
  "pattern": "listDetail",
  "patternReason": "`listProducts` reads the population and `getWaitTimes` reads one of them — list, select, act",
  "purpose": "Start a plan for the visit — which attractions, in what order — before arriving.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every plan your adventure",
       "bindsTo": "Product",
       "columns": [
        "Product.id",
        "Product.code",
        "Product.name",
        "Product.description",
        "Product.kind",
        "Product.venueId",
        "Product.scopePath",
        "Product.createdByPrincipalId",
        "Product.approvedByPrincipalId",
        "Product.responsibleDepartmentId",
        "Product.onSaleFrom",
        "Product.onSaleTo"
       ],
       "operation": "listProducts",
       "provenance": "contract catalogue.yaml GET /products"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected plan your adventure",
       "bindsTo": "WaitTime",
       "columns": [
        "WaitTime.queueId",
        "WaitTime.queueName",
        "WaitTime.attractionProductId",
        "WaitTime.status",
        "WaitTime.waitMinutes",
        "WaitTime.source",
        "WaitTime.isStale",
        "WaitTime.heightRequirementCm",
        "WaitTime.zone",
        "WaitTime.asOf"
       ],
       "operation": "getWaitTimes",
       "provenance": "contract queue.yaml GET /queues/wait-times"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The plan your adventure list.",
   "error": "Could not load. Names which read failed and leaves the plan your adventure untouched.",
   "emptyFirstRun": "No plan your adventure yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the plan your adventure are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
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
   }
  ],
  "entryState": {
   "preloaded": [
    "WaitTime.queueId",
    "WaitTime.queueName",
    "WaitTime.attractionProductId",
    "WaitTime.status",
    "WaitTime.waitMinutes"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P02 Guest App.dc.html#gst-051"
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
  "requiresModule": "ai",
  "wave": 3,
  "capability": "AI-35",
  "implementation": {
   "app": "guest-app",
   "route": "/general/suggested-itineraries",
   "component": "apps/guest-app/src/routes/general/SuggestedItinerariesDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "GST-001",
    "GST-051"
   ],
   "inferred": true,
   "exitTo": [
    "GST-001",
    "GST-002",
    "GST-003",
    "GST-053"
   ],
   "transitions": [
    {
     "to": "GST-053",
     "trigger": "They build their own instead",
     "provenance": "flow F49 step 2→3",
     "operation": "listProducts"
    },
    {
     "to": "GST-001",
     "trigger": "Home – Default",
     "carries": [
      "subjectId"
     ],
     "provenance": "derived — GST-001 declares entryState.params subjectId, so an edge into it must carry them"
    },
    {
     "to": "GST-003",
     "trigger": "Event & Attraction Listing",
     "carries": [
      "eventId"
     ],
     "provenance": "derived — GST-003 declares entryState.params eventId, so an edge into it must carry them"
    }
   ]
  },
  "notes": "Minuted 10 Aug §4.9. ** wired 24 August.** The board drew four bespoke AI endpoints for itinerary planning; **one operation with a kind answers all of them** (ADR-0028), and recording the outcome is what lets a model replace the heuristic later. **`recordSuggestionOutcome` removed from the guest surface.** `check-screens` refused it and was right: **a guest does not record an outcome — the platform observes what they did.** A guest app that self-reports whether it took the advice is a training label the guest could forge, and the observation belongs server-side where the plan and the visit can be compared.",
  "openQuestions": [
   "Inventory cites `GET /itineraries/suggested` — no matching operation. Written before the contracts existed."
  ],
  "density": "comfortable",
  "pattern": "listDetail",
  "patternReason": "`listProducts` reads a population and nothing reads one of them; the detail is the row until a `get` exists",
  "purpose": "Curated plans a guest can take rather than build.",
  "gaps": [
   {
    "operation": "listCatalogueBundles",
    "why": "**1 declared operation reach no component on this screen**: listCatalogueBundles. Either the screen is missing what calls them, or the declaration is residue.",
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
       "label": "Every suggested itineraries",
       "bindsTo": "Product",
       "columns": [
        "Product.id",
        "Product.code",
        "Product.name",
        "Product.description",
        "Product.kind",
        "Product.venueId",
        "Product.scopePath",
        "Product.createdByPrincipalId",
        "Product.approvedByPrincipalId",
        "Product.responsibleDepartmentId",
        "Product.onSaleFrom",
        "Product.onSaleTo"
       ],
       "operation": "listProducts",
       "provenance": "contract catalogue.yaml GET /products"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected suggested itineraries",
       "bindsTo": "Product",
       "columns": [
        "Product.id",
        "Product.code",
        "Product.name",
        "Product.description",
        "Product.kind",
        "Product.venueId",
        "Product.scopePath",
        "Product.createdByPrincipalId",
        "Product.approvedByPrincipalId",
        "Product.responsibleDepartmentId",
        "Product.onSaleFrom",
        "Product.onSaleTo",
        "Product.lifecycleState",
        "Product.isSellable",
        "Product.hasVariants",
        "Product.variantCount"
       ],
       "operation": "listProducts",
       "provenance": "contract catalogue.yaml GET /products"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Request",
       "operation": "requestSuggestion",
       "provenance": "contract ai.yaml POST /ai/suggestions"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The suggested itineraries list.",
   "error": "Could not load. Names which read failed and leaves the suggested itineraries untouched.",
   "emptyFirstRun": "No suggested itineraries yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the suggested itineraries are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
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
    "operationId": "requestSuggestion",
    "contract": "ai",
    "purpose": "",
    "trigger": "onAction",
    "invalidates": [
     "listProducts"
    ]
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "suggestionId",
     "from": "deepLink",
     "optional": true
    }
   ],
   "coldEntry": "A suggestion opened from a saved plan.",
   "preloaded": [
    "Product.id",
    "Product.code",
    "Product.name",
    "Product.description",
    "Product.kind"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P02 Guest App.dc.html#gst-052"
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
  "name": "Build Your Own Itinerary",
  "module": "Engagement & Support",
  "requiresModule": "ticketing",
  "wave": 3,
  "capability": "C02",
  "implementation": {
   "app": "guest-app",
   "route": "/general/build-your-own-itinerary",
   "component": "apps/guest-app/src/routes/general/BuildYourOwnItineraryDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "GST-001",
    "GST-052"
   ],
   "inferred": true,
   "exitTo": [
    "GST-001",
    "GST-002",
    "GST-003",
    "GST-054"
   ],
   "transitions": [
    {
     "to": "GST-054",
     "trigger": "An optimised order is proposed",
     "provenance": "flow F49 step 3→4",
     "operation": "listProducts"
    },
    {
     "to": "GST-001",
     "trigger": "Home – Default",
     "carries": [
      "subjectId"
     ],
     "provenance": "derived — GST-001 declares entryState.params subjectId, so an edge into it must carry them"
    },
    {
     "to": "GST-003",
     "trigger": "Event & Attraction Listing",
     "carries": [
      "eventId"
     ],
     "provenance": "derived — GST-003 declares entryState.params eventId, so an edge into it must carry them"
    }
   ]
  },
  "notes": "Minuted 10 Aug §4.9. **Group sharing agreed** — an in-app QR a friend scans to join the itinerary (Chinmay raised, Qossai confirmed).",
  "openQuestions": [
   "Inventory cites `POST /itineraries` — no matching operation. Written before the contracts existed."
  ],
  "density": "comfortable",
  "pattern": "listDetail",
  "patternReason": "`listProducts` reads the population and `getCart` reads one of them — list, select, act",
  "purpose": "Choose the attractions and the order yourself.",
  "gaps": [
   {
    "operation": "getWaitTimes",
    "why": "**1 declared operation reach no component on this screen**: getWaitTimes. Either the screen is missing what calls them, or the declaration is residue.",
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
       "label": "Every build your own",
       "bindsTo": "Product",
       "columns": [
        "Product.id",
        "Product.code",
        "Product.name",
        "Product.description",
        "Product.kind",
        "Product.venueId",
        "Product.scopePath",
        "Product.createdByPrincipalId",
        "Product.approvedByPrincipalId",
        "Product.responsibleDepartmentId",
        "Product.onSaleFrom",
        "Product.onSaleTo"
       ],
       "operation": "listProducts",
       "provenance": "contract catalogue.yaml GET /products"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected build your own",
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
       "label": "Add",
       "operation": "addCartLine",
       "provenance": "contract orders.yaml POST /carts/{cartId}/lines"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The build your own list.",
   "error": "Could not load. Names which read failed and leaves the build your own untouched.",
   "emptyFirstRun": "No build your own yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the build your own are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "offline": "**The offline banner shows.** What was already loaded stays on screen, marked with its age. Anything that spends money, holds capacity or changes the account waits for the connection, and its button says so rather than failing."
  },
  "apis": [
   {
    "operationId": "addCartLine",
    "contract": "orders",
    "purpose": "Add something",
    "trigger": "onAction",
    "invalidates": [
     "listProducts"
    ]
   },
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
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "cartId",
     "from": "session"
    }
   ],
   "coldEntry": "Resolves from the session; a cold arrival is the ordinary case.",
   "preloaded": [
    "Cart.id",
    "Cart.token",
    "Cart.venueId",
    "Cart.channel",
    "Cart.subjectId"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P02 Guest App.dc.html#gst-053"
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
  "name": "AI Optimized Itinerary",
  "module": "Engagement & Support",
  "requiresModule": "ai",
  "wave": 3,
  "capability": "AI-35",
  "implementation": {
   "app": "guest-app",
   "route": "/general/ai-optimized-itinerary",
   "component": "apps/guest-app/src/routes/general/AiOptimizedItineraryDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "GST-001",
    "GST-053"
   ],
   "inferred": true,
   "exitTo": [
    "GST-001",
    "GST-002",
    "GST-003",
    "GST-059"
   ],
   "transitions": [
    {
     "to": "GST-059",
     "trigger": "They follow it through the day",
     "provenance": "flow F49 step 4→5",
     "operation": "requestSuggestion"
    },
    {
     "to": "GST-001",
     "trigger": "Home – Default",
     "carries": [
      "subjectId"
     ],
     "provenance": "derived — GST-001 declares entryState.params subjectId, so an edge into it must carry them"
    },
    {
     "to": "GST-003",
     "trigger": "Event & Attraction Listing",
     "carries": [
      "eventId"
     ],
     "provenance": "derived — GST-003 declares entryState.params eventId, so an edge into it must carry them"
    }
   ]
  },
  "notes": "Minuted 10 Aug §4.9. **The AI half is Wave 2** — the manual planner must work without it (CF-41). **Guest concierge confirmed in Phase 1 on 17 August (CF-14), charged per token and bounded by `AiPolicy.guestCapabilityScope`.** Still degrades to the manual planner rather than to an error. ** wired 24 August.** The board drew four bespoke AI endpoints for itinerary planning; **one operation with a kind answers all of them** (ADR-0028), and recording the outcome is what lets a model replace the heuristic later. **`recordSuggestionOutcome` removed from the guest surface.** `check-screens` refused it and was right: **a guest does not record an outcome — the platform observes what they did.** A guest app that self-reports whether it took the advice is a training label the guest could forge, and the observation belongs server-side where the plan and the visit can be compared.",
  "openQuestions": [
   "Inventory cites `POST /ai/itinerary/optimise` — no matching operation. Written before the contracts existed."
  ],
  "density": "comfortable",
  "pattern": "listDetail",
  "patternReason": "`listProducts` reads the population and `getWaitTimes` reads one of them — list, select, act",
  "purpose": "Let the assistant order the day around waits and opening times.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every optimized itinerary",
       "bindsTo": "Product",
       "columns": [
        "Product.id",
        "Product.code",
        "Product.name",
        "Product.description",
        "Product.kind",
        "Product.venueId",
        "Product.scopePath",
        "Product.createdByPrincipalId",
        "Product.approvedByPrincipalId",
        "Product.responsibleDepartmentId",
        "Product.onSaleFrom",
        "Product.onSaleTo"
       ],
       "operation": "listProducts",
       "provenance": "contract catalogue.yaml GET /products"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected optimized itinerary",
       "bindsTo": "WaitTime",
       "columns": [
        "WaitTime.queueId",
        "WaitTime.queueName",
        "WaitTime.attractionProductId",
        "WaitTime.status",
        "WaitTime.waitMinutes",
        "WaitTime.source",
        "WaitTime.isStale",
        "WaitTime.heightRequirementCm",
        "WaitTime.zone",
        "WaitTime.asOf"
       ],
       "operation": "getWaitTimes",
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
       "label": "Send",
       "operation": "sendAiMessage",
       "provenance": "contract ai.yaml POST /conversations/{conversationId}/messages"
      },
      {
       "kind": "secondaryButton",
       "label": "Request",
       "operation": "requestSuggestion",
       "provenance": "contract ai.yaml POST /ai/suggestions"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The optimized itinerary list.",
   "error": "Could not load. Names which read failed and leaves the optimized itinerary untouched.",
   "emptyFirstRun": "No optimized itinerary yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the optimized itinerary are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
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
    "operationId": "sendAiMessage",
    "contract": "ai",
    "purpose": "Ask",
    "trigger": "onAction",
    "invalidates": [
     "listProducts"
    ]
   },
   {
    "operationId": "requestSuggestion",
    "contract": "ai",
    "purpose": "",
    "trigger": "onAction",
    "invalidates": [
     "listProducts"
    ]
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "conversationId",
     "from": "deepLink"
    },
    {
     "name": "suggestionId",
     "from": "deepLink",
     "optional": true
    }
   ],
   "coldEntry": "A conversation link an agent opens from a notification. Resolves, or says it was closed and by whom. A suggestion opened from a saved plan.",
   "preloaded": [
    "WaitTime.queueId",
    "WaitTime.queueName",
    "WaitTime.attractionProductId",
    "WaitTime.status",
    "WaitTime.waitMinutes"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P02 Guest App.dc.html#gst-054"
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
   }
  ],
  "requestBody": "AddCartLineRequest",
  "responds": "Cart"
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
 "getCart": {
  "method": "GET",
  "path": "/carts/{cartId}",
  "contract": "orders",
  "summary": "The cart, priced and checked, right now",
  "permission": null,
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
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
  "summary": "List published bundles",
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
  "responds": "Case"
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
 "raiseMyCase": {
  "method": "POST",
  "path": "/my/cases",
  "contract": "marketing-crm",
  "summary": "Report something — lost property, a complaint, a question",
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
  "responds": "Case"
 },
 "replyToMyCase": {
  "method": "POST",
  "path": "/my/cases/{caseId}/messages",
  "contract": "marketing-crm",
  "summary": "Reply on a case the guest raised",
  "permission": null,
  "offlineCapable": false,
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
  "responds": "Case"
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
   "seatIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "parentLineId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "For an add-on attaching to a ticket already in the cart. **Removing the parent removes the child** — a locker with no admission is not a sale.\n"
   },
   "attributes": {
    "type": "object",
    "additionalProperties": true
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
    "type": "string"
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
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/AiSource"
    }
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
   "localLlm"
  ]
 },
 "AiSource": {
  "type": "object",
  "x-ticvai-persistence": "none — embedded in the interaction",
  "description": "What the answer was grounded in (8.3.70). **An answer with no sources is a guess**, and the interface should show it as one.\n",
  "properties": {
   "kind": {
    "type": "string",
    "enum": [
     "document",
     "product",
     "entitlement",
     "report",
     "record"
    ]
   },
   "id": {
    "type": "string"
   },
   "title": {
    "type": "string"
   },
   "collectionId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "excerpt": {
    "type": "string"
   },
   "relevance": {
    "type": "number"
   }
  }
 },
 "BundleSummary": {
  "x-ticvai-persistence": "none — projection over bundle",
  "type": "object",
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
   "subtotal": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "discountTotal": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "taxTotal": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "total": {
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
     "requiresPrerequisite"
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
    "description": "Most are not. `requiresPrerequisite` is — an add-on with no ticket to attach to cannot be sold.\n"
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
   "seatIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
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
    "format": "uuid",
    "nullable": true,
    "description": "The capacity held for this line. **Null for a product with no capacity** — a t-shirt needs stock, not a lease.\n"
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
    "type": "string"
   },
   "caseNumber": {
    "type": "string"
   },
   "subjectId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "guestName": {
    "type": "string",
    "nullable": true
   },
   "subject": {
    "type": "string"
   },
   "categoryId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
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
    "type": "boolean"
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
    "readOnly": true
   },
   "estimatedWaitSeconds": {
    "type": "integer",
    "nullable": true,
    "readOnly": true
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
  "x-ticvai-persistence": "marketing.conversation_message",
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
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
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
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
   },
   "locationSessionId": {
    "type": "string",
    "nullable": true,
    "description": "Where the order is going. Required for delivery to a table, seat, cabana or named location. Absent for collection, where the outlet is named instead.\n"
   },
   "outletId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Required for collection. Ignored where a table session is supplied."
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
           "type": "string"
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
     "tableService"
    ]
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
    "type": "string"
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
 "ModifierGroup": {
  "x-ticvai-persistence": "fnb.modifier_group + fnb.modifier_option",
  "type": "object",
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
    "type": "string"
   },
   "orderNumber": {
    "type": "string"
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
    "nullable": true
   },
   "subjectId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
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
  "x-ticvai-persistence": "orders.order_line",
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
      "items": {
       "type": "string"
      }
     },
     "crossRegionRightIds": {
      "type": "array",
      "items": {
       "type": "string"
      },
      "description": "Redemption rights propagated to other cells for this line."
     }
    }
   }
  ]
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
    "type": "string"
   },
   "orderId": {
    "type": "string"
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
    "type": "number",
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
    "nullable": true
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
     "configuration"
    ]
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
    "description": "The request body a person would submit, ready to review."
   },
   "summary": {
    "type": "string"
   },
   "status": {
    "type": "string",
    "enum": [
     "proposed",
     "approved",
     "rejected",
     "applied",
     "expired"
    ]
   },
   "approvalLevel": {
    "type": "integer",
    "description": "8.3.65. Multi-level, because a discount and a pricing change differ in authority."
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
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
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
    "description": "Aspect chips — exhibitions, staff, cleanliness, food, value.",
    "items": {
     "type": "string"
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
  "description": "What is being suggested. **A closed set, and the reason it is closed is the swap.** Every entry here is a question a venue asks that a model could answer better than a rule — and each one starts as a heuristic and becomes a model when there is data.\n**Six of these were drawn as their own endpoints on the client F&B boards** — `suggestPrice`, `simulateScenario`, `simulateSlaPolicy`, `suggestRequisition`, `suggestReplenishment`, `publishDemandPlan`. **Building six endpoints means six places to change when a model changes**, and the model will change more often than the venue's question does.\n",
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
   "scenario"
  ]
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
    "description": "The underlying feed has gone quiet past its expected interval. The figure is shown with a caveat rather than frozen and presented as current.\n"
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
    "format": "date-time"
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
