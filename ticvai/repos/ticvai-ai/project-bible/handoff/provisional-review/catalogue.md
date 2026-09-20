# catalogue — 108 operations awaiting sign-off

> **These are specified, not unfinished.** Each has a request, a response and a citation of
> the pack page it was read from. `x-ticvai-provisional` means **nobody who has to build it
> has agreed it** — so the only thing that closes one is a decision in this column: *agreed*,
> *corrected* (say how), or *not needed*.

**3 pack(s), read in page order.** A session opens a book and walks it.

- Pricing Revenue Management — **70**
- Sales Channel Management — **20**
- Product Lifecycle Catalogue Governance — **18**


---

## Pricing Revenue Management

### p6   · `listCommercialPricing`

`GET /commercial-pricing` · PRODUCT_VIEW · staff · **Commercial Pricing Command Center**

> Provide the central administrative workspace for all commercial pricing structures across This is the first page a Revenue/Pricing Administrator sees when entering the module.

**`CommercialPricingCommandCenterView`** — `activePriceLists`, `brand`, `code`, `configuredRates`, `currencies`, `currency`, `draftPriceLists`, `effectivePeriod`, `market`, `markets`, `modifyPricingStructure`, `name`, `owner`, `priceCategories`, `priceListId`, `pricingValidationIssues`, `productCount`, `productsMissingPricing`, `productsWithPricing`, `rateCount`, `recentlyModifiedPriceLists`, `status`, `totalPriceLists`, `type`, `upcomingPriceStructures`, `venue`, `version`

> ⚠ **27 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P08 BO-533 Pricing Simulation, Validation & AI Commercial Intelligence
- serves P09 ADM-048 Commercial Pricing Command Center

**Decision:** 

### p8   · `setPriceListMaster`

`PUT /price-list-master` · PRODUCT_CONFIGURE · staff · **Price List Master Configuration**

> Create the master container that holds commercial rates. A Price List should be reusable across products and channels.

**`PriceListMasterConfigurationView`** — `allowInheritance`, `allowMultipleCurrencies`, `allowOverrides`, `allowProductSpecificRates`, `brand`, `businessUnit`, `country`, `defaultCurrency`, `defaultPriceHierarchy`, `defaultRateCategory`, `defaultRoundingProfile`, `description`, `event`, `global`, `into`, `legalEntity`, `market`, `owner`, `priceListCode`, `priceListName`, `priceListType`, `status`, `tags`, `venue`

- serves P09 ADM-049 Price List Master Configuration

**Decision:** 

### p9   · `listPriceCategoryRate`

`GET /price-category-rate` · PRODUCT_VIEW · staff · **Price Category & Rate Type Library**

> Define standardized commercial rate categories used across TICVAI. This avoids different venues independently creating categories such as: “Adult,” “Adult Standard,” “Normal Adult,” and “Full Adult.”

**`PriceCategoryRateTypeLibraryView`** — `activeInactive`, `adult`, `b2b`, `categoryFamily`, `categoryId`, `child`, `code`, `complimentary`, `corporate`, `custom`, `description`, `displayName`, `group`, `iconLabel`, `junior`, `member`, `name`, `nonResident`, `promotional`, `resident`, `senior`, `staff`, `student`, `vip`

- serves P09 ADM-050 Price Category & Rate Type Library

**Decision:** 

### p11  · `setRateStructure`

`PUT /rate-structure` · PRODUCT_CONFIGURE · staff · **Rate Structure Builder**

> Define the actual monetary rates contained within a price list. This is the core commercial configuration screen.

**`RateStructureBuilderView`** — `amount`, `childReduced`, `circularRateRelationship`, `currency`, `d250`, `groupGroup`, `invalidDerivedRate`, `missingAmounts`, `perDay`, `perHour`, `perMembershipPeriod`, `perPackage`, `perPerson`, `perResource`, `perSession`, `perTicket`, `perUnit`, `precision`, `priceCategory`, `rateCode`, `rateId`, `rateName`, `rateType`, `residentReduced`, `roundingProfile`, `seniorReduced`, `status`, `unitBasis`, `unsupportedCurrency`

> ⚠ **29 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P09 ADM-051 Rate Structure Builder

**Decision:** 

### p13  · `setProductServicePrice`

`PUT /product-service-price` · PRODUCT_CONFIGURE · staff · **Product & Service Price Assignment**

> Connect commercial rates to the actual products and services being sold.

**`ProductServicePriceAssignmentView`** — `addOn`, `admission`, `andAssign`, `annualPass`, `event`, `experience`, `fBItem`, `membership`, `otherSellableService`, `performance`, `productLevel`, `productVariant`, `rentalItem`, `reservationService`, `resource`, `retailProduct`, `ticketProduct`, `ticketType`, `uaeStandardAdmissionPriceList`, `venue`

- serves P09 ADM-052 Product & Service Price Assignment

**Decision:** 

### p14  · `listPackageBundleAdd`

`GET /package-bundle-add` · PRODUCT_VIEW · staff · **Package, Bundle & Add-On Pricing**

> Provide dedicated commercial structures for products containing multiple components. This is separate from the Product Relationship/Bundle module. Product Catalogue defines what the bundle contains. Pricing defines how that bundle is priced.

**`PackageBundleAddOnPricingView`** — `additionalSession`, `componentOverride`, `componentPackageSaving`, `derivedPackagePrice`, `discountedComponentSum`, `equipment`, `fastTrack`, `fixedPackagePrice`, `includedComponent`, `individualComponents`, `meal`, `optionalPaidComponent`, `packageTotalOnly`, `parking`, `photo`, `premiumAccess`, `sumOfComponents`

- serves P09 ADM-053 Package, Bundle & Add-On Pricing

**Decision:** 

### p15  · `listMarketVenueCurrency`

`GET /market-venue-currency` · PRODUCT_VIEW · staff · **Market, Venue & Currency Pricing Structure**

> Support TICVAI's multi-country, multi-market, multi-venue and multi-currency commercial model.

**`MarketVenueCurrencyPricingStructureView`** — `aed250Sar255`, `baseCurrency`, `brand`, `conversions`, `country`, `currency`, `currencyPrecision`, `displayFormat`, `legalEntity`, `market`, `region`, `rounding`, `sellingCurrency`, `venue`

- serves P09 ADM-054 Market, Venue & Currency Pricing Structure

**Decision:** 

### p17  · `setPriceHierarchyInheritance`

`PUT /price-hierarchy-inheritance` · PRODUCT_CONFIGURE · staff · **Price Hierarchy & Inheritance Configuration**

> Define where TICVAI should obtain a price when multiple commercial pricing layers exist. This is essential to prevent conflicting prices.

**`PriceHierarchyInheritanceConfigurationView`** — `fallbackBehavior`, `hierarchyLevel`, `inheritance`, `maximumOverrideRange`, `priority`, `returnToParentPrice`

- serves P09 ADM-055 Price Hierarchy & Inheritance Configuration

**Decision:** 

### p18  · `listPriceListTemplate`

`GET /price-list-template` · PRODUCT_VIEW · staff · **Price List Templates, Clone & Reuse**

> Accelerate commercial setup across new venues, events, seasons and markets.

**`PriceListTemplatesCloneReuseView`** — `completePriceList`, `currencyStructure`, `existingTicvaiConfiguration`, `hierarchy`, `marketStructure`, `optionsType`, `packagePricingPattern`, `priceCategories`, `productAssignments`, `productMappingPattern`, `productPortfolio`, `rateMatrixStructure`, `rateStructureOnly`, `rateTypes`, `selectedCategories`, `similarVenues`, `venueType`

- serves P09 ADM-056 Price List Templates, Clone & Reuse

**Decision:** 

### p19  · `listCommercialPricingStructure`

`GET /commercial-pricing-structure` · PRODUCT_VIEW · staff · **Commercial Pricing Structure Validation**

> Validate that the commercial pricing foundation is structurally complete before it proceeds to rule configuration, governance, or publication. This is not the final publication screen. Board 4 owns approval and publication.

**`CommercialPricingStructureValidationView`** — `calculation`, `calculationEngine`, `categoriesConfigured`, `componentPricingValid`, `currencyAndVenueConfigurationValid`, `currencyDefined`, `derivedRelationshipsValid`, `doesNotPerformDynamicPricing`, `fallbackConfigured`, `monetaryValuesValid`, `noConflictingSourcePriority`, `noOrphanAssignments`, `optimizationSuggestion`, `ownershipAssigned`, `requiredFieldsComplete`, `requiredProductsPriced`, `revenueOptimization`, `saleCannotProceed`

- serves P09 ADM-048 Commercial Pricing Command Center
- serves P09 ADM-057 Commercial Pricing Structure Validation

**Decision:** 

### p23  · `listPricingRule`

`GET /pricing-rule` · PRODUCT_VIEW · staff · **Pricing Rule Command Center**

> Provide administrators with a centralized workspace for all pricing eligibility and contextual pricing rules. 23 | Pag e

**`PricingRuleCommandCenterView`** — `activePricingRules`, `channel`, `channelRules`, `corporateB2b`, `custom`, `customerScope`, `customerSegment`, `customerSegmentRules`, `dayOfWeek`, `draftRules`, `effectiveFrom`, `effectiveTo`, `event`, `group`, `location`, `locationRules`, `loyalty`, `membership`, `membershipRules`, `nationality`, `owner`, `priceList`, `priority`, `productScope`, `quantity`, `quantityRules`, `residency`, `residencyRules`, `ruleConflicts`, `ruleId`, `ruleName`, `ruleType`, `rulesExpiringSoon`, `seasonal`, `seasonalRules`, `status`, `testRule`, `timeslot`, `timeslotRules`, `venueLocation`

> ⚠ **40 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P09 ADM-058 Pricing Rule Command Center

**Decision:** 

### p25  · `listCustomerSegmentProfile`

`GET /customer-segment-profile` · PRODUCT_VIEW · staff · **Customer Segment & Profile Pricing Rules**

> Define price eligibility based on customer characteristics and commercial segments.

**`CustomerSegmentProfilePricingRulesView`** — `accountType`, `applicableProducts`, `b2bPartner`, `corporateAccount`, `corporateCustomer`, `crm`, `crmSegment`, `customerProfile`, `customerSegment`, `customerType`, `effectiveDates`, `employeeStaff`, `guestRegisteredUser`, `membership`, `partnerCustomer`, `priceList`, `priority`, `rate`, `ruleName`, `segment`, `status`, `vipStatus`

- serves P08 BO-737 Customer 360 Profile
- serves P09 ADM-059 Customer Segment & Profile Pricing Rules

**Decision:** 

### p26  · `listMembershipLoyaltyPricing`

`GET /membership-loyalty-pricing` · PRODUCT_VIEW · staff · **Membership & Loyalty Pricing Rules**

> Control member-specific and loyalty-tier pricing.

**`MembershipLoyaltyPricingRulesView`** — `activeSuspendedStatus`, `annualPassType`, `customerStatus`, `loyaltyProgram`, `loyaltyTier`, `member1Guest`, `memberFamily`, `memberOnly`, `membershipLevel`, `membershipProduct`, `membershipStatus`, `membershipTier`, `pointsBand`, `selectedQuantity`

- serves P09 ADM-060 Membership & Loyalty Pricing Rules

**Decision:** 

### p27  · `listResidencyNationalityMarket`

`GET /residency-nationality-market` · PRODUCT_VIEW · staff · **Residency, Nationality & Market Pricing Rules**

> Support geographically differentiated commercial pricing.

**`ResidencyNationalityMarketPricingRulesView`** — `accountProfile`, `country`, `customerAddress`, `customerDeclaration`, `governmentIdIntegrationWhereApplicable`, `governmentIdentityVerification`, `idUpload`, `market`, `nationality`, `region`, `residency`, `staffVerification`, `verifiedId`

- serves P09 ADM-061 Residency, Nationality & Market Pricing Rules

**Decision:** 

### p29  · `listChannelBasedPricing`

`GET /channel-based-pricing` · PRODUCT_VIEW · staff · **Channel-Based Pricing Rules**

> Determine which commercial rate applies based on sales channel.

**`ChannelBasedPricingRulesView`** — `channel`, `effectiveDates`, `market`, `priceList`, `priority`, `product`, `rate`, `relationshipWithSalesChannelManagement`, `startDate`, `venue`

- serves P09 ADM-062 Channel-Based Pricing Rules

**Decision:** 

### p30  · `listLocationVenueEvent`

`GET /location-venue-event` · PRODUCT_VIEW · staff · **Location, Venue & Event Pricing Rules**

> Allow rates to vary according to where and for which event/experience the product is sold.

**`LocationVenueEventPricingRulesView`** — `attraction`, `city`, `country`, `dubaiVenueAed275`, `effectiveDates`, `event`, `exhibition`, `experience`, `globalRateAed250`, `location`, `performance`, `popUpVenue`, `priority`, `product`, `rate`, `seasonalSite`, `specialEventAed320`, `temporaryEventLocation`, `venue`, `zone`

- serves P09 ADM-063 Location, Venue & Event Pricing Rules

**Decision:** 

### p31  · `listQuantityGroupVolume`

`GET /quantity-group-volume` · PRODUCT_VIEW · staff · **Quantity, Group & Volume Pricing Rules**

> Support commercial rates based on purchased quantity or group size.

**`QuantityGroupVolumePricingRulesView`** — `b2b`, `buyXRate`, `corporate`, `custom`, `family`, `groupMinimum`, `groupSize`, `groupType`, `maximumGroupSize`, `minimumQuantity`, `perPersonGroupRate`, `quantityBands`, `school`, `tour`, `volumeThreshold`

- serves P09 ADM-064 Quantity, Group & Volume Pricing Rules

**Decision:** 

### p32  · `listEffectiveDateSeason`

`GET /effective-date-season` · PRODUCT_VIEW · staff · **Effective Date, Season & Day-Based Pricing Rules**

> Control commercial price selection over time.

**`EffectiveDateSeasonDayBasedPricingRulesView`** — `blackoutDates`, `effectiveFrom`, `effectiveTo`, `eventPeriod`, `holidayPeriod`, `peakDates`, `publicHolidays`, `salesEnd`, `salesStart`, `schoolHolidays`, `season`, `specialDates`, `visitDateRange`

- serves P09 ADM-065 Effective Date, Season & Day-Based Pricing Rules

**Decision:** 

### p33  · `listTimeslotPerformanceTime`

`GET /timeslot-performance-time` · PRODUCT_VIEW · staff · **Timeslot, Performance & Time-of-Day Pricing Rules**

> Allow commercial pricing to differ across times within the same day or event.

**`TimeslotPerformanceTimeOfDayPricingRulesView`** — `arrivalWindow`, `conflictingPerformanceRule`, `earlyEntry`, `effectiveDates`, `eveningAed450`, `event`, `finalPerformanceAed550`, `lateEntry`, `matineeAed350`, `missingTimeslotRate`, `offPeak`, `overlappingTimeRanges`, `peak`, `performance`, `priceList`, `priority`, `product`, `rate`, `session`, `standard`, `startTime`, `timeOfDayBand`, `timeRange`, `timeslot`

- serves P09 ADM-066 Timeslot, Performance & Time-of-Day Pricing Rules

**Decision:** 

### p34  · `listPricingRulePriority`

`GET /pricing-rule-priority` · PRODUCT_VIEW · staff · **Pricing Rule Priority, Conflict Resolution & Testing**

> Define how TICVAI decides the final applicable rate when multiple pricing rules match. 34 | Pag e This is the critical control screen for Board 2.

**`PricingRulePriorityConflictResolutionTestingView`** — `amount`, `backendScreen`, `channel`, `channelB2c`, `channelBasedPricingRulesChannelPricing`, `circularFallback`, `continueProcessing`, `contradictoryRates`, `customer`, `customerGoldMember`, `date`, `dateSaturday`, `fallbackBehavior`, `goldMemberAed190`, `membership`, `missingFallback`, `overlappingTimeDateConditions`, `priority`, `product`, `productAdultAdmission`, `quantity`, `residency`, `residencyUae`, `samePriorityMatches`, `saturdayPeakAed280`, `specificity`, `standardAdultAed250`, `stopProcessing`, `time1800`, `timeslot`, `uaeResidentAed220`, `unreachableRule`, `venue`, `venueDubai`, `whatServiceFeeApplies`, `whatTaxApplies`

> ⚠ **36 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P09 ADM-058 Pricing Rule Command Center
- serves P09 ADM-067 Pricing Rule Priority, Conflict Resolution & Testing

**Decision:** 

### p39  · `listTaxFeeCalculation`

`GET /tax-fee-calculation` · PRODUCT_VIEW · staff · **Tax, Fee & Calculation Command Center**

> Provide Finance, Commercial and Pricing administrators with one central view of TICVAI's price-calculation configuration.

**`TaxFeeCalculationCommandCenterView`** — `activeFeeProfiles`, `activeSurcharges`, `activeTaxProfiles`, `calculationProfiles`, `configurationConflicts`, `country`, `currency`, `effectivePeriod`, `exemptionRules`, `legalEntity`, `market`, `owner`, `productScope`, `productsMissingCalculationProfile`, `productsMissingTax`, `profileName`, `recentlyModifiedRules`, `status`, `taxJurisdictions`, `type`, `upcomingTaxChanges`, `validationIssues`

- serves P09 ADM-068 Tax, Fee & Calculation Command Center

**Decision:** 

### p40  · `setTaxProfileJurisdiction`

`PUT /tax-profile-jurisdiction` · PRODUCT_CONFIGURE · staff · **Tax Profile & Jurisdiction Configuration**

> Define reusable tax profiles according to legal entity, country, jurisdiction and commercial context.

**`TaxProfileJurisdictionConfigurationView`** — `channelWhereLegallyApplicable`, `country`, `countryUae`, `currency`, `customRegulatoryTax`, `effectiveFrom`, `effectiveTo`, `entertainmentTax`, `gst`, `legalEntity`, `market`, `municipalityTax`, `owner`, `product`, `productCategory`, `rate5`, `regionJurisdiction`, `salesTax`, `service`, `serviceTax`, `status`, `taxProfileCode`, `taxProfileName`, `taxRegistrationNumber`, `taxType`, `taxTypeVat`, `tourismTax`, `vat`, `venue`, `whereDifferentRulesApply`

> ⚠ **30 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P09 ADM-069 Tax Profile & Jurisdiction Configuration

**Decision:** 

### p41  · `setTaxRuleTreatment`

`PUT /tax-rule-treatment` · PRODUCT_CONFIGURE · staff · **Tax Rule & Treatment Builder**

> Define how taxes are applied to products and transactions.

**`TaxRuleTreatmentBuilderView`** — `compound`, `country`, `customerTypeWhereLegallyRelevant`, `effectiveDate`, `exampleExclusive`, `exampleInclusive`, `fixedTax`, `legalEntity`, `multipleConcurrentTaxes`, `outOfScope`, `percentage`, `product`, `productCategory`, `salesChannelWhereLegallyRelevant`, `sequential`, `taxExclusive`, `taxExempt`, `taxInclusive`, `tiered`, `transactionType`, `venue`, `zeroRated`

- serves P09 ADM-070 Tax Rule & Treatment Builder

**Decision:** 

### p43  · `listFeeSurcharge`

`GET /fee-surcharge` · PRODUCT_VIEW · staff · **Fee & Surcharge Library**

> Create standardized reusable non-base-price charges.

**`FeeSurchargeLibraryView`** — `bookingFee`, `calculationMethod`, `cancellationFee`, `channelFee`, `convenienceFee`, `currency`, `customFee`, `customerVisible`, `deliveryFee`, `description`, `effectivePeriod`, `facilityFee`, `feeCode`, `feeName`, `feeType`, `fixedAmount`, `handlingFee`, `includedInDisplayPrice`, `internalOnly`, `modificationFee`, `paymentFee`, `perDay`, `perOrder`, `perPerson`, `perProduct`, `perTicket`, `perTransaction`, `percentage`, `refundability`, `reschedulingFee`, `serviceFee`, `shownSeparately`, `status`, `surcharge`, `taxTreatment`, `tiered`, `transactionFee`, `value`

> ⚠ **38 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P09 ADM-071 Fee & Surcharge Library

**Decision:** 

### p44  · `setFeeApplicabilityCharging`

`PUT /fee-applicability-charging` · PRODUCT_CONFIGURE · staff · **Fee Applicability & Charging Rule Builder**

> Determine when a fee or surcharge should apply. Screen 10.3.4 defines the fee. Screen 10.3.5 defines the conditions that trigger it.

**`FeeApplicabilityChargingRuleBuilderView`** — `channel`, `continueProcessing`, `country`, `customerType`, `deliveryMethod`, `event`, `excludeAnotherFee`, `market`, `membership`, `mutualExclusion`, `orderValue`, `paymentMethod`, `product`, `productCategory`, `quantity`, `rulePriority`, `serviceAction`, `stack`, `stopProcessing`, `transactionType`, `venue`

- serves P09 ADM-072 Fee Applicability & Charging Rule Builder

**Decision:** 

### p46  · `listFeeWaiverTax`

`GET /fee-waiver-tax` · PRODUCT_VIEW · staff · **Fee Waiver, Tax Exemption & Exception Rules**

> Govern circumstances under which a normally applicable tax or fee may be reduced, waived or exempted.

**`FeeWaiverTaxExemptionExceptionRulesView`** — `b2bContract`, `complimentaryTransaction`, `contractualWaiver`, `corporateAgreement`, `customerSegment`, `evidence`, `exemptionType`, `feeReduction`, `feeWaiver`, `legalExemption`, `loyaltyTier`, `membershipBenefit`, `operationalIssue`, `operationalWaiver`, `promotion`, `reasonMandatory`, `reference`, `serviceRecovery`, `staffRole`, `supervisorOverride`, `taxExemption`, `validity`, `verificationStatus`, `waiveAed25ModificationFee`, `zeroRatedTax`

- serves P09 ADM-073 Fee Waiver, Tax Exemption & Exception Rules

**Decision:** 

### p47  · `listPriceCalculationSequence`

`GET /price-calculation-sequence` · PRODUCT_VIEW · staff · **Price Calculation Sequence & Formula Engine**

> Define the exact sequence TICVAI follows to calculate the final payable amount. This is the heart of Board 3.

**`PriceCalculationSequenceFormulaEngineView`** — `aed20`, `conditional`, `customGovernedFormula`, `dependency`, `final`, `fixedAmount`, `formula`, `input`, `maximum`, `minimum`, `output`, `percentage`, `percentageOfBase`, `percentageOfSubtotal`, `rounding`, `sequence`, `serviceFee`, `taxability`, `tiered`, `vat`

- serves P09 ADM-074 Price Calculation Sequence & Formula Engine

**Decision:** 

### p49  · `listCurrencyPrecisionRounding`

`GET /currency-precision-rounding` · PRODUCT_VIEW · staff · **Currency Precision, Rounding & Monetary Rules**

> Ensure monetary calculations remain consistent across countries, currencies, channels and payment systems.

**`CurrencyPrecisionRoundingMonetaryRulesView`** — `atOrderTotal`, `bankerSRounding`, `calculated`, `calculationPrecision`, `chf1998`, `chf2000`, `currency`, `customRegulatoryRule`, `decimalPlaces`, `display`, `displayPrecision`, `minimumMonetaryUnit`, `nearestCurrencyUnit`, `perFee`, `perItem`, `perLine`, `perTax`, `resultingMonetaryValuesAreCalculated`, `resultingMonetaryValuesAreRounded`, `roundDown`, `roundUp`, `roundingMethod`, `standard`

- serves P09 ADM-075 Currency Precision, Rounding & Monetary Rules

**Decision:** 

### p50  · `simulatePriceBreakdownCalculation`

`PUT /price-breakdown-calculation` · PRODUCT_CONFIGURE · staff · **Price Breakdown, Calculation Simulation & Explainability**

> Allow administrators to test the complete calculation before releasing configuration into production.

**`PriceBreakdownCalculationSimulationExplainabilityView`** — `aed25`, `aed50`, `bookingFee`, `finalPayable`, `formula`, `input`, `output`, `reason`, `rule`, `selectType`, `sequence`, `source`, `taxTreatment`, `vat`

- serves P08 BO-1049 Scenario & What-If Planning
- serves P09 ADM-076 Price Breakdown, Calculation Simulation & Explainability

**Decision:** 

### p52  · `listCalculationValidationReconciliation`

`GET /calculation-validation-reconciliation` · PRODUCT_VIEW · staff · **Calculation Validation, Reconciliation & Service Interface**

> Provide final technical and commercial validation of the pricing calculation engine and define how other TICVAI modules consume it.

**`CalculationValidationReconciliationServiceInterfaceView`** — `authentication`, `b2bSale`, `baseAed250`, `calculationVersion`, `circularDependency`, `conflictingRule`, `discountAed25`, `discountTotal`, `discounts`, `expiredRule`, `explanationReference`, `feeAed10`, `feeTotal`, `fees`, `finalAed24675`, `finalPayable`, `finalTotal`, `groupBooking`, `invalidPrecision`, `invalidRate`, `invalidSequence`, `lineTotal`, `memberSale`, `missingInput`, `missingProfile`, `missingTaxTreatment`, `multiCurrencySale`, `multiProductOrder`, `overlappingRule`, `packageSale`, `posSale`, `reschedule`, `rounding`, `roundingDifference`, `selectedPrice`, `standardB2cSale`, `taxTotal`, `taxes`, `unsupportedCurrency`, `vatAed1175`

> ⚠ **40 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P09 ADM-077 Calculation Validation, Reconciliation & Service Interface

**Decision:** 

### p57  · `listPricingGovernance`

`GET /pricing-governance` · PRODUCT_VIEW · staff · **Pricing Governance Command Center**

> Provide Commercial, Revenue, Finance, and authorized management with one operational view of all pricing changes and governance activities.

**`PricingGovernanceCommandCenterView`** — `aed`, `approvedChanges`, `bulkUpdate`, `by`, `emergencyChanges`, `expiringPrices`, `failedPublications`, `governanceExceptions`, `highRiskChanges`, `pendingApproval`, `pendingValidation`, `pricingChangesInDraft`, `publishedToday`, `rollbacks`, `scheduledPublications`

- serves P09 ADM-078 Pricing Governance Command Center

**Decision:** 

### p58  · `setPricingChangeRequest`

`PUT /pricing-change-request` · PRODUCT_CONFIGURE · staff · **Pricing Change Request & Workspace**

> Provide a governed workspace for creating individual or structured pricing changes before modifying production pricing.

**`PricingChangeRequestWorkspaceView`** — `attachments`, `businessReason`, `businessUnit`, `changeId`, `changeName`, `changeType`, `currencyRoundingChange`, `difference`, `effectiveDate`, `eligibilityRuleChange`, `emergencyChange`, `expiryDate`, `feeChange`, `formulaChange`, `legalEntity`, `market`, `multipleMarkets`, `multipleProducts`, `multipleRates`, `multipleVenues`, `newRate`, `owner`, `priceChange`, `priceListChange`, `priority`, `rateRemoval`, `reasonsType`, `requestedBy`, `supportingNotes`, `taxChange`, `venue`

> ⚠ **31 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P09 ADM-079 Pricing Change Request & Workspace

**Decision:** 

### p60  · `listBulkPricingUpdate`

`GET /bulk-pricing-update` · PRODUCT_VIEW · staff · **Bulk Pricing Update, Import & Mass Maintenance**

> Allow large pricing portfolios to be updated efficiently without manually editing hundreds or thousands of records.

**`BulkPricingUpdateImportMassMaintenanceView`** — `activateDeactivate`, `byType`, `changeCurrency`, `csvXlsxPricingFiles`, `decreaseBy`, `decreaseFixedAmount`, `effectiveDates`, `errors12`, `increase5`, `increaseBy`, `increaseFixedAmount`, `invalidAmount`, `invalidDate`, `invalidProduct`, `mappings`, `missingMandatoryField`, `priceLists`, `rateValues`, `recordsRead5420`, `unknownRateCode`, `unsupportedCurrency`, `valid5371`, `warnings37`

- serves P09 ADM-080 Bulk Pricing Update, Import & Mass Maintenance

**Decision:** 

### p62  · `listPricingVersionBaseline`

`GET /pricing-version-baseline` · PRODUCT_VIEW · staff · **Pricing Version & Baseline Management**

> Maintain immutable versions of pricing configuration so TICVAI always knows what configuration existed at a particular time.

**`PricingVersionBaselineManagementView`** — `added`, `adult10`, `ce`, `changeCount`, `changeRequest`, `child83`, `createdBy`, `createdDate`, `effectiveDate`, `modified`, `priceList`, `productCount`, `r190200`, `rateV42V43`, `removed`, `status`, `transactionOccurred`, `unchanged`, `version`, `version42`, `version43`

- serves P09 ADM-081 Pricing Version & Baseline Management

**Decision:** 

### p63  · `listPricingChangeImpact`

`GET /pricing-change-impact` · PRODUCT_VIEW · staff · **Pricing Change Impact Analysis**

> Determine the commercial and operational consequences of a pricing change before approval and publication. This is one of the most important screens in Board 4.

**`PricingChangeImpactAnalysisView`** — `aed34m`, `apis`, `averagePriceChange`, `b2bPartners`, `basedOnConfigurableCriteria`, `channels`, `contractRates`, `currentRevenue`, `customerExposure`, `derivedRates`, `dynamicPricingGuardrails`, `events`, `existingOrdersNo`, `existingReservations`, `existingReservationsNo`, `futureReservations`, `futureUnsoldInventoryYes`, `groupRates`, `integrations`, `marginImpact`, `markets`, `maximumChange`, `membershipRates`, `memberships`, `minimumChange`, `packages`, `performances`, `products`, `projectedRevenue`, `promotions`, `transactionVolume`, `venues`

> ⚠ **32 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P09 ADM-082 Pricing Change Impact Analysis

**Decision:** 

### p64  · `approvePricingWorkflowAuthority`

`PUT /pricing-workflow-authority` · PRODUCT_CONFIGURE · staff · **Pricing Approval Workflow & Authority Matrix**

> Configure who must approve pricing changes based on their commercial risk and scope.

**`PricingApprovalWorkflowAuthorityMatrixView`** — `alternateApprover`, `change`, `channel`, `comment`, `commercialDirector`, `dateTime`, `decision`, `delegate`, `emergencyStatus`, `escalation`, `expectedApprovalTime`, `feeChange`, `financeCompliance`, `legalEntity`, `market`, `monetaryImpact`, `priceList`, `product`, `reminder`, `requestInformation`, `returnForModification`, `revenueImpact`, `role`, `taxChange`, `user`, `venue`, `version`

> ⚠ **27 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P09 ADM-083 Pricing Approval Workflow & Authority Matrix

**Decision:** 

### p66  · `publishPricingEffectiveDate`

`PUT /pricing-effective-date` · PRODUCT_CONFIGURE · staff · **Pricing Publication & Effective-Date Scheduler**

> Control exactly when approved pricing becomes commercially effective.

**`PricingPublicationEffectiveDateSchedulerView`** — `approvalComplete`, `channel`, `channelByChannel`, `channelsReady`, `dependenciesAvailable`, `effectiveDate`, `effectiveDatesValid`, `expiryDate`, `futureEffectiveDate`, `market`, `marketByMarket`, `noCriticalConflicts`, `publicationDate`, `scheduledPublication`, `stagedPublication`, `theseDatesMayDiffer`, `validationPassed`, `venue`, `venueByVenue`, `version`

- serves P09 ADM-084 Pricing Publication & Effective-Date Scheduler

**Decision:** 

### p67  · `listPricingDistributionSynchronization`

`GET /pricing-distribution-synchronization` · PRODUCT_VIEW · staff · **Pricing Distribution, Synchronization & Publication Monitor**

> Ensure published pricing reaches every TICVAI channel and dependent system consistently.

**`PricingDistributionSynchronizationPublicationMonitorView`** — `apis`, `b2b`, `b2c`, `cacheCdnWhereApplicable`, `callCenter`, `channels`, `externalIntegratedSystems`, `investigate`, `kiosk`, `lastUpdated`, `latency`, `mobileApp`, `mobilePos`, `ota`, `pos`, `publicationStarted`, `queue`, `recordsFailed`, `recordsPublished`, `reseller`, `rollbackTarget`, `targetVersion`

- serves P09 ADM-085 Pricing Distribution, Synchronization & Publication Monitor

**Decision:** 

### p69  · `listPricingRollbackEmergency`

`GET /pricing-rollback-emergency` · PRODUCT_VIEW · staff · **Pricing Rollback & Emergency Control Center**

> Provide controlled recovery when a pricing publication is incorrect or creates unacceptable commercial impact.

**`PricingRollbackEmergencyControlCenterView`** — `authorizedRole`, `channelsAffected`, `commercialBaseline`, `dubaiVenueOnly`, `entirePublication`, `existingOrders`, `futureSales`, `incidentReference`, `incorrectAdultRate`, `previousPrice`, `previousVersion`, `productsAffected`, `reason`, `revenueExposure`, `selectedChannel`, `selectedMarket`, `selectedProducts`, `selectedVenue`, `selectedVersion`, `stopDistribution`, `stopScheduledPublication`, `timestamp`, `transactionsSinceActivation`, `version52`, `version53`

- serves P09 ADM-086 Pricing Rollback & Emergency Control Center

**Decision:** 

### p70  · `listPricingCompliance`

`GET /pricing-compliance` · PRODUCT_VIEW · staff · **Pricing History, Audit & Compliance Explorer**

> Provide complete forensic traceability for every pricing configuration and change.

**`PricingHistoryAuditComplianceExplorerView`** — `approvalAudit`, `changedBy`, `compliance`, `configurationAudit`, `dateTime`, `effectiveDate`, `emergencyActionAudit`, `finance`, `guardrailsResolvedDynamicPrice`, `inBoards6And7`, `internalAudit`, `oldValueNewValue`, `plus`, `price`, `producedThisPrice`, `publication`, `publicationAudit`, `reason`, `regulatoryReview`, `respectingCommercialGuardrails`, `rollbackAudit`, `source`, `synchronizationAudit`, `whatPricesExist`

- serves P09 ADM-087 Pricing History, Audit & Compliance Explorer

**Decision:** 

### p75  · `listDynamicPricingStrategy`

`GET /dynamic-pricing-strategy` · PRODUCT_VIEW · staff · **Dynamic Pricing Strategy Command Center**

> Provide the central backend workspace for creating, monitoring, and managing all dynamic- pricing strategies. This should be the primary operational screen for Revenue Managers.

**`DynamicPricingStrategyCommandCenterView`** — `activeStrategies`, `adjustmentRange`, `automationMode`, `availabilityBased`, `basePriceSource`, `bookingVelocity`, `channel`, `currentPrice`, `currentPriceAdjustments`, `dayOfWeek`, `demandBased`, `draftStrategies`, `effectivePeriod`, `eventsUnderDynamicPricing`, `frozenStrategies`, `hybrid`, `inventoryBased`, `location`, `occupancyBased`, `owner`, `performancesUnderDynamicPricing`, `pricesAtMaximumGuardrail`, `pricesAtMinimumGuardrail`, `productEvent`, `productsUnderDynamicPricing`, `retire`, `ruleConflicts`, `ruleCount`, `rulesActive`, `seasonal`, `segment`, `status`, `strategyId`, `strategyName`, `strategyType`, `test`, `timeToEvent`, `timeslot`, `upcomingActivations`, `venue`

> ⚠ **40 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P08 BO-1044 Dynamic Seat Pricing
- serves P08 BO-528 Dynamic Pricing & AI Recommendation
- serves P09 ADM-088 Dynamic Pricing Strategy Command Center

**Decision:** 

### p76  · `setDynamicPricingStrategy`

`PUT /dynamic-pricing-strategy-2` · PRODUCT_CONFIGURE · staff · **Dynamic Pricing Strategy Builder**

> Create the master dynamic-pricing strategy and define what commercial objects it controls.

**`DynamicPricingStrategyBuilderView`** — `actsAsFallback`, `basePriceSource`, `businessUnit`, `canBecome`, `canCombineWithOtherStrategies`, `description`, `effectiveFrom`, `effectiveTo`, `evaluationFrequency`, `event`, `hasExclusiveControl`, `market`, `multiplePerformances`, `operatesIndependently`, `owner`, `performance`, `priceCategory`, `product`, `productFamily`, `selectedPriceCategories`, `selectedTimeslots`, `singleProduct`, `status`, `strategyCode`, `strategyName`, `strategyType`, `timeslot`, `venue`

> ⚠ **28 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P09 ADM-089 Dynamic Pricing Strategy Builder

**Decision:** 

### p78  · `setDemandOccupancyAvailability`

`PUT /demand-occupancy-availability` · PRODUCT_CONFIGURE · staff · **Demand, Occupancy & Availability Rule Builder**

> Configure price movements driven by actual demand and capacity consumption. This directly covers the fundamental matrix requirements for: Demand-Based Pricing Occupancy-Based Pricing Availability-Based Pricing Inventory-Based Pricing

**`DemandOccupancyAvailabilityRuleBuilderView`** — `availableSeats`, `capacityUtilization`, `currentDemand`, `cyAction`, `occupancy`, `remainingCapacity`, `remainingInventory`, `salesPace`, `ticketsSold`

- serves P09 ADM-090 Demand, Occupancy & Availability Rule Builder

**Decision:** 

### p80  · `setBookingVelocityTime`

`PUT /booking-velocity-time` · PRODUCT_CONFIGURE · staff · **Booking Velocity & Time-to-Event Rule Builder**

> Control price movement based on how quickly inventory is selling and how much time remains before the event or visit date. This is critical because occupancy alone is insufficient for effective revenue management.

**`BookingVelocityTimeToEventRuleBuilderView`** — `currentBookingPace`, `expectedBookingPace`, `historicalBookingCurve`, `increaseCurrentPriceBy5`, `orCustomIntervals`, `paceVariance`, `remainingInventory`, `salesPerDay`, `salesPerHour`, `salesPerWeek`, `sameDay`, `t1`, `t14`, `t180`, `t2Days`, `t3`, `t30`, `t60`, `t7`, `t90`, `then15`, `velocity`

- serves P09 ADM-091 Booking Velocity & Time-to-Event Rule Builder

**Decision:** 

### p81  · `listSeasonalCalendarDay`

`GET /seasonal-calendar-day` · PRODUCT_VIEW · staff · **Seasonal, Calendar, Day & Timeslot Dynamic Rules**

> Configure dynamic pricing behavior according to temporal commercial patterns.

**`SeasonalCalendarDayTimeslotDynamicRulesView`** — `base20`, `baseTo15`, `baseTo20`, `christmas`, `customCommercialCalendar`, `dateRange`, `dayOfWeek`, `eid`, `month`, `nationalDay`, `newYear`, `performance`, `publicHoliday`, `ramadan`, `schoolBreak`, `schoolHoliday`, `season`, `specialDate`, `timeOfDay`, `timeslot`, `week`, `weekend`

- serves P09 ADM-092 Seasonal, Calendar, Day & Timeslot Dynamic Rules

**Decision:** 

### p83  · `listChannelCustomerSegment`

`GET /channel-customer-segment` · PRODUCT_VIEW · staff · **Channel, Customer Segment & Location Dynamic Rules**

> Allow dynamic-pricing behavior to differ according to commercial context.

**`ChannelCustomerSegmentLocationDynamicRulesView`** — `api`, `attraction`, `b2b`, `b2c`, `callCenter`, `corporate`, `corporateAgreements`, `country`, `customSegment`, `dynamicRange0To10`, `dynamicRange15`, `eventLocation`, `fixedGroupRates`, `group`, `kiosk`, `loyaltyTier`, `market`, `maximum15`, `maximumDynamicUplift20`, `member`, `membershipGuarantees`, `mobileApp`, `ota`, `partnerContractRates`, `pos`, `reseller`, `resident`, `standardCustomer`, `venue`, `vip`, `zone`

> ⚠ **31 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P09 ADM-093 Channel, Customer Segment & Location Dynamic Rules
- serves P09 ADM-234 Customer, Segment, Channel & Partner Analytics

**Decision:** 

### p84  · `listDynamicPriceBand`

`GET /dynamic-price-band` · PRODUCT_VIEW · staff · **Dynamic Price Bands, Ladders & Adjustment Matrix**

> Define the controlled monetary steps through which prices can move. This is preferable to allowing unrestricted price generation for many products.

**`DynamicPriceBandsLaddersAdjustmentMatrixView`** — `continuousRangeWherePermitted`, `cooldownPeriod`, `derivedBands`, `downwardMovement`, `fixedAmountSteps`, `fixedPriceBands`, `maximum10`, `maximum5PerAdjustment`, `maximumBandsPerMovement`, `minimumBaseMaximum`, `minimumTimeBetweenMovements`, `p1`, `p2`, `p3`, `p4`, `p5`, `p6`, `p7`, `percentageBands`, `reversalRules`, `upwardMovement`, `whereRequired`

- serves P09 ADM-094 Dynamic Price Bands, Ladders & Adjustment Matrix

**Decision:** 

### p86  · `listDynamicPricingGuardrail`

`GET /dynamic-pricing-guardrail` · PRODUCT_VIEW · staff · **Dynamic Pricing Guardrails & Commercial Protection**

> Establish the non-negotiable boundaries for every dynamic-pricing strategy.

**`DynamicPricingGuardrailsCommercialProtectionView`** — `absoluteMaximumPrice`, `absoluteMinimumPrice`, `alreadyPurchasedTickets`, `complimentaryRates`, `contractRates`, `controlForCriticalIncidents`, `corporateRates`, `existingReservationsWhereApplicable`, `maximumChangesPerDay`, `maximumDailyChange`, `maximumOccupancyTrigger`, `maximumReduction`, `maximumSingleChange`, `maximumUplift`, `maximumWeeklyChange`, `membershipRates`, `minimumChangeInterval`, `minimumInventory`, `minimumMargin`, `promotionalLockedRates`, `regulatoryPrices`, `returnToBasePrice`

- serves P09 ADM-095 Dynamic Pricing Guardrails & Commercial Protection

**Decision:** 

### p87  · `listDynamicPricingAutomation`

`GET /dynamic-pricing-automation` · PRODUCT_VIEW · staff · **Dynamic Pricing Automation Policy & Control**

> Define how much authority the pricing engine has to act on a calculated dynamic price. This is different from Board 4's approval workflow. Board 5 determines whether the engine may act automatically. Board 4 handles governance when formal approval is required.

**`DynamicPricingAutomationPolicyControlView`** — `channel`, `event`, `expiry`, `market`, `maximumAutomaticChangesDay`, `minimumTimeBetweenChanges`, `mode0Monitor`, `mode1Recommend`, `mode2PrepareChange`, `noChangeWindows`, `nt`, `product`, `reason`, `returnBehavior`, `start`, `strategy`, `thresholdMet`, `user`, `venue`

- serves P09 ADM-096 Dynamic Pricing Automation Policy & Control

**Decision:** 

### p89  · `listRulePriorityConflict`

`GET /rule-priority-conflict` · PRODUCT_VIEW · staff · **Rule Priority, Conflict Resolution & Dynamic Pricing Test Console**

> Determine the final dynamic price when multiple strategies and rules are simultaneously applicable. This is the final and most important control screen of Board 5.

**`RulePriorityConflictResolutionDynamicPricingTestConsView`** — `administratorsConfigureRuleHierarchy`, `basePrice`, `basePriceAed250`, `bookingVelocity`, `bookingVelocity305`, `channel`, `circularDependency`, `contradictoryRules`, `cumulativeAdjustment`, `customGovernedResolution`, `customerSegment`, `date`, `event`, `guardrailConflict`, `highDemand`, `highestPriorityWins`, `impossibleCondition`, `inventory`, `lowDemand`, `maximumAdjustmentWins`, `minimumAdjustmentWins`, `missingFallback`, `mostSpecificRuleWins`, `nearSellOut`, `occupancy`, `occupancy10`, `occupancy8710`, `overlappingStrategy`, `performance`, `product`, `samePriority`, `stopProcessing`, `t3Days8`, `timeToEvent`, `timeslot`, `velocity5`, `weekend5`, `weightedCombination`, `whyAed300`, `withTheCompleteCalculationPath`

> ⚠ **40 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P08 BO-441 Price Priority & Conflict Rules
- serves P09 ADM-097 Rule Priority, Conflict Resolution & Dynamic Pricing Test Console

**Decision:** 

### p94  · `listPricing`

`GET /pricing` · PRODUCT_VIEW · staff · **AI Pricing Intelligence Command Center**

> Provide Revenue Managers with a single operational view of all AI signals, forecasts, opportunities and risks influencing pricing.

**`AiPricingIntelligenceCommandCenterView`** — `activeAiRecommendations`, `adjustment`, `averageAiConfidence`, `bookingVelocity`, `competitorMovements`, `competitorPrice`, `concerts`, `conferences`, `confidence`, `confidence91`, `currentAed250`, `currentPrice`, `dataQualityIssues`, `demandForecast`, `demandRisksDetected`, `demandSurgesDetected`, `estimatedRevenueOpportunity`, `exhibitions`, `expectedRevenueUpliftAed73400`, `externalSignalsActive`, `festivals`, `forecastAccuracy`, `highPriorityOpportunities`, `nearbyEventsDetected`, `nearbyExhibition`, `primaryDrivers`, `productEvent`, `recommendedAed270`, `recommendedPrice`, `remainingCapacity`, `revenueOpportunity`, `risk`, `sportsEvents`, `tourismEvents`, `urgency`, `venue`, `weatherConditions`, `weatherImpacts`

> ⚠ **38 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P08 BO-443 Pricing Audit, Approval & Publication
- serves P09 ADM-098 AI Pricing Intelligence Command Center

**Decision:** 

### p95  · `listInternalDemandBooking`

`GET /internal-demand-booking` · PRODUCT_VIEW · staff · **Internal Demand & Booking Signal Hub**

> Centralize the internal TICVAI signals used by forecasting and AI pricing models. These are generally the highest-confidence signals because they come directly from TICVAI transactions.

**`InternalDemandBookingSignalHubView`** — `accelerationDeceleration`, `availability`, `averageSellingPrice`, `bookingVelocity`, `cancellation`, `capacity`, `cartAbandonment`, `channelTimeslot`, `conversion`, `conversionRate`, `forecastBaseline`, `geography`, `leadTime`, `membership`, `noShow`, `occupancy`, `orders`, `previousEvent`, `previousWeek`, `remainingInventory`, `repeatPurchase`, `reschedule`, `revenue`, `revenueVelocity`, `salesPerDay`, `salesPerHour`, `sameDayLastYear`, `searchToPurchaseConversion`, `seatZoneAvailability`, `segment`, `similarEvent`, `ticketsSold`, `yesterday`

> ⚠ **33 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P09 ADM-099 Internal Demand & Booking Signal Hub

**Decision:** 

### p97  · `listWeatherDemandImpact`

`GET /weather-demand-impact` · PRODUCT_VIEW · staff · **Weather Intelligence & Demand Impact Configuration**

> Allow TICVAI to understand how weather conditions affect demand for different venues and experiences. This should be much more sophisticated than simply connecting a weather API.

**`WeatherIntelligenceDemandImpactConfigurationView`** — `airQualityWhereAvailable`, `andWeatherSensitivity`, `configurableFutureWindow`, `currentConditions`, `dailyForecast`, `demandImpact17`, `demandImpact8`, `estimatedDemandImpact812`, `extremeHeat`, `extremeHeatNegative`, `extremeHeatPotentialPositive`, `feelsLikeTemperature`, `heavyRainStrongNegative`, `highTemperaturePositive`, `hourlyForecast`, `humidity`, `rain`, `rainProbability`, `storm`, `temperature`, `today`, `visibility`, `weatherForecastConfidence93`, `wind`

- serves P09 ADM-100 Weather Intelligence & Demand Impact Configuration

**Decision:** 

### p99  · `listNearbyEventExhibition`

`GET /nearby-event-exhibition` · PRODUCT_VIEW · staff · **Nearby Event, Exhibition & Local Demand Intelligence**

> Detect external events around TICVAI venues that could materially affect visitor demand. This directly addresses the exhibition-near-the-venue scenario.

**`NearbyEventExhibitionLocalDemandIntelligenceView`** — `afterEvent`, `attendance60000`, `audienceType`, `beforeEvent`, `concert`, `conference`, `confidence`, `convention`, `currentPricing`, `customLocalEvent`, `demandForecast`, `distance12Km`, `distanceFromTicvaiVenue`, `duration4Days`, `duringEvent`, `evening`, `eventName`, `eventType`, `exhibition`, `expectedAttendance`, `festival`, `followingDay`, `location`, `lunchPeriod`, `majorAttractionEvent`, `occupancy`, `predictedImpact`, `publicCelebration`, `schoolEvent`, `source`, `sportsEvent`, `startEndDate`, `startEndTime`, `ticvaiEvents`, `tradeShow`, `venue`

> ⚠ **36 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P09 ADM-101 Nearby Event, Exhibition & Local Demand Intelligence

**Decision:** 

### p100 · `listCompetitorPricingMarket`

`GET /competitor-pricing-market` · PRODUCT_VIEW · staff · **Competitor Pricing & Market Position Intelligence**

> Allow TICVAI to understand its commercial position relative to relevant competitors.

**`CompetitorPricingMarketPositionIntelligenceView`** — `against`, `availability`, `collectionMethod`, `comparableTicvaiProduct`, `competitor`, `conversion`, `currency`, `date`, `demand`, `market`, `memberPriceWherePubliclyAvailable`, `peakPrice`, `priceSensitivity`, `promotionalPrice`, `publishedPrice`, `refreshFrequency`, `reliability`, `residentPrice`, `source`, `timeslot`, `venueProduct`, `vipPremiumPackage`, `weekendPrice`

- serves P09 ADM-102 Competitor Pricing & Market Position Intelligence

**Decision:** 

### p102 · `listMarketTourismHoliday`

`GET /market-tourism-holiday` · PRODUCT_VIEW · staff · **Market, Tourism, Holiday & Contextual Signal Hub**

> Capture broader external factors that may affect visitor demand beyond weather and nearby events.

**`MarketTourismHolidayContextualSignalHubView`** — `activeInactive`, `airportPassengerVolume`, `christmas`, `consumerDemandTrends`, `currentEstimatedImpact`, `destinationDemand`, `destinationPopularity`, `dubaiHotelOccupancy`, `eid`, `flightArrivals`, `geography`, `historicalCorrelation`, `hotelOccupancy`, `hotelRates`, `longWeekends`, `marketActivity`, `newYear`, `publicHolidays`, `publicTransportDemand`, `ramadan`, `refreshFrequency`, `reliability`, `schoolHolidays`, `source`, `tourismDemand`, `trafficConditions`, `venueDemand8`, `visitorArrivals`, `weight`

> ⚠ **29 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P09 ADM-103 Market, Tourism, Holiday & Contextual Signal Hub

**Decision:** 

### p103 · `listDemandBookingCurve`

`GET /demand-booking-curve` · PRODUCT_VIEW · staff · **AI Demand Forecasting & Booking Curve Studio**

> Predict future demand at a granular commercial level. This is the core predictive engine behind intelligent dynamic pricing.

**`AiDemandForecastingBookingCurveStudioView`** — `attendance`, `bookingVelocity20`, `channel`, `competitor5`, `confidence91`, `conversion`, `date`, `demand`, `event`, `eventHorizon`, `expectedAtT7`, `expectedSellOutTime`, `forecastBias`, `forecastFinalOccupancy`, `historicalEvents15`, `internalSales35`, `intraday`, `mape`, `marketTourism7`, `nearbyExhibition10`, `occupancy`, `overForecast`, `performance`, `priceCategory`, `product`, `reliableExternalSignals`, `remainingInventory`, `revenue`, `seasonalHorizon`, `sellThrough`, `stableBookingPattern`, `strongHistoricalData`, `timeslot`, `tomorrow`, `underForecast`, `venue`, `weather8`

> ⚠ **37 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P08 BO-1046 Inventory Forecasting
- serves P08 BO-1047 Section Revenue Forecast
- serves P08 BO-1058 Sales Pace & Pick Curves

**Decision:** 

### p105 · `listPriceElasticityRevenue`

`GET /price-elasticity-revenue` · PRODUCT_VIEW · staff · **Price Elasticity & Revenue Response Intelligence**

> Estimate how customers are likely to respond to different prices.

**`PriceElasticityRevenueResponseIntelligenceView`** — `channel`, `conversion`, `customerSegment`, `demand`, `elasticityConfidenceLow`, `margin`, `occupancy`, `price`, `product`, `revenue`, `time`

- serves P09 ADM-105 Price Elasticity & Revenue Response Intelligence

**Decision:** 

### p107 · `listPricingRecommendationExplainability`

`GET /pricing-recommendation-explainability` · PRODUCT_VIEW · staff · **AI Pricing Recommendation & Explainability Center**

> Convert all intelligence generated by Board 6 into actionable pricing recommendations. This is the central AI recommendation screen.

**`AiPricingRecommendationExplainabilityCenterView`** — `accept`, `bookingVelocity`, `competitorPricing`, `confidence`, `executionBelongsDownstream`, `expectedOccupancy`, `expectedRevenueImpact`, `ignore`, `modify`, `nearbyExhibition`, `occupancy`, `overall`, `priceElasticity`, `weather`

- serves P09 ADM-106 AI Pricing Recommendation & Explainability Center

**Decision:** 

### p108 · `listSignalDataQuality`

`GET /signal-data-quality` · PRODUCT_VIEW · staff · **AI Signal Registry, Data Quality & Model Governance**

> Govern the complete data and intelligence ecosystem behind AI pricing. This is critical. Without this screen, Development team could connect many external sources without giving TICVAI proper control over them.

**`AiSignalRegistryDataQualityModelGovernanceView`** — `advisoryOnly`, `approved`, `bias`, `blocked`, `category`, `competitorA8Hr83`, `confidenceExplanation`, `daily88`, `delayedData`, `deploymentDate`, `drift`, `experimental`, `forecastAccuracy`, `freshness`, `historicalCorrelation`, `internalExternal`, `invalidValues`, `lastUpdate`, `market`, `missingData`, `modelName`, `nearbyEvents1Hr91`, `outliers`, `owner`, `provider`, `purpose`, `recommendationAccuracy`, `refreshFrequency`, `reliability`, `revenuePerformance`, `signal`, `source`, `sourceFailure`, `ssTy`, `status`, `trainingWindow`, `unexpectedChanges`, `validationResult`, `version`, `weather10Min97`

> ⚠ **40 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P09 ADM-107 AI Signal Registry, Data Quality & Model Governance

**Decision:** 

### p114 · `listRevenue`

`GET /revenue` · PRODUCT_VIEW · staff · **Revenue Optimization Command Center**

> Provide Revenue Managers with the operational control center for all dynamic pricing simulations, AI recommendations, automated changes, experiments and revenue optimization activity.

**`RevenueOptimizationCommandCenterView`** — `activeABTests`, `activeOptimizations`, `aed235Aed41k88`, `approvalRequired`, `approvalStatus`, `autoExecutedChanges`, `automationMode`, `confidence`, `currentPrice`, `demandVariance`, `eventProduct`, `eventProximity`, `executionStatus`, `expectedUplift`, `forecastAccuracy`, `forecastRevenue`, `incrementalRevenueGenerated`, `inventoryPosition`, `ntEdItyCe`, `optimizationSuccessRate`, `pendingSimulations`, `performance`, `pricingExceptions`, `recommendationsAwaitingAction`, `recommendedPrice`, `revenueAtRisk`, `revenueOpportunity`, `revenueRisk`, `startExperiment`, `urgency`, `venue`

> ⚠ **31 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P08 BO-1043 Revenue Command Center
- serves P08 BO-1050 Revenue Analytics & Audit
- serves P09 ADM-108 Revenue Optimization Command Center

**Decision:** 

### p115 · `setPricing`

`PUT /pricing-2` · PRODUCT_CONFIGURE · staff · **Pricing Simulation Studio**

> Allow any proposed dynamic-pricing change to be tested before affecting live customers. This should become the sandbox of the Dynamic Pricing Engine.

**`PricingSimulationStudioView`** — `approvalThresholdRevenueManager`, `averageSellingPrice`, `basedOn`, `board5DynamicRule`, `board6AiRecommendation`, `bulkPriceChange`, `commercialGuardrailPass`, `contractProtectionPass`, `dataVolume`, `discard`, `elasticityConfidence`, `existingStrategyModification`, `expectedAttendance`, `expectedConversion`, `expectedDemand`, `expectedMargin`, `expectedOccupancy`, `expectedRevenue`, `expectedSellOutTime`, `expectedSellThrough`, `externalSignalQuality`, `forecastConfidence`, `historicalSimilarity`, `manualPriceChange`, `newDynamicStrategy`, `priceLadderPass`, `selectType`, `simulationConfidence89`, `startExperiment`

> ⚠ **29 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P09 ADM-109 Pricing Simulation Studio

**Decision:** 

### p117 · `listScenarioModelingWhat`

`GET /scenario-modeling-what` · PRODUCT_VIEW · staff · **Scenario Modeling & What-If Analysis**

> Scenario Modeling & What-If Analysis

**`ScenarioModelingWhatIfAnalysisView`** — `avgPrice250262270`, `bookingVelocity`, `cancellationSurge`, `competitorPrice`, `competitorPriceDrop`, `competitorPriceIncrease`, `conversion`, `customScenario`, `demand`, `eventProximity`, `expectedDemand`, `extremeWeather`, `highDemand`, `inventory`, `inventoryReduction`, `lowDemand`, `majorConcert`, `margin191m198m`, `nearbyEventImpact`, `nearbyExhibition`, `occupancy`, `price`, `rain`, `remainingCapacity`, `revenue255m261m`, `sellOut`, `share`, `tourismSurge`, `weatherImpact`

> ⚠ **29 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P09 ADM-110 Scenario Modeling & What-If Analysis

**Decision:** 

### p119 · `setPricingExperiment`

`PUT /pricing-experiment` · PRODUCT_CONFIGURE · staff · **A/B Pricing Experiment Studio**

> Allow TICVAI to scientifically test different pricing strategies using controlled customer groups. This is essential because AI should learn from actual customer behavior, not only historical assumptions.

**`ABPricingExperimentStudioView`** — `aAed250`, `asp6`, `bAed260`, `cAed270`, `channel`, `confidence96`, `confidenceLevel`, `contractRates`, `conversion12`, `customerSegment`, `endDate`, `event`, `experimentDuration`, `experimentName`, `maximumPrice`, `membershipRates`, `minimumPrice`, `objective`, `performance`, `product`, `regulatoryRequirements`, `revenue78`, `sampleSize`, `selectType`, `startDate`, `statisticalSignificance`

> ⚠ **26 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P09 ADM-111 A/B Pricing Experiment Studio

**Decision:** 

### p120 · `listRevenueDemandImpact`

`GET /revenue-demand-impact` · PRODUCT_VIEW · staff · **Revenue & Demand Impact Forecasting**

> Provide a dedicated commercial impact assessment before a dynamic-pricing action is approved or executed.

**`RevenueDemandImpactForecastingView`** — `aed62k`, `aed70k29`, `asp`, `attendance`, `b2bImpact`, `conversion`, `customersToAnotherProduct`, `demand`, `expectedDemand9500`, `expectedDemand9800`, `expectedOccupancy89`, `expectedOccupancy91`, `expectedRevenueAed245m`, `expectedRevenueAed252m`, `familyImpact`, `margin`, `memberImpact`, `occupancy`, `residentImpact`, `revenue`, `sellOutProbability`, `sellThrough`, `touristImpact`

- serves P09 ADM-112 Revenue & Demand Impact Forecasting

**Decision:** 

### p122 · `listRecommendationReviewDecision`

`GET /recommendation-review-decision` · PRODUCT_VIEW · staff · **AI Recommendation Review & Decision Queue**

> Provide the human decision workspace for recommendations produced by Board 6. This should be the Revenue Manager's inbox.

**`AiRecommendationReviewDecisionQueueView`** — `accept`, `actualRevenueResult59`, `brandPositioning`, `change`, `commercialJudgment`, `confidence`, `currentPrice`, `customerSensitivity`, `dataConcern`, `demandImpact`, `event`, `eventStrategy`, `fromBoard6`, `fromBoard7`, `governanceLevel`, `incorrectSignal`, `modify`, `recommendation`, `recommendedPrice`, `revenueOpportunity`, `simulateAgain`, `simulationRevenueUplift`, `theSystemRecordsTheModification`, `urgency`, `venue`

- serves P09 ADM-113 AI Recommendation Review & Decision Queue

**Decision:** 

### p123 · `listAutomationPolicyAutonomous`

`GET /automation-policy-autonomou` · PRODUCT_VIEW · staff · **Automation Policy & Autonomous Pricing Orchestrator**

> Control when TICVAI is allowed to execute pricing changes automatically. 123 | Pag e Board 5 defines the strategy-level automation permission. This screen manages operational autonomous execution at scale.

**`AutomationPolicyAutonomousPricingOrchestratorView`** — `aiRecommendsHumanApproval`, `aiRecommendsOnly`, `channel`, `conversionDropsAbnormally`, `dataQualityFalls`, `dateTime`, `evaluationFrequency`, `event`, `executionFrequency`, `forecastDataHealthy`, `guardrailsPassed`, `integrationFails`, `market`, `maximumChangesPerDay`, `minimumTimeBetweenChanges`, `modelConfidenceDrops`, `noProtectedRate`, `priceVolatilityExceedsThreshold`, `product`, `revenueFalls`, `strategy`, `tenant`, `venue`, `withStrictPermissionControl`

- serves P09 ADM-114 Automation Policy & Autonomous Pricing Orchestrator

**Decision:** 

### p125 · `createLiveDynamicPrice`

`POST /live-dynamic-price` · PRODUCT_CONFIGURE · staff · **Live Dynamic Price Execution & Deployment Monitor**

> Monitor pricing actions as they are executed across TICVAI's selling ecosystem.

**`LiveDynamicPriceExecutionDeploymentMonitorView`** — `aed250Aed265`, `aiRecommendation`, `apis`, `approval`, `b2b`, `b2c`, `bookingVelocityOccupancy`, `callCenter`, `event`, `executionSource`, `hold`, `kiosk`, `mobileApp`, `newPrice`, `ota`, `pos`, `previousPrice`, `priceInconsistencyDetected`, `product`, `reseller`, `revert`, `status`, `strategy`, `timestamp`

- serves P09 ADM-115 Live Dynamic Price Execution & Deployment Monitor

**Decision:** 

### p126 · `listDynamicPricingPerformance`

`GET /dynamic-pricing-performance` · PRODUCT_VIEW · staff · **Dynamic Pricing Performance & Optimization Analytics**

> Determine whether dynamic pricing actually improves TICVAI's commercial performance. 126 | Pag e

**`DynamicPricingPerformanceOptimizationAnalyticsView`** — `accepted`, `aiVsHuman`, `aiVsRules`, `asp`, `attendance`, `autoExecuted`, `averageSellingPrice`, `bookingVelocity`, `channelVsChannel`, `conversion`, `currentVsPreviousPeriod`, `demand`, `dynamicVsFixedPricing`, `eventVsEvent`, `incrementalRevenue`, `margin`, `marginUplift`, `modified`, `movement`, `negativeOutcome`, `numberOfPriceChanges`, `occupancy`, `recommendationsGenerated`, `recommendationsWereRejected`, `rejected`, `revenue`, `revenuePerAvailableCapacity`, `revenueUplift`, `sellThrough`, `strategyRoi`, `strategyVsStrategy`, `successful`, `venueVsVenue`, `with`

> ⚠ **34 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P09 ADM-116 Dynamic Pricing Performance & Optimization Analytics

**Decision:** 

### p128 · `listLearningModelPerformance`

`GET /learning-model-performance` · PRODUCT_VIEW · staff · **AI Learning, Model Performance & Optimization Feedback**

> Close the intelligence loop by comparing AI predictions and recommendations with actual commercial outcomes. This is what allows the system to improve over time.

**`AiLearningModelPerformanceOptimizationFeedbackView`** — `aed256m`, `calculatesTheFinalPayableAmount`, `channel`, `competitorMedium82`, `confidenceCalibration`, `configuredAndGoverned`, `definesTheCommercialPriceStructures`, `demandForecastAccuracy`, `elasticityAccuracy`, `eventType`, `falsePositiveRate`, `forecastError`, `forecastHorizon`, `high91`, `high96`, `market`, `occupancyHigh98`, `product`, `recommendationSuccess`, `revenueForecastAccuracy`, `revenueUplift`, `season`, `venue`, `weatherMedium87`, `wouldFreezeForDevelopmentTeam`

- serves P09 ADM-117 AI Learning, Model Performance & Optimization Feedback

**Decision:** 


---

## Product Lifecycle Catalogue Governance

### p3   · `listProductLifecycle`

`GET /product-lifecycle` · PRODUCT_VIEW · staff · **Product Lifecycle Command Center**

> Provide administrators with a centralized operational view of every product and its current lifecycle state.

**`ProductLifecycleCommandCenterView`** — `allowAdvancedFilteringBy`, `displayEffectiveActivationDates`, `oActive`, `oApproved`, `oArchived`, `oChannel`, `oCreationDate`, `oDepartment`, `oDisabled`, `oDraft`, `oEffectiveDate`, `oInConfiguration`, `oLastModification`, `oLocation`, `oOwner`, `oPendingApproval`, `oProductType`, `oPublished`, `oRetired`, `oScheduled`, `oStatus`, `oSuspended`, `oVenue`, `showCurrentLifecycleStatus`, `showPendingLifecycleActions`, `showPublicationStatusByChannel`

> ⚠ **26 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P09 ADM-118 Product Lifecycle Command Center

**Decision:** 

### p5   · `setLifecycleStatuWorkflow`

`PUT /lifecycle-statu-workflow` · PRODUCT_CONFIGURE · staff · **Lifecycle Status & Workflow Configuration**

> Configure how products move between lifecycle states.

**`LifecycleStatusWorkflowConfigurationView`** — `allowedStatusTransitions`, `availableLifecycleStatuses`, `effectiveDateRequirements`, `notificationTriggers`, `reasonCommentRequirements`, `requiredInformationBeforeTransition`, `statusSequence`, `statusSpecificEditPermissions`, `validationRequirements`, `whetherApprovalIsRequired`

- serves P09 ADM-120 Lifecycle Status & Workflow Configuration

**Decision:** 

### p6   · `createBulkProductCatalogue`

`POST /bulk-product-catalogue` · PRODUCT_CONFIGURE · staff · **Bulk Product Creation & Catalogue Import**

> Allow large catalogues to be created efficiently rather than configuring every product manually. This directly addresses the matrix requirement for catalogue creation through bulk-file upload.

**`BulkProductCreationCatalogueImportView`** — `correctErrors`, `csv`, `excel`, `excludeSelectedRecords`, `existingCatalogueFiles`, `pdfBrochures`, `previewProductsBeforeCreation`, `productDocuments`, `structuredSpreadsheetTemplates`

- serves P09 ADM-121 Bulk Product Creation & Catalogue Import

**Decision:** 

### p7   · `listProductImportExport`

`GET /product-import-export` · PRODUCT_VIEW · staff · **Product Import / Export & Environment Transfer**

> Allow controlled movement of product configurations between TICVAI environments. This covers the matrix requirement for importing/exporting catalogue products between different environments.

**`ProductImportExportEnvironmentTransferView`** — `detectMissingReferences`, `executeTransfer`, `mapDependencies`, `mapVenueLocationReferences`, `previewChanges`

- serves P09 ADM-122 Product Import / Export & Environment Transfer

**Decision:** 

### p8   · `setProductContextOwnership`

`PUT /product-context-ownership` · PRODUCT_CONFIGURE · staff · **Product Context, Ownership & Assignment**

> Define where the product belongs and who is responsible for it.

**`ProductContextOwnershipAssignmentView`** — `attraction`, `brand`, `businessUnit`, `creator`, `customerSegment`, `event`, `legalEntity`, `location`, `market`, `operationalContact`, `productFamily`, `productOwner`, `responsibleDepartment`, `salesTerritory`, `segments`, `site`, `tenant`, `venue`

- serves P09 ADM-123 Product Context, Ownership & Assignment

**Decision:** 

### p9   · `publishChannelAvailability`

`PUT /channel-availability` · PRODUCT_CONFIGURE · staff · **Channel Publication & Availability**

> Control where a product may be exposed for sale.

**`ChannelPublicationAvailabilityView`** — `detectMissingChannelDependencies`, `enableDisableChannels`, `previewPublicationStatus`

> ⚠ **1 of 3 property names read as sentences** rather than fields — likely the pack's bullets (triggers, behaviours) taken as a directory: `enableDisableChannels`

- serves P09 ADM-124 Channel Publication & Availability

**Decision:** 

### p10  · `publishActivationScheduler`

`PUT /activation-scheduler` · PRODUCT_CONFIGURE · staff · **Publication & Activation Scheduler**

> Automate future product lifecycle actions.

**`PublicationActivationSchedulerView`** — `activation`, `channel`, `date`, `deactivation`, `endOfSale`, `endOfSaleDates`, `failedScheduledJobs`, `failureHandling`, `lifecycleConflicts`, `notification`, `preActionValidation`, `product`, `publication`, `retirementTrigger`, `salesStart`, `salesSuspension`, `scheduledSuspensions`, `statusTransition`, `time`, `timeZone`, `upcomingActivations`, `upcomingPublications`, `venue`

- serves P09 ADM-125 Publication & Activation Scheduler

**Decision:** 

### p11  · `listProductDuplicationTemplate`

`GET /product-duplication-template` · PRODUCT_VIEW · staff · **Product Duplication & Template Library**

> Accelerate product configuration by allowing administrators to reuse proven configurations. The source matrix explicitly requires duplication of products together with associated configuration, rules, pricing and entitlements.

**`ProductDuplicationTemplateLibraryView`** — `addOn`, `annualPass`, `capacity`, `channels`, `childAdmission`, `dates`, `event`, `eventTicket`, `groupProduct`, `optionsType`, `prices`, `standardAdmission`, `tax`, `timeslotTicket`, `venue`, `venueSpecificTemplates`, `vipTicket`

- serves P09 ADM-126 Product Duplication & Template Library

**Decision:** 

### p12  · `setCatalogueReview`

`PUT /catalogue-review` · PRODUCT_CONFIGURE · staff · **AI Catalogue Builder & Configuration Review**

> Provide TICVAI's AI-first interface for accelerating product creation and configuration. This directly supports the matrix requirement allowing administrators to upload spreadsheets, brochures, PDFs or existing catalogues and use AI to generate product structures, pricing, rules, entitlements and configurations.

**`AiCatalogueBuilderConfigurationReviewView`** — `andPublishingIt`, `eventualDesign`, `productSafely`, `scheduledLifecycleGovernanceAndAccountability`, `scheduledLifecycleGovernanceAndOwnership`, `typeANaturalLanguageRequest`

- serves P09 ADM-127 AI Catalogue Builder & Configuration Review

**Decision:** 

### p15  · `listProductGovernance`

`GET /product-governance` · PRODUCT_VIEW · staff · **Product Governance Command Center**

> Provide management and administrators with a single control center for all product governance activities.

**`ProductGovernanceCommandCenterView`** — `approvalStatus`, `assignedApprover`, `changeType`, `changesAwaitingApproval`, `currentVersion`, `effectiveDate`, `failedPublications`, `failedRollbacks`, `highRiskConfigurationChanges`, `impactedChannels`, `product`, `productOwner`, `productsApproachingRetirement`, `productsAwaitingApproval`, `productsWithDependencyConflicts`, `productsWithGovernanceWarnings`, `productsWithUnpublishedChanges`, `proposedVersion`, `recentlyPublishedVersions`, `rejectedChanges`, `requestedBy`, `requestedDate`, `riskLevel`, `scheduledChanges`, `venue`

- serves P09 ADM-128 Product Governance Command Center

**Decision:** 

### p17  · `approveWorkflow`

`PUT /workflow` · PRODUCT_CONFIGURE · staff · **Approval Workflow Designer**

> Configure reusable approval workflows governing product creation and modification.

**`ApprovalWorkflowDesignerView`** — `applicableProductTypes`, `approvalGroup`, `approvalStages`, `approverRole`, `changeType`, `delegation`, `department`, `escalation`, `mandatoryOptionalStage`, `rejectionBehavior`, `reminderFrequency`, `resubmissionBehavior`, `sequentialParallelApproval`, `sla`, `specificApprover`, `venue`, `workflowName`

- serves P08 BO-637 Approval Workflow Builder
- serves P09 ADM-129 Approval Workflow Designer
- serves P09 ADM-319 Approval Workflow Library

**Decision:** 

### p18  · `approveReviewDecision`

`PUT /review-decision` · PRODUCT_CONFIGURE · staff · **Approval Review & Decision Workspace**

> Give approvers a clear interface for reviewing a proposed product or product change before making a decision.

**`ApprovalReviewDecisionWorkspaceView`** — `accessImpact`, `attachments`, `businessJustification`, `capacityImpact`, `channelsAffected`, `currentSales`, `delegate`, `effectiveDate`, `financeImpact`, `futureReservations`, `onD`, `pricingImpact`, `reasonForChange`, `reassign`, `refundableLe`, `requestChanges`, `requester`

- serves P09 ADM-130 Approval Review & Decision Workspace

**Decision:** 

### p20  · `listRollbackRecovery`

`GET /rollback-recovery` · PRODUCT_VIEW · staff · **Rollback & Recovery Management**

> Safely restore an earlier product configuration when a newly published configuration causes an issue.

**`RollbackRecoveryManagementView`** — `channelAssociation`, `enhancedAuditLogging`, `enterRollbackReason`, `entireProduct`, `entitlementConfiguration`, `executeImmediateRollbackWhereAuthorized`, `identifyDependencies`, `media`, `monitorRollbackStatus`, `policy`, `pricingAssociation`, `subjectToSystemGovernance`, `validityConfiguration`

- serves P09 ADM-132 Rollback & Recovery Management

**Decision:** 

### p21  · `listChangeImpactAnalysis`

`GET /change-impact-analysi` · PRODUCT_VIEW · staff · **Change Impact Analysis**

> Show administrators what will be affected before a product change is approved or published. This directly addresses the matrix requirement to perform impact analysis before product changes are published.

**`ChangeImpactAnalysisView`** — `accessControl`, `b2bPartners`, `b2c`, `capacity`, `critical`, `entitlements`, `finance`, `futureOrders`, `high`, `issuedTickets`, `kiosk`, `low`, `media`, `medium`, `membership`, `otas`, `pos`, `pricing`, `promotions`, `reporting`, `reservations`, `salesChannels`, `tax`

- serves P09 ADM-082 Pricing Change Impact Analysis
- serves P09 ADM-133 Change Impact Analysis

**Decision:** 

### p22  · `listChangePropagationDependency`

`GET /change-propagation-dependency` · PRODUCT_VIEW · staff · **Change Propagation & Dependency Control**

> Control whether approved product changes should automatically propagate to related products or dependent configurations. The source matrix requires controlled propagation of changes to linked products.

**`ChangePropagationDependencyControlView`** — `adultAdmission`, `childAdmission`, `overwritten`, `propagates`, `residentAdmission`, `seniorAdmission`, `typesType`

- serves P09 ADM-134 Change Propagation & Dependency Control

**Decision:** 

### p23  · `listProductRetirementSuspension`

`GET /product-retirement-suspension` · PRODUCT_VIEW · staff · **Product Retirement, Suspension & Archive**

> Provide a governed end-of-life process for products. The source matrix explicitly requires disabling or retiring products without affecting previously sold tickets.

**`ProductRetirementSuspensionArchiveView`** — `activePriceLists`, `activePromotions`, `bundles`, `channelAssignments`, `channels`, `communicationRequirements`, `endOfSaleDate`, `endSale`, `existingReservationTreatment`, `existingTicketTreatment`, `from`, `futureReservations`, `membershipBenefits`, `reason`, `replacementProduct`, `reportingTreatment`, `resellerAgreements`, `retire`, `retirementDate`, `temporarilyDisable`, `validityOfPreviouslyIssuedEntitlements`, `validityOfPreviouslyIssuedTickets`

- serves P09 ADM-135 Product Retirement, Suspension & Archive

**Decision:** 

### p24  · `listProductTrailChange`

`GET /product-trail-change` · PRODUCT_VIEW · staff · **Product Audit Trail & Change History**

> Provide a complete, immutable history of product configuration and governance activity. The matrix requires tracking configuration changes with timestamps and user information.

**`ProductAuditTrailChangeHistoryView`** — `action`, `approvalReference`, `configurationArea`, `dateTime`, `environment`, `ipDeviceMetadataWhereApplicable`, `newValue`, `previousValue`, `product`, `reason`, `role`, `sourceChannel`, `user`, `version`

- serves P09 ADM-136 Product Audit Trail & Change History

**Decision:** 

### p26  · `listGovernanceRiskMonitoring`

`GET /governance-risk-monitoring` · PRODUCT_VIEW · staff · **Governance Risk, AI Monitoring & Control Center**

> Use TICVAI intelligence to continuously identify catalogue governance risks rather than relying entirely on administrators to discover them manually.

**`GovernanceRiskAiMonitoringControlCenterView`** — `assessment`, `businessImpact`, `configurations`, `dueDate`, `owner`, `product`, `recommendedAction`, `risk`, `status`, `venue`, `with`

- serves P09 ADM-137 Governance Risk, AI Monitoring & Control Center
- serves P09 ADM-365 Risk & Governance Analytics
- serves P09 ADM-549 AI Governance Monitoring Command Center

**Decision:** 


---

## Sales Channel Management

### p3   · `listSaleChannel`

`GET /sale-channel` · PRODUCT_VIEW · staff · **Sales Channel Command Center**

> Provide administrators with one centralized view of every TICVAI sales channel and its current operational/configuration status.

**`SalesChannelCommandCenterView`** — `activeChannels`, `api`, `b2bPortal`, `b2cMobileApp`, `b2cWeb`, `brand`, `callCenter`, `channelId`, `channelName`, `channelType`, `channelsInDraft`, `channelsWithCapacityAlerts`, `channelsWithErrors`, `channelsWithPricingIssues`, `currency`, `customChannel`, `flyingPos`, `inactiveChannels`, `integrationStatus`, `kiosk`, `lastUpdated`, `marketplace`, `mobilePos`, `ota`, `owner`, `partnerPortal`, `pos`, `priceProfile`, `products`, `productsDistributed`, `publicationStatus`, `reseller`, `scheduledActivations`, `scheduledDeactivations`, `status`, `thirdPartyChannel`, `totalChannels`, `venueScope`

> ⚠ **38 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P09 ADM-258 Sales Channel Command Center
- serves P09 ADM-383 Sales Channel Assessment
- serves P17 SGN-005 Sales Channel Assessment

**Decision:** 

### p5   · `createChannelProfile`

`POST /channel-profile` · PRODUCT_CONFIGURE · staff · **Channel Creation & Profile Configuration**

> Create and define a sales channel before products and commercial rules are assigned.

**`ChannelCreationProfileConfigurationView`** — `allocationRules`, `apiConnection`, `attraction`, `brand`, `businessUnit`, `cashierAccess`, `channelCode`, `channelName`, `channelType`, `commercialOwner`, `country`, `currency`, `customerFacingName`, `digitalCustomerJourney`, `domainBrand`, `event`, `financeOwner`, `global`, `internalDescription`, `location`, `market`, `mayRequire`, `operationalOwner`, `owner`, `partner`, `region`, `responsibleDepartment`, `selectedBusinessUnit`, `technicalOwner`, `tenant`, `timeZone`, `venue`, `webstore`, `workstationGroups`

> ⚠ **34 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P09 ADM-259 Channel Creation & Profile Configuration

**Decision:** 

### p7   · `setProductCatalogue`

`PUT /product-catalogue` · PRODUCT_CONFIGURE · staff · **Product & Catalogue Assignment**

> Control exactly which products are available through each sales channel.

**`ProductCatalogueAssignmentView`** — `attraction`, `capacityStatus`, `channelStatus`, `draftProducts`, `effectiveFrom`, `effectiveTo`, `entireApprovedCatalogue`, `event`, `individualProduct`, `pricingStatus`, `product`, `productCategory`, `productCollection`, `productFamily`, `productType`, `productsOutsideValidity`, `productsUnavailableForTheChannel`, `retiredProducts`, `status`, `validity`, `venue`, `venueCatalogue`

- serves P09 ADM-260 Product & Catalogue Assignment

**Decision:** 

### p8   · `setChannelPricingCommercial`

`PUT /channel-pricing-commercial` · PRODUCT_CONFIGURE · staff · **Channel Pricing & Commercial Profile Assignment**

> Determine which pricing configuration a channel consumes.

**`ChannelPricingCommercialProfileAssignmentView`** — `b2bRate`, `channelPriceList`, `currency`, `customerSegment`, `dynamicPricingProfile`, `effectiveFrom`, `effectiveTo`, `event`, `otaRate`, `posPrice`, `priceProfile`, `priority`, `product`, `promotionalPriceProfile`, `resellerRate`, `standardPriceList`, `venue`

- serves P09 ADM-261 Channel Pricing & Commercial Profile Assignment
- serves P09 ADM-483 Pricing & Commercial Configuration

**Decision:** 

### p10  · `listInventoryCapacityChannel`

`GET /inventory-capacity-channel` · PRODUCT_VIEW · staff · **Inventory, Capacity & Channel Allocation**

> Control how much product inventory or event capacity is available to each sales channel.

**`InventoryCapacityChannelAllocationView`** — `allocated`, `allocation`, `capacityPool`, `channel`, `exampleOtaReceives15`, `held`, `maximum`, `minimum`, `oversellPermission`, `productEvent`, `released`, `remaining`, `replenishmentRule`, `returned`, `sold`, `utilization`, `waitlistBehaviorWhereApplicable`

- serves P09 ADM-262 Inventory, Capacity & Channel Allocation

**Decision:** 

### p11  · `listChannelSaleSchedule`

`GET /channel-sale-schedule` · PRODUCT_VIEW · staff · **Channel Sales Schedule & Availability Windows**

> Control when each channel is permitted to sell.

**`ChannelSalesScheduleAvailabilityWindowsView`** — `activeSellingPeriods`, `blackoutDates`, `blackouts`, `changeApplicableRule`, `conflicts`, `daysOfWeek`, `eventDates`, `eventRelativeWindows`, `hoursOfOperation`, `salesEndDate`, `salesEndTime`, `salesStartDate`, `salesStartTime`, `scheduledClosures`, `scheduledOpenings`, `timeZone`

- serves P09 ADM-258 Sales Channel Command Center
- serves P09 ADM-263 Channel Sales Schedule & Availability Windows

**Decision:** 

### p12  · `listCustomerEligibilityRule`

`GET /customer-eligibility-rule` · PRODUCT_VIEW · staff · **Customer & Eligibility Rules by Channel**

> Determine who is allowed to purchase through a particular channel.

**`CustomerEligibilityRulesByChannelView`** — `age`, `authenticationStatus`, `b2c`, `corporateAccount`, `corporateAccountRequired`, `country`, `customerSegment`, `customerType`, `guestAllowed`, `identityVerificationRequired`, `internationalReseller`, `loginRequired`, `loyaltyTier`, `membership`, `membershipRequired`, `ota`, `partner`, `pos`, `promoEligibility`, `purchaseHistory`, `residency`, `salesTerritory`, `withExplanation`

- serves P09 ADM-264 Customer & Eligibility Rules by Channel

**Decision:** 

### p13  · `listChannelSaleRule`

`GET /channel-sale-rule` · PRODUCT_VIEW · staff · **Channel Sales Rules, Limits & Restrictions**

> Configure operational restrictions that apply specifically to a sales channel.

**`ChannelSalesRulesLimitsRestrictionsView`** — `audited`, `discountPermitted`, `effectiveDated`, `exchangePermitted`, `holdPermitted`, `maximumPerCustomer`, `maximumPerDay`, `maximumPerEvent`, `maximumPerProduct`, `maximumPerTransaction`, `maximumQuantity`, `minimumQuantity`, `partialPaymentPermitted`, `paymentLinkPermitted`, `permissionControlled`, `promoCodePermitted`, `reschedulePermitted`, `reservationPermitted`, `visible`, `withControlledOverrideGovernance`

- serves P09 ADM-258 Sales Channel Command Center
- serves P09 ADM-265 Channel Sales Rules, Limits & Restrictions

**Decision:** 

### p14  · `setChannelFeePayment`

`PUT /channel-fee-payment` · PRODUCT_CONFIGURE · staff · **Channel Fees, Payment & Fulfillment Configuration**

> Define the commercial and fulfillment behavior associated with each channel.

**`ChannelFeesPaymentFulfillmentConfigurationView`** — `accountCredit`, `apiTicketDelivery`, `appleGoogleWallet`, `b2bCredit`, `bookingFee`, `card`, `cash`, `channelFee`, `collection`, `creditDebitCard`, `deliveryFee`, `digitalTicket`, `digitalWallet`, `email`, `kioskPrint`, `mobileApp`, `mobileWallet`, `nfc`, `otherConfiguredMethods`, `paymentFee`, `paymentLink`, `posPrint`, `printedTicket`, `rfid`, `serviceFee`, `transactionFee`, `voucher`, `wallet`, `wristband`

> ⚠ **29 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P09 ADM-266 Channel Fees, Payment & Fulfillment Configuration

**Decision:** 

### p16  · `publishChannelReadinessValidation`

`PUT /channel-readiness-validation` · PRODUCT_CONFIGURE · staff · **Channel Publication, Readiness & AI Validation**

> Perform final validation before a sales channel or channel/product configuration becomes commercially active.

**`ChannelPublicationReadinessAiValidationView`** — `assigned`, `available`, `beforeActivation`, `complete`, `configured`, `critical`, `high`, `low`, `managingAvailabilityAndSynchronization`, `medium`, `period`, `preview`, `readyWhereRequired`, `recommendation`, `returnForChanges`, `troubleshootGovernAndOptimizeThem`, `valid`

- serves P09 ADM-267 Channel Publication, Readiness & AI Validation

**Decision:** 

### p20  · `listChannel`

`GET /channel` · PRODUCT_VIEW · staff · **Channel Operations Command Center**

> Provide a real-time operational view of all active TICVAI sales channels.

**`ChannelOperationsCommandCenterView`** — `activeChannels`, `capacityAlerts`, `channel`, `connectedChannels`, `connectionStatus`, `degradedChannels`, `errorCount`, `failedTransactions`, `forceSync`, `grossSales`, `healthScore`, `inventoryStatus`, `lastSync`, `offlineChannels`, `otaTiqtripInventorySynchronized1041`, `pricingErrors`, `pricingStatus`, `products`, `productsAvailable`, `salesValue`, `synchronizationErrors`, `transactions`, `transactionsToday`, `type`, `venueScope`

- serves P09 ADM-268 Channel Operations Command Center
- serves P09 ADM-277 AI Channel Optimization & Intelligence Center

**Decision:** 

### p22  · `listChannelConnectionIntegration`

`GET /channel-connection-integration` · PRODUCT_VIEW · staff · **Channel Connection & Integration Manager**

> Configure and manage the technical connection between TICVAI and external or internal sales channels.

**`ChannelConnectionIntegrationManagerView`** — `apiKey`, `apiVersion`, `authenticationType`, `certificate`, `certificates`, `channel`, `clientCredentials`, `connectionStatus`, `connectorName`, `credentialsReference`, `customConnector`, `endpoint`, `environment`, `fileSftpWhereRequired`, `ipRestrictions`, `middleware`, `oauth`, `otaAdapter`, `partner`, `partnerApi`, `rateLimit`, `resellerApi`, `restApi`, `signedRequests`, `testAuthentication`, `testAvailability`, `testCancellationWhereSupported`, `testConnectivity`, `testOrder`, `testPrice`, `testProduct`, `thisScreenManagesChannelConnectivity`, `ticvaiNative`, `timeout`, `webhook`

> ⚠ **35 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P09 ADM-269 Channel Connection & Integration Manager

**Decision:** 

### p23  · `listProductPriceAvailability`

`GET /product-price-availability` · PRODUCT_VIEW · staff · **Product, Price & Availability Synchronization**

> Control how TICVAI distributes commercial information to connected channels and receives supported updates.

**`ProductPriceAvailabilitySynchronizationView`** — `availability`, `capacity`, `channelTicvai`, `duration`, `eventTriggered`, `failed`, `fees`, `lastSuccessfulSync`, `manual`, `media`, `nearRealTime`, `nextSync`, `pending`, `price`, `product`, `productDescription`, `realTime`, `recordsProcessed`, `reprocess`, `restrictions`, `salesStatus`, `scheduled`, `successful`, `tax`, `warning`

- serves P09 ADM-270 Product, Price & Availability Synchronization

**Decision:** 

### p25  · `listRealTimeChannel`

`GET /real-time-channel` · PRODUCT_VIEW · staff · **Real-Time Channel Availability & Inventory Monitor**

> Provide operations with a live view of what each channel can currently sell.

**`RealTimeChannelAvailabilityInventoryMonitorView`** — `againstTheSeatMapCapacityPool`, `allocated`, `available`, `closed`, `ctBA`, `dD`, `forecastedSellOut`, `held`, `lowAvailability`, `notAssigned`, `remaining`, `salesVelocity`, `sold`, `soldOut`, `suspended`, `utilization`

- serves P09 ADM-271 Real-Time Channel Availability & Inventory Monitor

**Decision:** 

### p26  · `listChannelAllocationRebalancing`

`GET /channel-allocation-rebalancing` · PRODUCT_VIEW · staff · **Channel Allocation & Rebalancing Operations**

> Allow authorized users to operationally adjust inventory allocations as demand changes. Board 1 defines the allocation rules. Board 2 manages those allocations during live operations.

**`ChannelAllocationRebalancingOperationsView`** — `allocated1000`, `allocated6000`, `approvalThresholds`, `capacity`, `channel`, `confirmedTransactions`, `contractualAllocation`, `existingHolds`, `forecast`, `held`, `increaseAllocation`, `initialAllocation`, `minimumGuaranteedInventory`, `recommendedAllocation`, `reduceAllocation`, `remaining`, `remaining120`, `remaining720`, `returnInventory`, `salesVelocity`, `sold`, `sold280`, `sold5880`, `utilization`

- serves P09 ADM-272 Channel Allocation & Rebalancing Operations

**Decision:** 

### p27  · `listChannelExceptionIncident`

`GET /channel-exception-incident` · PRODUCT_VIEW · staff · **Channel Exceptions, Incidents & Recovery**

> Provide one operational workspace for resolving channel problems.

**`ChannelExceptionsIncidentsRecoveryView`** — `affectedEvent`, `affectedProduct`, `apiRequestReference`, `authenticationFailure`, `businessImpact`, `cancellationFailure`, `channel`, `connectionFailure`, `correlationId`, `currentStatus`, `errorCode`, `errorType`, `firstDetected`, `fulfillmentFailure`, `incidentId`, `inventoryMismatch`, `orderFailure`, `owner`, `partner`, `partnerError`, `paymentError`, `pricingMismatch`, `productSyncFailure`, `rateLimit`, `reSync`, `reprocess`, `response`, `severity`, `sla`, `switchToManual`, `timeout`, `timestamp`, `transactionsAffected`

> ⚠ **33 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P09 ADM-273 Channel Exceptions, Incidents & Recovery

**Decision:** 

### p29  · `listChannelPerformanceCommercial`

`GET /channel-performance-commercial` · PRODUCT_VIEW · staff · **Channel Performance & Commercial Analytics**

> Compare the commercial effectiveness of TICVAI sales channels.

**`ChannelPerformanceCommercialAnalyticsView`** — `allocation`, `averageOrderValue`, `cancellation`, `cancellationRate`, `capacityUtilization`, `commission`, `conversionRate`, `costOfSaleWhereAvailable`, `fees`, `grossSales`, `growth`, `netSales`, `revenue`, `revenuePerAvailableUnit`, `settlement`, `sold`, `ticketsSold`, `transactions`, `utilization`

- serves P09 ADM-274 Channel Performance & Commercial Analytics

**Decision:** 

### p30  · `listChannelLogTransaction`

`GET /channel-log-transaction` · PRODUCT_VIEW · staff · **Channel Audit, Logs & Transaction Traceability**

> Provide complete traceability across channel configuration, synchronization and transactions.

**`ChannelAuditLogsTransactionTraceabilityView`** — `action`, `activation`, `allocationChange`, `cancellation`, `compliance`, `configurationChange`, `environment`, `error`, `finance`, `integrationChange`, `manualIntervention`, `newValue`, `order`, `partnerDisputes`, `previousValue`, `priceAssignment`, `reference`, `result`, `suspension`, `technicalInvestigation`, `timestamp`, `userSystem`

- serves P09 ADM-275 Channel Audit, Logs & Transaction Traceability

**Decision:** 

### p32  · `listChannelGovernanceSla`

`GET /channel-governance-sla` · PRODUCT_VIEW · staff · **Channel Governance, SLA & Partner Control**

> Govern live channels and ensure that internal/external channels operate within approved commercial and service conditions.

**`ChannelGovernanceSlaPartnerControlView`** — `actual9972`, `apiResponseTime`, `availability`, `availability999`, `channelOwner`, `commercialAgreementReference`, `contractDates`, `errorRate`, `escalationContacts`, `excessiveTransactionFailures`, `expiredAgreement`, `expiredCertificate`, `expiringApiCredentials`, `incidentResolutionTime`, `missingOwner`, `partnerOwner`, `placeUnderReview`, `rateLimits`, `reactivate`, `renewalDate`, `resellerOtaDistributionArea`, `restrict`, `sla`, `slaBreach`, `statusSlaBreach`, `supportContacts`, `transactionLimits`, `transactionSuccess`, `unapprovedProductionIntegration`

> ⚠ **29 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P09 ADM-276 Channel Governance, SLA & Partner Control

**Decision:** 

### p33  · `listChannel2`

`GET /channel-2` · PRODUCT_VIEW · staff · **AI Channel Optimization & Intelligence Center**

> Create the AI intelligence layer that looks across all sales channels together rather than optimizing each channel in isolation.

**`AiChannelOptimizationIntelligenceCenterView`** — `allocation`, `availability`, `capacity`, `channelFees`, `channelUtilization`, `commission`, `confidence`, `constraints`, `contractualConstraints`, `conversion`, `customerDemand`, `expectedImpact`, `expectedUnitsSold`, `failures`, `historicalPerformance`, `netRevenue`, `paymentFulfillmentValidatePublish`, `pricing`, `realTimeChannelAvailabilityInventory`, `reason`, `recommendation`, `requiredApproval`, `revenue`, `revenueImpact`, `risk`, `salesVelocity`, `timeToEvent`

> ⚠ **27 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P09 ADM-268 Channel Operations Command Center
- serves P09 ADM-277 AI Channel Optimization & Intelligence Center

**Decision:** 

