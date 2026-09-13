# Guest web and guest app — parity audit

**Derived.** `python3 tools/audit-guest-parity.py`, 2026-09-14. Reads only.

**The rule, decided 12 September 2026: guest web (P01) and guest app (P02) are identical.** Every difference below either has a reason recorded against it or is a defect waiting for a decision. Which web screen is which app screen is `screens/_guest-pairs.yaml`.

| | |
|---|---|
| Screens | P01 46 · P02 71 |
| Capability groups | 53 — appOnly 7 · folded 3 · paired 42 · webOnly 1 |
| Operations | web 154 · app 155 · shared 154 |
| Findings | high 26 · medium 109 · low 197 · info 4 |

## By dimension

| Dimension | high | medium | low | info |
|---|---|---|---|---|
| licence | 12 |  |  |  |
| wave | 11 |  |  | 1 |
| frontend manifest | 2 | 1 |  |  |
| coverage | 1 | 5 | 3 | 2 |
| operations |  | 44 |  | 1 |
| entry parameters |  | 22 |  |  |
| flows |  | 12 |  |  |
| cross-shell handover |  | 8 |  |  |
| contracts |  | 7 |  |  |
| overlays |  | 3 |  |  |
| states |  | 3 |  |  |
| design |  | 1 |  |  |
| documents |  | 1 | 3 |  |
| events |  | 1 |  |  |
| platform |  | 1 |  |  |
| capability code |  |  | 41 |  |
| components |  |  | 33 |  |
| layout split |  |  | 14 |  |
| naming |  |  | 15 |  |
| navigation |  |  | 42 |  |
| section |  |  | 10 |  |
| state wording |  |  | 36 |  |

## What may differ, and why

- **code** — the platform id
- **formFactor** — web and mobileApp are the two shells
- **runtime** — reactWeb and reactNative are how each shell is built
- **deployment** — a CDN and an app store ship differently (ADR-0006 tiers distribution, not features)
- **wireframeBoard** — one board file per platform
- **offlineCapable** — the app keeps a store across restarts and the web keeps what this visit loaded — what the guest reads offline is identical (12 September)
- **targetApp** — names the sibling, which necessarily differs
- **designReferences** — compared in the design-sources finding instead
- **screenCount** — checked against the real count instead
- **app** — compared in the frontend-manifest finding instead
- **appStatus** — build status
- **density** — compact on the web, comfortable on the app: the input, not the product
- **routes and component paths** — each shell's own codebase

## High — 26

| Dimension | Where | Difference | Resolve by |
|---|---|---|---|
| coverage | add-to-calendar | GST-018 Add to Calendar / Reminders — app only (gap). Adding a visit to a calendar is as much a desktop act as a phone one, and issueWalletPass is already on the web's My Tickets. | add the screen to the web |
| frontend manifest | frontend/guest-app.yaml | lists 80 screens against 71: missing 8 (GST-066, GST-067, GST-068, GST-069, GST-070, GST-071, GST-072, GST-073); ghosts ['GST-060', 'GST-064']; 4 renamed, 1 in another wave | derive-frontend.py carries `screens`, `screenCount` and `byWave` over from the previous file (`e.setdefault` on every existing key) and never recomputes them — derive them |
| frontend manifest | frontend/guest-web.yaml | lists 35 screens against 46: missing 11 (WEB-036, WEB-037, WEB-038, WEB-039, WEB-040, WEB-041, WEB-042, WEB-043, WEB-044, WEB-045, WEB-046); ghosts —; 6 renamed, 1 in another wave | derive-frontend.py carries `screens`, `screenCount` and `byWave` over from the previous file (`e.setdefault` on every existing key) and never recomputes them — derive them |
| licence | ai-concierge (WEB-044 ↔ GST-031/GST-032/GST-033) | web requires ['ai'], app requires ['ai', 'fnb', 'ticketing'] — a tenant licensed for one and not the other sees it on one shell only | one requiresModule for the capability |
| licence | checkout-and-payment (WEB-011/WEB-012/WEB-014 ↔ GST-009) | web requires ['marketing', 'ticketing'], app requires ['ticketing'] — a tenant licensed for one and not the other sees it on one shell only | one requiresModule for the capability |
| licence | help-content-and-accessibility (WEB-045 ↔ GST-040/GST-057) | web requires ['core'], app requires ['core', 'marketing'] — a tenant licensed for one and not the other sees it on one shell only | one requiresModule for the capability |
| licence | home (WEB-001 ↔ GST-001) | web requires ['ticketing'], app requires ['marketing'] — a tenant licensed for one and not the other sees it on one shell only | one requiresModule for the capability |
| licence | in-venue-notifications (WEB-046 ↔ GST-030) | web requires ['marketing'], app requires ['fnb'] — a tenant licensed for one and not the other sees it on one shell only | one requiresModule for the capability |
| licence | lost-and-found (WEB-034 ↔ GST-034) | web requires ['marketing'], app requires ['fnb'] — a tenant licensed for one and not the other sees it on one shell only | one requiresModule for the capability |
| licence | privacy-security-devices (WEB-024 ↔ GST-066/GST-073) | web requires ['marketing'], app requires ['core'] — a tenant licensed for one and not the other sees it on one shell only | one requiresModule for the capability |
| licence | shop (WEB-033 ↔ GST-026) | web requires ['retail'], app requires ['games'] — a tenant licensed for one and not the other sees it on one shell only | one requiresModule for the capability |
| licence | sign-in (WEB-016 ↔ GST-042) | web requires ['ticketing'], app requires ['core'] — a tenant licensed for one and not the other sees it on one shell only | one requiresModule for the capability |
| licence | venue-info (WEB-028 ↔ GST-029) | web requires ['core'], app requires ['fnb'] — a tenant licensed for one and not the other sees it on one shell only | one requiresModule for the capability |
| licence | venue-map-and-wait-times (WEB-039 ↔ GST-021/GST-022) | web requires ['queue'], app requires ['queue', 'seating'] — a tenant licensed for one and not the other sees it on one shell only | one requiresModule for the capability |
| licence | wallet-and-payment-methods (WEB-021 ↔ GST-011/GST-071) | web requires ['retail'], app requires ['core', 'retail'] — a tenant licensed for one and not the other sees it on one shell only | one requiresModule for the capability |
| wave | help-and-cases (WEB-025 ↔ GST-068) | ships in wave 1 on the web and wave 2 on the app | one wave for both, or record why one shell waits |
| wave | lost-and-found (WEB-034 ↔ GST-034) | ships in wave 3 on the web and wave 2 on the app | one wave for both, or record why one shell waits |
| wave | newsletter (WEB-027 ↔ GST-065) | ships in wave 2 on the web and wave 3 on the app | one wave for both, or record why one shell waits |
| wave | order-history (WEB-019 ↔ GST-019) | ships in wave 1 on the web and wave 2 on the app | one wave for both, or record why one shell waits |
| wave | parking (WEB-041 ↔ GST-027/GST-028) | ships in wave 2 on the web and wave 3 on the app | one wave for both, or record why one shell waits |
| wave | privacy-security-devices (WEB-024 ↔ GST-066/GST-073) | ships in wave 3 on the web and wave 2 on the app | one wave for both, or record why one shell waits |
| wave | shop-and-drop (WEB-042 ↔ GST-062) | ships in wave 2 on the web and wave 3 on the app | one wave for both, or record why one shell waits |
| wave | ticket-transfer (WEB-030 ↔ GST-014/GST-045) | ships in wave 1 on the web and wave 2 on the app | one wave for both, or record why one shell waits |
| wave | venue-info (WEB-028 ↔ GST-029) | ships in wave 1 on the web and wave 2 on the app | one wave for both, or record why one shell waits |
| wave | virtual-queue (WEB-040 ↔ GST-023) | ships in wave 2 on the web and wave 3 on the app | one wave for both, or record why one shell waits |
| wave | waiting-room (WEB-015 ↔ GST-046) | ships in wave 2 on the web and wave 1 on the app | one wave for both, or record why one shell waits |

## Medium — 109

| Dimension | Where | Difference | Resolve by |
|---|---|---|---|
| contracts | contracts/satellite/ai.yaml:7 | x-ticvai-platforms names P02 and not P01 | name both guest shells |
| contracts | contracts/satellite/fnb.yaml:17 | x-ticvai-platforms names P02 and not P01 | name both guest shells |
| contracts | contracts/satellite/games.yaml:12 | x-ticvai-platforms names P02 and not P01 | name both guest shells |
| contracts | contracts/satellite/marketing-crm.yaml:21 | x-ticvai-platforms names P02 and not P01 | name both guest shells |
| contracts | contracts/satellite/queue.yaml:10 | x-ticvai-platforms names P02 and not P01 | name both guest shells |
| contracts | contracts/satellite/retail.yaml:10 | x-ticvai-platforms names P02 and not P01 | name both guest shells |
| contracts | contracts/satellite/venue-map.yaml:8 | x-ticvai-platforms names P02 and not P01 | name both guest shells |
| coverage | account-hub | WEB-017 My Account Dashboard — web only (raise). The web has an account dashboard; the app reaches the same things from Home and Profile. A navigation difference rather than a capability one, but it is a difference. | ask the client whether it ships, then add it to both or remove it |
| coverage | cabana-booking | GST-050 Resource Booking – Cabana, GST-058 Resource Availability (Cabana) — app only (raise). Unsourced (guest-surface-parity.md). bookResource and getResourceAvailability are on the web's My Reservations, so the web can book a cabana with no screen drawn for choosing one. | ask the client whether it ships, then add it to both or remove it |
| coverage | digital-companion-mode | GST-038 Digital Companion Mode — app only (raise). Unsourced (CF-92) — reads as a framing for the in-venue screens rather than a capability. "What is near you" lives here and nowhere on the web. | ask the client whether it ships, then add it to both or remove it |
| coverage | itinerary-planning | GST-051 Plan Your Adventure – Start, GST-052 Suggested Itineraries, GST-053 Build Your Own Itinerary, GST-054 AI Optimized Itinerary, GST-059 Plan My Day – In Progress — app only (raise). Five screens with no requirement (guest-surface-parity.md); GST-054 assumes parked AI. | ask the client whether it ships, then add it to both or remove it |
| coverage | rtl-specimen | GST-043 Arabic / RTL Experience — app only (raise). Both platforms declare ltr and rtl. This screen calls nothing — it is a specimen of the Arabic layout, drawn for the app only. | ask the client whether it ships, then add it to both or remove it |
| cross-shell handover | help-content-and-accessibility (WEB-045 ↔ GST-040/GST-057) | GST-040 hands the guest to WEB-034 on the web — "They report something lost" (flow F54 step 2→3) | a twin exists on the same shell; hand over only where the device matters |
| cross-shell handover | lost-and-found (WEB-034 ↔ GST-034) | WEB-034 hands the guest to GST-034 on the app — "They track it" (flow F54 step 3→4) | a twin exists on the same shell; hand over only where the device matters |
| cross-shell handover | loyalty (WEB-043 ↔ GST-036) | GST-036 hands the guest to WEB-024 on the web — "They see rewards and manage their devices" (flow F53 step 1→2) | a twin exists on the same shell; hand over only where the device matters |
| cross-shell handover | privacy-security-devices (WEB-024 ↔ GST-066/GST-073) | WEB-024 hands the guest to GST-037 on the app — "Offers are shown against what they hold" (flow F53 step 2→3) | a twin exists on the same shell; hand over only where the device matters |
| cross-shell handover | shop (WEB-033 ↔ GST-026) | WEB-033 hands the guest to GST-062 on the app — "On the way out they find their collection point" (flow F51 step 2→3) | a twin exists on the same shell; hand over only where the device matters |
| cross-shell handover | sign-in (WEB-016 ↔ GST-042) | WEB-016 hands the guest to GST-039 on the app — "They set a profile" (flow F56 step 3→4) | a twin exists on the same shell; hand over only where the device matters |
| cross-shell handover | sign-in (WEB-016 ↔ GST-042) | GST-042 hands the guest to WEB-016 on the web — "A guest who checked out anonymously links their order" (flow F56 step 2→3) | a twin exists on the same shell; hand over only where the device matters |
| cross-shell handover | ticket-transfer (WEB-030 ↔ GST-014/GST-045) | WEB-030 hands the guest to GST-014 on the app — "The friend claims it in the app" (flow F55 step 4→5) | a twin exists on the same shell; hand over only where the device matters |
| design | Claude Design | web 13/13 batches drawn, app 0/18 — the web is designed and the app is generated boxes, and the only app reference (TICVAI_Mobile.dc.html) uses a different design system from the drawn web frames | draw the app batches against the web's house style, or decide which system is the guest's |
| documents | docs/active/mom-digest.md:3830 | "can differ in functionality" — a client minute says web and app may differ — the 12 September rule says they do not; worth confirming with the client | confirm with the client |
| entry parameters | ai-concierge (WEB-044 ↔ GST-031/GST-032/GST-033) | web opens with ['conversationId', 'outletId'], app with ['cartId', 'conversationId', 'orderId', 'outletId'] — one shared link cannot open both | one deep-link shape per capability |
| entry parameters | cart (WEB-010 ↔ GST-041) | web opens with ['cartId', 'code', 'lineId'], app with ['cartId', 'lineId', 'productId'] — one shared link cannot open both | one deep-link shape per capability |
| entry parameters | checkout-and-payment (WEB-011/WEB-012/WEB-014 ↔ GST-009) | web opens with ['deviceId', 'itemId', 'orderId', 'paymentId', 'subjectId', 'token'], app with ['cartId', 'orderId', 'paymentId', 'token'] — one shared link cannot open both | one deep-link shape per capability |
| entry parameters | date-and-session (WEB-006 ↔ GST-007) | web opens with ['performanceId'], app with ['eventId'] — one shared link cannot open both | one deep-link shape per capability |
| entry parameters | detail (WEB-004 ↔ GST-004/GST-006) | web opens with ['eventId', 'productId'], app with ['eventId', 'performanceId', 'productId'] — one shared link cannot open both | one deep-link shape per capability |
| entry parameters | help-and-cases (WEB-025 ↔ GST-068) | web opens with —, app with ['subjectId'] — one shared link cannot open both | one deep-link shape per capability |
| entry parameters | help-content-and-accessibility (WEB-045 ↔ GST-040/GST-057) | web opens with —, app with ['caseId'] — one shared link cannot open both | one deep-link shape per capability |
| entry parameters | home (WEB-001 ↔ GST-001) | web opens with —, app with ['subjectId'] — one shared link cannot open both | one deep-link shape per capability |
| entry parameters | lost-and-found (WEB-034 ↔ GST-034) | web opens with ['caseId'], app with ['caseId', 'orderId'] — one shared link cannot open both | one deep-link shape per capability |
| entry parameters | memberships (WEB-022/WEB-023 ↔ GST-015) | web opens with ['orderId', 'productId'], app with ['guestLinkId', 'subjectId'] — one shared link cannot open both | one deep-link shape per capability |
| entry parameters | newsletter (WEB-027 ↔ GST-065) | web opens with ['deviceId', 'itemId', 'subjectId'], app with ['subjectId'] — one shared link cannot open both | one deep-link shape per capability |
| entry parameters | offers (WEB-032 ↔ GST-037) | web opens with ['promotionId'], app with ['code', 'promotionId'] — one shared link cannot open both | one deep-link shape per capability |
| entry parameters | order-tracking (WEB-038 ↔ GST-025) | web opens with ['orderId', 'sessionId', 'venueId'], app with ['orderId', 'sessionId'] — one shared link cannot open both | one deep-link shape per capability |
| entry parameters | parking (WEB-041 ↔ GST-027/GST-028) | web opens with ['entitlementId', 'venueId'], app with ['entitlementId'] — one shared link cannot open both | one deep-link shape per capability |
| entry parameters | privacy-security-devices (WEB-024 ↔ GST-066/GST-073) | web opens with ['deviceId', 'enrolmentId', 'itemId', 'subjectId'], app with ['deviceId', 'subjectId'] — one shared link cannot open both | one deep-link shape per capability |
| entry parameters | reservations (WEB-031 ↔ GST-016/GST-017) | web opens with ['groupBookingId', 'reservationId', 'resourceId'], app with ['reservationId'] — one shared link cannot open both | one deep-link shape per capability |
| entry parameters | shop (WEB-033 ↔ GST-026) | web opens with ['cartId', 'outletId'], app with ['cardCode', 'outletId'] — one shared link cannot open both | one deep-link shape per capability |
| entry parameters | shop-and-drop (WEB-042 ↔ GST-062) | web opens with ['outletId'], app with — — one shared link cannot open both | one deep-link shape per capability |
| entry parameters | sign-in (WEB-016 ↔ GST-042) | web opens with ['cartId', 'challengeId', 'methodId', 'providerId'], app with ['challengeId', 'methodId', 'providerId'] — one shared link cannot open both | one deep-link shape per capability |
| entry parameters | ticket-selection (WEB-005 ↔ GST-008) | web opens with ['productId'], app with ['orderId'] — one shared link cannot open both | one deep-link shape per capability |
| entry parameters | venue-info (WEB-028 ↔ GST-029) | web opens with —, app with ['venueId'] — one shared link cannot open both | one deep-link shape per capability |
| entry parameters | venue-map-and-wait-times (WEB-039 ↔ GST-021/GST-022) | web opens with ['mapId', 'venueId'], app with ['mapId'] — one shared link cannot open both | one deep-link shape per capability |
| events | events/whitelabel-contentPublished.yaml | consumed by guest-app only | both guest shells render the content this event invalidates |
| flows | F01 | "Guest buys a ticket online" walks web screens only, though its capabilities exist on the app (cart, checkout-and-payment, confirmation, date-and-session, detail, home) | name both platforms, or say why the journey is one shell's |
| flows | F02 | "Guest buys seated tickets" walks web screens only, though its capabilities exist on the app (cart, checkout-and-payment, date-and-session, seat-selection) | name both platforms, or say why the journey is one shell's |
| flows | F11 | "Guest orders food to a lounger" walks app screens only, though its capabilities exist on the web (checkout-and-payment, fnb-order, order-tracking) | name both platforms, or say why the journey is one shell's |
| flows | F17 | "A guest buys merchandise and collects later" walks app screens only, though its capabilities exist on the web (shop) | name both platforms, or say why the journey is one shell's |
| flows | F18 | "A guest plays an arcade game" walks app screens only, though its capabilities exist on the web (shop) | name both platforms, or say why the journey is one shell's |
| flows | F19 | "A membership works in another country" walks app screens only, though its capabilities exist on the web (memberships) | name both platforms, or say why the journey is one shell's |
| flows | F21 | "A ride queue fills and a guest is redirected" walks app screens only, though its capabilities exist on the web (browse, venue-map-and-wait-times) | name both platforms, or say why the journey is one shell's |
| flows | F25 | "A guest rents a cabana" walks app screens only, though its capabilities exist on the web (venue-map-and-wait-times) | name both platforms, or say why the journey is one shell's |
| flows | F26 | "A venue maps its site" walks app screens only, though its capabilities exist on the web (venue-map-and-wait-times) | name both platforms, or say why the journey is one shell's |
| flows | F48 | "A guest finds it, queues for it, and eats" walks app screens only, though its capabilities exist on the web (fnb-order, in-venue-notifications, order-tracking, venue-map-and-wait-times, virtual-queue) | name both platforms, or say why the journey is one shell's |
| flows | F50 | "A guest arrives, parks, and gets in" walks app screens only, though its capabilities exist on the web (dynamic-qr-ticket, parking, tickets) | name both platforms, or say why the journey is one shell's |
| flows | F52 | "A guest books a cabana and uses it" walks app screens only, though its capabilities exist on the web (cabana-booking, reservations) | name both platforms, or say why the journey is one shell's |
| frontend manifest | frontend/guest-app.yaml | also carries KSK screens — the kiosk (reactWeb) ships inside the reactNative guest app while the web, the app's sibling, ships separately | decide whether TICVAI Guest is one codebase or three |
| operations | ai-concierge (WEB-044 ↔ GST-031/GST-032/GST-033) | the web calls listAiConversations here; the app calls listAiConversations on GST-068 | same operations on the same capability, so a guest finds it in the same place |
| operations | ai-concierge (WEB-044 ↔ GST-031/GST-032/GST-033) | the app calls addCartLine, checkoutCart, createGuestFnbOrder, getCart, getGuestOrderStatus here; the web calls addCartLine on WEB-008/WEB-010/WEB-033; checkoutCart on WEB-010; createGuestFnbOrder on WEB-036; getCart on WEB-010; getGuestOrderStatus on WEB-036/WEB-038 | same operations on the same capability, so a guest finds it in the same place |
| operations | cart (WEB-010 ↔ GST-041) | the web calls addCartLine, evaluatePromotions, getCouponCode here; the app calls addCartLine on GST-032/GST-048/GST-050/GST-053/GST-056; evaluatePromotions on GST-036/GST-037; getCouponCode on GST-037 | same operations on the same capability, so a guest finds it in the same place |
| operations | cart (WEB-010 ↔ GST-041) | the app calls claimCart, listProductVariants here; the web calls claimCart on WEB-016; listProductVariants on WEB-005 | same operations on the same capability, so a guest finds it in the same place |
| operations | checkout-and-payment (WEB-011/WEB-012/WEB-014 ↔ GST-009) | the web calls addToWishlist, getGuestProfile, getOrder, getWishlist, listConsentPurposes, listGuestDevices, recordConsent, registerGuestDevice, removeFromWishlist, revokeGuestDevice, updateMyProfile, uploadGuestDocument here; the app calls addToWishlist on GST-020; getGuestProfile on GST-001; getOrder on GST-010/GST-018/GST-019; getWishlist on GST-020; listConsentPurposes on GST-065; listGuestDevices on GST-073; recordConsent on GST-039/GST-065; registerGuestDevice on GST-073; removeFromWishlist on GST-020; revokeGuestDevice on GST-073; updateMyProfile on GST-039; uploadGuestDocument on GST-066 | same operations on the same capability, so a guest finds it in the same place |
| operations | checkout-and-payment (WEB-011/WEB-012/WEB-014 ↔ GST-009) | the app calls acquireInventoryHold, checkoutCart, getCart here; the web calls acquireInventoryHold on WEB-006; checkoutCart on WEB-010; getCart on WEB-010 | same operations on the same capability, so a guest finds it in the same place |
| operations | date-and-session (WEB-006 ↔ GST-007) | the web calls acquireInventoryHold, getPerformance here; the app calls acquireInventoryHold on GST-009; getPerformance on GST-006 | same operations on the same capability, so a guest finds it in the same place |
| operations | date-and-session (WEB-006 ↔ GST-007) | the app calls listPerformances here; the web calls listPerformances on WEB-002/WEB-004 | same operations on the same capability, so a guest finds it in the same place |
| operations | detail (WEB-004 ↔ GST-004/GST-006) | the app calls getPerformance here; the web calls getPerformance on WEB-006 | same operations on the same capability, so a guest finds it in the same place |
| operations | feedback (WEB-026 ↔ GST-035) | the app calls raiseMyCase here; the web calls raiseMyCase on WEB-034 | same operations on the same capability, so a guest finds it in the same place |
| operations | fnb-order (WEB-036 ↔ GST-024) | the web calls createTableReservation, joinRestaurantWaitlist here; the app calls createTableReservation on GST-070; joinRestaurantWaitlist on GST-070 | same operations on the same capability, so a guest finds it in the same place |
| operations | help-and-cases (WEB-025 ↔ GST-068) | the web calls getTenantAppStatus here; the app calls getTenantAppStatus on GST-001/GST-038/GST-047 | same operations on the same capability, so a guest finds it in the same place |
| operations | help-and-cases (WEB-025 ↔ GST-068) | the app calls listAiConversations here; the web calls listAiConversations on WEB-044 | same operations on the same capability, so a guest finds it in the same place |
| operations | help-content-and-accessibility (WEB-045 ↔ GST-040/GST-057) | the app calls listMyCases, raiseMyCase, replyToMyCase here; the web calls listMyCases on WEB-034; raiseMyCase on WEB-034; replyToMyCase on WEB-034 | same operations on the same capability, so a guest finds it in the same place |
| operations | home (WEB-001 ↔ GST-001) | the web calls listProducts here; the app calls listProducts on GST-002/GST-003/GST-005/GST-015/GST-021/GST-038/GST-044/GST-050/GST-051/GST-052/GST-053/GST-054/GST-058/GST-059 | same operations on the same capability, so a guest finds it in the same place |
| operations | home (WEB-001 ↔ GST-001) | the app calls getGuestProfile, listMyEntitlements, searchCatalogue here; the web calls getGuestProfile on WEB-011/WEB-020; listMyEntitlements on WEB-018; searchCatalogue on WEB-002/WEB-003 | same operations on the same capability, so a guest finds it in the same place |
| operations | loyalty (WEB-043 ↔ GST-036) | the web calls createReferral, redeemLoyaltyPoints here; the app calls createReferral on GST-072; redeemLoyaltyPoints on GST-071 | same operations on the same capability, so a guest finds it in the same place |
| operations | memberships (WEB-022/WEB-023 ↔ GST-015) | the web calls getProduct, transferOrderTickets here; the app calls getProduct on GST-004/GST-006; transferOrderTickets on GST-008/GST-009/GST-010/GST-012/GST-013/GST-014/GST-019/GST-045/GST-055 | same operations on the same capability, so a guest finds it in the same place |
| operations | memberships (WEB-022/WEB-023 ↔ GST-015) | the app calls grantDelegation, listDelegations here; the web calls grantDelegation on WEB-024; listDelegations on WEB-024 | same operations on the same capability, so a guest finds it in the same place |
| operations | newsletter (WEB-027 ↔ GST-065) | the web calls addToWishlist, getWishlist, listGuestDevices, registerGuestDevice, removeFromWishlist, revokeGuestDevice here; the app calls addToWishlist on GST-020; getWishlist on GST-020; listGuestDevices on GST-073; registerGuestDevice on GST-073; removeFromWishlist on GST-020; revokeGuestDevice on GST-073 | same operations on the same capability, so a guest finds it in the same place |
| operations | newsletter (WEB-027 ↔ GST-065) | the app calls listConsentPurposes here; the web calls listConsentPurposes on WEB-011/WEB-020 | same operations on the same capability, so a guest finds it in the same place |
| operations | offers (WEB-032 ↔ GST-037) | the app calls getCouponCode here; the web calls getCouponCode on WEB-010 | same operations on the same capability, so a guest finds it in the same place |
| operations | order-history (WEB-019 ↔ GST-019) | the web calls createRefundRequest here; the app calls createRefundRequest on GST-067 | same operations on the same capability, so a guest finds it in the same place |
| operations | privacy-security-devices (WEB-024 ↔ GST-066/GST-073) | the web calls addToWishlist, getFacePassEnrolment, getWaiverStatus, getWishlist, grantDelegation, listDelegations, recordConsent, removeFromWishlist, revokeFacePass here; the app calls addToWishlist on GST-020; getFacePassEnrolment on GST-069; getWaiverStatus on GST-067; getWishlist on GST-020; grantDelegation on GST-015; listDelegations on GST-015; recordConsent on GST-039/GST-065; removeFromWishlist on GST-020; revokeFacePass on GST-069 | same operations on the same capability, so a guest finds it in the same place |
| operations | privacy-security-devices (WEB-024 ↔ GST-066/GST-073) | the app calls createMfaChallenge, updateGuestPreferences, uploadGuestDocument, verifyGuestEmail here; the web calls createMfaChallenge on WEB-016; updateGuestPreferences on WEB-020; uploadGuestDocument on WEB-011; verifyGuestEmail on WEB-020 | same operations on the same capability, so a guest finds it in the same place |
| operations | profile (WEB-020 ↔ GST-039) | the web calls getGuestProfile, listConsentPurposes, updateGuestPreferences, verifyGuestEmail here; the app calls getGuestProfile on GST-001; listConsentPurposes on GST-065; updateGuestPreferences on GST-066; verifyGuestEmail on GST-073 | same operations on the same capability, so a guest finds it in the same place |
| operations | reservations (WEB-031 ↔ GST-016/GST-017) | the web calls bookResource, getGroupBooking, getResourceAvailability, updateTableReservation here; the app calls bookResource on GST-070; getGroupBooking on GST-072; getResourceAvailability on GST-070; updateTableReservation on GST-070 | same operations on the same capability, so a guest finds it in the same place |
| operations | search (WEB-003 ↔ GST-063) | the web calls listProducts here; the app calls listProducts on GST-002/GST-003/GST-005/GST-015/GST-021/GST-038/GST-044/GST-050/GST-051/GST-052/GST-053/GST-054/GST-058/GST-059 | same operations on the same capability, so a guest finds it in the same place |
| operations | shop (WEB-033 ↔ GST-026) | the web calls addCartLine here; the app calls addCartLine on GST-032/GST-048/GST-050/GST-053/GST-056 | same operations on the same capability, so a guest finds it in the same place |
| operations | shop (WEB-033 ↔ GST-026) | the app calls getGameCard here; the web calls getGameCard on WEB-021 | same operations on the same capability, so a guest finds it in the same place |
| operations | shop-and-drop (WEB-042 ↔ GST-062) | the web calls listMerchandise, lookupMerchandise, reserveMerchandise here; the app calls listMerchandise on GST-026; lookupMerchandise on GST-026; reserveMerchandise on GST-026 | same operations on the same capability, so a guest finds it in the same place |
| operations | sign-in (WEB-016 ↔ GST-042) | the web calls claimCart, createMfaChallenge here; the app calls claimCart on GST-041; createMfaChallenge on GST-073 | same operations on the same capability, so a guest finds it in the same place |
| operations | ticket-selection (WEB-005 ↔ GST-008) | the web calls evaluatePromotions, listProductVariants here; the app calls evaluatePromotions on GST-036/GST-037; listProductVariants on GST-041 | same operations on the same capability, so a guest finds it in the same place |
| operations | ticket-selection (WEB-005 ↔ GST-008) | the app calls transferOrderTickets here; the web calls transferOrderTickets on WEB-012/WEB-013/WEB-018/WEB-019/WEB-023/WEB-030 | same operations on the same capability, so a guest finds it in the same place |
| operations | ticket-transfer (WEB-030 ↔ GST-014/GST-045) | the web calls createResaleListing here; the app calls createResaleListing on GST-067 | same operations on the same capability, so a guest finds it in the same place |
| operations | tickets (WEB-018 ↔ GST-012/GST-013) | the web calls issueWalletPass, shareEntitlement here; the app calls issueWalletPass on GST-018; shareEntitlement on GST-072 | same operations on the same capability, so a guest finds it in the same place |
| operations | venue-info (WEB-028 ↔ GST-029) | the web calls getTenantAppStatus here; the app calls getTenantAppStatus on GST-001/GST-038/GST-047 | same operations on the same capability, so a guest finds it in the same place |
| operations | venue-info (WEB-028 ↔ GST-029) | the app calls listDeliveryLocations, listDiningOutlets here; the web calls listDeliveryLocations on WEB-036; listDiningOutlets on WEB-036 | same operations on the same capability, so a guest finds it in the same place |
| operations | venue-map-and-wait-times (WEB-039 ↔ GST-021/GST-022) | the web calls listQueues here; the app calls listQueues on GST-023 | same operations on the same capability, so a guest finds it in the same place |
| operations | venue-map-and-wait-times (WEB-039 ↔ GST-021/GST-022) | the app calls listProducts here; the web calls listProducts on WEB-001/WEB-002/WEB-003/WEB-022/WEB-035 | same operations on the same capability, so a guest finds it in the same place |
| operations | virtual-queue (WEB-040 ↔ GST-023) | the web calls joinWaitlist, leaveWaitlist here; the app calls joinWaitlist on GST-070; leaveWaitlist on GST-070 | same operations on the same capability, so a guest finds it in the same place |
| operations | virtual-queue (WEB-040 ↔ GST-023) | the app calls listQueues here; the web calls listQueues on WEB-039 | same operations on the same capability, so a guest finds it in the same place |
| operations | wallet-and-payment-methods (WEB-021 ↔ GST-011/GST-071) | the web calls getGameCard here; the app calls getGameCard on GST-026 | same operations on the same capability, so a guest finds it in the same place |
| operations | wallet-and-payment-methods (WEB-021 ↔ GST-011/GST-071) | the app calls redeemLoyaltyPoints here; the web calls redeemLoyaltyPoints on WEB-043 | same operations on the same capability, so a guest finds it in the same place |
| overlays | cart (WEB-010 ↔ GST-041) | declared on the web only |  |
| overlays | checkout-and-payment (WEB-011/WEB-012/WEB-014 ↔ GST-009) | declared on the web only |  |
| overlays | newsletter (WEB-027 ↔ GST-065) | declared on the web only |  |
| platform | themes | web declares ['light'], app declares ['light', 'dark'] — a guest who uses dark mode on the app gets light on the web; both boards are drawn light | declare the same themes on both, or record why the web has no dark mode |
| states | profile (WEB-020 ↔ GST-039) | web only ['emptyNoResults'], app only — |  |
| states | shop-and-drop (WEB-042 ↔ GST-062) | web only ['emptyNoResults'], app only — |  |
| states | ticket-selection (WEB-005 ↔ GST-008) | web only ['emptyNoResults'], app only — |  |

## Low — 197

| Dimension | Where | Difference | Resolve by |
|---|---|---|---|
| capability code | add-ons (WEB-008 ↔ GST-048/GST-056) | web ['C86'], app ['C87', 'C88'] — traceability counts them as two |  |
| capability code | ai-concierge (WEB-044 ↔ GST-031/GST-032/GST-033) | web —, app ['AI-02'] — traceability counts them as two |  |
| capability code | browse (WEB-002 ↔ GST-002/GST-003/GST-005) | web ['C79'], app ['C02', 'C84'] — traceability counts them as two |  |
| capability code | cart (WEB-010 ↔ GST-041) | web ['C02'], app ['C56'] — traceability counts them as two |  |
| capability code | checkout-and-payment (WEB-011/WEB-012/WEB-014 ↔ GST-009) | web ['C03', 'C04'], app ['C47'] — traceability counts them as two |  |
| capability code | confirmation (WEB-013 ↔ GST-010) | web ['C03'], app ['C02'] — traceability counts them as two |  |
| capability code | date-and-session (WEB-006 ↔ GST-007) | web ['C81'], app ['C02'] — traceability counts them as two |  |
| capability code | detail (WEB-004 ↔ GST-004/GST-006) | web ['C79'], app ['C02', 'C84'] — traceability counts them as two |  |
| capability code | feedback (WEB-026 ↔ GST-035) | web ['C33'], app ['C62'] — traceability counts them as two |  |
| capability code | fnb-order (WEB-036 ↔ GST-024) | web —, app ['C05'] — traceability counts them as two |  |
| capability code | help-and-cases (WEB-025 ↔ GST-068) | web ['C105'], app ['read-write'] — traceability counts them as two |  |
| capability code | help-content-and-accessibility (WEB-045 ↔ GST-040/GST-057) | web —, app ['C17'] — traceability counts them as two |  |
| capability code | home (WEB-001 ↔ GST-001) | web ['C79'], app ['C02'] — traceability counts them as two |  |
| capability code | in-venue-notifications (WEB-046 ↔ GST-030) | web —, app ['C61'] — traceability counts them as two |  |
| capability code | lost-and-found (WEB-034 ↔ GST-034) | web ['C00'], app ['C18'] — traceability counts them as two |  |
| capability code | loyalty (WEB-043 ↔ GST-036) | web —, app ['C64'] — traceability counts them as two |  |
| capability code | memberships (WEB-022/WEB-023 ↔ GST-015) | web ['C31'], app ['C03'] — traceability counts them as two |  |
| capability code | menu-item (WEB-037 ↔ GST-061) | web —, app ['C05'] — traceability counts them as two |  |
| capability code | multi-currency (WEB-035 ↔ GST-044) | web ['C00'], app ['C107'] — traceability counts them as two |  |
| capability code | newsletter (WEB-027 ↔ GST-065) | web ['C59'], app ['C00'] — traceability counts them as two |  |
| capability code | offers (WEB-032 ↔ GST-037) | web ['C00'], app ['C86'] — traceability counts them as two |  |
| capability code | order-history (WEB-019 ↔ GST-019) | web ['C34'], app ['C21'] — traceability counts them as two |  |
| capability code | order-tracking (WEB-038 ↔ GST-025) | web —, app ['C05'] — traceability counts them as two |  |
| capability code | parking (WEB-041 ↔ GST-027/GST-028) | web —, app ['C23'] — traceability counts them as two |  |
| capability code | privacy-security-devices (WEB-024 ↔ GST-066/GST-073) | web ['C93'], app ['read-write'] — traceability counts them as two |  |
| capability code | profile (WEB-020 ↔ GST-039) | web ['C36'], app ['C58'] — traceability counts them as two |  |
| capability code | reservations (WEB-031 ↔ GST-016/GST-017) | web ['C00'], app ['C02'] — traceability counts them as two |  |
| capability code | search (WEB-003 ↔ GST-063) | web ['C79'], app ['C00'] — traceability counts them as two |  |
| capability code | seat-selection (WEB-007 ↔ GST-049) | web ['C51'], app ['C53'] — traceability counts them as two |  |
| capability code | shop (WEB-033 ↔ GST-026) | web ['C00'], app ['C08'] — traceability counts them as two |  |
| capability code | shop-and-drop (WEB-042 ↔ GST-062) | web —, app ['C21'] — traceability counts them as two |  |
| capability code | sign-in (WEB-016 ↔ GST-042) | web ['C36'], app ['C56'] — traceability counts them as two |  |
| capability code | ticket-selection (WEB-005 ↔ GST-008) | web ['C80'], app ['C02'] — traceability counts them as two |  |
| capability code | ticket-transfer (WEB-030 ↔ GST-014/GST-045) | web ['C00'], app ['C02'] — traceability counts them as two |  |
| capability code | tickets (WEB-018 ↔ GST-012/GST-013) | web ['C09'], app ['C02'] — traceability counts them as two |  |
| capability code | venue-info (WEB-028 ↔ GST-029) | web ['C105'], app ['C17'] — traceability counts them as two |  |
| capability code | venue-map-and-wait-times (WEB-039 ↔ GST-021/GST-022) | web —, app ['C39', 'C82'] — traceability counts them as two |  |
| capability code | virtual-queue (WEB-040 ↔ GST-023) | web —, app ['C82'] — traceability counts them as two |  |
| capability code | waiting-room (WEB-015 ↔ GST-046) | web —, app ['C98'] — traceability counts them as two |  |
| capability code | wallet-and-payment-methods (WEB-021 ↔ GST-011/GST-071) | web ['C21'], app ['C37', 'read-write'] — traceability counts them as two |  |
| capability code | wishlist (WEB-009 ↔ GST-020) | web ['C79'], app ['C58'] — traceability counts them as two |  |
| components | add-ons (WEB-008 ↔ GST-048/GST-056) | web only ['secondaryButton'], app only ['dataTable'] (4 vs 5 components) |  |
| components | ai-concierge (WEB-044 ↔ GST-031/GST-032/GST-033) | web only ['cardList'], app only — (7 vs 14 components) |  |
| components | browse (WEB-002 ↔ GST-002/GST-003/GST-005) | web only ['cardList', 'datePicker', 'multiSelect', 'searchField'], app only — (6 vs 6 components) |  |
| components | cart (WEB-010 ↔ GST-041) | web only ['banner', 'destructiveButton', 'secondaryButton', 'textField'], app only — (11 vs 2 components) |  |
| components | checkout-and-payment (WEB-011/WEB-012/WEB-014 ↔ GST-009) | web only ['banner', 'cartPanel', 'consentBlock', 'dataTable', 'destructiveButton', 'textField'], app only — (26 vs 5 components) |  |
| components | confirmation (WEB-013 ↔ GST-010) | web only ['banner'], app only — (6 vs 3 components) |  |
| components | date-and-session (WEB-006 ↔ GST-007) | web only ['cardList', 'datePicker', 'primaryButton'], app only ['dataTable'] (4 vs 1 components) |  |
| components | detail (WEB-004 ↔ GST-004/GST-006) | web only ['banner', 'primaryButton'], app only — (4 vs 3 components) |  |
| components | fnb-order (WEB-036 ↔ GST-024) | web only ['cardList'], app only — (7 vs 5 components) |  |
| components | help-and-cases (WEB-025 ↔ GST-068) | web only ['secondaryButton'], app only — (4 vs 3 components) |  |
| components | help-content-and-accessibility (WEB-045 ↔ GST-040/GST-057) | web only ['cardList'], app only ['metricTile', 'primaryButton', 'secondaryButton'] (4 vs 8 components) |  |
| components | home (WEB-001 ↔ GST-001) | web only ['banner', 'cardList', 'iconButton', 'secondaryButton'], app only — (6 vs 2 components) |  |
| components | in-venue-notifications (WEB-046 ↔ GST-030) | web only ['cardList', 'detailPanel'], app only ['secondaryButton'] (3 vs 2 components) |  |
| components | loyalty (WEB-043 ↔ GST-036) | web only ['cardList', 'detailPanel'], app only — (4 vs 2 components) |  |
| components | menu-item (WEB-037 ↔ GST-061) | web only ['cardList'], app only ['banner', 'selectField'] (4 vs 4 components) |  |
| components | newsletter (WEB-027 ↔ GST-065) | web only ['confirmDialog', 'destructiveButton'], app only — (12 vs 4 components) |  |
| components | offers (WEB-032 ↔ GST-037) | web only ['secondaryButton'], app only — (5 vs 3 components) |  |
| components | order-tracking (WEB-038 ↔ GST-025) | web only ['cardList'], app only — (4 vs 2 components) |  |
| components | parking (WEB-041 ↔ GST-027/GST-028) | web only ['cardList'], app only — (6 vs 7 components) |  |
| components | privacy-security-devices (WEB-024 ↔ GST-066/GST-073) | web only ['confirmDialog'], app only — (12 vs 8 components) |  |
| components | profile (WEB-020 ↔ GST-039) | web only ['dataTable', 'detailPanel', 'secondaryButton'], app only ['textField'] (8 vs 7 components) |  |
| components | reservations (WEB-031 ↔ GST-016/GST-017) | web only ['confirmDialog', 'secondaryButton'], app only — (7 vs 5 components) |  |
| components | search (WEB-003 ↔ GST-063) | web only —, app only ['searchField'] (2 vs 3 components) |  |
| components | seat-selection (WEB-007 ↔ GST-049) | web only ['banner'], app only — (6 vs 7 components) |  |
| components | shop (WEB-033 ↔ GST-026) | web only ['primaryButton', 'searchField', 'secondaryButton'], app only — (7 vs 2 components) |  |
| components | shop-and-drop (WEB-042 ↔ GST-062) | web only ['cardList', 'dataTable', 'detailPanel', 'secondaryButton'], app only ['banner'] (7 vs 2 components) |  |
| components | ticket-selection (WEB-005 ↔ GST-008) | web only ['banner', 'cardList', 'dataTable', 'detailPanel'], app only ['secondaryButton'] (6 vs 2 components) |  |
| components | venue-info (WEB-028 ↔ GST-029) | web only —, app only ['dataTable'] (1 vs 2 components) |  |
| components | venue-map-and-wait-times (WEB-039 ↔ GST-021/GST-022) | web only ['cardList'], app only — (4 vs 5 components) |  |
| components | virtual-queue (WEB-040 ↔ GST-023) | web only ['cardList'], app only — (5 vs 3 components) |  |
| components | waiting-room (WEB-015 ↔ GST-046) | web only ['secondaryButton'], app only — (3 vs 2 components) |  |
| components | wallet-and-payment-methods (WEB-021 ↔ GST-011/GST-071) | web only —, app only ['primaryButton', 'secondaryButton'] (3 vs 7 components) |  |
| components | wishlist (WEB-009 ↔ GST-020) | web only ['confirmDialog', 'secondaryButton'], app only — (7 vs 3 components) |  |
| coverage | refunds-and-resale | GST-067 Refunds & Resale has no web screen; its operations are on WEB-019, WEB-030; getWaiverStatus on WEB-024 | draw the screen on the other shell, or record the fold as the decision |
| coverage | reserve-table-or-cabana | GST-070 Reserve a Table or Cabana has no web screen; its operations are on WEB-031, WEB-036, WEB-040 | draw the screen on the other shell, or record the fold as the decision |
| coverage | share-and-group-booking | GST-072 Share & Group Booking has no web screen; its operations are on WEB-017, WEB-018, WEB-031, WEB-043 | draw the screen on the other shell, or record the fold as the decision |
| documents | contracts/spine/catalogue.yaml:784 | "browses by category and cannot search" — GST-063 Search exists since 17 August | rewrite to the 12 September rule |
| documents | docs/active/design-plan.md:267 | "guest-app surfaces are not" — P02 is offlineCapable: true | rewrite to the 12 September rule |
| documents | docs/registers/conflicts.md:148 | "stay app-only by design" — CF-93 predates WEB-036–046 and the 10 September decision | rewrite to the 12 September rule |
| layout split | add-ons (WEB-008 ↔ GST-048/GST-056) | 1 screen(s) on the web, 2 on the app: Add-ons & Upsell ↔ Upsell / Cross-Sell; Bundle Package | fine if deliberate; a builder should know it is one capability |
| layout split | ai-concierge (WEB-044 ↔ GST-031/GST-032/GST-033) | 1 screen(s) on the web, 3 on the app: AI Concierge – Home ↔ AI Concierge – Home; AI Concierge – Chat; AI Concierge – Contextual Help | fine if deliberate; a builder should know it is one capability |
| layout split | browse (WEB-002 ↔ GST-002/GST-003/GST-005) | 1 screen(s) on the web, 3 on the app: Event & Attraction Listing ↔ Explore Categories; Event & Attraction Listing; What's On | fine if deliberate; a builder should know it is one capability |
| layout split | checkout-and-payment (WEB-011/WEB-012/WEB-014 ↔ GST-009) | 3 screen(s) on the web, 1 on the app: Guest Details & Attendee Forms; Checkout — Payment; Pay for a Booking ↔ Review & Payment | fine if deliberate; a builder should know it is one capability |
| layout split | detail (WEB-004 ↔ GST-004/GST-006) | 1 screen(s) on the web, 2 on the app: Attraction Details ↔ Attraction Details; Event / Exhibition Details | fine if deliberate; a builder should know it is one capability |
| layout split | help-content-and-accessibility (WEB-045 ↔ GST-040/GST-057) | 1 screen(s) on the web, 2 on the app: Help Centre & Accessibility ↔ Help & Support; Accessibility Information | fine if deliberate; a builder should know it is one capability |
| layout split | memberships (WEB-022/WEB-023 ↔ GST-015) | 2 screen(s) on the web, 1 on the app: Membership Plans; Membership Management ↔ Memberships | fine if deliberate; a builder should know it is one capability |
| layout split | parking (WEB-041 ↔ GST-027/GST-028) | 1 screen(s) on the web, 2 on the app: Parking – Reserve & Pay ↔ Parking – Reserve & Pay; Parking – Reservation Confirmed | fine if deliberate; a builder should know it is one capability |
| layout split | privacy-security-devices (WEB-024 ↔ GST-066/GST-073) | 1 screen(s) on the web, 2 on the app: Devices, Wishlist & Consent ↔ Privacy & My Data; Security & Sign-in | fine if deliberate; a builder should know it is one capability |
| layout split | reservations (WEB-031 ↔ GST-016/GST-017) | 1 screen(s) on the web, 2 on the app: My Reservations ↔ My Reservations; Reservation Details | fine if deliberate; a builder should know it is one capability |
| layout split | ticket-transfer (WEB-030 ↔ GST-014/GST-045) | 1 screen(s) on the web, 2 on the app: Ticket Transfer ↔ Ticket Transfer; Ticket Delivery & Sharing | fine if deliberate; a builder should know it is one capability |
| layout split | tickets (WEB-018 ↔ GST-012/GST-013) | 1 screen(s) on the web, 2 on the app: My Tickets ↔ My Tickets; Ticket Details | fine if deliberate; a builder should know it is one capability |
| layout split | venue-map-and-wait-times (WEB-039 ↔ GST-021/GST-022) | 1 screen(s) on the web, 2 on the app: Venue Map & Wait Times ↔ Interactive Map; Attraction Wait Times | fine if deliberate; a builder should know it is one capability |
| layout split | wallet-and-payment-methods (WEB-021 ↔ GST-011/GST-071) | 1 screen(s) on the web, 2 on the app: Wallet & Gift Cards ↔ Wallet Overview; Payment Methods | fine if deliberate; a builder should know it is one capability |
| naming | cart (WEB-010 ↔ GST-041) | "Shopping Cart" ↔ "Checkout Entry" | one name for one journey (31 August rule) |
| naming | date-and-session (WEB-006 ↔ GST-007) | "Date & Session Selection" ↔ "Select Date & Time" | one name for one journey (31 August rule) |
| naming | feedback (WEB-026 ↔ GST-035) | "Survey & Feedback" ↔ "Feedback & Ratings" | one name for one journey (31 August rule) |
| naming | help-and-cases (WEB-025 ↔ GST-068) | "Help Centre / FAQ" ↔ "Help & My Cases" | one name for one journey (31 August rule) |
| naming | home (WEB-001 ↔ GST-001) | "Home / Landing" ↔ "Home – Default" | one name for one journey (31 August rule) |
| naming | newsletter (WEB-027 ↔ GST-065) | "Newsletter Subscription" ↔ "Newsletter & Preferences" | one name for one journey (31 August rule) |
| naming | profile (WEB-020 ↔ GST-039) | "Profile & Preferences" ↔ "Profile" | one name for one journey (31 August rule) |
| naming | search (WEB-003 ↔ GST-063) | "Search Results" ↔ "Search" | one name for one journey (31 August rule) |
| naming | shop (WEB-033 ↔ GST-026) | "Shop" ↔ "Retail / Merchandise" | one name for one journey (31 August rule) |
| naming | shop-and-drop (WEB-042 ↔ GST-062) | "Retail & Shop and Drop" ↔ "Shop & Drop Collection" | one name for one journey (31 August rule) |
| naming | sign-in (WEB-016 ↔ GST-042) | "Login / Register" ↔ "Simple Registration & OTP" | one name for one journey (31 August rule) |
| naming | system-states (WEB-029 ↔ GST-047) | "Error / Sold Out / Maintenance" ↔ "Maintenance / Upgrade Page" | one name for one journey (31 August rule) |
| naming | ticket-selection (WEB-005 ↔ GST-008) | "Ticket Type Selection" ↔ "Tickets & Add-ons" | one name for one journey (31 August rule) |
| naming | venue-info (WEB-028 ↔ GST-029) | "Contact & Venue Information" ↔ "Venue Info & Services" | one name for one journey (31 August rule) |
| naming | wishlist (WEB-009 ↔ GST-020) | "Wishlist" ↔ "Saved Items / Wishlist" | one name for one journey (31 August rule) |
| navigation | add-ons (WEB-008 ↔ GST-048/GST-056) | leads on to ['date-and-session', 'seat-selection', 'ticket-selection'] on the web only and ['browse'] on the app only |  |
| navigation | ai-concierge (WEB-044 ↔ GST-031/GST-032/GST-033) | leads on to — on the web only and ['browse'] on the app only |  |
| navigation | browse (WEB-002 ↔ GST-002/GST-003/GST-005) | leads on to ['search'] on the web only and — on the app only |  |
| navigation | cart (WEB-010 ↔ GST-041) | leads on to ['checkout-and-payment', 'confirmation', 'ticket-transfer'] on the web only and ['browse'] on the app only |  |
| navigation | checkout-and-payment (WEB-011/WEB-012/WEB-014 ↔ GST-009) | leads on to ['cart', 'confirmation'] on the web only and ['browse'] on the app only |  |
| navigation | confirmation (WEB-013 ↔ GST-010) | leads on to ['cart', 'checkout-and-payment', 'tickets'] on the web only and ['browse'] on the app only |  |
| navigation | date-and-session (WEB-006 ↔ GST-007) | leads on to ['add-ons', 'cart', 'seat-selection', 'ticket-selection'] on the web only and ['browse'] on the app only |  |
| navigation | detail (WEB-004 ↔ GST-004/GST-006) | leads on to ['search', 'ticket-selection'] on the web only and — on the app only |  |
| navigation | feedback (WEB-026 ↔ GST-035) | leads on to ['help-and-cases', 'newsletter', 'venue-info'] on the web only and ['browse'] on the app only |  |
| navigation | fnb-order (WEB-036 ↔ GST-024) | leads on to — on the web only and ['browse', 'checkout-and-payment', 'order-tracking'] on the app only |  |
| navigation | help-and-cases (WEB-025 ↔ GST-068) | leads on to ['feedback', 'home', 'newsletter', 'venue-info'] on the web only and ['profile'] on the app only |  |
| navigation | help-content-and-accessibility (WEB-045 ↔ GST-040/GST-057) | leads on to — on the web only and ['browse'] on the app only |  |
| navigation | home (WEB-001 ↔ GST-001) | leads on to ['ai-concierge', 'fnb-order', 'help-content-and-accessibility', 'in-venue-notifications', 'loyalty', 'menu-item', 'order-tracking', 'parking', 'search', 'shop-and-drop', 'sign-in', 'venue-map-and-wait-times', 'virtual-queue'] on the web only and — on the app only |  |
| navigation | in-venue-notifications (WEB-046 ↔ GST-030) | leads on to — on the web only and ['ai-concierge', 'browse'] on the app only |  |
| navigation | lost-and-found (WEB-034 ↔ GST-034) | leads on to — on the web only and ['browse'] on the app only |  |
| navigation | loyalty (WEB-043 ↔ GST-036) | leads on to — on the web only and ['browse'] on the app only |  |
| navigation | memberships (WEB-022/WEB-023 ↔ GST-015) | leads on to ['privacy-security-devices', 'wallet-and-payment-methods'] on the web only and ['browse'] on the app only |  |
| navigation | menu-item (WEB-037 ↔ GST-061) | leads on to — on the web only and ['shop-and-drop'] on the app only |  |
| navigation | multi-currency (WEB-035 ↔ GST-044) | leads on to ['reservations', 'ticket-transfer'] on the web only and ['browse'] on the app only |  |
| navigation | newsletter (WEB-027 ↔ GST-065) | leads on to ['feedback', 'help-and-cases', 'venue-info'] on the web only and — on the app only |  |
| navigation | offers (WEB-032 ↔ GST-037) | leads on to — on the web only and ['browse', 'wallet-and-payment-methods'] on the app only |  |
| navigation | order-history (WEB-019 ↔ GST-019) | leads on to ['account-hub', 'sign-in', 'tickets'] on the web only and ['browse'] on the app only |  |
| navigation | order-tracking (WEB-038 ↔ GST-025) | leads on to — on the web only and ['browse', 'in-venue-notifications'] on the app only |  |
| navigation | parking (WEB-041 ↔ GST-027/GST-028) | leads on to — on the web only and ['browse', 'tickets'] on the app only |  |
| navigation | privacy-security-devices (WEB-024 ↔ GST-066/GST-073) | leads on to ['home', 'memberships', 'wallet-and-payment-methods'] on the web only and ['profile'] on the app only |  |
| navigation | profile (WEB-020 ↔ GST-039) | leads on to ['account-hub', 'sign-in', 'tickets'] on the web only and ['browse', 'newsletter'] on the app only |  |
| navigation | reservations (WEB-031 ↔ GST-016/GST-017) | leads on to ['multi-currency', 'ticket-transfer'] on the web only and ['browse'] on the app only |  |
| navigation | search (WEB-003 ↔ GST-063) | leads on to ['browse', 'detail'] on the web only and — on the app only |  |
| navigation | seat-selection (WEB-007 ↔ GST-049) | leads on to ['add-ons', 'cart', 'date-and-session', 'ticket-selection'] on the web only and ['browse'] on the app only |  |
| navigation | shop (WEB-033 ↔ GST-026) | leads on to — on the web only and ['browse'] on the app only |  |
| navigation | shop-and-drop (WEB-042 ↔ GST-062) | leads on to — on the web only and ['menu-item'] on the app only |  |
| navigation | sign-in (WEB-016 ↔ GST-042) | leads on to ['account-hub', 'order-history', 'tickets'] on the web only and ['browse'] on the app only |  |
| navigation | system-states (WEB-029 ↔ GST-047) | leads on to — on the web only and ['browse'] on the app only |  |
| navigation | ticket-selection (WEB-005 ↔ GST-008) | leads on to ['add-ons', 'cart', 'date-and-session', 'seat-selection'] on the web only and ['browse'] on the app only |  |
| navigation | ticket-transfer (WEB-030 ↔ GST-014/GST-045) | leads on to ['multi-currency', 'reservations'] on the web only and ['browse'] on the app only |  |
| navigation | tickets (WEB-018 ↔ GST-012/GST-013) | leads on to ['account-hub', 'order-history', 'sign-in'] on the web only and ['browse', 'dynamic-qr-ticket'] on the app only |  |
| navigation | venue-info (WEB-028 ↔ GST-029) | leads on to ['feedback', 'help-and-cases', 'newsletter'] on the web only and ['browse'] on the app only |  |
| navigation | venue-map-and-wait-times (WEB-039 ↔ GST-021/GST-022) | leads on to — on the web only and ['browse', 'itinerary-planning', 'virtual-queue'] on the app only |  |
| navigation | virtual-queue (WEB-040 ↔ GST-023) | leads on to — on the web only and ['browse', 'fnb-order'] on the app only |  |
| navigation | waiting-room (WEB-015 ↔ GST-046) | leads on to — on the web only and ['browse'] on the app only |  |
| navigation | wallet-and-payment-methods (WEB-021 ↔ GST-011/GST-071) | leads on to ['memberships', 'privacy-security-devices'] on the web only and ['browse', 'profile', 'wishlist'] on the app only |  |
| navigation | wishlist (WEB-009 ↔ GST-020) | leads on to ['date-and-session', 'seat-selection', 'ticket-selection'] on the web only and ['browse'] on the app only |  |
| section | help-content-and-accessibility (WEB-045 ↔ GST-040/GST-057) | web section ['Support'], app ['Discovery & Browse', 'Engagement & Support'] |  |
| section | menu-item (WEB-037 ↔ GST-061) | web section ['In-venue Services'], app ['In-Venue Experience'] |  |
| section | newsletter (WEB-027 ↔ GST-065) | web section ['Engagement & Support'], app ['Marketing'] |  |
| section | privacy-security-devices (WEB-024 ↔ GST-066/GST-073) | web section ['Membership, Loyalty & Value'], app ['Account & Self-Service'] |  |
| section | search (WEB-003 ↔ GST-063) | web section ['Discovery & Browse'], app ['Discovery'] |  |
| section | shop-and-drop (WEB-042 ↔ GST-062) | web section ['Retail'], app ['In-Venue Experience'] |  |
| section | ticket-transfer (WEB-030 ↔ GST-014/GST-045) | web section ['Ticketing'], app ['Account & Self-Service', 'Ticketing'] |  |
| section | venue-info (WEB-028 ↔ GST-029) | web section ['Engagement & Support'], app ['In-venue Services'] |  |
| section | wallet-and-payment-methods (WEB-021 ↔ GST-011/GST-071) | web section ['Membership, Loyalty & Value'], app ['Account & Self-Service', 'Membership, Loyalty & Value'] |  |
| section | wishlist (WEB-009 ↔ GST-020) | web section ['Booking & Selection'], app ['Account & Self-Service'] |  |
| state wording | add-ons (WEB-008 ↔ GST-048/GST-056) | 4 state(s) worded differently: emptyFirstRun, emptyNoResults, error, loading | one copy per state — the 12 September offline sync is the model |
| state wording | ai-concierge (WEB-044 ↔ GST-031/GST-032/GST-033) | 5 state(s) worded differently: emptyFirstRun, emptyNoAccess, emptyNoResults, error, loading | one copy per state — the 12 September offline sync is the model |
| state wording | browse (WEB-002 ↔ GST-002/GST-003/GST-005) | 4 state(s) worded differently: emptyFirstRun, emptyNoResults, error, loading | one copy per state — the 12 September offline sync is the model |
| state wording | cart (WEB-010 ↔ GST-041) | 4 state(s) worded differently: emptyFirstRun, emptyNoResults, error, loading | one copy per state — the 12 September offline sync is the model |
| state wording | checkout-and-payment (WEB-011/WEB-012/WEB-014 ↔ GST-009) | 5 state(s) worded differently: emptyFirstRun, emptyNoAccess, emptyNoResults, error, loading | one copy per state — the 12 September offline sync is the model |
| state wording | date-and-session (WEB-006 ↔ GST-007) | 4 state(s) worded differently: emptyFirstRun, emptyNoResults, error, loading | one copy per state — the 12 September offline sync is the model |
| state wording | detail (WEB-004 ↔ GST-004/GST-006) | 4 state(s) worded differently: emptyFirstRun, emptyNoResults, error, loading | one copy per state — the 12 September offline sync is the model |
| state wording | feedback (WEB-026 ↔ GST-035) | 3 state(s) worded differently: emptyFirstRun, error, loading | one copy per state — the 12 September offline sync is the model |
| state wording | fnb-order (WEB-036 ↔ GST-024) | 5 state(s) worded differently: emptyFirstRun, emptyNoAccess, emptyNoResults, error, loading | one copy per state — the 12 September offline sync is the model |
| state wording | help-and-cases (WEB-025 ↔ GST-068) | 4 state(s) worded differently: emptyFirstRun, emptyNoResults, error, loading | one copy per state — the 12 September offline sync is the model |
| state wording | help-content-and-accessibility (WEB-045 ↔ GST-040/GST-057) | 5 state(s) worded differently: emptyFirstRun, emptyNoAccess, emptyNoResults, error, loading | one copy per state — the 12 September offline sync is the model |
| state wording | home (WEB-001 ↔ GST-001) | 4 state(s) worded differently: emptyFirstRun, emptyNoResults, error, loading | one copy per state — the 12 September offline sync is the model |
| state wording | in-venue-notifications (WEB-046 ↔ GST-030) | 4 state(s) worded differently: emptyFirstRun, emptyNoAccess, error, loading | one copy per state — the 12 September offline sync is the model |
| state wording | loyalty (WEB-043 ↔ GST-036) | 5 state(s) worded differently: emptyFirstRun, emptyNoAccess, emptyNoResults, error, loading | one copy per state — the 12 September offline sync is the model |
| state wording | memberships (WEB-022/WEB-023 ↔ GST-015) | 4 state(s) worded differently: emptyFirstRun, emptyNoResults, error, loading | one copy per state — the 12 September offline sync is the model |
| state wording | menu-item (WEB-037 ↔ GST-061) | 5 state(s) worded differently: emptyFirstRun, emptyNoAccess, emptyNoResults, error, loading | one copy per state — the 12 September offline sync is the model |
| state wording | newsletter (WEB-027 ↔ GST-065) | 4 state(s) worded differently: emptyFirstRun, emptyNoResults, error, loading | one copy per state — the 12 September offline sync is the model |
| state wording | order-tracking (WEB-038 ↔ GST-025) | 5 state(s) worded differently: emptyFirstRun, emptyNoAccess, emptyNoResults, error, loading | one copy per state — the 12 September offline sync is the model |
| state wording | parking (WEB-041 ↔ GST-027/GST-028) | 5 state(s) worded differently: emptyFirstRun, emptyNoAccess, emptyNoResults, error, loading | one copy per state — the 12 September offline sync is the model |
| state wording | privacy-security-devices (WEB-024 ↔ GST-066/GST-073) | 4 state(s) worded differently: emptyFirstRun, emptyNoResults, error, loading | one copy per state — the 12 September offline sync is the model |
| state wording | profile (WEB-020 ↔ GST-039) | 3 state(s) worded differently: emptyFirstRun, error, loading | one copy per state — the 12 September offline sync is the model |
| state wording | reservations (WEB-031 ↔ GST-016/GST-017) | 4 state(s) worded differently: emptyFirstRun, emptyNoResults, error, loading | one copy per state — the 12 September offline sync is the model |
| state wording | search (WEB-003 ↔ GST-063) | 4 state(s) worded differently: emptyFirstRun, emptyNoResults, error, loading | one copy per state — the 12 September offline sync is the model |
| state wording | shop (WEB-033 ↔ GST-026) | 4 state(s) worded differently: emptyFirstRun, emptyNoResults, error, loading | one copy per state — the 12 September offline sync is the model |
| state wording | shop-and-drop (WEB-042 ↔ GST-062) | 4 state(s) worded differently: emptyFirstRun, emptyNoAccess, error, loading | one copy per state — the 12 September offline sync is the model |
| state wording | sign-in (WEB-016 ↔ GST-042) | 4 state(s) worded differently: emptyFirstRun, emptyNoResults, error, loading | one copy per state — the 12 September offline sync is the model |
| state wording | system-states (WEB-029 ↔ GST-047) | 4 state(s) worded differently: emptyFirstRun, emptyNoResults, error, loading | one copy per state — the 12 September offline sync is the model |
| state wording | ticket-selection (WEB-005 ↔ GST-008) | 3 state(s) worded differently: emptyFirstRun, error, loading | one copy per state — the 12 September offline sync is the model |
| state wording | ticket-transfer (WEB-030 ↔ GST-014/GST-045) | 4 state(s) worded differently: emptyFirstRun, emptyNoResults, error, loading | one copy per state — the 12 September offline sync is the model |
| state wording | tickets (WEB-018 ↔ GST-012/GST-013) | 4 state(s) worded differently: emptyFirstRun, emptyNoResults, error, loading | one copy per state — the 12 September offline sync is the model |
| state wording | venue-info (WEB-028 ↔ GST-029) | 4 state(s) worded differently: emptyFirstRun, emptyNoResults, error, loading | one copy per state — the 12 September offline sync is the model |
| state wording | venue-map-and-wait-times (WEB-039 ↔ GST-021/GST-022) | 5 state(s) worded differently: emptyFirstRun, emptyNoAccess, emptyNoResults, error, loading | one copy per state — the 12 September offline sync is the model |
| state wording | virtual-queue (WEB-040 ↔ GST-023) | 5 state(s) worded differently: emptyFirstRun, emptyNoAccess, emptyNoResults, error, loading | one copy per state — the 12 September offline sync is the model |
| state wording | waiting-room (WEB-015 ↔ GST-046) | 3 state(s) worded differently: emptyFirstRun, error, loading | one copy per state — the 12 September offline sync is the model |
| state wording | wallet-and-payment-methods (WEB-021 ↔ GST-011/GST-071) | 4 state(s) worded differently: emptyFirstRun, emptyNoResults, error, loading | one copy per state — the 12 September offline sync is the model |
| state wording | wishlist (WEB-009 ↔ GST-020) | 4 state(s) worded differently: emptyFirstRun, emptyNoResults, error, loading | one copy per state — the 12 September offline sync is the model |

## Info — 4

| Dimension | Where | Difference | Resolve by |
|---|---|---|---|
| coverage | dynamic-qr-ticket | GST-055 Dynamic QR Ticket — app only (deliberate). The 2 September session decided a dynamic-QR ticket bought on the web is redirected into the app, because a credential that needs a network round trip at a gate fails at the gate (_components.yaml, credentialPresenter). |  |
| coverage | face-pass | GST-069 Face Pass — app only (deliberate). enrolFacePass needs a camera and a liveness check (apply-web-parity.py). Viewing and revoking an enrolment are on the web's Devices, Wishlist & Consent. Not callable on the web: enrolFacePass. |  |
| operations | app only | enrolFacePass — camera and liveness, deliberate (apply-web-parity.py) |  |
| wave | multi-currency (WEB-035 ↔ GST-044) | ships in wave 1 on the web and wave 2 on the app — sanctioned: CF-111 — web is Wave 1 because that is where an overseas guest compares before booking, and the app is Wave 2 because that is where they check after. |  |

## Capability groups

| Group | Kind | Web | App |
|---|---|---|---|
| home | paired | WEB-001 | GST-001 |
| browse | paired | WEB-002 | GST-002, GST-003, GST-005 |
| search | paired | WEB-003 | GST-063 |
| detail | paired | WEB-004 | GST-004, GST-006 |
| ticket-selection | paired | WEB-005 | GST-008 |
| date-and-session | paired | WEB-006 | GST-007 |
| seat-selection | paired | WEB-007 | GST-049 |
| add-ons | paired | WEB-008 | GST-048, GST-056 |
| wishlist | paired | WEB-009 | GST-020 |
| waiting-room | paired | WEB-015 | GST-046 |
| cart | paired | WEB-010 | GST-041 |
| checkout-and-payment | paired | WEB-011, WEB-012, WEB-014 | GST-009 |
| confirmation | paired | WEB-013 | GST-010 |
| sign-in | paired | WEB-016 | GST-042 |
| account-hub | webOnly · raise | WEB-017 | — |
| tickets | paired | WEB-018 | GST-012, GST-013 |
| order-history | paired | WEB-019 | GST-019 |
| profile | paired | WEB-020 | GST-039 |
| privacy-security-devices | paired | WEB-024 | GST-066, GST-073 |
| ticket-transfer | paired | WEB-030 | GST-014, GST-045 |
| reservations | paired | WEB-031 | GST-016, GST-017 |
| refunds-and-resale | folded | — | GST-067 |
| share-and-group-booking | folded | — | GST-072 |
| add-to-calendar | appOnly · gap | — | GST-018 |
| dynamic-qr-ticket | appOnly · deliberate | — | GST-055 |
| face-pass | appOnly · deliberate | — | GST-069 |
| wallet-and-payment-methods | paired | WEB-021 | GST-011, GST-071 |
| memberships | paired | WEB-022, WEB-023 | GST-015 |
| loyalty | paired | WEB-043 | GST-036 |
| offers | paired | WEB-032 | GST-037 |
| multi-currency | paired | WEB-035 | GST-044 |
| venue-map-and-wait-times | paired | WEB-039 | GST-021, GST-022 |
| virtual-queue | paired | WEB-040 | GST-023 |
| fnb-order | paired | WEB-036 | GST-024 |
| menu-item | paired | WEB-037 | GST-061 |
| order-tracking | paired | WEB-038 | GST-025 |
| parking | paired | WEB-041 | GST-027, GST-028 |
| shop | paired | WEB-033 | GST-026 |
| shop-and-drop | paired | WEB-042 | GST-062 |
| in-venue-notifications | paired | WEB-046 | GST-030 |
| venue-info | paired | WEB-028 | GST-029 |
| reserve-table-or-cabana | folded | — | GST-070 |
| digital-companion-mode | appOnly · raise | — | GST-038 |
| cabana-booking | appOnly · raise | — | GST-050, GST-058 |
| itinerary-planning | appOnly · raise | — | GST-051, GST-052, GST-053, GST-054, GST-059 |
| help-and-cases | paired | WEB-025 | GST-068 |
| help-content-and-accessibility | paired | WEB-045 | GST-040, GST-057 |
| lost-and-found | paired | WEB-034 | GST-034 |
| feedback | paired | WEB-026 | GST-035 |
| newsletter | paired | WEB-027 | GST-065 |
| ai-concierge | paired | WEB-044 | GST-031, GST-032, GST-033 |
| system-states | paired | WEB-029 | GST-047 |
| rtl-specimen | appOnly · raise | — | GST-043 |
