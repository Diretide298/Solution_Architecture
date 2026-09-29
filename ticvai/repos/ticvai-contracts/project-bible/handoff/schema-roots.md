# Schema roots — the primary table of each schema, and how the rest derive from it

**Derived by `tools/derive-schema-roots.py`. Do not hand-edit.**

The relationship graph knows every edge and nothing said which table each schema is
*about*. This does. **A root chosen by one number is a root nobody can argue with and
nobody should trust**, so three signals are scored and disagreements are stated:

| Signal | What it means |
|---|---|
| **Own** | tables inside this schema that point at it |
| **Reach** | tables anywhere in the package that point at it |
| **Out** | tables it points at — a root points at few, a leaf at many |

Ambient edges are excluded throughout: a lineage coupling is two tables written by one
operation, which is a fact about the code rather than about the data.


## The spine — where dependencies actually stop

**Following every table's own outbound keys to a fixed point gives 42 terminal
tables**, and the distribution is the honest shape of the package:

| Terminal table | Tables that reach it |
|---|---:|
| `platform.scope` | 840 |
| `identity.role` | 684 |
| `ledger.legal_entity` | 314 |
| `platform.configuration_profile` | 214 |
| `access.admission_rules` | 209 |
| `reporting.site_normalisation_basis` | 190 |
| `catalogue.variant` | 153 |
| `embedded as window_starts_at and window_ends_at on orders.cart_line and orders.order_line` | 54 |
| `embedded as attributes (jsonb) on orders.cart_line and orders.order_line` | 54 |
| `ai.decision_record` | 31 |

`platform.scope` is reached by 289 of 353 — **the tenancy spine, and almost
everything hangs off it.** `identity.role` at 207 is the authorisation spine.

**A first pass walked the other way** — asking who points *at* a root — and left 222
tables reaching nothing, including `identity.role` itself, because `principal` points
at `role` rather than the reverse. **The direction was the bug, not the data.**

## `marketing` — 132 tables

**Root: `marketing.guest_profile`**  ·  own 1 · reach 1 · out 5

> **Overridden.** The arithmetic picks `marketing.case`. **`campaign` scores higher and a campaign is something done *to* a guest.** The schema is a CRM: the profile is what persists and campaigns come and go.

- **1 step from the root** — `guest_match_decision`

- **Reaches the root through nothing** — `agent_availability`, `agent_service_profile`, `attribution_touch`, `audience_activation`, `audience_list`, `badge`, `booking_consent_record`, `business_event`, `campaign`, `campaign_target`, `campaign_variant`, `case`, `case_category`, `case_compensation_request`, `case_escalation`, `case_internal_request`, `case_linked_record`, `case_message`, `case_resolution`, `case_routing_rule`, `case_service_action`, `challenge`, `challenge_progress`, `communication_policy_decision`, `communication_preference_type`, `communication_provider`, `communication_routing_rule`, `consent_capture_point`, `consent_propagation`, `consent_purpose`, `consent_purpose_channel`, `consent_question`, `consent_question_version`, `consent_record`, `consent_record_channel`, `contact_automation`, `conversation`, `conversation_message`, `conversation_message_attachment`, `cookie_banner_design`, `cookie_scan_policy`, `cookie_scan_run`, `customer_badge`, `device_consent`, `device_consent_category`, `duplicate_candidate`, `feedback_classification`, `form_definition`, `form_definition_field`, `form_submission`, `guest_attribute_model`, `guest_device`, `guest_document`, `guest_extra_field`, `guest_extra_option`, `guest_extra_value`, `guest_match_policy`, `guest_note`, `guest_preference`, `guest_relationship`, `identity_rules`, `invitation`, `invitation_campaign`, `journey`, `journey_enrollment`, `journey_step`, `kiosk_assist_session`, `legal_hold`, `lost_item`, `loyalty_campaign`, `loyalty_points`, `loyalty_position`, `loyalty_programme`, `loyalty_rule`, `message_delivery`, `message_dispatch`, `message_dispatch_attempt`, `message_template`, `message_template_version`, `message_trigger`, `message_trigger_condition`, `minor_privacy_rule`, `points_earning_rule`, `points_redemption_rule`, `privacy_action`, `privacy_audit_event`, `privacy_change_set`, `privacy_exception`, `privacy_export_package`, `privacy_incident`, `privacy_notice_governance`, `privacy_request`, `privacy_request_deadline`, `privacy_request_type`, `processing_purpose`, `programme_tier`, `quality_evaluation`, `referral`, `retention_policy`, `retention_run`, `review`, `review_response`, `reward`, `reward_assignment`, `segment`, `segment_criterion`, `sender_identity`, `service_copilot_config`, `service_queue`, `sla_policy`, `subscription`, `suppression`, `touch_point`, `tracking_technology`, `waiver_association`, `waiver_exception`, `waiver_field_rule`, `waiver_form_layout`, `waiver_localisation`, `waiver_master`, `waiver_requirement`, `waiver_requirement_event`, `waiver_signatory_rule`, `waiver_signatory_rule (guardian threshold and flag on marketing`, `waiver_signature`, `waiver_trigger_rule`, `waiver_verification`, `waiver_version_control`, `waiver_version_control (checklist, simulation and aiFindings computed at read time)`, `wishlist_item`

  Standalone configuration, or a table whose foreign key is not declared. **Not a defect on its own** — a password policy belongs to a scope rather than to a principal — but it is where an undeclared key hides.

## `orders` — 81 tables

**Root: `orders.sales_order`**  ·  own 21 · reach 60 · out 5

- **1 step from the root** — `after_sale_request`, `credit_override`, `deposit`, `discount`, `external_reference_mapping`, `group_booking`, `membership_migration`, `membership_renewal`, `order_event`, `order_fee`, `order_line`, `order_relationship`, `payment`, `payment_link`, `refund`, `reservation`, `ticket_transfer`, `upgrade`, `visit_reminder`
- **2 steps from the root** — `chargeback`, `group_participant_list`, `group_payment_schedule`, `group_quote`, `group_task`, `group_ticket_allocation`, `group_ticket_fulfillment`, `group_visit_plan`, `order_line_eligibility`, `payment_tip`, `reservation_line`
- **3 steps from the root** — `chargeback_evidence`, `chargeback_investigation_log`, `group_participant`, `group_payment_milestone`, `group_quote_line`, `group_ticket_allocation_line`

- **Reaches the root through nothing** — `after_sale_policy`, `after_sale_policy_window`, `b2b_credit`, `cart`, `cart_line`, `cash_count_line`, `cash_movement`, `deposit_box`, `deposit_box_foreign_holding`, `deposit_box_opening_denomination`, `deposit_policy`, `deposit_policy (dining_* columns)`, `fraud_rule`, `group_customer_organization`, `group_customer_organization_contact`, `group_enquiry`, `invitation`, `invitation_allowance`, `member_exception`, `membership_activation_action`, `no_sale_event`, `order_source_channel`, `payment_allocation_rule`, `pos_shift`, `pos_shift_approval`, `pos_shift_incident`, `refund_batch`, `refund_calculation_policy`, `refund_policy`, `refund_policy_time_band`, `resale_eligibility_rule`, `resale_fee_policy`, `resale_listing`, `resale_marketplace_config`, `resale_recommendation`, `resale_settlement`, `reservation_hold_policy`, `sales_order_unassigned`, `status_transition_rule`, `stored_value_authorisation`, `ticket_template`, `ticket_template_channel`, `upgrade_rule`, `wallet_pass`

  Standalone configuration, or a table whose foreign key is not declared. **Not a defect on its own** — a password policy belongs to a scope rather than to a principal — but it is where an undeclared key hides.

## `catalogue` — 79 tables

**Root: `catalogue.product`**  ·  own 29 · reach 61 · out 9

- **1 step from the root** — `ai_catalogue_session`, `ai_finding`, `alternative_code`, `audit_entry`, `change_request`, `channel_incident`, `channel_sales_rule`, `configuration_template`, `demand_forecast`, `demand_signal`, `dynamic_pricing_strategy`, `group_package`, `lifecycle_action`, `package_pricing`, `price_assignment`, `price_execution`, `pricing_experiment`, `pricing_recommendation`, `pricing_simulation`, `product_channel_assignment`, `product_eligibility_rule`, `product_link`, `product_version`, `rollback_action`, `tax_rule`, `variant`, `variant_dimension`
- **2 steps from the root** — `change_request_line`, `entitlement_template`, `import_job`, `price`, `price_ladder`, `price_list_version`, `pricing_publication`, `pricing_recommendation_decision`, `waitlist_entry`
- **3 steps from the root** — `membership_benefit`, `plan_benefit`, `pricing_publication_target`

- **Reaches the root through nothing** — `approval_policy`, `calculation_profile`, `calculation_step`, `channel_allocation`, `channel_capacity`, `channel_connection`, `channel_sync`, `donation_campaign`, `dynamic_pricing_control`, `event`, `event_capacity_profile`, `event_registration`, `event_reschedule`, `event_resource_plan`, `event_schedule`, `event_type`, `fee`, `fee_rule`, `inventory_hold`, `lifecycle_workflow`, `membership_programme`, `performance`, `performance_media`, `performance_template`, `prepaid_minutes`, `price_category`, `price_list`, `price_resolution_policy`, `pricing_market`, `pricing_test_case`, `product_category`, `product_media`, `published_bundle`, `rate`, `rounding_profile`, `sales_channel`, `signal_registry`, `space`, `tax_profile`

  Standalone configuration, or a table whose foreign key is not declared. **Not a defect on its own** — a password policy belongs to a scope rather than to a principal — but it is where an undeclared key hides.

## `access` — 77 tables

**Root: `access.entitlement`**  ·  own 13 · reach 20 · out 7

> **Overridden.** The arithmetic picks `access.entitlement`. **`access_point` has more inbound edges and the schema is about entitlements.** A gate is equipment; the thing being admitted is the point. `entitlement` also did not exist as a table until 18 August, which is why the arithmetic still favours the gate.

- **1 step from the root** — `biometric_audit_event`, `credential_binding`, `credential_delivery`, `credential_event`, `credential_exception`, `credential_issuance`, `credential_sharing_case`, `device_binding`, `face_reenrolment_attempt`, `scan_event`, `security_alert`, `security_investigation`
- **2 steps from the root** — `identity_lock`

- **Reaches the root through nothing** — `access_area`, `access_attribute`, `access_change`, `access_device`, `access_incident`, `access_map`, `access_point`, `access_point_configuration`, `access_point_group`, `accreditation_credential`, `admission_rules`, `attraction_access`, `biometric_profile`, `blacklist`, `branding_profile`, `companion_rule`, `configuration_change`, `configuration_version`, `consumption_rule`, `credential_event_propagation_rule`, `credential_issuance_retry_policy`, `credential_policy`, `credential_security_profile`, `device_configuration`, `dynamic_field`, `dynamic_policy`, `dynamic_policy_version`, `edge_node`, `edge_package`, `entry_rule_point`, `external_credential_integration`, `fast_pass_profile`, `fraud_rule`, `gate_lane`, `gate_mode_change`, `gate_mode_policy`, `gate_outcome_profile`, `group_admission_rule`, `hardware_deployment`, `hardware_model`, `journey_profile`, `journey_sequence_rule`, `media_binding_rule`, `media_compatibility_test`, `media_encoding_profile`, `media_replacement_policy`, `media_template`, `media_template_version`, `media_type`, `offline_policy`, `operating_calendar_entry`, `parking_entitlement`, `parking_facility`, `podium`, `podium_shift`, `policy_evaluation_setting`, `policy_scope_assignment`, `reason_code`, `risk_scoring_config`, `scan_event_unassigned`, `security_playbook`, `ticket_status_transition`, `verification_method_policy`

  Standalone configuration, or a table whose foreign key is not declared. **Not a defect on its own** — a password policy belongs to a scope rather than to a principal — but it is where an undeclared key hides.

## `control` — 75 tables

**Root: `control.partner`**  ·  own 24 · reach 28 · out 6

- **1 step from the root** — `developer_account`, `partner_agreement`, `partner_allocation`, `partner_application`, `partner_billing_profile`, `partner_booking_limit`, `partner_capability_grant`, `partner_case`, `partner_change_request`, `partner_commercial_exception`, `partner_commission_line`, `partner_commission_rule`, `partner_contact`, `partner_credit_profile`, `partner_distribution_right`, `partner_document`, `partner_rate`, `partner_reconciliation_exception`, `partner_scope_assignment`, `partner_security`, `partner_settlement_batch`, `partner_status_history`, `partner_user`
- **2 steps from the root** — `api_client`, `integration_listing`, `partner_application_review_task`, `partner_commission_rule_tier`, `partner_rate_volume_band`, `sandbox`
- **3 steps from the root** — `api_limit`, `webhook_subscription`
- **4 steps from the root** — `webhook_delivery`

- **Reaches the root through nothing** — `api_licence`, `api_version`, `archival_job`, `backup_run`, `burst_environment`, `cell`, `cell_cluster`, `cell_instance`, `cell_job`, `cell_tenant`, `channel_listing`, `content_block`, `credit_note`, `credit_note_line`, `environment`, `invoice`, `invoice_line`, `licence_add_on`, `licence_add_on_limit`, `migration`, `migration_plan`, `migration_plan_cell`, `migration_run`, `migration_run_cell`, `migration_run_tenant`, `onboarding_application`, `release`, `release_component`, `rollout`, `rollout_cell`, `rollout_tenant`, `scaling_policy`, `seo_metadata`, `support_notice`, `tenant`, `tenant_migration`, `tenant_migration_plan`, `upgrade_schedule`, `url_redirect`, `usage_record`, `venue_type_template`, `waf_rule`

  Standalone configuration, or a table whose foreign key is not declared. **Not a defect on its own** — a password policy belongs to a scope rather than to a principal — but it is where an undeclared key hides.

## `ai` — 69 tables

**Root: `ai.decision_record`**  ·  own 7 · reach 8 · out 0

- **1 step from the root** — `activity`, `approval_request_score`, `forecast_version`, `guided_choice_suggestion`, `insight`, `intervention`, `risk_assessment`
- **2 steps from the root** — `forecast_accuracy`, `forecast_export`, `forecast_point`, `forecast_scenario`, `operational_requirement`, `proposed_action`, `risk_alert`
- **3 steps from the root** — `action_plan`, `message`
- **4 steps from the root** — `action_step`, `answer_feedback`, `case_action`, `config_session`
- **5 steps from the root** — `blueprint`, `config_source`
- **6 steps from the root** — `blueprint_decision`

- **Reaches the root through nothing** — `anomaly_detector`, `assistant_profile`, `byok_enablement`, `capability`, `case_evidence`, `chunk_embedding`, `chunk_ref`, `control`, `control_test`, `conversation`, `entity_risk`, `eval_run`, `eval_suite`, `evidence_package`, `forecast_definition`, `governance_alert`, `governance_policy`, `governance_policy_version`, `incident`, `index_entry`, `index_failure`, `index_job`, `index_source`, `knowledge_collection`, `knowledge_document`, `knowledge_gap`, `layout_draft`, `model`, `policy`, `policy_exception`, `prompt_template`, `provider`, `rec_decision`, `rec_decline`, `rec_event`, `release`, `risk_case`, `risk_edge`, `risk_register`, `risk_strategy`, `signal_observation`, `signal_source`, `suggestion`, `suggestion_outcome`, `tool`

  Standalone configuration, or a table whose foreign key is not declared. **Not a defect on its own** — a password policy belongs to a scope rather than to a principal — but it is where an undeclared key hides.

## `fnb` — 50 tables

**Root: `fnb.service_order`**  ·  own 3 · reach 3 · out 4

> **Overridden.** The arithmetic picks `fnb.table_visit`. **`table_visit` scores higher and not every F&B order has a table** — a kiosk order, a lounger delivery and a collection order have none. The order is the constant.

- **1 step from the root** — `kitchen_ticket`, `order_fulfilment`, `service_order_line`
- **2 steps from the root** — `kitchen_exception`, `kitchen_ticket_line`

- **Reaches the root through nothing** — `allergen_verdict`, `bill_split`, `cold_chain_event`, `combo`, `combo_slot`, `corrective_action`, `course_rule`, `delivery_location`, `delivery_location_outlet`, `delivery_policy`, `dining_table`, `guest_note`, `ingredient_substitute`, `kitchen_station`, `location_session`, `menu`, `menu_item`, `menu_item_modifier`, `menu_schedule`, `menu_section`, `menu_version`, `modifier_group`, `modifier_option`, `outlet_template`, `product_recommendation`, `production_plan`, `production_plan_line`, `production_run`, `recipe`, `recipe_ingredient`, `reservation_policy`, `reservation_table`, `service_charge_policy`, `sold_out_item`, `sub_bill`, `substitution_rule`, `table_combination`, `table_reservation`, `table_reservation (deposit_* columns; the money itself is orders`, `table_session`, `table_visit`, `temperature_checkpoint`, `temperature_log`, `waitlist_entry`

  Standalone configuration, or a table whose foreign key is not declared. **Not a defect on its own** — a password policy belongs to a scope rather than to a principal — but it is where an undeclared key hides.

## `identity` — 33 tables

**Root: `identity.principal`**  ·  own 24 · reach 354 · out 2

- **1 step from the root** — `access_decision`, `access_override`, `access_review_campaign`, `access_review_item`, `authz_audit`, `delegated_access`, `guest_identity_verification`, `membership_history`, `mfa_challenge`, `mfa_method`, `mfa_recovery_code`, `module_access`, `platform_staff_grant`, `principal_credential`, `refresh_token`, `role_permission`, `session`

- **Reaches the root through nothing** — `access_policy`, `access_policy_version`, `benefit_usage`, `capability_template`, `customer_membership`, `guest_session`, `guest_verification_policy`, `module`, `otp_challenge`, `password_policy`, `permission`, `role`, `segregation_rule`, `sso_group_mapping`, `sso_provider`

  Standalone configuration, or a table whose foreign key is not declared. **Not a defect on its own** — a password policy belongs to a scope rather than to a principal — but it is where an undeclared key hides.

## `payments` — 32 tables

**Root: `payments.provider_connection`**  ·  own 6 · reach 6 · out 1

- **1 step from the root** — `payment_attempt`, `provider_cost`, `reconciliation_source`, `terminal`, `terminal_certification_level3`

- **Reaches the root through nothing** — `authentication_policy`, `chargeback_evidence`, `credit_account`, `currency_rule`, `deposit_activity`, `dunning_case`, `dunning_policy`, `eligibility_rule`, `failover_policy`, `fee_rule`, `hosted_checkout`, `instalment`, `instalment_plan`, `instalment_policy`, `matching_rules`, `merchant_account`, `method`, `method_config`, `mixed_tender_rules`, `payment_terms`, `provider`, `risk_rules`, `routing_rule`, `stored_forward`, `terminal_certification`, `token`

  Standalone configuration, or a table whose foreign key is not declared. **Not a defect on its own** — a password policy belongs to a scope rather than to a principal — but it is where an undeclared key hides.

## `wallet` — 31 tables

**Root: `wallet.wallet`**  ·  own 10 · reach 10 · out 1

- **1 step from the root** — `adjustment`, `auto_reload_setting`, `balance`, `credential`, `credit_lot`, `dispute`, `exit_settlement`, `hold`, `restriction`, `shared_wallet`

- **Reaches the root through nothing** — `accounting_mapping`, `authentication_policy`, `channel_rules`, `configuration_version`, `configuration_version_snapshot`, `consumption_policy`, `credit_eligibility`, `credit_type`, `funding_rules`, `gift_card`, `gift_card_product`, `integration_mapping`, `reconciliation_source`, `refund_policy`, `risk_rules`, `shared_wallet_member`, `transfer_rules`, `voucher_type`, `wallet_transaction`, `wallet_type`

  Standalone configuration, or a table whose foreign key is not declared. **Not a defect on its own** — a password policy belongs to a scope rather than to a principal — but it is where an undeclared key hides.

## `promotions` — 30 tables

**Root: `promotions.promotion`**  ·  own 5 · reach 9 · out 2

> **Overridden.** The arithmetic picks `promotions.campaign`. **`bundle` scores higher because bundle lines point at it.** A bundle is one kind of promotion, not the thing promotions are about.

- **1 step from the root** — `promotion_alert`, `promotion_audit`, `promotion_channel_publication`, `promotion_rule`, `promotion_variant`

- **Reaches the root through nothing** — `allocation_component`, `allocation_split`, `bundle`, `bundle_capacity_policy`, `bundle_choice_group`, `bundle_choice_option`, `bundle_component`, `campaign`, `campaign_budget`, `coupon_campaign`, `coupon_code`, `coupon_code_batch`, `partner_bundle_product`, `product_relationship`, `promotion_conflict`, `promotion_evaluation_trace`, `recommendation_experiment`, `recommendation_outcome`, `recommendation_strategy`, `recommendation_suppression`, `stacking_rule`, `upsell_rule`, `voucher`, `voucher_batch`

  Standalone configuration, or a table whose foreign key is not declared. **Not a defect on its own** — a password policy belongs to a scope rather than to a principal — but it is where an undeclared key hides.

## `approvals` — 30 tables

**Root: `approvals.request`**  ·  own 9 · reach 50 · out 1

- **1 step from the root** — `accreditation_badge`, `approved_action_execution`, `decision`, `decision_record`, `escalation`, `external_dispatch`, `signature`, `workflow_step_execution`, `workflow_version`
- **2 steps from the root** — `automation_execution`, `workflow_definition`, `workflow_exception`, `workflow_instance`, `workflow_intervention`
- **3 steps from the root** — `automation`, `workflow_trigger`

- **Reaches the root through nothing** — `approver_availability`, `business_rule`, `control_policy`, `decision_table`, `decision_table_row`, `delegation`, `evidence_package`, `external_provider`, `matrix`, `retention_policy`, `rule`, `sla_policy`, `step_up_policy`

  Standalone configuration, or a table whose foreign key is not declared. **Not a defect on its own** — a password policy belongs to a scope rather than to a principal — but it is where an undeclared key hides.

## `workforce` — 28 tables

**Root: `workforce.employee`**  ·  own 5 · reach 5 · out 3

- **1 step from the root** — `employment`, `leave_balance`, `sync_conflict`, `work_assignment`

- **Reaches the root through nothing** — `announcement`, `announcement_receipt`, `attendance`, `attendance_amendment`, `field_ownership`, `forecast_requirement`, `integration_source`, `job_title`, `labour_budget`, `leave_request`, `leave_type`, `open_shift`, `position_requirement`, `rota_assignment`, `shift`, `shift_swap`, `shift_template`, `staff_conversation`, `staff_conversation_participant`, `staff_message`, `staffing_rules`, `sync_run`, `training_record`

  Standalone configuration, or a table whose foreign key is not declared. **Not a defect on its own** — a password policy belongs to a scope rather than to a principal — but it is where an undeclared key hides.

## `ledger` — 27 tables

**Root: `ledger.account`**  ·  own 11 · reach 17 · out 1

- **1 step from the root** — `account_mapping`, `deposit`, `journal_line`, `posting`, `recognition_schedule`, `tax_code`, `tax_invoice`
- **2 steps from the root** — `credit_memo`, `tax_exemption`, `tax_invoice_line`
- **3 steps from the root** — `credit_memo_line`

- **Reaches the root through nothing** — `cost_center`, `einvoice_transmission`, `einvoicing_provider`, `event_budget`, `fiscal_period`, `fiscal_period_event`, `fx_provider_assignment`, `fx_rate`, `inter_entity_obligation`, `journal_entry`, `legal_entity`, `price_variance`, `settlement`, `settlement_exception`, `tax_invoice_template`

  Standalone configuration, or a table whose foreign key is not declared. **Not a defect on its own** — a password policy belongs to a scope rather than to a principal — but it is where an undeclared key hides.

## `platform` — 26 tables

**Root: `platform.scope`**  ·  own 12 · reach 196 · out 0

- **1 step from the root** — `audit_record`, `cross_region_entitlement`, `outlet`, `region_settings`, `sale_board`, `tenant`, `venue_settings`, `workstation`
- **2 steps from the root** — `device`, `sale_board_page`
- **3 steps from the root** — `device_heartbeat`, `sale_board_tile`

- **Reaches the root through nothing** — `audit_read`, `cell_endpoint`, `configuration_profile`, `connectivity_policy`, `dead_letter`, `denomination`, `dsar_request`, `guest_link`, `offline_policy`, `outbox`, `profile_deployment`, `schema_version`, `wallet_authorisation`

  Standalone configuration, or a table whose foreign key is not declared. **Not a defect on its own** — a password policy belongs to a scope rather than to a principal — but it is where an undeclared key hides.

## `rental` — 24 tables

**Root: `rental.product`**  ·  own 6 · reach 6 · out 5

- **1 step from the root** — `blackout`, `booking`, `deposit_policy`, `fee_policy`, `pricing_profile`, `quote`
- **2 steps from the root** — `incident`, `override`, `settlement`

- **Reaches the root through nothing** — `agreement`, `agreement_item`, `agreement_rules`, `agreement_signature`, `availability_rules`, `damage_assessment`, `duration_rules`, `equipment_assignment`, `inspection`, `inspection_item`, `inventory_model`, `location_rule`, `operational_rules`, `participant`

  Standalone configuration, or a table whose foreign key is not declared. **Not a defect on its own** — a password policy belongs to a scope rather than to a principal — but it is where an undeclared key hides.

## `reporting` — 24 tables

**Root: `reporting.report_definition`**  ·  own 9 · reach 9 · out 1

- **1 step from the root** — `dashboard_tile`, `delivery`, `execution`, `report_column`, `report_field`, `report_filter`, `report_parameter`, `schedule`, `subscription`
- **2 steps from the root** — `export`, `schedule_recipient`

- **Reaches the root through nothing** — `alert`, `alert_rule`, `anomaly`, `dashboard`, `dashboard_view`, `kpi_definition`, `kpi_target`, `natural_language_query`, `pipeline`, `report_definition_version`, `semantic_model`, `site_normalisation_basis`

  Standalone configuration, or a table whose foreign key is not declared. **Not a defect on its own** — a password policy belongs to a scope rather than to a principal — but it is where an undeclared key hides.

## `games` — 23 tables

**Root: `games.game`**  ·  own 6 · reach 6 · out 3

- **1 step from the root** — `gameplay_transaction`, `operational_config`, `play`, `pricing`, `pricing_exception`, `reader`
- **2 steps from the root** — `reader_deployment`, `reader_sync_status`

- **Reaches the root through nothing** — `attraction_type`, `authorisation`, `card`, `card_expiry_rules`, `credit_ledger`, `entitlement`, `kiosk_config`, `prize`, `prize_cost`, `reader_profile`, `redemption`, `redemption_line`, `redemption_rules`, `validation_rules`

  Standalone configuration, or a table whose foreign key is not declared. **Not a defect on its own** — a password policy belongs to a scope rather than to a principal — but it is where an undeclared key hides.

## `subscription` — 23 tables

**Root: `subscription.membership_product`**  ·  own 6 · reach 6 · out 2

- **1 step from the root** — `membership_eligibility_rule`, `membership_entitlement`, `membership_household_policy`, `membership_product_history`, `membership_renewal_policy`, `membership_usage_policy`
- **2 steps from the root** — `membership_household_policy_role_limit`

- **Reaches the root through nothing** — `capacity_pack`, `contract`, `enforcement_policy`, `go_live_readiness`, `licensing_model`, `module_listing`, `partner_quote`, `plan`, `plan_limit`, `plan_module`, `tier_allowance`, `tier_module`, `trial_config`, `vsi_assessment`, `vsi_model`

  Standalone configuration, or a table whose foreign key is not declared. **Not a defect on its own** — a password policy belongs to a scope rather than to a principal — but it is where an undeclared key hides.

## `seating` — 22 tables

**Root: `seating.seat_map`**  ·  own 7 · reach 10 · out 1

- **1 step from the root** — `accessible`, `import_job`, `recommendation_rules`, `seat`, `seat_rules`, `seating_rules`, `zone`
- **2 steps from the root** — `group_request_participant`, `seat_block_item`, `seat_hold_item`

- **Reaches the root through nothing** — `group_request`, `hold_pool`, `hold_type`, `reassignment`, `seat_block`, `seat_category`, `seat_hold`, `seat_map_template`, `seat_price_band`, `section`, `section_row`

  Standalone configuration, or a table whose foreign key is not declared. **Not a defect on its own** — a password policy belongs to a scope rather than to a principal — but it is where an undeclared key hides.

## `inventory` — 22 tables

**Root: `inventory.item`**  ·  own 13 · reach 20 · out 2

- **1 step from the root** — `count_line`, `goods_receipt_line`, `kit_component`, `movement`, `purchase_order_line`, `quotation_line`, `requisition_line`, `serialised_item`, `stock_batch`, `stock_level`, `stock_reservation`, `transfer_line`

- **Reaches the root through nothing** — `count`, `goods_receipt`, `location`, `purchase_order`, `quotation`, `requisition`, `supplier`, `supplier_contract`, `transfer`

  Standalone configuration, or a table whose foreign key is not declared. **Not a defect on its own** — a password policy belongs to a scope rather than to a principal — but it is where an undeclared key hides.

## `resources` — 20 tables

**Root: `resources.resource`**  ·  own 11 · reach 16 · out 3

- **1 step from the root** — `booking`, `qualification`, `resource_audit`, `resource_block`, `resource_cost`, `resource_dependency`, `resource_relation`, `resource_request`, `resource_requirement`, `resource_schedule`

- **Reaches the root through nothing** — `allocation_policy`, `attribute_definition`, `performance_participant`, `resource_category`, `resource_hold`, `resource_package`, `resource_type`, `selection_policy`, `venue_assignment`

  Standalone configuration, or a table whose foreign key is not declared. **Not a defect on its own** — a password policy belongs to a scope rather than to a principal — but it is where an undeclared key hides.

## `whitelabel` — 20 tables

**Root: `whitelabel.footer_config`**  ·  own 3 · reach 3 · out 0

- **1 step from the root** — `footer_config_column`, `footer_config_social_link`, `tenant_config`
- **2 steps from the root** — `banner`, `feature_toggle`, `module_enablement`

- **Reaches the root through nothing** — `analytics_provider`, `config_version`, `content_page`, `custom_domain`, `faq_category`, `faq_entry`, `guided_choice`, `guided_choice_answer`, `guided_choice_question`, `homepage_section`, `navigation_item`, `policy`, `promo_block`

  Standalone configuration, or a table whose foreign key is not declared. **Not a defect on its own** — a password policy belongs to a scope rather than to a principal — but it is where an undeclared key hides.

## `accreditation` — 16 tables

**Root: `accreditation.holder`**  ·  own 8 · reach 9 · out 3

- **1 step from the root** — `application`, `audit`, `credential`, `document`, `holder_access`, `identity_conflict`, `mobile_credential_delivery`

- **Reaches the root through nothing** — `access_profile`, `badge_template`, `data_export`, `notification_rules`, `print_job`, `programme`, `requirements`, `validity`

  Standalone configuration, or a table whose foreign key is not declared. **Not a defect on its own** — a password policy belongs to a scope rather than to a principal — but it is where an undeclared key hides.

## `maintenance` — 15 tables

**Root: `maintenance.asset`**  ·  own 6 · reach 19 · out 6

- **1 step from the root** — `asset_document`, `asset_status_change`, `incident`, `inspection`, `preventive_plan`, `work_order`
- **2 steps from the root** — `incident_authority_notification`, `incident_investigation_note`, `incident_involved_party`, `inspection_item`, `work_order_attachment`

- **Reaches the root through nothing** — `asset_category`, `inspection_template`, `inspection_template_item`

  Standalone configuration, or a table whose foreign key is not declared. **Not a defect on its own** — a password policy belongs to a scope rather than to a principal — but it is where an undeclared key hides.

## `assets` — 14 tables

**Root: `assets.media_asset`**  ·  own 4 · reach 29 · out 2

- **1 step from the root** — `media_collection`, `media_collection_member`, `media_upload`, `media_usage`

- **Reaches the root through nothing** — `approval`, `asset_version`, `audit`, `distribution_channel`, `media_fingerprint`, `rendition`, `share`, `tag`, `taxonomy`

  Standalone configuration, or a table whose foreign key is not declared. **Not a defect on its own** — a password policy belongs to a scope rather than to a principal — but it is where an undeclared key hides.

## `retail` — 13 tables

**Root: `retail.sale`**  ·  own 5 · reach 5 · out 4

- **1 step from the root** — `exchange`, `return`, `sale_line`, `shop_and_drop`
- **2 steps from the root** — `return_line`, `shop_and_drop_line`

- **Reaches the root through nothing** — `merchandise`, `product_recommendation`, `reservation`, `reservation_line`, `return_policy`, `store_rule`

  Standalone configuration, or a table whose foreign key is not declared. **Not a defect on its own** — a password policy belongs to a scope rather than to a principal — but it is where an undeclared key hides.

## `transport` — 12 tables

**Root: `transport.station`**  ·  own 5 · reach 5 · out 1

- **1 step from the root** — `fare_matrix_cell`, `favourite_route`, `route_stop`

- **Reaches the root through nothing** — `departure`, `fare_passenger_type`, `fare_table`, `network_import`, `pass_type`, `route`, `timetable`, `timetable_run`

  Standalone configuration, or a table whose foreign key is not declared. **Not a defect on its own** — a password policy belongs to a scope rather than to a principal — but it is where an undeclared key hides.

## `tenancy` — 8 tables

**Root: `tenancy.device_firmware`**  ·  own 1 · reach 1 · out 1

- **1 step from the root** — `device_rollout`

- **Reaches the root through nothing** — `data_retention_setting`, `device_assignment`, `device_audit`, `device_credential`, `device_tamper_event`, `device_telemetry`

  Standalone configuration, or a table whose foreign key is not declared. **Not a defect on its own** — a password policy belongs to a scope rather than to a principal — but it is where an undeclared key hides.

## `venuemap` — 6 tables

**Root: `venuemap.map`**  ·  own 5 · reach 7 · out 2

- **1 step from the root** — `import_job`, `map_version`, `path`, `placed_resource`, `point`

## `pii` — 5 tables

**Root: `pii.subject`**  ·  own 4 · reach 98 · out 1

- **1 step from the root** — `subject_biometric`, `subject_contact`, `subject_document`

- **Reaches the root through nothing** — `consent_identifier`

  Standalone configuration, or a table whose foreign key is not declared. **Not a defect on its own** — a password policy belongs to a scope rather than to a principal — but it is where an undeclared key hides.

## `queue` — 5 tables

**Root: `queue.queue`**  ·  own 6 · reach 6 · out 6

- **1 step from the root** — `entry`, `feed`, `queue_operating_window`, `reading`

## `pricing` — 3 tables

**Root: `pricing.dynamic_price_rule`**  ·  own 2 · reach 2 · out 3

- **1 step from the root** — `dynamic_price_action`, `dynamic_price_condition`

## `sync` — 3 tables

**Root: `sync.rejection`**  ·  own 0 · reach 0 · out 2


- **Reaches the root through nothing** — `cell_connection`, `cross_cell_request`

  Standalone configuration, or a table whose foreign key is not declared. **Not a defect on its own** — a password policy belongs to a scope rather than to a principal — but it is where an undeclared key hides.

## `embedded as window_starts_at and window_ends_at on orders` — 1 tables

**Root: `embedded as window_starts_at and window_ends_at on orders.cart_line and orders.order_line`**  ·  own 0 · reach 3 · out 0


## `embedded as attributes (jsonb) on orders` — 1 tables

**Root: `embedded as attributes (jsonb) on orders.cart_line and orders.order_line`**  ·  own 0 · reach 3 · out 0


