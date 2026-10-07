# Guest web and guest app — parity audit

**Derived.** `python3 tools/audit-guest-parity.py`, 2026-10-08. Reads only.

**The rule, decided 12 September 2026: guest web (P01) and guest app (P02) are identical.** Every difference below either has a reason recorded against it or is a defect waiting for a decision. Which web screen is which app screen is `screens/_guest-pairs.yaml`.

| | |
|---|---|
| Screens | P01 50 · P02 77 |
| Capability groups | 56 — appOnly 6 · folded 3 · paired 46 · webOnly 1 |
| Operations | web 213 · app 218 · shared 204 |
| Findings | high 29 · medium 165 · low 222 · info 3 |

## By dimension

| Dimension | high | medium | low | info |
|---|---|---|---|---|
| operations | 15 | 39 |  | 1 |
| licence | 10 |  |  |  |
| coverage | 2 | 4 | 2 | 2 |
| frontend manifest | 2 | 1 |  |  |
| bindings |  | 26 |  |  |
| entry parameters |  | 24 |  |  |
| states |  | 19 |  |  |
| flows |  | 13 |  |  |
| unbound operations |  | 12 | 21 |  |
| cross-shell handover |  | 8 |  |  |
| overlays |  | 7 |  |  |
| contracts |  | 5 |  |  |
| events |  | 2 |  |  |
| platform |  | 2 |  |  |
| design |  | 1 |  |  |
| documents |  | 1 | 3 |  |
| machine |  | 1 |  |  |
| capability code |  |  | 42 |  |
| components |  |  | 28 |  |
| layout split |  |  | 16 |  |
| naming |  |  | 15 |  |
| navigation |  |  | 43 |  |
| section |  |  | 11 |  |
| state wording |  |  | 41 |  |

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

## High — 29

| Dimension | Where | Difference | Resolve by |
|---|---|---|---|
| coverage | add-to-calendar | GST-018 Add to Calendar / Reminders — app only (gap). Adding a visit to a calendar is as much a desktop act as a phone one, and issueWalletPass is already on the web's My Tickets. Not callable on the web: getOrderCalendarEvent, getVisitReminder, setVisitReminder. | add the screen to the web |
| coverage | reserve-table-or-cabana | GST-070 Reserve a Table has no web screen; its operations are on WEB-031, WEB-036, WEB-040; **not callable on the web at all: listBookableOutlets** | draw the screen on the other shell, or record the fold as the decision |
| frontend manifest | frontend/guest-app.yaml | lists 80 screens against 77: missing 14 (GST-066, GST-067, GST-068, GST-069, GST-070, GST-071, GST-072, GST-073, GST-074, GST-075, GST-076, GST-077…); ghosts ['GST-060', 'GST-064']; 14 renamed, 43 in another wave | derive-frontend.py carries `screens`, `screenCount` and `byWave` over from the previous file (`e.setdefault` on every existing key) and never recomputes them — derive them |
| frontend manifest | frontend/guest-web.yaml | lists 35 screens against 50: missing 15 (WEB-036, WEB-037, WEB-038, WEB-039, WEB-040, WEB-041, WEB-042, WEB-043, WEB-044, WEB-045, WEB-046, WEB-047…); ghosts —; 7 renamed, 15 in another wave | derive-frontend.py carries `screens`, `screenCount` and `byWave` over from the previous file (`e.setdefault` on every existing key) and never recomputes them — derive them |
| licence | ai-concierge (WEB-044 ↔ GST-031/GST-032/GST-033) | web requires ['ai'], app requires ['ai', 'ticketing'] — a tenant licensed for one and not the other sees it on one shell only | one requiresModule for the capability |
| licence | checkout-and-payment (WEB-011/WEB-012/WEB-014 ↔ GST-009) | web requires ['marketing', 'ticketing'], app requires ['ticketing'] — a tenant licensed for one and not the other sees it on one shell only | one requiresModule for the capability |
| licence | help-content-and-accessibility (WEB-045 ↔ GST-040/GST-057) | web requires ['core'], app requires ['core', 'marketing'] — a tenant licensed for one and not the other sees it on one shell only | one requiresModule for the capability |
| licence | home (WEB-001 ↔ GST-001) | web requires ['ticketing'], app requires ['marketing'] — a tenant licensed for one and not the other sees it on one shell only | one requiresModule for the capability |
| licence | in-venue-notifications (WEB-046 ↔ GST-030) | web requires ['marketing'], app requires ['fnb'] — a tenant licensed for one and not the other sees it on one shell only | one requiresModule for the capability |
| licence | itinerary-planning (WEB-050 ↔ GST-051/GST-052/GST-053/GST-054/GST-059) | web requires ['ticketing'], app requires ['ai', 'ticketing'] — a tenant licensed for one and not the other sees it on one shell only | one requiresModule for the capability |
| licence | lost-and-found (WEB-034 ↔ GST-034) | web requires ['marketing'], app requires ['fnb'] — a tenant licensed for one and not the other sees it on one shell only | one requiresModule for the capability |
| licence | privacy-security-devices (WEB-024 ↔ GST-066/GST-073) | web requires ['marketing'], app requires ['core'] — a tenant licensed for one and not the other sees it on one shell only | one requiresModule for the capability |
| licence | venue-map-and-wait-times (WEB-039 ↔ GST-021/GST-022) | web requires ['queue'], app requires ['queue', 'seating'] — a tenant licensed for one and not the other sees it on one shell only | one requiresModule for the capability |
| licence | wallet-and-payment-methods (WEB-021 ↔ GST-011/GST-071) | web requires ['retail'], app requires ['core', 'retail'] — a tenant licensed for one and not the other sees it on one shell only | one requiresModule for the capability |
| operations | app only | bindCredentialDevice, claimTicketTransfer, createOrder, enrolFacePass, getOrderCalendarEvent, getTransportDeparture, getVisitReminder, grantDelegation, listBookableOutlets, listCatalogueBundles, listTicketTransfers, registerGuestDevice, reserveMerchandise, setVisitReminder |  |
| operations | cart (WEB-010 ↔ GST-041) | the web calls createCart, evaluatePromotions and the app cannot call it anywhere |  |
| operations | checkout-and-payment (WEB-011/WEB-012/WEB-014 ↔ GST-009) | the web calls extendSeatHold and the app cannot call it anywhere |  |
| operations | checkout-and-payment (WEB-011/WEB-012/WEB-014 ↔ GST-009) | the app calls createOrder and the web cannot call it anywhere |  |
| operations | itinerary-planning (WEB-050 ↔ GST-051/GST-052/GST-053/GST-054/GST-059) | the app calls listCatalogueBundles and the web cannot call it anywhere |  |
| operations | memberships (WEB-022/WEB-023 ↔ GST-015) | the app calls grantDelegation and the web cannot call it anywhere |  |
| operations | privacy-security-devices (WEB-024 ↔ GST-066/GST-073) | the web calls getWaiverStatus and the app cannot call it anywhere |  |
| operations | privacy-security-devices (WEB-024 ↔ GST-066/GST-073) | the app calls registerGuestDevice and the web cannot call it anywhere |  |
| operations | profile (WEB-020 ↔ GST-039) | the web calls getMyIdentityVerification, submitGuestIdentityDocument, updateGuestPreferences and the app cannot call it anywhere |  |
| operations | reservations (WEB-031 ↔ GST-016/GST-017) | the web calls getResourceAvailability and the app cannot call it anywhere |  |
| operations | shop (WEB-033 ↔ GST-026) | the app calls reserveMerchandise and the web cannot call it anywhere |  |
| operations | ticket-selection (WEB-005 ↔ GST-008) | the web calls evaluatePromotions and the app cannot call it anywhere |  |
| operations | ticket-transfer (WEB-030 ↔ GST-014/GST-045) | the app calls claimTicketTransfer, listTicketTransfers and the web cannot call it anywhere |  |
| operations | tickets (WEB-018 ↔ GST-012/GST-013) | the app calls bindCredentialDevice and the web cannot call it anywhere |  |
| operations | web only | createCart, evaluatePromotions, extendSeatHold, getMyChallenges, getMyIdentityVerification, getResourceAvailability, getWaiverStatus, submitGuestIdentityDocument, updateGuestPreferences |  |

## Medium — 165

| Dimension | Where | Difference | Resolve by |
|---|---|---|---|
| bindings | add-ons (WEB-008 ↔ GST-048/GST-056) | web shows ['BookingFlow'] only, app shows ['Cart'] only | bind both twins to the same schemas |
| bindings | ai-concierge (WEB-044 ↔ GST-031/GST-032/GST-033) | web shows — only, app shows ['Cart', 'GuestOrderStatus'] only | bind both twins to the same schemas |
| bindings | browse (WEB-002 ↔ GST-002/GST-003/GST-005) | web shows — only, app shows ['Performance'] only | bind both twins to the same schemas |
| bindings | cart (WEB-010 ↔ GST-041) | web shows ['CouponCode', 'PromotionEvaluation'] only, app shows — only | bind both twins to the same schemas |
| bindings | checkout-and-payment (WEB-011/WEB-012/WEB-014 ↔ GST-009) | web shows ['ConsentPurposeConfig'] only, app shows — only | bind both twins to the same schemas |
| bindings | date-and-session (WEB-006 ↔ GST-007) | web shows ['PerformanceAvailabilityPage'] only, app shows ['ProductCategory'] only | bind both twins to the same schemas |
| bindings | detail (WEB-004 ↔ GST-004/GST-006) | web shows — only, app shows ['VenuePoint'] only | bind both twins to the same schemas |
| bindings | fnb-order (WEB-036 ↔ GST-024) | web shows ['MyTableBooking'] only, app shows — only | bind both twins to the same schemas |
| bindings | help-and-cases (WEB-025 ↔ GST-068) | web shows ['PublishedFaqCategory'] only, app shows ['AiConversation'] only | bind both twins to the same schemas |
| bindings | help-content-and-accessibility (WEB-045 ↔ GST-040/GST-057) | web shows — only, app shows ['Case'] only | bind both twins to the same schemas |
| bindings | home (WEB-001 ↔ GST-001) | web shows ['HomepageLayout', 'Product'] only, app shows ['GuestProfile', 'PublishedTenantConfig'] only | bind both twins to the same schemas |
| bindings | memberships (WEB-022/WEB-023 ↔ GST-015) | web shows — only, app shows ['DelegatedAccess'] only | bind both twins to the same schemas |
| bindings | offers (WEB-032 ↔ GST-037) | web shows — only, app shows ['CouponCode'] only | bind both twins to the same schemas |
| bindings | parking (WEB-041 ↔ GST-027/GST-028) | web shows — only, app shows ['Entitlement', 'Order'] only | bind both twins to the same schemas |
| bindings | privacy-security-devices (WEB-024 ↔ GST-066/GST-073) | web shows ['DelegatedAccess', 'Entitlement', 'FacePassEnrolment', 'Wishlist'] only, app shows ['GuestSession'] only | bind both twins to the same schemas |
| bindings | reservations (WEB-031 ↔ GST-016/GST-017) | web shows ['GroupBooking', 'GroupPackageDefinition', 'MyTableBooking', 'ResourceAvailability'] only, app shows — only | bind both twins to the same schemas |
| bindings | search (WEB-003 ↔ GST-063) | web shows ['Product'] only, app shows — only | bind both twins to the same schemas |
| bindings | seat-selection (WEB-007 ↔ GST-049) | web shows ['BookingFlow'] only, app shows — only | bind both twins to the same schemas |
| bindings | shop (WEB-033 ↔ GST-026) | web shows ['MerchandiseItem'] only, app shows ['GuestMerchandiseItem'] only | bind both twins to the same schemas |
| bindings | shop-and-drop (WEB-042 ↔ GST-062) | web shows ['GuestMerchandiseItem'] only, app shows ['Entitlement'] only | bind both twins to the same schemas |
| bindings | ticket-selection (WEB-005 ↔ GST-008) | web shows ['PromotionEvaluation'] only, app shows ['Product'] only | bind both twins to the same schemas |
| bindings | ticket-transfer (WEB-030 ↔ GST-014/GST-045) | web shows — only, app shows ['Entitlement', 'TicketTransfer'] only | bind both twins to the same schemas |
| bindings | venue-info (WEB-028 ↔ GST-029) | web shows ['PublishedTenantConfig'] only, app shows ['DiningOutlet', 'VenueContact'] only | bind both twins to the same schemas |
| bindings | venue-map-and-wait-times (WEB-039 ↔ GST-021/GST-022) | web shows ['Queue'] only, app shows ['Product'] only | bind both twins to the same schemas |
| bindings | virtual-queue (WEB-040 ↔ GST-023) | web shows — only, app shows ['Queue'] only | bind both twins to the same schemas |
| bindings | wallet-and-payment-methods (WEB-021 ↔ GST-011/GST-071) | web shows — only, app shows ['ConsentPurposeConfig', 'PublishedTenantConfig', 'WalletAutoReloadSetting'] only | bind both twins to the same schemas |
| contracts | contracts/satellite/fnb.yaml:17 | x-ticvai-platforms names P02 and not P01 | name both guest shells |
| contracts | contracts/satellite/games.yaml:12 | x-ticvai-platforms names P02 and not P01 | name both guest shells |
| contracts | contracts/satellite/marketing-crm.yaml:21 | x-ticvai-platforms names P02 and not P01 | name both guest shells |
| contracts | contracts/satellite/queue.yaml:10 | x-ticvai-platforms names P02 and not P01 | name both guest shells |
| contracts | contracts/satellite/retail.yaml:10 | x-ticvai-platforms names P02 and not P01 | name both guest shells |
| coverage | account-hub | WEB-017 My Account Dashboard — web only (raise). The web has an account dashboard; the app reaches the same things from Home and Profile. A navigation difference rather than a capability one, but it is a difference. Not callable on the app: getMyChallenges. | ask the client whether it ships, then add it to both or remove it |
| coverage | cabana-booking | GST-050 Resource Booking – Cabana, GST-058 Resource Availability (Cabana) — app only (raise). Unsourced (guest-surface-parity.md). A resource sold as capacity, where the venue has no map: the guest buys the product and the unit is assigned (`bookResource` stays staff-only). **A cabana placed on a venue map is picked on the map** since 29 September (rev 3 REV3-15 and GAP-C2, superseding audit R073 (c) for those resources): that is the map-booking group, on both shells. | ask the client whether it ships, then add it to both or remove it |
| coverage | digital-companion-mode | GST-038 At the Venue — app only (raise). Unsourced (CF-92) — reads as a framing for the in-venue screens rather than a capability. "What is near you" lives here and nowhere on the web. | ask the client whether it ships, then add it to both or remove it |
| coverage | rtl-specimen | GST-043 Arabic / RTL Experience — app only (raise). Both platforms declare ltr and rtl. This screen calls nothing — it is a specimen of the Arabic layout, drawn for the app only. | ask the client whether it ships, then add it to both or remove it |
| cross-shell handover | help-content-and-accessibility (WEB-045 ↔ GST-040/GST-057) | GST-040 hands the guest to WEB-034 on the web — "They report something lost" (flow F54 step 2→3) | a twin exists on the same shell; hand over only where the device matters |
| cross-shell handover | lost-and-found (WEB-034 ↔ GST-034) | WEB-034 hands the guest to GST-034 on the app — "They track it" (flow F54 step 3→4) | a twin exists on the same shell; hand over only where the device matters |
| cross-shell handover | loyalty (WEB-043 ↔ GST-036) | GST-036 hands the guest to WEB-024 on the web — "They see rewards and manage their devices" (flow F53 step 1→2) | a twin exists on the same shell; hand over only where the device matters |
| cross-shell handover | privacy-security-devices (WEB-024 ↔ GST-066/GST-073) | WEB-024 hands the guest to GST-037 on the app — "Offers are shown against what they hold" (flow F53 step 2→3) | a twin exists on the same shell; hand over only where the device matters |
| cross-shell handover | shop (WEB-033 ↔ GST-026) | WEB-033 hands the guest to GST-062 on the app — "On the way out they find their collection point" (flow F51 step 2→3) | a twin exists on the same shell; hand over only where the device matters |
| cross-shell handover | sign-in (WEB-016 ↔ GST-042) | WEB-016 hands the guest to GST-039 on the app — "They set a profile" (flow F56 step 3→4) | a twin exists on the same shell; hand over only where the device matters |
| cross-shell handover | sign-in (WEB-016 ↔ GST-042) | GST-042 hands the guest to WEB-016 on the web — "A guest who checked out anonymously links their order" (flow F56 step 2→3) | a twin exists on the same shell; hand over only where the device matters |
| cross-shell handover | ticket-transfer (WEB-030 ↔ GST-014/GST-045) | WEB-030 hands the guest to GST-014 on the app — "The friend claims it in the app" (flow F55 step 4→5) | a twin exists on the same shell; hand over only where the device matters |
| design | Claude Design | web 14/14 batches drawn, app 19/19 — the web is designed and the app is generated boxes, and the only app reference (TICVAI_Mobile.dc.html) uses a different design system from the drawn web frames | draw the app batches against the web's house style, or decide which system is the guest's |
| documents | docs/active/mom-digest.md:3908 | "can differ in functionality" — a client minute says web and app may differ — the 12 September rule says they do not; worth confirming with the client | confirm with the client |
| entry parameters | add-ons (WEB-008 ↔ GST-048/GST-056) | web opens with ['bundleId', 'cartId', 'venueId'], app with ['bundleId', 'cartId'] — one shared link cannot open both | one deep-link shape per capability |
| entry parameters | ai-concierge (WEB-044 ↔ GST-031/GST-032/GST-033) | web opens with ['conversationId', 'messageId', 'outletId'], app with ['cartId', 'conversationId', 'messageId', 'orderId', 'outletId'] — one shared link cannot open both | one deep-link shape per capability |
| entry parameters | cart (WEB-010 ↔ GST-041) | web opens with ['cartId', 'code', 'holdId', 'lineId', 'performanceId', 'venueId'], app with ['cartId', 'holdId', 'lineId', 'performanceId', 'productId', 'venueId'] — one shared link cannot open both | one deep-link shape per capability |
| entry parameters | checkout-and-payment (WEB-011/WEB-012/WEB-014 ↔ GST-009) | web opens with ['cartId', 'holdId', 'orderId', 'paymentId', 'subjectId', 'token', 'venueId'], app with ['cartId', 'orderId', 'paymentId', 'token', 'venueId'] — one shared link cannot open both | one deep-link shape per capability |
| entry parameters | date-and-session (WEB-006 ↔ GST-007) | web opens with ['cartId', 'eventId', 'performanceId', 'venueId'], app with ['cartId', 'eventId', 'venueId'] — one shared link cannot open both | one deep-link shape per capability |
| entry parameters | detail (WEB-004 ↔ GST-004/GST-006) | web opens with ['eventId', 'productId'], app with ['bundleId', 'eventId', 'mapId', 'performanceId', 'productId'] — one shared link cannot open both | one deep-link shape per capability |
| entry parameters | fnb-order (WEB-036 ↔ GST-024) | web opens with ['cartId', 'entryId', 'orderId', 'outletId', 'reservationId', 'venueId'], app with ['orderId', 'outletId', 'venueId'] — one shared link cannot open both | one deep-link shape per capability |
| entry parameters | help-and-cases (WEB-025 ↔ GST-068) | web opens with ['caseId'], app with ['caseId', 'subjectId'] — one shared link cannot open both | one deep-link shape per capability |
| entry parameters | help-content-and-accessibility (WEB-045 ↔ GST-040/GST-057) | web opens with —, app with ['caseId'] — one shared link cannot open both | one deep-link shape per capability |
| entry parameters | home (WEB-001 ↔ GST-001) | web opens with —, app with ['subjectId'] — one shared link cannot open both | one deep-link shape per capability |
| entry parameters | itinerary-planning (WEB-050 ↔ GST-051/GST-052/GST-053/GST-054/GST-059) | web opens with ['itemId', 'planId', 'venueId'], app with ['cartId', 'conversationId', 'itemId', 'planId', 'venueId'] — one shared link cannot open both | one deep-link shape per capability |
| entry parameters | memberships (WEB-022/WEB-023 ↔ GST-015) | web opens with ['caseId', 'orderId', 'productId', 'statementId', 'subjectId'], app with ['caseId', 'guestLinkId', 'statementId', 'subjectId'] — one shared link cannot open both | one deep-link shape per capability |
| entry parameters | newsletter (WEB-027 ↔ GST-065) | web opens with ['subjectId', 'unsubscribeToken'], app with ['subjectId'] — one shared link cannot open both | one deep-link shape per capability |
| entry parameters | offers (WEB-032 ↔ GST-037) | web opens with ['promotionId'], app with ['code', 'promotionId'] — one shared link cannot open both | one deep-link shape per capability |
| entry parameters | order-tracking (WEB-038 ↔ GST-025) | web opens with ['orderId', 'sessionId', 'subjectId', 'venueId'], app with ['orderId', 'sessionId'] — one shared link cannot open both | one deep-link shape per capability |
| entry parameters | parking (WEB-041 ↔ GST-027/GST-028) | web opens with ['cartId', 'entitlementId', 'venueId'], app with ['cartId', 'entitlementId', 'orderId', 'subjectId'] — one shared link cannot open both | one deep-link shape per capability |
| entry parameters | privacy-security-devices (WEB-024 ↔ GST-066/GST-073) | web opens with ['deviceId', 'enrolmentId', 'itemId', 'methodId', 'subjectId'], app with ['challengeId', 'deviceId', 'methodId', 'subjectId'] — one shared link cannot open both | one deep-link shape per capability |
| entry parameters | reservations (WEB-031 ↔ GST-016/GST-017) | web opens with ['groupBookingId', 'productId', 'reservationId', 'resourceId', 'subjectId'], app with ['reservationId', 'subjectId'] — one shared link cannot open both | one deep-link shape per capability |
| entry parameters | seat-selection (WEB-007 ↔ GST-049) | web opens with ['eventId', 'holdId', 'performanceId', 'venueId'], app with ['eventId', 'holdId', 'performanceId'] — one shared link cannot open both | one deep-link shape per capability |
| entry parameters | shop-and-drop (WEB-042 ↔ GST-062) | web opens with ['cartId', 'outletId'], app with ['subjectId'] — one shared link cannot open both | one deep-link shape per capability |
| entry parameters | ticket-selection (WEB-005 ↔ GST-008) | web opens with ['cartId', 'productId', 'venueId'], app with ['cartId', 'performanceId', 'productId', 'venueId'] — one shared link cannot open both | one deep-link shape per capability |
| entry parameters | tickets (WEB-018 ↔ GST-012/GST-013) | web opens with ['entitlementId', 'orderId', 'subjectId'], app with ['credentialId', 'entitlementId', 'orderId', 'subjectId'] — one shared link cannot open both | one deep-link shape per capability |
| entry parameters | transport (WEB-049 ↔ GST-076/GST-077/GST-078/GST-079) | web opens with ['cartId', 'favouriteId', 'routeId'], app with ['cartId', 'departureId', 'favouriteId', 'routeId', 'subjectId'] — one shared link cannot open both | one deep-link shape per capability |
| entry parameters | venue-info (WEB-028 ↔ GST-029) | web opens with —, app with ['venueId'] — one shared link cannot open both | one deep-link shape per capability |
| events | events/storefront-sessionEvent.yaml | consumed by guest-app only | both guest shells render the content this event invalidates |
| events | events/whitelabel-contentPublished.yaml | consumed by guest-app only | both guest shells render the content this event invalidates |
| flows | F01 | "Guest buys a ticket online" walks web screens only, though its capabilities exist on the app (cart, checkout-and-payment, confirmation, date-and-session, detail, home) | name both platforms, or say why the journey is one shell's |
| flows | F02 | "Guest buys seated tickets" walks web screens only, though its capabilities exist on the app (cart, checkout-and-payment, date-and-session, seat-selection) | name both platforms, or say why the journey is one shell's |
| flows | F11 | "Guest orders food to a lounger" walks app screens only, though its capabilities exist on the web (checkout-and-payment, fnb-order, order-tracking) | name both platforms, or say why the journey is one shell's |
| flows | F17 | "A guest buys merchandise and collects later" walks app screens only, though its capabilities exist on the web (shop-and-drop) | name both platforms, or say why the journey is one shell's |
| flows | F18 | "A guest plays an arcade game" walks app screens only, though its capabilities exist on the web (wallet-and-payment-methods) | name both platforms, or say why the journey is one shell's |
| flows | F19 | "A membership works in another country" walks app screens only, though its capabilities exist on the web (memberships) | name both platforms, or say why the journey is one shell's |
| flows | F21 | "A ride queue fills and a guest is redirected" walks app screens only, though its capabilities exist on the web (browse, venue-map-and-wait-times) | name both platforms, or say why the journey is one shell's |
| flows | F25 | "A guest rents a cabana" walks app screens only, though its capabilities exist on the web (venue-map-and-wait-times) | name both platforms, or say why the journey is one shell's |
| flows | F26 | "A venue maps its site" walks app screens only, though its capabilities exist on the web (venue-map-and-wait-times) | name both platforms, or say why the journey is one shell's |
| flows | F48 | "A guest finds it, queues for it, and eats" walks app screens only, though its capabilities exist on the web (fnb-order, order-tracking, venue-map-and-wait-times, virtual-queue) | name both platforms, or say why the journey is one shell's |
| flows | F49 | "A guest plans a day and follows it" walks app screens only, though its capabilities exist on the web (cart, itinerary-planning) | name both platforms, or say why the journey is one shell's |
| flows | F50 | "A guest arrives, parks, and gets in" walks app screens only, though its capabilities exist on the web (checkout-and-payment, dynamic-qr-ticket, parking, tickets) | name both platforms, or say why the journey is one shell's |
| flows | F52 | "A guest books a cabana and uses it" walks app screens only, though its capabilities exist on the web (map-booking, reservations) | name both platforms, or say why the journey is one shell's |
| frontend manifest | frontend/guest-app.yaml | also carries KSK screens — the kiosk (reactWeb) ships inside the reactNative guest app while the web, the app's sibling, ships separately | decide whether TICVAI Guest is one codebase or three |
| machine | itinerary-planning (WEB-050 ↔ GST-051/GST-052/GST-053/GST-054/GST-059) | declared on the app only |  |
| operations | add-ons (WEB-008 ↔ GST-048/GST-056) | the web calls getPublishedBookingFlow here; the app calls getPublishedBookingFlow on GST-007/GST-008/GST-009/GST-041 | same operations on the same capability, so a guest finds it in the same place |
| operations | add-ons (WEB-008 ↔ GST-048/GST-056) | the app calls getCart here; the web calls getCart on WEB-006/WEB-010/WEB-011 | same operations on the same capability, so a guest finds it in the same place |
| operations | ai-concierge (WEB-044 ↔ GST-031/GST-032/GST-033) | the app calls addCartLine, checkoutCart, createGuestFnbOrder, getCart, getGuestOrderStatus here; the web calls addCartLine on WEB-005/WEB-006/WEB-008/WEB-010/WEB-033/WEB-036/WEB-041/WEB-042/WEB-047/WEB-048/WEB-049; checkoutCart on WEB-010/WEB-012/WEB-033; createGuestFnbOrder on WEB-036; getCart on WEB-006/WEB-010/WEB-011; getGuestOrderStatus on WEB-036/WEB-038 | same operations on the same capability, so a guest finds it in the same place |
| operations | cart (WEB-010 ↔ GST-041) | the web calls addCartLine, getCouponCode here; the app calls addCartLine on GST-007/GST-008/GST-026/GST-027/GST-032/GST-048/GST-050/GST-056/GST-070/GST-074/GST-075/GST-077/GST-078; getCouponCode on GST-037 | same operations on the same capability, so a guest finds it in the same place |
| operations | cart (WEB-010 ↔ GST-041) | the app calls claimCart, listProductVariants here; the web calls claimCart on WEB-016; listProductVariants on WEB-005/WEB-048 | same operations on the same capability, so a guest finds it in the same place |
| operations | checkout-and-payment (WEB-011/WEB-012/WEB-014 ↔ GST-009) | the web calls getMyProfile, getOrder, listConsentPurposes, recordConsentAnswers, updateMyProfile here; the app calls getMyProfile on GST-001/GST-039; getOrder on GST-010/GST-018/GST-019/GST-028/GST-067; listConsentPurposes on GST-039/GST-065/GST-066/GST-071; recordConsentAnswers on GST-007; updateMyProfile on GST-039 | same operations on the same capability, so a guest finds it in the same place |
| operations | date-and-session (WEB-006 ↔ GST-007) | the web calls getPerformance here; the app calls getPerformance on GST-006/GST-041 | same operations on the same capability, so a guest finds it in the same place |
| operations | date-and-session (WEB-006 ↔ GST-007) | the app calls listProductCategories, listProducts here; the web calls listProductCategories on WEB-002/WEB-005; listProducts on WEB-001/WEB-002/WEB-003/WEB-005/WEB-022/WEB-035/WEB-048/WEB-050 | same operations on the same capability, so a guest finds it in the same place |
| operations | detail (WEB-004 ↔ GST-004/GST-006) | the app calls getBundle, getPerformance, getVenueMap here; the web calls getBundle on WEB-008; getPerformance on WEB-006/WEB-010; getVenueMap on WEB-039/WEB-047 | same operations on the same capability, so a guest finds it in the same place |
| operations | fnb-order (WEB-036 ↔ GST-024) | the web calls addCartLine, createTableReservation, joinRestaurantWaitlist, leaveRestaurantWaitlist, listMyTableReservations, updateTableReservation here; the app calls addCartLine on GST-007/GST-008/GST-026/GST-027/GST-032/GST-048/GST-050/GST-056/GST-070/GST-074/GST-075/GST-077/GST-078; createTableReservation on GST-070; joinRestaurantWaitlist on GST-070; leaveRestaurantWaitlist on GST-070; listMyTableReservations on GST-070; updateTableReservation on GST-070 | same operations on the same capability, so a guest finds it in the same place |
| operations | help-and-cases (WEB-025 ↔ GST-068) | the web calls getTenantAppStatus, listPublishedFaqs here; the app calls getTenantAppStatus on GST-001/GST-029/GST-038/GST-040/GST-047/GST-051; listPublishedFaqs on GST-040 | same operations on the same capability, so a guest finds it in the same place |
| operations | help-and-cases (WEB-025 ↔ GST-068) | the app calls listAiConversations here; the web calls listAiConversations on WEB-044 | same operations on the same capability, so a guest finds it in the same place |
| operations | help-content-and-accessibility (WEB-045 ↔ GST-040/GST-057) | the app calls listMyCases, raiseMyCase, replyToMyCase here; the web calls listMyCases on WEB-025/WEB-034; raiseMyCase on WEB-025/WEB-026/WEB-034; replyToMyCase on WEB-025/WEB-034 | same operations on the same capability, so a guest finds it in the same place |
| operations | home (WEB-001 ↔ GST-001) | the app calls getMyProfile, listProductCategories, searchCatalogue here; the web calls getMyProfile on WEB-011/WEB-020; listProductCategories on WEB-002/WEB-005; searchCatalogue on WEB-002/WEB-003 | same operations on the same capability, so a guest finds it in the same place |
| operations | itinerary-planning (WEB-050 ↔ GST-051/GST-052/GST-053/GST-054/GST-059) | the app calls createAiConversation, getCart, getWaitTimes, requestSuggestion, sendAiMessage here; the web calls createAiConversation on WEB-044; getCart on WEB-006/WEB-010/WEB-011; getWaitTimes on WEB-002/WEB-004/WEB-039/WEB-040; requestSuggestion on WEB-044; sendAiMessage on WEB-044 | same operations on the same capability, so a guest finds it in the same place |
| operations | memberships (WEB-022/WEB-023 ↔ GST-015) | the web calls getProduct here; the app calls getProduct on GST-004/GST-006 | same operations on the same capability, so a guest finds it in the same place |
| operations | memberships (WEB-022/WEB-023 ↔ GST-015) | the app calls listDelegations here; the web calls listDelegations on WEB-024 | same operations on the same capability, so a guest finds it in the same place |
| operations | offers (WEB-032 ↔ GST-037) | the app calls getCouponCode here; the web calls getCouponCode on WEB-010 | same operations on the same capability, so a guest finds it in the same place |
| operations | order-history (WEB-019 ↔ GST-019) | the web calls createRefundRequest here; the app calls createRefundRequest on GST-067 | same operations on the same capability, so a guest finds it in the same place |
| operations | parking (WEB-041 ↔ GST-027/GST-028) | the app calls getOrder, listMyEntitlements here; the web calls getOrder on WEB-012/WEB-013/WEB-019; listMyEntitlements on WEB-001/WEB-017/WEB-018/WEB-024 | same operations on the same capability, so a guest finds it in the same place |
| operations | privacy-security-devices (WEB-024 ↔ GST-066/GST-073) | the web calls getFacePassEnrolment, getWishlist, listDelegations, listMyEntitlements, revokeFacePass here; the app calls getFacePassEnrolment on GST-069; getWishlist on GST-020; listDelegations on GST-015/GST-069; listMyEntitlements on GST-001/GST-012/GST-028/GST-045/GST-055/GST-062/GST-069; revokeFacePass on GST-069 | same operations on the same capability, so a guest finds it in the same place |
| operations | privacy-security-devices (WEB-024 ↔ GST-066/GST-073) | the app calls createMfaChallenge, getGuestSession, guestLogout, verifyGuestEmail, verifyMfaChallenge here; the web calls createMfaChallenge on WEB-016; getGuestSession on WEB-016; guestLogout on WEB-016; verifyGuestEmail on WEB-013/WEB-020; verifyMfaChallenge on WEB-016 | same operations on the same capability, so a guest finds it in the same place |
| operations | profile (WEB-020 ↔ GST-039) | the web calls verifyGuestEmail here; the app calls verifyGuestEmail on GST-010/GST-073 | same operations on the same capability, so a guest finds it in the same place |
| operations | reservations (WEB-031 ↔ GST-016/GST-017) | the web calls getGroupBooking, getGroupPackageDefinition, listGroupPackages, listMyTableReservations, requestGroupBooking, updateTableReservation here; the app calls getGroupBooking on GST-072; getGroupPackageDefinition on GST-072; listGroupPackages on GST-072; listMyTableReservations on GST-070; requestGroupBooking on GST-072; updateTableReservation on GST-070 | same operations on the same capability, so a guest finds it in the same place |
| operations | search (WEB-003 ↔ GST-063) | the web calls listProducts here; the app calls listProducts on GST-001/GST-002/GST-003/GST-005/GST-007/GST-008/GST-015/GST-021/GST-038/GST-044/GST-050/GST-051/GST-052/GST-053/GST-075 | same operations on the same capability, so a guest finds it in the same place |
| operations | seat-selection (WEB-007 ↔ GST-049) | the web calls getPublishedBookingFlow here; the app calls getPublishedBookingFlow on GST-007/GST-008/GST-009/GST-041 | same operations on the same capability, so a guest finds it in the same place |
| operations | shop (WEB-033 ↔ GST-026) | the web calls checkoutCart, createPayment here; the app calls checkoutCart on GST-009/GST-032/GST-041; createPayment on GST-009 | same operations on the same capability, so a guest finds it in the same place |
| operations | shop-and-drop (WEB-042 ↔ GST-062) | the web calls addCartLine, listMerchandise here; the app calls addCartLine on GST-007/GST-008/GST-026/GST-027/GST-032/GST-048/GST-050/GST-056/GST-070/GST-074/GST-075/GST-077/GST-078; listMerchandise on GST-026 | same operations on the same capability, so a guest finds it in the same place |
| operations | shop-and-drop (WEB-042 ↔ GST-062) | the app calls listMyEntitlements here; the web calls listMyEntitlements on WEB-001/WEB-017/WEB-018/WEB-024 | same operations on the same capability, so a guest finds it in the same place |
| operations | sign-in (WEB-016 ↔ GST-042) | the web calls claimCart here; the app calls claimCart on GST-041 | same operations on the same capability, so a guest finds it in the same place |
| operations | ticket-transfer (WEB-030 ↔ GST-014/GST-045) | the web calls createResaleListing here; the app calls createResaleListing on GST-067 | same operations on the same capability, so a guest finds it in the same place |
| operations | ticket-transfer (WEB-030 ↔ GST-014/GST-045) | the app calls listMyEntitlements here; the web calls listMyEntitlements on WEB-001/WEB-017/WEB-018/WEB-024 | same operations on the same capability, so a guest finds it in the same place |
| operations | tickets (WEB-018 ↔ GST-012/GST-013) | the web calls issueWalletPass, shareEntitlement here; the app calls issueWalletPass on GST-018; shareEntitlement on GST-072 | same operations on the same capability, so a guest finds it in the same place |
| operations | venue-info (WEB-028 ↔ GST-029) | the web calls getPublishedTenantConfig here; the app calls getPublishedTenantConfig on GST-001/GST-043/GST-047/GST-071 | same operations on the same capability, so a guest finds it in the same place |
| operations | venue-info (WEB-028 ↔ GST-029) | the app calls getTenantAppStatus, listDeliveryLocations, listDiningOutlets here; the web calls getTenantAppStatus on WEB-001/WEB-025/WEB-029/WEB-045/WEB-050; listDeliveryLocations on WEB-036; listDiningOutlets on WEB-036 | same operations on the same capability, so a guest finds it in the same place |
| operations | venue-map-and-wait-times (WEB-039 ↔ GST-021/GST-022) | the web calls listQueues here; the app calls listQueues on GST-023 | same operations on the same capability, so a guest finds it in the same place |
| operations | venue-map-and-wait-times (WEB-039 ↔ GST-021/GST-022) | the app calls listProducts here; the web calls listProducts on WEB-001/WEB-002/WEB-003/WEB-005/WEB-022/WEB-035/WEB-048/WEB-050 | same operations on the same capability, so a guest finds it in the same place |
| operations | virtual-queue (WEB-040 ↔ GST-023) | the app calls listQueues here; the web calls listQueues on WEB-039 | same operations on the same capability, so a guest finds it in the same place |
| operations | wallet-and-payment-methods (WEB-021 ↔ GST-011/GST-071) | the app calls getPublishedTenantConfig, listConsentPurposes, redeemLoyaltyPoints here; the web calls getPublishedTenantConfig on WEB-001/WEB-028/WEB-029; listConsentPurposes on WEB-011/WEB-020/WEB-024/WEB-027; redeemLoyaltyPoints on WEB-043 | same operations on the same capability, so a guest finds it in the same place |
| overlays | ai-concierge (WEB-044 ↔ GST-031/GST-032/GST-033) | declared on the app only |  |
| overlays | checkout-and-payment (WEB-011/WEB-012/WEB-014 ↔ GST-009) | declared on the web only |  |
| overlays | fnb-order (WEB-036 ↔ GST-024) | declared on the web only |  |
| overlays | help-content-and-accessibility (WEB-045 ↔ GST-040/GST-057) | declared on the app only |  |
| overlays | home (WEB-001 ↔ GST-001) | declared on the app only |  |
| overlays | shop (WEB-033 ↔ GST-026) | declared on the app only |  |
| overlays | shop-and-drop (WEB-042 ↔ GST-062) | declared on the web only |  |
| platform | appShell | web null · app {"buyButton": "A persistent **Buy tickets** button on every screen, opening GST-003 Buy Tickets. Style from `NavigationC |  |
| platform | navigationSets | web null · app {"appTabs": {"destinations": ["GST-001", "GST-002", "GST-003", "GST-051", "GST-012", "GST-038"], "members": ["GST-001",  |  |
| states | add-ons (WEB-008 ↔ GST-048/GST-056) | web only —, app only ['emptyNoResults'] |  |
| states | cart (WEB-010 ↔ GST-041) | web only —, app only ['emptyNoResults'] |  |
| states | checkout-and-payment (WEB-011/WEB-012/WEB-014 ↔ GST-009) | web only ['emptyNoResults'], app only — |  |
| states | feedback (WEB-026 ↔ GST-035) | web only ['emptyNoAccess'], app only — |  |
| states | home (WEB-001 ↔ GST-001) | web only —, app only ['introVideo'] |  |
| states | in-venue-notifications (WEB-046 ↔ GST-030) | web only ['emptyNoAccess'], app only — |  |
| states | itinerary-planning (WEB-050 ↔ GST-051/GST-052/GST-053/GST-054/GST-059) | web only —, app only ['aiUnavailable'] |  |
| states | lost-and-found (WEB-034 ↔ GST-034) | web only ['emptyNoAccess'], app only — |  |
| states | order-tracking (WEB-038 ↔ GST-025) | web only ['emptyNoAccess'], app only — |  |
| states | profile (WEB-020 ↔ GST-039) | web only ['emptyNoResults'], app only — |  |
| states | search (WEB-003 ↔ GST-063) | web only ['emptyNoAccess'], app only — |  |
| states | seat-selection (WEB-007 ↔ GST-049) | web only ['emptyNoResults'], app only — |  |
| states | shop-and-drop (WEB-042 ↔ GST-062) | web only ['emptyNoResults'], app only — |  |
| states | system-states (WEB-029 ↔ GST-047) | web only —, app only ['forcedUpgrade'] |  |
| states | venue-info (WEB-028 ↔ GST-029) | web only ['emptyNoAccess'], app only ['emptyNoResults'] |  |
| states | venue-map-and-wait-times (WEB-039 ↔ GST-021/GST-022) | web only —, app only ['map3dUnavailable', 'weakGps'] |  |
| states | virtual-queue (WEB-040 ↔ GST-023) | web only ['emptyNoResults'], app only — |  |
| states | waiting-room (WEB-015 ↔ GST-046) | web only ['emptyNoAccess'], app only — |  |
| states | wishlist (WEB-009 ↔ GST-020) | web only ['emptyNoAccess'], app only — |  |
| unbound operations | ai-concierge (WEB-044 ↔ GST-031/GST-032/GST-033) | GST-032 declares recordAnswerFeedback and no component in its layout calls it; the twin binds or lacks recordAnswerFeedback | bind each to a component, or move it to the screen that calls it |
| unbound operations | cart (WEB-010 ↔ GST-041) | WEB-010 declares createCart, getResourceHold and no component in its layout calls them; the twin binds or lacks createCart | bind each to a component, or move it to the screen that calls it |
| unbound operations | checkout-and-payment (WEB-011/WEB-012/WEB-014 ↔ GST-009) | WEB-011 declares recordConsentAnswers and no component in its layout calls it; the twin binds or lacks recordConsentAnswers | bind each to a component, or move it to the screen that calls it |
| unbound operations | date-and-session (WEB-006 ↔ GST-007) | GST-007 declares addCartLine, checkBookingEligibility, getCart, recordConsentAnswers and no component in its layout calls them; the twin binds or lacks addCartLine | bind each to a component, or move it to the screen that calls it |
| unbound operations | fnb-order (WEB-036 ↔ GST-024) | WEB-036 declares addCartLine and no component in its layout calls it; the twin binds or lacks addCartLine | bind each to a component, or move it to the screen that calls it |
| unbound operations | itinerary-planning (WEB-050 ↔ GST-051/GST-052/GST-053/GST-054/GST-059) | GST-051 declares getWaitTimes and no component in its layout calls it; the twin binds or lacks getWaitTimes | bind each to a component, or move it to the screen that calls it |
| unbound operations | itinerary-planning (WEB-050 ↔ GST-051/GST-052/GST-053/GST-054/GST-059) | GST-053 declares getCart, listProducts and no component in its layout calls them; the twin binds or lacks getCart, listProducts | bind each to a component, or move it to the screen that calls it |
| unbound operations | itinerary-planning (WEB-050 ↔ GST-051/GST-052/GST-053/GST-054/GST-059) | GST-054 declares createAiConversation, requestSuggestion and no component in its layout calls them; the twin binds or lacks createAiConversation, requestSuggestion | bind each to a component, or move it to the screen that calls it |
| unbound operations | privacy-security-devices (WEB-024 ↔ GST-066/GST-073) | WEB-024 declares enrolMfaMethod, getCookieConsentRuntime, getDeviceConsentHistory, listPublishedTrackingTechnologies, recordDeviceConsent, removeMfaMethod, verifyMfaEnrolment and no component in its layout calls them; the twin binds or lacks enrolMfaMethod | bind each to a component, or move it to the screen that calls it |
| unbound operations | privacy-security-devices (WEB-024 ↔ GST-066/GST-073) | GST-073 declares createMfaChallenge, registerGuestDevice, removeMfaMethod, verifyMfaChallenge, verifyMfaEnrolment and no component in its layout calls them; the twin binds or lacks createMfaChallenge, registerGuestDevice, verifyMfaChallenge | bind each to a component, or move it to the screen that calls it |
| unbound operations | profile (WEB-020 ↔ GST-039) | WEB-020 declares getMyIdentityVerification, submitGuestIdentityDocument and no component in its layout calls them; the twin binds or lacks getMyIdentityVerification, submitGuestIdentityDocument | bind each to a component, or move it to the screen that calls it |
| unbound operations | wallet-and-payment-methods (WEB-021 ↔ GST-011/GST-071) | WEB-021 declares getWalletAutoReloadSetting, getWalletExitBalance, setWalletAutoReloadSetting, settleWalletAtExit and no component in its layout calls them; the twin binds or lacks setWalletAutoReloadSetting | bind each to a component, or move it to the screen that calls it |

## Low — 222

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
| capability code | itinerary-planning (WEB-050 ↔ GST-051/GST-052/GST-053/GST-054/GST-059) | web ['AI-35'], app ['AI-35', 'C02'] — traceability counts them as two |  |
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
| components | add-ons (WEB-008 ↔ GST-048/GST-056) | web only ['progressIndicator'], app only — (4 vs 5 components) |  |
| components | ai-concierge (WEB-044 ↔ GST-031/GST-032/GST-033) | web only —, app only ['dataTable'] (8 vs 22 components) |  |
| components | browse (WEB-002 ↔ GST-002/GST-003/GST-005) | web only ['multiSelect'], app only ['dataTable'] (9 vs 16 components) |  |
| components | cart (WEB-010 ↔ GST-041) | web only ['banner'], app only — (13 vs 12 components) |  |
| components | checkout-and-payment (WEB-011/WEB-012/WEB-014 ↔ GST-009) | web only ['cartPanel', 'secondaryButton', 'textField'], app only — (23 vs 11 components) |  |
| components | confirmation (WEB-013 ↔ GST-010) | web only ['banner'], app only — (9 vs 7 components) |  |
| components | date-and-session (WEB-006 ↔ GST-007) | web only ['detailPanel', 'primaryButton'], app only — (11 vs 10 components) |  |
| components | detail (WEB-004 ↔ GST-004/GST-006) | web only ['banner', 'datePicker', 'primaryButton'], app only ['seatMap'] (11 vs 13 components) |  |
| components | fnb-order (WEB-036 ↔ GST-024) | web only ['destructiveButton', 'secondaryButton'], app only — (15 vs 10 components) |  |
| components | help-content-and-accessibility (WEB-045 ↔ GST-040/GST-057) | web only —, app only ['primaryButton', 'secondaryButton'] (6 vs 9 components) |  |
| components | home (WEB-001 ↔ GST-001) | web only ['iconButton'], app only ['detailPanel', 'searchField'] (9 vs 11 components) |  |
| components | in-venue-notifications (WEB-046 ↔ GST-030) | web only ['detailPanel'], app only — (4 vs 3 components) |  |
| components | itinerary-planning (WEB-050 ↔ GST-051/GST-052/GST-053/GST-054/GST-059) | web only —, app only ['assistantPanel', 'cardList', 'dataTable', 'destructiveButton'] (18 vs 39 components) |  |
| components | memberships (WEB-022/WEB-023 ↔ GST-015) | web only —, app only ['primaryButton'] (10 vs 10 components) |  |
| components | menu-item (WEB-037 ↔ GST-061) | web only —, app only ['banner', 'selectField'] (1 vs 3 components) |  |
| components | newsletter (WEB-027 ↔ GST-065) | web only —, app only ['destructiveButton'] (5 vs 6 components) |  |
| components | order-history (WEB-019 ↔ GST-019) | web only ['datePicker'], app only — (9 vs 7 components) |  |
| components | privacy-security-devices (WEB-024 ↔ GST-066/GST-073) | web only ['confirmDialog', 'selectField'], app only — (19 vs 13 components) |  |
| components | profile (WEB-020 ↔ GST-039) | web only ['secondaryButton'], app only — (8 vs 6 components) |  |
| components | reservations (WEB-031 ↔ GST-016/GST-017) | web only ['confirmDialog', 'primaryButton', 'secondaryButton', 'selectField'], app only — (12 vs 5 components) |  |
| components | seat-selection (WEB-007 ↔ GST-049) | web only ['banner', 'primaryButton', 'progressIndicator'], app only — (9 vs 6 components) |  |
| components | shop (WEB-033 ↔ GST-026) | web only —, app only ['toggle'] (8 vs 8 components) |  |
| components | shop-and-drop (WEB-042 ↔ GST-062) | web only ['primaryButton', 'searchField', 'secondaryButton', 'selectField', 'toggle'], app only ['banner'] (7 vs 3 components) |  |
| components | ticket-selection (WEB-005 ↔ GST-008) | web only ['iconButton', 'selectField'], app only — (11 vs 8 components) |  |
| components | ticket-transfer (WEB-030 ↔ GST-014/GST-045) | web only ['secondaryButton'], app only ['banner', 'dataTable', 'textField'] (3 vs 8 components) |  |
| components | venue-info (WEB-028 ↔ GST-029) | web only —, app only ['cardList', 'selectField', 'toggle'] (1 vs 5 components) |  |
| components | wallet-and-payment-methods (WEB-021 ↔ GST-011/GST-071) | web only —, app only ['consentBlock', 'numberField', 'selectField', 'toggle'] (7 vs 15 components) |  |
| components | wishlist (WEB-009 ↔ GST-020) | web only ['confirmDialog'], app only — (5 vs 4 components) |  |
| coverage | refunds-and-resale | GST-067 Refunds & Resale has no web screen; its operations are on WEB-019, WEB-030 | draw the screen on the other shell, or record the fold as the decision |
| coverage | share-and-group-booking | GST-072 Share & Group Booking has no web screen; its operations are on WEB-017, WEB-018, WEB-031, WEB-043 | draw the screen on the other shell, or record the fold as the decision |
| documents | contracts/spine/catalogue.yaml:1160 | "browses by category and cannot search" — GST-063 Search exists since 17 August | rewrite to the 12 September rule |
| documents | docs/active/design-plan.md:267 | "guest-app surfaces are not" — P02 is offlineCapable: true | rewrite to the 12 September rule |
| documents | docs/registers/conflicts.md:145 | "stay app-only by design" — CF-93 predates WEB-036–046 and the 10 September decision | rewrite to the 12 September rule |
| layout split | add-ons (WEB-008 ↔ GST-048/GST-056) | 1 screen(s) on the web, 2 on the app: Add-ons & Upsell ↔ Upsell / Cross-Sell; Bundle Package | fine if deliberate; a builder should know it is one capability |
| layout split | ai-concierge (WEB-044 ↔ GST-031/GST-032/GST-033) | 1 screen(s) on the web, 3 on the app: AI Concierge – Home ↔ AI Concierge – Home; AI Concierge – Chat; AI Concierge – Contextual Help | fine if deliberate; a builder should know it is one capability |
| layout split | browse (WEB-002 ↔ GST-002/GST-003/GST-005) | 1 screen(s) on the web, 3 on the app: Event & Attraction Listing ↔ Explore; Buy Tickets; What's On | fine if deliberate; a builder should know it is one capability |
| layout split | checkout-and-payment (WEB-011/WEB-012/WEB-014 ↔ GST-009) | 3 screen(s) on the web, 1 on the app: Guest Details & Attendee Forms; Checkout — Payment; Pay for a Booking ↔ Review & Payment | fine if deliberate; a builder should know it is one capability |
| layout split | detail (WEB-004 ↔ GST-004/GST-006) | 1 screen(s) on the web, 2 on the app: Attraction Details ↔ Item Detail; Item Detail – Event / Exhibition | fine if deliberate; a builder should know it is one capability |
| layout split | help-content-and-accessibility (WEB-045 ↔ GST-040/GST-057) | 1 screen(s) on the web, 2 on the app: Help Centre & Accessibility ↔ Help & Support; Accessibility Information | fine if deliberate; a builder should know it is one capability |
| layout split | itinerary-planning (WEB-050 ↔ GST-051/GST-052/GST-053/GST-054/GST-059) | 1 screen(s) on the web, 5 on the app: Plan Your Visit ↔ Plan; Suggested Itineraries; Your Plan; AI Planner; Plan in Progress | fine if deliberate; a builder should know it is one capability |
| layout split | memberships (WEB-022/WEB-023 ↔ GST-015) | 2 screen(s) on the web, 1 on the app: Membership Plans; Membership Management ↔ Memberships | fine if deliberate; a builder should know it is one capability |
| layout split | parking (WEB-041 ↔ GST-027/GST-028) | 1 screen(s) on the web, 2 on the app: Parking – Reserve & Pay ↔ Parking – Reserve & Pay; Parking – Reservation Confirmed | fine if deliberate; a builder should know it is one capability |
| layout split | privacy-security-devices (WEB-024 ↔ GST-066/GST-073) | 1 screen(s) on the web, 2 on the app: Devices, Wishlist & Consent ↔ Privacy & My Data; Security & Sign-in | fine if deliberate; a builder should know it is one capability |
| layout split | reservations (WEB-031 ↔ GST-016/GST-017) | 1 screen(s) on the web, 2 on the app: My Reservations ↔ My Reservations; Reservation Details | fine if deliberate; a builder should know it is one capability |
| layout split | ticket-transfer (WEB-030 ↔ GST-014/GST-045) | 1 screen(s) on the web, 2 on the app: Ticket Transfer ↔ Ticket Transfer; Ticket Delivery & Sharing | fine if deliberate; a builder should know it is one capability |
| layout split | tickets (WEB-018 ↔ GST-012/GST-013) | 1 screen(s) on the web, 2 on the app: My Tickets ↔ My Tickets; Ticket Details | fine if deliberate; a builder should know it is one capability |
| layout split | transport (WEB-049 ↔ GST-076/GST-077/GST-078/GST-079) | 1 screen(s) on the web, 4 on the app: Transport — Route & Schedule ↔ Intercity Trip — Route & Schedule; Intercity Trip — Route & Passengers; Intercity Trip — Multi-trip Passes; Intercity Trip — Favourite Routes | fine if deliberate; a builder should know it is one capability |
| layout split | venue-map-and-wait-times (WEB-039 ↔ GST-021/GST-022) | 1 screen(s) on the web, 2 on the app: Venue Map & Wait Times ↔ Interactive Map; Attraction Wait Times | fine if deliberate; a builder should know it is one capability |
| layout split | wallet-and-payment-methods (WEB-021 ↔ GST-011/GST-071) | 1 screen(s) on the web, 2 on the app: Wallet & Gift Cards ↔ Wallet Overview; Payment Methods | fine if deliberate; a builder should know it is one capability |
| naming | cart (WEB-010 ↔ GST-041) | "Shopping Cart" ↔ "Checkout Entry" | one name for one journey (31 August rule) |
| naming | date-and-session (WEB-006 ↔ GST-007) | "Date & Performance Selection" ↔ "Select Date & Time" | one name for one journey (31 August rule) |
| naming | feedback (WEB-026 ↔ GST-035) | "Survey & Feedback" ↔ "Feedback & Ratings" | one name for one journey (31 August rule) |
| naming | help-and-cases (WEB-025 ↔ GST-068) | "Help Centre / FAQ" ↔ "Help & My Cases" | one name for one journey (31 August rule) |
| naming | home (WEB-001 ↔ GST-001) | "Home / Landing" ↔ "Home" | one name for one journey (31 August rule) |
| naming | newsletter (WEB-027 ↔ GST-065) | "Newsletter Subscription" ↔ "Newsletter & Preferences" | one name for one journey (31 August rule) |
| naming | profile (WEB-020 ↔ GST-039) | "Profile & Preferences" ↔ "Profile" | one name for one journey (31 August rule) |
| naming | search (WEB-003 ↔ GST-063) | "Search Results" ↔ "Explore – Search Results" | one name for one journey (31 August rule) |
| naming | shop (WEB-033 ↔ GST-026) | "Shop" ↔ "Retail / Merchandise" | one name for one journey (31 August rule) |
| naming | shop-and-drop (WEB-042 ↔ GST-062) | "Retail & Shop and Drop" ↔ "Shop & Drop Collection" | one name for one journey (31 August rule) |
| naming | sign-in (WEB-016 ↔ GST-042) | "Login / Register" ↔ "Simple Registration & OTP" | one name for one journey (31 August rule) |
| naming | system-states (WEB-029 ↔ GST-047) | "Error / Sold Out / Maintenance" ↔ "Maintenance / Upgrade Page" | one name for one journey (31 August rule) |
| naming | ticket-selection (WEB-005 ↔ GST-008) | "Ticket Type Selection" ↔ "Tickets & Add-ons" | one name for one journey (31 August rule) |
| naming | venue-info (WEB-028 ↔ GST-029) | "Contact & Venue Information" ↔ "Venue Info & Services" | one name for one journey (31 August rule) |
| naming | wishlist (WEB-009 ↔ GST-020) | "Wishlist" ↔ "Saved Items / Wishlist" | one name for one journey (31 August rule) |
| navigation | add-ons (WEB-008 ↔ GST-048/GST-056) | leads on to ['date-and-session', 'sign-in', 'ticket-selection'] on the web only and ['browse'] on the app only |  |
| navigation | ai-concierge (WEB-044 ↔ GST-031/GST-032/GST-033) | leads on to — on the web only and ['browse'] on the app only |  |
| navigation | browse (WEB-002 ↔ GST-002/GST-003/GST-005) | leads on to — on the web only and ['add-ons', 'date-and-session', 'map-booking', 'space-by-the-hour'] on the app only |  |
| navigation | cart (WEB-010 ↔ GST-041) | leads on to ['confirmation', 'ticket-transfer'] on the web only and ['browse', 'itinerary-planning'] on the app only |  |
| navigation | checkout-and-payment (WEB-011/WEB-012/WEB-014 ↔ GST-009) | leads on to ['cart', 'sign-in'] on the web only and ['browse', 'parking'] on the app only |  |
| navigation | confirmation (WEB-013 ↔ GST-010) | leads on to ['cart', 'checkout-and-payment', 'tickets'] on the web only and ['browse'] on the app only |  |
| navigation | date-and-session (WEB-006 ↔ GST-007) | leads on to ['add-ons', 'cart'] on the web only and ['browse'] on the app only |  |
| navigation | detail (WEB-004 ↔ GST-004/GST-006) | leads on to ['search'] on the web only and ['add-ons', 'digital-companion-mode'] on the app only |  |
| navigation | feedback (WEB-026 ↔ GST-035) | leads on to ['help-and-cases', 'newsletter', 'venue-info'] on the web only and ['browse'] on the app only |  |
| navigation | fnb-order (WEB-036 ↔ GST-024) | leads on to — on the web only and ['browse', 'checkout-and-payment', 'order-tracking'] on the app only |  |
| navigation | help-and-cases (WEB-025 ↔ GST-068) | leads on to ['feedback', 'home', 'newsletter', 'venue-info'] on the web only and ['profile'] on the app only |  |
| navigation | help-content-and-accessibility (WEB-045 ↔ GST-040/GST-057) | leads on to — on the web only and ['browse'] on the app only |  |
| navigation | home (WEB-001 ↔ GST-001) | leads on to ['account-hub', 'newsletter', 'privacy-security-devices'] on the web only and ['add-to-calendar', 'cabana-booking', 'cart', 'checkout-and-payment', 'confirmation', 'date-and-session', 'digital-companion-mode', 'dynamic-qr-ticket', 'multi-currency', 'reservations', 'reserve-table-or-cabana', 'rtl-specimen', 'seat-selection', 'ticket-selection', 'ticket-transfer'] on the app only |  |
| navigation | in-venue-notifications (WEB-046 ↔ GST-030) | leads on to — on the web only and ['ai-concierge', 'browse'] on the app only |  |
| navigation | itinerary-planning (WEB-050 ↔ GST-051/GST-052/GST-053/GST-054/GST-059) | leads on to ['detail'] on the web only and ['add-ons', 'digital-companion-mode'] on the app only |  |
| navigation | lost-and-found (WEB-034 ↔ GST-034) | leads on to — on the web only and ['browse'] on the app only |  |
| navigation | loyalty (WEB-043 ↔ GST-036) | leads on to — on the web only and ['browse'] on the app only |  |
| navigation | map-booking (WEB-047 ↔ GST-074) | leads on to ['add-ons'] on the web only and ['reservations'] on the app only |  |
| navigation | memberships (WEB-022/WEB-023 ↔ GST-015) | leads on to ['privacy-security-devices', 'wallet-and-payment-methods'] on the web only and ['browse'] on the app only |  |
| navigation | menu-item (WEB-037 ↔ GST-061) | leads on to — on the web only and ['cart', 'fnb-order'] on the app only |  |
| navigation | multi-currency (WEB-035 ↔ GST-044) | leads on to ['reservations', 'ticket-transfer'] on the web only and ['browse'] on the app only |  |
| navigation | newsletter (WEB-027 ↔ GST-065) | leads on to ['feedback', 'help-and-cases', 'venue-info'] on the web only and — on the app only |  |
| navigation | offers (WEB-032 ↔ GST-037) | leads on to — on the web only and ['browse', 'wallet-and-payment-methods'] on the app only |  |
| navigation | order-history (WEB-019 ↔ GST-019) | leads on to ['account-hub', 'sign-in', 'tickets'] on the web only and ['browse', 'refunds-and-resale'] on the app only |  |
| navigation | order-tracking (WEB-038 ↔ GST-025) | leads on to — on the web only and ['browse', 'in-venue-notifications', 'virtual-queue'] on the app only |  |
| navigation | parking (WEB-041 ↔ GST-027/GST-028) | leads on to — on the web only and ['browse', 'checkout-and-payment', 'tickets'] on the app only |  |
| navigation | privacy-security-devices (WEB-024 ↔ GST-066/GST-073) | leads on to ['home', 'memberships', 'wallet-and-payment-methods'] on the web only and ['profile'] on the app only |  |
| navigation | profile (WEB-020 ↔ GST-039) | leads on to ['account-hub', 'sign-in', 'tickets'] on the web only and ['browse', 'face-pass', 'newsletter', 'privacy-security-devices', 'wallet-and-payment-methods'] on the app only |  |
| navigation | reservations (WEB-031 ↔ GST-016/GST-017) | leads on to ['multi-currency', 'ticket-transfer'] on the web only and ['browse'] on the app only |  |
| navigation | seat-selection (WEB-007 ↔ GST-049) | leads on to ['add-ons', 'date-and-session'] on the web only and ['browse'] on the app only |  |
| navigation | shop (WEB-033 ↔ GST-026) | leads on to — on the web only and ['browse', 'cart'] on the app only |  |
| navigation | shop-and-drop (WEB-042 ↔ GST-062) | leads on to ['cart'] on the web only and — on the app only |  |
| navigation | sign-in (WEB-016 ↔ GST-042) | leads on to ['account-hub', 'checkout-and-payment', 'order-history', 'tickets'] on the web only and ['browse'] on the app only |  |
| navigation | system-states (WEB-029 ↔ GST-047) | leads on to — on the web only and ['browse'] on the app only |  |
| navigation | ticket-selection (WEB-005 ↔ GST-008) | leads on to ['add-ons', 'seat-selection'] on the web only and ['share-and-group-booking'] on the app only |  |
| navigation | ticket-transfer (WEB-030 ↔ GST-014/GST-045) | leads on to ['multi-currency', 'reservations'] on the web only and ['browse'] on the app only |  |
| navigation | tickets (WEB-018 ↔ GST-012/GST-013) | leads on to ['account-hub', 'order-history', 'sign-in'] on the web only and ['browse', 'dynamic-qr-ticket'] on the app only |  |
| navigation | venue-info (WEB-028 ↔ GST-029) | leads on to ['feedback', 'help-and-cases', 'newsletter'] on the web only and ['browse'] on the app only |  |
| navigation | venue-map-and-wait-times (WEB-039 ↔ GST-021/GST-022) | leads on to — on the web only and ['browse', 'itinerary-planning', 'virtual-queue'] on the app only |  |
| navigation | virtual-queue (WEB-040 ↔ GST-023) | leads on to — on the web only and ['browse', 'fnb-order'] on the app only |  |
| navigation | waiting-room (WEB-015 ↔ GST-046) | leads on to — on the web only and ['browse'] on the app only |  |
| navigation | wallet-and-payment-methods (WEB-021 ↔ GST-011/GST-071) | leads on to ['memberships', 'privacy-security-devices'] on the web only and ['browse', 'profile', 'wishlist'] on the app only |  |
| navigation | wishlist (WEB-009 ↔ GST-020) | leads on to ['date-and-session', 'ticket-selection'] on the web only and ['browse'] on the app only |  |
| section | help-content-and-accessibility (WEB-045 ↔ GST-040/GST-057) | web section ['Support'], app ['Discovery & Browse', 'Engagement & Support'] |  |
| section | itinerary-planning (WEB-050 ↔ GST-051/GST-052/GST-053/GST-054/GST-059) | web section ['Discovery & Browse'], app ['Engagement & Support'] |  |
| section | menu-item (WEB-037 ↔ GST-061) | web section ['In-venue Services'], app ['In-Venue Experience'] |  |
| section | newsletter (WEB-027 ↔ GST-065) | web section ['Engagement & Support'], app ['Marketing'] |  |
| section | privacy-security-devices (WEB-024 ↔ GST-066/GST-073) | web section ['Membership, Loyalty & Value'], app ['Account & Self-Service'] |  |
| section | search (WEB-003 ↔ GST-063) | web section ['Discovery & Browse'], app ['Discovery'] |  |
| section | shop-and-drop (WEB-042 ↔ GST-062) | web section ['Retail'], app ['In-Venue Experience'] |  |
| section | ticket-transfer (WEB-030 ↔ GST-014/GST-045) | web section ['Ticketing'], app ['Account & Self-Service', 'Ticketing'] |  |
| section | venue-info (WEB-028 ↔ GST-029) | web section ['Engagement & Support'], app ['In-venue Services'] |  |
| section | wallet-and-payment-methods (WEB-021 ↔ GST-011/GST-071) | web section ['Membership, Loyalty & Value'], app ['Account & Self-Service', 'Membership, Loyalty & Value'] |  |
| section | wishlist (WEB-009 ↔ GST-020) | web section ['Booking & Selection'], app ['Account & Self-Service'] |  |
| state wording | add-ons (WEB-008 ↔ GST-048/GST-056) | 4 state(s) worded differently: emptyFirstRun, emptyNoAccess, error, loading | one copy per state — the 12 September offline sync is the model |
| state wording | ai-concierge (WEB-044 ↔ GST-031/GST-032/GST-033) | 4 state(s) worded differently: emptyFirstRun, emptyNoResults, error, loading | one copy per state — the 12 September offline sync is the model |
| state wording | browse (WEB-002 ↔ GST-002/GST-003/GST-005) | 5 state(s) worded differently: emptyFirstRun, emptyNoAccess, emptyNoResults, error, loading | one copy per state — the 12 September offline sync is the model |
| state wording | cart (WEB-010 ↔ GST-041) | 4 state(s) worded differently: emptyFirstRun, emptyNoAccess, error, loading | one copy per state — the 12 September offline sync is the model |
| state wording | checkout-and-payment (WEB-011/WEB-012/WEB-014 ↔ GST-009) | 4 state(s) worded differently: emptyFirstRun, emptyNoAccess, error, loading | one copy per state — the 12 September offline sync is the model |
| state wording | date-and-session (WEB-006 ↔ GST-007) | 4 state(s) worded differently: emptyFirstRun, emptyNoAccess, error, loading | one copy per state — the 12 September offline sync is the model |
| state wording | detail (WEB-004 ↔ GST-004/GST-006) | 7 state(s) worded differently: emptyFirstRun, emptyNoAccess, emptyNoResults, error, loading, videoBuffering, videoUnavailable | one copy per state — the 12 September offline sync is the model |
| state wording | feedback (WEB-026 ↔ GST-035) | 3 state(s) worded differently: emptyFirstRun, error, loading | one copy per state — the 12 September offline sync is the model |
| state wording | fnb-order (WEB-036 ↔ GST-024) | 2 state(s) worded differently: error, loading | one copy per state — the 12 September offline sync is the model |
| state wording | help-and-cases (WEB-025 ↔ GST-068) | 4 state(s) worded differently: emptyFirstRun, emptyNoAccess, error, loading | one copy per state — the 12 September offline sync is the model |
| state wording | help-content-and-accessibility (WEB-045 ↔ GST-040/GST-057) | 5 state(s) worded differently: emptyFirstRun, emptyNoAccess, emptyNoResults, error, loading | one copy per state — the 12 September offline sync is the model |
| state wording | home (WEB-001 ↔ GST-001) | 5 state(s) worded differently: emptyFirstRun, emptyNoAccess, emptyNoResults, error, loading | one copy per state — the 12 September offline sync is the model |
| state wording | in-venue-notifications (WEB-046 ↔ GST-030) | 3 state(s) worded differently: emptyFirstRun, error, loading | one copy per state — the 12 September offline sync is the model |
| state wording | itinerary-planning (WEB-050 ↔ GST-051/GST-052/GST-053/GST-054/GST-059) | 6 state(s) worded differently: emptyFirstRun, emptyNoAccess, emptyNoResults, error, loading, preferenceNotAtVenue | one copy per state — the 12 September offline sync is the model |
| state wording | loyalty (WEB-043 ↔ GST-036) | 4 state(s) worded differently: emptyFirstRun, emptyNoResults, error, loading | one copy per state — the 12 September offline sync is the model |
| state wording | memberships (WEB-022/WEB-023 ↔ GST-015) | 5 state(s) worded differently: emptyFirstRun, emptyNoAccess, emptyNoResults, error, loading | one copy per state — the 12 September offline sync is the model |
| state wording | menu-item (WEB-037 ↔ GST-061) | 3 state(s) worded differently: emptyFirstRun, error, loading | one copy per state — the 12 September offline sync is the model |
| state wording | multi-currency (WEB-035 ↔ GST-044) | 1 state(s) worded differently: emptyNoAccess | one copy per state — the 12 September offline sync is the model |
| state wording | newsletter (WEB-027 ↔ GST-065) | 5 state(s) worded differently: emptyFirstRun, emptyNoAccess, emptyNoResults, error, loading | one copy per state — the 12 September offline sync is the model |
| state wording | offers (WEB-032 ↔ GST-037) | 1 state(s) worded differently: emptyNoAccess | one copy per state — the 12 September offline sync is the model |
| state wording | order-history (WEB-019 ↔ GST-019) | 3 state(s) worded differently: emptyFirstRun, emptyNoAccess, emptyNoResults | one copy per state — the 12 September offline sync is the model |
| state wording | order-tracking (WEB-038 ↔ GST-025) | 1 state(s) worded differently: error | one copy per state — the 12 September offline sync is the model |
| state wording | parking (WEB-041 ↔ GST-027/GST-028) | 6 state(s) worded differently: emptyFirstRun, emptyNoAccess, emptyNoResults, error, loading, soldOutForDay | one copy per state — the 12 September offline sync is the model |
| state wording | privacy-security-devices (WEB-024 ↔ GST-066/GST-073) | 5 state(s) worded differently: emptyFirstRun, emptyNoAccess, emptyNoResults, error, loading | one copy per state — the 12 September offline sync is the model |
| state wording | profile (WEB-020 ↔ GST-039) | 4 state(s) worded differently: emptyFirstRun, emptyNoAccess, error, loading | one copy per state — the 12 September offline sync is the model |
| state wording | reservations (WEB-031 ↔ GST-016/GST-017) | 5 state(s) worded differently: emptyFirstRun, emptyNoAccess, emptyNoResults, error, loading | one copy per state — the 12 September offline sync is the model |
| state wording | search (WEB-003 ↔ GST-063) | 3 state(s) worded differently: emptyFirstRun, error, loading | one copy per state — the 12 September offline sync is the model |
| state wording | seat-selection (WEB-007 ↔ GST-049) | 1 state(s) worded differently: emptyNoAccess | one copy per state — the 12 September offline sync is the model |
| state wording | shop (WEB-033 ↔ GST-026) | 5 state(s) worded differently: emptyFirstRun, emptyNoAccess, emptyNoResults, error, loading | one copy per state — the 12 September offline sync is the model |
| state wording | shop-and-drop (WEB-042 ↔ GST-062) | 4 state(s) worded differently: emptyFirstRun, emptyNoAccess, error, loading | one copy per state — the 12 September offline sync is the model |
| state wording | system-states (WEB-029 ↔ GST-047) | 3 state(s) worded differently: emptyFirstRun, error, loading | one copy per state — the 12 September offline sync is the model |
| state wording | ticket-selection (WEB-005 ↔ GST-008) | 4 state(s) worded differently: emptyFirstRun, emptyNoResults, error, loading | one copy per state — the 12 September offline sync is the model |
| state wording | ticket-transfer (WEB-030 ↔ GST-014/GST-045) | 5 state(s) worded differently: emptyFirstRun, emptyNoAccess, emptyNoResults, error, loading | one copy per state — the 12 September offline sync is the model |
| state wording | tickets (WEB-018 ↔ GST-012/GST-013) | 5 state(s) worded differently: emptyFirstRun, emptyNoAccess, emptyNoResults, error, loading | one copy per state — the 12 September offline sync is the model |
| state wording | transport (WEB-049 ↔ GST-076/GST-077/GST-078/GST-079) | 3 state(s) worded differently: emptyFirstRun, emptyNoResults, loading | one copy per state — the 12 September offline sync is the model |
| state wording | venue-info (WEB-028 ↔ GST-029) | 3 state(s) worded differently: emptyFirstRun, error, loading | one copy per state — the 12 September offline sync is the model |
| state wording | venue-map-and-wait-times (WEB-039 ↔ GST-021/GST-022) | 5 state(s) worded differently: emptyFirstRun, emptyNoAccess, emptyNoResults, error, loading | one copy per state — the 12 September offline sync is the model |
| state wording | virtual-queue (WEB-040 ↔ GST-023) | 3 state(s) worded differently: emptyFirstRun, error, loading | one copy per state — the 12 September offline sync is the model |
| state wording | waiting-room (WEB-015 ↔ GST-046) | 1 state(s) worded differently: error | one copy per state — the 12 September offline sync is the model |
| state wording | wallet-and-payment-methods (WEB-021 ↔ GST-011/GST-071) | 5 state(s) worded differently: emptyFirstRun, emptyNoAccess, emptyNoResults, error, loading | one copy per state — the 12 September offline sync is the model |
| state wording | wishlist (WEB-009 ↔ GST-020) | 3 state(s) worded differently: emptyFirstRun, error, loading | one copy per state — the 12 September offline sync is the model |
| unbound operations | add-ons (WEB-008 ↔ GST-048/GST-056) | WEB-008 declares recordRecommendationEvents and no component in its layout calls it | bind each to a component, or move it to the screen that calls it |
| unbound operations | add-ons (WEB-008 ↔ GST-048/GST-056) | GST-048 declares recordRecommendationEvents and no component in its layout calls it | bind each to a component, or move it to the screen that calls it |
| unbound operations | ai-concierge (WEB-044 ↔ GST-031/GST-032/GST-033) | WEB-044 declares createAiConversation, requestSuggestion and no component in its layout calls them | bind each to a component, or move it to the screen that calls it |
| unbound operations | ai-concierge (WEB-044 ↔ GST-031/GST-032/GST-033) | GST-031 declares createAiConversation, requestSuggestion and no component in its layout calls them | bind each to a component, or move it to the screen that calls it |
| unbound operations | ai-concierge (WEB-044 ↔ GST-031/GST-032/GST-033) | GST-033 declares createAiConversation and no component in its layout calls it | bind each to a component, or move it to the screen that calls it |
| unbound operations | cart (WEB-010 ↔ GST-041) | GST-041 declares getResourceHold and no component in its layout calls it | bind each to a component, or move it to the screen that calls it |
| unbound operations | date-and-session (WEB-006 ↔ GST-007) | WEB-006 declares checkBookingEligibility, getCart, recordConsentAnswers and no component in its layout calls them | bind each to a component, or move it to the screen that calls it |
| unbound operations | home (WEB-001 ↔ GST-001) | WEB-001 declares decideRecommendations, getCookieConsentRuntime, recordDeviceConsent, recordRecommendationEvents, recordStorefrontSessionEvents and no component in its layout calls them | bind each to a component, or move it to the screen that calls it |
| unbound operations | home (WEB-001 ↔ GST-001) | GST-001 declares decideRecommendations, getCookieConsentRuntime, recordDeviceConsent, recordRecommendationEvents, recordStorefrontSessionEvents and no component in its layout calls them | bind each to a component, or move it to the screen that calls it |
| unbound operations | loyalty (WEB-043 ↔ GST-036) | WEB-043 declares decideRecommendations, recordRecommendationEvents and no component in its layout calls them | bind each to a component, or move it to the screen that calls it |
| unbound operations | loyalty (WEB-043 ↔ GST-036) | GST-036 declares decideRecommendations, recordRecommendationEvents and no component in its layout calls them | bind each to a component, or move it to the screen that calls it |
| unbound operations | memberships (WEB-022/WEB-023 ↔ GST-015) | WEB-023 declares createInstalmentPlan, listInstalmentPlans and no component in its layout calls them | bind each to a component, or move it to the screen that calls it |
| unbound operations | memberships (WEB-022/WEB-023 ↔ GST-015) | GST-015 declares createInstalmentPlan, listInstalmentPlans and no component in its layout calls them | bind each to a component, or move it to the screen that calls it |
| unbound operations | privacy-security-devices (WEB-024 ↔ GST-066/GST-073) | GST-066 declares getCookieConsentRuntime, getDeviceConsentHistory, listPublishedTrackingTechnologies, recordDeviceConsent and no component in its layout calls them | bind each to a component, or move it to the screen that calls it |
| unbound operations | seat-selection (WEB-007 ↔ GST-049) | WEB-007 declares relinquishSeatHold and no component in its layout calls it | bind each to a component, or move it to the screen that calls it |
| unbound operations | seat-selection (WEB-007 ↔ GST-049) | GST-049 declares relinquishSeatHold and no component in its layout calls it | bind each to a component, or move it to the screen that calls it |
| unbound operations | sign-in (WEB-016 ↔ GST-042) | WEB-016 declares claimDeviceConsent, createMfaChallenge, refreshToken and no component in its layout calls them | bind each to a component, or move it to the screen that calls it |
| unbound operations | sign-in (WEB-016 ↔ GST-042) | GST-042 declares claimDeviceConsent, createMfaChallenge, refreshToken and no component in its layout calls them | bind each to a component, or move it to the screen that calls it |
| unbound operations | transport (WEB-049 ↔ GST-076/GST-077/GST-078/GST-079) | WEB-049 declares getTransportRoute and no component in its layout calls it | bind each to a component, or move it to the screen that calls it |
| unbound operations | transport (WEB-049 ↔ GST-076/GST-077/GST-078/GST-079) | GST-077 declares getTransportRoute and no component in its layout calls it | bind each to a component, or move it to the screen that calls it |
| unbound operations | wallet-and-payment-methods (WEB-021 ↔ GST-011/GST-071) | GST-011 declares getWalletAutoReloadSetting, getWalletExitBalance, settleWalletAtExit and no component in its layout calls them | bind each to a component, or move it to the screen that calls it |

## Info — 3

| Dimension | Where | Difference | Resolve by |
|---|---|---|---|
| coverage | dynamic-qr-ticket | GST-055 Dynamic QR Ticket — app only (deliberate). The 2 September session decided a dynamic-QR ticket bought on the web is redirected into the app, because a credential that needs a network round trip at a gate fails at the gate (_components.yaml, credentialPresenter). Since 28 September the code is derived on the device from the `rotation` seed (audit R230), and the web's My Tickets shows the same rotating code. Not callable on the web: bindCredentialDevice. |  |
| coverage | face-pass | GST-069 Face Pass — app only (deliberate). enrolFacePass needs a camera and a liveness check (apply-web-parity.py). Viewing and revoking an enrolment are on the web's Devices, Wishlist & Consent. Not callable on the web: enrolFacePass. |  |
| operations | transport (WEB-049 ↔ GST-076/GST-077/GST-078/GST-079) | the app calls getTransportDeparture and the web cannot call it anywhere — sanctioned: CHG-GTRB-007 - GST-077 is a screen of its own, opened on one departure, so it reloads that departure (getTransportDeparture, CHG-R1S-004); WEB-049 draws the departures beside the route from searchTransportDepartures and never opens one by id. The two shells read the same records through different operations. |  |

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
| map-booking | paired | WEB-047 | GST-074 |
| space-by-the-hour | paired | WEB-048 | GST-075 |
| transport | paired | WEB-049 | GST-076, GST-077, GST-078, GST-079 |
| itinerary-planning | paired | WEB-050 | GST-051, GST-052, GST-053, GST-054, GST-059 |
| help-and-cases | paired | WEB-025 | GST-068 |
| help-content-and-accessibility | paired | WEB-045 | GST-040, GST-057 |
| lost-and-found | paired | WEB-034 | GST-034 |
| feedback | paired | WEB-026 | GST-035 |
| newsletter | paired | WEB-027 | GST-065 |
| ai-concierge | paired | WEB-044 | GST-031, GST-032, GST-033 |
| system-states | paired | WEB-029 | GST-047 |
| rtl-specimen | appOnly · raise | — | GST-043 |
