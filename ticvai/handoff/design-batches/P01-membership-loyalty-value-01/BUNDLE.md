# P01-membership-loyalty-value-01 — P01 · Membership, Loyalty & Value

**5 screens · 33 operations · 25 schemas · 11 permissions**

Platform P01 Guest Web · ships as **guest** ·
guest audience · web ·
online only

## What to build

**A working surface, not a drawing of one.** The reference is `sources/designs/TICVAI_POS_Terminal_client_approved.html` — a Claude Design
build from these same sources, and the one the client responded to. Open it and match its depth:
real state, seeded data, controls that do something. Do not describe it, read it.

## What is in this folder

| file | what it is |
|---|---|
| `screens.json` | Every field of every screen in the batch. `machine` is what a screen is *in the middle of*; `overlays` is what opens over it and what closing it does; `navigation.transitions` is how you leave, with `carries` naming the state that travels. |
| `operations.json` | Method, path, parameters, request and response schema for every operation these screens call. Write fetches against these; do not invent endpoints. |
| `schemas.json` | The data those operations carry, resolved one level deep. **Seed from these.** The prototype hardcodes 57 models and every one corresponds to a schema here — a build that invents its own will disagree with the backend on day one. |

## Rules that are not style preferences

- **Every control that can be refused must be gated.** 11 permissions apply here:
  `GUEST_MANAGE, GUEST_VIEW, GUEST_VIEW_PII, LOYALTY_REDEEM, MARKETING_MANAGE, MARKETING_VIEW, ORDER_CREATE, ORDER_MODIFY, ORDER_VIEW, PRICE_VIEW, PRODUCT_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **7 of these operations work offline**: evaluatePromotions, getGameCard, getProduct, getWaiverStatus, listLoyaltyProgrammes, listProducts, listPromotions
  — and the rest do not. A surface that looks the same online and off is lying.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `WEB-021` | Wallet & Gift Cards | listDetail | 7 | 0 | — |
| `WEB-022` | Membership Plans | listDetail | 4 | 0 | — |
| `WEB-023` | Membership Management | listDetail | 3 | 0 | — |
| `WEB-024` | Devices, Wishlist & Consent | listDetail | 15 | 2 | — |
| `WEB-043` | Loyalty & Rewards | listDetail | 6 | 0 | — |

## Thin screens in this batch

**WEB-021, WEB-022, WEB-023 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "WEB-021",
  "name": "Wallet & Gift Cards",
  "module": "Membership, Loyalty & Value",
  "requiresModule": "retail",
  "wave": 2,
  "capability": "C21",
  "implementation": {
   "app": "guest-web",
   "route": "/membership-loyalty-and-value/wallet-and-gift-cards",
   "component": "apps/guest-web/src/routes/membership-loyalty-and-value/WalletAndGiftCardsDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "WEB-001"
   ],
   "exitTo": [
    "WEB-001",
    "WEB-022",
    "WEB-023",
    "WEB-024"
   ],
   "inferred": true,
   "transitions": [
    {
     "to": "WEB-022",
     "trigger": "Membership Plans",
     "carries": [
      "productId"
     ],
     "provenance": "derived — WEB-022 declares entryState.params productId, so an edge into it must carry them"
    },
    {
     "to": "WEB-023",
     "trigger": "Membership Management",
     "carries": [
      "orderId"
     ],
     "provenance": "derived — WEB-023 declares entryState.params orderId, so an edge into it must carry them"
    },
    {
     "to": "WEB-024",
     "trigger": "Devices, Wishlist & Consent",
     "carries": [
      "deviceId",
      "itemId",
      "subjectId"
     ],
     "provenance": "derived — WEB-024 declares entryState.params deviceId, itemId, subjectId, so an edge into it must carry them"
    }
   ]
  },
  "notes": "Purpose derived from the screen name and its operations on 17 August, not from a requirement.",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listWalletTransactions` reads the population and `getWallet` reads one of them — list, select, act",
  "purpose": "See wallet & gift cards for this venue.",
  "gaps": [
   {
    "operation": "getGiftCard",
    "why": "**1 declared operation reach no component on this screen**: getGiftCard. Either the screen is missing what calls them, or the declaration is residue.",
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
       "label": "Every wallet gift cards",
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
       "label": "The selected wallet gift cards",
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
    },
    {
     "name": "contentBody",
     "slot": "carried",
     "components": [
      {
       "kind": "dataTable",
       "derived": true,
       "impliedBy": "listWalletTransactions",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The wallet gift cards list.",
   "error": "Could not load. Names which read failed and leaves the wallet gift cards untouched.",
   "emptyFirstRun": "No wallet gift cards yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the wallet gift cards are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
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
   },
   {
    "operationId": "getGiftCard",
    "contract": "retail",
    "purpose": "Check a gift card balance",
    "trigger": "onLoad"
   },
   {
    "operationId": "getGameCard",
    "contract": "games",
    "purpose": "Balance on a game card",
    "trigger": "onLoad"
   },
   {
    "operationId": "listPaymentTokens",
    "contract": "orders",
    "purpose": "Saved cards on this account",
    "trigger": "onLoad"
   },
   {
    "operationId": "storePaymentToken",
    "contract": "orders",
    "purpose": "Save a card for next time",
    "trigger": "onAction"
   },
   {
    "operationId": "transferWalletBalance",
    "contract": "retail",
    "purpose": "Move value between wallets",
    "trigger": "onAction"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "cardCode",
     "from": "deepLink"
    },
    {
     "name": "subjectId",
     "from": "session"
    },
    {
     "name": "walletId",
     "from": "navigation"
    }
   ],
   "coldEntry": "**A guest arriving cold on a link that no longer resolves is shown what happened and one way onward — never a 404.** A shared ticket, a forwarded confirmation and a push notification opened three weeks late all land here, and the person holding the link did nothing wrong. **The screen names the thing, says it is expired, cancelled or withdrawn, and offers the list it came from.** Arrives with `cardCode`.",
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
   "board": "wireframes/P01 Guest Web.dc.html#web-021"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 3 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "_platform": {
   "code": "P01",
   "audience": "guest",
   "formFactor": "web",
   "shortName": "Guest Web",
   "name": "Guest Web — Storefront",
   "offlineCapable": false,
   "app": "guest-web",
   "operator": "guest",
   "targetApp": {
    "app": "guest",
    "name": "TICVAI Guest",
    "shell": "web",
    "siblings": [
     "P02",
     "P05"
    ],
    "note": "**One guest product in three shells.** Web, mobile and kiosk share 73–91% of their operations; the kiosk is the same product in a fixed frame with no keyboard, and is deliberately narrower rather than different.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "WEB-022",
  "name": "Membership Plans",
  "module": "Membership, Loyalty & Value",
  "requiresModule": "ticketing",
  "wave": 2,
  "capability": "C31",
  "implementation": {
   "app": "guest-web",
   "route": "/membership-loyalty-and-value/membership-plans",
   "component": "apps/guest-web/src/routes/membership-loyalty-and-value/MembershipPlansDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "WEB-001"
   ],
   "exitTo": [
    "WEB-001",
    "WEB-021",
    "WEB-023",
    "WEB-024"
   ],
   "inferred": true,
   "transitions": [
    {
     "to": "WEB-021",
     "trigger": "Wallet & Gift Cards",
     "carries": [
      "cardCode",
      "subjectId"
     ],
     "provenance": "derived — WEB-021 declares entryState.params cardCode, subjectId, so an edge into it must carry them"
    },
    {
     "to": "WEB-023",
     "trigger": "Membership Management",
     "carries": [
      "orderId"
     ],
     "provenance": "derived — WEB-023 declares entryState.params orderId, so an edge into it must carry them"
    },
    {
     "to": "WEB-024",
     "trigger": "Devices, Wishlist & Consent",
     "carries": [
      "deviceId",
      "itemId",
      "subjectId"
     ],
     "provenance": "derived — WEB-024 declares entryState.params deviceId, itemId, subjectId, so an edge into it must carry them"
    }
   ]
  },
  "notes": "Purpose derived from the screen name and its operations on 17 August, not from a requirement. **Wired 24 August**: getMyMemberships, listGuestMemberships. **The web surface drew the screen and could not fetch what it shows** — the app had these and the browser did not, and there is no reason a membership or a bundle should need an app.",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listProducts` reads the population and `getProduct` reads one of them — list, select, act",
  "purpose": "Membership Plans — the screen a person opens when they need to deal with membership plans.",
  "gaps": [
   {
    "operation": "getMyMemberships",
    "why": "**2 declared operations reach no component on this screen**: getMyMemberships, listGuestMemberships. Either the screen is missing what calls them, or the declaration is residue.",
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
       "label": "Every membership plans",
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
       "label": "The selected membership plans",
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
       "operation": "getProduct",
       "provenance": "contract catalogue.yaml GET /products/{productId}"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "carried",
     "components": [
      {
       "kind": "dataTable",
       "derived": true,
       "impliedBy": "listProducts",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The membership plans list.",
   "error": "Could not load. Names which read failed and leaves the membership plans untouched.",
   "emptyFirstRun": "No membership plans yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the membership plans are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listProducts",
    "contract": "catalogue",
    "purpose": "List products",
    "trigger": "onLoad"
   },
   {
    "operationId": "getProduct",
    "contract": "catalogue",
    "purpose": "Read a product",
    "trigger": "onLoad"
   },
   {
    "operationId": "getMyMemberships",
    "contract": "catalogue",
    "purpose": "A guest's own memberships, benefits and history",
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
     "name": "productId",
     "from": "WEB-001"
    }
   ],
   "coldEntry": "Resolves from the session; a cold arrival is the ordinary case.",
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
   "board": "wireframes/P01 Guest Web.dc.html#web-022"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 4 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "_platform": {
   "code": "P01",
   "audience": "guest",
   "formFactor": "web",
   "shortName": "Guest Web",
   "name": "Guest Web — Storefront",
   "offlineCapable": false,
   "app": "guest-web",
   "operator": "guest",
   "targetApp": {
    "app": "guest",
    "name": "TICVAI Guest",
    "shell": "web",
    "siblings": [
     "P02",
     "P05"
    ],
    "note": "**One guest product in three shells.** Web, mobile and kiosk share 73–91% of their operations; the kiosk is the same product in a fixed frame with no keyboard, and is deliberately narrower rather than different.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "WEB-023",
  "name": "Membership Management",
  "module": "Membership, Loyalty & Value",
  "requiresModule": "ticketing",
  "wave": 2,
  "capability": "C31",
  "implementation": {
   "app": "guest-web",
   "route": "/membership-loyalty-and-value/membership-management",
   "component": "apps/guest-web/src/routes/membership-loyalty-and-value/MembershipManagementForm.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "WEB-001"
   ],
   "inferred": true,
   "exitTo": [
    "WEB-001",
    "WEB-021",
    "WEB-022",
    "WEB-024"
   ],
   "transitions": [
    {
     "to": "WEB-021",
     "trigger": "Wallet & Gift Cards",
     "carries": [
      "cardCode",
      "subjectId"
     ],
     "provenance": "derived — WEB-021 declares entryState.params cardCode, subjectId, so an edge into it must carry them"
    },
    {
     "to": "WEB-022",
     "trigger": "Membership Plans",
     "carries": [
      "productId"
     ],
     "provenance": "derived — WEB-022 declares entryState.params productId, so an edge into it must carry them"
    },
    {
     "to": "WEB-024",
     "trigger": "Devices, Wishlist & Consent",
     "carries": [
      "deviceId",
      "itemId",
      "subjectId"
     ],
     "provenance": "derived — WEB-024 declares entryState.params deviceId, itemId, subjectId, so an edge into it must carry them"
    }
   ]
  },
  "notes": "Purpose derived from the screen name and its operations on 17 August, not from a requirement. **Wired 24 August**: getMyMemberships, listGuestMemberships. **The web surface drew the screen and could not fetch what it shows** — the app had these and the browser did not, and there is no reason a membership or a bundle should need an app.",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listGuestMemberships` reads the population and `getMyMemberships` reads one of them — list, select, act",
  "purpose": "Work with membership management for this venue.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every membership",
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
       "operation": "listGuestMemberships",
       "provenance": "contract catalogue.yaml GET /guest/memberships"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected membership",
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
       "label": "Transfer",
       "operation": "transferOrderTickets",
       "provenance": "contract orders.yaml POST /orders/{orderId}/transfer"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "Membership and its benefits",
   "error": "Could not load. Cancellation and renewal are both blocked",
   "emptyFirstRun": "—",
   "emptyNoResults": "The filter narrowed it and the membership are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "transferOrderTickets",
    "contract": "orders",
    "purpose": "Transfer tickets to another guest",
    "trigger": "onAction",
    "invalidates": [
     "listGuestMemberships"
    ]
   },
   {
    "operationId": "getMyMemberships",
    "contract": "catalogue",
    "purpose": "A guest's own memberships, benefits and history",
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
     "name": "orderId",
     "from": "deepLink"
    }
   ],
   "coldEntry": "**A guest opening an order link weeks later.** Shows the order if it still resolves; if it was refunded or the performance passed, says which and offers the order list rather than an error.",
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
   "board": "wireframes/P01 Guest Web.dc.html#web-023"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 3 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "_platform": {
   "code": "P01",
   "audience": "guest",
   "formFactor": "web",
   "shortName": "Guest Web",
   "name": "Guest Web — Storefront",
   "offlineCapable": false,
   "app": "guest-web",
   "operator": "guest",
   "targetApp": {
    "app": "guest",
    "name": "TICVAI Guest",
    "shell": "web",
    "siblings": [
     "P02",
     "P05"
    ],
    "note": "**One guest product in three shells.** Web, mobile and kiosk share 73–91% of their operations; the kiosk is the same product in a fixed frame with no keyboard, and is deliberately narrower rather than different.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "WEB-024",
  "name": "Devices, Wishlist & Consent",
  "module": "Membership, Loyalty & Value",
  "requiresModule": "marketing",
  "wave": 3,
  "capability": "C93",
  "implementation": {
   "app": "guest-web",
   "route": "/membership-loyalty-and-value/loyalty-and-rewards",
   "component": "apps/guest-web/src/routes/membership-loyalty-and-value/LoyaltyAndRewardsDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "WEB-001"
   ],
   "exitTo": [
    "WEB-001",
    "WEB-021",
    "WEB-022",
    "WEB-023"
   ],
   "inferred": true,
   "transitions": [
    {
     "to": "WEB-021",
     "trigger": "Wallet & Gift Cards",
     "carries": [
      "cardCode",
      "subjectId"
     ],
     "provenance": "derived — WEB-021 declares entryState.params cardCode, subjectId, so an edge into it must carry them"
    },
    {
     "to": "WEB-022",
     "trigger": "Membership Plans",
     "carries": [
      "productId"
     ],
     "provenance": "derived — WEB-022 declares entryState.params productId, so an edge into it must carry them"
    },
    {
     "to": "WEB-023",
     "trigger": "Membership Management",
     "carries": [
      "orderId"
     ],
     "provenance": "derived — WEB-023 declares entryState.params orderId, so an edge into it must carry them"
    },
    {
     "to": "GST-037",
     "trigger": "Offers are shown against what they hold",
     "provenance": "flow F53 step 2→3",
     "crossesDevice": true,
     "back": false
    }
   ]
  },
  "notes": "Purpose derived from the screen name and its operations on 17 August, not from a requirement. **Renamed 31 August** from *Loyalty & Rewards*. **A guest surface is one product with two renderings** — a screen named differently on web and app is two screens to a developer and one journey to a guest.",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listGuestDevices` reads the population and `getWishlist` reads one of them — list, select, act",
  "purpose": "See loyalty & rewards for this venue.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every devices wishlist consent",
       "bindsTo": "GuestDevice",
       "columns": [
        "GuestDevice.id",
        "GuestDevice.subjectId",
        "GuestDevice.platform",
        "GuestDevice.tokenFingerprint",
        "GuestDevice.appVersion",
        "GuestDevice.osVersion",
        "GuestDevice.deviceModel",
        "GuestDevice.locale",
        "GuestDevice.status",
        "GuestDevice.failureCount",
        "GuestDevice.registeredAt",
        "GuestDevice.lastSeenAt"
       ],
       "operation": "listGuestDevices",
       "provenance": "contract marketing-crm.yaml GET /guests/{subjectId}/devices"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected devices wishlist consent",
       "bindsTo": "Wishlist",
       "columns": [
        "Wishlist.subjectId",
        "Wishlist.items"
       ],
       "operation": "getWishlist",
       "provenance": "contract marketing-crm.yaml GET /guests/{subjectId}/wishlist"
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
       "operation": "addToWishlist",
       "provenance": "contract marketing-crm.yaml POST /guests/{subjectId}/wishlist"
      },
      {
       "kind": "secondaryButton",
       "label": "Record",
       "operation": "recordConsent",
       "provenance": "contract marketing-crm.yaml POST /guests/{subjectId}/consents"
      },
      {
       "kind": "secondaryButton",
       "label": "Register",
       "operation": "registerGuestDevice",
       "provenance": "contract marketing-crm.yaml POST /guests/{subjectId}/devices"
      },
      {
       "kind": "destructiveButton",
       "label": "Remove",
       "operation": "removeFromWishlist",
       "provenance": "contract marketing-crm.yaml DELETE /guests/{subjectId}/wishlist/{itemId}"
      },
      {
       "kind": "destructiveButton",
       "label": "Revoke",
       "operation": "revokeGuestDevice",
       "provenance": "contract marketing-crm.yaml DELETE /guests/{subjectId}/devices/{deviceId}"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "carried",
     "components": [
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "addToWishlist",
       "label": "Add to wishlist",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "dataTable",
       "derived": true,
       "impliedBy": "listGuestDevices",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "destructiveButton",
       "derived": true,
       "impliedBy": "removeFromWishlist",
       "notes": "**Always confirms, never the default focus.** The consequence goes in the body — *cancel 3 orders worth AED 480* is a confirmation, *are you sure* is not.",
       "label": "Remove from wishlist",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "addToWishlist",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "confirmDialog",
       "derived": true,
       "label": "Confirm",
       "notes": "**The consequence goes in the body, not the title.** *Cancel 3 orders worth AED 480* is a confirmation; *are you sure* is not — and a dialog that cannot name what it destroys is a dialog somebody dismisses.\n\n**Added 31 August.** `confirmDialog` and `modal` were both in the component library and used **zero times across 492 screens**, while `destructiveButton` was used 39 times and its own entry reads *always requires confirmation*.",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "overlays": [
   {
    "id": "confirmRemoveFromWishlist",
    "component": "confirmDialog",
    "trigger": "Remove",
    "body": "**Names what `removeFromWishlist` changes and what it leaves alone**, in the consequence rather than the verb. A devices wishlist consent this affects should be identified in the dialog, not just counted.",
    "provenance": "contract marketing-crm.yaml DELETE /guests/{subjectId}/wishlist/{itemId}"
   },
   {
    "id": "confirmRevokeGuestDevice",
    "component": "confirmDialog",
    "trigger": "Revoke",
    "body": "**Names what `revokeGuestDevice` changes and what it leaves alone**, in the consequence rather than the verb. A devices wishlist consent this affects should be identified in the dialog, not just counted.",
    "provenance": "contract marketing-crm.yaml DELETE /guests/{subjectId}/devices/{deviceId}"
   }
  ],
  "states": {
   "loading": "Points and rewards",
   "error": "Could not load",
   "emptyFirstRun": "No points yet — explains how they accrue",
   "emptyNoResults": "Nothing matches the current filters. **The filters are named and clearable from here** — an empty list with the filter state hidden elsewhere is a person who thinks the data is gone. **Added 25 August with the derived list component**: a screen that lists has to say what it shows when the list is empty, and this screen gained the list before it gained the sentence.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "addToWishlist",
    "contract": "marketing-crm",
    "purpose": "Save an item",
    "trigger": "onAction",
    "invalidates": [
     "listGuestDevices"
    ]
   },
   {
    "operationId": "getWishlist",
    "contract": "marketing-crm",
    "purpose": "Read a guest's saved items",
    "trigger": "onLoad"
   },
   {
    "operationId": "listGuestDevices",
    "contract": "marketing-crm",
    "purpose": "A guest's registered devices",
    "trigger": "onLoad"
   },
   {
    "operationId": "recordConsent",
    "contract": "marketing-crm",
    "purpose": "Record a consent decision",
    "trigger": "onAction",
    "invalidates": [
     "listGuestDevices"
    ]
   },
   {
    "operationId": "registerGuestDevice",
    "contract": "marketing-crm",
    "purpose": "Register a device for push",
    "trigger": "onAction",
    "invalidates": [
     "listGuestDevices"
    ]
   },
   {
    "operationId": "removeFromWishlist",
    "contract": "marketing-crm",
    "purpose": "Remove a saved item",
    "trigger": "onAction",
    "invalidates": [
     "listGuestDevices"
    ]
   },
   {
    "operationId": "revokeGuestDevice",
    "contract": "marketing-crm",
    "purpose": "Revoke a device registration",
    "trigger": "onAction",
    "invalidates": [
     "listGuestDevices"
    ]
   },
   {
    "operationId": "deleteGuestAccount",
    "contract": "identity",
    "purpose": "Ask for the account to be deleted",
    "trigger": "onAction"
   },
   {
    "operationId": "exportSubjectData",
    "contract": "identity",
    "purpose": "Export everything held about this guest",
    "trigger": "onAction"
   },
   {
    "operationId": "getFacePassEnrolment",
    "contract": "access",
    "purpose": "Whether a face pass is enrolled on this account",
    "trigger": "onLoad"
   },
   {
    "operationId": "getGuestConsents",
    "contract": "marketing-crm",
    "purpose": "What this guest has consented to",
    "trigger": "onLoad"
   },
   {
    "operationId": "getWaiverStatus",
    "contract": "marketing-crm",
    "purpose": "Which waivers are signed and which are due",
    "trigger": "onLoad"
   },
   {
    "operationId": "grantDelegation",
    "contract": "identity",
    "purpose": "Let somebody else manage a booking",
    "trigger": "onAction"
   },
   {
    "operationId": "listDelegations",
    "contract": "identity",
    "purpose": "Who may act for this guest",
    "trigger": "onLoad"
   },
   {
    "operationId": "revokeFacePass",
    "contract": "access",
    "purpose": "Revoke it after losing the phone that made it",
    "trigger": "onAction"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "deviceId",
     "from": "deepLink"
    },
    {
     "name": "itemId",
     "from": "deepLink"
    },
    {
     "name": "subjectId",
     "from": "session"
    },
    {
     "name": "enrolmentId",
     "from": "navigation"
    }
   ],
   "coldEntry": "**A guest arriving cold on a link that no longer resolves is shown what happened and one way onward — never a 404.** A shared ticket, a forwarded confirmation and a push notification opened three weeks late all land here, and the person holding the link did nothing wrong. **The screen names the thing, says it is expired, cancelled or withdrawn, and offers the list it came from.** Arrives with `deviceId`, `itemId`.",
   "preloaded": [
    "Wishlist.subjectId",
    "Wishlist.items"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P01 Guest Web.dc.html#web-024"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 7 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "_platform": {
   "code": "P01",
   "audience": "guest",
   "formFactor": "web",
   "shortName": "Guest Web",
   "name": "Guest Web — Storefront",
   "offlineCapable": false,
   "app": "guest-web",
   "operator": "guest",
   "targetApp": {
    "app": "guest",
    "name": "TICVAI Guest",
    "shell": "web",
    "siblings": [
     "P02",
     "P05"
    ],
    "note": "**One guest product in three shells.** Web, mobile and kiosk share 73–91% of their operations; the kiosk is the same product in a fixed frame with no keyboard, and is deliberately narrower rather than different.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "WEB-043",
  "name": "Loyalty & Rewards",
  "module": "Membership, Loyalty & Value",
  "requiresModule": "marketing",
  "wave": 2,
  "implementation": {
   "app": "guest-web",
   "route": "/loyalty-and-rewards",
   "component": "apps/guest-web/src/routes/LoyaltyRewards.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "WEB-001"
   ],
   "exitTo": [
    "WEB-001"
   ]
  },
  "notes": "**P01 Board 3 drew *Membership* with nothing behind it.** `getLoyaltyPosition` and `listLoyaltyProgrammes` were app-only — **the surface a guest checks their points on between visits is the web one.**",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listLoyaltyProgrammes` reads the population and `getLoyaltyPosition` reads one of them — list, select, act",
  "purpose": "Points, tier, and what the next one needs.",
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
    },
    {
     "name": "contentBody",
     "slot": "carried",
     "components": [
      {
       "kind": "cardList",
       "label": "Loyalty & Rewards",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "detailPanel",
       "label": "Detail",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "Content resolves in place.",
   "error": "Could not load. **The rest of the site is unaffected.**",
   "emptyFirstRun": "**Nothing here yet for this venue.** Names what turns it on rather than showing an empty panel.",
   "emptyNoResults": "Nothing matches.",
   "emptyNoAccess": "**Sign in to see this.** A guest who is not signed in is offered the door, not refused."
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
    "operationId": "listPromotions",
    "contract": "promotions",
    "purpose": "List promotions",
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
    "operationId": "createReferral",
    "contract": "marketing-crm",
    "purpose": "Refer a friend",
    "trigger": "onAction"
   },
   {
    "operationId": "redeemLoyaltyPoints",
    "contract": "marketing-crm",
    "purpose": "Spend points",
    "trigger": "onAction"
   }
  ],
  "entryState": {
   "params": [],
   "coldEntry": "**A guest arriving cold on a link that no longer resolves is shown what happened and one way onward — never a 404.** A shared link, a scanned code and a forwarded confirmation all land here, and the person holding it did nothing wrong. Arrives with no parameter — the venue comes from the site."
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P01 Guest Web.dc.html#web-043"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 4 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "_platform": {
   "code": "P01",
   "audience": "guest",
   "formFactor": "web",
   "shortName": "Guest Web",
   "name": "Guest Web — Storefront",
   "offlineCapable": false,
   "app": "guest-web",
   "operator": "guest",
   "targetApp": {
    "app": "guest",
    "name": "TICVAI Guest",
    "shell": "web",
    "siblings": [
     "P02",
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
 "addToWishlist": {
  "method": "POST",
  "path": "/guests/{subjectId}/wishlist",
  "contract": "marketing-crm",
  "summary": "Save an item",
  "permission": null,
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "subject",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "Wishlist"
 },
 "createReferral": {
  "method": "POST",
  "path": "/referrals",
  "contract": "marketing-crm",
  "summary": "Issue a referral code",
  "permission": "MARKETING_MANAGE",
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
  "requestBody": "Referral",
  "responds": "Referral"
 },
 "deleteGuestAccount": {
  "method": "DELETE",
  "path": "/auth/guest/account",
  "contract": "identity",
  "summary": "Self-service account deletion",
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
 "exportSubjectData": {
  "method": "POST",
  "path": "/guests/{subjectId}/data-export",
  "contract": "identity",
  "summary": "Everything the platform holds about one guest",
  "permission": "GUEST_VIEW_PII",
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
 "getFacePassEnrolment": {
  "method": "GET",
  "path": "/face-pass/enrolments/{enrolmentId}",
  "contract": "access",
  "summary": "Whether a pass has a face registered, and when",
  "permission": "GUEST_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "FacePassEnrolment"
 },
 "getGameCard": {
  "method": "GET",
  "path": "/game-cards/{cardCode}",
  "contract": "games",
  "summary": "Read a card's balances",
  "permission": null,
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "GameCard"
 },
 "getGiftCard": {
  "method": "GET",
  "path": "/gift-cards/{cardCode}",
  "contract": "retail",
  "summary": "Check a gift card balance",
  "permission": "ORDER_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "GiftCard"
 },
 "getGuestConsents": {
  "method": "GET",
  "path": "/guests/{subjectId}/consents",
  "contract": "marketing-crm",
  "summary": "Read a guest's consent state",
  "permission": "GUEST_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "ConsentState"
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
 "getProduct": {
  "method": "GET",
  "path": "/products/{productId}",
  "contract": "catalogue",
  "summary": "Read a product",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "Product"
 },
 "getWaiverStatus": {
  "method": "GET",
  "path": "/guests/{subjectId}/waiver-status",
  "contract": "marketing-crm",
  "summary": "Whether this guest may be issued a ticket that requires a waiver",
  "permission": "GUEST_VIEW",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "productId",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": null
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
 "getWishlist": {
  "method": "GET",
  "path": "/guests/{subjectId}/wishlist",
  "contract": "marketing-crm",
  "summary": "Read a guest's saved items",
  "permission": null,
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "subject",
  "parameters": [],
  "requestBody": null,
  "responds": "Wishlist"
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
 "listGuestDevices": {
  "method": "GET",
  "path": "/guests/{subjectId}/devices",
  "contract": "marketing-crm",
  "summary": "A guest's registered devices",
  "permission": null,
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "subject",
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
  "responds": "GuestDevice"
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
 "listPaymentTokens": {
  "method": "GET",
  "path": "/payment-tokens",
  "contract": "orders",
  "summary": "A guest's saved payment methods",
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
  "responds": "PaymentToken"
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
 },
 "recordConsent": {
  "method": "POST",
  "path": "/guests/{subjectId}/consents",
  "contract": "marketing-crm",
  "summary": "Record a consent decision",
  "permission": null,
  "offlineCapable": false,
  "conflictPolicy": "append",
  "scopeLevel": "subject",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "RecordConsentRequest",
  "responds": "ConsentState"
 },
 "redeemLoyaltyPoints": {
  "method": "POST",
  "path": "/loyalty/redemptions",
  "contract": "marketing-crm",
  "summary": "Spend points",
  "permission": "LOYALTY_REDEEM",
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
  "responds": "LoyaltyPosition"
 },
 "registerGuestDevice": {
  "method": "POST",
  "path": "/guests/{subjectId}/devices",
  "contract": "marketing-crm",
  "summary": "Register a device for push",
  "permission": null,
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "subject",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "GuestDevice"
 },
 "removeFromWishlist": {
  "method": "DELETE",
  "path": "/guests/{subjectId}/wishlist/{itemId}",
  "contract": "marketing-crm",
  "summary": "Remove a saved item",
  "permission": null,
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "subject",
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
 "revokeFacePass": {
  "method": "DELETE",
  "path": "/face-pass/enrolments/{enrolmentId}",
  "contract": "access",
  "summary": "Remove a facial profile",
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
  "responds": null
 },
 "revokeGuestDevice": {
  "method": "DELETE",
  "path": "/guests/{subjectId}/devices/{deviceId}",
  "contract": "marketing-crm",
  "summary": "Revoke a device registration",
  "permission": null,
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "subject",
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
 "storePaymentToken": {
  "method": "POST",
  "path": "/payment-tokens",
  "contract": "orders",
  "summary": "Save a payment method for future use",
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
  "responds": "PaymentToken"
 },
 "transferOrderTickets": {
  "method": "POST",
  "path": "/orders/{orderId}/transfer",
  "contract": "orders",
  "summary": "Transfer tickets to another guest",
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
  "responds": null
 },
 "transferWalletBalance": {
  "method": "POST",
  "path": "/wallets/{walletId}/transfer",
  "contract": "retail",
  "summary": "Send balance to another guest",
  "permission": "ORDER_MODIFY",
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
  "responds": null
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
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
 "ConsentDecision": {
  "type": "string",
  "enum": [
   "granted",
   "withdrawn",
   "notAsked"
  ]
 },
 "ConsentPurpose": {
  "type": "string",
  "enum": [
   "marketing",
   "personalisation",
   "profiling",
   "thirdPartySharing",
   "aiProcessing",
   "transactional"
  ]
 },
 "ConsentSource": {
  "type": "string",
  "enum": [
   "guestApp",
   "website",
   "kiosk",
   "pos",
   "callCentre",
   "import",
   "agentRecorded"
  ]
 },
 "ConsentState": {
  "x-ticvai-persistence": "none — projection over consent_record",
  "type": "object",
  "required": [
   "subjectId",
   "purposes"
  ],
  "properties": {
   "subjectId": {
    "type": "string",
    "format": "uuid"
   },
   "purposes": {
    "type": "array",
    "items": {
     "type": "object",
     "required": [
      "purpose",
      "decision",
      "requiresRenewal"
     ],
     "properties": {
      "purpose": {
       "$ref": "#/components/schemas/ConsentPurpose"
      },
      "decision": {
       "$ref": "#/components/schemas/ConsentDecision"
      },
      "channels": {
       "type": "array",
       "items": {
        "$ref": "#/components/schemas/MessageChannel"
       }
      },
      "noticeVersion": {
       "type": "string",
       "nullable": true
      },
      "requiresRenewal": {
       "type": "boolean",
       "description": "True where the notice has been superseded since consent was given."
      },
      "decidedAt": {
       "type": "string",
       "format": "date-time",
       "nullable": true
      }
     }
    }
   }
  }
 },
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
 "FacePassEnrolment": {
  "type": "object",
  "x-ticvai-persistence": "pii.subject_biometric",
  "description": "3.2.43. **Metadata about a facial profile. Never the profile.**\n",
  "required": [
   "id",
   "subjectId",
   "entitlementId",
   "source",
   "capturedAt"
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
   "entitlementId": {
    "type": "string",
    "format": "uuid"
   },
   "source": {
    "type": "string",
    "enum": [
     "guestApp",
     "ticketCounter",
     "annualPassCounter"
    ]
   },
   "capturedAt": {
    "type": "string",
    "format": "date-time"
   },
   "consentPurposeId": {
    "type": "string",
    "format": "uuid"
   },
   "consentGivenAt": {
    "type": "string",
    "format": "date-time"
   },
   "guardianSubjectId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Where the subject is a minor (3.2.12)."
   },
   "isActive": {
    "type": "boolean",
    "readOnly": true
   },
   "expiresAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "description": "**Bounded by the entitlement it belongs to.** A face outliving the pass it was enrolled for is a biometric held for no stated purpose, which CF-64 has to settle.\n"
   }
  }
 },
 "GameCard": {
  "x-ticvai-persistence": "games.card",
  "type": "object",
  "required": [
   "cardCode",
   "venueId",
   "credits",
   "bonusCredits",
   "points",
   "status",
   "issuedAt"
  ],
  "properties": {
   "cardCode": {
    "type": "string"
   },
   "kind": {
    "type": "string"
   },
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "subjectId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "credits": {
    "type": "integer",
    "description": "Bought with money. Buys plays."
   },
   "bonusCredits": {
    "type": "integer",
    "description": "From a promotion. Typically non-refundable and spent before paid credits.\n"
   },
   "points": {
    "type": "integer",
    "description": "Won by playing. Buys prizes. **Not interchangeable with credits** — a guest who wins should not simply be able to play more.\n"
   },
   "status": {
    "type": "string",
    "enum": [
     "active",
     "blocked",
     "expired",
     "transferred"
    ]
   },
   "blockedReason": {
    "type": "string",
    "nullable": true
   },
   "transferredToCardCode": {
    "type": "string",
    "nullable": true
   },
   "lastPlayedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "issuedAt": {
    "type": "string",
    "format": "date-time"
   },
   "expiresAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   }
  }
 },
 "GiftCard": {
  "x-ticvai-persistence": "retail.gift_card",
  "type": "object",
  "required": [
   "cardCode",
   "faceValue",
   "balance",
   "status",
   "issuedAt"
  ],
  "properties": {
   "cardCode": {
    "type": "string"
   },
   "kind": {
    "type": "string"
   },
   "faceValue": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "balance": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "status": {
    "type": "string",
    "enum": [
     "issued",
     "active",
     "partiallyRedeemed",
     "redeemed",
     "expired",
     "blocked"
    ]
   },
   "blockedReason": {
    "type": "string",
    "nullable": true
   },
   "issuedAt": {
    "type": "string",
    "format": "date-time"
   },
   "activatedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "expiresAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   }
  }
 },
 "GuestDevice": {
  "type": "object",
  "x-ticvai-persistence": "marketing.guest_device",
  "required": [
   "id",
   "subjectId",
   "platform",
   "status",
   "registeredAt"
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
   "platform": {
    "type": "string",
    "enum": [
     "ios",
     "android",
     "web"
    ]
   },
   "tokenFingerprint": {
    "type": "string",
    "description": "Hash of the token, not the token. The token itself is write-only — returning it would put a push credential in every response a support agent can read.\n"
   },
   "appVersion": {
    "type": "string",
    "nullable": true
   },
   "osVersion": {
    "type": "string",
    "nullable": true
   },
   "deviceModel": {
    "type": "string",
    "nullable": true
   },
   "locale": {
    "type": "string",
    "nullable": true
   },
   "status": {
    "type": "string",
    "enum": [
     "active",
     "revoked",
     "failed"
    ]
   },
   "failureCount": {
    "type": "integer",
    "description": "Consecutive delivery failures. Past the threshold the device is marked failed and stops being targeted — a dead token retried forever is wasted quota and a misleading delivery rate.\n"
   },
   "registeredAt": {
    "type": "string",
    "format": "date-time"
   },
   "lastSeenAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "revokedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
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
 "LoyaltyPosition": {
  "x-ticvai-persistence": "marketing.loyalty_position",
  "type": "object",
  "required": [
   "subjectId",
   "programmeId",
   "pointsBalance",
   "tierCode"
  ],
  "properties": {
   "subjectId": {
    "type": "string",
    "format": "uuid"
   },
   "programmeId": {
    "type": "string",
    "format": "uuid"
   },
   "pointsBalance": {
    "type": "integer"
   },
   "lifetimePoints": {
    "type": "integer"
   },
   "tierCode": {
    "type": "string"
   },
   "tierName": {
    "type": "string"
   },
   "pointsToNextTier": {
    "type": "integer",
    "nullable": true
   },
   "nextExpiryPoints": {
    "type": "integer",
    "nullable": true
   },
   "nextExpiryAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
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
 "PaymentToken": {
  "type": "object",
  "x-ticvai-persistence": "orders.payment_token",
  "description": "BL-116. **A stored credential, held by the provider and referenced here.** The platform never sees a card number, which is what keeps PCI scope where it belongs.\n**A token is provider-scoped.** A card tokenised with one gateway does not work with another, so a routing change does not silently move a guest's saved card — it means asking them again, and the model should make that visible rather than surprising.\n",
  "required": [
   "id",
   "subjectId",
   "providerId",
   "token",
   "isDefault"
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
   "providerId": {
    "type": "string",
    "format": "uuid"
   },
   "token": {
    "type": "string",
    "format": "password",
    "description": "**Write-only, never returned.** The provider's reference to a credential it holds.\n"
   },
   "method": {
    "type": "string"
   },
   "maskedIdentifier": {
    "type": "string",
    "description": "What a guest sees — the last four digits, the card brand. **Enough to choose between two saved cards and not enough to use one.**\n"
   },
   "expiresAt": {
    "type": "string",
    "format": "date",
    "nullable": true
   },
   "isDefault": {
    "type": "boolean"
   },
   "consentPurposeId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "**Storing a card for future use is a purpose a guest consents to**, separate from the payment they are making now. A token taken without it is a card kept on a guest's behalf that they never agreed to.\n"
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
   "lifecycleState": {
    "$ref": "#/components/schemas/ProductLifecycleState"
   },
   "isSellable": {
    "type": "boolean",
    "description": "True only when live **and** carried by a published bundle. Approval and publication are different acts.\n"
   },
   "hasVariants": {
    "type": "boolean"
   },
   "variantCount": {
    "type": "integer"
   },
   "segmentTags": {
    "type": "array",
    "description": "7.3.5. **A channel and a segment tag are mandatory and nothing required either.** A catalogue that cannot be filtered by segment is a catalogue nobody can report on.\n**Hierarchical, not flat** — `family/with-toddlers` narrows `family` without duplicating it, which is how the promotions engine already treats scope.\n",
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
   }
  }
 },
 "ProductKind": {
  "type": "string",
  "description": "**`openDated` added 24 August** from the client's *Create Ticket Flow* board, which names six main ticket types and this was the one with no kind: **valid on any date within an eligible range, rather than for a named performance or a fixed date.**\nThe mechanism already existed — `access.entitlement` carries `valid_from`, `valid_to`, `entries_allowed` and `frozen_days`, which is exactly an open-dated pass. **What was missing was the product saying it is one**, so a catalogue could not offer it and a report could not count it.\n**`datedAdmission` is a different thing and the two were being conflated**: dated is *this Tuesday*, open-dated is *any Tuesday between March and June*. A guest buying the second and being sold the first has bought the wrong ticket.\n",
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
 "RecordConsentRequest": {
  "x-ticvai-persistence": "none — request only",
  "type": "object",
  "required": [
   "purpose",
   "decision",
   "noticeVersion",
   "source",
   "recordedAt"
  ],
  "properties": {
   "purpose": {
    "$ref": "#/components/schemas/ConsentPurpose"
   },
   "decision": {
    "$ref": "#/components/schemas/ConsentDecision"
   },
   "channels": {
    "type": "array",
    "description": "Omit to apply to every channel the purpose covers.",
    "items": {
     "$ref": "#/components/schemas/MessageChannel"
    }
   },
   "noticeVersion": {
    "type": "string"
   },
   "source": {
    "$ref": "#/components/schemas/ConsentSource"
   },
   "recordedAt": {
    "type": "string",
    "format": "date-time"
   }
  }
 },
 "Referral": {
  "type": "object",
  "x-ticvai-persistence": "marketing.referral",
  "description": "BL-034. **No referrer, no reward, nothing anywhere.**\n**The reward fires on the referee's qualifying act, not on the sign-up**, because a referral that pays on registration pays for accounts rather than for guests.\n",
  "required": [
   "id",
   "referrerSubjectId",
   "code",
   "status"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "referrerSubjectId": {
    "type": "string",
    "format": "uuid"
   },
   "refereeSubjectId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "code": {
    "type": "string"
   },
   "status": {
    "type": "string",
    "enum": [
     "issued",
     "registered",
     "qualified",
     "rewarded",
     "expired",
     "void"
    ]
   },
   "qualifyingAction": {
    "type": "string",
    "enum": [
     "firstPurchase",
     "firstVisit",
     "membershipPurchase"
    ]
   },
   "referrerRewardId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "refereeRewardId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "expiresAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "scopePath": {
    "type": "string",
    "description": "**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `venue` scope.**"
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
 },
 "Wishlist": {
  "type": "object",
  "required": [
   "subjectId",
   "items"
  ],
  "x-ticvai-persistence": "none — wrapper. The items are the table, keyed by subject",
  "properties": {
   "subjectId": {
    "type": "string",
    "format": "uuid"
   },
   "items": {
    "type": "array",
    "x-ticvai-persistence": "marketing.wishlist_item",
    "items": {
     "type": "object",
     "required": [
      "id",
      "variantId",
      "addedAt",
      "isAvailable"
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
       "type": "string"
      },
      "performanceId": {
       "type": "string",
       "format": "uuid",
       "nullable": true
      },
      "performanceStartsAt": {
       "type": "string",
       "format": "date-time",
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
       "description": "False where the product has been withdrawn or the performance has passed. Returned rather than dropped — a guest who saved something and finds it silently gone assumes the feature is broken.\n"
      },
      "unavailableReason": {
       "type": "string",
       "nullable": true
      },
      "note": {
       "type": "string",
       "nullable": true
      },
      "addedAt": {
       "type": "string",
       "format": "date-time"
      }
     }
    }
   }
  }
 }
}
```
