# Two worklists, itemised

Every row below is read off the package on disk — `ticvai/`, platform pages derived
2026-08-31 — by the same two builders the viewer reads: `viewer/lib/platforms.mjs`
and `viewer/lib/uiux.mjs`. Nothing here was typed by anybody. The gaps are closure
over the lineage and the flows; the frames are closure over the boards.

- [Part 1 — the derived gaps](#part-1--the-derived-gaps) · 1076 across 14 of 15 platforms
- [Part 2 — the unclaimed frames](#part-2--the-unclaimed-frames) · 811 across 74 boards
- [Part 3 — reconciliation](#part-3--reconciliation-if-your-count-differs) · what to diff if your count differs

---

## Part 1 — the derived gaps

**1076 derived gaps across 14 of the 15 platforms, 1 clean.**

492 screens · 1392 operations · 1054 operations reaching no screen · 0 undrawn.

Four kinds of missing thing:

- **1054** — Operations with no screen: in a contract this platform uses, callable by its audience, reaching no screen anywhere. On 14 platforms.
- **22** — Modules split across waves: sells in one wave, cannot finish the job until a later one. On 9 platforms.
- **0** — Screens not drawn: exists on paper, nobody has seen it. On 0 platforms.
- **0** — Flows naming a missing screen: the journey needs a screen that does not exist. On 0 platforms.

**Read the 1076 as platform × gap rows, not as 1076 distinct missing things.** An
operation reaching no screen is a gap on every platform whose contracts include it, so
the same operation is counted once per platform it fails. The 1054 operation rows are
**252 distinct operations**; the 22 wave rows are **18 distinct modules**. Both readings are
legitimate — a delivery lead owns one platform and wants their row count — but they are
different numbers and the itemised list below is per platform.

### Every platform, worst first

| # | Platform | Audience | Screens | Ops | No screen | Split waves | Not drawn | Flows → missing | Gaps |
|--:|---|---|--:|--:|--:|--:|--:|--:|--:|
| 1 | `P08` Venue Management — Back Office | staff | 143 | 441 | 220 | 8 | 0 | 0 | **228** |
| 2 | `P04` Venue POS — Terminal and Tablet | staff | 24 | 118 | 188 | 2 | 0 | 0 | **190** |
| 3 | `P06` Venue Staff App — Operations | staff | 66 | 180 | 145 | 1 | 0 | 0 | **146** |
| 4 | `P13` Venue CMS — White Label | staff | 20 | 77 | 118 | 0 | 0 | 0 | **118** |
| 5 | `P16` Venue Analytics — Cross-Domain Reporting | staff | 10 | 20 | 102 | 0 | 0 | 0 | **102** |
| 6 | `P09` TICVAI Web — Platform Console | platformAdmin | 37 | 110 | 70 | 1 | 0 | 0 | **71** |
| 7 | `P12` Venue Support — Agent Console | staff | 8 | 33 | 59 | 1 | 0 | 0 | **60** |
| 8 | `P07` Venue Scanner — Access Control | staff | 11 | 23 | 40 | 0 | 0 | 0 | **40** |
| 9 | `P01` Guest Web — Storefront | guest | 46 | 113 | 28 | 5 | 0 | 0 | **33** |
| 10 | `P15` Kitchen Display — Pass and Stations | staff | 10 | 24 | 31 | 0 | 0 | 0 | **31** |
| 11 | `P02` Guest App — Mobile | guest | 63 | 101 | 28 | 2 | 0 | 0 | **30** |
| 12 | `P05` Guest Kiosk — Self-Service | guest | 17 | 23 | 21 | 0 | 0 | 0 | **21** |
| 13 | `P10` Partner Web — Reseller Portal | partner | 21 | 105 | 3 | 1 | 0 | 0 | **4** |
| 14 | `P14` Developer Portal | partner | 8 | 21 | 1 | 1 | 0 | 0 | **2** |
| 15 | `P11` Accreditation Web — Applications | public | 8 | 3 | 0 | 0 | 0 | 0 | **0** |
| | **Total** | | **492** | **1392** | **1054** | **22** | **0** | **0** | **1076** |

`Ops` is what this platform's own screens call; `No screen` is drawn from a different
population — every operation in the contracts this platform uses, callable by its
audience, reaching no screen on any platform. That is why six platforms show more
no-screen gaps than operations. It is not an arithmetic error, it is two populations.

### The 252 distinct operations behind the 1054 rows

Sorted by how many platforms each one fails on. Fix one row here and it clears from
every platform in the last column at once.

| # | Operation | Contract | Verb | Platforms | On | Summary |
|--:|---|---|---|---|--:|---|
| 1 | `createMfaChallenge` | identity | POST | P01 P02 P04 P06 P07 P08 P09 P10 P12 P13 P16 | 11 | Step-up authentication for a sensitive action |
| 2 | `exportSubjectData` | identity | POST | P01 P02 P04 P06 P07 P08 P09 P12 P13 P16 | 10 | Everything the platform holds about one guest |
| 3 | `createReferral` | marketing-crm | POST | P01 P02 P04 P05 P06 P08 P12 P13 P16 | 9 | Issue a referral code |
| 4 | `getMyChallenges` | marketing-crm | GET | P01 P02 P04 P05 P06 P08 P12 P13 P16 | 9 | Active challenges and how far along I am |
| 5 | `getWaiverStatus` | marketing-crm | GET | P01 P02 P04 P05 P06 P08 P12 P13 P16 | 9 | Whether this guest may be issued a ticket that requires a waiver |
| 6 | `recordLostItem` | marketing-crm | POST | P01 P02 P04 P05 P06 P08 P12 P13 P16 | 9 | Report something lost, or hand something in |
| 7 | `submitForm` | marketing-crm | POST | P01 P02 P04 P05 P06 P08 P12 P13 P16 | 9 | Sign a waiver, answer a survey, capture details |
| 8 | `updateGuestPreferences` | marketing-crm | PUT | P01 P02 P04 P05 P06 P08 P12 P13 P16 | 9 | The things a regular should not have to say twice |
| 9 | `uploadGuestDocument` | marketing-crm | POST | P01 P02 P04 P05 P06 P08 P12 P13 P16 | 9 | Store a guest photo, ID or signed document |
| 10 | `convertToTermProduct` | orders | POST | P01 P02 P04 P05 P06 P07 P08 P13 P16 | 9 | Turn a visit into a membership or season pass |
| 11 | `createResaleListing` | orders | POST | P01 P02 P04 P05 P06 P07 P08 P13 P16 | 9 | List an entitlement for resale |
| 12 | `getGroupBooking` | orders | GET | P01 P02 P04 P05 P06 P07 P08 P13 P16 | 9 |  |
| 13 | `listPaymentTokens` | orders | GET | P01 P02 P04 P05 P06 P07 P08 P13 P16 | 9 | A guest's saved payment methods |
| 14 | `quoteUpgrade` | orders | POST | P01 P02 P04 P05 P06 P07 P08 P13 P16 | 9 | What an upgrade costs, pro-rata |
| 15 | `shareEntitlement` | orders | POST | P01 P02 P04 P05 P06 P07 P08 P13 P16 | 9 | Let somebody else use this, without giving it away |
| 16 | `storePaymentToken` | orders | POST | P01 P02 P04 P05 P06 P07 P08 P13 P16 | 9 | Save a payment method for future use |
| 17 | `setPasswordPolicy` | identity | PUT | P04 P06 P07 P08 P09 P12 P13 P16 | 8 | Length, breach check, lockout and step-up |
| 18 | `setSegregationRules` | identity | PUT | P04 P06 P07 P08 P09 P12 P13 P16 | 8 | Which permissions may not be held together |
| 19 | `freezeEntitlement` | catalogue | POST | P01 P02 P04 P05 P06 P08 P16 | 7 | Pause a membership at the guest's request |
| 20 | `cancelReportExecution` | reporting | DELETE | P04 P06 P08 P09 P12 P15 P16 | 7 | Cancel a running execution |
| 21 | `deleteReportSchedule` | reporting | DELETE | P04 P06 P08 P09 P12 P15 P16 | 7 | Delete a schedule |
| 22 | `exportReportResult` | reporting | POST | P04 P06 P08 P09 P12 P15 P16 | 7 | Export a completed result |
| 23 | `getReportExecution` | reporting | GET | P04 P06 P08 P09 P12 P15 P16 | 7 | Execution status and result |
| 24 | `getReportExport` | reporting | GET | P04 P06 P08 P09 P12 P15 P16 | 7 | Export status and download link |
| 25 | `getReportResult` | reporting | GET | P04 P06 P08 P09 P12 P15 P16 | 7 | Paged result rows |
| 26 | `listAlertRules` | reporting | GET | P04 P06 P08 P09 P12 P15 P16 | 7 | What raises an alert, and when |
| 27 | `listReportFields` | reporting | GET | P04 P06 P08 P09 P12 P15 P16 | 7 | Fields available for a data source |
| 28 | `listReportSchedules` | reporting | GET | P04 P06 P08 P09 P12 P15 P16 | 7 | List scheduled reports |
| 29 | `listSeededReports` | reporting | GET | P04 P06 P08 P09 P12 P15 P16 | 7 |  |
| 30 | `updateReportSchedule` | reporting | PATCH | P04 P06 P08 P09 P12 P15 P16 | 7 | Amend, pause or resume a schedule |
| 31 | `enrolFacePass` | access | POST | P01 P02 P04 P06 P07 P08 | 6 | Register a facial profile against an entitlement |
| 32 | `getFacePassEnrolment` | access | GET | P01 P02 P04 P06 P07 P08 | 6 | Whether a pass has a face registered, and when |
| 33 | `revokeFacePass` | access | DELETE | P01 P02 P04 P06 P07 P08 | 6 | Remove a facial profile |
| 34 | `activateJourney` | marketing-crm | POST | P04 P06 P08 P12 P13 P16 | 6 | Start it, or stop it |
| 35 | `addGuestNote` | marketing-crm | POST | P04 P06 P08 P12 P13 P16 | 6 | What the floor needs to know about this table |
| 36 | `addSuppression` | marketing-crm | POST | P04 P06 P08 P12 P13 P16 | 6 | Suppress an address |
| 37 | `createChallenge` | marketing-crm | POST | P04 P06 P08 P12 P13 P16 | 6 | Define a challenge, mission or streak |
| 38 | `createForm` | marketing-crm | POST | P04 P06 P08 P12 P13 P16 | 6 | Define a waiver, survey or capture form |
| 39 | `createInvitationCampaign` | marketing-crm | POST | P04 P06 P08 P12 P13 P16 | 6 | A quota-bounded, addressed invitation |
| 40 | `createLoyaltyProgramme` | marketing-crm | POST | P04 P06 P08 P12 P13 P16 | 6 | Create a loyalty programme |
| 41 | `createUrlRedirect` | marketing-crm | POST | P04 P06 P08 P12 P13 P16 | 6 | 301, 302 and custom redirects |
| 42 | `getJourneyPerformance` | marketing-crm | GET | P04 P06 P08 P12 P13 P16 | 6 | Entrants, completions, goals reached |
| 43 | `getLostItemMatches` | marketing-crm | GET | P04 P06 P08 P12 P13 P16 | 6 | Candidate matches, scored |
| 44 | `getSuppressionList` | marketing-crm | GET | P04 P06 P08 P12 P13 P16 | 6 | Addresses suppressed from all sending |
| 45 | `listMessageTriggers` | marketing-crm | GET | P04 P06 P08 P12 P13 P16 | 6 | What fires a message, and when |
| 46 | `listReviews` | marketing-crm | GET | P04 P06 P08 P12 P13 P16 | 6 | List guest reviews and ratings |
| 47 | `listSegmentMembers` | marketing-crm | GET | P04 P06 P08 P12 P13 P16 | 6 | List guests currently matching a segment |
| 48 | `matchGuest` | marketing-crm | POST | P04 P06 P08 P12 P13 P16 | 6 | Is this the same person we already have? |
| 49 | `mergeGuests` | marketing-crm | POST | P04 P06 P08 P12 P13 P16 | 6 | Two records, one person |
| 50 | `recordPrivacyIncident` | marketing-crm | POST | P04 P06 P08 P12 P13 P16 | 6 | Log a personal-data breach and start the clock |
| 51 | `respondToReview` | marketing-crm | POST | P04 P06 P08 P12 P13 P16 | 6 | Respond to a review |
| 52 | `retryMessageDispatch` | marketing-crm | POST | P04 P06 P08 P12 P13 P16 | 6 | Send it again, or by another channel |
| 53 | `setCallDisposition` | marketing-crm | POST | P04 P06 P08 P12 P13 P16 | 6 | Why the conversation ended, and any callback |
| 54 | `setConsentPurposes` | marketing-crm | PUT | P04 P06 P08 P12 P13 P16 | 6 | Configure consent purposes |
| 55 | `setMessageTrigger` | marketing-crm | POST | P04 P06 P08 P12 P13 P16 | 6 | Fire a message from a platform event |
| 56 | `setSeoMetadata` | marketing-crm | PUT | P04 P06 P08 P12 P13 P16 | 6 | Titles, descriptions, canonicals and hreflang |
| 57 | `startKioskAssist` | marketing-crm | POST | P04 P06 P08 P12 P13 P16 | 6 | A staff member helps a guest at a kiosk, remotely |
| 58 | `captureStoredValue` | orders | POST | P04 P06 P07 P08 P13 P16 | 6 | Take some or all of a held balance |
| 59 | `convertReservation` | orders | POST | P04 P06 P07 P08 P13 P16 | 6 | Convert a reservation into an order |
| 60 | `createPaymentLink` | orders | POST | P04 P06 P07 P08 P13 P16 | 6 | Send a guest a link to pay later |
| 61 | `createReservation` | orders | POST | P04 P06 P07 P08 P13 P16 | 6 | Hold without payment |
| 62 | `extendReservation` | orders | POST | P04 P06 P07 P08 P13 P16 | 6 | Extend a reservation |
| 63 | `issueInvitation` | orders | POST | P04 P06 P07 P08 P13 P16 | 6 | Issue a complimentary entitlement, with no payment expected |
| 64 | `listAbandonedCarts` | orders | GET | P04 P06 P07 P08 P13 P16 | 6 | Carts that lapsed without checking out |
| 65 | `listChargebacks` | orders | GET | P04 P06 P07 P08 P13 P16 | 6 | Open disputes, by deadline |
| 66 | `listFraudRules` | orders | GET | P04 P06 P07 P08 P13 P16 | 6 |  |
| 67 | `listInvitationAllowances` | orders | GET | P04 P06 P07 P08 P13 P16 | 6 | Who may issue comps, and how many are left |
| 68 | `listPaymentProviders` | orders | GET | P04 P06 P07 P08 P13 P16 | 6 | Gateways configured for this scope |
| 69 | `openGuestCreditAccount` | orders | POST | P04 P06 P07 P08 P13 P16 | 6 | A credit limit for an individual booking ahead |
| 70 | `printTicketProof` | orders | POST | P04 P06 P07 P08 P13 P16 | 6 | Print a sample without selling anything |
| 71 | `pushWalletPassUpdate` | orders | POST | P04 P06 P07 P08 P13 P16 | 6 | Push a change to every device holding it |
| 72 | `reissueEntitlement` | orders | POST | P04 P06 P07 P08 P13 P16 | 6 | Zero-value reissue of an expired entitlement for a later date |
| 73 | `resendPaymentLink` | orders | POST | P04 P06 P07 P08 P13 P16 | 6 |  |
| 74 | `respondToChargeback` | orders | POST | P04 P06 P07 P08 P13 P16 | 6 | Submit evidence, or accept the loss |
| 75 | `setFraudRules` | orders | PUT | P04 P06 P07 P08 P13 P16 | 6 |  |
| 76 | `setPaymentProvider` | orders | PUT | P04 P06 P07 P08 P13 P16 | 6 | Configure a gateway and its routing |
| 77 | `splitOrder` | orders | POST | P04 P06 P07 P08 P13 P16 | 6 | Break one order into independent orders |
| 78 | `voidPayment` | orders | POST | P04 P06 P07 P08 P13 P16 | 6 | Release an authorisation before it is captured |
| 79 | `transferWalletBalance` | retail | POST | P01 P02 P04 P05 P06 P08 | 6 | Send balance to another guest |
| 80 | `getRegionSettings` | tenancy | GET | P04 P06 P08 P09 P15 P16 | 6 | Read region settings |
| 81 | `updateRegionSettings` | tenancy | PUT | P04 P06 P08 P09 P15 P16 | 6 | Update region settings |
| 82 | `attachModifierGroup` | fnb | PUT | P04 P06 P08 P13 P15 | 5 | Give an item its choices |
| 83 | `clearTable` | fnb | POST | P04 P06 P08 P13 P15 | 5 | Mark a table cleared and free |
| 84 | `closeCorrectiveAction` | fnb | POST | P04 P06 P08 P13 P15 | 5 | Close a signed finding |
| 85 | `createCombo` | fnb | POST | P04 P06 P08 P13 P15 | 5 | A meal deal, priced as one thing |
| 86 | `createModifierGroup` | fnb | POST | P04 P06 P08 P13 P15 | 5 | Create a modifier group |
| 87 | `createTable` | fnb | POST | P04 P06 P08 P13 P15 | 5 | A table as a thing, not an inference |
| 88 | `escalateCorrectiveAction` | fnb | POST | P04 P06 P08 P13 P15 | 5 | Escalate a finding |
| 89 | `getTableVisit` | fnb | GET | P04 P06 P08 P13 P15 | 5 | Read a visit with all its orders |
| 90 | `rebalanceStationLoad` | fnb | POST | P04 P06 P08 P13 P15 | 5 | Move work between stations mid-service |
| 91 | `recordCorrectiveAction` | fnb | POST | P04 P06 P08 P13 P15 | 5 | Record what was done about a finding |
| 92 | `requestBill` | fnb | POST | P04 P06 P08 P13 P15 | 5 | The party asked to pay |
| 93 | `resolveBookingConflict` | fnb | GET | P04 P06 P08 P13 P15 | 5 | Two bookings, one table — and what to do about it |
| 94 | `sendBookingConfirmation` | fnb | POST | P04 P06 P08 P13 P15 | 5 | Confirm a booking, and ask them to confirm back |
| 95 | `sendOrderNotification` | fnb | POST | P04 P06 P08 P13 P15 | 5 | Tell the guest where their order is |
| 96 | `setComboSlots` | fnb | PUT | P04 P06 P08 P13 P15 | 5 | What the guest chooses, and what it costs extra |
| 97 | `setKitchenSla` | fnb | PUT | P04 P06 P08 P13 P15 | 5 | How long a ticket may sit before it is late |
| 98 | `setSectionLayout` | fnb | PUT | P04 P06 P08 P13 P15 | 5 | Divide the floor into sections and give each a server |
| 99 | `updateTable` | fnb | PUT | P04 P06 P08 P13 P15 | 5 | Change what a table is |
| 100 | `createKnowledgeCollection` | ai | POST | P06 P08 P09 P16 | 4 | Create a collection |
| 101 | `generateVenueLayout` | ai | POST | P06 P08 P09 P16 | 4 | Draft a seat map from an uploaded plan |
| 102 | `ingestKnowledgeDocument` | ai | POST | P06 P08 P09 P16 | 4 | Add a document |
| 103 | `listIndexSources` | ai | GET | P06 P08 P09 P16 | 4 | What is indexed, and how current it is |
| 104 | `listKnowledgeCollections` | ai | GET | P06 P08 P09 P16 | 4 | Collections available to this tenant |
| 105 | `proposeTranslations` | ai | POST | P06 P08 P09 P16 | 4 |  |
| 106 | `proposeWalkways` | ai | POST | P06 P08 P09 P16 | 4 | Find walkable space in a drawing that has no vectors |
| 107 | `reindexSource` | ai | POST | P06 P08 P09 P16 | 4 | Rebuild a source |
| 108 | `removeIndexEntry` | ai | DELETE | P06 P08 P09 P16 | 4 | Remove one record from the index |
| 109 | `setIndexSource` | ai | PUT | P06 P08 P09 P16 | 4 | Declare a source indexed |
| 110 | `setSuggestionProvider` | ai | PUT | P06 P08 P09 P16 | 4 |  |
| 111 | `assessProductChange` | catalogue | POST | P04 P06 P08 P16 | 4 | What a change would touch, before making it |
| 112 | `bulkChangePrices` | catalogue | POST | P04 P06 P08 P16 | 4 | Reprice a category or a whole catalogue |
| 113 | `cloneProduct` | catalogue | POST | P04 P06 P08 P16 | 4 | Copy a product as a new draft |
| 114 | `commitCatalogueImport` | catalogue | POST | P04 P06 P08 P16 | 4 | Apply a parsed catalogue import |
| 115 | `createDonationCampaign` | catalogue | POST | P04 P06 P08 P16 | 4 | Create a campaign |
| 116 | `listDonationCampaigns` | catalogue | GET | P04 P06 P08 P16 | 4 | Campaigns a guest can give to |
| 117 | `listProductVersions` | catalogue | GET | P04 P06 P08 P16 | 4 | What this product used to be |
| 118 | `listWaitlistEntries` | catalogue | GET | P04 P06 P08 P16 | 4 | Who is waiting for capacity |
| 119 | `offerWaitlistCapacity` | catalogue | POST | P04 P06 P08 P16 | 4 | Tell a waiting guest that capacity appeared |
| 120 | `reinstateEntitlement` | catalogue | POST | P04 P06 P08 P16 | 4 | Lift a suspension |
| 121 | `restoreProductVersion` | catalogue | POST | P04 P06 P08 P16 | 4 | Put a previous version back |
| 122 | `suspendEntitlement` | catalogue | POST | P04 P06 P08 P16 | 4 | Suspend or reinstate an entitlement |
| 123 | `updateDonationCampaign` | catalogue | PATCH | P04 P06 P08 P16 | 4 | Amend or close a campaign |
| 124 | `submitCountLines` | inventory | POST | P04 P06 P08 P16 | 4 | Submit counted quantities |
| 125 | `assignSeats` | seating | POST | P01 P02 P04 P08 | 4 | Pick and hold the best available seats |
| 126 | `createPartnerUser` | subscription | POST | P08 P09 P10 P13 | 4 | Add a user to a partner branch |
| 127 | `listPartnerUsers` | subscription | GET | P08 P09 P10 P13 | 4 | Users beneath a partner, by branch |
| 128 | `joinWaitlist` | catalogue | POST | P01 P02 P05 | 3 | Ask to be told if capacity frees up |
| 129 | `leaveWaitlist` | catalogue | DELETE | P01 P02 P05 | 3 | Stop waiting |
| 130 | `calculateTax` | finance | POST | P04 P08 P12 | 3 | Compute tax for a set of lines |
| 131 | `disputeObligation` | finance | POST | P04 P08 P12 | 3 | One entity disagrees with the amount |
| 132 | `getForeignTenderReport` | finance | GET | P04 P08 P12 | 3 | What was taken in which currency |
| 133 | `getUnifiedReconciliation` | finance | GET | P04 P08 P12 | 3 | Every money source against the ledger, in one view |
| 134 | `ingestFxRates` | finance | POST | P04 P08 P12 | 3 | Pull rates from the configured provider |
| 135 | `listInterEntityObligations` | finance | GET | P04 P08 P12 | 3 | What one entity owes another |
| 136 | `recordDeposit` | finance | POST | P04 P08 P12 | 3 | Money taken before the sale is complete |
| 137 | `recordSettlement` | finance | POST | P04 P08 P12 | 3 | One entity paid another |
| 138 | `recordWriteOff` | finance | POST | P04 P08 P12 | 3 | Write off an uncollectable balance |
| 139 | `resolveObligationDispute` | finance | POST | P04 P08 P12 | 3 | Agree what is actually owed |
| 140 | `runFxRevaluation` | finance | POST | P04 P08 P12 | 3 | Revalue monetary balances at close |
| 141 | `setFxProvider` | finance | PUT | P04 P08 P12 | 3 | Which provider serves which purpose |
| 142 | `validateRecognitionSchedules` | finance | POST | P04 P08 P12 | 3 | Find product kinds claimed by more than one schedule |
| 143 | `updateTableReservation` | fnb | PATCH | P01 P02 P05 | 3 | Change or cancel a booking |
| 144 | `updateMaintenancePlan` | maintenance | PATCH | P06 P08 P13 | 3 | Amend or suspend a plan |
| 145 | `respondToInvitation` | marketing-crm | POST | P01 P02 P05 | 3 | Accept or decline |
| 146 | `createCart` | orders | POST | P01 P02 P05 | 3 | Start a cart |
| 147 | `activateGiftCard` | retail | POST | P04 P06 P08 | 3 | Activate a card at the point of sale |
| 148 | `adjustWallet` | retail | POST | P04 P06 P08 | 3 | Manually adjust a wallet balance |
| 149 | `blockGiftCard` | retail | POST | P04 P06 P08 | 3 | Block a gift card |
| 150 | `cancelMerchandiseReservation` | retail | POST | P04 P06 P08 | 3 | Release a reservation |
| 151 | `closeWallet` | retail | POST | P04 P06 P08 | 3 | Close a wallet |
| 152 | `collectMerchandiseReservation` | retail | POST | P04 P06 P08 | 3 | The guest picked it up |
| 153 | `collectShopAndDrop` | retail | POST | P04 P06 P08 | 3 | Hand the goods over |
| 154 | `createRetailExchange` | retail | POST | P04 P06 P08 | 3 | Exchange one item for another |
| 155 | `createShopAndDrop` | retail | POST | P04 P06 P08 | 3 | Buy now, collect on the way out |
| 156 | `disposeShopAndDrop` | retail | POST | P04 P06 P08 | 3 | Dispose of an uncollected item |
| 157 | `issueGiftCard` | retail | POST | P04 P06 P08 | 3 | Issue or activate a gift card |
| 158 | `listRetailReturns` | retail | GET | P04 P06 P08 | 3 | List returns |
| 159 | `redeemGiftCard` | retail | POST | P04 P06 P08 | 3 | Spend against a card |
| 160 | `reinstateWallet` | retail | POST | P04 P06 P08 | 3 | Unfreeze a wallet |
| 161 | `suspendWallet` | retail | POST | P04 P06 P08 | 3 | Freeze a wallet |
| 162 | `topUpWallet` | retail | POST | P04 P06 P08 | 3 | Add value to a wallet |
| 163 | `cancelInvoice` | subscription | POST | P08 P09 P13 | 3 | Cancel or credit an invoice |
| 164 | `cancelSubscription` | subscription | POST | P08 P09 P13 | 3 | Terminate a tenant subscription |
| 165 | `disputeInvoice` | subscription | POST | P08 P09 P13 | 3 | Raise a dispute |
| 166 | `executeTenantMigration` | subscription | POST | P08 P09 P13 | 3 | Move the tenant |
| 167 | `exportPartnerInvoice` | subscription | POST | P08 P09 P13 | 3 | Partner invoice and settlement, in an ERP format |
| 168 | `launchCellCluster` | subscription | POST | P08 P09 P13 | 3 | Launch an identical cluster |
| 169 | `listCellClusters` | subscription | GET | P08 P09 P13 | 3 | Clusters in a region |
| 170 | `listTenantMigrations` | subscription | GET | P08 P09 P13 | 3 | Tenant moves between cells |
| 171 | `listVenueTypeTemplates` | subscription | GET | P08 P09 P13 | 3 | Starting configurations by venue kind |
| 172 | `planTenantMigration` | subscription | POST | P08 P09 P13 | 3 | Plan moving a tenant to another cell |
| 173 | `recordInvoicePayment` | subscription | POST | P08 P09 P13 | 3 | Record payment against an invoice |
| 174 | `resolveInvoiceDispute` | subscription | POST | P08 P09 P13 | 3 | Resolve a dispute |
| 175 | `rollbackTenantMigration` | subscription | POST | P08 P09 P13 | 3 | Roll a cutover back |
| 176 | `settleAiUsage` | subscription | POST | P08 P09 P13 | 3 | Turn metered AI interactions into a billable usage record |
| 177 | `broadcastToGuests` | workforce | POST | P04 P06 P08 | 3 |  |
| 178 | `authoriseWalletSpend` | cross-cell | POST | P07 P09 | 2 | Hold funds against the guest's home-cell balance |
| 179 | `captureWalletAuthorisation` | cross-cell | POST | P07 P09 | 2 | Capture a held amount |
| 180 | `getWalletAllocation` | cross-cell | GET | P07 P09 | 2 | The consuming cell's bounded offline allocation |
| 181 | `releaseWalletAuthorisation` | cross-cell | POST | P07 P09 | 2 | Release a hold without capturing |
| 182 | `setWalletAllocationPolicy` | cross-cell | PUT | P07 P09 | 2 | Set the allocation cap policy |
| 183 | `adjustGameCard` | games | POST | P04 P08 | 2 | Manually adjust credits or points |
| 184 | `createGame` | games | POST | P04 P08 | 2 | Register a game |
| 185 | `createPrize` | games | POST | P04 P08 | 2 | Add a prize |
| 186 | `listPrizes` | games | GET | P04 P08 | 2 | The prize catalogue |
| 187 | `redeemPrize` | games | POST | P04 P08 | 2 | Redeem points for a prize |
| 188 | `setReaderProfile` | games | PUT | P04 P08 | 2 | How a reader behaves and what it shows |
| 189 | `transferGameCard` | games | POST | P04 P08 | 2 | Move balances to another card |
| 190 | `deleteGuestAccount` | identity | DELETE | P01 P02 | 2 | Self-service account deletion |
| 191 | `skipRolloutCell` | platform-ops | POST | P08 P09 | 2 | Exclude a cell from this wave |
| 192 | `assignCoupon` | promotions | POST | P04 P08 | 2 | Assign a coupon to a named guest |
| 193 | `createUpsellRule` | promotions | POST | P04 P08 | 2 | Create an upsell rule |
| 194 | `createVoucherBatch` | promotions | POST | P04 P08 | 2 | Issue a voucher batch |
| 195 | `deleteUpsellRule` | promotions | DELETE | P04 P08 | 2 | Remove an upsell rule |
| 196 | `listAllocationSplits` | promotions | GET | P04 P08 | 2 | List allocation split definitions |
| 197 | `listBundles` | promotions | GET | P04 P08 | 2 | List bundles |
| 198 | `listUpsellRules` | promotions | GET | P04 P08 | 2 | List upsell and cross-sell rules |
| 199 | `listVoucherBatches` | promotions | GET | P04 P08 | 2 | List voucher batches |
| 200 | `previewAllocationSplit` | promotions | POST | P04 P08 | 2 | Preview how an amount divides |
| 201 | `redeemVoucher` | promotions | POST | P04 P08 | 2 | Redeem voucher value against an order |
| 202 | `setPromotionVariants` | promotions | PUT | P04 P08 | 2 | A/B test two versions against each other |
| 203 | `updateBundle` | promotions | PATCH | P04 P08 | 2 | Amend a bundle |
| 204 | `voidVoucher` | promotions | POST | P04 P08 | 2 | Cancel a voucher |
| 205 | `overrideWaitingGuest` | queue | POST | P06 P08 | 2 | Admit against a failed redemption |
| 206 | `redeemWaitingGuest` | queue | POST | P06 P08 | 2 | Admit a party at the ride |
| 207 | `cloneSeatMap` | seating | POST | P04 P08 | 2 | Clone a map, optionally into another venue |
| 208 | `commitImportJob` | seating | POST | P04 P08 | 2 | Apply a parsed import |
| 209 | `copySeatMapSection` | seating | POST | P04 P08 | 2 | Copy one section into another map |
| 210 | `createSeatCategory` | seating | POST | P04 P08 | 2 | Create a seat category |
| 211 | `createSeatMap` | seating | POST | P04 P08 | 2 | Create a seat map |
| 212 | `createSeatMapTemplate` | seating | POST | P04 P08 | 2 | Save a map as a reusable template |
| 213 | `diffSeatMapVersions` | seating | GET | P04 P08 | 2 | Compare two versions of a layout |
| 214 | `getImportJob` | seating | GET | P04 P08 | 2 | Import progress and findings |
| 215 | `getSeatingRules` | seating | GET | P04 P08 | 2 | Read seating rules |
| 216 | `getSeatMap` | seating | GET | P04 P08 | 2 | Read a seat map with its structure |
| 217 | `getSeatMapImport` | seating | GET | P04 P08 | 2 | How the import went |
| 218 | `importSeatGeometry` | seating | POST | P04 P08 | 2 | Import seat geometry from a plan |
| 219 | `importSeatManifest` | seating | POST | P04 P08 | 2 | Import the logical seat structure |
| 220 | `importSeatMap` | seating | POST | P04 P08 | 2 | Import a seat map from a plan or a manifest |
| 221 | `listSeatCategories` | seating | GET | P04 P08 | 2 | List seat categories |
| 222 | `listSeatMaps` | seating | GET | P04 P08 | 2 | List seat maps |
| 223 | `listSeatMapTemplates` | seating | GET | P04 P08 | 2 | List reusable layout templates |
| 224 | `listSeats` | seating | GET | P04 P08 | 2 | List seats in a map |
| 225 | `publishSeatMap` | seating | POST | P04 P08 | 2 | Validate and publish a seat map |
| 226 | `setMapZones` | seating | PUT | P04 P08 | 2 | Standing areas, suites, stages and obstructions |
| 227 | `setSeatingRules` | seating | PUT | P04 P08 | 2 | Set seating rules |
| 228 | `updateSeatMap` | seating | PATCH | P04 P08 | 2 | Rename or amend a seat map |
| 229 | `updateSeats` | seating | PATCH | P04 P08 | 2 | Bulk-amend seats |
| 230 | `validateSeatMap` | seating | POST | P04 P08 | 2 | Run validation without publishing |
| 231 | `acceptWalkwayProposals` | venue-map | POST | P06 P08 | 2 | Accept or reject proposed walkways |
| 232 | `createBanner` | white-label | POST | P09 P13 | 2 | Create a banner |
| 233 | `createContentBlock` | white-label | POST | P09 P13 | 2 | Author a block of content |
| 234 | `createContentPage` | white-label | POST | P09 P13 | 2 | Create a content page |
| 235 | `createPromoBlock` | white-label | POST | P09 P13 | 2 | Create a promotional block |
| 236 | `deleteBanner` | white-label | DELETE | P09 P13 | 2 | Delete a banner |
| 237 | `deleteContentPage` | white-label | DELETE | P09 P13 | 2 | Delete a content page |
| 238 | `deletePromoBlock` | white-label | DELETE | P09 P13 | 2 | Delete a promotional block |
| 239 | `getFeatureToggles` | white-label | GET | P09 P13 | 2 | Read tenant feature toggles |
| 240 | `getModuleEnablement` | white-label | GET | P09 P13 | 2 | Read module enablement |
| 241 | `getNavigation` | white-label | GET | P09 P13 | 2 | Read navigation |
| 242 | `publishContentBlock` | white-label | POST | P09 P13 | 2 | Publish now, or schedule it |
| 243 | `setFeatureToggles` | white-label | PUT | P09 P13 | 2 | Set feature toggles |
| 244 | `setFooter` | white-label | PUT | P09 P13 | 2 | Footer columns, legal links and social |
| 245 | `setHeader` | white-label | PUT | P09 P13 | 2 | Configure the header |
| 246 | `setMaintenanceMode` | white-label | PUT | P09 P13 | 2 | Enable or clear maintenance mode |
| 247 | `setModuleEnablement` | white-label | PUT | P09 P13 | 2 | Enable or disable modules |
| 248 | `setNavigation` | white-label | PUT | P09 P13 | 2 | Set main and overflow navigation |
| 249 | `updateBanner` | white-label | PATCH | P09 P13 | 2 | Amend or activate a banner |
| 250 | `updateContentPage` | white-label | PUT | P09 P13 | 2 | Amend a content page |
| 251 | `updatePromoBlock` | white-label | PATCH | P09 P13 | 2 | Amend a promotional block |
| 252 | `issueApiToken` | public-api | POST | P14 | 1 | Exchange a credential for an access token |

---

### `P08` Venue Management — Back Office — 228 gaps

venue-management-web · staff · web · operator: venue

143 screens · 441 operations · 25 contracts · 8 modules

#### Operations with no screen — 220

_in a contract this platform uses, callable by its audience, reaching no screen anywhere._

| # | Operation | Contract | Verb | Summary |
|--:|---|---|---|---|
| 1 | `enrolFacePass` | access | POST | Register a facial profile against an entitlement |
| 2 | `getFacePassEnrolment` | access | GET | Whether a pass has a face registered, and when |
| 3 | `revokeFacePass` | access | DELETE | Remove a facial profile |
| 4 | `createKnowledgeCollection` | ai | POST | Create a collection |
| 5 | `generateVenueLayout` | ai | POST | Draft a seat map from an uploaded plan |
| 6 | `ingestKnowledgeDocument` | ai | POST | Add a document |
| 7 | `listIndexSources` | ai | GET | What is indexed, and how current it is |
| 8 | `listKnowledgeCollections` | ai | GET | Collections available to this tenant |
| 9 | `proposeTranslations` | ai | POST |  |
| 10 | `proposeWalkways` | ai | POST | Find walkable space in a drawing that has no vectors |
| 11 | `reindexSource` | ai | POST | Rebuild a source |
| 12 | `removeIndexEntry` | ai | DELETE | Remove one record from the index |
| 13 | `setIndexSource` | ai | PUT | Declare a source indexed |
| 14 | `setSuggestionProvider` | ai | PUT |  |
| 15 | `assessProductChange` | catalogue | POST | What a change would touch, before making it |
| 16 | `bulkChangePrices` | catalogue | POST | Reprice a category or a whole catalogue |
| 17 | `cloneProduct` | catalogue | POST | Copy a product as a new draft |
| 18 | `commitCatalogueImport` | catalogue | POST | Apply a parsed catalogue import |
| 19 | `createDonationCampaign` | catalogue | POST | Create a campaign |
| 20 | `freezeEntitlement` | catalogue | POST | Pause a membership at the guest's request |
| 21 | `listDonationCampaigns` | catalogue | GET | Campaigns a guest can give to |
| 22 | `listProductVersions` | catalogue | GET | What this product used to be |
| 23 | `listWaitlistEntries` | catalogue | GET | Who is waiting for capacity |
| 24 | `offerWaitlistCapacity` | catalogue | POST | Tell a waiting guest that capacity appeared |
| 25 | `reinstateEntitlement` | catalogue | POST | Lift a suspension |
| 26 | `restoreProductVersion` | catalogue | POST | Put a previous version back |
| 27 | `suspendEntitlement` | catalogue | POST | Suspend or reinstate an entitlement |
| 28 | `updateDonationCampaign` | catalogue | PATCH | Amend or close a campaign |
| 29 | `calculateTax` | finance | POST | Compute tax for a set of lines |
| 30 | `disputeObligation` | finance | POST | One entity disagrees with the amount |
| 31 | `getForeignTenderReport` | finance | GET | What was taken in which currency |
| 32 | `getUnifiedReconciliation` | finance | GET | Every money source against the ledger, in one view |
| 33 | `ingestFxRates` | finance | POST | Pull rates from the configured provider |
| 34 | `listInterEntityObligations` | finance | GET | What one entity owes another |
| 35 | `recordDeposit` | finance | POST | Money taken before the sale is complete |
| 36 | `recordSettlement` | finance | POST | One entity paid another |
| 37 | `recordWriteOff` | finance | POST | Write off an uncollectable balance |
| 38 | `resolveObligationDispute` | finance | POST | Agree what is actually owed |
| 39 | `runFxRevaluation` | finance | POST | Revalue monetary balances at close |
| 40 | `setFxProvider` | finance | PUT | Which provider serves which purpose |
| 41 | `validateRecognitionSchedules` | finance | POST | Find product kinds claimed by more than one schedule |
| 42 | `attachModifierGroup` | fnb | PUT | Give an item its choices |
| 43 | `clearTable` | fnb | POST | Mark a table cleared and free |
| 44 | `closeCorrectiveAction` | fnb | POST | Close a signed finding |
| 45 | `createCombo` | fnb | POST | A meal deal, priced as one thing |
| 46 | `createModifierGroup` | fnb | POST | Create a modifier group |
| 47 | `createTable` | fnb | POST | A table as a thing, not an inference |
| 48 | `escalateCorrectiveAction` | fnb | POST | Escalate a finding |
| 49 | `getTableVisit` | fnb | GET | Read a visit with all its orders |
| 50 | `rebalanceStationLoad` | fnb | POST | Move work between stations mid-service |
| 51 | `recordCorrectiveAction` | fnb | POST | Record what was done about a finding |
| 52 | `requestBill` | fnb | POST | The party asked to pay |
| 53 | `resolveBookingConflict` | fnb | GET | Two bookings, one table — and what to do about it |
| 54 | `sendBookingConfirmation` | fnb | POST | Confirm a booking, and ask them to confirm back |
| 55 | `sendOrderNotification` | fnb | POST | Tell the guest where their order is |
| 56 | `setComboSlots` | fnb | PUT | What the guest chooses, and what it costs extra |
| 57 | `setKitchenSla` | fnb | PUT | How long a ticket may sit before it is late |
| 58 | `setSectionLayout` | fnb | PUT | Divide the floor into sections and give each a server |
| 59 | `updateTable` | fnb | PUT | Change what a table is |
| 60 | `adjustGameCard` | games | POST | Manually adjust credits or points |
| 61 | `createGame` | games | POST | Register a game |
| 62 | `createPrize` | games | POST | Add a prize |
| 63 | `listPrizes` | games | GET | The prize catalogue |
| 64 | `redeemPrize` | games | POST | Redeem points for a prize |
| 65 | `setReaderProfile` | games | PUT | How a reader behaves and what it shows |
| 66 | `transferGameCard` | games | POST | Move balances to another card |
| 67 | `createMfaChallenge` | identity | POST | Step-up authentication for a sensitive action |
| 68 | `exportSubjectData` | identity | POST | Everything the platform holds about one guest |
| 69 | `setPasswordPolicy` | identity | PUT | Length, breach check, lockout and step-up |
| 70 | `setSegregationRules` | identity | PUT | Which permissions may not be held together |
| 71 | `submitCountLines` | inventory | POST | Submit counted quantities |
| 72 | `updateMaintenancePlan` | maintenance | PATCH | Amend or suspend a plan |
| 73 | `activateJourney` | marketing-crm | POST | Start it, or stop it |
| 74 | `addGuestNote` | marketing-crm | POST | What the floor needs to know about this table |
| 75 | `addSuppression` | marketing-crm | POST | Suppress an address |
| 76 | `createChallenge` | marketing-crm | POST | Define a challenge, mission or streak |
| 77 | `createForm` | marketing-crm | POST | Define a waiver, survey or capture form |
| 78 | `createInvitationCampaign` | marketing-crm | POST | A quota-bounded, addressed invitation |
| 79 | `createLoyaltyProgramme` | marketing-crm | POST | Create a loyalty programme |
| 80 | `createReferral` | marketing-crm | POST | Issue a referral code |
| 81 | `createUrlRedirect` | marketing-crm | POST | 301, 302 and custom redirects |
| 82 | `getJourneyPerformance` | marketing-crm | GET | Entrants, completions, goals reached |
| 83 | `getLostItemMatches` | marketing-crm | GET | Candidate matches, scored |
| 84 | `getMyChallenges` | marketing-crm | GET | Active challenges and how far along I am |
| 85 | `getSuppressionList` | marketing-crm | GET | Addresses suppressed from all sending |
| 86 | `getWaiverStatus` | marketing-crm | GET | Whether this guest may be issued a ticket that requires a waiver |
| 87 | `listMessageTriggers` | marketing-crm | GET | What fires a message, and when |
| 88 | `listReviews` | marketing-crm | GET | List guest reviews and ratings |
| 89 | `listSegmentMembers` | marketing-crm | GET | List guests currently matching a segment |
| 90 | `matchGuest` | marketing-crm | POST | Is this the same person we already have? |
| 91 | `mergeGuests` | marketing-crm | POST | Two records, one person |
| 92 | `recordLostItem` | marketing-crm | POST | Report something lost, or hand something in |
| 93 | `recordPrivacyIncident` | marketing-crm | POST | Log a personal-data breach and start the clock |
| 94 | `respondToReview` | marketing-crm | POST | Respond to a review |
| 95 | `retryMessageDispatch` | marketing-crm | POST | Send it again, or by another channel |
| 96 | `setCallDisposition` | marketing-crm | POST | Why the conversation ended, and any callback |
| 97 | `setConsentPurposes` | marketing-crm | PUT | Configure consent purposes |
| 98 | `setMessageTrigger` | marketing-crm | POST | Fire a message from a platform event |
| 99 | `setSeoMetadata` | marketing-crm | PUT | Titles, descriptions, canonicals and hreflang |
| 100 | `startKioskAssist` | marketing-crm | POST | A staff member helps a guest at a kiosk, remotely |
| 101 | `submitForm` | marketing-crm | POST | Sign a waiver, answer a survey, capture details |
| 102 | `updateGuestPreferences` | marketing-crm | PUT | The things a regular should not have to say twice |
| 103 | `uploadGuestDocument` | marketing-crm | POST | Store a guest photo, ID or signed document |
| 104 | `captureStoredValue` | orders | POST | Take some or all of a held balance |
| 105 | `convertReservation` | orders | POST | Convert a reservation into an order |
| 106 | `convertToTermProduct` | orders | POST | Turn a visit into a membership or season pass |
| 107 | `createPaymentLink` | orders | POST | Send a guest a link to pay later |
| 108 | `createResaleListing` | orders | POST | List an entitlement for resale |
| 109 | `createReservation` | orders | POST | Hold without payment |
| 110 | `extendReservation` | orders | POST | Extend a reservation |
| 111 | `getGroupBooking` | orders | GET |  |
| 112 | `issueInvitation` | orders | POST | Issue a complimentary entitlement, with no payment expected |
| 113 | `listAbandonedCarts` | orders | GET | Carts that lapsed without checking out |
| 114 | `listChargebacks` | orders | GET | Open disputes, by deadline |
| 115 | `listFraudRules` | orders | GET |  |
| 116 | `listInvitationAllowances` | orders | GET | Who may issue comps, and how many are left |
| 117 | `listPaymentProviders` | orders | GET | Gateways configured for this scope |
| 118 | `listPaymentTokens` | orders | GET | A guest's saved payment methods |
| 119 | `openGuestCreditAccount` | orders | POST | A credit limit for an individual booking ahead |
| 120 | `printTicketProof` | orders | POST | Print a sample without selling anything |
| 121 | `pushWalletPassUpdate` | orders | POST | Push a change to every device holding it |
| 122 | `quoteUpgrade` | orders | POST | What an upgrade costs, pro-rata |
| 123 | `reissueEntitlement` | orders | POST | Zero-value reissue of an expired entitlement for a later date |
| 124 | `resendPaymentLink` | orders | POST |  |
| 125 | `respondToChargeback` | orders | POST | Submit evidence, or accept the loss |
| 126 | `setFraudRules` | orders | PUT |  |
| 127 | `setPaymentProvider` | orders | PUT | Configure a gateway and its routing |
| 128 | `shareEntitlement` | orders | POST | Let somebody else use this, without giving it away |
| 129 | `splitOrder` | orders | POST | Break one order into independent orders |
| 130 | `storePaymentToken` | orders | POST | Save a payment method for future use |
| 131 | `voidPayment` | orders | POST | Release an authorisation before it is captured |
| 132 | `skipRolloutCell` | platform-ops | POST | Exclude a cell from this wave |
| 133 | `assignCoupon` | promotions | POST | Assign a coupon to a named guest |
| 134 | `createUpsellRule` | promotions | POST | Create an upsell rule |
| 135 | `createVoucherBatch` | promotions | POST | Issue a voucher batch |
| 136 | `deleteUpsellRule` | promotions | DELETE | Remove an upsell rule |
| 137 | `listAllocationSplits` | promotions | GET | List allocation split definitions |
| 138 | `listBundles` | promotions | GET | List bundles |
| 139 | `listUpsellRules` | promotions | GET | List upsell and cross-sell rules |
| 140 | `listVoucherBatches` | promotions | GET | List voucher batches |
| 141 | `previewAllocationSplit` | promotions | POST | Preview how an amount divides |
| 142 | `redeemVoucher` | promotions | POST | Redeem voucher value against an order |
| 143 | `setPromotionVariants` | promotions | PUT | A/B test two versions against each other |
| 144 | `updateBundle` | promotions | PATCH | Amend a bundle |
| 145 | `voidVoucher` | promotions | POST | Cancel a voucher |
| 146 | `overrideWaitingGuest` | queue | POST | Admit against a failed redemption |
| 147 | `redeemWaitingGuest` | queue | POST | Admit a party at the ride |
| 148 | `cancelReportExecution` | reporting | DELETE | Cancel a running execution |
| 149 | `deleteReportSchedule` | reporting | DELETE | Delete a schedule |
| 150 | `exportReportResult` | reporting | POST | Export a completed result |
| 151 | `getReportExecution` | reporting | GET | Execution status and result |
| 152 | `getReportExport` | reporting | GET | Export status and download link |
| 153 | `getReportResult` | reporting | GET | Paged result rows |
| 154 | `listAlertRules` | reporting | GET | What raises an alert, and when |
| 155 | `listReportFields` | reporting | GET | Fields available for a data source |
| 156 | `listReportSchedules` | reporting | GET | List scheduled reports |
| 157 | `listSeededReports` | reporting | GET |  |
| 158 | `updateReportSchedule` | reporting | PATCH | Amend, pause or resume a schedule |
| 159 | `activateGiftCard` | retail | POST | Activate a card at the point of sale |
| 160 | `adjustWallet` | retail | POST | Manually adjust a wallet balance |
| 161 | `blockGiftCard` | retail | POST | Block a gift card |
| 162 | `cancelMerchandiseReservation` | retail | POST | Release a reservation |
| 163 | `closeWallet` | retail | POST | Close a wallet |
| 164 | `collectMerchandiseReservation` | retail | POST | The guest picked it up |
| 165 | `collectShopAndDrop` | retail | POST | Hand the goods over |
| 166 | `createRetailExchange` | retail | POST | Exchange one item for another |
| 167 | `createShopAndDrop` | retail | POST | Buy now, collect on the way out |
| 168 | `disposeShopAndDrop` | retail | POST | Dispose of an uncollected item |
| 169 | `issueGiftCard` | retail | POST | Issue or activate a gift card |
| 170 | `listRetailReturns` | retail | GET | List returns |
| 171 | `redeemGiftCard` | retail | POST | Spend against a card |
| 172 | `reinstateWallet` | retail | POST | Unfreeze a wallet |
| 173 | `suspendWallet` | retail | POST | Freeze a wallet |
| 174 | `topUpWallet` | retail | POST | Add value to a wallet |
| 175 | `transferWalletBalance` | retail | POST | Send balance to another guest |
| 176 | `assignSeats` | seating | POST | Pick and hold the best available seats |
| 177 | `cloneSeatMap` | seating | POST | Clone a map, optionally into another venue |
| 178 | `commitImportJob` | seating | POST | Apply a parsed import |
| 179 | `copySeatMapSection` | seating | POST | Copy one section into another map |
| 180 | `createSeatCategory` | seating | POST | Create a seat category |
| 181 | `createSeatMap` | seating | POST | Create a seat map |
| 182 | `createSeatMapTemplate` | seating | POST | Save a map as a reusable template |
| 183 | `diffSeatMapVersions` | seating | GET | Compare two versions of a layout |
| 184 | `getImportJob` | seating | GET | Import progress and findings |
| 185 | `getSeatMap` | seating | GET | Read a seat map with its structure |
| 186 | `getSeatMapImport` | seating | GET | How the import went |
| 187 | `getSeatingRules` | seating | GET | Read seating rules |
| 188 | `importSeatGeometry` | seating | POST | Import seat geometry from a plan |
| 189 | `importSeatManifest` | seating | POST | Import the logical seat structure |
| 190 | `importSeatMap` | seating | POST | Import a seat map from a plan or a manifest |
| 191 | `listSeatCategories` | seating | GET | List seat categories |
| 192 | `listSeatMapTemplates` | seating | GET | List reusable layout templates |
| 193 | `listSeatMaps` | seating | GET | List seat maps |
| 194 | `listSeats` | seating | GET | List seats in a map |
| 195 | `publishSeatMap` | seating | POST | Validate and publish a seat map |
| 196 | `setMapZones` | seating | PUT | Standing areas, suites, stages and obstructions |
| 197 | `setSeatingRules` | seating | PUT | Set seating rules |
| 198 | `updateSeatMap` | seating | PATCH | Rename or amend a seat map |
| 199 | `updateSeats` | seating | PATCH | Bulk-amend seats |
| 200 | `validateSeatMap` | seating | POST | Run validation without publishing |
| 201 | `cancelInvoice` | subscription | POST | Cancel or credit an invoice |
| 202 | `cancelSubscription` | subscription | POST | Terminate a tenant subscription |
| 203 | `createPartnerUser` | subscription | POST | Add a user to a partner branch |
| 204 | `disputeInvoice` | subscription | POST | Raise a dispute |
| 205 | `executeTenantMigration` | subscription | POST | Move the tenant |
| 206 | `exportPartnerInvoice` | subscription | POST | Partner invoice and settlement, in an ERP format |
| 207 | `launchCellCluster` | subscription | POST | Launch an identical cluster |
| 208 | `listCellClusters` | subscription | GET | Clusters in a region |
| 209 | `listPartnerUsers` | subscription | GET | Users beneath a partner, by branch |
| 210 | `listTenantMigrations` | subscription | GET | Tenant moves between cells |
| 211 | `listVenueTypeTemplates` | subscription | GET | Starting configurations by venue kind |
| 212 | `planTenantMigration` | subscription | POST | Plan moving a tenant to another cell |
| 213 | `recordInvoicePayment` | subscription | POST | Record payment against an invoice |
| 214 | `resolveInvoiceDispute` | subscription | POST | Resolve a dispute |
| 215 | `rollbackTenantMigration` | subscription | POST | Roll a cutover back |
| 216 | `settleAiUsage` | subscription | POST | Turn metered AI interactions into a billable usage record |
| 217 | `getRegionSettings` | tenancy | GET | Read region settings |
| 218 | `updateRegionSettings` | tenancy | PUT | Update region settings |
| 219 | `acceptWalkwayProposals` | venue-map | POST | Accept or reject proposed walkways |
| 220 | `broadcastToGuests` | workforce | POST |  |

#### Modules split across waves — 8

_sells in one wave, cannot finish the job until a later one._

| # | Module | Waves |
|--:|---|---|
| 1 | Access & Venue | 1, 2, 3 |
| 2 | Food & Beverage | 1, 2 |
| 3 | Guests & Marketing | 1, 2 |
| 4 | Orders & Money | 1, 2, 3 |
| 5 | People & Access Rights | 1, 2, 3 |
| 6 | Sell | 1, 2 |
| 7 | Stock & Supply | 1, 2 |
| 8 | Venue Operations | 1, 2 |

---

### `P04` Venue POS — Terminal and Tablet — 190 gaps

venue-pos · staff · posTerminal · operator: venue · offline capable

24 screens · 118 operations · 18 contracts · 4 modules

#### Operations with no screen — 188

_in a contract this platform uses, callable by its audience, reaching no screen anywhere._

| # | Operation | Contract | Verb | Summary |
|--:|---|---|---|---|
| 1 | `enrolFacePass` | access | POST | Register a facial profile against an entitlement |
| 2 | `getFacePassEnrolment` | access | GET | Whether a pass has a face registered, and when |
| 3 | `revokeFacePass` | access | DELETE | Remove a facial profile |
| 4 | `assessProductChange` | catalogue | POST | What a change would touch, before making it |
| 5 | `bulkChangePrices` | catalogue | POST | Reprice a category or a whole catalogue |
| 6 | `cloneProduct` | catalogue | POST | Copy a product as a new draft |
| 7 | `commitCatalogueImport` | catalogue | POST | Apply a parsed catalogue import |
| 8 | `createDonationCampaign` | catalogue | POST | Create a campaign |
| 9 | `freezeEntitlement` | catalogue | POST | Pause a membership at the guest's request |
| 10 | `listDonationCampaigns` | catalogue | GET | Campaigns a guest can give to |
| 11 | `listProductVersions` | catalogue | GET | What this product used to be |
| 12 | `listWaitlistEntries` | catalogue | GET | Who is waiting for capacity |
| 13 | `offerWaitlistCapacity` | catalogue | POST | Tell a waiting guest that capacity appeared |
| 14 | `reinstateEntitlement` | catalogue | POST | Lift a suspension |
| 15 | `restoreProductVersion` | catalogue | POST | Put a previous version back |
| 16 | `suspendEntitlement` | catalogue | POST | Suspend or reinstate an entitlement |
| 17 | `updateDonationCampaign` | catalogue | PATCH | Amend or close a campaign |
| 18 | `calculateTax` | finance | POST | Compute tax for a set of lines |
| 19 | `disputeObligation` | finance | POST | One entity disagrees with the amount |
| 20 | `getForeignTenderReport` | finance | GET | What was taken in which currency |
| 21 | `getUnifiedReconciliation` | finance | GET | Every money source against the ledger, in one view |
| 22 | `ingestFxRates` | finance | POST | Pull rates from the configured provider |
| 23 | `listInterEntityObligations` | finance | GET | What one entity owes another |
| 24 | `recordDeposit` | finance | POST | Money taken before the sale is complete |
| 25 | `recordSettlement` | finance | POST | One entity paid another |
| 26 | `recordWriteOff` | finance | POST | Write off an uncollectable balance |
| 27 | `resolveObligationDispute` | finance | POST | Agree what is actually owed |
| 28 | `runFxRevaluation` | finance | POST | Revalue monetary balances at close |
| 29 | `setFxProvider` | finance | PUT | Which provider serves which purpose |
| 30 | `validateRecognitionSchedules` | finance | POST | Find product kinds claimed by more than one schedule |
| 31 | `attachModifierGroup` | fnb | PUT | Give an item its choices |
| 32 | `clearTable` | fnb | POST | Mark a table cleared and free |
| 33 | `closeCorrectiveAction` | fnb | POST | Close a signed finding |
| 34 | `createCombo` | fnb | POST | A meal deal, priced as one thing |
| 35 | `createModifierGroup` | fnb | POST | Create a modifier group |
| 36 | `createTable` | fnb | POST | A table as a thing, not an inference |
| 37 | `escalateCorrectiveAction` | fnb | POST | Escalate a finding |
| 38 | `getTableVisit` | fnb | GET | Read a visit with all its orders |
| 39 | `rebalanceStationLoad` | fnb | POST | Move work between stations mid-service |
| 40 | `recordCorrectiveAction` | fnb | POST | Record what was done about a finding |
| 41 | `requestBill` | fnb | POST | The party asked to pay |
| 42 | `resolveBookingConflict` | fnb | GET | Two bookings, one table — and what to do about it |
| 43 | `sendBookingConfirmation` | fnb | POST | Confirm a booking, and ask them to confirm back |
| 44 | `sendOrderNotification` | fnb | POST | Tell the guest where their order is |
| 45 | `setComboSlots` | fnb | PUT | What the guest chooses, and what it costs extra |
| 46 | `setKitchenSla` | fnb | PUT | How long a ticket may sit before it is late |
| 47 | `setSectionLayout` | fnb | PUT | Divide the floor into sections and give each a server |
| 48 | `updateTable` | fnb | PUT | Change what a table is |
| 49 | `adjustGameCard` | games | POST | Manually adjust credits or points |
| 50 | `createGame` | games | POST | Register a game |
| 51 | `createPrize` | games | POST | Add a prize |
| 52 | `listPrizes` | games | GET | The prize catalogue |
| 53 | `redeemPrize` | games | POST | Redeem points for a prize |
| 54 | `setReaderProfile` | games | PUT | How a reader behaves and what it shows |
| 55 | `transferGameCard` | games | POST | Move balances to another card |
| 56 | `createMfaChallenge` | identity | POST | Step-up authentication for a sensitive action |
| 57 | `exportSubjectData` | identity | POST | Everything the platform holds about one guest |
| 58 | `setPasswordPolicy` | identity | PUT | Length, breach check, lockout and step-up |
| 59 | `setSegregationRules` | identity | PUT | Which permissions may not be held together |
| 60 | `submitCountLines` | inventory | POST | Submit counted quantities |
| 61 | `activateJourney` | marketing-crm | POST | Start it, or stop it |
| 62 | `addGuestNote` | marketing-crm | POST | What the floor needs to know about this table |
| 63 | `addSuppression` | marketing-crm | POST | Suppress an address |
| 64 | `createChallenge` | marketing-crm | POST | Define a challenge, mission or streak |
| 65 | `createForm` | marketing-crm | POST | Define a waiver, survey or capture form |
| 66 | `createInvitationCampaign` | marketing-crm | POST | A quota-bounded, addressed invitation |
| 67 | `createLoyaltyProgramme` | marketing-crm | POST | Create a loyalty programme |
| 68 | `createReferral` | marketing-crm | POST | Issue a referral code |
| 69 | `createUrlRedirect` | marketing-crm | POST | 301, 302 and custom redirects |
| 70 | `getJourneyPerformance` | marketing-crm | GET | Entrants, completions, goals reached |
| 71 | `getLostItemMatches` | marketing-crm | GET | Candidate matches, scored |
| 72 | `getMyChallenges` | marketing-crm | GET | Active challenges and how far along I am |
| 73 | `getSuppressionList` | marketing-crm | GET | Addresses suppressed from all sending |
| 74 | `getWaiverStatus` | marketing-crm | GET | Whether this guest may be issued a ticket that requires a waiver |
| 75 | `listMessageTriggers` | marketing-crm | GET | What fires a message, and when |
| 76 | `listReviews` | marketing-crm | GET | List guest reviews and ratings |
| 77 | `listSegmentMembers` | marketing-crm | GET | List guests currently matching a segment |
| 78 | `matchGuest` | marketing-crm | POST | Is this the same person we already have? |
| 79 | `mergeGuests` | marketing-crm | POST | Two records, one person |
| 80 | `recordLostItem` | marketing-crm | POST | Report something lost, or hand something in |
| 81 | `recordPrivacyIncident` | marketing-crm | POST | Log a personal-data breach and start the clock |
| 82 | `respondToReview` | marketing-crm | POST | Respond to a review |
| 83 | `retryMessageDispatch` | marketing-crm | POST | Send it again, or by another channel |
| 84 | `setCallDisposition` | marketing-crm | POST | Why the conversation ended, and any callback |
| 85 | `setConsentPurposes` | marketing-crm | PUT | Configure consent purposes |
| 86 | `setMessageTrigger` | marketing-crm | POST | Fire a message from a platform event |
| 87 | `setSeoMetadata` | marketing-crm | PUT | Titles, descriptions, canonicals and hreflang |
| 88 | `startKioskAssist` | marketing-crm | POST | A staff member helps a guest at a kiosk, remotely |
| 89 | `submitForm` | marketing-crm | POST | Sign a waiver, answer a survey, capture details |
| 90 | `updateGuestPreferences` | marketing-crm | PUT | The things a regular should not have to say twice |
| 91 | `uploadGuestDocument` | marketing-crm | POST | Store a guest photo, ID or signed document |
| 92 | `captureStoredValue` | orders | POST | Take some or all of a held balance |
| 93 | `convertReservation` | orders | POST | Convert a reservation into an order |
| 94 | `convertToTermProduct` | orders | POST | Turn a visit into a membership or season pass |
| 95 | `createPaymentLink` | orders | POST | Send a guest a link to pay later |
| 96 | `createResaleListing` | orders | POST | List an entitlement for resale |
| 97 | `createReservation` | orders | POST | Hold without payment |
| 98 | `extendReservation` | orders | POST | Extend a reservation |
| 99 | `getGroupBooking` | orders | GET |  |
| 100 | `issueInvitation` | orders | POST | Issue a complimentary entitlement, with no payment expected |
| 101 | `listAbandonedCarts` | orders | GET | Carts that lapsed without checking out |
| 102 | `listChargebacks` | orders | GET | Open disputes, by deadline |
| 103 | `listFraudRules` | orders | GET |  |
| 104 | `listInvitationAllowances` | orders | GET | Who may issue comps, and how many are left |
| 105 | `listPaymentProviders` | orders | GET | Gateways configured for this scope |
| 106 | `listPaymentTokens` | orders | GET | A guest's saved payment methods |
| 107 | `openGuestCreditAccount` | orders | POST | A credit limit for an individual booking ahead |
| 108 | `printTicketProof` | orders | POST | Print a sample without selling anything |
| 109 | `pushWalletPassUpdate` | orders | POST | Push a change to every device holding it |
| 110 | `quoteUpgrade` | orders | POST | What an upgrade costs, pro-rata |
| 111 | `reissueEntitlement` | orders | POST | Zero-value reissue of an expired entitlement for a later date |
| 112 | `resendPaymentLink` | orders | POST |  |
| 113 | `respondToChargeback` | orders | POST | Submit evidence, or accept the loss |
| 114 | `setFraudRules` | orders | PUT |  |
| 115 | `setPaymentProvider` | orders | PUT | Configure a gateway and its routing |
| 116 | `shareEntitlement` | orders | POST | Let somebody else use this, without giving it away |
| 117 | `splitOrder` | orders | POST | Break one order into independent orders |
| 118 | `storePaymentToken` | orders | POST | Save a payment method for future use |
| 119 | `voidPayment` | orders | POST | Release an authorisation before it is captured |
| 120 | `assignCoupon` | promotions | POST | Assign a coupon to a named guest |
| 121 | `createUpsellRule` | promotions | POST | Create an upsell rule |
| 122 | `createVoucherBatch` | promotions | POST | Issue a voucher batch |
| 123 | `deleteUpsellRule` | promotions | DELETE | Remove an upsell rule |
| 124 | `listAllocationSplits` | promotions | GET | List allocation split definitions |
| 125 | `listBundles` | promotions | GET | List bundles |
| 126 | `listUpsellRules` | promotions | GET | List upsell and cross-sell rules |
| 127 | `listVoucherBatches` | promotions | GET | List voucher batches |
| 128 | `previewAllocationSplit` | promotions | POST | Preview how an amount divides |
| 129 | `redeemVoucher` | promotions | POST | Redeem voucher value against an order |
| 130 | `setPromotionVariants` | promotions | PUT | A/B test two versions against each other |
| 131 | `updateBundle` | promotions | PATCH | Amend a bundle |
| 132 | `voidVoucher` | promotions | POST | Cancel a voucher |
| 133 | `cancelReportExecution` | reporting | DELETE | Cancel a running execution |
| 134 | `deleteReportSchedule` | reporting | DELETE | Delete a schedule |
| 135 | `exportReportResult` | reporting | POST | Export a completed result |
| 136 | `getReportExecution` | reporting | GET | Execution status and result |
| 137 | `getReportExport` | reporting | GET | Export status and download link |
| 138 | `getReportResult` | reporting | GET | Paged result rows |
| 139 | `listAlertRules` | reporting | GET | What raises an alert, and when |
| 140 | `listReportFields` | reporting | GET | Fields available for a data source |
| 141 | `listReportSchedules` | reporting | GET | List scheduled reports |
| 142 | `listSeededReports` | reporting | GET |  |
| 143 | `updateReportSchedule` | reporting | PATCH | Amend, pause or resume a schedule |
| 144 | `activateGiftCard` | retail | POST | Activate a card at the point of sale |
| 145 | `adjustWallet` | retail | POST | Manually adjust a wallet balance |
| 146 | `blockGiftCard` | retail | POST | Block a gift card |
| 147 | `cancelMerchandiseReservation` | retail | POST | Release a reservation |
| 148 | `closeWallet` | retail | POST | Close a wallet |
| 149 | `collectMerchandiseReservation` | retail | POST | The guest picked it up |
| 150 | `collectShopAndDrop` | retail | POST | Hand the goods over |
| 151 | `createRetailExchange` | retail | POST | Exchange one item for another |
| 152 | `createShopAndDrop` | retail | POST | Buy now, collect on the way out |
| 153 | `disposeShopAndDrop` | retail | POST | Dispose of an uncollected item |
| 154 | `issueGiftCard` | retail | POST | Issue or activate a gift card |
| 155 | `listRetailReturns` | retail | GET | List returns |
| 156 | `redeemGiftCard` | retail | POST | Spend against a card |
| 157 | `reinstateWallet` | retail | POST | Unfreeze a wallet |
| 158 | `suspendWallet` | retail | POST | Freeze a wallet |
| 159 | `topUpWallet` | retail | POST | Add value to a wallet |
| 160 | `transferWalletBalance` | retail | POST | Send balance to another guest |
| 161 | `assignSeats` | seating | POST | Pick and hold the best available seats |
| 162 | `cloneSeatMap` | seating | POST | Clone a map, optionally into another venue |
| 163 | `commitImportJob` | seating | POST | Apply a parsed import |
| 164 | `copySeatMapSection` | seating | POST | Copy one section into another map |
| 165 | `createSeatCategory` | seating | POST | Create a seat category |
| 166 | `createSeatMap` | seating | POST | Create a seat map |
| 167 | `createSeatMapTemplate` | seating | POST | Save a map as a reusable template |
| 168 | `diffSeatMapVersions` | seating | GET | Compare two versions of a layout |
| 169 | `getImportJob` | seating | GET | Import progress and findings |
| 170 | `getSeatMap` | seating | GET | Read a seat map with its structure |
| 171 | `getSeatMapImport` | seating | GET | How the import went |
| 172 | `getSeatingRules` | seating | GET | Read seating rules |
| 173 | `importSeatGeometry` | seating | POST | Import seat geometry from a plan |
| 174 | `importSeatManifest` | seating | POST | Import the logical seat structure |
| 175 | `importSeatMap` | seating | POST | Import a seat map from a plan or a manifest |
| 176 | `listSeatCategories` | seating | GET | List seat categories |
| 177 | `listSeatMapTemplates` | seating | GET | List reusable layout templates |
| 178 | `listSeatMaps` | seating | GET | List seat maps |
| 179 | `listSeats` | seating | GET | List seats in a map |
| 180 | `publishSeatMap` | seating | POST | Validate and publish a seat map |
| 181 | `setMapZones` | seating | PUT | Standing areas, suites, stages and obstructions |
| 182 | `setSeatingRules` | seating | PUT | Set seating rules |
| 183 | `updateSeatMap` | seating | PATCH | Rename or amend a seat map |
| 184 | `updateSeats` | seating | PATCH | Bulk-amend seats |
| 185 | `validateSeatMap` | seating | POST | Run validation without publishing |
| 186 | `getRegionSettings` | tenancy | GET | Read region settings |
| 187 | `updateRegionSettings` | tenancy | PUT | Update region settings |
| 188 | `broadcastToGuests` | workforce | POST |  |

#### Modules split across waves — 2

_sells in one wave, cannot finish the job until a later one._

| # | Module | Waves |
|--:|---|---|
| 1 | Sell | 1, 2 |
| 2 | Shift | 1, 2 |

---

### `P06` Venue Staff App — Operations — 146 gaps

venue-staff-app · staff · mobileApp · operator: venue · offline capable

66 screens · 180 operations · 17 contracts · 3 modules

#### Operations with no screen — 145

_in a contract this platform uses, callable by its audience, reaching no screen anywhere._

| # | Operation | Contract | Verb | Summary |
|--:|---|---|---|---|
| 1 | `enrolFacePass` | access | POST | Register a facial profile against an entitlement |
| 2 | `getFacePassEnrolment` | access | GET | Whether a pass has a face registered, and when |
| 3 | `revokeFacePass` | access | DELETE | Remove a facial profile |
| 4 | `createKnowledgeCollection` | ai | POST | Create a collection |
| 5 | `generateVenueLayout` | ai | POST | Draft a seat map from an uploaded plan |
| 6 | `ingestKnowledgeDocument` | ai | POST | Add a document |
| 7 | `listIndexSources` | ai | GET | What is indexed, and how current it is |
| 8 | `listKnowledgeCollections` | ai | GET | Collections available to this tenant |
| 9 | `proposeTranslations` | ai | POST |  |
| 10 | `proposeWalkways` | ai | POST | Find walkable space in a drawing that has no vectors |
| 11 | `reindexSource` | ai | POST | Rebuild a source |
| 12 | `removeIndexEntry` | ai | DELETE | Remove one record from the index |
| 13 | `setIndexSource` | ai | PUT | Declare a source indexed |
| 14 | `setSuggestionProvider` | ai | PUT |  |
| 15 | `assessProductChange` | catalogue | POST | What a change would touch, before making it |
| 16 | `bulkChangePrices` | catalogue | POST | Reprice a category or a whole catalogue |
| 17 | `cloneProduct` | catalogue | POST | Copy a product as a new draft |
| 18 | `commitCatalogueImport` | catalogue | POST | Apply a parsed catalogue import |
| 19 | `createDonationCampaign` | catalogue | POST | Create a campaign |
| 20 | `freezeEntitlement` | catalogue | POST | Pause a membership at the guest's request |
| 21 | `listDonationCampaigns` | catalogue | GET | Campaigns a guest can give to |
| 22 | `listProductVersions` | catalogue | GET | What this product used to be |
| 23 | `listWaitlistEntries` | catalogue | GET | Who is waiting for capacity |
| 24 | `offerWaitlistCapacity` | catalogue | POST | Tell a waiting guest that capacity appeared |
| 25 | `reinstateEntitlement` | catalogue | POST | Lift a suspension |
| 26 | `restoreProductVersion` | catalogue | POST | Put a previous version back |
| 27 | `suspendEntitlement` | catalogue | POST | Suspend or reinstate an entitlement |
| 28 | `updateDonationCampaign` | catalogue | PATCH | Amend or close a campaign |
| 29 | `attachModifierGroup` | fnb | PUT | Give an item its choices |
| 30 | `clearTable` | fnb | POST | Mark a table cleared and free |
| 31 | `closeCorrectiveAction` | fnb | POST | Close a signed finding |
| 32 | `createCombo` | fnb | POST | A meal deal, priced as one thing |
| 33 | `createModifierGroup` | fnb | POST | Create a modifier group |
| 34 | `createTable` | fnb | POST | A table as a thing, not an inference |
| 35 | `escalateCorrectiveAction` | fnb | POST | Escalate a finding |
| 36 | `getTableVisit` | fnb | GET | Read a visit with all its orders |
| 37 | `rebalanceStationLoad` | fnb | POST | Move work between stations mid-service |
| 38 | `recordCorrectiveAction` | fnb | POST | Record what was done about a finding |
| 39 | `requestBill` | fnb | POST | The party asked to pay |
| 40 | `resolveBookingConflict` | fnb | GET | Two bookings, one table — and what to do about it |
| 41 | `sendBookingConfirmation` | fnb | POST | Confirm a booking, and ask them to confirm back |
| 42 | `sendOrderNotification` | fnb | POST | Tell the guest where their order is |
| 43 | `setComboSlots` | fnb | PUT | What the guest chooses, and what it costs extra |
| 44 | `setKitchenSla` | fnb | PUT | How long a ticket may sit before it is late |
| 45 | `setSectionLayout` | fnb | PUT | Divide the floor into sections and give each a server |
| 46 | `updateTable` | fnb | PUT | Change what a table is |
| 47 | `createMfaChallenge` | identity | POST | Step-up authentication for a sensitive action |
| 48 | `exportSubjectData` | identity | POST | Everything the platform holds about one guest |
| 49 | `setPasswordPolicy` | identity | PUT | Length, breach check, lockout and step-up |
| 50 | `setSegregationRules` | identity | PUT | Which permissions may not be held together |
| 51 | `submitCountLines` | inventory | POST | Submit counted quantities |
| 52 | `updateMaintenancePlan` | maintenance | PATCH | Amend or suspend a plan |
| 53 | `activateJourney` | marketing-crm | POST | Start it, or stop it |
| 54 | `addGuestNote` | marketing-crm | POST | What the floor needs to know about this table |
| 55 | `addSuppression` | marketing-crm | POST | Suppress an address |
| 56 | `createChallenge` | marketing-crm | POST | Define a challenge, mission or streak |
| 57 | `createForm` | marketing-crm | POST | Define a waiver, survey or capture form |
| 58 | `createInvitationCampaign` | marketing-crm | POST | A quota-bounded, addressed invitation |
| 59 | `createLoyaltyProgramme` | marketing-crm | POST | Create a loyalty programme |
| 60 | `createReferral` | marketing-crm | POST | Issue a referral code |
| 61 | `createUrlRedirect` | marketing-crm | POST | 301, 302 and custom redirects |
| 62 | `getJourneyPerformance` | marketing-crm | GET | Entrants, completions, goals reached |
| 63 | `getLostItemMatches` | marketing-crm | GET | Candidate matches, scored |
| 64 | `getMyChallenges` | marketing-crm | GET | Active challenges and how far along I am |
| 65 | `getSuppressionList` | marketing-crm | GET | Addresses suppressed from all sending |
| 66 | `getWaiverStatus` | marketing-crm | GET | Whether this guest may be issued a ticket that requires a waiver |
| 67 | `listMessageTriggers` | marketing-crm | GET | What fires a message, and when |
| 68 | `listReviews` | marketing-crm | GET | List guest reviews and ratings |
| 69 | `listSegmentMembers` | marketing-crm | GET | List guests currently matching a segment |
| 70 | `matchGuest` | marketing-crm | POST | Is this the same person we already have? |
| 71 | `mergeGuests` | marketing-crm | POST | Two records, one person |
| 72 | `recordLostItem` | marketing-crm | POST | Report something lost, or hand something in |
| 73 | `recordPrivacyIncident` | marketing-crm | POST | Log a personal-data breach and start the clock |
| 74 | `respondToReview` | marketing-crm | POST | Respond to a review |
| 75 | `retryMessageDispatch` | marketing-crm | POST | Send it again, or by another channel |
| 76 | `setCallDisposition` | marketing-crm | POST | Why the conversation ended, and any callback |
| 77 | `setConsentPurposes` | marketing-crm | PUT | Configure consent purposes |
| 78 | `setMessageTrigger` | marketing-crm | POST | Fire a message from a platform event |
| 79 | `setSeoMetadata` | marketing-crm | PUT | Titles, descriptions, canonicals and hreflang |
| 80 | `startKioskAssist` | marketing-crm | POST | A staff member helps a guest at a kiosk, remotely |
| 81 | `submitForm` | marketing-crm | POST | Sign a waiver, answer a survey, capture details |
| 82 | `updateGuestPreferences` | marketing-crm | PUT | The things a regular should not have to say twice |
| 83 | `uploadGuestDocument` | marketing-crm | POST | Store a guest photo, ID or signed document |
| 84 | `captureStoredValue` | orders | POST | Take some or all of a held balance |
| 85 | `convertReservation` | orders | POST | Convert a reservation into an order |
| 86 | `convertToTermProduct` | orders | POST | Turn a visit into a membership or season pass |
| 87 | `createPaymentLink` | orders | POST | Send a guest a link to pay later |
| 88 | `createResaleListing` | orders | POST | List an entitlement for resale |
| 89 | `createReservation` | orders | POST | Hold without payment |
| 90 | `extendReservation` | orders | POST | Extend a reservation |
| 91 | `getGroupBooking` | orders | GET |  |
| 92 | `issueInvitation` | orders | POST | Issue a complimentary entitlement, with no payment expected |
| 93 | `listAbandonedCarts` | orders | GET | Carts that lapsed without checking out |
| 94 | `listChargebacks` | orders | GET | Open disputes, by deadline |
| 95 | `listFraudRules` | orders | GET |  |
| 96 | `listInvitationAllowances` | orders | GET | Who may issue comps, and how many are left |
| 97 | `listPaymentProviders` | orders | GET | Gateways configured for this scope |
| 98 | `listPaymentTokens` | orders | GET | A guest's saved payment methods |
| 99 | `openGuestCreditAccount` | orders | POST | A credit limit for an individual booking ahead |
| 100 | `printTicketProof` | orders | POST | Print a sample without selling anything |
| 101 | `pushWalletPassUpdate` | orders | POST | Push a change to every device holding it |
| 102 | `quoteUpgrade` | orders | POST | What an upgrade costs, pro-rata |
| 103 | `reissueEntitlement` | orders | POST | Zero-value reissue of an expired entitlement for a later date |
| 104 | `resendPaymentLink` | orders | POST |  |
| 105 | `respondToChargeback` | orders | POST | Submit evidence, or accept the loss |
| 106 | `setFraudRules` | orders | PUT |  |
| 107 | `setPaymentProvider` | orders | PUT | Configure a gateway and its routing |
| 108 | `shareEntitlement` | orders | POST | Let somebody else use this, without giving it away |
| 109 | `splitOrder` | orders | POST | Break one order into independent orders |
| 110 | `storePaymentToken` | orders | POST | Save a payment method for future use |
| 111 | `voidPayment` | orders | POST | Release an authorisation before it is captured |
| 112 | `overrideWaitingGuest` | queue | POST | Admit against a failed redemption |
| 113 | `redeemWaitingGuest` | queue | POST | Admit a party at the ride |
| 114 | `cancelReportExecution` | reporting | DELETE | Cancel a running execution |
| 115 | `deleteReportSchedule` | reporting | DELETE | Delete a schedule |
| 116 | `exportReportResult` | reporting | POST | Export a completed result |
| 117 | `getReportExecution` | reporting | GET | Execution status and result |
| 118 | `getReportExport` | reporting | GET | Export status and download link |
| 119 | `getReportResult` | reporting | GET | Paged result rows |
| 120 | `listAlertRules` | reporting | GET | What raises an alert, and when |
| 121 | `listReportFields` | reporting | GET | Fields available for a data source |
| 122 | `listReportSchedules` | reporting | GET | List scheduled reports |
| 123 | `listSeededReports` | reporting | GET |  |
| 124 | `updateReportSchedule` | reporting | PATCH | Amend, pause or resume a schedule |
| 125 | `activateGiftCard` | retail | POST | Activate a card at the point of sale |
| 126 | `adjustWallet` | retail | POST | Manually adjust a wallet balance |
| 127 | `blockGiftCard` | retail | POST | Block a gift card |
| 128 | `cancelMerchandiseReservation` | retail | POST | Release a reservation |
| 129 | `closeWallet` | retail | POST | Close a wallet |
| 130 | `collectMerchandiseReservation` | retail | POST | The guest picked it up |
| 131 | `collectShopAndDrop` | retail | POST | Hand the goods over |
| 132 | `createRetailExchange` | retail | POST | Exchange one item for another |
| 133 | `createShopAndDrop` | retail | POST | Buy now, collect on the way out |
| 134 | `disposeShopAndDrop` | retail | POST | Dispose of an uncollected item |
| 135 | `issueGiftCard` | retail | POST | Issue or activate a gift card |
| 136 | `listRetailReturns` | retail | GET | List returns |
| 137 | `redeemGiftCard` | retail | POST | Spend against a card |
| 138 | `reinstateWallet` | retail | POST | Unfreeze a wallet |
| 139 | `suspendWallet` | retail | POST | Freeze a wallet |
| 140 | `topUpWallet` | retail | POST | Add value to a wallet |
| 141 | `transferWalletBalance` | retail | POST | Send balance to another guest |
| 142 | `getRegionSettings` | tenancy | GET | Read region settings |
| 143 | `updateRegionSettings` | tenancy | PUT | Update region settings |
| 144 | `acceptWalkwayProposals` | venue-map | POST | Accept or reject proposed walkways |
| 145 | `broadcastToGuests` | workforce | POST |  |

#### Modules split across waves — 1

_sells in one wave, cannot finish the job until a later one._

| # | Module | Waves |
|--:|---|---|
| 1 | Operations | 1, 2, 3 |

---

### `P13` Venue CMS — White Label — 118 gaps

venue-management-web · staff · web · operator: venue

20 screens · 77 operations · 8 contracts · 1 modules

#### Operations with no screen — 118

_in a contract this platform uses, callable by its audience, reaching no screen anywhere._

| # | Operation | Contract | Verb | Summary |
|--:|---|---|---|---|
| 1 | `attachModifierGroup` | fnb | PUT | Give an item its choices |
| 2 | `clearTable` | fnb | POST | Mark a table cleared and free |
| 3 | `closeCorrectiveAction` | fnb | POST | Close a signed finding |
| 4 | `createCombo` | fnb | POST | A meal deal, priced as one thing |
| 5 | `createModifierGroup` | fnb | POST | Create a modifier group |
| 6 | `createTable` | fnb | POST | A table as a thing, not an inference |
| 7 | `escalateCorrectiveAction` | fnb | POST | Escalate a finding |
| 8 | `getTableVisit` | fnb | GET | Read a visit with all its orders |
| 9 | `rebalanceStationLoad` | fnb | POST | Move work between stations mid-service |
| 10 | `recordCorrectiveAction` | fnb | POST | Record what was done about a finding |
| 11 | `requestBill` | fnb | POST | The party asked to pay |
| 12 | `resolveBookingConflict` | fnb | GET | Two bookings, one table — and what to do about it |
| 13 | `sendBookingConfirmation` | fnb | POST | Confirm a booking, and ask them to confirm back |
| 14 | `sendOrderNotification` | fnb | POST | Tell the guest where their order is |
| 15 | `setComboSlots` | fnb | PUT | What the guest chooses, and what it costs extra |
| 16 | `setKitchenSla` | fnb | PUT | How long a ticket may sit before it is late |
| 17 | `setSectionLayout` | fnb | PUT | Divide the floor into sections and give each a server |
| 18 | `updateTable` | fnb | PUT | Change what a table is |
| 19 | `createMfaChallenge` | identity | POST | Step-up authentication for a sensitive action |
| 20 | `exportSubjectData` | identity | POST | Everything the platform holds about one guest |
| 21 | `setPasswordPolicy` | identity | PUT | Length, breach check, lockout and step-up |
| 22 | `setSegregationRules` | identity | PUT | Which permissions may not be held together |
| 23 | `updateMaintenancePlan` | maintenance | PATCH | Amend or suspend a plan |
| 24 | `activateJourney` | marketing-crm | POST | Start it, or stop it |
| 25 | `addGuestNote` | marketing-crm | POST | What the floor needs to know about this table |
| 26 | `addSuppression` | marketing-crm | POST | Suppress an address |
| 27 | `createChallenge` | marketing-crm | POST | Define a challenge, mission or streak |
| 28 | `createForm` | marketing-crm | POST | Define a waiver, survey or capture form |
| 29 | `createInvitationCampaign` | marketing-crm | POST | A quota-bounded, addressed invitation |
| 30 | `createLoyaltyProgramme` | marketing-crm | POST | Create a loyalty programme |
| 31 | `createReferral` | marketing-crm | POST | Issue a referral code |
| 32 | `createUrlRedirect` | marketing-crm | POST | 301, 302 and custom redirects |
| 33 | `getJourneyPerformance` | marketing-crm | GET | Entrants, completions, goals reached |
| 34 | `getLostItemMatches` | marketing-crm | GET | Candidate matches, scored |
| 35 | `getMyChallenges` | marketing-crm | GET | Active challenges and how far along I am |
| 36 | `getSuppressionList` | marketing-crm | GET | Addresses suppressed from all sending |
| 37 | `getWaiverStatus` | marketing-crm | GET | Whether this guest may be issued a ticket that requires a waiver |
| 38 | `listMessageTriggers` | marketing-crm | GET | What fires a message, and when |
| 39 | `listReviews` | marketing-crm | GET | List guest reviews and ratings |
| 40 | `listSegmentMembers` | marketing-crm | GET | List guests currently matching a segment |
| 41 | `matchGuest` | marketing-crm | POST | Is this the same person we already have? |
| 42 | `mergeGuests` | marketing-crm | POST | Two records, one person |
| 43 | `recordLostItem` | marketing-crm | POST | Report something lost, or hand something in |
| 44 | `recordPrivacyIncident` | marketing-crm | POST | Log a personal-data breach and start the clock |
| 45 | `respondToReview` | marketing-crm | POST | Respond to a review |
| 46 | `retryMessageDispatch` | marketing-crm | POST | Send it again, or by another channel |
| 47 | `setCallDisposition` | marketing-crm | POST | Why the conversation ended, and any callback |
| 48 | `setConsentPurposes` | marketing-crm | PUT | Configure consent purposes |
| 49 | `setMessageTrigger` | marketing-crm | POST | Fire a message from a platform event |
| 50 | `setSeoMetadata` | marketing-crm | PUT | Titles, descriptions, canonicals and hreflang |
| 51 | `startKioskAssist` | marketing-crm | POST | A staff member helps a guest at a kiosk, remotely |
| 52 | `submitForm` | marketing-crm | POST | Sign a waiver, answer a survey, capture details |
| 53 | `updateGuestPreferences` | marketing-crm | PUT | The things a regular should not have to say twice |
| 54 | `uploadGuestDocument` | marketing-crm | POST | Store a guest photo, ID or signed document |
| 55 | `captureStoredValue` | orders | POST | Take some or all of a held balance |
| 56 | `convertReservation` | orders | POST | Convert a reservation into an order |
| 57 | `convertToTermProduct` | orders | POST | Turn a visit into a membership or season pass |
| 58 | `createPaymentLink` | orders | POST | Send a guest a link to pay later |
| 59 | `createResaleListing` | orders | POST | List an entitlement for resale |
| 60 | `createReservation` | orders | POST | Hold without payment |
| 61 | `extendReservation` | orders | POST | Extend a reservation |
| 62 | `getGroupBooking` | orders | GET |  |
| 63 | `issueInvitation` | orders | POST | Issue a complimentary entitlement, with no payment expected |
| 64 | `listAbandonedCarts` | orders | GET | Carts that lapsed without checking out |
| 65 | `listChargebacks` | orders | GET | Open disputes, by deadline |
| 66 | `listFraudRules` | orders | GET |  |
| 67 | `listInvitationAllowances` | orders | GET | Who may issue comps, and how many are left |
| 68 | `listPaymentProviders` | orders | GET | Gateways configured for this scope |
| 69 | `listPaymentTokens` | orders | GET | A guest's saved payment methods |
| 70 | `openGuestCreditAccount` | orders | POST | A credit limit for an individual booking ahead |
| 71 | `printTicketProof` | orders | POST | Print a sample without selling anything |
| 72 | `pushWalletPassUpdate` | orders | POST | Push a change to every device holding it |
| 73 | `quoteUpgrade` | orders | POST | What an upgrade costs, pro-rata |
| 74 | `reissueEntitlement` | orders | POST | Zero-value reissue of an expired entitlement for a later date |
| 75 | `resendPaymentLink` | orders | POST |  |
| 76 | `respondToChargeback` | orders | POST | Submit evidence, or accept the loss |
| 77 | `setFraudRules` | orders | PUT |  |
| 78 | `setPaymentProvider` | orders | PUT | Configure a gateway and its routing |
| 79 | `shareEntitlement` | orders | POST | Let somebody else use this, without giving it away |
| 80 | `splitOrder` | orders | POST | Break one order into independent orders |
| 81 | `storePaymentToken` | orders | POST | Save a payment method for future use |
| 82 | `voidPayment` | orders | POST | Release an authorisation before it is captured |
| 83 | `cancelInvoice` | subscription | POST | Cancel or credit an invoice |
| 84 | `cancelSubscription` | subscription | POST | Terminate a tenant subscription |
| 85 | `createPartnerUser` | subscription | POST | Add a user to a partner branch |
| 86 | `disputeInvoice` | subscription | POST | Raise a dispute |
| 87 | `executeTenantMigration` | subscription | POST | Move the tenant |
| 88 | `exportPartnerInvoice` | subscription | POST | Partner invoice and settlement, in an ERP format |
| 89 | `launchCellCluster` | subscription | POST | Launch an identical cluster |
| 90 | `listCellClusters` | subscription | GET | Clusters in a region |
| 91 | `listPartnerUsers` | subscription | GET | Users beneath a partner, by branch |
| 92 | `listTenantMigrations` | subscription | GET | Tenant moves between cells |
| 93 | `listVenueTypeTemplates` | subscription | GET | Starting configurations by venue kind |
| 94 | `planTenantMigration` | subscription | POST | Plan moving a tenant to another cell |
| 95 | `recordInvoicePayment` | subscription | POST | Record payment against an invoice |
| 96 | `resolveInvoiceDispute` | subscription | POST | Resolve a dispute |
| 97 | `rollbackTenantMigration` | subscription | POST | Roll a cutover back |
| 98 | `settleAiUsage` | subscription | POST | Turn metered AI interactions into a billable usage record |
| 99 | `createBanner` | white-label | POST | Create a banner |
| 100 | `createContentBlock` | white-label | POST | Author a block of content |
| 101 | `createContentPage` | white-label | POST | Create a content page |
| 102 | `createPromoBlock` | white-label | POST | Create a promotional block |
| 103 | `deleteBanner` | white-label | DELETE | Delete a banner |
| 104 | `deleteContentPage` | white-label | DELETE | Delete a content page |
| 105 | `deletePromoBlock` | white-label | DELETE | Delete a promotional block |
| 106 | `getFeatureToggles` | white-label | GET | Read tenant feature toggles |
| 107 | `getModuleEnablement` | white-label | GET | Read module enablement |
| 108 | `getNavigation` | white-label | GET | Read navigation |
| 109 | `publishContentBlock` | white-label | POST | Publish now, or schedule it |
| 110 | `setFeatureToggles` | white-label | PUT | Set feature toggles |
| 111 | `setFooter` | white-label | PUT | Footer columns, legal links and social |
| 112 | `setHeader` | white-label | PUT | Configure the header |
| 113 | `setMaintenanceMode` | white-label | PUT | Enable or clear maintenance mode |
| 114 | `setModuleEnablement` | white-label | PUT | Enable or disable modules |
| 115 | `setNavigation` | white-label | PUT | Set main and overflow navigation |
| 116 | `updateBanner` | white-label | PATCH | Amend or activate a banner |
| 117 | `updateContentPage` | white-label | PUT | Amend a content page |
| 118 | `updatePromoBlock` | white-label | PATCH | Amend a promotional block |

---

### `P16` Venue Analytics — Cross-Domain Reporting — 102 gaps

venue-management-web · staff · web · operator: venue

10 screens · 20 operations · 8 contracts · 1 modules

#### Operations with no screen — 102

_in a contract this platform uses, callable by its audience, reaching no screen anywhere._

| # | Operation | Contract | Verb | Summary |
|--:|---|---|---|---|
| 1 | `createKnowledgeCollection` | ai | POST | Create a collection |
| 2 | `generateVenueLayout` | ai | POST | Draft a seat map from an uploaded plan |
| 3 | `ingestKnowledgeDocument` | ai | POST | Add a document |
| 4 | `listIndexSources` | ai | GET | What is indexed, and how current it is |
| 5 | `listKnowledgeCollections` | ai | GET | Collections available to this tenant |
| 6 | `proposeTranslations` | ai | POST |  |
| 7 | `proposeWalkways` | ai | POST | Find walkable space in a drawing that has no vectors |
| 8 | `reindexSource` | ai | POST | Rebuild a source |
| 9 | `removeIndexEntry` | ai | DELETE | Remove one record from the index |
| 10 | `setIndexSource` | ai | PUT | Declare a source indexed |
| 11 | `setSuggestionProvider` | ai | PUT |  |
| 12 | `assessProductChange` | catalogue | POST | What a change would touch, before making it |
| 13 | `bulkChangePrices` | catalogue | POST | Reprice a category or a whole catalogue |
| 14 | `cloneProduct` | catalogue | POST | Copy a product as a new draft |
| 15 | `commitCatalogueImport` | catalogue | POST | Apply a parsed catalogue import |
| 16 | `createDonationCampaign` | catalogue | POST | Create a campaign |
| 17 | `freezeEntitlement` | catalogue | POST | Pause a membership at the guest's request |
| 18 | `listDonationCampaigns` | catalogue | GET | Campaigns a guest can give to |
| 19 | `listProductVersions` | catalogue | GET | What this product used to be |
| 20 | `listWaitlistEntries` | catalogue | GET | Who is waiting for capacity |
| 21 | `offerWaitlistCapacity` | catalogue | POST | Tell a waiting guest that capacity appeared |
| 22 | `reinstateEntitlement` | catalogue | POST | Lift a suspension |
| 23 | `restoreProductVersion` | catalogue | POST | Put a previous version back |
| 24 | `suspendEntitlement` | catalogue | POST | Suspend or reinstate an entitlement |
| 25 | `updateDonationCampaign` | catalogue | PATCH | Amend or close a campaign |
| 26 | `createMfaChallenge` | identity | POST | Step-up authentication for a sensitive action |
| 27 | `exportSubjectData` | identity | POST | Everything the platform holds about one guest |
| 28 | `setPasswordPolicy` | identity | PUT | Length, breach check, lockout and step-up |
| 29 | `setSegregationRules` | identity | PUT | Which permissions may not be held together |
| 30 | `submitCountLines` | inventory | POST | Submit counted quantities |
| 31 | `activateJourney` | marketing-crm | POST | Start it, or stop it |
| 32 | `addGuestNote` | marketing-crm | POST | What the floor needs to know about this table |
| 33 | `addSuppression` | marketing-crm | POST | Suppress an address |
| 34 | `createChallenge` | marketing-crm | POST | Define a challenge, mission or streak |
| 35 | `createForm` | marketing-crm | POST | Define a waiver, survey or capture form |
| 36 | `createInvitationCampaign` | marketing-crm | POST | A quota-bounded, addressed invitation |
| 37 | `createLoyaltyProgramme` | marketing-crm | POST | Create a loyalty programme |
| 38 | `createReferral` | marketing-crm | POST | Issue a referral code |
| 39 | `createUrlRedirect` | marketing-crm | POST | 301, 302 and custom redirects |
| 40 | `getJourneyPerformance` | marketing-crm | GET | Entrants, completions, goals reached |
| 41 | `getLostItemMatches` | marketing-crm | GET | Candidate matches, scored |
| 42 | `getMyChallenges` | marketing-crm | GET | Active challenges and how far along I am |
| 43 | `getSuppressionList` | marketing-crm | GET | Addresses suppressed from all sending |
| 44 | `getWaiverStatus` | marketing-crm | GET | Whether this guest may be issued a ticket that requires a waiver |
| 45 | `listMessageTriggers` | marketing-crm | GET | What fires a message, and when |
| 46 | `listReviews` | marketing-crm | GET | List guest reviews and ratings |
| 47 | `listSegmentMembers` | marketing-crm | GET | List guests currently matching a segment |
| 48 | `matchGuest` | marketing-crm | POST | Is this the same person we already have? |
| 49 | `mergeGuests` | marketing-crm | POST | Two records, one person |
| 50 | `recordLostItem` | marketing-crm | POST | Report something lost, or hand something in |
| 51 | `recordPrivacyIncident` | marketing-crm | POST | Log a personal-data breach and start the clock |
| 52 | `respondToReview` | marketing-crm | POST | Respond to a review |
| 53 | `retryMessageDispatch` | marketing-crm | POST | Send it again, or by another channel |
| 54 | `setCallDisposition` | marketing-crm | POST | Why the conversation ended, and any callback |
| 55 | `setConsentPurposes` | marketing-crm | PUT | Configure consent purposes |
| 56 | `setMessageTrigger` | marketing-crm | POST | Fire a message from a platform event |
| 57 | `setSeoMetadata` | marketing-crm | PUT | Titles, descriptions, canonicals and hreflang |
| 58 | `startKioskAssist` | marketing-crm | POST | A staff member helps a guest at a kiosk, remotely |
| 59 | `submitForm` | marketing-crm | POST | Sign a waiver, answer a survey, capture details |
| 60 | `updateGuestPreferences` | marketing-crm | PUT | The things a regular should not have to say twice |
| 61 | `uploadGuestDocument` | marketing-crm | POST | Store a guest photo, ID or signed document |
| 62 | `captureStoredValue` | orders | POST | Take some or all of a held balance |
| 63 | `convertReservation` | orders | POST | Convert a reservation into an order |
| 64 | `convertToTermProduct` | orders | POST | Turn a visit into a membership or season pass |
| 65 | `createPaymentLink` | orders | POST | Send a guest a link to pay later |
| 66 | `createResaleListing` | orders | POST | List an entitlement for resale |
| 67 | `createReservation` | orders | POST | Hold without payment |
| 68 | `extendReservation` | orders | POST | Extend a reservation |
| 69 | `getGroupBooking` | orders | GET |  |
| 70 | `issueInvitation` | orders | POST | Issue a complimentary entitlement, with no payment expected |
| 71 | `listAbandonedCarts` | orders | GET | Carts that lapsed without checking out |
| 72 | `listChargebacks` | orders | GET | Open disputes, by deadline |
| 73 | `listFraudRules` | orders | GET |  |
| 74 | `listInvitationAllowances` | orders | GET | Who may issue comps, and how many are left |
| 75 | `listPaymentProviders` | orders | GET | Gateways configured for this scope |
| 76 | `listPaymentTokens` | orders | GET | A guest's saved payment methods |
| 77 | `openGuestCreditAccount` | orders | POST | A credit limit for an individual booking ahead |
| 78 | `printTicketProof` | orders | POST | Print a sample without selling anything |
| 79 | `pushWalletPassUpdate` | orders | POST | Push a change to every device holding it |
| 80 | `quoteUpgrade` | orders | POST | What an upgrade costs, pro-rata |
| 81 | `reissueEntitlement` | orders | POST | Zero-value reissue of an expired entitlement for a later date |
| 82 | `resendPaymentLink` | orders | POST |  |
| 83 | `respondToChargeback` | orders | POST | Submit evidence, or accept the loss |
| 84 | `setFraudRules` | orders | PUT |  |
| 85 | `setPaymentProvider` | orders | PUT | Configure a gateway and its routing |
| 86 | `shareEntitlement` | orders | POST | Let somebody else use this, without giving it away |
| 87 | `splitOrder` | orders | POST | Break one order into independent orders |
| 88 | `storePaymentToken` | orders | POST | Save a payment method for future use |
| 89 | `voidPayment` | orders | POST | Release an authorisation before it is captured |
| 90 | `cancelReportExecution` | reporting | DELETE | Cancel a running execution |
| 91 | `deleteReportSchedule` | reporting | DELETE | Delete a schedule |
| 92 | `exportReportResult` | reporting | POST | Export a completed result |
| 93 | `getReportExecution` | reporting | GET | Execution status and result |
| 94 | `getReportExport` | reporting | GET | Export status and download link |
| 95 | `getReportResult` | reporting | GET | Paged result rows |
| 96 | `listAlertRules` | reporting | GET | What raises an alert, and when |
| 97 | `listReportFields` | reporting | GET | Fields available for a data source |
| 98 | `listReportSchedules` | reporting | GET | List scheduled reports |
| 99 | `listSeededReports` | reporting | GET |  |
| 100 | `updateReportSchedule` | reporting | PATCH | Amend, pause or resume a schedule |
| 101 | `getRegionSettings` | tenancy | GET | Read region settings |
| 102 | `updateRegionSettings` | tenancy | PUT | Update region settings |

---

### `P09` TICVAI Web — Platform Console — 71 gaps

ticvai-web · platformAdmin · web · operator: ticvai

37 screens · 110 operations · 9 contracts · 2 modules

#### Operations with no screen — 70

_in a contract this platform uses, callable by its audience, reaching no screen anywhere._

| # | Operation | Contract | Verb | Summary |
|--:|---|---|---|---|
| 1 | `createKnowledgeCollection` | ai | POST | Create a collection |
| 2 | `generateVenueLayout` | ai | POST | Draft a seat map from an uploaded plan |
| 3 | `ingestKnowledgeDocument` | ai | POST | Add a document |
| 4 | `listIndexSources` | ai | GET | What is indexed, and how current it is |
| 5 | `listKnowledgeCollections` | ai | GET | Collections available to this tenant |
| 6 | `proposeTranslations` | ai | POST |  |
| 7 | `proposeWalkways` | ai | POST | Find walkable space in a drawing that has no vectors |
| 8 | `reindexSource` | ai | POST | Rebuild a source |
| 9 | `removeIndexEntry` | ai | DELETE | Remove one record from the index |
| 10 | `setIndexSource` | ai | PUT | Declare a source indexed |
| 11 | `setSuggestionProvider` | ai | PUT |  |
| 12 | `authoriseWalletSpend` | cross-cell | POST | Hold funds against the guest's home-cell balance |
| 13 | `captureWalletAuthorisation` | cross-cell | POST | Capture a held amount |
| 14 | `getWalletAllocation` | cross-cell | GET | The consuming cell's bounded offline allocation |
| 15 | `releaseWalletAuthorisation` | cross-cell | POST | Release a hold without capturing |
| 16 | `setWalletAllocationPolicy` | cross-cell | PUT | Set the allocation cap policy |
| 17 | `createMfaChallenge` | identity | POST | Step-up authentication for a sensitive action |
| 18 | `exportSubjectData` | identity | POST | Everything the platform holds about one guest |
| 19 | `setPasswordPolicy` | identity | PUT | Length, breach check, lockout and step-up |
| 20 | `setSegregationRules` | identity | PUT | Which permissions may not be held together |
| 21 | `skipRolloutCell` | platform-ops | POST | Exclude a cell from this wave |
| 22 | `cancelReportExecution` | reporting | DELETE | Cancel a running execution |
| 23 | `deleteReportSchedule` | reporting | DELETE | Delete a schedule |
| 24 | `exportReportResult` | reporting | POST | Export a completed result |
| 25 | `getReportExecution` | reporting | GET | Execution status and result |
| 26 | `getReportExport` | reporting | GET | Export status and download link |
| 27 | `getReportResult` | reporting | GET | Paged result rows |
| 28 | `listAlertRules` | reporting | GET | What raises an alert, and when |
| 29 | `listReportFields` | reporting | GET | Fields available for a data source |
| 30 | `listReportSchedules` | reporting | GET | List scheduled reports |
| 31 | `listSeededReports` | reporting | GET |  |
| 32 | `updateReportSchedule` | reporting | PATCH | Amend, pause or resume a schedule |
| 33 | `cancelInvoice` | subscription | POST | Cancel or credit an invoice |
| 34 | `cancelSubscription` | subscription | POST | Terminate a tenant subscription |
| 35 | `createPartnerUser` | subscription | POST | Add a user to a partner branch |
| 36 | `disputeInvoice` | subscription | POST | Raise a dispute |
| 37 | `executeTenantMigration` | subscription | POST | Move the tenant |
| 38 | `exportPartnerInvoice` | subscription | POST | Partner invoice and settlement, in an ERP format |
| 39 | `launchCellCluster` | subscription | POST | Launch an identical cluster |
| 40 | `listCellClusters` | subscription | GET | Clusters in a region |
| 41 | `listPartnerUsers` | subscription | GET | Users beneath a partner, by branch |
| 42 | `listTenantMigrations` | subscription | GET | Tenant moves between cells |
| 43 | `listVenueTypeTemplates` | subscription | GET | Starting configurations by venue kind |
| 44 | `planTenantMigration` | subscription | POST | Plan moving a tenant to another cell |
| 45 | `recordInvoicePayment` | subscription | POST | Record payment against an invoice |
| 46 | `resolveInvoiceDispute` | subscription | POST | Resolve a dispute |
| 47 | `rollbackTenantMigration` | subscription | POST | Roll a cutover back |
| 48 | `settleAiUsage` | subscription | POST | Turn metered AI interactions into a billable usage record |
| 49 | `getRegionSettings` | tenancy | GET | Read region settings |
| 50 | `updateRegionSettings` | tenancy | PUT | Update region settings |
| 51 | `createBanner` | white-label | POST | Create a banner |
| 52 | `createContentBlock` | white-label | POST | Author a block of content |
| 53 | `createContentPage` | white-label | POST | Create a content page |
| 54 | `createPromoBlock` | white-label | POST | Create a promotional block |
| 55 | `deleteBanner` | white-label | DELETE | Delete a banner |
| 56 | `deleteContentPage` | white-label | DELETE | Delete a content page |
| 57 | `deletePromoBlock` | white-label | DELETE | Delete a promotional block |
| 58 | `getFeatureToggles` | white-label | GET | Read tenant feature toggles |
| 59 | `getModuleEnablement` | white-label | GET | Read module enablement |
| 60 | `getNavigation` | white-label | GET | Read navigation |
| 61 | `publishContentBlock` | white-label | POST | Publish now, or schedule it |
| 62 | `setFeatureToggles` | white-label | PUT | Set feature toggles |
| 63 | `setFooter` | white-label | PUT | Footer columns, legal links and social |
| 64 | `setHeader` | white-label | PUT | Configure the header |
| 65 | `setMaintenanceMode` | white-label | PUT | Enable or clear maintenance mode |
| 66 | `setModuleEnablement` | white-label | PUT | Enable or disable modules |
| 67 | `setNavigation` | white-label | PUT | Set main and overflow navigation |
| 68 | `updateBanner` | white-label | PATCH | Amend or activate a banner |
| 69 | `updateContentPage` | white-label | PUT | Amend a content page |
| 70 | `updatePromoBlock` | white-label | PATCH | Amend a promotional block |

#### Modules split across waves — 1

_sells in one wave, cannot finish the job until a later one._

| # | Module | Waves |
|--:|---|---|
| 1 | TODO | 1, 2, 3 |

---

### `P12` Venue Support — Agent Console — 60 gaps

venue-support-web · staff · web · operator: venue

8 screens · 33 operations · 4 contracts · 1 modules

#### Operations with no screen — 59

_in a contract this platform uses, callable by its audience, reaching no screen anywhere._

| # | Operation | Contract | Verb | Summary |
|--:|---|---|---|---|
| 1 | `calculateTax` | finance | POST | Compute tax for a set of lines |
| 2 | `disputeObligation` | finance | POST | One entity disagrees with the amount |
| 3 | `getForeignTenderReport` | finance | GET | What was taken in which currency |
| 4 | `getUnifiedReconciliation` | finance | GET | Every money source against the ledger, in one view |
| 5 | `ingestFxRates` | finance | POST | Pull rates from the configured provider |
| 6 | `listInterEntityObligations` | finance | GET | What one entity owes another |
| 7 | `recordDeposit` | finance | POST | Money taken before the sale is complete |
| 8 | `recordSettlement` | finance | POST | One entity paid another |
| 9 | `recordWriteOff` | finance | POST | Write off an uncollectable balance |
| 10 | `resolveObligationDispute` | finance | POST | Agree what is actually owed |
| 11 | `runFxRevaluation` | finance | POST | Revalue monetary balances at close |
| 12 | `setFxProvider` | finance | PUT | Which provider serves which purpose |
| 13 | `validateRecognitionSchedules` | finance | POST | Find product kinds claimed by more than one schedule |
| 14 | `createMfaChallenge` | identity | POST | Step-up authentication for a sensitive action |
| 15 | `exportSubjectData` | identity | POST | Everything the platform holds about one guest |
| 16 | `setPasswordPolicy` | identity | PUT | Length, breach check, lockout and step-up |
| 17 | `setSegregationRules` | identity | PUT | Which permissions may not be held together |
| 18 | `activateJourney` | marketing-crm | POST | Start it, or stop it |
| 19 | `addGuestNote` | marketing-crm | POST | What the floor needs to know about this table |
| 20 | `addSuppression` | marketing-crm | POST | Suppress an address |
| 21 | `createChallenge` | marketing-crm | POST | Define a challenge, mission or streak |
| 22 | `createForm` | marketing-crm | POST | Define a waiver, survey or capture form |
| 23 | `createInvitationCampaign` | marketing-crm | POST | A quota-bounded, addressed invitation |
| 24 | `createLoyaltyProgramme` | marketing-crm | POST | Create a loyalty programme |
| 25 | `createReferral` | marketing-crm | POST | Issue a referral code |
| 26 | `createUrlRedirect` | marketing-crm | POST | 301, 302 and custom redirects |
| 27 | `getJourneyPerformance` | marketing-crm | GET | Entrants, completions, goals reached |
| 28 | `getLostItemMatches` | marketing-crm | GET | Candidate matches, scored |
| 29 | `getMyChallenges` | marketing-crm | GET | Active challenges and how far along I am |
| 30 | `getSuppressionList` | marketing-crm | GET | Addresses suppressed from all sending |
| 31 | `getWaiverStatus` | marketing-crm | GET | Whether this guest may be issued a ticket that requires a waiver |
| 32 | `listMessageTriggers` | marketing-crm | GET | What fires a message, and when |
| 33 | `listReviews` | marketing-crm | GET | List guest reviews and ratings |
| 34 | `listSegmentMembers` | marketing-crm | GET | List guests currently matching a segment |
| 35 | `matchGuest` | marketing-crm | POST | Is this the same person we already have? |
| 36 | `mergeGuests` | marketing-crm | POST | Two records, one person |
| 37 | `recordLostItem` | marketing-crm | POST | Report something lost, or hand something in |
| 38 | `recordPrivacyIncident` | marketing-crm | POST | Log a personal-data breach and start the clock |
| 39 | `respondToReview` | marketing-crm | POST | Respond to a review |
| 40 | `retryMessageDispatch` | marketing-crm | POST | Send it again, or by another channel |
| 41 | `setCallDisposition` | marketing-crm | POST | Why the conversation ended, and any callback |
| 42 | `setConsentPurposes` | marketing-crm | PUT | Configure consent purposes |
| 43 | `setMessageTrigger` | marketing-crm | POST | Fire a message from a platform event |
| 44 | `setSeoMetadata` | marketing-crm | PUT | Titles, descriptions, canonicals and hreflang |
| 45 | `startKioskAssist` | marketing-crm | POST | A staff member helps a guest at a kiosk, remotely |
| 46 | `submitForm` | marketing-crm | POST | Sign a waiver, answer a survey, capture details |
| 47 | `updateGuestPreferences` | marketing-crm | PUT | The things a regular should not have to say twice |
| 48 | `uploadGuestDocument` | marketing-crm | POST | Store a guest photo, ID or signed document |
| 49 | `cancelReportExecution` | reporting | DELETE | Cancel a running execution |
| 50 | `deleteReportSchedule` | reporting | DELETE | Delete a schedule |
| 51 | `exportReportResult` | reporting | POST | Export a completed result |
| 52 | `getReportExecution` | reporting | GET | Execution status and result |
| 53 | `getReportExport` | reporting | GET | Export status and download link |
| 54 | `getReportResult` | reporting | GET | Paged result rows |
| 55 | `listAlertRules` | reporting | GET | What raises an alert, and when |
| 56 | `listReportFields` | reporting | GET | Fields available for a data source |
| 57 | `listReportSchedules` | reporting | GET | List scheduled reports |
| 58 | `listSeededReports` | reporting | GET |  |
| 59 | `updateReportSchedule` | reporting | PATCH | Amend, pause or resume a schedule |

#### Modules split across waves — 1

_sells in one wave, cannot finish the job until a later one._

| # | Module | Waves |
|--:|---|---|
| 1 | TODO | 2, 3 |

---

### `P07` Venue Scanner — Access Control — 40 gaps

venue-scanner · staff · handheld · operator: venue · offline capable

11 screens · 23 operations · 5 contracts · 1 modules

#### Operations with no screen — 40

_in a contract this platform uses, callable by its audience, reaching no screen anywhere._

| # | Operation | Contract | Verb | Summary |
|--:|---|---|---|---|
| 1 | `enrolFacePass` | access | POST | Register a facial profile against an entitlement |
| 2 | `getFacePassEnrolment` | access | GET | Whether a pass has a face registered, and when |
| 3 | `revokeFacePass` | access | DELETE | Remove a facial profile |
| 4 | `authoriseWalletSpend` | cross-cell | POST | Hold funds against the guest's home-cell balance |
| 5 | `captureWalletAuthorisation` | cross-cell | POST | Capture a held amount |
| 6 | `getWalletAllocation` | cross-cell | GET | The consuming cell's bounded offline allocation |
| 7 | `releaseWalletAuthorisation` | cross-cell | POST | Release a hold without capturing |
| 8 | `setWalletAllocationPolicy` | cross-cell | PUT | Set the allocation cap policy |
| 9 | `createMfaChallenge` | identity | POST | Step-up authentication for a sensitive action |
| 10 | `exportSubjectData` | identity | POST | Everything the platform holds about one guest |
| 11 | `setPasswordPolicy` | identity | PUT | Length, breach check, lockout and step-up |
| 12 | `setSegregationRules` | identity | PUT | Which permissions may not be held together |
| 13 | `captureStoredValue` | orders | POST | Take some or all of a held balance |
| 14 | `convertReservation` | orders | POST | Convert a reservation into an order |
| 15 | `convertToTermProduct` | orders | POST | Turn a visit into a membership or season pass |
| 16 | `createPaymentLink` | orders | POST | Send a guest a link to pay later |
| 17 | `createResaleListing` | orders | POST | List an entitlement for resale |
| 18 | `createReservation` | orders | POST | Hold without payment |
| 19 | `extendReservation` | orders | POST | Extend a reservation |
| 20 | `getGroupBooking` | orders | GET |  |
| 21 | `issueInvitation` | orders | POST | Issue a complimentary entitlement, with no payment expected |
| 22 | `listAbandonedCarts` | orders | GET | Carts that lapsed without checking out |
| 23 | `listChargebacks` | orders | GET | Open disputes, by deadline |
| 24 | `listFraudRules` | orders | GET |  |
| 25 | `listInvitationAllowances` | orders | GET | Who may issue comps, and how many are left |
| 26 | `listPaymentProviders` | orders | GET | Gateways configured for this scope |
| 27 | `listPaymentTokens` | orders | GET | A guest's saved payment methods |
| 28 | `openGuestCreditAccount` | orders | POST | A credit limit for an individual booking ahead |
| 29 | `printTicketProof` | orders | POST | Print a sample without selling anything |
| 30 | `pushWalletPassUpdate` | orders | POST | Push a change to every device holding it |
| 31 | `quoteUpgrade` | orders | POST | What an upgrade costs, pro-rata |
| 32 | `reissueEntitlement` | orders | POST | Zero-value reissue of an expired entitlement for a later date |
| 33 | `resendPaymentLink` | orders | POST |  |
| 34 | `respondToChargeback` | orders | POST | Submit evidence, or accept the loss |
| 35 | `setFraudRules` | orders | PUT |  |
| 36 | `setPaymentProvider` | orders | PUT | Configure a gateway and its routing |
| 37 | `shareEntitlement` | orders | POST | Let somebody else use this, without giving it away |
| 38 | `splitOrder` | orders | POST | Break one order into independent orders |
| 39 | `storePaymentToken` | orders | POST | Save a payment method for future use |
| 40 | `voidPayment` | orders | POST | Release an authorisation before it is captured |

---

### `P01` Guest Web — Storefront — 33 gaps

guest-web · guest · web · operator: guest

46 screens · 113 operations · 14 contracts · 13 modules

#### Operations with no screen — 28

_in a contract this platform uses, callable by its audience, reaching no screen anywhere._

| # | Operation | Contract | Verb | Summary |
|--:|---|---|---|---|
| 1 | `enrolFacePass` | access | POST | Register a facial profile against an entitlement |
| 2 | `getFacePassEnrolment` | access | GET | Whether a pass has a face registered, and when |
| 3 | `revokeFacePass` | access | DELETE | Remove a facial profile |
| 4 | `freezeEntitlement` | catalogue | POST | Pause a membership at the guest's request |
| 5 | `joinWaitlist` | catalogue | POST | Ask to be told if capacity frees up |
| 6 | `leaveWaitlist` | catalogue | DELETE | Stop waiting |
| 7 | `updateTableReservation` | fnb | PATCH | Change or cancel a booking |
| 8 | `createMfaChallenge` | identity | POST | Step-up authentication for a sensitive action |
| 9 | `deleteGuestAccount` | identity | DELETE | Self-service account deletion |
| 10 | `exportSubjectData` | identity | POST | Everything the platform holds about one guest |
| 11 | `createReferral` | marketing-crm | POST | Issue a referral code |
| 12 | `getMyChallenges` | marketing-crm | GET | Active challenges and how far along I am |
| 13 | `getWaiverStatus` | marketing-crm | GET | Whether this guest may be issued a ticket that requires a waiver |
| 14 | `recordLostItem` | marketing-crm | POST | Report something lost, or hand something in |
| 15 | `respondToInvitation` | marketing-crm | POST | Accept or decline |
| 16 | `submitForm` | marketing-crm | POST | Sign a waiver, answer a survey, capture details |
| 17 | `updateGuestPreferences` | marketing-crm | PUT | The things a regular should not have to say twice |
| 18 | `uploadGuestDocument` | marketing-crm | POST | Store a guest photo, ID or signed document |
| 19 | `convertToTermProduct` | orders | POST | Turn a visit into a membership or season pass |
| 20 | `createCart` | orders | POST | Start a cart |
| 21 | `createResaleListing` | orders | POST | List an entitlement for resale |
| 22 | `getGroupBooking` | orders | GET |  |
| 23 | `listPaymentTokens` | orders | GET | A guest's saved payment methods |
| 24 | `quoteUpgrade` | orders | POST | What an upgrade costs, pro-rata |
| 25 | `shareEntitlement` | orders | POST | Let somebody else use this, without giving it away |
| 26 | `storePaymentToken` | orders | POST | Save a payment method for future use |
| 27 | `transferWalletBalance` | retail | POST | Send balance to another guest |
| 28 | `assignSeats` | seating | POST | Pick and hold the best available seats |

#### Modules split across waves — 5

_sells in one wave, cannot finish the job until a later one._

| # | Module | Waves |
|--:|---|---|
| 1 | Booking & Selection | 1, 2, 3 |
| 2 | Engagement & Support | 1, 2, 3 |
| 3 | Membership, Loyalty & Value | 2, 3 |
| 4 | Support | 2, 3 |
| 5 | Ticketing | 1, 2 |

---

### `P15` Kitchen Display — Pass and Stations — 31 gaps

kitchen-display · staff · kiosk · operator: venue · offline capable

10 screens · 24 operations · 3 contracts · 1 modules

#### Operations with no screen — 31

_in a contract this platform uses, callable by its audience, reaching no screen anywhere._

| # | Operation | Contract | Verb | Summary |
|--:|---|---|---|---|
| 1 | `attachModifierGroup` | fnb | PUT | Give an item its choices |
| 2 | `clearTable` | fnb | POST | Mark a table cleared and free |
| 3 | `closeCorrectiveAction` | fnb | POST | Close a signed finding |
| 4 | `createCombo` | fnb | POST | A meal deal, priced as one thing |
| 5 | `createModifierGroup` | fnb | POST | Create a modifier group |
| 6 | `createTable` | fnb | POST | A table as a thing, not an inference |
| 7 | `escalateCorrectiveAction` | fnb | POST | Escalate a finding |
| 8 | `getTableVisit` | fnb | GET | Read a visit with all its orders |
| 9 | `rebalanceStationLoad` | fnb | POST | Move work between stations mid-service |
| 10 | `recordCorrectiveAction` | fnb | POST | Record what was done about a finding |
| 11 | `requestBill` | fnb | POST | The party asked to pay |
| 12 | `resolveBookingConflict` | fnb | GET | Two bookings, one table — and what to do about it |
| 13 | `sendBookingConfirmation` | fnb | POST | Confirm a booking, and ask them to confirm back |
| 14 | `sendOrderNotification` | fnb | POST | Tell the guest where their order is |
| 15 | `setComboSlots` | fnb | PUT | What the guest chooses, and what it costs extra |
| 16 | `setKitchenSla` | fnb | PUT | How long a ticket may sit before it is late |
| 17 | `setSectionLayout` | fnb | PUT | Divide the floor into sections and give each a server |
| 18 | `updateTable` | fnb | PUT | Change what a table is |
| 19 | `cancelReportExecution` | reporting | DELETE | Cancel a running execution |
| 20 | `deleteReportSchedule` | reporting | DELETE | Delete a schedule |
| 21 | `exportReportResult` | reporting | POST | Export a completed result |
| 22 | `getReportExecution` | reporting | GET | Execution status and result |
| 23 | `getReportExport` | reporting | GET | Export status and download link |
| 24 | `getReportResult` | reporting | GET | Paged result rows |
| 25 | `listAlertRules` | reporting | GET | What raises an alert, and when |
| 26 | `listReportFields` | reporting | GET | Fields available for a data source |
| 27 | `listReportSchedules` | reporting | GET | List scheduled reports |
| 28 | `listSeededReports` | reporting | GET |  |
| 29 | `updateReportSchedule` | reporting | PATCH | Amend, pause or resume a schedule |
| 30 | `getRegionSettings` | tenancy | GET | Read region settings |
| 31 | `updateRegionSettings` | tenancy | PUT | Update region settings |

---

### `P02` Guest App — Mobile — 30 gaps

guest-app · guest · mobileApp · operator: guest · offline capable

63 screens · 101 operations · 15 contracts · 4 modules

#### Operations with no screen — 28

_in a contract this platform uses, callable by its audience, reaching no screen anywhere._

| # | Operation | Contract | Verb | Summary |
|--:|---|---|---|---|
| 1 | `enrolFacePass` | access | POST | Register a facial profile against an entitlement |
| 2 | `getFacePassEnrolment` | access | GET | Whether a pass has a face registered, and when |
| 3 | `revokeFacePass` | access | DELETE | Remove a facial profile |
| 4 | `freezeEntitlement` | catalogue | POST | Pause a membership at the guest's request |
| 5 | `joinWaitlist` | catalogue | POST | Ask to be told if capacity frees up |
| 6 | `leaveWaitlist` | catalogue | DELETE | Stop waiting |
| 7 | `updateTableReservation` | fnb | PATCH | Change or cancel a booking |
| 8 | `createMfaChallenge` | identity | POST | Step-up authentication for a sensitive action |
| 9 | `deleteGuestAccount` | identity | DELETE | Self-service account deletion |
| 10 | `exportSubjectData` | identity | POST | Everything the platform holds about one guest |
| 11 | `createReferral` | marketing-crm | POST | Issue a referral code |
| 12 | `getMyChallenges` | marketing-crm | GET | Active challenges and how far along I am |
| 13 | `getWaiverStatus` | marketing-crm | GET | Whether this guest may be issued a ticket that requires a waiver |
| 14 | `recordLostItem` | marketing-crm | POST | Report something lost, or hand something in |
| 15 | `respondToInvitation` | marketing-crm | POST | Accept or decline |
| 16 | `submitForm` | marketing-crm | POST | Sign a waiver, answer a survey, capture details |
| 17 | `updateGuestPreferences` | marketing-crm | PUT | The things a regular should not have to say twice |
| 18 | `uploadGuestDocument` | marketing-crm | POST | Store a guest photo, ID or signed document |
| 19 | `convertToTermProduct` | orders | POST | Turn a visit into a membership or season pass |
| 20 | `createCart` | orders | POST | Start a cart |
| 21 | `createResaleListing` | orders | POST | List an entitlement for resale |
| 22 | `getGroupBooking` | orders | GET |  |
| 23 | `listPaymentTokens` | orders | GET | A guest's saved payment methods |
| 24 | `quoteUpgrade` | orders | POST | What an upgrade costs, pro-rata |
| 25 | `shareEntitlement` | orders | POST | Let somebody else use this, without giving it away |
| 26 | `storePaymentToken` | orders | POST | Save a payment method for future use |
| 27 | `transferWalletBalance` | retail | POST | Send balance to another guest |
| 28 | `assignSeats` | seating | POST | Pick and hold the best available seats |

#### Modules split across waves — 2

_sells in one wave, cannot finish the job until a later one._

| # | Module | Waves |
|--:|---|---|
| 1 | In-Venue Experience | 2, 3 |
| 2 | TODO | 1, 2, 3 |

---

### `P05` Guest Kiosk — Self-Service — 21 gaps

guest-app · guest · kiosk · operator: guest

17 screens · 23 operations · 8 contracts · 2 modules

#### Operations with no screen — 21

_in a contract this platform uses, callable by its audience, reaching no screen anywhere._

| # | Operation | Contract | Verb | Summary |
|--:|---|---|---|---|
| 1 | `freezeEntitlement` | catalogue | POST | Pause a membership at the guest's request |
| 2 | `joinWaitlist` | catalogue | POST | Ask to be told if capacity frees up |
| 3 | `leaveWaitlist` | catalogue | DELETE | Stop waiting |
| 4 | `updateTableReservation` | fnb | PATCH | Change or cancel a booking |
| 5 | `createReferral` | marketing-crm | POST | Issue a referral code |
| 6 | `getMyChallenges` | marketing-crm | GET | Active challenges and how far along I am |
| 7 | `getWaiverStatus` | marketing-crm | GET | Whether this guest may be issued a ticket that requires a waiver |
| 8 | `recordLostItem` | marketing-crm | POST | Report something lost, or hand something in |
| 9 | `respondToInvitation` | marketing-crm | POST | Accept or decline |
| 10 | `submitForm` | marketing-crm | POST | Sign a waiver, answer a survey, capture details |
| 11 | `updateGuestPreferences` | marketing-crm | PUT | The things a regular should not have to say twice |
| 12 | `uploadGuestDocument` | marketing-crm | POST | Store a guest photo, ID or signed document |
| 13 | `convertToTermProduct` | orders | POST | Turn a visit into a membership or season pass |
| 14 | `createCart` | orders | POST | Start a cart |
| 15 | `createResaleListing` | orders | POST | List an entitlement for resale |
| 16 | `getGroupBooking` | orders | GET |  |
| 17 | `listPaymentTokens` | orders | GET | A guest's saved payment methods |
| 18 | `quoteUpgrade` | orders | POST | What an upgrade costs, pro-rata |
| 19 | `shareEntitlement` | orders | POST | Let somebody else use this, without giving it away |
| 20 | `storePaymentToken` | orders | POST | Save a payment method for future use |
| 21 | `transferWalletBalance` | retail | POST | Send balance to another guest |

---

### `P10` Partner Web — Reseller Portal — 4 gaps

partner-web · partner · web · operator: partner

21 screens · 105 operations · 9 contracts · 1 modules

#### Operations with no screen — 3

_in a contract this platform uses, callable by its audience, reaching no screen anywhere._

| # | Operation | Contract | Verb | Summary |
|--:|---|---|---|---|
| 1 | `createMfaChallenge` | identity | POST | Step-up authentication for a sensitive action |
| 2 | `createPartnerUser` | subscription | POST | Add a user to a partner branch |
| 3 | `listPartnerUsers` | subscription | GET | Users beneath a partner, by branch |

#### Modules split across waves — 1

_sells in one wave, cannot finish the job until a later one._

| # | Module | Waves |
|--:|---|---|
| 1 | TODO | 2, 3 |

---

### `P14` Developer Portal — 2 gaps

developer-portal-web · partner · web · operator: partner

8 screens · 21 operations · 1 contracts · 1 modules

#### Operations with no screen — 1

_in a contract this platform uses, callable by its audience, reaching no screen anywhere._

| # | Operation | Contract | Verb | Summary |
|--:|---|---|---|---|
| 1 | `issueApiToken` | public-api | POST | Exchange a credential for an access token |

#### Modules split across waves — 1

_sells in one wave, cannot finish the job until a later one._

| # | Module | Waves |
|--:|---|---|
| 1 | Developer & API | 2, 3 |

---

### `P11` Accreditation Web — Applications — 0 gaps

accreditation-web · public · web · operator: public

8 screens · 3 operations · 2 contracts · 2 modules

No gaps. Every operation this audience can call reaches a screen, no module straddles
a wave, every screen is drawn, and no flow names a screen that does not exist.

---

## Part 2 — the unclaimed frames

**811 frames no screen claims, across 74 boards.**

100 boards on disk · 1362 frames after de-duplication · 551 claimed by a screen
· 615 that something can name · 55 boards nothing points at
· 133 screens drawn by hand · 359 drawn by the generator.

A frame is in one of three states, and they are three different jobs:

- **ok** — a screen claims it and something can name it. Finished.
- **named** — something can name it, no screen claims it. The mapping job.
- **bare** — nobody names it and nobody claims it. The mapping job, blind.

Of the 811 unclaimed: **64 named**, **747 bare**.

### The full board list — all 100 boards

This is the list the 811 is counted over. `raw id=` is every `id="..."` match in the
file before folding case and de-duplicating; `frames` is what remains. The two differ
because most boards carry each anchor twice (see Part 3).

| # | Board | Folder | Kind | In git | Platforms | raw id= | frames | claimed | unclaimed | wired | bytes | modified |
|--:|---|---|---|---|---|--:|--:|--:|--:|---|--:|---|
| 1 | P08 Staff Web Back Office | wireframes | generated | yes | — | 73 | 73 | 0 | **73** | no | 733456 | 2026-08-25 |
| 2 | P06 Staff App | wireframes | generated | yes | — | 50 | 50 | 0 | **50** | no | 285850 | 2026-08-25 |
| 3 | P08 Venue Management | wireframes | generated | yes | P08 | 143 | 143 | 100 | **43** | yes | 415704 | 2026-08-31 |
| 4 | P09 Admin Web | wireframes | generated | yes | — | 36 | 36 | 0 | **36** | no | 338829 | 2026-08-25 |
| 5 | P13 White-Label CMS | wireframes | generated | yes | — | 20 | 20 | 0 | **20** | no | 171979 | 2026-08-25 |
| 6 | P07 Staff Scanner | wireframes | generated | yes | — | 16 | 16 | 0 | **16** | no | 93080 | 2026-08-25 |
| 7 | FnB Board 2 | wireframes | pack | yes | P08 | 26 | 18 | 5 | **13** | yes | 279332 | 2026-08-31 |
| 8 | P04 Venue POS | wireframes | generated | yes | P04 | 24 | 24 | 12 | **12** | yes | 76833 | 2026-08-31 |
| 9 | Retail Board 2 | wireframes | pack | yes | P08 | 22 | 18 | 7 | **11** | yes | 239537 | 2026-08-31 |
| 10 | Retail Board 6 | wireframes | pack | yes | P08 P16 | 22 | 14 | 3 | **11** | yes | 203088 | 2026-08-31 |
| 11 | Retail Board 4 | wireframes | pack | yes | P06 P08 | 20 | 19 | 9 | **10** | yes | 197744 | 2026-08-31 |
| 12 | FnB Board 4 | wireframes | pack | yes | P06 | 20 | 18 | 8 | **10** | yes | 213738 | 2026-08-31 |
| 13 | FnB Board 3 | wireframes | pack | yes | P15 | 20 | 17 | 7 | **10** | yes | 208094 | 2026-08-31 |
| 14 | Retail Board 3 | wireframes | pack | yes | P04 P08 | 20 | 15 | 5 | **10** | yes | 192232 | 2026-08-31 |
| 15 | Retail Board 5 | wireframes | pack | yes | P08 | 20 | 15 | 5 | **10** | yes | 192575 | 2026-08-31 |
| 16 | FnB Board 5 | wireframes | pack | yes | P06 | 20 | 13 | 3 | **10** | yes | 205470 | 2026-08-31 |
| 17 | Seat Platform Board 13 | wireframes | pack | **local only** | P08 | 20 | 11 | 1 | **10** | yes | 144748 | 2026-08-31 |
| 18 | Seat Platform Board 7 | wireframes | pack | **local only** | P08 | 20 | 11 | 1 | **10** | yes | 130810 | 2026-08-31 |
| 19 | FnB Board 6 | wireframes | pack | yes | — | 20 | 10 | 0 | **10** | no | 182854 | 2026-08-31 |
| 20 | Inventory Board 2 | wireframes | pack | yes | — | 20 | 10 | 0 | **10** | no | 197697 | 2026-08-31 |
| 21 | Inventory Board 3 | wireframes | pack | yes | — | 20 | 10 | 0 | **10** | no | 178364 | 2026-08-31 |
| 22 | Inventory Board 4 | wireframes | pack | yes | — | 20 | 10 | 0 | **10** | no | 182288 | 2026-08-31 |
| 23 | Inventory Board 5 | wireframes | pack | yes | — | 20 | 10 | 0 | **10** | no | 178821 | 2026-08-31 |
| 24 | Inventory Board 6 | wireframes | pack | yes | — | 20 | 10 | 0 | **10** | no | 166018 | 2026-08-31 |
| 25 | Inventory Board 7 | wireframes | pack | yes | — | 20 | 10 | 0 | **10** | no | 156659 | 2026-08-31 |
| 26 | Marketing Board 10 | wireframes | pack | **local only** | — | 20 | 10 | 0 | **10** | no | 147515 | 2026-08-31 |
| 27 | Marketing Board 11 | wireframes | pack | **local only** | — | 20 | 10 | 0 | **10** | no | 149020 | 2026-08-31 |
| 28 | Marketing Board 12 | wireframes | pack | **local only** | — | 20 | 10 | 0 | **10** | no | 139495 | 2026-08-31 |
| 29 | Marketing Board 2 | wireframes | pack | **local only** | — | 20 | 10 | 0 | **10** | no | 138648 | 2026-08-31 |
| 30 | Marketing Board 3 | wireframes | pack | **local only** | — | 20 | 10 | 0 | **10** | no | 148170 | 2026-08-31 |
| 31 | Marketing Board 4 | wireframes | pack | **local only** | — | 20 | 10 | 0 | **10** | no | 152610 | 2026-08-31 |
| 32 | Marketing Board 5 | wireframes | pack | **local only** | — | 20 | 10 | 0 | **10** | no | 139261 | 2026-08-31 |
| 33 | Marketing Board 6 | wireframes | pack | **local only** | — | 20 | 10 | 0 | **10** | no | 145353 | 2026-08-31 |
| 34 | Marketing Board 8 | wireframes | pack | **local only** | — | 20 | 10 | 0 | **10** | no | 159216 | 2026-08-31 |
| 35 | Marketing Board 9 | wireframes | pack | **local only** | — | 20 | 10 | 0 | **10** | no | 156833 | 2026-08-31 |
| 36 | P04 Staff POS | wireframes | generated | yes | — | 10 | 10 | 0 | **10** | no | 117589 | 2026-08-25 |
| 37 | Seat Platform Board 1 | wireframes | pack | **local only** | — | 20 | 10 | 0 | **10** | no | 148219 | 2026-08-31 |
| 38 | Seat Platform Board 10 | wireframes | pack | **local only** | — | 20 | 10 | 0 | **10** | no | 137588 | 2026-08-31 |
| 39 | Seat Platform Board 11 | wireframes | pack | **local only** | — | 20 | 10 | 0 | **10** | no | 130961 | 2026-08-31 |
| 40 | Seat Platform Board 12 | wireframes | pack | **local only** | — | 20 | 10 | 0 | **10** | no | 149134 | 2026-08-31 |
| 41 | Seat Platform Board 2 | wireframes | pack | **local only** | — | 20 | 10 | 0 | **10** | no | 142851 | 2026-08-31 |
| 42 | Seat Platform Board 3 | wireframes | pack | **local only** | — | 20 | 10 | 0 | **10** | no | 133045 | 2026-08-31 |
| 43 | Seat Platform Board 4 | wireframes | pack | **local only** | — | 20 | 10 | 0 | **10** | no | 136779 | 2026-08-31 |
| 44 | Seat Platform Board 5 | wireframes | pack | **local only** | — | 20 | 10 | 0 | **10** | no | 136925 | 2026-08-31 |
| 45 | Seat Platform Board 6 | wireframes | pack | **local only** | — | 20 | 10 | 0 | **10** | no | 137840 | 2026-08-31 |
| 46 | Seat Platform Board 8 | wireframes | pack | **local only** | — | 20 | 10 | 0 | **10** | no | 105395 | 2026-08-31 |
| 47 | Seat Platform Board 9 | wireframes | pack | **local only** | — | 20 | 10 | 0 | **10** | no | 121177 | 2026-08-31 |
| 48 | P06 Venue Staff App | wireframes | generated | yes | P06 | 66 | 66 | 57 | **9** | yes | 207255 | 2026-08-31 |
| 49 | Retail Board 1 | wireframes | pack | yes | P08 | 18 | 12 | 3 | **9** | yes | 139385 | 2026-08-31 |
| 50 | FnB Board 1 | wireframes | pack | yes | P08 | 18 | 11 | 2 | **9** | yes | 180484 | 2026-08-31 |
| 51 | Marketing Board 1 | wireframes | pack | **local only** | P08 | 20 | 10 | 1 | **9** | yes | 149257 | 2026-08-31 |
| 52 | Marketing Board 7 | wireframes | pack | **local only** | P13 | 20 | 10 | 1 | **9** | yes | 141240 | 2026-08-31 |
| 53 | P11 Accreditation | wireframes | generated | yes | — | 8 | 8 | 0 | **8** | no | 82560 | 2026-08-25 |
| 54 | P12 Support Console | wireframes | generated | yes | — | 8 | 8 | 0 | **8** | no | 86988 | 2026-08-25 |
| 55 | Inventory Board 1 | wireframes | pack | yes | P06 | 16 | 8 | 1 | **7** | yes | 147417 | 2026-08-31 |
| 56 | POS Board 4 | wireframes | pack | yes | P08 | 12 | 11 | 5 | **6** | yes | 121940 | 2026-08-31 |
| 57 | POS Board 5 | wireframes | pack | yes | P08 | 12 | 11 | 5 | **6** | yes | 120314 | 2026-08-31 |
| 58 | POS Board 1 | wireframes | pack | yes | P08 | 12 | 10 | 4 | **6** | yes | 128646 | 2026-08-31 |
| 59 | POS Board 3 | wireframes | pack | yes | P04 | 12 | 10 | 4 | **6** | yes | 118302 | 2026-08-31 |
| 60 | TICVAI Boards | wireframes | pack | yes | P04 | 12 | 8 | 2 | **6** | yes | 136749 | 2026-08-31 |
| 61 | POS Board 6 | wireframes | pack | yes | — | 12 | 6 | 0 | **6** | no | 124835 | 2026-08-31 |
| 62 | Guest Mobile Board 1 | wireframes | pack | **local only** | P02 | 10 | 6 | 1 | **5** | yes | 58007 | 2026-08-31 |
| 63 | Guest Mobile Board 2 | wireframes | pack | **local only** | — | 10 | 5 | 0 | **5** | no | 53046 | 2026-08-31 |
| 64 | Guest Mobile Board 3 | wireframes | pack | **local only** | — | 10 | 5 | 0 | **5** | no | 53794 | 2026-08-31 |
| 65 | Guest Mobile Board 4 | wireframes | pack | **local only** | — | 10 | 5 | 0 | **5** | no | 51723 | 2026-08-31 |
| 66 | Guest Mobile Board 5 | wireframes | pack | **local only** | — | 10 | 5 | 0 | **5** | no | 51302 | 2026-08-31 |
| 67 | Guest Mobile Board 6 | wireframes | pack | **local only** | — | 10 | 5 | 0 | **5** | no | 56477 | 2026-08-31 |
| 68 | Guest Mobile Board 7 | wireframes | pack | **local only** | — | 10 | 5 | 0 | **5** | no | 53139 | 2026-08-31 |
| 69 | Guest Mobile Board 8 | wireframes | pack | **local only** | — | 10 | 5 | 0 | **5** | no | 48786 | 2026-08-31 |
| 70 | POS Frontline Board 2 | wireframes | pack | yes | P04 | 8 | 7 | 3 | **4** | yes | 70010 | 2026-08-31 |
| 71 | Seat Board 4 | wireframes | pack | yes | P02 P06 | 6 | 6 | 3 | **3** | yes | 36622 | 2026-08-31 |
| 72 | Seat Board 2 | wireframes | pack | yes | P08 | 10 | 7 | 5 | **2** | yes | 113050 | 2026-08-31 |
| 73 | Seat Board 3 | wireframes | pack | yes | P01 P04 P10 | 8 | 6 | 4 | **2** | yes | 76826 | 2026-08-31 |
| 74 | Seat Board 1 | wireframes | pack | yes | P08 | 6 | 4 | 3 | **1** | yes | 70498 | 2026-08-31 |
| 75 | P02 Guest App | wireframes | generated | yes | P02 | 63 | 63 | 63 | 0 | yes | 131646 | 2026-08-31 |
| 76 | P01 Guest Web | wireframes | generated | yes | P01 | 46 | 46 | 46 | 0 | yes | 111531 | 2026-08-31 |
| 77 | P09 TICVAI Web | wireframes | generated | yes | P09 | 37 | 37 | 37 | 0 | yes | 93222 | 2026-08-31 |
| 78 | P10 Partner Web | wireframes | generated | yes | P10 | 21 | 21 | 21 | 0 | yes | 60621 | 2026-08-31 |
| 79 | P13 Venue CMS | wireframes | generated | yes | P13 | 20 | 20 | 20 | 0 | yes | 61377 | 2026-08-31 |
| 80 | P05 Guest Kiosk | wireframes | generated | yes | P05 | 17 | 17 | 17 | 0 | yes | 46515 | 2026-08-31 |
| 81 | P07 Venue Scanner | wireframes | generated | yes | P07 | 11 | 11 | 11 | 0 | yes | 41445 | 2026-08-31 |
| 82 | P15 Kitchen Display | wireframes | generated | yes | P15 | 10 | 10 | 10 | 0 | yes | 42222 | 2026-08-31 |
| 83 | P16 Venue Analytics | wireframes | generated | yes | P16 | 10 | 10 | 10 | 0 | yes | 44248 | 2026-08-31 |
| 84 | Kiosk Board 1 | wireframes | pack | **local only** | P05 | 18 | 9 | 9 | 0 | yes | 50444 | 2026-08-31 |
| 85 | Kiosk Board 2 | wireframes | pack | **local only** | P05 | 16 | 8 | 8 | 0 | yes | 45509 | 2026-08-31 |
| 86 | P11 Accreditation Web | wireframes | generated | yes | P11 | 8 | 8 | 8 | 0 | yes | 26160 | 2026-08-31 |
| 87 | P12 Venue Support | wireframes | generated | yes | P12 | 8 | 8 | 8 | 0 | yes | 27002 | 2026-08-31 |
| 88 | P14 Developer | wireframes | generated | yes | P14 | 8 | 8 | 8 | 0 | yes | 30896 | 2026-08-31 |
| 89 | Dashboards Board | wireframes | pack | yes | P01 P09 P10 P12 | 10 | 5 | 5 | 0 | yes | 98846 | 2026-08-31 |
| 90 | Park POS | designs | single | yes | — | 0 | 0 | 0 | 0 | no | 121145 | 2026-08-25 |
| 91 | Park POS | designs | single | yes | — | 0 | 0 | 0 | 0 | no | 46665 | 2026-08-25 |
| 92 | Adam Invite | ui-design | single | yes | — | 0 | 0 | 0 | 0 | no | 11128 | 2026-08-31 |
| 93 | Adam Invite Day | ui-design | single | yes | — | 0 | 0 | 0 | 0 | no | 11430 | 2026-08-31 |
| 94 | Adam Landing | ui-design | single | yes | — | 0 | 0 | 0 | 0 | no | 22309 | 2026-08-31 |
| 95 | Adam Sign In | ui-design | single | yes | — | 0 | 0 | 0 | 0 | no | 18810 | 2026-08-31 |
| 96 | Adam Sign In Day | ui-design | single | yes | — | 0 | 0 | 0 | 0 | no | 19106 | 2026-08-31 |
| 97 | Viewer Redesign - Topbar | ui-design | single | yes | — | 0 | 0 | 0 | 0 | no | 68894 | 2026-08-31 |
| 98 | Viewer Redesign - Topbar Night | ui-design | single | yes | — | 0 | 0 | 0 | 0 | no | 68962 | 2026-08-31 |
| 99 | TICVAI All Boards Index | wireframes | index | yes | — | 0 | 0 | 0 | 0 | no | 970754 | 2026-08-31 |
| 100 | TICVAI Wireframe Boards | wireframes | single | yes | — | 0 | 0 | 0 | 0 | no | 12357 | 2026-08-31 |
| | **100 boards** | | | | | **1829** | **1362** | **551** | **811** | | | |

---

### Frame by frame, worst board first

Only the 74 boards with something unclaimed. Frames a screen already
claims are left out of these tables — they are not on the worklist.

#### P08 Staff Web Back Office — 73 of 73 unclaimed

`wireframes/P08 Staff Web Back Office.dc.html` · generated · no platform · nothing points at it

| # | Anchor | State | Name |
|--:|---|---|---|
| 1 | `bo-001` | bare | — |
| 2 | `bo-002` | bare | — |
| 3 | `bo-003` | bare | — |
| 4 | `bo-004` | bare | — |
| 5 | `bo-005` | bare | — |
| 6 | `bo-007` | bare | — |
| 7 | `bo-008` | bare | — |
| 8 | `bo-009` | bare | — |
| 9 | `bo-010` | bare | — |
| 10 | `bo-011` | bare | — |
| 11 | `bo-012` | bare | — |
| 12 | `bo-013` | bare | — |
| 13 | `bo-014` | bare | — |
| 14 | `bo-015` | bare | — |
| 15 | `bo-016` | bare | — |
| 16 | `bo-017` | bare | — |
| 17 | `bo-018` | bare | — |
| 18 | `bo-019` | bare | — |
| 19 | `bo-020` | bare | — |
| 20 | `bo-021` | bare | — |
| 21 | `bo-022` | bare | — |
| 22 | `bo-023` | bare | — |
| 23 | `bo-024` | bare | — |
| 24 | `bo-025` | bare | — |
| 25 | `bo-026` | bare | — |
| 26 | `bo-027` | bare | — |
| 27 | `bo-028` | bare | — |
| 28 | `bo-030` | bare | — |
| 29 | `bo-031` | bare | — |
| 30 | `bo-032` | bare | — |
| 31 | `bo-033` | bare | — |
| 32 | `bo-034` | bare | — |
| 33 | `bo-035` | bare | — |
| 34 | `bo-036` | bare | — |
| 35 | `bo-037` | bare | — |
| 36 | `bo-038` | bare | — |
| 37 | `bo-039` | bare | — |
| 38 | `bo-040` | bare | — |
| 39 | `bo-041` | bare | — |
| 40 | `bo-042` | bare | — |
| 41 | `bo-043` | bare | — |
| 42 | `bo-044` | bare | — |
| 43 | `bo-045` | bare | — |
| 44 | `bo-046` | bare | — |
| 45 | `bo-047` | bare | — |
| 46 | `bo-048` | bare | — |
| 47 | `bo-049` | bare | — |
| 48 | `bo-050` | bare | — |
| 49 | `bo-051` | bare | — |
| 50 | `bo-052` | bare | — |
| 51 | `bo-053` | bare | — |
| 52 | `bo-054` | bare | — |
| 53 | `bo-055` | bare | — |
| 54 | `bo-056` | bare | — |
| 55 | `bo-057` | bare | — |
| 56 | `bo-029` | bare | — |
| 57 | `bo-058` | bare | — |
| 58 | `bo-059` | bare | — |
| 59 | `bo-060` | bare | — |
| 60 | `bo-061` | bare | — |
| 61 | `bo-006` | bare | — |
| 62 | `bo-062` | bare | — |
| 63 | `bo-063` | bare | — |
| 64 | `bo-064` | bare | — |
| 65 | `bo-065` | bare | — |
| 66 | `bo-066` | bare | — |
| 67 | `bo-067` | bare | — |
| 68 | `bo-068` | bare | — |
| 69 | `bo-069` | bare | — |
| 70 | `bo-070` | bare | — |
| 71 | `bo-071` | bare | — |
| 72 | `bo-072` | bare | — |
| 73 | `bo-073` | bare | — |

#### P06 Staff App — 50 of 50 unclaimed

`wireframes/P06 Staff App.dc.html` · generated · no platform · nothing points at it

| # | Anchor | State | Name |
|--:|---|---|---|
| 1 | `emp-001` | bare | — |
| 2 | `emp-002` | bare | — |
| 3 | `emp-003` | bare | — |
| 4 | `emp-048` | bare | — |
| 5 | `emp-009` | bare | — |
| 6 | `emp-010` | bare | — |
| 7 | `emp-011` | bare | — |
| 8 | `emp-012` | bare | — |
| 9 | `emp-013` | bare | — |
| 10 | `emp-014` | bare | — |
| 11 | `emp-015` | bare | — |
| 12 | `emp-016` | bare | — |
| 13 | `emp-017` | bare | — |
| 14 | `emp-018` | bare | — |
| 15 | `emp-004` | bare | — |
| 16 | `emp-005` | bare | — |
| 17 | `emp-006` | bare | — |
| 18 | `emp-007` | bare | — |
| 19 | `emp-008` | bare | — |
| 20 | `emp-019` | bare | — |
| 21 | `emp-020` | bare | — |
| 22 | `emp-031` | bare | — |
| 23 | `emp-032` | bare | — |
| 24 | `emp-033` | bare | — |
| 25 | `emp-034` | bare | — |
| 26 | `emp-035` | bare | — |
| 27 | `emp-036` | bare | — |
| 28 | `emp-037` | bare | — |
| 29 | `emp-039` | bare | — |
| 30 | `emp-047` | bare | — |
| 31 | `emp-050` | bare | — |
| 32 | `emp-021` | bare | — |
| 33 | `emp-022` | bare | — |
| 34 | `emp-023` | bare | — |
| 35 | `emp-024` | bare | — |
| 36 | `emp-025` | bare | — |
| 37 | `emp-026` | bare | — |
| 38 | `emp-027` | bare | — |
| 39 | `emp-028` | bare | — |
| 40 | `emp-029` | bare | — |
| 41 | `emp-030` | bare | — |
| 42 | `emp-038` | bare | — |
| 43 | `emp-040` | bare | — |
| 44 | `emp-041` | bare | — |
| 45 | `emp-042` | bare | — |
| 46 | `emp-043` | bare | — |
| 47 | `emp-044` | bare | — |
| 48 | `emp-045` | bare | — |
| 49 | `emp-046` | bare | — |
| 50 | `emp-049` | bare | — |

#### P08 Venue Management — 43 of 143 unclaimed

`wireframes/P08 Venue Management.dc.html` · generated · P08 · 100 screen claims on this board

| # | Anchor | State | Name |
|--:|---|---|---|
| 1 | `bo-007` | named | Product Directory |
| 2 | `bo-009` | named | Pricing Rules |
| 3 | `bo-010` | named | Promotions & Coupons |
| 4 | `bo-011` | named | Packages & Bundles |
| 5 | `bo-013` | named | Channel & Distribution |
| 6 | `bo-014` | named | Catalogue Publishing |
| 7 | `bo-037` | named | Offline Package Status |
| 8 | `bo-111` | named | Ingredient Substitution, Allergen & Nutrition |
| 9 | `bo-112` | named | Production Planning & Production Sheets |
| 10 | `bo-113` | named | Central Kitchen & Commissary Management |
| 11 | `bo-114` | named | Variants, Attributes, Barcode & RFID Management |
| 12 | `bo-115` | named | Category, Brand & Merchandise Hierarchy |
| 13 | `bo-116` | named | Merchandising & Product Presentation |
| 14 | `bo-117` | named | Product Import, Governance & AI Configuration Assistant |
| 15 | `bo-118` | named | Campaign & Audience Management |
| 16 | `bo-119` | named | Cross-Sell, Upsell & Recommendation Rules |
| 17 | `bo-121` | named | Personalized Offers & Guest Engagement |
| 18 | `bo-122` | named | POS Experience Dashboard |
| 19 | `bo-124` | named | Layout & Journey Builder |
| 20 | `bo-125` | named | Product & Category Button Configuration |
| 21 | `bo-126` | named | Deployment, Preview & Audit |
| 22 | `bo-008` | named | Product Detail & Variants |
| 23 | `bo-024` | named | Payment Exceptions |
| 24 | `bo-021` | named | Order Search |
| 25 | `bo-045` | named | Menu Management |
| 26 | `bo-136` | named | F&B Global Settings & Controls |
| 27 | `bo-036` | named | Device Registry |
| 28 | `bo-044` | named | F&B Outlets |
| 29 | `bo-058` | named | Reporting Home |
| 30 | `bo-128` | named | Live Workstation Health Monitor |
| 31 | `bo-129` | named | Software, Configuration & Version Management |
| 32 | `bo-130` | named | Offline Policy & Rules Configuration |
| 33 | `bo-133` | named | Offline Alerts, Limits & Audit |
| 34 | `bo-049` | named | Stock Levels |
| 35 | `bo-052` | named | Goods Receipt |
| 36 | `bo-078` | named | Requisitions |
| 37 | `bo-079` | named | Stock Count |
| 38 | `bo-080` | named | Stock Transfers |
| 39 | `bo-081` | named | Inventory Items |
| 40 | `bo-082` | named | Stock Movements |
| 41 | `bo-083` | named | Suppliers |
| 42 | `bo-137` | named | Recipe Consumption & Theoretical Inventory |
| 43 | `bo-068` | named | Audit Log |

#### P09 Admin Web — 36 of 36 unclaimed

`wireframes/P09 Admin Web.dc.html` · generated · no platform · nothing points at it

| # | Anchor | State | Name |
|--:|---|---|---|
| 1 | `adm-001` | bare | — |
| 2 | `adm-002` | bare | — |
| 3 | `adm-003` | bare | — |
| 4 | `adm-004` | bare | — |
| 5 | `adm-005` | bare | — |
| 6 | `adm-006` | bare | — |
| 7 | `adm-007` | bare | — |
| 8 | `adm-012` | bare | — |
| 9 | `adm-013` | bare | — |
| 10 | `adm-008` | bare | — |
| 11 | `adm-009` | bare | — |
| 12 | `adm-010` | bare | — |
| 13 | `adm-011` | bare | — |
| 14 | `adm-016` | bare | — |
| 15 | `adm-017` | bare | — |
| 16 | `adm-018` | bare | — |
| 17 | `adm-020` | bare | — |
| 18 | `adm-021` | bare | — |
| 19 | `adm-019` | bare | — |
| 20 | `adm-022` | bare | — |
| 21 | `adm-023` | bare | — |
| 22 | `adm-024` | bare | — |
| 23 | `adm-025` | bare | — |
| 24 | `adm-026` | bare | — |
| 25 | `adm-027` | bare | — |
| 26 | `adm-028` | bare | — |
| 27 | `adm-029` | bare | — |
| 28 | `adm-014` | bare | — |
| 29 | `adm-015` | bare | — |
| 30 | `adm-030` | bare | — |
| 31 | `adm-033` | bare | — |
| 32 | `adm-034` | bare | — |
| 33 | `adm-031` | bare | — |
| 34 | `adm-032` | bare | — |
| 35 | `adm-035` | bare | — |
| 36 | `adm-036` | bare | — |

#### P13 White-Label CMS — 20 of 20 unclaimed

`wireframes/P13 White-Label CMS.dc.html` · generated · no platform · nothing points at it

| # | Anchor | State | Name |
|--:|---|---|---|
| 1 | `cms-001` | bare | — |
| 2 | `cms-002` | bare | — |
| 3 | `cms-003` | bare | — |
| 4 | `cms-004` | bare | — |
| 5 | `cms-005` | bare | — |
| 6 | `cms-006` | bare | — |
| 7 | `cms-007` | bare | — |
| 8 | `cms-008` | bare | — |
| 9 | `cms-009` | bare | — |
| 10 | `cms-010` | bare | — |
| 11 | `cms-013` | bare | — |
| 12 | `cms-011` | bare | — |
| 13 | `cms-012` | bare | — |
| 14 | `cms-014` | bare | — |
| 15 | `cms-015` | bare | — |
| 16 | `cms-016` | bare | — |
| 17 | `cms-017` | bare | — |
| 18 | `cms-018` | bare | — |
| 19 | `cms-019` | bare | — |
| 20 | `cms-020` | bare | — |

#### P07 Staff Scanner — 16 of 16 unclaimed

`wireframes/P07 Staff Scanner.dc.html` · generated · no platform · nothing points at it

| # | Anchor | State | Name |
|--:|---|---|---|
| 1 | `scn-001` | bare | — |
| 2 | `scn-002` | bare | — |
| 3 | `scn-003` | bare | — |
| 4 | `scn-004` | bare | — |
| 5 | `scn-005` | bare | — |
| 6 | `scn-006` | bare | — |
| 7 | `scn-007` | bare | — |
| 8 | `scn-008` | bare | — |
| 9 | `scn-009` | bare | — |
| 10 | `scn-010` | bare | — |
| 11 | `scn-011` | bare | — |
| 12 | `scn-012` | bare | — |
| 13 | `scn-013` | bare | — |
| 14 | `scn-014` | bare | — |
| 15 | `scn-015` | bare | — |
| 16 | `scn-016` | bare | — |

#### FnB Board 2 — 13 of 18 unclaimed

`wireframes/FnB Board 2.dc.html` · pack · P08 · 5 screen claims on this board

| # | Anchor | State | Name |
|--:|---|---|---|
| 1 | `bo-045` | bare | — |
| 2 | `bo-109` | bare | — |
| 3 | `fnb-2c` | bare | — |
| 4 | `fnb-2d` | bare | — |
| 5 | `fnb-2e` | bare | — |
| 6 | `bo-137` | bare | — |
| 7 | `fnb-2g` | bare | — |
| 8 | `fnb-2h` | bare | — |
| 9 | `fnb-2j` | bare | — |
| 10 | `fnb-2k` | bare | — |
| 11 | `bo-111` | bare | — |
| 12 | `bo-136` | bare | — |
| 13 | `fnb-2n` | bare | — |

#### P04 Venue POS — 12 of 24 unclaimed

`wireframes/P04 Venue POS.dc.html` · generated · P04 · 12 screen claims on this board

| # | Anchor | State | Name |
|--:|---|---|---|
| 1 | `pos-001` | named | Begin Shift |
| 2 | `pos-007` | named | Close Shift |
| 3 | `pos-009` | named | Staff Roster |
| 4 | `pos-002` | named | Sell — Ticket Catalogue |
| 5 | `pos-006` | named | Held Orders |
| 6 | `pos-011` | named | Returns, Refunds & Exchanges |
| 7 | `pos-012` | named | Omnichannel Order & Fulfilment Center |
| 8 | `pos-013` | named | Mobile POS, Event Sales & Offline Operations |
| 9 | `pos-018` | named | Safe Drop & Cash Transfer Management |
| 10 | `pos-019` | named | Shift Templates & Policies |
| 11 | `pos-020` | named | Shift Exceptions & Alerts |
| 12 | `pos-005` | named | Payment |

#### Retail Board 2 — 11 of 18 unclaimed

`wireframes/Retail Board 2.dc.html` · pack · P08 · 7 screen claims on this board

| # | Anchor | State | Name |
|--:|---|---|---|
| 1 | `bo-007` | bare | — |
| 2 | `ret-2b` | bare | — |
| 3 | `bo-008` | bare | — |
| 4 | `bo-113` | bare | — |
| 5 | `bo-112` | bare | — |
| 6 | `bo-009` | bare | — |
| 7 | `bo-083` | bare | — |
| 8 | `bo-014` | bare | — |
| 9 | `ret-2j` | bare | — |
| 10 | `ret-2k` | bare | — |
| 11 | `ret-2l` | bare | — |

#### Retail Board 6 — 11 of 14 unclaimed

`wireframes/Retail Board 6.dc.html` · pack · P08, P16 · 3 screen claims on this board

| # | Anchor | State | Name |
|--:|---|---|---|
| 1 | `ret-6a` | bare | — |
| 2 | `ret-6l` | bare | — |
| 3 | `ret-6b` | bare | — |
| 4 | `ret-6c` | bare | — |
| 5 | `anl-006` | bare | — |
| 6 | `ret-6e` | bare | — |
| 7 | `ret-6f` | bare | — |
| 8 | `ret-6g` | bare | — |
| 9 | `bo-058` | bare | — |
| 10 | `bo-068` | bare | — |
| 11 | `ret-6k` | bare | — |

#### FnB Board 3 — 10 of 17 unclaimed

`wireframes/FnB Board 3.dc.html` · pack · P15 · 7 screen claims on this board

| # | Anchor | State | Name |
|--:|---|---|---|
| 1 | `kit-001` | bare | — |
| 2 | `kit-002` | bare | — |
| 3 | `kit-003` | bare | — |
| 4 | `fnb-3d` | bare | — |
| 5 | `kit-005` | bare | — |
| 6 | `kit-006` | bare | — |
| 7 | `fnb-3g` | bare | — |
| 8 | `kit-008` | bare | — |
| 9 | `kit-009` | bare | — |
| 10 | `fnb-3k` | bare | — |

#### FnB Board 4 — 10 of 18 unclaimed

`wireframes/FnB Board 4.dc.html` · pack · P06 · 13 screen claims on this board

| # | Anchor | State | Name |
|--:|---|---|---|
| 1 | `emp-058` | bare | — |
| 2 | `emp-052` | bare | — |
| 3 | `emp-060` | bare | — |
| 4 | `emp-061` | bare | — |
| 5 | `emp-055` | bare | — |
| 6 | `emp-063` | bare | — |
| 7 | `emp-064` | bare | — |
| 8 | `fnb-4h` | bare | — |
| 9 | `emp-059` | bare | — |
| 10 | `fnb-4k` | bare | — |

#### FnB Board 5 — 10 of 13 unclaimed

`wireframes/FnB Board 5.dc.html` · pack · P06 · 3 screen claims on this board

| # | Anchor | State | Name |
|--:|---|---|---|
| 1 | `fnb-5a` | bare | — |
| 2 | `fnb-5b` | bare | — |
| 3 | `fnb-5c` | bare | — |
| 4 | `fnb-5d` | bare | — |
| 5 | `emp-067` | bare | — |
| 6 | `fnb-5f` | bare | — |
| 7 | `emp-065` | bare | — |
| 8 | `fnb-5h` | bare | — |
| 9 | `emp-062` | bare | — |
| 10 | `fnb-5k` | bare | — |

#### FnB Board 6 — 10 of 10 unclaimed

`wireframes/FnB Board 6.dc.html` · pack · no platform · nothing points at it

| # | Anchor | State | Name |
|--:|---|---|---|
| 1 | `fnb-6a` | bare | — |
| 2 | `fnb-6b` | bare | — |
| 3 | `fnb-6c` | bare | — |
| 4 | `fnb-6d` | bare | — |
| 5 | `fnb-6e` | bare | — |
| 6 | `fnb-6f` | bare | — |
| 7 | `fnb-6g` | bare | — |
| 8 | `fnb-6h` | bare | — |
| 9 | `fnb-6j` | bare | — |
| 10 | `fnb-6k` | bare | — |

#### Inventory Board 2 — 10 of 10 unclaimed

`wireframes/Inventory Board 2.dc.html` · pack · no platform · nothing points at it

| # | Anchor | State | Name |
|--:|---|---|---|
| 1 | `inv-2a` | bare | — |
| 2 | `inv-2b` | bare | — |
| 3 | `inv-2c` | bare | — |
| 4 | `inv-2d` | bare | — |
| 5 | `inv-2e` | bare | — |
| 6 | `inv-2f` | bare | — |
| 7 | `inv-2g` | bare | — |
| 8 | `inv-2h` | bare | — |
| 9 | `inv-2j` | bare | — |
| 10 | `inv-2k` | bare | — |

#### Inventory Board 3 — 10 of 10 unclaimed

`wireframes/Inventory Board 3.dc.html` · pack · no platform · nothing points at it

| # | Anchor | State | Name |
|--:|---|---|---|
| 1 | `inv-3a` | bare | — |
| 2 | `inv-3b` | bare | — |
| 3 | `inv-3c` | bare | — |
| 4 | `inv-3d` | bare | — |
| 5 | `inv-3e` | bare | — |
| 6 | `inv-3f` | bare | — |
| 7 | `inv-3g` | bare | — |
| 8 | `inv-3h` | bare | — |
| 9 | `inv-3j` | bare | — |
| 10 | `inv-3k` | bare | — |

#### Inventory Board 4 — 10 of 10 unclaimed

`wireframes/Inventory Board 4.dc.html` · pack · no platform · nothing points at it

| # | Anchor | State | Name |
|--:|---|---|---|
| 1 | `inv-4a` | bare | — |
| 2 | `inv-4b` | bare | — |
| 3 | `inv-4c` | bare | — |
| 4 | `inv-4d` | bare | — |
| 5 | `inv-4e` | bare | — |
| 6 | `inv-4f` | bare | — |
| 7 | `inv-4g` | bare | — |
| 8 | `inv-4h` | bare | — |
| 9 | `inv-4j` | bare | — |
| 10 | `inv-4k` | bare | — |

#### Inventory Board 5 — 10 of 10 unclaimed

`wireframes/Inventory Board 5.dc.html` · pack · no platform · nothing points at it

| # | Anchor | State | Name |
|--:|---|---|---|
| 1 | `inv-5a` | bare | — |
| 2 | `inv-5b` | bare | — |
| 3 | `inv-5c` | bare | — |
| 4 | `inv-5d` | bare | — |
| 5 | `inv-5e` | bare | — |
| 6 | `inv-5f` | bare | — |
| 7 | `inv-5g` | bare | — |
| 8 | `inv-5h` | bare | — |
| 9 | `inv-5j` | bare | — |
| 10 | `inv-5k` | bare | — |

#### Inventory Board 6 — 10 of 10 unclaimed

`wireframes/Inventory Board 6.dc.html` · pack · no platform · nothing points at it

| # | Anchor | State | Name |
|--:|---|---|---|
| 1 | `inv-6a` | bare | — |
| 2 | `inv-6b` | bare | — |
| 3 | `inv-6c` | bare | — |
| 4 | `inv-6d` | bare | — |
| 5 | `inv-6e` | bare | — |
| 6 | `inv-6f` | bare | — |
| 7 | `inv-6g` | bare | — |
| 8 | `inv-6h` | bare | — |
| 9 | `inv-6i` | bare | — |
| 10 | `inv-6j` | bare | — |

#### Inventory Board 7 — 10 of 10 unclaimed

`wireframes/Inventory Board 7.dc.html` · pack · no platform · nothing points at it

| # | Anchor | State | Name |
|--:|---|---|---|
| 1 | `inv-7a` | bare | — |
| 2 | `inv-7b` | bare | — |
| 3 | `inv-7c` | bare | — |
| 4 | `inv-7d` | bare | — |
| 5 | `inv-7e` | bare | — |
| 6 | `inv-7f` | bare | — |
| 7 | `inv-7g` | bare | — |
| 8 | `inv-7h` | bare | — |
| 9 | `inv-7i` | bare | — |
| 10 | `inv-7j` | bare | — |

#### Marketing Board 10 — 10 of 10 unclaimed

`wireframes/Marketing Board 10.dc.html` · pack · no platform · nothing points at it

| # | Anchor | State | Name |
|--:|---|---|---|
| 1 | `crm-10a` | bare | — |
| 2 | `crm-10b` | bare | — |
| 3 | `crm-10c` | bare | — |
| 4 | `crm-10d` | bare | — |
| 5 | `crm-10e` | bare | — |
| 6 | `crm-10f` | bare | — |
| 7 | `crm-10g` | bare | — |
| 8 | `crm-10h` | bare | — |
| 9 | `crm-10i` | bare | — |
| 10 | `crm-10j` | bare | — |

#### Marketing Board 11 — 10 of 10 unclaimed

`wireframes/Marketing Board 11.dc.html` · pack · no platform · nothing points at it

| # | Anchor | State | Name |
|--:|---|---|---|
| 1 | `crm-11a` | bare | — |
| 2 | `crm-11b` | bare | — |
| 3 | `crm-11c` | bare | — |
| 4 | `crm-11d` | bare | — |
| 5 | `crm-11e` | bare | — |
| 6 | `crm-11f` | bare | — |
| 7 | `crm-11g` | bare | — |
| 8 | `crm-11h` | bare | — |
| 9 | `crm-11i` | bare | — |
| 10 | `crm-11j` | bare | — |

#### Marketing Board 12 — 10 of 10 unclaimed

`wireframes/Marketing Board 12.dc.html` · pack · no platform · nothing points at it

| # | Anchor | State | Name |
|--:|---|---|---|
| 1 | `crm-12a` | bare | — |
| 2 | `crm-12b` | bare | — |
| 3 | `crm-12c` | bare | — |
| 4 | `crm-12d` | bare | — |
| 5 | `crm-12e` | bare | — |
| 6 | `crm-12f` | bare | — |
| 7 | `crm-12g` | bare | — |
| 8 | `crm-12h` | bare | — |
| 9 | `crm-12i` | bare | — |
| 10 | `crm-12j` | bare | — |

#### Marketing Board 2 — 10 of 10 unclaimed

`wireframes/Marketing Board 2.dc.html` · pack · no platform · nothing points at it

| # | Anchor | State | Name |
|--:|---|---|---|
| 1 | `crm-2a` | bare | — |
| 2 | `crm-2b` | bare | — |
| 3 | `crm-2c` | bare | — |
| 4 | `crm-2d` | bare | — |
| 5 | `crm-2e` | bare | — |
| 6 | `crm-2f` | bare | — |
| 7 | `crm-2g` | bare | — |
| 8 | `crm-2h` | bare | — |
| 9 | `crm-2i` | bare | — |
| 10 | `crm-2j` | bare | — |

#### Marketing Board 3 — 10 of 10 unclaimed

`wireframes/Marketing Board 3.dc.html` · pack · no platform · nothing points at it

| # | Anchor | State | Name |
|--:|---|---|---|
| 1 | `crm-3a` | bare | — |
| 2 | `crm-3b` | bare | — |
| 3 | `crm-3c` | bare | — |
| 4 | `crm-3d` | bare | — |
| 5 | `crm-3e` | bare | — |
| 6 | `crm-3f` | bare | — |
| 7 | `crm-3g` | bare | — |
| 8 | `crm-3h` | bare | — |
| 9 | `crm-3i` | bare | — |
| 10 | `crm-3j` | bare | — |

#### Marketing Board 4 — 10 of 10 unclaimed

`wireframes/Marketing Board 4.dc.html` · pack · no platform · nothing points at it

| # | Anchor | State | Name |
|--:|---|---|---|
| 1 | `crm-4a` | bare | — |
| 2 | `crm-4b` | bare | — |
| 3 | `crm-4c` | bare | — |
| 4 | `crm-4d` | bare | — |
| 5 | `crm-4e` | bare | — |
| 6 | `crm-4f` | bare | — |
| 7 | `crm-4g` | bare | — |
| 8 | `crm-4h` | bare | — |
| 9 | `crm-4i` | bare | — |
| 10 | `crm-4j` | bare | — |

#### Marketing Board 5 — 10 of 10 unclaimed

`wireframes/Marketing Board 5.dc.html` · pack · no platform · nothing points at it

| # | Anchor | State | Name |
|--:|---|---|---|
| 1 | `crm-5a` | bare | — |
| 2 | `crm-5b` | bare | — |
| 3 | `crm-5c` | bare | — |
| 4 | `crm-5d` | bare | — |
| 5 | `crm-5e` | bare | — |
| 6 | `crm-5f` | bare | — |
| 7 | `crm-5g` | bare | — |
| 8 | `crm-5h` | bare | — |
| 9 | `crm-5i` | bare | — |
| 10 | `crm-5j` | bare | — |

#### Marketing Board 6 — 10 of 10 unclaimed

`wireframes/Marketing Board 6.dc.html` · pack · no platform · nothing points at it

| # | Anchor | State | Name |
|--:|---|---|---|
| 1 | `crm-6a` | bare | — |
| 2 | `crm-6b` | bare | — |
| 3 | `crm-6c` | bare | — |
| 4 | `crm-6d` | bare | — |
| 5 | `crm-6e` | bare | — |
| 6 | `crm-6f` | bare | — |
| 7 | `crm-6g` | bare | — |
| 8 | `crm-6h` | bare | — |
| 9 | `crm-6i` | bare | — |
| 10 | `crm-6j` | bare | — |

#### Marketing Board 8 — 10 of 10 unclaimed

`wireframes/Marketing Board 8.dc.html` · pack · no platform · nothing points at it

| # | Anchor | State | Name |
|--:|---|---|---|
| 1 | `crm-8a` | bare | — |
| 2 | `crm-8b` | bare | — |
| 3 | `crm-8c` | bare | — |
| 4 | `crm-8d` | bare | — |
| 5 | `crm-8e` | bare | — |
| 6 | `crm-8f` | bare | — |
| 7 | `crm-8g` | bare | — |
| 8 | `crm-8h` | bare | — |
| 9 | `crm-8i` | bare | — |
| 10 | `crm-8j` | bare | — |

#### Marketing Board 9 — 10 of 10 unclaimed

`wireframes/Marketing Board 9.dc.html` · pack · no platform · nothing points at it

| # | Anchor | State | Name |
|--:|---|---|---|
| 1 | `crm-9a` | bare | — |
| 2 | `crm-9b` | bare | — |
| 3 | `crm-9c` | bare | — |
| 4 | `crm-9d` | bare | — |
| 5 | `crm-9e` | bare | — |
| 6 | `crm-9f` | bare | — |
| 7 | `crm-9g` | bare | — |
| 8 | `crm-9h` | bare | — |
| 9 | `crm-9i` | bare | — |
| 10 | `crm-9j` | bare | — |

#### P04 Staff POS — 10 of 10 unclaimed

`wireframes/P04 Staff POS.dc.html` · generated · no platform · nothing points at it

| # | Anchor | State | Name |
|--:|---|---|---|
| 1 | `pos-001` | bare | — |
| 2 | `pos-002` | bare | — |
| 3 | `pos-003` | bare | — |
| 4 | `pos-004` | bare | — |
| 5 | `pos-010` | bare | — |
| 6 | `pos-005` | bare | — |
| 7 | `pos-006` | bare | — |
| 8 | `pos-007` | bare | — |
| 9 | `pos-008` | bare | — |
| 10 | `pos-009` | bare | — |

#### Retail Board 3 — 10 of 15 unclaimed

`wireframes/Retail Board 3.dc.html` · pack · P04, P08 · 5 screen claims on this board

| # | Anchor | State | Name |
|--:|---|---|---|
| 1 | `bo-021` | bare | — |
| 2 | `pos-002` | bare | — |
| 3 | `ret-3c` | bare | — |
| 4 | `ret-3d` | bare | — |
| 5 | `pos-005` | bare | — |
| 6 | `pos-006` | bare | — |
| 7 | `ret-3g` | bare | — |
| 8 | `ret-3h` | bare | — |
| 9 | `ret-3j` | bare | — |
| 10 | `bo-024` | bare | — |

#### Retail Board 4 — 10 of 19 unclaimed

`wireframes/Retail Board 4.dc.html` · pack · P06, P08 · 11 screen claims on this board

| # | Anchor | State | Name |
|--:|---|---|---|
| 1 | `bo-049` | bare | — |
| 2 | `bo-081` | bare | — |
| 3 | `bo-078` | bare | — |
| 4 | `bo-080` | bare | — |
| 5 | `bo-052` | bare | — |
| 6 | `bo-079` | bare | — |
| 7 | `bo-082` | bare | — |
| 8 | `emp-068` | bare | — |
| 9 | `bo-114` | bare | — |
| 10 | `ret-4k` | bare | — |

#### Retail Board 5 — 10 of 15 unclaimed

`wireframes/Retail Board 5.dc.html` · pack · P08 · 6 screen claims on this board

| # | Anchor | State | Name |
|--:|---|---|---|
| 1 | `ret-5a` | bare | — |
| 2 | `ret-5b` | bare | — |
| 3 | `ret-5c` | bare | — |
| 4 | `bo-119` | bare | — |
| 5 | `ret-5e` | bare | — |
| 6 | `bo-121` | bare | — |
| 7 | `bo-120` | bare | — |
| 8 | `bo-011` | bare | — |
| 9 | `bo-122` | bare | — |
| 10 | `ret-5k` | bare | — |

#### Seat Platform Board 1 — 10 of 10 unclaimed

`wireframes/Seat Platform Board 1.dc.html` · pack · no platform · nothing points at it

| # | Anchor | State | Name |
|--:|---|---|---|
| 1 | `seatp-1a` | bare | — |
| 2 | `seatp-1b` | bare | — |
| 3 | `seatp-1c` | bare | — |
| 4 | `seatp-1d` | bare | — |
| 5 | `seatp-1e` | bare | — |
| 6 | `seatp-1f` | bare | — |
| 7 | `seatp-1g` | bare | — |
| 8 | `seatp-1h` | bare | — |
| 9 | `seatp-1i` | bare | — |
| 10 | `seatp-1j` | bare | — |

#### Seat Platform Board 10 — 10 of 10 unclaimed

`wireframes/Seat Platform Board 10.dc.html` · pack · no platform · nothing points at it

| # | Anchor | State | Name |
|--:|---|---|---|
| 1 | `seatp-10a` | bare | — |
| 2 | `seatp-10b` | bare | — |
| 3 | `seatp-10c` | bare | — |
| 4 | `seatp-10d` | bare | — |
| 5 | `seatp-10e` | bare | — |
| 6 | `seatp-10f` | bare | — |
| 7 | `seatp-10g` | bare | — |
| 8 | `seatp-10h` | bare | — |
| 9 | `seatp-10i` | bare | — |
| 10 | `seatp-10j` | bare | — |

#### Seat Platform Board 11 — 10 of 10 unclaimed

`wireframes/Seat Platform Board 11.dc.html` · pack · no platform · nothing points at it

| # | Anchor | State | Name |
|--:|---|---|---|
| 1 | `seatp-11a` | bare | — |
| 2 | `seatp-11b` | bare | — |
| 3 | `seatp-11c` | bare | — |
| 4 | `seatp-11d` | bare | — |
| 5 | `seatp-11e` | bare | — |
| 6 | `seatp-11f` | bare | — |
| 7 | `seatp-11g` | bare | — |
| 8 | `seatp-11h` | bare | — |
| 9 | `seatp-11i` | bare | — |
| 10 | `seatp-11j` | bare | — |

#### Seat Platform Board 12 — 10 of 10 unclaimed

`wireframes/Seat Platform Board 12.dc.html` · pack · no platform · nothing points at it

| # | Anchor | State | Name |
|--:|---|---|---|
| 1 | `seatp-12a` | bare | — |
| 2 | `seatp-12b` | bare | — |
| 3 | `seatp-12c` | bare | — |
| 4 | `seatp-12d` | bare | — |
| 5 | `seatp-12e` | bare | — |
| 6 | `seatp-12f` | bare | — |
| 7 | `seatp-12g` | bare | — |
| 8 | `seatp-12h` | bare | — |
| 9 | `seatp-12i` | bare | — |
| 10 | `seatp-12j` | bare | — |

#### Seat Platform Board 13 — 10 of 11 unclaimed

`wireframes/Seat Platform Board 13.dc.html` · pack · P08 · 1 screen claim on this board

| # | Anchor | State | Name |
|--:|---|---|---|
| 1 | `seatp-13a` | bare | — |
| 2 | `seatp-13b` | bare | — |
| 3 | `seatp-13c` | bare | — |
| 4 | `bo-067` | bare | — |
| 5 | `seatp-13e` | bare | — |
| 6 | `seatp-13f` | bare | — |
| 7 | `seatp-13g` | bare | — |
| 8 | `seatp-13h` | bare | — |
| 9 | `seatp-13i` | bare | — |
| 10 | `seatp-13j` | bare | — |

#### Seat Platform Board 2 — 10 of 10 unclaimed

`wireframes/Seat Platform Board 2.dc.html` · pack · no platform · nothing points at it

| # | Anchor | State | Name |
|--:|---|---|---|
| 1 | `seatp-2a` | bare | — |
| 2 | `seatp-2b` | bare | — |
| 3 | `seatp-2c` | bare | — |
| 4 | `seatp-2d` | bare | — |
| 5 | `seatp-2e` | bare | — |
| 6 | `seatp-2f` | bare | — |
| 7 | `seatp-2g` | bare | — |
| 8 | `seatp-2h` | bare | — |
| 9 | `seatp-2i` | bare | — |
| 10 | `seatp-2j` | bare | — |

#### Seat Platform Board 3 — 10 of 10 unclaimed

`wireframes/Seat Platform Board 3.dc.html` · pack · no platform · nothing points at it

| # | Anchor | State | Name |
|--:|---|---|---|
| 1 | `seatp-3a` | bare | — |
| 2 | `seatp-3b` | bare | — |
| 3 | `seatp-3c` | bare | — |
| 4 | `seatp-3d` | bare | — |
| 5 | `seatp-3e` | bare | — |
| 6 | `seatp-3f` | bare | — |
| 7 | `seatp-3g` | bare | — |
| 8 | `seatp-3h` | bare | — |
| 9 | `seatp-3i` | bare | — |
| 10 | `seatp-3j` | bare | — |

#### Seat Platform Board 4 — 10 of 10 unclaimed

`wireframes/Seat Platform Board 4.dc.html` · pack · no platform · nothing points at it

| # | Anchor | State | Name |
|--:|---|---|---|
| 1 | `seatp-4a` | bare | — |
| 2 | `seatp-4b` | bare | — |
| 3 | `seatp-4c` | bare | — |
| 4 | `seatp-4d` | bare | — |
| 5 | `seatp-4e` | bare | — |
| 6 | `seatp-4f` | bare | — |
| 7 | `seatp-4g` | bare | — |
| 8 | `seatp-4h` | bare | — |
| 9 | `seatp-4i` | bare | — |
| 10 | `seatp-4j` | bare | — |

#### Seat Platform Board 5 — 10 of 10 unclaimed

`wireframes/Seat Platform Board 5.dc.html` · pack · no platform · nothing points at it

| # | Anchor | State | Name |
|--:|---|---|---|
| 1 | `seatp-5a` | bare | — |
| 2 | `seatp-5b` | bare | — |
| 3 | `seatp-5c` | bare | — |
| 4 | `seatp-5d` | bare | — |
| 5 | `seatp-5e` | bare | — |
| 6 | `seatp-5f` | bare | — |
| 7 | `seatp-5g` | bare | — |
| 8 | `seatp-5h` | bare | — |
| 9 | `seatp-5i` | bare | — |
| 10 | `seatp-5j` | bare | — |

#### Seat Platform Board 6 — 10 of 10 unclaimed

`wireframes/Seat Platform Board 6.dc.html` · pack · no platform · nothing points at it

| # | Anchor | State | Name |
|--:|---|---|---|
| 1 | `seatp-6a` | bare | — |
| 2 | `seatp-6b` | bare | — |
| 3 | `seatp-6c` | bare | — |
| 4 | `seatp-6d` | bare | — |
| 5 | `seatp-6e` | bare | — |
| 6 | `seatp-6f` | bare | — |
| 7 | `seatp-6g` | bare | — |
| 8 | `seatp-6h` | bare | — |
| 9 | `seatp-6i` | bare | — |
| 10 | `seatp-6j` | bare | — |

#### Seat Platform Board 7 — 10 of 11 unclaimed

`wireframes/Seat Platform Board 7.dc.html` · pack · P08 · 1 screen claim on this board

| # | Anchor | State | Name |
|--:|---|---|---|
| 1 | `seatp-7a` | bare | — |
| 2 | `seatp-7b` | bare | — |
| 3 | `seatp-7c` | bare | — |
| 4 | `seatp-7d` | bare | — |
| 5 | `bo-026` | bare | — |
| 6 | `seatp-7f` | bare | — |
| 7 | `seatp-7g` | bare | — |
| 8 | `seatp-7h` | bare | — |
| 9 | `seatp-7i` | bare | — |
| 10 | `seatp-7j` | bare | — |

#### Seat Platform Board 8 — 10 of 10 unclaimed

`wireframes/Seat Platform Board 8.dc.html` · pack · no platform · nothing points at it

| # | Anchor | State | Name |
|--:|---|---|---|
| 1 | `seatp-8a` | bare | — |
| 2 | `seatp-8b` | bare | — |
| 3 | `seatp-8c` | bare | — |
| 4 | `seatp-8d` | bare | — |
| 5 | `seatp-8e` | bare | — |
| 6 | `seatp-8f` | bare | — |
| 7 | `seatp-8g` | bare | — |
| 8 | `seatp-8h` | bare | — |
| 9 | `seatp-8i` | bare | — |
| 10 | `seatp-8j` | bare | — |

#### Seat Platform Board 9 — 10 of 10 unclaimed

`wireframes/Seat Platform Board 9.dc.html` · pack · no platform · nothing points at it

| # | Anchor | State | Name |
|--:|---|---|---|
| 1 | `seatp-9a` | bare | — |
| 2 | `seatp-9b` | bare | — |
| 3 | `seatp-9c` | bare | — |
| 4 | `seatp-9d` | bare | — |
| 5 | `seatp-9e` | bare | — |
| 6 | `seatp-9f` | bare | — |
| 7 | `seatp-9g` | bare | — |
| 8 | `seatp-9h` | bare | — |
| 9 | `seatp-9i` | bare | — |
| 10 | `seatp-9j` | bare | — |

#### FnB Board 1 — 9 of 11 unclaimed

`wireframes/FnB Board 1.dc.html` · pack · P08 · 2 screen claims on this board

| # | Anchor | State | Name |
|--:|---|---|---|
| 1 | `fnb-1b` | bare | — |
| 2 | `fnb-1c` | bare | — |
| 3 | `fnb-1d` | bare | — |
| 4 | `fnb-1e` | bare | — |
| 5 | `fnb-1f` | bare | — |
| 6 | `fnb-1g` | bare | — |
| 7 | `bo-134` | bare | — |
| 8 | `bo-135` | bare | — |
| 9 | `fnb-1k` | bare | — |

#### Marketing Board 1 — 9 of 10 unclaimed

`wireframes/Marketing Board 1.dc.html` · pack · P08 · 1 screen claim on this board

| # | Anchor | State | Name |
|--:|---|---|---|
| 1 | `crm-1a` | bare | — |
| 2 | `crm-1c` | bare | — |
| 3 | `crm-1d` | bare | — |
| 4 | `crm-1e` | bare | — |
| 5 | `crm-1f` | bare | — |
| 6 | `crm-1g` | bare | — |
| 7 | `crm-1h` | bare | — |
| 8 | `crm-1i` | bare | — |
| 9 | `crm-1j` | bare | — |

#### Marketing Board 7 — 9 of 10 unclaimed

`wireframes/Marketing Board 7.dc.html` · pack · P13 · 1 screen claim on this board

| # | Anchor | State | Name |
|--:|---|---|---|
| 1 | `crm-7a` | bare | — |
| 2 | `crm-7b` | bare | — |
| 3 | `crm-7c` | bare | — |
| 4 | `crm-7d` | bare | — |
| 5 | `crm-7e` | bare | — |
| 6 | `crm-7g` | bare | — |
| 7 | `crm-7h` | bare | — |
| 8 | `crm-7i` | bare | — |
| 9 | `crm-7j` | bare | — |

#### P06 Venue Staff App — 9 of 66 unclaimed

`wireframes/P06 Venue Staff App.dc.html` · generated · P06 · 57 screen claims on this board

| # | Anchor | State | Name |
|--:|---|---|---|
| 1 | `emp-058` | named | Live Table & Service Management |
| 2 | `emp-059` | named | Table Order, Bill & Payment Management |
| 3 | `emp-060` | named | Reservation & Table Performance |
| 4 | `emp-061` | named | Retail Inventory Command Center |
| 5 | `emp-062` | named | Store Stock & SKU Availability |
| 6 | `emp-063` | named | Requisition & Smart Store Replenishment |
| 7 | `emp-064` | named | Store-to-Store & Warehouse Transfers |
| 8 | `emp-065` | named | Receiving & Store Put-Away |
| 9 | `emp-067` | named | Damage, Loss, Shrinkage & Stock Adjustment |

#### Retail Board 1 — 9 of 12 unclaimed

`wireframes/Retail Board 1.dc.html` · pack · P08 · 3 screen claims on this board

| # | Anchor | State | Name |
|--:|---|---|---|
| 1 | `bo-044` | bare | — |
| 2 | `ret-1c` | bare | — |
| 3 | `ret-1d` | bare | — |
| 4 | `ret-1e` | bare | — |
| 5 | `ret-1f` | bare | — |
| 6 | `ret-1g` | bare | — |
| 7 | `ret-1h` | bare | — |
| 8 | `bo-142` | bare | — |
| 9 | `bo-143` | bare | — |

#### P11 Accreditation — 8 of 8 unclaimed

`wireframes/P11 Accreditation.dc.html` · generated · no platform · nothing points at it

| # | Anchor | State | Name |
|--:|---|---|---|
| 1 | `acc-001` | bare | — |
| 2 | `acc-002` | bare | — |
| 3 | `acc-003` | bare | — |
| 4 | `acc-004` | bare | — |
| 5 | `acc-005` | bare | — |
| 6 | `acc-006` | bare | — |
| 7 | `acc-007` | bare | — |
| 8 | `acc-008` | bare | — |

#### P12 Support Console — 8 of 8 unclaimed

`wireframes/P12 Support Console.dc.html` · generated · no platform · nothing points at it

| # | Anchor | State | Name |
|--:|---|---|---|
| 1 | `sup-001` | bare | — |
| 2 | `sup-002` | bare | — |
| 3 | `sup-003` | bare | — |
| 4 | `sup-004` | bare | — |
| 5 | `sup-005` | bare | — |
| 6 | `sup-006` | bare | — |
| 7 | `sup-007` | bare | — |
| 8 | `sup-008` | bare | — |

#### Inventory Board 1 — 7 of 8 unclaimed

`wireframes/Inventory Board 1.dc.html` · pack · P06 · 1 screen claim on this board

| # | Anchor | State | Name |
|--:|---|---|---|
| 1 | `inv-2` | bare | — |
| 2 | `inv-3` | bare | — |
| 3 | `inv-4` | bare | — |
| 4 | `inv-5` | bare | — |
| 5 | `inv-7` | bare | — |
| 6 | `inv-8` | bare | — |
| 7 | `inv-9` | bare | — |

#### POS Board 1 — 6 of 10 unclaimed

`wireframes/POS Board 1.dc.html` · pack · P08 · 4 screen claims on this board

| # | Anchor | State | Name |
|--:|---|---|---|
| 1 | `bo-036` | bare | — |
| 2 | `pos-1b` | bare | — |
| 3 | `pos-1c` | bare | — |
| 4 | `bo-124` | bare | — |
| 5 | `bo-125` | bare | — |
| 6 | `bo-126` | bare | — |

#### POS Board 3 — 6 of 10 unclaimed

`wireframes/POS Board 3.dc.html` · pack · P04 · 4 screen claims on this board

| # | Anchor | State | Name |
|--:|---|---|---|
| 1 | `pos-009` | bare | — |
| 2 | `pos-018` | bare | — |
| 3 | `pos-019` | bare | — |
| 4 | `pos-3d` | bare | — |
| 5 | `pos-020` | bare | — |
| 6 | `pos-3f` | bare | — |

#### POS Board 4 — 6 of 11 unclaimed

`wireframes/POS Board 4.dc.html` · pack · P08 · 5 screen claims on this board

| # | Anchor | State | Name |
|--:|---|---|---|
| 1 | `bo-115` | bare | — |
| 2 | `bo-116` | bare | — |
| 3 | `bo-117` | bare | — |
| 4 | `bo-118` | bare | — |
| 5 | `bo-010` | bare | — |
| 6 | `pos-4f` | bare | — |

#### POS Board 5 — 6 of 11 unclaimed

`wireframes/POS Board 5.dc.html` · pack · P08 · 5 screen claims on this board

| # | Anchor | State | Name |
|--:|---|---|---|
| 1 | `bo-037` | bare | — |
| 2 | `bo-128` | bare | — |
| 3 | `pos-5c` | bare | — |
| 4 | `bo-129` | bare | — |
| 5 | `bo-130` | bare | — |
| 6 | `bo-133` | bare | — |

#### POS Board 6 — 6 of 6 unclaimed

`wireframes/POS Board 6.dc.html` · pack · no platform · nothing points at it

| # | Anchor | State | Name |
|--:|---|---|---|
| 1 | `pos-6a` | bare | — |
| 2 | `pos-6b` | bare | — |
| 3 | `pos-6c` | bare | — |
| 4 | `pos-6d` | bare | — |
| 5 | `pos-6e` | bare | — |
| 6 | `pos-6f` | bare | — |

#### TICVAI Boards — 6 of 8 unclaimed

`wireframes/TICVAI Boards v2.dc.html` · pack · P04 · 2 screen claims on this board

| # | Anchor | State | Name |
|--:|---|---|---|
| 1 | `pos-001` | bare | — |
| 2 | `pos-007` | bare | — |
| 3 | `ret-1a` | bare | — |
| 4 | `fnb-1a` | bare | — |
| 5 | `inv-1a` | bare | — |
| 6 | `inv-6` | bare | — |

#### Guest Mobile Board 1 — 5 of 6 unclaimed

`wireframes/Guest Mobile Board 1.dc.html` · pack · P02 · 1 screen claim on this board

| # | Anchor | State | Name |
|--:|---|---|---|
| 1 | `gm-1a` | bare | — |
| 2 | `gst-005` | bare | — |
| 3 | `gm-1c` | bare | — |
| 4 | `gm-1d` | bare | — |
| 5 | `gm-1e` | bare | — |

#### Guest Mobile Board 2 — 5 of 5 unclaimed

`wireframes/Guest Mobile Board 2.dc.html` · pack · no platform · nothing points at it

| # | Anchor | State | Name |
|--:|---|---|---|
| 1 | `gm-2a` | bare | — |
| 2 | `gm-2b` | bare | — |
| 3 | `gm-2c` | bare | — |
| 4 | `gm-2d` | bare | — |
| 5 | `gm-2e` | bare | — |

#### Guest Mobile Board 3 — 5 of 5 unclaimed

`wireframes/Guest Mobile Board 3.dc.html` · pack · no platform · nothing points at it

| # | Anchor | State | Name |
|--:|---|---|---|
| 1 | `gm-3a` | bare | — |
| 2 | `gm-3b` | bare | — |
| 3 | `gm-3c` | bare | — |
| 4 | `gm-3d` | bare | — |
| 5 | `gm-3e` | bare | — |

#### Guest Mobile Board 4 — 5 of 5 unclaimed

`wireframes/Guest Mobile Board 4.dc.html` · pack · no platform · nothing points at it

| # | Anchor | State | Name |
|--:|---|---|---|
| 1 | `gm-4a` | bare | — |
| 2 | `gm-4b` | bare | — |
| 3 | `gm-4c` | bare | — |
| 4 | `gm-4d` | bare | — |
| 5 | `gm-4e` | bare | — |

#### Guest Mobile Board 5 — 5 of 5 unclaimed

`wireframes/Guest Mobile Board 5.dc.html` · pack · no platform · nothing points at it

| # | Anchor | State | Name |
|--:|---|---|---|
| 1 | `gm-5a` | bare | — |
| 2 | `gm-5b` | bare | — |
| 3 | `gm-5c` | bare | — |
| 4 | `gm-5d` | bare | — |
| 5 | `gm-5e` | bare | — |

#### Guest Mobile Board 6 — 5 of 5 unclaimed

`wireframes/Guest Mobile Board 6.dc.html` · pack · no platform · nothing points at it

| # | Anchor | State | Name |
|--:|---|---|---|
| 1 | `gm-6a` | bare | — |
| 2 | `gm-6b` | bare | — |
| 3 | `gm-6c` | bare | — |
| 4 | `gm-6d` | bare | — |
| 5 | `gm-6e` | bare | — |

#### Guest Mobile Board 7 — 5 of 5 unclaimed

`wireframes/Guest Mobile Board 7.dc.html` · pack · no platform · nothing points at it

| # | Anchor | State | Name |
|--:|---|---|---|
| 1 | `gm-7a` | bare | — |
| 2 | `gm-7b` | bare | — |
| 3 | `gm-7c` | bare | — |
| 4 | `gm-7d` | bare | — |
| 5 | `gm-7e` | bare | — |

#### Guest Mobile Board 8 — 5 of 5 unclaimed

`wireframes/Guest Mobile Board 8.dc.html` · pack · no platform · nothing points at it

| # | Anchor | State | Name |
|--:|---|---|---|
| 1 | `gm-8a` | bare | — |
| 2 | `gm-8b` | bare | — |
| 3 | `gm-8c` | bare | — |
| 4 | `gm-8d` | bare | — |
| 5 | `gm-8e` | bare | — |

#### POS Frontline Board 2 — 4 of 7 unclaimed

`wireframes/POS Frontline Board 2.dc.html` · pack · P04 · 5 screen claims on this board

| # | Anchor | State | Name |
|--:|---|---|---|
| 1 | `pos-016` | bare | — |
| 2 | `pos-012` | bare | — |
| 3 | `pos-017` | bare | — |
| 4 | `pos-2e` | bare | — |

#### Seat Board 4 — 3 of 6 unclaimed

`wireframes/Seat Board 4.dc.html` · pack · P02, P06 · 3 screen claims on this board

| # | Anchor | State | Name |
|--:|---|---|---|
| 1 | `gst-049` | bare | — |
| 2 | `gst-021` | bare | — |
| 3 | `emp-030` | bare | — |

#### Seat Board 2 — 2 of 7 unclaimed

`wireframes/Seat Board 2.dc.html` · pack · P08 · 5 screen claims on this board

| # | Anchor | State | Name |
|--:|---|---|---|
| 1 | `bo-002` | bare | — |
| 2 | `bo-092` | bare | — |

#### Seat Board 3 — 2 of 6 unclaimed

`wireframes/Seat Board 3.dc.html` · pack · P01, P04, P10 · 4 screen claims on this board

| # | Anchor | State | Name |
|--:|---|---|---|
| 1 | `web-007` | bare | — |
| 2 | `web-039` | bare | — |

#### Seat Board 1 — 1 of 4 unclaimed

`wireframes/Seat Board 1.dc.html` · pack · P08 · 3 screen claims on this board

| # | Anchor | State | Name |
|--:|---|---|---|
| 1 | `bo-063` | bare | — |

---

## Part 3 — reconciliation, if your count differs

### Where the boards were found

| Folder on disk | Label | Boards | Frames | Unclaimed | Boards with unclaimed |
|---|---|--:|--:|--:|--:|
| `wireframes/` | Wireframes | 91 | 1362 | 811 | 74 |
| `designs/` | Design language | 2 | 0 | 0 | 0 |
| `ui-design/designs/` | Product design | 7 | 0 | 0 | 0 |
| | **Total** | **100** | **1362** | **811** | **74** |

Three directories, not two. A scan that reads only `wireframes/` and `designs/` misses
`ui-design/designs/`; a scan that reads only the first misses nine boards. Every frame in
this package happens to live in `wireframes/` — the other two folders hold single-artboard
boards with no `id` anchors at all — so a folder difference moves the **board** count
without moving the frame count.

### If your board count is not 100 — check the drop first

**35 of the 100 boards are not committed.** They are a local drop sitting in the
working tree, and any count taken from the repository will not see them:

| Committed | Boards | Frames | Unclaimed |
|---|--:|--:|--:|
| yes | 65 | 1052 | 523 |
| no — local only | 35 | 310 | 288 |
| | **100** | **1362** | **811** |

The local-only boards, by name — this is the list to check against your drop:

- **Guest Mobile Board** — 8 boards: Guest Mobile Board 1 (6 frames, 5 unclaimed), Guest Mobile Board 2 (5 frames, 5 unclaimed), Guest Mobile Board 3 (5 frames, 5 unclaimed), Guest Mobile Board 4 (5 frames, 5 unclaimed), Guest Mobile Board 5 (5 frames, 5 unclaimed), Guest Mobile Board 6 (5 frames, 5 unclaimed), Guest Mobile Board 7 (5 frames, 5 unclaimed), Guest Mobile Board 8 (5 frames, 5 unclaimed)
- **Kiosk Board** — 2 boards: Kiosk Board 1 (9 frames, 0 unclaimed), Kiosk Board 2 (8 frames, 0 unclaimed)
- **Marketing Board** — 12 boards: Marketing Board 1 (10 frames, 9 unclaimed), Marketing Board 2 (10 frames, 10 unclaimed), Marketing Board 3 (10 frames, 10 unclaimed), Marketing Board 4 (10 frames, 10 unclaimed), Marketing Board 5 (10 frames, 10 unclaimed), Marketing Board 6 (10 frames, 10 unclaimed), Marketing Board 7 (10 frames, 9 unclaimed), Marketing Board 8 (10 frames, 10 unclaimed), Marketing Board 9 (10 frames, 10 unclaimed), Marketing Board 10 (10 frames, 10 unclaimed), Marketing Board 11 (10 frames, 10 unclaimed), Marketing Board 12 (10 frames, 10 unclaimed)
- **Seat Platform Board** — 13 boards: Seat Platform Board 1 (10 frames, 10 unclaimed), Seat Platform Board 2 (10 frames, 10 unclaimed), Seat Platform Board 3 (10 frames, 10 unclaimed), Seat Platform Board 4 (10 frames, 10 unclaimed), Seat Platform Board 5 (10 frames, 10 unclaimed), Seat Platform Board 6 (10 frames, 10 unclaimed), Seat Platform Board 7 (11 frames, 10 unclaimed), Seat Platform Board 8 (10 frames, 10 unclaimed), Seat Platform Board 9 (10 frames, 10 unclaimed), Seat Platform Board 10 (10 frames, 10 unclaimed), Seat Platform Board 11 (10 frames, 10 unclaimed), Seat Platform Board 12 (10 frames, 10 unclaimed), Seat Platform Board 13 (11 frames, 10 unclaimed)

### 82 is `wireframes/manifest.json` — and the nine it does not list

The package writes its own account of the folder. It names 15 generated boards,
65 client packs and 3 indexes — **82 of them `.dc.html`**. That is the 82.

The folder holds 91. The 9 it does not account for are all pre-rename ghosts,
and they carry **227 of the 811 unclaimed frames**:

| Board | Frames | Unclaimed | Superseded by |
|---|--:|--:|---|
| P08 Staff Web Back Office | 73 | 73 | P08 Venue Management |
| P06 Staff App | 50 | 50 | P06 Venue Staff App |
| P09 Admin Web | 36 | 36 | P09 TICVAI Web |
| P13 White-Label CMS | 20 | 20 | P13 Venue CMS |
| P07 Staff Scanner | 16 | 16 | P07 Venue Scanner |
| P04 Staff POS | 10 | 10 | P04 Venue POS |
| P11 Accreditation | 8 | 8 | P11 Accreditation Web |
| P12 Support Console | 8 | 8 | P12 Venue Support |
| TICVAI Boards | 8 | 6 | the current index — this is `TICVAI Boards v2.dc.html`, a superseded one |

So the two counts are one count over two file sets, and **neither has an arithmetic bug**:
811 is every frame in the folder, 584 is every frame on a board the package
still claims. The ghosts are real files a consumer counting the folder will count, which is
why they are worth deleting rather than arguing about — `derive-wireframes.py` removes the
eight `P##` ones on its next run, and the ninth is a superseded index.

Two caveats on the 82, both checkable above: the manifest is generated, so it describes the
folder as of the last successful `derive-wireframes.py` run; and its `unrecognised` list read
empty while these nine sat on disk, because every one of them takes a shape the classifier
filtered out before it asked the question.

Every board count this tree can produce, under every scoping rule we could think of:

| Scoping rule | Boards |
|---|--:|
| every board, all three folders — what these numbers are | 100 |
| committed boards only | 65 |
| `wireframes/` only | 91 |
| `wireframes/` + `designs/`, missing the third folder | 93 |
| boards that actually carry frames | 89 |
| client packs + generated, dropping the index and the single artboards | 89 |
| client packs only, no generated boards | 66 |
| committed `wireframes/` only | 56 |
| boards something points at | 45 |

**None of these is 82** — that number comes from the manifest, not from a scoping rule over
the folder, which is the section above. If your count is none of these either, send the
filenames: the full table carries every name, byte count and mtime to diff against.

### What counts as a board

| Kind | Boards | Frames | Unclaimed | What it is |
|---|--:|--:|--:|---|
| pack | 66 | 649 | 526 | a client design pack, `<x-dc>` out of the design tool — does not title its own frames |
| generated | 23 | 713 | 285 | drawn by `tools/derive-wireframes.py` from the screen definitions — titles its own frames |
| single | 10 | 0 | 0 | one artboard, no `id` attributes — nothing to count, not an empty board |
| index | 1 | 0 | 0 | `TICVAI All Boards Index`, 255 links and no frames — a contents page, not an empty board |

`wireframes/` holds 91 `.dc.html` files at top level and every one of them is
counted here. The `screens/` subdirectory under it is one file per screen and is **not**
a board — counting those inflates the board count without adding frames.

### The de-duplication, which is the likeliest place for a bug

Raw `id="..."` matches across all boards: **1829**. After folding case and keeping
one frame per anchor: **1362**. The difference is 467.

65 of the 100 boards carry at least one anchor more than once — typically
`id="FNB-6A"` on the frame and `id="fnb-6a"` on the thumbnail that links to it. They are the
same frame. Counting both reports frames the package does not draw, and every figure derived
from it comes out high — 1829 against 1362 is 34%.

If your total is above ours, check this first. If it is below, check whether you are reading
all three folders and whether unwired boards — the 55 nothing points at — are in your scan;
a board nobody has wired up is still a board.

### What "claimed" means

A frame is claimed when a screen in `screens/` names it, through either `wireframe.board`
or `wireframe.generatedFallback`, and the anchor matches after the case fold. Claims are
551 of 1362. If your claimed count differs, the join is the thing to diff, not the frames.

