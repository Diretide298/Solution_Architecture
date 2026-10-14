#!/usr/bin/env python3
"""One-off, batch STO (Block A storage audit, 14 October 2026): what an operation's ids, description and drafted
request say about storage. Already applied; kept as the record of what was changed and why. Idempotent.

* CHG-STO-019 (check-parameter-columns P-PARAM-NO-COLUMN): an `<x>Id` parameter matches a column the operation's
  lineage reads or writes. Where the column has another name, or the id is its row's own `id`, the parameter says
  which (`x-ticvai-column: <schema>.<table>.<column>`: `templateId` is `plan_benefit.entitlement_template_id`, a
  `programmeId` is the loyalty tables' `program_id`, a path's `profileId` is `admission_rules.id`); where the table the
  id selects through was missing from the lineage, the lineage reads it (`listEmployees` reads
  `workforce.work_assignment` for `jobTitleId`); where the table had no key at all, it gets one (a rental damage
  assessment, equipment assignment and inspection name their booking; a rendition its media asset; each rental rule
  set its product; a resource's venue assignment its resource; a guest link the local subject it resolves). An id
  that selects no row and is an input to what the operation computes (the customer a price simulation is for, the
  device a policy bundle is signed for, the length variant whose duration is the window) says `x-ticvai-column: none`.
* CHG-STO-020 (P-NAMED-TABLE): a table an operation's description names is in its lineage (an approval writes its
  `tenancy.device_audit` row, a checkout its `orders.deposit`, an incident report its involved parties, a sync its
  `workforce.employee` rows), or the operation declares it named for context only (`x-ticvai-names-for-context`): a
  contrast ("not `approvals.sla_policy`"), the table another module's operation writes ("written by OrderService").
* CHG-STO-021 (P-DRAFTED-UNMAPPED): a drafted workspace request names the table its operation writes
  (`x-ticvai-persistence: none — request only; applied to <table> ...`), not "no existing table".

    python3 tools/applied/sto-parameters-14-october.py [--apply]
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from sto_markers import Contracts  # noqa: E402

# (operationId, parameter, column it matches as <schema>.<table>.<column>, or none)
PARAM_COLUMN = [
    ("amendAttendance", "recordId", "workforce.attendance.id"),
    ("setAiRiskRegisterEntry", "entryId", "ai.risk_register.id"),
    ("listLeaveBalances", "leaveTypeId", "workforce.leave_balance.type_id"),
    ("listPrivacyEvidenceCompliance", "requestId", "marketing.privacy_audit_event.related_request_id"),
    ("recordBenefitUsage", "membershipId", "identity.benefit_usage.customer_membership_id"),
    ("getPlanBenefits", "templateId", "catalogue.plan_benefit.entitlement_template_id"),
    ("setPlanBenefits", "templateId", "catalogue.plan_benefit.entitlement_template_id"),
    ("getWaiverTesting", "eventId", "marketing.waiver_association.target_id"),
    ("getWaiverTesting", "productId", "marketing.waiver_association.target_id"),
    ("listWaiverConsent", "eventId", "marketing.waiver_association.target_id"),
    ("listWaiverConsent", "productId", "marketing.waiver_association.target_id"),
    ("listLoyaltyPointEntries", "programmeId", "marketing.loyalty_points.program_id"),
    ("listLoyaltyCampaigns", "programmeId", "marketing.loyalty_campaign.program_id"),
    ("listRewards", "programmeId", "marketing.reward.loyalty_program_id"),
    ("listConsentAnswers", "subjectId", "marketing.booking_consent_record.person_subject_id"),
    ("getExperienceResourceRequirements", "experienceId", "resources.resource_requirement.product_id"),
    ("setExperienceResourceRequirements", "experienceId", "resources.resource_requirement.product_id"),
    ("getFacePassEnrolment", "enrolmentId", "pii.subject_biometric.id"),
    ("revokeFacePass", "enrolmentId", "pii.subject_biometric.id"),
    ("getTaxDocumentRendition", "documentId", "ledger.tax_invoice.id"),
    ("listCustomerService", "agentPrincipalId", "marketing.case.assigned_to_principal_id"),
    ("listCustomerSatisfactionFeedback", "agentPrincipalId", "marketing.case.assigned_to_principal_id"),
    ("updateAdmissionRules", "profileId", "access.admission_rules.id"),
    ("listUnifiedInteractionCommunication", "agentPrincipalId", "marketing.conversation.assigned_principal_id"),
    ("listUnifiedInteractionCommunication", "orderId", "marketing.case.related_order_id"),
    ("listUnifiedInteractionCommunication", "ticketId", "marketing.case.id"),
    ("listPermissionFindings", "draftPolicyId", "identity.authorisation_policy.id"),
    ("revokeEntitlementShare", "shareId", "identity.delegated_access.id"),
    ("listChannelCustomerSegment", "strategyId", "pricing.dynamic_price_rule.dynamic_pricing_strategy_id"),
    ("listRulePriorityConflict", "strategyId", "pricing.dynamic_price_rule.dynamic_pricing_strategy_id"),
    ("listDynamicPriceBand", "strategyId", "catalogue.price_ladder.dynamic_pricing_strategy_id"),
    ("listLocationVenueEvent", "contextRefId", "catalogue.event.id"),
    ("listProductTrailChange", "userId", "catalogue.audit_entry.actor_principal_id"),
    ("listCredentialIdentityToken", "virtualTicketId", "access.entitlement.id"),
    ("listTicketCredentialInvestigation", "virtualCredentialId", "access.entitlement.id"),
    ("listChannelLogTransaction", "transactionId", "orders.sales_order.id"),
    ("listPartnerOrderBooking", "ticvaiOrderId", "orders.payment.order_id"),
    ("listSiteWaiverException", "customerSubjectId", "marketing.waiver_requirement.signatory_subject_id"),
    ("listSiteWaiverException", "membershipId", "marketing.waiver_requirement.ticket_id"),
    ("listMemberExceptionOverride", "membershipId", "access.entitlement.id"),
    ("listMemberLifecycleCase", "membershipId", "access.entitlement.id"),
    ("listOrderReservation", "membershipId", "orders.membership_renewal.customer_membership_id"),
    # inputs to a computation, not row selectors
    ("getAuthorisationPolicyBundle", "deviceId", "none"),
    ("listPricingRulePriority", "customerId", "none"),
    ("listPricingRulePriority", "membershipId", "none"),
    ("listCustomerSegmentProfile", "customerId", "none"),
    ("listProductStartTimes", "variantId", "none"),
]
# operationId -> {"reads+": [...], "writes+": [...]}: the table the id or the description reaches, same module
LINEAGE = {
    # CHG-STO-019
    "listRentalProducts": {"reads+": ["rental.location_rule"]},
    "setMediaAssetTags": {"writes+": ["assets.media_asset"]},
    "signRentalAgreement": {"reads+": ["rental.booking"]},
    "skipRolloutCell": {"writes+": ["control.rollout_cell"]},
    "listEmployees": {"reads+": ["workforce.work_assignment"]},
    "listRetailReturns": {"reads+": ["retail.sale"]},
    "listSiteWaiverException": {"reads+": ["marketing.waiver_requirement"]},
    "listStoredForwardTransactions": {"reads+": ["payments.terminal"]},
    "getSuggestedRequisitions": {"reads+": ["inventory.location"]},
    "getSeatMapImport": {"reads+": ["seating.import_job"]},
    "getSeatInventory": {"reads+": ["seating.section_row"]},
    "deleteBanner": {"writes+": ["whitelabel.banner"]},
    "deleteContentPage": {"writes+": ["whitelabel.content_page"]},
    "getGuestMenu": {"reads+": ["fnb.menu"]},
    "getOutletStock": {"reads+": ["retail.merchandise"]},
    "searchMedia": {"reads+": ["assets.media_collection_member"]},
    "cancelMerchandiseReservation": {"writes+": ["retail.reservation"]},
    "collectMerchandiseReservation": {"writes+": ["retail.reservation"]},
    "listChangePropagationDependency": {"reads+": ["catalogue.change_request"]},
    "listChannelLogTransaction": {"reads+": ["catalogue.channel_incident"]},
    "getWaiverTesting": {"reads+": ["marketing.waiver_association"]},
    "listUnifiedInteractionCommunication": {"reads+": ["marketing.case"]},
    "listOrderReservation": {"reads+": ["orders.membership_renewal"]},
    "listPrivacyCompliance": {"reads+": ["marketing.segment"]},
    # CHG-STO-020
    "approveDevice": {"writes+": ["tenancy.device_audit"]},
    "checkoutCart": {"writes+": ["orders.deposit"]},
    "recordAuthorityNotification": {"writes+": ["maintenance.incident_authority_notification"]},
    "reportIncident": {"writes+": ["maintenance.incident_involved_party"]},
    "setAccessPointDirection": {"writes+": ["access.configuration_change", "access.gate_mode_change"]},
    "startSync": {"writes+": ["workforce.employee"]},
}
_REF = "type: string\nformat: uuid\nnullable: true\nreadOnly: true\n"
NEW_PROPS = [
    ("rental", "RentalDamageAssessment", "bookingId", _REF + "x-ticvai-references: rental.booking\n"
     "description: The rental booking assessed, from the path of `assessRentalDamage`."),
    ("rental", "RentalEquipmentAssignment", "bookingId", _REF + "x-ticvai-references: rental.booking\n"
     "description: The rental booking the equipment is assigned to, from the path of `assignRentalEquipment`."),
    ("rental", "RentalInspection", "bookingId", _REF + "x-ticvai-references: rental.booking\n"
     "description: The rental booking inspected, from the path of `recordRentalInspection`."),
    ("assets", "MediaRendition", "assetId", _REF + "x-ticvai-references: assets.media_asset\n"
     "description: The media asset this is a rendition of, from the path of `requestMediaRendition`."),
    ("rental", "RentalAgreementRules", "productId", _REF + "x-ticvai-references: rental.product\nx-ticvai-unique: tenant\n"
     "description: The rental product these rules are for (one set per product), from the path."),
    ("rental", "RentalAvailabilityRules", "productId", _REF + "x-ticvai-references: rental.product\nx-ticvai-unique: tenant\n"
     "description: The rental product these rules are for (one set per product), from the path."),
    ("rental", "RentalDurationRules", "productId", _REF + "x-ticvai-references: rental.product\nx-ticvai-unique: tenant\n"
     "description: The rental product these rules are for (one set per product), from the path."),
    ("rental", "RentalInventoryModel", "productId", _REF + "x-ticvai-references: rental.product\nx-ticvai-unique: tenant\n"
     "description: The rental product this model is for (one per product), from the path."),
    ("rental", "RentalOperationalRules", "productId", _REF + "x-ticvai-references: rental.product\nx-ticvai-unique: tenant\n"
     "description: The rental product these rules are for (one set per product), from the path."),
    ("rental", "RentalLocationRule", "productId", _REF + "x-ticvai-references: rental.product\n"
     "description: The rental product offered at this location, from the path of `setRentalProductLocations`."),
    ("resources", "ResourceVenueAssignment", "resourceId", _REF + "x-ticvai-references: resources.resource\n"
     "description: The resource assigned, from the path of `setResourceVenueAssignment`."),
    ("cross-region", "GuestLink", "localSubjectId", _REF + "x-ticvai-references: pii.subject\n"
     "description: The guest in this cell the link resolves to (`resolveGuestLink`); never sent to another cell."),
]
# operationId -> tables the description names to explain the operation, which it neither reads nor writes
NAMES_FOR_CONTEXT = {
    "askReportingQuestion": ["ai.knowledge_gap"],
    "runSemanticQuery": ["ai.knowledge_gap"],
    "authoriseWalletSpend": ["wallet.balance"],
    "createRentalAgreement": ["rental.agreement_signature"],
    "createTableReservation": ["orders.deposit"],
    "createWebhookSubscription": ["platform.outbox"],
    "getFnbServiceChargePolicy": ["rental.fee_policy"],
    "getLoyaltyRules": ["marketing.loyalty_programme"],
    "getPaymentRules": ["whitelabel.policy"],
    "getPdfPrintablePos": ["access.configuration_change"],
    "getPerformanceManifest": ["catalogue.performance"],
    "getResaleFeePolicy": ["orders.order_fee", "orders.resale_listing", "payments.fee_rule"],
    "issueInvitation": ["orders.sales_order"],
    "listDepositActivity": ["ledger.deposit", "orders.deposit"],
    "listDeposits": ["ledger.deposit"],
    "listDeviceConsents": ["pii.consent_identifier"],
    "listDevices": ["access.device_placement"],
    "listGuestDevices": ["platform.device"],
    "listIndexSources": ["catalogue.product"],
    "listLoyaltyPointEntries": ["marketing.loyalty_position"],
    "listMembershipProgrammes": ["catalogue.entitlement_template"],
    "listSlaPolicies": ["approvals.sla_policy"],
    "listStockReservations": ["rental.agreement_item"],
    "listWalletHolds": ["control.rollout", "seating.seat_reservation_item"],
    "placeAccessDevice": ["platform.device"],
    "publishPromotion": ["promotions.promotion_conflict"],
    "recordConsentIdentifier": ["marketing.device_consent", "platform.outbox"],
    "replayDeadLetter": ["platform.outbox"],
    "respondToInvitation": ["access.entitlement"],
    "setAiCredential": ["ai.activity"],
    "setFeeDefinition": ["catalogue.fee_rule", "orders.order_fee", "payments.fee_rule"],
    "setFnbReservationPolicy": ["fnb.service_charge_policy", "orders.order_fee"],
    "setGateOfflinePolicy": ["access.edge_package"],
    "setLeaderboardNickname": ["pii.subject"],
    "setResaleMarketplaceConfig": ["orders.resale_eligibility_rule", "orders.resale_fee_policy"],
    "setTurnstileMode": ["access.configuration_change"],
    "transferOrderItems": ["orders.order_line"],
    "updateAccessDevicePlacement": ["platform.device"],
    "updateGuestSubjectDetails": ["platform.outbox"],
    "updateTransportDeparture": ["catalogue.channel_capacity"],
    "verifyAccreditationCredential": ["access.accreditation_credential"],
    "verifyCustomDomain": ["control.tenant_domain"],
}
# (contract stem, drafted request schema, the table its operation writes, the other tables it writes)
DRAFTED = [
    ('access', 'AccessAreaZoneBuilderInput', 'access.access_area', ['access.configuration_change']),  # setAccessAreaZone
    ('access', 'AccessControlGraphicalMapDesignerInput', 'access.access_map', ['access.configuration_change']),  # setAccessGraphicalMap
    ('access', 'AppleWalletPassDesignerInput', 'access.media_template', ['access.configuration_change']),  # setAppleWalletPass
    ('access', 'AttractionAccessConfigurationInput', 'access.attraction_access', ['access.configuration_change']),  # setAttractionAccess
    ('access', 'BiometricVerificationProfileBuilderInput', 'access.biometric_profile', ['access.configuration_change']),  # setBiometricVerificationProfile
    ('access', 'BleBeaconGeofenceConfigurationInput', 'access.access_point', ['access.configuration_change', 'access.device_placement']),  # setBleBeaconGeofence
    ('access', 'ContextTimeEventCapacityPolicyBuilderInput', 'access.dynamic_policy', ['access.configuration_change', 'access.dynamic_policy_version']),  # setContextTimeEvent
    ('access', 'DeviceSoftwareContentRemoteConfigurationInput', 'access.device_configuration', ['access.configuration_change']),  # setDeviceSoftwareContent
    ('access', 'DigitalCardMembershipWearableDesignerInput', 'access.media_template', ['access.configuration_change']),  # setDigitalCardMembership
    ('access', 'DigitalQrBarcodeTicketDesignerInput', 'access.media_template', ['access.configuration_change']),  # setDigitalBarcodeTicket
    ('access', 'DynamicFieldsDataMappingContentBuilderInput', 'access.dynamic_field', ['access.configuration_change']),  # setDynamicFieldData
    ('access', 'DynamicQrSecurityProfileBuilderInput', 'access.credential_security_profile', ['access.configuration_change']),  # setDynamicSecurityProfile
    ('access', 'EdgeNodeLocalProcessingConfigurationInput', 'access.edge_node', ['access.configuration_change']),  # setEdgeNodeLocal
    ('access', 'EmbeddedEntitlementPayloadDesignerInput', 'access.credential_security_profile', ['access.configuration_change']),  # setEmbeddedEntitlementPayload
    ('access', 'FacePassEnrollmentConfigurationInput', 'access.biometric_profile', ['access.configuration_change']),  # setFacePassEnrollment
    ('access', 'GateLaneConfigurationInput', 'access.gate_lane', ['access.configuration_change']),  # setGateLane
    ('access', 'GoogleWalletPassDesignerInput', 'access.media_template', ['access.configuration_change']),  # setGoogleWalletPass
    ('access', 'GroupB2bAdmissionProfileBuilderInput', 'access.group_admission_rule', ['access.configuration_change']),  # setGroupAdmissionProfile
    ('access', 'HandheldMobileAccessDeviceConfigurationInput', 'access.device_configuration', ['access.configuration_change']),  # setHandheldMobileAccess
    ('access', 'ManualOverrideSupervisorApprovalInput', 'access.scan_event', []),  # approveManualOverrideSupervisor
    ('access', 'MediaBindingActivationAssignmentOperationsInput', 'access.credential_binding', ['access.credential_event']),  # setMediaBindingActivation
    ('access', 'MediaCompatibilityTestingPublicationInput', 'access.media_compatibility_test', []),  # publishMediaCompatibilityTesting
    ('access', 'MultiMediaPreviewTestingApprovalPublicationInput', 'access.media_template', ['access.configuration_change', 'access.media_template_version']),  # approveMultiMediaPreview
    ('access', 'OperationalIncidentExceptionWorkspaceInput', 'access.access_incident', []),  # setOperationalIncidentException
    ('access', 'ReaderScannerPeripheralConfigurationInput', 'access.access_point_configuration', ['access.configuration_change']),  # setReaderScannerPeripheral
    ('access', 'RealTimeSecurityResponsePlaybookBuilderInput', 'access.security_playbook', ['access.configuration_change']),  # setRealTimeSecurity
    ('access', 'RfidNfcCardWristbandMediaDesignerInput', 'access.media_template', ['access.configuration_change']),  # setRfidNfcCard
    ('access', 'RfidNfcConfigurationInput', 'access.media_encoding_profile', ['access.configuration_change']),  # setRfidNfc
    ('access', 'RuleSimulationConflictCheckPublicationInput', 'access.configuration_version', ['access.configuration_change']),  # publishRuleConflictCheck
    ('access', 'SecurityInvestigationEvidenceWorkspaceInput', 'access.security_investigation', []),  # setSecurityInvestigationEvidence
    ('access', 'TopologyValidationPublicationInput', 'access.configuration_version', ['access.configuration_change', 'access.hardware_deployment']),  # publishTopologyValidation
    ('access', 'TurnstileLaneBehaviorConfigurationInput', 'access.access_point_configuration', ['access.configuration_change']),  # setTurnstileLaneBehavior
    ('access', 'ValidationOutcomeGuestFeedbackDesignerInput', 'access.gate_outcome_profile', ['access.configuration_change']),  # setValidationOutcomeGuest
    ('access', 'VirtualTicketIdentityMasterRecordConfigurationInput', 'access.credential_policy', ['access.configuration_change']),  # setVirtualTicketIdentity
    ('access', 'VisualAccessRuleBuilderInput', 'access.admission_rules', ['access.configuration_change', 'access.entry_rule_point']),  # setVisualAccessRule
    ('access', 'VisualDynamicPolicyBuilderInput', 'access.dynamic_policy', ['access.configuration_change', 'access.dynamic_policy_version']),  # setVisualDynamicPolicy
    ('approvals', 'UnifiedApprovalInboxDecisionWorkspaceInput', 'approvals.decision', ['approvals.request', 'platform.outbox']),  # approveUnifiedDecision
    ('catalogue', 'ABPricingExperimentStudioInput', 'catalogue.pricing_experiment', ['catalogue.audit_entry']),  # setPricingExperiment
    ('catalogue', 'AiCatalogueBuilderConfigurationReviewInput', 'catalogue.ai_catalogue_session', ['catalogue.audit_entry', 'catalogue.product']),  # setCatalogueReview
    ('catalogue', 'ApprovalReviewDecisionWorkspaceInput', 'catalogue.change_request', ['catalogue.audit_entry']),  # approveReviewDecision
    ('catalogue', 'ApprovalWorkflowDesignerInput', 'catalogue.approval_policy', ['catalogue.audit_entry']),  # approveWorkflow
    ('catalogue', 'BookingVelocityTimeToEventRuleBuilderInput', 'pricing.dynamic_price_action', ['catalogue.audit_entry', 'pricing.dynamic_price_condition', 'pricing.dynamic_price_rule']),  # setBookingVelocityTime
    ('catalogue', 'ChannelCreationProfileConfigurationInput', 'catalogue.sales_channel', ['catalogue.audit_entry']),  # createChannelProfile
    ('catalogue', 'ChannelFeesPaymentFulfillmentConfigurationInput', 'catalogue.sales_channel', ['catalogue.audit_entry']),  # setChannelFeePayment
    ('catalogue', 'ChannelPricingCommercialProfileAssignmentInput', 'catalogue.price_assignment', ['catalogue.audit_entry']),  # setChannelPricingCommercial
    ('catalogue', 'ChannelPublicationAvailabilityInput', 'catalogue.product', ['catalogue.audit_entry', 'catalogue.product_channel_assignment']),  # publishChannelAvailability
    ('catalogue', 'ChannelPublicationReadinessAiValidationInput', 'catalogue.sales_channel', ['catalogue.audit_entry']),  # publishChannelReadinessValidation
    ('catalogue', 'DemandOccupancyAvailabilityRuleBuilderInput', 'pricing.dynamic_price_action', ['catalogue.audit_entry', 'pricing.dynamic_price_condition', 'pricing.dynamic_price_rule']),  # setDemandOccupancyAvailability
    ('catalogue', 'DynamicPricingStrategyBuilderInput', 'catalogue.dynamic_pricing_strategy', ['catalogue.audit_entry']),  # setDynamicPricingStrategy
    ('catalogue', 'FeeApplicabilityChargingRuleBuilderInput', 'catalogue.fee_rule', ['catalogue.audit_entry']),  # setFeeApplicabilityCharging
    ('catalogue', 'LifecycleStatusWorkflowConfigurationInput', 'catalogue.lifecycle_workflow', ['catalogue.audit_entry']),  # setLifecycleStatuWorkflow
    ('catalogue', 'LiveDynamicPriceExecutionDeploymentMonitorInput', 'catalogue.price', ['catalogue.audit_entry', 'catalogue.price_execution', 'catalogue.pricing_recommendation_decision', 'platform.outbox']),  # createLiveDynamicPrice
    ('catalogue', 'PriceHierarchyInheritanceConfigurationInput', 'catalogue.price_resolution_policy', ['catalogue.audit_entry']),  # setPriceHierarchyInheritance
    ('catalogue', 'PricingApprovalWorkflowAuthorityMatrixInput', 'catalogue.approval_policy', ['catalogue.audit_entry']),  # approvePricingWorkflowAuthority
    ('catalogue', 'PricingChangeRequestWorkspaceInput', 'catalogue.change_request', ['catalogue.audit_entry', 'catalogue.change_request_line']),  # setPricingChangeRequest
    ('catalogue', 'PricingPublicationEffectiveDateSchedulerInput', 'catalogue.change_request', ['catalogue.audit_entry', 'catalogue.price_list_version', 'catalogue.pricing_publication', 'catalogue.pricing_publication_target', 'platform.outbox']),  # publishPricingEffectiveDate
    ('catalogue', 'PricingSimulationStudioInput', 'catalogue.pricing_recommendation', ['catalogue.pricing_simulation']),  # setPricing
    ('catalogue', 'ProductCatalogueAssignmentInput', 'catalogue.product', ['catalogue.audit_entry', 'catalogue.product_channel_assignment']),  # setProductCatalogue
    ('catalogue', 'ProductContextOwnershipAssignmentInput', 'catalogue.product', ['catalogue.audit_entry']),  # setProductContextOwnership
    ('catalogue', 'ProductServicePriceAssignmentInput', 'catalogue.price_assignment', ['catalogue.audit_entry']),  # setProductServicePrice
    ('catalogue', 'PublicationActivationSchedulerInput', 'catalogue.lifecycle_action', ['catalogue.audit_entry']),  # publishActivationScheduler
    ('catalogue', 'TaxProfileJurisdictionConfigurationInput', 'catalogue.tax_profile', ['catalogue.audit_entry']),  # setTaxProfileJurisdiction
    ('catalogue', 'TaxRuleTreatmentBuilderInput', 'catalogue.tax_rule', ['catalogue.audit_entry']),  # setTaxRuleTreatment
    ('orders', 'CustomerGuestAccountAssignmentInput', 'orders.reservation', ['orders.sales_order']),  # setCustomerGuestAccount
    ('orders', 'ListingCreationSellerConfigurationInput', 'orders.resale_listing', []),  # createListingSeller
]



def drafted_text(table, others):
    more = (" (with " + ", ".join(f"`{t}`" for t in others) + ")") if others else ""
    return (f"none — request only; applied to `{table}`{more}, the table its operation writes (CHG-STO-021); a field "
            f"with no column there is a working input of the screen and is not kept")


def main() -> int:
    apply = "--apply" in sys.argv
    tic = Path(__file__).resolve().parents[2]
    sys.path.insert(0, str(tic / "tools"))
    import audit_guard as g
    ops = g.operations()
    c = Contracts(tic)
    n, bad = 0, 0
    for oid, p, col in PARAM_COLUMN:
        try:
            n += c.set_param_marker(ops[oid]["contract"], oid, p, "x-ticvai-column", col) != "="
        except (LookupError, KeyError) as e:
            print("  !", oid, p, e)
            bad += 1
    for stem, schema, prop, block in NEW_PROPS:
        try:
            n += c.add_property(stem, schema, prop, block) != "="
        except LookupError as e:
            print("  !", e)
            bad += 1
    for oid, tables in NAMES_FOR_CONTEXT.items():
        try:
            o = ops[oid]
            n += c.set_op_list(o["contract"], oid, "x-ticvai-names-for-context", tables) != "="
        except (LookupError, KeyError) as e:
            print("  !", oid, e)
            bad += 1
    for stem, schema, table, others in DRAFTED:
        try:
            n += c.set_persistence(stem, schema, drafted_text(table, others)) != "="
        except LookupError as e:
            print("  !", e)
            bad += 1
    print(f"  {n} contract edit(s), {bad} not found")
    lp = tic / "handoff" / "api-data-lineage.json"
    raw = lp.read_text(encoding="utf-8")
    lin = json.loads(raw)
    m = 0
    for oid, ch in LINEAGE.items():
        e = lin.get(oid)
        if e is None:
            print("  ! lineage has no", oid)
            bad += 1
            continue
        for k in ("reads", "writes"):
            if ch.get(k + "+"):
                new = sorted(set(e.get(k) or []) | set(ch[k + "+"]))
                if new != sorted(e.get(k) or []):
                    e[k] = new
                    m += 1
    print(f"  {m} lineage entr(ies) changed")
    if apply and not bad:
        print("  wrote", ", ".join(c.save()) or "nothing")
        if m:
            indent = 1 if raw.startswith("{\n ") else None
            lp.write_text(json.dumps(lin, indent=indent, ensure_ascii=False) + ("\n" if raw.endswith("\n") else ""),
                          encoding="utf-8")
    elif not apply:
        print("dry run; pass --apply")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
