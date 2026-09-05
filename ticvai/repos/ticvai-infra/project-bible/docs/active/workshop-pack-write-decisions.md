# The 153 drafted writes, and whether each deserves a table

*Derived by `tools/derive-write-decisions.py`. Do not edit; re-run it.*

Every drafted read is settled: a command centre, a list or an analytics screen is a **projection**, assembled at read time from tables that already exist, and all 424 say so in their own persistence tag. This document is about the other 153.

## What was measured

For each drafted write, its request fields against the real columns of every table its contract owns, read out of `backend/*/0*.sql`.

| | writes |
|---|---:|
| Look like an update to a table that exists (>=50% overlap) | **0** |
| Share a few fields with something (1-24%) | **50** |
| Share **not one field** with any table the package has | **103** |
| **Total** | **153** |

**The pack is not a data model.** It specifies screens, and the fields those screens configure are vocabulary this package does not currently store. That is the finding, and it is why no table was created: 153 tables asserted from a PDF reading, with names this package generated rather than names anyone agreed, would be the largest single change to the data model in its history and wrong in detail everywhere.

A name match would have said the opposite. Fuzzy-matching screen titles against table names claimed 77 of these already had a home, pairing `setMinorGuardianAge` with `marketing.privacy_incident` at a score of 100. The fields disagree with the names, and the fields are what a table is made of.

## Where to start: the 13 the client wrote as records

These carry an explicit per-entity directory - the client writing a row rather than a screen. They are the strongest candidates for a real table and the cheapest to settle.

| Operation | Screen | The pack's words | Fields | Nearest table |
|---|---|---|---:|---|
| `setAccessAreaZone` | Access Area & Zone Builder | *Each zone receives* | 7 | `access.parking_facility` 14% |
| `setOrderDetailTransaction` | Order Detail & Transaction Workspace | *Each line should display* | 14 | `orders.cart_line` 14% |
| `setVirtualTicketCredential` | Virtual Ticket & Credential 360° Workspace | *For each media show* | 24 | `access.entitlement` 9% |
| `setAttractionAccess` | Attraction Access Configuration | *For each attraction* | 17 | `access.parking_facility` 6% |
| `setChannelPricingCommercial` | Channel Pricing & Commercial Profile Assignm | *For each assignment* | 17 | `catalogue.price_list` 6% |
| `approvePricingWorkflowAuthority` | Pricing Approval Workflow & Authority Matrix | *Every approval action records* | 27 | `catalogue.channel_allocation` 4% |
| `setRateStructure` | Rate Structure Builder | *Each rate should contain* | 25 | `catalogue.price` 4% |
| `setChannelProvider` | Channel & Provider Configuration | *For each provider* | 26 | `control.api_client` 4% |
| `setConsentCapturePoint` | Consent Capture Point & Customer Journey Con | *For each capture point define* | 28 | `marketing.attribution_touch` 4% |
| `setGroupOperationalPlanning` | Group Operational Planning & Task Workspace | *Each task should contain* | 32 | `catalogue.price_list` 3% |
| `setGroupQuotationProposal` | Group Quotation Builder & Proposal Generatio | *For each line* | 30 | `orders.cart` 3% |
| `setOrderReservationStatus` | Order & Reservation Status Lifecycle Configu | *For each transition define* | 11 | none |
| `setGuestChoiceBuild` | Guest Choice & Build-Your-Own Bundle Designe | *For each group* | 19 | none |

## Every drafted write

`Fields` is what the operation accepts today; each one carries the sentence it was read from in its own `description`. `Nearest` is the closest existing table by field overlap - a low number is evidence that this is not an update to it.

### access (40)

| Operation | Screen | Fields | Nearest | Permission | Scope |
|---|---|---:|---|---|---|
| `setAccessAreaZone` | Access Area & Zone Builder | 7 | `access.parking_facility` 14% | `ACCESS_POINT_CONFIGURE` | venue |
| `setVirtualTicketCredential` | Virtual Ticket & Credential 360° Workspace | 24 | `access.entitlement` 9% | `ACCESS_POINT_CONFIGURE` | venue |
| `setAttractionAccess` | Attraction Access Configuration | 17 | `access.parking_facility` 6% | `ACCESS_POINT_CONFIGURE` | venue |
| `setDynamicSecurityProfile` | Dynamic QR Security Profile Builder | 15 | `access.scan_event` 7% | `ACCESS_POINT_CONFIGURE` | venue |
| `setDynamicFieldData` | Dynamic Fields, Data Mapping & Content Builder | 40 | `access.entitlement` 3% | `ACCESS_POINT_CONFIGURE` | venue |
| `approveManualOverrideSupervisor` | Manual Override & Supervisor Approval | 6 | — | `ACCESS_POINT_CONFIGURE` | venue |
| `approveMultiMediaPreview` | Multi-Media Preview, Testing, Approval & Publi | 40 | — | `ACCESS_POINT_CONFIGURE` | venue |
| `publishMediaCompatibilityTesting` | Media Compatibility, Testing & Publication | 10 | — | `ACCESS_POINT_CONFIGURE` | venue |
| `publishRuleConflictCheck` | Rule Simulation, Conflict Check & Publication | 16 | — | `ACCESS_POINT_CONFIGURE` | venue |
| `publishTopologyValidation` | Topology Validation & Publication | 10 | — | `ACCESS_POINT_CONFIGURE` | venue |
| `setAccessGraphicalMap` | Access Control Graphical Map Designer | 7 | — | `ACCESS_POINT_CONFIGURE` | venue |
| `setAppleWalletPass` | Apple Wallet Pass Designer | 25 | — | `ACCESS_POINT_CONFIGURE` | venue |
| `setBiometricVerificationProfile` | Biometric Verification Profile Builder | 9 | — | `ACCESS_POINT_CONFIGURE` | venue |
| `setBleBeaconGeofence` | BLE Beacon & Geofence Configuration | 12 | — | `ACCESS_POINT_CONFIGURE` | venue |
| `setContextTimeEvent` | Context, Time, Event & Capacity Policy Builder | 10 | — | `ACCESS_POINT_CONFIGURE` | venue |
| `setDeviceSoftwareContent` | Device Software, Content & Remote Configuratio | 16 | — | `ACCESS_POINT_CONFIGURE` | venue |
| `setDigitalBarcodeTicket` | Digital QR & Barcode Ticket Designer | 40 | — | `ACCESS_POINT_CONFIGURE` | venue |
| `setDigitalCardMembership` | Digital Card, Membership & Wearable Designer | 21 | — | `ACCESS_POINT_CONFIGURE` | venue |
| `setEdgeNodeLocal` | Edge Node & Local Processing Configuration | 15 | — | `ACCESS_POINT_CONFIGURE` | venue |
| `setEmbeddedEntitlementPayload` | Embedded Entitlement Payload Designer | 19 | — | `ACCESS_POINT_CONFIGURE` | venue |
| `setFacePassEnrollment` | Face Pass Enrollment Configuration | 13 | — | `ACCESS_POINT_CONFIGURE` | venue |
| `setGateLane` | Gate & Lane Configuration | 17 | — | `ACCESS_POINT_CONFIGURE` | venue |
| `setGoogleWalletPass` | Google Wallet Pass Designer | 27 | — | `ACCESS_POINT_CONFIGURE` | venue |
| `setGroupAdmissionProfile` | Group & B2B Admission Profile Builder | 20 | — | `ACCESS_POINT_CONFIGURE` | venue |
| `setHandheldMobileAccess` | Handheld & Mobile Access Device Configuration | 19 | — | `ACCESS_POINT_CONFIGURE` | venue |
| `setMediaBindingActivation` | Media Binding, Activation & Assignment Operati | 13 | — | `ACCESS_POINT_CONFIGURE` | venue |
| `setOperationalIncidentException` | Operational Incident & Exception Workspace | 14 | — | `ACCESS_POINT_CONFIGURE` | venue |
| `setPdfPrintablePos` | PDF, Printable & POS Ticket Designer | 28 | — | `ACCESS_POINT_CONFIGURE` | venue |
| `setReaderScannerPeripheral` | Reader, Scanner & Peripheral Configuration | 2 | — | `ACCESS_POINT_CONFIGURE` | venue |
| `setRealTimeSecurity` | Real-Time Security Response & Playbook Builder | 8 | — | `ACCESS_POINT_CONFIGURE` | venue |
| `setRfidNfc` | RFID & NFC Configuration | 18 | — | `ACCESS_POINT_CONFIGURE` | venue |
| `setRfidNfcCard` | RFID, NFC, Card & Wristband Media Designer | 35 | — | `ACCESS_POINT_CONFIGURE` | venue |
| `setSecurityInvestigationEvidence` | Security Investigation & Evidence Workspace | 16 | — | `ACCESS_POINT_CONFIGURE` | venue |
| `setTurnstileLaneBehavior` | Turnstile & Lane Behavior Configuration | 15 | — | `ACCESS_POINT_CONFIGURE` | venue |
| `setValidationOutcomeGuest` | Validation Outcome & Guest Feedback Designer | 14 | — | `ACCESS_POINT_CONFIGURE` | venue |
| `setVirtualTicketIdentity` | Virtual Ticket Identity & Master Record Config | 40 | — | `ACCESS_POINT_CONFIGURE` | venue |
| `setVisualAccessRule` | Visual Access Rule Builder | 5 | — | `ACCESS_POINT_CONFIGURE` | venue |
| `setVisualDynamicPolicy` | Visual Dynamic Policy Builder | 7 | — | `ACCESS_POINT_CONFIGURE` | venue |
| `simulateOfflineResilienceTesting` | Offline Simulation & Resilience Testing | 7 | — | `ACCESS_POINT_CONFIGURE` | venue |
| `simulatePolicyConflictImpact` | Policy Simulation, Conflict & Impact Analysis | 3 | — | `ACCESS_POINT_CONFIGURE` | venue |

### catalogue (30)

| Operation | Screen | Fields | Nearest | Permission | Scope |
|---|---|---:|---|---|---|
| `setChannelPricingCommercial` | Channel Pricing & Commercial Profile Assignmen | 17 | `catalogue.price_list` 6% | `PRODUCT_CONFIGURE` | venue |
| `approvePricingWorkflowAuthority` | Pricing Approval Workflow & Authority Matrix | 27 | `catalogue.channel_allocation` 4% | `PRODUCT_CONFIGURE` | venue |
| `setRateStructure` | Rate Structure Builder | 25 | `catalogue.price` 4% | `PRODUCT_CONFIGURE` | venue |
| `setPriceHierarchyInheritance` | Price Hierarchy & Inheritance Configuration | 6 | `catalogue.price_list` 17% | `PRODUCT_CONFIGURE` | venue |
| `setFeeApplicabilityCharging` | Fee Applicability & Charging Rule Builder | 21 | `catalogue.channel_allocation` 5% | `PRODUCT_CONFIGURE` | venue |
| `setPricingExperiment` | A/B Pricing Experiment Studio | 22 | `catalogue.channel_allocation` 5% | `PRODUCT_CONFIGURE` | venue |
| `publishActivationScheduler` | Publication & Activation Scheduler | 23 | `catalogue.channel_allocation` 4% | `PRODUCT_CONFIGURE` | venue |
| `setPricingChangeRequest` | Pricing Change Request & Workspace | 30 | `catalogue.entitlement_template` 3% | `PRODUCT_CONFIGURE` | venue |
| `approveReviewDecision` | Approval Review & Decision Workspace | 17 | — | `PRODUCT_CONFIGURE` | venue |
| `approveWorkflow` | Approval Workflow Designer | 17 | — | `PRODUCT_CONFIGURE` | venue |
| `createBulkProductCatalogue` | Bulk Product Creation & Catalogue Import | 9 | — | `PRODUCT_CONFIGURE` | venue |
| `createChannelProfile` | Channel Creation & Profile Configuration | 34 | — | `PRODUCT_CONFIGURE` | venue |
| `createLiveDynamicPrice` | Live Dynamic Price Execution & Deployment Moni | 15 | — | `PRODUCT_CONFIGURE` | venue |
| `publishChannelAvailability` | Channel Publication & Availability | 3 | — | `PRODUCT_CONFIGURE` | venue |
| `publishChannelReadinessValidation` | Channel Publication, Readiness & AI Validation | 17 | — | `PRODUCT_CONFIGURE` | venue |
| `publishPricingEffectiveDate` | Pricing Publication & Effective-Date Scheduler | 13 | — | `PRODUCT_CONFIGURE` | venue |
| `setBookingVelocityTime` | Booking Velocity & Time-to-Event Rule Builder | 21 | — | `PRODUCT_CONFIGURE` | venue |
| `setCatalogueReview` | AI Catalogue Builder & Configuration Review | 6 | — | `PRODUCT_CONFIGURE` | venue |
| `setChannelFeePayment` | Channel Fees, Payment & Fulfillment Configurat | 29 | — | `PRODUCT_CONFIGURE` | venue |
| `setDemandOccupancyAvailability` | Demand, Occupancy & Availability Rule Builder | 9 | — | `PRODUCT_CONFIGURE` | venue |
| `setDynamicPricingStrategy` | Dynamic Pricing Strategy Builder | 28 | — | `PRODUCT_CONFIGURE` | venue |
| `setLifecycleStatuWorkflow` | Lifecycle Status & Workflow Configuration | 10 | — | `PRODUCT_CONFIGURE` | venue |
| `setPriceListMaster` | Price List Master Configuration | 24 | — | `PRODUCT_CONFIGURE` | venue |
| `setPricing` | Pricing Simulation Studio | 22 | — | `PRODUCT_CONFIGURE` | venue |
| `setProductCatalogue` | Product & Catalogue Assignment | 12 | — | `PRODUCT_CONFIGURE` | venue |
| `setProductContextOwnership` | Product Context, Ownership & Assignment | 18 | — | `PRODUCT_CONFIGURE` | venue |
| `setProductServicePrice` | Product & Service Price Assignment | 20 | — | `PRODUCT_CONFIGURE` | venue |
| `setTaxProfileJurisdiction` | Tax Profile & Jurisdiction Configuration | 29 | — | `PRODUCT_CONFIGURE` | venue |
| `setTaxRuleTreatment` | Tax Rule & Treatment Builder | 22 | — | `PRODUCT_CONFIGURE` | venue |
| `simulatePriceBreakdownCalculation` | Price Breakdown, Calculation Simulation & Expl | 11 | — | `PRODUCT_CONFIGURE` | venue |

### orders (23)

| Operation | Screen | Fields | Nearest | Permission | Scope |
|---|---|---:|---|---|---|
| `setOrderDetailTransaction` | Order Detail & Transaction Workspace | 14 | `orders.cart_line` 14% | `ORDER_CREATE` | venue |
| `setGroupOperationalPlanning` | Group Operational Planning & Task Workspace | 32 | `catalogue.price_list` 3% | `ORDER_CREATE` | venue |
| `setGroupQuotationProposal` | Group Quotation Builder & Proposal Generation | 30 | `orders.cart` 3% | `ORDER_CREATE` | venue |
| `setOrderReservationStatus` | Order & Reservation Status Lifecycle Configura | 11 | — | `ORDER_CREATE` | venue |
| `approveExceptionServiceRecovery` | Approval, Exception & Service Recovery Managem | 17 | `orders.cash_movement` 6% | `ORDER_CREATE` | venue |
| `setCancellationPartialPolicy` | Cancellation & Partial Cancellation Policy Con | 18 | `catalogue.channel_allocation` 6% | `ORDER_CREATE` | venue |
| `setMultiPaymentSplit` | Multi-Payment, Split Tender & Payment Allocati | 16 | `catalogue.channel_allocation` 6% | `ORDER_CREATE` | venue |
| `approveGroupDiscountException` | Group Discount, Exception & Approval Workflow | 20 | `orders.cash_movement` 5% | `ORDER_CREATE` | venue |
| `setOrderAmendment` | Order Amendment Workspace | 22 | `catalogue.channel_capacity` 5% | `ORDER_CREATE` | venue |
| `createOrderSourceChannel` | Order Creation & Source/Channel Configuration | 35 | `catalogue.channel_allocation` 3% | `ORDER_CREATE` | venue |
| `setAmendmentEligibilityPolicy` | Amendment Eligibility & Policy Rule Builder | 33 | `catalogue.channel_allocation` 3% | `ORDER_CREATE` | venue |
| `setReservationHoldPolicy` | Reservation & Hold Policy Configuration | 29 | `catalogue.channel_allocation` 3% | `ORDER_CREATE` | venue |
| `approveListingModeration` | Listing Approval & Moderation | 12 | — | `ORDER_CREATE` | venue |
| `createListingSeller` | Listing Creation & Seller Configuration | 32 | — | `ORDER_CREATE` | venue |
| `createUpgradeCredentialRegeneration` | Upgrade Execution, Credential Regeneration & C | 27 | — | `ORDER_CREATE` | venue |
| `setAfterSaleFinancial` | After-Sales Financial Settlement & Adjustment  | 4 | — | `ORDER_CREATE` | venue |
| `setCustomerGuestAccount` | Customer, Guest & Account Assignment | 24 | — | `ORDER_CREATE` | venue |
| `setGroupBookingHandover` | Group Booking 360° & Handover Workspace | 10 | — | `ORDER_CREATE` | venue |
| `setGroupPackageExperience` | Group Package & Experience Builder | 21 | — | `ORDER_CREATE` | venue |
| `setProRataResidual` | Pro-Rata, Residual Value & Entitlement Credit  | 11 | — | `ORDER_CREATE` | venue |
| `setResaleEligibilityRule` | Resale Eligibility Rule Configuration | 32 | — | `ORDER_CREATE` | venue |
| `setResaleMarketplaceRecommendation` | AI Resale Configuration & Marketplace Recommen | 15 | — | `ORDER_CREATE` | venue |
| `setUpgradeConversionPath` | Upgrade & Conversion Path Builder | 0 | — | `ORDER_CREATE` | venue |

### marketing-crm (19)

| Operation | Screen | Fields | Nearest | Permission | Scope |
|---|---|---:|---|---|---|
| `setChannelProvider` | Channel & Provider Configuration | 26 | `control.api_client` 4% | `MARKETING_MANAGE` | venue |
| `setConsentCapturePoint` | Consent Capture Point & Customer Journey Confi | 28 | `marketing.attribution_touch` 4% | `MARKETING_MANAGE` | venue |
| `setIntelligentRoutingSkill` | Intelligent Routing, Skills & Assignment Engin | 19 | `marketing.message_trigger` 11% | `MARKETING_MANAGE` | venue |
| `createCaseClassificationIntelligent` | Case Creation, Classification & Intelligent Ro | 34 | `marketing.message_trigger` 6% | `MARKETING_MANAGE` | venue |
| `setCommunicationPreferenceMarketing` | Communication Preference & Marketing Permissio | 31 | `marketing.guest_profile` 6% | `MARKETING_MANAGE` | venue |
| `setSenderIdentityDomain` | Sender Identity, Domain & Brand Configuration | 19 | `control.api_client` 6% | `MARKETING_MANAGE` | venue |
| `approvePrivacyTesting` | Privacy Configuration Testing, Approval & Publ | 40 | `marketing.suppression` 5% | `MARKETING_MANAGE` | venue |
| `setCustomerServiceCopilot` | AI Customer Service Copilot & Knowledge Worksp | 20 | `marketing.guest_profile` 5% | `MARKETING_MANAGE` | venue |
| `setDataDiscoveryAccess` | Data Discovery, Access, Export & Correction Wo | 23 | `marketing.guest_profile` 4% | `MARKETING_MANAGE` | venue |
| `setMinorGuardianAge` | Minor, Guardian & Age-Based Privacy Configurat | 26 | `marketing.guest_profile` 4% | `MARKETING_MANAGE` | venue |
| `approveWaiverTesting` | Waiver Approval, Testing & Publication Workspa | 25 | — | `MARKETING_MANAGE` | venue |
| `setCaseInvestigationResolution` | Case Investigation & Resolution Workspace | 21 | — | `MARKETING_MANAGE` | venue |
| `setDigitalWaiverForm` | Digital Waiver & Form Builder | 27 | — | `MARKETING_MANAGE` | venue |
| `setLocalizationBrandingCustomer` | Localization, Branding & Customer Experience C | 24 | — | `MARKETING_MANAGE` | venue |
| `setOrderBookingTicket` | Order, Booking & Ticket Service Workspace | 8 | — | `MARKETING_MANAGE` | venue |
| `setPrivacyComplianceException` | Privacy Compliance, Exception & Investigation  | 18 | — | `MARKETING_MANAGE` | venue |
| `setRefundCompensationService` | Refund, Compensation & Service Exception Works | 13 | — | `MARKETING_MANAGE` | venue |
| `setSignatorySignatureGuardian` | Signatory, Signature & Guardian Rule Configura | 30 | — | `MARKETING_MANAGE` | venue |
| `setWaiverVerificationValidation` | Waiver Verification & Validation Workspace | 11 | — | `MARKETING_MANAGE` | venue |

### promotions (17)

| Operation | Screen | Fields | Nearest | Permission | Scope |
|---|---|---:|---|---|---|
| `setGuestChoiceBuild` | Guest Choice & Build-Your-Own Bundle Designer | 19 | — | `PRICE_CONFIGURE` | venue |
| `setBuyGetBogo` | Buy X Get Y / BOGO Rule Builder | 15 | `promotions.bundle_component` 7% | `PRICE_CONFIGURE` | venue |
| `setGiftFreeProduct` | Gift, Free Product & Added-Value Offer Builder | 15 | `promotions.bundle_component` 7% | `PRICE_CONFIGURE` | venue |
| `approveCampaignWorkflow` | Campaign Approval Workflow Designer | 18 | `promotions.coupon_campaign` 6% | `PRICE_CONFIGURE` | venue |
| `setBundleDefinition` | Bundle Definition & Setup | 19 | `promotions.allocation_split` 5% | `PRICE_CONFIGURE` | venue |
| `setPromotionRule` | Promotion Rule Builder | 21 | `promotions.upsell_rule` 5% | `PRICE_CONFIGURE` | venue |
| `setRuleTestRecommendation` | Rule Test, Simulation & AI Recommendation Work | 35 | `promotions.bundle_component` 3% | `PRICE_CONFIGURE` | venue |
| `simulateBundlePreviewRecommendation` | Bundle Preview, Simulation & AI Recommendation | 35 | `promotions.bundle_component` 3% | `PRICE_CONFIGURE` | venue |
| `approveDecision` | Approval Inbox & Decision Workspace | 4 | — | `PRICE_CONFIGURE` | venue |
| `setBundleComponent` | Bundle Component Builder | 26 | — | `PRICE_CONFIGURE` | venue |
| `setCampaignBudgetFinancial` | Campaign Budget & Financial Limit Setup | 24 | — | `PRICE_CONFIGURE` | venue |
| `setCodeDistributionManager` | Code Distribution & Assignment Manager | 18 | — | `PRICE_CONFIGURE` | venue |
| `setCouponPromoCode` | Coupon & Promo Code Builder | 20 | — | `PRICE_CONFIGURE` | venue |
| `setCrossCategoryPromotion` | Cross-Category Promotion Builder | 10 | — | `PRICE_CONFIGURE` | venue |
| `setEligibilityRule` | Eligibility Rule Builder | 21 | — | `PRICE_CONFIGURE` | venue |
| `setFixedPriceOffer` | Fixed-Price & “N for X” Offer Builder | 14 | — | `PRICE_CONFIGURE` | venue |
| `setPromotionStackingRule` | Promotion Stacking Rule Builder | 11 | — | `PRICE_CONFIGURE` | venue |

### subscription (15)

| Operation | Screen | Fields | Nearest | Permission | Scope |
|---|---|---:|---|---|---|
| `setPartnerRateNet` | Partner Rate & Net Pricing Configuration | 20 | `control.api_licence` 10% | `PLATFORM_CELL_MANAGE` | tenant |
| `setMembershipProductTier` | Membership Product & Tier Builder | 28 | `control.api_licence` 7% | `PLATFORM_CELL_MANAGE` | tenant |
| `setAgreementContractTerm` | Agreement & Contract Terms Builder | 36 | `control.api_licence` 6% | `PLATFORM_CELL_MANAGE` | tenant |
| `approveBookingLimitCommercial` | Booking Limits, Commercial Exceptions & Approv | 25 | `control.tenant_migration` 4% | `PLATFORM_CELL_MANAGE` | tenant |
| `setMembershipEntitlementAdmission` | Membership Entitlement & Admission Benefit Bui | 35 | `control.webhook_delivery` 3% | `PLATFORM_CELL_MANAGE` | tenant |
| `setPartnerProfileOrganization` | Partner Profile & Organization Setup | 29 | `control.developer_account` 3% | `PLATFORM_CELL_MANAGE` | tenant |
| `approveMembershipProductValidation` | Membership Product Validation, Approval, Publi | 31 | — | `PLATFORM_CELL_MANAGE` | tenant |
| `approvePartnerStatuLifecycle` | Partner Approval, Status & Lifecycle Managemen | 28 | — | `PLATFORM_CELL_MANAGE` | tenant |
| `setFamilyHouseholdDependent` | Family, Household & Dependent Membership Confi | 28 | — | `PLATFORM_CELL_MANAGE` | tenant |
| `setMemberMembershipAccount` | Member 360° Membership Account Workspace | 7 | — | `PLATFORM_CELL_MANAGE` | tenant |
| `setMembershipEligibilityQualification` | Membership Eligibility & Qualification Rule Bu | 28 | — | `PLATFORM_CELL_MANAGE` | tenant |
| `setPartnerBrandVenue` | Partner Brand, Venue & Business Scope Assignme | 16 | — | `PLATFORM_CELL_MANAGE` | tenant |
| `setPaymentTermBilling` | Payment Terms, Billing & Account Configuration | 22 | — | `PLATFORM_CELL_MANAGE` | tenant |
| `setRenewalAutoMembership` | Renewal, Auto-Renewal & Membership Continuity  | 25 | — | `PLATFORM_CELL_MANAGE` | tenant |
| `setValidityActivationExpiry` | Validity, Activation & Expiry Configuration | 7 | — | `PLATFORM_CELL_MANAGE` | tenant |

### approvals (9)

| Operation | Screen | Fields | Nearest | Permission | Scope |
|---|---|---:|---|---|---|
| `approveRoleAuthorityDelegation` | Roles, Authority, Delegation & Approval Limits | 24 | `approvals.decision` 4% | `APPROVAL_REQUEST` | venue |
| `setVisualWorkflow` | Visual Workflow Designer | 25 | `approvals.decision` 4% | `APPROVAL_REQUEST` | venue |
| `approveMatrixMultiLevel` | Approval Matrix & Multi-Level Approval Configu | 30 | `approvals.request` 3% | `APPROVAL_REQUEST` | venue |
| `approveUnifiedDecision` | Unified Approval Inbox & Decision Workspace | 6 | — | `APPROVAL_REQUEST` | venue |
| `approveVersioningGovernance` | Versioning, Governance, Approval & Publication | 31 | — | `APPROVAL_REQUEST` | venue |
| `createAutomationAutonomouAction` | Automation Execution & Autonomous Action Monit | 8 | — | `APPROVAL_REQUEST` | venue |
| `setTriggerActionCross` | Trigger, Action & Cross-Module Orchestration C | 18 | — | `APPROVAL_REQUEST` | venue |
| `setVisualBusinessRule` | Visual Business Rule Builder | 9 | — | `APPROVAL_REQUEST` | venue |
| `simulateWorkflowTestingImpact` | Workflow Testing, Simulation & Impact Analysis | 9 | — | `APPROVAL_REQUEST` | venue |

