# promotions — 96 operations awaiting sign-off

> **These are specified, not unfinished.** Each has a request, a response and a citation of
> the pack page it was read from. `x-ticvai-provisional` means **nobody who has to build it
> has agreed it** — so the only thing that closes one is a decision in this column: *agreed*,
> *corrected* (say how), or *not needed*.

**1 pack(s), read in page order.** A session opens a book and walks it.

- Promotions Bundles Management — **96**


---

## Promotions Bundles Management

### p8   · `listPromotionCampaign`

`GET /promotion-campaign` · PRICE_VIEW · staff · **Promotion & Campaign Directory**

> Provide the master searchable list of every promotion and commercial campaign created within TICVAI.

**`PromotionCampaignDirectoryView`** — `approvalState`, `approvalStatus`, `attraction`, `budget`, `budgetStatus`, `businessEntity`, `campaign`, `channel`, `customerSegment`, `date`, `discountType`, `discountValue`, `endDate`, `event`, `fB`, `lastModified`, `membership`, `owner`, `partner`, `product`, `productCategory`, `promotionId`, `promotionName`, `promotionType`, `promotionValue`, `redemptionCount`, `retail`, `revenueGenerated`, `startDate`, `status`, `statusesType`, `targetSegment`, `venue`, `version`

> ⚠ **34 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P09 ADM-139 Promotion & Campaign Directory
- serves P09 ADM-229 Campaign & Promotion Performance Explorer

**Decision:** 

### p11  · `listPromotionLifecycleStatus`

`GET /promotion-lifecycle-statu` · PRICE_VIEW · staff · **Promotion Lifecycle & Status Manager**

> Control the operational lifecycle of promotions.

**`PromotionLifecycleStatusManagerView`** — `aPartnerRequestsSuspension`, `approvalIsCompleted`, `budgetExistsWhereRequired`, `campaignBudgetIsExhausted`, `channelsAreAssigned`, `customerEligibilityExists`, `datesAreValid`, `financialExposureIsAbnormal`, `fraudIsDetected`, `incorrectDiscountOccurs`, `inventoryBecomesUnavailable`, `pausedSuspendedExpiredArchived`, `promotionRulesDoNotConflict`, `requiredConfigurationIsCompleted`, `terminate`, `validProductsExist`

> ⚠ **11 of 16 property names read as sentences** rather than fields — likely the pack's bullets (triggers, behaviours) taken as a directory: `aPartnerRequestsSuspension`, `approvalIsCompleted`, `budgetExistsWhereRequired`, `campaignBudgetIsExhausted`, `channelsAreAssigned`

- serves P09 ADM-141 Promotion Lifecycle & Status Manager

**Decision:** 

### p12  · `listCampaignCalendarTimeline`

`GET /campaign-calendar-timeline` · PRICE_VIEW · staff · **Campaign Calendar & Timeline**

> Provide a calendar-based operational view of promotions.

**`CampaignCalendarTimelineView`** — `active`, `attraction`, `campaign`, `campaignTimeline`, `channel`, `conflicting`, `day`, `dragChangeDatesSubjectToPermission`, `endingSoon`, `expired`, `month`, `pendingApproval`, `product`, `promotionFamily`, `quarter`, `segmentDateAndChannel`, `suspended`, `upcoming`, `venue`, `week`

- serves P08 BO-765 Campaign Library & Calendar
- serves P09 ADM-142 Campaign Calendar & Timeline

**Decision:** 

### p13  · `listPromotionChannel`

`GET /promotion-channel` · PRICE_VIEW · staff · **Promotion Channel & Publication Monitor**

> Ensure promotional configurations are correctly synchronized across every TICVAI sales channel.

**`PromotionChannelPublicationMonitorView`** — `channelRestrictions`, `channelsType`, `codeAvailability`, `errorMessages`, `lastSynchronized`, `notAssigned`, `outOfSync`, `pendingPublication`, `platformAndAllConsumerFacingChannels`, `productsPublished`, `promotionVersion`, `publicationFailed`, `published`, `republish`, `rulesPublished`, `suspended`, `synchronizing`

- serves P09 ADM-143 Promotion Channel & Publication Monitor

**Decision:** 

### p14  · `listPromotionAlertException`

`GET /promotion-alert-exception` · PRICE_VIEW · staff · **Promotion Alerts & Exception Center**

> Centralize operational, commercial, and financial alerts affecting promotions.

**`PromotionAlertsExceptionCenterView`** — `abnormalCouponUsage`, `budgetExceeded`, `budgetNearLimit`, `bundleComponentUnavailable`, `campaignUnderperforming`, `channelSynchronizationFailure`, `critical`, `excessiveDiscountExposure`, `excessiveRepeatRedemption`, `information`, `invalidCode`, `invalidDates`, `invalidDiscount`, `lowConversion`, `lowRedemption`, `marginBelowThreshold`, `missingApproval`, `missingEligibility`, `missingProduct`, `productUnavailable`, `promoCodeLeakage`, `promotionFailedToPublish`, `suspiciousCustomerBehavior`, `unexpectedHighRedemption`, `warning`

- serves P09 ADM-144 Promotion Alerts & Exception Center
- serves P16 ANL-018 Alerts & Exception Center

**Decision:** 

### p16  · `listPromotionHealthPerformance`

`GET /promotion-health-performance` · PRICE_VIEW · staff · **Promotion Health & Performance Monitor**

> Provide near-real-time operational performance monitoring while campaigns are running.

**`PromotionHealthPerformanceMonitorView`** — `aovUplift`, `budgetConsumed`, `budgetRemaining`, `channelVsChannel`, `conversionRate`, `costPerRedemption`, `discountGranted`, `eligibleTransactions`, `grossSales`, `impressions`, `incrementalRevenue`, `margin`, `netSales`, `promotionApplications`, `promotionViews`, `promotionVsAiForecast`, `promotionVsBaseline`, `promotionVsControlGroup`, `promotionVsPreviousCampaign`, `redemptionRate`, `redemptions`, `venueVsVenue`

- serves P09 ADM-146 Promotion Health & Performance Monitor
- serves P09 ADM-228 Promotion Performance Command Center

**Decision:** 

### p17  · `listPromotionActivityVersion`

`GET /promotion-activity-version` · PRICE_VIEW · staff · **Promotion Audit, Activity & Version History**

> Provide complete governance and traceability for every promotion.

**`PromotionAuditActivityVersionHistoryView`** — `andSeeExactlyWhatChanged`, `approvalGranted`, `approvalReference`, `approvalRejected`, `approvalSubmitted`, `approver`, `auditor`, `b2bManager`, `budgetChanged`, `campaignManager`, `channelChanged`, `commercialManager`, `dateTime`, `datesChanged`, `discountChanged`, `eligibilityChanged`, `finance`, `marketingAdministrator`, `newValue`, `operations`, `previousValue`, `productAdded`, `productRemoved`, `promotionActivated`, `promotionArchived`, `promotionCreated`, `promotionEdited`, `promotionExpired`, `promotionPaused`, `promotionSuspended`, `promotionVersion`, `readOnly`, `reason`, `revenueManager`, `role`, `ruleChanged`, `systemAdministrator`, `user`, `venueManager`, `version23Version24`

> ⚠ **40 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P09 ADM-147 Promotion Audit, Activity & Version History

**Decision:** 

### p22  · `setPromotionRule`

`PUT /promotion-rule` · PRICE_CONFIGURE · staff · **Promotion Rule Builder**

> Provide the main no-code workspace for creating the commercial logic behind a promotion.

**`PromotionRuleBuilderView`** — `addedValue`, `businessEntity`, `description`, `fixedDiscount`, `fixedSellingPrice`, `freeProduct`, `freeTicket`, `logic`, `multipleOutcomes`, `nestedConditionGroups`, `owner`, `percentageDiscount`, `priority`, `promotion`, `rewardEntitlement`, `ruleId`, `ruleName`, `ruleOrdering`, `ruleStatus`, `venue`, `voucher`

- serves P09 ADM-148 Promotion Rule Builder
- serves P09 ADM-210 Promotion Stacking Rule Builder

**Decision:** 

### p24  · `listPercentageFixedDiscount`

`GET /percentage-fixed-discount` · PRICE_VIEW · staff · **Percentage & Fixed Discount Configurator**

> Configure the two fundamental discount types required by the matrix. The matrix explicitly states that discounts may be defined as percentage or fixed value.

**`PercentageFixedDiscountConfiguratorView`** — `b2bPrice`, `currency`, `currentSellingPrice`, `discountAboveAuthorizedCeiling`, `discountAmount`, `discountPercentage`, `dynamicPrice`, `marginBelowMinimumThreshold`, `maximumMonetaryDiscount`, `maximumPercentage`, `maximumUses`, `membershipPrice`, `minimumBasketValue`, `minimumQualifyingAmount`, `negativePrices`, `packagePrice`, `priceBelowConfiguredFloor`, `roundingMethod`, `standardPrice`

- serves P09 ADM-149 Percentage & Fixed Discount Configurator

**Decision:** 

### p25  · `listCartTransactionThreshold`

`GET /cart-transaction-threshold` · PRICE_VIEW · staff · **Cart & Transaction Threshold Rules**

> Configure promotions triggered by basket value, ticket quantity, transaction value, or purchase composition. The matrix specifically requires rules such as if more than X tickets are purchased, apply Y discount to the entire transaction.

**`CartTransactionThresholdRulesView`** — `aed`, `aed2505`, `aed50010`, `discountsAreEvaluatedBeforeAfterThreshold`, `feesCount`, `nt`, `refundedItemsAffectQualification`, `taxCountsTowardThreshold`, `voidedItemsAreExcluded`, `vouchersCount`

- serves P09 ADM-150 Cart & Transaction Threshold Rules

**Decision:** 

### p26  · `listVolumeBulkTier`

`GET /volume-bulk-tier` · PRICE_VIEW · staff · **Volume, Bulk & Tier Discount Configurator**

> Manage quantity-based and bulk-purchase commercial rules. The matrix requires configurable bulk thresholds and discount percentages, dedicated group pricing, and tiered bulk purchasing.

**`VolumeBulkTierDiscountConfiguratorView`** — `discount`, `discountValue`, `eligibleChannel`, `eligibleCustomer`, `eligibleProduct`, `fixedUnitPrice`, `maximumQuantity`, `minimumQuantity`, `schools`, `tyNt`

- serves P09 ADM-151 Volume, Bulk & Tier Discount Configurator

**Decision:** 

### p27  · `listTimeBasedSeasonal`

`GET /time-based-seasonal` · PRICE_VIEW · staff · **Time-Based & Seasonal Discount Rules**

> Configure promotional pricing based on when the customer purchases or visits.

**`TimeBasedSeasonalDiscountRulesView`** — `customSeasons`, `dayOfWeek`, `daysBeforeVisit`, `eid`, `eventPeriod`, `hoursBeforeVisit`, `nationalDay`, `peakOffPeak`, `purchaseDate`, `ramadan`, `schoolHolidays`, `season`, `summer`, `time`, `timeslot`, `visitDate`

- serves P09 ADM-152 Time-Based & Seasonal Discount Rules

**Decision:** 

### p28  · `listCustomerMembershipSegment`

`GET /customer-membership-segment` · PRICE_VIEW · staff · **Customer, Membership & Segment Discount Rules**

> Configure discounts based on who the customer is.

**`CustomerMembershipSegmentDiscountRulesView`** — `account`, `ageCategory`, `annualPassHolder`, `b2bCustomer`, `corporateAffiliation`, `countryResidency`, `crmSegment`, `customerSegment`, `guestCategory`, `loyaltyTier`, `membershipStatus`, `membershipTier`, `partnerAffiliation`

- serves P09 ADM-153 Customer, Membership & Segment Discount Rules

**Decision:** 

### p29  · `listPaymentMethodBank`

`GET /payment-method-bank` · PRICE_VIEW · staff · **Payment Method, Bank & Partner Discount Rules**

> Configure discounts triggered by how the guest pays or which commercial partner they belong to. The matrix specifically includes discounts for payment types and bank credit/debit cards.

**`PaymentMethodBankPartnerDiscountRulesView`** — `airlines`, `applePay`, `bankSpecificCard`, `banks`, `binIinEligibilityReference`, `campaignBudget`, `corporatePartners`, `creditCard`, `customerLimit`, `debitCard`, `discount`, `eligibleProducts`, `giftCard`, `governmentPartners`, `hotels`, `mada`, `mastercard`, `maximumDiscount`, `membershipPrograms`, `minimumSpend`, `numberOfUses`, `partnerBank`, `promotionPeriod`, `selectedPaymentGateway`, `tourismPartners`, `visa`, `wallet`

> ⚠ **27 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P09 ADM-154 Payment Method, Bank & Partner Discount Rules

**Decision:** 

### p30  · `listSpecialPriceGuest`

`GET /special-price-guest` · PRICE_VIEW · staff · **Special Price & Guest Offer Configurator**

> Manage commercially distinct special-price products and targeted offers without unnecessarily duplicating product SKUs.

**`SpecialPriceGuestOfferConfiguratorView`** — `annualPass`, `capacity`, `channel`, `discount`, `eligibleGuest`, `eligibleProduct`, `employeePrice`, `familyPass`, `familyPrice`, `groupPrice`, `ladiesNight`, `multiParksPass`, `offerName`, `partnerPrice`, `price`, `quantity`, `residentPrice`, `restrictions`, `schoolPrice`, `studentPrice`, `touristPrice`, `twoParksPass`, `validDates`, `validVisitDates`, `venue`

- serves P09 ADM-155 Special Price & Guest Offer Configurator

**Decision:** 

### p31  · `listDiscountLimitGuardrail`

`GET /discount-limit-guardrail` · PRICE_VIEW · staff · **Discount Limits, Guardrails & Commercial Controls**

> Protect the business from incorrectly configured discounts and excessive commercial exposure.

**`DiscountLimitsGuardrailsCommercialControlsView`** — `above40`, `maximumCampaignExposure`, `maximumCustomerDiscount`, `maximumDiscount`, `maximumDiscount15`, `maximumDiscount25`, `maximumDiscount40`, `maximumDiscountValue`, `maximumRedemptionCount`, `maximumTransactionDiscount`, `minimumMargin`, `minimumSellingPrice`, `perAccountUsage`, `perCustomerUsage`, `requireApproval`, `requiredByTheMatrix`

- serves P09 ADM-156 Discount Limits, Guardrails & Commercial Controls

**Decision:** 

### p32  · `setRuleTestRecommendation`

`PUT /rule-test-recommendation` · PRICE_CONFIGURE · staff · **Rule Test, Simulation & AI Recommendation Workspace**

> Allow administrators to test promotional rules before activating them. This is critical because the matrix requires simulation of redemption, discount exposure, revenue impact, margin impact and financial performance before activation.

**`RuleTestSimulationAiRecommendationWorkspaceView`** — `approver`, `auditor`, `b2bManager`, `b2c`, `campaignManager`, `changeDates`, `changeDiscount`, `changeSegments`, `changeThresholds`, `channel`, `commercialManager`, `companySegmentsAndPartnerPricing`, `currentPriceAndPricingFloors`, `date`, `discount`, `familySegment`, `finance`, `guest`, `guestCustomerSegments`, `loyalty`, `marketingAdministrator`, `membership`, `membershipAndTierEligibility`, `paymentMethodAndBankEligibility`, `paymentType`, `products`, `productsEligibleForPromotionalRules`, `promoCode`, `quantity`, `revenueManager`, `revenueMarginAndDiscountExposure`, `rule421Qualified`, `segment`, `systemAdministrator`, `validDate`, `venue`, `venueManager`

> ⚠ **37 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P09 ADM-157 Rule Test, Simulation & AI Recommendation Workspace

**Decision:** 

### p32  · `simulateBundlePreviewRecommendation`

`PUT /bundle-preview-recommendation` · PRICE_CONFIGURE · staff · **Bundle Preview, Simulation & AI Recommendation**

> Allow administrators to test promotional rules before activating them. This is critical because the matrix requires simulation of redemption, discount exposure, revenue impact, margin impact and financial performance before activation.

**`BundlePreviewSimulationAiRecommendationView`** — `approver`, `auditor`, `b2bManager`, `b2c`, `campaignManager`, `changeDates`, `changeDiscount`, `changeSegments`, `changeThresholds`, `channel`, `commercialManager`, `companySegmentsAndPartnerPricing`, `currentPriceAndPricingFloors`, `date`, `discount`, `familySegment`, `finance`, `guest`, `guestCustomerSegments`, `loyalty`, `marketingAdministrator`, `membership`, `membershipAndTierEligibility`, `paymentMethodAndBankEligibility`, `paymentType`, `products`, `productsEligibleForPromotionalRules`, `promoCode`, `quantity`, `revenueManager`, `revenueMarginAndDiscountExposure`, `rule421Qualified`, `segment`, `systemAdministrator`, `validDate`, `venue`, `venueManager`

> ⚠ **37 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P09 ADM-187 Bundle Preview, Simulation & AI Recommendation

**Decision:** 

### p37  · `setCouponPromoCode`

`PUT /coupon-promo-code` · PRICE_CONFIGURE · staff · **Coupon & Promo Code Builder**

> Create the commercial definition of a coupon or promo-code campaign.

**`CouponPromoCodeBuilderView`** — `addedValue`, `bulkCampaignCode`, `bundleBenefit`, `commonPromoCode`, `compensationServiceRecoveryCode`, `coupon`, `discountVoucher`, `employeeCode`, `fixedPromotionalPrice`, `fixedValueDiscount`, `freeAddOn`, `freeProduct`, `freeTicket`, `freeTicketCode`, `influencerAffiliateCode`, `partnerCode`, `percentageDiscount`, `promotionalVoucher`, `thanDuplicateDiscountLogic`, `uniquePromoCode`

- serves P09 ADM-159 Coupon & Promo Code Builder

**Decision:** 

### p38  · `listUniqueCodeGeneration`

`GET /unique-code-generation` · PRICE_VIEW · staff · **Unique Code Generation & Batch Manager**

> Generate and manage large quantities of secure unique promotional codes.

**`UniqueCodeGenerationBatchManagerView`** — `assignedPartner`, `batchId`, `campaign`, `caseSensitivity`, `characterType`, `codeLength`, `distributionOwner`, `distributionStatus`, `expiration`, `expiry`, `generatedBy`, `generationDate`, `it`, `numberOfCodes`, `numberOfUses`, `permissionsExplicitlyAllowIt`, `prefix`, `quantityGenerated`, `redeemedQuantity`, `remainingQuantity`, `suffix`

- serves P09 ADM-160 Unique Code Generation & Batch Manager

**Decision:** 

### p39  · `listCodeEligibilityRestriction`

`GET /code-eligibility-restriction` · PRICE_VIEW · staff · **Code Eligibility & Restriction Manager**

> Determine where, when, by whom, and against what a code can be redeemed. The matrix explicitly requires promo codes to support restrictions for usage, dates, duration, capacity, frequency, location, group, partner, operating area, and sales channel.

**`CodeEligibilityRestrictionManagerView`** — `addOn`, `api`, `attraction`, `b2b`, `b2bAccount`, `b2c`, `bundle`, `businessEntity`, `callCenter`, `conditions`, `corporateGroup`, `crmSegment`, `event`, `fB`, `guestType`, `kiosk`, `location`, `loyaltyTier`, `membership`, `mobileApp`, `mobilePos`, `operatingArea`, `partner`, `pos`, `product`, `productCategory`, `reseller`, `retail`, `ticket`, `ticketType`, `venue`

> ⚠ **31 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P09 ADM-161 Code Eligibility & Restriction Manager

**Decision:** 

### p41  · `listUsageCapacityFrequency`

`GET /usage-capacity-frequency` · PRICE_VIEW · staff · **Usage, Capacity & Frequency Control**

> Control exactly how frequently and how many times promotional codes may be redeemed. Control the temporal validity of coupons and codes.

**`UsageCapacityFrequencyControlView`** — `at`, `issued50000`, `maximumPerAccount`, `maximumPerChannel`, `maximumPerCustomer`, `maximumPerDay`, `maximumPerTransaction`, `maximumPerVenue`, `maximumTotalRedemptions`, `multipleUse`, `redeemed31450`, `remaining18130`, `reservedPending420`, `singleUse`, `thresholdsShallBeConfigurable`, `unlimitedUse`

- serves P09 ADM-162 Usage, Capacity & Frequency Control

**Decision:** 

### p41  · `listValidityDateTime`

`GET /validity-date-time` · PRICE_VIEW · staff · **Validity, Date & Time Control**

> Control the temporal validity of coupons and codes.

**`ValidityDateTimeControlView`** — `blackoutDates`, `expirationGracePeriod`, `holidays`, `mondayThursdayOnly`, `seasonalCalendars`, `selectedEvents`, `selectedTimeslots`, `theAdministratorSBrowserTimezone`, `valid18002200`

- serves P09 ADM-163 Validity, Date & Time Control

**Decision:** 

### p42  · `setCodeDistributionManager`

`PUT /code-distribution-manager` · PRICE_CONFIGURE · staff · **Code Distribution & Assignment Manager**

> Manage how promotional codes are allocated and distributed.

**`CodeDistributionAssignmentManagerView`** — `assigned`, `assigned25000`, `b2bCompany`, `bank`, `batchBankabc2027001`, `cancelled`, `channelsType`, `codes25000`, `corporatePartner`, `customerSegment`, `delivered`, `expired`, `generated`, `hotel`, `individualCustomer`, `marketingCampaign`, `membershipAccount`, `partnerBankAbc`, `redeemed`, `redeemed8720`, `remaining16280`, `reseller`, `school`, `sent`, `travelAgency`, `viewedWhereAvailable`

> ⚠ **26 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P09 ADM-164 Code Distribution & Assignment Manager

**Decision:** 

### p43  · `listRedemptionCodeLookup`

`GET /redemption-code-lookup` · PRICE_VIEW · staff · **Redemption Monitor & Code Lookup**

> Provide real-time operational visibility into coupon and promo-code redemption.

**`RedemptionMonitorCodeLookupView`** — `batchId`, `booking`, `campaign`, `cancelled`, `channel`, `code`, `couponId`, `customer`, `customerAccountReference`, `devicePos`, `discount`, `expired`, `finalValue`, `invalidChannel`, `invalidCustomer`, `invalidLocation`, `invalidProduct`, `notStarted`, `operator`, `originalValue`, `partner`, `product`, `promoCode`, `redeemed`, `redemptionDate`, `redemptionTime`, `requiresRedemptionReporting`, `suspended`, `transaction`, `usageLimitReached`, `valid`, `validationResult`, `venue`

> ⚠ **33 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P09 ADM-165 Redemption Monitor & Code Lookup

**Decision:** 

### p44  · `listCodeSecurityFraud`

`GET /code-security-fraud` · PRICE_VIEW · staff · **Code Security, Fraud & Exception Center**

> Detect promo-code abuse, leakage, abnormal redemption, and suspicious campaign behavior.

**`CodeSecurityFraudExceptionCenterView`** — `codeEnumerationAttempts`, `excessiveRedemptionVelocity`, `highVolumeRedemptionFromOneDevice`, `levelsType`, `multipleCustomersUsingCustomerSpecificCode`, `partnerCodeLeakage`, `redemptionAboveExpectedCampaignPattern`, `reinstateCode`, `repeatedFailedAttempts`, `suspiciousPosOperatorActivity`, `unusualGeographicUsage`

- serves P09 ADM-166 Code Security, Fraud & Exception Center

**Decision:** 

### p45  · `listRedemption`

`GET /redemption` · PRICE_VIEW · staff · **Redemption Analytics, Audit & AI Optimization**

> Provide complete performance analytics and governance for coupon and promo-code campaigns.

**`RedemptionAnalyticsAuditAiOptimizationView`** — `aovUplift`, `approvalReference`, `assigned`, `bundlesBundleRelatedCouponBenefits`, `cancelled`, `codesDistributed`, `codesGenerated`, `codesRedeemed`, `conversionRate`, `costPerRedemption`, `created`, `determinesQualificationAndCalculation`, `discountGranted`, `distributed`, `expired`, `expiredUnusedCodes`, `generated`, `identifiesBenefit`, `incrementalRevenue`, `marginImpact`, `matrixCoverageBoard3`, `modified`, `newValue`, `paymentPaymentMethodDependentPromotions`, `previousValue`, `reactivated`, `reason`, `redeemed`, `redemptionRate`, `revenueGenerated`, `suspended`, `ticketingCatalogueEligibleTicketsProducts`, `timestamp`, `user`

> ⚠ **34 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P08 BO-444 Redemption Operations Dashboard
- serves P09 ADM-167 Redemption Analytics, Audit & AI Optimization

**Decision:** 

### p50  · `listAdvancedOffer`

`GET /advanced-offer` · PRICE_VIEW · staff · **Advanced Offer Command Center**

> Provide the centralized management workspace for all advanced promotional mechanics.

**`AdvancedOfferCommandCenterView`** — `active`, `activeAdvancedOffers`, `aovUplift`, `archived`, `bogoCampaigns`, `crossCategoryOffers`, `discountGranted`, `draft`, `expired`, `fixedPriceOffers`, `freeItemsIssued`, `giftWithPurchaseOffers`, `marginImpact`, `paused`, `pendingApproval`, `pendingValidation`, `revenueGenerated`, `scheduled`, `scheduledOffers`, `suspended`, `totalRedemptions`

- serves P09 ADM-168 Advanced Offer Command Center

**Decision:** 

### p52  · `setBuyGetBogo`

`PUT /buy-get-bogo` · PRICE_CONFIGURE · staff · **Buy X Get Y / BOGO Rule Builder**

> Configure the fundamental qualifier → reward relationship.

**`BuyXGetYBogoRuleBuilderView`** — `channel`, `customerSegment`, `dateTime`, `differentProduct`, `fixedDiscount`, `fixedRewardPrice`, `free`, `minimumSpend`, `percentageDiscount`, `product`, `productCategory`, `quantity`, `sameProduct`, `ticketType`, `venue`

- serves P09 ADM-169 Buy X Get Y / BOGO Rule Builder

**Decision:** 

### p53  · `listCheapestLowestValue`

`GET /cheapest-lowest-value` · PRICE_VIEW · staff · **Cheapest / Lowest-Value Item Promotion**

> Configure offers where TICVAI dynamically identifies the lowest-priced qualifying item. Pag e 53 | 158TICVAI • 53 The matrix explicitly requires “buy multiple products and get cheapest item free” and adding cheaper qualifying items within the same transaction.

**`CheapestLowestValueItemPromotionView`** — `buy4CheapestFree`, `cheapestItem50Off`, `cheapestItemFree`, `cheapestLowestPricedSelection`, `e100`, `eligibleCategories`, `eligibleProducts`, `maximumFreeItemValue`, `maximumRepetitions`, `minimumQuantity`, `nCheapestItemsFree`, `numberOfFreeItems`

- serves P09 ADM-171 Cheapest / Lowest-Value Item Promotion

**Decision:** 

### p53  · `listMultiBuyQuantity`

`GET /multi-buy-quantity` · PRICE_VIEW · staff · **Multi-Buy & Quantity Offer Configurator**

> Configure advanced quantity relationships that go beyond simple BOGO. Configure offers where TICVAI dynamically identifies the lowest-priced qualifying item. Pag e 53 | 158TICVAI • 53

**`MultiBuyQuantityOfferConfiguratorView`** — `amountOff`, `exactQuantity`, `fixedTotalPrice`, `maximumRepetitions`, `minimumQuantity`, `multipleFree`, `multiplesOfX`, `oneFree`, `percentageOff`, `quantityRange`, `repeatAutomatically`

- serves P09 ADM-170 Multi-Buy & Quantity Offer Configurator

**Decision:** 

### p54  · `setFixedPriceOffer`

`PUT /fixed-price-offer` · PRICE_CONFIGURE · staff · **Fixed-Price & “N for X” Offer Builder**

> Configure promotions where a qualifying collection of products is sold for a fixed promotional total.

**`FixedPriceNForXOfferBuilderView`** — `currency`, `fixedPromotionalPrice`, `for`, `maximumRepetitions`, `minimumMaximumProductValues`, `mixAndMatchAllowed`, `partnerSettlement`, `productCategory`, `refunds`, `reporting`, `requiredProducts`, `requiredQuantity`, `revenueRecognition`, `tax`

- serves P09 ADM-172 Fixed-Price & “N for X” Offer Builder

**Decision:** 

### p55  · `setGiftFreeProduct`

`PUT /gift-free-product` · PRICE_CONFIGURE · staff · **Gift, Free Product & Added-Value Offer Builder**

> Configure promotions where a purchase generates an additional entitlement rather than simply reducing price. The matrix explicitly provides the example: “Buy for more than 200 AED and get a free pencil.”

**`GiftFreeProductAddedValueOfferBuilderView`** — `allowLaterFulfillment`, `basketValue`, `customerSegment`, `doNotOfferPromotion`, `eligibleFulfillmentPoint`, `inventoryAvailability`, `locationInventory`, `membership`, `product`, `productCategory`, `provideAlternativeReward`, `quantity`, `substitutionRules`, `ticket`, `typesType`

- serves P09 ADM-173 Gift, Free Product & Added-Value Offer Builder

**Decision:** 

### p56  · `setCrossCategoryPromotion`

`PUT /cross-category-promotion` · PRICE_CONFIGURE · staff · **Cross-Category Promotion Builder**

> Create promotions spanning different TICVAI commercial domains.

**`CrossCategoryPromotionBuilderView`** — `addOns`, `attractions`, `events`, `experiences`, `fB`, `membership`, `parking`, `retail`, `services`, `ticketing`

- serves P09 ADM-174 Cross-Category Promotion Builder

**Decision:** 

### p57  · `listRewardSelectionSubstitution`

`GET /reward-selection-substitution` · PRICE_VIEW · staff · **Reward Selection, Substitution & Customer Choice**

> Control situations where the customer can choose between multiple promotional rewards.

**`RewardSelectionSubstitutionCustomerChoiceView`** — `guestSelectsFromConfiguredOptions`, `posCallCenterOperatorSelects`

- serves P09 ADM-175 Reward Selection, Substitution & Customer Choice

**Decision:** 

### p58  · `listAdvancedOfferGuardrail`

`GET /advanced-offer-guardrail` · PRICE_VIEW · staff · **Advanced Offer Guardrails & Conflict Controls**

> Prevent advanced offers from generating unintended financial or operational outcomes. This screen handles offer-specific safeguards; the complete cross-promotion stacking hierarchy remains in Board 8.

**`AdvancedOfferGuardrailsConflictControlsView`** — `canCombine`, `cannotCombine`, `deferToCentralStackingEngine`, `exclusive`, `inventoryRequirement`, `maximumApplicationsPerBasket`, `maximumApplicationsPerCustomer`, `maximumCampaignRedemptions`, `maximumDailyRedemptions`, `maximumDiscount`, `maximumFreeItems`, `maximumRewardValue`, `minimumMargin`, `minimumTransactionValue`

- serves P09 ADM-168 Advanced Offer Command Center
- serves P09 ADM-176 Advanced Offer Guardrails & Conflict Controls

**Decision:** 

### p59  · `listOfferBasketTrace`

`GET /offer-basket-trace` · PRICE_VIEW · staff · **Offer Simulation, Basket Trace & AI Optimization**

> Test complex promotion mechanics before publication.

**`OfferSimulationBasketTraceAiOptimizationView`** — `adult`, `board4AdvancedMechanics`, `bulkScenarioTesting`, `cheapestAdmissionSelected`, `child`, `childTicketAed150`, `codeTriggeredAdvancedOffers`, `couponEngineBoard3`, `customerSegmentationAndPersonalization`, `eligibleChannel`, `eligibleVenue`, `finalTotalAed600`, `finalTransactionAmount`, `forecastSimulation`, `freeProductAvailabilityAndSubstitution`, `historicalTransactionReplay`, `marginFloorMaintained`, `matrixCoverageBoard4`, `maximumRewardAed200`, `memberEligibilityAndBenefits`, `menuProductsPricesAndInventory`, `originalTotalAed750`, `priceBasisAndMarginProtection`, `promotionAed150`, `qualifierAndRewardTicketProducts`, `retailProductsAndStockAvailability`, `revenueAllocationAndPromotionalCost`, `sampleCustomerSegment`, `singleTransaction`, `subtotalAed750`, `whatProductToProductRewardRelationshipOccurs`, `yPrice`

> ⚠ **32 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P09 ADM-177 Offer Simulation, Basket Trace & AI Optimization

**Decision:** 

### p63  · `listBundleCombo`

`GET /bundle-combo` · PRICE_VIEW · staff · **Bundle & Combo Command Center**

> Provide centralized visibility and management of all bundles and combo products across

**`BundleComboCommandCenterView`** — `active`, `activeBundles`, `aovUplift`, `archived`, `averageBundleValue`, `bundleConversionRate`, `bundleMargin`, `bundleRevenue`, `bundleSales`, `draft`, `draftBundles`, `dynamicBundles`, `expired`, `fixedBundles`, `guestChoiceBundles`, `incomplete`, `partnerBundles`, `paused`, `pendingApproval`, `pendingValidation`, `redemptionRate`, `scheduled`, `scheduledBundles`, `suspended`

- serves P09 ADM-178 Bundle & Combo Command Center

**Decision:** 

### p65  · `setBundleDefinition`

`PUT /bundle-definition` · PRICE_CONFIGURE · staff · **Bundle Definition & Setup**

> Create the commercial identity and high-level behavior of a bundle.

**`BundleDefinitionSetupView`** — `allComponentsPredefined`, `appearsAsStandaloneProduct`, `bundleCategory`, `bundleId`, `bundleName`, `businessEntity`, `campaign`, `chooseAny3Attractions`, `containsInternalAndExternalProducts`, `customerSelectsFromPermittedCategories`, `effectiveDates`, `guestFacingDescription`, `internalDescription`, `isRecommendedDuringCheckout`, `owner`, `requiredComponentsPlusOptionalChoices`, `requiresAnotherProduct`, `salesStatus`, `venue`

- serves P09 ADM-179 Bundle Definition & Setup

**Decision:** 

### p66  · `setBundleComponent`

`PUT /bundle-component` · PRICE_CONFIGURE · staff · **Bundle Component Builder**

> Define exactly what products and services make up the bundle.

**`BundleComponentBuilderView`** — `admissionTicket`, `annualPass`, `attraction`, `event`, `experience`, `externalProduct`, `fBMealPackage`, `fBProduct`, `fixedQuantity`, `giftCard`, `locker`, `maximum`, `membership`, `minimum`, `ntYEntTreatment`, `parking`, `photo`, `photo1OptionalAed30`, `quantityBasedOnGuestCount`, `quantityBasedOnTicketCount`, `rental`, `retailProduct`, `service`, `timeslot`, `typesType`, `voucher`

> ⚠ **26 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P09 ADM-180 Bundle Component Builder

**Decision:** 

### p67  · `setGuestChoiceBuild`

`PUT /guest-choice-build` · PRICE_CONFIGURE · staff · **Guest Choice & Build-Your-Own Bundle Designer**

> Configure bundles where the guest chooses products from predefined groups. The matrix specifically requires the guest to be able to choose attractions, experiences, F&B, retail products, or services from predefined categories while maintaining bundle pricing rules.

**`GuestChoiceBuildYourOwnBundleDesignerView`** — `additionalCharge`, `adventurePark`, `aquarium`, `category`, `eligibleProducts`, `groupName`, `locker`, `maximumSelections`, `mealA`, `mealB`, `mealC`, `minimumSelections`, `museum`, `observationDeck`, `parking`, `photo`, `requiredOptional`, `selectionOrder`, `waterPark`

- serves P09 ADM-181 Guest Choice & Build-Your-Own Bundle Designer

**Decision:** 

### p68  · `listBundlePricingCommercial`

`GET /bundle-pricing-commercial` · PRICE_VIEW · staff · **Bundle Pricing & Commercial Model**

> Determine how the bundle is commercially priced.

**`BundlePricingCommercialModelView`** — `aed30`, `basePrice`, `bundleDiscount15`, `calculatedThroughTicvaiSPricingEngine`, `channelSpecificPrice`, `currency`, `discount`, `discountAmount`, `eachComponentRetainsConfiguredPrice`, `guestSpecificPrice`, `marginFloor`, `maximumPrice`, `minimumPrice`, `priceFloor`

- serves P09 ADM-048 Commercial Pricing Command Center
- serves P09 ADM-182 Bundle Pricing & Commercial Model

**Decision:** 

### p69  · `listBundleAvailabilityCapacity`

`GET /bundle-availability-capacity` · PRICE_VIEW · staff · **Bundle Availability, Capacity & Validation**

> Ensure that TICVAI does not sell a bundle unless all required components can actually be fulfilled. This is a direct requirement of the matrix: each bundle component maintains independent inventory, capacity, validity, redemption rules, and availability, and the system validates included products before confirming the …

**`BundleAvailabilityCapacityValidationView`** — `available`, `capacityUnavailable`, `independentCapacity`, `invalidDate`, `lowAvailability`, `soldOut`, `suspended`, `unpublished`

- serves P09 ADM-183 Bundle Availability, Capacity & Validation

**Decision:** 

### p70  · `listBundleValidityScheduling`

`GET /bundle-validity-scheduling` · PRICE_VIEW · staff · **Bundle Validity, Scheduling & Redemption Rules**

> Control when bundle components may be consumed and whether they must be redeemed together or separately.

**`BundleValiditySchedulingRedemptionRulesView`** — `allComponentsTogether`, `firstUseActivation`, `independentRedemption`, `ownAccessRule`, `ownCapacity`, `ownEntitlement`, `ownRedemptionCount`, `ownTimeslot`, `ownValidity`, `scheduledRedemption`, `sequentialRedemption`, `timeslotReservationRequired`, `valid1June31August`

- serves P09 ADM-184 Bundle Validity, Scheduling & Redemption Rules

**Decision:** 

### p71  · `listPartnerExternalProduct`

`GET /partner-external-product` · PRICE_VIEW · staff · **Partner & External Product Bundle Manager**

> Allow TICVAI bundles to include products or services owned by external operators. The matrix requires combinations with external products/services and bundles across different destinations, including systems that may use different databases.

**`PartnerExternalProductBundleManagerView`** — `apiError`, `apiSource`, `availabilitySource`, `available`, `cancellationRule`, `commission`, `connected`, `degraded`, `externalDesertSafari`, `externalHotelNight`, `externalPrice`, `externalProductId`, `mappingError`, `partner`, `productName`, `productUnavailable`, `redemptionMethod`, `settlementRule`, `soldAsOneCommercialPackage`, `ticvaiMealVoucher`, `ticvaiSellingPrice`, `ticvaiWaterPark`

- serves P09 ADM-185 Partner & External Product Bundle Manager

**Decision:** 

### p72  · `listRevenueAllocationCost`

`GET /revenue-allocation-cost` · PRICE_VIEW · staff · **Revenue Allocation, Cost & Settlement Rules**

> Determine how bundle revenue is allocated across its components. This is explicitly required by the matrix for allocation across products, attractions, departments, partners, operators, and accounting entities.

**`RevenueAllocationCostSettlementRulesView`** — `commission`, `componentRefund`, `contractualPartnerAllocation`, `costCenter`, `costPlus`, `department`, `fixedAmount`, `fullRefund`, `legalEntity`, `on`, `partialRefund`, `partnerPayable`, `percentage`, `proportionalListPrice`, `redemptionBasedAllocation`, `revenueAccount`, `settlementCycle`, `taxTreatment`, `unredeemedComponentRefund`, `weightedAllocation`

- serves P09 ADM-186 Revenue Allocation, Cost & Settlement Rules

**Decision:** 

### p78  · `listDynamicBundle`

`GET /dynamic-bundle` · PRICE_VIEW · staff · **Dynamic Bundle Operations Command Center**

> Provide real-time visibility into the operational health of all active bundles.

**`DynamicBundleOperationsCommandCenterView`** — `activeDynamicBundles`, `aquariumAvailable`, `bundleHealthWarning`, `bundleSalesToday`, `bundlesWithLowCapacity`, `capacityReserved`, `componentsSoldOut`, `critical`, `failedBundleAttempts`, `familyMealLowStock`, `healthy`, `partiallyAvailableBundles`, `photoAvailable`, `recoveredRevenue`, `revenueAtRisk`, `sellableBundles`, `substitutionsTriggered`, `unavailable`, `unavailableBundles`, `warning`, `waterParkAvailable`

- serves P09 ADM-188 Dynamic Bundle Operations Command Center
- serves P09 ADM-197 Dynamic Bundle Simulation & AI Optimization

**Decision:** 

### p79  · `listComponentInventoryAvailability`

`GET /component-inventory-availability` · PRICE_VIEW · staff · **Component Inventory & Availability Matrix**

> Provide one centralized matrix showing availability for every component within every active bundle.

**`ComponentInventoryAvailabilityMatrixView`** — `apiUnavailable`, `attractionCapacity`, `available`, `closed`, `dE`, `eventCapacity`, `externalPartnerApi`, `fBAvailability`, `limited`, `low`, `parking`, `rental`, `resourceAvailability`, `retailStock`, `seatInventory`, `soldOut`, `souvenir0Open`, `suspended`, `tRyTyLe`, `ticketInventory`, `timeslots`, `unpublished`

- serves P09 ADM-189 Component Inventory & Availability Matrix

**Decision:** 

### p80  · `listBundleSellabilityDependency`

`GET /bundle-sellability-dependency` · PRICE_VIEW · staff · **Bundle Sellability & Dependency Rule Engine**

> Determine whether the overall bundle can be sold based on the state of its underlying components.

**`BundleSellabilityDependencyRuleEngineView`** — `allComponentsRequired`, `aquariumMandatory`, `atLeastOneFromCategory`, `atLeastXOfY`, `conditionalComponent`, `optionalComponent`, `partnerComponentRequired`, `photoOptional`, `substituteAllowed`, `waterParkMandatory`

- serves P09 ADM-190 Bundle Sellability & Dependency Rule Engine

**Decision:** 

### p81  · `listCapacityPoolReservation`

`GET /capacity-pool-reservation` · PRICE_VIEW · staff · **Capacity Pool & Reservation Manager**

> Manage how bundle sales consume capacity from underlying products. This is particularly important because a bundle must not create artificial inventory separate from the actual attraction/product capacity.

**`CapacityPoolReservationManagerView`** — `aquariumRemainingCapacity`, `capacityAutomaticallyReleased`, `channelAllocation`, `dedicatedBundleAllocation`, `eventCapacity`, `hardAllocation`, `held`, `holdDuration`, `overbookingPolicy`, `partnerAllocation`, `remainingSellable`, `resourceCapacity`, `seatInventory`, `sharedPool`, `softAllocation`, `standaloneSales`, `temporaryReservation`, `timeslotCapacity`, `waitlistBehavior`

- serves P09 ADM-191 Capacity Pool & Reservation Manager

**Decision:** 

### p82  · `listDynamicComponentSubstitution`

`GET /dynamic-component-substitution` · PRICE_VIEW · staff · **Dynamic Component Substitution Engine**

> Automatically replace unavailable bundle components according to predefined commercial rules.

**`DynamicComponentSubstitutionEngineView`** — `addsSurcharge`, `alternative1`, `alternative2`, `alternative3`, `capacityExhausted`, `externalApiUnavailable`, `fallbackAction`, `inventoryBelowThreshold`, `maintainsSameBundlePrice`, `primaryComponent`, `productSuspended`, `reducesBundlePrice`, `requiresCustomerApproval`, `requiresOperatorApproval`, `soldOut`, `venueClosed`

- serves P09 ADM-192 Dynamic Component Substitution Engine

**Decision:** 

### p83  · `listDynamicBundleRule`

`GET /dynamic-bundle-rule` · PRICE_VIEW · staff · **Dynamic Bundle Rule & Composition Engine**

> Allow the actual composition of a bundle to change dynamically according to business and guest conditions. This builds upon the matrix requirement for dynamic bundles where guests select attractions, experiences, F&B, Retail, or services from predefined categories.

**`DynamicBundleRuleCompositionEngineView`** — `campaign`, `capacity`, `day`, `guestSegment`, `guestType`, `inventory`, `loyaltyTier`, `membership`, `numberOfGuests`, `productPopularity`, `purchaseHistory`, `salesChannel`, `season`, `time`, `venue`

- serves P09 ADM-188 Dynamic Bundle Operations Command Center
- serves P09 ADM-193 Dynamic Bundle Rule & Composition Engine
- serves P09 ADM-197 Dynamic Bundle Simulation & AI Optimization

**Decision:** 

### p84  · `listRealTimeAvailability`

`GET /real-time-availability` · PRICE_VIEW · staff · **Real-Time Availability & Checkout Validation**

> Perform the final authoritative validation immediately before transaction confirmation. This is essential because availability may change between browsing and payment.

**`RealTimeAvailabilityCheckoutValidationView`** — `capacityAvailable`, `componentMappingValid`, `inventoryAvailable`, `partnerComponentValid`, `priceValid`, `productActive`, `promotionValid`, `resourceAvailable`, `timeslotAvailable`

- serves P08 BO-518 Real-Time Availability Calendar
- serves P08 BO-997 Real-Time Availability & Locking
- serves P09 ADM-194 Real-Time Availability & Checkout Validation

**Decision:** 

### p85  · `listBundleAvailabilityChannel`

`GET /bundle-availability-channel` · PRICE_VIEW · staff · **Bundle Availability by Channel, Venue & Partner**

> Control where a bundle is sellable based on operational availability.

**`BundleAvailabilityByChannelVenuePartnerView`** — `attractionSpecificAvailability`, `bookingCutoff`, `capacityCeiling`, `channelsType`, `countryMarket`, `dedicatedAllocation`, `eEE`, `operatingArea`, `salesLocation`, `sharedAllocation`, `venueSpecificAvailability`

- serves P09 ADM-195 Bundle Availability by Channel, Venue & Partner

**Decision:** 

### p86  · `listBundleAvailabilityForecast`

`GET /bundle-availability-forecast` · PRICE_VIEW · staff · **Bundle Availability Forecast, Alerts & Recovery**

> Predict bundle availability problems before they affect sales.

**`BundleAvailabilityForecastAlertsRecoveryView`** — `campaignActivity`, `capacity`, `currentBookingVelocity`, `dayOfWeek`, `historicalDemand`, `increaseAlternativeInventory`, `inventory`, `levelsType`, `partnerReservations`, `potentialRevenueRecoverableThroughSubstitution`, `recommendAnotherTimeslot`, `reduceBundleAllocation`, `restrictChannel`, `seasonality`, `switchChoiceGroup`, `timeslotUtilization`

- serves P09 ADM-196 Bundle Availability Forecast, Alerts & Recovery

**Decision:** 

### p87  · `listDynamicBundle2`

`GET /dynamic-bundle-2` · PRICE_VIEW · staff · **Dynamic Bundle Simulation & AI Optimization**

> Test how a bundle behaves under different operational scenarios before activating dynamic rules.

**`DynamicBundleSimulationAiOptimizationView`** — `aed20`, `aquariumRequiredSubstituteAllowed`, `aquariumUnavailable`, `attractionEventCapacity`, `beforeRecommendingSubstitutions`, `bundleRemainsSellable`, `bundleStatus`, `capacityImpact`, `change`, `checkoutPaymentCoordination`, `commercialImpact`, `componentsSelected`, `customerApprovalRequired`, `customerImpact`, `entitlementRedemptionState`, `externalAvailability`, `humanApproves`, `level1RecommendOnly`, `level2PreApprovedAutomation`, `marginImpact`, `matrixCoverageBoard6`, `membershipBasedComponents`, `menuAvailability`, `observationDeckAvailable`, `partnerAllocation`, `physicalInventory`, `priceImpact`, `productStatusAndInventory`, `promotionQualification`, `realTimePricing`, `resourceAvailability`, `revenueImpact`, `seatAvailabilityWhereIncluded`, `substitutions`, `whatIsTheBundle`

> ⚠ **35 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P09 ADM-188 Dynamic Bundle Operations Command Center
- serves P09 ADM-197 Dynamic Bundle Simulation & AI Optimization

**Decision:** 

### p94  · `listTargetingEligibility`

`GET /targeting-eligibility` · PRICE_VIEW · staff · **Targeting & Eligibility Command Center**

> Provide centralized visibility into all promotion audiences, eligibility rules, segments, targeting strategies, and their performance.

**`TargetingEligibilityCommandCenterView`** — `activeSegments`, `activeTargetingRules`, `aiRecommendedSegments`, `aovUplift`, `bundlesUsingTargeting`, `conflict`, `conversionRate`, `eligibilityPassRate`, `eligibleCustomers`, `expired`, `healthy`, `missingData`, `noAudience`, `oversizedAudience`, `personalizedOffers`, `promotionsUsingTargeting`, `targetedCustomers`, `targetedRevenue`, `warning`

- serves P09 ADM-198 Targeting & Eligibility Command Center

**Decision:** 

### p95  · `setEligibilityRule`

`PUT /eligibility-rule` · PRICE_CONFIGURE · staff · **Eligibility Rule Builder**

> Provide a no-code rule engine for determining promotion eligibility.

**`EligibilityRuleBuilderView`** — `ageCategory`, `campaign`, `channel`, `customerAccountAttributes`, `customerSegment`, `dateTime`, `exclude`, `guestType`, `include`, `location`, `loyaltyTier`, `membership`, `multipleConditionSets`, `nestedGroups`, `partner`, `paymentMethod`, `productPurchased`, `purchaseHistory`, `transactionValue`, `venue`, `visitHistory`

- serves P09 ADM-199 Eligibility Rule Builder
- serves P09 ADM-279 Resale Eligibility Rule Configuration

**Decision:** 

### p96  · `listCrmCustomerSegment`

`GET /crm-customer-segment` · PRICE_VIEW · staff · **CRM & Customer Segment Manager**

> Connect promotion eligibility directly to TICVAI CRM segmentation. The board should consume CRM segments rather than recreate CRM functionality.

**`CrmCustomerSegmentManagerView`** — `b2bAccounts`, `conversion`, `estimatedAudience`, `externalCdp`, `externalCrm`, `importedSegment`, `lastRefreshed`, `loyalty`, `marketingAutomation`, `membership`, `promotionsUsingSegment`, `revenue`, `segmentName`, `source`, `status`, `ticvaiCrm`

- serves P09 ADM-200 CRM & Customer Segment Manager

**Decision:** 

### p97  · `listMembershipLoyaltyGuest`

`GET /membership-loyalty-guest` · PRICE_VIEW · staff · **Membership, Loyalty & Guest Eligibility**

> Configure targeting based on membership, loyalty status, guest categories, and entitlement relationships.

**`MembershipLoyaltyGuestEligibilityView`** — `adult`, `bronze5`, `child`, `expiryDate`, `family`, `fit`, `gold15`, `group`, `loyaltyActivity`, `loyaltyTier`, `membershipStartDate`, `membershipStatus`, `membershipTenure`, `membershipTier`, `membershipType`, `pointsBalance`, `pointsEarned`, `pointsRedeemed`, `renewalStatus`, `resident`, `senior`, `silver10`, `student`, `tierProgression`, `tourist`, `vip`

> ⚠ **26 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P09 ADM-201 Membership, Loyalty & Guest Eligibility

**Decision:** 

### p98  · `listBehavioralTransactionTargeting`

`GET /behavioral-transaction-targeting` · PRICE_VIEW · staff · **Behavioral & Transaction Targeting**

> Target promotions according to what the guest has previously purchased or done.

**`BehavioralTransactionTargetingView`** — `abandonedCart`, `averageBasket`, `averageTransactionValue`, `bookingFrequency`, `customPeriod`, `daysSinceLastVisit`, `last7Days`, `lastPurchase`, `lifetime`, `lifetimeSpend`, `numberOfTransactions`, `previousAttractionVisited`, `previousProductPurchased`, `previousPromotionRedemption`, `productAffinity`, `productMix`, `purchaseChannel`, `purchaseFrequency`, `totalCustomerValue`, `visitFrequency`

- serves P09 ADM-202 Behavioral & Transaction Targeting

**Decision:** 

### p99  · `listContextLocationChannel`

`GET /context-location-channel` · PRICE_VIEW · staff · **Context, Location, Channel & Time Targeting**

> Determine promotion eligibility according to the customer's current commercial context.

**`ContextLocationChannelTimeTargetingView`** — `api`, `attraction`, `b2b`, `b2cWebsite`, `businessEntity`, `callCenter`, `campaignPeriod`, `currentBasket`, `currentBooking`, `day`, `event`, `holiday`, `inVenueStateWhereAvailable`, `kiosk`, `marketCountry`, `mobileApp`, `mobilePos`, `operatingArea`, `ota`, `partner`, `pos`, `productCurrentlyViewed`, `purchaseDate`, `reseller`, `salesLocation`, `season`, `time`, `venue`, `visitDate`, `visitState`

> ⚠ **30 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P09 ADM-203 Context, Location, Channel & Time Targeting

**Decision:** 

### p100 · `listPartnerPaymentEligibility`

`GET /partner-payment-eligibility` · PRICE_VIEW · staff · **Partner, B2B & Payment Eligibility**

> Configure eligibility for partner, corporate, reseller, B2B, and payment-related campaigns.

**`PartnerB2bPaymentEligibilityView`** — `approvedPaymentPartner`, `b2bAccount`, `bank`, `contract`, `corporateAccount`, `customerGroup`, `eligibleCardProgram`, `employer`, `giftCard`, `governmentEntity`, `hotel`, `loyaltyPayment`, `market`, `masterAccount`, `partner`, `partnerCategory`, `paymentMethod`, `salesChannel`, `school`, `subAccount`, `tourOperator`, `travelAgency`, `wallet`

- serves P09 ADM-204 Partner, B2B & Payment Eligibility

**Decision:** 

### p101 · `listAudiencePreviewReach`

`GET /audience-preview-reach` · PRICE_VIEW · staff · **Audience Preview, Reach & Eligibility Simulator**

> Allow administrators to understand exactly who will qualify before activating the targeting rule. This is a critical safeguard.

**`AudiencePreviewReachEligibilitySimulatorView`** — `estimatedAudience`, `estimatedPromotionCost`, `estimatedRevenue`, `expectedRedemptions`, `historicalAov`, `historicalConversion`, `mobileAppEnabled`, `percentageOfCustomerBase`, `profileAEligible`, `profileBNotEligible`

- serves P09 ADM-205 Audience Preview, Reach & Eligibility Simulator

**Decision:** 

### p102 · `listTargetingConflictFrequency`

`GET /targeting-conflict-frequency` · PRICE_VIEW · staff · **Targeting Conflict, Frequency & Exclusion Controls**

> Prevent customers from being over-targeted and prevent inappropriate promotional eligibility.

**`TargetingConflictFrequencyExclusionControlsView`** — `accountType`, `alreadyPurchasedProduct`, `alreadyRedeemedPromotion`, `campaignExclusions`, `coolingOffPeriod`, `employee`, `existingMember`, `fraudRiskStatus`, `maximumCampaignsPerMonth`, `maximumOffersPerDay`, `maximumOffersPerWeek`, `maximumRedemptions`, `operationalExclusions`, `partnerExclusions`, `partnerRestriction`, `productOwnership`, `repeatCampaignRestriction`, `specificCrmSegment`

- serves P09 ADM-206 Targeting Conflict, Frequency & Exclusion Controls

**Decision:** 

### p103 · `listAudienceDiscoveryTargeting`

`GET /audience-discovery-targeting` · PRICE_VIEW · staff · **AI Audience Discovery & Targeting Optimization**

> Use TICVAI's AI layer to identify customer audiences and promotion opportunities that business users may not have manually defined.

**`AiAudienceDiscoveryTargetingOptimizationView`** — `audience48260`, `audienceSize126500`, `auditEligibilityRuleChanges`, `auditSegmentUse`, `bundleEngineBoards56`, `bundleTargeting`, `campaignAudienceActivation`, `changeChannel`, `changeEligibility`, `changePromotion`, `changeTiming`, `channelLocationPartnerRestrictions`, `codeBasedEligibility`, `commercialBenefits`, `contextAndChannel`, `couponEngineBoard3`, `customerAccountSpecificPromotionConditions`, `customerGuestEligibilityAndTargetedDiscounts`, `doesThisCustomerQualify`, `estimatedIncrementalRevenueAed740k`, `excludeLowValueSegment`, `expandAudience`, `individualCustomerIdentities`, `matrixCoverageBoard7`, `membershipAndLoyaltyEligibility`, `membershipTierEligibility`, `narrowAudience`, `partnerAccountEligibility`, `paymentMethodEligibility`, `performanceAndPredictiveTargeting`, `predictedConversion128`, `productRelationships`, `purchasedAquariumAdmission`, `reduceFrequency`, `respectConfiguredMarketingSuppression`, `respectCustomerConsentPreferencesWhereApplicable`, `suggestedOffer15AquariumDiscount`, `useOnlyPermittedCustomerAttributes`, `whatCommercialBenefitApplies`, `whyThisAudience`

> ⚠ **40 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P08 BO-761 AI Audience Discovery
- serves P09 ADM-207 AI Audience Discovery & Targeting Optimization

**Decision:** 

### p109 · `listStackingConflict`

`GET /stacking-conflict` · PRICE_VIEW · staff · **Stacking & Conflict Command Center**

> Provide centralized operational visibility into promotion interactions across TICVAI.

**`StackingConflictCommandCenterView`** — `activePromotionRules`, `autoResolvedConflicts`, `averagePromotionsPerTransaction`, `conflictsDetected`, `critical`, `criticalConflicts`, `discountExposure`, `exclusivePromotions`, `high`, `information`, `preventedOverDiscount`, `priorityRules`, `promotionType`, `revenueProtected`, `stackablePromotions`, `transactionsWithMultipleOffers`, `warning`

- serves P09 ADM-208 Stacking & Conflict Command Center

**Decision:** 

### p110 · `listPromotionPriorityHierarchy`

`GET /promotion-priority-hierarchy` · PRICE_VIEW · staff · **Promotion Priority & Hierarchy Manager**

> Define the relative priority of different promotion families and individual offers.

**`PromotionPriorityHierarchyManagerView`** — `businessEntity`, `campaign`, `channel`, `customerSegment`, `customerType`, `effectiveDates`, `priority200`, `priority300`, `priorityGroup`, `priorityNumber`, `productCategory`, `promotion`, `promotionFamily`, `tenant`, `venue`

- serves P09 ADM-209 Promotion Priority & Hierarchy Manager

**Decision:** 

### p111 · `setPromotionStackingRule`

`PUT /promotion-stacking-rule` · PRICE_CONFIGURE · staff · **Promotion Stacking Rule Builder**

> Define which promotions can be combined.

**`PromotionStackingRuleBuilderView`** — `bundleComponent`, `but`, `channel`, `couponDiscount`, `customer`, `entireTransaction`, `individualTicket`, `onlyOnePromotionCanApply`, `product`, `productCategory`, `promotionAPromotionB`

- serves P09 ADM-148 Promotion Rule Builder
- serves P09 ADM-210 Promotion Stacking Rule Builder

**Decision:** 

### p112 · `listPromotionExclusionCompatibility`

`GET /promotion-exclusion-compatibility` · PRICE_VIEW · staff · **Promotion Exclusion & Compatibility Matrix**

> Provide administrators with a visual matrix showing which promotion categories can interact.

**`PromotionExclusionCompatibilityMatrixView`** — `allowed`, `applicableProducts`, `applicableVenues`, `channels`, `conditional`, `customerSegments`, `effectiveDates`, `exceptions`, `nHipTyKO`, `notAllowed`, `notConfigured`, `priority`, `priorityBased`, `rule`

- serves P09 ADM-211 Promotion Exclusion & Compatibility Matrix

**Decision:** 

### p113 · `listDiscountCalculationApplication`

`GET /discount-calculation-application` · PRICE_VIEW · staff · **Discount Calculation & Application Sequence**

> Control the mathematical order in which multiple permitted benefits are calculated.

**`DiscountCalculationApplicationSequenceView`** — `additivePercentage`, `aed100Aed70`, `aed100Aed80`, `aed80Aed72`, `afterFee`, `afterTax`, `beforeFee`, `beforeTax`, `bestPriceOnly`, `fixedThenPercentage`, `highestValueDiscountOnly`, `lowestPriceResult`, `percentageThenFixed`, `priorityOrder`, `productOnly`, `sequential`, `then10`, `transactionTotal`

- serves P09 ADM-212 Discount Calculation & Application Sequence

**Decision:** 

### p114 · `listBestOfferCustomer`

`GET /best-offer-customer` · PRICE_VIEW · staff · **Best Offer & Customer Benefit Resolver**

> Determine which promotion or combination gives the guest the correct/best permitted commercial outcome.

**`BestOfferCustomerBenefitResolverView`** — `bank1011750`, `bestAvailableOfferAppliedAutomatically`, `family15Aed`, `favorAStrategicallySelectedCampaign`, `honorContractualCustomerSpecificPricingFirst`, `saving`, `useTheHighestRankedPromotion`

- serves P09 ADM-213 Best Offer & Customer Benefit Resolver

**Decision:** 

### p115 · `listDiscountCapMaximum`

`GET /discount-cap-maximum` · PRICE_VIEW · staff · **Discount Cap & Maximum Benefit Controller**

> Prevent stacked promotions from exceeding financial or contractual limits.

**`DiscountCapMaximumBenefitControllerView`** — `bank10`, `campaign`, `category`, `channel`, `configuredMaximum`, `coupon20`, `customer`, `maximumFreeItemValue`, `maximumPromotionalBenefit`, `maximumPromotionsPerBasket`, `maximumTotalDiscount`, `maximumTotalDiscountAmount`, `membership15`, `minimumMargin`, `minimumProductPrice`, `minimumTransactionValue`, `partner`, `potentialCombinedBenefit`, `product`, `reduceDiscount`, `requireApproval`, `tenant`, `transaction`, `useBestPermittedCombination`, `venue`

- serves P09 ADM-214 Discount Cap & Maximum Benefit Controller

**Decision:** 

### p116 · `listConflictDetectionResolution`

`GET /conflict-detection-resolution` · PRICE_VIEW · staff · **Conflict Detection & Resolution Center**

> Detect promotion conflicts during both configuration and runtime.

**`ConflictDetectionResolutionCenterView`** — `automatic`, `bank10`, `bestPrice`, `circularDependency`, `discountCapBreach`, `family20`, `incompatiblePromotions`, `manualIntervention`, `missingHierarchy`, `missingStackingRule`, `priority`, `ruleBased`, `sameAudience`, `sameChannel`, `sameProduct`, `sameValidity`, `summer25`, `vip15`

- serves P09 ADM-215 Conflict Detection & Resolution Center

**Decision:** 

### p117 · `listPromotionDecisionTrace`

`GET /promotion-decision-trace` · PRICE_VIEW · staff · **Promotion Decision Trace & Transaction Explainer**

> Provide complete explainability of how TICVAI arrived at the final promotional price. This screen will be extremely important for: Customer service Finance Operations Audit Partner disputes Technical support

**`PromotionDecisionTraceTransactionExplainerView`** — `aed160`, `aed64`, `bank10`, `bank10StackableWithFamily20`, `bestPermittedCombinationCalculated`, `family20`, `family20Eligible`, `family20Retained`, `loyalty5`, `summer25`, `totalSaving`

- serves P09 ADM-216 Promotion Decision Trace & Transaction Explainer

**Decision:** 

### p118 · `listConflict`

`GET /conflict` · PRICE_VIEW · staff · **Conflict Simulation & AI Optimization**

> Test promotion interaction scenarios before publishing campaigns.

**`ConflictSimulationAiOptimizationView`** — `approver`, `areCommercialLimitsRespected`, `auditor`, `b2bManager`, `bankAbc10`, `basket`, `boards24PromotionMechanics`, `bogo29`, `bogoAed`, `bogoBank24`, `buy4Pay3`, `calculateAuthoritativeFinalPrice`, `campaignManager`, `channel`, `collectFinalAmount`, `commercialManager`, `coupon`, `coupon33`, `customerSegment`, `dateTime`, `estimatedProtectedMarginAed284kMonth`, `finance`, `gND`, `goldMember15`, `loyalty`, `margin`, `marketingAdministrator`, `member36`, `memberAed`, `membership`, `mutuallyExclusive`, `paymentMethod`, `paymentMethodOffers`, `products`, `revenueManager`, `sameCentralizedEngine`, `summer20`, `systemAdministrator`, `venue`, `whoQualifies`

> ⚠ **40 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P09 ADM-217 Conflict Simulation & AI Optimization

**Decision:** 

### p125 · `listCampaignGovernanceBudget`

`GET /campaign-governance-budget` · PRICE_VIEW · staff · **Campaign Governance & Budget Command Center**

> Provide executives, Marketing, Commercial, Revenue, and Finance with one centralized view of the financial and governance status of promotional campaigns.

**`CampaignGovernanceBudgetCommandCenterView`** — `activeCampaigns`, `budgetAed500000`, `budgetConsumed`, `budgetExhausted`, `campaignBudget`, `campaignRoi`, `campaignsNearBudgetLimit`, `consumedAed387500`, `critical`, `discountExposure`, `healthy`, `incrementalRevenue`, `monitor`, `pendingApprovals`, `redemptionValue`, `remainingAed112500`, `remainingBudget`, `revenueAed284m`, `revenueGenerated`, `roi53x`, `statusHealthy`, `suspended`, `suspendedCampaigns`, `utilization775`, `warning`

- serves P09 ADM-218 Campaign Governance & Budget Command Center

**Decision:** 

### p126 · `setCampaignBudgetFinancial`

`PUT /campaign-budget-financial` · PRICE_CONFIGURE · staff · **Campaign Budget & Financial Limit Setup**

> Define the financial envelope within which a campaign is permitted to operate.

**`CampaignBudgetFinancialLimitSetupView`** — `budgetAmount`, `budgetOwner`, `businessEntity`, `campaign`, `channel`, `costCenter`, `currency`, `customerSegment`, `department`, `departmentBudget`, `discountBudget`, `effectiveDates`, `entireCampaign`, `freeProductBudget`, `fundingSource`, `marketingFundedBudget`, `partner`, `partnerFundedBudget`, `product`, `promotion`, `rewardBudget`, `totalCampaignBudget`, `venue`, `venueBudget`

- serves P09 ADM-219 Campaign Budget & Financial Limit Setup

**Decision:** 

### p128 · `listRedemptionDiscountExposure`

`GET /redemption-discount-exposure` · PRICE_VIEW · staff · **Redemption, Discount & Exposure Limit Manager**

> Define non-budget commercial limits controlling campaign exposure.

**`RedemptionDiscountExposureLimitManagerView`** — `dailyRedemptionLimit`, `maximumCustomerRedemption`, `maximumRedemptions`, `orCustomThresholds`, `typesType`

- serves P09 ADM-220 Redemption, Discount & Exposure Limit Manager

**Decision:** 

### p129 · `listBudgetConsumptionForecast`

`GET /budget-consumption-forecast` · PRICE_VIEW · staff · **Budget Consumption & Forecast Monitor**

> Provide real-time tracking of campaign financial consumption and predict when limits will be reached.

**`BudgetConsumptionForecastMonitorView`** — `committed`, `completedTransaction`, `consumed`, `dailyBurnRate`, `forecastFinalSpend`, `originalBudget`, `remaining`, `reserved`

- serves P09 ADM-221 Budget Consumption & Forecast Monitor

**Decision:** 

### p130 · `listThresholdActionAutomatic`

`GET /threshold-action-automatic` · PRICE_VIEW · staff · **Threshold Actions & Automatic Suspension**

> Define what TICVAI should do as financial or redemption thresholds are approached or exceeded. This is explicitly required by the matrix.

**`ThresholdActionsAutomaticSuspensionView`** — `allowGraceAmount`, `continueWithExecutiveAuthorization`, `reduceAllocation`, `requireApproval`, `stopCampaign`, `stopPartner`, `stopPromotion`, `stopSpecificChannel`, `warn`

- serves P09 ADM-222 Threshold Actions & Automatic Suspension

**Decision:** 

### p131 · `approveCampaignWorkflow`

`PUT /campaign-workflow` · PRICE_CONFIGURE · staff · **Campaign Approval Workflow Designer**

> Configure multi-level approval workflows for promotions and campaigns. The matrix explicitly requires configurable multi-level approval for promotion creation, modification, activation, and deactivation.

**`CampaignApprovalWorkflowDesignerView`** — `campaignBudget`, `campaignDuration`, `channel`, `conditionalApproval`, `delegation`, `discount`, `discount1025`, `escalation`, `financialExposure`, `freeProductValue`, `mandatoryApproval`, `margin`, `optionalReview`, `parallelApproval`, `partner`, `promotionType`, `sequentialApproval`, `venue`

- serves P08 BO-770 Campaign Approval Workflow
- serves P09 ADM-223 Campaign Approval Workflow Designer

**Decision:** 

### p132 · `approveDecision`

`PUT /decision` · PRICE_CONFIGURE · staff · **Approval Inbox & Decision Workspace**

> Provide approvers with enough commercial information to make an informed decision without navigating through every configuration screen.

**`ApprovalInboxDecisionWorkspaceView`** — `aed500kAed750k`, `aiForecast`, `budget`, `campaign`, `commercial`, `customerReach`, `delegate`, `discount`, `estimatedRedemptions`, `estimatedRevenue`, `marginImpact`, `marketing`, `promotion`, `requestDate`, `requestInformation`, `requestedAction`, `requestedBy`, `returnForChange`, `riskLevel`

- serves P08 BO-374 Approval Decision Workspace
- serves P08 BO-642 Approval Decision History
- serves P09 ADM-224 Approval Inbox & Decision Workspace

**Decision:** 

### p133 · `listCampaignFinancialCommercial`

`GET /campaign-financial-commercial` · PRICE_VIEW · staff · **Campaign Financial & Commercial Simulator**

> Simulate the likely financial result of a campaign before activation. This is a major matrix requirement.

**`CampaignFinancialCommercialSimulatorView`** — `audience`, `averageOrderValue`, `budget`, `channels`, `discount`, `discountCost`, `duration`, `eligibleAudience`, `expectedBudgetConsumption`, `expectedRedemptions`, `expectedTraffic`, `expectedTransactions`, `grossMargin`, `grossRevenue`, `historicalConversion`, `incrementalRevenue`, `marginImpact`, `netRevenue`, `products`, `promotion`, `redemptionLimit`, `roi`

- serves P09 ADM-225 Campaign Financial & Commercial Simulator

**Decision:** 

### p134 · `listCampaignExperimentTest`

`GET /campaign-experiment-test` · PRICE_VIEW · staff · **Campaign Experiment & A/B Test Manager**

> Allow TICVAI to test campaign variants and determine which commercial strategy performs better. The matrix explicitly requires A/B testing of promotion variants, including discount levels, validity periods, bundles, and target segments.

**`CampaignExperimentABTestManagerView`** — `a40`, `aiRecommendation`, `aov`, `audience`, `b40`, `bundle`, `channel`, `control20`, `conversion`, `discount`, `discountCost`, `discountValue`, `freeFBVoucher`, `incrementalRevenue`, `manualWinner`, `margin`, `messageOffer`, `promotionType`, `redemption`, `revenue`, `reward`, `roi`, `ruleBasedWinner`, `timing`, `validity`

- serves P09 ADM-226 Campaign Experiment & A/B Test Manager

**Decision:** 

### p136 · `listGovernanceRiskLaunch`

`GET /governance-risk-launch` · PRICE_VIEW · staff · **Governance Audit, AI Risk & Launch Readiness**

> Provide the final governance checkpoint before a campaign is allowed to go live.

**`GovernanceAuditAiRiskLaunchReadinessView`** — `actualTransactionValues`, `aiRecommends`, `approvalAuthority`, `approvalDecisions`, `approvalSubmissions`, `audienceAndHistoricalResponse`, `audienceSize`, `auditRequirements`, `automaticSuspension`, `board7Targeting`, `board8Stacking`, `boards24PromotionMechanics`, `boards56Bundles`, `budget`, `budgetAccountingAndProfitability`, `budgetChange`, `budgetCreation`, `bundleFinancialImpact`, `campaignLaunch`, `campaignOperationalStatus`, `channelPublication`, `combinedDiscountExposure`, `discountRewardExposure`, `eligibility`, `experimentChanges`, `forecastsAndCampaignAnalytics`, `humanDecides`, `level1Advisory`, `level2GovernedAutomation`, `limitChanges`, `marginGuardrail`, `overrides`, `priceAndMargin`, `promotionConfiguration`, `reactivation`, `redemptionLimits`, `requiredApproval`, `simulationCompleted`, `simulationResults`, `stackingRules`

> ⚠ **40 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P09 ADM-227 Governance Audit, AI Risk & Launch Readiness
- serves P09 ADM-365 Risk & Governance Analytics

**Decision:** 

### p142 · `listPromotionPerformance`

`GET /promotion-performance` · PRICE_VIEW · staff · **Promotion Performance Command Center**

> Provide executives, Marketing, Commercial, Revenue, and Finance with the overall performance of promotions and bundles.

**`PromotionPerformanceCommandCenterView`** — `activeCampaigns`, `attraction`, `averageOrderValue`, `bundle`, `businessEntity`, `campaign`, `channel`, `conversionRate`, `currency`, `customerSegment`, `dateRange`, `discountGranted`, `estimatedIncrementalRevenue`, `grossMargin`, `grossSales`, `market`, `netRevenue`, `overTime`, `partner`, `product`, `promotion`, `promotionCost`, `promotionInfluencedRevenue`, `redemptions`, `revenuePerRedemption`, `roi`, `transactions`, `venue`

> ⚠ **28 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P09 ADM-146 Promotion Health & Performance Monitor
- serves P09 ADM-228 Promotion Performance Command Center
- serves P09 ADM-229 Campaign & Promotion Performance Explorer

**Decision:** 

### p143 · `listCampaignPromotionPerformance`

`GET /campaign-promotion-performance` · PRICE_VIEW · staff · **Campaign & Promotion Performance Explorer**

> Allow users to compare every promotion and campaign using consistent commercial KPIs.

**`CampaignPromotionPerformanceExplorerView`** — `aed38`, `aed41`, `aov`, `app1092k310k34132`, `conversion`, `critical`, `customerAcquisition`, `discount`, `excellent`, `family20310k740k29118`, `healthy`, `margin`, `marginRisk`, `monitor`, `redemptions`, `repeatPurchase`, `revenue`, `roi`, `subjectToUserPermissions`, `summer1Aed26`, `transactions`, `underperforming`, `units`

- serves P09 ADM-139 Promotion & Campaign Directory
- serves P09 ADM-228 Promotion Performance Command Center
- serves P09 ADM-229 Campaign & Promotion Performance Explorer

**Decision:** 

### p144 · `listRedemptionConversionFunnel`

`GET /redemption-conversion-funnel` · PRICE_VIEW · staff · **Redemption, Conversion & Funnel Analytics**

> Measure how effectively offers move customers from exposure to purchase and redemption.

**`RedemptionConversionFunnelAnalyticsView`** — `abandonment`, `cartRate`, `conversionRate`, `engagementRate`, `expiredBenefitRate`, `exposureRate`, `redemptionRate`, `unusedPromotionRate`

- serves P09 ADM-230 Redemption, Conversion & Funnel Analytics

**Decision:** 

### p145 · `listDiscountMarginProfitability`

`GET /discount-margin-profitability` · PRICE_VIEW · staff · **Discount, Margin & Profitability Analytics**

> Determine whether promotions are commercially profitable rather than merely generating sales.

**`DiscountMarginProfitabilityAnalyticsView`** — `discountValue`, `grossMargin`, `grossProfit`, `grossRevenue`, `highRevenueHighMargin`, `highRevenueLowMargin`, `lowRevenueHighMargin`, `lowRevenueLowMargin`, `marginChange`, `netRevenue`, `productCost`, `profitUplift`, `promotionCost`, `revenueUplift`, `roi`, `toIdentify`

- serves P09 ADM-231 Discount, Margin & Profitability Analytics

**Decision:** 

### p146 · `listBundleBogoAdvanced`

`GET /bundle-bogo-advanced` · PRICE_VIEW · staff · **Bundle, BOGO & Advanced Offer Analytics**

> Measure performance specifically for the commercial mechanics created in Boards 4–6.

**`BundleBogoAdvancedOfferAnalyticsView`** — `aquarium100`, `availabilityFailureRate`, `averageRewardValue`, `bogoTransactions`, `bundleAov`, `bundleConversion`, `bundleMargin`, `bundleRevenue`, `bundleSales`, `bundleVsStandaloneRevenue`, `componentAttachRate`, `componentRedemption`, `freeItemsIssued`, `incrementalRevenue`, `incrementalUnits`, `marginImpact`, `mealA68`, `mealB22`, `mealC10`, `parking42`, `photoAddOn31`, `substitutionRate`, `waterPark100`

- serves P09 ADM-232 Bundle, BOGO & Advanced Offer Analytics

**Decision:** 

### p147 · `listUpsellCrossSell`

`GET /upsell-cross-sell` · PRICE_VIEW · staff · **Upsell, Cross-Sell & Attach-Rate Analytics**

> Measure whether promotions and bundles successfully increase the customer's basket beyond the original purchase. This screen is particularly important for the cross-sale metrics you originally raised.

**`UpsellCrossSellAttachRateAnalyticsView`** — `attachRate`, `crossCategoryConversion`, `crossSellRevenue`, `fBRetail`, `incrementalBasketValue`, `itemsPerTransaction`, `membershipExperience`, `recommendedOfferAcceptance`, `retailFB`, `revenuePerTransaction`, `ticketExperience`, `ticketFB`, `ticketMembership`, `ticketRetail`, `ticketTicket`, `upsellRevenue`

- serves P09 ADM-233 Upsell, Cross-Sell & Attach-Rate Analytics
- serves P09 ADM-659 Cross-Sell Command Center

**Decision:** 

### p148 · `listCustomerSegmentChannel`

`GET /customer-segment-channel` · PRICE_VIEW · staff · **Customer, Segment, Channel & Partner Analytics**

> Determine which audiences and distribution channels respond best to promotions.

**`CustomerSegmentChannelPartnerAnalyticsView`** — `aed32`, `aed44`, `aov`, `api`, `b2b`, `b2c`, `callCenter`, `campaignRoi`, `commission`, `conversion`, `customersReached`, `discount`, `discountCost`, `families14229`, `kiosk`, `margin`, `memberAed51`, `mobileApp`, `netContribution`, `newCustomers`, `ntOnN`, `ota`, `partnerRedemptions`, `partnerRevenue`, `pos`, `redemption`, `repeatPurchase`, `reseller`, `returningCustomers`, `revenue`, `s710X`, `tourists9834`

> ⚠ **32 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P09 ADM-234 Customer, Segment, Channel & Partner Analytics

**Decision:** 

### p149 · `listIncrementalityAttributionCannibalization`

`GET /incrementality-attribution-cannibalization` · PRICE_VIEW · staff · **Incrementality, Attribution & Cannibalization Analysis**

> Incrementality, Attribution & Cannibalization Analysis

**`IncrementalityAttributionCannibalizationAnalysisView`** — `aBTestAttribution`, `aed12m`, `aed38m`, `aed50m`, `aiEstimatedIncrementality`, `campaignAttribution`, `channelMigrationCausedByDiscounting`, `controlGroupComparison`, `directAttribution`, `higherMarginBundleLowerMarginPromotion`, `matchedAudienceAnalysis`, `prePostComparison`, `promotionCodeAttribution`, `standardTicketDiscountedTicket`

- serves P09 ADM-235 Incrementality, Attribution & Cannibalization Analysis

**Decision:** 

### p150 · `listNextBestAction`

`GET /next-best-action` · PRICE_VIEW · staff · **AI Optimization & Next-Best-Action Center**

> Turn analytics into actionable commercial recommendations. This should be one of the strongest AI screens in the Promotions module.

**`AiOptimizationNextBestActionCenterView`** — `acceptAsDraft`, `changeBundlePrice`, `changeDay`, `changeMechanic`, `changeThreshold`, `changeTime`, `endPromotion`, `excludeSegment`, `expandChannel`, `expandSegment`, `grossProfitAed186k`, `increaseDiscount`, `narrowSegment`, `reallocateCampaignBudget`, `reduceCampaignDuration`, `reduceDiscount`, `restrictChannel`, `revenueAed42k`, `simulate`, `snooze`

- serves P09 ADM-236 AI Optimization & Next-Best-Action Center

**Decision:** 

### p151 · `listExecutivePromotionReporting`

`GET /executive-promotion-reporting` · PRICE_VIEW · staff · **Executive Promotion Intelligence & Reporting Studio**

> Provide executive reporting and configurable analytics output across the complete Promotions & Bundles module.

**`ExecutivePromotionIntelligenceReportingStudioView`** — `accordingToConfiguredFinancialRules`, `aov`, `api`, `auditor`, `b2b`, `by`, `commercial`, `comparisonPeriod`, `conversion`, `crm`, `csv`, `dashboards`, `dataAnalyst`, `date`, `dimension`, `excel`, `executive`, `familySegmentConversion142`, `finance`, `grouping`, `highDiscountCost`, `higherValueOption`, `incrementalRevenue`, `lowConversion`, `lowIncrementality`, `marketing`, `metric`, `negativeMarginImpact`, `pdf`, `powerBi`, `productRelationship`, `profit`, `revenueManagement`, `reward`, `roi`, `scheduledReport`, `systemAdministrator`, `transactionPromotionEvents`, `venueManagement`, `visualization`

> ⚠ **40 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P09 ADM-237 Executive Promotion Intelligence & Reporting Studio

**Decision:** 

