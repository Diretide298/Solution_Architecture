# Screen and contract linkage

**143 of 642 operations reach a defined screen.** 499 do not.

Derived both directions by `tools/link-screens-contracts.py`: `x-ticvai-consumed-by` on each
operation, and validated operation ids on each screen.

## What the gap means now

It used to mean missing screens. **All 347 screens now exist**, so it no longer does — it means
screens that name no operation. 203 of 347 declare none, and every one of those is a screen
somebody can draw and nobody can build.

| | |
|---|---|
| Operations reaching a screen | 143 |
| Operations reaching none | 499 |
| Screens declaring an operation | 144 of 347 |

## Operations no screen calls

Not all are defects. Sync endpoints, webhooks and service-to-service calls legitimately have
no screen. The ones worth checking are the rest.

```
abandonPeriodClose, acceptFnbOrder, acknowledgePurchaseOrder, addBlacklistEntry, addLicenceAddOn, addSuppression
adjustGameCard, adjustLoyaltyPoints, adjustWallet, amendFnbOrder, analysePromotionConflicts, approveJournalEntry
approveRefund, approveRequisition, approveShiftOpen, askReportingQuestion, assignCoupon, authoriseWalletSpend
beginPeriodClose, blockGiftCard, calculateTax, cancelDecommission, cancelFnbOrder, cancelPerformance
cancelPurchaseOrder, cancelReportExecution, cancelReservation, cancelStockCount, cancelWorkOrder, capturePayment
captureWalletAuthorisation, claimTableSession, claimTicketTransfer, clearTable, cloneSeatMap, closeFiscalPeriod
closePurchaseOrderShort, closeTableVisit, collectShopAndDrop, commitImportJob, compareQuotations, completeSsoAuthorization
completeUpload, configureWorkstation, consumeRedemptionRight, convertReservation, copyPriceList, createAccessPoint
createAccount, createAdmissionProfile, createAsset, createBanner, createBulkRefund, createBundle
createCampaign, createCashMovement, createCollection, createContentPage, createCostCenter, createCouponCampaign
createDashboard, createDsarRequest, createEntitlementTemplate, createEnvelope, createEvent, createFnbOrder
createGame, createGoodsReceipt, createGuestLink, createInspectionTemplate, createInventoryItem, createJournalEntry
createLegalEntity, createLoyaltyProgramme, createMaintenancePlan, createMenu, createMerchandise, createMessageTemplate
createMfaChallenge, createModifierGroup, createOutlet, createPerformances, createPlan, createPlanVersion
createPreview, createPriceList, createPrincipal, createPrize, createProduct, createPromoBlock
createPromotion, createPurchaseOrder, createRecognitionSchedule, createRefund, createRefundRequest, createRelease
createReport, createReportSchedule, createRequisition, createReservation, createRetailExchange, createRetailReturn
createRetailSale, createSaleBoard, createScopeNode, createSeatBlock, createSeatCategory, createSeatMap
createSeatMapTemplate, createSegment, createShopAndDrop, createStockLocation, createStockMovement, createStockTransfer
createSupplier, createTaxCode, createTaxExemption, createTenant, createUpload, createUpsellRule
createVoucherBatch, createWorkOrder, decommissionCell, deleteBanner, deleteContentPage, deleteGrant
deleteGuestAccount, deleteMediaAsset, deleteReport, deleteReportSchedule, deleteUpsellRule, diffConfigVersion
endPromotion, enrolMfaMethod, exchangeOrderLines, executeTenantMigration, exportReportResult, extendReservation
forceLogout, forceReleaseLease, generateCouponCodes, generateInvoice, getAccessPoint, getAccount
getAppIcons, getAsset, getAssetHistory, getBill, getBrandIdentity, getCampaign
getCampaignPerformance, getCell, getCellCapacity, getConsentHistory, getCountVariance, getCurrentSession
getDashboard, getDeferredRevenue, getDsarRequest, getDueMaintenance, getExpiringRights, getFinancialReport
getFnbOrder, getFonts, getForeignTenderReport, getGameCard, getGuestConsents, getGuestLink
getGuestSession, getHomepageLayout, getImportJob, getInventoryItem, getJournalEntry, getLatestBundle
getMediaAsset, getMenu, getMessageStatus, getMigrationRun, getModuleEnablement, getNavigation
```

…and 319 more.
