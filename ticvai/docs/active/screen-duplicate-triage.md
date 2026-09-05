# Identical operation sets — what each cluster actually is

**Derived by `tools/screen-ledger.py --duplicates`. Regenerate rather than editing.**

**"107 exact functional duplicates" reads as "delete 107 screens", and that is wrong.** Clustering by operation signature puts three unrelated things in one bucket, and only one of them is duplication.

| Kind | Clusters | Screens | What to do |
|---|---:|---:|---|
| same journey, two form factors | 40 | 98 | **Nothing.** One product on two devices is the design. |
| different audience | 11 | 31 | **Nothing, but say so.** Same operations, different scope — a venue managing its own domain and a platform admin managing anyone's. |
| a pair - one step and its next | 6 | 12 | **Nothing.** A detail reads the row its list read, and an answer reads the conversation its question opened. |

## Every cluster

### same journey, two form factors

| Platform(s) | Screens | Shared operations |
|---|---|---|
| P06, P07, P08 | EMP-010 Scan — ready<br>EMP-015 Group scan<br>SCN-007 Group admission<br>SCN-008 Manual entry<br>SCN-009 Ticket lookup<br>SCN-013 Offline journal<br>SCN-015 Offline package<br>BO-034 Scan Activity | `getOfflinePackage`, `listScans`, `lookupTicket`, `overrideAccess`, `syncScans`, `validateAccess` +1 |
| P06, P08 | EMP-007 Handover notes<br>EMP-037 Notifications<br>EMP-039 Announcements<br>EMP-047 Emergency mode<br>EMP-038 Broadcast to team<br>BO-066 Notification Settings | `acknowledgeAnnouncement`, `getAnnouncementReach`, `listAnnouncements`, `publishAnnouncement` |
| P02, P05 | GST-008 Tickets & Add-ons<br>GST-045 Ticket Delivery & Sharing<br>GST-055 Dynamic QR Ticket<br>KSK-010 Print failure<br>KSK-012 Booking found | `transferOrderTickets` |
| P06, P08 | EMP-009 End shift<br>BO-039 Shift Directory<br>BO-040 Variance Approval<br>BO-041 Cash Movements<br>BO-042 Banking & Safe | `acceptShiftVariance`, `approveShiftOpen`, `closeShift`, `createCashMovement`, `getCurrentShift`, `getShift` +7 |
| P01, P02 | WEB-025 Help Centre / FAQ<br>WEB-028 Contact & Venue Information<br>WEB-029 Error / Sold Out / Maintenance<br>GST-047 Maintenance / Upgrade Page | `getTenantAppStatus` |
| P01, P02 | WEB-002 Event & Attraction Listing<br>GST-003 Event & Attraction Listing | `getWaitTimes`, `listPerformances`, `listProducts`, `searchCatalogue` |
| P01, P02 | WEB-004 Attraction Details<br>GST-004 Attraction Details | `getAvailability`, `getProduct`, `getWaitTimes`, `listPerformances` |
| P01, P05 | WEB-006 Date & Session Selection<br>KSK-005 Choose a session | `acquireInventoryHold`, `getAvailability` |
| P01, P02 | WEB-007 Interactive Seat Selection<br>GST-049 Interactive Seat Selection | `createSeatHold`, `getSeatAvailability`, `recommendSeats` |
| P01, P02 | WEB-008 Add-ons & Upsell<br>GST-048 Upsell / Cross-Sell | `addCartLine`, `getUpsellSuggestions` |
| P01, P02 | WEB-009 Wishlist<br>GST-020 Saved Items / Wishlist | `addToWishlist`, `getWishlist`, `removeFromWishlist` |
| P01, P02 | WEB-013 Booking Confirmation<br>GST-010 Booking Confirmation | `getOrder`, `reprintOrder`, `transferOrderTickets` |
| P01, P02 | WEB-015 Branded Queue / Waiting Room<br>GST-046 Branded Queue / Waiting Room | `getWaitTimes`, `getWaitingGuest`, `joinQueue` |
| P01, P02 | WEB-018 My Tickets<br>GST-012 My Tickets | `getEntitlement`, `getEntitlementCredential`, `getEntitlementHistory`, `listEntitlements`, `listMyEntitlements`, `transferOrderTickets` |
| P01, P02 | WEB-019 Order History<br>GST-019 Order History | `getOrder`, `listMyOrders`, `listOrders`, `transferOrderTickets` |
| P01, P02 | WEB-030 Ticket Transfer<br>GST-014 Ticket Transfer | `claimTicketTransfer`, `listOrders`, `transferOrderTickets` |
| P01, P02 | WEB-031 My Reservations<br>GST-016 My Reservations | `cancelReservation`, `getReservation`, `listReservations` |
| P01, P02 | WEB-032 Offers & Promotions<br>GST-037 Offers & Promotions | `evaluatePromotions`, `getPromotion`, `listPromotions` |
| P01, P05 | WEB-033 Shop<br>KSK-017 Shop | `addCartLine`, `listMerchandise`, `lookupMerchandise`, `reserveMerchandise` |
| P01, P02 | WEB-034 Lost & Found<br>GST-034 Lost & Found | `listMyCases`, `raiseMyCase`, `replyToMyCase` |
| P01, P02 | WEB-035 Multi-Currency & Pricing<br>GST-044 Multi-Currency & Pricing | `listFxRates`, `listProducts` |
| P01, P02 | WEB-036 F&B – Browse & Order<br>GST-024 F&B – Browse & Order | `claimLocationSession`, `claimTableSession`, `createGuestFnbOrder`, `getGuestMenu`, `getGuestOrderStatus`, `listDeliveryLocations` +2 |
| P01, P02 | WEB-037 Menu Item Detail<br>GST-061 Menu Item Detail | `getGuestMenu`, `listModifierGroups` |
| P01, P02 | WEB-038 F&B – Order Tracking<br>GST-025 F&B – Order Tracking | `claimTableSession`, `getGuestBill`, `getGuestOrderStatus` |
| P01, P02 | WEB-040 Virtual Queue<br>GST-023 Virtual Queue | `getWaitTimes`, `getWaitingGuest`, `joinQueue`, `leaveQueue` |
| P01, P02 | WEB-041 Parking – Reserve & Pay<br>GST-027 Parking – Reserve & Pay | `createParkingEntitlement`, `listParkingFacilities`, `updateParkingEntitlement` |
| P01, P02 | WEB-043 Loyalty & Rewards<br>GST-036 Loyalty & Rewards | `evaluatePromotions`, `getLoyaltyPosition`, `listLoyaltyProgrammes`, `listPromotions` |
| P01, P02 | WEB-044 AI Concierge – Home<br>GST-031 AI Concierge – Home | `createAiConversation`, `getGuestMenu`, `handoverToAgent`, `requestSuggestion`, `sendAiMessage` |
| P01, P02 | WEB-046 In-Venue Notifications<br>GST-030 In-Venue Notifications | `claimLocationSession` |
| P02, P05 | GST-002 Explore Categories<br>KSK-003 What are you buying | `listProducts` |
| P06, P07 | EMP-017 Sync & reconciliation<br>SCN-014 Sync & reconciliation | `getOfflinePackage`, `listScans`, `listSyncRejections`, `lookupTicket`, `overrideAccess`, `syncOrders` +3 |
| P06, P08 | EMP-033 Capacity view<br>BO-017 Capacity Management | `createChannelCapacity`, `getChannelAllocations`, `listChannelCapacities`, `releaseChannelAllocation`, `setChannelAllocations`, `updateChannelCapacity` |
| P06, P08 | EMP-024 Clock in / out<br>BO-056 Time & Attendance | `amendAttendance`, `listAttendance`, `recordAttendance` |
| P06, P08 | EMP-026 Incident report<br>BO-072 Incident Log | `getIncident`, `listIncidents`, `recordAuthorityNotification`, `reportIncident`, `updateIncident` |
| P06, P08 | EMP-069 Barcode, RFID, Serialized Stock & Traceability<br>BO-114 Variants, Attributes, Barcode & RFID Management | `listSerialisedItems`, `lookupMerchandise` |
| P06, P08 | EMP-070 Inventory Exceptions, AI Replenishment & Action Center<br>BO-141 Operational Alerts, AI Replenishment & Action Center | `acknowledgeAlert`, `createRequisition`, `listAlerts` |
| P08, P13 | BO-031 Asset Register<br>CMS-004 Logo & Assets | `createAsset`, `getAsset`, `getAssetHistory`, `listAssets`, `lookupAsset`, `setAssetStatus` +1 |
| P08, P15 | BO-134 Kitchen & Preparation Stations<br>KIT-005 Kitchen Station Workload & Dynamic Routing | `listKitchenStations`, `setKitchenStations` |
| P10, P14 | PTR-019 API Credentials & Integration<br>DEV-003 Clients & Credentials | `createApiClient`, `listApiClients`, `revokeApiCredential`, `rotateApiCredential` |
| P15, P16 | KIT-010 Kitchen Performance, AI & Operational Optimization<br>ANL-008 Demand Forecasting | `askReportingQuestion`, `getDashboard` |

### different audience

| Platform(s) | Screens | Shared operations |
|---|---|---|
| P04, P06, P08, P10 | POS-006 Held Orders<br>EMP-014 Ticket lookup<br>BO-022 Order Detail<br>BO-026 Group Bookings<br>BO-047 F&B Order Management<br>PTR-008 Booking Creation<br>PTR-015 Order History | `applyManualDiscount`, `createOrder`, `createRefund`, `exchangeOrderLines`, `getOrder`, `getOrderStatement` +8 |
| P08, P10 | BO-029 Report Builder<br>BO-059 Sales Reports<br>BO-061 Scheduled Reports<br>PTR-018 Reports & Sales Performance | `askReportingQuestion`, `createReport`, `deleteReport`, `getFinancialReport`, `getReport`, `listReports` +3 |
| P08, P10 | BO-051 Purchase Orders<br>BO-070 Work Orders<br>PTR-016 Voucher / Ticket Download | `applyManualDiscount`, `createOrder`, `exchangeOrderLines`, `getOrder`, `getOrderStatement`, `holdOrder` +7 |
| P08, P09, P10 | BO-053 Staff Directory<br>ADM-020 Platform User Directory<br>PTR-003 Profile & Company Details | `createPrincipal`, `getPrincipal`, `listPrincipals`, `updatePrincipal` |
| P02, P11 | GST-022 Attraction Wait Times<br>ACC-006 Reviewer Queue | `getWaitTimes` |
| P06, P10 | EMP-035 Payment on device<br>PTR-012 Checkout / Credit Purchase | `addTip`, `capturePayment`, `createPayment`, `inquirePaymentStatus` |
| P06, P10 | EMP-028 Lost & found<br>PTR-021 Support & Contact | `addCaseMessage`, `createCase`, `escalateCase`, `getCase`, `listCases`, `reopenCase` +1 |
| P08, P10 | BO-025 Chargebacks & Disputes<br>PTR-014 Settlement & Payment History | `getSettlement`, `ingestSettlementFile`, `listSettlementExceptions`, `listSettlements`, `resolveSettlementException` |
| P08, P09 | BO-054 Role Assignment<br>ADM-021 Platform Role Management | `createRole`, `listRoles` |
| P09, P12 | ADM-001 Platform Login / MFA<br>SUP-001 Agent Login | `forceLogout`, `getCurrentSession`, `getGuestSession`, `listActiveSessions`, `listMfaMethods`, `listSsoProviders` +2 |
| P09, P13 | ADM-017 Domain & Certificate Management<br>CMS-017 Domain & Certificate | `claimCustomDomain`, `listCustomDomains`, `releaseCustomDomain`, `verifyCustomDomain` |

### a pair - one step and its next

| Platform(s) | Screens | Shared operations |
|---|---|---|
| P01 | WEB-017 My Account Dashboard<br>WEB-024 Devices, Wishlist & Consent | `addToWishlist`, `getWishlist`, `listGuestDevices`, `recordConsent`, `registerGuestDevice`, `removeFromWishlist` +1 |
| P06 | EMP-004 Task list<br>EMP-005 Task detail | `acceptWorkOrder`, `attachWorkOrderEvidence`, `cancelWorkOrder`, `closeWorkOrder`, `completeWorkOrder`, `getWorkOrder` +9 |
| P06 | EMP-019 AI assistant — home<br>EMP-020 AI assistant — answer | `createAiConversation`, `listAiConversations`, `sendAiMessage` |
| P07 | SCN-002 Access point & direction<br>SCN-016 Gate mode | `getAccessPoint`, `listAccessPoints`, `setTurnstileMode` |
| P08 | BO-015 Session Calendar<br>BO-016 Session Template | `cancelPerformance`, `createEvent`, `createPerformances`, `getEvent`, `getPerformance`, `getSeatAvailability` +5 |
| P09 | ADM-022 Release & Version Management<br>ADM-023 Staging Promotion & Approval | `createRelease`, `getRelease`, `getReleaseReadiness`, `listReleases`, `promoteRelease`, `rejectRelease` +1 |
