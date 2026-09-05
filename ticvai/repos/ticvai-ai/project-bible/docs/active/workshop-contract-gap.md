# Workshop pack — the contract gap, as named operations

**Derived by `tools/derive-pack-linkage.py`. Regenerate rather than editing.**

| | |
|---|---:|
| Pack screens | 590 |
| Wired to an operation that exists | **13** |
| Candidate match below the threshold | 27 |
| No operation exists | **550** |
| Distinct operations to author | **613** |

## How these were derived

A screen's operations follow from **what entity it acts on and what it does to it**, and this pack titles every screen after both — `Access Point Directory` is a list of access points, `Offline Validation Policy Builder` sets an offline policy. Matched against operation names that is precise: `listAccessPoints`, `setOfflinePolicy`, `enrolFacePass`, `listQueues`, `setBrandIdentity` all came out of it.

**Two weaker signals were tried first and both failed the same way** — the terms they agree on are the generic ones. Bag-of-words over summaries and tables put eight unrelated screens on `listScans` at 0.75. Joining the field lists through the schema resolved only 9% of 4,756 field terms, and the ones that resolved were `status`, `owner` and `channel`, so `Pricing Rule Command Center` came back pointing at `pii.subject`.

**A proposed name is a specification, not a decision.** The verb comes from the archetype and the entity from the title; the shape of the request and response does not follow from either, and neither does the permission, the scope level or the audience. Those are the parts a person writes.

## Access Control Module — board 1

9 screens · 9 operations to author

| Screen | Operation to author |
|---|---|
| Access Control Command Center | `listAccess` |
| Venue & Park Access Structure | `listVenueParkAccess` |
| Access Area & Zone Builder | `setAccessAreaZone` |
| Attraction Access Configuration | `setAttractionAccess` |
| Gate & Lane Configuration | `setGateLane` |
| Access Control Graphical Map Designer | `setAccessGraphicalMap` |
| Access Location Grouping | `listAccessLocationGrouping` |
| Operating Calendar & Special Access Days | `listOperatingCalendarSpecial` |
| Topology Validation & Publication | `publishTopologyValidation` |

## Access Control Module — board 10

9 screens · 9 operations to author

| Screen | Operation to author |
|---|---|
| Dynamic Access Policy Command Center | `listDynamicAccessPolicy` |
| Access Attribute Catalog | `listAccessAttributeCatalog` |
| Visual Dynamic Policy Builder | `setVisualDynamicPolicy` |
| Context, Time, Event & Capacity Policy Builder | `setContextTimeEvent` |
| Identity, Membership & Accreditation Policies | `listIdentityMembershipAccreditation` |
| Policy Scope, Hierarchy & Inheritance | `listPolicyScopeHierarchy` |
| Authorization Governance & Temporary Access | `listAuthorizationGovernanceTemporary` |
| Policy Evaluation Architecture & Offline Distribution | `listPolicyEvaluationArchitecture` |
| Policy Simulation, Conflict & Impact Analysis | `simulatePolicyConflictImpact` |

## Access Control Module — board 11

10 screens · 10 operations to author

| Screen | Operation to author |
|---|---|
| Access Security & Fraud Command Center | `listAccessSecurityFraud` |
| Fraud Detection Rule & Signal Library | `listFraudDetectionRule` |
| Credential Sharing & Concurrent Usage Detection | `listCredentialSharingConcurrent` |
| Unified Identity & Credential Lock Manager | `listUnifiedIdentityCredential` |
| Biometric & Identity Integrity Monitoring | `listBiometricIdentityIntegrity` |
| Relationship & Companion Fraud Monitoring | `listRelationshipCompanionFraud` |
| Access Risk Scoring & Decision Engine | `listAccessRiskScoring` |
| Real-Time Security Response & Playbook Builder | `setRealTimeSecurity` |
| Security Investigation & Evidence Workspace | `setSecurityInvestigationEvidence` |
| Security Analytics, AI Detection & Governance | `listSecurityDetectionGovernance` |

## Access Control Module — board 12

10 screens · 10 operations to author

| Screen | Operation to author |
|---|---|
| Access Monitoring & Analytics Command Center | `listAccessMonitoring` |
| Live Venue Occupancy & People Counting | `listLiveVenueOccupancy` |
| Graphical Access Map & Live Gate Performance | `listGraphicalAccessMap` |
| Attendance & Admission Analytics | `listAttendanceAdmission` |
| Entry, Exit, Re-entry & Crossover Analytics | `listEntryExitCrossover` |
| Throughput, Queue & Validation Performance Analytics | `listThroughputQueueValidation` |
| Validation Outcome & Rejection Analytics | `listValidationOutcomeRejection` |
| Guest Dwell Time, Length of Stay & Attraction Flow | `listGuestDwellTime` |
| Access Reports, Scheduled Reporting & Data Export | `listAccessReportScheduled` |
| AI Access Intelligence, Forecasting & Executive Insights | `listAccessExecutiveInsight` |

## Access Control Module — board 2

11 screens · 11 operations to author

| Screen | Operation to author |
|---|---|
| Access Rule Command Center | `listAccessRule` |
| Visual Access Rule Builder | `setVisualAccessRule` |
| Entry, Exit & Re-entry Rules | `listEntryExitRule` |
| Anti-Passback & Journey Sequence | `listAntiPassbackJourney` |
| Access Validity & Time Rules | `listAccessValidityTime` |
| Entitlement Consumption Engine | `listEntitlementConsumption` |
| Multi-Park & Crossover Rules | `listMultiParkCrossover` |
| Guest, Companion & Eligibility Rules | `listGuestCompanionEligibility` |
| Group Admission & Quantity Validation | `listGroupAdmissionQuantity` |
| Rule Simulation, Conflict Check & Publication | `publishRuleConflictCheck` |
| Rule Simulation, Conflict Check & Publication | `simulateRuleConflictCheck` |

## Access Control Module — board 3

12 screens · 12 operations to author

| Screen | Operation to author |
|---|---|
| Digital Credential Security Command Center | `listDigitalCredentialSecurity` |
| Dynamic QR Security Profile Builder | `setDynamicSecurityProfile` |
| Credential Activation & Display Rules | `listCredentialActivationDisplay` |
| Device Binding & Session Security | `listDeviceBindingSession` |
| BLE Beacon & Geofence Configuration | `setBleBeaconGeofence` |
| Credential Transfer & Rebinding | `listCredentialTransferRebinding` |
| Credential Revocation & Lifecycle Events | `listCredentialRevocationLifecycle` |
| Offline Cryptographic Validation Profile | `listOfflineCryptographicValidation` |
| Embedded Entitlement Payload Designer | `setEmbeddedEntitlementPayload` |
| Credential Security Simulation, Audit & Publication | `listCredentialSecurity` |
| Credential Security Simulation, Audit & Publication | `publishCredentialSecurity` |
| Credential Security Simulation, Audit & Publication | `simulateCredentialSecurity` |

## Access Control Module — board 4

10 screens · 10 operations to author

| Screen | Operation to author |
|---|---|
| Media & Credential Command Center | `listMediaCredential` |
| Media Type & Technology Library | `listMediaTypeTechnology` |
| Virtual Credential & Media Association | `listVirtualCredentialMedia` |
| Verification Method Selection & Locking | `listVerificationMethodSelection` |
| Media Issuance & Encoding Profile | `listMediaIssuanceEncoding` |
| Media Swap & Replacement | `listMediaSwapReplacement` |
| RFID & NFC Configuration | `setRfidNfc` |
| External & Partner Credential Mapping | `listExternalPartnerCredential` |
| Hotel, Wallet & External Media Integration | `listHotelWalletExternal` |
| Media Compatibility, Testing & Publication | `publishMediaCompatibilityTesting` |

## Access Control Module — board 5

12 screens · 12 operations to author

| Screen | Operation to author |
|---|---|
| Biometric Access Command Center | `listBiometricAccess` |
| Biometric Verification Profile Builder | `setBiometricVerificationProfile` |
| Face Pass Enrollment Configuration | `setFacePassEnrollment` |
| Biometric Consent & Guardian Management | `listBiometricConsentGuardian` |
| Face Tag Temporary Enrollment | `listFaceTagTemporary` |
| Face Matching & Verification Thresholds | `listFaceMatchingVerification` |
| Face Change, Re-enrollment & Identity Protection | `listFaceChangeEnrollment` |
| Biometric Validation at Gate | `listBiometricValidationGate` |
| Biometric Lifecycle, Retention & Deletion | `listBiometricLifecycleRetention` |
| Biometric Simulation, Audit & Publication | `listBiometric` |
| Biometric Simulation, Audit & Publication | `publishBiometric` |
| Biometric Simulation, Audit & Publication | `simulateBiometric` |

## Access Control Module — board 6

10 screens · 10 operations to author

| Screen | Operation to author |
|---|---|
| Device & Gate Command Center | `listDeviceGate` |
| Device Type & Hardware Library | `listDeviceTypeHardware` |
| Physical Device Registration & Provisioning | `listPhysicalDeviceRegistration` |
| Turnstile & Lane Behavior Configuration | `setTurnstileLaneBehavior` |
| Validation Outcome & Guest Feedback Designer | `setValidationOutcomeGuest` |
| Reader, Scanner & Peripheral Configuration | `setReaderScannerPeripheral` |
| Handheld & Mobile Access Device Configuration | `setHandheldMobileAccess` |
| Gate Modes, Free Spin & Emergency Controls | `listGateModeFree` |
| Device Software, Content & Remote Configuration | `setDeviceSoftwareContent` |
| Hardware Compatibility, Health, Testing & Deployment | `listHardwareCompatibilityHealth` |

## Access Control Module — board 7

9 screens · 9 operations to author

| Screen | Operation to author |
|---|---|
| Offline & Edge Operations Command Center | `listOfflineEdge` |
| Edge Node & Local Processing Configuration | `setEdgeNodeLocal` |
| Edge Package & Data Distribution | `listEdgePackageData` |
| Offline Credential & Revocation Cache | `listOfflineCredentialRevocation` |
| Offline Entitlement & Usage Ledger | `listOfflineEntitlementUsage` |
| Connectivity Failure & Degraded Mode Policy | `listConnectivityFailureDegraded` |
| Reconnection, Synchronization & Conflict Resolution | `listReconnectionSynchronizationConflict` |
| Offline Simulation & Resilience Testing | `simulateOfflineResilienceTesting` |
| Edge Security, Audit & Deployment | `listEdgeSecurityDeployment` |

## Access Control Module — board 8

9 screens · 9 operations to author

| Screen | Operation to author |
|---|---|
| Guest Journey Command Center | `listGuestJourney` |
| Group & B2B Admission Profile Builder | `setGroupAdmissionProfile` |
| Group Leader & Fast B2B Validation | `listGroupLeaderFast` |
| Group Attendance & Partial Entry Manager | `listGroupAttendancePartial` |
| Family, Child, POD & Companion Journey | `listFamilyChildPod` |
| Re-entry & Temporary Exit Journey | `listEntryTemporaryExit` |
| Multi-Park & Crossover Journey Orchestrator | `listMultiParkCrossover` |
| Fast Pass & Attraction Access Journey | `listFastPassAttraction` |
| Special Event, Free View & Alternative Admission | `listSpecialEventFree` |

## Access Control Module — board 9

10 screens · 10 operations to author

| Screen | Operation to author |
|---|---|
| Live Access Operations Command Center | `listLiveAccess` |
| Podium Operations Console | `listPodiumConsole` |
| Ticket & Credential Investigation Console | `listTicketCredentialInvestigation` |
| Validation Exception & Reason Code Manager | `listValidationExceptionReason` |
| Manual Override & Supervisor Approval | `approveManualOverrideSupervisor` |
| Credential Disable, Blacklist & Whitelist Operations | `listCredentialDisableBlacklist` |
| Live Gate Mode & Lane Control | `listLiveGateMode` |
| Queue, Throughput & Lane Optimization | `listQueueThroughputLane` |
| Operational Incident & Exception Workspace | `setOperationalIncidentException` |
| Operations Audit, Shift Handover & Control Summary | `listShiftHandoverSummary` |

## B2B, Reseller & OTA Partner Management — board 1

11 screens · 11 operations to author

| Screen | Operation to author |
|---|---|
| Partner Management Command Center | `listPartner` |
| Partner Profile & Organization Setup | `setPartnerProfileOrganization` |
| Partner Onboarding & Application Workflow | `listPartnerOnboardingApplication` |
| Partner Contacts & User Administration | `listPartnerContactUser` |
| Territory, Market & Distribution Rights | `listTerritoryMarketDistribution` |
| Partner Brand, Venue & Business Scope Assignment | `setPartnerBrandVenue` |
| Partner Documentation & Compliance Repository | `listPartnerDocumentationCompliance` |
| Partner Access, Roles & Permission Profile | `listPartnerAccessRole` |
| Partner Approval, Status & Lifecycle Management | `approvePartnerStatuLifecycle` |
| Partner Approval, Status & Lifecycle Management | `listPartnerStatuLifecycle` |
| Partner 360° Profile, Readiness & AI Review | `listPartnerProfileReadiness` |

## B2B, Reseller & OTA Partner Management — board 2

10 screens · 10 operations to author

| Screen | Operation to author |
|---|---|
| Commercial Agreement Command Center | `listCommercialAgreement` |
| Agreement & Contract Terms Builder | `setAgreementContractTerm` |
| Partner Rate & Net Pricing Configuration | `setPartnerRateNet` |
| Commission, Margin & Incentive Management | `listCommissionMarginIncentive` |
| Credit Limit & Exposure Management | `listCreditLimitExposure` |
| Deposit, Guarantee & Financial Security Management | `listDepositGuaranteeFinancial` |
| Payment Terms, Billing & Account Configuration | `setPaymentTermBilling` |
| Commercial Allocation, Quota & Commitment Management | `listCommercialAllocationQuota` |
| Booking Limits, Commercial Exceptions & Approval | `approveBookingLimitCommercial` |
| Commercial Agreement 360°, Health & AI Review | `listCommercialAgreementHealth` |

## B2B, Reseller & OTA Partner Management — board 3

10 screens · 10 operations to author

| Screen | Operation to author |
|---|---|
| Partner Operations Command Center | `listPartner` |
| Partner Orders & Booking Management | `listPartnerOrderBooking` |
| Reservations, Holds & Release Management | `listReservationHoldRelease` |
| Partner Cancellations, Refunds & Amendments | `listPartnerCancellationRefund` |
| Partner Statement & Account Activity | `listPartnerStatementAccount` |
| Partner Reconciliation & Exception Management | `listPartnerReconciliationException` |
| Commission Calculation & Settlement Management | `listCommissionCalculationSettlement` |
| Partner Disputes, Cases & Service Management | `listPartnerDisputeCase` |
| Partner Performance Scorecard & Risk Monitoring | `listPartnerPerformanceScorecard` |
| Partner AI Intelligence & Relationship Optimization | `listPartnerRelationship` |

## Communication & Notification Platform Services — board 1

10 screens · 10 operations to author

| Screen | Operation to author |
|---|---|
| Communication Service Command Center | `listCommunicationService` |
| Channel & Provider Configuration | `setChannelProvider` |
| Sender Identity, Domain & Brand Configuration | `setSenderIdentityDomain` |
| System Transactional Template Registry | `listSystemTransactionalTemplate` |
| Business Event & Notification Trigger Mapping | `listBusinessEventNotification` |
| Routing, Priority, Throttling & Fallback Rules | `listRoutingPriorityThrottling` |
| Consent, Preference & Communication Policy Enforcement | `listConsentPreferenceCommunication` |
| Delivery Queue, Failure & Retry Management | `listDeliveryQueueFailure` |
| Provider Health, Usage & Cost Monitoring | `listProviderHealthUsage` |
| AI Delivery Optimization & Communication Platform Diagnostics | `listDeliveryCommunicationPlatform` |

## Customer Service — board 1

10 screens · 10 operations to author

| Screen | Operation to author |
|---|---|
| Customer Service Command Center | `listCustomerService` |
| Customer 360° Service Profile | `listCustomerServiceProfile` |
| Unified Interaction & Communication History | `listUnifiedInteractionCommunication` |
| Case Creation, Classification & Intelligent Routing | `createCaseClassificationIntelligent` |
| Case Investigation & Resolution Workspace | `setCaseInvestigationResolution` |
| Order, Booking & Ticket Service Workspace | `setOrderBookingTicket` |
| Refund, Compensation & Service Exception Workspace | `setRefundCompensationService` |
| Escalation, Collaboration & Internal Resolution | `listEscalationCollaborationInternal` |
| Case Resolution, Closure & Customer Feedback | `listCaseResolutionClosure` |
| AI Customer Service Copilot & Knowledge Workspace | `setCustomerServiceCopilot` |

## Customer Service — board 2

10 screens · 10 operations to author

| Screen | Operation to author |
|---|---|
| Contact Center Operations Command Center | `listContact` |
| Intelligent Routing, Skills & Assignment Engine | `setIntelligentRoutingSkill` |
| SLA Policy & Service-Level Management | `listSlaPolicyService` |
| Agent Workload, Availability & Workforce Control | `listAgentWorkloadAvailability` |
| Escalation & Critical Case Monitor | `listEscalationCriticalCase` |
| Quality Management & Agent Evaluation | `listQualityAgentEvaluation` |
| Customer Satisfaction, Feedback & Voice of Customer | `listCustomerSatisfactionFeedback` |
| Service Analytics & Root-Cause Intelligence | `listServiceRootCause` |
| AI Contact Center Intelligence & Automation Studio | `listContactAutomation` |
| AI Contact Center Intelligence & Automation Studio | `setContactAutomation` |

## Group Sales   Corporate Booking Management — board 1

10 screens · 10 operations to author

| Screen | Operation to author |
|---|---|
| Group Sales Command Center | `listGroupSale` |
| Group Enquiry & Opportunity Capture | `listGroupEnquiryOpportunity` |
| Group Customer & Organization Profile | `listGroupCustomerOrganization` |
| Group Requirements, Availability & Capacity Planner | `listGroupRequirementAvailability` |
| Group Package & Experience Builder | `setGroupPackageExperience` |
| Group Quotation Builder & Proposal Generation | `setGroupQuotationProposal` |
| Quote Revision, Negotiation & Version Management | `listQuoteRevisionNegotiation` |
| Group Discount, Exception & Approval Workflow | `approveGroupDiscountException` |
| Quote-to-Booking Conversion & Confirmation | `listQuoteBookingConversion` |
| Group Booking 360° & Handover Workspace | `setGroupBookingHandover` |

## Group Sales   Corporate Booking Management — board 2

10 screens · 10 operations to author

| Screen | Operation to author |
|---|---|
| Group Booking Operations Command Center | `listGroupBooking` |
| Group Operational Planning & Task Workspace | `setGroupOperationalPlanning` |
| Participants, Guest Lists & Group Structure | `listParticipantGuestList` |
| Group Payment, Deposit & Balance Management | `listGroupPaymentDeposit` |
| Group Ticket, Seat & Entitlement Allocation | `listGroupTicketSeat` |
| Group Ticket Fulfillment & Distribution | `listGroupTicketFulfillment` |
| Group Arrival, Check-In & Admission Operations | `listGroupArrivalCheck` |
| Group Amendments, Cancellation & Refund Operations | `listGroupAmendmentCancellation` |
| Group Booking Reconciliation, Closure & Performance | `listGroupBookingReconciliation` |
| Group Sales Analytics & AI Intelligence Center | `listGroupSale` |

## Membership   Annual Pass Management — board 1

11 screens · 11 operations to author

| Screen | Operation to author |
|---|---|
| Membership & Annual Pass Command Center | `listMembershipAnnualPass` |
| Membership Product & Tier Builder | `setMembershipProductTier` |
| Membership Eligibility & Qualification Rule Builder | `setMembershipEligibilityQualification` |
| Validity, Activation & Expiry Configuration | `setValidityActivationExpiry` |
| Membership Entitlement & Admission Benefit Builder | `setMembershipEntitlementAdmission` |
| Membership Usage, Visit & Consumption Rules | `listMembershipUsageVisit` |
| Family, Household & Dependent Membership Configuration | `setFamilyHouseholdDependent` |
| Membership Commercial, Pricing & Channel Association | `listMembershipCommercialPricing` |
| Renewal, Auto-Renewal & Membership Continuity Configuration | `setRenewalAutoMembership` |
| Membership Product Validation, Approval, Publication & Versioning | `approveMembershipProductValidation` |
| Membership Product Validation, Approval, Publication & Versioning | `publishMembershipProductValidation` |

## Membership   Annual Pass Management — board 2

11 screens · 11 operations to author

| Screen | Operation to author |
|---|---|
| Member Operations Command Center | `listMember` |
| Member 360° Membership Account Workspace | `setMemberMembershipAccount` |
| Membership Activation, Assignment & Credential Management | `listMembershipActivationCredential` |
| Membership Activation, Assignment & Credential Management | `setMembershipActivationCredential` |
| Visit, Admission & Entitlement Usage Monitor | `listVisitAdmissionEntitlement` |
| Membership Freeze, Suspension & Reactivation Management | `listMembershipFreezeSuspension` |
| Membership Upgrade, Downgrade & Product Migration Operations | `listMembershipUpgradeDowngrade` |
| Renewal Operations & Auto-Renewal Management | `listRenewalAuto` |
| Member Exceptions, Overrides & Service Recovery | `listMemberExceptionOverride` |
| Member Lifecycle History, Audit & Case Timeline | `listMemberLifecycleCase` |
| Membership Analytics, Renewal Intelligence & AI Retention Center | `listMembershipRenewalRetention` |

## Order   Reservation Management — board 1

11 screens · 11 operations to author

| Screen | Operation to author |
|---|---|
| Order & Reservation Command Center | `listOrderReservation` |
| Order Detail & Transaction Workspace | `setOrderDetailTransaction` |
| Reservation & Hold Policy Configuration | `setReservationHoldPolicy` |
| Order & Reservation Status Lifecycle Configuration | `setOrderReservationStatu` |
| Order Creation & Source/Channel Configuration | `createOrderSourceChannel` |
| Order Creation & Source/Channel Configuration | `setOrderSourceChannel` |
| Customer, Guest & Account Assignment | `setCustomerGuestAccount` |
| Order Line, Product & Entitlement Composition | `listOrderLineProduct` |
| Capacity Reservation & Inventory Commitment | `listCapacityReservationInventory` |
| Reservation Confirmation, Expiry & Fulfillment Readiness | `listReservationConfirmationExpiry` |
| Order Lifecycle Timeline, SLA, Exceptions & AI Operations | `listOrderLifecycleTimeline` |

## Order   Reservation Management — board 2

10 screens · 9 operations to author

| Screen | Operation to author |
|---|---|
| Amendment & After-Sales Command Center | `listAmendmentAfterSale` |
| Order Amendment Workspace | `setOrderAmendment` |
| Amendment Eligibility & Policy Rule Builder | `setAmendmentEligibilityPolicy` |
| Cancellation & Partial Cancellation Policy Configuration | `setCancellationPartialPolicy` |
| Void, Reversal & Same-Day Correction Management | `listVoidReversalSame` |
| Ticket Reissue & Fulfillment Regeneration | `listTicketReissueFulfillment` |
| After-Sales Financial Settlement & Adjustment Workspace | `setAfterSaleFinancial` |
| Approval, Exception & Service Recovery Management | `approveExceptionServiceRecovery` |
| Approval, Exception & Service Recovery Management | `listExceptionServiceRecovery` |
| Amendment History, Audit & After-Sales Analytics | `listAmendmentAfterSale` |

## Order   Reservation Management — board 3

10 screens · 10 operations to author

| Screen | Operation to author |
|---|---|
| Payment & Order Financial Command Center | `listPaymentOrderFinancial` |
| Order Payment Detail & Transaction Ledger | `listOrderPaymentDetail` |
| Multi-Payment, Split Tender & Payment Allocation Configuration | `setMultiPaymentSplit` |
| Deposit, Partial Payment & Outstanding Balance Management | `listDepositPartialPayment` |
| Order Split, Merge & Transaction Relationship Management | `listOrderSplitMerge` |
| Related Order & Transaction Relationship Explorer | `listRelatedOrderTransaction` |
| External Payment, Partner & Settlement Reference Mapping | `listExternalPaymentPartner` |
| Payment Reconciliation & Exception Management | `listPaymentReconciliationException` |
| Financial Traceability, Control & Audit Explorer | `listFinancialTraceability` |
| Order Financial Analytics & AI Reconciliation Intelligence | `listOrderFinancialReconciliation` |

## Pricing   Revenue Management — board 1

10 screens · 10 operations to author

| Screen | Operation to author |
|---|---|
| Commercial Pricing Command Center | `listCommercialPricing` |
| Price List Master Configuration | `setPriceListMaster` |
| Price Category & Rate Type Library | `listPriceCategoryRate` |
| Rate Structure Builder | `setRateStructure` |
| Product & Service Price Assignment | `setProductServicePrice` |
| Package, Bundle & Add-On Pricing | `listPackageBundleAdd` |
| Market, Venue & Currency Pricing Structure | `listMarketVenueCurrency` |
| Price Hierarchy & Inheritance Configuration | `setPriceHierarchyInheritance` |
| Price List Templates, Clone & Reuse | `listPriceListTemplate` |
| Commercial Pricing Structure Validation | `listCommercialPricingStructure` |

## Pricing   Revenue Management — board 2

10 screens · 10 operations to author

| Screen | Operation to author |
|---|---|
| Pricing Rule Command Center | `listPricingRule` |
| Customer Segment & Profile Pricing Rules | `listCustomerSegmentProfile` |
| Membership & Loyalty Pricing Rules | `listMembershipLoyaltyPricing` |
| Residency, Nationality & Market Pricing Rules | `listResidencyNationalityMarket` |
| Channel-Based Pricing Rules | `listChannelBasedPricing` |
| Location, Venue & Event Pricing Rules | `listLocationVenueEvent` |
| Quantity, Group & Volume Pricing Rules | `listQuantityGroupVolume` |
| Effective Date, Season & Day-Based Pricing Rules | `listEffectiveDateSeason` |
| Timeslot, Performance & Time-of-Day Pricing Rules | `listTimeslotPerformanceTime` |
| Pricing Rule Priority, Conflict Resolution & Testing | `listPricingRulePriority` |

## Pricing   Revenue Management — board 3

10 screens · 10 operations to author

| Screen | Operation to author |
|---|---|
| Tax, Fee & Calculation Command Center | `listTaxFeeCalculation` |
| Tax Profile & Jurisdiction Configuration | `setTaxProfileJurisdiction` |
| Tax Rule & Treatment Builder | `setTaxRuleTreatment` |
| Fee & Surcharge Library | `listFeeSurcharge` |
| Fee Applicability & Charging Rule Builder | `setFeeApplicabilityCharging` |
| Fee Waiver, Tax Exemption & Exception Rules | `listFeeWaiverTax` |
| Price Calculation Sequence & Formula Engine | `listPriceCalculationSequence` |
| Currency Precision, Rounding & Monetary Rules | `listCurrencyPrecisionRounding` |
| Price Breakdown, Calculation Simulation & Explainability | `simulatePriceBreakdownCalculation` |
| Calculation Validation, Reconciliation & Service Interface | `listCalculationValidationReconciliation` |

## Pricing   Revenue Management — board 4

11 screens · 11 operations to author

| Screen | Operation to author |
|---|---|
| Pricing Governance Command Center | `listPricingGovernance` |
| Pricing Change Request & Workspace | `setPricingChangeRequest` |
| Bulk Pricing Update, Import & Mass Maintenance | `listBulkPricingUpdate` |
| Pricing Version & Baseline Management | `listPricingVersionBaseline` |
| Pricing Change Impact Analysis | `listPricingChangeImpact` |
| Pricing Approval Workflow & Authority Matrix | `approvePricingWorkflowAuthority` |
| Pricing Publication & Effective-Date Scheduler | `publishPricingEffectiveDate` |
| Pricing Distribution, Synchronization & Publication Monitor | `listPricingDistributionSynchronization` |
| Pricing Distribution, Synchronization & Publication Monitor | `publishPricingDistributionSynchronization` |
| Pricing Rollback & Emergency Control Center | `listPricingRollbackEmergency` |
| Pricing History, Audit & Compliance Explorer | `listPricingCompliance` |

## Pricing   Revenue Management — board 5

10 screens · 10 operations to author

| Screen | Operation to author |
|---|---|
| Dynamic Pricing Strategy Command Center | `listDynamicPricingStrategy` |
| Dynamic Pricing Strategy Builder | `setDynamicPricingStrategy` |
| Demand, Occupancy & Availability Rule Builder | `setDemandOccupancyAvailability` |
| Booking Velocity & Time-to-Event Rule Builder | `setBookingVelocityTime` |
| Seasonal, Calendar, Day & Timeslot Dynamic Rules | `listSeasonalCalendarDay` |
| Channel, Customer Segment & Location Dynamic Rules | `listChannelCustomerSegment` |
| Dynamic Price Bands, Ladders & Adjustment Matrix | `listDynamicPriceBand` |
| Dynamic Pricing Guardrails & Commercial Protection | `listDynamicPricingGuardrail` |
| Dynamic Pricing Automation Policy & Control | `listDynamicPricingAutomation` |
| Rule Priority, Conflict Resolution & Dynamic Pricing Test Console | `listRulePriorityConflict` |

## Pricing   Revenue Management — board 6

12 screens · 12 operations to author

| Screen | Operation to author |
|---|---|
| AI Pricing Intelligence Command Center | `listPricing` |
| Internal Demand & Booking Signal Hub | `listInternalDemandBooking` |
| Weather Intelligence & Demand Impact Configuration | `listWeatherDemandImpact` |
| Weather Intelligence & Demand Impact Configuration | `setWeatherDemandImpact` |
| Nearby Event, Exhibition & Local Demand Intelligence | `listNearbyEventExhibition` |
| Competitor Pricing & Market Position Intelligence | `listCompetitorPricingMarket` |
| Market, Tourism, Holiday & Contextual Signal Hub | `listMarketTourismHoliday` |
| AI Demand Forecasting & Booking Curve Studio | `listDemandBookingCurve` |
| AI Demand Forecasting & Booking Curve Studio | `setDemandBookingCurve` |
| Price Elasticity & Revenue Response Intelligence | `listPriceElasticityRevenue` |
| AI Pricing Recommendation & Explainability Center | `listPricingRecommendationExplainability` |
| AI Signal Registry, Data Quality & Model Governance | `listSignalDataQuality` |

## Pricing   Revenue Management — board 7

12 screens · 12 operations to author

| Screen | Operation to author |
|---|---|
| Revenue Optimization Command Center | `listRevenue` |
| Pricing Simulation Studio | `setPricing` |
| Pricing Simulation Studio | `simulatePricing` |
| Scenario Modeling & What-If Analysis | `listScenarioModelingWhat` |
| A/B Pricing Experiment Studio | `setPricingExperiment` |
| Revenue & Demand Impact Forecasting | `listRevenueDemandImpact` |
| AI Recommendation Review & Decision Queue | `listRecommendationReviewDecision` |
| Automation Policy & Autonomous Pricing Orchestrator | `listAutomationPolicyAutonomou` |
| Live Dynamic Price Execution & Deployment Monitor | `createLiveDynamicPrice` |
| Live Dynamic Price Execution & Deployment Monitor | `listLiveDynamicPrice` |
| Dynamic Pricing Performance & Optimization Analytics | `listDynamicPricingPerformance` |
| AI Learning, Model Performance & Optimization Feedback | `listLearningModelPerformance` |

## Privacy  Consent   Preference Management — board 1

13 screens · 13 operations to author

| Screen | Operation to author |
|---|---|
| Privacy & Consent Configuration Command Center | `listPrivacyConsent` |
| Privacy & Consent Configuration Command Center | `setPrivacyConsent` |
| Data Processing Purpose & Lawful Basis Registry | `listDataProcessingPurpose` |
| Communication Preference & Marketing Permission Configuration | `setCommunicationPreferenceMarketing` |
| Cookie, Tracking & Digital Technology Registry | `listCookieTrackingDigital` |
| Cookie Banner & Preference Center Designer | `listCookieBannerPreference` |
| Cookie Banner & Preference Center Designer | `setCookieBannerPreference` |
| Consent Capture Point & Customer Journey Configuration | `setConsentCapturePoint` |
| Privacy Notice, Policy & Terms Version Management | `listPrivacyNoticePolicy` |
| Minor, Guardian & Age-Based Privacy Configuration | `setMinorGuardianAge` |
| Privacy Configuration Testing, Approval & Publication | `approvePrivacyTesting` |
| Privacy Configuration Testing, Approval & Publication | `publishPrivacyTesting` |
| Privacy Configuration Testing, Approval & Publication | `setPrivacyTesting` |

## Privacy  Consent   Preference Management — board 2

10 screens · 10 operations to author

| Screen | Operation to author |
|---|---|
| Privacy Operations Command Center | `listPrivacy` |
| Customer Privacy, Consent & Preference 360° | `listCustomerPrivacyConsent` |
| Consent Evidence, History & Withdrawal Management | `listConsentEvidenceWithdrawal` |
| Data Subject / Customer Privacy Request Management | `listDataSubjectCustomer` |
| Data Discovery, Access, Export & Correction Workspace | `setDataDiscoveryAccess` |
| Deletion, Anonymization & Restriction Operations | `listDeletionAnonymizationRestriction` |
| Data Retention, Expiry & Legal Hold Operations | `listDataRetentionExpiry` |
| Privacy Compliance, Exception & Investigation Workspace | `setPrivacyComplianceException` |
| Privacy Audit, Evidence & Compliance Reporting | `listPrivacyEvidenceCompliance` |
| Privacy Analytics & AI Compliance Intelligence | `listPrivacyCompliance` |

## Product Lifecycle   Catalogue Governance — board 1

9 screens · 9 operations to author

| Screen | Operation to author |
|---|---|
| Product Lifecycle Command Center | `listProductLifecycle` |
| Lifecycle Status & Workflow Configuration | `setLifecycleStatuWorkflow` |
| Bulk Product Creation & Catalogue Import | `createBulkProductCatalogue` |
| Product Import / Export & Environment Transfer | `listProductImportExport` |
| Product Context, Ownership & Assignment | `setProductContextOwnership` |
| Channel Publication & Availability | `publishChannelAvailability` |
| Publication & Activation Scheduler | `publishActivationScheduler` |
| Product Duplication & Template Library | `listProductDuplicationTemplate` |
| AI Catalogue Builder & Configuration Review | `setCatalogueReview` |

## Product Lifecycle   Catalogue Governance — board 2

11 screens · 11 operations to author

| Screen | Operation to author |
|---|---|
| Product Governance Command Center | `listProductGovernance` |
| Approval Workflow Designer | `approveWorkflow` |
| Approval Workflow Designer | `setWorkflow` |
| Approval Review & Decision Workspace | `approveReviewDecision` |
| Approval Review & Decision Workspace | `setReviewDecision` |
| Rollback & Recovery Management | `listRollbackRecovery` |
| Change Impact Analysis | `listChangeImpactAnalysi` |
| Change Propagation & Dependency Control | `listChangePropagationDependency` |
| Product Retirement, Suspension & Archive | `listProductRetirementSuspension` |
| Product Audit Trail & Change History | `listProductTrailChange` |
| Governance Risk, AI Monitoring & Control Center | `listGovernanceRiskMonitoring` |

## Promotions   Bundles Management — board 1

8 screens · 8 operations to author

| Screen | Operation to author |
|---|---|
| Promotion & Campaign Directory | `listPromotionCampaign` |
| Promotion Lifecycle & Status Manager | `listPromotionLifecycleStatu` |
| Campaign Calendar & Timeline | `listCampaignCalendarTimeline` |
| Promotion Channel & Publication Monitor | `listPromotionChannel` |
| Promotion Channel & Publication Monitor | `publishPromotionChannel` |
| Promotion Alerts & Exception Center | `listPromotionAlertException` |
| Promotion Health & Performance Monitor | `listPromotionHealthPerformance` |
| Promotion Audit, Activity & Version History | `listPromotionActivityVersion` |

## Promotions   Bundles Management — board 10

11 screens · 11 operations to author

| Screen | Operation to author |
|---|---|
| Promotion Performance Command Center | `listPromotionPerformance` |
| Campaign & Promotion Performance Explorer | `listCampaignPromotionPerformance` |
| Redemption, Conversion & Funnel Analytics | `listRedemptionConversionFunnel` |
| Discount, Margin & Profitability Analytics | `listDiscountMarginProfitability` |
| Bundle, BOGO & Advanced Offer Analytics | `listBundleBogoAdvanced` |
| Upsell, Cross-Sell & Attach-Rate Analytics | `listUpsellCrossSell` |
| Customer, Segment, Channel & Partner Analytics | `listCustomerSegmentChannel` |
| Incrementality, Attribution & Cannibalization Analysis | `listIncrementalityAttributionCannibalization` |
| AI Optimization & Next-Best-Action Center | `listNextBestAction` |
| Executive Promotion Intelligence & Reporting Studio | `listExecutivePromotionReporting` |
| Executive Promotion Intelligence & Reporting Studio | `setExecutivePromotionReporting` |

## Promotions   Bundles Management — board 2

11 screens · 11 operations to author

| Screen | Operation to author |
|---|---|
| Promotion Rule Builder | `setPromotionRule` |
| Percentage & Fixed Discount Configurator | `listPercentageFixedDiscount` |
| Cart & Transaction Threshold Rules | `listCartTransactionThreshold` |
| Volume, Bulk & Tier Discount Configurator | `listVolumeBulkTier` |
| Time-Based & Seasonal Discount Rules | `listTimeBasedSeasonal` |
| Customer, Membership & Segment Discount Rules | `listCustomerMembershipSegment` |
| Payment Method, Bank & Partner Discount Rules | `listPaymentMethodBank` |
| Special Price & Guest Offer Configurator | `listSpecialPriceGuest` |
| Discount Limits, Guardrails & Commercial Controls | `listDiscountLimitGuardrail` |
| Rule Test, Simulation & AI Recommendation Workspace | `setRuleTestRecommendation` |
| Rule Test, Simulation & AI Recommendation Workspace | `simulateRuleTestRecommendation` |

## Promotions   Bundles Management — board 3

9 screens · 9 operations to author

| Screen | Operation to author |
|---|---|
| Coupon & Promo Code Builder | `setCouponPromoCode` |
| Unique Code Generation & Batch Manager | `listUniqueCodeGeneration` |
| Code Eligibility & Restriction Manager | `listCodeEligibilityRestriction` |
| Usage, Capacity & Frequency Control | `listUsageCapacityFrequency` |
| Validity, Date & Time Control | `listValidityDateTime` |
| Code Distribution & Assignment Manager | `setCodeDistributionManager` |
| Redemption Monitor & Code Lookup | `listRedemptionCodeLookup` |
| Code Security, Fraud & Exception Center | `listCodeSecurityFraud` |
| Redemption Analytics, Audit & AI Optimization | `listRedemption` |

## Promotions   Bundles Management — board 4

11 screens · 11 operations to author

| Screen | Operation to author |
|---|---|
| Advanced Offer Command Center | `listAdvancedOffer` |
| Buy X Get Y / BOGO Rule Builder | `setBuyGetBogo` |
| Multi-Buy & Quantity Offer Configurator | `listMultiBuyQuantity` |
| Cheapest / Lowest-Value Item Promotion | `listCheapestLowestValue` |
| Fixed-Price & “N for X” Offer Builder | `setFixedPriceOffer` |
| Gift, Free Product & Added-Value Offer Builder | `setGiftFreeProduct` |
| Cross-Category Promotion Builder | `setCrossCategoryPromotion` |
| Reward Selection, Substitution & Customer Choice | `listRewardSelectionSubstitution` |
| Advanced Offer Guardrails & Conflict Controls | `listAdvancedOfferGuardrail` |
| Offer Simulation, Basket Trace & AI Optimization | `listOfferBasketTrace` |
| Offer Simulation, Basket Trace & AI Optimization | `simulateOfferBasketTrace` |

## Promotions   Bundles Management — board 5

10 screens · 10 operations to author

| Screen | Operation to author |
|---|---|
| Bundle & Combo Command Center | `listBundleCombo` |
| Bundle Definition & Setup | `setBundleDefinition` |
| Bundle Component Builder | `setBundleComponent` |
| Guest Choice & Build-Your-Own Bundle Designer | `setGuestChoiceBuild` |
| Bundle Pricing & Commercial Model | `listBundlePricingCommercial` |
| Bundle Availability, Capacity & Validation | `listBundleAvailabilityCapacity` |
| Bundle Validity, Scheduling & Redemption Rules | `listBundleValidityScheduling` |
| Partner & External Product Bundle Manager | `listPartnerExternalProduct` |
| Revenue Allocation, Cost & Settlement Rules | `listRevenueAllocationCost` |
| Bundle Preview, Simulation & AI Recommendation | `simulateBundlePreviewRecommendation` |

## Promotions   Bundles Management — board 6

11 screens · 10 operations to author

| Screen | Operation to author |
|---|---|
| Dynamic Bundle Operations Command Center | `listDynamicBundle` |
| Component Inventory & Availability Matrix | `listComponentInventoryAvailability` |
| Bundle Sellability & Dependency Rule Engine | `listBundleSellabilityDependency` |
| Capacity Pool & Reservation Manager | `listCapacityPoolReservation` |
| Dynamic Component Substitution Engine | `listDynamicComponentSubstitution` |
| Dynamic Bundle Rule & Composition Engine | `listDynamicBundleRule` |
| Real-Time Availability & Checkout Validation | `listRealTimeAvailability` |
| Bundle Availability by Channel, Venue & Partner | `listBundleAvailabilityChannel` |
| Bundle Availability Forecast, Alerts & Recovery | `listBundleAvailabilityForecast` |
| Dynamic Bundle Simulation & AI Optimization | `listDynamicBundle` |
| Dynamic Bundle Simulation & AI Optimization | `simulateDynamicBundle` |

## Promotions   Bundles Management — board 7

10 screens · 10 operations to author

| Screen | Operation to author |
|---|---|
| Targeting & Eligibility Command Center | `listTargetingEligibility` |
| Eligibility Rule Builder | `setEligibilityRule` |
| CRM & Customer Segment Manager | `listCrmCustomerSegment` |
| Membership, Loyalty & Guest Eligibility | `listMembershipLoyaltyGuest` |
| Behavioral & Transaction Targeting | `listBehavioralTransactionTargeting` |
| Context, Location, Channel & Time Targeting | `listContextLocationChannel` |
| Partner, B2B & Payment Eligibility | `listPartnerPaymentEligibility` |
| Audience Preview, Reach & Eligibility Simulator | `listAudiencePreviewReach` |
| Targeting Conflict, Frequency & Exclusion Controls | `listTargetingConflictFrequency` |
| AI Audience Discovery & Targeting Optimization | `listAudienceDiscoveryTargeting` |

## Promotions   Bundles Management — board 8

11 screens · 11 operations to author

| Screen | Operation to author |
|---|---|
| Stacking & Conflict Command Center | `listStackingConflict` |
| Promotion Priority & Hierarchy Manager | `listPromotionPriorityHierarchy` |
| Promotion Stacking Rule Builder | `setPromotionStackingRule` |
| Promotion Exclusion & Compatibility Matrix | `listPromotionExclusionCompatibility` |
| Discount Calculation & Application Sequence | `listDiscountCalculationApplication` |
| Best Offer & Customer Benefit Resolver | `listBestOfferCustomer` |
| Discount Cap & Maximum Benefit Controller | `listDiscountCapMaximum` |
| Conflict Detection & Resolution Center | `listConflictDetectionResolution` |
| Promotion Decision Trace & Transaction Explainer | `listPromotionDecisionTrace` |
| Conflict Simulation & AI Optimization | `listConflict` |
| Conflict Simulation & AI Optimization | `simulateConflict` |

## Promotions   Bundles Management — board 9

13 screens · 13 operations to author

| Screen | Operation to author |
|---|---|
| Campaign Governance & Budget Command Center | `listCampaignGovernanceBudget` |
| Campaign Budget & Financial Limit Setup | `setCampaignBudgetFinancial` |
| Redemption, Discount & Exposure Limit Manager | `listRedemptionDiscountExposure` |
| Budget Consumption & Forecast Monitor | `listBudgetConsumptionForecast` |
| Threshold Actions & Automatic Suspension | `listThresholdActionAutomatic` |
| Campaign Approval Workflow Designer | `approveCampaignWorkflow` |
| Campaign Approval Workflow Designer | `setCampaignWorkflow` |
| Approval Inbox & Decision Workspace | `approveDecision` |
| Approval Inbox & Decision Workspace | `listDecision` |
| Approval Inbox & Decision Workspace | `setDecision` |
| Campaign Financial & Commercial Simulator | `listCampaignFinancialCommercial` |
| Campaign Experiment & A/B Test Manager | `listCampaignExperimentTest` |
| Governance Audit, AI Risk & Launch Readiness | `listGovernanceRiskLaunch` |

## Rules  Workflow  Approval   Automation Engine — board 1

12 screens · 12 operations to author

| Screen | Operation to author |
|---|---|
| Rules & Workflow Command Center | `listRuleWorkflow` |
| Visual Business Rule Builder | `setVisualBusinessRule` |
| Conditions, Decision Logic & Decision Tables | `listConditionDecisionLogic` |
| Visual Workflow Designer | `setVisualWorkflow` |
| Approval Matrix & Multi-Level Approval Configuration | `approveMatrixMultiLevel` |
| Approval Matrix & Multi-Level Approval Configuration | `setMatrixMultiLevel` |
| Roles, Authority, Delegation & Approval Limits | `approveRoleAuthorityDelegation` |
| SLA, Escalation, Reminder & Timeout Rules | `listSlaEscalationReminder` |
| Trigger, Action & Cross-Module Orchestration Configuration | `setTriggerActionCross` |
| Workflow Testing, Simulation & Impact Analysis | `simulateWorkflowTestingImpact` |
| Versioning, Governance, Approval & Publication | `approveVersioningGovernance` |
| Versioning, Governance, Approval & Publication | `publishVersioningGovernance` |

## Rules  Workflow  Approval   Automation Engine — board 2

13 screens · 13 operations to author

| Screen | Operation to author |
|---|---|
| Workflow Operations Command Center | `listWorkflow` |
| Unified Approval Inbox & Decision Workspace | `approveUnifiedDecision` |
| Unified Approval Inbox & Decision Workspace | `listUnifiedDecision` |
| Unified Approval Inbox & Decision Workspace | `setUnifiedDecision` |
| Workflow Instance Monitor & Process Timeline | `listWorkflowInstanceProcess` |
| Workflow Exception, Failure & Recovery Center | `listWorkflowExceptionFailure` |
| SLA, Escalation & Bottleneck Monitor | `listSlaEscalationBottleneck` |
| Automation Execution & Autonomous Action Monitor | `createAutomationAutonomouAction` |
| Automation Execution & Autonomous Action Monitor | `listAutomationAutonomouAction` |
| Cross-Module Orchestration Monitor | `listCrossModuleOrchestration` |
| Workflow Analytics & Process Performance | `listWorkflowProcessPerformance` |
| Process Optimization & Automation Opportunity Center | `listProcessAutomationOpportunity` |
| AI Workflow Intelligence & Autonomous Governance Center | `listWorkflowAutonomouGovernance` |

## Sales Channel Management — board 1

11 screens · 11 operations to author

| Screen | Operation to author |
|---|---|
| Sales Channel Command Center | `listSaleChannel` |
| Channel Creation & Profile Configuration | `createChannelProfile` |
| Channel Creation & Profile Configuration | `setChannelProfile` |
| Product & Catalogue Assignment | `setProductCatalogue` |
| Channel Pricing & Commercial Profile Assignment | `setChannelPricingCommercial` |
| Inventory, Capacity & Channel Allocation | `listInventoryCapacityChannel` |
| Channel Sales Schedule & Availability Windows | `listChannelSaleSchedule` |
| Customer & Eligibility Rules by Channel | `listCustomerEligibilityRule` |
| Channel Sales Rules, Limits & Restrictions | `listChannelSaleRule` |
| Channel Fees, Payment & Fulfillment Configuration | `setChannelFeePayment` |
| Channel Publication, Readiness & AI Validation | `publishChannelReadinessValidation` |

## Sales Channel Management — board 2

10 screens · 9 operations to author

| Screen | Operation to author |
|---|---|
| Channel Operations Command Center | `listChannel` |
| Channel Connection & Integration Manager | `listChannelConnectionIntegration` |
| Product, Price & Availability Synchronization | `listProductPriceAvailability` |
| Real-Time Channel Availability & Inventory Monitor | `listRealTimeChannel` |
| Channel Allocation & Rebalancing Operations | `listChannelAllocationRebalancing` |
| Channel Exceptions, Incidents & Recovery | `listChannelExceptionIncident` |
| Channel Performance & Commercial Analytics | `listChannelPerformanceCommercial` |
| Channel Audit, Logs & Transaction Traceability | `listChannelLogTransaction` |
| Channel Governance, SLA & Partner Control | `listChannelGovernanceSla` |
| AI Channel Optimization & Intelligence Center | `listChannel` |

## Ticket Media   Credential Management — board 1

10 screens · 10 operations to author

| Screen | Operation to author |
|---|---|
| Virtual Ticket Command Center | `listVirtualTicket` |
| Virtual Ticket Identity & Master Record Configuration | `setVirtualTicketIdentity` |
| Virtual Ticket Status & Lifecycle Model | `listVirtualTicketStatu` |
| Media Type & Credential Technology Registry | `listMediaTypeCredential` |
| Multi-Media Binding & Association Rules | `listMultiMediaBinding` |
| Credential Identity, Token & Reference Mapping | `listCredentialIdentityToken` |
| Entitlement & Cross-Media Synchronization Rules | `listEntitlementCrossMedia` |
| Media Activation, Priority & Fallback Rules | `listMediaActivationPriority` |
| Media Replacement, Revocation & Rebinding Rules | `listMediaReplacementRevocation` |
| Virtual Ticket Architecture Testing, Governance & Audit | `listVirtualTicketArchitecture` |

## Ticket Media   Credential Management — board 2

12 screens · 12 operations to author

| Screen | Operation to author |
|---|---|
| Media Design Studio Command Center | `listMediaDesign` |
| Media Design Studio Command Center | `setMediaDesign` |
| Digital QR & Barcode Ticket Designer | `setDigitalBarcodeTicket` |
| PDF, Printable & POS Ticket Designer | `setPdfPrintablePos` |
| Apple Wallet Pass Designer | `setAppleWalletPass` |
| Google Wallet Pass Designer | `setGoogleWalletPass` |
| RFID, NFC, Card & Wristband Media Designer | `setRfidNfcCard` |
| Digital Card, Membership & Wearable Designer | `setDigitalCardMembership` |
| Dynamic Fields, Data Mapping & Content Builder | `setDynamicFieldData` |
| Branding, Localization & Template Inheritance | `listBrandingLocalizationTemplate` |
| Multi-Media Preview, Testing, Approval & Publication | `approveMultiMediaPreview` |
| Multi-Media Preview, Testing, Approval & Publication | `publishMultiMediaPreview` |

## Ticket Media   Credential Management — board 3

10 screens · 10 operations to author

| Screen | Operation to author |
|---|---|
| Credential Operations Command Center | `listCredential` |
| Virtual Ticket & Credential 360° Workspace | `setVirtualTicketCredential` |
| Credential Generation & Issuance Monitor | `listCredentialGenerationIssuance` |
| Credential Delivery & Distribution Operations | `listCredentialDeliveryDistribution` |
| Media Binding, Activation & Assignment Operations | `setMediaBindingActivation` |
| Credential Replacement, Reissue, Revocation & Recovery | `listCredentialReplacementReissue` |
| Failed Generation, Delivery & Credential Exception Management | `listFailedGenerationDelivery` |
| Credential Usage & Cross-Media Traceability | `listCredentialUsageCross` |
| Credential Security, Audit & Operational Evidence | `listCredentialSecurityOperational` |
| Ticket Media Analytics & AI Operations Intelligence | `listTicketMedia` |

## Ticket Resale Marketplace — board 1

11 screens · 11 operations to author

| Screen | Operation to author |
|---|---|
| Resale Marketplace Command Center | `listResaleMarketplace` |
| Resale Eligibility Rule Configuration | `setResaleEligibilityRule` |
| Resale Policy & Marketplace Settings | `listResalePolicyMarketplace` |
| Listing Creation & Seller Configuration | `createListingSeller` |
| Listing Creation & Seller Configuration | `setListingSeller` |
| Resale Pricing & Price Guardrails | `listResalePricingPrice` |
| Resale Fees, Commission & Seller Proceeds | `listResaleFeeCommission` |
| Listing Approval & Moderation | `approveListingModeration` |
| Resale Inventory & Availability Management | `listResaleInventoryAvailability` |
| Listing Lifecycle, Expiry & Cancellation | `listListingLifecycleExpiry` |
| AI Resale Configuration & Marketplace Recommendations | `setResaleMarketplaceRecommendation` |

## Ticket Resale Marketplace — board 2

10 screens · 9 operations to author

| Screen | Operation to author |
|---|---|
| Resale Operations Command Center | `listResale` |
| Buyer Purchase & Resale Order Management | `listBuyerPurchaseResale` |
| Ticket Ownership Transfer Management | `listTicketOwnershipTransfer` |
| Credential Revocation & Regeneration | `listCredentialRevocationRegeneration` |
| Resale Fraud & Duplicate Sale Protection | `listResaleFraudDuplicate` |
| Capacity & Inventory Reconciliation | `listCapacityInventoryReconciliation` |
| Seller Settlement & Payout Management | `listSellerSettlementPayout` |
| Refunds, Disputes & Resale Exceptions | `listRefundDisputeResale` |
| Resale Audit & Ownership History | `listResaleOwnership` |
| Resale Analytics & AI Intelligence | `listResale` |

## Ticket Resale Marketplace — board 3

10 screens · 10 operations to author

| Screen | Operation to author |
|---|---|
| My Tickets & Resale Marketplace Entry | `listTicketResaleMarketplace` |
| Resale Eligibility & Ticket Selection | `listResaleEligibilityTicket` |
| Create Listing & Resale Price Selection | `listCreateListingResale` |
| Fees, Seller Proceeds & Listing Confirmation | `listFeeSellerProceed` |
| My Resale Listings & Seller Dashboard | `listResaleListingSeller` |
| Official Resale Marketplace & Buyer Discovery | `listOfficialResaleMarketplace` |
| Resale Ticket Detail, Seat Selection & Primary-vs-Resale Experience | `listResaleTicketDetail` |
| Buyer Checkout, Inventory Hold & Secure Payment | `listBuyerCheckoutInventory` |
| Resale Confirmation, Ownership Transfer & Ticket Delivery | `listResaleConfirmationOwnership` |
| White-Label Marketplace Deployment & Experience Architecture | `listWhiteLabelMarketplace` |

## Ticket Upgrade, Exchange & Conversion — board 1

10 screens · 10 operations to author

| Screen | Operation to author |
|---|---|
| Upgrade & Conversion Command Center | `listUpgradeConversion` |
| Upgrade & Conversion Path Builder | `setUpgradeConversionPath` |
| Upgrade Eligibility & Qualification Rules | `listUpgradeEligibilityQualification` |
| Upgrade Timing, Usage & Ticket Status Rules | `listUpgradeTimingUsage` |
| Upgrade Financial Treatment & Price Difference Rules | `listUpgradeFinancialTreatment` |
| Pro-Rata, Residual Value & Entitlement Credit Configuration | `setProRataResidual` |
| Person-Type, Product & Entitlement Conversion Rules | `listPersonTypeProduct` |
| Bulk, Group & Assisted Upgrade Operations | `listBulkGroupAssisted` |
| Upgrade Execution, Credential Regeneration & Channel Controls | `createUpgradeCredentialRegeneration` |
| Upgrade History, Exception Management & Audit Explorer | `listUpgradeException` |

## Waiver, Consent & Digital Form Management — board 1

13 screens · 13 operations to author

| Screen | Operation to author |
|---|---|
| Waiver & Consent Command Center | `listWaiverConsent` |
| Waiver Template Library & Master Setup | `listWaiverTemplateMaster` |
| Waiver Template Library & Master Setup | `setWaiverTemplateMaster` |
| Digital Waiver & Form Builder | `setDigitalWaiverForm` |
| Dynamic Fields, Questions & Conditional Logic | `listDynamicFieldQuestion` |
| Signatory, Signature & Guardian Rule Configuration | `setSignatorySignatureGuardian` |
| Product, Event & Experience Association | `listProductEventExperience` |
| Waiver Trigger, Eligibility & Completion Rules | `listWaiverTriggerEligibility` |
| Versioning, Effective Dates & Legal Change Control | `listVersioningEffectiveDate` |
| Localization, Branding & Customer Experience Configuration | `setLocalizationBrandingCustomer` |
| Waiver Approval, Testing & Publication Workspace | `approveWaiverTesting` |
| Waiver Approval, Testing & Publication Workspace | `publishWaiverTesting` |
| Waiver Approval, Testing & Publication Workspace | `setWaiverTesting` |

## Waiver, Consent & Digital Form Management — board 2

10 screens · 10 operations to author

| Screen | Operation to author |
|---|---|
| Waiver Operations Command Center | `listWaiver` |
| Participant Waiver Status & Tracking | `listParticipantWaiverStatu` |
| Digital Signing & Collection Operations | `listDigitalSigningCollection` |
| Minor, Guardian & Group Consent Management | `listMinorGuardianGroup` |
| Waiver Verification & Validation Workspace | `setWaiverVerificationValidation` |
| Missing, Expired & Invalid Waiver Management | `listMissingExpiredInvalid` |
| On-Site Waiver & Exception Handling | `listSiteWaiverException` |
| Compliance Evidence, Audit & Waiver Repository | `listComplianceEvidenceWaiver` |
| Waiver Analytics, Compliance & Operational Insights | `listWaiverComplianceOperational` |
| AI Waiver Compliance & Risk Intelligence Center | `listWaiverComplianceRisk` |
