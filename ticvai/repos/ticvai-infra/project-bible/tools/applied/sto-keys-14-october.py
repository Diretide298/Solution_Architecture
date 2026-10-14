#!/usr/bin/env python3
"""One-off, batch STO (Block A storage audit, 14 October 2026): every NOT NULL key into its own database that was a
naming convention is declared on its contract field (`x-ticvai-references`), and the ten keys the name rule guessed into
another module are declared to the right table or refused (`none`). Already applied; kept as the record. Idempotent.

* CHG-STO-001 (check-storage-promises SP-KEY-UNDECLARED, 389 at audit-base b93b5a87, and SP-KEY-TENANT-FALLBACK, 45):
  as CHG-DDL-004 settled CR-069 and CHG-CNS-002 settled CR-090, a key is declared so 900 has its foreign key and 920
  can scope a child through its parent. The convention target is kept where it names the table the field means; where
  the name rule picked the wrong one the target is corrected (`OVERRIDE` in the generator of this list, recorded in
  the entry's notes): a media file is `assets.media_asset`, not `maintenance.asset`; a product a recommendation or a
  relationship points at is `catalogue.product`, not the recommendation table itself; a plan's tier is
  `subscription.plan` (`/plans/{planId}/tiers`); an entitlement's template is `catalogue.entitlement_template`; a
  waiver signature's template is the waiver's `marketing.form_definition`; an outbox or inbox `event_id` is the
  envelope's id, not `catalogue.event`. `none` says a field is not a key at all: a `tenant_id` in a tenant database
  (the database is the tenant, ADR-0038), an id held in another cell or another system, a node of a workflow
  version's graph, a target product whose module `targetService` names.
* CHG-STO-002 (SP-KEY-GUESSED, 10): `deposit_authorisation_id` is `orders.stored_value_authorisation` (CF-126), not
  `games.authorisation`; a tax exemption's evidence is an uploaded `assets.media_asset`; an external reference's
  merchant is `payments.merchant_account`; a workflow node, a venue-map zone, an attraction and a membership
  benefit's central pricing rule name no table here and are `none`. `pii.subject.erasure_request_id` is a storage-only
  column (no contract field): it is declared in tools/derive-schema.py `STORAGE_REFERENCES`, with
  `wallet.wallet_transaction.subject_id`.

    python3 tools/applied/sto-keys-14-october.py [--apply]
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from sto_markers import Contracts  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
TIC = ROOT / "ticvai" if (ROOT / "ticvai").is_dir() else ROOT.parent if (ROOT.parent / "contracts").is_dir() else ROOT

# (contract stem, schema, property path, target table or none)  # the column it stores
REFERENCES = [
    ('access', 'AccessAccessChange', 'newAccessId', 'access.entitlement'),  # access.access_change.new_access_id
    ('access', 'AccessAccessChange', 'oldAccessId', 'access.entitlement'),  # access.access_change.old_access_id
    ('access', 'AccessAccessIncident', 'venueId', 'platform.scope'),  # access.access_incident.venue_id
    ('access', 'AccessAccessMap', 'mapId', 'venuemap.map'),  # access.access_map.map_id
    ('access', 'AccessAccessMap', 'venueId', 'platform.scope'),  # access.access_map.venue_id
    ('access', 'AccessAccessPointConfiguration', 'accessPointId', 'access.access_point'),  # access.access_point_configuration.access_point_id
    ('access', 'AccessAccessPointConfiguration', 'venueId', 'platform.scope'),  # access.access_point_configuration.venue_id
    ('access', 'AccessAccessPointGroup', 'venueId', 'platform.scope'),  # access.access_point_group.venue_id
    ('access', 'AccessAccreditationCredential', 'holderId', 'accreditation.holder'),  # access.accreditation_credential.holder_id
    ('access', 'AccessAttractionAccess', 'attractionId', 'none'),  # access.attraction_access.attraction_id
    ('access', 'AccessAttractionAccess', 'venueId', 'platform.scope'),  # access.attraction_access.venue_id
    ('access', 'AccessBiometricAuditEvent', 'venueId', 'platform.scope'),  # access.biometric_audit_event.venue_id
    ('access', 'AccessBiometricProfile', 'venueId', 'platform.scope'),  # access.biometric_profile.venue_id
    ('access', 'AccessBrandingProfile', 'scopeId', 'platform.scope'),  # access.branding_profile.scope_id
    ('access', 'AccessCompanionRule', 'venueId', 'platform.scope'),  # access.companion_rule.venue_id
    ('access', 'AccessConfigurationChange', 'changedByPrincipalId', 'identity.principal'),  # access.configuration_change.changed_by_principal_id
    ('access', 'AccessCredentialBinding', 'entitlementId', 'access.entitlement'),  # access.credential_binding.entitlement_id
    ('access', 'AccessCredentialBinding', 'mediaTypeId', 'access.media_type'),  # access.credential_binding.media_type_id
    ('access', 'AccessCredentialDelivery', 'entitlementId', 'access.entitlement'),  # access.credential_delivery.entitlement_id
    ('access', 'AccessCredentialEvent', 'entitlementId', 'access.entitlement'),  # access.credential_event.entitlement_id
    ('access', 'AccessCredentialIssuance', 'entitlementId', 'access.entitlement'),  # access.credential_issuance.entitlement_id
    ('access', 'AccessCredentialIssuance', 'mediaTypeId', 'access.media_type'),  # access.credential_issuance.media_type_id
    ('access', 'AccessCredentialSharingCase', 'entitlementId', 'access.entitlement'),  # access.credential_sharing_case.entitlement_id
    ('access', 'AccessDeviceBinding', 'deviceId', 'platform.device'),  # access.device_binding.device_id
    ('access', 'AccessDeviceBinding', 'entitlementId', 'access.entitlement'),  # access.device_binding.entitlement_id
    ('access', 'AccessDeviceConfiguration', 'venueId', 'platform.scope'),  # access.device_configuration.venue_id
    ('access', 'AccessDevicePlacement', 'venueId', 'platform.scope'),  # access.device_placement.venue_id
    ('access', 'AccessDynamicPolicyVersion', 'dynamicPolicyId', 'access.dynamic_policy'),  # access.dynamic_policy_version.dynamic_policy_id
    ('access', 'AccessEdgeNode', 'venueId', 'platform.scope'),  # access.edge_node.venue_id
    ('access', 'AccessEdgePackage', 'venueId', 'platform.scope'),  # access.edge_package.venue_id
    ('access', 'AccessEntryRulePoint', 'accessPointId', 'access.access_point'),  # access.entry_rule_point.access_point_id
    ('access', 'AccessFaceReenrolmentAttempt', 'subjectId', 'pii.subject'),  # access.face_reenrolment_attempt.subject_id
    ('access', 'AccessFaceReenrolmentAttempt', 'venueId', 'platform.scope'),  # access.face_reenrolment_attempt.venue_id
    ('access', 'AccessGateLane', 'accessPointId', 'access.access_point'),  # access.gate_lane.access_point_id
    ('access', 'AccessGateLane', 'venueId', 'platform.scope'),  # access.gate_lane.venue_id
    ('access', 'AccessGateModeChange', 'accessPointId', 'access.access_point'),  # access.gate_mode_change.access_point_id
    ('access', 'AccessGateModeChange', 'changedByPrincipalId', 'identity.principal'),  # access.gate_mode_change.changed_by_principal_id
    ('access', 'AccessGateModeChange', 'venueId', 'platform.scope'),  # access.gate_mode_change.venue_id
    ('access', 'AccessGateModePolicy', 'venueId', 'platform.scope'),  # access.gate_mode_policy.venue_id
    ('access', 'AccessGateOutcomeProfile', 'venueId', 'platform.scope'),  # access.gate_outcome_profile.venue_id
    ('access', 'AccessGroupAdmissionRule', 'venueId', 'platform.scope'),  # access.group_admission_rule.venue_id
    ('access', 'AccessHardwareCertification', 'modelId', 'access.hardware_model'),  # access.hardware_certification.model_id
    ('access', 'AccessIdentityLock', 'subjectId', 'pii.subject'),  # access.identity_lock.subject_id
    ('access', 'AccessMediaCompatibilityTest', 'mediaTypeId', 'access.media_type'),  # access.media_compatibility_test.media_type_id
    ('access', 'AccessMediaCompatibilityTest', 'venueId', 'platform.scope'),  # access.media_compatibility_test.venue_id
    ('access', 'AccessMediaTemplateVersion', 'mediaTemplateId', 'access.media_template'),  # access.media_template_version.media_template_id
    ('access', 'AccessOfflinePolicy', 'venueId', 'platform.scope'),  # access.offline_policy.venue_id
    ('access', 'AccessOperatingCalendarEntry', 'venueId', 'platform.scope'),  # access.operating_calendar_entry.venue_id
    ('access', 'AccessPodium', 'venueId', 'platform.scope'),  # access.podium.venue_id
    ('access', 'AccessPodiumShift', 'operatorPrincipalId', 'identity.principal'),  # access.podium_shift.operator_principal_id
    ('access', 'AccessPodiumShift', 'venueId', 'platform.scope'),  # access.podium_shift.venue_id
    ('access', 'AccessPolicyScopeAssignment', 'dynamicPolicyId', 'access.dynamic_policy'),  # access.policy_scope_assignment.dynamic_policy_id
    ('access', 'AccessPolicyScopeAssignment', 'scopeId', 'platform.scope'),  # access.policy_scope_assignment.scope_id
    ('access', 'AccessVerificationMethodPolicy', 'productId', 'catalogue.product'),  # access.verification_method_policy.product_id
    ('access', 'CredentialIssuanceRetryPolicyView', 'venueId', 'platform.scope'),  # access.credential_issuance_retry_policy.venue_id
    ('access', 'Entitlement', 'templateId', 'catalogue.entitlement_template'),  # access.entitlement.template_id
    ('accreditation', 'AccreditationApplication', 'programmeId', 'accreditation.programme'),  # accreditation.application.programme_id
    ('accreditation', 'AccreditationCredential', 'holderId', 'accreditation.holder'),  # accreditation.credential.holder_id
    ('accreditation', 'AccreditationCredentialDelivery', 'credentialId', 'accreditation.credential'),  # accreditation.mobile_credential_delivery.credential_id
    ('accreditation', 'AccreditationDocument', 'assetId', 'assets.media_asset'),  # accreditation.document.asset_id
    ('ai', 'AiByokEnablement', 'tenantId', 'none'),  # ai.byok_enablement.tenant_id
    ('ai', 'AiGuidedChoiceSuggestion', 'venueId', 'platform.scope'),  # ai.guided_choice_suggestion.venue_id
    ('ai', 'AiHistoryImport', 'venueId', 'platform.scope'),  # ai.history_import.venue_id
    ('ai', 'AiHistoryObservation', 'venueId', 'platform.scope'),  # ai.history_observation.venue_id
    ('ai', 'SuggestionOutcome', 'suggestionId', 'ai.suggestion'),  # ai.suggestion_outcome.suggestion_id
    ('approvals', 'ApprovalExternalDispatch', 'providerId', 'approvals.external_provider'),  # approvals.external_dispatch.provider_id
    ('approvals', 'ApprovalExternalDispatch', 'requestId', 'approvals.request'),  # approvals.external_dispatch.request_id
    ('approvals', 'ApprovedActionExecutionView', 'approvalRequestId', 'approvals.request'),  # approvals.approved_action_execution.approval_request_id
    ('approvals', 'AutomationExecution', 'automationId', 'approvals.automation'),  # approvals.automation_execution.automation_id
    ('approvals', 'WorkflowException', 'workflowInstanceId', 'approvals.workflow_instance'),  # approvals.workflow_exception.workflow_instance_id
    ('approvals', 'WorkflowInstance', 'currentNodeId', 'none'),  # approvals.workflow_instance.current_node_id
    ('approvals', 'WorkflowInstance', 'workflowDefinitionId', 'approvals.workflow_definition'),  # approvals.workflow_instance.workflow_definition_id
    ('approvals', 'WorkflowInstance', 'workflowVersionId', 'approvals.workflow_version'),  # approvals.workflow_instance.workflow_version_id
    ('approvals', 'WorkflowIntervention', 'actorPrincipalId', 'identity.principal'),  # approvals.workflow_intervention.actor_principal_id
    ('approvals', 'WorkflowIntervention', 'alternativeNodeId', 'none'),  # approvals.workflow_intervention.alternative_node_id
    ('approvals', 'WorkflowIntervention', 'workflowInstanceId', 'approvals.workflow_instance'),  # approvals.workflow_intervention.workflow_instance_id
    ('approvals', 'WorkflowStepExecution', 'workflowInstanceId', 'approvals.workflow_instance'),  # approvals.workflow_step_execution.workflow_instance_id
    ('approvals', 'WorkflowTrigger', 'workflowDefinitionId', 'approvals.workflow_definition'),  # approvals.workflow_trigger.workflow_definition_id
    ('approvals', 'WorkflowVersion', 'workflowDefinitionId', 'approvals.workflow_definition'),  # approvals.workflow_version.workflow_definition_id
    ('assets', 'MediaCollectionMember', 'assetId', 'assets.media_asset'),  # assets.media_collection_member.asset_id
    ('assets', 'MediaCollectionMember', 'collectionId', 'assets.media_collection'),  # assets.media_collection_member.collection_id
    ('catalogue', 'CatalogueChangeRequest', 'requestedByPrincipalId', 'identity.principal'),  # catalogue.change_request.requested_by_principal_id
    ('catalogue', 'CataloguePlanBenefit', 'entitlementTemplateId', 'catalogue.entitlement_template'),  # catalogue.plan_benefit.entitlement_template_id
    ('catalogue', 'CataloguePlanBenefit', 'membershipBenefitId', 'catalogue.membership_benefit'),  # catalogue.plan_benefit.membership_benefit_id
    ('catalogue', 'CatalogueRollbackAction', 'requestedByPrincipalId', 'identity.principal'),  # catalogue.rollback_action.requested_by_principal_id
    ('catalogue', 'ChannelConnection', 'salesChannelId', 'catalogue.sales_channel'),  # catalogue.channel_connection.sales_channel_id
    ('catalogue', 'ChannelIncident', 'salesChannelId', 'catalogue.sales_channel'),  # catalogue.channel_incident.sales_channel_id
    ('catalogue', 'ChannelSalesRule', 'salesChannelId', 'catalogue.sales_channel'),  # catalogue.channel_sales_rule.sales_channel_id
    ('catalogue', 'ChannelSync', 'salesChannelId', 'catalogue.sales_channel'),  # catalogue.channel_sync.sales_channel_id
    ('catalogue', 'LifecycleAction', 'productId', 'catalogue.product'),  # catalogue.lifecycle_action.product_id
    ('catalogue', 'PackagePricing', 'productId', 'catalogue.product'),  # catalogue.package_pricing.product_id
    ('catalogue', 'PerformanceMediaAssignment', 'assetId', 'assets.media_asset'),  # catalogue.performance_media.asset_id
    ('catalogue', 'PerformanceMediaAssignment', 'participantId', 'catalogue.event_registration'),  # catalogue.performance_media.participant_id
    ('catalogue', 'PerformanceMediaAssignment', 'performanceId', 'catalogue.performance'),  # catalogue.performance_media.performance_id
    ('catalogue', 'PriceAssignment', 'priceListId', 'catalogue.price_list'),  # catalogue.price_assignment.price_list_id
    ('catalogue', 'PriceLadder', 'dynamicPricingStrategyId', 'catalogue.dynamic_pricing_strategy'),  # catalogue.price_ladder.dynamic_pricing_strategy_id
    ('catalogue', 'PriceListRate', 'priceCategoryId', 'catalogue.price_category'),  # catalogue.rate.price_category_id
    ('catalogue', 'PriceListRate', 'priceListId', 'catalogue.price_list'),  # catalogue.rate.price_list_id
    ('catalogue', 'PriceListVersion', 'priceListId', 'catalogue.price_list'),  # catalogue.price_list_version.price_list_id
    ('catalogue', 'PricingDynamicPriceAction', 'dynamicPriceRuleId', 'pricing.dynamic_price_rule'),  # pricing.dynamic_price_action.dynamic_price_rule_id
    ('catalogue', 'PricingDynamicPriceCondition', 'dynamicPriceRuleId', 'pricing.dynamic_price_rule'),  # pricing.dynamic_price_condition.dynamic_price_rule_id
    ('catalogue', 'PricingPublication', 'changeRequestId', 'catalogue.change_request'),  # catalogue.pricing_publication.change_request_id
    ('catalogue', 'PricingRecommendationDecision', 'decidedByPrincipalId', 'identity.principal'),  # catalogue.pricing_recommendation_decision.decided_by_principal_id
    ('catalogue', 'PricingRecommendationDecision', 'recommendationId', 'catalogue.pricing_recommendation'),  # catalogue.pricing_recommendation_decision.recommendation_id
    ('catalogue', 'ProductChannelAssignment', 'productId', 'catalogue.product'),  # catalogue.product_channel_assignment.product_id
    ('catalogue', 'ProductLink', 'sourceProductId', 'catalogue.product'),  # catalogue.product_link.source_product_id
    ('catalogue', 'ProductVersion', 'publishedByPrincipalId', 'identity.principal'),  # catalogue.product_version.published_by_principal_id
    ('catalogue', 'SeatPricingRule', 'seatMapId', 'seating.seat_map'),  # catalogue.seat_pricing_rule.seat_map_id
    ('catalogue', 'Space', 'venueMapZoneId', 'none'),  # catalogue.space.venue_map_zone_id
    ('catalogue', 'TaxProfile', 'taxCodeId', 'ledger.tax_code'),  # catalogue.tax_profile.tax_code_id
    ('catalogue', 'WaitingRoomSetting', 'venueId', 'platform.scope'),  # catalogue.waiting_room_setting.venue_id
    ('cross-region', 'SyncCrossCellRequest', 'guestLinkId', 'sync.guest_link'),  # sync.cross_cell_request.guest_link_id
    ('cross-region', 'WalletAuthorisation', 'authorisationId', 'none'),  # sync.wallet_authorisation.authorisation_id
    ('finance', 'FinCreditMemo', 'legalEntityId', 'ledger.legal_entity'),  # ledger.credit_memo.legal_entity_id
    ('finance', 'FinCreditMemo', 'taxInvoiceId', 'ledger.tax_invoice'),  # ledger.credit_memo.tax_invoice_id
    ('finance', 'FinEInvoiceTransmission', 'legalEntityId', 'ledger.legal_entity'),  # ledger.einvoice_transmission.legal_entity_id
    ('finance', 'FinEInvoicingProvider', 'legalEntityId', 'ledger.legal_entity'),  # ledger.einvoicing_provider.legal_entity_id
    ('finance', 'FinTaxInvoice', 'legalEntityId', 'ledger.legal_entity'),  # ledger.tax_invoice.legal_entity_id
    ('finance', 'FinTaxInvoiceTemplate', 'legalEntityId', 'ledger.legal_entity'),  # ledger.tax_invoice_template.legal_entity_id
    ('finance', 'FiscalPeriod', 'events[].principalId', 'identity.principal'),  # ledger.fiscal_period_event.principal_id
    ('finance', 'InterEntityObligation', 'fromLegalEntityId', 'ledger.legal_entity'),  # ledger.inter_entity_obligation.from_legal_entity_id
    ('finance', 'InterEntityObligation', 'toLegalEntityId', 'ledger.legal_entity'),  # ledger.inter_entity_obligation.to_legal_entity_id
    ('finance', 'JournalEntry', 'lines[].accountId', 'ledger.account'),  # ledger.journal_line.account_id
    ('finance', 'TaxExemption', 'evidenceDocumentId', 'assets.media_asset'),  # ledger.tax_exemption.evidence_document_id
    ('fnb', 'AllergenVerdict', 'menuItemId', 'fnb.menu_item'),  # fnb.allergen_verdict.menu_item_id
    ('fnb', 'ComboSlot', 'options[].menuItemId', 'fnb.menu_item'),  # fnb.combo_slot_option.menu_item_id
    ('fnb', 'EightySixEvent', 'menuItemId', 'fnb.menu_item'),  # fnb.sold_out_item.menu_item_id
    ('fnb', 'FnbDeliveryPolicy', 'outletId', 'platform.outlet'),  # fnb.delivery_policy.outlet_id
    ('fnb', 'FnbIngredientSubstitute', 'fromInventoryItemId', 'inventory.inventory_item'),  # fnb.ingredient_substitute.from_inventory_item_id
    ('fnb', 'FnbIngredientSubstitute', 'toInventoryItemId', 'inventory.inventory_item'),  # fnb.ingredient_substitute.to_inventory_item_id
    ('fnb', 'FnbMenuItemModifier', 'groupId', 'fnb.modifier_group'),  # fnb.menu_item_modifier.group_id
    ('fnb', 'FnbMenuItemModifier', 'itemId', 'fnb.menu_item'),  # fnb.menu_item_modifier.item_id
    ('fnb', 'FnbOrder', 'lines[].menuItemId', 'fnb.menu_item'),  # fnb.service_order_line.menu_item_id
    ('fnb', 'FnbProductRecommendation', 'sourceProductId', 'catalogue.product'),  # fnb.product_recommendation.source_product_id
    ('fnb', 'FnbProductRecommendation', 'targetProductId', 'none'),  # fnb.product_recommendation.target_product_id
    ('fnb', 'FnbReservationTable', 'reservationId', 'fnb.table_reservation'),  # fnb.reservation_table.reservation_id
    ('fnb', 'KitchenRoutingRules', 'defaultStationId', 'fnb.kitchen_station'),  # fnb.kitchen_routing_rule.default_station_id
    ('fnb', 'KitchenSla', 'outletId', 'platform.outlet'),  # fnb.kitchen_sla.outlet_id
    ('fnb', 'KitchenTicket', 'orderId', 'fnb.service_order'),  # fnb.kitchen_ticket.order_id
    ('fnb', 'MenuSchedule', 'menuId', 'fnb.menu'),  # fnb.menu_schedule.menu_id
    ('fnb', 'MenuVersion', 'menuId', 'fnb.menu'),  # fnb.menu_version.menu_id
    ('fnb', 'ProductionPlan', 'lines[].itemId', 'fnb.menu_item'),  # fnb.production_plan_line.item_id
    ('fnb', 'SubBill', 'visitId', 'fnb.table_visit'),  # fnb.sub_bill.visit_id
    ('fnb', 'SubstitutionRule', 'fromIngredientId', 'fnb.recipe_ingredient'),  # fnb.substitution_rule.from_ingredient_id
    ('fnb', 'SubstitutionRule', 'recipeId', 'fnb.recipe'),  # fnb.substitution_rule.recipe_id
    ('fnb', 'SubstitutionRule', 'toIngredientId', 'fnb.recipe_ingredient'),  # fnb.substitution_rule.to_ingredient_id
    ('games', 'GamePricingException', 'gameId', 'games.game'),  # games.pricing_exception.game_id
    ('games', 'Reader', 'deviceId', 'platform.device'),  # games.reader.device_id
    ('games', 'ReaderOfflineQueue', 'readerId', 'games.reader'),  # games.reader_sync_status.reader_id
    ('identity', 'GuestCredential', 'subjectId', 'pii.subject'),  # identity.guest_credential.subject_id
    ('identity', 'IdentityBenefitUsage', 'customerMembershipId', 'identity.customer_membership'),  # identity.benefit_usage.customer_membership_id
    ('identity', 'IdentityBenefitUsage', 'membershipBenefitId', 'catalogue.membership_benefit'),  # identity.benefit_usage.membership_benefit_id
    ('identity', 'IdentityCustomerMembership', 'entitlementTemplateId', 'catalogue.entitlement_template'),  # identity.customer_membership.entitlement_template_id
    ('identity', 'IdentityGuestVerification', 'subjectId', 'pii.subject'),  # identity.guest_identity_verification.subject_id
    ('identity', 'IdentityMembershipHistory', 'customerMembershipId', 'identity.customer_membership'),  # identity.membership_history.customer_membership_id
    ('identity', 'IdentityPermission', 'moduleId', 'identity.module'),  # identity.permission.module_id
    ('identity', 'IdentityRefreshToken', 'principalId', 'identity.principal'),  # identity.refresh_token.principal_id
    ('identity', 'PlatformStaffGrant', 'operatorPrincipalId', 'identity.principal'),  # identity.platform_staff_grant.operator_principal_id
    ('inventory', 'InventorySupplierContract', 'supplierId', 'inventory.supplier'),  # inventory.supplier_contract.supplier_id
    ('inventory', 'StockCount', 'locationId', 'inventory.location'),  # inventory.count.location_id
    ('inventory', 'StockTransfer', 'fromLocationId', 'inventory.location'),  # inventory.transfer.from_location_id
    ('inventory', 'StockTransfer', 'toLocationId', 'inventory.location'),  # inventory.transfer.to_location_id
    ('maintenance', 'AssetDocument', 'assetId', 'maintenance.asset'),  # maintenance.asset_document.asset_id
    ('maintenance', 'AssetStatusChange', 'assetId', 'maintenance.asset'),  # maintenance.asset_status_change.asset_id
    ('maintenance', 'IncidentAuthorityNotification', 'incidentId', 'maintenance.incident'),  # maintenance.incident_authority_notification.incident_id
    ('maintenance', 'IncidentHistoryEntry', 'incidentId', 'maintenance.incident'),  # maintenance.incident_history.incident_id
    ('maintenance', 'IncidentHistoryEntry', 'principalId', 'identity.principal'),  # maintenance.incident_history.principal_id
    ('maintenance', 'IncidentInvestigationNote', 'incidentId', 'maintenance.incident'),  # maintenance.incident_investigation_note.incident_id
    ('maintenance', 'IncidentInvolvedParty', 'incidentId', 'maintenance.incident'),  # maintenance.incident_involved_party.incident_id
    ('maintenance', 'IncidentMedia', 'incidentId', 'maintenance.incident'),  # maintenance.incident_media.incident_id
    ('maintenance', 'SubmitInspectionRequest', 'templateId', 'maintenance.inspection_template'),  # maintenance.inspection.template_id
    ('maintenance', 'VendorServiceRequest', 'supplierId', 'inventory.supplier'),  # maintenance.vendor_service_request.supplier_id
    ('maintenance', 'VendorServiceRequest', 'workOrderId', 'maintenance.work_order'),  # maintenance.vendor_service_request.work_order_id
    ('marketing-crm', 'AgentServiceProfile', 'principalId', 'identity.principal'),  # marketing.agent_service_profile.principal_id
    ('marketing-crm', 'AudienceActivation', 'segmentId', 'marketing.segment'),  # marketing.audience_activation.segment_id
    ('marketing-crm', 'CaseEscalation', 'caseId', 'marketing.case'),  # marketing.case_escalation.case_id
    ('marketing-crm', 'CaseInvestigationResolutionWorkspaceInput', 'caseId', 'marketing.case'),  # marketing.case_linked_record.case_id
    ('marketing-crm', 'CaseResolutionClosureCustomerFeedbackView', 'caseId', 'marketing.case'),  # marketing.case_resolution.case_id
    ('marketing-crm', 'ConsentCaptureIdentifier', 'deviceConsentId', 'marketing.device_consent'),  # pii.consent_identifier.device_consent_id
    ('marketing-crm', 'ConsentPreferenceCommunicationPolicyEnforcementView', 'subjectId', 'pii.subject'),  # marketing.communication_policy_decision.subject_id
    ('marketing-crm', 'ConsentPropagation', 'consentRecordId', 'marketing.consent_record'),  # marketing.consent_propagation.consent_record_id
    ('marketing-crm', 'DataDiscoveryAccessExportCorrectionWorkspaceView', 'requestId', 'marketing.privacy_request'),  # marketing.privacy_export_package.request_id
    ('marketing-crm', 'DataSubjectCustomerPrivacyRequestManagementView', 'subjectId', 'pii.subject'),  # marketing.privacy_request.subject_id
    ('marketing-crm', 'DeletionAnonymizationRestrictionOperationsView', 'subjectId', 'pii.subject'),  # marketing.privacy_action.subject_id
    ('marketing-crm', 'EscalationCollaborationInternalResolutionView', 'caseId', 'marketing.case'),  # marketing.case_internal_request.case_id
    ('marketing-crm', 'GuestNote', 'subjectId', 'pii.subject'),  # marketing.guest_note.subject_id
    ('marketing-crm', 'JourneyEntrant', 'journeyId', 'marketing.journey'),  # marketing.journey_enrollment.journey_id
    ('marketing-crm', 'JourneyEntrant', 'stepId', 'marketing.journey_step'),  # marketing.journey_enrollment.step_id
    ('marketing-crm', 'JourneyEntrant', 'subjectId', 'pii.subject'),  # marketing.journey_enrollment.subject_id
    ('marketing-crm', 'MarketingCampaignTarget', 'campaignId', 'marketing.campaign'),  # marketing.campaign_target.campaign_id
    ('marketing-crm', 'MarketingCustomerBadge', 'badgeId', 'marketing.badge'),  # marketing.customer_badge.badge_id
    ('marketing-crm', 'MarketingGuestExtraField', 'tenantId', 'none'),  # marketing.guest_extra_field.tenant_id
    ('marketing-crm', 'MarketingLoyaltyRule', 'campaignId', 'marketing.campaign'),  # marketing.loyalty_rule.campaign_id
    ('marketing-crm', 'MarketingReviewResponse', 'reviewId', 'marketing.review'),  # marketing.review_response.review_id
    ('marketing-crm', 'MarketingRewardAssignment', 'rewardId', 'marketing.reward'),  # marketing.reward_assignment.reward_id
    ('marketing-crm', 'MarketingSubscription', 'subjectId', 'pii.subject'),  # marketing.subscription.subject_id
    ('marketing-crm', 'MarketingWaiverSignature', 'templateId', 'marketing.form_definition'),  # marketing.waiver_signature.template_id
    ('marketing-crm', 'MessageDispatchAttempt', 'communicationProviderId', 'marketing.communication_provider'),  # marketing.message_dispatch_attempt.communication_provider_id
    ('marketing-crm', 'MessageDispatchAttempt', 'messageDispatchId', 'marketing.message_dispatch'),  # marketing.message_dispatch_attempt.message_dispatch_id
    ('marketing-crm', 'MessageTemplateVersion', 'messageTemplateId', 'marketing.message_template'),  # marketing.message_template_version.message_template_id
    ('marketing-crm', 'MessageTrigger', 'templateId', 'marketing.message_template'),  # marketing.message_trigger.template_id
    ('marketing-crm', 'MessageTriggerCondition', 'messageTriggerId', 'marketing.message_trigger'),  # marketing.message_trigger_condition.message_trigger_id
    ('marketing-crm', 'OrderBookingTicketServiceWorkspaceInput', 'orderId', 'orders.sales_order'),  # marketing.case_service_action.order_id
    ('marketing-crm', 'QualityManagementAgentEvaluationView', 'agentPrincipalId', 'identity.principal'),  # marketing.quality_evaluation.agent_principal_id
    ('marketing-crm', 'Referral', 'referrerSubjectId', 'pii.subject'),  # marketing.referral.referrer_subject_id
    ('marketing-crm', 'RefundCompensationServiceExceptionWorkspaceInput', 'caseId', 'marketing.case'),  # marketing.case_compensation_request.case_id
    ('marketing-crm', 'SenderIdentityDomainBrandConfigurationInput', 'providerId', 'marketing.communication_provider'),  # marketing.sender_identity.provider_id
    ('marketing-crm', 'WaiverAccessException', 'requirementId', 'marketing.waiver_requirement'),  # marketing.waiver_exception.requirement_id
    ('marketing-crm', 'WaiverRequirement', 'formDefinitionId', 'marketing.form_definition'),  # marketing.waiver_requirement.form_definition_id
    ('marketing-crm', 'WaiverRequirement', 'orderId', 'orders.sales_order'),  # marketing.waiver_requirement.order_id
    ('marketing-crm', 'WaiverRequirement', 'participantSubjectId', 'pii.subject'),  # marketing.waiver_requirement.participant_subject_id
    ('marketing-crm', 'WaiverRequirementEvent', 'waiverRequirementId', 'marketing.waiver_requirement'),  # marketing.waiver_requirement_event.waiver_requirement_id
    ('marketing-crm', 'WaiverVerificationValidationWorkspaceInput', 'submissionId', 'marketing.form_submission'),  # marketing.waiver_verification.submission_id
    ('marketing-crm', 'WishlistItem', 'variantId', 'catalogue.variant'),  # marketing.wishlist_item.variant_id
    ('orders', 'AfterSaleRequest', 'orderId', 'orders.sales_order'),  # orders.after_sale_request.order_id
    ('orders', 'ExternalReferenceMapping', 'merchantId', 'payments.merchant_account'),  # orders.external_reference_mapping.merchant_id
    ('orders', 'ExternalReferenceMapping', 'orderId', 'orders.sales_order'),  # orders.external_reference_mapping.order_id
    ('orders', 'GroupBooking', 'leaderSubjectId', 'pii.subject'),  # orders.group_booking.leader_subject_id
    ('orders', 'GroupPaymentScheduleView', 'groupBookingId', 'orders.group_booking'),  # orders.group_payment_schedule.group_booking_id
    ('orders', 'GroupTicketAllocationView', 'allocations[].productId', 'catalogue.product'),  # orders.group_ticket_allocation_line.product_id
    ('orders', 'GroupTicketAllocationView', 'groupBookingId', 'orders.group_booking'),  # orders.group_ticket_allocation.group_booking_id
    ('orders', 'GroupTicketFulfillmentView', 'groupBookingId', 'orders.group_booking'),  # orders.group_ticket_fulfillment.group_booking_id
    ('orders', 'GuestCreditAccount', 'subjectId', 'pii.subject'),  # orders.guest_credit_account.subject_id
    ('orders', 'Invitation', 'offeredByPrincipalId', 'identity.principal'),  # orders.invitation.offered_by_principal_id
    ('orders', 'OrderRelationship', 'orderId', 'orders.sales_order'),  # orders.order_relationship.order_id
    ('orders', 'OrderRelationship', 'relatedOrderId', 'orders.sales_order'),  # orders.order_relationship.related_order_id
    ('orders', 'OrdersMembershipRenewal', 'customerMembershipId', 'identity.customer_membership'),  # orders.membership_renewal.customer_membership_id
    ('orders', 'OrdersMembershipRenewal', 'entitlementTemplateId', 'catalogue.entitlement_template'),  # orders.membership_renewal.entitlement_template_id
    ('orders', 'OrdersUpgrade', 'originalOrderLineId', 'orders.order_line'),  # orders.upgrade.original_order_line_id
    ('orders', 'ResaleListing', 'sellerSubjectId', 'pii.subject'),  # orders.resale_listing.seller_subject_id
    ('orders', 'ResaleSettlement', 'sellerSubjectId', 'pii.subject'),  # orders.resale_settlement.seller_subject_id
    ('orders', 'Reservation', 'lines[].variantId', 'catalogue.variant'),  # orders.reservation_line.variant_id
    ('platform-ops', 'InboxEntry', 'eventId', 'none'),  # kernel.inbox.event_id
    ('platform-ops', 'MigrationRun', 'cells[].cellId', 'control.cell'),  # control.migration_run_cell.cell_id
    ('platform-ops', 'MigrationRun', 'planId', 'control.migration_plan'),  # control.migration_run.plan_id
    ('platform-ops', 'MigrationRun', 'tenants[].cellId', 'control.cell'),  # control.migration_run_tenant.cell_id
    ('platform-ops', 'MigrationRun', 'tenants[].tenantId', 'control.tenant'),  # control.migration_run_tenant.tenant_id
    ('platform-ops', 'OutboxEntry', 'eventId', 'none'),  # platform.outbox.event_id
    ('platform-ops', 'OutboxEntry', 'tenantId', 'none'),  # platform.outbox.tenant_id
    ('platform-ops', 'RolloutCell', 'rolloutId', 'control.rollout'),  # control.rollout_cell.rollout_id
    ('platform-ops', 'RolloutTenant', 'cellId', 'control.cell'),  # control.rollout_tenant.cell_id
    ('platform-ops', 'RolloutTenant', 'tenantId', 'control.tenant'),  # control.rollout_tenant.tenant_id
    ('platform-ops', 'UpgradeSchedule', 'tenantId', 'control.tenant'),  # control.upgrade_schedule.tenant_id
    ('promotions', 'AllocationComponent', 'variantId', 'catalogue.variant'),  # promotions.allocation_component.variant_id
    ('promotions', 'BundleCapacityPolicy', 'bundleId', 'promotions.bundle'),  # promotions.bundle_capacity_policy.bundle_id
    ('promotions', 'BundleChoiceGroup', 'options[].variantId', 'catalogue.variant'),  # promotions.bundle_choice_option.variant_id
    ('promotions', 'BundleComponent', 'variantId', 'catalogue.variant'),  # promotions.bundle_component.variant_id
    ('promotions', 'CommercialCampaign', 'venueId', 'platform.scope'),  # promotions.campaign.venue_id
    ('promotions', 'CouponCodeBatch', 'campaignId', 'promotions.campaign'),  # promotions.coupon_code_batch.campaign_id
    ('promotions', 'PartnerBundleProduct', 'bundleComponentId', 'promotions.bundle_component'),  # promotions.partner_bundle_product.bundle_component_id
    ('promotions', 'PartnerBundleProduct', 'externalProductId', 'none'),  # promotions.partner_bundle_product.external_product_id
    ('promotions', 'ProductRelationship', 'fromProductId', 'catalogue.product'),  # promotions.product_relationship.from_product_id
    ('promotions', 'ProductRelationship', 'toProductId', 'catalogue.product'),  # promotions.product_relationship.to_product_id
    ('promotions', 'PromotionAlert', 'venueId', 'platform.scope'),  # promotions.promotion_alert.venue_id
    ('promotions', 'PromotionAuditEvent', 'venueId', 'platform.scope'),  # promotions.promotion_audit.venue_id
    ('promotions', 'PromotionChannelPublication', 'venueId', 'platform.scope'),  # promotions.promotion_channel_publication.venue_id
    ('promotions', 'PromotionConflict', 'venueId', 'platform.scope'),  # promotions.promotion_conflict.venue_id
    ('promotions', 'PromotionEvaluationTrace', 'orderId', 'orders.sales_order'),  # promotions.promotion_evaluation_trace.order_id
    ('promotions', 'PromotionEvaluationTrace', 'venueId', 'platform.scope'),  # promotions.promotion_evaluation_trace.venue_id
    ('promotions', 'PromotionRule', 'venueId', 'platform.scope'),  # promotions.promotion_rule.venue_id
    ('promotions', 'StackingRule', 'venueId', 'platform.scope'),  # promotions.stacking_rule.venue_id
    ('public-api', 'ApiClient', 'developerId', 'control.developer_account'),  # control.api_client.developer_id
    ('public-api', 'ApiQuota', 'clientId', 'control.api_client'),  # control.api_limit.client_id
    ('public-api', 'IntegrationListing', 'developerId', 'control.developer_account'),  # control.integration_listing.developer_id
    ('public-api', 'ProductionAccessRequest', 'developerId', 'control.developer_account'),  # control.production_access_request.developer_id
    ('public-api', 'WebhookDelivery', 'subscriptionId', 'control.webhook_subscription'),  # control.webhook_delivery.subscription_id
    ('public-api', 'WebhookSubscription', 'clientId', 'control.api_client'),  # control.webhook_subscription.client_id
    ('rental', 'RentalAgreementItem', 'catalogueProductId', 'catalogue.product'),  # rental.agreement_item.catalogue_product_id
    ('rental', 'RentalAgreementItem', 'orderLineId', 'orders.order_line'),  # rental.agreement_item.order_line_id
    ('rental', 'RentalAgreementItem', 'rentalAgreementId', 'rental.agreement'),  # rental.agreement_item.rental_agreement_id
    ('rental', 'RentalBooking', 'depositAuthorisationId', 'orders.stored_value_authorisation'),  # rental.booking.deposit_authorisation_id
    ('rental', 'RentalBooking', 'productId', 'rental.product'),  # rental.booking.product_id
    ('rental', 'RentalEquipmentAssignment', 'assetId', 'maintenance.asset'),  # rental.equipment_assignment.asset_id
    ('rental', 'RentalInspectionItem', 'rentalAgreementItemId', 'rental.agreement_item'),  # rental.inspection_item.rental_agreement_item_id
    ('rental', 'RentalInspectionItem', 'rentalInspectionId', 'rental.inspection'),  # rental.inspection_item.rental_inspection_id
    ('rental', 'RentalLocationRule', 'locationId', 'inventory.location'),  # rental.location_rule.location_id
    ('rental', 'RentalQuote', 'productId', 'rental.product'),  # rental.quote.product_id
    ('reporting', 'Alert', 'ruleId', 'reporting.alert_rule'),  # reporting.alert.rule_id
    ('reporting', 'NaturalLanguageQuery', 'askedByPrincipalId', 'identity.principal'),  # reporting.natural_language_query.asked_by_principal_id
    ('resources', 'PerformanceParticipant', 'performanceId', 'catalogue.performance'),  # resources.performance_participant.performance_id
    ('resources', 'PerformanceParticipant', 'subjectId', 'pii.subject'),  # resources.performance_participant.subject_id
    ('resources', 'ResourceBlock', 'resourceId', 'resources.resource'),  # resources.resource_block.resource_id
    ('resources', 'ResourceBooking', 'depositAuthorisationId', 'orders.stored_value_authorisation'),  # resources.booking.deposit_authorisation_id
    ('resources', 'ResourceCostEntry', 'resourceId', 'resources.resource'),  # resources.resource_cost.resource_id
    ('resources', 'ResourceHold', 'mapId', 'venuemap.map'),  # resources.resource_reservation.map_id
    ('resources', 'ResourceRelation', 'resourceId', 'resources.resource'),  # resources.resource_relation.resource_id
    ('resources', 'ResourceRequest', 'raisedByPrincipalId', 'identity.principal'),  # resources.resource_request.raised_by_principal_id
    ('resources', 'ResourceSelectionPolicy', 'ticketTypeId', 'catalogue.product'),  # resources.selection_policy.ticket_type_id
    ('resources', 'ResourceVenueAssignment', 'primaryVenueId', 'platform.scope'),  # resources.venue_assignment.primary_venue_id
    ('seating', 'GroupSeatRequest', 'performanceId', 'catalogue.performance'),  # seating.group_request.performance_id
    ('seating', 'SeatHoldPool', 'holdTypeId', 'seating.hold_type'),  # seating.hold_pool.hold_type_id
    ('seating', 'SeatHoldPool', 'performanceId', 'catalogue.performance'),  # seating.hold_pool.performance_id
    ('seating', 'SeatingSeatBlockItem', 'seatId', 'seating.seat'),  # seating.seat_block_item.seat_id
    ('seating', 'SeatingSeatHoldItem', 'seatId', 'seating.seat'),  # seating.seat_reservation_item.seat_id
    ('shift', 'CashCountLine', 'denominationId', 'platform.denomination'),  # orders.cash_count_line.denomination_id
    ('shift', 'DepositBox', 'openingDenominations[].denominationId', 'platform.denomination'),  # orders.deposit_box_opening_denomination.denomination_id
    ('shift', 'Shift', 'approvals[].principalId', 'identity.principal'),  # orders.pos_shift_approval.principal_id
    ('shift', 'TillShiftPolicy', 'venueId', 'platform.scope'),  # orders.till_shift_policy.venue_id
    ('subscription', 'CapacityPack', 'tenantId', 'none'),  # subscription.capacity_pack.tenant_id
    ('subscription', 'CellInstance', 'cellId', 'control.cell'),  # control.cell_instance.cell_id
    ('subscription', 'CellTenant', 'cellId', 'control.cell'),  # control.cell_tenant.cell_id
    ('subscription', 'CellTenant', 'instanceId', 'control.cell_instance'),  # control.cell_tenant.instance_id
    ('subscription', 'CellTenant', 'tenantId', 'control.tenant'),  # control.cell_tenant.tenant_id
    ('subscription', 'MembershipEligibilityRule', 'membershipProductId', 'subscription.membership_product'),  # subscription.membership_eligibility_rule.membership_product_id
    ('subscription', 'MembershipEntitlement', 'membershipProductId', 'subscription.membership_product'),  # subscription.membership_entitlement.membership_product_id
    ('subscription', 'MembershipEntitlement', 'pricingRuleId', 'none'),  # subscription.membership_entitlement.pricing_rule_id
    ('subscription', 'MembershipHouseholdPolicy', 'membershipProductId', 'subscription.membership_product'),  # subscription.membership_household_policy.membership_product_id
    ('subscription', 'MembershipProductHistory', 'changedByPrincipalId', 'identity.principal'),  # subscription.membership_product_history.changed_by_principal_id
    ('subscription', 'MembershipProductHistory', 'membershipProductId', 'subscription.membership_product'),  # subscription.membership_product_history.membership_product_id
    ('subscription', 'MembershipRenewalPolicy', 'membershipProductId', 'subscription.membership_product'),  # subscription.membership_renewal_policy.membership_product_id
    ('subscription', 'MembershipUsagePolicy', 'membershipProductId', 'subscription.membership_product'),  # subscription.membership_usage_policy.membership_product_id
    ('subscription', 'PartnerAllocation', 'agreementId', 'control.partner_agreement'),  # control.partner_allocation.agreement_id
    ('subscription', 'PartnerAllocation', 'partnerId', 'control.partner'),  # control.partner_allocation.partner_id
    ('subscription', 'PartnerBillingProfile', 'agreementId', 'control.partner_agreement'),  # control.partner_billing_profile.agreement_id
    ('subscription', 'PartnerBillingProfile', 'partnerId', 'control.partner'),  # control.partner_billing_profile.partner_id
    ('subscription', 'PartnerCapabilityGrant', 'partnerId', 'control.partner'),  # control.partner_capability_grant.partner_id
    ('subscription', 'PartnerCase', 'partnerId', 'control.partner'),  # control.partner_case.partner_id
    ('subscription', 'PartnerChangeRequest', 'partnerId', 'control.partner'),  # control.partner_change_request.partner_id
    ('subscription', 'PartnerCommercialException', 'partnerId', 'control.partner'),  # control.partner_commercial_exception.partner_id
    ('subscription', 'PartnerCommissionLine', 'agreementId', 'control.partner_agreement'),  # control.partner_commission_line.agreement_id
    ('subscription', 'PartnerCommissionLine', 'partnerId', 'control.partner'),  # control.partner_commission_line.partner_id
    ('subscription', 'PartnerCommissionRule', 'agreementId', 'control.partner_agreement'),  # control.partner_commission_rule.agreement_id
    ('subscription', 'PartnerCommissionRule', 'partnerId', 'control.partner'),  # control.partner_commission_rule.partner_id
    ('subscription', 'PartnerContact', 'partnerId', 'control.partner'),  # control.partner_contact.partner_id
    ('subscription', 'PartnerCreditProfile', 'agreementId', 'control.partner_agreement'),  # control.partner_credit_profile.agreement_id
    ('subscription', 'PartnerCreditProfile', 'partnerId', 'control.partner'),  # control.partner_credit_profile.partner_id
    ('subscription', 'PartnerDistributionRight', 'partnerId', 'control.partner'),  # control.partner_distribution_right.partner_id
    ('subscription', 'PartnerDocument', 'partnerId', 'control.partner'),  # control.partner_document.partner_id
    ('subscription', 'PartnerRate', 'agreementId', 'control.partner_agreement'),  # control.partner_rate.agreement_id
    ('subscription', 'PartnerRate', 'partnerId', 'control.partner'),  # control.partner_rate.partner_id
    ('subscription', 'PartnerReconciliationException', 'partnerId', 'control.partner'),  # control.partner_reconciliation_exception.partner_id
    ('subscription', 'PartnerScopeAssignment', 'partnerId', 'control.partner'),  # control.partner_scope_assignment.partner_id
    ('subscription', 'PartnerSecurity', 'partnerId', 'control.partner'),  # control.partner_security.partner_id
    ('subscription', 'PartnerSettlementBatch', 'partnerId', 'control.partner'),  # control.partner_settlement_batch.partner_id
    ('subscription', 'PartnerStatusHistory', 'partnerId', 'control.partner'),  # control.partner_status_history.partner_id
    ('subscription', 'SubscriptionCreditNote', 'invoiceId', 'control.invoice'),  # control.credit_note.invoice_id
    ('subscription', 'SubscriptionCreditNote', 'tenantId', 'control.tenant'),  # control.credit_note.tenant_id
    ('subscription', 'SubscriptionInvoice', 'tenantId', 'control.tenant'),  # control.invoice.tenant_id
    ('subscription', 'SubscriptionTierAllowance', 'tierId', 'subscription.plan'),  # subscription.tier_allowance.tier_id
    ('subscription', 'SubscriptionTierModule', 'tierId', 'subscription.plan'),  # subscription.tier_module.tier_id
    ('subscription', 'TenantMigrationPlan', 'fromCellId', 'control.cell'),  # control.tenant_migration_plan.from_cell_id
    ('subscription', 'TenantMigrationPlan', 'toCellId', 'control.cell'),  # control.tenant_migration_plan.to_cell_id
    ('tenancy', 'DeviceFirmwareRollout', 'firmwareId', 'tenancy.device_firmware'),  # tenancy.device_rollout.firmware_id
    ('tenancy', 'DeviceTamperEvent', 'deviceId', 'platform.device'),  # tenancy.device_tamper_event.device_id
    ('tenancy', 'ProfileDeployment', 'profileId', 'platform.configuration_profile'),  # platform.profile_deployment.profile_id
    ('transport', 'Departure', 'performanceId', 'catalogue.performance'),  # transport.departure.performance_id
    ('transport', 'Departure', 'routeId', 'transport.route'),  # transport.departure.route_id
    ('transport', 'Departure', 'timetableId', 'transport.timetable'),  # transport.departure.timetable_id
    ('transport', 'FareTable', 'matrix[].fromStationId', 'transport.station'),  # transport.fare_matrix_cell.from_station_id
    ('transport', 'FareTable', 'matrix[].toStationId', 'transport.station'),  # transport.fare_matrix_cell.to_station_id
    ('transport', 'FareTable', 'routeId', 'transport.route'),  # transport.fare_table.route_id
    ('transport', 'FavouriteRoute', 'fromStationId', 'transport.station'),  # transport.favourite_route.from_station_id
    ('transport', 'FavouriteRoute', 'toStationId', 'transport.station'),  # transport.favourite_route.to_station_id
    ('transport', 'FavouriteRoute', 'venueId', 'platform.scope'),  # transport.favourite_route.venue_id
    ('transport', 'PassType', 'venueId', 'platform.scope'),  # transport.pass_type.venue_id
    ('transport', 'RouteStop', 'stationId', 'transport.station'),  # transport.route_stop.station_id
    ('transport', 'Station', 'venueId', 'platform.scope'),  # transport.station.venue_id
    ('transport', 'Timetable', 'routeId', 'transport.route'),  # transport.timetable.route_id
    ('transport', 'TransportNetworkImport', 'venueId', 'platform.scope'),  # transport.network_import.venue_id
    ('transport', 'TransportRoute', 'venueId', 'platform.scope'),  # transport.route.venue_id
    ('venue-map', 'VisitPlan', 'venueId', 'platform.scope'),  # venuemap.visit_plan.venue_id
    ('wallet', 'CreditLot', 'creditTypeId', 'wallet.credit_type'),  # wallet.credit_lot.credit_type_id
    ('wallet', 'SharedWallet', 'walletId', 'wallet.wallet'),  # wallet.shared_wallet.wallet_id
    ('wallet', 'SharedWalletMember', 'subjectId', 'pii.subject'),  # wallet.shared_wallet_member.subject_id
    ('wallet', 'WalletBalance', 'walletBalanceId', 'none'),  # wallet.balance.wallet_balance_id
    ('wallet', 'WalletBalance', 'walletId', 'wallet.wallet'),  # wallet.balance.wallet_id
    ('wallet', 'WalletCredential', 'walletId', 'wallet.wallet'),  # wallet.credential.wallet_id
    ('wallet', 'WalletDispute', 'walletId', 'wallet.wallet'),  # wallet.dispute.wallet_id
    ('wallet', 'WalletExitSettlement', 'walletId', 'wallet.wallet'),  # wallet.exit_settlement.wallet_id
    ('wallet', 'WalletHold', 'walletId', 'wallet.wallet'),  # wallet.fund_reservation.wallet_id
    ('wallet', 'WalletRestriction', 'walletId', 'wallet.wallet'),  # wallet.restriction.wallet_id
    ('white-label', 'CustomDomain', 'tenantId', 'none'),  # whitelabel.custom_domain.tenant_id
    ('white-label', 'GuidedChoice', 'venueId', 'platform.scope'),  # whitelabel.guided_choice.venue_id
    ('white-label', 'KioskConfigVersion', 'kioskConfigId', 'whitelabel.kiosk_config'),  # whitelabel.kiosk_config_version.kiosk_config_id
    ('workforce', 'AttendanceAmendment', 'amendedByPrincipalId', 'identity.principal'),  # workforce.attendance_amendment.amended_by_principal_id
    ('workforce', 'LabourBudget', 'venueId', 'platform.scope'),  # workforce.labour_budget.venue_id
    ('workforce', 'LeaveRequest', 'principalId', 'identity.principal'),  # workforce.leave_request.principal_id
    ('workforce', 'ShiftSwap', 'fromPrincipalId', 'identity.principal'),  # workforce.shift_swap.from_principal_id
    ('workforce', 'ShiftSwap', 'toPrincipalId', 'identity.principal'),  # workforce.shift_swap.to_principal_id
    ('workforce', 'WorkforceEmployee', 'tenantId', 'none'),  # workforce.employee.tenant_id
    ('workforce', 'WorkforceEmployment', 'employeeId', 'workforce.employee'),  # workforce.employment.employee_id
    ('workforce', 'WorkforceJobTitle', 'tenantId', 'none'),  # workforce.job_title.tenant_id
    ('workforce', 'WorkforceLeaveBalance', 'employeeId', 'workforce.employee'),  # workforce.leave_balance.employee_id
    ('workforce', 'WorkforceLeaveBalance', 'typeId', 'workforce.leave_type'),  # workforce.leave_balance.type_id
    ('workforce', 'WorkforceLeaveType', 'tenantId', 'none'),  # workforce.leave_type.tenant_id
    ('workforce', 'WorkforceShift', 'tenantId', 'none'),  # workforce.shift.tenant_id
    ('workforce', 'WorkforceStaffConversation', 'createdByPrincipalId', 'identity.principal'),  # workforce.staff_conversation.created_by_principal_id
    ('workforce', 'WorkforceStaffConversation', 'venueId', 'platform.scope'),  # workforce.staff_conversation.venue_id
    ('workforce', 'WorkforceStaffConversationParticipant', 'principalId', 'identity.principal'),  # workforce.staff_conversation_participant.principal_id
    ('workforce', 'WorkforceStaffConversationParticipant', 'staffConversationId', 'workforce.staff_conversation'),  # workforce.staff_conversation_participant.staff_conversation_id
    ('workforce', 'WorkforceStaffMessage', 'senderPrincipalId', 'identity.principal'),  # workforce.staff_message.sender_principal_id
    ('workforce', 'WorkforceStaffMessage', 'staffConversationId', 'workforce.staff_conversation'),  # workforce.staff_message.staff_conversation_id
    ('workforce', 'WorkforceSyncConflict', 'sourceId', 'workforce.integration_source'),  # workforce.sync_conflict.source_id
    ('workforce', 'WorkforceSyncRun', 'sourceId', 'workforce.integration_source'),  # workforce.sync_run.source_id
    ('workforce', 'WorkforceWorkAssignment', 'employeeId', 'workforce.employee'),  # workforce.work_assignment.employee_id
    ('workforce', 'WorkforceWorkAssignment', 'jobTitleId', 'workforce.job_title'),  # workforce.work_assignment.job_title_id
]


def main() -> int:
    apply = "--apply" in sys.argv
    tic = Path(__file__).resolve().parents[2]
    c = Contracts(tic)
    n = {"+": 0, "~": 0, "=": 0}
    bad = 0
    for stem, schema, path, target, *_ in REFERENCES:
        try:
            how, where = c.set_marker(stem, schema, path, "x-ticvai-references", target)
        except (LookupError, ValueError) as e:
            print("  !", e)
            bad += 1
            continue
        n[how] += 1
        if how != "=":
            print(f"  {how} {where} {path} -> {target}")
    print(f"  declared {n['+']}, changed {n['~']}, already so {n['=']}, not found {bad}")
    if apply:
        print("  wrote", ", ".join(c.save()) or "nothing")
    else:
        print("dry run; pass --apply")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
