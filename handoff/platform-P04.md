# P04 Venue POS — platform

**Derived.** `python3 tools/derive-platform.py P04`. App `venue-pos` · venue · posTerminal · offline-capable

| | |
|---|---|
| Screens | 10 |
| Operations | 98 |
| Contracts | 11 |
| Modules | 6 |
| Undrawn | 0 |
| Operations with no screen | 91 |
| Waves | wave1 7 · wave2 3 |

## Gaps

### 91 operations with no screen here

**In a contract this platform uses, callable by its audience, and reaching no screen on any platform serving that audience.** Either a screen is missing or the endpoint should not exist — and the second is worth considering first.

| Operation | Contract | | |
|---|---|---|---|
| `createApprovalRequest` | approvals | POST | Raise a request |
| `createDonationCampaign` | catalogue | POST | Create a campaign |
| `joinWaitlist` | catalogue | POST | Ask to be told if capacity frees up |
| `leaveWaitlist` | catalogue | DELETE | Stop waiting |
| `listDonationCampaigns` | catalogue | GET | Campaigns a guest can give to |
| `listWaitlistEntries` | catalogue | GET | Who is waiting for capacity |
| `offerWaitlistCapacity` | catalogue | POST | Tell a waiting guest that capacity appeared |
| `suspendEntitlement` | catalogue | POST | Suspend or reinstate an entitlement |
| `updateDonationCampaign` | catalogue | PATCH | Amend or close a campaign |
| `calculateTax` | finance | POST | Compute tax for a set of lines |
| `disputeObligation` | finance | POST | One entity disagrees with the amount |
| `recordSettlement` | finance | POST | One entity paid another |
| `resolveObligationDispute` | finance | POST | Agree what is actually owed |
| `adjustGameCard` | games | POST | Manually adjust credits or points |
| `createGame` | games | POST | Register a game |
| `createPrize` | games | POST | Add a prize |
| `listPrizes` | games | GET | The prize catalogue |
| `redeemPrize` | games | POST | Redeem points for a prize |
| `transferGameCard` | games | POST | Move balances to another card |
| `convertReservation` | orders | POST | Convert a reservation into an order |
| `createCart` | orders | POST | Start a cart |
| `createReservation` | orders | POST | Hold without payment |
| `extendReservation` | orders | POST | Extend a reservation |
| `listAbandonedCarts` | orders | GET | Carts that lapsed without checking out |
| `voidPayment` | orders | POST | Release an authorisation before it is captured |
| `assignCoupon` | promotions | POST | Assign a coupon to a named guest |
| `createBundle` | promotions | POST | Create a bundle |
| `createUpsellRule` | promotions | POST | Create an upsell rule |
| `createVoucherBatch` | promotions | POST | Issue a voucher batch |
| `deleteUpsellRule` | promotions | DELETE | Remove an upsell rule |
| `listAllocationSplits` | promotions | GET | List allocation split definitions |
| `listBundles` | promotions | GET | List bundles |
| `listUpsellRules` | promotions | GET | List upsell and cross-sell rules |
| `listVoucherBatches` | promotions | GET | List voucher batches |
| `previewAllocationSplit` | promotions | POST | Preview how an amount divides |
| `redeemVoucher` | promotions | POST | Redeem voucher value against an order |
| `updateBundle` | promotions | PATCH | Amend a bundle |
| `voidCouponCode` | promotions | POST | Void a code |
| `voidVoucher` | promotions | POST | Cancel a voucher |
| `cancelReportExecution` | reporting | DELETE | Cancel a running execution |
| … | | | 51 more |

### 1 modules split across waves

**A platform that sells in one wave and cannot refund until a later one can take money and not give it back.** Not always wrong — worth a look each time.

- **shift** — waves 1, 2

## Modules

| Module | Screens | Waves |
|---|---|---|
| shift | 3 | 1, 2 |
| orders | 3 | 1 |
| catalogue | 1 | 1 |
| seating | 1 | 2 |
| reporting | 1 | 2 |
| assets | 1 | 1 |

## Screens

| | Name | Module | Wave | Ops | Drawn |
|---|---|---|---|---|---|
| `POS-001` | Begin Shift | shift | 1 | 13 | yes |
| `POS-002` | Sell — Ticket Catalogue | orders | 1 | 41 | yes |
| `POS-003` | Sell — Timed Entry | catalogue | 1 | 16 | yes |
| `POS-004` | Sell — Seat Map | seating | 2 | 12 | yes |
| `POS-005` | Payment | orders | 1 | 10 | yes |
| `POS-006` | Held Orders | orders | 1 | 14 | yes |
| `POS-007` | Close Shift | shift | 1 | 13 | yes |
| `POS-008` | Reports | reporting | 2 | 9 | yes |
| `POS-009` | Staff Roster | shift | 2 | 12 | yes |
| `POS-010` | Add to Existing Ticket | assets | 1 | 12 | yes |

