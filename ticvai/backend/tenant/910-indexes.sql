-- Indexes in the tenant database: declared foreign keys, conventions and scope paths.
-- **Derived by tools/derive-ddl.py. Do not hand-edit.**
--
-- **Every declared foreign key is indexed** (data-and-storage.md) -- Postgres does not
-- index the referencing column itself. **A convention is indexed and not constrained**
-- (ADR-0011): most references are naming habits the contracts never asserted, and
-- enforcing one fails on the first row that legitimately points nowhere.
-- Names follow naming-and-style 6.1: `<table>_<columns>_idx`.

-- convention, not declared: access.access_change.changed_by_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS access_change_changed_by_principal_id_idx ON access.access_change (changed_by_principal_id);
-- convention, not declared: access.access_change.new_access_id -> access.access_point
CREATE INDEX IF NOT EXISTS access_change_new_access_id_idx ON access.access_change (new_access_id);
-- convention, not declared: access.access_change.old_access_id -> access.access_point
CREATE INDEX IF NOT EXISTS access_change_old_access_id_idx ON access.access_change (old_access_id);
-- convention, not declared: access.access_change.upgrade_id -> orders.upgrade
CREATE INDEX IF NOT EXISTS access_change_upgrade_id_idx ON access.access_change (upgrade_id);
-- convention, not declared: access.entitlement.order_line_id -> orders.order_line
CREATE INDEX IF NOT EXISTS entitlement_order_line_id_idx ON access.entitlement (order_line_id);
-- convention, not declared: access.entitlement.subject_id -> pii.subject
CREATE INDEX IF NOT EXISTS entitlement_subject_id_idx ON access.entitlement (subject_id);
-- convention, not declared: access.entitlement.supersedes_entitlement_id -> access.entitlement
CREATE INDEX IF NOT EXISTS entitlement_supersedes_entitlement_id_idx ON access.entitlement (supersedes_entitlement_id);
-- convention, not declared: access.entry_rule_point.access_point_id -> access.access_point
CREATE INDEX IF NOT EXISTS entry_rule_point_access_point_id_idx ON access.entry_rule_point (access_point_id);
-- convention, not declared: accreditation.application.approval_request_id -> approvals.request
CREATE INDEX IF NOT EXISTS application_approval_request_id_idx ON accreditation.application (approval_request_id);
-- convention, not declared: accreditation.application.holder_id -> accreditation.holder
CREATE INDEX IF NOT EXISTS application_holder_id_idx ON accreditation.application (holder_id);
-- convention, not declared: accreditation.application.programme_id -> accreditation.programme
CREATE INDEX IF NOT EXISTS application_programme_id_idx ON accreditation.application (programme_id);
-- convention, not declared: accreditation.application.submitted_by_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS application_submitted_by_principal_id_idx ON accreditation.application (submitted_by_principal_id);
-- convention, not declared: accreditation.audit.actor_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS audit_actor_principal_id_idx ON accreditation.audit (actor_principal_id);
-- convention, not declared: accreditation.audit.approval_request_id -> approvals.request
CREATE INDEX IF NOT EXISTS audit_approval_request_id_idx ON accreditation.audit (approval_request_id);
-- convention, not declared: accreditation.audit.holder_id -> accreditation.holder
CREATE INDEX IF NOT EXISTS audit_holder_id_idx ON accreditation.audit (holder_id);
-- convention, not declared: accreditation.badge_template.background_asset_id -> assets.media_asset
CREATE INDEX IF NOT EXISTS badge_template_background_asset_id_idx ON accreditation.badge_template (background_asset_id);
-- convention, not declared: accreditation.credential.badge_template_id -> accreditation.badge_template
CREATE INDEX IF NOT EXISTS credential_badge_template_id_idx ON accreditation.credential (badge_template_id);
-- convention, not declared: accreditation.credential.holder_id -> accreditation.holder
CREATE INDEX IF NOT EXISTS credential_holder_id_idx ON accreditation.credential (holder_id);
-- convention, not declared: accreditation.credential.replaces_credential_id -> accreditation.credential
CREATE INDEX IF NOT EXISTS credential_replaces_credential_id_idx ON accreditation.credential (replaces_credential_id);
-- convention, not declared: accreditation.document.application_id -> accreditation.application
CREATE INDEX IF NOT EXISTS document_application_id_idx ON accreditation.document (application_id);
-- convention, not declared: accreditation.document.asset_id -> maintenance.asset
CREATE INDEX IF NOT EXISTS document_asset_id_idx ON accreditation.document (asset_id);
-- convention, not declared: accreditation.document.holder_id -> accreditation.holder
CREATE INDEX IF NOT EXISTS document_holder_id_idx ON accreditation.document (holder_id);
-- convention, not declared: accreditation.holder.photo_asset_id -> assets.media_asset
CREATE INDEX IF NOT EXISTS holder_photo_asset_id_idx ON accreditation.holder (photo_asset_id);
-- convention, not declared: accreditation.holder.programme_id -> accreditation.programme
CREATE INDEX IF NOT EXISTS holder_programme_id_idx ON accreditation.holder (programme_id);
-- convention, not declared: accreditation.holder.subject_id -> pii.subject
CREATE INDEX IF NOT EXISTS holder_subject_id_idx ON accreditation.holder (subject_id);
-- convention, not declared: accreditation.holder_access.holder_id -> accreditation.holder
CREATE INDEX IF NOT EXISTS holder_access_holder_id_idx ON accreditation.holder_access (holder_id);
-- convention, not declared: accreditation.notification_rules.programme_id -> accreditation.programme
CREATE INDEX IF NOT EXISTS notification_rules_programme_id_idx ON accreditation.notification_rules (programme_id);
-- convention, not declared: accreditation.print_job.printer_device_id -> platform.device
CREATE INDEX IF NOT EXISTS print_job_printer_device_id_idx ON accreditation.print_job (printer_device_id);
-- convention, not declared: accreditation.requirements.programme_id -> accreditation.programme
CREATE INDEX IF NOT EXISTS requirements_programme_id_idx ON accreditation.requirements (programme_id);
-- convention, not declared: accreditation.validity.programme_id -> accreditation.programme
CREATE INDEX IF NOT EXISTS validity_programme_id_idx ON accreditation.validity (programme_id);
-- convention, not declared: ai.activity.billable_to_tenant_id -> platform.tenant
CREATE INDEX IF NOT EXISTS activity_billable_to_tenant_id_idx ON ai.activity (billable_to_tenant_id);
-- convention, not declared: ai.index_failure.job_id -> ai.index_job
CREATE INDEX IF NOT EXISTS index_failure_job_id_idx ON ai.index_failure (job_id);
-- convention, not declared: ai.index_failure.source_id -> ai.index_source
CREATE INDEX IF NOT EXISTS index_failure_source_id_idx ON ai.index_failure (source_id);
-- convention, not declared: ai.knowledge_document.supersedes_document_id -> ai.knowledge_document
CREATE INDEX IF NOT EXISTS knowledge_document_supersedes_document_id_idx ON ai.knowledge_document (supersedes_document_id);
-- convention, not declared: ai.policy.fallback_provider_id -> ai.provider
CREATE INDEX IF NOT EXISTS policy_fallback_provider_id_idx ON ai.policy (fallback_provider_id);
-- convention, not declared: ai.provider.failover_provider_id -> ai.provider
CREATE INDEX IF NOT EXISTS provider_failover_provider_id_idx ON ai.provider (failover_provider_id);
-- convention, not declared: ai.provider.tenant_id -> platform.tenant
CREATE INDEX IF NOT EXISTS provider_tenant_id_idx ON ai.provider (tenant_id);
-- convention, not declared: ai.suggestion_outcome.decided_by_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS suggestion_outcome_decided_by_principal_id_idx ON ai.suggestion_outcome (decided_by_principal_id);
-- convention, not declared: ai.suggestion_outcome.suggestion_id -> ai.suggestion
CREATE INDEX IF NOT EXISTS suggestion_outcome_suggestion_id_idx ON ai.suggestion_outcome (suggestion_id);
-- convention, not declared: approvals.accreditation_badge.approval_request_id -> approvals.request
CREATE INDEX IF NOT EXISTS accreditation_badge_approval_request_id_idx ON approvals.accreditation_badge (approval_request_id);
-- convention, not declared: approvals.approver_availability.delegation_id -> approvals.delegation
CREATE INDEX IF NOT EXISTS approver_availability_delegation_id_idx ON approvals.approver_availability (delegation_id);
-- convention, not declared: approvals.approver_availability.principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS approver_availability_principal_id_idx ON approvals.approver_availability (principal_id);
-- convention, not declared: approvals.approver_availability.substitute_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS approver_availability_substitute_principal_id_idx ON approvals.approver_availability (substitute_principal_id);
-- convention, not declared: approvals.decision_record.request_id -> approvals.request
CREATE INDEX IF NOT EXISTS decision_record_request_id_idx ON approvals.decision_record (request_id);
-- convention, not declared: approvals.evidence_package.asset_id -> maintenance.asset
CREATE INDEX IF NOT EXISTS evidence_package_asset_id_idx ON approvals.evidence_package (asset_id);
-- convention, not declared: approvals.signature.request_id -> approvals.request
CREATE INDEX IF NOT EXISTS signature_request_id_idx ON approvals.signature (request_id);
-- convention, not declared: assets.media_collection.parent_collection_id -> assets.media_collection
CREATE INDEX IF NOT EXISTS media_collection_parent_collection_id_idx ON assets.media_collection (parent_collection_id);
-- convention, not declared: assets.media_collection_member.added_by_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS media_collection_member_added_by_principal_id_idx ON assets.media_collection_member (added_by_principal_id);
-- convention, not declared: assets.media_collection_member.asset_id -> assets.media_asset
CREATE INDEX IF NOT EXISTS media_collection_member_asset_id_idx ON assets.media_collection_member (asset_id);
-- convention, not declared: assets.media_collection_member.collection_id -> assets.media_collection
CREATE INDEX IF NOT EXISTS media_collection_member_collection_id_idx ON assets.media_collection_member (collection_id);
-- convention, not declared: assets.media_upload.asset_id -> assets.media_asset
CREATE INDEX IF NOT EXISTS media_upload_asset_id_idx ON assets.media_upload (asset_id);
-- convention, not declared: assets.media_upload.venue_id -> platform.scope
CREATE INDEX IF NOT EXISTS media_upload_venue_id_idx ON assets.media_upload (venue_id);
-- convention, not declared: catalogue.entitlement_template.renewal_variant_id -> catalogue.variant
CREATE INDEX IF NOT EXISTS entitlement_template_renewal_variant_id_idx ON catalogue.entitlement_template (renewal_variant_id);
-- convention, not declared: catalogue.event.parent_event_id -> catalogue.event
CREATE INDEX IF NOT EXISTS event_parent_event_id_idx ON catalogue.event (parent_event_id);
-- convention, not declared: catalogue.event_capacity_profile.event_id -> catalogue.event
CREATE INDEX IF NOT EXISTS event_capacity_profile_event_id_idx ON catalogue.event_capacity_profile (event_id);
-- convention, not declared: catalogue.event_capacity_profile.performance_id -> catalogue.performance
CREATE INDEX IF NOT EXISTS event_capacity_profile_performance_id_idx ON catalogue.event_capacity_profile (performance_id);
-- convention, not declared: catalogue.event_capacity_profile.seat_map_id -> seating.seat_map
CREATE INDEX IF NOT EXISTS event_capacity_profile_seat_map_id_idx ON catalogue.event_capacity_profile (seat_map_id);
-- convention, not declared: catalogue.event_registration.event_id -> catalogue.event
CREATE INDEX IF NOT EXISTS event_registration_event_id_idx ON catalogue.event_registration (event_id);
-- convention, not declared: catalogue.event_reschedule.approval_request_id -> approvals.request
CREATE INDEX IF NOT EXISTS event_reschedule_approval_request_id_idx ON catalogue.event_reschedule (approval_request_id);
-- convention, not declared: catalogue.event_reschedule.new_space_id -> catalogue.space
CREATE INDEX IF NOT EXISTS event_reschedule_new_space_id_idx ON catalogue.event_reschedule (new_space_id);
-- convention, not declared: catalogue.event_resource_plan.event_id -> catalogue.event
CREATE INDEX IF NOT EXISTS event_resource_plan_event_id_idx ON catalogue.event_resource_plan (event_id);
-- convention, not declared: catalogue.event_schedule.event_id -> catalogue.event
CREATE INDEX IF NOT EXISTS event_schedule_event_id_idx ON catalogue.event_schedule (event_id);
-- convention, not declared: catalogue.group_package.product_id -> catalogue.product
CREATE INDEX IF NOT EXISTS group_package_product_id_idx ON catalogue.group_package (product_id);
-- convention, not declared: catalogue.membership_benefit.entitlement_template_id -> catalogue.entitlement_template
CREATE INDEX IF NOT EXISTS membership_benefit_entitlement_template_id_idx ON catalogue.membership_benefit (entitlement_template_id);
-- convention, not declared: catalogue.performance.approval_request_id -> approvals.request
CREATE INDEX IF NOT EXISTS performance_approval_request_id_idx ON catalogue.performance (approval_request_id);
-- convention, not declared: catalogue.plan_benefit.entitlement_template_id -> catalogue.entitlement_template
CREATE INDEX IF NOT EXISTS plan_benefit_entitlement_template_id_idx ON catalogue.plan_benefit (entitlement_template_id);
-- convention, not declared: catalogue.plan_benefit.membership_benefit_id -> catalogue.membership_benefit
CREATE INDEX IF NOT EXISTS plan_benefit_membership_benefit_id_idx ON catalogue.plan_benefit (membership_benefit_id);
-- convention, not declared: catalogue.prepaid_minutes.credit_type_id -> wallet.credit_type
CREATE INDEX IF NOT EXISTS prepaid_minutes_credit_type_id_idx ON catalogue.prepaid_minutes (credit_type_id);
-- convention, not declared: catalogue.product.approved_by_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS product_approved_by_principal_id_idx ON catalogue.product (approved_by_principal_id);
-- convention, not declared: catalogue.product.category_id -> catalogue.product_category
CREATE INDEX IF NOT EXISTS product_category_id_idx ON catalogue.product (category_id);
-- convention, not declared: catalogue.product.created_by_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS product_created_by_principal_id_idx ON catalogue.product (created_by_principal_id);
-- convention, not declared: catalogue.product_category.image_asset_id -> assets.media_asset
CREATE INDEX IF NOT EXISTS product_category_image_asset_id_idx ON catalogue.product_category (image_asset_id);
-- convention, not declared: catalogue.product_eligibility_rule.product_id -> catalogue.product
CREATE INDEX IF NOT EXISTS product_eligibility_rule_product_id_idx ON catalogue.product_eligibility_rule (product_id);
-- convention, not declared: catalogue.product_version.published_by_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS product_version_published_by_principal_id_idx ON catalogue.product_version (published_by_principal_id);
-- convention, not declared: catalogue.session_template.space_id -> catalogue.space
CREATE INDEX IF NOT EXISTS session_template_space_id_idx ON catalogue.session_template (space_id);
-- convention, not declared: catalogue.space.parent_space_id -> catalogue.space
CREATE INDEX IF NOT EXISTS space_parent_space_id_idx ON catalogue.space (parent_space_id);
-- convention, not declared: catalogue.space.resource_id -> resources.resource
CREATE INDEX IF NOT EXISTS space_resource_id_idx ON catalogue.space (resource_id);
-- convention, not declared: catalogue.space.venue_map_zone_id -> seating.zone
CREATE INDEX IF NOT EXISTS space_venue_map_zone_id_idx ON catalogue.space (venue_map_zone_id);
-- convention, not declared: fnb.cold_chain_event.corrective_action_id -> fnb.corrective_action
CREATE INDEX IF NOT EXISTS cold_chain_event_corrective_action_id_idx ON fnb.cold_chain_event (corrective_action_id);
-- convention, not declared: fnb.cold_chain_event.goods_receipt_id -> inventory.goods_receipt
CREATE INDEX IF NOT EXISTS cold_chain_event_goods_receipt_id_idx ON fnb.cold_chain_event (goods_receipt_id);
-- convention, not declared: fnb.cold_chain_event.transfer_id -> inventory.transfer
CREATE INDEX IF NOT EXISTS cold_chain_event_transfer_id_idx ON fnb.cold_chain_event (transfer_id);
-- convention, not declared: fnb.combo.outlet_id -> platform.outlet
CREATE INDEX IF NOT EXISTS combo_outlet_id_idx ON fnb.combo (outlet_id);
-- convention, not declared: fnb.combo_slot.combo_id -> fnb.combo
CREATE INDEX IF NOT EXISTS combo_slot_combo_id_idx ON fnb.combo_slot (combo_id);
-- convention, not declared: fnb.corrective_action.escalated_to_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS corrective_action_escalated_to_principal_id_idx ON fnb.corrective_action (escalated_to_principal_id);
-- convention, not declared: fnb.corrective_action.raised_by_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS corrective_action_raised_by_principal_id_idx ON fnb.corrective_action (raised_by_principal_id);
-- convention, not declared: fnb.corrective_action.signed_by_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS corrective_action_signed_by_principal_id_idx ON fnb.corrective_action (signed_by_principal_id);
-- convention, not declared: fnb.course_rule.outlet_id -> platform.outlet
CREATE INDEX IF NOT EXISTS course_rule_outlet_id_idx ON fnb.course_rule (outlet_id);
-- convention, not declared: fnb.delivery_policy.outlet_id -> platform.outlet
CREATE INDEX IF NOT EXISTS delivery_policy_outlet_id_idx ON fnb.delivery_policy (outlet_id);
-- convention, not declared: fnb.ingredient_substitute.from_inventory_item_id -> inventory.item
CREATE INDEX IF NOT EXISTS ingredient_substitute_from_inventory_item_id_idx ON fnb.ingredient_substitute (from_inventory_item_id);
-- convention, not declared: fnb.ingredient_substitute.to_inventory_item_id -> inventory.item
CREATE INDEX IF NOT EXISTS ingredient_substitute_to_inventory_item_id_idx ON fnb.ingredient_substitute (to_inventory_item_id);
-- convention, not declared: fnb.kitchen_exception.outlet_id -> platform.outlet
CREATE INDEX IF NOT EXISTS kitchen_exception_outlet_id_idx ON fnb.kitchen_exception (outlet_id);
-- convention, not declared: fnb.kitchen_exception.raised_by_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS kitchen_exception_raised_by_principal_id_idx ON fnb.kitchen_exception (raised_by_principal_id);
-- convention, not declared: fnb.kitchen_exception.station_id -> fnb.kitchen_station
CREATE INDEX IF NOT EXISTS kitchen_exception_station_id_idx ON fnb.kitchen_exception (station_id);
-- convention, not declared: fnb.kitchen_exception.ticket_id -> fnb.kitchen_ticket
CREATE INDEX IF NOT EXISTS kitchen_exception_ticket_id_idx ON fnb.kitchen_exception (ticket_id);
-- convention, not declared: fnb.kitchen_ticket.order_id -> fnb.service_order
CREATE INDEX IF NOT EXISTS kitchen_ticket_order_id_idx ON fnb.kitchen_ticket (order_id);
-- convention, not declared: fnb.menu_item.menu_section_id -> fnb.menu_section
CREATE INDEX IF NOT EXISTS menu_item_menu_section_id_idx ON fnb.menu_item (menu_section_id);
-- convention, not declared: fnb.menu_item_modifier.group_id -> fnb.modifier_group
CREATE INDEX IF NOT EXISTS menu_item_modifier_group_id_idx ON fnb.menu_item_modifier (group_id);
-- convention, not declared: fnb.menu_item_modifier.item_id -> fnb.menu_item
CREATE INDEX IF NOT EXISTS menu_item_modifier_item_id_idx ON fnb.menu_item_modifier (item_id);
-- convention, not declared: fnb.menu_schedule.created_by_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS menu_schedule_created_by_principal_id_idx ON fnb.menu_schedule (created_by_principal_id);
-- convention, not declared: fnb.menu_schedule.menu_id -> fnb.menu
CREATE INDEX IF NOT EXISTS menu_schedule_menu_id_idx ON fnb.menu_schedule (menu_id);
-- convention, not declared: fnb.menu_version.menu_id -> fnb.menu
CREATE INDEX IF NOT EXISTS menu_version_menu_id_idx ON fnb.menu_version (menu_id);
-- convention, not declared: fnb.menu_version.published_by_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS menu_version_published_by_principal_id_idx ON fnb.menu_version (published_by_principal_id);
-- convention, not declared: fnb.order_fulfilment.service_order_id -> fnb.service_order
CREATE INDEX IF NOT EXISTS order_fulfilment_service_order_id_idx ON fnb.order_fulfilment (service_order_id);
-- convention, not declared: fnb.product_recommendation.source_product_id -> fnb.product_recommendation
CREATE INDEX IF NOT EXISTS product_recommendation_source_product_id_idx ON fnb.product_recommendation (source_product_id);
-- convention, not declared: fnb.product_recommendation.source_variant_id -> catalogue.variant
CREATE INDEX IF NOT EXISTS product_recommendation_source_variant_id_idx ON fnb.product_recommendation (source_variant_id);
-- convention, not declared: fnb.product_recommendation.target_product_id -> fnb.product_recommendation
CREATE INDEX IF NOT EXISTS product_recommendation_target_product_id_idx ON fnb.product_recommendation (target_product_id);
-- convention, not declared: fnb.product_recommendation.target_variant_id -> catalogue.variant
CREATE INDEX IF NOT EXISTS product_recommendation_target_variant_id_idx ON fnb.product_recommendation (target_variant_id);
-- convention, not declared: fnb.production_plan.based_on_suggestion_id -> ai.suggestion
CREATE INDEX IF NOT EXISTS production_plan_based_on_suggestion_id_idx ON fnb.production_plan (based_on_suggestion_id);
-- convention, not declared: fnb.production_plan.outlet_id -> platform.outlet
CREATE INDEX IF NOT EXISTS production_plan_outlet_id_idx ON fnb.production_plan (outlet_id);
-- convention, not declared: fnb.production_plan_line.station_id -> fnb.kitchen_station
CREATE INDEX IF NOT EXISTS production_plan_line_station_id_idx ON fnb.production_plan_line (station_id);
-- convention, not declared: fnb.production_run.producing_outlet_id -> platform.outlet
CREATE INDEX IF NOT EXISTS production_run_producing_outlet_id_idx ON fnb.production_run (producing_outlet_id);
-- convention, not declared: fnb.production_run.production_plan_id -> fnb.production_plan
CREATE INDEX IF NOT EXISTS production_run_production_plan_id_idx ON fnb.production_run (production_plan_id);
-- convention, not declared: fnb.reservation_policy.outlet_id -> platform.outlet
CREATE INDEX IF NOT EXISTS reservation_policy_outlet_id_idx ON fnb.reservation_policy (outlet_id);
-- convention, not declared: fnb.reservation_table.reservation_id -> fnb.table_reservation
CREATE INDEX IF NOT EXISTS reservation_table_reservation_id_idx ON fnb.reservation_table (reservation_id);
-- convention, not declared: fnb.service_order.sales_order_id -> orders.sales_order
CREATE INDEX IF NOT EXISTS service_order_sales_order_id_idx ON fnb.service_order (sales_order_id);
-- convention, not declared: fnb.service_order_line.menu_item_id -> fnb.menu_item
CREATE INDEX IF NOT EXISTS service_order_line_menu_item_id_idx ON fnb.service_order_line (menu_item_id);
-- convention, not declared: fnb.sold_out_item.called_by_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS sold_out_item_called_by_principal_id_idx ON fnb.sold_out_item (called_by_principal_id);
-- convention, not declared: fnb.sold_out_item.menu_item_id -> fnb.menu_item
CREATE INDEX IF NOT EXISTS sold_out_item_menu_item_id_idx ON fnb.sold_out_item (menu_item_id);
-- convention, not declared: fnb.sold_out_item.outlet_id -> platform.outlet
CREATE INDEX IF NOT EXISTS sold_out_item_outlet_id_idx ON fnb.sold_out_item (outlet_id);
-- convention, not declared: fnb.sub_bill.visit_id -> fnb.table_visit
CREATE INDEX IF NOT EXISTS sub_bill_visit_id_idx ON fnb.sub_bill (visit_id);
-- convention, not declared: fnb.substitution_rule.from_ingredient_id -> fnb.recipe_ingredient
CREATE INDEX IF NOT EXISTS substitution_rule_from_ingredient_id_idx ON fnb.substitution_rule (from_ingredient_id);
-- convention, not declared: fnb.substitution_rule.to_ingredient_id -> fnb.recipe_ingredient
CREATE INDEX IF NOT EXISTS substitution_rule_to_ingredient_id_idx ON fnb.substitution_rule (to_ingredient_id);
-- convention, not declared: fnb.table_combination.outlet_id -> platform.outlet
CREATE INDEX IF NOT EXISTS table_combination_outlet_id_idx ON fnb.table_combination (outlet_id);
-- convention, not declared: fnb.table_reservation.group_id -> fnb.modifier_group
CREATE INDEX IF NOT EXISTS table_reservation_group_id_idx ON fnb.table_reservation (group_id);
-- convention, not declared: fnb.table_visit.merged_into_visit_id -> fnb.table_visit
CREATE INDEX IF NOT EXISTS table_visit_merged_into_visit_id_idx ON fnb.table_visit (merged_into_visit_id);
-- convention, not declared: fnb.temperature_checkpoint.outlet_id -> platform.outlet
CREATE INDEX IF NOT EXISTS temperature_checkpoint_outlet_id_idx ON fnb.temperature_checkpoint (outlet_id);
-- convention, not declared: fnb.temperature_log.corrective_action_id -> fnb.corrective_action
CREATE INDEX IF NOT EXISTS temperature_log_corrective_action_id_idx ON fnb.temperature_log (corrective_action_id);
-- convention, not declared: fnb.temperature_log.recorded_by_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS temperature_log_recorded_by_principal_id_idx ON fnb.temperature_log (recorded_by_principal_id);
-- convention, not declared: games.authorisation.entitlement_id -> games.entitlement
CREATE INDEX IF NOT EXISTS authorisation_entitlement_id_idx ON games.authorisation (entitlement_id);
-- convention, not declared: games.game.reader_id -> games.reader
CREATE INDEX IF NOT EXISTS game_reader_id_idx ON games.game (reader_id);
-- convention, not declared: games.gameplay_transaction.card_id -> games.card
CREATE INDEX IF NOT EXISTS gameplay_transaction_card_id_idx ON games.gameplay_transaction (card_id);
-- convention, not declared: games.gameplay_transaction.entitlement_id -> games.entitlement
CREATE INDEX IF NOT EXISTS gameplay_transaction_entitlement_id_idx ON games.gameplay_transaction (entitlement_id);
-- convention, not declared: games.gameplay_transaction.game_id -> games.game
CREATE INDEX IF NOT EXISTS gameplay_transaction_game_id_idx ON games.gameplay_transaction (game_id);
-- convention, not declared: games.gameplay_transaction.reader_id -> games.reader
CREATE INDEX IF NOT EXISTS gameplay_transaction_reader_id_idx ON games.gameplay_transaction (reader_id);
-- convention, not declared: games.kiosk_config.kiosk_device_id -> platform.device
CREATE INDEX IF NOT EXISTS kiosk_config_kiosk_device_id_idx ON games.kiosk_config (kiosk_device_id);
-- convention, not declared: games.operational_config.game_id -> games.game
CREATE INDEX IF NOT EXISTS operational_config_game_id_idx ON games.operational_config (game_id);
-- convention, not declared: games.pricing.game_id -> games.game
CREATE INDEX IF NOT EXISTS pricing_game_id_idx ON games.pricing (game_id);
-- convention, not declared: games.prize_cost.inventory_item_id -> inventory.item
CREATE INDEX IF NOT EXISTS prize_cost_inventory_item_id_idx ON games.prize_cost (inventory_item_id);
-- convention, not declared: games.prize_cost.prize_id -> games.prize
CREATE INDEX IF NOT EXISTS prize_cost_prize_id_idx ON games.prize_cost (prize_id);
-- convention, not declared: games.reader.device_id -> platform.device
CREATE INDEX IF NOT EXISTS reader_device_id_idx ON games.reader (device_id);
-- convention, not declared: games.reader.game_id -> games.game
CREATE INDEX IF NOT EXISTS reader_game_id_idx ON games.reader (game_id);
-- convention, not declared: games.reader.reader_profile_id -> games.reader_profile
CREATE INDEX IF NOT EXISTS reader_reader_profile_id_idx ON games.reader (reader_profile_id);
-- convention, not declared: games.reader_deployment.reader_id -> games.reader
CREATE INDEX IF NOT EXISTS reader_deployment_reader_id_idx ON games.reader_deployment (reader_id);
-- convention, not declared: games.redemption_rules.ticket_credit_type_id -> wallet.credit_type
CREATE INDEX IF NOT EXISTS redemption_rules_ticket_credit_type_id_idx ON games.redemption_rules (ticket_credit_type_id);
-- convention, not declared: identity.access_decision.override_id -> identity.access_override
CREATE INDEX IF NOT EXISTS access_decision_override_id_idx ON identity.access_decision (override_id);
-- convention, not declared: identity.access_decision.principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS access_decision_principal_id_idx ON identity.access_decision (principal_id);
-- convention, not declared: identity.access_override.principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS access_override_principal_id_idx ON identity.access_override (principal_id);
-- convention, not declared: identity.access_policy_version.policy_id -> identity.access_policy
CREATE INDEX IF NOT EXISTS access_policy_version_policy_id_idx ON identity.access_policy_version (policy_id);
-- convention, not declared: identity.benefit_usage.customer_membership_id -> identity.customer_membership
CREATE INDEX IF NOT EXISTS benefit_usage_customer_membership_id_idx ON identity.benefit_usage (customer_membership_id);
-- convention, not declared: identity.benefit_usage.membership_benefit_id -> catalogue.membership_benefit
CREATE INDEX IF NOT EXISTS benefit_usage_membership_benefit_id_idx ON identity.benefit_usage (membership_benefit_id);
-- convention, not declared: identity.customer_membership.entitlement_template_id -> catalogue.entitlement_template
CREATE INDEX IF NOT EXISTS customer_membership_entitlement_template_id_idx ON identity.customer_membership (entitlement_template_id);
-- convention, not declared: identity.delegated_access.over_subject_id -> pii.subject
CREATE INDEX IF NOT EXISTS delegated_access_over_subject_id_idx ON identity.delegated_access (over_subject_id);
-- convention, not declared: identity.delegated_access.permission_id -> identity.permission
CREATE INDEX IF NOT EXISTS delegated_access_permission_id_idx ON identity.delegated_access (permission_id);
-- convention, not declared: identity.membership_history.changed_by_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS membership_history_changed_by_principal_id_idx ON identity.membership_history (changed_by_principal_id);
-- convention, not declared: identity.membership_history.customer_membership_id -> identity.customer_membership
CREATE INDEX IF NOT EXISTS membership_history_customer_membership_id_idx ON identity.membership_history (customer_membership_id);
-- convention, not declared: identity.module.parent_module_id -> identity.module
CREATE INDEX IF NOT EXISTS module_parent_module_id_idx ON identity.module (parent_module_id);
-- convention, not declared: identity.module_access.granted_by_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS module_access_granted_by_principal_id_idx ON identity.module_access (granted_by_principal_id);
-- convention, not declared: identity.module_access.principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS module_access_principal_id_idx ON identity.module_access (principal_id);
-- convention, not declared: identity.permission.module_id -> identity.module
CREATE INDEX IF NOT EXISTS permission_module_id_idx ON identity.permission (module_id);
-- convention, not declared: identity.refresh_token.principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS refresh_token_principal_id_idx ON identity.refresh_token (principal_id);
-- convention, not declared: identity.refresh_token.replaced_by_token_id -> identity.refresh_token
CREATE INDEX IF NOT EXISTS refresh_token_replaced_by_token_id_idx ON identity.refresh_token (replaced_by_token_id);
-- convention, not declared: identity.role.inherits_from_role_id -> identity.role
CREATE INDEX IF NOT EXISTS role_inherits_from_role_id_idx ON identity.role (inherits_from_role_id);
-- convention, not declared: identity.role_permission.granted_by_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS role_permission_granted_by_principal_id_idx ON identity.role_permission (granted_by_principal_id);
-- convention, not declared: identity.sso_provider.client_id -> control.api_client
CREATE INDEX IF NOT EXISTS sso_provider_client_id_idx ON identity.sso_provider (client_id);
-- convention, not declared: inventory.count.location_id -> inventory.location
CREATE INDEX IF NOT EXISTS count_location_id_idx ON inventory.count (location_id);
-- convention, not declared: inventory.count_line.batch_id -> inventory.stock_batch
CREATE INDEX IF NOT EXISTS count_line_batch_id_idx ON inventory.count_line (batch_id);
-- convention, not declared: inventory.count_line.counted_by_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS count_line_counted_by_principal_id_idx ON inventory.count_line (counted_by_principal_id);
-- convention, not declared: inventory.count_line.item_id -> inventory.item
CREATE INDEX IF NOT EXISTS count_line_item_id_idx ON inventory.count_line (item_id);
-- convention, not declared: inventory.count_line.location_id -> inventory.location
CREATE INDEX IF NOT EXISTS count_line_location_id_idx ON inventory.count_line (location_id);
-- convention, not declared: inventory.goods_receipt.location_id -> inventory.location
CREATE INDEX IF NOT EXISTS goods_receipt_location_id_idx ON inventory.goods_receipt (location_id);
-- convention, not declared: inventory.location.parent_location_id -> inventory.location
CREATE INDEX IF NOT EXISTS location_parent_location_id_idx ON inventory.location (parent_location_id);
-- convention, not declared: inventory.movement.location_id -> inventory.location
CREATE INDEX IF NOT EXISTS movement_location_id_idx ON inventory.movement (location_id);
-- convention, not declared: inventory.purchase_order.deliver_to_location_id -> inventory.location
CREATE INDEX IF NOT EXISTS purchase_order_deliver_to_location_id_idx ON inventory.purchase_order (deliver_to_location_id);
-- convention, not declared: inventory.purchase_order.quotation_id -> inventory.quotation
CREATE INDEX IF NOT EXISTS purchase_order_quotation_id_idx ON inventory.purchase_order (quotation_id);
-- convention, not declared: inventory.requisition.cost_center_id -> ledger.cost_center
CREATE INDEX IF NOT EXISTS requisition_cost_center_id_idx ON inventory.requisition (cost_center_id);
-- convention, not declared: inventory.serialised_item.batch_id -> inventory.stock_batch
CREATE INDEX IF NOT EXISTS serialised_item_batch_id_idx ON inventory.serialised_item (batch_id);
-- convention, not declared: inventory.serialised_item.item_id -> inventory.item
CREATE INDEX IF NOT EXISTS serialised_item_item_id_idx ON inventory.serialised_item (item_id);
-- convention, not declared: inventory.serialised_item.location_id -> inventory.location
CREATE INDEX IF NOT EXISTS serialised_item_location_id_idx ON inventory.serialised_item (location_id);
-- convention, not declared: inventory.stock_reservation.item_id -> inventory.item
CREATE INDEX IF NOT EXISTS stock_reservation_item_id_idx ON inventory.stock_reservation (item_id);
-- convention, not declared: inventory.stock_reservation.location_id -> inventory.location
CREATE INDEX IF NOT EXISTS stock_reservation_location_id_idx ON inventory.stock_reservation (location_id);
-- convention, not declared: inventory.supplier_contract.created_by_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS supplier_contract_created_by_principal_id_idx ON inventory.supplier_contract (created_by_principal_id);
-- convention, not declared: inventory.supplier_contract.supplier_id -> inventory.supplier
CREATE INDEX IF NOT EXISTS supplier_contract_supplier_id_idx ON inventory.supplier_contract (supplier_id);
-- convention, not declared: inventory.transfer.from_location_id -> inventory.location
CREATE INDEX IF NOT EXISTS transfer_from_location_id_idx ON inventory.transfer (from_location_id);
-- convention, not declared: inventory.transfer.to_location_id -> inventory.location
CREATE INDEX IF NOT EXISTS transfer_to_location_id_idx ON inventory.transfer (to_location_id);
-- convention, not declared: ledger.deposit.liability_account_id -> ledger.account
CREATE INDEX IF NOT EXISTS deposit_liability_account_id_idx ON ledger.deposit (liability_account_id);
-- convention, not declared: ledger.fiscal_period_event.approver_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS fiscal_period_event_approver_principal_id_idx ON ledger.fiscal_period_event (approver_principal_id);
-- convention, not declared: ledger.fiscal_period_event.principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS fiscal_period_event_principal_id_idx ON ledger.fiscal_period_event (principal_id);
-- convention, not declared: ledger.fx_rate.set_by_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS fx_rate_set_by_principal_id_idx ON ledger.fx_rate (set_by_principal_id);
-- convention, not declared: ledger.inter_entity_obligation.from_legal_entity_id -> ledger.legal_entity
CREATE INDEX IF NOT EXISTS inter_entity_obligation_from_legal_entity_id_idx ON ledger.inter_entity_obligation (from_legal_entity_id);
-- convention, not declared: ledger.inter_entity_obligation.to_legal_entity_id -> ledger.legal_entity
CREATE INDEX IF NOT EXISTS inter_entity_obligation_to_legal_entity_id_idx ON ledger.inter_entity_obligation (to_legal_entity_id);
-- convention, not declared: ledger.journal_entry.rejected_by_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS journal_entry_rejected_by_principal_id_idx ON ledger.journal_entry (rejected_by_principal_id);
-- convention, not declared: ledger.journal_entry.reversal_of_entry_id -> ledger.journal_entry
CREATE INDEX IF NOT EXISTS journal_entry_reversal_of_entry_id_idx ON ledger.journal_entry (reversal_of_entry_id);
-- convention, not declared: ledger.journal_entry.reversed_by_entry_id -> ledger.journal_entry
CREATE INDEX IF NOT EXISTS journal_entry_reversed_by_entry_id_idx ON ledger.journal_entry (reversed_by_entry_id);
-- convention, not declared: ledger.journal_line.account_id -> ledger.account
CREATE INDEX IF NOT EXISTS journal_line_account_id_idx ON ledger.journal_line (account_id);
-- convention, not declared: ledger.journal_line.cost_center_id -> ledger.cost_center
CREATE INDEX IF NOT EXISTS journal_line_cost_center_id_idx ON ledger.journal_line (cost_center_id);
-- convention, not declared: ledger.recognition_schedule.no_show_account_id -> ledger.account
CREATE INDEX IF NOT EXISTS recognition_schedule_no_show_account_id_idx ON ledger.recognition_schedule (no_show_account_id);
-- convention, not declared: ledger.tax_code.compound_on_tax_code_id -> ledger.tax_code
CREATE INDEX IF NOT EXISTS tax_code_compound_on_tax_code_id_idx ON ledger.tax_code (compound_on_tax_code_id);
-- convention, not declared: maintenance.asset.category_id -> maintenance.asset_category
CREATE INDEX IF NOT EXISTS asset_category_id_idx ON maintenance.asset (category_id);
-- convention, not declared: maintenance.asset.device_id -> platform.device
CREATE INDEX IF NOT EXISTS asset_device_id_idx ON maintenance.asset (device_id);
-- convention, not declared: maintenance.asset.resource_id -> resources.resource
CREATE INDEX IF NOT EXISTS asset_resource_id_idx ON maintenance.asset (resource_id);
-- convention, not declared: maintenance.asset_category.icon_asset_id -> assets.media_asset
CREATE INDEX IF NOT EXISTS asset_category_icon_asset_id_idx ON maintenance.asset_category (icon_asset_id);
-- convention, not declared: maintenance.asset_category.parent_category_id -> maintenance.asset_category
CREATE INDEX IF NOT EXISTS asset_category_parent_category_id_idx ON maintenance.asset_category (parent_category_id);
-- convention, not declared: maintenance.asset_document.asset_id -> maintenance.asset
CREATE INDEX IF NOT EXISTS asset_document_asset_id_idx ON maintenance.asset_document (asset_id);
-- convention, not declared: maintenance.asset_status_change.asset_id -> maintenance.asset
CREATE INDEX IF NOT EXISTS asset_status_change_asset_id_idx ON maintenance.asset_status_change (asset_id);
-- convention, not declared: maintenance.asset_status_change.changed_by_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS asset_status_change_changed_by_principal_id_idx ON maintenance.asset_status_change (changed_by_principal_id);
-- convention, not declared: maintenance.asset_status_change.inspection_id -> maintenance.inspection
CREATE INDEX IF NOT EXISTS asset_status_change_inspection_id_idx ON maintenance.asset_status_change (inspection_id);
-- convention, not declared: maintenance.asset_status_change.work_order_id -> maintenance.work_order
CREATE INDEX IF NOT EXISTS asset_status_change_work_order_id_idx ON maintenance.asset_status_change (work_order_id);
-- convention, not declared: maintenance.incident_authority_notification.incident_id -> maintenance.incident
CREATE INDEX IF NOT EXISTS incident_authority_notification_incident_id_idx ON maintenance.incident_authority_notification (incident_id);
-- convention, not declared: maintenance.incident_authority_notification.notified_by_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS incident_authority_notification_notified_by_principal_id_idx ON maintenance.incident_authority_notification (notified_by_principal_id);
-- convention, not declared: maintenance.incident_involved_party.incident_id -> maintenance.incident
CREATE INDEX IF NOT EXISTS incident_involved_party_incident_id_idx ON maintenance.incident_involved_party (incident_id);
-- convention, not declared: maintenance.incident_involved_party.principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS incident_involved_party_principal_id_idx ON maintenance.incident_involved_party (principal_id);
-- convention, not declared: maintenance.incident_involved_party.subject_id -> pii.subject
CREATE INDEX IF NOT EXISTS incident_involved_party_subject_id_idx ON maintenance.incident_involved_party (subject_id);
-- convention, not declared: maintenance.inspection.template_id -> maintenance.inspection_template
CREATE INDEX IF NOT EXISTS inspection_template_id_idx ON maintenance.inspection (template_id);
-- convention, not declared: maintenance.inspection_item.template_item_id -> maintenance.inspection_template_item
CREATE INDEX IF NOT EXISTS inspection_item_template_item_id_idx ON maintenance.inspection_item (template_item_id);
-- convention, not declared: maintenance.inspection_template.applies_to_asset_category_id -> maintenance.asset_category
CREATE INDEX IF NOT EXISTS inspection_template_applies_to_asset_category_id_idx ON maintenance.inspection_template (applies_to_asset_category_id);
-- convention, not declared: maintenance.preventive_plan.asset_category_id -> maintenance.asset_category
CREATE INDEX IF NOT EXISTS preventive_plan_asset_category_id_idx ON maintenance.preventive_plan (asset_category_id);
-- convention, not declared: maintenance.work_order.category_id -> maintenance.asset_category
CREATE INDEX IF NOT EXISTS work_order_category_id_idx ON maintenance.work_order (category_id);
-- convention, not declared: maintenance.work_order.closed_by_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS work_order_closed_by_principal_id_idx ON maintenance.work_order (closed_by_principal_id);
-- convention, not declared: maintenance.work_order.completed_by_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS work_order_completed_by_principal_id_idx ON maintenance.work_order (completed_by_principal_id);
-- convention, not declared: maintenance.work_order.duplicate_of_work_order_id -> maintenance.work_order
CREATE INDEX IF NOT EXISTS work_order_duplicate_of_work_order_id_idx ON maintenance.work_order (duplicate_of_work_order_id);
-- convention, not declared: maintenance.work_order.superseded_by_work_order_id -> maintenance.work_order
CREATE INDEX IF NOT EXISTS work_order_superseded_by_work_order_id_idx ON maintenance.work_order (superseded_by_work_order_id);
-- convention, not declared: maintenance.work_order.verified_by_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS work_order_verified_by_principal_id_idx ON maintenance.work_order (verified_by_principal_id);
-- convention, not declared: maintenance.work_order_attachment.captured_by_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS work_order_attachment_captured_by_principal_id_idx ON maintenance.work_order_attachment (captured_by_principal_id);
-- convention, not declared: marketing.audience_activation.approval_request_id -> approvals.request
CREATE INDEX IF NOT EXISTS audience_activation_approval_request_id_idx ON marketing.audience_activation (approval_request_id);
-- convention, not declared: marketing.audience_activation.segment_id -> marketing.segment
CREATE INDEX IF NOT EXISTS audience_activation_segment_id_idx ON marketing.audience_activation (segment_id);
-- convention, not declared: marketing.audience_list.asset_id -> maintenance.asset
CREATE INDEX IF NOT EXISTS audience_list_asset_id_idx ON marketing.audience_list (asset_id);
-- convention, not declared: marketing.campaign_target.campaign_id -> marketing.campaign
CREATE INDEX IF NOT EXISTS campaign_target_campaign_id_idx ON marketing.campaign_target (campaign_id);
-- convention, not declared: marketing.challenge.badge_asset_id -> assets.media_asset
CREATE INDEX IF NOT EXISTS challenge_badge_asset_id_idx ON marketing.challenge (badge_asset_id);
-- convention, not declared: marketing.conversation.assist_session_id -> marketing.kiosk_assist_session
CREATE INDEX IF NOT EXISTS conversation_assist_session_id_idx ON marketing.conversation (assist_session_id);
-- convention, not declared: marketing.conversation_message.sender_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS conversation_message_sender_principal_id_idx ON marketing.conversation_message (sender_principal_id);
-- convention, not declared: marketing.conversation_message_attachment.asset_id -> maintenance.asset
CREATE INDEX IF NOT EXISTS conversation_message_attachment_asset_id_idx ON marketing.conversation_message_attachment (asset_id);
-- convention, not declared: marketing.customer_badge.badge_id -> marketing.badge
CREATE INDEX IF NOT EXISTS customer_badge_badge_id_idx ON marketing.customer_badge (badge_id);
-- convention, not declared: marketing.customer_badge.challenge_id -> marketing.challenge
CREATE INDEX IF NOT EXISTS customer_badge_challenge_id_idx ON marketing.customer_badge (challenge_id);
-- convention, not declared: marketing.form_definition_field.consent_purpose_id -> marketing.consent_purpose
CREATE INDEX IF NOT EXISTS form_definition_field_consent_purpose_id_idx ON marketing.form_definition_field (consent_purpose_id);
-- convention, not declared: marketing.form_submission.on_behalf_of_subject_id -> pii.subject
CREATE INDEX IF NOT EXISTS form_submission_on_behalf_of_subject_id_idx ON marketing.form_submission (on_behalf_of_subject_id);
-- convention, not declared: marketing.form_submission.signature_asset_id -> assets.media_asset
CREATE INDEX IF NOT EXISTS form_submission_signature_asset_id_idx ON marketing.form_submission (signature_asset_id);
-- convention, not declared: marketing.guest_document.uploaded_by_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS guest_document_uploaded_by_principal_id_idx ON marketing.guest_document (uploaded_by_principal_id);
-- convention, not declared: marketing.guest_extra_field.tenant_id -> platform.tenant
CREATE INDEX IF NOT EXISTS guest_extra_field_tenant_id_idx ON marketing.guest_extra_field (tenant_id);
-- convention, not declared: marketing.guest_match_decision.cart_id -> orders.cart
CREATE INDEX IF NOT EXISTS guest_match_decision_cart_id_idx ON marketing.guest_match_decision (cart_id);
-- convention, not declared: marketing.guest_match_decision.matched_profile_id -> marketing.guest_profile
CREATE INDEX IF NOT EXISTS guest_match_decision_matched_profile_id_idx ON marketing.guest_match_decision (matched_profile_id);
-- convention, not declared: marketing.guest_note.author_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS guest_note_author_principal_id_idx ON marketing.guest_note (author_principal_id);
-- convention, not declared: marketing.guest_note.subject_id -> pii.subject
CREATE INDEX IF NOT EXISTS guest_note_subject_id_idx ON marketing.guest_note (subject_id);
-- convention, not declared: marketing.guest_preference.subject_id -> pii.subject
CREATE INDEX IF NOT EXISTS guest_preference_subject_id_idx ON marketing.guest_preference (subject_id);
-- convention, not declared: marketing.guest_profile.merged_into_subject_id -> pii.subject
CREATE INDEX IF NOT EXISTS guest_profile_merged_into_subject_id_idx ON marketing.guest_profile (merged_into_subject_id);
-- convention, not declared: marketing.guest_relationship.related_subject_id -> pii.subject
CREATE INDEX IF NOT EXISTS guest_relationship_related_subject_id_idx ON marketing.guest_relationship (related_subject_id);
-- convention, not declared: marketing.invitation.issued_by_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS invitation_issued_by_principal_id_idx ON marketing.invitation (issued_by_principal_id);
-- convention, not declared: marketing.invitation.offered_by_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS invitation_offered_by_principal_id_idx ON marketing.invitation (offered_by_principal_id);
-- convention, not declared: marketing.journey_enrollment.journey_id -> marketing.journey
CREATE INDEX IF NOT EXISTS journey_enrollment_journey_id_idx ON marketing.journey_enrollment (journey_id);
-- convention, not declared: marketing.journey_enrollment.step_id -> marketing.journey_step
CREATE INDEX IF NOT EXISTS journey_enrollment_step_id_idx ON marketing.journey_enrollment (step_id);
-- convention, not declared: marketing.journey_enrollment.subject_id -> pii.subject
CREATE INDEX IF NOT EXISTS journey_enrollment_subject_id_idx ON marketing.journey_enrollment (subject_id);
-- convention, not declared: marketing.journey_step.campaign_id -> marketing.campaign
CREATE INDEX IF NOT EXISTS journey_step_campaign_id_idx ON marketing.journey_step (campaign_id);
-- convention, not declared: marketing.journey_step.failure_journey_step_id -> marketing.journey_step
CREATE INDEX IF NOT EXISTS journey_step_failure_journey_step_id_idx ON marketing.journey_step (failure_journey_step_id);
-- convention, not declared: marketing.journey_step.message_template_id -> marketing.message_template
CREATE INDEX IF NOT EXISTS journey_step_message_template_id_idx ON marketing.journey_step (message_template_id);
-- convention, not declared: marketing.journey_step.next_journey_step_id -> marketing.journey_step
CREATE INDEX IF NOT EXISTS journey_step_next_journey_step_id_idx ON marketing.journey_step (next_journey_step_id);
-- convention, not declared: marketing.lost_item.case_id -> marketing.case
CREATE INDEX IF NOT EXISTS lost_item_case_id_idx ON marketing.lost_item (case_id);
-- convention, not declared: marketing.lost_item.matched_item_id -> marketing.lost_item
CREATE INDEX IF NOT EXISTS lost_item_matched_item_id_idx ON marketing.lost_item (matched_item_id);
-- convention, not declared: marketing.lost_item.reported_by_subject_id -> pii.subject
CREATE INDEX IF NOT EXISTS lost_item_reported_by_subject_id_idx ON marketing.lost_item (reported_by_subject_id);
-- convention, not declared: marketing.loyalty_campaign.campaign_id -> marketing.campaign
CREATE INDEX IF NOT EXISTS loyalty_campaign_campaign_id_idx ON marketing.loyalty_campaign (campaign_id);
-- convention, not declared: marketing.loyalty_points.author_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS loyalty_points_author_principal_id_idx ON marketing.loyalty_points (author_principal_id);
-- convention, not declared: marketing.loyalty_points.reversed_loyalty_points_id -> marketing.loyalty_points
CREATE INDEX IF NOT EXISTS loyalty_points_reversed_loyalty_points_id_idx ON marketing.loyalty_points (reversed_loyalty_points_id);
-- convention, not declared: marketing.loyalty_position.tier_id -> marketing.programme_tier
CREATE INDEX IF NOT EXISTS loyalty_position_tier_id_idx ON marketing.loyalty_position (tier_id);
-- convention, not declared: marketing.loyalty_rule.campaign_id -> marketing.campaign
CREATE INDEX IF NOT EXISTS loyalty_rule_campaign_id_idx ON marketing.loyalty_rule (campaign_id);
-- convention, not declared: marketing.loyalty_rule.points_earning_rule_id -> marketing.points_earning_rule
CREATE INDEX IF NOT EXISTS loyalty_rule_points_earning_rule_id_idx ON marketing.loyalty_rule (points_earning_rule_id);
-- convention, not declared: marketing.loyalty_rule.reward_id -> marketing.reward
CREATE INDEX IF NOT EXISTS loyalty_rule_reward_id_idx ON marketing.loyalty_rule (reward_id);
-- convention, not declared: marketing.message_dispatch.template_id -> marketing.message_template
CREATE INDEX IF NOT EXISTS message_dispatch_template_id_idx ON marketing.message_dispatch (template_id);
-- convention, not declared: marketing.message_template.provider_template_id -> marketing.message_template
CREATE INDEX IF NOT EXISTS message_template_provider_template_id_idx ON marketing.message_template (provider_template_id);
-- convention, not declared: marketing.message_trigger.template_id -> marketing.message_template
CREATE INDEX IF NOT EXISTS message_trigger_template_id_idx ON marketing.message_trigger (template_id);
-- convention, not declared: marketing.referral.referee_reward_id -> marketing.reward
CREATE INDEX IF NOT EXISTS referral_referee_reward_id_idx ON marketing.referral (referee_reward_id);
-- convention, not declared: marketing.referral.referee_subject_id -> pii.subject
CREATE INDEX IF NOT EXISTS referral_referee_subject_id_idx ON marketing.referral (referee_subject_id);
-- convention, not declared: marketing.referral.referrer_reward_id -> marketing.reward
CREATE INDEX IF NOT EXISTS referral_referrer_reward_id_idx ON marketing.referral (referrer_reward_id);
-- convention, not declared: marketing.referral.referrer_subject_id -> pii.subject
CREATE INDEX IF NOT EXISTS referral_referrer_subject_id_idx ON marketing.referral (referrer_subject_id);
-- convention, not declared: marketing.review_response.responded_by_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS review_response_responded_by_principal_id_idx ON marketing.review_response (responded_by_principal_id);
-- convention, not declared: marketing.review_response.review_id -> marketing.review
CREATE INDEX IF NOT EXISTS review_response_review_id_idx ON marketing.review_response (review_id);
-- convention, not declared: marketing.reward_assignment.reward_id -> marketing.reward
CREATE INDEX IF NOT EXISTS reward_assignment_reward_id_idx ON marketing.reward_assignment (reward_id);
-- convention, not declared: marketing.subscription.subject_id -> pii.subject
CREATE INDEX IF NOT EXISTS subscription_subject_id_idx ON marketing.subscription (subject_id);
-- convention, not declared: marketing.waiver_signature.template_id -> marketing.message_template
CREATE INDEX IF NOT EXISTS waiver_signature_template_id_idx ON marketing.waiver_signature (template_id);
-- convention, not declared: orders.cart_line.parent_line_id -> orders.cart_line
CREATE INDEX IF NOT EXISTS cart_line_parent_line_id_idx ON orders.cart_line (parent_line_id);
-- convention, not declared: orders.cash_count_line.cash_movement_id -> orders.cash_movement
CREATE INDEX IF NOT EXISTS cash_count_line_cash_movement_id_idx ON orders.cash_count_line (cash_movement_id);
-- convention, not declared: orders.cash_count_line.denomination_id -> platform.denomination
CREATE INDEX IF NOT EXISTS cash_count_line_denomination_id_idx ON orders.cash_count_line (denomination_id);
-- convention, not declared: orders.cash_count_line.deposit_box_id -> orders.deposit_box
CREATE INDEX IF NOT EXISTS cash_count_line_deposit_box_id_idx ON orders.cash_count_line (deposit_box_id);
-- convention, not declared: orders.cash_movement.deposit_box_id -> orders.deposit_box
CREATE INDEX IF NOT EXISTS cash_movement_deposit_box_id_idx ON orders.cash_movement (deposit_box_id);
-- convention, not declared: orders.cash_movement.witness_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS cash_movement_witness_principal_id_idx ON orders.cash_movement (witness_principal_id);
-- convention, not declared: orders.credit_override.authorised_by_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS credit_override_authorised_by_principal_id_idx ON orders.credit_override (authorised_by_principal_id);
-- convention, not declared: orders.deposit.rental_agreement_id -> rental.agreement
CREATE INDEX IF NOT EXISTS deposit_rental_agreement_id_idx ON orders.deposit (rental_agreement_id);
-- convention, not declared: orders.deposit_box.closed_by_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS deposit_box_closed_by_principal_id_idx ON orders.deposit_box (closed_by_principal_id);
-- convention, not declared: orders.deposit_box_opening_denomination.denomination_id -> platform.denomination
CREATE INDEX IF NOT EXISTS deposit_box_opening_denomination_denomination_id_idx ON orders.deposit_box_opening_denomination (denomination_id);
-- convention, not declared: orders.discount.promotion_id -> promotions.promotion
CREATE INDEX IF NOT EXISTS discount_promotion_id_idx ON orders.discount (promotion_id);
-- convention, not declared: orders.group_booking.leader_subject_id -> pii.subject
CREATE INDEX IF NOT EXISTS group_booking_leader_subject_id_idx ON orders.group_booking (leader_subject_id);
-- convention, not declared: orders.invitation.issued_by_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS invitation_issued_by_principal_id_idx ON orders.invitation (issued_by_principal_id);
-- convention, not declared: orders.invitation.offered_by_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS invitation_offered_by_principal_id_idx ON orders.invitation (offered_by_principal_id);
-- convention, not declared: orders.membership_renewal.customer_membership_id -> identity.customer_membership
CREATE INDEX IF NOT EXISTS membership_renewal_customer_membership_id_idx ON orders.membership_renewal (customer_membership_id);
-- convention, not declared: orders.membership_renewal.entitlement_template_id -> catalogue.entitlement_template
CREATE INDEX IF NOT EXISTS membership_renewal_entitlement_template_id_idx ON orders.membership_renewal (entitlement_template_id);
-- convention, not declared: orders.order_fee.payment_method_id -> payments.method
CREATE INDEX IF NOT EXISTS order_fee_payment_method_id_idx ON orders.order_fee (payment_method_id);
-- convention, not declared: orders.payment_link.issued_by_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS payment_link_issued_by_principal_id_idx ON orders.payment_link (issued_by_principal_id);
-- convention, not declared: orders.payment_link.reservation_id -> orders.reservation
CREATE INDEX IF NOT EXISTS payment_link_reservation_id_idx ON orders.payment_link (reservation_id);
-- convention, not declared: orders.pos_shift.closed_by_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS pos_shift_closed_by_principal_id_idx ON orders.pos_shift (closed_by_principal_id);
-- convention, not declared: orders.pos_shift_approval.principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS pos_shift_approval_principal_id_idx ON orders.pos_shift_approval (principal_id);
-- convention, not declared: orders.pos_shift_incident.principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS pos_shift_incident_principal_id_idx ON orders.pos_shift_incident (principal_id);
-- convention, not declared: orders.refund.batch_id -> orders.refund_batch
CREATE INDEX IF NOT EXISTS refund_batch_id_idx ON orders.refund (batch_id);
-- convention, not declared: orders.refund.ledger_entry_id -> ledger.journal_entry
CREATE INDEX IF NOT EXISTS refund_ledger_entry_id_idx ON orders.refund (ledger_entry_id);
-- convention, not declared: orders.refund.tax_reversal_entry_id -> queue.entry
CREATE INDEX IF NOT EXISTS refund_tax_reversal_entry_id_idx ON orders.refund (tax_reversal_entry_id);
-- convention, not declared: orders.refund_batch.event_id -> catalogue.event
CREATE INDEX IF NOT EXISTS refund_batch_event_id_idx ON orders.refund_batch (event_id);
-- convention, not declared: orders.refund_batch.performance_id -> catalogue.performance
CREATE INDEX IF NOT EXISTS refund_batch_performance_id_idx ON orders.refund_batch (performance_id);
-- convention, not declared: orders.refund_batch.requested_by_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS refund_batch_requested_by_principal_id_idx ON orders.refund_batch (requested_by_principal_id);
-- convention, not declared: orders.refund_batch.venue_id -> platform.scope
CREATE INDEX IF NOT EXISTS refund_batch_venue_id_idx ON orders.refund_batch (venue_id);
-- convention, not declared: orders.resale_fee_policy.event_id -> catalogue.event
CREATE INDEX IF NOT EXISTS resale_fee_policy_event_id_idx ON orders.resale_fee_policy (event_id);
-- convention, not declared: orders.resale_listing.seller_subject_id -> pii.subject
CREATE INDEX IF NOT EXISTS resale_listing_seller_subject_id_idx ON orders.resale_listing (seller_subject_id);
-- convention, not declared: orders.resale_listing.sold_to_subject_id -> pii.subject
CREATE INDEX IF NOT EXISTS resale_listing_sold_to_subject_id_idx ON orders.resale_listing (sold_to_subject_id);
-- convention, not declared: orders.reservation.subject_id -> pii.subject
CREATE INDEX IF NOT EXISTS reservation_subject_id_idx ON orders.reservation (subject_id);
-- convention, not declared: orders.reservation_line.inventory_hold_id -> catalogue.inventory_hold
CREATE INDEX IF NOT EXISTS reservation_line_inventory_hold_id_idx ON orders.reservation_line (inventory_hold_id);
-- convention, not declared: orders.reservation_line.performance_id -> catalogue.performance
CREATE INDEX IF NOT EXISTS reservation_line_performance_id_idx ON orders.reservation_line (performance_id);
-- convention, not declared: orders.reservation_line.variant_id -> catalogue.variant
CREATE INDEX IF NOT EXISTS reservation_line_variant_id_idx ON orders.reservation_line (variant_id);
-- convention, not declared: orders.upgrade.new_order_line_id -> orders.order_line
CREATE INDEX IF NOT EXISTS upgrade_new_order_line_id_idx ON orders.upgrade (new_order_line_id);
-- convention, not declared: orders.upgrade.original_order_line_id -> orders.order_line
CREATE INDEX IF NOT EXISTS upgrade_original_order_line_id_idx ON orders.upgrade (original_order_line_id);
-- convention, not declared: orders.upgrade.requested_by_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS upgrade_requested_by_principal_id_idx ON orders.upgrade (requested_by_principal_id);
-- convention, not declared: orders.visit_reminder.subject_id -> pii.subject
CREATE INDEX IF NOT EXISTS visit_reminder_subject_id_idx ON orders.visit_reminder (subject_id);
-- convention, not declared: payments.authentication_policy.mandate_text_asset_id -> assets.media_asset
CREATE INDEX IF NOT EXISTS authentication_policy_mandate_text_asset_id_idx ON payments.authentication_policy (mandate_text_asset_id);
-- convention, not declared: payments.chargeback_evidence.chargeback_id -> orders.chargeback
CREATE INDEX IF NOT EXISTS chargeback_evidence_chargeback_id_idx ON payments.chargeback_evidence (chargeback_id);
-- convention, not declared: payments.deposit_activity.created_by_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS deposit_activity_created_by_principal_id_idx ON payments.deposit_activity (created_by_principal_id);
-- convention, not declared: payments.dunning_case.resolved_by_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS dunning_case_resolved_by_principal_id_idx ON payments.dunning_case (resolved_by_principal_id);
-- convention, not declared: payments.dunning_case.subject_id -> pii.subject
CREATE INDEX IF NOT EXISTS dunning_case_subject_id_idx ON payments.dunning_case (subject_id);
-- convention, not declared: payments.eligibility_rule.payment_method_id -> payments.method
CREATE INDEX IF NOT EXISTS eligibility_rule_payment_method_id_idx ON payments.eligibility_rule (payment_method_id);
-- convention, not declared: payments.fee_rule.payment_method_id -> payments.method
CREATE INDEX IF NOT EXISTS fee_rule_payment_method_id_idx ON payments.fee_rule (payment_method_id);
-- convention, not declared: payments.fee_rule.provider_id -> payments.provider
CREATE INDEX IF NOT EXISTS fee_rule_provider_id_idx ON payments.fee_rule (provider_id);
-- convention, not declared: payments.hosted_checkout.branding_asset_id -> assets.media_asset
CREATE INDEX IF NOT EXISTS hosted_checkout_branding_asset_id_idx ON payments.hosted_checkout (branding_asset_id);
-- convention, not declared: payments.merchant_account.legal_entity_id -> ledger.legal_entity
CREATE INDEX IF NOT EXISTS merchant_account_legal_entity_id_idx ON payments.merchant_account (legal_entity_id);
-- convention, not declared: payments.method_config.payment_method_id -> payments.method
CREATE INDEX IF NOT EXISTS method_config_payment_method_id_idx ON payments.method_config (payment_method_id);
-- convention, not declared: payments.payment_terms.account_id -> ledger.account
CREATE INDEX IF NOT EXISTS payment_terms_account_id_idx ON payments.payment_terms (account_id);
-- convention, not declared: payments.provider_connection.merchant_account_id -> payments.merchant_account
CREATE INDEX IF NOT EXISTS provider_connection_merchant_account_id_idx ON payments.provider_connection (merchant_account_id);
-- convention, not declared: payments.reconciliation_source.connection_id -> payments.provider_connection
CREATE INDEX IF NOT EXISTS reconciliation_source_connection_id_idx ON payments.reconciliation_source (connection_id);
-- convention, not declared: payments.routing_rule.fallback_provider_id -> payments.provider
CREATE INDEX IF NOT EXISTS routing_rule_fallback_provider_id_idx ON payments.routing_rule (fallback_provider_id);
-- convention, not declared: payments.routing_rule.provider_id -> payments.provider
CREATE INDEX IF NOT EXISTS routing_rule_provider_id_idx ON payments.routing_rule (provider_id);
-- convention, not declared: payments.stored_forward.device_id -> platform.device
CREATE INDEX IF NOT EXISTS stored_forward_device_id_idx ON payments.stored_forward (device_id);
-- convention, not declared: payments.terminal.acquirer_connection_id -> payments.provider_connection
CREATE INDEX IF NOT EXISTS terminal_acquirer_connection_id_idx ON payments.terminal (acquirer_connection_id);
-- convention, not declared: payments.terminal.device_id -> platform.device
CREATE INDEX IF NOT EXISTS terminal_device_id_idx ON payments.terminal (device_id);
-- convention, not declared: payments.terminal.merchant_account_id -> payments.merchant_account
CREATE INDEX IF NOT EXISTS terminal_merchant_account_id_idx ON payments.terminal (merchant_account_id);
-- convention, not declared: payments.token.provider_id -> payments.provider
CREATE INDEX IF NOT EXISTS token_provider_id_idx ON payments.token (provider_id);
-- convention, not declared: pii.subject.erasure_request_id -> approvals.request
CREATE INDEX IF NOT EXISTS subject_erasure_request_id_idx ON pii.subject (erasure_request_id);
-- convention, not declared: pii.subject_biometric.guardian_subject_id -> pii.subject
CREATE INDEX IF NOT EXISTS subject_biometric_guardian_subject_id_idx ON pii.subject_biometric (guardian_subject_id);
-- convention, not declared: platform.audit_record.workstation_id -> platform.workstation
CREATE INDEX IF NOT EXISTS audit_record_workstation_id_idx ON platform.audit_record (workstation_id);
-- convention, not declared: platform.dead_letter.outbox_id -> platform.outbox
CREATE INDEX IF NOT EXISTS dead_letter_outbox_id_idx ON platform.dead_letter (outbox_id);
-- convention, not declared: platform.device.configuration_profile_id -> platform.configuration_profile
CREATE INDEX IF NOT EXISTS device_configuration_profile_id_idx ON platform.device (configuration_profile_id);
-- convention, not declared: platform.profile_deployment.profile_id -> platform.configuration_profile
CREATE INDEX IF NOT EXISTS profile_deployment_profile_id_idx ON platform.profile_deployment (profile_id);
-- convention, not declared: platform.wallet_authorisation.authorisation_id -> games.authorisation
CREATE INDEX IF NOT EXISTS wallet_authorisation_authorisation_id_idx ON platform.wallet_authorisation (authorisation_id);
-- convention, not declared: platform.wallet_authorisation.fx_rate_id -> ledger.fx_rate
CREATE INDEX IF NOT EXISTS wallet_authorisation_fx_rate_id_idx ON platform.wallet_authorisation (fx_rate_id);
-- convention, not declared: platform.workstation.configuration_profile_id -> platform.configuration_profile
CREATE INDEX IF NOT EXISTS workstation_configuration_profile_id_idx ON platform.workstation (configuration_profile_id);
-- convention, not declared: pricing.dynamic_price_action.dynamic_price_rule_id -> pricing.dynamic_price_rule
CREATE INDEX IF NOT EXISTS dynamic_price_action_dynamic_price_rule_id_idx ON pricing.dynamic_price_action (dynamic_price_rule_id);
-- convention, not declared: pricing.dynamic_price_action.rule_id -> approvals.rule
CREATE INDEX IF NOT EXISTS dynamic_price_action_rule_id_idx ON pricing.dynamic_price_action (rule_id);
-- convention, not declared: pricing.dynamic_price_condition.dynamic_price_rule_id -> pricing.dynamic_price_rule
CREATE INDEX IF NOT EXISTS dynamic_price_condition_dynamic_price_rule_id_idx ON pricing.dynamic_price_condition (dynamic_price_rule_id);
-- convention, not declared: pricing.dynamic_price_condition.rule_id -> approvals.rule
CREATE INDEX IF NOT EXISTS dynamic_price_condition_rule_id_idx ON pricing.dynamic_price_condition (rule_id);
-- convention, not declared: pricing.dynamic_price_rule.price_list_id -> catalogue.price_list
CREATE INDEX IF NOT EXISTS dynamic_price_rule_price_list_id_idx ON pricing.dynamic_price_rule (price_list_id);
-- convention, not declared: promotions.allocation_component.variant_id -> catalogue.variant
CREATE INDEX IF NOT EXISTS allocation_component_variant_id_idx ON promotions.allocation_component (variant_id);
-- convention, not declared: promotions.bundle_choice_option.variant_id -> catalogue.variant
CREATE INDEX IF NOT EXISTS bundle_choice_option_variant_id_idx ON promotions.bundle_choice_option (variant_id);
-- convention, not declared: promotions.bundle_component.variant_id -> catalogue.variant
CREATE INDEX IF NOT EXISTS bundle_component_variant_id_idx ON promotions.bundle_component (variant_id);
-- convention, not declared: promotions.coupon_code.batch_id -> promotions.coupon_code_batch
CREATE INDEX IF NOT EXISTS coupon_code_batch_id_idx ON promotions.coupon_code (batch_id);
-- convention, not declared: promotions.coupon_code.campaign_id -> promotions.coupon_campaign
CREATE INDEX IF NOT EXISTS coupon_code_campaign_id_idx ON promotions.coupon_code (campaign_id);
-- convention, not declared: promotions.coupon_code_batch.campaign_id -> promotions.coupon_campaign
CREATE INDEX IF NOT EXISTS coupon_code_batch_campaign_id_idx ON promotions.coupon_code_batch (campaign_id);
-- convention, not declared: promotions.coupon_code_batch.requested_by_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS coupon_code_batch_requested_by_principal_id_idx ON promotions.coupon_code_batch (requested_by_principal_id);
-- convention, not declared: promotions.product_relationship.from_product_id -> promotions.product_relationship
CREATE INDEX IF NOT EXISTS product_relationship_from_product_id_idx ON promotions.product_relationship (from_product_id);
-- convention, not declared: promotions.product_relationship.to_product_id -> promotions.product_relationship
CREATE INDEX IF NOT EXISTS product_relationship_to_product_id_idx ON promotions.product_relationship (to_product_id);
-- convention, not declared: promotions.promotion_variant.promotion_id -> promotions.promotion
CREATE INDEX IF NOT EXISTS promotion_variant_promotion_id_idx ON promotions.promotion_variant (promotion_id);
-- convention, not declared: queue.queue.parent_queue_id -> queue.queue
CREATE INDEX IF NOT EXISTS queue_parent_queue_id_idx ON queue.queue (parent_queue_id);
-- convention, not declared: queue.reading.feed_id -> queue.feed
CREATE INDEX IF NOT EXISTS reading_feed_id_idx ON queue.reading (feed_id);
-- convention, not declared: rental.agreement_item.asset_id -> maintenance.asset
CREATE INDEX IF NOT EXISTS agreement_item_asset_id_idx ON rental.agreement_item (asset_id);
-- convention, not declared: rental.agreement_item.catalogue_product_id -> catalogue.product
CREATE INDEX IF NOT EXISTS agreement_item_catalogue_product_id_idx ON rental.agreement_item (catalogue_product_id);
-- convention, not declared: rental.agreement_item.inventory_item_id -> inventory.item
CREATE INDEX IF NOT EXISTS agreement_item_inventory_item_id_idx ON rental.agreement_item (inventory_item_id);
-- convention, not declared: rental.agreement_item.order_line_id -> orders.order_line
CREATE INDEX IF NOT EXISTS agreement_item_order_line_id_idx ON rental.agreement_item (order_line_id);
-- convention, not declared: rental.agreement_item.rental_agreement_id -> rental.agreement
CREATE INDEX IF NOT EXISTS agreement_item_rental_agreement_id_idx ON rental.agreement_item (rental_agreement_id);
-- convention, not declared: rental.agreement_item.resource_booking_id -> resources.booking
CREATE INDEX IF NOT EXISTS agreement_item_resource_booking_id_idx ON rental.agreement_item (resource_booking_id);
-- convention, not declared: rental.agreement_item.resource_id -> resources.resource
CREATE INDEX IF NOT EXISTS agreement_item_resource_id_idx ON rental.agreement_item (resource_id);
-- convention, not declared: rental.agreement_item.stock_reservation_id -> inventory.stock_reservation
CREATE INDEX IF NOT EXISTS agreement_item_stock_reservation_id_idx ON rental.agreement_item (stock_reservation_id);
-- convention, not declared: rental.agreement_rules.terms_document_asset_id -> assets.media_asset
CREATE INDEX IF NOT EXISTS agreement_rules_terms_document_asset_id_idx ON rental.agreement_rules (terms_document_asset_id);
-- convention, not declared: rental.agreement_signature.document_asset_id -> assets.media_asset
CREATE INDEX IF NOT EXISTS agreement_signature_document_asset_id_idx ON rental.agreement_signature (document_asset_id);
-- convention, not declared: rental.agreement_signature.participant_id -> rental.participant
CREATE INDEX IF NOT EXISTS agreement_signature_participant_id_idx ON rental.agreement_signature (participant_id);
-- convention, not declared: rental.agreement_signature.signature_asset_id -> assets.media_asset
CREATE INDEX IF NOT EXISTS agreement_signature_signature_asset_id_idx ON rental.agreement_signature (signature_asset_id);
-- convention, not declared: rental.blackout.location_id -> inventory.location
CREATE INDEX IF NOT EXISTS blackout_location_id_idx ON rental.blackout (location_id);
-- convention, not declared: rental.blackout.product_id -> rental.product
CREATE INDEX IF NOT EXISTS blackout_product_id_idx ON rental.blackout (product_id);
-- convention, not declared: rental.booking.deposit_authorisation_id -> games.authorisation
CREATE INDEX IF NOT EXISTS booking_deposit_authorisation_id_idx ON rental.booking (deposit_authorisation_id);
-- convention, not declared: rental.booking.location_id -> inventory.location
CREATE INDEX IF NOT EXISTS booking_location_id_idx ON rental.booking (location_id);
-- convention, not declared: rental.booking.product_id -> rental.product
CREATE INDEX IF NOT EXISTS booking_product_id_idx ON rental.booking (product_id);
-- convention, not declared: rental.booking.return_location_id -> inventory.location
CREATE INDEX IF NOT EXISTS booking_return_location_id_idx ON rental.booking (return_location_id);
-- convention, not declared: rental.damage_assessment.asset_id -> maintenance.asset
CREATE INDEX IF NOT EXISTS damage_assessment_asset_id_idx ON rental.damage_assessment (asset_id);
-- convention, not declared: rental.damage_assessment.inspection_id -> rental.inspection
CREATE INDEX IF NOT EXISTS damage_assessment_inspection_id_idx ON rental.damage_assessment (inspection_id);
-- convention, not declared: rental.damage_assessment.work_order_id -> maintenance.work_order
CREATE INDEX IF NOT EXISTS damage_assessment_work_order_id_idx ON rental.damage_assessment (work_order_id);
-- convention, not declared: rental.deposit_policy.product_id -> rental.product
CREATE INDEX IF NOT EXISTS deposit_policy_product_id_idx ON rental.deposit_policy (product_id);
-- convention, not declared: rental.equipment_assignment.asset_id -> maintenance.asset
CREATE INDEX IF NOT EXISTS equipment_assignment_asset_id_idx ON rental.equipment_assignment (asset_id);
-- convention, not declared: rental.fee_policy.product_id -> rental.product
CREATE INDEX IF NOT EXISTS fee_policy_product_id_idx ON rental.fee_policy (product_id);
-- convention, not declared: rental.incident.asset_id -> maintenance.asset
CREATE INDEX IF NOT EXISTS incident_asset_id_idx ON rental.incident (asset_id);
-- convention, not declared: rental.incident.booking_id -> rental.booking
CREATE INDEX IF NOT EXISTS incident_booking_id_idx ON rental.incident (booking_id);
-- convention, not declared: rental.incident.work_order_id -> maintenance.work_order
CREATE INDEX IF NOT EXISTS incident_work_order_id_idx ON rental.incident (work_order_id);
-- convention, not declared: rental.inspection.asset_id -> maintenance.asset
CREATE INDEX IF NOT EXISTS inspection_asset_id_idx ON rental.inspection (asset_id);
-- convention, not declared: rental.inspection_item.rental_agreement_item_id -> rental.agreement_item
CREATE INDEX IF NOT EXISTS inspection_item_rental_agreement_item_id_idx ON rental.inspection_item (rental_agreement_item_id);
-- convention, not declared: rental.inspection_item.rental_inspection_id -> rental.inspection
CREATE INDEX IF NOT EXISTS inspection_item_rental_inspection_id_idx ON rental.inspection_item (rental_inspection_id);
-- convention, not declared: rental.location_rule.location_id -> inventory.location
CREATE INDEX IF NOT EXISTS location_rule_location_id_idx ON rental.location_rule (location_id);
-- convention, not declared: rental.override.approval_request_id -> approvals.request
CREATE INDEX IF NOT EXISTS override_approval_request_id_idx ON rental.override (approval_request_id);
-- convention, not declared: rental.override.booking_id -> rental.booking
CREATE INDEX IF NOT EXISTS override_booking_id_idx ON rental.override (booking_id);
-- convention, not declared: rental.pricing_profile.customer_segment_id -> marketing.segment
CREATE INDEX IF NOT EXISTS pricing_profile_customer_segment_id_idx ON rental.pricing_profile (customer_segment_id);
-- convention, not declared: rental.pricing_profile.product_id -> rental.product
CREATE INDEX IF NOT EXISTS pricing_profile_product_id_idx ON rental.pricing_profile (product_id);
-- convention, not declared: rental.product.catalogue_product_id -> catalogue.product
CREATE INDEX IF NOT EXISTS product_catalogue_product_id_idx ON rental.product (catalogue_product_id);
-- convention, not declared: rental.product.image_asset_id -> assets.media_asset
CREATE INDEX IF NOT EXISTS product_image_asset_id_idx ON rental.product (image_asset_id);
-- convention, not declared: rental.product.resource_type_id -> resources.resource_type
CREATE INDEX IF NOT EXISTS product_resource_type_id_idx ON rental.product (resource_type_id);
-- convention, not declared: rental.product.tenant_id -> platform.tenant
CREATE INDEX IF NOT EXISTS product_tenant_id_idx ON rental.product (tenant_id);
-- convention, not declared: rental.settlement.booking_id -> rental.booking
CREATE INDEX IF NOT EXISTS settlement_booking_id_idx ON rental.settlement (booking_id);
-- convention, not declared: reporting.alert.acknowledged_by_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS alert_acknowledged_by_principal_id_idx ON reporting.alert (acknowledged_by_principal_id);
-- convention, not declared: reporting.alert.item_id -> inventory.item
CREATE INDEX IF NOT EXISTS alert_item_id_idx ON reporting.alert (item_id);
-- convention, not declared: reporting.alert.rule_id -> reporting.alert_rule
CREATE INDEX IF NOT EXISTS alert_rule_id_idx ON reporting.alert (rule_id);
-- convention, not declared: reporting.alert.shift_id -> workforce.shift
CREATE INDEX IF NOT EXISTS alert_shift_id_idx ON reporting.alert (shift_id);
-- convention, not declared: reporting.alert.workstation_id -> platform.workstation
CREATE INDEX IF NOT EXISTS alert_workstation_id_idx ON reporting.alert (workstation_id);
-- convention, not declared: reporting.delivery.subscription_id -> reporting.subscription
CREATE INDEX IF NOT EXISTS delivery_subscription_id_idx ON reporting.delivery (subscription_id);
-- convention, not declared: reporting.kpi_target.kpi_id -> reporting.kpi_definition
CREATE INDEX IF NOT EXISTS kpi_target_kpi_id_idx ON reporting.kpi_target (kpi_id);
-- convention, not declared: reporting.natural_language_query.asked_by_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS natural_language_query_asked_by_principal_id_idx ON reporting.natural_language_query (asked_by_principal_id);
-- convention, not declared: reporting.report_definition_version.published_by_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS report_definition_version_published_by_principal_id_idx ON reporting.report_definition_version (published_by_principal_id);
-- convention, not declared: reporting.subscription.runs_as_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS subscription_runs_as_principal_id_idx ON reporting.subscription (runs_as_principal_id);
-- convention, not declared: reporting.subscription.schedule_id -> reporting.schedule
CREATE INDEX IF NOT EXISTS subscription_schedule_id_idx ON reporting.subscription (schedule_id);
-- convention, not declared: resources.booking.deposit_authorisation_id -> games.authorisation
CREATE INDEX IF NOT EXISTS booking_deposit_authorisation_id_idx ON resources.booking (deposit_authorisation_id);
-- convention, not declared: resources.qualification.document_asset_id -> assets.media_asset
CREATE INDEX IF NOT EXISTS qualification_document_asset_id_idx ON resources.qualification (document_asset_id);
-- convention, not declared: resources.qualification.resource_id -> resources.resource
CREATE INDEX IF NOT EXISTS qualification_resource_id_idx ON resources.qualification (resource_id);
-- convention, not declared: resources.resource.parent_resource_id -> resources.resource
CREATE INDEX IF NOT EXISTS resource_parent_resource_id_idx ON resources.resource (parent_resource_id);
-- convention, not declared: resources.resource_audit.resource_id -> resources.resource
CREATE INDEX IF NOT EXISTS resource_audit_resource_id_idx ON resources.resource_audit (resource_id);
-- convention, not declared: resources.resource_block.resource_id -> resources.resource
CREATE INDEX IF NOT EXISTS resource_block_resource_id_idx ON resources.resource_block (resource_id);
-- convention, not declared: resources.resource_category.parent_category_id -> resources.resource_category
CREATE INDEX IF NOT EXISTS resource_category_parent_category_id_idx ON resources.resource_category (parent_category_id);
-- convention, not declared: resources.resource_dependency.target_resource_id -> resources.resource
CREATE INDEX IF NOT EXISTS resource_dependency_target_resource_id_idx ON resources.resource_dependency (target_resource_id);
-- convention, not declared: resources.resource_dependency.target_resource_type_id -> resources.resource_type
CREATE INDEX IF NOT EXISTS resource_dependency_target_resource_type_id_idx ON resources.resource_dependency (target_resource_type_id);
-- convention, not declared: resources.resource_relation.resource_id -> resources.resource
CREATE INDEX IF NOT EXISTS resource_relation_resource_id_idx ON resources.resource_relation (resource_id);
-- convention, not declared: resources.resource_requirement.category_id -> resources.resource_category
CREATE INDEX IF NOT EXISTS resource_requirement_category_id_idx ON resources.resource_requirement (category_id);
-- convention, not declared: resources.resource_requirement.resource_id -> resources.resource
CREATE INDEX IF NOT EXISTS resource_requirement_resource_id_idx ON resources.resource_requirement (resource_id);
-- convention, not declared: resources.resource_requirement.resource_type_id -> resources.resource_type
CREATE INDEX IF NOT EXISTS resource_requirement_resource_type_id_idx ON resources.resource_requirement (resource_type_id);
-- convention, not declared: resources.resource_schedule.resource_id -> resources.resource
CREATE INDEX IF NOT EXISTS resource_schedule_resource_id_idx ON resources.resource_schedule (resource_id);
-- convention, not declared: resources.venue_assignment.primary_venue_id -> resources.venue_assignment
CREATE INDEX IF NOT EXISTS venue_assignment_primary_venue_id_idx ON resources.venue_assignment (primary_venue_id);
-- convention, not declared: retail.product_recommendation.source_product_id -> retail.product_recommendation
CREATE INDEX IF NOT EXISTS product_recommendation_source_product_id_idx ON retail.product_recommendation (source_product_id);
-- convention, not declared: retail.product_recommendation.source_variant_id -> catalogue.variant
CREATE INDEX IF NOT EXISTS product_recommendation_source_variant_id_idx ON retail.product_recommendation (source_variant_id);
-- convention, not declared: retail.product_recommendation.target_product_id -> retail.product_recommendation
CREATE INDEX IF NOT EXISTS product_recommendation_target_product_id_idx ON retail.product_recommendation (target_product_id);
-- convention, not declared: retail.product_recommendation.target_variant_id -> catalogue.variant
CREATE INDEX IF NOT EXISTS product_recommendation_target_variant_id_idx ON retail.product_recommendation (target_variant_id);
-- convention, not declared: retail.store_rule.outlet_id -> platform.outlet
CREATE INDEX IF NOT EXISTS store_rule_outlet_id_idx ON retail.store_rule (outlet_id);
-- convention, not declared: retail.store_rule.updated_by_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS store_rule_updated_by_principal_id_idx ON retail.store_rule (updated_by_principal_id);
-- convention, not declared: seating.accessible.seat_map_id -> seating.seat_map
CREATE INDEX IF NOT EXISTS accessible_seat_map_id_idx ON seating.accessible (seat_map_id);
-- convention, not declared: seating.group_request.performance_id -> catalogue.performance
CREATE INDEX IF NOT EXISTS group_request_performance_id_idx ON seating.group_request (performance_id);
-- convention, not declared: seating.hold_pool.hold_type_id -> seating.hold_type
CREATE INDEX IF NOT EXISTS hold_pool_hold_type_id_idx ON seating.hold_pool (hold_type_id);
-- convention, not declared: seating.hold_pool.performance_id -> catalogue.performance
CREATE INDEX IF NOT EXISTS hold_pool_performance_id_idx ON seating.hold_pool (performance_id);
-- convention, not declared: seating.recommendation_rules.performance_id -> catalogue.performance
CREATE INDEX IF NOT EXISTS recommendation_rules_performance_id_idx ON seating.recommendation_rules (performance_id);
-- convention, not declared: seating.recommendation_rules.seat_map_id -> seating.seat_map
CREATE INDEX IF NOT EXISTS recommendation_rules_seat_map_id_idx ON seating.recommendation_rules (seat_map_id);
-- convention, not declared: seating.seat.category_id -> seating.seat_category
CREATE INDEX IF NOT EXISTS seat_category_id_idx ON seating.seat (category_id);
-- convention, not declared: seating.seat_block_item.block_id -> seating.seat_block
CREATE INDEX IF NOT EXISTS seat_block_item_block_id_idx ON seating.seat_block_item (block_id);
-- convention, not declared: seating.seat_block_item.seat_id -> seating.seat
CREATE INDEX IF NOT EXISTS seat_block_item_seat_id_idx ON seating.seat_block_item (seat_id);
-- convention, not declared: seating.seat_hold_item.hold_id -> seating.seat_hold
CREATE INDEX IF NOT EXISTS seat_hold_item_hold_id_idx ON seating.seat_hold_item (hold_id);
-- convention, not declared: seating.seat_hold_item.seat_id -> seating.seat
CREATE INDEX IF NOT EXISTS seat_hold_item_seat_id_idx ON seating.seat_hold_item (seat_id);
-- convention, not declared: seating.seat_rules.seat_map_id -> seating.seat_map
CREATE INDEX IF NOT EXISTS seat_rules_seat_map_id_idx ON seating.seat_rules (seat_map_id);
-- convention, not declared: subscription.capacity_pack.invoice_id -> control.invoice
CREATE INDEX IF NOT EXISTS capacity_pack_invoice_id_idx ON subscription.capacity_pack (invoice_id);
-- convention, not declared: subscription.capacity_pack.tenant_id -> platform.tenant
CREATE INDEX IF NOT EXISTS capacity_pack_tenant_id_idx ON subscription.capacity_pack (tenant_id);
-- convention, not declared: subscription.go_live_readiness.tenant_id -> platform.tenant
CREATE INDEX IF NOT EXISTS go_live_readiness_tenant_id_idx ON subscription.go_live_readiness (tenant_id);
-- convention, not declared: subscription.partner_quote.agreement_id -> rental.agreement
CREATE INDEX IF NOT EXISTS partner_quote_agreement_id_idx ON subscription.partner_quote (agreement_id);
-- convention, not declared: subscription.tier_allowance.tier_id -> subscription.tier_module
CREATE INDEX IF NOT EXISTS tier_allowance_tier_id_idx ON subscription.tier_allowance (tier_id);
-- convention, not declared: subscription.tier_module.tier_id -> subscription.tier_allowance
CREATE INDEX IF NOT EXISTS tier_module_tier_id_idx ON subscription.tier_module (tier_id);
-- convention, not declared: sync.cell_connection.source_cell_id -> control.cell
CREATE INDEX IF NOT EXISTS cell_connection_source_cell_id_idx ON sync.cell_connection (source_cell_id);
-- convention, not declared: sync.cell_connection.target_cell_id -> control.cell
CREATE INDEX IF NOT EXISTS cell_connection_target_cell_id_idx ON sync.cell_connection (target_cell_id);
-- convention, not declared: sync.cross_cell_request.guest_link_id -> platform.guest_link
CREATE INDEX IF NOT EXISTS cross_cell_request_guest_link_id_idx ON sync.cross_cell_request (guest_link_id);
-- convention, not declared: sync.cross_cell_request.source_cell_id -> control.cell
CREATE INDEX IF NOT EXISTS cross_cell_request_source_cell_id_idx ON sync.cross_cell_request (source_cell_id);
-- convention, not declared: sync.cross_cell_request.target_cell_id -> control.cell
CREATE INDEX IF NOT EXISTS cross_cell_request_target_cell_id_idx ON sync.cross_cell_request (target_cell_id);
-- convention, not declared: tenancy.device_assignment.assigned_workstation_id -> platform.workstation
CREATE INDEX IF NOT EXISTS device_assignment_assigned_workstation_id_idx ON tenancy.device_assignment (assigned_workstation_id);
-- convention, not declared: tenancy.device_assignment.custodian_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS device_assignment_custodian_principal_id_idx ON tenancy.device_assignment (custodian_principal_id);
-- convention, not declared: tenancy.device_assignment.device_id -> platform.device
CREATE INDEX IF NOT EXISTS device_assignment_device_id_idx ON tenancy.device_assignment (device_id);
-- convention, not declared: tenancy.device_audit.actor_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS device_audit_actor_principal_id_idx ON tenancy.device_audit (actor_principal_id);
-- convention, not declared: tenancy.device_audit.device_id -> platform.device
CREATE INDEX IF NOT EXISTS device_audit_device_id_idx ON tenancy.device_audit (device_id);
-- convention, not declared: tenancy.device_credential.device_id -> platform.device
CREATE INDEX IF NOT EXISTS device_credential_device_id_idx ON tenancy.device_credential (device_id);
-- convention, not declared: tenancy.device_firmware.artefact_asset_id -> assets.media_asset
CREATE INDEX IF NOT EXISTS device_firmware_artefact_asset_id_idx ON tenancy.device_firmware (artefact_asset_id);
-- convention, not declared: tenancy.device_rollout.firmware_id -> tenancy.device_firmware
CREATE INDEX IF NOT EXISTS device_rollout_firmware_id_idx ON tenancy.device_rollout (firmware_id);
-- convention, not declared: tenancy.device_tamper_event.device_id -> platform.device
CREATE INDEX IF NOT EXISTS device_tamper_event_device_id_idx ON tenancy.device_tamper_event (device_id);
-- convention, not declared: tenancy.device_telemetry.device_id -> platform.device
CREATE INDEX IF NOT EXISTS device_telemetry_device_id_idx ON tenancy.device_telemetry (device_id);
-- convention, not declared: venuemap.map_version.map_id -> venuemap.map
CREATE INDEX IF NOT EXISTS map_version_map_id_idx ON venuemap.map_version (map_id);
-- convention, not declared: venuemap.map_version.published_by_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS map_version_published_by_principal_id_idx ON venuemap.map_version (published_by_principal_id);
-- convention, not declared: venuemap.path.from_point_id -> venuemap.point
CREATE INDEX IF NOT EXISTS path_from_point_id_idx ON venuemap.path (from_point_id);
-- convention, not declared: venuemap.path.restricted_by_point_id -> venuemap.point
CREATE INDEX IF NOT EXISTS path_restricted_by_point_id_idx ON venuemap.path (restricted_by_point_id);
-- convention, not declared: venuemap.path.to_point_id -> venuemap.point
CREATE INDEX IF NOT EXISTS path_to_point_id_idx ON venuemap.path (to_point_id);
-- convention, not declared: wallet.adjustment.wallet_id -> wallet.wallet
CREATE INDEX IF NOT EXISTS adjustment_wallet_id_idx ON wallet.adjustment (wallet_id);
-- convention, not declared: wallet.balance.wallet_balance_id -> wallet.balance
CREATE INDEX IF NOT EXISTS balance_wallet_balance_id_idx ON wallet.balance (wallet_balance_id);
-- convention, not declared: wallet.balance.wallet_id -> wallet.wallet
CREATE INDEX IF NOT EXISTS balance_wallet_id_idx ON wallet.balance (wallet_id);
-- convention, not declared: wallet.credential.replaced_by_credential_id -> wallet.credential
CREATE INDEX IF NOT EXISTS credential_replaced_by_credential_id_idx ON wallet.credential (replaced_by_credential_id);
-- convention, not declared: wallet.credential.wallet_id -> wallet.wallet
CREATE INDEX IF NOT EXISTS credential_wallet_id_idx ON wallet.credential (wallet_id);
-- convention, not declared: wallet.credit_eligibility.credit_type_id -> wallet.credit_type
CREATE INDEX IF NOT EXISTS credit_eligibility_credit_type_id_idx ON wallet.credit_eligibility (credit_type_id);
-- convention, not declared: wallet.credit_lot.credit_type_id -> wallet.credit_type
CREATE INDEX IF NOT EXISTS credit_lot_credit_type_id_idx ON wallet.credit_lot (credit_type_id);
-- convention, not declared: wallet.dispute.adjustment_id -> wallet.adjustment
CREATE INDEX IF NOT EXISTS dispute_adjustment_id_idx ON wallet.dispute (adjustment_id);
-- convention, not declared: wallet.dispute.wallet_id -> wallet.wallet
CREATE INDEX IF NOT EXISTS dispute_wallet_id_idx ON wallet.dispute (wallet_id);
-- convention, not declared: wallet.funding_rules.wallet_type_id -> wallet.wallet_type
CREATE INDEX IF NOT EXISTS funding_rules_wallet_type_id_idx ON wallet.funding_rules (wallet_type_id);
-- convention, not declared: wallet.gift_card_product.credit_type_id -> wallet.credit_type
CREATE INDEX IF NOT EXISTS gift_card_product_credit_type_id_idx ON wallet.gift_card_product (credit_type_id);
-- convention, not declared: wallet.hold.payment_id -> orders.payment
CREATE INDEX IF NOT EXISTS hold_payment_id_idx ON wallet.hold (payment_id);
-- convention, not declared: wallet.hold.wallet_hold_id -> wallet.hold
CREATE INDEX IF NOT EXISTS hold_wallet_hold_id_idx ON wallet.hold (wallet_hold_id);
-- convention, not declared: wallet.hold.wallet_id -> wallet.wallet
CREATE INDEX IF NOT EXISTS hold_wallet_id_idx ON wallet.hold (wallet_id);
-- convention, not declared: wallet.refund_policy.wallet_refund_credit_type_id -> wallet.credit_type
CREATE INDEX IF NOT EXISTS refund_policy_wallet_refund_credit_type_id_idx ON wallet.refund_policy (wallet_refund_credit_type_id);
-- convention, not declared: wallet.restriction.wallet_id -> wallet.wallet
CREATE INDEX IF NOT EXISTS restriction_wallet_id_idx ON wallet.restriction (wallet_id);
-- convention, not declared: wallet.shared_wallet.owner_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS shared_wallet_owner_principal_id_idx ON wallet.shared_wallet (owner_principal_id);
-- convention, not declared: wallet.shared_wallet.wallet_id -> wallet.wallet
CREATE INDEX IF NOT EXISTS shared_wallet_wallet_id_idx ON wallet.shared_wallet (wallet_id);
-- convention, not declared: wallet.shared_wallet_member.subject_id -> pii.subject
CREATE INDEX IF NOT EXISTS shared_wallet_member_subject_id_idx ON wallet.shared_wallet_member (subject_id);
-- convention, not declared: wallet.wallet_transaction.subject_id -> pii.subject
CREATE INDEX IF NOT EXISTS wallet_transaction_subject_id_idx ON wallet.wallet_transaction (subject_id);
-- convention, not declared: whitelabel.custom_domain.tenant_id -> platform.tenant
CREATE INDEX IF NOT EXISTS custom_domain_tenant_id_idx ON whitelabel.custom_domain (tenant_id);
-- convention, not declared: workforce.announcement.published_by_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS announcement_published_by_principal_id_idx ON workforce.announcement (published_by_principal_id);
-- convention, not declared: workforce.attendance.amended_by_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS attendance_amended_by_principal_id_idx ON workforce.attendance (amended_by_principal_id);
-- convention, not declared: workforce.employee.manager_employee_id -> workforce.employee
CREATE INDEX IF NOT EXISTS employee_manager_employee_id_idx ON workforce.employee (manager_employee_id);
-- convention, not declared: workforce.employee.principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS employee_principal_id_idx ON workforce.employee (principal_id);
-- convention, not declared: workforce.employee.tenant_id -> platform.tenant
CREATE INDEX IF NOT EXISTS employee_tenant_id_idx ON workforce.employee (tenant_id);
-- convention, not declared: workforce.employment.employee_id -> workforce.employee
CREATE INDEX IF NOT EXISTS employment_employee_id_idx ON workforce.employment (employee_id);
-- convention, not declared: workforce.field_ownership.source_id -> workforce.integration_source
CREATE INDEX IF NOT EXISTS field_ownership_source_id_idx ON workforce.field_ownership (source_id);
-- convention, not declared: workforce.job_title.tenant_id -> platform.tenant
CREATE INDEX IF NOT EXISTS job_title_tenant_id_idx ON workforce.job_title (tenant_id);
-- convention, not declared: workforce.leave_balance.employee_id -> workforce.employee
CREATE INDEX IF NOT EXISTS leave_balance_employee_id_idx ON workforce.leave_balance (employee_id);
-- convention, not declared: workforce.leave_balance.type_id -> workforce.leave_type
CREATE INDEX IF NOT EXISTS leave_balance_type_id_idx ON workforce.leave_balance (type_id);
-- convention, not declared: workforce.leave_request.principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS leave_request_principal_id_idx ON workforce.leave_request (principal_id);
-- convention, not declared: workforce.leave_type.tenant_id -> platform.tenant
CREATE INDEX IF NOT EXISTS leave_type_tenant_id_idx ON workforce.leave_type (tenant_id);
-- convention, not declared: workforce.open_shift.rota_assignment_id -> workforce.rota_assignment
CREATE INDEX IF NOT EXISTS open_shift_rota_assignment_id_idx ON workforce.open_shift (rota_assignment_id);
-- convention, not declared: workforce.open_shift.shift_template_id -> workforce.shift_template
CREATE INDEX IF NOT EXISTS open_shift_shift_template_id_idx ON workforce.open_shift (shift_template_id);
-- convention, not declared: workforce.rota_assignment.required_role_id -> identity.role
CREATE INDEX IF NOT EXISTS rota_assignment_required_role_id_idx ON workforce.rota_assignment (required_role_id);
-- convention, not declared: workforce.shift.tenant_id -> platform.tenant
CREATE INDEX IF NOT EXISTS shift_tenant_id_idx ON workforce.shift (tenant_id);
-- convention, not declared: workforce.shift_swap.from_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS shift_swap_from_principal_id_idx ON workforce.shift_swap (from_principal_id);
-- convention, not declared: workforce.shift_swap.to_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS shift_swap_to_principal_id_idx ON workforce.shift_swap (to_principal_id);
-- convention, not declared: workforce.sync_conflict.employee_id -> workforce.employee
CREATE INDEX IF NOT EXISTS sync_conflict_employee_id_idx ON workforce.sync_conflict (employee_id);
-- convention, not declared: workforce.sync_conflict.resolved_by_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS sync_conflict_resolved_by_principal_id_idx ON workforce.sync_conflict (resolved_by_principal_id);
-- convention, not declared: workforce.sync_conflict.source_id -> workforce.integration_source
CREATE INDEX IF NOT EXISTS sync_conflict_source_id_idx ON workforce.sync_conflict (source_id);
-- convention, not declared: workforce.sync_conflict.sync_run_id -> workforce.sync_run
CREATE INDEX IF NOT EXISTS sync_conflict_sync_run_id_idx ON workforce.sync_conflict (sync_run_id);
-- convention, not declared: workforce.sync_run.source_id -> workforce.integration_source
CREATE INDEX IF NOT EXISTS sync_run_source_id_idx ON workforce.sync_run (source_id);
-- convention, not declared: workforce.training_record.principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS training_record_principal_id_idx ON workforce.training_record (principal_id);
-- convention, not declared: workforce.work_assignment.employee_id -> workforce.employee
CREATE INDEX IF NOT EXISTS work_assignment_employee_id_idx ON workforce.work_assignment (employee_id);
-- convention, not declared: workforce.work_assignment.job_title_id -> workforce.job_title
CREATE INDEX IF NOT EXISTS work_assignment_job_title_id_idx ON workforce.work_assignment (job_title_id);
-- convention, not declared: workforce.work_assignment.outlet_id -> platform.outlet
CREATE INDEX IF NOT EXISTS work_assignment_outlet_id_idx ON workforce.work_assignment (outlet_id);
-- crosses the database boundary: platform.cell_endpoint.cell_id -> control.cell
CREATE INDEX IF NOT EXISTS cell_endpoint_cell_id_idx ON platform.cell_endpoint (cell_id);
-- crosses the database boundary: whitelabel.tenant_config.footer_config_id -> control.footer_config
CREATE INDEX IF NOT EXISTS tenant_config_footer_config_id_idx ON whitelabel.tenant_config (footer_config_id);
-- declared: access.access_change.order_id -> orders.sales_order
CREATE INDEX IF NOT EXISTS access_change_order_id_idx ON access.access_change (order_id);
-- declared: access.access_point.venue_id -> platform.scope
CREATE INDEX IF NOT EXISTS access_point_venue_id_idx ON access.access_point (venue_id);
-- declared: access.blacklist.added_by_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS blacklist_added_by_principal_id_idx ON access.blacklist (added_by_principal_id);
-- declared: access.entitlement.order_id -> orders.sales_order
CREATE INDEX IF NOT EXISTS entitlement_order_id_idx ON access.entitlement (order_id);
-- declared: access.entitlement.product_id -> catalogue.product
CREATE INDEX IF NOT EXISTS entitlement_product_id_idx ON access.entitlement (product_id);
-- declared: access.entitlement.venue_id -> platform.scope
CREATE INDEX IF NOT EXISTS entitlement_venue_id_idx ON access.entitlement (venue_id);
-- declared: access.entry_rule_point.admission_profile_id -> access.admission_rules
CREATE INDEX IF NOT EXISTS entry_rule_point_admission_profile_id_idx ON access.entry_rule_point (admission_profile_id);
-- declared: access.parking_entitlement.facility_id -> access.parking_facility
CREATE INDEX IF NOT EXISTS parking_entitlement_facility_id_idx ON access.parking_entitlement (facility_id);
-- declared: access.parking_entitlement.order_id -> orders.sales_order
CREATE INDEX IF NOT EXISTS parking_entitlement_order_id_idx ON access.parking_entitlement (order_id);
-- declared: access.parking_entitlement.subject_id -> pii.subject
CREATE INDEX IF NOT EXISTS parking_entitlement_subject_id_idx ON access.parking_entitlement (subject_id);
-- declared: access.parking_facility.venue_id -> platform.scope
CREATE INDEX IF NOT EXISTS parking_facility_venue_id_idx ON access.parking_facility (venue_id);
-- declared: access.scan_event.access_point_id -> access.access_point
CREATE INDEX IF NOT EXISTS scan_event_access_point_id_idx ON access.scan_event (access_point_id);
-- declared: access.scan_event.device_id -> platform.device
CREATE INDEX IF NOT EXISTS scan_event_device_id_idx ON access.scan_event (device_id);
-- declared: access.scan_event.operator_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS scan_event_operator_principal_id_idx ON access.scan_event (operator_principal_id);
-- declared: access.scan_event.overridden_by_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS scan_event_overridden_by_principal_id_idx ON access.scan_event (overridden_by_principal_id);
-- declared: access.scan_event.ticket_id -> access.entitlement
CREATE INDEX IF NOT EXISTS scan_event_ticket_id_idx ON access.scan_event (ticket_id);
-- declared: access.scan_event.venue_id -> platform.scope
CREATE INDEX IF NOT EXISTS scan_event_venue_id_idx ON access.scan_event (venue_id);
-- declared: ai.activity.conversation_id -> ai.conversation
CREATE INDEX IF NOT EXISTS activity_conversation_id_idx ON ai.activity (conversation_id);
-- declared: ai.activity.principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS activity_principal_id_idx ON ai.activity (principal_id);
-- declared: ai.activity.subject_id -> pii.subject
CREATE INDEX IF NOT EXISTS activity_subject_id_idx ON ai.activity (subject_id);
-- declared: ai.chunk_ref.document_id -> ai.knowledge_document
CREATE INDEX IF NOT EXISTS chunk_ref_document_id_idx ON ai.chunk_ref (document_id);
-- declared: ai.conversation.principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS conversation_principal_id_idx ON ai.conversation (principal_id);
-- declared: ai.index_entry.source_id -> ai.index_source
CREATE INDEX IF NOT EXISTS index_entry_source_id_idx ON ai.index_entry (source_id);
-- declared: ai.index_job.source_id -> ai.index_source
CREATE INDEX IF NOT EXISTS index_job_source_id_idx ON ai.index_job (source_id);
-- declared: ai.index_source.collection_id -> ai.knowledge_collection
CREATE INDEX IF NOT EXISTS index_source_collection_id_idx ON ai.index_source (collection_id);
-- declared: ai.knowledge_document.collection_id -> ai.knowledge_collection
CREATE INDEX IF NOT EXISTS knowledge_document_collection_id_idx ON ai.knowledge_document (collection_id);
-- declared: ai.layout_draft.asset_id -> assets.media_asset
CREATE INDEX IF NOT EXISTS layout_draft_asset_id_idx ON ai.layout_draft (asset_id);
-- declared: ai.message.conversation_id -> ai.conversation
CREATE INDEX IF NOT EXISTS message_conversation_id_idx ON ai.message (conversation_id);
-- declared: ai.message.proposed_action_id -> ai.proposed_action
CREATE INDEX IF NOT EXISTS message_proposed_action_id_idx ON ai.message (proposed_action_id);
-- declared: ai.policy.tenant_id -> platform.tenant
CREATE INDEX IF NOT EXISTS policy_tenant_id_idx ON ai.policy (tenant_id);
-- declared: ai.proposed_action.decided_by_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS proposed_action_decided_by_principal_id_idx ON ai.proposed_action (decided_by_principal_id);
-- declared: ai.proposed_action.interaction_id -> ai.activity
CREATE INDEX IF NOT EXISTS proposed_action_interaction_id_idx ON ai.proposed_action (interaction_id);
-- declared: ai.provider.region_id -> platform.scope
CREATE INDEX IF NOT EXISTS provider_region_id_idx ON ai.provider (region_id);
-- declared: approvals.decision.principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS decision_principal_id_idx ON approvals.decision (principal_id);
-- declared: approvals.decision.request_id -> approvals.request
CREATE INDEX IF NOT EXISTS decision_request_id_idx ON approvals.decision (request_id);
-- declared: approvals.delegation.delegate_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS delegation_delegate_principal_id_idx ON approvals.delegation (delegate_principal_id);
-- declared: approvals.delegation.delegator_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS delegation_delegator_principal_id_idx ON approvals.delegation (delegator_principal_id);
-- declared: approvals.escalation.request_id -> approvals.request
CREATE INDEX IF NOT EXISTS escalation_request_id_idx ON approvals.escalation (request_id);
-- declared: approvals.request.requested_by_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS request_requested_by_principal_id_idx ON approvals.request (requested_by_principal_id);
-- declared: approvals.rule.matrix_id -> approvals.matrix
CREATE INDEX IF NOT EXISTS rule_matrix_id_idx ON approvals.rule (matrix_id);
-- declared: assets.media_asset.uploaded_by_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS media_asset_uploaded_by_principal_id_idx ON assets.media_asset (uploaded_by_principal_id);
-- declared: assets.media_asset.venue_id -> platform.scope
CREATE INDEX IF NOT EXISTS media_asset_venue_id_idx ON assets.media_asset (venue_id);
-- declared: assets.media_collection.cover_asset_id -> assets.media_asset
CREATE INDEX IF NOT EXISTS media_collection_cover_asset_id_idx ON assets.media_collection (cover_asset_id);
-- declared: assets.media_collection.venue_id -> platform.scope
CREATE INDEX IF NOT EXISTS media_collection_venue_id_idx ON assets.media_collection (venue_id);
-- declared: assets.media_usage.asset_id -> assets.media_asset
CREATE INDEX IF NOT EXISTS media_usage_asset_id_idx ON assets.media_usage (asset_id);
-- declared: catalogue.alternative_code.product_id -> catalogue.product
CREATE INDEX IF NOT EXISTS alternative_code_product_id_idx ON catalogue.alternative_code (product_id);
-- declared: catalogue.alternative_code.variant_id -> catalogue.variant
CREATE INDEX IF NOT EXISTS alternative_code_variant_id_idx ON catalogue.alternative_code (variant_id);
-- declared: catalogue.channel_allocation.envelope_id -> catalogue.channel_capacity
CREATE INDEX IF NOT EXISTS channel_allocation_envelope_id_idx ON catalogue.channel_allocation (envelope_id);
-- declared: catalogue.channel_capacity.performance_id -> catalogue.performance
CREATE INDEX IF NOT EXISTS channel_capacity_performance_id_idx ON catalogue.channel_capacity (performance_id);
-- declared: catalogue.channel_capacity.seat_category_id -> seating.seat_category
CREATE INDEX IF NOT EXISTS channel_capacity_seat_category_id_idx ON catalogue.channel_capacity (seat_category_id);
-- declared: catalogue.donation_campaign.liability_account_id -> ledger.account
CREATE INDEX IF NOT EXISTS donation_campaign_liability_account_id_idx ON catalogue.donation_campaign (liability_account_id);
-- declared: catalogue.donation_campaign.venue_id -> platform.scope
CREATE INDEX IF NOT EXISTS donation_campaign_venue_id_idx ON catalogue.donation_campaign (venue_id);
-- declared: catalogue.entitlement_template.admission_rules_id -> access.admission_rules
CREATE INDEX IF NOT EXISTS entitlement_template_admission_rules_id_idx ON catalogue.entitlement_template (admission_rules_id);
-- declared: catalogue.event.venue_id -> platform.scope
CREATE INDEX IF NOT EXISTS event_venue_id_idx ON catalogue.event (venue_id);
-- declared: catalogue.inventory_hold.channel_capacity_id -> catalogue.channel_capacity
CREATE INDEX IF NOT EXISTS inventory_hold_channel_capacity_id_idx ON catalogue.inventory_hold (channel_capacity_id);
-- declared: catalogue.inventory_hold.force_released_by_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS inventory_hold_force_released_by_principal_id_idx ON catalogue.inventory_hold (force_released_by_principal_id);
-- declared: catalogue.inventory_hold.holder_workstation_id -> platform.workstation
CREATE INDEX IF NOT EXISTS inventory_hold_holder_workstation_id_idx ON catalogue.inventory_hold (holder_workstation_id);
-- declared: catalogue.performance.admission_rules_id -> access.admission_rules
CREATE INDEX IF NOT EXISTS performance_admission_rules_id_idx ON catalogue.performance (admission_rules_id);
-- declared: catalogue.performance.event_id -> catalogue.event
CREATE INDEX IF NOT EXISTS performance_event_id_idx ON catalogue.performance (event_id);
-- declared: catalogue.performance.seat_map_id -> seating.seat_map
CREATE INDEX IF NOT EXISTS performance_seat_map_id_idx ON catalogue.performance (seat_map_id);
-- declared: catalogue.price.price_list_id -> catalogue.price_list
CREATE INDEX IF NOT EXISTS price_price_list_id_idx ON catalogue.price (price_list_id);
-- declared: catalogue.price.tax_code_id -> ledger.tax_code
CREATE INDEX IF NOT EXISTS price_tax_code_id_idx ON catalogue.price (tax_code_id);
-- declared: catalogue.price.variant_id -> catalogue.variant
CREATE INDEX IF NOT EXISTS price_variant_id_idx ON catalogue.price (variant_id);
-- declared: catalogue.price_list.venue_id -> platform.scope
CREATE INDEX IF NOT EXISTS price_list_venue_id_idx ON catalogue.price_list (venue_id);
-- declared: catalogue.product.entitlement_template_id -> catalogue.entitlement_template
CREATE INDEX IF NOT EXISTS product_entitlement_template_id_idx ON catalogue.product (entitlement_template_id);
-- declared: catalogue.product.venue_id -> platform.scope
CREATE INDEX IF NOT EXISTS product_venue_id_idx ON catalogue.product (venue_id);
-- declared: catalogue.product_version.product_id -> catalogue.product
CREATE INDEX IF NOT EXISTS product_version_product_id_idx ON catalogue.product_version (product_id);
-- declared: catalogue.published_bundle.venue_id -> platform.scope
CREATE INDEX IF NOT EXISTS published_bundle_venue_id_idx ON catalogue.published_bundle (venue_id);
-- declared: catalogue.space.venue_id -> platform.scope
CREATE INDEX IF NOT EXISTS space_venue_id_idx ON catalogue.space (venue_id);
-- declared: catalogue.variant.product_id -> catalogue.product
CREATE INDEX IF NOT EXISTS variant_product_id_idx ON catalogue.variant (product_id);
-- declared: catalogue.variant_dimension.product_id -> catalogue.product
CREATE INDEX IF NOT EXISTS variant_dimension_product_id_idx ON catalogue.variant_dimension (product_id);
-- declared: catalogue.waitlist_entry.performance_id -> catalogue.performance
CREATE INDEX IF NOT EXISTS waitlist_entry_performance_id_idx ON catalogue.waitlist_entry (performance_id);
-- declared: catalogue.waitlist_entry.subject_id -> pii.subject
CREATE INDEX IF NOT EXISTS waitlist_entry_subject_id_idx ON catalogue.waitlist_entry (subject_id);
-- declared: catalogue.waitlist_entry.variant_id -> catalogue.variant
CREATE INDEX IF NOT EXISTS waitlist_entry_variant_id_idx ON catalogue.waitlist_entry (variant_id);
-- declared: fnb.bill_split.visit_id -> fnb.table_visit
CREATE INDEX IF NOT EXISTS bill_split_visit_id_idx ON fnb.bill_split (visit_id);
-- declared: fnb.delivery_location.seat_id -> seating.seat
CREATE INDEX IF NOT EXISTS delivery_location_seat_id_idx ON fnb.delivery_location (seat_id);
-- declared: fnb.delivery_location.table_id -> fnb.dining_table
CREATE INDEX IF NOT EXISTS delivery_location_table_id_idx ON fnb.delivery_location (table_id);
-- declared: fnb.delivery_location.venue_id -> platform.scope
CREATE INDEX IF NOT EXISTS delivery_location_venue_id_idx ON fnb.delivery_location (venue_id);
-- declared: fnb.delivery_location_outlet.location_id -> fnb.delivery_location
CREATE INDEX IF NOT EXISTS delivery_location_outlet_location_id_idx ON fnb.delivery_location_outlet (location_id);
-- declared: fnb.delivery_location_outlet.outlet_id -> platform.outlet
CREATE INDEX IF NOT EXISTS delivery_location_outlet_outlet_id_idx ON fnb.delivery_location_outlet (outlet_id);
-- declared: fnb.dining_table.outlet_id -> platform.outlet
CREATE INDEX IF NOT EXISTS dining_table_outlet_id_idx ON fnb.dining_table (outlet_id);
-- declared: fnb.kitchen_station.outlet_id -> platform.outlet
CREATE INDEX IF NOT EXISTS kitchen_station_outlet_id_idx ON fnb.kitchen_station (outlet_id);
-- declared: fnb.kitchen_ticket.outlet_id -> platform.outlet
CREATE INDEX IF NOT EXISTS kitchen_ticket_outlet_id_idx ON fnb.kitchen_ticket (outlet_id);
-- declared: fnb.kitchen_ticket.prioritised_by_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS kitchen_ticket_prioritised_by_principal_id_idx ON fnb.kitchen_ticket (prioritised_by_principal_id);
-- declared: fnb.kitchen_ticket_line.kitchen_ticket_id -> fnb.kitchen_ticket
CREATE INDEX IF NOT EXISTS kitchen_ticket_line_kitchen_ticket_id_idx ON fnb.kitchen_ticket_line (kitchen_ticket_id);
-- declared: fnb.kitchen_ticket_line.station_id -> fnb.kitchen_station
CREATE INDEX IF NOT EXISTS kitchen_ticket_line_station_id_idx ON fnb.kitchen_ticket_line (station_id);
-- declared: fnb.location_session.location_id -> fnb.delivery_location
CREATE INDEX IF NOT EXISTS location_session_location_id_idx ON fnb.location_session (location_id);
-- declared: fnb.location_session.outlet_id -> platform.outlet
CREATE INDEX IF NOT EXISTS location_session_outlet_id_idx ON fnb.location_session (outlet_id);
-- declared: fnb.location_session.subject_id -> pii.subject
CREATE INDEX IF NOT EXISTS location_session_subject_id_idx ON fnb.location_session (subject_id);
-- declared: fnb.location_session.venue_id -> platform.scope
CREATE INDEX IF NOT EXISTS location_session_venue_id_idx ON fnb.location_session (venue_id);
-- declared: fnb.location_session.visit_id -> fnb.table_visit
CREATE INDEX IF NOT EXISTS location_session_visit_id_idx ON fnb.location_session (visit_id);
-- declared: fnb.menu.outlet_id -> platform.outlet
CREATE INDEX IF NOT EXISTS menu_outlet_id_idx ON fnb.menu (outlet_id);
-- declared: fnb.menu_item.product_variant_id -> catalogue.variant
CREATE INDEX IF NOT EXISTS menu_item_product_variant_id_idx ON fnb.menu_item (product_variant_id);
-- declared: fnb.menu_item.station_id -> fnb.kitchen_station
CREATE INDEX IF NOT EXISTS menu_item_station_id_idx ON fnb.menu_item (station_id);
-- declared: fnb.menu_section.menu_id -> fnb.menu
CREATE INDEX IF NOT EXISTS menu_section_menu_id_idx ON fnb.menu_section (menu_id);
-- declared: fnb.modifier_option.modifier_group_id -> fnb.modifier_group
CREATE INDEX IF NOT EXISTS modifier_option_modifier_group_id_idx ON fnb.modifier_option (modifier_group_id);
-- declared: fnb.production_plan_line.production_plan_id -> fnb.production_plan
CREATE INDEX IF NOT EXISTS production_plan_line_production_plan_id_idx ON fnb.production_plan_line (production_plan_id);
-- declared: fnb.production_run.recipe_id -> fnb.recipe
CREATE INDEX IF NOT EXISTS production_run_recipe_id_idx ON fnb.production_run (recipe_id);
-- declared: fnb.recipe.menu_item_id -> fnb.menu_item
CREATE INDEX IF NOT EXISTS recipe_menu_item_id_idx ON fnb.recipe (menu_item_id);
-- declared: fnb.recipe_ingredient.inventory_item_id -> inventory.item
CREATE INDEX IF NOT EXISTS recipe_ingredient_inventory_item_id_idx ON fnb.recipe_ingredient (inventory_item_id);
-- declared: fnb.recipe_ingredient.recipe_id -> fnb.recipe
CREATE INDEX IF NOT EXISTS recipe_ingredient_recipe_id_idx ON fnb.recipe_ingredient (recipe_id);
-- declared: fnb.reservation_table.table_id -> fnb.dining_table
CREATE INDEX IF NOT EXISTS reservation_table_table_id_idx ON fnb.reservation_table (table_id);
-- declared: fnb.service_order.kitchen_ticket_id -> fnb.kitchen_ticket
CREATE INDEX IF NOT EXISTS service_order_kitchen_ticket_id_idx ON fnb.service_order (kitchen_ticket_id);
-- declared: fnb.service_order.outlet_id -> platform.outlet
CREATE INDEX IF NOT EXISTS service_order_outlet_id_idx ON fnb.service_order (outlet_id);
-- declared: fnb.service_order.table_visit_id -> fnb.table_visit
CREATE INDEX IF NOT EXISTS service_order_table_visit_id_idx ON fnb.service_order (table_visit_id);
-- declared: fnb.service_order_line.service_order_id -> fnb.service_order
CREATE INDEX IF NOT EXISTS service_order_line_service_order_id_idx ON fnb.service_order_line (service_order_id);
-- declared: fnb.sub_bill.bill_split_id -> fnb.bill_split
CREATE INDEX IF NOT EXISTS sub_bill_bill_split_id_idx ON fnb.sub_bill (bill_split_id);
-- declared: fnb.table_reservation.outlet_id -> platform.outlet
CREATE INDEX IF NOT EXISTS table_reservation_outlet_id_idx ON fnb.table_reservation (outlet_id);
-- declared: fnb.table_reservation.subject_id -> pii.subject
CREATE INDEX IF NOT EXISTS table_reservation_subject_id_idx ON fnb.table_reservation (subject_id);
-- declared: fnb.table_reservation.table_visit_id -> fnb.table_visit
CREATE INDEX IF NOT EXISTS table_reservation_table_visit_id_idx ON fnb.table_reservation (table_visit_id);
-- declared: fnb.table_session.outlet_id -> platform.outlet
CREATE INDEX IF NOT EXISTS table_session_outlet_id_idx ON fnb.table_session (outlet_id);
-- declared: fnb.table_session.subject_id -> pii.subject
CREATE INDEX IF NOT EXISTS table_session_subject_id_idx ON fnb.table_session (subject_id);
-- declared: fnb.table_session.table_id -> fnb.dining_table
CREATE INDEX IF NOT EXISTS table_session_table_id_idx ON fnb.table_session (table_id);
-- declared: fnb.table_session.visit_id -> fnb.table_visit
CREATE INDEX IF NOT EXISTS table_session_visit_id_idx ON fnb.table_session (visit_id);
-- declared: fnb.table_visit.outlet_id -> platform.outlet
CREATE INDEX IF NOT EXISTS table_visit_outlet_id_idx ON fnb.table_visit (outlet_id);
-- declared: fnb.table_visit.server_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS table_visit_server_principal_id_idx ON fnb.table_visit (server_principal_id);
-- declared: fnb.table_visit.subject_id -> pii.subject
CREATE INDEX IF NOT EXISTS table_visit_subject_id_idx ON fnb.table_visit (subject_id);
-- declared: fnb.table_visit.table_id -> fnb.dining_table
CREATE INDEX IF NOT EXISTS table_visit_table_id_idx ON fnb.table_visit (table_id);
-- declared: fnb.waitlist_entry.outlet_id -> platform.outlet
CREATE INDEX IF NOT EXISTS waitlist_entry_outlet_id_idx ON fnb.waitlist_entry (outlet_id);
-- declared: fnb.waitlist_entry.subject_id -> pii.subject
CREATE INDEX IF NOT EXISTS waitlist_entry_subject_id_idx ON fnb.waitlist_entry (subject_id);
-- declared: games.card.subject_id -> pii.subject
CREATE INDEX IF NOT EXISTS card_subject_id_idx ON games.card (subject_id);
-- declared: games.card.venue_id -> platform.scope
CREATE INDEX IF NOT EXISTS card_venue_id_idx ON games.card (venue_id);
-- declared: games.credit_ledger.card_id -> games.card
CREATE INDEX IF NOT EXISTS credit_ledger_card_id_idx ON games.credit_ledger (card_id);
-- declared: games.game.asset_id -> maintenance.asset
CREATE INDEX IF NOT EXISTS game_asset_id_idx ON games.game (asset_id);
-- declared: games.game.venue_id -> platform.scope
CREATE INDEX IF NOT EXISTS game_venue_id_idx ON games.game (venue_id);
-- declared: games.play.game_id -> games.game
CREATE INDEX IF NOT EXISTS play_game_id_idx ON games.play (game_id);
-- declared: games.prize.merchandise_id -> retail.merchandise
CREATE INDEX IF NOT EXISTS prize_merchandise_id_idx ON games.prize (merchandise_id);
-- declared: games.prize.venue_id -> platform.scope
CREATE INDEX IF NOT EXISTS prize_venue_id_idx ON games.prize (venue_id);
-- declared: games.redemption.issued_by_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS redemption_issued_by_principal_id_idx ON games.redemption (issued_by_principal_id);
-- declared: games.redemption.venue_id -> platform.scope
CREATE INDEX IF NOT EXISTS redemption_venue_id_idx ON games.redemption (venue_id);
-- declared: games.redemption_line.prize_id -> games.prize
CREATE INDEX IF NOT EXISTS redemption_line_prize_id_idx ON games.redemption_line (prize_id);
-- declared: games.redemption_line.redemption_id -> games.redemption
CREATE INDEX IF NOT EXISTS redemption_line_redemption_id_idx ON games.redemption_line (redemption_id);
-- declared: identity.access_policy_version.current_id -> identity.access_policy
CREATE INDEX IF NOT EXISTS access_policy_version_current_id_idx ON identity.access_policy_version (current_id);
-- declared: identity.access_policy_version.previous_id -> identity.access_policy
CREATE INDEX IF NOT EXISTS access_policy_version_previous_id_idx ON identity.access_policy_version (previous_id);
-- declared: identity.authz_audit.actor_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS authz_audit_actor_principal_id_idx ON identity.authz_audit (actor_principal_id);
-- declared: identity.authz_audit.subject_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS authz_audit_subject_principal_id_idx ON identity.authz_audit (subject_principal_id);
-- declared: identity.delegated_access.created_by_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS delegated_access_created_by_principal_id_idx ON identity.delegated_access (created_by_principal_id);
-- declared: identity.delegated_access.granted_by_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS delegated_access_granted_by_principal_id_idx ON identity.delegated_access (granted_by_principal_id);
-- declared: identity.delegated_access.principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS delegated_access_principal_id_idx ON identity.delegated_access (principal_id);
-- declared: identity.delegated_access.revoked_by_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS delegated_access_revoked_by_principal_id_idx ON identity.delegated_access (revoked_by_principal_id);
-- declared: identity.delegated_access.role_id -> identity.role
CREATE INDEX IF NOT EXISTS delegated_access_role_id_idx ON identity.delegated_access (role_id);
-- declared: identity.delegated_access.scope_id -> platform.scope
CREATE INDEX IF NOT EXISTS delegated_access_scope_id_idx ON identity.delegated_access (scope_id);
-- declared: identity.delegated_access.subject_id -> pii.subject
CREATE INDEX IF NOT EXISTS delegated_access_subject_id_idx ON identity.delegated_access (subject_id);
-- declared: identity.mfa_challenge.principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS mfa_challenge_principal_id_idx ON identity.mfa_challenge (principal_id);
-- declared: identity.mfa_method.principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS mfa_method_principal_id_idx ON identity.mfa_method (principal_id);
-- declared: identity.mfa_recovery_code.principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS mfa_recovery_code_principal_id_idx ON identity.mfa_recovery_code (principal_id);
-- declared: identity.otp_challenge.subject_id -> pii.subject
CREATE INDEX IF NOT EXISTS otp_challenge_subject_id_idx ON identity.otp_challenge (subject_id);
-- declared: identity.principal.home_scope_id -> platform.scope
CREATE INDEX IF NOT EXISTS principal_home_scope_id_idx ON identity.principal (home_scope_id);
-- declared: identity.principal.primary_role_id -> identity.role
CREATE INDEX IF NOT EXISTS principal_primary_role_id_idx ON identity.principal (primary_role_id);
-- declared: identity.principal_credential.principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS principal_credential_principal_id_idx ON identity.principal_credential (principal_id);
-- declared: identity.role_permission.role_id -> identity.role
CREATE INDEX IF NOT EXISTS role_permission_role_id_idx ON identity.role_permission (role_id);
-- declared: identity.sso_group_mapping.provider_id -> identity.sso_provider
CREATE INDEX IF NOT EXISTS sso_group_mapping_provider_id_idx ON identity.sso_group_mapping (provider_id);
-- declared: identity.sso_group_mapping.role_id -> identity.role
CREATE INDEX IF NOT EXISTS sso_group_mapping_role_id_idx ON identity.sso_group_mapping (role_id);
-- declared: identity.sso_group_mapping.scope_id -> platform.scope
CREATE INDEX IF NOT EXISTS sso_group_mapping_scope_id_idx ON identity.sso_group_mapping (scope_id);
-- declared: inventory.count.journal_entry_id -> ledger.journal_entry
CREATE INDEX IF NOT EXISTS count_journal_entry_id_idx ON inventory.count (journal_entry_id);
-- declared: inventory.count.posted_by_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS count_posted_by_principal_id_idx ON inventory.count (posted_by_principal_id);
-- declared: inventory.count.started_by_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS count_started_by_principal_id_idx ON inventory.count (started_by_principal_id);
-- declared: inventory.count_line.count_id -> inventory.count
CREATE INDEX IF NOT EXISTS count_line_count_id_idx ON inventory.count_line (count_id);
-- declared: inventory.goods_receipt.journal_entry_id -> ledger.journal_entry
CREATE INDEX IF NOT EXISTS goods_receipt_journal_entry_id_idx ON inventory.goods_receipt (journal_entry_id);
-- declared: inventory.goods_receipt.purchase_order_id -> inventory.purchase_order
CREATE INDEX IF NOT EXISTS goods_receipt_purchase_order_id_idx ON inventory.goods_receipt (purchase_order_id);
-- declared: inventory.goods_receipt.received_by_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS goods_receipt_received_by_principal_id_idx ON inventory.goods_receipt (received_by_principal_id);
-- declared: inventory.goods_receipt_line.goods_receipt_id -> inventory.goods_receipt
CREATE INDEX IF NOT EXISTS goods_receipt_line_goods_receipt_id_idx ON inventory.goods_receipt_line (goods_receipt_id);
-- declared: inventory.goods_receipt_line.item_id -> inventory.item
CREATE INDEX IF NOT EXISTS goods_receipt_line_item_id_idx ON inventory.goods_receipt_line (item_id);
-- declared: inventory.item.preferred_supplier_id -> inventory.supplier
CREATE INDEX IF NOT EXISTS item_preferred_supplier_id_idx ON inventory.item (preferred_supplier_id);
-- declared: inventory.item.venue_id -> platform.scope
CREATE INDEX IF NOT EXISTS item_venue_id_idx ON inventory.item (venue_id);
-- declared: inventory.location.venue_id -> platform.scope
CREATE INDEX IF NOT EXISTS location_venue_id_idx ON inventory.location (venue_id);
-- declared: inventory.movement.cost_center_id -> ledger.cost_center
CREATE INDEX IF NOT EXISTS movement_cost_center_id_idx ON inventory.movement (cost_center_id);
-- declared: inventory.movement.item_id -> inventory.item
CREATE INDEX IF NOT EXISTS movement_item_id_idx ON inventory.movement (item_id);
-- declared: inventory.movement.journal_entry_id -> ledger.journal_entry
CREATE INDEX IF NOT EXISTS movement_journal_entry_id_idx ON inventory.movement (journal_entry_id);
-- declared: inventory.movement.principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS movement_principal_id_idx ON inventory.movement (principal_id);
-- declared: inventory.purchase_order.raised_by_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS purchase_order_raised_by_principal_id_idx ON inventory.purchase_order (raised_by_principal_id);
-- declared: inventory.purchase_order.requisition_id -> inventory.requisition
CREATE INDEX IF NOT EXISTS purchase_order_requisition_id_idx ON inventory.purchase_order (requisition_id);
-- declared: inventory.purchase_order.supplier_id -> inventory.supplier
CREATE INDEX IF NOT EXISTS purchase_order_supplier_id_idx ON inventory.purchase_order (supplier_id);
-- declared: inventory.purchase_order.venue_id -> platform.scope
CREATE INDEX IF NOT EXISTS purchase_order_venue_id_idx ON inventory.purchase_order (venue_id);
-- declared: inventory.purchase_order_line.item_id -> inventory.item
CREATE INDEX IF NOT EXISTS purchase_order_line_item_id_idx ON inventory.purchase_order_line (item_id);
-- declared: inventory.purchase_order_line.purchase_order_id -> inventory.purchase_order
CREATE INDEX IF NOT EXISTS purchase_order_line_purchase_order_id_idx ON inventory.purchase_order_line (purchase_order_id);
-- declared: inventory.quotation.requisition_id -> inventory.requisition
CREATE INDEX IF NOT EXISTS quotation_requisition_id_idx ON inventory.quotation (requisition_id);
-- declared: inventory.quotation.supplier_id -> inventory.supplier
CREATE INDEX IF NOT EXISTS quotation_supplier_id_idx ON inventory.quotation (supplier_id);
-- declared: inventory.quotation_line.item_id -> inventory.item
CREATE INDEX IF NOT EXISTS quotation_line_item_id_idx ON inventory.quotation_line (item_id);
-- declared: inventory.quotation_line.quotation_id -> inventory.quotation
CREATE INDEX IF NOT EXISTS quotation_line_quotation_id_idx ON inventory.quotation_line (quotation_id);
-- declared: inventory.requisition.approved_by_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS requisition_approved_by_principal_id_idx ON inventory.requisition (approved_by_principal_id);
-- declared: inventory.requisition.department_id -> platform.scope
CREATE INDEX IF NOT EXISTS requisition_department_id_idx ON inventory.requisition (department_id);
-- declared: inventory.requisition.raised_by_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS requisition_raised_by_principal_id_idx ON inventory.requisition (raised_by_principal_id);
-- declared: inventory.requisition.venue_id -> platform.scope
CREATE INDEX IF NOT EXISTS requisition_venue_id_idx ON inventory.requisition (venue_id);
-- declared: inventory.requisition_line.item_id -> inventory.item
CREATE INDEX IF NOT EXISTS requisition_line_item_id_idx ON inventory.requisition_line (item_id);
-- declared: inventory.requisition_line.requisition_id -> inventory.requisition
CREATE INDEX IF NOT EXISTS requisition_line_requisition_id_idx ON inventory.requisition_line (requisition_id);
-- declared: inventory.stock_batch.item_id -> inventory.item
CREATE INDEX IF NOT EXISTS stock_batch_item_id_idx ON inventory.stock_batch (item_id);
-- declared: inventory.stock_batch.location_id -> inventory.location
CREATE INDEX IF NOT EXISTS stock_batch_location_id_idx ON inventory.stock_batch (location_id);
-- declared: inventory.stock_batch.supplier_id -> inventory.supplier
CREATE INDEX IF NOT EXISTS stock_batch_supplier_id_idx ON inventory.stock_batch (supplier_id);
-- declared: inventory.supplier.account_id -> ledger.account
CREATE INDEX IF NOT EXISTS supplier_account_id_idx ON inventory.supplier (account_id);
-- declared: inventory.transfer.dispatched_by_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS transfer_dispatched_by_principal_id_idx ON inventory.transfer (dispatched_by_principal_id);
-- declared: inventory.transfer.received_by_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS transfer_received_by_principal_id_idx ON inventory.transfer (received_by_principal_id);
-- declared: inventory.transfer_line.item_id -> inventory.item
CREATE INDEX IF NOT EXISTS transfer_line_item_id_idx ON inventory.transfer_line (item_id);
-- declared: inventory.transfer_line.transfer_id -> inventory.transfer
CREATE INDEX IF NOT EXISTS transfer_line_transfer_id_idx ON inventory.transfer_line (transfer_id);
-- declared: ledger.account.legal_entity_id -> ledger.legal_entity
CREATE INDEX IF NOT EXISTS account_legal_entity_id_idx ON ledger.account (legal_entity_id);
-- declared: ledger.account_mapping.credit_account_id -> ledger.account
CREATE INDEX IF NOT EXISTS account_mapping_credit_account_id_idx ON ledger.account_mapping (credit_account_id);
-- declared: ledger.account_mapping.debit_account_id -> ledger.account
CREATE INDEX IF NOT EXISTS account_mapping_debit_account_id_idx ON ledger.account_mapping (debit_account_id);
-- declared: ledger.account_mapping.venue_id -> platform.scope
CREATE INDEX IF NOT EXISTS account_mapping_venue_id_idx ON ledger.account_mapping (venue_id);
-- declared: ledger.cost_center.venue_id -> platform.scope
CREATE INDEX IF NOT EXISTS cost_center_venue_id_idx ON ledger.cost_center (venue_id);
-- declared: ledger.deposit.order_id -> orders.sales_order
CREATE INDEX IF NOT EXISTS deposit_order_id_idx ON ledger.deposit (order_id);
-- declared: ledger.deposit.subject_id -> pii.subject
CREATE INDEX IF NOT EXISTS deposit_subject_id_idx ON ledger.deposit (subject_id);
-- declared: ledger.event_budget.cost_center_id -> ledger.cost_center
CREATE INDEX IF NOT EXISTS event_budget_cost_center_id_idx ON ledger.event_budget (cost_center_id);
-- declared: ledger.event_budget.event_id -> catalogue.event
CREATE INDEX IF NOT EXISTS event_budget_event_id_idx ON ledger.event_budget (event_id);
-- declared: ledger.fiscal_period.closed_by_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS fiscal_period_closed_by_principal_id_idx ON ledger.fiscal_period (closed_by_principal_id);
-- declared: ledger.fiscal_period.legal_entity_id -> ledger.legal_entity
CREATE INDEX IF NOT EXISTS fiscal_period_legal_entity_id_idx ON ledger.fiscal_period (legal_entity_id);
-- declared: ledger.fiscal_period_event.fiscal_period_id -> ledger.fiscal_period
CREATE INDEX IF NOT EXISTS fiscal_period_event_fiscal_period_id_idx ON ledger.fiscal_period_event (fiscal_period_id);
-- declared: ledger.fx_rate.region_id -> platform.scope
CREATE INDEX IF NOT EXISTS fx_rate_region_id_idx ON ledger.fx_rate (region_id);
-- declared: ledger.inter_entity_obligation.entitlement_id -> access.entitlement
CREATE INDEX IF NOT EXISTS inter_entity_obligation_entitlement_id_idx ON ledger.inter_entity_obligation (entitlement_id);
-- declared: ledger.inter_entity_obligation.order_id -> orders.sales_order
CREATE INDEX IF NOT EXISTS inter_entity_obligation_order_id_idx ON ledger.inter_entity_obligation (order_id);
-- declared: ledger.journal_entry.approved_by_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS journal_entry_approved_by_principal_id_idx ON ledger.journal_entry (approved_by_principal_id);
-- declared: ledger.journal_entry.fiscal_period_id -> ledger.fiscal_period
CREATE INDEX IF NOT EXISTS journal_entry_fiscal_period_id_idx ON ledger.journal_entry (fiscal_period_id);
-- declared: ledger.journal_entry.posted_by_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS journal_entry_posted_by_principal_id_idx ON ledger.journal_entry (posted_by_principal_id);
-- declared: ledger.journal_line.journal_entry_id -> ledger.journal_entry
CREATE INDEX IF NOT EXISTS journal_line_journal_entry_id_idx ON ledger.journal_line (journal_entry_id);
-- declared: ledger.journal_line.venue_id -> platform.scope
CREATE INDEX IF NOT EXISTS journal_line_venue_id_idx ON ledger.journal_line (venue_id);
-- declared: ledger.posting.account_id -> ledger.account
CREATE INDEX IF NOT EXISTS posting_account_id_idx ON ledger.posting (account_id);
-- declared: ledger.posting.cost_center_id -> ledger.cost_center
CREATE INDEX IF NOT EXISTS posting_cost_center_id_idx ON ledger.posting (cost_center_id);
-- declared: ledger.posting.journal_entry_id -> ledger.journal_entry
CREATE INDEX IF NOT EXISTS posting_journal_entry_id_idx ON ledger.posting (journal_entry_id);
-- declared: ledger.posting.venue_id -> platform.scope
CREATE INDEX IF NOT EXISTS posting_venue_id_idx ON ledger.posting (venue_id);
-- declared: ledger.price_variance.journal_entry_id -> ledger.journal_entry
CREATE INDEX IF NOT EXISTS price_variance_journal_entry_id_idx ON ledger.price_variance (journal_entry_id);
-- declared: ledger.price_variance.order_id -> orders.sales_order
CREATE INDEX IF NOT EXISTS price_variance_order_id_idx ON ledger.price_variance (order_id);
-- declared: ledger.price_variance.order_line_id -> orders.order_line
CREATE INDEX IF NOT EXISTS price_variance_order_line_id_idx ON ledger.price_variance (order_line_id);
-- declared: ledger.price_variance.reviewed_by_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS price_variance_reviewed_by_principal_id_idx ON ledger.price_variance (reviewed_by_principal_id);
-- declared: ledger.price_variance.variant_id -> catalogue.variant
CREATE INDEX IF NOT EXISTS price_variance_variant_id_idx ON ledger.price_variance (variant_id);
-- declared: ledger.price_variance.venue_id -> platform.scope
CREATE INDEX IF NOT EXISTS price_variance_venue_id_idx ON ledger.price_variance (venue_id);
-- declared: ledger.recognition_schedule.breakage_account_id -> ledger.account
CREATE INDEX IF NOT EXISTS recognition_schedule_breakage_account_id_idx ON ledger.recognition_schedule (breakage_account_id);
-- declared: ledger.recognition_schedule.deferred_account_id -> ledger.account
CREATE INDEX IF NOT EXISTS recognition_schedule_deferred_account_id_idx ON ledger.recognition_schedule (deferred_account_id);
-- declared: ledger.recognition_schedule.recognised_account_id -> ledger.account
CREATE INDEX IF NOT EXISTS recognition_schedule_recognised_account_id_idx ON ledger.recognition_schedule (recognised_account_id);
-- declared: ledger.settlement_exception.payment_id -> orders.payment
CREATE INDEX IF NOT EXISTS settlement_exception_payment_id_idx ON ledger.settlement_exception (payment_id);
-- declared: ledger.settlement_exception.resolved_by_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS settlement_exception_resolved_by_principal_id_idx ON ledger.settlement_exception (resolved_by_principal_id);
-- declared: ledger.settlement_exception.settlement_id -> ledger.settlement
CREATE INDEX IF NOT EXISTS settlement_exception_settlement_id_idx ON ledger.settlement_exception (settlement_id);
-- declared: ledger.tax_code.account_id -> ledger.account
CREATE INDEX IF NOT EXISTS tax_code_account_id_idx ON ledger.tax_code (account_id);
-- declared: ledger.tax_exemption.tax_code_id -> ledger.tax_code
CREATE INDEX IF NOT EXISTS tax_exemption_tax_code_id_idx ON ledger.tax_exemption (tax_code_id);
-- declared: maintenance.asset.linked_access_point_id -> access.access_point
CREATE INDEX IF NOT EXISTS asset_linked_access_point_id_idx ON maintenance.asset (linked_access_point_id);
-- declared: maintenance.asset.supplier_id -> inventory.supplier
CREATE INDEX IF NOT EXISTS asset_supplier_id_idx ON maintenance.asset (supplier_id);
-- declared: maintenance.asset.venue_id -> platform.scope
CREATE INDEX IF NOT EXISTS asset_venue_id_idx ON maintenance.asset (venue_id);
-- declared: maintenance.incident.asset_id -> maintenance.asset
CREATE INDEX IF NOT EXISTS incident_asset_id_idx ON maintenance.incident (asset_id);
-- declared: maintenance.incident.assigned_to_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS incident_assigned_to_principal_id_idx ON maintenance.incident (assigned_to_principal_id);
-- declared: maintenance.incident.corrective_work_order_id -> maintenance.work_order
CREATE INDEX IF NOT EXISTS incident_corrective_work_order_id_idx ON maintenance.incident (corrective_work_order_id);
-- declared: maintenance.incident.reported_by_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS incident_reported_by_principal_id_idx ON maintenance.incident (reported_by_principal_id);
-- declared: maintenance.incident.venue_id -> platform.scope
CREATE INDEX IF NOT EXISTS incident_venue_id_idx ON maintenance.incident (venue_id);
-- declared: maintenance.inspection.asset_id -> maintenance.asset
CREATE INDEX IF NOT EXISTS inspection_asset_id_idx ON maintenance.inspection (asset_id);
-- declared: maintenance.inspection.performed_by_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS inspection_performed_by_principal_id_idx ON maintenance.inspection (performed_by_principal_id);
-- declared: maintenance.inspection.venue_id -> platform.scope
CREATE INDEX IF NOT EXISTS inspection_venue_id_idx ON maintenance.inspection (venue_id);
-- declared: maintenance.inspection_item.inspection_id -> maintenance.inspection
CREATE INDEX IF NOT EXISTS inspection_item_inspection_id_idx ON maintenance.inspection_item (inspection_id);
-- declared: maintenance.inspection_template.venue_id -> platform.scope
CREATE INDEX IF NOT EXISTS inspection_template_venue_id_idx ON maintenance.inspection_template (venue_id);
-- declared: maintenance.inspection_template_item.inspection_template_id -> maintenance.inspection_template
CREATE INDEX IF NOT EXISTS inspection_template_item_inspection_template_id_idx ON maintenance.inspection_template_item (inspection_template_id);
-- declared: maintenance.preventive_plan.asset_id -> maintenance.asset
CREATE INDEX IF NOT EXISTS preventive_plan_asset_id_idx ON maintenance.preventive_plan (asset_id);
-- declared: maintenance.work_order.asset_id -> maintenance.asset
CREATE INDEX IF NOT EXISTS work_order_asset_id_idx ON maintenance.work_order (asset_id);
-- declared: maintenance.work_order.assigned_to_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS work_order_assigned_to_principal_id_idx ON maintenance.work_order (assigned_to_principal_id);
-- declared: maintenance.work_order.raised_by_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS work_order_raised_by_principal_id_idx ON maintenance.work_order (raised_by_principal_id);
-- declared: maintenance.work_order.source_incident_id -> maintenance.incident
CREATE INDEX IF NOT EXISTS work_order_source_incident_id_idx ON maintenance.work_order (source_incident_id);
-- declared: maintenance.work_order.source_inspection_id -> maintenance.inspection
CREATE INDEX IF NOT EXISTS work_order_source_inspection_id_idx ON maintenance.work_order (source_inspection_id);
-- declared: maintenance.work_order.venue_id -> platform.scope
CREATE INDEX IF NOT EXISTS work_order_venue_id_idx ON maintenance.work_order (venue_id);
-- declared: maintenance.work_order_attachment.asset_ref -> assets.media_asset
CREATE INDEX IF NOT EXISTS work_order_attachment_asset_ref_idx ON maintenance.work_order_attachment (asset_ref);
-- declared: maintenance.work_order_attachment.work_order_id -> maintenance.work_order
CREATE INDEX IF NOT EXISTS work_order_attachment_work_order_id_idx ON maintenance.work_order_attachment (work_order_id);
-- declared: marketing.agent_availability.principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS agent_availability_principal_id_idx ON marketing.agent_availability (principal_id);
-- declared: marketing.attribution_touch.campaign_id -> marketing.campaign
CREATE INDEX IF NOT EXISTS attribution_touch_campaign_id_idx ON marketing.attribution_touch (campaign_id);
-- declared: marketing.attribution_touch.journey_id -> marketing.journey
CREATE INDEX IF NOT EXISTS attribution_touch_journey_id_idx ON marketing.attribution_touch (journey_id);
-- declared: marketing.attribution_touch.order_id -> orders.sales_order
CREATE INDEX IF NOT EXISTS attribution_touch_order_id_idx ON marketing.attribution_touch (order_id);
-- declared: marketing.attribution_touch.subject_id -> pii.subject
CREATE INDEX IF NOT EXISTS attribution_touch_subject_id_idx ON marketing.attribution_touch (subject_id);
-- declared: marketing.campaign.created_by_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS campaign_created_by_principal_id_idx ON marketing.campaign (created_by_principal_id);
-- declared: marketing.campaign.segment_id -> marketing.segment
CREATE INDEX IF NOT EXISTS campaign_segment_id_idx ON marketing.campaign (segment_id);
-- declared: marketing.campaign.venue_id -> platform.scope
CREATE INDEX IF NOT EXISTS campaign_venue_id_idx ON marketing.campaign (venue_id);
-- declared: marketing.case.assigned_to_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS case_assigned_to_principal_id_idx ON marketing."case" (assigned_to_principal_id);
-- declared: marketing.case.related_order_id -> orders.sales_order
CREATE INDEX IF NOT EXISTS case_related_order_id_idx ON marketing."case" (related_order_id);
-- declared: marketing.case.subject_id -> pii.subject
CREATE INDEX IF NOT EXISTS case_subject_id_idx ON marketing."case" (subject_id);
-- declared: marketing.case.venue_id -> platform.scope
CREATE INDEX IF NOT EXISTS case_venue_id_idx ON marketing."case" (venue_id);
-- declared: marketing.case_message.author_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS case_message_author_principal_id_idx ON marketing.case_message (author_principal_id);
-- declared: marketing.case_message.case_id -> marketing.case
CREATE INDEX IF NOT EXISTS case_message_case_id_idx ON marketing.case_message (case_id);
-- declared: marketing.challenge.event_id -> catalogue.event
CREATE INDEX IF NOT EXISTS challenge_event_id_idx ON marketing.challenge (event_id);
-- declared: marketing.challenge_progress.challenge_id -> marketing.challenge
CREATE INDEX IF NOT EXISTS challenge_progress_challenge_id_idx ON marketing.challenge_progress (challenge_id);
-- declared: marketing.challenge_progress.subject_id -> pii.subject
CREATE INDEX IF NOT EXISTS challenge_progress_subject_id_idx ON marketing.challenge_progress (subject_id);
-- declared: marketing.consent_purpose.tenant_id -> platform.tenant
CREATE INDEX IF NOT EXISTS consent_purpose_tenant_id_idx ON marketing.consent_purpose (tenant_id);
-- declared: marketing.consent_purpose_channel.consent_purpose_id -> marketing.consent_purpose
CREATE INDEX IF NOT EXISTS consent_purpose_channel_consent_purpose_id_idx ON marketing.consent_purpose_channel (consent_purpose_id);
-- declared: marketing.consent_record.recorded_by_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS consent_record_recorded_by_principal_id_idx ON marketing.consent_record (recorded_by_principal_id);
-- declared: marketing.consent_record.subject_id -> pii.subject
CREATE INDEX IF NOT EXISTS consent_record_subject_id_idx ON marketing.consent_record (subject_id);
-- declared: marketing.consent_record_channel.consent_record_id -> marketing.consent_record
CREATE INDEX IF NOT EXISTS consent_record_channel_consent_record_id_idx ON marketing.consent_record_channel (consent_record_id);
-- declared: marketing.conversation.assigned_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS conversation_assigned_principal_id_idx ON marketing.conversation (assigned_principal_id);
-- declared: marketing.conversation.case_id -> marketing.case
CREATE INDEX IF NOT EXISTS conversation_case_id_idx ON marketing.conversation (case_id);
-- declared: marketing.conversation.queue_id -> queue.queue
CREATE INDEX IF NOT EXISTS conversation_queue_id_idx ON marketing.conversation (queue_id);
-- declared: marketing.conversation.subject_id -> pii.subject
CREATE INDEX IF NOT EXISTS conversation_subject_id_idx ON marketing.conversation (subject_id);
-- declared: marketing.conversation.venue_id -> platform.scope
CREATE INDEX IF NOT EXISTS conversation_venue_id_idx ON marketing.conversation (venue_id);
-- declared: marketing.conversation_message.ai_interaction_id -> ai.activity
CREATE INDEX IF NOT EXISTS conversation_message_ai_interaction_id_idx ON marketing.conversation_message (ai_interaction_id);
-- declared: marketing.conversation_message.conversation_id -> marketing.conversation
CREATE INDEX IF NOT EXISTS conversation_message_conversation_id_idx ON marketing.conversation_message (conversation_id);
-- declared: marketing.conversation_message_attachment.conversation_message_id -> marketing.conversation_message
CREATE INDEX IF NOT EXISTS conversation_message_attachment_conversation_message_id_idx ON marketing.conversation_message_attachment (conversation_message_id);
-- declared: marketing.form_definition_field.form_definition_id -> marketing.form_definition
CREATE INDEX IF NOT EXISTS form_definition_field_form_definition_id_idx ON marketing.form_definition_field (form_definition_id);
-- declared: marketing.form_submission.subject_id -> pii.subject
CREATE INDEX IF NOT EXISTS form_submission_subject_id_idx ON marketing.form_submission (subject_id);
-- declared: marketing.guest_device.subject_id -> pii.subject
CREATE INDEX IF NOT EXISTS guest_device_subject_id_idx ON marketing.guest_device (subject_id);
-- declared: marketing.guest_document.consent_purpose_id -> marketing.consent_purpose
CREATE INDEX IF NOT EXISTS guest_document_consent_purpose_id_idx ON marketing.guest_document (consent_purpose_id);
-- declared: marketing.guest_document.subject_id -> pii.subject
CREATE INDEX IF NOT EXISTS guest_document_subject_id_idx ON marketing.guest_document (subject_id);
-- declared: marketing.guest_profile.guest_link_id -> platform.guest_link
CREATE INDEX IF NOT EXISTS guest_profile_guest_link_id_idx ON marketing.guest_profile (guest_link_id);
-- declared: marketing.guest_profile.loyalty_position_id -> marketing.loyalty_position
CREATE INDEX IF NOT EXISTS guest_profile_loyalty_position_id_idx ON marketing.guest_profile (loyalty_position_id);
-- declared: marketing.guest_profile.segment_id -> marketing.segment
CREATE INDEX IF NOT EXISTS guest_profile_segment_id_idx ON marketing.guest_profile (segment_id);
-- declared: marketing.guest_profile.subject_id -> pii.subject
CREATE INDEX IF NOT EXISTS guest_profile_subject_id_idx ON marketing.guest_profile (subject_id);
-- declared: marketing.invitation.cost_center_id -> ledger.cost_center
CREATE INDEX IF NOT EXISTS invitation_cost_center_id_idx ON marketing.invitation (cost_center_id);
-- declared: marketing.invitation.performance_id -> catalogue.performance
CREATE INDEX IF NOT EXISTS invitation_performance_id_idx ON marketing.invitation (performance_id);
-- declared: marketing.invitation.product_id -> catalogue.product
CREATE INDEX IF NOT EXISTS invitation_product_id_idx ON marketing.invitation (product_id);
-- declared: marketing.invitation_campaign.event_id -> catalogue.event
CREATE INDEX IF NOT EXISTS invitation_campaign_event_id_idx ON marketing.invitation_campaign (event_id);
-- declared: marketing.invitation_campaign.product_id -> catalogue.product
CREATE INDEX IF NOT EXISTS invitation_campaign_product_id_idx ON marketing.invitation_campaign (product_id);
-- declared: marketing.journey_step.journey_id -> marketing.journey
CREATE INDEX IF NOT EXISTS journey_step_journey_id_idx ON marketing.journey_step (journey_id);
-- declared: marketing.kiosk_assist_session.cart_id -> orders.cart
CREATE INDEX IF NOT EXISTS kiosk_assist_session_cart_id_idx ON marketing.kiosk_assist_session (cart_id);
-- declared: marketing.kiosk_assist_session.staff_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS kiosk_assist_session_staff_principal_id_idx ON marketing.kiosk_assist_session (staff_principal_id);
-- declared: marketing.kiosk_assist_session.venue_id -> platform.scope
CREATE INDEX IF NOT EXISTS kiosk_assist_session_venue_id_idx ON marketing.kiosk_assist_session (venue_id);
-- declared: marketing.lost_item.venue_id -> platform.scope
CREATE INDEX IF NOT EXISTS lost_item_venue_id_idx ON marketing.lost_item (venue_id);
-- declared: marketing.loyalty_position.programme_id -> marketing.loyalty_programme
CREATE INDEX IF NOT EXISTS loyalty_position_programme_id_idx ON marketing.loyalty_position (programme_id);
-- declared: marketing.loyalty_position.subject_id -> pii.subject
CREATE INDEX IF NOT EXISTS loyalty_position_subject_id_idx ON marketing.loyalty_position (subject_id);
-- declared: marketing.loyalty_programme.points_liability_account_id -> ledger.account
CREATE INDEX IF NOT EXISTS loyalty_programme_points_liability_account_id_idx ON marketing.loyalty_programme (points_liability_account_id);
-- declared: marketing.loyalty_programme.venue_id -> platform.scope
CREATE INDEX IF NOT EXISTS loyalty_programme_venue_id_idx ON marketing.loyalty_programme (venue_id);
-- declared: marketing.message_delivery.campaign_id -> marketing.campaign
CREATE INDEX IF NOT EXISTS message_delivery_campaign_id_idx ON marketing.message_delivery (campaign_id);
-- declared: marketing.message_dispatch.campaign_id -> marketing.campaign
CREATE INDEX IF NOT EXISTS message_dispatch_campaign_id_idx ON marketing.message_dispatch (campaign_id);
-- declared: marketing.message_dispatch.subject_id -> pii.subject
CREATE INDEX IF NOT EXISTS message_dispatch_subject_id_idx ON marketing.message_dispatch (subject_id);
-- declared: marketing.message_template.tenant_id -> platform.tenant
CREATE INDEX IF NOT EXISTS message_template_tenant_id_idx ON marketing.message_template (tenant_id);
-- declared: marketing.points_earning_rule.loyalty_programme_id -> marketing.loyalty_programme
CREATE INDEX IF NOT EXISTS points_earning_rule_loyalty_programme_id_idx ON marketing.points_earning_rule (loyalty_programme_id);
-- declared: marketing.points_redemption_rule.product_id -> catalogue.product
CREATE INDEX IF NOT EXISTS points_redemption_rule_product_id_idx ON marketing.points_redemption_rule (product_id);
-- declared: marketing.programme_tier.loyalty_programme_id -> marketing.loyalty_programme
CREATE INDEX IF NOT EXISTS programme_tier_loyalty_programme_id_idx ON marketing.programme_tier (loyalty_programme_id);
-- declared: marketing.review.opened_case_id -> marketing.case
CREATE INDEX IF NOT EXISTS review_opened_case_id_idx ON marketing.review (opened_case_id);
-- declared: marketing.review.related_order_id -> orders.sales_order
CREATE INDEX IF NOT EXISTS review_related_order_id_idx ON marketing.review (related_order_id);
-- declared: marketing.review.responded_by_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS review_responded_by_principal_id_idx ON marketing.review (responded_by_principal_id);
-- declared: marketing.review.subject_id -> pii.subject
CREATE INDEX IF NOT EXISTS review_subject_id_idx ON marketing.review (subject_id);
-- declared: marketing.review.venue_id -> platform.scope
CREATE INDEX IF NOT EXISTS review_venue_id_idx ON marketing.review (venue_id);
-- declared: marketing.reward.product_id -> catalogue.product
CREATE INDEX IF NOT EXISTS reward_product_id_idx ON marketing.reward (product_id);
-- declared: marketing.segment.venue_id -> platform.scope
CREATE INDEX IF NOT EXISTS segment_venue_id_idx ON marketing.segment (venue_id);
-- declared: marketing.segment_criterion.segment_id -> marketing.segment
CREATE INDEX IF NOT EXISTS segment_criterion_segment_id_idx ON marketing.segment_criterion (segment_id);
-- declared: marketing.suppression.suppressed_by_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS suppression_suppressed_by_principal_id_idx ON marketing.suppression (suppressed_by_principal_id);
-- declared: marketing.touch_point.campaign_id -> marketing.campaign
CREATE INDEX IF NOT EXISTS touch_point_campaign_id_idx ON marketing.touch_point (campaign_id);
-- declared: marketing.touch_point.journey_id -> marketing.journey
CREATE INDEX IF NOT EXISTS touch_point_journey_id_idx ON marketing.touch_point (journey_id);
-- declared: marketing.touch_point.order_id -> orders.sales_order
CREATE INDEX IF NOT EXISTS touch_point_order_id_idx ON marketing.touch_point (order_id);
-- declared: marketing.touch_point.subject_id -> pii.subject
CREATE INDEX IF NOT EXISTS touch_point_subject_id_idx ON marketing.touch_point (subject_id);
-- declared: marketing.wishlist_item.performance_id -> catalogue.performance
CREATE INDEX IF NOT EXISTS wishlist_item_performance_id_idx ON marketing.wishlist_item (performance_id);
-- declared: marketing.wishlist_item.subject_id -> pii.subject
CREATE INDEX IF NOT EXISTS wishlist_item_subject_id_idx ON marketing.wishlist_item (subject_id);
-- declared: marketing.wishlist_item.variant_id -> catalogue.variant
CREATE INDEX IF NOT EXISTS wishlist_item_variant_id_idx ON marketing.wishlist_item (variant_id);
-- declared: orders.b2b_credit.account_id -> ledger.account
CREATE INDEX IF NOT EXISTS b2b_credit_account_id_idx ON orders.b2b_credit (account_id);
-- declared: orders.cart.subject_id -> pii.subject
CREATE INDEX IF NOT EXISTS cart_subject_id_idx ON orders.cart (subject_id);
-- declared: orders.cart.venue_id -> platform.scope
CREATE INDEX IF NOT EXISTS cart_venue_id_idx ON orders.cart (venue_id);
-- declared: orders.cart_line.cart_id -> orders.cart
CREATE INDEX IF NOT EXISTS cart_line_cart_id_idx ON orders.cart_line (cart_id);
-- declared: orders.cart_line.inventory_hold_id -> catalogue.inventory_hold
CREATE INDEX IF NOT EXISTS cart_line_inventory_hold_id_idx ON orders.cart_line (inventory_hold_id);
-- declared: orders.cart_line.performance_id -> catalogue.performance
CREATE INDEX IF NOT EXISTS cart_line_performance_id_idx ON orders.cart_line (performance_id);
-- declared: orders.cart_line.variant_id -> catalogue.variant
CREATE INDEX IF NOT EXISTS cart_line_variant_id_idx ON orders.cart_line (variant_id);
-- declared: orders.cash_count_line.shift_id -> orders.pos_shift
CREATE INDEX IF NOT EXISTS cash_count_line_shift_id_idx ON orders.cash_count_line (shift_id);
-- declared: orders.cash_movement.authorised_by_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS cash_movement_authorised_by_principal_id_idx ON orders.cash_movement (authorised_by_principal_id);
-- declared: orders.cash_movement.shift_id -> orders.pos_shift
CREATE INDEX IF NOT EXISTS cash_movement_shift_id_idx ON orders.cash_movement (shift_id);
-- declared: orders.chargeback.payment_id -> orders.payment
CREATE INDEX IF NOT EXISTS chargeback_payment_id_idx ON orders.chargeback (payment_id);
-- declared: orders.credit_override.b2b_credit_id -> orders.b2b_credit
CREATE INDEX IF NOT EXISTS credit_override_b2b_credit_id_idx ON orders.credit_override (b2b_credit_id);
-- declared: orders.credit_override.order_id -> orders.sales_order
CREATE INDEX IF NOT EXISTS credit_override_order_id_idx ON orders.credit_override (order_id);
-- declared: orders.deposit.order_id -> orders.sales_order
CREATE INDEX IF NOT EXISTS deposit_order_id_idx ON orders.deposit (order_id);
-- declared: orders.deposit_box.cashier_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS deposit_box_cashier_principal_id_idx ON orders.deposit_box (cashier_principal_id);
-- declared: orders.deposit_box.shift_id -> orders.pos_shift
CREATE INDEX IF NOT EXISTS deposit_box_shift_id_idx ON orders.deposit_box (shift_id);
-- declared: orders.deposit_box.venue_id -> platform.scope
CREATE INDEX IF NOT EXISTS deposit_box_venue_id_idx ON orders.deposit_box (venue_id);
-- declared: orders.deposit_box.workstation_id -> platform.workstation
CREATE INDEX IF NOT EXISTS deposit_box_workstation_id_idx ON orders.deposit_box (workstation_id);
-- declared: orders.deposit_box_foreign_holding.deposit_box_id -> orders.deposit_box
CREATE INDEX IF NOT EXISTS deposit_box_foreign_holding_deposit_box_id_idx ON orders.deposit_box_foreign_holding (deposit_box_id);
-- declared: orders.deposit_box_opening_denomination.deposit_box_id -> orders.deposit_box
CREATE INDEX IF NOT EXISTS deposit_box_opening_denomination_deposit_box_id_idx ON orders.deposit_box_opening_denomination (deposit_box_id);
-- declared: orders.discount.order_id -> orders.sales_order
CREATE INDEX IF NOT EXISTS discount_order_id_idx ON orders.discount (order_id);
-- declared: orders.group_booking.order_id -> orders.sales_order
CREATE INDEX IF NOT EXISTS group_booking_order_id_idx ON orders.group_booking (order_id);
-- declared: orders.invitation.cost_center_id -> ledger.cost_center
CREATE INDEX IF NOT EXISTS invitation_cost_center_id_idx ON orders.invitation (cost_center_id);
-- declared: orders.invitation.performance_id -> catalogue.performance
CREATE INDEX IF NOT EXISTS invitation_performance_id_idx ON orders.invitation (performance_id);
-- declared: orders.invitation.product_id -> catalogue.product
CREATE INDEX IF NOT EXISTS invitation_product_id_idx ON orders.invitation (product_id);
-- declared: orders.invitation_allowance.principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS invitation_allowance_principal_id_idx ON orders.invitation_allowance (principal_id);
-- declared: orders.invitation_allowance.role_id -> identity.role
CREATE INDEX IF NOT EXISTS invitation_allowance_role_id_idx ON orders.invitation_allowance (role_id);
-- declared: orders.membership_renewal.order_id -> orders.sales_order
CREATE INDEX IF NOT EXISTS membership_renewal_order_id_idx ON orders.membership_renewal (order_id);
-- declared: orders.no_sale_event.principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS no_sale_event_principal_id_idx ON orders.no_sale_event (principal_id);
-- declared: orders.no_sale_event.shift_id -> orders.pos_shift
CREATE INDEX IF NOT EXISTS no_sale_event_shift_id_idx ON orders.no_sale_event (shift_id);
-- declared: orders.no_sale_event.workstation_id -> platform.workstation
CREATE INDEX IF NOT EXISTS no_sale_event_workstation_id_idx ON orders.no_sale_event (workstation_id);
-- declared: orders.order_fee.order_id -> orders.sales_order
CREATE INDEX IF NOT EXISTS order_fee_order_id_idx ON orders.order_fee (order_id);
-- declared: orders.order_line.inventory_hold_id -> catalogue.inventory_hold
CREATE INDEX IF NOT EXISTS order_line_inventory_hold_id_idx ON orders.order_line (inventory_hold_id);
-- declared: orders.order_line.performance_id -> catalogue.performance
CREATE INDEX IF NOT EXISTS order_line_performance_id_idx ON orders.order_line (performance_id);
-- declared: orders.order_line.sales_order_id -> orders.sales_order
CREATE INDEX IF NOT EXISTS order_line_sales_order_id_idx ON orders.order_line (sales_order_id);
-- declared: orders.order_line.variant_id -> catalogue.variant
CREATE INDEX IF NOT EXISTS order_line_variant_id_idx ON orders.order_line (variant_id);
-- declared: orders.order_line_eligibility.order_line_id -> orders.order_line
CREATE INDEX IF NOT EXISTS order_line_eligibility_order_line_id_idx ON orders.order_line_eligibility (order_line_id);
-- declared: orders.payment.order_id -> orders.sales_order
CREATE INDEX IF NOT EXISTS payment_order_id_idx ON orders.payment (order_id);
-- declared: orders.payment_link.order_id -> orders.sales_order
CREATE INDEX IF NOT EXISTS payment_link_order_id_idx ON orders.payment_link (order_id);
-- declared: orders.payment_tip.payment_id -> orders.payment
CREATE INDEX IF NOT EXISTS payment_tip_payment_id_idx ON orders.payment_tip (payment_id);
-- declared: orders.pos_shift.principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS pos_shift_principal_id_idx ON orders.pos_shift (principal_id);
-- declared: orders.pos_shift.venue_id -> platform.scope
CREATE INDEX IF NOT EXISTS pos_shift_venue_id_idx ON orders.pos_shift (venue_id);
-- declared: orders.pos_shift.workstation_id -> platform.workstation
CREATE INDEX IF NOT EXISTS pos_shift_workstation_id_idx ON orders.pos_shift (workstation_id);
-- declared: orders.pos_shift_approval.pos_shift_id -> orders.pos_shift
CREATE INDEX IF NOT EXISTS pos_shift_approval_pos_shift_id_idx ON orders.pos_shift_approval (pos_shift_id);
-- declared: orders.pos_shift_incident.pos_shift_id -> orders.pos_shift
CREATE INDEX IF NOT EXISTS pos_shift_incident_pos_shift_id_idx ON orders.pos_shift_incident (pos_shift_id);
-- declared: orders.refund.approved_by_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS refund_approved_by_principal_id_idx ON orders.refund (approved_by_principal_id);
-- declared: orders.refund.order_id -> orders.sales_order
CREATE INDEX IF NOT EXISTS refund_order_id_idx ON orders.refund (order_id);
-- declared: orders.refund.requested_by_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS refund_requested_by_principal_id_idx ON orders.refund (requested_by_principal_id);
-- declared: orders.refund.secondary_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS refund_secondary_principal_id_idx ON orders.refund (secondary_principal_id);
-- declared: orders.refund_policy.venue_id -> platform.scope
CREATE INDEX IF NOT EXISTS refund_policy_venue_id_idx ON orders.refund_policy (venue_id);
-- declared: orders.refund_policy_time_band.refund_policy_id -> orders.refund_policy
CREATE INDEX IF NOT EXISTS refund_policy_time_band_refund_policy_id_idx ON orders.refund_policy_time_band (refund_policy_id);
-- declared: orders.resale_fee_policy.product_id -> catalogue.product
CREATE INDEX IF NOT EXISTS resale_fee_policy_product_id_idx ON orders.resale_fee_policy (product_id);
-- declared: orders.resale_listing.entitlement_id -> access.entitlement
CREATE INDEX IF NOT EXISTS resale_listing_entitlement_id_idx ON orders.resale_listing (entitlement_id);
-- declared: orders.reservation.converted_order_id -> orders.sales_order
CREATE INDEX IF NOT EXISTS reservation_converted_order_id_idx ON orders.reservation (converted_order_id);
-- declared: orders.reservation.venue_id -> platform.scope
CREATE INDEX IF NOT EXISTS reservation_venue_id_idx ON orders.reservation (venue_id);
-- declared: orders.reservation_line.reservation_id -> orders.reservation
CREATE INDEX IF NOT EXISTS reservation_line_reservation_id_idx ON orders.reservation_line (reservation_id);
-- declared: orders.sales_order.principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS sales_order_principal_id_idx ON orders.sales_order (principal_id);
-- declared: orders.sales_order.shift_id -> orders.pos_shift
CREATE INDEX IF NOT EXISTS sales_order_shift_id_idx ON orders.sales_order (shift_id);
-- declared: orders.sales_order.subject_id -> pii.subject
CREATE INDEX IF NOT EXISTS sales_order_subject_id_idx ON orders.sales_order (subject_id);
-- declared: orders.sales_order.venue_id -> platform.scope
CREATE INDEX IF NOT EXISTS sales_order_venue_id_idx ON orders.sales_order (venue_id);
-- declared: orders.sales_order.workstation_id -> platform.workstation
CREATE INDEX IF NOT EXISTS sales_order_workstation_id_idx ON orders.sales_order (workstation_id);
-- declared: orders.ticket_template_channel.ticket_template_id -> orders.ticket_template
CREATE INDEX IF NOT EXISTS ticket_template_channel_ticket_template_id_idx ON orders.ticket_template_channel (ticket_template_id);
-- declared: orders.ticket_transfer.from_subject_id -> pii.subject
CREATE INDEX IF NOT EXISTS ticket_transfer_from_subject_id_idx ON orders.ticket_transfer (from_subject_id);
-- declared: orders.ticket_transfer.order_id -> orders.sales_order
CREATE INDEX IF NOT EXISTS ticket_transfer_order_id_idx ON orders.ticket_transfer (order_id);
-- declared: orders.ticket_transfer.to_subject_id -> pii.subject
CREATE INDEX IF NOT EXISTS ticket_transfer_to_subject_id_idx ON orders.ticket_transfer (to_subject_id);
-- declared: orders.upgrade.order_id -> orders.sales_order
CREATE INDEX IF NOT EXISTS upgrade_order_id_idx ON orders.upgrade (order_id);
-- declared: orders.visit_reminder.order_id -> orders.sales_order
CREATE INDEX IF NOT EXISTS visit_reminder_order_id_idx ON orders.visit_reminder (order_id);
-- declared: orders.wallet_pass.entitlement_id -> access.entitlement
CREATE INDEX IF NOT EXISTS wallet_pass_entitlement_id_idx ON orders.wallet_pass (entitlement_id);
-- declared: payments.deposit_activity.payment_id -> orders.payment
CREATE INDEX IF NOT EXISTS deposit_activity_payment_id_idx ON payments.deposit_activity (payment_id);
-- declared: payments.dunning_case.order_id -> orders.sales_order
CREATE INDEX IF NOT EXISTS dunning_case_order_id_idx ON payments.dunning_case (order_id);
-- declared: payments.token.consent_purpose_id -> marketing.consent_purpose
CREATE INDEX IF NOT EXISTS token_consent_purpose_id_idx ON payments.token (consent_purpose_id);
-- declared: payments.token.subject_id -> pii.subject
CREATE INDEX IF NOT EXISTS token_subject_id_idx ON payments.token (subject_id);
-- declared: pii.subject_biometric.consent_purpose_id -> marketing.consent_purpose
CREATE INDEX IF NOT EXISTS subject_biometric_consent_purpose_id_idx ON pii.subject_biometric (consent_purpose_id);
-- declared: pii.subject_biometric.entitlement_id -> access.entitlement
CREATE INDEX IF NOT EXISTS subject_biometric_entitlement_id_idx ON pii.subject_biometric (entitlement_id);
-- declared: pii.subject_biometric.subject_id -> pii.subject
CREATE INDEX IF NOT EXISTS subject_biometric_subject_id_idx ON pii.subject_biometric (subject_id);
-- declared: pii.subject_contact.subject_id -> pii.subject
CREATE INDEX IF NOT EXISTS subject_contact_subject_id_idx ON pii.subject_contact (subject_id);
-- declared: pii.subject_document.subject_id -> pii.subject
CREATE INDEX IF NOT EXISTS subject_document_subject_id_idx ON pii.subject_document (subject_id);
-- declared: platform.audit_read.principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS audit_read_principal_id_idx ON platform.audit_read (principal_id);
-- declared: platform.audit_read.subject_id -> pii.subject
CREATE INDEX IF NOT EXISTS audit_read_subject_id_idx ON platform.audit_read (subject_id);
-- declared: platform.audit_record.org_unit_id -> platform.scope
CREATE INDEX IF NOT EXISTS audit_record_org_unit_id_idx ON platform.audit_record (org_unit_id);
-- declared: platform.audit_record.principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS audit_record_principal_id_idx ON platform.audit_record (principal_id);
-- declared: platform.cross_region_entitlement.admission_rules_id -> access.admission_rules
CREATE INDEX IF NOT EXISTS cross_region_entitlement_admission_rules_id_idx ON platform.cross_region_entitlement (admission_rules_id);
-- declared: platform.cross_region_entitlement.guest_link_id -> platform.guest_link
CREATE INDEX IF NOT EXISTS cross_region_entitlement_guest_link_id_idx ON platform.cross_region_entitlement (guest_link_id);
-- declared: platform.cross_region_entitlement.ticket_id -> access.entitlement
CREATE INDEX IF NOT EXISTS cross_region_entitlement_ticket_id_idx ON platform.cross_region_entitlement (ticket_id);
-- declared: platform.cross_region_entitlement.venue_id -> platform.scope
CREATE INDEX IF NOT EXISTS cross_region_entitlement_venue_id_idx ON platform.cross_region_entitlement (venue_id);
-- declared: platform.device.workstation_id -> platform.workstation
CREATE INDEX IF NOT EXISTS device_workstation_id_idx ON platform.device (workstation_id);
-- declared: platform.device_heartbeat.device_id -> platform.device
CREATE INDEX IF NOT EXISTS device_heartbeat_device_id_idx ON platform.device_heartbeat (device_id);
-- declared: platform.dsar_request.guest_link_id -> platform.guest_link
CREATE INDEX IF NOT EXISTS dsar_request_guest_link_id_idx ON platform.dsar_request (guest_link_id);
-- declared: platform.dsar_request.request_id -> approvals.request
CREATE INDEX IF NOT EXISTS dsar_request_request_id_idx ON platform.dsar_request (request_id);
-- declared: platform.outlet.cost_center_id -> ledger.cost_center
CREATE INDEX IF NOT EXISTS outlet_cost_center_id_idx ON platform.outlet (cost_center_id);
-- declared: platform.outlet.stock_location_id -> inventory.location
CREATE INDEX IF NOT EXISTS outlet_stock_location_id_idx ON platform.outlet (stock_location_id);
-- declared: platform.outlet.venue_id -> platform.scope
CREATE INDEX IF NOT EXISTS outlet_venue_id_idx ON platform.outlet (venue_id);
-- declared: platform.region_settings.org_unit_id -> platform.scope
CREATE INDEX IF NOT EXISTS region_settings_org_unit_id_idx ON platform.region_settings (org_unit_id);
-- declared: platform.sale_board.venue_id -> platform.scope
CREATE INDEX IF NOT EXISTS sale_board_venue_id_idx ON platform.sale_board (venue_id);
-- declared: platform.sale_board_page.sale_board_id -> platform.sale_board
CREATE INDEX IF NOT EXISTS sale_board_page_sale_board_id_idx ON platform.sale_board_page (sale_board_id);
-- declared: platform.sale_board_tile.page_id -> platform.sale_board_page
CREATE INDEX IF NOT EXISTS sale_board_tile_page_id_idx ON platform.sale_board_tile (page_id);
-- declared: platform.tenant.home_region_id -> platform.scope
CREATE INDEX IF NOT EXISTS tenant_home_region_id_idx ON platform.tenant (home_region_id);
-- declared: platform.venue_settings.org_unit_id -> platform.scope
CREATE INDEX IF NOT EXISTS venue_settings_org_unit_id_idx ON platform.venue_settings (org_unit_id);
-- declared: platform.venue_settings.venue_id -> platform.scope
CREATE INDEX IF NOT EXISTS venue_settings_venue_id_idx ON platform.venue_settings (venue_id);
-- declared: platform.wallet_authorisation.guest_link_id -> platform.guest_link
CREATE INDEX IF NOT EXISTS wallet_authorisation_guest_link_id_idx ON platform.wallet_authorisation (guest_link_id);
-- declared: platform.wallet_authorisation.order_id -> orders.sales_order
CREATE INDEX IF NOT EXISTS wallet_authorisation_order_id_idx ON platform.wallet_authorisation (order_id);
-- declared: platform.workstation.access_point_id -> access.access_point
CREATE INDEX IF NOT EXISTS workstation_access_point_id_idx ON platform.workstation (access_point_id);
-- declared: platform.workstation.department_id -> platform.scope
CREATE INDEX IF NOT EXISTS workstation_department_id_idx ON platform.workstation (department_id);
-- declared: platform.workstation.org_unit_id -> platform.scope
CREATE INDEX IF NOT EXISTS workstation_org_unit_id_idx ON platform.workstation (org_unit_id);
-- declared: platform.workstation.region_id -> platform.scope
CREATE INDEX IF NOT EXISTS workstation_region_id_idx ON platform.workstation (region_id);
-- declared: platform.workstation.venue_id -> platform.scope
CREATE INDEX IF NOT EXISTS workstation_venue_id_idx ON platform.workstation (venue_id);
-- declared: pricing.dynamic_price_rule.product_id -> catalogue.product
CREATE INDEX IF NOT EXISTS dynamic_price_rule_product_id_idx ON pricing.dynamic_price_rule (product_id);
-- declared: promotions.allocation_component.allocation_split_id -> promotions.allocation_split
CREATE INDEX IF NOT EXISTS allocation_component_allocation_split_id_idx ON promotions.allocation_component (allocation_split_id);
-- declared: promotions.allocation_component.legal_entity_id -> ledger.legal_entity
CREATE INDEX IF NOT EXISTS allocation_component_legal_entity_id_idx ON promotions.allocation_component (legal_entity_id);
-- declared: promotions.allocation_component.revenue_account_id -> ledger.account
CREATE INDEX IF NOT EXISTS allocation_component_revenue_account_id_idx ON promotions.allocation_component (revenue_account_id);
-- declared: promotions.allocation_component.venue_id -> platform.scope
CREATE INDEX IF NOT EXISTS allocation_component_venue_id_idx ON promotions.allocation_component (venue_id);
-- declared: promotions.allocation_split.bundle_id -> promotions.bundle
CREATE INDEX IF NOT EXISTS allocation_split_bundle_id_idx ON promotions.allocation_split (bundle_id);
-- declared: promotions.bundle.venue_id -> platform.scope
CREATE INDEX IF NOT EXISTS bundle_venue_id_idx ON promotions.bundle (venue_id);
-- declared: promotions.bundle_choice_group.bundle_id -> promotions.bundle
CREATE INDEX IF NOT EXISTS bundle_choice_group_bundle_id_idx ON promotions.bundle_choice_group (bundle_id);
-- declared: promotions.bundle_choice_option.bundle_choice_group_id -> promotions.bundle_choice_group
CREATE INDEX IF NOT EXISTS bundle_choice_option_bundle_choice_group_id_idx ON promotions.bundle_choice_option (bundle_choice_group_id);
-- declared: promotions.bundle_component.bundle_id -> promotions.bundle
CREATE INDEX IF NOT EXISTS bundle_component_bundle_id_idx ON promotions.bundle_component (bundle_id);
-- declared: promotions.bundle_component.venue_id -> platform.scope
CREATE INDEX IF NOT EXISTS bundle_component_venue_id_idx ON promotions.bundle_component (venue_id);
-- declared: promotions.coupon_campaign.venue_id -> platform.scope
CREATE INDEX IF NOT EXISTS coupon_campaign_venue_id_idx ON promotions.coupon_campaign (venue_id);
-- declared: promotions.coupon_code.assigned_subject_id -> pii.subject
CREATE INDEX IF NOT EXISTS coupon_code_assigned_subject_id_idx ON promotions.coupon_code (assigned_subject_id);
-- declared: promotions.coupon_code.redeemed_order_id -> orders.sales_order
CREATE INDEX IF NOT EXISTS coupon_code_redeemed_order_id_idx ON promotions.coupon_code (redeemed_order_id);
-- declared: promotions.promotion.venue_id -> platform.scope
CREATE INDEX IF NOT EXISTS promotion_venue_id_idx ON promotions.promotion (venue_id);
-- declared: promotions.recommendation_outcome.order_id -> orders.sales_order
CREATE INDEX IF NOT EXISTS recommendation_outcome_order_id_idx ON promotions.recommendation_outcome (order_id);
-- declared: promotions.upsell_rule.suggested_bundle_id -> promotions.bundle
CREATE INDEX IF NOT EXISTS upsell_rule_suggested_bundle_id_idx ON promotions.upsell_rule (suggested_bundle_id);
-- declared: promotions.voucher.batch_id -> promotions.voucher_batch
CREATE INDEX IF NOT EXISTS voucher_batch_id_idx ON promotions.voucher (batch_id);
-- declared: promotions.voucher_batch.venue_id -> platform.scope
CREATE INDEX IF NOT EXISTS voucher_batch_venue_id_idx ON promotions.voucher_batch (venue_id);
-- declared: queue.entry.entitlement_id -> access.entitlement
CREATE INDEX IF NOT EXISTS entry_entitlement_id_idx ON queue.entry (entitlement_id);
-- declared: queue.entry.queue_id -> queue.queue
CREATE INDEX IF NOT EXISTS entry_queue_id_idx ON queue.entry (queue_id);
-- declared: queue.entry.subject_id -> pii.subject
CREATE INDEX IF NOT EXISTS entry_subject_id_idx ON queue.entry (subject_id);
-- declared: queue.feed.queue_id -> queue.queue
CREATE INDEX IF NOT EXISTS feed_queue_id_idx ON queue.feed (queue_id);
-- declared: queue.queue.access_point_id -> access.access_point
CREATE INDEX IF NOT EXISTS queue_access_point_id_idx ON queue.queue (access_point_id);
-- declared: queue.queue.asset_id -> maintenance.asset
CREATE INDEX IF NOT EXISTS queue_asset_id_idx ON queue.queue (asset_id);
-- declared: queue.queue.attraction_product_id -> catalogue.product
CREATE INDEX IF NOT EXISTS queue_attraction_product_id_idx ON queue.queue (attraction_product_id);
-- declared: queue.queue.venue_id -> platform.scope
CREATE INDEX IF NOT EXISTS queue_venue_id_idx ON queue.queue (venue_id);
-- declared: queue.queue_operating_window.queue_id -> queue.queue
CREATE INDEX IF NOT EXISTS queue_operating_window_queue_id_idx ON queue.queue_operating_window (queue_id);
-- declared: queue.reading.queue_id -> queue.queue
CREATE INDEX IF NOT EXISTS reading_queue_id_idx ON queue.reading (queue_id);
-- declared: rental.agreement.order_id -> orders.sales_order
CREATE INDEX IF NOT EXISTS agreement_order_id_idx ON rental.agreement (order_id);
-- declared: rental.agreement.venue_id -> platform.scope
CREATE INDEX IF NOT EXISTS agreement_venue_id_idx ON rental.agreement (venue_id);
-- declared: rental.booking.order_id -> orders.sales_order
CREATE INDEX IF NOT EXISTS booking_order_id_idx ON rental.booking (order_id);
-- declared: rental.pricing_profile.venue_id -> platform.scope
CREATE INDEX IF NOT EXISTS pricing_profile_venue_id_idx ON rental.pricing_profile (venue_id);
-- declared: rental.product.venue_id -> platform.scope
CREATE INDEX IF NOT EXISTS product_venue_id_idx ON rental.product (venue_id);
-- declared: reporting.dashboard.owner_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS dashboard_owner_principal_id_idx ON reporting.dashboard (owner_principal_id);
-- declared: reporting.dashboard.venue_id -> platform.scope
CREATE INDEX IF NOT EXISTS dashboard_venue_id_idx ON reporting.dashboard (venue_id);
-- declared: reporting.dashboard_tile.dashboard_id -> reporting.dashboard
CREATE INDEX IF NOT EXISTS dashboard_tile_dashboard_id_idx ON reporting.dashboard_tile (dashboard_id);
-- declared: reporting.dashboard_tile.report_id -> reporting.report_definition
CREATE INDEX IF NOT EXISTS dashboard_tile_report_id_idx ON reporting.dashboard_tile (report_id);
-- declared: reporting.delivery.report_id -> reporting.report_definition
CREATE INDEX IF NOT EXISTS delivery_report_id_idx ON reporting.delivery (report_id);
-- declared: reporting.execution.report_id -> reporting.report_definition
CREATE INDEX IF NOT EXISTS execution_report_id_idx ON reporting.execution (report_id);
-- declared: reporting.execution.requested_by_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS execution_requested_by_principal_id_idx ON reporting.execution (requested_by_principal_id);
-- declared: reporting.execution.schedule_id -> reporting.schedule
CREATE INDEX IF NOT EXISTS execution_schedule_id_idx ON reporting.execution (schedule_id);
-- declared: reporting.export.execution_id -> reporting.execution
CREATE INDEX IF NOT EXISTS export_execution_id_idx ON reporting.export (execution_id);
-- declared: reporting.export.requested_by_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS export_requested_by_principal_id_idx ON reporting.export (requested_by_principal_id);
-- declared: reporting.report_column.report_definition_id -> reporting.report_definition
CREATE INDEX IF NOT EXISTS report_column_report_definition_id_idx ON reporting.report_column (report_definition_id);
-- declared: reporting.report_definition.created_by_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS report_definition_created_by_principal_id_idx ON reporting.report_definition (created_by_principal_id);
-- declared: reporting.report_filter.report_definition_id -> reporting.report_definition
CREATE INDEX IF NOT EXISTS report_filter_report_definition_id_idx ON reporting.report_filter (report_definition_id);
-- declared: reporting.report_parameter.definition_id -> reporting.report_definition
CREATE INDEX IF NOT EXISTS report_parameter_definition_id_idx ON reporting.report_parameter (definition_id);
-- declared: reporting.schedule.owner_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS schedule_owner_principal_id_idx ON reporting.schedule (owner_principal_id);
-- declared: reporting.schedule.report_id -> reporting.report_definition
CREATE INDEX IF NOT EXISTS schedule_report_id_idx ON reporting.schedule (report_id);
-- declared: reporting.schedule_recipient.principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS schedule_recipient_principal_id_idx ON reporting.schedule_recipient (principal_id);
-- declared: reporting.schedule_recipient.schedule_id -> reporting.schedule
CREATE INDEX IF NOT EXISTS schedule_recipient_schedule_id_idx ON reporting.schedule_recipient (schedule_id);
-- declared: reporting.subscription.report_id -> reporting.report_definition
CREATE INDEX IF NOT EXISTS subscription_report_id_idx ON reporting.subscription (report_id);
-- declared: resources.booking.order_id -> orders.sales_order
CREATE INDEX IF NOT EXISTS booking_order_id_idx ON resources.booking (order_id);
-- declared: resources.booking.resource_id -> resources.resource
CREATE INDEX IF NOT EXISTS booking_resource_id_idx ON resources.booking (resource_id);
-- declared: resources.booking.subject_id -> pii.subject
CREATE INDEX IF NOT EXISTS booking_subject_id_idx ON resources.booking (subject_id);
-- declared: resources.resource.principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS resource_principal_id_idx ON resources.resource (principal_id);
-- declared: resources.resource.venue_id -> platform.scope
CREATE INDEX IF NOT EXISTS resource_venue_id_idx ON resources.resource (venue_id);
-- declared: resources.resource_dependency.venue_id -> platform.scope
CREATE INDEX IF NOT EXISTS resource_dependency_venue_id_idx ON resources.resource_dependency (venue_id);
-- declared: resources.session_participant.subject_id -> pii.subject
CREATE INDEX IF NOT EXISTS session_participant_subject_id_idx ON resources.session_participant (subject_id);
-- declared: retail.exchange.new_sale_id -> retail.sale
CREATE INDEX IF NOT EXISTS exchange_new_sale_id_idx ON retail.exchange (new_sale_id);
-- declared: retail.exchange.return_id -> retail.return
CREATE INDEX IF NOT EXISTS exchange_return_id_idx ON retail.exchange (return_id);
-- declared: retail.exchange.sale_id -> retail.sale
CREATE INDEX IF NOT EXISTS exchange_sale_id_idx ON retail.exchange (sale_id);
-- declared: retail.merchandise.inventory_item_id -> inventory.item
CREATE INDEX IF NOT EXISTS merchandise_inventory_item_id_idx ON retail.merchandise (inventory_item_id);
-- declared: retail.merchandise.outlet_id -> platform.outlet
CREATE INDEX IF NOT EXISTS merchandise_outlet_id_idx ON retail.merchandise (outlet_id);
-- declared: retail.merchandise.variant_id -> catalogue.variant
CREATE INDEX IF NOT EXISTS merchandise_variant_id_idx ON retail.merchandise (variant_id);
-- declared: retail.reservation.outlet_id -> platform.outlet
CREATE INDEX IF NOT EXISTS reservation_outlet_id_idx ON retail.reservation (outlet_id);
-- declared: retail.reservation.subject_id -> pii.subject
CREATE INDEX IF NOT EXISTS reservation_subject_id_idx ON retail.reservation (subject_id);
-- declared: retail.reservation_line.merchandise_id -> retail.merchandise
CREATE INDEX IF NOT EXISTS reservation_line_merchandise_id_idx ON retail.reservation_line (merchandise_id);
-- declared: retail.reservation_line.reservation_id -> retail.reservation
CREATE INDEX IF NOT EXISTS reservation_line_reservation_id_idx ON retail.reservation_line (reservation_id);
-- declared: retail.return.accepted_by_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS return_accepted_by_principal_id_idx ON retail."return" (accepted_by_principal_id);
-- declared: retail.return.refund_id -> orders.refund
CREATE INDEX IF NOT EXISTS return_refund_id_idx ON retail."return" (refund_id);
-- declared: retail.return.sale_id -> retail.sale
CREATE INDEX IF NOT EXISTS return_sale_id_idx ON retail."return" (sale_id);
-- declared: retail.return.secondary_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS return_secondary_principal_id_idx ON retail."return" (secondary_principal_id);
-- declared: retail.return_line.merchandise_id -> retail.merchandise
CREATE INDEX IF NOT EXISTS return_line_merchandise_id_idx ON retail.return_line (merchandise_id);
-- declared: retail.return_line.return_id -> retail.return
CREATE INDEX IF NOT EXISTS return_line_return_id_idx ON retail.return_line (return_id);
-- declared: retail.return_policy.outlet_id -> platform.outlet
CREATE INDEX IF NOT EXISTS return_policy_outlet_id_idx ON retail.return_policy (outlet_id);
-- declared: retail.sale.order_id -> orders.sales_order
CREATE INDEX IF NOT EXISTS sale_order_id_idx ON retail.sale (order_id);
-- declared: retail.sale.outlet_id -> platform.outlet
CREATE INDEX IF NOT EXISTS sale_outlet_id_idx ON retail.sale (outlet_id);
-- declared: retail.sale.shift_id -> orders.pos_shift
CREATE INDEX IF NOT EXISTS sale_shift_id_idx ON retail.sale (shift_id);
-- declared: retail.sale.subject_id -> pii.subject
CREATE INDEX IF NOT EXISTS sale_subject_id_idx ON retail.sale (subject_id);
-- declared: retail.sale_line.merchandise_id -> retail.merchandise
CREATE INDEX IF NOT EXISTS sale_line_merchandise_id_idx ON retail.sale_line (merchandise_id);
-- declared: retail.sale_line.sale_id -> retail.sale
CREATE INDEX IF NOT EXISTS sale_line_sale_id_idx ON retail.sale_line (sale_id);
-- declared: retail.shop_and_drop.collected_by_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS shop_and_drop_collected_by_principal_id_idx ON retail.shop_and_drop (collected_by_principal_id);
-- declared: retail.shop_and_drop.collection_point_id -> fnb.delivery_location
CREATE INDEX IF NOT EXISTS shop_and_drop_collection_point_id_idx ON retail.shop_and_drop (collection_point_id);
-- declared: retail.shop_and_drop.entitlement_id -> access.entitlement
CREATE INDEX IF NOT EXISTS shop_and_drop_entitlement_id_idx ON retail.shop_and_drop (entitlement_id);
-- declared: retail.shop_and_drop.sale_id -> retail.sale
CREATE INDEX IF NOT EXISTS shop_and_drop_sale_id_idx ON retail.shop_and_drop (sale_id);
-- declared: retail.shop_and_drop.subject_id -> pii.subject
CREATE INDEX IF NOT EXISTS shop_and_drop_subject_id_idx ON retail.shop_and_drop (subject_id);
-- declared: retail.shop_and_drop.venue_id -> platform.scope
CREATE INDEX IF NOT EXISTS shop_and_drop_venue_id_idx ON retail.shop_and_drop (venue_id);
-- declared: retail.shop_and_drop_line.merchandise_id -> retail.merchandise
CREATE INDEX IF NOT EXISTS shop_and_drop_line_merchandise_id_idx ON retail.shop_and_drop_line (merchandise_id);
-- declared: retail.shop_and_drop_line.shop_and_drop_id -> retail.shop_and_drop
CREATE INDEX IF NOT EXISTS shop_and_drop_line_shop_and_drop_id_idx ON retail.shop_and_drop_line (shop_and_drop_id);
-- declared: retail.store_rule.venue_id -> platform.scope
CREATE INDEX IF NOT EXISTS store_rule_venue_id_idx ON retail.store_rule (venue_id);
-- declared: seating.group_request.order_id -> orders.sales_order
CREATE INDEX IF NOT EXISTS group_request_order_id_idx ON seating.group_request (order_id);
-- declared: seating.import_job.seat_map_id -> seating.seat_map
CREATE INDEX IF NOT EXISTS import_job_seat_map_id_idx ON seating.import_job (seat_map_id);
-- declared: seating.reassignment.order_id -> orders.sales_order
CREATE INDEX IF NOT EXISTS reassignment_order_id_idx ON seating.reassignment (order_id);
-- declared: seating.seat.seat_map_id -> seating.seat_map
CREATE INDEX IF NOT EXISTS seat_seat_map_id_idx ON seating.seat (seat_map_id);
-- declared: seating.seat_block.created_by_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS seat_block_created_by_principal_id_idx ON seating.seat_block (created_by_principal_id);
-- declared: seating.seat_block.performance_id -> catalogue.performance
CREATE INDEX IF NOT EXISTS seat_block_performance_id_idx ON seating.seat_block (performance_id);
-- declared: seating.seat_category.venue_id -> platform.scope
CREATE INDEX IF NOT EXISTS seat_category_venue_id_idx ON seating.seat_category (venue_id);
-- declared: seating.seat_hold.block_id -> seating.seat_block
CREATE INDEX IF NOT EXISTS seat_hold_block_id_idx ON seating.seat_hold (block_id);
-- declared: seating.seat_hold.held_by_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS seat_hold_held_by_principal_id_idx ON seating.seat_hold (held_by_principal_id);
-- declared: seating.seat_hold.performance_id -> catalogue.performance
CREATE INDEX IF NOT EXISTS seat_hold_performance_id_idx ON seating.seat_hold (performance_id);
-- declared: seating.seat_hold.subject_id -> pii.subject
CREATE INDEX IF NOT EXISTS seat_hold_subject_id_idx ON seating.seat_hold (subject_id);
-- declared: seating.seat_map.venue_id -> platform.scope
CREATE INDEX IF NOT EXISTS seat_map_venue_id_idx ON seating.seat_map (venue_id);
-- declared: seating.seat_map_template.region_id -> platform.scope
CREATE INDEX IF NOT EXISTS seat_map_template_region_id_idx ON seating.seat_map_template (region_id);
-- declared: seating.seating_rules.seat_map_id -> seating.seat_map
CREATE INDEX IF NOT EXISTS seating_rules_seat_map_id_idx ON seating.seating_rules (seat_map_id);
-- declared: seating.section_row.section_id -> seating.section
CREATE INDEX IF NOT EXISTS section_row_section_id_idx ON seating.section_row (section_id);
-- declared: seating.zone.seat_category_id -> seating.seat_category
CREATE INDEX IF NOT EXISTS zone_seat_category_id_idx ON seating.zone (seat_category_id);
-- declared: seating.zone.seat_map_id -> seating.seat_map
CREATE INDEX IF NOT EXISTS zone_seat_map_id_idx ON seating.zone (seat_map_id);
-- declared: subscription.contract.plan_id -> subscription.plan
CREATE INDEX IF NOT EXISTS contract_plan_id_idx ON subscription.contract (plan_id);
-- declared: subscription.contract.tenant_id -> platform.tenant
CREATE INDEX IF NOT EXISTS contract_tenant_id_idx ON subscription.contract (tenant_id);
-- declared: subscription.plan_limit.plan_id -> subscription.plan
CREATE INDEX IF NOT EXISTS plan_limit_plan_id_idx ON subscription.plan_limit (plan_id);
-- declared: subscription.plan_module.plan_id -> subscription.plan
CREATE INDEX IF NOT EXISTS plan_module_plan_id_idx ON subscription.plan_module (plan_id);
-- declared: sync.rejection.resolved_by_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS rejection_resolved_by_principal_id_idx ON sync.rejection (resolved_by_principal_id);
-- declared: sync.rejection.workstation_id -> platform.workstation
CREATE INDEX IF NOT EXISTS rejection_workstation_id_idx ON sync.rejection (workstation_id);
-- declared: venuemap.import_job.map_id -> venuemap.map
CREATE INDEX IF NOT EXISTS import_job_map_id_idx ON venuemap.import_job (map_id);
-- declared: venuemap.map.base_asset_id -> assets.media_asset
CREATE INDEX IF NOT EXISTS map_base_asset_id_idx ON venuemap.map (base_asset_id);
-- declared: venuemap.map.venue_id -> platform.scope
CREATE INDEX IF NOT EXISTS map_venue_id_idx ON venuemap.map (venue_id);
-- declared: venuemap.path.map_id -> venuemap.map
CREATE INDEX IF NOT EXISTS path_map_id_idx ON venuemap.path (map_id);
-- declared: venuemap.point.access_point_id -> access.access_point
CREATE INDEX IF NOT EXISTS point_access_point_id_idx ON venuemap.point (access_point_id);
-- declared: venuemap.point.map_id -> venuemap.map
CREATE INDEX IF NOT EXISTS point_map_id_idx ON venuemap.point (map_id);
-- declared: venuemap.point.outlet_id -> platform.outlet
CREATE INDEX IF NOT EXISTS point_outlet_id_idx ON venuemap.point (outlet_id);
-- declared: venuemap.point.product_id -> catalogue.product
CREATE INDEX IF NOT EXISTS point_product_id_idx ON venuemap.point (product_id);
-- declared: wallet.credit_lot.wallet_id -> wallet.wallet
CREATE INDEX IF NOT EXISTS credit_lot_wallet_id_idx ON wallet.credit_lot (wallet_id);
-- declared: wallet.gift_card.subject_id -> pii.subject
CREATE INDEX IF NOT EXISTS gift_card_subject_id_idx ON wallet.gift_card (subject_id);
-- declared: wallet.hold.order_id -> orders.sales_order
CREATE INDEX IF NOT EXISTS hold_order_id_idx ON wallet.hold (order_id);
-- declared: wallet.wallet.subject_id -> pii.subject
CREATE INDEX IF NOT EXISTS wallet_subject_id_idx ON wallet.wallet (subject_id);
-- declared: wallet.wallet_transaction.order_id -> orders.sales_order
CREATE INDEX IF NOT EXISTS wallet_transaction_order_id_idx ON wallet.wallet_transaction (order_id);
-- declared: wallet.wallet_transaction.principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS wallet_transaction_principal_id_idx ON wallet.wallet_transaction (principal_id);
-- declared: wallet.wallet_transaction.venue_id -> platform.scope
CREATE INDEX IF NOT EXISTS wallet_transaction_venue_id_idx ON wallet.wallet_transaction (venue_id);
-- declared: whitelabel.banner.tenant_config_id -> whitelabel.tenant_config
CREATE INDEX IF NOT EXISTS banner_tenant_config_id_idx ON whitelabel.banner (tenant_config_id);
-- declared: whitelabel.config_version.published_by_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS config_version_published_by_principal_id_idx ON whitelabel.config_version (published_by_principal_id);
-- declared: whitelabel.faq_entry.faq_category_id -> whitelabel.faq_category
CREATE INDEX IF NOT EXISTS faq_entry_faq_category_id_idx ON whitelabel.faq_entry (faq_category_id);
-- declared: whitelabel.feature_toggle.tenant_config_id -> whitelabel.tenant_config
CREATE INDEX IF NOT EXISTS feature_toggle_tenant_config_id_idx ON whitelabel.feature_toggle (tenant_config_id);
-- declared: whitelabel.homepage_section.content_page_id -> whitelabel.content_page
CREATE INDEX IF NOT EXISTS homepage_section_content_page_id_idx ON whitelabel.homepage_section (content_page_id);
-- declared: whitelabel.module_enablement.tenant_config_id -> whitelabel.tenant_config
CREATE INDEX IF NOT EXISTS module_enablement_tenant_config_id_idx ON whitelabel.module_enablement (tenant_config_id);
-- declared: whitelabel.policy.published_by_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS policy_published_by_principal_id_idx ON whitelabel.policy (published_by_principal_id);
-- declared: whitelabel.promo_block.promotion_id -> promotions.promotion
CREATE INDEX IF NOT EXISTS promo_block_promotion_id_idx ON whitelabel.promo_block (promotion_id);
-- declared: whitelabel.tenant_config.homepage_section_id -> whitelabel.homepage_section
CREATE INDEX IF NOT EXISTS tenant_config_homepage_section_id_idx ON whitelabel.tenant_config (homepage_section_id);
-- declared: whitelabel.tenant_config.navigation_item_id -> whitelabel.navigation_item
CREATE INDEX IF NOT EXISTS tenant_config_navigation_item_id_idx ON whitelabel.tenant_config (navigation_item_id);
-- declared: whitelabel.tenant_config.tenant_id -> platform.tenant
CREATE INDEX IF NOT EXISTS tenant_config_tenant_id_idx ON whitelabel.tenant_config (tenant_id);
-- declared: workforce.announcement.venue_id -> platform.scope
CREATE INDEX IF NOT EXISTS announcement_venue_id_idx ON workforce.announcement (venue_id);
-- declared: workforce.announcement_receipt.announcement_id -> workforce.announcement
CREATE INDEX IF NOT EXISTS announcement_receipt_announcement_id_idx ON workforce.announcement_receipt (announcement_id);
-- declared: workforce.announcement_receipt.principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS announcement_receipt_principal_id_idx ON workforce.announcement_receipt (principal_id);
-- declared: workforce.attendance.access_point_id -> access.access_point
CREATE INDEX IF NOT EXISTS attendance_access_point_id_idx ON workforce.attendance (access_point_id);
-- declared: workforce.attendance.assignment_id -> workforce.rota_assignment
CREATE INDEX IF NOT EXISTS attendance_assignment_id_idx ON workforce.attendance (assignment_id);
-- declared: workforce.attendance.principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS attendance_principal_id_idx ON workforce.attendance (principal_id);
-- declared: workforce.attendance.venue_id -> platform.scope
CREATE INDEX IF NOT EXISTS attendance_venue_id_idx ON workforce.attendance (venue_id);
-- declared: workforce.leave_request.approval_request_id -> approvals.request
CREATE INDEX IF NOT EXISTS leave_request_approval_request_id_idx ON workforce.leave_request (approval_request_id);
-- declared: workforce.open_shift.venue_id -> platform.scope
CREATE INDEX IF NOT EXISTS open_shift_venue_id_idx ON workforce.open_shift (venue_id);
-- declared: workforce.rota_assignment.department_id -> platform.scope
CREATE INDEX IF NOT EXISTS rota_assignment_department_id_idx ON workforce.rota_assignment (department_id);
-- declared: workforce.rota_assignment.principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS rota_assignment_principal_id_idx ON workforce.rota_assignment (principal_id);
-- declared: workforce.rota_assignment.venue_id -> platform.scope
CREATE INDEX IF NOT EXISTS rota_assignment_venue_id_idx ON workforce.rota_assignment (venue_id);
-- declared: workforce.rota_assignment.workstation_id -> platform.workstation
CREATE INDEX IF NOT EXISTS rota_assignment_workstation_id_idx ON workforce.rota_assignment (workstation_id);
-- declared: workforce.shift_swap.approval_request_id -> approvals.request
CREATE INDEX IF NOT EXISTS shift_swap_approval_request_id_idx ON workforce.shift_swap (approval_request_id);
-- declared: workforce.shift_swap.assignment_id -> workforce.rota_assignment
CREATE INDEX IF NOT EXISTS shift_swap_assignment_id_idx ON workforce.shift_swap (assignment_id);
-- declared: workforce.work_assignment.department_id -> platform.scope
CREATE INDEX IF NOT EXISTS work_assignment_department_id_idx ON workforce.work_assignment (department_id);
-- declared: workforce.work_assignment.venue_id -> platform.scope
CREATE INDEX IF NOT EXISTS work_assignment_venue_id_idx ON workforce.work_assignment (venue_id);
CREATE INDEX IF NOT EXISTS access_decision_scope_path_idx ON identity.access_decision USING gist (scope_path);
CREATE INDEX IF NOT EXISTS access_override_scope_path_idx ON identity.access_override USING gist (scope_path);
CREATE INDEX IF NOT EXISTS access_point_scope_path_idx ON access.access_point USING gist (scope_path);
CREATE INDEX IF NOT EXISTS access_policy_scope_path_idx ON identity.access_policy USING gist (scope_path);
CREATE INDEX IF NOT EXISTS access_policy_version_scope_path_idx ON identity.access_policy_version USING gist (scope_path);
CREATE INDEX IF NOT EXISTS access_profile_scope_path_idx ON accreditation.access_profile USING gist (scope_path);
CREATE INDEX IF NOT EXISTS accessible_scope_path_idx ON seating.accessible USING gist (scope_path);
CREATE INDEX IF NOT EXISTS accounting_mapping_scope_path_idx ON wallet.accounting_mapping USING gist (scope_path);
CREATE INDEX IF NOT EXISTS activity_scope_path_idx ON ai.activity USING gist (scope_path);
CREATE INDEX IF NOT EXISTS adjustment_scope_path_idx ON wallet.adjustment USING gist (scope_path);
CREATE INDEX IF NOT EXISTS admission_rules_scope_path_idx ON access.admission_rules USING gist (scope_path);
CREATE INDEX IF NOT EXISTS agreement_rules_scope_path_idx ON rental.agreement_rules USING gist (scope_path);
CREATE INDEX IF NOT EXISTS agreement_signature_scope_path_idx ON rental.agreement_signature USING gist (scope_path);
CREATE INDEX IF NOT EXISTS alert_rule_scope_path_idx ON reporting.alert_rule USING gist (scope_path);
CREATE INDEX IF NOT EXISTS alert_scope_path_idx ON reporting.alert USING gist (scope_path);
CREATE INDEX IF NOT EXISTS allocation_policy_scope_path_idx ON resources.allocation_policy USING gist (scope_path);
CREATE INDEX IF NOT EXISTS anomaly_scope_path_idx ON reporting.anomaly USING gist (scope_path);
CREATE INDEX IF NOT EXISTS application_scope_path_idx ON accreditation.application USING gist (scope_path);
CREATE INDEX IF NOT EXISTS approval_scope_path_idx ON assets.approval USING gist (scope_path);
CREATE INDEX IF NOT EXISTS approver_availability_scope_path_idx ON approvals.approver_availability USING gist (scope_path);
CREATE INDEX IF NOT EXISTS asset_category_scope_path_idx ON maintenance.asset_category USING gist (scope_path);
CREATE INDEX IF NOT EXISTS asset_version_scope_path_idx ON assets.asset_version USING gist (scope_path);
CREATE INDEX IF NOT EXISTS attraction_type_scope_path_idx ON games.attraction_type USING gist (scope_path);
CREATE INDEX IF NOT EXISTS attribute_definition_scope_path_idx ON resources.attribute_definition USING gist (scope_path);
CREATE INDEX IF NOT EXISTS audience_activation_scope_path_idx ON marketing.audience_activation USING gist (scope_path);
CREATE INDEX IF NOT EXISTS audience_list_scope_path_idx ON marketing.audience_list USING gist (scope_path);
CREATE INDEX IF NOT EXISTS audit_scope_path_idx ON accreditation.audit USING gist (scope_path);
CREATE INDEX IF NOT EXISTS audit_scope_path_idx ON assets.audit USING gist (scope_path);
CREATE INDEX IF NOT EXISTS authentication_policy_scope_path_idx ON payments.authentication_policy USING gist (scope_path);
CREATE INDEX IF NOT EXISTS authorisation_scope_path_idx ON games.authorisation USING gist (scope_path);
CREATE INDEX IF NOT EXISTS availability_rules_scope_path_idx ON rental.availability_rules USING gist (scope_path);
CREATE INDEX IF NOT EXISTS b2b_credit_scope_path_idx ON orders.b2b_credit USING gist (scope_path);
CREATE INDEX IF NOT EXISTS badge_template_scope_path_idx ON accreditation.badge_template USING gist (scope_path);
CREATE INDEX IF NOT EXISTS blacklist_scope_path_idx ON access.blacklist USING gist (scope_path);
CREATE INDEX IF NOT EXISTS blackout_scope_path_idx ON rental.blackout USING gist (scope_path);
CREATE INDEX IF NOT EXISTS booking_scope_path_idx ON rental.booking USING gist (scope_path);
CREATE INDEX IF NOT EXISTS capability_template_scope_path_idx ON identity.capability_template USING gist (scope_path);
CREATE INDEX IF NOT EXISTS card_expiry_rules_scope_path_idx ON games.card_expiry_rules USING gist (scope_path);
CREATE INDEX IF NOT EXISTS challenge_scope_path_idx ON marketing.challenge USING gist (scope_path);
CREATE INDEX IF NOT EXISTS channel_rules_scope_path_idx ON wallet.channel_rules USING gist (scope_path);
CREATE INDEX IF NOT EXISTS chargeback_evidence_scope_path_idx ON payments.chargeback_evidence USING gist (scope_path);
CREATE INDEX IF NOT EXISTS config_version_scope_path_idx ON whitelabel.config_version USING gist (scope_path);
CREATE INDEX IF NOT EXISTS configuration_profile_scope_path_idx ON platform.configuration_profile USING gist (scope_path);
CREATE INDEX IF NOT EXISTS configuration_version_scope_path_idx ON wallet.configuration_version USING gist (scope_path);
CREATE INDEX IF NOT EXISTS connectivity_policy_scope_path_idx ON platform.connectivity_policy USING gist (scope_path);
CREATE INDEX IF NOT EXISTS consumption_policy_scope_path_idx ON wallet.consumption_policy USING gist (scope_path);
CREATE INDEX IF NOT EXISTS content_page_scope_path_idx ON whitelabel.content_page USING gist (scope_path);
CREATE INDEX IF NOT EXISTS control_policy_scope_path_idx ON approvals.control_policy USING gist (scope_path);
CREATE INDEX IF NOT EXISTS conversation_scope_path_idx ON ai.conversation USING gist (scope_path);
CREATE INDEX IF NOT EXISTS corrective_action_scope_path_idx ON fnb.corrective_action USING gist (scope_path);
CREATE INDEX IF NOT EXISTS coupon_code_scope_path_idx ON promotions.coupon_code USING gist (scope_path);
CREATE INDEX IF NOT EXISTS course_rule_scope_path_idx ON fnb.course_rule USING gist (scope_path);
CREATE INDEX IF NOT EXISTS credential_scope_path_idx ON accreditation.credential USING gist (scope_path);
CREATE INDEX IF NOT EXISTS credential_scope_path_idx ON wallet.credential USING gist (scope_path);
CREATE INDEX IF NOT EXISTS credit_account_scope_path_idx ON payments.credit_account USING gist (scope_path);
CREATE INDEX IF NOT EXISTS credit_eligibility_scope_path_idx ON wallet.credit_eligibility USING gist (scope_path);
CREATE INDEX IF NOT EXISTS credit_lot_scope_path_idx ON wallet.credit_lot USING gist (scope_path);
CREATE INDEX IF NOT EXISTS credit_type_scope_path_idx ON wallet.credit_type USING gist (scope_path);
CREATE INDEX IF NOT EXISTS currency_rule_scope_path_idx ON payments.currency_rule USING gist (scope_path);
CREATE INDEX IF NOT EXISTS damage_assessment_scope_path_idx ON rental.damage_assessment USING gist (scope_path);
CREATE INDEX IF NOT EXISTS dead_letter_scope_path_idx ON platform.dead_letter USING gist (scope_path);
CREATE INDEX IF NOT EXISTS decision_record_scope_path_idx ON approvals.decision_record USING gist (scope_path);
CREATE INDEX IF NOT EXISTS delegated_access_scope_path_idx ON identity.delegated_access USING gist (scope_path);
CREATE INDEX IF NOT EXISTS delegation_scope_path_idx ON approvals.delegation USING gist (scope_path);
CREATE INDEX IF NOT EXISTS delivery_policy_scope_path_idx ON fnb.delivery_policy USING gist (scope_path);
CREATE INDEX IF NOT EXISTS delivery_scope_path_idx ON reporting.delivery USING gist (scope_path);
CREATE INDEX IF NOT EXISTS deposit_policy_scope_path_idx ON orders.deposit_policy USING gist (scope_path);
CREATE INDEX IF NOT EXISTS deposit_policy_scope_path_idx ON rental.deposit_policy USING gist (scope_path);
CREATE INDEX IF NOT EXISTS device_assignment_scope_path_idx ON tenancy.device_assignment USING gist (scope_path);
CREATE INDEX IF NOT EXISTS device_audit_scope_path_idx ON tenancy.device_audit USING gist (scope_path);
CREATE INDEX IF NOT EXISTS device_credential_scope_path_idx ON tenancy.device_credential USING gist (scope_path);
CREATE INDEX IF NOT EXISTS device_rollout_scope_path_idx ON tenancy.device_rollout USING gist (scope_path);
CREATE INDEX IF NOT EXISTS device_tamper_event_scope_path_idx ON tenancy.device_tamper_event USING gist (scope_path);
CREATE INDEX IF NOT EXISTS device_telemetry_scope_path_idx ON tenancy.device_telemetry USING gist (scope_path);
CREATE INDEX IF NOT EXISTS dispute_scope_path_idx ON wallet.dispute USING gist (scope_path);
CREATE INDEX IF NOT EXISTS distribution_channel_scope_path_idx ON assets.distribution_channel USING gist (scope_path);
CREATE INDEX IF NOT EXISTS document_scope_path_idx ON accreditation.document USING gist (scope_path);
CREATE INDEX IF NOT EXISTS dunning_case_scope_path_idx ON payments.dunning_case USING gist (scope_path);
CREATE INDEX IF NOT EXISTS dunning_policy_scope_path_idx ON payments.dunning_policy USING gist (scope_path);
CREATE INDEX IF NOT EXISTS duplicate_candidate_scope_path_idx ON marketing.duplicate_candidate USING gist (scope_path);
CREATE INDEX IF NOT EXISTS duration_rules_scope_path_idx ON rental.duration_rules USING gist (scope_path);
CREATE INDEX IF NOT EXISTS dynamic_price_rule_scope_path_idx ON pricing.dynamic_price_rule USING gist (scope_path);
CREATE INDEX IF NOT EXISTS eligibility_rule_scope_path_idx ON payments.eligibility_rule USING gist (scope_path);
CREATE INDEX IF NOT EXISTS entitlement_scope_path_idx ON access.entitlement USING gist (scope_path);
CREATE INDEX IF NOT EXISTS entitlement_scope_path_idx ON games.entitlement USING gist (scope_path);
CREATE INDEX IF NOT EXISTS entitlement_template_scope_path_idx ON catalogue.entitlement_template USING gist (scope_path);
CREATE INDEX IF NOT EXISTS equipment_assignment_scope_path_idx ON rental.equipment_assignment USING gist (scope_path);
CREATE INDEX IF NOT EXISTS event_capacity_profile_scope_path_idx ON catalogue.event_capacity_profile USING gist (scope_path);
CREATE INDEX IF NOT EXISTS event_registration_scope_path_idx ON catalogue.event_registration USING gist (scope_path);
CREATE INDEX IF NOT EXISTS event_reschedule_scope_path_idx ON catalogue.event_reschedule USING gist (scope_path);
CREATE INDEX IF NOT EXISTS event_resource_plan_scope_path_idx ON catalogue.event_resource_plan USING gist (scope_path);
CREATE INDEX IF NOT EXISTS event_schedule_scope_path_idx ON catalogue.event_schedule USING gist (scope_path);
CREATE INDEX IF NOT EXISTS event_scope_path_idx ON catalogue.event USING gist (scope_path);
CREATE INDEX IF NOT EXISTS event_type_scope_path_idx ON catalogue.event_type USING gist (scope_path);
CREATE INDEX IF NOT EXISTS evidence_package_scope_path_idx ON approvals.evidence_package USING gist (scope_path);
CREATE INDEX IF NOT EXISTS failover_policy_scope_path_idx ON payments.failover_policy USING gist (scope_path);
CREATE INDEX IF NOT EXISTS faq_category_scope_path_idx ON whitelabel.faq_category USING gist (scope_path);
CREATE INDEX IF NOT EXISTS fee_policy_scope_path_idx ON rental.fee_policy USING gist (scope_path);
CREATE INDEX IF NOT EXISTS field_ownership_scope_path_idx ON workforce.field_ownership USING gist (scope_path);
CREATE INDEX IF NOT EXISTS form_definition_scope_path_idx ON marketing.form_definition USING gist (scope_path);
CREATE INDEX IF NOT EXISTS fraud_rule_scope_path_idx ON orders.fraud_rule USING gist (scope_path);
CREATE INDEX IF NOT EXISTS funding_rules_scope_path_idx ON wallet.funding_rules USING gist (scope_path);
CREATE INDEX IF NOT EXISTS fx_provider_assignment_scope_path_idx ON ledger.fx_provider_assignment USING gist (scope_path);
CREATE INDEX IF NOT EXISTS gameplay_transaction_scope_path_idx ON games.gameplay_transaction USING gist (scope_path);
CREATE INDEX IF NOT EXISTS gift_card_product_scope_path_idx ON wallet.gift_card_product USING gist (scope_path);
CREATE INDEX IF NOT EXISTS group_package_scope_path_idx ON catalogue.group_package USING gist (scope_path);
CREATE INDEX IF NOT EXISTS group_request_scope_path_idx ON seating.group_request USING gist (scope_path);
CREATE INDEX IF NOT EXISTS guest_attribute_model_scope_path_idx ON marketing.guest_attribute_model USING gist (scope_path);
CREATE INDEX IF NOT EXISTS guest_match_decision_scope_path_idx ON marketing.guest_match_decision USING gist (scope_path);
CREATE INDEX IF NOT EXISTS guest_match_policy_scope_path_idx ON marketing.guest_match_policy USING gist (scope_path);
CREATE INDEX IF NOT EXISTS guest_relationship_scope_path_idx ON marketing.guest_relationship USING gist (scope_path);
CREATE INDEX IF NOT EXISTS hold_pool_scope_path_idx ON seating.hold_pool USING gist (scope_path);
CREATE INDEX IF NOT EXISTS hold_type_scope_path_idx ON seating.hold_type USING gist (scope_path);
CREATE INDEX IF NOT EXISTS holder_access_scope_path_idx ON accreditation.holder_access USING gist (scope_path);
CREATE INDEX IF NOT EXISTS holder_scope_path_idx ON accreditation.holder USING gist (scope_path);
CREATE INDEX IF NOT EXISTS hosted_checkout_scope_path_idx ON payments.hosted_checkout USING gist (scope_path);
CREATE INDEX IF NOT EXISTS identity_rules_scope_path_idx ON marketing.identity_rules USING gist (scope_path);
CREATE INDEX IF NOT EXISTS import_job_scope_path_idx ON catalogue.import_job USING gist (scope_path);
CREATE INDEX IF NOT EXISTS incident_scope_path_idx ON rental.incident USING gist (scope_path);
CREATE INDEX IF NOT EXISTS inspection_scope_path_idx ON rental.inspection USING gist (scope_path);
CREATE INDEX IF NOT EXISTS integration_source_scope_path_idx ON workforce.integration_source USING gist (scope_path);
CREATE INDEX IF NOT EXISTS inventory_model_scope_path_idx ON rental.inventory_model USING gist (scope_path);
CREATE INDEX IF NOT EXISTS invitation_campaign_scope_path_idx ON marketing.invitation_campaign USING gist (scope_path);
CREATE INDEX IF NOT EXISTS invitation_scope_path_idx ON marketing.invitation USING gist (scope_path);
CREATE INDEX IF NOT EXISTS journey_enrollment_scope_path_idx ON marketing.journey_enrollment USING gist (scope_path);
CREATE INDEX IF NOT EXISTS journey_scope_path_idx ON marketing.journey USING gist (scope_path);
CREATE INDEX IF NOT EXISTS kiosk_config_scope_path_idx ON games.kiosk_config USING gist (scope_path);
CREATE INDEX IF NOT EXISTS knowledge_collection_scope_path_idx ON ai.knowledge_collection USING gist (scope_path);
CREATE INDEX IF NOT EXISTS kpi_definition_scope_path_idx ON reporting.kpi_definition USING gist (scope_path);
CREATE INDEX IF NOT EXISTS kpi_target_scope_path_idx ON reporting.kpi_target USING gist (scope_path);
CREATE INDEX IF NOT EXISTS layout_draft_scope_path_idx ON ai.layout_draft USING gist (scope_path);
CREATE INDEX IF NOT EXISTS leave_request_scope_path_idx ON workforce.leave_request USING gist (scope_path);
CREATE INDEX IF NOT EXISTS legal_entity_scope_path_idx ON ledger.legal_entity USING gist (scope_path);
CREATE INDEX IF NOT EXISTS location_rule_scope_path_idx ON rental.location_rule USING gist (scope_path);
CREATE INDEX IF NOT EXISTS map_scope_path_idx ON venuemap.map USING gist (scope_path);
CREATE INDEX IF NOT EXISTS matching_rules_scope_path_idx ON payments.matching_rules USING gist (scope_path);
CREATE INDEX IF NOT EXISTS matrix_scope_path_idx ON approvals.matrix USING gist (scope_path);
CREATE INDEX IF NOT EXISTS menu_schedule_scope_path_idx ON fnb.menu_schedule USING gist (scope_path);
CREATE INDEX IF NOT EXISTS menu_version_scope_path_idx ON fnb.menu_version USING gist (scope_path);
CREATE INDEX IF NOT EXISTS merchant_account_scope_path_idx ON payments.merchant_account USING gist (scope_path);
CREATE INDEX IF NOT EXISTS message_trigger_scope_path_idx ON marketing.message_trigger USING gist (scope_path);
CREATE INDEX IF NOT EXISTS method_config_scope_path_idx ON payments.method_config USING gist (scope_path);
CREATE INDEX IF NOT EXISTS method_scope_path_idx ON payments.method USING gist (scope_path);
CREATE INDEX IF NOT EXISTS mixed_tender_rules_scope_path_idx ON payments.mixed_tender_rules USING gist (scope_path);
CREATE INDEX IF NOT EXISTS modifier_group_scope_path_idx ON fnb.modifier_group USING gist (scope_path);
CREATE INDEX IF NOT EXISTS module_access_scope_path_idx ON identity.module_access USING gist (scope_path);
CREATE INDEX IF NOT EXISTS natural_language_query_scope_path_idx ON reporting.natural_language_query USING gist (scope_path);
CREATE INDEX IF NOT EXISTS notification_rules_scope_path_idx ON accreditation.notification_rules USING gist (scope_path);
CREATE INDEX IF NOT EXISTS offline_policy_scope_path_idx ON platform.offline_policy USING gist (scope_path);
CREATE INDEX IF NOT EXISTS open_shift_scope_path_idx ON workforce.open_shift USING gist (scope_path);
CREATE INDEX IF NOT EXISTS operational_config_scope_path_idx ON games.operational_config USING gist (scope_path);
CREATE INDEX IF NOT EXISTS operational_rules_scope_path_idx ON rental.operational_rules USING gist (scope_path);
CREATE INDEX IF NOT EXISTS order_fulfilment_scope_path_idx ON fnb.order_fulfilment USING gist (scope_path);
CREATE INDEX IF NOT EXISTS outbox_scope_path_idx ON platform.outbox USING gist (scope_path);
CREATE INDEX IF NOT EXISTS override_scope_path_idx ON rental.override USING gist (scope_path);
CREATE INDEX IF NOT EXISTS password_policy_scope_path_idx ON identity.password_policy USING gist (scope_path);
CREATE INDEX IF NOT EXISTS payment_link_scope_path_idx ON orders.payment_link USING gist (scope_path);
CREATE INDEX IF NOT EXISTS payment_terms_scope_path_idx ON payments.payment_terms USING gist (scope_path);
CREATE INDEX IF NOT EXISTS pipeline_scope_path_idx ON reporting.pipeline USING gist (scope_path);
CREATE INDEX IF NOT EXISTS policy_scope_path_idx ON ai.policy USING gist (scope_path);
CREATE INDEX IF NOT EXISTS policy_scope_path_idx ON whitelabel.policy USING gist (scope_path);
CREATE INDEX IF NOT EXISTS pos_shift_scope_path_idx ON orders.pos_shift USING gist (scope_path);
CREATE INDEX IF NOT EXISTS prepaid_minutes_scope_path_idx ON catalogue.prepaid_minutes USING gist (scope_path);
CREATE INDEX IF NOT EXISTS pricing_profile_scope_path_idx ON rental.pricing_profile USING gist (scope_path);
CREATE INDEX IF NOT EXISTS pricing_scope_path_idx ON games.pricing USING gist (scope_path);
CREATE INDEX IF NOT EXISTS print_job_scope_path_idx ON accreditation.print_job USING gist (scope_path);
CREATE INDEX IF NOT EXISTS privacy_incident_scope_path_idx ON marketing.privacy_incident USING gist (scope_path);
CREATE INDEX IF NOT EXISTS prize_cost_scope_path_idx ON games.prize_cost USING gist (scope_path);
CREATE INDEX IF NOT EXISTS product_category_scope_path_idx ON catalogue.product_category USING gist (scope_path);
CREATE INDEX IF NOT EXISTS product_eligibility_rule_scope_path_idx ON catalogue.product_eligibility_rule USING gist (scope_path);
CREATE INDEX IF NOT EXISTS product_recommendation_scope_path_idx ON fnb.product_recommendation USING gist (scope_path);
CREATE INDEX IF NOT EXISTS product_recommendation_scope_path_idx ON retail.product_recommendation USING gist (scope_path);
CREATE INDEX IF NOT EXISTS product_relationship_scope_path_idx ON promotions.product_relationship USING gist (scope_path);
CREATE INDEX IF NOT EXISTS product_scope_path_idx ON catalogue.product USING gist (scope_path);
CREATE INDEX IF NOT EXISTS product_scope_path_idx ON rental.product USING gist (scope_path);
CREATE INDEX IF NOT EXISTS programme_scope_path_idx ON accreditation.programme USING gist (scope_path);
CREATE INDEX IF NOT EXISTS promo_block_scope_path_idx ON whitelabel.promo_block USING gist (scope_path);
CREATE INDEX IF NOT EXISTS provider_connection_scope_path_idx ON payments.provider_connection USING gist (scope_path);
CREATE INDEX IF NOT EXISTS provider_scope_path_idx ON ai.provider USING gist (scope_path);
CREATE INDEX IF NOT EXISTS provider_scope_path_idx ON payments.provider USING gist (scope_path);
CREATE INDEX IF NOT EXISTS purchase_order_scope_path_idx ON inventory.purchase_order USING gist (scope_path);
CREATE INDEX IF NOT EXISTS qualification_scope_path_idx ON resources.qualification USING gist (scope_path);
CREATE INDEX IF NOT EXISTS quotation_scope_path_idx ON inventory.quotation USING gist (scope_path);
CREATE INDEX IF NOT EXISTS reader_profile_scope_path_idx ON games.reader_profile USING gist (scope_path);
CREATE INDEX IF NOT EXISTS reader_scope_path_idx ON games.reader USING gist (scope_path);
CREATE INDEX IF NOT EXISTS reassignment_scope_path_idx ON seating.reassignment USING gist (scope_path);
CREATE INDEX IF NOT EXISTS recommendation_experiment_scope_path_idx ON promotions.recommendation_experiment USING gist (scope_path);
CREATE INDEX IF NOT EXISTS recommendation_outcome_scope_path_idx ON promotions.recommendation_outcome USING gist (scope_path);
CREATE INDEX IF NOT EXISTS recommendation_rules_scope_path_idx ON seating.recommendation_rules USING gist (scope_path);
CREATE INDEX IF NOT EXISTS recommendation_strategy_scope_path_idx ON promotions.recommendation_strategy USING gist (scope_path);
CREATE INDEX IF NOT EXISTS recommendation_suppression_scope_path_idx ON promotions.recommendation_suppression USING gist (scope_path);
CREATE INDEX IF NOT EXISTS reconciliation_source_scope_path_idx ON payments.reconciliation_source USING gist (scope_path);
CREATE INDEX IF NOT EXISTS redemption_rules_scope_path_idx ON games.redemption_rules USING gist (scope_path);
CREATE INDEX IF NOT EXISTS referral_scope_path_idx ON marketing.referral USING gist (scope_path);
CREATE INDEX IF NOT EXISTS refund_batch_scope_path_idx ON orders.refund_batch USING gist (scope_path);
CREATE INDEX IF NOT EXISTS refund_policy_scope_path_idx ON wallet.refund_policy USING gist (scope_path);
CREATE INDEX IF NOT EXISTS rendition_scope_path_idx ON assets.rendition USING gist (scope_path);
CREATE INDEX IF NOT EXISTS report_definition_scope_path_idx ON reporting.report_definition USING gist (scope_path);
CREATE INDEX IF NOT EXISTS report_definition_version_scope_path_idx ON reporting.report_definition_version USING gist (scope_path);
CREATE INDEX IF NOT EXISTS request_scope_path_idx ON approvals.request USING gist (scope_path);
CREATE INDEX IF NOT EXISTS requirements_scope_path_idx ON accreditation.requirements USING gist (scope_path);
CREATE INDEX IF NOT EXISTS resale_fee_policy_scope_path_idx ON orders.resale_fee_policy USING gist (scope_path);
CREATE INDEX IF NOT EXISTS resale_listing_scope_path_idx ON orders.resale_listing USING gist (scope_path);
CREATE INDEX IF NOT EXISTS reservation_policy_scope_path_idx ON fnb.reservation_policy USING gist (scope_path);
CREATE INDEX IF NOT EXISTS resource_audit_scope_path_idx ON resources.resource_audit USING gist (scope_path);
CREATE INDEX IF NOT EXISTS resource_block_scope_path_idx ON resources.resource_block USING gist (scope_path);
CREATE INDEX IF NOT EXISTS resource_category_scope_path_idx ON resources.resource_category USING gist (scope_path);
CREATE INDEX IF NOT EXISTS resource_dependency_scope_path_idx ON resources.resource_dependency USING gist (scope_path);
CREATE INDEX IF NOT EXISTS resource_package_scope_path_idx ON resources.resource_package USING gist (scope_path);
CREATE INDEX IF NOT EXISTS resource_relation_scope_path_idx ON resources.resource_relation USING gist (scope_path);
CREATE INDEX IF NOT EXISTS resource_requirement_scope_path_idx ON resources.resource_requirement USING gist (scope_path);
CREATE INDEX IF NOT EXISTS resource_schedule_scope_path_idx ON resources.resource_schedule USING gist (scope_path);
CREATE INDEX IF NOT EXISTS resource_scope_path_idx ON resources.resource USING gist (scope_path);
CREATE INDEX IF NOT EXISTS resource_type_scope_path_idx ON resources.resource_type USING gist (scope_path);
CREATE INDEX IF NOT EXISTS restriction_scope_path_idx ON wallet.restriction USING gist (scope_path);
CREATE INDEX IF NOT EXISTS retention_policy_scope_path_idx ON approvals.retention_policy USING gist (scope_path);
CREATE INDEX IF NOT EXISTS retention_policy_scope_path_idx ON marketing.retention_policy USING gist (scope_path);
CREATE INDEX IF NOT EXISTS risk_rules_scope_path_idx ON payments.risk_rules USING gist (scope_path);
CREATE INDEX IF NOT EXISTS risk_rules_scope_path_idx ON wallet.risk_rules USING gist (scope_path);
CREATE INDEX IF NOT EXISTS routing_rule_scope_path_idx ON payments.routing_rule USING gist (scope_path);
CREATE INDEX IF NOT EXISTS sales_order_scope_path_idx ON orders.sales_order USING gist (scope_path);
CREATE INDEX IF NOT EXISTS scan_event_scope_path_idx ON access.scan_event USING gist (scope_path);
CREATE INDEX IF NOT EXISTS scope_path_idx ON platform.scope USING gist (path);
CREATE INDEX IF NOT EXISTS seat_block_scope_path_idx ON seating.seat_block USING gist (scope_path);
CREATE INDEX IF NOT EXISTS seat_rules_scope_path_idx ON seating.seat_rules USING gist (scope_path);
CREATE INDEX IF NOT EXISTS section_scope_path_idx ON seating.section USING gist (scope_path);
CREATE INDEX IF NOT EXISTS segregation_rule_scope_path_idx ON identity.segregation_rule USING gist (scope_path);
CREATE INDEX IF NOT EXISTS semantic_model_scope_path_idx ON reporting.semantic_model USING gist (scope_path);
CREATE INDEX IF NOT EXISTS service_charge_policy_scope_path_idx ON fnb.service_charge_policy USING gist (scope_path);
CREATE INDEX IF NOT EXISTS session_template_scope_path_idx ON catalogue.session_template USING gist (scope_path);
CREATE INDEX IF NOT EXISTS settlement_scope_path_idx ON ledger.settlement USING gist (scope_path);
CREATE INDEX IF NOT EXISTS settlement_scope_path_idx ON rental.settlement USING gist (scope_path);
CREATE INDEX IF NOT EXISTS share_scope_path_idx ON assets.share USING gist (scope_path);
CREATE INDEX IF NOT EXISTS shared_wallet_scope_path_idx ON wallet.shared_wallet USING gist (scope_path);
CREATE INDEX IF NOT EXISTS shift_template_scope_path_idx ON workforce.shift_template USING gist (scope_path);
CREATE INDEX IF NOT EXISTS signature_scope_path_idx ON approvals.signature USING gist (scope_path);
CREATE INDEX IF NOT EXISTS sla_policy_scope_path_idx ON approvals.sla_policy USING gist (scope_path);
CREATE INDEX IF NOT EXISTS sla_policy_scope_path_idx ON marketing.sla_policy USING gist (scope_path);
CREATE INDEX IF NOT EXISTS space_scope_path_idx ON catalogue.space USING gist (scope_path);
CREATE INDEX IF NOT EXISTS sso_group_mapping_scope_path_idx ON identity.sso_group_mapping USING gist (scope_path);
CREATE INDEX IF NOT EXISTS sso_provider_scope_path_idx ON identity.sso_provider USING gist (scope_path);
CREATE INDEX IF NOT EXISTS staffing_rules_scope_path_idx ON workforce.staffing_rules USING gist (scope_path);
CREATE INDEX IF NOT EXISTS stored_forward_scope_path_idx ON payments.stored_forward USING gist (scope_path);
CREATE INDEX IF NOT EXISTS stored_value_authorisation_scope_path_idx ON orders.stored_value_authorisation USING gist (scope_path);
CREATE INDEX IF NOT EXISTS subscription_scope_path_idx ON reporting.subscription USING gist (scope_path);
CREATE INDEX IF NOT EXISTS suggestion_scope_path_idx ON ai.suggestion USING gist (scope_path);
CREATE INDEX IF NOT EXISTS supplier_scope_path_idx ON inventory.supplier USING gist (scope_path);
CREATE INDEX IF NOT EXISTS suppression_scope_path_idx ON marketing.suppression USING gist (scope_path);
CREATE INDEX IF NOT EXISTS sync_conflict_scope_path_idx ON workforce.sync_conflict USING gist (scope_path);
CREATE INDEX IF NOT EXISTS sync_run_scope_path_idx ON workforce.sync_run USING gist (scope_path);
CREATE INDEX IF NOT EXISTS table_combination_scope_path_idx ON fnb.table_combination USING gist (scope_path);
CREATE INDEX IF NOT EXISTS tag_scope_path_idx ON assets.tag USING gist (scope_path);
CREATE INDEX IF NOT EXISTS taxonomy_scope_path_idx ON assets.taxonomy USING gist (scope_path);
CREATE INDEX IF NOT EXISTS temperature_checkpoint_scope_path_idx ON fnb.temperature_checkpoint USING gist (scope_path);
CREATE INDEX IF NOT EXISTS terminal_scope_path_idx ON payments.terminal USING gist (scope_path);
CREATE INDEX IF NOT EXISTS transfer_rules_scope_path_idx ON wallet.transfer_rules USING gist (scope_path);
CREATE INDEX IF NOT EXISTS transfer_scope_path_idx ON inventory.transfer USING gist (scope_path);
CREATE INDEX IF NOT EXISTS validation_rules_scope_path_idx ON games.validation_rules USING gist (scope_path);
CREATE INDEX IF NOT EXISTS validity_scope_path_idx ON accreditation.validity USING gist (scope_path);
CREATE INDEX IF NOT EXISTS venue_assignment_scope_path_idx ON resources.venue_assignment USING gist (scope_path);
CREATE INDEX IF NOT EXISTS visit_reminder_scope_path_idx ON orders.visit_reminder USING gist (scope_path);
CREATE INDEX IF NOT EXISTS voucher_type_scope_path_idx ON wallet.voucher_type USING gist (scope_path);
CREATE INDEX IF NOT EXISTS wallet_pass_scope_path_idx ON orders.wallet_pass USING gist (scope_path);
CREATE INDEX IF NOT EXISTS wallet_type_scope_path_idx ON wallet.wallet_type USING gist (scope_path);
CREATE INDEX IF NOT EXISTS work_assignment_scope_path_idx ON workforce.work_assignment USING gist (scope_path);
CREATE INDEX IF NOT EXISTS workstation_scope_path_idx ON platform.workstation USING gist (scope_path);
