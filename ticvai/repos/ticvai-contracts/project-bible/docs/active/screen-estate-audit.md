# Screen estate audit — duplication, connectivity, and stranded capability

**Derived by `tools/audit-screen-estate.py`. Regenerate rather than editing.**

| | |
|---|---:|
| Screens | 1091 |
| Platforms | 15 |
| Operations called by at least one screen | 784 |
| **Audience declared and never served** | **74** |
| **Single-audience operation on a shared entity** | **94** |
| Screens nothing navigates to — authored | **184** |
| Screens nothing navigates to — from the pack | 590 |
| …of all those, also exiting nowhere | 599 |

## What a finding here is

**A question, not a defect.** An operation declared `staff` and used only by staff is correct. An operation declared `staff, guest` and used only by staff is either a missing surface or a wrong declaration, and this tool cannot tell you which — that is a product decision. It tells you where to look.

Duplication is not recomputed here. `tools/check-screen-redundancy.py` clusters by operation signature and remains the authority on it.

## 1. Declared for an audience no screen serves

`x-ticvai-audience` says who **may** call an operation. The screens say who **does**.

| Operation | Declared | Actually served | Never served | Platforms |
|---|---|---|---|---|
| `allocateBlockedSeats` | partner, staff | partner | **staff** | P10 |
| `authoriseStoredValue` | device, guest, staff | staff | **guest** | P08 |
| `cancelReservation` | guest, staff | anonymous, guest, public | **staff** | P01, P02 |
| `certifyIntegration` | staff | partner | **staff** | P14 |
| `createApiClient` | partner, staff | partner | **staff** | P14 |
| `createDelegatedAccess` | partner, staff | partner | **staff** | P10 |
| `createMfaChallenge` | guest, partner, staff | anonymous, guest, public | **partner, staff** | P02 |
| `createReferral` | guest, staff | anonymous, guest, public | **staff** | P02 |
| `createResaleListing` | guest, staff | anonymous, guest, public | **staff** | P02 |
| `createSandbox` | partner, staff | partner | **staff** | P14 |
| `createSeatBlock` | partner, staff | partner | **staff** | P10 |
| `createWebhookSubscription` | partner, staff | partner | **staff** | P14 |
| `deleteDelegatedAccess` | partner, staff | partner | **staff** | P10 |
| `deprecateApiVersion` | staff | partner | **staff** | P14 |
| `enrolFacePass` | guest, staff | anonymous, guest, public | **staff** | P02 |
| `enrolMfaMethod` | guest, partner, staff | anonymous, guest, public | **partner, staff** | P01, P02 |
| `exportSubjectData` | guest, staff | anonymous, guest, public | **staff** | P02 |
| `getB2bCredit` | partner, staff | partner | **staff** | P10 |
| `getBundle` | guest, staff | anonymous, guest, public | **staff** | P02 |
| `getCommissionStatement` | partner, staff | partner | **staff** | P10 |
| `getCouponCode` | guest, staff | anonymous, guest, public | **staff** | P01 |
| `getEntitlement` | guest, staff | anonymous, guest, public | **staff** | P01, P02 |
| `getEntitlementCredential` | guest, staff | anonymous, guest, public | **staff** | P01, P02 |
| `getEntitlementHistory` | guest, staff | anonymous, guest, public | **staff** | P01, P02 |
| `getFacePassEnrolment` | guest, staff | anonymous, guest, public | **staff** | P02 |
| `getGiftCard` | guest, staff | anonymous, guest, public | **staff** | P01 |
| `getGroupBooking` | guest, staff | anonymous, guest, public | **staff** | P02 |
| `getMessageStatus` | partner, staff | partner | **staff** | P10 |
| `getMyChallenges` | guest, staff | anonymous, guest, public | **staff** | P02 |
| `getMyMemberships` | guest, staff | anonymous, guest, public | **staff** | P01, P02 |
| `getRecommendations` | guest, staff | staff | **guest** | P08 |
| `getReservation` | guest, staff | anonymous, guest, public | **staff** | P01, P02 |
| `getWaiverStatus` | device, guest, staff | anonymous, guest, public | **staff** | P02 |
| `getWallet` | guest, staff | anonymous, guest, public | **staff** | P01, P02 |
| `grantDelegation` | guest, staff | anonymous, guest, public | **staff** | P02 |
| `issueWalletPass` | guest, staff | anonymous, guest, public | **staff** | P02 |
| `listApiVersions` | partner, public | partner | **public** | P14 |
| `listConsentPurposes` | guest, staff | anonymous, guest, public | **staff** | P01, P02 |
| `listContentPages` | guest, staff | anonymous, guest, public | **staff** | P01, P02 |
| `listDelegatedAccess` | partner, staff | partner | **staff** | P10 |
| `listDelegations` | guest, staff | anonymous, guest, public | **staff** | P02 |
| `listGuestMemberships` | guest, staff | anonymous, guest, public | **staff** | P01, P02 |
| `listIntegrationListings` | partner, public, staff | partner | **public, staff** | P14 |
| `listLostItems` | guest, staff | staff | **guest** | P08 |
| `listLoyaltyProgrammes` | guest, staff | anonymous, guest, public | **staff** | P01, P02 |
| `listPaymentTokens` | guest, staff | anonymous, guest, public | **staff** | P02 |
| `listProductCategories` | guest, staff | staff | **guest** | P08 |
| `listReservations` | guest, staff | anonymous, guest, public | **staff** | P01, P02 |
| `listSandboxes` | partner, staff | partner | **staff** | P14 |
| `listSeatBlocks` | partner, staff | partner | **staff** | P10 |
| `listWalletTransactions` | guest, staff | anonymous, guest, public | **staff** | P01, P02 |
| `listWebhookDeliveries` | partner, staff | partner | **staff** | P14 |
| `listWebhookSubscriptions` | partner, staff | partner | **staff** | P14 |
| `lookupShopAndDrop` | guest, staff | anonymous, guest, public | **staff** | P01, P02, P05 |
| `overrideCreditLimit` | partner, staff | partner | **staff** | P10 |
| `recordGamePlay` | guest | staff | **guest** | P08 |
| `refreshToken` | guest, partner, staff | anonymous, guest, public | **partner, staff** | P01, P02 |
| `registerDeveloper` | public | partner | **public** | P14 |
| `releaseSeatBlock` | partner, staff | partner | **staff** | P10 |
| `removeMfaMethod` | guest, partner, staff | anonymous, guest, public | **partner, staff** | P01, P02 |
| `replayEvents` | partner, staff | partner | **staff** | P14 |
| `resetSandbox` | partner, staff | partner | **staff** | P14 |
| `revokeApiCredential` | partner, staff | partner | **staff** | P14 |
| `revokeFacePass` | guest, staff | anonymous, guest, public | **staff** | P02 |
| `rotateApiCredential` | partner, staff | partner | **staff** | P14 |
| `setApiLicensing` | staff | partner | **staff** | P14 |
| `setB2bCreditLimit` | partner, staff | partner | **staff** | P10 |
| `shareEntitlement` | guest, staff | anonymous, guest, public | **staff** | P02 |
| `storePaymentToken` | guest, staff | anonymous, guest, public | **staff** | P02 |
| `transferWalletBalance` | guest, staff | anonymous, guest, public | **staff** | P02 |
| `updateGuestPreferences` | guest, staff | anonymous, guest, public | **staff** | P02 |
| `uploadGuestDocument` | guest, staff | anonymous, guest, public | **staff** | P02 |
| `verifyMfaChallenge` | guest, partner, staff | anonymous, guest, public | **partner, staff** | P01, P02 |
| `verifyMfaEnrolment` | guest, partner, staff | anonymous, guest, public | **partner, staff** | P01, P02 |

## 2. One audience, on an entity several audiences work

**The harder half.** These operations are not mis-declared — they are reachable from one audience while the *same entity* is worked by others. A venue-side function a guest plausibly needs looks exactly like this, and no annotation marks it.

| Operation | Reachable from | Entity | Also worked by | Platforms |
|---|---|---|---|---|
| `getAccessPoint` | staff | access, point | **guest, partner** | P07, P08 |
| `getAiUsage` | staff | usage | **partner, platformAdmin** | P08 |
| `getB2bCredit` | partner | credit | **staff** | P10 |
| `getBill` | staff | bill | **guest** | P06 |
| `getBundle` | guest | bundle | **staff** | P02 |
| `getCampaignPerformance` | staff | performance | **guest** | P08 |
| `getCell` | platformAdmin | cell | **staff** | P09 |
| `getCellCapacity` | platformAdmin | capacity, cell | **partner, staff** | P09 |
| `getCellHealth` | platformAdmin | cell, health | **staff** | P09 |
| `getCommissionStatement` | partner | statement | **staff** | P10 |
| `getConsentHistory` | staff | consent | **guest** | P08, P13 |
| `getConversation` | staff | conversation | **guest** | P12 |
| `getCouponCode` | guest | coupon | **platformAdmin, staff** | P01 |
| `getCurrentShift` | staff | current | **partner, platformAdmin** | P04, P06, P07, P08 |
| `getEntitlement` | guest | entitlement | **platformAdmin, staff** | P01, P02 |
| `getEntitlementCredential` | guest | credential, entitlement | **partner, platformAdmin, staff** | P01, P02 |
| `getEntitlementHistory` | guest | entitlement | **platformAdmin, staff** | P01, P02 |
| `getGameCard` | guest | card, game | **staff** | P02 |
| `getGiftCard` | guest | card | **staff** | P01 |
| `getGuestBill` | guest | bill, guest | **partner, platformAdmin, staff** | P01, P02 |
| `getGuestLoyalty` | staff | guest, loyalty | **guest, partner, platformAdmin** | P08, P13 |
| `getHaccpStatus` | staff | statu | **guest, partner** | P06, P08, P15 |
| `getInventoryItem` | staff | inventory | **guest** | P08 |
| `getLatestBundle` | staff | bundle | **guest** | P04, P06, P08 |
| `getMediaEntitlements` | staff | entitlement | **guest, platformAdmin** | P04, P06, P08, P13 |
| `getMenu` | staff | menu | **guest** | P08, P13 |
| `getMessageStatus` | partner | message, statu | **guest, staff** | P10 |
| `getOrgUnit` | staff | unit | **platformAdmin** | P08 |
| `getOutletStock` | staff | outlet | **guest** | P08 |
| `getPlan` | platformAdmin | plan | **staff** | P09 |
| `getQueue` | staff | queue | **guest** | P06, P08 |
| `getQueueFeedHealth` | staff | health, queue | **guest, platformAdmin** | P08 |
| `getRefundPolicy` | staff | refund | **guest, partner** | P08 |
| `getRelease` | platformAdmin | release | **partner, staff** | P09 |
| `getReleaseReadiness` | platformAdmin | release | **partner, staff** | P09 |
| `getReservation` | guest | reservation | **staff** | P01, P02 |
| `getRollout` | platformAdmin | rollout | **staff** | P09 |
| `getSeatHold` | staff | hold, seat | **guest, partner** | P04 |
| `getStockPositions` | staff | position | **guest** | P06, P08 |
| `getStockTransfer` | staff | transfer | **guest** | P06, P08 |
| `getSupplierPerformance` | staff | performance | **guest** | P08 |
| `getTableMap` | staff | table | **guest** | P06, P08 |
| `getTrialBalance` | staff | balance | **guest** | P08 |
| `getVersionSkew` | platformAdmin | version | **partner, staff** | P09 |
| `getWaitingGuest` | guest | guest | **partner, platformAdmin, staff** | P01, P02 |
| `getWaiverStatus` | guest | statu | **partner, staff** | P02 |
| `getWorkstationHealth` | staff | health | **platformAdmin** | P04, P08 |
| `listAccessPoints` | staff | access, point | **guest, partner** | P07, P08 |
| `listAiProviders` | platformAdmin | provider | **guest, partner, staff** | P09 |
| `listApiVersions` | partner | version | **platformAdmin, staff** | P14 |
| `listApprovalDelegations` | staff | delegation | **guest** | P08 |
| `listCellJobs` | platformAdmin | cell, job | **staff** | P09 |
| `listChannelListings` | staff | channel, listing | **guest, partner** | P08 |
| `listConsentPurposes` | guest | consent, purpose | **staff** | P01, P02 |
| `listConversations` | staff | conversation | **guest** | P12 |
| `listCouponCampaigns` | staff | coupon | **guest, platformAdmin** | P08 |
| `listDelegatedAccess` | partner | access | **staff** | P10 |
| `listDelegations` | guest | delegation | **staff** | P02 |
| `listDevices` | staff | device | **guest** | P06, P08, P16 |
| `listEntitlementTemplates` | staff | entitlement | **guest, platformAdmin** | P08 |
| `listEntitlements` | guest | entitlement | **platformAdmin, staff** | P01, P02 |
| `listGames` | staff | game | **guest** | P08 |
| `listGuestMemberships` | guest | guest | **partner, platformAdmin, staff** | P01, P02 |
| `listIndexJobs` | staff | job | **platformAdmin** | P08 |
| `listIntegrationListings` | partner | listing | **guest, staff** | P14 |
| `listInventoryHolds` | staff | hold, inventory | **guest, partner** | P04, P08 |
| `listInventoryItems` | staff | inventory | **guest** | P08 |
| `listKitchenTickets` | staff | ticket | **guest** | P04, P08, P15 |
| `listLoyaltyProgrammes` | guest | loyalty | **staff** | P01, P02 |
| `listMaintenancePlans` | staff | plan | **platformAdmin** | P08 |
| `listMenus` | staff | menu | **guest** | P04, P08, P13 |
| `listMessageTemplates` | staff | message | **guest, partner** | P12 |
| `listMyCases` | guest | case | **partner, staff** | P01, P02 |
| `listOutlets` | staff | outlet | **guest** | P04, P08 |
| `listPlans` | platformAdmin | plan | **staff** | P09 |
| `listProductVersions` | platformAdmin | version | **partner, staff** | P09 |
| `listPromoBlocks` | staff | block | **partner** | P13 |
| `listQueueEntries` | staff | queue | **guest** | P06, P08 |
| `listQueueFeeds` | staff | queue | **guest** | P08 |
| `listRecognitionSchedules` | staff | schedule | **platformAdmin** | P08 |
| `listReleases` | platformAdmin | release | **partner, staff** | P09 |
| `listReservations` | guest | reservation | **staff** | P01, P02 |
| `listResources` | staff | resource | **guest** | P08 |
| `listRollouts` | platformAdmin | rollout | **staff** | P09 |
| `listSeatBlocks` | partner | block, seat | **guest, staff** | P10 |
| `listStockLocations` | staff | location | **guest** | P06, P08 |
| `listStockTransfers` | staff | transfer | **guest** | P08 |
| `listTableReservations` | staff | reservation, table | **guest** | P06 |
| `listUpgradeSchedules` | platformAdmin | schedule | **staff** | P09 |
| `listWebhookDeliveries` | partner | delivery | **guest, staff** | P14 |
| `listWebhookSubscriptions` | partner | subscription | **platformAdmin, staff** | P14 |
| `searchCatalogue` | guest | catalogue, search | **staff** | P01, P02 |
| `searchGuests` | staff | guest, search | **guest, partner, platformAdmin** | P08, P13 |
| `searchMedia` | staff | search | **guest** | P13 |

## 3. Connectivity

A screen nothing navigates to is reachable only by knowing its id. One that also exits nowhere is not in the graph at all.

| Screen | Platform | Nothing navigates to it | Exits nowhere |
|---|---|---|---|
| WEB-009 Wishlist | P01 | yes | no |
| WEB-014 Pay for a Booking | P01 | yes | no |
| WEB-015 Branded Queue / Waiting Room | P01 | yes | no |
| WEB-020 Profile & Preferences | P01 | yes | no |
| WEB-029 Error / Sold Out / Maintenance | P01 | yes | no |
| WEB-032 Offers & Promotions | P01 | yes | no |
| WEB-033 Shop | P01 | yes | no |
| WEB-034 Lost & Found | P01 | yes | no |
| GST-005 What's On | P02 | yes | no |
| GST-006 Event / Exhibition Details | P02 | yes | no |
| GST-007 Select Date & Time | P02 | yes | no |
| GST-008 Tickets & Add-ons | P02 | yes | no |
| GST-010 Booking Confirmation | P02 | yes | no |
| GST-011 Wallet Overview | P02 | yes | no |
| GST-012 My Tickets | P02 | yes | no |
| GST-013 Ticket Details | P02 | yes | no |
| GST-014 Ticket Transfer | P02 | yes | no |
| GST-015 Memberships | P02 | yes | no |
| GST-016 My Reservations | P02 | yes | no |
| GST-017 Reservation Details | P02 | yes | no |
| GST-018 Add to Calendar / Reminders | P02 | yes | no |
| GST-019 Order History | P02 | yes | no |
| GST-020 Saved Items / Wishlist | P02 | yes | no |
| GST-021 Interactive Map | P02 | yes | no |
| GST-022 Attraction Wait Times | P02 | yes | no |
| GST-023 Virtual Queue | P02 | yes | no |
| GST-024 F&B – Browse & Order | P02 | yes | no |
| GST-025 F&B – Order Tracking | P02 | yes | no |
| GST-026 Retail / Merchandise | P02 | yes | no |
| GST-027 Parking – Reserve & Pay | P02 | yes | no |
| GST-028 Parking – Reservation Confirmed | P02 | yes | no |
| GST-029 Venue Info & Services | P02 | yes | no |
| GST-030 In-Venue Notifications | P02 | yes | no |
| GST-034 Lost & Found | P02 | yes | no |
| GST-035 Feedback & Ratings | P02 | yes | no |
| GST-036 Loyalty & Rewards | P02 | yes | no |
| GST-037 Offers & Promotions | P02 | yes | no |
| GST-038 Digital Companion Mode | P02 | yes | no |
| GST-040 Help & Support | P02 | yes | no |
| GST-041 Checkout Entry | P02 | yes | no |
| GST-042 Simple Registration & OTP | P02 | yes | no |
| GST-043 Arabic / RTL Experience | P02 | yes | no |
| GST-044 Multi-Currency & Pricing | P02 | yes | no |
| GST-045 Ticket Delivery & Sharing | P02 | yes | no |
| GST-046 Branded Queue / Waiting Room | P02 | yes | no |
| GST-047 Maintenance / Upgrade Page | P02 | yes | no |
| GST-048 Upsell / Cross-Sell | P02 | yes | no |
| GST-049 Interactive Seat Selection | P02 | yes | no |
| GST-050 Resource Booking – Cabana | P02 | yes | no |
| GST-051 Plan Your Adventure – Start | P02 | yes | no |
| GST-052 Suggested Itineraries | P02 | yes | no |
| GST-053 Build Your Own Itinerary | P02 | yes | no |
| GST-054 AI Optimized Itinerary | P02 | yes | no |
| GST-055 Dynamic QR Ticket | P02 | yes | no |
| GST-056 Bundle Package | P02 | yes | no |
| GST-057 Accessibility Information | P02 | yes | no |
| GST-058 Resource Availability (Cabana) | P02 | yes | no |
| GST-063 Search | P02 | yes | no |
| GST-065 Newsletter & Preferences | P02 | yes | no |
| GST-066 Privacy & My Data | P02 | yes | no |
| GST-067 Refunds & Resale | P02 | yes | no |
| GST-068 Help & My Cases | P02 | yes | no |
| GST-069 Face Pass | P02 | yes | no |
| GST-070 Reserve a Table or Cabana | P02 | yes | no |
| GST-071 Payment Methods | P02 | yes | no |
| GST-072 Share & Group Booking | P02 | yes | no |
| GST-073 Security & Sign-in | P02 | yes | no |
| POS-008 Reports | P04 | yes | no |
| POS-012 Omnichannel Order & Fulfilment Center | P04 | yes | yes |
| POS-014 Sales Exceptions, Controls & Operational Actions | P04 | yes | yes |
| POS-015 Cash Operations Dashboard | P04 | yes | yes |
| POS-016 Till Configuration | P04 | yes | yes |
| POS-017 Cash In / Cash Out Operations | P04 | yes | yes |
| POS-018 Safe Drop & Cash Transfer Management | P04 | yes | yes |
| POS-019 Shift Templates & Policies | P04 | yes | yes |
| KSK-008 Payment unresolved | P05 | yes | no |
| KSK-010 Print failure | P05 | yes | no |
| KSK-011 Collect a booking | P05 | yes | no |
| KSK-012 Booking found | P05 | yes | no |
| KSK-014 Out of service | P05 | yes | no |
| KSK-015 Assistant | P05 | yes | no |
| KSK-016 Order Food | P05 | yes | no |
| EMP-006 Raise a task | P06 | yes | no |
| EMP-008 Shift summary | P06 | yes | no |
| EMP-010 Scan — ready | P06 | yes | no |
| EMP-014 Ticket lookup | P06 | yes | no |
| EMP-015 Group scan | P06 | yes | no |
| EMP-017 Sync & reconciliation | P06 | yes | no |
| EMP-018 Offline package | P06 | yes | no |
| EMP-019 AI assistant — home | P06 | yes | no |
| EMP-020 AI assistant — answer | P06 | yes | no |
| EMP-021 Roster | P06 | yes | no |
| EMP-022 My rota | P06 | yes | no |
| EMP-023 Swap request | P06 | yes | no |
| EMP-024 Clock in / out | P06 | yes | no |
| EMP-025 Break management | P06 | yes | no |
| EMP-026 Incident report | P06 | yes | no |
| EMP-027 Incident detail | P06 | yes | no |
| EMP-028 Lost & found | P06 | yes | no |
| EMP-029 Guest assistance | P06 | yes | no |
| EMP-030 Venue map | P06 | yes | no |
| EMP-031 Queue monitor | P06 | yes | no |
| EMP-032 Manual wait entry | P06 | yes | no |
| EMP-033 Capacity view | P06 | yes | no |
| EMP-034 Walk-up sale | P06 | yes | no |
| EMP-035 Payment on device | P06 | yes | no |
| EMP-036 Issue media | P06 | yes | no |
| EMP-037 Notifications | P06 | yes | no |
| EMP-038 Broadcast to team | P06 | yes | no |
| EMP-039 Announcements | P06 | yes | no |
| EMP-040 Knowledge base | P06 | yes | no |
| EMP-041 Training | P06 | yes | no |
| EMP-042 Profile | P06 | yes | no |
| EMP-043 Device settings | P06 | yes | no |
| EMP-044 Accessibility | P06 | yes | no |
| EMP-045 Arabic / RTL | P06 | yes | no |
| EMP-046 Sign out | P06 | yes | no |
| EMP-047 Emergency mode | P06 | yes | no |
| EMP-049 Hand over the journal | P06 | yes | no |
| EMP-050 Post-incident restore | P06 | yes | no |
| SCN-007 Group admission | P07 | yes | no |
| SCN-008 Manual entry | P07 | yes | no |
| SCN-009 Ticket lookup | P07 | yes | no |
| SCN-011 Delegated right | P07 | yes | no |
| SCN-013 Offline journal | P07 | yes | no |
| SCN-014 Sync & reconciliation | P07 | yes | no |
| SCN-016 Gate mode | P07 | yes | no |
| BO-144 Access Control Command Center | P08 | yes | yes |
| BO-145 Venue & Park Access Structure | P08 | yes | yes |
| BO-146 Access Area & Zone Builder | P08 | yes | yes |
| BO-147 Attraction Access Configuration | P08 | yes | yes |
| BO-148 Access Point Directory | P08 | yes | yes |
| BO-149 Gate & Lane Configuration | P08 | yes | yes |
| BO-150 Access Control Graphical Map Designer | P08 | yes | yes |
| BO-151 Access Location Grouping | P08 | yes | yes |
| BO-152 Operating Calendar & Special Access Days | P08 | yes | yes |
| BO-153 Topology Validation & Publication | P08 | yes | yes |
| BO-154 Access Rule Command Center | P08 | yes | yes |
| BO-155 Visual Access Rule Builder | P08 | yes | yes |
| BO-156 Entry, Exit & Re-entry Rules | P08 | yes | yes |
| BO-157 Anti-Passback & Journey Sequence | P08 | yes | yes |
| BO-158 Access Validity & Time Rules | P08 | yes | yes |
| BO-159 Entitlement Consumption Engine | P08 | yes | yes |
| BO-160 Multi-Park & Crossover Rules | P08 | yes | yes |
| BO-161 Guest, Companion & Eligibility Rules | P08 | yes | yes |
| BO-162 Group Admission & Quantity Validation | P08 | yes | yes |
| BO-163 Rule Simulation, Conflict Check & Publication | P08 | yes | yes |
| BO-164 Digital Credential Security Command Center | P08 | yes | yes |
| BO-165 Dynamic QR Security Profile Builder | P08 | yes | yes |
| BO-166 Credential Activation & Display Rules | P08 | yes | yes |
| BO-167 Device Binding & Session Security | P08 | yes | yes |
| BO-168 BLE Beacon & Geofence Configuration | P08 | yes | yes |
| BO-169 Credential Transfer & Rebinding | P08 | yes | yes |
| BO-170 Credential Revocation & Lifecycle Events | P08 | yes | yes |
| BO-171 Offline Cryptographic Validation Profile | P08 | yes | yes |
| BO-172 Embedded Entitlement Payload Designer | P08 | yes | yes |
| BO-173 Credential Security Simulation, Audit & Publication | P08 | yes | yes |
| BO-174 Media & Credential Command Center | P08 | yes | yes |
| BO-175 Media Type & Technology Library | P08 | yes | yes |
| BO-176 Virtual Credential & Media Association | P08 | yes | yes |
| BO-177 Verification Method Selection & Locking | P08 | yes | yes |
| BO-178 Media Issuance & Encoding Profile | P08 | yes | yes |
| BO-179 Media Swap & Replacement | P08 | yes | yes |
| BO-180 RFID & NFC Configuration | P08 | yes | yes |
| BO-181 External & Partner Credential Mapping | P08 | yes | yes |
| BO-182 Hotel, Wallet & External Media Integration | P08 | yes | yes |
| BO-183 Media Compatibility, Testing & Publication | P08 | yes | yes |
| BO-184 Biometric Access Command Center | P08 | yes | yes |
| BO-185 Biometric Verification Profile Builder | P08 | yes | yes |
| BO-186 Face Pass Enrollment Configuration | P08 | yes | yes |
| BO-187 Biometric Consent & Guardian Management | P08 | yes | yes |
| BO-188 Face Tag Temporary Enrollment | P08 | yes | yes |
| BO-189 Face Matching & Verification Thresholds | P08 | yes | yes |
| BO-190 Face Change, Re-enrollment & Identity Protection | P08 | yes | yes |
| BO-191 Biometric Validation at Gate | P08 | yes | yes |
| BO-192 Biometric Lifecycle, Retention & Deletion | P08 | yes | yes |
| BO-193 Biometric Simulation, Audit & Publication | P08 | yes | yes |
| BO-194 Device & Gate Command Center | P08 | yes | yes |
| BO-195 Device Type & Hardware Library | P08 | yes | yes |
| BO-196 Physical Device Registration & Provisioning | P08 | yes | yes |
| BO-197 Turnstile & Lane Behavior Configuration | P08 | yes | yes |
| BO-198 Validation Outcome & Guest Feedback Designer | P08 | yes | yes |
| BO-199 Reader, Scanner & Peripheral Configuration | P08 | yes | yes |
| BO-200 Handheld & Mobile Access Device Configuration | P08 | yes | yes |
| BO-201 Gate Modes, Free Spin & Emergency Controls | P08 | yes | yes |
| BO-202 Device Software, Content & Remote Configuration | P08 | yes | yes |
| BO-203 Hardware Compatibility, Health, Testing & Deployment | P08 | yes | yes |
| BO-204 Offline & Edge Operations Command Center | P08 | yes | yes |
| BO-205 Edge Node & Local Processing Configuration | P08 | yes | yes |
| BO-206 Offline Validation Policy Builder | P08 | yes | yes |
| BO-207 Edge Package & Data Distribution | P08 | yes | yes |
| BO-208 Offline Credential & Revocation Cache | P08 | yes | yes |
| BO-209 Offline Entitlement & Usage Ledger | P08 | yes | yes |
| BO-210 Connectivity Failure & Degraded Mode Policy | P08 | yes | yes |
| BO-211 Reconnection, Synchronization & Conflict Resolution | P08 | yes | yes |
| BO-212 Offline Simulation & Resilience Testing | P08 | yes | yes |
| BO-213 Edge Security, Audit & Deployment | P08 | yes | yes |
| BO-214 Guest Journey Command Center | P08 | yes | yes |
| BO-215 Group & B2B Admission Profile Builder | P08 | yes | yes |
| BO-216 Group Leader & Fast B2B Validation | P08 | yes | yes |
| BO-217 Group Attendance & Partial Entry Manager | P08 | yes | yes |
| BO-218 Family, Child, POD & Companion Journey | P08 | yes | yes |
| BO-219 Re-entry & Temporary Exit Journey | P08 | yes | yes |
| BO-220 Multi-Park & Crossover Journey Orchestrator | P08 | yes | yes |
| BO-221 Fast Pass & Attraction Access Journey | P08 | yes | yes |
| BO-222 Special Event, Free View & Alternative Admission | P08 | yes | yes |
| BO-223 Journey Simulation, Audit & Publication | P08 | yes | yes |
| BO-224 Live Access Operations Command Center | P08 | yes | yes |
| BO-225 Podium Operations Console | P08 | yes | yes |
| BO-226 Ticket & Credential Investigation Console | P08 | yes | yes |
| BO-227 Validation Exception & Reason Code Manager | P08 | yes | yes |
| BO-228 Manual Override & Supervisor Approval | P08 | yes | yes |
| BO-229 Credential Disable, Blacklist & Whitelist Operations | P08 | yes | yes |
| BO-230 Live Gate Mode & Lane Control | P08 | yes | yes |
| BO-231 Queue, Throughput & Lane Optimization | P08 | yes | yes |
| BO-232 Operational Incident & Exception Workspace | P08 | yes | yes |
| BO-233 Operations Audit, Shift Handover & Control Summary | P08 | yes | yes |
| BO-234 Dynamic Access Policy Command Center | P08 | yes | yes |
| BO-235 Access Attribute Catalog | P08 | yes | yes |
| BO-236 Visual Dynamic Policy Builder | P08 | yes | yes |
| BO-237 Context, Time, Event & Capacity Policy Builder | P08 | yes | yes |
| BO-238 Identity, Membership & Accreditation Policies | P08 | yes | yes |
| BO-239 Policy Scope, Hierarchy & Inheritance | P08 | yes | yes |
| BO-240 Authorization Governance & Temporary Access | P08 | yes | yes |
| BO-241 Policy Evaluation Architecture & Offline Distribution | P08 | yes | yes |
| BO-242 Policy Simulation, Conflict & Impact Analysis | P08 | yes | yes |
| BO-243 Policy Approval, Audit, Analytics & AI Optimization | P08 | yes | yes |
| BO-244 Access Security & Fraud Command Center | P08 | yes | yes |
| BO-245 Fraud Detection Rule & Signal Library | P08 | yes | yes |
| BO-246 Credential Sharing & Concurrent Usage Detection | P08 | yes | yes |
| BO-247 Unified Identity & Credential Lock Manager | P08 | yes | yes |
| BO-248 Biometric & Identity Integrity Monitoring | P08 | yes | yes |
| BO-249 Relationship & Companion Fraud Monitoring | P08 | yes | yes |
| BO-250 Access Risk Scoring & Decision Engine | P08 | yes | yes |
| BO-251 Real-Time Security Response & Playbook Builder | P08 | yes | yes |
| BO-252 Security Investigation & Evidence Workspace | P08 | yes | yes |
| BO-253 Security Analytics, AI Detection & Governance | P08 | yes | yes |
| BO-254 Access Monitoring & Analytics Command Center | P08 | yes | yes |
| BO-255 Live Venue Occupancy & People Counting | P08 | yes | yes |
| BO-256 Graphical Access Map & Live Gate Performance | P08 | yes | yes |
| BO-257 Attendance & Admission Analytics | P08 | yes | yes |
| BO-258 Entry, Exit, Re-entry & Crossover Analytics | P08 | yes | yes |
| BO-259 Throughput, Queue & Validation Performance Analytics | P08 | yes | yes |
| BO-260 Validation Outcome & Rejection Analytics | P08 | yes | yes |
| BO-261 Guest Dwell Time, Length of Stay & Attraction Flow | P08 | yes | yes |
| BO-262 Access Reports, Scheduled Reporting & Data Export | P08 | yes | yes |
| BO-263 AI Access Intelligence, Forecasting & Executive Insights | P08 | yes | yes |
| BO-264 Group Sales Command Center | P08 | yes | yes |
| BO-265 Group Enquiry & Opportunity Capture | P08 | yes | yes |
| BO-266 Group Customer & Organization Profile | P08 | yes | yes |
| BO-267 Group Requirements, Availability & Capacity Planner | P08 | yes | yes |
| BO-268 Group Package & Experience Builder | P08 | yes | yes |
| BO-269 Group Quotation Builder & Proposal Generation | P08 | yes | yes |
| BO-270 Quote Revision, Negotiation & Version Management | P08 | yes | yes |
| BO-271 Group Discount, Exception & Approval Workflow | P08 | yes | yes |
| BO-272 Quote-to-Booking Conversion & Confirmation | P08 | yes | yes |
| BO-273 Group Booking 360° & Handover Workspace | P08 | yes | yes |
| BO-274 Group Booking Operations Command Center | P08 | yes | yes |
| BO-275 Group Operational Planning & Task Workspace | P08 | yes | yes |
| BO-276 Participants, Guest Lists & Group Structure | P08 | yes | yes |
| BO-277 Group Payment, Deposit & Balance Management | P08 | yes | yes |
| BO-278 Group Ticket, Seat & Entitlement Allocation | P08 | yes | yes |
| BO-279 Group Ticket Fulfillment & Distribution | P08 | yes | yes |
| BO-280 Group Arrival, Check-In & Admission Operations | P08 | yes | yes |
| BO-281 Group Amendments, Cancellation & Refund Operations | P08 | yes | yes |
| BO-282 Group Booking Reconciliation, Closure & Performance | P08 | yes | yes |
| BO-283 Group Sales Analytics & AI Intelligence Center | P08 | yes | yes |
| BO-284 Membership & Annual Pass Command Center | P08 | yes | yes |
| BO-285 Membership Product & Tier Builder | P08 | yes | yes |
| BO-286 Membership Eligibility & Qualification Rule Builder | P08 | yes | yes |
| BO-287 Validity, Activation & Expiry Configuration | P08 | yes | yes |
| BO-288 Membership Entitlement & Admission Benefit Builder | P08 | yes | yes |
| BO-289 Membership Usage, Visit & Consumption Rules | P08 | yes | yes |
| BO-290 Family, Household & Dependent Membership Configuration | P08 | yes | yes |
| BO-291 Membership Commercial, Pricing & Channel Association | P08 | yes | yes |
| BO-292 Renewal, Auto-Renewal & Membership Continuity Configuration | P08 | yes | yes |
| BO-293 Membership Product Validation, Approval, Publication & Versioning | P08 | yes | yes |
| BO-294 Member Operations Command Center | P08 | yes | yes |
| BO-295 Member 360° Membership Account Workspace | P08 | yes | yes |
| BO-296 Membership Activation, Assignment & Credential Management | P08 | yes | yes |
| BO-297 Visit, Admission & Entitlement Usage Monitor | P08 | yes | yes |
| BO-298 Membership Freeze, Suspension & Reactivation Management | P08 | yes | yes |
| BO-299 Membership Upgrade, Downgrade & Product Migration Operations | P08 | yes | yes |
| BO-300 Renewal Operations & Auto-Renewal Management | P08 | yes | yes |
| BO-301 Member Exceptions, Overrides & Service Recovery | P08 | yes | yes |
| BO-302 Member Lifecycle History, Audit & Case Timeline | P08 | yes | yes |
| BO-303 Membership Analytics, Renewal Intelligence & AI Retention Center | P08 | yes | yes |
| BO-304 Order & Reservation Command Center | P08 | yes | yes |
| BO-305 Order Detail & Transaction Workspace | P08 | yes | yes |
| BO-306 Reservation & Hold Policy Configuration | P08 | yes | yes |
| BO-307 Order & Reservation Status Lifecycle Configuration | P08 | yes | yes |
| BO-308 Order Creation & Source/Channel Configuration | P08 | yes | yes |
| BO-309 Customer, Guest & Account Assignment | P08 | yes | yes |
| BO-310 Order Line, Product & Entitlement Composition | P08 | yes | yes |
| BO-311 Capacity Reservation & Inventory Commitment | P08 | yes | yes |
| BO-312 Reservation Confirmation, Expiry & Fulfillment Readiness | P08 | yes | yes |
| BO-313 Order Lifecycle Timeline, SLA, Exceptions & AI Operations | P08 | yes | yes |
| BO-314 Amendment & After-Sales Command Center | P08 | yes | yes |
| BO-315 Order Amendment Workspace | P08 | yes | yes |
| BO-316 Amendment Eligibility & Policy Rule Builder | P08 | yes | yes |
| BO-317 Cancellation & Partial Cancellation Policy Configuration | P08 | yes | yes |
| BO-318 Refund Policy & Refund Calculation Configuration | P08 | yes | yes |
| BO-319 Void, Reversal & Same-Day Correction Management | P08 | yes | yes |
| BO-320 Ticket Reissue & Fulfillment Regeneration | P08 | yes | yes |
| BO-321 After-Sales Financial Settlement & Adjustment Workspace | P08 | yes | yes |
| BO-322 Approval, Exception & Service Recovery Management | P08 | yes | yes |
| BO-323 Amendment History, Audit & After-Sales Analytics | P08 | yes | yes |
| BO-324 Payment & Order Financial Command Center | P08 | yes | yes |
| BO-325 Order Payment Detail & Transaction Ledger | P08 | yes | yes |
| BO-326 Multi-Payment, Split Tender & Payment Allocation Configuration | P08 | yes | yes |
| BO-327 Deposit, Partial Payment & Outstanding Balance Management | P08 | yes | yes |
| BO-328 Order Split, Merge & Transaction Relationship Management | P08 | yes | yes |
| BO-329 Related Order & Transaction Relationship Explorer | P08 | yes | yes |
| BO-330 External Payment, Partner & Settlement Reference Mapping | P08 | yes | yes |
| BO-331 Payment Reconciliation & Exception Management | P08 | yes | yes |
| BO-332 Financial Traceability, Control & Audit Explorer | P08 | yes | yes |
| BO-333 Order Financial Analytics & AI Reconciliation Intelligence | P08 | yes | yes |
| BO-334 Virtual Ticket Command Center | P08 | yes | yes |
| BO-335 Virtual Ticket Identity & Master Record Configuration | P08 | yes | yes |
| BO-336 Virtual Ticket Status & Lifecycle Model | P08 | yes | yes |
| BO-337 Media Type & Credential Technology Registry | P08 | yes | yes |
| BO-338 Multi-Media Binding & Association Rules | P08 | yes | yes |
| BO-339 Credential Identity, Token & Reference Mapping | P08 | yes | yes |
| BO-340 Entitlement & Cross-Media Synchronization Rules | P08 | yes | yes |
| BO-341 Media Activation, Priority & Fallback Rules | P08 | yes | yes |
| BO-342 Media Replacement, Revocation & Rebinding Rules | P08 | yes | yes |
| BO-343 Virtual Ticket Architecture Testing, Governance & Audit | P08 | yes | yes |
| BO-344 Media Design Studio Command Center | P08 | yes | yes |
| BO-345 Digital QR & Barcode Ticket Designer | P08 | yes | yes |
| BO-346 PDF, Printable & POS Ticket Designer | P08 | yes | yes |
| BO-347 Apple Wallet Pass Designer | P08 | yes | yes |
| BO-348 Google Wallet Pass Designer | P08 | yes | yes |
| BO-349 RFID, NFC, Card & Wristband Media Designer | P08 | yes | yes |
| BO-350 Digital Card, Membership & Wearable Designer | P08 | yes | yes |
| BO-351 Dynamic Fields, Data Mapping & Content Builder | P08 | yes | yes |
| BO-352 Branding, Localization & Template Inheritance | P08 | yes | yes |
| BO-353 Multi-Media Preview, Testing, Approval & Publication | P08 | yes | yes |
| BO-354 Credential Operations Command Center | P08 | yes | yes |
| BO-355 Virtual Ticket & Credential 360° Workspace | P08 | yes | yes |
| BO-356 Credential Generation & Issuance Monitor | P08 | yes | yes |
| BO-357 Credential Delivery & Distribution Operations | P08 | yes | yes |
| BO-358 Media Binding, Activation & Assignment Operations | P08 | yes | yes |
| BO-359 Credential Replacement, Reissue, Revocation & Recovery | P08 | yes | yes |
| BO-360 Failed Generation, Delivery & Credential Exception Management | P08 | yes | yes |
| BO-361 Credential Usage & Cross-Media Traceability | P08 | yes | yes |
| BO-362 Credential Security, Audit & Operational Evidence | P08 | yes | yes |
| BO-363 Ticket Media Analytics & AI Operations Intelligence | P08 | yes | yes |
| ADM-009 Tenant Billing & Invoicing | P09 | yes | no |
| ADM-010 Usage Metering | P09 | yes | no |
| ADM-011 Licence & Seat Management | P09 | yes | no |
| ADM-013 Tenant Performance Monitor | P09 | yes | no |
| ADM-014 Auto-Scaling Configuration | P09 | yes | no |
| ADM-015 API Rate Limit & Quota Management | P09 | yes | no |
| ADM-016 White-Label Branding Management | P09 | yes | no |
| ADM-017 Domain & Certificate Management | P09 | yes | no |
| ADM-018 Localisation & Language Pack | P09 | yes | no |
| ADM-019 Global Configuration & Defaults | P09 | yes | no |
| ADM-020 Platform User Directory | P09 | yes | no |
| ADM-021 Platform Role Management | P09 | yes | no |
| ADM-022 Release & Version Management | P09 | yes | no |
| ADM-024 Release Notification Composer | P09 | yes | no |
| ADM-025 Tenant Upgrade Scheduler | P09 | yes | no |
| ADM-026 End-of-Support Notice Management | P09 | yes | no |
| ADM-028 Environment Registry | P09 | yes | no |
| ADM-030 Infrastructure Sizing & Scaling Policy | P09 | yes | no |
| ADM-031 Security & Compliance Dashboard | P09 | yes | no |
| ADM-032 WAF & Security Policy View | P09 | yes | no |
| ADM-033 Backup & DR Status | P09 | yes | no |
| ADM-034 Archival Job Monitor | P09 | yes | no |
| ADM-035 Support & Escalation Console | P09 | yes | no |
| ADM-036 Platform Notification Broadcast | P09 | yes | no |
| ADM-037 AI Provider & Credentials | P09 | yes | no |
| ADM-038 Communication Service Command Center | P09 | yes | yes |
| ADM-039 Channel & Provider Configuration | P09 | yes | yes |
| ADM-040 Sender Identity, Domain & Brand Configuration | P09 | yes | yes |
| ADM-041 System Transactional Template Registry | P09 | yes | yes |
| ADM-042 Business Event & Notification Trigger Mapping | P09 | yes | yes |
| ADM-043 Routing, Priority, Throttling & Fallback Rules | P09 | yes | yes |
| ADM-044 Consent, Preference & Communication Policy Enforcement | P09 | yes | yes |
| ADM-045 Delivery Queue, Failure & Retry Management | P09 | yes | yes |
| ADM-046 Provider Health, Usage & Cost Monitoring | P09 | yes | yes |
| ADM-047 AI Delivery Optimization & Communication Platform Diagnostics | P09 | yes | yes |
| ADM-048 Commercial Pricing Command Center | P09 | yes | yes |
| ADM-049 Price List Master Configuration | P09 | yes | yes |
| ADM-050 Price Category & Rate Type Library | P09 | yes | yes |
| ADM-051 Rate Structure Builder | P09 | yes | yes |
| ADM-052 Product & Service Price Assignment | P09 | yes | yes |
| ADM-053 Package, Bundle & Add-On Pricing | P09 | yes | yes |
| ADM-054 Market, Venue & Currency Pricing Structure | P09 | yes | yes |
| ADM-055 Price Hierarchy & Inheritance Configuration | P09 | yes | yes |
| ADM-056 Price List Templates, Clone & Reuse | P09 | yes | yes |
| ADM-057 Commercial Pricing Structure Validation | P09 | yes | yes |
| ADM-058 Pricing Rule Command Center | P09 | yes | yes |
| ADM-059 Customer Segment & Profile Pricing Rules | P09 | yes | yes |
| ADM-060 Membership & Loyalty Pricing Rules | P09 | yes | yes |
| ADM-061 Residency, Nationality & Market Pricing Rules | P09 | yes | yes |
| ADM-062 Channel-Based Pricing Rules | P09 | yes | yes |
| ADM-063 Location, Venue & Event Pricing Rules | P09 | yes | yes |
| ADM-064 Quantity, Group & Volume Pricing Rules | P09 | yes | yes |
| ADM-065 Effective Date, Season & Day-Based Pricing Rules | P09 | yes | yes |