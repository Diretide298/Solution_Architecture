# P04 Venue POS — platform

**Derived.** `python3 tools/derive-platform.py P04`. App `venue-pos` · venue · posTerminal · offline-capable

| | |
|---|---|
| Screens | 24 |
| Operations | 118 |
| Contracts | 18 |
| Modules | 4 |
| Undrawn | 0 |
| Operations with no screen | 186 |
| Waves | wave1 21 · wave2 3 |

## Gaps

### 186 operations with no screen here

**In a contract this platform uses, callable by its audience, and reaching no screen on any platform serving that audience.** Either a screen is missing or the endpoint should not exist — and the second is worth considering first.

| Operation | Contract | | |
|---|---|---|---|
| `enrolFacePass` | access | POST | Register a facial profile against an entitlement |
| `getFacePassEnrolment` | access | GET | Whether a pass has a face registered, and when |
| `revokeFacePass` | access | DELETE | Remove a facial profile |
| `assessProductChange` | catalogue | POST | What a change would touch, before making it |
| `bulkChangePrices` | catalogue | POST | Reprice a category or a whole catalogue |
| `cloneProduct` | catalogue | POST | Copy a product as a new draft |
| `commitCatalogueImport` | catalogue | POST | Apply a parsed catalogue import |
| `createDonationCampaign` | catalogue | POST | Create a campaign |
| `freezeEntitlement` | catalogue | POST | Pause a membership at the guest's request |
| `listDonationCampaigns` | catalogue | GET | Campaigns a guest can give to |
| `listProductVersions` | catalogue | GET | What this product used to be |
| `listWaitlistEntries` | catalogue | GET | Who is waiting for capacity |
| `offerWaitlistCapacity` | catalogue | POST | Tell a waiting guest that capacity appeared |
| `reinstateEntitlement` | catalogue | POST | Lift a suspension |
| `restoreProductVersion` | catalogue | POST | Put a previous version back |
| `suspendEntitlement` | catalogue | POST | Suspend or reinstate an entitlement |
| `updateDonationCampaign` | catalogue | PATCH | Amend or close a campaign |
| `calculateTax` | finance | POST | Compute tax for a set of lines |
| `disputeObligation` | finance | POST | One entity disagrees with the amount |
| `getForeignTenderReport` | finance | GET | What was taken in which currency |
| `getUnifiedReconciliation` | finance | GET | Every money source against the ledger, in one view |
| `listInterEntityObligations` | finance | GET | What one entity owes another |
| `recordDeposit` | finance | POST | Money taken before the sale is complete |
| `recordSettlement` | finance | POST | One entity paid another |
| `recordWriteOff` | finance | POST | Write off an uncollectable balance |
| `resolveObligationDispute` | finance | POST | Agree what is actually owed |
| `runFxRevaluation` | finance | POST | Revalue monetary balances at close |
| `validateRecognitionSchedules` | finance | POST | Find product kinds claimed by more than one schedule |
| `attachModifierGroup` | fnb | PUT | Give an item its choices |
| `clearTable` | fnb | POST | Mark a table cleared and free |
| `closeCorrectiveAction` | fnb | POST | Close a signed finding |
| `createCombo` | fnb | POST | A meal deal, priced as one thing |
| `createModifierGroup` | fnb | POST | Create a modifier group |
| `createTable` | fnb | POST | A table as a thing, not an inference |
| `escalateCorrectiveAction` | fnb | POST | Escalate a finding |
| `getTableVisit` | fnb | GET | Read a visit with all its orders |
| `rebalanceStationLoad` | fnb | POST | Move work between stations mid-service |
| `recordCorrectiveAction` | fnb | POST | Record what was done about a finding |
| `requestBill` | fnb | POST | The party asked to pay |
| `resolveBookingConflict` | fnb | GET | Two bookings, one table — and what to do about it |
| … | | | 146 more |

### 2 modules split across waves

**A platform that sells in one wave and cannot refund until a later one can take money and not give it back.** Not always wrong — worth a look each time.

- **Sell** — waves 1, 2
- **Shift** — waves 1, 2

## Modules

| Module | Screens | Waves |
|---|---|---|
| Sell | 19 | 1, 2 |
| Shift | 3 | 1, 2 |
| Payment | 1 | 1 |
| Reports | 1 | 2 |

## Screens

| | Name | Module | Wave | Ops | Drawn |
|---|---|---|---|---|---|
| `POS-001` | Begin Shift | Shift | 1 | 17 | yes |
| `POS-002` | Sell — Ticket Catalogue | Sell | 1 | 41 | yes |
| `POS-003` | Sell — Timed Entry | Sell | 1 | 10 | yes |
| `POS-004` | Sell — Seat Map | Sell | 2 | 11 | yes |
| `POS-005` | Payment | Payment | 1 | 11 | yes |
| `POS-006` | Held Orders | Sell | 1 | 14 | yes |
| `POS-007` | Close Shift | Shift | 1 | 17 | yes |
| `POS-008` | Reports | Reports | 2 | 7 | yes |
| `POS-009` | Staff Roster | Shift | 2 | 16 | yes |
| `POS-010` | Add to Existing Ticket | Sell | 1 | 5 | yes |
| `POS-011` | Returns, Refunds & Exchanges | Sell | 1 | 9 | yes |
| `POS-012` | Omnichannel Order & Fulfilment Center | Sell | 1 | 7 | yes |
| `POS-013` | Mobile POS, Event Sales & Offline Operations | Sell | 1 | 8 | yes |
| `POS-014` | Sales Exceptions, Controls & Operational Actions | Sell | 1 | 3 | yes |
| `POS-015` | Cash Operations Dashboard | Sell | 1 | 2 | yes |
| `POS-016` | Till Configuration | Sell | 1 | 2 | yes |
| `POS-017` | Cash In / Cash Out Operations | Sell | 1 | 1 | yes |
| `POS-018` | Safe Drop & Cash Transfer Management | Sell | 1 | 5 | yes |
| `POS-019` | Shift Templates & Policies | Sell | 1 | 3 | yes |
| `POS-020` | Shift Exceptions & Alerts | Sell | 1 | 5 | yes |
| `POS-021` | Sell — Food & Drink | Sell | 1 | 6 | yes |
| `POS-022` | Send to Kitchen | Sell | 1 | 4 | yes |
| `POS-023` | Sell — Merchandise | Sell | 1 | 5 | yes |
| `POS-024` | Outlet Setup | Sell | 1 | 5 | yes |

