-- Conventions and scope paths in the tenant database.
-- **A convention is indexed and not constrained** (ADR-0011): most references are
-- naming habits the contracts never asserted, and enforcing one fails on the first
-- row that legitimately points nowhere.

-- convention, not declared: access.entitlement.order_line_id -> orders.order_line
CREATE INDEX IF NOT EXISTS ix_entitlement_order_line_id ON access.entitlement (order_line_id);
-- convention, not declared: access.entitlement.product_id -> catalogue.product
CREATE INDEX IF NOT EXISTS ix_entitlement_product_id ON access.entitlement (product_id);
-- convention, not declared: access.entitlement.subject_id -> pii.subject
CREATE INDEX IF NOT EXISTS ix_entitlement_subject_id ON access.entitlement (subject_id);
-- convention, not declared: access.entitlement.supersedes_entitlement_id -> access.entitlement
CREATE INDEX IF NOT EXISTS ix_entitlement_supersedes_entitlement_id ON access.entitlement (supersedes_entitlement_id);
-- convention, not declared: ai.index_failure.source_id -> ai.index_source
CREATE INDEX IF NOT EXISTS ix_index_failure_source_id ON ai.index_failure (source_id);
-- convention, not declared: ai.interaction.billable_to_tenant_id -> control.tenant
CREATE INDEX IF NOT EXISTS ix_interaction_billable_to_tenant_id ON ai.interaction (billable_to_tenant_id);
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
-- convention, not declared: assets.media_upload.upload_id -> assets.media_upload
CREATE INDEX IF NOT EXISTS ix_media_upload_upload_id ON assets.media_upload (upload_id);
-- convention, not declared: catalogue.entitlement_template.admission_rules_id -> access.admission_rules
CREATE INDEX IF NOT EXISTS ix_entitlement_template_admission_rules_id ON catalogue.entitlement_template (admission_rules_id);
-- convention, not declared: catalogue.entitlement_template.entitlement_id -> access.entitlement
CREATE INDEX IF NOT EXISTS ix_entitlement_template_entitlement_id ON catalogue.entitlement_template (entitlement_id);
-- convention, not declared: catalogue.entitlement_template.transferred_to_subject_id -> pii.subject
CREATE INDEX IF NOT EXISTS ix_entitlement_template_transferred_to_subject_id ON catalogue.entitlement_template (transferred_to_subject_id);
-- convention, not declared: catalogue.event.parent_event_id -> catalogue.event
CREATE INDEX IF NOT EXISTS ix_event_parent_event_id ON catalogue.event (parent_event_id);
-- convention, not declared: catalogue.inventory_hold.channel_capacity_id -> catalogue.channel_capacity
CREATE INDEX IF NOT EXISTS ix_inventory_hold_channel_capacity_id ON catalogue.inventory_hold (channel_capacity_id);
-- convention, not declared: catalogue.inventory_hold.parent_lease_id -> catalogue.inventory_hold
CREATE INDEX IF NOT EXISTS ix_inventory_hold_parent_lease_id ON catalogue.inventory_hold (parent_lease_id);
-- convention, not declared: catalogue.performance.admission_rules_id -> access.admission_rules
CREATE INDEX IF NOT EXISTS ix_performance_admission_rules_id ON catalogue.performance (admission_rules_id);
-- convention, not declared: catalogue.performance.approval_request_id -> approvals.request
CREATE INDEX IF NOT EXISTS ix_performance_approval_request_id ON catalogue.performance (approval_request_id);
-- convention, not declared: catalogue.product.approved_by_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS ix_product_approved_by_principal_id ON catalogue.product (approved_by_principal_id);
-- convention, not declared: catalogue.product.created_by_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS ix_product_created_by_principal_id ON catalogue.product (created_by_principal_id);
-- convention, not declared: catalogue.product_category.image_asset_id -> maintenance.asset
CREATE INDEX IF NOT EXISTS ix_product_category_image_asset_id ON catalogue.product_category (image_asset_id);
-- convention, not declared: catalogue.product_version.published_by_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS ix_product_version_published_by_principal_id ON catalogue.product_version (published_by_principal_id);
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
-- convention, not declared: fnb.eighty_six_event.called_by_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS ix_eighty_six_event_called_by_principal_id ON fnb.eighty_six_event (called_by_principal_id);
-- convention, not declared: fnb.eighty_six_event.menu_item_id -> fnb.menu_item
CREATE INDEX IF NOT EXISTS ix_eighty_six_event_menu_item_id ON fnb.eighty_six_event (menu_item_id);
-- convention, not declared: fnb.eighty_six_event.outlet_id -> platform.outlet
CREATE INDEX IF NOT EXISTS ix_eighty_six_event_outlet_id ON fnb.eighty_six_event (outlet_id);
-- convention, not declared: fnb.fnb_order_line.menu_item_id -> fnb.menu_item
CREATE INDEX IF NOT EXISTS ix_fnb_order_line_menu_item_id ON fnb.fnb_order_line (menu_item_id);
-- convention, not declared: fnb.kitchen_exception.outlet_id -> platform.outlet
CREATE INDEX IF NOT EXISTS ix_kitchen_exception_outlet_id ON fnb.kitchen_exception (outlet_id);
-- convention, not declared: fnb.kitchen_exception.raised_by_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS ix_kitchen_exception_raised_by_principal_id ON fnb.kitchen_exception (raised_by_principal_id);
-- convention, not declared: fnb.kitchen_exception.station_id -> fnb.kitchen_station
CREATE INDEX IF NOT EXISTS ix_kitchen_exception_station_id ON fnb.kitchen_exception (station_id);
-- convention, not declared: fnb.kitchen_exception.ticket_id -> fnb.kitchen_ticket
CREATE INDEX IF NOT EXISTS ix_kitchen_exception_ticket_id ON fnb.kitchen_exception (ticket_id);
-- convention, not declared: fnb.production_plan.based_on_suggestion_id -> ai.suggestion
CREATE INDEX IF NOT EXISTS ix_production_plan_based_on_suggestion_id ON fnb.production_plan (based_on_suggestion_id);
-- convention, not declared: fnb.production_plan.outlet_id -> platform.outlet
CREATE INDEX IF NOT EXISTS ix_production_plan_outlet_id ON fnb.production_plan (outlet_id);
-- convention, not declared: fnb.production_run.producing_outlet_id -> platform.outlet
CREATE INDEX IF NOT EXISTS ix_production_run_producing_outlet_id ON fnb.production_run (producing_outlet_id);
-- convention, not declared: fnb.sub_bill.sub_bill_id -> fnb.sub_bill
CREATE INDEX IF NOT EXISTS ix_sub_bill_sub_bill_id ON fnb.sub_bill (sub_bill_id);
-- convention, not declared: fnb.sub_bill.visit_id -> fnb.table_visit
CREATE INDEX IF NOT EXISTS ix_sub_bill_visit_id ON fnb.sub_bill (visit_id);
-- convention, not declared: fnb.substitution_rule.from_ingredient_id -> fnb.recipe_ingredient
CREATE INDEX IF NOT EXISTS ix_substitution_rule_from_ingredient_id ON fnb.substitution_rule (from_ingredient_id);
-- convention, not declared: fnb.substitution_rule.to_ingredient_id -> fnb.recipe_ingredient
CREATE INDEX IF NOT EXISTS ix_substitution_rule_to_ingredient_id ON fnb.substitution_rule (to_ingredient_id);
-- convention, not declared: fnb.table_reservation.group_id -> orders.group_booking
CREATE INDEX IF NOT EXISTS ix_table_reservation_group_id ON fnb.table_reservation (group_id);
-- convention, not declared: fnb.table_visit.merged_into_visit_id -> fnb.table_visit
CREATE INDEX IF NOT EXISTS ix_table_visit_merged_into_visit_id ON fnb.table_visit (merged_into_visit_id);
-- convention, not declared: fnb.temperature_log.check_point_id -> venuemap.point
CREATE INDEX IF NOT EXISTS ix_temperature_log_check_point_id ON fnb.temperature_log (check_point_id);
-- convention, not declared: fnb.temperature_log.corrective_action_id -> fnb.corrective_action
CREATE INDEX IF NOT EXISTS ix_temperature_log_corrective_action_id ON fnb.temperature_log (corrective_action_id);
-- convention, not declared: fnb.temperature_log.recorded_by_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS ix_temperature_log_recorded_by_principal_id ON fnb.temperature_log (recorded_by_principal_id);
-- convention, not declared: games.play.play_id -> games.play
CREATE INDEX IF NOT EXISTS ix_play_play_id ON games.play (play_id);
-- convention, not declared: identity.delegated_access.over_subject_id -> pii.subject
CREATE INDEX IF NOT EXISTS ix_delegated_access_over_subject_id ON identity.delegated_access (over_subject_id);
-- convention, not declared: identity.role.inherits_from_role_id -> identity.role
CREATE INDEX IF NOT EXISTS ix_role_inherits_from_role_id ON identity.role (inherits_from_role_id);
-- convention, not declared: identity.role_permission.granted_by_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS ix_role_permission_granted_by_principal_id ON identity.role_permission (granted_by_principal_id);
-- convention, not declared: identity.sso_provider.client_id -> control.api_client
CREATE INDEX IF NOT EXISTS ix_sso_provider_client_id ON identity.sso_provider (client_id);
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
-- convention, not declared: inventory.movement.source_id -> ai.index_source
CREATE INDEX IF NOT EXISTS ix_movement_source_id ON inventory.movement (source_id);
-- convention, not declared: inventory.serialised_item.item_id -> inventory.item
CREATE INDEX IF NOT EXISTS ix_serialised_item_item_id ON inventory.serialised_item (item_id);
-- convention, not declared: inventory.serialised_item.location_id -> inventory.location
CREATE INDEX IF NOT EXISTS ix_serialised_item_location_id ON inventory.serialised_item (location_id);
-- convention, not declared: inventory.serialised_item.sold_on_order_line_id -> orders.order_line
CREATE INDEX IF NOT EXISTS ix_serialised_item_sold_on_order_line_id ON inventory.serialised_item (sold_on_order_line_id);
-- convention, not declared: ledger.deposit.liability_account_id -> ledger.account
CREATE INDEX IF NOT EXISTS ix_deposit_liability_account_id ON ledger.deposit (liability_account_id);
-- convention, not declared: ledger.fx_rate.set_by_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS ix_fx_rate_set_by_principal_id ON ledger.fx_rate (set_by_principal_id);
-- convention, not declared: ledger.inter_entity_obligation.from_legal_entity_id -> ledger.legal_entity
CREATE INDEX IF NOT EXISTS ix_inter_entity_obligation_from_legal_entity_id ON ledger.inter_entity_obligation (from_legal_entity_id);
-- convention, not declared: ledger.inter_entity_obligation.to_legal_entity_id -> ledger.legal_entity
CREATE INDEX IF NOT EXISTS ix_inter_entity_obligation_to_legal_entity_id ON ledger.inter_entity_obligation (to_legal_entity_id);
-- convention, not declared: ledger.journal_entry.source_id -> ai.index_source
CREATE INDEX IF NOT EXISTS ix_journal_entry_source_id ON ledger.journal_entry (source_id);
-- convention, not declared: ledger.journal_line.account_id -> ledger.account
CREATE INDEX IF NOT EXISTS ix_journal_line_account_id ON ledger.journal_line (account_id);
-- convention, not declared: ledger.journal_line.cost_center_id -> ledger.cost_center
CREATE INDEX IF NOT EXISTS ix_journal_line_cost_center_id ON ledger.journal_line (cost_center_id);
-- convention, not declared: ledger.posting.source_id -> ai.index_source
CREATE INDEX IF NOT EXISTS ix_posting_source_id ON ledger.posting (source_id);
-- convention, not declared: ledger.recognition_schedule.no_show_account_id -> ledger.account
CREATE INDEX IF NOT EXISTS ix_recognition_schedule_no_show_account_id ON ledger.recognition_schedule (no_show_account_id);
-- convention, not declared: ledger.tax_code.compound_on_tax_code_id -> ledger.tax_code
CREATE INDEX IF NOT EXISTS ix_tax_code_compound_on_tax_code_id ON ledger.tax_code (compound_on_tax_code_id);
-- convention, not declared: maintenance.asset.resource_id -> resources.resource
CREATE INDEX IF NOT EXISTS ix_asset_resource_id ON maintenance.asset (resource_id);
-- convention, not declared: maintenance.work_order.verified_by_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS ix_work_order_verified_by_principal_id ON maintenance.work_order (verified_by_principal_id);
-- convention, not declared: maintenance.work_order_attachment.captured_by_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS ix_work_order_attachment_captured_by_principal_id ON maintenance.work_order_attachment (captured_by_principal_id);
-- convention, not declared: marketing.challenge.badge_asset_id -> maintenance.asset
CREATE INDEX IF NOT EXISTS ix_challenge_badge_asset_id ON marketing.challenge (badge_asset_id);
-- convention, not declared: marketing.conversation.assist_session_id -> marketing.kiosk_assist_session
CREATE INDEX IF NOT EXISTS ix_conversation_assist_session_id ON marketing.conversation (assist_session_id);
-- convention, not declared: marketing.conversation_message.sender_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS ix_conversation_message_sender_principal_id ON marketing.conversation_message (sender_principal_id);
-- convention, not declared: marketing.form_submission.on_behalf_of_subject_id -> pii.subject
CREATE INDEX IF NOT EXISTS ix_form_submission_on_behalf_of_subject_id ON marketing.form_submission (on_behalf_of_subject_id);
-- convention, not declared: marketing.form_submission.signature_asset_id -> maintenance.asset
CREATE INDEX IF NOT EXISTS ix_form_submission_signature_asset_id ON marketing.form_submission (signature_asset_id);
-- convention, not declared: marketing.guest_document.uploaded_by_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS ix_guest_document_uploaded_by_principal_id ON marketing.guest_document (uploaded_by_principal_id);
-- convention, not declared: marketing.invitation.issued_by_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS ix_invitation_issued_by_principal_id ON marketing.invitation (issued_by_principal_id);
-- convention, not declared: marketing.invitation.offered_by_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS ix_invitation_offered_by_principal_id ON marketing.invitation (offered_by_principal_id);
-- convention, not declared: marketing.journey_entrant.journey_id -> marketing.journey
CREATE INDEX IF NOT EXISTS ix_journey_entrant_journey_id ON marketing.journey_entrant (journey_id);
-- convention, not declared: marketing.journey_entrant.step_id -> approvals.step_up_policy
CREATE INDEX IF NOT EXISTS ix_journey_entrant_step_id ON marketing.journey_entrant (step_id);
-- convention, not declared: marketing.journey_entrant.subject_id -> pii.subject
CREATE INDEX IF NOT EXISTS ix_journey_entrant_subject_id ON marketing.journey_entrant (subject_id);
-- convention, not declared: marketing.lost_item.last_seen_point_id -> venuemap.point
CREATE INDEX IF NOT EXISTS ix_lost_item_last_seen_point_id ON marketing.lost_item (last_seen_point_id);
-- convention, not declared: marketing.lost_item.reported_by_subject_id -> pii.subject
CREATE INDEX IF NOT EXISTS ix_lost_item_reported_by_subject_id ON marketing.lost_item (reported_by_subject_id);
-- convention, not declared: marketing.referral.referee_subject_id -> pii.subject
CREATE INDEX IF NOT EXISTS ix_referral_referee_subject_id ON marketing.referral (referee_subject_id);
-- convention, not declared: marketing.referral.referrer_subject_id -> pii.subject
CREATE INDEX IF NOT EXISTS ix_referral_referrer_subject_id ON marketing.referral (referrer_subject_id);
-- convention, not declared: marketing.subscription.guest_id -> queue.waiting_guest
CREATE INDEX IF NOT EXISTS ix_subscription_guest_id ON marketing.subscription (guest_id);
-- convention, not declared: orders.cart_line.inventory_hold_id -> catalogue.inventory_hold
CREATE INDEX IF NOT EXISTS ix_cart_line_inventory_hold_id ON orders.cart_line (inventory_hold_id);
-- convention, not declared: orders.cash_count_line.denomination_id -> platform.denomination
CREATE INDEX IF NOT EXISTS ix_cash_count_line_denomination_id ON orders.cash_count_line (denomination_id);
-- convention, not declared: orders.cash_count_line.deposit_box_id -> orders.deposit_box
CREATE INDEX IF NOT EXISTS ix_cash_count_line_deposit_box_id ON orders.cash_count_line (deposit_box_id);
-- convention, not declared: orders.credit_override.authorised_by_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS ix_credit_override_authorised_by_principal_id ON orders.credit_override (authorised_by_principal_id);
-- convention, not declared: orders.deposit_box.closed_by_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS ix_deposit_box_closed_by_principal_id ON orders.deposit_box (closed_by_principal_id);
-- convention, not declared: orders.group_booking.leader_subject_id -> pii.subject
CREATE INDEX IF NOT EXISTS ix_group_booking_leader_subject_id ON orders.group_booking (leader_subject_id);
-- convention, not declared: orders.invitation.issued_by_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS ix_invitation_issued_by_principal_id ON orders.invitation (issued_by_principal_id);
-- convention, not declared: orders.invitation.offered_by_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS ix_invitation_offered_by_principal_id ON orders.invitation (offered_by_principal_id);
-- convention, not declared: orders.order_line.inventory_hold_id -> catalogue.inventory_hold
CREATE INDEX IF NOT EXISTS ix_order_line_inventory_hold_id ON orders.order_line (inventory_hold_id);
-- convention, not declared: orders.payment_link.issued_by_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS ix_payment_link_issued_by_principal_id ON orders.payment_link (issued_by_principal_id);
-- convention, not declared: orders.payment_link.reservation_id -> retail.reservation
CREATE INDEX IF NOT EXISTS ix_payment_link_reservation_id ON orders.payment_link (reservation_id);
-- convention, not declared: orders.payment_routing.fallback_provider_id -> ai.provider
CREATE INDEX IF NOT EXISTS ix_payment_routing_fallback_provider_id ON orders.payment_routing (fallback_provider_id);
-- convention, not declared: orders.refund.tax_reversal_entry_id -> queue.waiting_guest
CREATE INDEX IF NOT EXISTS ix_refund_tax_reversal_entry_id ON orders.refund (tax_reversal_entry_id);
-- convention, not declared: orders.resale_listing.entitlement_id -> catalogue.entitlement_template
CREATE INDEX IF NOT EXISTS ix_resale_listing_entitlement_id ON orders.resale_listing (entitlement_id);
-- convention, not declared: orders.resale_listing.seller_subject_id -> pii.subject
CREATE INDEX IF NOT EXISTS ix_resale_listing_seller_subject_id ON orders.resale_listing (seller_subject_id);
-- convention, not declared: orders.resale_listing.sold_to_subject_id -> pii.subject
CREATE INDEX IF NOT EXISTS ix_resale_listing_sold_to_subject_id ON orders.resale_listing (sold_to_subject_id);
-- convention, not declared: orders.wallet_pass.entitlement_id -> catalogue.entitlement_template
CREATE INDEX IF NOT EXISTS ix_wallet_pass_entitlement_id ON orders.wallet_pass (entitlement_id);
-- convention, not declared: pii.subject.erasure_request_id -> approvals.request
CREATE INDEX IF NOT EXISTS ix_subject_erasure_request_id ON pii.subject (erasure_request_id);
-- convention, not declared: pii.subject_biometric.entitlement_id -> catalogue.entitlement_template
CREATE INDEX IF NOT EXISTS ix_subject_biometric_entitlement_id ON pii.subject_biometric (entitlement_id);
-- convention, not declared: pii.subject_biometric.guardian_subject_id -> pii.subject
CREATE INDEX IF NOT EXISTS ix_subject_biometric_guardian_subject_id ON pii.subject_biometric (guardian_subject_id);
-- convention, not declared: platform.cross_region_entitlement.admission_rules_id -> access.admission_rules
CREATE INDEX IF NOT EXISTS ix_cross_region_entitlement_admission_rules_id ON platform.cross_region_entitlement (admission_rules_id);
-- convention, not declared: platform.cross_region_entitlement.right_id -> platform.cross_region_entitlement
CREATE INDEX IF NOT EXISTS ix_cross_region_entitlement_right_id ON platform.cross_region_entitlement (right_id);
-- convention, not declared: platform.dead_letter.outbox_id -> platform.outbox
CREATE INDEX IF NOT EXISTS ix_dead_letter_outbox_id ON platform.dead_letter (outbox_id);
-- convention, not declared: platform.profile_deployment.profile_id -> platform.profile_deployment
CREATE INDEX IF NOT EXISTS ix_profile_deployment_profile_id ON platform.profile_deployment (profile_id);
-- convention, not declared: platform.wallet_authorisation.authorisation_id -> platform.wallet_authorisation
CREATE INDEX IF NOT EXISTS ix_wallet_authorisation_authorisation_id ON platform.wallet_authorisation (authorisation_id);
-- convention, not declared: platform.wallet_authorisation.fx_rate_id -> ledger.fx_rate
CREATE INDEX IF NOT EXISTS ix_wallet_authorisation_fx_rate_id ON platform.wallet_authorisation (fx_rate_id);
-- convention, not declared: platform.workstation.configuration_profile_id -> platform.configuration_profile
CREATE INDEX IF NOT EXISTS ix_workstation_configuration_profile_id ON platform.workstation (configuration_profile_id);
-- convention, not declared: platform.workstation.edge_node_id -> platform.org_unit
CREATE INDEX IF NOT EXISTS ix_workstation_edge_node_id ON platform.workstation (edge_node_id);
-- convention, not declared: queue.queue.parent_queue_id -> queue.queue
CREATE INDEX IF NOT EXISTS ix_queue_parent_queue_id ON queue.queue (parent_queue_id);
-- convention, not declared: reporting.alert.acknowledged_by_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS ix_alert_acknowledged_by_principal_id ON reporting.alert (acknowledged_by_principal_id);
-- convention, not declared: resources.booking.deposit_authorisation_id -> platform.wallet_authorisation
CREATE INDEX IF NOT EXISTS ix_booking_deposit_authorisation_id ON resources.booking (deposit_authorisation_id);
-- convention, not declared: resources.booking.recurrence_group_id -> orders.group_booking
CREATE INDEX IF NOT EXISTS ix_booking_recurrence_group_id ON resources.booking (recurrence_group_id);
-- convention, not declared: resources.qualification.document_asset_id -> maintenance.asset
CREATE INDEX IF NOT EXISTS ix_qualification_document_asset_id ON resources.qualification (document_asset_id);
-- convention, not declared: resources.resource.parent_resource_id -> resources.resource
CREATE INDEX IF NOT EXISTS ix_resource_parent_resource_id ON resources.resource (parent_resource_id);
-- convention, not declared: retail.store_rule.outlet_id -> platform.outlet
CREATE INDEX IF NOT EXISTS ix_store_rule_outlet_id ON retail.store_rule (outlet_id);
-- convention, not declared: subscription.partner_quote.agreement_id -> control.partner_agreement
CREATE INDEX IF NOT EXISTS ix_partner_quote_agreement_id ON subscription.partner_quote (agreement_id);
-- convention, not declared: venuemap.map.base_asset_id -> maintenance.asset
CREATE INDEX IF NOT EXISTS ix_map_base_asset_id ON venuemap.map (base_asset_id);
-- convention, not declared: venuemap.path.from_point_id -> venuemap.point
CREATE INDEX IF NOT EXISTS ix_path_from_point_id ON venuemap.path (from_point_id);
-- convention, not declared: venuemap.path.restricted_by_point_id -> venuemap.point
CREATE INDEX IF NOT EXISTS ix_path_restricted_by_point_id ON venuemap.path (restricted_by_point_id);
-- convention, not declared: venuemap.path.to_point_id -> venuemap.point
CREATE INDEX IF NOT EXISTS ix_path_to_point_id ON venuemap.path (to_point_id);
-- convention, not declared: whitelabel.custom_domain.tenant_id -> platform.tenant
CREATE INDEX IF NOT EXISTS ix_custom_domain_tenant_id ON whitelabel.custom_domain (tenant_id);
-- convention, not declared: workforce.announcement.published_by_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS ix_announcement_published_by_principal_id ON workforce.announcement (published_by_principal_id);
-- convention, not declared: workforce.attendance.amended_by_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS ix_attendance_amended_by_principal_id ON workforce.attendance (amended_by_principal_id);
-- convention, not declared: workforce.rota_assignment.required_role_id -> identity.role
CREATE INDEX IF NOT EXISTS ix_rota_assignment_required_role_id ON workforce.rota_assignment (required_role_id);
-- convention, not declared: workforce.shift_swap.from_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS ix_shift_swap_from_principal_id ON workforce.shift_swap (from_principal_id);
-- convention, not declared: workforce.shift_swap.to_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS ix_shift_swap_to_principal_id ON workforce.shift_swap (to_principal_id);
-- convention, not declared: workforce.training_record.principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS ix_training_record_principal_id ON workforce.training_record (principal_id);
-- crosses the database boundary: ai.provider.tenant_id -> control.tenant
CREATE INDEX IF NOT EXISTS ix_provider_tenant_id ON ai.provider (tenant_id);
-- crosses the database boundary: maintenance.work_order.source_plan_id -> control.subscription_plan
CREATE INDEX IF NOT EXISTS ix_work_order_source_plan_id ON maintenance.work_order (source_plan_id);
-- crosses the database boundary: whitelabel.tenant_config.footer -> control.footer_config
CREATE INDEX IF NOT EXISTS ix_tenant_config_footer ON whitelabel.tenant_config (footer);
CREATE INDEX IF NOT EXISTS ix_access_point_scope ON access.access_point (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_admission_rules_scope ON access.admission_rules (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_alert_rule_scope ON reporting.alert_rule (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_alert_scope ON reporting.alert (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_b2b_credit_scope ON orders.b2b_credit (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_blacklist_scope ON access.blacklist (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_challenge_scope ON marketing.challenge (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_config_version_scope ON whitelabel.config_version (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_configuration_profile_scope ON platform.configuration_profile (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_connectivity_policy_scope ON platform.connectivity_policy (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_content_page_scope ON whitelabel.content_page (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_conversation_scope ON ai.conversation (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_corrective_action_scope ON fnb.corrective_action (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_coupon_code_scope ON promotions.coupon_code (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_dead_letter_scope ON platform.dead_letter (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_delegated_access_scope ON identity.delegated_access (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_delegation_scope ON approvals.delegation (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_entitlement_scope ON access.entitlement (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_entitlement_template_scope ON catalogue.entitlement_template (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_event_scope ON catalogue.event (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_faq_category_scope ON whitelabel.faq_category (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_form_definition_scope ON marketing.form_definition (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_fraud_rule_scope ON orders.fraud_rule (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_import_job_scope ON catalogue.import_job (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_interaction_scope ON ai.interaction (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_invitation_campaign_scope ON marketing.invitation_campaign (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_invitation_scope ON marketing.invitation (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_journey_entrant_scope ON marketing.journey_entrant (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_journey_scope ON marketing.journey (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_knowledge_collection_scope ON ai.knowledge_collection (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_layout_draft_scope ON ai.layout_draft (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_legal_entity_scope ON ledger.legal_entity (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_map_scope ON venuemap.map (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_matrix_scope ON approvals.matrix (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_message_trigger_scope ON marketing.message_trigger (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_modifier_group_scope ON fnb.modifier_group (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_offline_policy_scope ON platform.offline_policy (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_outbox_scope ON platform.outbox (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_password_policy_scope ON identity.password_policy (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_payment_link_scope ON orders.payment_link (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_payment_provider_scope ON orders.payment_provider (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_payment_routing_scope ON orders.payment_routing (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_policy_scope ON whitelabel.policy (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_privacy_incident_scope ON marketing.privacy_incident (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_product_category_scope ON catalogue.product_category (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_product_scope ON catalogue.product (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_promo_block_scope ON whitelabel.promo_block (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_provider_scope ON ai.provider (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_purchase_order_scope ON inventory.purchase_order (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_qualification_scope ON resources.qualification (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_quotation_scope ON inventory.quotation (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_reader_profile_scope ON games.reader_profile (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_referral_scope ON marketing.referral (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_report_definition_scope ON reporting.report_definition (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_request_scope ON approvals.request (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_resale_listing_scope ON orders.resale_listing (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_resource_scope ON resources.resource (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_sales_order_scope ON orders.sales_order (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_scan_event_scope ON access.scan_event (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_seat_block_scope ON seating.seat_block (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_section_scope ON seating.section (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_segregation_rule_scope ON identity.segregation_rule (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_settlement_scope ON ledger.settlement (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_shift_scope ON orders.shift (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_sso_group_mapping_scope ON identity.sso_group_mapping (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_sso_provider_scope ON identity.sso_provider (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_stored_value_authorisation_scope ON orders.stored_value_authorisation (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_suggestion_scope ON ai.suggestion (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_supplier_scope ON inventory.supplier (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_suppression_scope ON marketing.suppression (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_transfer_scope ON inventory.transfer (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_wallet_pass_scope ON orders.wallet_pass (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_workstation_scope ON platform.workstation (scope_path text_pattern_ops);
