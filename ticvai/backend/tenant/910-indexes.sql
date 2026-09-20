-- Conventions and scope paths in the tenant database.
-- **A convention is indexed and not constrained** (ADR-0011): most references are
-- naming habits the contracts never asserted, and enforcing one fails on the first
-- row that legitimately points nowhere.

-- convention, not declared: access.access_change.changed_by_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS ix_access_change_changed_by_principal_id ON access.access_change (changed_by_principal_id);
-- convention, not declared: access.access_change.new_access_id -> access.access_point
CREATE INDEX IF NOT EXISTS ix_access_change_new_access_id ON access.access_change (new_access_id);
-- convention, not declared: access.access_change.old_access_id -> access.access_point
CREATE INDEX IF NOT EXISTS ix_access_change_old_access_id ON access.access_change (old_access_id);
-- convention, not declared: access.access_change.upgrade_id -> orders.upgrade
CREATE INDEX IF NOT EXISTS ix_access_change_upgrade_id ON access.access_change (upgrade_id);
-- convention, not declared: access.entitlement.order_line_id -> orders.order_line
CREATE INDEX IF NOT EXISTS ix_entitlement_order_line_id ON access.entitlement (order_line_id);
-- convention, not declared: access.entitlement.subject_id -> pii.subject
CREATE INDEX IF NOT EXISTS ix_entitlement_subject_id ON access.entitlement (subject_id);
-- convention, not declared: access.entitlement.supersedes_entitlement_id -> access.entitlement
CREATE INDEX IF NOT EXISTS ix_entitlement_supersedes_entitlement_id ON access.entitlement (supersedes_entitlement_id);
-- convention, not declared: access.entry_rule_point.access_point_id -> access.access_point
CREATE INDEX IF NOT EXISTS ix_entry_rule_point_access_point_id ON access.entry_rule_point (access_point_id);
-- convention, not declared: accreditation.application.approval_request_id -> approvals.request
CREATE INDEX IF NOT EXISTS ix_application_approval_request_id ON accreditation.application (approval_request_id);
-- convention, not declared: accreditation.application.holder_id -> accreditation.holder
CREATE INDEX IF NOT EXISTS ix_application_holder_id ON accreditation.application (holder_id);
-- convention, not declared: accreditation.application.programme_id -> accreditation.programme
CREATE INDEX IF NOT EXISTS ix_application_programme_id ON accreditation.application (programme_id);
-- convention, not declared: accreditation.application.submitted_by_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS ix_application_submitted_by_principal_id ON accreditation.application (submitted_by_principal_id);
-- convention, not declared: accreditation.audit.actor_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS ix_audit_actor_principal_id ON accreditation.audit (actor_principal_id);
-- convention, not declared: accreditation.audit.approval_request_id -> approvals.request
CREATE INDEX IF NOT EXISTS ix_audit_approval_request_id ON accreditation.audit (approval_request_id);
-- convention, not declared: accreditation.audit.holder_id -> accreditation.holder
CREATE INDEX IF NOT EXISTS ix_audit_holder_id ON accreditation.audit (holder_id);
-- convention, not declared: accreditation.badge_template.background_asset_id -> assets.media_asset
CREATE INDEX IF NOT EXISTS ix_badge_template_background_asset_id ON accreditation.badge_template (background_asset_id);
-- convention, not declared: accreditation.credential.badge_template_id -> accreditation.badge_template
CREATE INDEX IF NOT EXISTS ix_credential_badge_template_id ON accreditation.credential (badge_template_id);
-- convention, not declared: accreditation.credential.holder_id -> accreditation.holder
CREATE INDEX IF NOT EXISTS ix_credential_holder_id ON accreditation.credential (holder_id);
-- convention, not declared: accreditation.credential.replaces_credential_id -> accreditation.credential
CREATE INDEX IF NOT EXISTS ix_credential_replaces_credential_id ON accreditation.credential (replaces_credential_id);
-- convention, not declared: accreditation.document.application_id -> accreditation.application
CREATE INDEX IF NOT EXISTS ix_document_application_id ON accreditation.document (application_id);
-- convention, not declared: accreditation.document.asset_id -> maintenance.asset
CREATE INDEX IF NOT EXISTS ix_document_asset_id ON accreditation.document (asset_id);
-- convention, not declared: accreditation.document.holder_id -> accreditation.holder
CREATE INDEX IF NOT EXISTS ix_document_holder_id ON accreditation.document (holder_id);
-- convention, not declared: accreditation.holder.photo_asset_id -> assets.media_asset
CREATE INDEX IF NOT EXISTS ix_holder_photo_asset_id ON accreditation.holder (photo_asset_id);
-- convention, not declared: accreditation.holder.programme_id -> accreditation.programme
CREATE INDEX IF NOT EXISTS ix_holder_programme_id ON accreditation.holder (programme_id);
-- convention, not declared: accreditation.holder.subject_id -> pii.subject
CREATE INDEX IF NOT EXISTS ix_holder_subject_id ON accreditation.holder (subject_id);
-- convention, not declared: accreditation.holder_access.holder_id -> accreditation.holder
CREATE INDEX IF NOT EXISTS ix_holder_access_holder_id ON accreditation.holder_access (holder_id);
-- convention, not declared: accreditation.notification_rules.programme_id -> accreditation.programme
CREATE INDEX IF NOT EXISTS ix_notification_rules_programme_id ON accreditation.notification_rules (programme_id);
-- convention, not declared: accreditation.print_job.printer_device_id -> platform.device
CREATE INDEX IF NOT EXISTS ix_print_job_printer_device_id ON accreditation.print_job (printer_device_id);
-- convention, not declared: accreditation.requirements.programme_id -> accreditation.programme
CREATE INDEX IF NOT EXISTS ix_requirements_programme_id ON accreditation.requirements (programme_id);
-- convention, not declared: accreditation.validity.programme_id -> accreditation.programme
CREATE INDEX IF NOT EXISTS ix_validity_programme_id ON accreditation.validity (programme_id);
-- convention, not declared: ai.index_failure.job_id -> ai.index_job
CREATE INDEX IF NOT EXISTS ix_index_failure_job_id ON ai.index_failure (job_id);
-- convention, not declared: ai.index_failure.source_id -> ai.index_source
CREATE INDEX IF NOT EXISTS ix_index_failure_source_id ON ai.index_failure (source_id);
-- convention, not declared: ai.knowledge_document.source_asset_id -> maintenance.asset
CREATE INDEX IF NOT EXISTS ix_knowledge_document_source_asset_id ON ai.knowledge_document (source_asset_id);
-- convention, not declared: ai.policy.fallback_provider_id -> ai.provider
CREATE INDEX IF NOT EXISTS ix_policy_fallback_provider_id ON ai.policy (fallback_provider_id);
-- convention, not declared: ai.provider.failover_provider_id -> ai.provider
CREATE INDEX IF NOT EXISTS ix_provider_failover_provider_id ON ai.provider (failover_provider_id);
-- convention, not declared: ai.suggestion_outcome.decided_by_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS ix_suggestion_outcome_decided_by_principal_id ON ai.suggestion_outcome (decided_by_principal_id);
-- convention, not declared: ai.suggestion_outcome.suggestion_id -> ai.suggestion
CREATE INDEX IF NOT EXISTS ix_suggestion_outcome_suggestion_id ON ai.suggestion_outcome (suggestion_id);
-- convention, not declared: approvals.accreditation_badge.approval_request_id -> approvals.request
CREATE INDEX IF NOT EXISTS ix_accreditation_badge_approval_request_id ON approvals.accreditation_badge (approval_request_id);
-- convention, not declared: approvals.approver_availability.delegation_id -> approvals.delegation
CREATE INDEX IF NOT EXISTS ix_approver_availability_delegation_id ON approvals.approver_availability (delegation_id);
-- convention, not declared: approvals.approver_availability.principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS ix_approver_availability_principal_id ON approvals.approver_availability (principal_id);
-- convention, not declared: approvals.approver_availability.substitute_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS ix_approver_availability_substitute_principal_id ON approvals.approver_availability (substitute_principal_id);
-- convention, not declared: approvals.decision_record.request_id -> approvals.request
CREATE INDEX IF NOT EXISTS ix_decision_record_request_id ON approvals.decision_record (request_id);
-- convention, not declared: approvals.evidence_package.asset_id -> maintenance.asset
CREATE INDEX IF NOT EXISTS ix_evidence_package_asset_id ON approvals.evidence_package (asset_id);
-- convention, not declared: approvals.signature.request_id -> approvals.request
CREATE INDEX IF NOT EXISTS ix_signature_request_id ON approvals.signature (request_id);
-- convention, not declared: assets.approval.asset_id -> maintenance.asset
CREATE INDEX IF NOT EXISTS ix_approval_asset_id ON assets.approval (asset_id);
-- convention, not declared: assets.asset_version.asset_id -> maintenance.asset
CREATE INDEX IF NOT EXISTS ix_asset_version_asset_id ON assets.asset_version (asset_id);
-- convention, not declared: assets.audit.asset_id -> maintenance.asset
CREATE INDEX IF NOT EXISTS ix_audit_asset_id ON assets.audit (asset_id);
-- convention, not declared: assets.distribution_channel.fallback_asset_id -> maintenance.asset
CREATE INDEX IF NOT EXISTS ix_distribution_channel_fallback_asset_id ON assets.distribution_channel (fallback_asset_id);
-- convention, not declared: assets.media_collection.parent_collection_id -> assets.media_collection
CREATE INDEX IF NOT EXISTS ix_media_collection_parent_collection_id ON assets.media_collection (parent_collection_id);
-- convention, not declared: assets.media_upload.upload_id -> assets.media_upload
CREATE INDEX IF NOT EXISTS ix_media_upload_upload_id ON assets.media_upload (upload_id);
-- convention, not declared: catalogue.entitlement_template.admission_rules_id -> access.admission_rules
CREATE INDEX IF NOT EXISTS ix_entitlement_template_admission_rules_id ON catalogue.entitlement_template (admission_rules_id);
-- convention, not declared: catalogue.entitlement_template.renewal_variant_id -> catalogue.variant
CREATE INDEX IF NOT EXISTS ix_entitlement_template_renewal_variant_id ON catalogue.entitlement_template (renewal_variant_id);
-- convention, not declared: catalogue.entitlement_template.transferred_to_subject_id -> pii.subject
CREATE INDEX IF NOT EXISTS ix_entitlement_template_transferred_to_subject_id ON catalogue.entitlement_template (transferred_to_subject_id);
-- convention, not declared: catalogue.event.parent_event_id -> catalogue.event
CREATE INDEX IF NOT EXISTS ix_event_parent_event_id ON catalogue.event (parent_event_id);
-- convention, not declared: catalogue.event_capacity_profile.event_id -> catalogue.event
CREATE INDEX IF NOT EXISTS ix_event_capacity_profile_event_id ON catalogue.event_capacity_profile (event_id);
-- convention, not declared: catalogue.event_capacity_profile.performance_id -> catalogue.performance
CREATE INDEX IF NOT EXISTS ix_event_capacity_profile_performance_id ON catalogue.event_capacity_profile (performance_id);
-- convention, not declared: catalogue.event_capacity_profile.seat_map_id -> seating.seat_map
CREATE INDEX IF NOT EXISTS ix_event_capacity_profile_seat_map_id ON catalogue.event_capacity_profile (seat_map_id);
-- convention, not declared: catalogue.event_registration.event_id -> catalogue.event
CREATE INDEX IF NOT EXISTS ix_event_registration_event_id ON catalogue.event_registration (event_id);
-- convention, not declared: catalogue.event_reschedule.approval_request_id -> approvals.request
CREATE INDEX IF NOT EXISTS ix_event_reschedule_approval_request_id ON catalogue.event_reschedule (approval_request_id);
-- convention, not declared: catalogue.event_reschedule.new_space_id -> catalogue.space
CREATE INDEX IF NOT EXISTS ix_event_reschedule_new_space_id ON catalogue.event_reschedule (new_space_id);
-- convention, not declared: catalogue.event_resource_plan.event_id -> catalogue.event
CREATE INDEX IF NOT EXISTS ix_event_resource_plan_event_id ON catalogue.event_resource_plan (event_id);
-- convention, not declared: catalogue.event_schedule.event_id -> catalogue.event
CREATE INDEX IF NOT EXISTS ix_event_schedule_event_id ON catalogue.event_schedule (event_id);
-- convention, not declared: catalogue.inventory_hold.channel_capacity_id -> catalogue.channel_capacity
CREATE INDEX IF NOT EXISTS ix_inventory_hold_channel_capacity_id ON catalogue.inventory_hold (channel_capacity_id);
-- convention, not declared: catalogue.membership_benefit.entitlement_template_id -> catalogue.entitlement_template
CREATE INDEX IF NOT EXISTS ix_membership_benefit_entitlement_template_id ON catalogue.membership_benefit (entitlement_template_id);
-- convention, not declared: catalogue.performance.admission_rules_id -> access.admission_rules
CREATE INDEX IF NOT EXISTS ix_performance_admission_rules_id ON catalogue.performance (admission_rules_id);
-- convention, not declared: catalogue.performance.approval_request_id -> approvals.request
CREATE INDEX IF NOT EXISTS ix_performance_approval_request_id ON catalogue.performance (approval_request_id);
-- convention, not declared: catalogue.plan_benefit.entitlement_template_id -> catalogue.entitlement_template
CREATE INDEX IF NOT EXISTS ix_plan_benefit_entitlement_template_id ON catalogue.plan_benefit (entitlement_template_id);
-- convention, not declared: catalogue.plan_benefit.membership_benefit_id -> catalogue.membership_benefit
CREATE INDEX IF NOT EXISTS ix_plan_benefit_membership_benefit_id ON catalogue.plan_benefit (membership_benefit_id);
-- convention, not declared: catalogue.prepaid_minutes.credit_type_id -> wallet.credit_type
CREATE INDEX IF NOT EXISTS ix_prepaid_minutes_credit_type_id ON catalogue.prepaid_minutes (credit_type_id);
-- convention, not declared: catalogue.product.approved_by_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS ix_product_approved_by_principal_id ON catalogue.product (approved_by_principal_id);
-- convention, not declared: catalogue.product.category_id -> catalogue.product_category
CREATE INDEX IF NOT EXISTS ix_product_category_id ON catalogue.product (category_id);
-- convention, not declared: catalogue.product.created_by_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS ix_product_created_by_principal_id ON catalogue.product (created_by_principal_id);
-- convention, not declared: catalogue.product_category.image_asset_id -> assets.media_asset
CREATE INDEX IF NOT EXISTS ix_product_category_image_asset_id ON catalogue.product_category (image_asset_id);
-- convention, not declared: catalogue.product_version.published_by_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS ix_product_version_published_by_principal_id ON catalogue.product_version (published_by_principal_id);
-- convention, not declared: catalogue.session_template.space_id -> catalogue.space
CREATE INDEX IF NOT EXISTS ix_session_template_space_id ON catalogue.session_template (space_id);
-- convention, not declared: catalogue.space.parent_space_id -> catalogue.space
CREATE INDEX IF NOT EXISTS ix_space_parent_space_id ON catalogue.space (parent_space_id);
-- convention, not declared: catalogue.space.resource_id -> resources.resource
CREATE INDEX IF NOT EXISTS ix_space_resource_id ON catalogue.space (resource_id);
-- convention, not declared: catalogue.space.venue_map_zone_id -> seating.zone
CREATE INDEX IF NOT EXISTS ix_space_venue_map_zone_id ON catalogue.space (venue_map_zone_id);
-- convention, not declared: fnb.cold_chain_event.corrective_action_id -> fnb.corrective_action
CREATE INDEX IF NOT EXISTS ix_cold_chain_event_corrective_action_id ON fnb.cold_chain_event (corrective_action_id);
-- convention, not declared: fnb.cold_chain_event.goods_receipt_id -> inventory.goods_receipt
CREATE INDEX IF NOT EXISTS ix_cold_chain_event_goods_receipt_id ON fnb.cold_chain_event (goods_receipt_id);
-- convention, not declared: fnb.cold_chain_event.transfer_id -> inventory.transfer
CREATE INDEX IF NOT EXISTS ix_cold_chain_event_transfer_id ON fnb.cold_chain_event (transfer_id);
-- convention, not declared: fnb.combo.outlet_id -> platform.outlet
CREATE INDEX IF NOT EXISTS ix_combo_outlet_id ON fnb.combo (outlet_id);
-- convention, not declared: fnb.combo_slot.combo_id -> fnb.combo
CREATE INDEX IF NOT EXISTS ix_combo_slot_combo_id ON fnb.combo_slot (combo_id);
-- convention, not declared: fnb.corrective_action.escalated_to_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS ix_corrective_action_escalated_to_principal_id ON fnb.corrective_action (escalated_to_principal_id);
-- convention, not declared: fnb.corrective_action.signed_by_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS ix_corrective_action_signed_by_principal_id ON fnb.corrective_action (signed_by_principal_id);
-- convention, not declared: fnb.ingredient_substitute.from_inventory_item_id -> inventory.item
CREATE INDEX IF NOT EXISTS ix_ingredient_substitute_from_inventory_item_id ON fnb.ingredient_substitute (from_inventory_item_id);
-- convention, not declared: fnb.ingredient_substitute.to_inventory_item_id -> inventory.item
CREATE INDEX IF NOT EXISTS ix_ingredient_substitute_to_inventory_item_id ON fnb.ingredient_substitute (to_inventory_item_id);
-- convention, not declared: fnb.kitchen_exception.outlet_id -> platform.outlet
CREATE INDEX IF NOT EXISTS ix_kitchen_exception_outlet_id ON fnb.kitchen_exception (outlet_id);
-- convention, not declared: fnb.kitchen_exception.raised_by_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS ix_kitchen_exception_raised_by_principal_id ON fnb.kitchen_exception (raised_by_principal_id);
-- convention, not declared: fnb.kitchen_exception.station_id -> fnb.kitchen_station
CREATE INDEX IF NOT EXISTS ix_kitchen_exception_station_id ON fnb.kitchen_exception (station_id);
-- convention, not declared: fnb.menu_item_modifier.group_id -> fnb.modifier_group
CREATE INDEX IF NOT EXISTS ix_menu_item_modifier_group_id ON fnb.menu_item_modifier (group_id);
-- convention, not declared: fnb.product_recommendation.source_product_id -> fnb.product_recommendation
CREATE INDEX IF NOT EXISTS ix_product_recommendation_source_product_id ON fnb.product_recommendation (source_product_id);
-- convention, not declared: fnb.product_recommendation.source_variant_id -> catalogue.variant
CREATE INDEX IF NOT EXISTS ix_product_recommendation_source_variant_id ON fnb.product_recommendation (source_variant_id);
-- convention, not declared: fnb.product_recommendation.target_product_id -> fnb.product_recommendation
CREATE INDEX IF NOT EXISTS ix_product_recommendation_target_product_id ON fnb.product_recommendation (target_product_id);
-- convention, not declared: fnb.product_recommendation.target_variant_id -> catalogue.variant
CREATE INDEX IF NOT EXISTS ix_product_recommendation_target_variant_id ON fnb.product_recommendation (target_variant_id);
-- convention, not declared: fnb.production_plan.based_on_suggestion_id -> ai.suggestion
CREATE INDEX IF NOT EXISTS ix_production_plan_based_on_suggestion_id ON fnb.production_plan (based_on_suggestion_id);
-- convention, not declared: fnb.production_plan.outlet_id -> platform.outlet
CREATE INDEX IF NOT EXISTS ix_production_plan_outlet_id ON fnb.production_plan (outlet_id);
-- convention, not declared: fnb.production_run.producing_outlet_id -> platform.outlet
CREATE INDEX IF NOT EXISTS ix_production_run_producing_outlet_id ON fnb.production_run (producing_outlet_id);
-- convention, not declared: fnb.reservation_table.reservation_id -> fnb.table_reservation
CREATE INDEX IF NOT EXISTS ix_reservation_table_reservation_id ON fnb.reservation_table (reservation_id);
-- convention, not declared: fnb.service_order.sales_order_id -> orders.sales_order
CREATE INDEX IF NOT EXISTS ix_service_order_sales_order_id ON fnb.service_order (sales_order_id);
-- convention, not declared: fnb.service_order_line.menu_item_id -> fnb.menu_item
CREATE INDEX IF NOT EXISTS ix_service_order_line_menu_item_id ON fnb.service_order_line (menu_item_id);
-- convention, not declared: fnb.sold_out_item.called_by_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS ix_sold_out_item_called_by_principal_id ON fnb.sold_out_item (called_by_principal_id);
-- convention, not declared: fnb.sold_out_item.menu_item_id -> fnb.menu_item
CREATE INDEX IF NOT EXISTS ix_sold_out_item_menu_item_id ON fnb.sold_out_item (menu_item_id);
-- convention, not declared: fnb.sold_out_item.outlet_id -> platform.outlet
CREATE INDEX IF NOT EXISTS ix_sold_out_item_outlet_id ON fnb.sold_out_item (outlet_id);
-- convention, not declared: fnb.sub_bill.sub_bill_id -> fnb.sub_bill
CREATE INDEX IF NOT EXISTS ix_sub_bill_sub_bill_id ON fnb.sub_bill (sub_bill_id);
-- convention, not declared: fnb.sub_bill.visit_id -> fnb.table_visit
CREATE INDEX IF NOT EXISTS ix_sub_bill_visit_id ON fnb.sub_bill (visit_id);
-- convention, not declared: fnb.table_reservation.group_id -> fnb.modifier_group
CREATE INDEX IF NOT EXISTS ix_table_reservation_group_id ON fnb.table_reservation (group_id);
-- convention, not declared: fnb.table_visit.merged_into_visit_id -> fnb.table_visit
CREATE INDEX IF NOT EXISTS ix_table_visit_merged_into_visit_id ON fnb.table_visit (merged_into_visit_id);
-- convention, not declared: fnb.temperature_log.check_point_id -> venuemap.point
CREATE INDEX IF NOT EXISTS ix_temperature_log_check_point_id ON fnb.temperature_log (check_point_id);
-- convention, not declared: fnb.temperature_log.corrective_action_id -> fnb.corrective_action
CREATE INDEX IF NOT EXISTS ix_temperature_log_corrective_action_id ON fnb.temperature_log (corrective_action_id);
-- convention, not declared: fnb.temperature_log.recorded_by_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS ix_temperature_log_recorded_by_principal_id ON fnb.temperature_log (recorded_by_principal_id);
-- convention, not declared: games.gameplay_transaction.card_id -> games.card
CREATE INDEX IF NOT EXISTS ix_gameplay_transaction_card_id ON games.gameplay_transaction (card_id);
-- convention, not declared: games.gameplay_transaction.game_id -> games.game
CREATE INDEX IF NOT EXISTS ix_gameplay_transaction_game_id ON games.gameplay_transaction (game_id);
-- convention, not declared: games.gameplay_transaction.reader_id -> games.reader
CREATE INDEX IF NOT EXISTS ix_gameplay_transaction_reader_id ON games.gameplay_transaction (reader_id);
-- convention, not declared: games.kiosk_config.kiosk_device_id -> platform.device
CREATE INDEX IF NOT EXISTS ix_kiosk_config_kiosk_device_id ON games.kiosk_config (kiosk_device_id);
-- convention, not declared: games.operational_config.game_id -> games.game
CREATE INDEX IF NOT EXISTS ix_operational_config_game_id ON games.operational_config (game_id);
-- convention, not declared: games.play.play_id -> games.play
CREATE INDEX IF NOT EXISTS ix_play_play_id ON games.play (play_id);
-- convention, not declared: games.pricing.game_id -> games.game
CREATE INDEX IF NOT EXISTS ix_pricing_game_id ON games.pricing (game_id);
-- convention, not declared: games.prize_cost.inventory_item_id -> inventory.item
CREATE INDEX IF NOT EXISTS ix_prize_cost_inventory_item_id ON games.prize_cost (inventory_item_id);
-- convention, not declared: games.prize_cost.prize_id -> games.prize
CREATE INDEX IF NOT EXISTS ix_prize_cost_prize_id ON games.prize_cost (prize_id);
-- convention, not declared: games.reader.device_id -> platform.device
CREATE INDEX IF NOT EXISTS ix_reader_device_id ON games.reader (device_id);
-- convention, not declared: games.reader.game_id -> games.game
CREATE INDEX IF NOT EXISTS ix_reader_game_id ON games.reader (game_id);
-- convention, not declared: games.reader.reader_profile_id -> games.reader_profile
CREATE INDEX IF NOT EXISTS ix_reader_reader_profile_id ON games.reader (reader_profile_id);
-- convention, not declared: games.reader_deployment.reader_id -> games.reader
CREATE INDEX IF NOT EXISTS ix_reader_deployment_reader_id ON games.reader_deployment (reader_id);
-- convention, not declared: games.redemption_rules.ticket_credit_type_id -> wallet.credit_type
CREATE INDEX IF NOT EXISTS ix_redemption_rules_ticket_credit_type_id ON games.redemption_rules (ticket_credit_type_id);
-- convention, not declared: identity.access_decision.override_id -> rental.override
CREATE INDEX IF NOT EXISTS ix_access_decision_override_id ON identity.access_decision (override_id);
-- convention, not declared: identity.access_decision.principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS ix_access_decision_principal_id ON identity.access_decision (principal_id);
-- convention, not declared: identity.access_override.principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS ix_access_override_principal_id ON identity.access_override (principal_id);
-- convention, not declared: identity.benefit_usage.customer_membership_id -> identity.customer_membership
CREATE INDEX IF NOT EXISTS ix_benefit_usage_customer_membership_id ON identity.benefit_usage (customer_membership_id);
-- convention, not declared: identity.benefit_usage.membership_benefit_id -> catalogue.membership_benefit
CREATE INDEX IF NOT EXISTS ix_benefit_usage_membership_benefit_id ON identity.benefit_usage (membership_benefit_id);
-- convention, not declared: identity.customer_membership.customer_id -> identity.customer_membership
CREATE INDEX IF NOT EXISTS ix_customer_membership_customer_id ON identity.customer_membership (customer_id);
-- convention, not declared: identity.customer_membership.entitlement_template_id -> catalogue.entitlement_template
CREATE INDEX IF NOT EXISTS ix_customer_membership_entitlement_template_id ON identity.customer_membership (entitlement_template_id);
-- convention, not declared: identity.delegated_access.over_subject_id -> pii.subject
CREATE INDEX IF NOT EXISTS ix_delegated_access_over_subject_id ON identity.delegated_access (over_subject_id);
-- convention, not declared: identity.delegated_access.permission_id -> identity.permission
CREATE INDEX IF NOT EXISTS ix_delegated_access_permission_id ON identity.delegated_access (permission_id);
-- convention, not declared: identity.membership_history.changed_by_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS ix_membership_history_changed_by_principal_id ON identity.membership_history (changed_by_principal_id);
-- convention, not declared: identity.membership_history.customer_membership_id -> identity.customer_membership
CREATE INDEX IF NOT EXISTS ix_membership_history_customer_membership_id ON identity.membership_history (customer_membership_id);
-- convention, not declared: identity.module.parent_module_id -> identity.module
CREATE INDEX IF NOT EXISTS ix_module_parent_module_id ON identity.module (parent_module_id);
-- convention, not declared: identity.permission.module_id -> identity.module
CREATE INDEX IF NOT EXISTS ix_permission_module_id ON identity.permission (module_id);
-- convention, not declared: identity.refresh_token.principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS ix_refresh_token_principal_id ON identity.refresh_token (principal_id);
-- convention, not declared: identity.refresh_token.replaced_by_token_id -> payments.token
CREATE INDEX IF NOT EXISTS ix_refresh_token_replaced_by_token_id ON identity.refresh_token (replaced_by_token_id);
-- convention, not declared: identity.role.inherits_from_role_id -> identity.role
CREATE INDEX IF NOT EXISTS ix_role_inherits_from_role_id ON identity.role (inherits_from_role_id);
-- convention, not declared: identity.role_permission.granted_by_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS ix_role_permission_granted_by_principal_id ON identity.role_permission (granted_by_principal_id);
-- convention, not declared: identity.sso_provider.client_id -> control.api_client
CREATE INDEX IF NOT EXISTS ix_sso_provider_client_id ON identity.sso_provider (client_id);
-- convention, not declared: inventory.count_line.batch_id -> inventory.stock_batch
CREATE INDEX IF NOT EXISTS ix_count_line_batch_id ON inventory.count_line (batch_id);
-- convention, not declared: inventory.count_line.count_id -> inventory.count
CREATE INDEX IF NOT EXISTS ix_count_line_count_id ON inventory.count_line (count_id);
-- convention, not declared: inventory.count_line.counted_by_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS ix_count_line_counted_by_principal_id ON inventory.count_line (counted_by_principal_id);
-- convention, not declared: inventory.count_line.item_id -> inventory.item
CREATE INDEX IF NOT EXISTS ix_count_line_item_id ON inventory.count_line (item_id);
-- convention, not declared: inventory.count_line.location_id -> inventory.location
CREATE INDEX IF NOT EXISTS ix_count_line_location_id ON inventory.count_line (location_id);
-- convention, not declared: inventory.location.parent_location_id -> inventory.location
CREATE INDEX IF NOT EXISTS ix_location_parent_location_id ON inventory.location (parent_location_id);
-- convention, not declared: inventory.serialised_item.batch_id -> inventory.stock_batch
CREATE INDEX IF NOT EXISTS ix_serialised_item_batch_id ON inventory.serialised_item (batch_id);
-- convention, not declared: inventory.serialised_item.item_id -> inventory.item
CREATE INDEX IF NOT EXISTS ix_serialised_item_item_id ON inventory.serialised_item (item_id);
-- convention, not declared: inventory.serialised_item.location_id -> inventory.location
CREATE INDEX IF NOT EXISTS ix_serialised_item_location_id ON inventory.serialised_item (location_id);
-- convention, not declared: inventory.serialised_item.sold_on_order_line_id -> orders.order_line
CREATE INDEX IF NOT EXISTS ix_serialised_item_sold_on_order_line_id ON inventory.serialised_item (sold_on_order_line_id);
-- convention, not declared: inventory.stock_reservation.item_id -> inventory.item
CREATE INDEX IF NOT EXISTS ix_stock_reservation_item_id ON inventory.stock_reservation (item_id);
-- convention, not declared: inventory.stock_reservation.location_id -> inventory.location
CREATE INDEX IF NOT EXISTS ix_stock_reservation_location_id ON inventory.stock_reservation (location_id);
-- convention, not declared: inventory.supplier_contract.created_by_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS ix_supplier_contract_created_by_principal_id ON inventory.supplier_contract (created_by_principal_id);
-- convention, not declared: inventory.supplier_contract.supplier_id -> inventory.supplier
CREATE INDEX IF NOT EXISTS ix_supplier_contract_supplier_id ON inventory.supplier_contract (supplier_id);
-- convention, not declared: ledger.deposit.liability_account_id -> ledger.account
CREATE INDEX IF NOT EXISTS ix_deposit_liability_account_id ON ledger.deposit (liability_account_id);
-- convention, not declared: ledger.fx_rate.set_by_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS ix_fx_rate_set_by_principal_id ON ledger.fx_rate (set_by_principal_id);
-- convention, not declared: ledger.inter_entity_obligation.from_legal_entity_id -> ledger.legal_entity
CREATE INDEX IF NOT EXISTS ix_inter_entity_obligation_from_legal_entity_id ON ledger.inter_entity_obligation (from_legal_entity_id);
-- convention, not declared: ledger.inter_entity_obligation.to_legal_entity_id -> ledger.legal_entity
CREATE INDEX IF NOT EXISTS ix_inter_entity_obligation_to_legal_entity_id ON ledger.inter_entity_obligation (to_legal_entity_id);
-- convention, not declared: ledger.journal_line.account_id -> ledger.account
CREATE INDEX IF NOT EXISTS ix_journal_line_account_id ON ledger.journal_line (account_id);
-- convention, not declared: ledger.journal_line.cost_center_id -> ledger.cost_center
CREATE INDEX IF NOT EXISTS ix_journal_line_cost_center_id ON ledger.journal_line (cost_center_id);
-- convention, not declared: ledger.recognition_schedule.no_show_account_id -> ledger.account
CREATE INDEX IF NOT EXISTS ix_recognition_schedule_no_show_account_id ON ledger.recognition_schedule (no_show_account_id);
-- convention, not declared: ledger.tax_code.compound_on_tax_code_id -> ledger.tax_code
CREATE INDEX IF NOT EXISTS ix_tax_code_compound_on_tax_code_id ON ledger.tax_code (compound_on_tax_code_id);
-- convention, not declared: maintenance.asset.category_id -> maintenance.asset_category
CREATE INDEX IF NOT EXISTS ix_asset_category_id ON maintenance.asset (category_id);
-- convention, not declared: maintenance.asset.device_id -> platform.device
CREATE INDEX IF NOT EXISTS ix_asset_device_id ON maintenance.asset (device_id);
-- convention, not declared: maintenance.asset.resource_id -> resources.resource
CREATE INDEX IF NOT EXISTS ix_asset_resource_id ON maintenance.asset (resource_id);
-- convention, not declared: maintenance.asset_category.default_deposit_policy_id -> rental.deposit_policy
CREATE INDEX IF NOT EXISTS ix_asset_category_default_deposit_policy_id ON maintenance.asset_category (default_deposit_policy_id);
-- convention, not declared: maintenance.asset_category.icon_asset_id -> assets.media_asset
CREATE INDEX IF NOT EXISTS ix_asset_category_icon_asset_id ON maintenance.asset_category (icon_asset_id);
-- convention, not declared: maintenance.asset_category.parent_category_id -> maintenance.asset_category
CREATE INDEX IF NOT EXISTS ix_asset_category_parent_category_id ON maintenance.asset_category (parent_category_id);
-- convention, not declared: maintenance.inspection.template_id -> maintenance.inspection_template
CREATE INDEX IF NOT EXISTS ix_inspection_template_id ON maintenance.inspection (template_id);
-- convention, not declared: maintenance.inspection_item.inspection_id -> maintenance.inspection
CREATE INDEX IF NOT EXISTS ix_inspection_item_inspection_id ON maintenance.inspection_item (inspection_id);
-- convention, not declared: maintenance.inspection_item.template_item_id -> maintenance.inspection_template_item
CREATE INDEX IF NOT EXISTS ix_inspection_item_template_item_id ON maintenance.inspection_item (template_item_id);
-- convention, not declared: maintenance.inspection_template.applies_to_asset_category_id -> maintenance.asset_category
CREATE INDEX IF NOT EXISTS ix_inspection_template_applies_to_asset_category_id ON maintenance.inspection_template (applies_to_asset_category_id);
-- convention, not declared: maintenance.preventive_plan.asset_category_id -> maintenance.asset_category
CREATE INDEX IF NOT EXISTS ix_preventive_plan_asset_category_id ON maintenance.preventive_plan (asset_category_id);
-- convention, not declared: maintenance.work_order.verified_by_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS ix_work_order_verified_by_principal_id ON maintenance.work_order (verified_by_principal_id);
-- convention, not declared: maintenance.work_order_attachment.captured_by_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS ix_work_order_attachment_captured_by_principal_id ON maintenance.work_order_attachment (captured_by_principal_id);
-- convention, not declared: marketing.audience_activation.approval_request_id -> approvals.request
CREATE INDEX IF NOT EXISTS ix_audience_activation_approval_request_id ON marketing.audience_activation (approval_request_id);
-- convention, not declared: marketing.audience_activation.segment_id -> marketing.segment
CREATE INDEX IF NOT EXISTS ix_audience_activation_segment_id ON marketing.audience_activation (segment_id);
-- convention, not declared: marketing.audience_list.asset_id -> maintenance.asset
CREATE INDEX IF NOT EXISTS ix_audience_list_asset_id ON marketing.audience_list (asset_id);
-- convention, not declared: marketing.campaign_target.campaign_id -> marketing.campaign
CREATE INDEX IF NOT EXISTS ix_campaign_target_campaign_id ON marketing.campaign_target (campaign_id);
-- convention, not declared: marketing.campaign_target.target_id -> marketing.campaign_target
CREATE INDEX IF NOT EXISTS ix_campaign_target_target_id ON marketing.campaign_target (target_id);
-- convention, not declared: marketing.challenge.badge_asset_id -> assets.media_asset
CREATE INDEX IF NOT EXISTS ix_challenge_badge_asset_id ON marketing.challenge (badge_asset_id);
-- convention, not declared: marketing.conversation.assist_session_id -> marketing.kiosk_assist_session
CREATE INDEX IF NOT EXISTS ix_conversation_assist_session_id ON marketing.conversation (assist_session_id);
-- convention, not declared: marketing.conversation_message.sender_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS ix_conversation_message_sender_principal_id ON marketing.conversation_message (sender_principal_id);
-- convention, not declared: marketing.customer_badge.badge_id -> marketing.badge
CREATE INDEX IF NOT EXISTS ix_customer_badge_badge_id ON marketing.customer_badge (badge_id);
-- convention, not declared: marketing.customer_badge.challenge_id -> marketing.challenge
CREATE INDEX IF NOT EXISTS ix_customer_badge_challenge_id ON marketing.customer_badge (challenge_id);
-- convention, not declared: marketing.customer_badge.customer_id -> marketing.customer_badge
CREATE INDEX IF NOT EXISTS ix_customer_badge_customer_id ON marketing.customer_badge (customer_id);
-- convention, not declared: marketing.form_submission.form_id -> marketing.form_definition
CREATE INDEX IF NOT EXISTS ix_form_submission_form_id ON marketing.form_submission (form_id);
-- convention, not declared: marketing.form_submission.on_behalf_of_subject_id -> pii.subject
CREATE INDEX IF NOT EXISTS ix_form_submission_on_behalf_of_subject_id ON marketing.form_submission (on_behalf_of_subject_id);
-- convention, not declared: marketing.form_submission.signature_asset_id -> assets.media_asset
CREATE INDEX IF NOT EXISTS ix_form_submission_signature_asset_id ON marketing.form_submission (signature_asset_id);
-- convention, not declared: marketing.guest_document.uploaded_by_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS ix_guest_document_uploaded_by_principal_id ON marketing.guest_document (uploaded_by_principal_id);
-- convention, not declared: marketing.guest_extra_value.customer_id -> marketing.customer_badge
CREATE INDEX IF NOT EXISTS ix_guest_extra_value_customer_id ON marketing.guest_extra_value (customer_id);
-- convention, not declared: marketing.invitation.issued_by_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS ix_invitation_issued_by_principal_id ON marketing.invitation (issued_by_principal_id);
-- convention, not declared: marketing.invitation.offered_by_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS ix_invitation_offered_by_principal_id ON marketing.invitation (offered_by_principal_id);
-- convention, not declared: marketing.journey_enrollment.journey_id -> marketing.journey
CREATE INDEX IF NOT EXISTS ix_journey_enrollment_journey_id ON marketing.journey_enrollment (journey_id);
-- convention, not declared: marketing.journey_enrollment.step_id -> marketing.journey_step
CREATE INDEX IF NOT EXISTS ix_journey_enrollment_step_id ON marketing.journey_enrollment (step_id);
-- convention, not declared: marketing.journey_enrollment.subject_id -> pii.subject
CREATE INDEX IF NOT EXISTS ix_journey_enrollment_subject_id ON marketing.journey_enrollment (subject_id);
-- convention, not declared: marketing.journey_step.campaign_id -> marketing.campaign
CREATE INDEX IF NOT EXISTS ix_journey_step_campaign_id ON marketing.journey_step (campaign_id);
-- convention, not declared: marketing.journey_step.failure_journey_step_id -> marketing.journey_step
CREATE INDEX IF NOT EXISTS ix_journey_step_failure_journey_step_id ON marketing.journey_step (failure_journey_step_id);
-- convention, not declared: marketing.journey_step.journey_id -> marketing.journey
CREATE INDEX IF NOT EXISTS ix_journey_step_journey_id ON marketing.journey_step (journey_id);
-- convention, not declared: marketing.journey_step.message_template_id -> marketing.message_template
CREATE INDEX IF NOT EXISTS ix_journey_step_message_template_id ON marketing.journey_step (message_template_id);
-- convention, not declared: marketing.journey_step.next_journey_step_id -> marketing.journey_step
CREATE INDEX IF NOT EXISTS ix_journey_step_next_journey_step_id ON marketing.journey_step (next_journey_step_id);
-- convention, not declared: marketing.lost_item.last_seen_point_id -> venuemap.point
CREATE INDEX IF NOT EXISTS ix_lost_item_last_seen_point_id ON marketing.lost_item (last_seen_point_id);
-- convention, not declared: marketing.lost_item.reported_by_subject_id -> pii.subject
CREATE INDEX IF NOT EXISTS ix_lost_item_reported_by_subject_id ON marketing.lost_item (reported_by_subject_id);
-- convention, not declared: marketing.loyalty_campaign.campaign_id -> marketing.campaign
CREATE INDEX IF NOT EXISTS ix_loyalty_campaign_campaign_id ON marketing.loyalty_campaign (campaign_id);
-- convention, not declared: marketing.loyalty_points.customer_id -> marketing.customer_badge
CREATE INDEX IF NOT EXISTS ix_loyalty_points_customer_id ON marketing.loyalty_points (customer_id);
-- convention, not declared: marketing.loyalty_points.reversed_loyalty_points_id -> marketing.loyalty_points
CREATE INDEX IF NOT EXISTS ix_loyalty_points_reversed_loyalty_points_id ON marketing.loyalty_points (reversed_loyalty_points_id);
-- convention, not declared: marketing.loyalty_position.tier_id -> marketing.programme_tier
CREATE INDEX IF NOT EXISTS ix_loyalty_position_tier_id ON marketing.loyalty_position (tier_id);
-- convention, not declared: marketing.loyalty_rule.campaign_id -> marketing.campaign
CREATE INDEX IF NOT EXISTS ix_loyalty_rule_campaign_id ON marketing.loyalty_rule (campaign_id);
-- convention, not declared: marketing.loyalty_rule.points_earning_rule_id -> marketing.points_earning_rule
CREATE INDEX IF NOT EXISTS ix_loyalty_rule_points_earning_rule_id ON marketing.loyalty_rule (points_earning_rule_id);
-- convention, not declared: marketing.loyalty_rule.reward_id -> marketing.reward
CREATE INDEX IF NOT EXISTS ix_loyalty_rule_reward_id ON marketing.loyalty_rule (reward_id);
-- convention, not declared: marketing.message_dispatch.template_id -> marketing.message_template
CREATE INDEX IF NOT EXISTS ix_message_dispatch_template_id ON marketing.message_dispatch (template_id);
-- convention, not declared: marketing.message_template.provider_template_id -> marketing.message_template
CREATE INDEX IF NOT EXISTS ix_message_template_provider_template_id ON marketing.message_template (provider_template_id);
-- convention, not declared: marketing.message_trigger.template_id -> marketing.message_template
CREATE INDEX IF NOT EXISTS ix_message_trigger_template_id ON marketing.message_trigger (template_id);
-- convention, not declared: marketing.programme_tier.loyalty_programme_id -> marketing.loyalty_programme
CREATE INDEX IF NOT EXISTS ix_programme_tier_loyalty_programme_id ON marketing.programme_tier (loyalty_programme_id);
-- convention, not declared: marketing.referral.referee_reward_id -> marketing.reward
CREATE INDEX IF NOT EXISTS ix_referral_referee_reward_id ON marketing.referral (referee_reward_id);
-- convention, not declared: marketing.referral.referee_subject_id -> pii.subject
CREATE INDEX IF NOT EXISTS ix_referral_referee_subject_id ON marketing.referral (referee_subject_id);
-- convention, not declared: marketing.referral.referrer_reward_id -> marketing.reward
CREATE INDEX IF NOT EXISTS ix_referral_referrer_reward_id ON marketing.referral (referrer_reward_id);
-- convention, not declared: marketing.referral.referrer_subject_id -> pii.subject
CREATE INDEX IF NOT EXISTS ix_referral_referrer_subject_id ON marketing.referral (referrer_subject_id);
-- convention, not declared: marketing.review_response.responded_by_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS ix_review_response_responded_by_principal_id ON marketing.review_response (responded_by_principal_id);
-- convention, not declared: marketing.review_response.review_id -> marketing.review
CREATE INDEX IF NOT EXISTS ix_review_response_review_id ON marketing.review_response (review_id);
-- convention, not declared: marketing.reward_assignment.customer_id -> marketing.customer_badge
CREATE INDEX IF NOT EXISTS ix_reward_assignment_customer_id ON marketing.reward_assignment (customer_id);
-- convention, not declared: marketing.reward_assignment.reward_id -> marketing.reward
CREATE INDEX IF NOT EXISTS ix_reward_assignment_reward_id ON marketing.reward_assignment (reward_id);
-- convention, not declared: marketing.waiver_signature.customer_id -> marketing.customer_badge
CREATE INDEX IF NOT EXISTS ix_waiver_signature_customer_id ON marketing.waiver_signature (customer_id);
-- convention, not declared: marketing.waiver_signature.template_id -> marketing.message_template
CREATE INDEX IF NOT EXISTS ix_waiver_signature_template_id ON marketing.waiver_signature (template_id);
-- convention, not declared: orders.cart_line.inventory_hold_id -> catalogue.inventory_hold
CREATE INDEX IF NOT EXISTS ix_cart_line_inventory_hold_id ON orders.cart_line (inventory_hold_id);
-- convention, not declared: orders.cash_count_line.denomination_id -> platform.denomination
CREATE INDEX IF NOT EXISTS ix_cash_count_line_denomination_id ON orders.cash_count_line (denomination_id);
-- convention, not declared: orders.cash_count_line.deposit_box_id -> orders.deposit_box
CREATE INDEX IF NOT EXISTS ix_cash_count_line_deposit_box_id ON orders.cash_count_line (deposit_box_id);
-- convention, not declared: orders.credit_override.authorised_by_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS ix_credit_override_authorised_by_principal_id ON orders.credit_override (authorised_by_principal_id);
-- convention, not declared: orders.deposit.rental_agreement_id -> rental.agreement
CREATE INDEX IF NOT EXISTS ix_deposit_rental_agreement_id ON orders.deposit (rental_agreement_id);
-- convention, not declared: orders.deposit_box.closed_by_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS ix_deposit_box_closed_by_principal_id ON orders.deposit_box (closed_by_principal_id);
-- convention, not declared: orders.discount.promotion_id -> promotions.promotion
CREATE INDEX IF NOT EXISTS ix_discount_promotion_id ON orders.discount (promotion_id);
-- convention, not declared: orders.group_booking.leader_subject_id -> pii.subject
CREATE INDEX IF NOT EXISTS ix_group_booking_leader_subject_id ON orders.group_booking (leader_subject_id);
-- convention, not declared: orders.invitation.issued_by_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS ix_invitation_issued_by_principal_id ON orders.invitation (issued_by_principal_id);
-- convention, not declared: orders.invitation.offered_by_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS ix_invitation_offered_by_principal_id ON orders.invitation (offered_by_principal_id);
-- convention, not declared: orders.membership_renewal.customer_membership_id -> identity.customer_membership
CREATE INDEX IF NOT EXISTS ix_membership_renewal_customer_membership_id ON orders.membership_renewal (customer_membership_id);
-- convention, not declared: orders.membership_renewal.entitlement_template_id -> catalogue.entitlement_template
CREATE INDEX IF NOT EXISTS ix_membership_renewal_entitlement_template_id ON orders.membership_renewal (entitlement_template_id);
-- convention, not declared: orders.order_fee.payment_method_id -> payments.method
CREATE INDEX IF NOT EXISTS ix_order_fee_payment_method_id ON orders.order_fee (payment_method_id);
-- convention, not declared: orders.order_fee.rule_id -> approvals.rule
CREATE INDEX IF NOT EXISTS ix_order_fee_rule_id ON orders.order_fee (rule_id);
-- convention, not declared: orders.order_line.inventory_hold_id -> catalogue.inventory_hold
CREATE INDEX IF NOT EXISTS ix_order_line_inventory_hold_id ON orders.order_line (inventory_hold_id);
-- convention, not declared: orders.payment_link.issued_by_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS ix_payment_link_issued_by_principal_id ON orders.payment_link (issued_by_principal_id);
-- convention, not declared: orders.payment_link.reservation_id -> orders.reservation
CREATE INDEX IF NOT EXISTS ix_payment_link_reservation_id ON orders.payment_link (reservation_id);
-- convention, not declared: orders.refund.tax_reversal_entry_id -> queue.entry
CREATE INDEX IF NOT EXISTS ix_refund_tax_reversal_entry_id ON orders.refund (tax_reversal_entry_id);
-- convention, not declared: orders.resale_listing.seller_subject_id -> pii.subject
CREATE INDEX IF NOT EXISTS ix_resale_listing_seller_subject_id ON orders.resale_listing (seller_subject_id);
-- convention, not declared: orders.resale_listing.sold_to_subject_id -> pii.subject
CREATE INDEX IF NOT EXISTS ix_resale_listing_sold_to_subject_id ON orders.resale_listing (sold_to_subject_id);
-- convention, not declared: orders.upgrade.new_order_line_id -> orders.order_line
CREATE INDEX IF NOT EXISTS ix_upgrade_new_order_line_id ON orders.upgrade (new_order_line_id);
-- convention, not declared: orders.upgrade.original_order_line_id -> orders.order_line
CREATE INDEX IF NOT EXISTS ix_upgrade_original_order_line_id ON orders.upgrade (original_order_line_id);
-- convention, not declared: orders.upgrade.requested_by_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS ix_upgrade_requested_by_principal_id ON orders.upgrade (requested_by_principal_id);
-- convention, not declared: orders.upgrade.rule_id -> approvals.rule
CREATE INDEX IF NOT EXISTS ix_upgrade_rule_id ON orders.upgrade (rule_id);
-- convention, not declared: payments.authentication_policy.mandate_text_asset_id -> assets.media_asset
CREATE INDEX IF NOT EXISTS ix_authentication_policy_mandate_text_asset_id ON payments.authentication_policy (mandate_text_asset_id);
-- convention, not declared: payments.chargeback_evidence.chargeback_id -> orders.chargeback
CREATE INDEX IF NOT EXISTS ix_chargeback_evidence_chargeback_id ON payments.chargeback_evidence (chargeback_id);
-- convention, not declared: payments.deposit_activity.created_by_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS ix_deposit_activity_created_by_principal_id ON payments.deposit_activity (created_by_principal_id);
-- convention, not declared: payments.deposit_activity.deposit_id -> payments.deposit_activity
CREATE INDEX IF NOT EXISTS ix_deposit_activity_deposit_id ON payments.deposit_activity (deposit_id);
-- convention, not declared: payments.dunning_case.resolved_by_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS ix_dunning_case_resolved_by_principal_id ON payments.dunning_case (resolved_by_principal_id);
-- convention, not declared: payments.dunning_case.subject_id -> pii.subject
CREATE INDEX IF NOT EXISTS ix_dunning_case_subject_id ON payments.dunning_case (subject_id);
-- convention, not declared: payments.eligibility_rule.payment_method_id -> payments.method
CREATE INDEX IF NOT EXISTS ix_eligibility_rule_payment_method_id ON payments.eligibility_rule (payment_method_id);
-- convention, not declared: payments.fee_rule.payment_method_id -> payments.method
CREATE INDEX IF NOT EXISTS ix_fee_rule_payment_method_id ON payments.fee_rule (payment_method_id);
-- convention, not declared: payments.fee_rule.provider_id -> payments.provider
CREATE INDEX IF NOT EXISTS ix_fee_rule_provider_id ON payments.fee_rule (provider_id);
-- convention, not declared: payments.hosted_checkout.branding_asset_id -> assets.media_asset
CREATE INDEX IF NOT EXISTS ix_hosted_checkout_branding_asset_id ON payments.hosted_checkout (branding_asset_id);
-- convention, not declared: payments.merchant_account.legal_entity_id -> ledger.legal_entity
CREATE INDEX IF NOT EXISTS ix_merchant_account_legal_entity_id ON payments.merchant_account (legal_entity_id);
-- convention, not declared: payments.method_config.payment_method_id -> payments.method
CREATE INDEX IF NOT EXISTS ix_method_config_payment_method_id ON payments.method_config (payment_method_id);
-- convention, not declared: payments.payment_terms.account_id -> ledger.account
CREATE INDEX IF NOT EXISTS ix_payment_terms_account_id ON payments.payment_terms (account_id);
-- convention, not declared: payments.provider_connection.merchant_account_id -> payments.merchant_account
CREATE INDEX IF NOT EXISTS ix_provider_connection_merchant_account_id ON payments.provider_connection (merchant_account_id);
-- convention, not declared: payments.reconciliation_source.connection_id -> payments.provider_connection
CREATE INDEX IF NOT EXISTS ix_reconciliation_source_connection_id ON payments.reconciliation_source (connection_id);
-- convention, not declared: payments.routing_rule.fallback_provider_id -> payments.provider
CREATE INDEX IF NOT EXISTS ix_routing_rule_fallback_provider_id ON payments.routing_rule (fallback_provider_id);
-- convention, not declared: payments.stored_forward.device_id -> platform.device
CREATE INDEX IF NOT EXISTS ix_stored_forward_device_id ON payments.stored_forward (device_id);
-- convention, not declared: payments.terminal.acquirer_connection_id -> payments.provider_connection
CREATE INDEX IF NOT EXISTS ix_terminal_acquirer_connection_id ON payments.terminal (acquirer_connection_id);
-- convention, not declared: payments.terminal.device_id -> platform.device
CREATE INDEX IF NOT EXISTS ix_terminal_device_id ON payments.terminal (device_id);
-- convention, not declared: payments.terminal.merchant_account_id -> payments.merchant_account
CREATE INDEX IF NOT EXISTS ix_terminal_merchant_account_id ON payments.terminal (merchant_account_id);
-- convention, not declared: pii.subject.erasure_request_id -> approvals.request
CREATE INDEX IF NOT EXISTS ix_subject_erasure_request_id ON pii.subject (erasure_request_id);
-- convention, not declared: pii.subject_biometric.guardian_subject_id -> pii.subject
CREATE INDEX IF NOT EXISTS ix_subject_biometric_guardian_subject_id ON pii.subject_biometric (guardian_subject_id);
-- convention, not declared: platform.cross_region_entitlement.admission_rules_id -> access.admission_rules
CREATE INDEX IF NOT EXISTS ix_cross_region_entitlement_admission_rules_id ON platform.cross_region_entitlement (admission_rules_id);
-- convention, not declared: platform.dead_letter.outbox_id -> platform.outbox
CREATE INDEX IF NOT EXISTS ix_dead_letter_outbox_id ON platform.dead_letter (outbox_id);
-- convention, not declared: platform.device.configuration_profile_id -> platform.configuration_profile
CREATE INDEX IF NOT EXISTS ix_device_configuration_profile_id ON platform.device (configuration_profile_id);
-- convention, not declared: platform.profile_deployment.profile_id -> platform.configuration_profile
CREATE INDEX IF NOT EXISTS ix_profile_deployment_profile_id ON platform.profile_deployment (profile_id);
-- convention, not declared: platform.wallet_authorisation.authorisation_id -> games.authorisation
CREATE INDEX IF NOT EXISTS ix_wallet_authorisation_authorisation_id ON platform.wallet_authorisation (authorisation_id);
-- convention, not declared: platform.wallet_authorisation.fx_rate_id -> ledger.fx_rate
CREATE INDEX IF NOT EXISTS ix_wallet_authorisation_fx_rate_id ON platform.wallet_authorisation (fx_rate_id);
-- convention, not declared: platform.workstation.configuration_profile_id -> platform.configuration_profile
CREATE INDEX IF NOT EXISTS ix_workstation_configuration_profile_id ON platform.workstation (configuration_profile_id);
-- convention, not declared: pricing.dynamic_price_action.dynamic_price_rule_id -> pricing.dynamic_price_rule
CREATE INDEX IF NOT EXISTS ix_dynamic_price_action_dynamic_price_rule_id ON pricing.dynamic_price_action (dynamic_price_rule_id);
-- convention, not declared: pricing.dynamic_price_action.rule_id -> approvals.rule
CREATE INDEX IF NOT EXISTS ix_dynamic_price_action_rule_id ON pricing.dynamic_price_action (rule_id);
-- convention, not declared: pricing.dynamic_price_condition.dynamic_price_rule_id -> pricing.dynamic_price_rule
CREATE INDEX IF NOT EXISTS ix_dynamic_price_condition_dynamic_price_rule_id ON pricing.dynamic_price_condition (dynamic_price_rule_id);
-- convention, not declared: pricing.dynamic_price_condition.rule_id -> approvals.rule
CREATE INDEX IF NOT EXISTS ix_dynamic_price_condition_rule_id ON pricing.dynamic_price_condition (rule_id);
-- convention, not declared: pricing.dynamic_price_rule.price_list_id -> catalogue.price_list
CREATE INDEX IF NOT EXISTS ix_dynamic_price_rule_price_list_id ON pricing.dynamic_price_rule (price_list_id);
-- convention, not declared: promotions.product_relationship.from_product_id -> promotions.product_relationship
CREATE INDEX IF NOT EXISTS ix_product_relationship_from_product_id ON promotions.product_relationship (from_product_id);
-- convention, not declared: promotions.product_relationship.to_product_id -> promotions.product_relationship
CREATE INDEX IF NOT EXISTS ix_product_relationship_to_product_id ON promotions.product_relationship (to_product_id);
-- convention, not declared: queue.queue.parent_queue_id -> queue.queue
CREATE INDEX IF NOT EXISTS ix_queue_parent_queue_id ON queue.queue (parent_queue_id);
-- convention, not declared: rental.agreement_item.asset_id -> maintenance.asset
CREATE INDEX IF NOT EXISTS ix_agreement_item_asset_id ON rental.agreement_item (asset_id);
-- convention, not declared: rental.agreement_item.catalogue_product_id -> rental.product
CREATE INDEX IF NOT EXISTS ix_agreement_item_catalogue_product_id ON rental.agreement_item (catalogue_product_id);
-- convention, not declared: rental.agreement_item.inventory_item_id -> inventory.item
CREATE INDEX IF NOT EXISTS ix_agreement_item_inventory_item_id ON rental.agreement_item (inventory_item_id);
-- convention, not declared: rental.agreement_item.order_line_id -> orders.order_line
CREATE INDEX IF NOT EXISTS ix_agreement_item_order_line_id ON rental.agreement_item (order_line_id);
-- convention, not declared: rental.agreement_item.rental_agreement_id -> rental.agreement
CREATE INDEX IF NOT EXISTS ix_agreement_item_rental_agreement_id ON rental.agreement_item (rental_agreement_id);
-- convention, not declared: rental.agreement_item.resource_booking_id -> rental.booking
CREATE INDEX IF NOT EXISTS ix_agreement_item_resource_booking_id ON rental.agreement_item (resource_booking_id);
-- convention, not declared: rental.agreement_item.resource_id -> resources.resource
CREATE INDEX IF NOT EXISTS ix_agreement_item_resource_id ON rental.agreement_item (resource_id);
-- convention, not declared: rental.agreement_item.stock_reservation_id -> inventory.stock_reservation
CREATE INDEX IF NOT EXISTS ix_agreement_item_stock_reservation_id ON rental.agreement_item (stock_reservation_id);
-- convention, not declared: rental.agreement_rules.terms_document_asset_id -> assets.media_asset
CREATE INDEX IF NOT EXISTS ix_agreement_rules_terms_document_asset_id ON rental.agreement_rules (terms_document_asset_id);
-- convention, not declared: rental.agreement_signature.document_asset_id -> assets.media_asset
CREATE INDEX IF NOT EXISTS ix_agreement_signature_document_asset_id ON rental.agreement_signature (document_asset_id);
-- convention, not declared: rental.agreement_signature.participant_id -> rental.participant
CREATE INDEX IF NOT EXISTS ix_agreement_signature_participant_id ON rental.agreement_signature (participant_id);
-- convention, not declared: rental.agreement_signature.signature_asset_id -> assets.media_asset
CREATE INDEX IF NOT EXISTS ix_agreement_signature_signature_asset_id ON rental.agreement_signature (signature_asset_id);
-- convention, not declared: rental.blackout.location_id -> inventory.location
CREATE INDEX IF NOT EXISTS ix_blackout_location_id ON rental.blackout (location_id);
-- convention, not declared: rental.booking.deposit_authorisation_id -> games.authorisation
CREATE INDEX IF NOT EXISTS ix_booking_deposit_authorisation_id ON rental.booking (deposit_authorisation_id);
-- convention, not declared: rental.booking.location_id -> inventory.location
CREATE INDEX IF NOT EXISTS ix_booking_location_id ON rental.booking (location_id);
-- convention, not declared: rental.booking.return_location_id -> inventory.location
CREATE INDEX IF NOT EXISTS ix_booking_return_location_id ON rental.booking (return_location_id);
-- convention, not declared: rental.damage_assessment.asset_id -> maintenance.asset
CREATE INDEX IF NOT EXISTS ix_damage_assessment_asset_id ON rental.damage_assessment (asset_id);
-- convention, not declared: rental.damage_assessment.inspection_id -> rental.inspection
CREATE INDEX IF NOT EXISTS ix_damage_assessment_inspection_id ON rental.damage_assessment (inspection_id);
-- convention, not declared: rental.damage_assessment.work_order_id -> maintenance.work_order
CREATE INDEX IF NOT EXISTS ix_damage_assessment_work_order_id ON rental.damage_assessment (work_order_id);
-- convention, not declared: rental.equipment_assignment.asset_id -> maintenance.asset
CREATE INDEX IF NOT EXISTS ix_equipment_assignment_asset_id ON rental.equipment_assignment (asset_id);
-- convention, not declared: rental.incident.asset_id -> maintenance.asset
CREATE INDEX IF NOT EXISTS ix_incident_asset_id ON rental.incident (asset_id);
-- convention, not declared: rental.incident.booking_id -> rental.booking
CREATE INDEX IF NOT EXISTS ix_incident_booking_id ON rental.incident (booking_id);
-- convention, not declared: rental.incident.work_order_id -> maintenance.work_order
CREATE INDEX IF NOT EXISTS ix_incident_work_order_id ON rental.incident (work_order_id);
-- convention, not declared: rental.inspection.asset_id -> maintenance.asset
CREATE INDEX IF NOT EXISTS ix_inspection_asset_id ON rental.inspection (asset_id);
-- convention, not declared: rental.inspection_item.rental_agreement_item_id -> rental.agreement_item
CREATE INDEX IF NOT EXISTS ix_inspection_item_rental_agreement_item_id ON rental.inspection_item (rental_agreement_item_id);
-- convention, not declared: rental.inspection_item.rental_inspection_id -> rental.inspection
CREATE INDEX IF NOT EXISTS ix_inspection_item_rental_inspection_id ON rental.inspection_item (rental_inspection_id);
-- convention, not declared: rental.location_rule.location_id -> inventory.location
CREATE INDEX IF NOT EXISTS ix_location_rule_location_id ON rental.location_rule (location_id);
-- convention, not declared: rental.override.approval_request_id -> approvals.request
CREATE INDEX IF NOT EXISTS ix_override_approval_request_id ON rental.override (approval_request_id);
-- convention, not declared: rental.override.booking_id -> rental.booking
CREATE INDEX IF NOT EXISTS ix_override_booking_id ON rental.override (booking_id);
-- convention, not declared: rental.pricing_profile.customer_segment_id -> marketing.segment
CREATE INDEX IF NOT EXISTS ix_pricing_profile_customer_segment_id ON rental.pricing_profile (customer_segment_id);
-- convention, not declared: rental.product.catalogue_product_id -> rental.product
CREATE INDEX IF NOT EXISTS ix_product_catalogue_product_id ON rental.product (catalogue_product_id);
-- convention, not declared: rental.product.image_asset_id -> assets.media_asset
CREATE INDEX IF NOT EXISTS ix_product_image_asset_id ON rental.product (image_asset_id);
-- convention, not declared: rental.product.resource_type_id -> resources.resource_type
CREATE INDEX IF NOT EXISTS ix_product_resource_type_id ON rental.product (resource_type_id);
-- convention, not declared: rental.settlement.booking_id -> rental.booking
CREATE INDEX IF NOT EXISTS ix_settlement_booking_id ON rental.settlement (booking_id);
-- convention, not declared: reporting.alert.acknowledged_by_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS ix_alert_acknowledged_by_principal_id ON reporting.alert (acknowledged_by_principal_id);
-- convention, not declared: reporting.delivery.subscription_id -> reporting.subscription
CREATE INDEX IF NOT EXISTS ix_delivery_subscription_id ON reporting.delivery (subscription_id);
-- convention, not declared: reporting.kpi_target.kpi_id -> reporting.kpi_definition
CREATE INDEX IF NOT EXISTS ix_kpi_target_kpi_id ON reporting.kpi_target (kpi_id);
-- convention, not declared: reporting.subscription.runs_as_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS ix_subscription_runs_as_principal_id ON reporting.subscription (runs_as_principal_id);
-- convention, not declared: reporting.subscription.schedule_id -> reporting.schedule
CREATE INDEX IF NOT EXISTS ix_subscription_schedule_id ON reporting.subscription (schedule_id);
-- convention, not declared: resources.booking.deposit_authorisation_id -> games.authorisation
CREATE INDEX IF NOT EXISTS ix_booking_deposit_authorisation_id ON resources.booking (deposit_authorisation_id);
-- convention, not declared: resources.qualification.document_asset_id -> assets.media_asset
CREATE INDEX IF NOT EXISTS ix_qualification_document_asset_id ON resources.qualification (document_asset_id);
-- convention, not declared: resources.resource.parent_resource_id -> resources.resource
CREATE INDEX IF NOT EXISTS ix_resource_parent_resource_id ON resources.resource (parent_resource_id);
-- convention, not declared: resources.resource_audit.resource_id -> resources.resource
CREATE INDEX IF NOT EXISTS ix_resource_audit_resource_id ON resources.resource_audit (resource_id);
-- convention, not declared: resources.resource_block.resource_id -> resources.resource
CREATE INDEX IF NOT EXISTS ix_resource_block_resource_id ON resources.resource_block (resource_id);
-- convention, not declared: resources.resource_category.parent_category_id -> resources.resource_category
CREATE INDEX IF NOT EXISTS ix_resource_category_parent_category_id ON resources.resource_category (parent_category_id);
-- convention, not declared: resources.resource_dependency.target_resource_id -> resources.resource
CREATE INDEX IF NOT EXISTS ix_resource_dependency_target_resource_id ON resources.resource_dependency (target_resource_id);
-- convention, not declared: resources.resource_dependency.target_resource_type_id -> resources.resource_type
CREATE INDEX IF NOT EXISTS ix_resource_dependency_target_resource_type_id ON resources.resource_dependency (target_resource_type_id);
-- convention, not declared: resources.resource_relation.resource_id -> resources.resource
CREATE INDEX IF NOT EXISTS ix_resource_relation_resource_id ON resources.resource_relation (resource_id);
-- convention, not declared: resources.resource_requirement.category_id -> resources.resource_category
CREATE INDEX IF NOT EXISTS ix_resource_requirement_category_id ON resources.resource_requirement (category_id);
-- convention, not declared: resources.resource_requirement.resource_id -> resources.resource
CREATE INDEX IF NOT EXISTS ix_resource_requirement_resource_id ON resources.resource_requirement (resource_id);
-- convention, not declared: resources.resource_requirement.resource_type_id -> resources.resource_type
CREATE INDEX IF NOT EXISTS ix_resource_requirement_resource_type_id ON resources.resource_requirement (resource_type_id);
-- convention, not declared: resources.resource_schedule.resource_id -> resources.resource
CREATE INDEX IF NOT EXISTS ix_resource_schedule_resource_id ON resources.resource_schedule (resource_id);
-- convention, not declared: resources.venue_assignment.primary_venue_id -> resources.venue_assignment
CREATE INDEX IF NOT EXISTS ix_venue_assignment_primary_venue_id ON resources.venue_assignment (primary_venue_id);
-- convention, not declared: retail.product_recommendation.source_product_id -> retail.product_recommendation
CREATE INDEX IF NOT EXISTS ix_product_recommendation_source_product_id ON retail.product_recommendation (source_product_id);
-- convention, not declared: retail.product_recommendation.source_variant_id -> catalogue.variant
CREATE INDEX IF NOT EXISTS ix_product_recommendation_source_variant_id ON retail.product_recommendation (source_variant_id);
-- convention, not declared: retail.product_recommendation.target_product_id -> retail.product_recommendation
CREATE INDEX IF NOT EXISTS ix_product_recommendation_target_product_id ON retail.product_recommendation (target_product_id);
-- convention, not declared: retail.product_recommendation.target_variant_id -> catalogue.variant
CREATE INDEX IF NOT EXISTS ix_product_recommendation_target_variant_id ON retail.product_recommendation (target_variant_id);
-- convention, not declared: retail.store_rule.outlet_id -> platform.outlet
CREATE INDEX IF NOT EXISTS ix_store_rule_outlet_id ON retail.store_rule (outlet_id);
-- convention, not declared: seating.accessible.seat_map_id -> seating.seat_map
CREATE INDEX IF NOT EXISTS ix_accessible_seat_map_id ON seating.accessible (seat_map_id);
-- convention, not declared: seating.group_request.performance_id -> catalogue.performance
CREATE INDEX IF NOT EXISTS ix_group_request_performance_id ON seating.group_request (performance_id);
-- convention, not declared: seating.hold_pool.hold_type_id -> seating.hold_type
CREATE INDEX IF NOT EXISTS ix_hold_pool_hold_type_id ON seating.hold_pool (hold_type_id);
-- convention, not declared: seating.hold_pool.performance_id -> catalogue.performance
CREATE INDEX IF NOT EXISTS ix_hold_pool_performance_id ON seating.hold_pool (performance_id);
-- convention, not declared: seating.recommendation_rules.performance_id -> catalogue.performance
CREATE INDEX IF NOT EXISTS ix_recommendation_rules_performance_id ON seating.recommendation_rules (performance_id);
-- convention, not declared: seating.recommendation_rules.seat_map_id -> seating.seat_map
CREATE INDEX IF NOT EXISTS ix_recommendation_rules_seat_map_id ON seating.recommendation_rules (seat_map_id);
-- convention, not declared: seating.seat.category_id -> seating.seat_category
CREATE INDEX IF NOT EXISTS ix_seat_category_id ON seating.seat (category_id);
-- convention, not declared: seating.seat_block_item.block_id -> seating.seat_block
CREATE INDEX IF NOT EXISTS ix_seat_block_item_block_id ON seating.seat_block_item (block_id);
-- convention, not declared: seating.seat_block_item.seat_id -> seating.seat
CREATE INDEX IF NOT EXISTS ix_seat_block_item_seat_id ON seating.seat_block_item (seat_id);
-- convention, not declared: seating.seat_hold_item.hold_id -> wallet.hold
CREATE INDEX IF NOT EXISTS ix_seat_hold_item_hold_id ON seating.seat_hold_item (hold_id);
-- convention, not declared: seating.seat_hold_item.seat_id -> seating.seat
CREATE INDEX IF NOT EXISTS ix_seat_hold_item_seat_id ON seating.seat_hold_item (seat_id);
-- convention, not declared: seating.seat_rules.seat_map_id -> seating.seat_map
CREATE INDEX IF NOT EXISTS ix_seat_rules_seat_map_id ON seating.seat_rules (seat_map_id);
-- convention, not declared: subscription.capacity_pack.invoice_id -> control.invoice
CREATE INDEX IF NOT EXISTS ix_capacity_pack_invoice_id ON subscription.capacity_pack (invoice_id);
-- convention, not declared: subscription.partner_quote.agreement_id -> rental.agreement
CREATE INDEX IF NOT EXISTS ix_partner_quote_agreement_id ON subscription.partner_quote (agreement_id);
-- convention, not declared: subscription.partner_quote.partner_id -> subscription.partner_quote
CREATE INDEX IF NOT EXISTS ix_partner_quote_partner_id ON subscription.partner_quote (partner_id);
-- convention, not declared: subscription.tier_allowance.tier_id -> subscription.tier_module
CREATE INDEX IF NOT EXISTS ix_tier_allowance_tier_id ON subscription.tier_allowance (tier_id);
-- convention, not declared: subscription.tier_module.tier_id -> subscription.tier_allowance
CREATE INDEX IF NOT EXISTS ix_tier_module_tier_id ON subscription.tier_module (tier_id);
-- convention, not declared: sync.cell_connection.source_cell_id -> control.cell
CREATE INDEX IF NOT EXISTS ix_cell_connection_source_cell_id ON sync.cell_connection (source_cell_id);
-- convention, not declared: sync.cell_connection.target_cell_id -> control.cell
CREATE INDEX IF NOT EXISTS ix_cell_connection_target_cell_id ON sync.cell_connection (target_cell_id);
-- convention, not declared: sync.cross_cell_request.guest_link_id -> platform.guest_link
CREATE INDEX IF NOT EXISTS ix_cross_cell_request_guest_link_id ON sync.cross_cell_request (guest_link_id);
-- convention, not declared: sync.cross_cell_request.source_cell_id -> control.cell
CREATE INDEX IF NOT EXISTS ix_cross_cell_request_source_cell_id ON sync.cross_cell_request (source_cell_id);
-- convention, not declared: sync.cross_cell_request.target_cell_id -> control.cell
CREATE INDEX IF NOT EXISTS ix_cross_cell_request_target_cell_id ON sync.cross_cell_request (target_cell_id);
-- convention, not declared: tenancy.device_assignment.assigned_workstation_id -> platform.workstation
CREATE INDEX IF NOT EXISTS ix_device_assignment_assigned_workstation_id ON tenancy.device_assignment (assigned_workstation_id);
-- convention, not declared: tenancy.device_assignment.custodian_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS ix_device_assignment_custodian_principal_id ON tenancy.device_assignment (custodian_principal_id);
-- convention, not declared: tenancy.device_assignment.device_id -> platform.device
CREATE INDEX IF NOT EXISTS ix_device_assignment_device_id ON tenancy.device_assignment (device_id);
-- convention, not declared: tenancy.device_audit.actor_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS ix_device_audit_actor_principal_id ON tenancy.device_audit (actor_principal_id);
-- convention, not declared: tenancy.device_audit.device_id -> platform.device
CREATE INDEX IF NOT EXISTS ix_device_audit_device_id ON tenancy.device_audit (device_id);
-- convention, not declared: tenancy.device_credential.device_id -> platform.device
CREATE INDEX IF NOT EXISTS ix_device_credential_device_id ON tenancy.device_credential (device_id);
-- convention, not declared: tenancy.device_firmware.artefact_asset_id -> assets.media_asset
CREATE INDEX IF NOT EXISTS ix_device_firmware_artefact_asset_id ON tenancy.device_firmware (artefact_asset_id);
-- convention, not declared: tenancy.device_rollout.firmware_id -> tenancy.device_firmware
CREATE INDEX IF NOT EXISTS ix_device_rollout_firmware_id ON tenancy.device_rollout (firmware_id);
-- convention, not declared: tenancy.device_tamper_event.device_id -> platform.device
CREATE INDEX IF NOT EXISTS ix_device_tamper_event_device_id ON tenancy.device_tamper_event (device_id);
-- convention, not declared: tenancy.device_telemetry.device_id -> platform.device
CREATE INDEX IF NOT EXISTS ix_device_telemetry_device_id ON tenancy.device_telemetry (device_id);
-- convention, not declared: venuemap.map.base_asset_id -> maintenance.asset
CREATE INDEX IF NOT EXISTS ix_map_base_asset_id ON venuemap.map (base_asset_id);
-- convention, not declared: venuemap.path.from_point_id -> venuemap.point
CREATE INDEX IF NOT EXISTS ix_path_from_point_id ON venuemap.path (from_point_id);
-- convention, not declared: venuemap.path.restricted_by_point_id -> venuemap.point
CREATE INDEX IF NOT EXISTS ix_path_restricted_by_point_id ON venuemap.path (restricted_by_point_id);
-- convention, not declared: venuemap.path.to_point_id -> venuemap.point
CREATE INDEX IF NOT EXISTS ix_path_to_point_id ON venuemap.path (to_point_id);
-- convention, not declared: wallet.adjustment.wallet_id -> wallet.wallet
CREATE INDEX IF NOT EXISTS ix_adjustment_wallet_id ON wallet.adjustment (wallet_id);
-- convention, not declared: wallet.balance.wallet_balance_id -> wallet.balance
CREATE INDEX IF NOT EXISTS ix_balance_wallet_balance_id ON wallet.balance (wallet_balance_id);
-- convention, not declared: wallet.balance.wallet_id -> wallet.wallet
CREATE INDEX IF NOT EXISTS ix_balance_wallet_id ON wallet.balance (wallet_id);
-- convention, not declared: wallet.credential.replaced_by_credential_id -> wallet.credential
CREATE INDEX IF NOT EXISTS ix_credential_replaced_by_credential_id ON wallet.credential (replaced_by_credential_id);
-- convention, not declared: wallet.credential.wallet_id -> wallet.wallet
CREATE INDEX IF NOT EXISTS ix_credential_wallet_id ON wallet.credential (wallet_id);
-- convention, not declared: wallet.credit_eligibility.credit_type_id -> wallet.credit_type
CREATE INDEX IF NOT EXISTS ix_credit_eligibility_credit_type_id ON wallet.credit_eligibility (credit_type_id);
-- convention, not declared: wallet.credit_lot.credit_type_id -> wallet.credit_type
CREATE INDEX IF NOT EXISTS ix_credit_lot_credit_type_id ON wallet.credit_lot (credit_type_id);
-- convention, not declared: wallet.credit_lot.wallet_id -> wallet.wallet
CREATE INDEX IF NOT EXISTS ix_credit_lot_wallet_id ON wallet.credit_lot (wallet_id);
-- convention, not declared: wallet.dispute.adjustment_id -> wallet.adjustment
CREATE INDEX IF NOT EXISTS ix_dispute_adjustment_id ON wallet.dispute (adjustment_id);
-- convention, not declared: wallet.dispute.wallet_id -> wallet.wallet
CREATE INDEX IF NOT EXISTS ix_dispute_wallet_id ON wallet.dispute (wallet_id);
-- convention, not declared: wallet.funding_rules.wallet_type_id -> wallet.wallet_type
CREATE INDEX IF NOT EXISTS ix_funding_rules_wallet_type_id ON wallet.funding_rules (wallet_type_id);
-- convention, not declared: wallet.gift_card_product.credit_type_id -> wallet.credit_type
CREATE INDEX IF NOT EXISTS ix_gift_card_product_credit_type_id ON wallet.gift_card_product (credit_type_id);
-- convention, not declared: wallet.hold.payment_id -> orders.payment
CREATE INDEX IF NOT EXISTS ix_hold_payment_id ON wallet.hold (payment_id);
-- convention, not declared: wallet.hold.wallet_hold_id -> wallet.hold
CREATE INDEX IF NOT EXISTS ix_hold_wallet_hold_id ON wallet.hold (wallet_hold_id);
-- convention, not declared: wallet.hold.wallet_id -> wallet.wallet
CREATE INDEX IF NOT EXISTS ix_hold_wallet_id ON wallet.hold (wallet_id);
-- convention, not declared: wallet.refund_policy.wallet_refund_credit_type_id -> wallet.credit_type
CREATE INDEX IF NOT EXISTS ix_refund_policy_wallet_refund_credit_type_id ON wallet.refund_policy (wallet_refund_credit_type_id);
-- convention, not declared: wallet.restriction.wallet_id -> wallet.wallet
CREATE INDEX IF NOT EXISTS ix_restriction_wallet_id ON wallet.restriction (wallet_id);
-- convention, not declared: wallet.shared_wallet.owner_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS ix_shared_wallet_owner_principal_id ON wallet.shared_wallet (owner_principal_id);
-- convention, not declared: wallet.shared_wallet.wallet_id -> wallet.wallet
CREATE INDEX IF NOT EXISTS ix_shared_wallet_wallet_id ON wallet.shared_wallet (wallet_id);
-- convention, not declared: wallet.shared_wallet_member.subject_id -> pii.subject
CREATE INDEX IF NOT EXISTS ix_shared_wallet_member_subject_id ON wallet.shared_wallet_member (subject_id);
-- convention, not declared: whitelabel.custom_domain.tenant_id -> whitelabel.tenant_config
CREATE INDEX IF NOT EXISTS ix_custom_domain_tenant_id ON whitelabel.custom_domain (tenant_id);
-- convention, not declared: workforce.announcement.published_by_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS ix_announcement_published_by_principal_id ON workforce.announcement (published_by_principal_id);
-- convention, not declared: workforce.attendance.amended_by_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS ix_attendance_amended_by_principal_id ON workforce.attendance (amended_by_principal_id);
-- convention, not declared: workforce.employee.manager_employee_id -> workforce.employee
CREATE INDEX IF NOT EXISTS ix_employee_manager_employee_id ON workforce.employee (manager_employee_id);
-- convention, not declared: workforce.employee.principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS ix_employee_principal_id ON workforce.employee (principal_id);
-- convention, not declared: workforce.employment.employee_id -> workforce.employee
CREATE INDEX IF NOT EXISTS ix_employment_employee_id ON workforce.employment (employee_id);
-- convention, not declared: workforce.leave_balance.employee_id -> workforce.employee
CREATE INDEX IF NOT EXISTS ix_leave_balance_employee_id ON workforce.leave_balance (employee_id);
-- convention, not declared: workforce.leave_balance.type_id -> workforce.leave_type
CREATE INDEX IF NOT EXISTS ix_leave_balance_type_id ON workforce.leave_balance (type_id);
-- convention, not declared: workforce.leave_request.principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS ix_leave_request_principal_id ON workforce.leave_request (principal_id);
-- convention, not declared: workforce.open_shift.rota_assignment_id -> workforce.rota_assignment
CREATE INDEX IF NOT EXISTS ix_open_shift_rota_assignment_id ON workforce.open_shift (rota_assignment_id);
-- convention, not declared: workforce.open_shift.shift_template_id -> workforce.shift_template
CREATE INDEX IF NOT EXISTS ix_open_shift_shift_template_id ON workforce.open_shift (shift_template_id);
-- convention, not declared: workforce.rota_assignment.required_role_id -> identity.role
CREATE INDEX IF NOT EXISTS ix_rota_assignment_required_role_id ON workforce.rota_assignment (required_role_id);
-- convention, not declared: workforce.shift_swap.from_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS ix_shift_swap_from_principal_id ON workforce.shift_swap (from_principal_id);
-- convention, not declared: workforce.shift_swap.to_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS ix_shift_swap_to_principal_id ON workforce.shift_swap (to_principal_id);
-- convention, not declared: workforce.sync_conflict.employee_id -> workforce.employee
CREATE INDEX IF NOT EXISTS ix_sync_conflict_employee_id ON workforce.sync_conflict (employee_id);
-- convention, not declared: workforce.sync_conflict.resolved_by_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS ix_sync_conflict_resolved_by_principal_id ON workforce.sync_conflict (resolved_by_principal_id);
-- convention, not declared: workforce.sync_conflict.sync_run_id -> workforce.sync_run
CREATE INDEX IF NOT EXISTS ix_sync_conflict_sync_run_id ON workforce.sync_conflict (sync_run_id);
-- convention, not declared: workforce.training_record.principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS ix_training_record_principal_id ON workforce.training_record (principal_id);
-- convention, not declared: workforce.work_assignment.employee_id -> workforce.employee
CREATE INDEX IF NOT EXISTS ix_work_assignment_employee_id ON workforce.work_assignment (employee_id);
-- convention, not declared: workforce.work_assignment.job_title_id -> workforce.job_title
CREATE INDEX IF NOT EXISTS ix_work_assignment_job_title_id ON workforce.work_assignment (job_title_id);
-- convention, not declared: workforce.work_assignment.outlet_id -> platform.outlet
CREATE INDEX IF NOT EXISTS ix_work_assignment_outlet_id ON workforce.work_assignment (outlet_id);
-- crosses the database boundary: ai.provider.tenant_id -> control.tenant
CREATE INDEX IF NOT EXISTS ix_provider_tenant_id ON ai.provider (tenant_id);
-- crosses the database boundary: platform.cell_endpoint.cell_id -> control.cell
CREATE INDEX IF NOT EXISTS ix_cell_endpoint_cell_id ON platform.cell_endpoint (cell_id);
-- crosses the database boundary: whitelabel.tenant_config.footer -> control.footer_config
CREATE INDEX IF NOT EXISTS ix_tenant_config_footer ON whitelabel.tenant_config (footer);
CREATE INDEX IF NOT EXISTS ix_access_decision_scope ON identity.access_decision (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_access_override_scope ON identity.access_override (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_access_point_scope ON access.access_point (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_access_policy_scope ON identity.access_policy (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_access_policy_version_scope ON identity.access_policy_version (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_access_profile_scope ON accreditation.access_profile (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_accessible_scope ON seating.accessible (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_accounting_mapping_scope ON wallet.accounting_mapping (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_activity_scope ON ai.activity (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_adjustment_scope ON wallet.adjustment (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_admission_rules_scope ON access.admission_rules (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_agreement_rules_scope ON rental.agreement_rules (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_agreement_signature_scope ON rental.agreement_signature (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_alert_rule_scope ON reporting.alert_rule (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_alert_scope ON reporting.alert (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_allocation_policy_scope ON resources.allocation_policy (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_anomaly_scope ON reporting.anomaly (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_application_scope ON accreditation.application (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_approval_scope ON assets.approval (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_approver_availability_scope ON approvals.approver_availability (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_asset_category_scope ON maintenance.asset_category (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_asset_version_scope ON assets.asset_version (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_attraction_type_scope ON games.attraction_type (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_attribute_definition_scope ON resources.attribute_definition (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_audience_activation_scope ON marketing.audience_activation (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_audience_list_scope ON marketing.audience_list (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_audit_scope ON accreditation.audit (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_audit_scope ON assets.audit (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_authentication_policy_scope ON payments.authentication_policy (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_authorisation_scope ON games.authorisation (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_availability_rules_scope ON rental.availability_rules (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_b2b_credit_scope ON orders.b2b_credit (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_badge_template_scope ON accreditation.badge_template (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_blacklist_scope ON access.blacklist (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_blackout_scope ON rental.blackout (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_booking_scope ON rental.booking (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_capability_template_scope ON identity.capability_template (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_card_expiry_rules_scope ON games.card_expiry_rules (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_challenge_scope ON marketing.challenge (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_channel_rules_scope ON wallet.channel_rules (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_chargeback_evidence_scope ON payments.chargeback_evidence (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_config_version_scope ON whitelabel.config_version (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_configuration_profile_scope ON platform.configuration_profile (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_configuration_version_scope ON wallet.configuration_version (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_connectivity_policy_scope ON platform.connectivity_policy (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_consumption_policy_scope ON wallet.consumption_policy (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_content_page_scope ON whitelabel.content_page (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_control_policy_scope ON approvals.control_policy (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_conversation_scope ON ai.conversation (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_corrective_action_scope ON fnb.corrective_action (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_coupon_code_scope ON promotions.coupon_code (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_credential_scope ON accreditation.credential (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_credential_scope ON wallet.credential (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_credit_account_scope ON payments.credit_account (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_credit_eligibility_scope ON wallet.credit_eligibility (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_credit_lot_scope ON wallet.credit_lot (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_credit_type_scope ON wallet.credit_type (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_currency_rule_scope ON payments.currency_rule (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_damage_assessment_scope ON rental.damage_assessment (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_dead_letter_scope ON platform.dead_letter (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_decision_record_scope ON approvals.decision_record (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_delegated_access_scope ON identity.delegated_access (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_delegation_scope ON approvals.delegation (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_delivery_scope ON reporting.delivery (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_deposit_policy_scope ON rental.deposit_policy (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_device_assignment_scope ON tenancy.device_assignment (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_device_audit_scope ON tenancy.device_audit (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_device_credential_scope ON tenancy.device_credential (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_device_rollout_scope ON tenancy.device_rollout (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_device_tamper_event_scope ON tenancy.device_tamper_event (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_device_telemetry_scope ON tenancy.device_telemetry (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_dispute_scope ON wallet.dispute (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_distribution_channel_scope ON assets.distribution_channel (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_document_scope ON accreditation.document (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_dunning_case_scope ON payments.dunning_case (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_dunning_policy_scope ON payments.dunning_policy (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_duplicate_candidate_scope ON marketing.duplicate_candidate (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_duration_rules_scope ON rental.duration_rules (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_dynamic_price_rule_scope ON pricing.dynamic_price_rule (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_eligibility_rule_scope ON payments.eligibility_rule (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_entitlement_scope ON access.entitlement (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_entitlement_scope ON games.entitlement (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_entitlement_template_scope ON catalogue.entitlement_template (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_equipment_assignment_scope ON rental.equipment_assignment (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_event_capacity_profile_scope ON catalogue.event_capacity_profile (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_event_registration_scope ON catalogue.event_registration (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_event_reschedule_scope ON catalogue.event_reschedule (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_event_resource_plan_scope ON catalogue.event_resource_plan (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_event_schedule_scope ON catalogue.event_schedule (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_event_scope ON catalogue.event (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_event_type_scope ON catalogue.event_type (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_evidence_package_scope ON approvals.evidence_package (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_failover_policy_scope ON payments.failover_policy (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_faq_category_scope ON whitelabel.faq_category (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_fee_policy_scope ON rental.fee_policy (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_field_ownership_scope ON workforce.field_ownership (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_form_definition_scope ON marketing.form_definition (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_fraud_rule_scope ON orders.fraud_rule (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_funding_rules_scope ON wallet.funding_rules (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_gameplay_transaction_scope ON games.gameplay_transaction (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_gift_card_product_scope ON wallet.gift_card_product (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_group_request_scope ON seating.group_request (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_guest_attribute_model_scope ON marketing.guest_attribute_model (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_guest_relationship_scope ON marketing.guest_relationship (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_hold_pool_scope ON seating.hold_pool (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_hold_type_scope ON seating.hold_type (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_holder_access_scope ON accreditation.holder_access (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_holder_scope ON accreditation.holder (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_hosted_checkout_scope ON payments.hosted_checkout (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_identity_rules_scope ON marketing.identity_rules (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_import_job_scope ON catalogue.import_job (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_incident_scope ON rental.incident (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_inspection_scope ON rental.inspection (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_integration_source_scope ON workforce.integration_source (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_inventory_model_scope ON rental.inventory_model (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_invitation_campaign_scope ON marketing.invitation_campaign (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_invitation_scope ON marketing.invitation (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_journey_enrollment_scope ON marketing.journey_enrollment (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_journey_scope ON marketing.journey (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_kiosk_config_scope ON games.kiosk_config (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_knowledge_collection_scope ON ai.knowledge_collection (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_kpi_definition_scope ON reporting.kpi_definition (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_kpi_target_scope ON reporting.kpi_target (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_layout_draft_scope ON ai.layout_draft (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_leave_request_scope ON workforce.leave_request (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_legal_entity_scope ON ledger.legal_entity (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_location_rule_scope ON rental.location_rule (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_map_scope ON venuemap.map (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_matching_rules_scope ON payments.matching_rules (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_matrix_scope ON approvals.matrix (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_merchant_account_scope ON payments.merchant_account (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_message_trigger_scope ON marketing.message_trigger (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_method_config_scope ON payments.method_config (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_method_scope ON payments.method (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_mixed_tender_rules_scope ON payments.mixed_tender_rules (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_modifier_group_scope ON fnb.modifier_group (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_module_access_scope ON identity.module_access (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_notification_rules_scope ON accreditation.notification_rules (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_offline_policy_scope ON platform.offline_policy (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_open_shift_scope ON workforce.open_shift (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_operational_config_scope ON games.operational_config (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_operational_rules_scope ON rental.operational_rules (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_outbox_scope ON platform.outbox (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_override_scope ON rental.override (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_password_policy_scope ON identity.password_policy (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_payment_link_scope ON orders.payment_link (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_payment_terms_scope ON payments.payment_terms (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_pipeline_scope ON reporting.pipeline (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_policy_scope ON whitelabel.policy (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_pos_shift_scope ON orders.pos_shift (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_prepaid_minutes_scope ON catalogue.prepaid_minutes (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_pricing_profile_scope ON rental.pricing_profile (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_pricing_scope ON games.pricing (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_print_job_scope ON accreditation.print_job (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_privacy_incident_scope ON marketing.privacy_incident (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_prize_cost_scope ON games.prize_cost (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_product_category_scope ON catalogue.product_category (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_product_recommendation_scope ON fnb.product_recommendation (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_product_recommendation_scope ON retail.product_recommendation (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_product_relationship_scope ON promotions.product_relationship (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_product_scope ON catalogue.product (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_product_scope ON rental.product (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_programme_scope ON accreditation.programme (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_promo_block_scope ON whitelabel.promo_block (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_provider_connection_scope ON payments.provider_connection (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_provider_scope ON ai.provider (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_provider_scope ON payments.provider (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_purchase_order_scope ON inventory.purchase_order (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_qualification_scope ON resources.qualification (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_quotation_scope ON inventory.quotation (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_reader_profile_scope ON games.reader_profile (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_reader_scope ON games.reader (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_reassignment_scope ON seating.reassignment (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_recommendation_experiment_scope ON promotions.recommendation_experiment (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_recommendation_outcome_scope ON promotions.recommendation_outcome (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_recommendation_rules_scope ON seating.recommendation_rules (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_recommendation_strategy_scope ON promotions.recommendation_strategy (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_recommendation_suppression_scope ON promotions.recommendation_suppression (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_reconciliation_source_scope ON payments.reconciliation_source (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_redemption_rules_scope ON games.redemption_rules (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_referral_scope ON marketing.referral (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_refund_policy_scope ON wallet.refund_policy (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_rendition_scope ON assets.rendition (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_report_definition_scope ON reporting.report_definition (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_request_scope ON approvals.request (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_requirements_scope ON accreditation.requirements (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_resale_listing_scope ON orders.resale_listing (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_resource_audit_scope ON resources.resource_audit (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_resource_block_scope ON resources.resource_block (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_resource_category_scope ON resources.resource_category (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_resource_dependency_scope ON resources.resource_dependency (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_resource_package_scope ON resources.resource_package (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_resource_relation_scope ON resources.resource_relation (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_resource_requirement_scope ON resources.resource_requirement (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_resource_schedule_scope ON resources.resource_schedule (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_resource_scope ON resources.resource (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_resource_type_scope ON resources.resource_type (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_restriction_scope ON wallet.restriction (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_retention_policy_scope ON approvals.retention_policy (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_retention_policy_scope ON marketing.retention_policy (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_risk_rules_scope ON payments.risk_rules (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_risk_rules_scope ON wallet.risk_rules (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_routing_rule_scope ON payments.routing_rule (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_sales_order_scope ON orders.sales_order (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_scan_event_scope ON access.scan_event (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_seat_block_scope ON seating.seat_block (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_seat_rules_scope ON seating.seat_rules (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_section_scope ON seating.section (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_segregation_rule_scope ON identity.segregation_rule (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_semantic_model_scope ON reporting.semantic_model (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_session_template_scope ON catalogue.session_template (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_settlement_scope ON ledger.settlement (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_settlement_scope ON rental.settlement (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_share_scope ON assets.share (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_shared_wallet_scope ON wallet.shared_wallet (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_shift_template_scope ON workforce.shift_template (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_signature_scope ON approvals.signature (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_sla_policy_scope ON approvals.sla_policy (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_sla_policy_scope ON marketing.sla_policy (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_space_scope ON catalogue.space (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_sso_group_mapping_scope ON identity.sso_group_mapping (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_sso_provider_scope ON identity.sso_provider (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_staffing_rules_scope ON workforce.staffing_rules (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_stored_forward_scope ON payments.stored_forward (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_stored_value_authorisation_scope ON orders.stored_value_authorisation (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_subscription_scope ON reporting.subscription (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_suggestion_scope ON ai.suggestion (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_supplier_scope ON inventory.supplier (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_suppression_scope ON marketing.suppression (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_sync_conflict_scope ON workforce.sync_conflict (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_sync_run_scope ON workforce.sync_run (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_tag_scope ON assets.tag (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_taxonomy_scope ON assets.taxonomy (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_terminal_scope ON payments.terminal (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_transfer_rules_scope ON wallet.transfer_rules (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_transfer_scope ON inventory.transfer (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_validation_rules_scope ON games.validation_rules (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_validity_scope ON accreditation.validity (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_venue_assignment_scope ON resources.venue_assignment (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_voucher_type_scope ON wallet.voucher_type (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_wallet_pass_scope ON orders.wallet_pass (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_wallet_type_scope ON wallet.wallet_type (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_work_assignment_scope ON workforce.work_assignment (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_workstation_scope ON platform.workstation (scope_path text_pattern_ops);
