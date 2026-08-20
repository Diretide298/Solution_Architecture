# P04 Venue POS — platform

**Derived.** `python3 tools/derive-platform.py P04`. App `venue-pos` · venue · posTerminal · offline-capable

| | |
|---|---|
| Screens | 10 |
| Operations | 89 |
| Contracts | 11 |
| Modules | 4 |
| Undrawn | 0 |
| Operations with no screen | 138 |
| Waves | wave1 7 · wave2 3 |

## Gaps

### 138 operations with no screen here

**In a contract this platform uses, callable by its audience, and reaching no screen on any platform serving that audience.** Either a screen is missing or the endpoint should not exist — and the second is worth considering first.

| Operation | Contract | | |
|---|---|---|---|
| `createApprovalRequest` | approvals | POST | Raise a request |
| `assessProductChange` | catalogue | POST | What a change would touch, before making it |
| `bulkChangePrices` | catalogue | POST | Reprice a category or a whole catalogue |
| `cloneProduct` | catalogue | POST | Copy a product as a new draft |
| `commitCatalogueImport` | catalogue | POST | Apply a parsed catalogue import |
| `createDonationCampaign` | catalogue | POST | Create a campaign |
| `freezeEntitlement` | catalogue | POST | Pause a membership at the guest's request |
| `importProductCatalogue` | catalogue | POST | Parse a catalogue file into a preview |
| `joinWaitlist` | catalogue | POST | Ask to be told if capacity frees up |
| `leaveWaitlist` | catalogue | DELETE | Stop waiting |
| `listDonationCampaigns` | catalogue | GET | Campaigns a guest can give to |
| `listGuestMemberships` | catalogue | GET | A guest's memberships, benefits and history |
| `listProductVersions` | catalogue | GET | What this product used to be |
| `listWaitlistEntries` | catalogue | GET | Who is waiting for capacity |
| `offerWaitlistCapacity` | catalogue | POST | Tell a waiting guest that capacity appeared |
| `reinstateEntitlement` | catalogue | POST | Lift a suspension |
| `restoreProductVersion` | catalogue | POST | Put a previous version back |
| `suspendEntitlement` | catalogue | POST | Suspend or reinstate an entitlement |
| `updateDonationCampaign` | catalogue | PATCH | Amend or close a campaign |
| `calculateTax` | finance | POST | Compute tax for a set of lines |
| `disputeObligation` | finance | POST | One entity disagrees with the amount |
| `getUnifiedReconciliation` | finance | GET | Every money source against the ledger, in one view |
| `recordDeposit` | finance | POST | Money taken before the sale is complete |
| `recordSettlement` | finance | POST | One entity paid another |
| `recordWriteOff` | finance | POST | Write off an uncollectable balance |
| `resolveObligationDispute` | finance | POST | Agree what is actually owed |
| `settleDeposit` | finance | POST | Convert to revenue, return it, or forfeit it |
| `validateRecognitionSchedules` | finance | POST | Find product kinds claimed by more than one schedule |
| `adjustGameCard` | games | POST | Manually adjust credits or points |
| `createGame` | games | POST | Register a game |
| `createPrize` | games | POST | Add a prize |
| `listPrizes` | games | GET | The prize catalogue |
| `redeemPrize` | games | POST | Redeem points for a prize |
| `setReaderProfile` | games | PUT | How a reader behaves and what it shows |
| `transferGameCard` | games | POST | Move balances to another card |
| `captureStoredValue` | orders | POST | Take some or all of a held balance |
| `convertReservation` | orders | POST | Convert a reservation into an order |
| `convertToTermProduct` | orders | POST | Turn a visit into a membership or season pass |
| `createCart` | orders | POST | Start a cart |
| `createPaymentLink` | orders | POST | Send a guest a link to pay later |
| … | | | 98 more |

### 2 modules split across waves

**A platform that sells in one wave and cannot refund until a later one can take money and not give it back.** Not always wrong — worth a look each time.

- **Sell** — waves 1, 2
- **Shift** — waves 1, 2

## Modules

| Module | Screens | Waves |
|---|---|---|
| Sell | 5 | 1, 2 |
| Shift | 3 | 1, 2 |
| Payment | 1 | 1 |
| Reports | 1 | 2 |

## Screens

| | Name | Module | Wave | Ops | Drawn |
|---|---|---|---|---|---|
| `POS-001` | Begin Shift | Shift | 1 | 13 | yes |
| `POS-002` | Sell — Ticket Catalogue | Sell | 1 | 41 | yes |
| `POS-003` | Sell — Timed Entry | Sell | 1 | 16 | yes |
| `POS-004` | Sell — Seat Map | Sell | 2 | 12 | yes |
| `POS-005` | Payment | Payment | 1 | 10 | yes |
| `POS-006` | Held Orders | Sell | 1 | 14 | yes |
| `POS-007` | Close Shift | Shift | 1 | 13 | yes |
| `POS-008` | Reports | Reports | 2 | 9 | yes |
| `POS-009` | Staff Roster | Shift | 2 | 12 | yes |
| `POS-010` | Add to Existing Ticket | Sell | 1 | 3 | yes |

