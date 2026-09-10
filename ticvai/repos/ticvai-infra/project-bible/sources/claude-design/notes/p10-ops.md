# P10 remaining screens — operations and contracts (from screens/P10-partner-reseller-portal.yaml)

Drawn already: PTR-001, 003, 004, 019, 020.

ORDER-SET = createOrder, listOrders, getOrder, getOrderStatement, applyManualDiscount,
exchangeOrderLines, holdOrder, resumeOrder, modifyOrder, rescheduleOrder, reprintOrder,
voidOrder, listOrderRefunds — all `contract: orders`.

- PTR-002 Partner Dashboard (Overview, w2, 16): ORDER-SET + getB2bCredit, overrideCreditLimit,
  setB2bCreditLimit. (no createRefund)
- PTR-005 Inventory & Allocation View (Inventory, w2, 19): catalogue = getChannelAllocations,
  setChannelAllocations, createChannelCapacity, listChannelCapacities, updateChannelCapacity,
  releaseChannelAllocation; plus ORDER-SET minus listOrderRefunds? (incl. listOrderRefunds) 13 orders ops.
- PTR-006 Product Catalog B2B Pricing (Inventory, w2, 17): all `catalogue` — listProducts, getProduct,
  createProduct, updateProduct, setProductAttributes, transitionProductLifecycle, listProductVariants,
  resolveProductByCode, listAlternativeCodes, setAlternativeCodes, getPriceList, listPriceLists,
  createPriceList, updatePriceList, copyPriceList, listPrices, setPrices.
- PTR-007 Availability Search (Inventory, w2, 1): getAvailability (catalogue).
- PTR-008 Booking Creation (Booking, w2, 14): ORDER-SET + createRefund.
- PTR-009 Group / Bulk Booking (Booking, w3, 4): seating = createSeatBlock, listSeatBlocks,
  allocateBlockedSeats, releaseSeatBlock.
- PTR-010 Cart & Quote (Booking, w3, 16): orders = getCart, addCartLine, updateCartLine,
  removeCartLine, checkoutCart; promotions = evaluatePromotions, analysePromotionConflicts,
  createPromotion, updatePromotion, publishPromotion, pausePromotion, endPromotion,
  unschedulePromotion, getPromotion, getPromotionUsage, listPromotions.
- PTR-011 Quote Management (Booking, w3, 2): subscription = listPartnerAgreements, getCommissionStatement.
- PTR-012 Checkout / Credit Purchase (Credit, w2, 4): orders = createPayment, capturePayment,
  inquirePaymentStatus, addTip.
- PTR-013 Credit Limit & Balance (Credit, w2, 3): orders = getB2bCredit, setB2bCreditLimit, overrideCreditLimit.
- PTR-014 Settlement & Payment History (Reports, w3, 5): finance = listSettlements, getSettlement,
  ingestSettlementFile, listSettlementExceptions, resolveSettlementException.
- PTR-015 Order History (Orders, w2, 14): ORDER-SET + createRefund.
- PTR-016 Voucher / Ticket Download (Orders, w2, 13): ORDER-SET (reprintOrder first).
- PTR-017 Commission Statement (Reports, w3, 2): subscription = getCommissionStatement, listPartnerAgreements.
- PTR-018 Reports & Sales Performance (Reports, w3, 9): reporting = runReport, askReportingQuestion,
  createReport, updateReport, deleteReport, getReport, listReports, saveNaturalLanguageQuery;
  finance = getFinancialReport (flag: same as SUP-008/ANL).
- PTR-021 Support & Contact (Support, w3, 7): marketing-crm = createCase, getCase, listCases,
  addCaseMessage, updateCase, escalateCase, reopenCase.

Count: 21 declared vs PTR-001..051 in YAML (30 extra, no operations).
Gap list (whole platform): createPartnerUser, listPartnerUsers (subscription) — belong on PTR-020.
Module wave splits: Access & Account (2,3), Booking & Quotes (2,3).
