# Validation rules

**194 refusal rules extracted from the contracts, plus 327 transition guards from the
state models — 521 testable rules.**

CF-24's artefact audit said 179 rules lived in contract prose and had never been extracted.
**They had been written; they had not been listed**, which is a different problem and a smaller
one — the rule is in the 409 description, and a test can be generated from it.

## Why this is a list and not a design

Every rule below already exists in a contract as the description of a refusal. **Extracting them
makes them testable**: each becomes a case that asserts the operation refuses, with that status,
for that reason.

A rule that lives only in prose is one a developer reads once and a test never checks.

| Contract | Rules |
|---|---|
| `orders` | 18 |
| `inventory` | 18 |
| `subscription` | 17 |
| `finance` | 13 |
| `fnb` | 13 |
| `catalogue` | 11 |
| `shift` | 10 |
| `promotions` | 9 |
| `identity` | 8 |
| `platform-ops` | 8 |
| `retail` | 8 |
| `cross-cell` | 7 |
| `maintenance` | 7 |
| `marketing-crm` | 7 |
| `seating` | 7 |
| `approvals` | 6 |
| `reporting` | 5 |
| `games` | 4 |
| `tenancy` | 3 |
| `ai` | 3 |
| `assets` | 3 |
| `white-label` | 3 |
| `access` | 2 |
| `queue` | 2 |
| `workforce` | 2 |
| **Total** | **194** |

## The rules that carry the most weight

Not the most numerous — the ones where the refusal is the control.

| Operation | Refuses when |
|---|---|
| `decideApprovalRequest` | Already decided, withdrawn or expired |
| `acquireLease` | No units remain, or the envelope is seated — seated inventory cannot be leased because a seat map is not a cou |
| `createSeatHold` | One or more seats are no longer available, or the selection breaks a seating rule. The response names the offe |
| `closeShift` | Shift already closed, or open orders remain |
| `createPayment` | Tender unavailable offline, or amount exceeds the balance due |
| `postStockCount` | Unreviewed variance lines remain, or approval is required |
| `closeFiscalPeriod` | Close checks failed — unapproved journals, unreconciled settlements, open shifts, or a prior period still open |
| `setApprovalMatrix` | The matrix would loosen a rule set at a higher scope, or a rule is unreachable behind an earlier one. |
| `createApprovalDelegation` | The delegate does not hold the permission being delegated |
| `promoteRelease` | Environment skipped, prior environment unhealthy, or the release has unapplied migrations in the target. |
| `verifyWorkOrder` | Verifier is the technician who completed the work |
| `publishSeatMap` | Validation failed. The response lists every finding |
| `commitImportJob` | Job has errors, or has already been committed |
| `createRefund` | Second authorisation required and absent, refund window closed, or the amount exceeds what remains refundable. |

## Full list

| Contract | Operation | Status | Refuses when |
|---|---|---|---|
| `access` | `overrideAccess` | 409 | The scan was not a denial, or has already been overridden |
| `access` | `validateGroupAccess` | 409 | Requested count exceeds the remaining group allowance |
| `ai` | `decideProposedAction` | 403 | The approver may not authorise this kind of action, or is the principal who prompted it. |
| `ai` | `generateVenueLayout` | 422 | The plan could not be interpreted. The reason is specific enough to act on |
| `ai` | `reindexSource` | 409 | Already rebuilding |
| `approvals` | `createApprovalDelegation` | 403 | The delegate does not hold the permission being delegated |
| `approvals` | `createApprovalRequest` | 409 | An open request already exists for this subject. Two approvals for one refund is how a refund gets paid twice. |
| `approvals` | `decideApprovalRequest` | 403 | The approver is the requester, lacks the permission, or is not in the resolved chain. |
| `approvals` | `decideApprovalRequest` | 409 | Already decided, withdrawn or expired |
| `approvals` | `setApprovalMatrix` | 409 | The matrix would loosen a rule set at a higher scope, or a rule is unreachable behind an earlier one. |
| `approvals` | `withdrawApprovalRequest` | 409 | Already decided |
| `assets` | `completeUpload` | 409 | Upload incomplete, checksum mismatch, or the file failed scanning |
| `assets` | `deleteMediaAsset` | 409 | Asset is in use. Every reference is listed |
| `assets` | `replaceMediaAsset` | 409 | Replacement is a different kind — an image cannot replace a document |
| `catalogue` | `acquireLease` | 409 | No units remain, or the envelope is seated — seated inventory cannot be leased because a seat map is not a count. |
| `catalogue` | `publishBundle` | 409 | A publish is already in progress for this venue |
| `catalogue` | `renewLease` | 409 | Lease already expired. Acquire a new one. |
| `catalogue` | `setAlternativeCodes` | 409 | Code already mapped to a different product for that partner |
| `catalogue` | `setChannelAllocations` | 409 | An allocation is below what that channel has already sold |
| `catalogue` | `setProductAttributes` | 409 | Regeneration would exceed the configured variant ceiling for this product. |
| `catalogue` | `transitionProductLifecycle` | 403 | Approval attempted by the principal who submitted it. Segregation applies here as it does to journals. |
| `catalogue` | `transitionProductLifecycle` | 409 | Transition not valid from the current state, or archiving attempted while unexpired entitlements exist. |
| `catalogue` | `updateEnvelope` | 409 | Capacity reduced below units already sold |
| `catalogue` | `updatePerformance` | 409 | Timing change attempted on a performance with sold tickets |
| `catalogue` | `updatePriceList` | 409 | Currency or scale change attempted after prices exist |
| `cross-cell` | `authoriseWalletSpend` | 409 | Guest link severed, or the wallet is suspended |
| `cross-cell` | `captureWalletAuthorisation` | 409 | Hold expired, already captured, or capture exceeds the hold |
| `cross-cell` | `consumeRedemptionRight` | 409 | Entries exhausted, or the right is revoked or outside its window |
| `cross-cell` | `createGuestLink` | 403 | Consent absent or expired |
| `cross-cell` | `createGuestLink` | 409 | The subject in the target cell is already linked to a different guest |
| `cross-cell` | `propagateRedemptionRight` | 409 | Right already propagated. Idempotent — returns the existing right. |
| `cross-cell` | `revokeRedemptionRight` | 409 | Already fully consumed. Revocation cannot undo a redemption that has happened — the guest was admitted. |
| `finance` | `abandonPeriodClose` | 409 | Not in a state that permits this |
| `finance` | `approveJournalEntry` | 403 | Approver is the poster, or lacks LEDGER_APPROVE |
| `finance` | `beginPeriodClose` | 409 | Not in a state that permits this |
| `finance` | `closeFiscalPeriod` | 409 | Close checks failed — unapproved journals, unreconciled settlements, open shifts, or a prior period still open. |
| `finance` | `createAccount` | 409 | Code already in use within this legal entity |
| `finance` | `createJournalEntry` | 409 | Fiscal period is closed |
| `finance` | `rejectJournal` | 409 | Not in a state that permits this |
| `finance` | `reopenPeriod` | 409 | Not in a state that permits this |
| `finance` | `reverseJournalEntry` | 409 | Already reversed, or the target period is closed |
| `finance` | `runFxRevaluation` | 409 | Period is not closing, or is already closed |
| `finance` | `runRecognition` | 409 | Period already closed, or a run is in progress |
| `finance` | `setFxRate` | 409 | Effective window overlaps an existing rate for the same pair and purpose |
| `finance` | `updateAccount` | 409 | Attempt to change an immutable field after entries exist |
| `fnb` | `acceptFnbOrder` | 409 | Already accepted, cancelled, or the outlet has stopped taking orders |
| `fnb` | `amendFnbOrder` | 409 | A targeted line is already preparing or served |
| `fnb` | `cancelFnbOrder` | 409 | Already served, collected or delivered — cancel is no longer the operation |
| `fnb` | `claimLocationSession` | 409 | Code expired or unknown, the location is out of service, or no outlet currently delivers to it — a cabana is useless as  |
| `fnb` | `claimTableSession` | 409 | Code expired or unknown, the outlet is closed, or the table is out of service. |
| `fnb` | `closeTableVisit` | 409 | Payments do not cover the bill, or lines remain unserved |
| `fnb` | `createFnbOrder` | 409 | An item is unavailable, modifier constraints are unmet, or a tracked item was ordered offline. |
| `fnb` | `createGuestFnbOrder` | 409 | An item became unavailable, the quoted total no longer matches, the table session expired, or the outlet stopped taking  |
| `fnb` | `mergeTableVisits` | 409 | Either visit is already closed |
| `fnb` | `openTableVisit` | 409 | Table already occupied |
| `fnb` | `recordOrderHandover` | 409 | Order is not ready, or already closed |
| `fnb` | `splitBill` | 409 | Visit already settled |
| `fnb` | `updateTableVisit` | 409 | Target table is occupied |
| `games` | `issueGameCard` | 409 | Card already active, or the code is unknown |
| `games` | `recordGamePlay` | 409 | Insufficient credits, card blocked, or the game is out of service. |
| `games` | `redeemPrize` | 409 | Insufficient points, or a prize is out of stock |
| `games` | `transferGameCard` | 409 | Target already carries a balance, or either card is blocked |
| `identity` | `completeSsoAuthorization` | 403 | Authenticated, but no group maps to a role in this tenant. The provider proved who they are; it did not grant them anyth |
| `identity` | `createPrincipal` | 409 | Username already in use within this cell |
| `identity` | `deleteGuestAccount` | 409 | Open orders or an unexpired entitlement exist. Deleting an account with a valid ticket in it strands the guest at a gate |
| `identity` | `linkGuestCheckout` | 403 | Contact detail on the order does not match the verified identifier |
| `identity` | `login` | 409 | An active session already exists for this principal on another device. Per §3.1.3 the new login is refused. A supervisor |
| `identity` | `registerGuest` | 409 | Identifier already registered. Deliberately indistinguishable in timing from success — a registration endpoint that reve |
| `identity` | `removeMfaMethod` | 409 | Last remaining method on a role that requires MFA |
| `identity` | `revokeAllSessions` | 403 | Step-up token missing, expired or issued for a different action |
| `inventory` | `acknowledgePurchaseOrder` | 409 | Not in a state that permits this |
| `inventory` | `cancelRequisition` | 409 | Not in a state that permits this |
| `inventory` | `cancelStockCount` | 409 | Not in a state that permits this |
| `inventory` | `closePurchaseOrderShort` | 409 | Not in a state that permits this |
| `inventory` | `closeTransferShort` | 409 | Not in a state that permits this |
| `inventory` | `createGoodsReceipt` | 409 | Over-receipt beyond tolerance, or the purchase order is closed |
| `inventory` | `createInventoryItem` | 409 | SKU already in use in this venue |
| `inventory` | `createPurchaseOrder` | 409 | Requisition is not approved, or the quotation does not match it |
| `inventory` | `createStockMovement` | 409 | Insufficient stock, and the item does not permit negative balances |
| `inventory` | `createStockTransfer` | 409 | Insufficient stock at the source |
| `inventory` | `getCountVariance` | 409 | Count is still open. Variance is not available during counting |
| `inventory` | `postStockCount` | 409 | Unreviewed variance lines remain, or approval is required |
| `inventory` | `recountStockCount` | 409 | Not in a state that permits this |
| `inventory` | `rejectRequisition` | 409 | Not in a state that permits this |
| `inventory` | `returnRequisition` | 409 | Not in a state that permits this |
| `inventory` | `sendPurchaseOrder` | 409 | Not in a state that permits this |
| `inventory` | `startStockCount` | 409 | A count is already open for this location |
| `inventory` | `updateInventoryItem` | 409 | Attempt to change costing method or base unit after movements exist |
| `maintenance` | `acceptWorkOrder` | 409 | Not assigned to this principal, or already accepted |
| `maintenance` | `cancelWorkOrder` | 409 | Work has started. Complete or abandon it instead |
| `maintenance` | `createAsset` | 409 | Asset tag already in use |
| `maintenance` | `recordWorkOrderParts` | 409 | Insufficient stock |
| `maintenance` | `recordWorkOrderTime` | 409 | Action inconsistent with the current timer state |
| `maintenance` | `setAssetStatus` | 409 | Return to service attempted without the inspection this asset category requires. |
| `maintenance` | `verifyWorkOrder` | 403 | Verifier is the technician who completed the work |
| `marketing-crm` | `launchCampaign` | 409 | Already launched, audience size differs beyond tolerance, or every recipient was excluded. |
| `marketing-crm` | `mergeGuestProfiles` | 409 | Either profile is already merged, or they are the same profile |
| `marketing-crm` | `pauseCampaign` | 409 | Not in a state that permits this |
| `marketing-crm` | `reopenCase` | 409 | Not in a state that permits this |
| `marketing-crm` | `sendTransactionalMessage` | 409 | Address suppressed, or the guest has no address for that channel |
| `marketing-crm` | `unscheduleCampaign` | 409 | Not in a state that permits this |
| `marketing-crm` | `updateCampaign` | 409 | Content or audience amended on a live campaign |
| `orders` | `addTip` | 409 | Payment not settled, or a tip is already recorded against it |
| `orders` | `appendEntitlementToMedia` | 409 | Media expired, blocked, already surrendered at exit, or the entitlement cannot share media — a single-entry ticket surre |
| `orders` | `applyManualDiscount` | 403 | Above the cashier's limit and no approver supplied, or the approver is the requester. |
| `orders` | `cancelReservation` | 409 | Already converted |
| `orders` | `convertReservation` | 409 | Expired or already converted |
| `orders` | `createOrder` | 409 | A lease covering a line has expired, capacity is exhausted, or the catalogue bundle the client priced from is beyond its |
| `orders` | `createPayment` | 409 | Tender unavailable offline, or amount exceeds the balance due |
| `orders` | `createRefund` | 409 | Second authorisation required and absent, refund window closed, or the amount exceeds what remains refundable. The probl |
| `orders` | `createRefundRequest` | 403 | Order does not belong to the authenticated subject |
| `orders` | `createReservation` | 409 | Capacity unavailable |
| `orders` | `exchangeOrderLines` | 409 | Replacement unavailable, outside the exchange window, or the original is redeemed. |
| `orders` | `extendReservation` | 409 | Expired, or the extension limit is reached |
| `orders` | `holdOrder` | 409 | Order is already paid, voided, or contains a seat hold about to expire |
| `orders` | `modifyOrder` | 409 | A targeted line's entitlement has been redeemed, or the order is voided. |
| `orders` | `rescheduleOrder` | 409 | Target performance is unavailable or outside the reschedule window |
| `orders` | `resumeOrder` | 409 | Held order expired, or already resumed at another till |
| `orders` | `transferOrderTickets` | 409 | Ticket already redeemed, already offered, or the product forbids transfer. |
| `orders` | `voidOrder` | 409 | Settled, or from a closed shift. Use a refund. |
| `platform-ops` | `applyMigration` | 409 | The plan is stale — cell state changed since it was computed. Re-plan and review before applying. |
| `platform-ops` | `promoteRelease` | 403 | Approver is the requester, or the step-up token is absent or expired |
| `platform-ops` | `promoteRelease` | 409 | Environment skipped, prior environment unhealthy, or the release has unapplied migrations in the target. |
| `platform-ops` | `rejectRelease` | 409 | Not in a state that permits this |
| `platform-ops` | `rollbackMigrationRun` | 409 | A migration in this run is irreversible |
| `platform-ops` | `rollbackRollout` | 409 | A migration in this release is irreversible. The response names it — a one-way door should be identified, not discovered |
| `platform-ops` | `startRollout` | 409 | Not in a state that permits this |
| `platform-ops` | `withdrawRelease` | 409 | Not in a state that permits this |
| `promotions` | `assignCoupon` | 409 | Not in a state that permits this |
| `promotions` | `endPromotion` | 409 | Not in a state that permits this |
| `promotions` | `pausePromotion` | 409 | Not in a state that permits this |
| `promotions` | `publishPromotion` | 409 | Conflict analysis failed. The response names each conflicting promotion |
| `promotions` | `redeemVoucher` | 409 | Expired, already fully redeemed, or amount exceeds the balance |
| `promotions` | `unschedulePromotion` | 409 | Not in a state that permits this |
| `promotions` | `updateBundle` | 409 | Structural change attempted after the bundle has been sold |
| `promotions` | `updatePromotion` | 409 | Conditions or discount amended on a live promotion |
| `promotions` | `voidCouponCode` | 409 | Already redeemed. A redeemed code cannot be voided |
| `queue` | `joinQueue` | 409 | Already in this queue, at the cross-queue limit, party exceeds the maximum, queue is paused or closed, or a party member |
| `queue` | `leaveQueue` | 409 | Already called or redeemed |
| `reporting` | `cancelReportExecution` | 409 | Already completed |
| `reporting` | `createReport` | 403 | Author does not hold the permission they assigned to the report |
| `reporting` | `deleteReport` | 409 | Active schedules reference this report |
| `reporting` | `exportReportResult` | 403 | Personal data requested without REPORT_EXPORT_PII |
| `reporting` | `getReportResult` | 409 | Execution has not completed |
| `retail` | `collectShopAndDrop` | 409 | Already collected, or past the collection deadline |
| `retail` | `createMerchandise` | 409 | Barcode already in use in this venue |
| `retail` | `createRetailExchange` | 409 | Replacement out of stock, or the original is not exchangeable |
| `retail` | `createRetailReturn` | 409 | Outside the return window, item is non-returnable, already returned, or a second authoriser is required. The response na |
| `retail` | `createRetailSale` | 409 | Insufficient stock, a serialised item has no serial number, or the terminal is offline. |
| `retail` | `createShopAndDrop` | 409 | Sale already dropped, an item is non-droppable — chilled, fragile, oversized — or the collection point is closed before  |
| `retail` | `issueGiftCard` | 409 | Card already activated, or the code is unknown |
| `retail` | `reserveMerchandise` | 409 | Insufficient stock |
| `seating` | `commitImportJob` | 409 | Job has errors, or has already been committed |
| `seating` | `createSeatBlock` | 409 | One or more seats already sold. Sold seats cannot be blocked |
| `seating` | `createSeatHold` | 409 | One or more seats are no longer available, or the selection breaks a seating rule. The response names the offending seat |
| `seating` | `extendSeatHold` | 409 | Already expired, or the extension limit is reached |
| `seating` | `publishSeatMap` | 409 | Validation failed. The response lists every finding |
| `seating` | `updateSeatMap` | 409 | Structural change attempted on a published map |
| `seating` | `updateSeats` | 409 | Map is published and the change is structural |
| `shift` | `approveShiftOpen` | 409 | Shift is not awaiting approval |
| `shift` | `closeShift` | 409 | Shift already closed, or open orders remain |
| `shift` | `createCashMovement` | 409 | Shift is not open, or the lift exceeds the counted float |
| `shift` | `openShift` | 409 | A shift is already open on this workstation, or a required device is absent. |
| `shift` | `recordNoSale` | 409 | Shift is not open |
| `shift` | `reopenShift` | 403 | Approver is the closing principal |
| `shift` | `reopenShift` | 409 | Shift is not closed, or the fiscal period has closed over it |
| `shift` | `resumeShift` | 403 | Not the principal who suspended it, and the caller does not hold SHIFT_CLOSE_OTHER. |
| `shift` | `resumeShift` | 409 | Another shift is now open on this workstation |
| `shift` | `suspendShift` | 409 | Shift is not in a suspendable state |
| `subscription` | `cancelDecommission` | 409 | Not in a state that permits this |
| `subscription` | `cancelInvoice` | 409 | Not in a state that permits this |
| `subscription` | `createTenant` | 409 | Code already in use |
| `subscription` | `decommissionCell` | 409 | Not in a state that permits this |
| `subscription` | `disputeInvoice` | 409 | Not in a state that permits this |
| `subscription` | `executeTenantMigration` | 409 | Plan stale, or the tenant has traded since it was computed |
| `subscription` | `generateInvoice` | 409 | An invoice already exists for this period |
| `subscription` | `launchCellCluster` | 409 | The model cell is mid-migration. Replicating a cell whose schema is moving produces a cluster at neither version. |
| `subscription` | `planTenantMigration` | 409 | Region mismatch, schema versions differ, or the tenant has open shifts. A tenant mid-trade cannot be moved — a cutover d |
| `subscription` | `provisionCell` | 409 | A cell already exists for this region |
| `subscription` | `reactivateTenant` | 409 | Tenant is terminated, not suspended. Termination is not reversible here |
| `subscription` | `recordInvoicePayment` | 409 | Not in a state that permits this |
| `subscription` | `removeLicenceAddOn` | 409 | Module is currently enabled by the tenant. Disable it there first |
| `subscription` | `resolveInvoiceDispute` | 409 | Not in a state that permits this |
| `subscription` | `rollbackTenantMigration` | 409 | Not in a state that permits this |
| `subscription` | `setSubscription` | 409 | Downgrade conflicts with current usage. The response names every module and limit that would be violated. |
| `subscription` | `terminateTenant` | 409 | Unsettled ledger balances exist |
| `tenancy` | `createOutlet` | 409 | Code already in use in this venue |
| `tenancy` | `registerDevice` | 409 | Identifier already bound to another workstation |
| `tenancy` | `updateRegionSettings` | 409 | Currency or scale change rejected because transactions exist in this region. |
| `white-label` | `createContentPage` | 409 | Slug already in use |
| `white-label` | `deleteContentPage` | 409 | Page is referenced by navigation or the homepage |
| `white-label` | `publishTenantConfig` | 409 | Validation failed. Every finding is listed |
| `workforce` | `createRotaAssignment` | 409 | Overlaps an existing assignment, or the person lacks the required role |
| `workforce` | `recordAttendance` | 409 | Out of sequence — a clock-out with no clock-in, or a second clock-in. **Reported rather than silently corrected.** |

## What this does not cover

**Field-level validation** — lengths, patterns, ranges — is in the schemas as `maxLength`,
`pattern` and `minimum`, and is enforced by the OpenAPI layer rather than by a rule. It needs
no register because a generated client already carries it.

**Business rules with no refusal.** A rule that changes behaviour rather than blocking it —
proportional allocation on a dynamic bundle (ADR-0019), scope resolution up the tree
(ADR-0018) — lives in an ADR, and the ADR is the test specification.

**The 40 test/acceptance requirements** are a separate artefact class. This register is the
input to them, not a replacement.
