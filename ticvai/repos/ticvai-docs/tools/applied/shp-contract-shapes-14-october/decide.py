"""C-NO-ADDRESS decisions: every member is S (x-ticvai-singleton, with a note saying what it is one of) or K (a path key).

    python -I decide.py <ticvai root> <scratch>   -> <scratch>/noaddr-decisions.json
"""
import sys, json, re
from pathlib import Path
root, S = Path(sys.argv[1]), Path(sys.argv[2])
rows = {r['op']: r for r in json.load(open(S / 'noaddr.json', encoding='utf-8'))}
cls = json.load(open(S / 'noaddr-cls.json', encoding='utf-8'))

# K: the write replaces one item of a collection, named by its own key. op -> path parameter (the body field it
# equals, or a new id). An existing item path under the collection is reused by the script.
K = {
    # persisted rows with their own id, listed beside the write or created-or-replaced one at a time
    'configureQueueFeed': 'feedId', 'setAccessPointGroup': 'groupId', 'setChannelConnectionConfiguration': 'connectionId',
    'setConfigurationProfile': 'profileId', 'setHardwareModel': 'modelId', 'setIndexSource': 'sourceId',
    'setIntegrationSource': 'sourceId', 'setJourneySequenceRule': 'ruleId', 'setMediaBindingRule': 'ruleId',
    'setOperatingCalendarEntry': 'entryId', 'setPaymentTerminalConfiguration': 'deviceId', 'setPodium': 'podiumId',
    'setPricingChangeRequest': 'changeId', 'setReasonCode': 'reasonCodeId', 'setRecipe': 'recipeId',
    'setAccessProfile': 'accessProfileId', 'setAgentServiceProfile': 'agentServiceProfileId', 'setAiProvider': 'providerId',
    'setAlertRule': 'alertRuleId', 'setAnalyticsProvider': 'analyticsProviderId', 'setApiAnomalyRule': 'anomalyRuleId',
    'setApiLicensing': 'licenceId', 'setApiQuota': 'quotaId', 'setApprovalControlPolicy': 'controlPolicyId',
    'setApprovalExternalProvider': 'externalProviderId', 'setApprovalMatrix': 'matrixId',
    'setAttractionType': 'attractionTypeId', 'setBadge': 'badgeId', 'setBadgeTemplate': 'badgeTemplateId',
    'setCapabilityTemplate': 'capabilityTemplateId', 'setCaseCategoryDefinition': 'caseCategoryId',
    'setCaseInternalRequest': 'internalRequestId', 'setChannelListing': 'listingId',
    'setCommunicationRoutingRule': 'routingRuleId', 'setContactAutomation': 'automationId',
    'setCookieBannerDesign': 'bannerDesignId', 'setCookieScanPolicy': 'scanPolicyId',
    'setEInvoicingProvider': 'eInvoicingProviderId', 'setEventType': 'eventTypeId', 'setFxRate': 'rateId',
    'setIntelligentRoutingSkill': 'routingRuleId', 'setJobTitle': 'jobTitleId', 'setLabourBudget': 'labourBudgetId',
    'setLeaveType': 'leaveTypeId', 'setLicensingModel': 'licensingModelId', 'setLoyaltyCampaign': 'loyaltyCampaignId',
    'setMembershipBenefit': 'benefitId', 'setMerchantAccount': 'merchantAccountId',
    'setParkingFacility': 'parkingFacilityId', 'setPaymentProvider': 'providerId',
    'setPerformanceTemplate': 'performanceTemplateId', 'setPrivacyComplianceException': 'exceptionId',
    'setPrivacyNoticePolicyGovernance': 'governanceId', 'setPrivacyRequestTypes': 'requestTypeId',
    'setQualityEvaluation': 'evaluationId', 'setReconciliationSource': 'sourceId', 'setReward': 'rewardId',
    'setSeatHoldType': 'holdTypeId', 'setServiceQueueDefinition': 'queueId', 'setShiftPattern': 'shiftPatternId',
    'setShiftTemplate': 'shiftTemplateId', 'setSlaPolicy': 'slaPolicyId', 'setSpace': 'spaceId',
    'setStoreRules': 'storeRuleId', 'setTaxInvoiceTemplate': 'invoiceTemplateId',
    'setTemperatureCheckpoint': 'checkpointId', 'setWafPolicy': 'wafRuleId', 'setWaiverAssociation': 'associationId',
    'setWaiverException': 'waiverExceptionId', 'setWaiverTriggerRule': 'triggerRuleId',
    'setWaiverVerificationValidation': 'verificationId', 'setWorkAssignment': 'workAssignmentId',
    'setCaseResolution': 'caseResolutionId',
    'setConfigurationTemplate': 'configurationTemplateId', 'setFastPassProfile': 'fastPassProfileId',
    'setFeeDefinition': 'feeId', 'setGateModePolicy': 'gateModePolicyId', 'setJourneyProfile': 'journeyProfileId',
    'setMarketPricingConfiguration': 'marketId', 'setPriceCalculationPolicy': 'calculationProfileId',
    'setPriceCategoryRateType': 'priceCategoryId', 'setRefundCompensationService': 'compensationRequestId',
    'setSignalRegistryPolicy': 'signalId', 'setApprovalSlaPolicy': 'slaPolicyId',
    'setDataRetentionPolicy': 'retentionPolicyId', 'setCurrencyRoundingRule': 'roundingProfileId',
    'setGiftCardProduct': 'giftCardProductId', 'setPrepaidMinutePackage': 'packageId',
    'setReaderProfile': 'readerProfileId', 'setChannelProvider': 'channelProviderId',
    'setSenderIdentityDomain': 'senderIdentityId', 'setApproverAvailability': 'availabilityId',
    'setApprovalRetentionPolicy': 'retentionPolicyId', 'setOrderBookingTicket': 'serviceActionId',
    'setTrialConfiguration': 'trialConfigurationId', 'setMediaDistributionChannels': 'code',
    # drafted or request-only bodies whose own key names one item of a list the screen shows
    'setAccessAttributeCatalog': 'attributeKey', 'setBiometricLifecycleRetention': 'policyId',
    'setBusinessEventMapping': 'eventId', 'setCredentialActivationDisplay': 'ruleId',
    'setDataProcessingPurpose': 'purposeId', 'setEntitlementConsumption': 'ruleId',
    'setFaceTagTemporaryEnrollment': 'profileId', 'setFraudDetectionRule': 'ruleId',
    'setGroupCustomerOrganization': 'organisationId', 'setGuestCompanionEligibility': 'ruleId',
    'setHotelWalletExternal': 'integrationId', 'setLegalHold': 'holdId', 'setMediaIssuanceEncoding': 'encodingProfileId',
    'setMediaTypeTechnology': 'mediaTypeId', 'setMembershipProgramme': 'programId', 'setModuleListing': 'moduleCode',
    'setOutletTemplate': 'code', 'setPolicyScopeHierarchy': 'policyId', 'setPrivacyAction': 'actionId',
    'setPrivacyRequest': 'requestId', 'setTrackingTechnology': 'technologyId', 'setWaiverTemplateMaster': 'waiverId',
    'setMediaReplacementRevocation': 'replacementReason', 'setFaceMatchingVerification': 'profileId',
    'publishActivationScheduler': 'scheduleId', 'setPartnerContact': 'contactId',
    'setDynamicFieldQuestion': 'formId/key',
    # a decision on one approval request, which the body never named
    'approveDecision': 'approvalRequestId', 'approveExceptionServiceRecovery': 'approvalRequestId',
    'approveGroupDiscountException': 'approvalRequestId',
}

# S per parent: op -> (body field, what it is one per). Everything else S per scope, set-replacement or self.
PARENT = {
    'approveBookingLimitCommercial': ('partnerId', 'partner'), 'approveMembershipProductValidation': ('membershipCode', 'membership product'),
    'approveMultiMediaPreview': ('templateId', 'ticket media template'), 'approvePartnerStatuLifecycle': ('partnerId', 'partner'),
    'approvePricingWorkflowAuthority': ('policyId', 'pricing approval policy'), 'approvePrivacyTesting': ('changeSetId', 'privacy change set'),
    'approveReviewDecision': ('changeRequestId', 'pricing change request'), 'approveUnifiedDecision': ('approvalRequestId', 'approval request'),
    'approveVersioningGovernance': ('workflowId', 'workflow'), 'approveWaiverTesting': ('formId', 'waiver form'),
    'approveWorkflow': ('workflowId', 'workflow'), 'approveMatrixMultiLevel': ('code', 'approval matrix code'),
    'publishChannelAvailability': ('productId', 'product'), 'publishChannelReadinessValidation': ('channelId', 'sales channel'),
    'publishMediaCompatibilityTesting': ('mediaProfileId', 'media profile'), 'publishPricingEffectiveDate': ('changeRequestId', 'pricing change request'),
    'publishRuleConflictCheck': ('ruleVersionId', 'access rule version'), 'publishTopologyValidation': ('configurationVersionId', 'access configuration version'),
    'setAccessAreaZone': ('zoneId', 'access zone'), 'setAccessGraphicalMap': ('mapId', 'venue access map'),
    'setAccessibleSeating': ('seatMapId', 'seat map'), 'setAccreditationNotificationRules': ('programmeId', 'accreditation programme'),
    'setAccreditationRequirements': ('programmeId', 'accreditation programme'), 'setAccreditationValidity': ('programmeId', 'accreditation programme'),
    'setAfterSaleFinancial': ('orderId', 'order'), 'setAgreementContractTerm': ('agreementId', 'partner agreement'),
    'setAppleWalletPass': ('templateId', 'ticket media template'), 'setAttractionAccess': ('attractionId', 'attraction'),
    'setBiometricVerificationProfile': ('profileId', 'biometric verification profile'), 'setBleBeaconGeofence': ('beaconId', 'beacon'),
    'setBookingVelocityTime': ('ruleId', 'pricing rule'), 'setBrandingLocalizationTemplate': ('scopeId', 'scope node'),
    'setCaseInvestigationResolution': ('caseId', 'case and linked record'), 'setCatalogueReview': ('sessionId', 'catalogue builder session'),
    'setChannelFeePayment': ('channelId', 'sales channel'), 'setChannelPricingCommercial': ('channelId', 'sales channel'),
    'setChannelSyncSetting': ('salesChannelId', 'sales channel and data domain'), 'setCodeDistributionManager': ('batchId', 'code batch'),
    'setCommunicationPreferenceMarketing': ('categoryCode', 'communication preference category'),
    'setConsentCapturePoint': ('capturePoint', 'capture point and channel'), 'setContextTimeEvent': ('policyId', 'access policy'),
    'setCredentialEventPropagationRule': ('triggerEvent', 'ticket lifecycle event'), 'setCustomerGuestAccount': ('customerId', 'customer'),
    'setDailyCount': ('locationId', 'stock location'), 'setDataDiscoveryAccess': ('requestId', 'privacy request'),
    'setDemandOccupancyAvailability': ('ruleId', 'pricing rule'), 'setDenominations': ('currencyCode', 'currency'),
    'setDeviceSoftwareContent': ('deviceGroupId', 'device group'), 'setDigitalBarcodeTicket': ('templateId', 'ticket media template'),
    'setDigitalCardMembership': ('templateId', 'ticket media template'), 'setDynamicFieldData': ('fieldKey', 'dynamic field'),
    'setDynamicPricingGuardrailPolicy': ('scopeId', 'scope node'), 'setDynamicPricingStrategy': ('strategyCode', 'pricing strategy'),
    'setDynamicSecurityProfile': ('profileId', 'dynamic QR security profile'), 'setEdgeNodeLocal': ('edgeNodeId', 'edge node'),
    'setEmbeddedEntitlementPayload': ('profileId', 'payload profile'), 'setFamilyHouseholdDependent': ('membershipCode', 'membership product'),
    'setFeeApplicabilityCharging': ('ruleId', 'fee rule'), 'setFnbDeliveryPolicy': ('outletId', 'outlet'),
    'setFnbReservationPolicy': ('outletId', 'outlet'), 'setGameKioskConfiguration': ('kioskDeviceId', 'kiosk'),
    'setGamePricing': ('gameId', 'game'), 'setGateLane': ('gateId', 'gate'), 'setGoogleWalletPass': ('templateId', 'ticket media template'),
    'setGroupAdmissionProfile': ('profileId', 'group admission profile'), 'setHandheldMobileAccess': ('profileId', 'handheld device profile'),
    'setMediaBindingActivation': ('virtualTicketId', 'virtual ticket'), 'setMemberMembershipAccount': ('membershipId', 'membership'),
    'setMembershipCommercialConfig': ('membershipCode', 'membership product'), 'setMembershipEligibilityQualification': ('membershipCode', 'membership product'),
    'setMembershipEntitlementAdmission': ('membershipCode', 'membership product'), 'setMembershipProductTier': ('membershipCode', 'membership product'),
    'setMembershipUsagePolicy': ('membershipCode', 'membership product'), 'setOperationalIncidentException': ('incidentId', 'incident'),
    'setPackagePricingDefinition': ('productId', 'package product'), 'setPartnerBrandVenue': ('partnerId', 'partner'),
    'setPartnerProfileOrganization': ('partnerId', 'partner'), 'setPartnerRateNet': ('agreementId', 'partner agreement'),
    'setPaymentTermBilling': ('agreementId', 'partner agreement'), 'setPdfPrintablePos': ('templateId', 'ticket media template'),
    'setPolicyEvaluationSetting': ('policyCategory', 'policy category'), 'setPriceHierarchyInheritance': ('hierarchyId', 'price hierarchy'),
    'setProductCatalogue': ('channelId', 'sales channel'), 'setProductServicePrice': ('assignmentId', 'price assignment'),
    'setReaderScannerPeripheral': ('accessPointId', 'access point'), 'setRealTimeSecurity': ('playbookId', 'security playbook'),
    'setReconciliationMatchingRules': None, 'setRedemptionRules': None,
    'setRelationshipFraudRule': ('ruleId', 'relationship fraud rule'), 'setRenewalAutoMembership': ('membershipCode', 'membership product'),
    'setRentalDepositPolicy': ('productId', 'rental product or category'), 'setRentalFeePolicy': ('productId', 'rental product'),
    'setResaleFeePolicy': ('eventId', 'event or product'), 'setResourceSelectionPolicy': ('ticketTypeId', 'ticket type'),
    'setRfidNfc': ('rfidNfcProfileId', 'RFID/NFC profile'), 'setRfidNfcCard': ('templateId', 'ticket media template'),
    'setRuleTestRecommendation': None, 'setSecurityInvestigationEvidence': ('investigationId', 'investigation'),
    'setSeatRecommendationRules': ('seatMapId', 'seat map'), 'setSeatRules': ('seatMapId', 'seat map'),
    'setSeoMetadata': ('entityId', 'entity and locale'), 'setStepUpPolicy': ('operationId', 'operation'),
    'setTaxProfileJurisdiction': ('taxProfileCode', 'tax profile'), 'setTaxRuleTreatment': ('taxRuleId', 'tax rule'),
    'setTicketStatusTransition': ('fromStatus', 'status transition (fromStatus, toStatus)'), 'setTriggerActionCross': ('workflowId', 'workflow'),
    'setTurnstileLaneBehavior': ('accessPointId', 'access point'), 'setUpgradeConversionPath': ('pathCode', 'upgrade path'),
    'setValidationOutcomeGuest': ('outcomeProfileId', 'outcome profile'), 'setValidityActivationExpiry': ('membershipCode', 'membership product'),
    'setVerificationMethodPolicy': ('productId', 'product'), 'setVirtualTicketCredential': ('virtualTicketId', 'virtual ticket'),
    'setVisualAccessRule': ('ruleId', 'access rule'), 'setVisualBusinessRule': ('ruleId', 'business rule'),
    'setVisualDynamicPolicy': ('policyId', 'dynamic policy'), 'setVisualWorkflow': None,
    'setWalletFundingRules': ('walletTypeId', 'wallet type'), 'setWalletIntegrationMapping': ('apiClientId', 'API client'),
    'simulateBundlePreviewRecommendation': ('bundleId', 'bundle'), 'simulatePolicyConflictImpact': ('policyId', 'access policy'),
    'simulateWorkflowTestingImpact': ('workflowId', 'workflow'), 'setMarketingSubscription': ('subjectId', 'guest, channel and list'),
    'setHomepageLayout': ('templateKey', 'site template'), 'setSiteSetupProgress': None,
    'setVenueSettingsDefaults': None, 'setScalingPolicy': ('cellId', 'cell and service'),
    'setWorkOrderPriorityPolicy': None, 'setAiPolicy': None, 'setCustomerServiceCopilot': None,
}
SET = {'setAccountMappings', 'setConsentPurposes', 'setFaqs', 'setFraudRules', 'setGuestExtraFields', 'setKitchenStations',
       'setPaymentRoutingRules', 'setProductCategories', 'setProductRelationships', 'setSegregationRules',
       'setSiteNormalisationBases', 'setSubstitutionRules', 'setRulePriorityConflict', 'setFxProvider',
       'setSuggestionProvider', 'setStoreAccounts', 'setFeatureToggles', 'setModuleEnablement', 'setPaymentRiskRules',
       'setWalletReconciliationSources', 'setWalletRiskRules', 'setWalletAccountingMapping'}
SELF = {'deleteGuestAccount': 'account', 'guestLogout': 'session', 'updateMyProfile': 'profile',
        'setLeaderboardNickname': 'leaderboard nickname', 'setAgentAvailability': 'availability'}
SCOPE_WORD = {'tenant': 'tenant', 'venue': 'venue', 'region': 'region', 'platform': 'platform', 'subject': 'guest'}

out = {}
for oid, r in rows.items():
    scope = SCOPE_WORD.get(r['scope'] or 'venue', r['scope'])
    if oid in K:
        out[oid] = {'kind': 'K', 'param': K[oid]}
    elif oid in SELF:
        who = 'staff member' if oid == 'setAgentAvailability' else 'guest'
        out[oid] = {'kind': 'S', 'note': f"The caller's own {SELF[oid]}: one per signed-in {who}, so there is no key in the path."}
    elif oid in SET:
        out[oid] = {'kind': 'S', 'note': f"One set per {scope}, the caller's {scope}: a PUT replaces the whole set, and an entry the body leaves out is removed. There is no key in the path."}
    elif PARENT.get(oid):
        field, what = PARENT[oid]
        out[oid] = {'kind': 'S', 'note': f"One per {what}, the one the body's `{field}` names, within the caller's {scope}: a PUT replaces it whole. There is no key in the path."}
    else:
        out[oid] = {'kind': 'S', 'note': f"One per {scope}, the caller's {scope}: a PUT replaces it whole. There is no key in the path."}
json.dump(out, open(S / 'noaddr-decisions.json', 'w', encoding='utf-8'), indent=1)
from collections import Counter
print(Counter(v['kind'] for v in out.values()))
missing_k = [o for o in K if o not in rows]
print('K not in class:', missing_k)
