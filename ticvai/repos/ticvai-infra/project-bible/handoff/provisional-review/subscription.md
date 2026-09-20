# subscription — 50 operations awaiting sign-off

> **These are specified, not unfinished.** Each has a request, a response and a citation of
> the pack page it was read from. `x-ticvai-provisional` means **nobody who has to build it
> has agreed it** — so the only thing that closes one is a decision in this column: *agreed*,
> *corrected* (say how), or *not needed*.

**2 pack(s), read in page order.** A session opens a book and walks it.

- B2B, Reseller & OTA Partner Management — **30**
- Membership Annual Pass Management — **20**


---

## B2B, Reseller & OTA Partner Management

### p5   · `listPartner`

`GET /partner` · PLATFORM_TENANT_VIEW · partner · **Partner Management Command Center**

> Provide a centralized management dashboard for all B2B, reseller, OTA and distribution partners across the TICVAI ecosystem.

**`PartnerManagementCommandCenterView`** — `accountStatus`, `activePartners`, `agreementStatus`, `assignedBrand`, `assignedVenue`, `commercialOwner`, `connectedOtaApiPartners`, `country`, `creditStatus`, `distributionChannel`, `documentationIssues`, `expiringAgreements`, `highRiskPartners`, `integrationStatus`, `lastActivity`, `legalEntity`, `onboardingStatus`, `partnerId`, `partnerRevenueYtd`, `partnerSalesYtd`, `partnerType`, `partnersWithCreditHolds`, `pendingApproval`, `pendingOnboarding`, `suspendedPartners`, `suspendedTerminatedArchived`, `territory`, `totalPartners`, `tradingName`

> ⚠ **29 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P10 PTR-022 Partner Management Command Center
- serves P10 PTR-042 Partner Operations Command Center

**Decision:** 

### p7   · `setPartnerProfileOrganization`

`PUT /partner-profile-organization` · PLATFORM_CELL_MANAGE · partner · **Partner Profile & Organization Setup**

> Create the master business record for each external distribution partner.

**`PartnerProfileOrganizationSetupView`** — `accountManager`, `businessAddress`, `city`, `commercialManager`, `country`, `defaultCurrency`, `financeOwner`, `generalEmail`, `highVolume`, `keyAccount`, `legalEntityName`, `mainTelephone`, `newPartner`, `operationalOwner`, `partnerId`, `partnerType`, `preferredLanguage`, `registeredAddress`, `registrationNumber`, `restricted`, `standard`, `strategic`, `taxVatNumber`, `technicalOwner`, `timeZone`, `tradingName`, `typesType`, `vip`, `website`

> ⚠ **29 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P10 PTR-023 Partner Profile & Organization Setup

**Decision:** 

### p8   · `listPartnerOnboardingApplication`

`GET /partner-onboarding-application` · PLATFORM_TENANT_VIEW · partner · **Partner Onboarding & Application Workflow**

> Manage the complete journey from a new partner application through internal review and activation. 8 | Pag e

**`PartnerOnboardingApplicationWorkflowView`** — `apiIntegrationRequirements`, `billingRequirements`, `businessCase`, `companyInformation`, `contactInformation`, `creditRequest`, `eachDepartmentReceivesRelevantTasks`, `escalation`, `estimatedAnnualBusiness`, `expectedSalesVolume`, `expectedVolume`, `fulfillmentRequirements`, `mandatoryStage`, `markets`, `optionalStage`, `parallelApproval`, `paymentTerms`, `preferredDistributionMethod`, `productRequirements`, `reassignment`, `rejection`, `requestMoreInformation`, `requestedPartnerType`, `requestedProducts`, `requestedVenues`, `sequentialApproval`, `sla`, `taxInformation`, `territory`

> ⚠ **29 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P10 PTR-024 Partner Onboarding & Application Workflow

**Decision:** 

### p10  · `listPartnerContactUser`

`GET /partner-contact-user` · PLATFORM_TENANT_VIEW · partner · **Partner Contacts & User Administration**

> Manage the individuals authorized to interact with TICVAI on behalf of each partner.

**`PartnerContactsUserAdministrationView`** — `accountExpiry`, `branch`, `commercial`, `contactType`, `currency`, `department`, `email`, `emergencyContact`, `finance`, `language`, `loginRestrictions`, `management`, `mfa`, `mobile`, `name`, `operations`, `partner`, `passwordPolicy`, `permissions`, `position`, `primaryContact`, `reassignRole`, `reservations`, `role`, `salesLocation`, `sessionControls`, `ssoWhereAvailable`, `status`, `technical`, `telephone`, `timeZone`, `username`

> ⚠ **32 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P10 PTR-025 Partner Contacts & User Administration

**Decision:** 

### p12  · `listTerritoryMarketDistribution`

`GET /territory-market-distribution` · PLATFORM_TENANT_VIEW · partner · **Territory, Market & Distribution Rights**

> Define where and through what business scope a partner is authorized to distribute TICVAI products.

**`TerritoryMarketDistributionRightsView`** — `affiliateLink`, `agentPortal`, `api`, `approvalRequired`, `attraction`, `b2bPortal`, `brand`, `city`, `country`, `directConsumerResale`, `dubai`, `effectiveFrom`, `effectiveTo`, `event`, `exclusive`, `market`, `maximumHierarchyDepth`, `nonExclusive`, `otaConnection`, `otherAuthorizedChannel`, `preferred`, `region`, `restricted`, `saudiMarket`, `subAgentsAllowed`, `subAgentsProhibited`, `subDistribution`, `uae`, `venue`, `voucherDistribution`

> ⚠ **30 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P10 PTR-026 Territory, Market & Distribution Rights

**Decision:** 

### p14  · `setPartnerBrandVenue`

`PUT /partner-brand-venue` · PLATFORM_CELL_MANAGE · partner · **Partner Brand, Venue & Business Scope Assignment**

> Determine which TICVAI business entities the partner relationship covers. This is deliberately separate from product assignment, which is governed through the Sales Channel and commercial configuration layers.

**`PartnerBrandVenueBusinessScopeAssignmentView`** — `abuDhabiWaterpark`, `allowControlledExceptions`, `attraction`, `brand`, `businessUnit`, `cityMuseum`, `dubaiArena`, `dubaiExperiences`, `endDate`, `eventPortfolio`, `market`, `seasonalScope`, `startDate`, `temporaryAssignment`, `tenant`, `venue`

- serves P10 PTR-027 Partner Brand, Venue & Business Scope Assignment

**Decision:** 

### p15  · `listPartnerDocumentationCompliance`

`GET /partner-documentation-compliance` · PLATFORM_TENANT_VIEW · partner · **Partner Documentation & Compliance Repository**

> Maintain required partner documentation and ensure that commercial accounts remain compliant.

**`PartnerDocumentationComplianceRepositoryView`** — `apiAgreement`, `bankDetails`, `commercialRegistration`, `complianceDocuments`, `documentNumber`, `documentType`, `expired`, `expiring`, `expiryDate`, `file`, `identificationOfAuthorizedSignatory`, `insurance`, `issuingAuthority`, `missing`, `nda`, `notes`, `otherRequiredDocuments`, `rejected`, `requireManualReview`, `signedAgreement`, `taxVatCertificate`, `tradeLicense`, `underReview`, `uploaded`, `verificationDate`, `verificationStatus`, `verified`, `verifiedBy`, `warnOnly`

> ⚠ **29 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P10 PTR-028 Partner Documentation & Compliance Repository

**Decision:** 

### p16  · `listPartnerAccessRole`

`GET /partner-access-role` · PLATFORM_TENANT_VIEW · partner · **Partner Access, Roles & Permission Profile**

> Control what a partner organization is permitted to do, beyond individual-user permissions.

**`PartnerAccessRolesPermissionProfileView`** — `accessCustomerDetails`, `accessReports`, `confirmBooking`, `creditAdjustment`, `customerDataExport`, `eventSpecific`, `highValueBooking`, `holdInventory`, `manualPriceOverride`, `mayRequireAdditionalInternalApproval`, `modifyBooking`, `permanent`, `seasonal`, `temporary`, `useApi`, `useCredit`, `usePaymentCard`

- serves P10 PTR-029 Partner Access, Roles & Permission Profile

**Decision:** 

### p18  · `approvePartnerStatuLifecycle`

`PUT /partner-statu-lifecycle` · PLATFORM_CELL_MANAGE · partner · **Partner Approval, Status & Lifecycle Management**

> Govern the complete business lifecycle of a partner after onboarding.

**`PartnerApprovalStatusLifecycleManagementView`** — `activeHolds`, `activeIntegrations`, `activeUsers`, `commercial`, `compliance`, `contractExpiry`, `credit`, `currentAllocations`, `customers`, `existingCustomers`, `existingTickets`, `fraud`, `futureBookings`, `managementDecision`, `orSelectedRestrictions`, `outstandingBalance`, `pendingSettlement`, `performance`, `reactivate`, `restrict`, `stopApi`, `stopCreditSales`, `stopNewBookings`, `stopSpecificMarket`, `stopSpecificVenue`, `technical`, `terminate`, `thenPotentially`

> ⚠ **28 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P10 PTR-030 Partner Approval, Status & Lifecycle Management

**Decision:** 

### p19  · `listPartnerProfileReadiness`

`GET /partner-profile-readiness` · PLATFORM_TENANT_VIEW · partner · **Partner 360° Profile, Readiness & AI Review**

> Provide one consolidated Partner 360 screen before activation and throughout the relationship. 19 | Pag e This should become one of the most useful screens for TICVAI commercial management.

**`Partner360ProfileReadinessAiReviewView`** — `activeB2bUsers`, `agreementCreditSummaryFromBoard2`, `allocationsIntoBoard1`, `approvedLimit`, `authorization`, `authorizedCapabilities`, `authorizedMarkets`, `brandsAndVenues`, `companyInformationAndHierarchy`, `complianceStatus`, `configuredHumanAuthorization`, `connectedChannelsFromArea4`, `keyPartnerContacts`, `restrict`, `returnForChanges`, `summaryFromBoard3`

- serves P10 PTR-031 Partner 360° Profile, Readiness & AI Review

**Decision:** 

### p23  · `listCommercialAgreement`

`GET /commercial-agreement` · PLATFORM_TENANT_VIEW · partner · **Commercial Agreement Command Center**

> Provide commercial and finance teams with a centralized view of all partner agreements and their current commercial health. 23 | Pag e

**`CommercialAgreementCommandCenterView`** — `activeAgreements`, `activeCommercialAllocations`, `agreementId`, `agreementStatus`, `agreementType`, `agreementsExpiringSoon`, `agreementsWithExceptions`, `allocationModel`, `brandVenue`, `commercialOwner`, `commercialRiskAlerts`, `commissionModel`, `creditLimit`, `currentCreditExposure`, `currentExposure`, `draftAgreements`, `effectiveFrom`, `effectiveTo`, `expiredAgreements`, `market`, `outstandingReceivables`, `partner`, `partnersOnCreditHold`, `paymentTerms`, `pendingApproval`, `pricingModel`, `totalApprovedCredit`

> ⚠ **27 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P10 PTR-032 Commercial Agreement Command Center

**Decision:** 

### p25  · `setAgreementContractTerm`

`PUT /agreement-contract-term` · PLATFORM_CELL_MANAGE · partner · **Agreement & Contract Terms Builder**

> Create the structured commercial agreement governing the partner relationship.

**`AgreementContractTermsBuilderView`** — `addendum`, `agreementId`, `agreementName`, `agreementType`, `allocationTerms`, `autoRenewal`, `bookingRestrictions`, `brand`, `cancellationConditions`, `commercialAnnex`, `commercialOwner`, `commissionTerms`, `contractReference`, `creditTerms`, `currency`, `effectiveFrom`, `effectiveTo`, `financeOwner`, `legalEntity`, `manualRenewal`, `minimumCommitment`, `nda`, `partner`, `paymentTerms`, `pricingBasis`, `rateSheet`, `renegotiationRequired`, `renewalApproval`, `renewalNoticePeriod`, `renewalType`, `salesTarget`, `settlementTerms`, `signedContract`, `sla`, `territory`, `venue`

> ⚠ **36 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P09 ADM-415 Commercial Agreement, Billable Definition & Customer Acceptance
- serves P10 PTR-033 Agreement & Contract Terms Builder
- serves P17 SGN-023 Commercial Agreement, Billable Definition & Customer Acceptance

**Decision:** 

### p27  · `setPartnerRateNet`

`PUT /partner-rate-net` · PLATFORM_CELL_MANAGE · partner · **Partner Rate & Net Pricing Configuration**

> Define the commercial pricing basis available to a partner without recreating TICVAI's Pricing Engine.

**`PartnerRateNetPricingConfigurationView`** — `agreement`, `approvalThreshold`, `blackoutDates`, `channel`, `effectiveFrom`, `effectiveTo`, `event`, `eventExceptions`, `manualOverride`, `marginFloor`, `market`, `maximumDiscount`, `minimumPermittedRate`, `partner`, `priceCategory`, `product`, `productFamily`, `seasonalRate`, `ticketType`, `venue`

- serves P10 PTR-034 Partner Rate & Net Pricing Configuration

**Decision:** 

### p29  · `listCommissionMarginIncentive`

`GET /commission-margin-incentive` · PLATFORM_TENANT_VIEW · partner · **Commission, Margin & Incentive Management**

> Configure how partner commissions and commercial incentives are calculated.

**`CommissionMarginIncentiveManagementView`** — `agreement`, `campaignIncentive`, `fixedAmount`, `fixedPercentage`, `partner`, `performanceIncentive`, `product`, `productSpecificCommission`, `revenueBasedCommission`, `tieredCommission`, `volumeBasedCommission`

- serves P10 PTR-035 Commission, Margin & Incentive Management

**Decision:** 

### p30  · `listCreditLimitExposure`

`GET /credit-limit-exposure` · PLATFORM_TENANT_VIEW · partner · **Credit Limit & Exposure Management**

> Control the financial exposure TICVAI permits for partners buying on account. This should be one of the strongest finance-control screens in the B2B module. 30 | Pag e

**`CreditLimitExposureManagementView`** — `activeHoldsReservationsAed40000`, `approvalAuthority`, `approvedCreditLimit`, `approvedCreditLimitAed500000`, `availableCreditAed155000`, `creditEnabled`, `creditOwner`, `currency`, `effectiveDates`, `highRiskAt90`, `increaseLimit`, `placeCreditHold`, `reduceLimit`, `riskClassification`, `temporaryCreditLimit`, `temporaryIncrease`, `unbilledTransactionsAed95000`, `unlessAnApprovedExceptionExists`, `warningAt70`

- serves P10 PTR-036 Credit Limit & Exposure Management

**Decision:** 

### p32  · `listDepositGuaranteeFinancial`

`GET /deposit-guarantee-financial` · PLATFORM_TENANT_VIEW · partner · **Deposit, Guarantee & Financial Security Management**

> Manage financial security required to support partner credit or commercial access.

**`DepositGuaranteeFinancialSecurityManagementView`** — `agreement`, `amount`, `bankGuarantee`, `blocksNewCreditSales`, `cashDeposit`, `corporateGuarantee`, `creditExposureAed500000`, `currency`, `document`, `effectiveDate`, `expiryDate`, `generatesWarning`, `guaranteeAed300000`, `issuingInstitution`, `letterOfCredit`, `otherApprovedSecurity`, `partner`, `placesPartnerOnHold`, `prepaymentBalance`, `reducesCredit`, `reference`, `requiresFinanceReview`, `securityDeposit`, `securityId`, `type`, `unsecuredExposureAed200000`, `verificationStatus`

> ⚠ **27 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P10 PTR-037 Deposit, Guarantee & Financial Security Management

**Decision:** 

### p33  · `setPaymentTermBilling`

`PUT /payment-term-billing` · PLATFORM_CELL_MANAGE · partner · **Payment Terms, Billing & Account Configuration**

> Define how the partner pays TICVAI and how transactions are financially grouped.

**`PaymentTermsBillingAccountConfigurationView`** — `availableCredit`, `bankTransfer`, `billingContact`, `billingCurrency`, `billingEntity`, `card`, `consolidatedBilling`, `creditAccount`, `currentBalance`, `depositBalance`, `financeEmail`, `immediatePayment`, `invoiceFrequency`, `invoiceGrouping`, `lastPayment`, `monthlyInvoice`, `nextInvoice`, `oldestOutstandingInvoice`, `otherApprovedMethod`, `outstanding`, `overdue`, `paymentLink`, `perTransactionBilling`, `prepaid`, `prepaidBalance`, `purchaseOrderRequired`, `statementFrequency`, `taxProfile`, `weeklyInvoice`

> ⚠ **29 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P10 PTR-038 Payment Terms, Billing & Account Configuration

**Decision:** 

### p35  · `listCommercialAllocationQuota`

`GET /commercial-allocation-quota` · PLATFORM_TENANT_VIEW · partner · **Commercial Allocation, Quota & Commitment Management**

> Define the commercial commitment of inventory to a partner. This differs from Area 4's operational channel allocation.

**`CommercialAllocationQuotaCommitmentManagementView`** — `agreement`, `allocated`, `automaticRelease`, `booked`, `commitmentAchievement`, `event`, `fixedQuantity`, `guaranteedAllocation`, `guaranteedMinimum`, `manualRelease`, `maximumAllocation`, `minimumCommitment`, `onRequestAllocation`, `partner`, `percentageAllocation`, `product`, `quantity`, `remaining`, `returnRule`, `returned`, `rollingAllocation`, `seasonalAllocation`, `sellThroughTarget`, `sharedAllocation`, `sold`, `takeOrPayWhereCommerciallyApplicable`, `ticketType`, `useItOrReleaseIt`, `utilization`, `venue`

> ⚠ **30 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P10 PTR-039 Commercial Allocation, Quota & Commitment Management

**Decision:** 

### p37  · `approveBookingLimitCommercial`

`PUT /booking-limit-commercial` · PLATFORM_CELL_MANAGE · partner · **Booking Limits, Commercial Exceptions & Approval**

> Control transaction limits and provide a governed mechanism for commercial exceptions.

**`BookingLimitsCommercialExceptionsApprovalView`** — `agreement`, `allocationException`, `amountImpact`, `bookingLimitException`, `cancellationException`, `cancellationLimit`, `commissionException`, `creditException`, `currentRule`, `dailyBookingLimit`, `dependingOnExceptionType`, `dependingOnExceptionValue`, `effectivePeriod`, `eventLimit`, `holdLimit`, `maximumBookingValue`, `maximumTicketsPerBooking`, `monthlyBookingLimit`, `partner`, `paymentTermException`, `priceException`, `productLimit`, `reason`, `requestType`, `requestedException`, `requester`, `reservationDuration`

> ⚠ **27 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P10 PTR-040 Booking Limits, Commercial Exceptions & Approval

**Decision:** 

### p38  · `listCommercialAgreementHealth`

`GET /commercial-agreement-health` · PLATFORM_TENANT_VIEW · partner · **Commercial Agreement 360°, Health & AI Review**

> Give management a single consolidated view of the complete commercial relationship with a partner.

**`CommercialAgreement360HealthAiReviewView`** — `achievement`, `activeApprovedExceptions`, `availableCredit`, `averageDiscount`, `changeTerms`, `channelAllocationArea4`, `commercialRisk`, `contractStatus`, `contractualAllocation`, `currentCommission`, `depositGuarantee`, `effectiveDates`, `expiry`, `exposure`, `incentives`, `increaseReduceCredit`, `intelligence`, `limit`, `minimumSales`, `outstandingBalance`, `overdueAmount`, `paymentTerms`, `placePartnerUnderReview`, `rateModel`, `rebalanceAllocation`, `reduceUnusedCommitment`, `renewAgreement`, `renewal`, `requestCommercialReview`, `requestCreditReview`, `requestUpdatedGuarantee`, `startRenewal`, `utilization`

> ⚠ **33 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P10 PTR-032 Commercial Agreement Command Center
- serves P10 PTR-041 Commercial Agreement 360°, Health & AI Review

**Decision:** 

### p44  · `listPartner2`

`GET /partner-2` · PLATFORM_TENANT_VIEW · partner · **Partner Operations Command Center**

> Provide commercial, operations and finance teams with one real-time view of active B2B, reseller and OTA business.

**`PartnerOperationsCommandCenterView`** — `accountManager`, `activeHolds`, `activePartnerOrders`, `activeReservations`, `allocationUtilization`, `cancellationRate`, `cancellations`, `commission`, `commissionPayable`, `creditUtilization`, `grossSales`, `netSales`, `operationalExceptions`, `operationalStatus`, `orders`, `outstandingBalance`, `outstandingReceivables`, `partner`, `partnerSalesMtd`, `partnerSalesToday`, `partnerType`, `partnersRequiringAttention`, `pendingSettlements`, `refunds`, `risk`, `tickets`, `ticketsSold`

> ⚠ **27 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P10 PTR-022 Partner Management Command Center
- serves P10 PTR-042 Partner Operations Command Center

**Decision:** 

### p46  · `listPartnerOrderBooking`

`GET /partner-order-booking` · PLATFORM_TENANT_VIEW · partner · **Partner Orders & Booking Management**

> Provide a consolidated operational view of orders created by each partner.

**`PartnerOrdersBookingManagementView`** — `agentUser`, `agreement`, `allocation`, `billingStatus`, `bookingLimit`, `cancellationPolicy`, `commission`, `credit`, `customerGuestWhereApplicable`, `fulfillmentStatus`, `grossValue`, `modify`, `netAmount`, `partnerRate`, `partnerReference`, `paymentMethod`, `productEligibility`, `products`, `quantity`, `rate`, `rebook`

- serves P10 PTR-043 Partner Orders & Booking Management

**Decision:** 

### p48  · `listReservationHoldRelease`

`GET /reservation-hold-release` · PLATFORM_TENANT_VIEW · partner · **Reservations, Holds & Release Management**

> Manage inventory temporarily reserved by B2B partners before final confirmation. This is particularly important for tour operators, corporate groups and travel-trade partners.

**`ReservationsHoldsReleaseManagementView`** — `activeHolds`, `allocationSource`, `approvalRequirement`, `commercialValue`, `convertedHolds`, `createdBy`, `event`, `eventCutoff`, `expiredHolds`, `expiringToday`, `heldTickets`, `heldValue`, `holdCreated`, `holdDuration`, `holdExpiry`, `holdId`, `maximumHoldQuantity`, `numberOfExtensions`, `partner`, `partnerHoldLimit`, `product`, `quantity`, `reassignWherePermitted`, `reduceHold`, `releasedInventory`, `seatZoneWhereApplicable`, `status`, `unlessAnApprovedExtensionExists`

> ⚠ **28 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P10 PTR-044 Reservations, Holds & Release Management

**Decision:** 

### p49  · `listPartnerCancellationRefund`

`GET /partner-cancellation-refund` · PLATFORM_TENANT_VIEW · partner · **Partner Cancellations, Refunds & Amendments**

> Manage post-booking changes according to the partner's commercial agreement and product policies.

**`PartnerCancellationsRefundsAmendmentsView`** — `approval`, `cancellationPercentage`, `customerNameChangeWherePermitted`, `dateChange`, `eventProximity`, `exceptionRequest`, `financialImpact`, `fullCancellation`, `newState`, `originalState`, `partialCancellation`, `partnerStatus`, `performanceChange`, `productChange`, `quantityReduction`, `reason`, `ticketReissue`, `transactionValue`, `user`

- serves P10 PTR-045 Partner Cancellations, Refunds & Amendments

**Decision:** 

### p51  · `listPartnerStatementAccount`

`GET /partner-statement-account` · PLATFORM_TENANT_VIEW · partner · **Partner Statement & Account Activity**

> Give finance and commercial teams a complete financial statement for each partner account.

**`PartnerStatementAccountActivityView`** — `adjustments`, `availableCredit`, `closingBalance`, `commission`, `credit`, `credits`, `current`, `customDateRange`, `daily`, `date`, `debit`, `dueDate`, `monthly`, `openingBalance`, `orderInvoice`, `overdueBalance`, `payments`, `reference`, `refunds`, `runningBalance`, `sales`, `status`, `transactionType`, `weekly`

- serves P10 PTR-046 Partner Statement & Account Activity

**Decision:** 

### p52  · `listPartnerReconciliationException`

`GET /partner-reconciliation-exception` · PLATFORM_TENANT_VIEW · partner · **Partner Reconciliation & Exception Management**

> Reconcile operational bookings against financial and channel records and identify discrepancies.

**`PartnerReconciliationExceptionManagementView`** — `acceptDifference`, `amountMismatches`, `cancellationsRefunds`, `commission`, `commissionDifferences`, `correct`, `differenceAed150`, `dispute`, `invoices`, `match`, `mismatchType`, `missingTickets`, `partnerAmountAed12450`, `partnerRates`, `paymentDifferences`, `paymentsCredit`, `pendingInvestigation`, `pricingDifferences`, `recordsReconciled`, `ticketsIssued`, `ticvaiOrders`, `unmatchedOrders`

- serves P10 PTR-047 Partner Reconciliation & Exception Management

**Decision:** 

### p54  · `listCommissionCalculationSettlement`

`GET /commission-calculation-settlement` · PLATFORM_TENANT_VIEW · partner · **Commission Calculation & Settlement Management**

> Calculate, approve and settle commission or incentive amounts owed under partner commercial agreements.

**`CommissionCalculationSettlementManagementView`** — `adjustment`, `approved`, `cancellation`, `chargeback`, `commission`, `commissionAmount`, `commissionBasis`, `commissionCorrection`, `commissionEarned`, `commissionPending`, `currency`, `customCycle`, `eventBased`, `grossValue`, `incentive`, `incentiveQualification`, `incentivesEarned`, `legalEntity`, `monthly`, `netRate`, `nextSettlement`, `onHold`, `order`, `paid`, `partialFulfillment`, `partner`, `payableAmount`, `perTransaction`, `period`, `product`, `reversed`, `weekly`

> ⚠ **32 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P10 PTR-048 Commission Calculation & Settlement Management

**Decision:** 

### p56  · `listPartnerDisputeCase`

`GET /partner-dispute-case` · PLATFORM_TENANT_VIEW · partner · **Partner Disputes, Cases & Service Management**

> Provide a structured case-management environment for partner operational and commercial disputes.

**`PartnerDisputesCasesServiceManagementView`** — `allocationIssue`, `amountInDispute`, `apiIssue`, `assignments`, `attachments`, `bookingDispute`, `cancellationDispute`, `caseId`, `category`, `commissionDispute`, `contact`, `creditDispute`, `departmentEscalation`, `description`, `evidence`, `financeReview`, `firstResponse`, `invoiceDispute`, `notes`, `owner`, `partner`, `pricingDispute`, `priority`, `proposedResolvedClosed`, `relatedInvoice`, `relatedOrder`, `relatedSettlement`, `resolutionTarget`, `settlementDispute`, `sla`, `slaBreach`, `status`, `technicalReview`, `ticketIssue`, `timeOpen`

> ⚠ **35 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P10 PTR-049 Partner Disputes, Cases & Service Management

**Decision:** 

### p57  · `listPartnerPerformanceScorecard`

`GET /partner-performance-scorecard` · PLATFORM_TENANT_VIEW · partner · **Partner Performance Scorecard & Risk Monitoring**

> Create a consistent scorecard for evaluating the quality and commercial value of every partner relationship.

**`PartnerPerformanceScorecardRiskMonitoringView`** — `agreementStatus`, `apiSuccess`, `averageOrderValue`, `cancellationRate`, `creditUtilization`, `declining`, `documentation`, `errorRate`, `growth`, `improving`, `margin`, `overdueBalance`, `paymentTimeliness`, `portfolioAverage`, `returnedInventory`, `revenue`, `sales`, `sameChannel`, `sameMarket`, `samePartnerType`, `securityGuaranteeStatus`, `sellThrough`, `stable`, `supportCases`, `transactionFailureRate`, `utilization`

> ⚠ **26 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P10 PTR-050 Partner Performance Scorecard & Risk Monitoring

**Decision:** 

### p59  · `listPartnerRelationship`

`GET /partner-relationship` · PLATFORM_TENANT_VIEW · partner · **Partner AI Intelligence & Relationship Optimization**

> Provide TICVAI's AI decision-support layer across the complete partner lifecycle. This screen should combine information from Boards 1, 2 and 3.

**`PartnerAiIntelligenceRelationshipOptimizationView`** — `additionalSales`, `agreements`, `ai`, `allocation`, `area8CompleteArchitecture`, `billingAllocationLimits`, `board2CommercialManagement`, `cancellations`, `cases`, `channelPerformance`, `chartAddedAtTheEnd`, `commission`, `confidence`, `credit`, `creditExposure`, `dashboard`, `expectedImpact`, `historicalTrends`, `howIsTheRelationshipPerforming`, `inventoryRisk`, `launchTheAppropriateGovernedWorkflow`, `management`, `margin`, `orders`, `partnerProfile`, `partnerReconciliationExceptionOperationalFinancial`, `paymentBehavior`, `rates`, `reason`, `recommendation`, `releasing320Tickets`, `revenue`, `risks`, `screenBackendScreenPrimaryResponsibility`, `settlement`, `supportingMetrics`, `territory`, `usingConfigurableBusinessCriteria`, `velocity`, `whoIsThePartner`

> ⚠ **40 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P10 PTR-051 Partner AI Intelligence & Relationship Optimization

**Decision:** 


---

## Membership Annual Pass Management

### p4   · `listMembershipAnnualPass`

`GET /membership-annual-pass` · PLATFORM_TENANT_VIEW · staff · **Membership & Annual Pass Command Center**

> Provide administrators with a centralized view of all membership, annual pass, season pass and subscription-style admission products.

**`MembershipAnnualPassCommandCenterView`** — `activationMethod`, `activeMembers`, `activeMembershipProducts`, `annualPass`, `annualPassProducts`, `averageMembershipDuration`, `conflictingRules`, `corporateMembership`, `currentMembers`, `customMembership`, `draftProducts`, `effectiveDates`, `familyIndividual`, `familyMembership`, `familyMemberships`, `fixedTermMembership`, `individualMembership`, `invalidEligibility`, `membershipName`, `membershipsExpiringSoon`, `missingEntitlements`, `missingPricingAssociation`, `missingRenewalPolicy`, `missingValidity`, `monthlyMembership`, `owner`, `preview`, `productId`, `productsWithConfigurationIssues`, `renewal`, `renewalEnabledProducts`, `seasonPass`, `status`, `studentMembership`, `suspendedProducts`, `tier`, `type`, `validity`, `venueAttraction`, `vipMembership`

> ⚠ **40 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P08 BO-284 Membership & Annual Pass Command Center

**Decision:** 

### p5   · `setMembershipProductTier`

`PUT /membership-product-tier` · PLATFORM_CELL_MANAGE · staff · **Membership Product & Tier Builder**

> Configure the fundamental definition and hierarchy of a membership/pass.

**`MembershipProductTierBuilderView`** — `admissionBasedBenefitBasedHybrid`, `attraction`, `autoRenewEligible`, `brand`, `contracts`, `currencyContext`, `customTiers`, `description`, `displayOrder`, `effectiveFrom`, `effectiveTo`, `gold`, `individualFamilyCorporate`, `market`, `membershipCode`, `membershipName`, `membershipType`, `namedTransferable`, `parentMembership`, `physicalDigital`, `platinum`, `renewableNonRenewable`, `replacementMembership`, `silver`, `standard`, `tierLevel`, `venue`, `vip`

> ⚠ **28 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P08 BO-285 Membership Product & Tier Builder

**Decision:** 

### p7   · `setMembershipEligibilityQualification`

`PUT /membership-eligibility-qualification` · PLATFORM_CELL_MANAGE · staff · **Membership Eligibility & Qualification Rule Builder**

> Determine who is allowed to purchase, activate, hold or renew a particular membership.

**`MembershipEligibilityQualificationRuleBuilderView`** — `age`, `allowDifferentRules`, `approvedCorporateAccountRequired`, `channel`, `corporateAffiliation`, `country`, `customerDeclaration`, `customerSegment`, `documentVerification`, `existingMembership`, `existingTierRequirement`, `externalVerification`, `identityVerification`, `membershipHistory`, `multipleMembershipsAllowed`, `mutuallyExclusiveMemberships`, `noVerification`, `oneMembershipPerCustomer`, `personType`, `prerequisiteMembership`, `previousPurchase`, `promotionalQualification`, `residency`, `residencyVerificationRequired`, `staffVerification`, `studentStatus`, `venue`, `withAnExplanation`

> ⚠ **28 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P08 BO-286 Membership Eligibility & Qualification Rule Builder

**Decision:** 

### p8   · `setValidityActivationExpiry`

`PUT /validity-activation-expiry` · PLATFORM_CELL_MANAGE · staff · **Validity, Activation & Expiry Configuration**

> Define exactly when a membership becomes valid, how long it remains valid and how it expires.

**`ValidityActivationExpiryConfigurationView`** — `configuredEnd`, `configuredStart`, `customerActivation`, `firstVisit`, `fixedStartDate`, `immediateOnPurchase`, `manualActivation`

- serves P08 BO-287 Validity, Activation & Expiry Configuration

**Decision:** 

### p9   · `setMembershipEntitlementAdmission`

`PUT /membership-entitlement-admission` · PLATFORM_CELL_MANAGE · staff · **Membership Entitlement & Admission Benefit Builder**

> Define exactly what the member receives. This is the heart of the membership product.

**`MembershipEntitlementAdmissionBenefitBuilderView`** — `accountShared`, `admissionType`, `attraction`, `attractionAccess`, `bookingPrivileges`, `days`, `dependentSpecific`, `eventAccess`, `eventType`, `fBBenefit`, `familyShared`, `fastTrack`, `freeParking`, `guestTickets`, `lifetimeOfMembership`, `limitedAdmissions`, `memberSpecific`, `numberOfVisits`, `otherConfiguredBenefits`, `parking`, `perDay`, `perMembershipYear`, `perMonth`, `perWeek`, `period`, `priorityEntry`, `rentalBenefit`, `retailBenefit`, `specialEventAccess`, `times`, `timeslots`, `unlimitedAdmission`, `unlimitedGeneralAdmission`, `venue`, `zoneAccess`

> ⚠ **35 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P08 BO-288 Membership Entitlement & Admission Benefit Builder

**Decision:** 

### p11  · `listMembershipUsageVisit`

`GET /membership-usage-visit` · PLATFORM_TENANT_VIEW · staff · **Membership Usage, Visit & Consumption Rules**

> Control how membership entitlements may actually be consumed. Screen 13.1.5 defines what the member receives. Screen 13.1.6 defines how it may be used.

**`MembershipUsageVisitConsumptionRulesView`** — `advanceBookingLimit`, `benefitConsumption`, `but`, `cancellationLimit`, `concurrentReservations`, `guestUsage`, `maximumActiveFutureReservations`, `maximumAdmissionsPerPeriod`, `maximumAdvanceBookingDays`, `maximumVisitsPerDay`, `noReEntry`, `noShowTreatment`, `parking12UsesThisYear`, `reEntryAfterXMinutes`, `reEntryCooldown`, `reservationOptional`, `reservationRequired`, `rules`, `sameDayReEntry`, `unlimitedSameDayReEntry`, `venueSpecificRule`, `walkInAllowed`

- serves P08 BO-289 Membership Usage, Visit & Consumption Rules

**Decision:** 

### p12  · `setFamilyHouseholdDependent`

`PUT /family-household-dependent` · PLATFORM_CELL_MANAGE · staff · **Family, Household & Dependent Membership Configuration**

> Support memberships covering more than one person while preserving individual identities and entitlements.

**`FamilyHouseholdDependentMembershipConfigurationView`** — `allowed`, `approval`, `authorizedManager`, `child`, `corporateGroup`, `couple`, `customGroupStructure`, `dependent`, `effectiveDate`, `eligibilityRevalidation`, `family`, `fee`, `frequency`, `gracePeriod`, `guardian`, `household`, `individual`, `manualReview`, `maximum3Children`, `maximumAge`, `minimumAge`, `parentChild`, `primaryMember`, `relationshipRequirement`, `renewalCorrection`, `sameHouseholdRequirementWhereApplicable`, `secondaryAdult`, `verificationRequirement`

> ⚠ **28 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P08 BO-290 Family, Household & Dependent Membership Configuration

**Decision:** 

### p14  · `listMembershipCommercialPricing`

`GET /membership-commercial-pricing` · PLATFORM_TENANT_VIEW · staff · **Membership Commercial, Pricing & Channel Association**

> Connect the membership contract to TICVAI's central commercial engines without duplicating pricing configuration.

**`MembershipCommercialPricingChannelAssociationView`** — `alwaysAvailable`, `api`, `area13IdentifiesEligibilityBenefit`, `autoRenewPayment`, `b2b`, `b2c`, `basePricingProfile`, `boxOffice`, `callCenter`, `callCenterBoxOffice`, `capacityLimited`, `corporate`, `corporateCredit`, `feeProfile`, `fixedSalesWindow`, `fullPayment`, `installmentsWhereSupported`, `invitationOnly`, `kiosk`, `membershipTierPrice`, `mobileApp`, `pos`, `promotionalPricingEligibility`, `renewalPrice`, `reseller`, `seasonalSale`, `taxProfile`

> ⚠ **27 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P08 BO-291 Membership Commercial, Pricing & Channel Association
- serves P09 ADM-048 Commercial Pricing Command Center

**Decision:** 

### p15  · `setRenewalAutoMembership`

`PUT /renewal-auto-membership` · PLATFORM_CELL_MANAGE · staff · **Renewal, Auto-Renewal & Membership Continuity Configuration**

> Define how a membership moves from one validity period into the next.

**`RenewalAutoRenewalMembershipContinuityConfigurationView`** — `age`, `agentAssistedRenewal`, `autoRenewal`, `consentRequirement`, `corporateAssociation`, `currentMembershipPrice`, `customerSelfServiceRenewal`, `eligibleProducts`, `failureHandling`, `fixedRenewalRate`, `invitationOnlyRenewal`, `loyaltyRate`, `manualRenewal`, `membershipStatus`, `nonRenewable`, `outstandingBalance`, `paymentMethodRequirement`, `preRenewalNotification`, `protectedRenewalPrice`, `qualification`, `renewalDiscount`, `residency`, `sameTierOnly`, `suggestedTier`, `through`

- serves P08 BO-292 Renewal, Auto-Renewal & Membership Continuity Configuration
- serves P09 ADM-464 Renewal Management Center

**Decision:** 

### p17  · `approveMembershipProductValidation`

`PUT /membership-product-validation` · PLATFORM_CELL_MANAGE · staff · **Membership Product Validation, Approval, Publication & Versioning**

> Provide the final governance layer before a membership/pass configuration becomes commercially available.

**`MembershipProductValidationApprovalPublicationVersioView`** — `accessControl`, `accessDependencies`, `activation`, `activeMembersAffected`, `allowFutureConfigurationChanges`, `b2b`, `b2c`, `callCenter`, `catalogueAssociation`, `channelAvailability`, `channels`, `configuredMigrationPolicy`, `effective1Jan`, `eligibilityRules`, `entitlements`, `entitlementsAffected`, `futureRenewals`, `intelligence`, `membershipPass`, `mobileApp`, `otherDependentServices`, `pos`, `pricingAssociation`, `pricingDependencies`, `productDefinitionComplete`, `renewalPolicy`, `requiredCredentialConfiguration`, `taxFeeAssociation`, `ticketing`, `usageRules`, `validity`

> ⚠ **31 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P08 BO-293 Membership Product Validation, Approval, Publication & Versioning
- serves P08 BO-503 Product Validation, Approval & Publication

**Decision:** 

### p21  · `listMember`

`GET /member` · PLATFORM_TENANT_VIEW · staff · **Member Operations Command Center**

> Provide membership teams with a real-time operational dashboard for the complete active member population.

**`MemberOperationsCommandCenterView`** — `activatedToday`, `activationDate`, `activeMembers`, `atRiskMembers`, `expiringIn30Days`, `expiryDate`, `frozenMemberships`, `member`, `membershipExceptions`, `membershipId`, `membershipProduct`, `membershipStatus`, `newMembersToday`, `outstandingIssue`, `owner`, `pendingActivation`, `renewalDue`, `renewalRate`, `renewalStatus`, `renewedThisMonth`, `suspendedMemberships`, `tier`, `usageLevel`, `venue`

- serves P08 BO-294 Member Operations Command Center

**Decision:** 

### p22  · `setMemberMembershipAccount`

`PUT /member-membership-account` · PLATFORM_CELL_MANAGE · staff · **Member 360° Membership Account Workspace**

> Provide a complete operational view of an individual member and their membership contract. This should be the primary screen an authorized membership-service agent opens when helping a member.

**`Member360MembershipAccountWorkspaceView`** — `activationDate`, `activationMethod`, `autoRenewStatus`, `credentialStatus`, `customerId`, `dependents`, `expiryDate`, `fBBenefit`, `individualBenefits`, `manageDependents`, `memberName`, `membershipChanges`, `membershipId`, `membershipProduct`, `membershipVersion`, `originalOrder`, `payments`, `primaryMember`, `primaryVenue`, `purchaseChannel`, `purchaseDate`, `refunds`, `renew`, `renewalPolicy`, `renewalStatus`, `renewals`, `retailBenefit`, `secondaryAdult`, `sharedBenefits`, `status`, `tier`, `upgrades`, `validity`

> ⚠ **33 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P08 BO-295 Member 360° Membership Account Workspace

**Decision:** 

### p24  · `listMembershipActivationCredential`

`GET /membership-activation-credential` · PLATFORM_TENANT_VIEW · staff · **Membership Activation, Assignment & Credential Management**

> Manage the operational process that turns a purchased membership product into an active membership assigned to a specific individual.

**`MembershipActivationAssignmentCredentialManagementView`** — `activationDeadline`, `activationFailed`, `activationMethod`, `age`, `awaitingActivation`, `awaitingDocumentVerification`, `awaitingIdentityVerification`, `awaitingMemberAssignment`, `barcode`, `calculatedExpiry`, `dependentRelationship`, `digitalMembershipCard`, `dynamicQr`, `eligibility`, `eligibleActivationDate`, `identity`, `nfc`, `photograph`, `physicalCard`, `purchaseDate`, `reason`, `requiredDocuments`, `residency`, `rfid`, `selectedStartDate`, `termsAcceptance`, `walletPass`

> ⚠ **27 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P08 BO-296 Membership Activation, Assignment & Credential Management

**Decision:** 

### p26  · `listVisitAdmissionEntitlement`

`GET /visit-admission-entitlement` · PLATFORM_TENANT_VIEW · staff · **Visit, Admission & Entitlement Usage Monitor**

> Provide membership teams with complete visibility of how a member uses admission and other membership entitlements.

**`VisitAdmissionEntitlementUsageMonitorView`** — `approvalWhereRequired`, `attraction`, `benefitExhausted`, `benefitUsage`, `blackoutAttempt`, `credential`, `date`, `entryTime`, `exitWhereAvailable`, `expiredMembershipUsage`, `gate`, `guest`, `guestTicketsRemaining`, `guestTicketsUsed`, `invalidReEntry`, `lastVisit`, `newValue`, `noShows`, `parkingUses`, `previousValue`, `reason`, `reservation`, `suspendedMembershipAttempt`, `totalVisits`, `upcomingReservation`, `usageAboveLimit`, `user`, `validationResult`, `venue`, `visitsThisMonth`

> ⚠ **30 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P08 BO-297 Visit, Admission & Entitlement Usage Monitor

**Decision:** 

### p27  · `listMembershipFreezeSuspension`

`GET /membership-freeze-suspension` · PLATFORM_TENANT_VIEW · staff · **Membership Freeze, Suspension & Reactivation Management**

> Manage temporary interruption of membership rights without necessarily terminating the membership contract.

**`MembershipFreezeSuspensionReactivationManagementView`** — `administrativeHold`, `approvedBy`, `duration`, `endDate`, `otherGovernedReason`, `policy`, `reactivate`, `reason`, `requestedBy`, `startDate`

- serves P08 BO-298 Membership Freeze, Suspension & Reactivation Management

**Decision:** 

### p29  · `listMembershipUpgradeDowngrade`

`GET /membership-upgrade-downgrade` · PLATFORM_TENANT_VIEW · staff · **Membership Upgrade, Downgrade & Product Migration Operations**

> Manage operational movement of an active member between membership products or tiers.

**`MembershipUpgradeDowngradeProductMigrationOperationsView`** — `area10ForPriceDifference`, `area11ForUpgradeConversionLogic`, `area12ForResultingOrderPayment`, `currentMembership`, `customerQualification`, `dD`, `effectiveDate`, `endOfCurrentTerm`, `entitlements`, `fixedDate`, `guest`, `immediately`, `nextRenewal`, `nextVisit`, `outstandingBalance`, `remainingValidity`, `targetMembership`, `usage`

- serves P08 BO-299 Membership Upgrade, Downgrade & Product Migration Operations

**Decision:** 

### p30  · `listRenewalAuto`

`GET /renewal-auto` · PLATFORM_TENANT_VIEW · staff · **Renewal Operations & Auto-Renewal Management**

> Operationally manage memberships approaching expiry and execute the renewal policies configured in Board 1.

**`RenewalOperationsAutoRenewalManagementView`** — `accordingToBoard1Configuration`, `autoRenew`, `autoRenewFailed`, `autoRenewScheduled`, `consent`, `currentStatus`, `eligibility`, `expiry`, `gracePeriod`, `member`, `membership`, `membershipVersion`, `outstandingIssues`, `paymentMethod`, `paymentMethodStatus`, `paymentPending`, `pricing`, `renewalEligible`, `renewalInvitationSent`, `renewalNotOpen`, `renewalPrice`, `renewalStarted`, `renewalStatus`, `renewalWindow`, `renewed`, `tier`

> ⚠ **26 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P08 BO-300 Renewal Operations & Auto-Renewal Management
- serves P09 ADM-376 Commercial Optimization & Expansion Opportunities
- serves P09 ADM-464 Renewal Management Center

**Decision:** 

### p32  · `listMemberExceptionOverride`

`GET /member-exception-override` · PLATFORM_TENANT_VIEW · staff · **Member Exceptions, Overrides & Service Recovery**

> Provide controlled handling of member-specific situations that fall outside normal membership policy.

**`MemberExceptionsOverridesServiceRecoveryView`** — `activationExtension`, `complimentaryBenefit`, `complimentaryRenewal`, `dependentException`, `duration`, `eligibilityOverride`, `entitlementAdjustment`, `entitlementImpact`, `exceptionType`, `expiryExtension`, `financialImpact`, `member`, `membership`, `membershipTier`, `reason`, `renewalException`, `replacementCredential`, `requestedAction`, `requestedException`, `requestor`, `standardPolicyResult`, `supportingDocumentation`, `suspensionOverride`, `value`

- serves P08 BO-301 Member Exceptions, Overrides & Service Recovery
- serves P08 BO-949 Approval, Exception & Override Control Center

**Decision:** 

### p33  · `listMemberLifecycleCase`

`GET /member-lifecycle-case` · PLATFORM_TENANT_VIEW · staff · **Member Lifecycle History, Audit & Case Timeline**

> Maintain a complete historical record of everything that has happened to the membership from purchase to final expiry.

**`MemberLifecycleHistoryAuditCaseTimelineView`** — `accessEvent`, `activation`, `agent`, `api`, `approval`, `assignment`, `audit`, `benefitUsage`, `cancellation`, `case`, `compliance`, `credential`, `credentialChanges`, `customer`, `customerService`, `dependentChanges`, `events`, `exceptions`, `expiry`, `finance`, `forConfigurationSensitiveMemberChangesCapture`, `integration`, `management`, `manager`, `order`, `payment`, `previousValueNewValue`, `purchase`, `reactivation`, `renewal`, `reservation`, `serviceRecovery`, `suspension`, `system`, `ticket`, `visits`

> ⚠ **36 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P08 BO-302 Member Lifecycle History, Audit & Case Timeline

**Decision:** 

### p35  · `listMembershipRenewalRetention`

`GET /membership-renewal-retention` · PLATFORM_TENANT_VIEW · staff · **Membership Analytics, Renewal Intelligence & AI Retention Center**

> Turn membership operational data into actionable intelligence for retention, renewal, product optimization and member engagement.

**`MembershipAnalyticsRenewalIntelligenceAiRetentionCenView`** — `activeMembers`, `autoRenewSuccess`, `averageMembershipTenure`, `averageVisitsPerMember`, `backendScreenCoreResponsibility`, `benefitUsage`, `benefitUtilization`, `churnRate`, `complaintsExceptions`, `confidence`, `dataFreshness`, `entitlements`, `expectedChurn`, `expectedRenewals`, `freezeSuspensionRate`, `guestTicketUsage`, `keyDrivers`, `member360MembershipAccountWorkspace`, `membershipBaseGrowth`, `membershipExpiresIn21Days`, `membershipUtilization`, `modelVersion`, `newMemberships`, `noVisitsIn90Days`, `previousRenewalOccurredLate`, `renewal`, `renewalRate`, `renewalRevenue`, `reservationBehavior`, `revenuePerMember`, `spend`, `twoUnusedGuestBenefits`, `visits`, `visitsDown58`

> ⚠ **34 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P08 BO-303 Membership Analytics, Renewal Intelligence & AI Retention Center
- serves P09 ADM-375 Renewal & Retention Center

**Decision:** 

