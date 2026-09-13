# P02-membership-loyalty-value-01 — P02 · Membership, Loyalty & Value

**3 screens · 11 operations · 7 schemas · 6 permissions**

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

- **Every control that can be refused must be gated.** 6 permissions apply here:
  `GUEST_MANAGE, GUEST_VIEW, MARKETING_VIEW, ORDER_VIEW, PRICE_VIEW, PRODUCT_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **4 of these operations work offline**: evaluatePromotions, listLoyaltyProgrammes, listProducts, listPromotions
  — and the rest do not. A surface that looks the same online and off is lying.
- **Offline, every screen shows one banner, the same on web and app:** *"You're offline. Connect to the internet to book, pay, order or join a queue."* The moment the connection drops, on every screen, above the screen's own content. By itself as soon as the connection is back, with a short "Back online" confirmation. **It never** Covers what is already on screen, or appears for a server error — that is the screen's own error state, and a guest told they are offline when the venue is down reconnects for nothing. Each screen's `states.offline` says what stays on screen and what waits.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `GST-011` | Wallet Overview | listDetail | 2 | 0 | — |
| `GST-015` | Memberships | listDetail | 5 | 0 | — |
| `GST-036` | Loyalty & Rewards | listDetail | 4 | 0 | — |

## Thin screens in this batch

**GST-011, GST-015, GST-036 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "GST-011",
  "name": "Wallet Overview",
  "module": "Membership, Loyalty & Value",
  "requiresModule": "retail",
  "wave": 2,
  "capability": "C37",
  "implementation": {
   "app": "guest-app",
   "route": "/general/wallet-overview",
   "component": "apps/guest-app/src/routes/general/WalletOverviewDashboard.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "GST-001",
    "GST-037"
   ],
   "inferred": true,
   "exitTo": [
    "GST-001",
    "GST-002",
    "GST-003",
    "GST-020"
   ],
   "transitions": [
    {
     "to": "GST-020",
     "trigger": "Saved items carry across sessions",
     "provenance": "flow F53 step 4→5"
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
  "notes": "States derived from the screen pattern on 17 August, not individually considered. Purpose derived from the screen name and its operations on 17 August, not from a requirement.",
  "openQuestions": [
   "Inventory cites `GET /wallet` — no matching operation. Written before the contracts existed."
  ],
  "density": "comfortable",
  "pattern": "listDetail",
  "patternReason": "`listWalletTransactions` reads the population and `getWallet` reads one of them — list, select, act",
  "purpose": "The screen this app sits on. Everything else is entered from here and returns to it.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every wallet overview",
       "bindsTo": "WalletTransaction",
       "columns": [
        "WalletTransaction.id",
        "WalletTransaction.kind",
        "WalletTransaction.amount",
        "WalletTransaction.balanceAfter",
        "WalletTransaction.orderId",
        "WalletTransaction.venueId",
        "WalletTransaction.reason",
        "WalletTransaction.principalId",
        "WalletTransaction.recordedAt"
       ],
       "operation": "listWalletTransactions",
       "provenance": "contract retail.yaml GET /wallets/{subjectId}/transactions"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected wallet overview",
       "bindsTo": "Wallet",
       "columns": [
        "Wallet.id",
        "Wallet.subjectId",
        "Wallet.balance",
        "Wallet.credits",
        "Wallet.bonusBalance",
        "Wallet.currency",
        "Wallet.status",
        "Wallet.homeCellName",
        "Wallet.expiresAt",
        "Wallet.lastActivityAt"
       ],
       "operation": "getWallet",
       "provenance": "contract retail.yaml GET /wallets/{subjectId}"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The wallet overview list.",
   "error": "Could not load. Names which read failed and leaves the wallet overview untouched.",
   "emptyFirstRun": "No wallet overview yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the wallet overview are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "offline": "**The offline banner shows.** Balances and stored cards already loaded stay visible with their age, cards masked. Storing a card and transferring value need the server."
  },
  "apis": [
   {
    "operationId": "getWallet",
    "contract": "retail",
    "purpose": "Read a guest wallet",
    "trigger": "onLoad"
   },
   {
    "operationId": "listWalletTransactions",
    "contract": "retail",
    "purpose": "Wallet transaction history",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "subjectId",
     "from": "GST-001"
    }
   ],
   "coldEntry": "Resolves from the session; a cold arrival is the ordinary case.",
   "preloaded": [
    "Wallet.id",
    "Wallet.subjectId",
    "Wallet.balance",
    "Wallet.credits",
    "Wallet.bonusBalance"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P02 Guest App.dc.html#gst-011"
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
  "id": "GST-015",
  "name": "Memberships",
  "module": "Membership, Loyalty & Value",
  "requiresModule": "ticketing",
  "wave": 2,
  "capability": "C03",
  "implementation": {
   "app": "guest-app",
   "route": "/general/memberships",
   "component": "apps/guest-app/src/routes/general/MembershipsDetail.tsx",
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
    },
    {
     "to": "ADM-003",
     "trigger": "The right is propagated to the other cell",
     "provenance": "flow F19 step 1→2",
     "crossesDevice": true,
     "back": false
    }
   ]
  },
  "notes": "States derived from the screen pattern on 17 August, not individually considered. Purpose derived from the screen name and its operations on 17 August, not from a requirement. Membership. **`listDelegations` and `grantDelegation` are the member list and add-member** Pranay asked for — CF-132 built them as delegated authority rather than a household table. **Rewired on the 20 August review.** **`getGuestLink` restored** — F19 step 1 calls it from here and my rewire dropped it. **A membership that works in another country resolves through the guest link**, and the flow checker caught what the screen edit did not. **Cross-platform navigation removed 24 August**: ADM-003. **A till does not navigate to a back office and a guest app does not navigate to either** — those are device handovers, and a flow declares them with `crossesDevice` rather than a screen pretending there is a link. **Wired 24 August from review**: getSubscription, listSubscriptionInvoices. **The operations existed and this screen could not call them** — reviewers reported them as missing APIs, which is what an unreachable operation looks like from a wireframe. **`getSubscription` and `listSubscriptionInvoices` removed the same day they were wired.** `check-screens` refused them: **both carry a staff permission and this is a guest surface.** The reviewer asked for `GET /memberships/current` — a guest-scoped read that does not exist. **That is the correct finding and the wiring was the wrong fix**: it is a new operation, not a missing link. **`getGuestLink` is `service` audience** — a cross-region pseudonymous lookup (ADR-0010), not something a membership screen calls. Removed 24 August. **`getMyMemberships` and `listGuestMemberships` wired 24 August**, replacing `getGuestLink`. A guest reading their own membership calls a guest operation; **`getGuestLink` is the cross-region pseudonymous lookup a service makes on their behalf** (ADR-0010), and F19 was walking it from a guest screen.",
  "openQuestions": [
   "Inventory cites `GET /memberships` — no matching operation. Written before the contracts existed."
  ],
  "density": "comfortable",
  "pattern": "listDetail",
  "patternReason": "`listDelegations` reads the population and `getMyMemberships` reads one of them — list, select, act",
  "purpose": "Find memberships for this venue.",
  "gaps": [
   {
    "operation": "listProducts",
    "why": "**2 declared operations reach no component on this screen**: listProducts, listGuestMemberships. Either the screen is missing what calls them, or the declaration is residue.",
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
       "label": "Every memberships",
       "bindsTo": "DelegatedAccess",
       "columns": [
        "DelegatedAccess.id",
        "DelegatedAccess.principalId",
        "DelegatedAccess.roleId",
        "DelegatedAccess.permission",
        "DelegatedAccess.subjectId",
        "DelegatedAccess.overSubjectId",
        "DelegatedAccess.overObjectRef",
        "DelegatedAccess.delegationKind",
        "DelegatedAccess.quota",
        "DelegatedAccess.isRevocableBySubject",
        "DelegatedAccess.scopePath",
        "DelegatedAccess.effect"
       ],
       "operation": "listDelegations",
       "provenance": "contract identity.yaml GET /guests/{subjectId}/delegations"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected memberships",
       "bindsTo": "GuestMembership",
       "columns": [
        "GuestMembership.entitlementId",
        "GuestMembership.productId",
        "GuestMembership.name",
        "GuestMembership.tier",
        "GuestMembership.status",
        "GuestMembership.validFrom",
        "GuestMembership.validTo",
        "GuestMembership.frozenDays",
        "GuestMembership.benefits",
        "GuestMembership.renewsOn",
        "GuestMembership.previousTerms"
       ],
       "operation": "getMyMemberships",
       "provenance": "contract catalogue.yaml GET /guests/me/memberships"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Grant",
       "operation": "grantDelegation",
       "provenance": "contract identity.yaml POST /guests/{subjectId}/delegations"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The memberships list.",
   "error": "Could not load. Names which read failed and leaves the memberships untouched.",
   "emptyFirstRun": "No memberships yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the memberships are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "offline": "**The offline banner shows.** What was already loaded stays on screen, marked with its age. Anything that spends money, holds capacity or changes the account waits for the connection, and its button says so rather than failing."
  },
  "apis": [
   {
    "operationId": "getMyMemberships",
    "contract": "catalogue",
    "purpose": "A guest's own memberships, benefits and history",
    "trigger": "onLoad"
   },
   {
    "operationId": "listDelegations",
    "contract": "identity",
    "purpose": "Who may act for this guest, and for whom they may act",
    "trigger": "onLoad"
   },
   {
    "operationId": "grantDelegation",
    "contract": "identity",
    "purpose": "Let one guest act for another",
    "trigger": "onAction",
    "invalidates": [
     "listDelegations"
    ]
   },
   {
    "operationId": "listProducts",
    "contract": "catalogue",
    "purpose": "List products",
    "trigger": "onLoad"
   },
   {
    "operationId": "listGuestMemberships",
    "contract": "catalogue",
    "purpose": "A guest's memberships, benefits and history",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "guestLinkId",
     "from": "deepLink"
    },
    {
     "name": "subjectId",
     "from": "GST-001"
    }
   ],
   "coldEntry": "**A guest arriving cold on a link that no longer resolves is shown what happened and one way onward — never a 404.** A shared ticket, a forwarded confirmation and a push notification opened three weeks late all land here, and the person holding the link did nothing wrong. **The screen names the thing, says it is expired, cancelled or withdrawn, and offers the list it came from.** Arrives with `guestLinkId`.",
   "preloaded": [
    "GuestMembership.entitlementId",
    "GuestMembership.productId",
    "GuestMembership.name",
    "GuestMembership.tier",
    "GuestMembership.status"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P02 Guest App.dc.html#gst-015"
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
  "id": "GST-036",
  "name": "Loyalty & Rewards",
  "module": "Membership, Loyalty & Value",
  "requiresModule": "marketing",
  "wave": 2,
  "capability": "C64",
  "implementation": {
   "app": "guest-app",
   "route": "/loyalty-rewards",
   "component": "apps/guest-app/src/routes/LoyaltyRewards.tsx",
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
     "to": "WEB-024",
     "trigger": "They see rewards and manage their devices",
     "provenance": "flow F53 step 1→2",
     "crossesDevice": true,
     "back": false
    }
   ]
  },
  "notes": "Merged with GST-064 on 18 August. **I created GST-064 in the parity sweep without noticing this screen existed** — same two operations, same capability, and the fuzzy match against the client storyboard is what surfaced it. Board 6 panel 6 shows one Loyalty & Rewards screen, not two. **Cross-surface parity, 31 August**: added evaluatePromotions, listPromotions. **The same screen on web and app was calling different operations** — one side could do something the other could not, and nothing recorded the difference as deliberate.",
  "openQuestions": [
   "Inventory cites `GET /loyalty` — no matching operation. Written before the contracts existed."
  ],
  "density": "comfortable",
  "pattern": "listDetail",
  "patternReason": "`listLoyaltyProgrammes` reads the population and `getLoyaltyPosition` reads one of them — list, select, act",
  "purpose": "Your points, your tier, and what is within reach.",
  "gaps": [
   {
    "operation": "getLoyaltyPosition",
    "why": "**2 declared operations reach no component on this screen**: getLoyaltyPosition, listPromotions. Either the screen is missing what calls them, or the declaration is residue.",
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
       "label": "Every loyalty rewards",
       "bindsTo": "LoyaltyProgramme",
       "columns": [
        "LoyaltyProgramme.id",
        "LoyaltyProgramme.code",
        "LoyaltyProgramme.name",
        "LoyaltyProgramme.venueId",
        "LoyaltyProgramme.pointsLiabilityAccountId",
        "LoyaltyProgramme.earnRules",
        "LoyaltyProgramme.tiers",
        "LoyaltyProgramme.pointsExpireAfterMonths",
        "LoyaltyProgramme.isActive"
       ],
       "operation": "listLoyaltyProgrammes",
       "provenance": "contract marketing-crm.yaml GET /loyalty/programmes"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Evaluate",
       "operation": "evaluatePromotions",
       "provenance": "contract promotions.yaml POST /promotions/evaluate"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The loyalty rewards list.",
   "error": "Could not load. Names which read failed and leaves the loyalty rewards untouched.",
   "emptyFirstRun": "No loyalty rewards yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the loyalty rewards are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "offline": "**The offline banner shows.** The last known balance stays with its age, and **points earned since are not shown** — and that is said. Redeeming and referring need the connection."
  },
  "apis": [
   {
    "operationId": "getLoyaltyPosition",
    "contract": "marketing-crm",
    "purpose": "A guest's points, tier and what is within reach",
    "trigger": "onLoad"
   },
   {
    "operationId": "listLoyaltyProgrammes",
    "contract": "marketing-crm",
    "purpose": "List loyalty programmes",
    "trigger": "onLoad"
   },
   {
    "operationId": "evaluatePromotions",
    "contract": "promotions",
    "purpose": "Evaluate promotions against a cart",
    "trigger": "onAction",
    "invalidates": [
     "listLoyaltyProgrammes"
    ]
   },
   {
    "operationId": "listPromotions",
    "contract": "promotions",
    "purpose": "List promotions",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P02 Guest App.dc.html#gst-036"
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
 "evaluatePromotions": {
  "method": "POST",
  "path": "/promotions/evaluate",
  "contract": "promotions",
  "summary": "Evaluate promotions against a cart",
  "permission": "PRICE_VIEW",
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
  "requestBody": "EvaluatePromotionsRequest",
  "responds": "PromotionEvaluation"
 },
 "getLoyaltyPosition": {
  "method": "GET",
  "path": "/loyalty/position",
  "contract": "marketing-crm",
  "summary": "A guest's points, tier and what is within reach",
  "permission": null,
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [],
  "requestBody": null,
  "responds": null
 },
 "getMyMemberships": {
  "method": "GET",
  "path": "/guests/me/memberships",
  "contract": "catalogue",
  "summary": "A guest's own memberships, benefits and history",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "includeLapsed",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "GuestMembership"
 },
 "getWallet": {
  "method": "GET",
  "path": "/wallets/{subjectId}",
  "contract": "retail",
  "summary": "Read a guest wallet",
  "permission": "ORDER_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "Wallet"
 },
 "grantDelegation": {
  "method": "POST",
  "path": "/guests/{subjectId}/delegations",
  "contract": "identity",
  "summary": "Let one guest act for another",
  "permission": "GUEST_MANAGE",
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
  "responds": "DelegatedAccess"
 },
 "listDelegations": {
  "method": "GET",
  "path": "/guests/{subjectId}/delegations",
  "contract": "identity",
  "summary": "Who may act for this guest, and for whom they may act",
  "permission": "GUEST_VIEW",
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
  "requestBody": null,
  "responds": null
 },
 "listGuestMemberships": {
  "method": "GET",
  "path": "/guest/memberships",
  "contract": "catalogue",
  "summary": "A guest's memberships, benefits and history",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "includeLapsed",
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
  "responds": "GuestMembership"
 },
 "listLoyaltyProgrammes": {
  "method": "GET",
  "path": "/loyalty/programmes",
  "contract": "marketing-crm",
  "summary": "List loyalty programmes",
  "permission": "MARKETING_VIEW",
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
  "responds": "LoyaltyProgramme"
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
 "listPromotions": {
  "method": "GET",
  "path": "/promotions",
  "contract": "promotions",
  "summary": "List promotions",
  "permission": "PRICE_VIEW",
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
    "name": "status",
    "in": "query",
    "required": null
   },
   {
    "name": "activeAt",
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
 "listWalletTransactions": {
  "method": "GET",
  "path": "/wallets/{subjectId}/transactions",
  "contract": "retail",
  "summary": "Wallet transaction history",
  "permission": "ORDER_VIEW",
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
  "requestBody": null,
  "responds": "Page"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "DelegatedAccess": {
  "x-ticvai-persistence": "identity.delegated_access",
  "type": "object",
  "required": [
   "id",
   "permission",
   "scopePath",
   "effect"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "principalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "roleId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "permission": {
    "type": "string",
    "description": "From the permission enum. `*` permitted on DENY only."
   },
   "subjectId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "CF-132, CL-05. **A grant held by a guest rather than a staff principal.**\nSection 5.5 asks for portfolios — a primary holder assigning entitlements, transfer between linked accounts, shared wallets with individual tracking — and it appears ten times across ten sections. **Every one of those reduces to the same question: who may act on whose behalf, over what, and until when.**\n**That is a grant, not a household table.** A primary holder assigning an entitlement is a grant. A group leader holding tickets for twelve is a grant. A corporate account enrolling members is a grant with a quota. **A shared wallet with individual tracking is a grant over a balance, and the transaction log already records who spent.**\n**A household table would answer one of those four.**\n"
   },
   "overSubjectId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Whose behalf. **Null for a staff grant, which is the existing behaviour** — every grant written before 18 August means exactly what it meant before.\n"
   },
   "overObjectRef": {
    "type": "string",
    "nullable": true,
    "description": "**Where the authority is over a thing rather than a scope** — a wallet, an entitlement, a booking. `scopePath` answers *where*; this answers *what*, and a guest's authority is almost always over a specific object rather than a branch of the tree.\n"
   },
   "delegationKind": {
    "type": "string",
    "nullable": true,
    "enum": [
     "primaryHolder",
     "familyMember",
     "groupLeader",
     "attendee",
     "corporateAdmin",
     "corporateMember",
     "carer"
    ],
    "description": "**What kind of relationship this expresses**, for display and for reporting. The mechanism does not branch on it — a family member and a group attendee are the same grant with different words around them, which is the point.\n"
   },
   "quota": {
    "type": "integer",
    "nullable": true,
    "description": "2.14.15 and 4.3.11. **How many the holder may assign.** A corporate account with fifty allocations and a family with four are the same structure with different numbers.\n"
   },
   "isRevocableBySubject": {
    "type": "boolean",
    "default": true,
    "description": "**Whether the person it is over can end it.** A guest who linked a family member should be able to unlink them; a corporate member should not be able to revoke their employer's oversight — and **a delegation nobody can end is a delegation somebody will regret.**\n"
   },
   "scopePath": {
    "type": "string"
   },
   "effect": {
    "type": "string",
    "enum": [
     "ALLOW",
     "DENY"
    ]
   },
   "validFrom": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "validTo": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "createdByPrincipalId": {
    "type": "string",
    "format": "uuid"
   },
   "createdAt": {
    "type": "string",
    "format": "date-time"
   }
  }
 },
 "EvaluatePromotionsRequest": {
  "x-ticvai-persistence": "none — request only",
  "type": "object",
  "required": [
   "venueId",
   "channel",
   "lines"
  ],
  "properties": {
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "channel": {
    "type": "string"
   },
   "subjectId": {
    "type": "string",
    "format": "uuid"
   },
   "membershipTierId": {
    "type": "string",
    "format": "uuid"
   },
   "couponCodes": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "evaluateAt": {
    "type": "string",
    "format": "date-time",
    "description": "For back-office testing of a rule before publishing."
   },
   "lines": {
    "type": "array",
    "minItems": 1,
    "items": {
     "type": "object",
     "required": [
      "lineId",
      "variantId",
      "quantity",
      "unitPrice"
     ],
     "properties": {
      "lineId": {
       "type": "string"
      },
      "variantId": {
       "type": "string",
       "format": "uuid"
      },
      "performanceId": {
       "type": "string",
       "format": "uuid"
      },
      "quantity": {
       "type": "integer",
       "minimum": 1
      },
      "unitPrice": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      }
     }
    }
   }
  }
 },
 "GuestMembership": {
  "type": "object",
  "description": "19.2.26 to 19.2.28. **A view, not a table** — assembled from the entitlement, the product that granted it and the order that bought it.\n",
  "required": [
   "entitlementId",
   "productId",
   "name",
   "status"
  ],
  "properties": {
   "entitlementId": {
    "type": "string",
    "format": "uuid"
   },
   "productId": {
    "type": "string",
    "format": "uuid"
   },
   "name": {
    "type": "string"
   },
   "tier": {
    "type": "string",
    "nullable": true
   },
   "status": {
    "type": "string",
    "enum": [
     "active",
     "frozen",
     "suspended",
     "expired",
     "cancelled"
    ],
    "description": "**Derived from the entitlement, not held here.** This schema is a view assembled from the entitlement, the product that granted it and the order that bought it — the lifecycle lives in `states/entitlement-status.yaml` and `frozen` is what `freezeEntitlement` sets.\nNo state model of its own, deliberately: **two models over one lifecycle drift.**\n"
   },
   "validFrom": {
    "type": "string",
    "format": "date"
   },
   "validTo": {
    "type": "string",
    "format": "date"
   },
   "frozenDays": {
    "type": "integer",
    "description": "Days lost to a freeze and added back to `validTo`. **Shown because a guest who paused a pass will check the maths**, and a validity date that moved without explanation is a support call.\n"
   },
   "benefits": {
    "type": "array",
    "description": "5.4.31. From the product's entitlement template. **Traceable to what grants them**, so a gate can honour what the app promised.\n",
    "items": {
     "type": "object",
     "properties": {
      "code": {
       "type": "string"
      },
      "name": {
       "type": "string"
      },
      "value": {
       "type": "string",
       "nullable": true
      }
     }
    }
   },
   "renewsOn": {
    "type": "string",
    "format": "date",
    "nullable": true
   },
   "previousTerms": {
    "type": "array",
    "description": "Prior terms, including lapsed ones.",
    "items": {
     "type": "object",
     "properties": {
      "validFrom": {
       "type": "string",
       "format": "date"
      },
      "validTo": {
       "type": "string",
       "format": "date"
      },
      "endedBecause": {
       "type": "string",
       "enum": [
        "expired",
        "renewed",
        "cancelled",
        "upgraded"
       ]
      }
     }
    }
   }
  }
 },
 "LoyaltyProgramme": {
  "x-ticvai-persistence": "marketing.loyalty_programme + marketing.loyalty_tier",
  "type": "object",
  "required": [
   "id",
   "code",
   "name",
   "earnRules",
   "tiers"
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
   "venueId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "pointsLiabilityAccountId": {
    "type": "string",
    "format": "uuid",
    "description": "Points post here on accrual. They are a liability from the moment they are earned, not from the moment they are spent.\n"
   },
   "earnRules": {
    "type": "array",
    "items": {
     "type": "object",
     "required": [
      "trigger",
      "points"
     ],
     "properties": {
      "trigger": {
       "type": "string",
       "enum": [
        "perCurrencyUnit",
        "perVisit",
        "perProduct",
        "onSignup",
        "onBirthday",
        "onReview"
       ]
      },
      "points": {
       "type": "number"
      },
      "productKinds": {
       "type": "array",
       "items": {
        "type": "string"
       }
      },
      "multiplier": {
       "type": "number"
      }
     }
    }
   },
   "tiers": {
    "type": "array",
    "items": {
     "type": "object",
     "required": [
      "code",
      "name",
      "thresholdPoints"
     ],
     "properties": {
      "code": {
       "type": "string"
      },
      "name": {
       "type": "string"
      },
      "thresholdPoints": {
       "type": "integer"
      },
      "benefits": {
       "type": "array",
       "items": {
        "type": "string"
       }
      },
      "earnMultiplier": {
       "type": "number"
      }
     }
    }
   },
   "pointsExpireAfterMonths": {
    "type": "integer",
    "nullable": true
   },
   "isActive": {
    "type": "boolean"
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
 "PromotionEvaluation": {
  "x-ticvai-persistence": "none — computed",
  "parameters": [
   {
    "$ref": "../shared/common.yaml#/components/parameters/IdempotencyKey"
   }
  ],
  "type": "object",
  "required": [
   "totalDiscount",
   "lines",
   "applied",
   "rejected"
  ],
  "properties": {
   "totalDiscount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "lines": {
    "type": "array",
    "items": {
     "type": "object",
     "required": [
      "lineId",
      "originalPrice",
      "discountedPrice",
      "discount"
     ],
     "properties": {
      "lineId": {
       "type": "string"
      },
      "originalPrice": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      },
      "discountedPrice": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      },
      "discount": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      },
      "appliedPromotionIds": {
       "type": "array",
       "items": {
        "type": "string",
        "format": "uuid"
       }
      }
     }
    }
   },
   "applied": {
    "type": "array",
    "items": {
     "type": "object",
     "required": [
      "promotionId",
      "promotionCode",
      "discount"
     ],
     "properties": {
      "promotionId": {
       "type": "string",
       "format": "uuid"
      },
      "promotionCode": {
       "type": "string"
      },
      "promotionName": {
       "type": "string"
      },
      "discount": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      },
      "couponCode": {
       "type": "string",
       "nullable": true
      }
     }
    }
   },
   "rejected": {
    "type": "array",
    "description": "Promotions that matched the products but did not apply, with the reason. This is what a cashier reads to a guest who expected a discount.\n",
    "items": {
     "type": "object",
     "required": [
      "promotionCode",
      "reason"
     ],
     "properties": {
      "promotionCode": {
       "type": "string"
      },
      "promotionName": {
       "type": "string"
      },
      "reason": {
       "type": "string",
       "enum": [
        "conditionsNotMet",
        "supersededByBetterOffer",
        "exclusivePromotionApplied",
        "redemptionLimitReached",
        "budgetExhausted",
        "outsideValidPeriod",
        "wrongChannel",
        "membershipRequired",
        "couponRequired"
       ]
      },
      "detail": {
       "type": "string"
      }
     }
    }
   }
  }
 },
 "Wallet": {
  "x-ticvai-persistence": "retail.wallet",
  "type": "object",
  "required": [
   "subjectId",
   "balance",
   "currency",
   "status"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "description": "**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"
   },
   "subjectId": {
    "type": "string",
    "format": "uuid"
   },
   "balance": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "credits": {
    "type": "array",
    "description": "4.3.5 and 4.3.19. **One balance and one bonus balance with one expiry could not express what the requirement asks for** — cash, bonus and redemption credit, each with its own expiry.\n**The expiries are the reason this is a list.** Cash a guest paid for should outlive a promotional credit they were given, and a single `expiresAt` either expires the money they paid or never expires the promotion.\n**Consumed first-expiry-first-out across all three** (4.3.19), which is also the order that is fairest to the guest — spend what is about to die before what is not.\n",
    "items": {
     "type": "object",
     "required": [
      "kind",
      "amount"
     ],
     "properties": {
      "kind": {
       "type": "string",
       "enum": [
        "cash",
        "bonus",
        "redemption",
        "refund",
        "goodwill"
       ],
       "description": "**`cash` is money the guest paid and the others are not.** That distinction decides what is refundable, what expires, and what shows as a liability.\n"
      },
      "amount": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      },
      "expiresAt": {
       "type": "string",
       "format": "date-time",
       "nullable": true
      },
      "sourceRef": {
       "type": "string",
       "nullable": true
      },
      "isRefundable": {
       "type": "boolean",
       "default": false,
       "description": "**True only for `cash`.** A guest cannot cash out a promotional credit, and a wallet that lets them has given away the promotion twice.\n"
      }
     }
    }
   },
   "bonusBalance": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "description": "Promotional value. Typically non-refundable and spent first."
   },
   "currency": {
    "type": "string",
    "pattern": "^[A-Z]{3}$"
   },
   "status": {
    "type": "string",
    "enum": [
     "active",
     "suspended",
     "closed"
    ]
   },
   "homeCellName": {
    "type": "string",
    "nullable": true,
    "description": "Where the authoritative balance lives. Present when the guest is linked across cells.\n"
   },
   "expiresAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "lastActivityAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   }
  }
 }
}
```
