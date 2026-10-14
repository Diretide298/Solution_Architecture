-- V0104 -- tenant database, after r1 (9cec72d) (20261015).
-- **Written by tools/derive-ddl.py in frozen mode. Do not edit after merge; a mistake is a new migration.**
--
-- The baseline under backend/tenant/ is frozen at r1 (9cec72d), so the change to the schema reference
-- since then is written here instead: additive only. Changes that are not additive (drops, renames,
-- type changes) are not generated; they are listed for a person in handoff/migration-review.md.
-- 3 table(s), 271 column(s), 154 index(es), 29 other statement(s), 204 row-level security polic(ies) re-applied.

ALTER TABLE access.access_point ADD COLUMN IF NOT EXISTS direction_effective_at timestamptz;

ALTER TABLE access.access_point ADD COLUMN IF NOT EXISTS direction_change_reason text CONSTRAINT access_point_direction_change_reason_chk CHECK (char_length(direction_change_reason) <= 200);

ALTER TABLE access.configuration_change ADD COLUMN IF NOT EXISTS reason text CONSTRAINT configuration_change_reason_chk CHECK (char_length(reason) <= 200);

ALTER TABLE access.security_alert ADD COLUMN IF NOT EXISTS note text CONSTRAINT security_alert_note_chk CHECK (char_length(note) <= 1000);

ALTER TABLE accreditation.holder ADD COLUMN IF NOT EXISTS status_effective_from timestamptz;

ALTER TABLE accreditation.holder ADD COLUMN IF NOT EXISTS status_review_at date;

ALTER TABLE accreditation.notification_rules ADD COLUMN IF NOT EXISTS rules jsonb;

ALTER TABLE accreditation.print_job ADD COLUMN IF NOT EXISTS failures jsonb;

ALTER TABLE accreditation.programme ADD COLUMN IF NOT EXISTS categories jsonb;

ALTER TABLE accreditation.requirements ADD COLUMN IF NOT EXISTS rows jsonb;

ALTER TABLE ai.approval_request_score ADD COLUMN IF NOT EXISTS signals jsonb;

ALTER TABLE ai.config_source ADD COLUMN IF NOT EXISTS scope_path ltree;

ALTER TABLE ai.decision_record ADD COLUMN IF NOT EXISTS annotations jsonb;

ALTER TABLE ai.forecast_scenario ADD COLUMN IF NOT EXISTS changes jsonb;

ALTER TABLE ai.guided_choice_suggestion ADD COLUMN IF NOT EXISTS questions jsonb;

ALTER TABLE ai.history_import ADD COLUMN IF NOT EXISTS findings jsonb;

ALTER TABLE ai.incident ADD COLUMN IF NOT EXISTS containment jsonb;

ALTER TABLE ai.index_entry ADD COLUMN IF NOT EXISTS record_key text CONSTRAINT index_entry_record_key_chk CHECK (char_length(record_key) <= 200);

ALTER TABLE ai.index_entry ADD COLUMN IF NOT EXISTS subject_id uuid;

ALTER TABLE ai.index_entry ADD COLUMN IF NOT EXISTS content_hash text;

ALTER TABLE ai.index_entry ADD COLUMN IF NOT EXISTS chunk_count integer;

ALTER TABLE ai.index_entry ADD COLUMN IF NOT EXISTS embedding_model text CONSTRAINT index_entry_embedding_model_chk CHECK (char_length(embedding_model) <= 200);

ALTER TABLE ai.index_entry ADD COLUMN IF NOT EXISTS point_ids text[];

ALTER TABLE ai.index_entry ADD COLUMN IF NOT EXISTS indexed_at timestamptz;

ALTER TABLE ai.index_entry ADD COLUMN IF NOT EXISTS last_job_id uuid;

ALTER TABLE ai.model ADD COLUMN IF NOT EXISTS task_fitness jsonb;

ALTER TABLE ai.provider ADD COLUMN IF NOT EXISTS fitness_warnings jsonb;

ALTER TABLE ai.risk_case ADD COLUMN IF NOT EXISTS entities jsonb;

ALTER TABLE ai.risk_strategy ADD COLUMN IF NOT EXISTS outcome_map jsonb;

ALTER TABLE ai.venue_settings ADD COLUMN IF NOT EXISTS opening_hours jsonb;

ALTER TABLE approvals.accreditation_badge ADD COLUMN IF NOT EXISTS scope_path ltree;

ALTER TABLE approvals.decision_record ADD COLUMN IF NOT EXISTS policy_versions jsonb;

ALTER TABLE approvals.escalation ADD COLUMN IF NOT EXISTS escalated_at timestamptz;

ALTER TABLE approvals.escalation ADD COLUMN IF NOT EXISTS reason text;

ALTER TABLE approvals.escalation ADD COLUMN IF NOT EXISTS from_level integer;

ALTER TABLE approvals.escalation ADD COLUMN IF NOT EXISTS to_level integer;

ALTER TABLE approvals.escalation ADD COLUMN IF NOT EXISTS was_automatic boolean;

ALTER TABLE approvals.escalation ADD COLUMN IF NOT EXISTS escalated_by_principal_id uuid;

ALTER TABLE approvals.escalation ADD COLUMN IF NOT EXISTS added_approver_principal_id uuid;

ALTER TABLE approvals.sla_policy ADD COLUMN IF NOT EXISTS reminders jsonb;

ALTER TABLE assets.rendition ADD COLUMN IF NOT EXISTS asset_id uuid;

ALTER TABLE assets.taxonomy ADD COLUMN IF NOT EXISTS categories jsonb;

ALTER TABLE assets.taxonomy ADD COLUMN IF NOT EXISTS fields jsonb;

ALTER TABLE assets.taxonomy ADD COLUMN IF NOT EXISTS keyword_vocabularies jsonb;

ALTER TABLE catalogue.alternative_code ADD COLUMN IF NOT EXISTS scope_path ltree;

ALTER TABLE catalogue.channel_incident ADD COLUMN IF NOT EXISTS resolution_note text CONSTRAINT channel_incident_resolution_note_chk CHECK (char_length(resolution_note) <= 1000);

ALTER TABLE catalogue.donation_campaign ADD COLUMN IF NOT EXISTS fixed_amounts numeric(18,4)[];

ALTER TABLE catalogue.entitlement_template ADD COLUMN IF NOT EXISTS valid_time_windows jsonb;

ALTER TABLE catalogue.event_registration ADD COLUMN IF NOT EXISTS participant_categories jsonb;

ALTER TABLE catalogue.event_resource_plan ADD COLUMN IF NOT EXISTS requirements jsonb;

ALTER TABLE catalogue.event_resource_plan ADD COLUMN IF NOT EXISTS contractors jsonb;

ALTER TABLE catalogue.event_schedule ADD COLUMN IF NOT EXISTS performances jsonb;

ALTER TABLE catalogue.import_job ADD COLUMN IF NOT EXISTS findings jsonb;

ALTER TABLE catalogue.membership_benefit ADD COLUMN IF NOT EXISTS scope_path ltree;

ALTER TABLE catalogue.membership_programme ADD COLUMN IF NOT EXISTS scope_path ltree;

ALTER TABLE catalogue.performance_template ADD COLUMN IF NOT EXISTS bands jsonb;

ALTER TABLE catalogue.product ADD COLUMN IF NOT EXISTS display_tags jsonb;

ALTER TABLE catalogue.variant_dimension ADD COLUMN IF NOT EXISTS values jsonb;

ALTER TABLE fnb.cold_chain_event ADD COLUMN IF NOT EXISTS scope_path ltree;

ALTER TABLE fnb.combo ADD COLUMN IF NOT EXISTS scope_path ltree;

ALTER TABLE fnb.combo_slot ADD COLUMN IF NOT EXISTS scope_path ltree;

ALTER TABLE fnb.dining_table ADD COLUMN IF NOT EXISTS scope_path ltree;

ALTER TABLE fnb.kitchen_exception ADD COLUMN IF NOT EXISTS scope_path ltree;

ALTER TABLE fnb.kitchen_station ADD COLUMN IF NOT EXISTS scope_path ltree;

ALTER TABLE fnb.menu_item ADD COLUMN IF NOT EXISTS unavailable_note text CONSTRAINT menu_item_unavailable_note_chk CHECK (char_length(unavailable_note) <= 500);

ALTER TABLE fnb.production_plan ADD COLUMN IF NOT EXISTS scope_path ltree;

ALTER TABLE fnb.reservation_policy ADD COLUMN IF NOT EXISTS turn_time_bands jsonb;

ALTER TABLE fnb.table_visit ADD COLUMN IF NOT EXISTS note text CONSTRAINT table_visit_note_chk CHECK (char_length(note) <= 500);

ALTER TABLE fnb.temperature_log ADD COLUMN IF NOT EXISTS scope_path ltree;

ALTER TABLE games.authorisation ADD COLUMN IF NOT EXISTS trace jsonb;

ALTER TABLE games.credit_ledger ADD COLUMN IF NOT EXISTS play_id uuid;

ALTER TABLE games.credit_ledger ADD COLUMN IF NOT EXISTS reader_id uuid;

ALTER TABLE games.credit_ledger ADD COLUMN IF NOT EXISTS sequence integer;

ALTER TABLE games.credit_ledger ADD COLUMN IF NOT EXISTS credits_used integer;

ALTER TABLE games.credit_ledger ADD COLUMN IF NOT EXISTS bonus_credits_used integer DEFAULT 0;

ALTER TABLE games.credit_ledger ADD COLUMN IF NOT EXISTS points_awarded integer;

ALTER TABLE games.credit_ledger ADD COLUMN IF NOT EXISTS credits_after integer;

ALTER TABLE games.credit_ledger ADD COLUMN IF NOT EXISTS points_after integer;

ALTER TABLE games.credit_ledger ADD COLUMN IF NOT EXISTS is_divergence boolean;

ALTER TABLE games.credit_ledger ADD COLUMN IF NOT EXISTS reconciled_at timestamptz;

ALTER TABLE games.credit_ledger ADD COLUMN IF NOT EXISTS recorded_at timestamptz;

ALTER TABLE games.credit_ledger ADD COLUMN IF NOT EXISTS synced_at timestamptz;

ALTER TABLE games.operational_config ADD COLUMN IF NOT EXISTS operating_hours jsonb;

ALTER TABLE games.play ADD COLUMN IF NOT EXISTS scope_path ltree;

ALTER TABLE games.pricing ADD COLUMN IF NOT EXISTS group_pricing jsonb;

ALTER TABLE games.pricing ADD COLUMN IF NOT EXISTS peak_pricing jsonb;

ALTER TABLE games.pricing ADD COLUMN IF NOT EXISTS calendar_exceptions jsonb;

ALTER TABLE games.reader_deployment ADD COLUMN IF NOT EXISTS scope_path ltree;

ALTER TABLE games.redemption_rules ADD COLUMN IF NOT EXISTS earn_rules jsonb;

ALTER TABLE identity.access_decision ADD COLUMN IF NOT EXISTS matched_policies jsonb;

ALTER TABLE identity.authorisation_policy ADD COLUMN IF NOT EXISTS status_reason text;

ALTER TABLE identity.benefit_usage ADD COLUMN IF NOT EXISTS recorded_at timestamptz;

ALTER TABLE identity.mfa_challenge ADD COLUMN IF NOT EXISTS method_id uuid;

ALTER TABLE identity.mfa_challenge ADD COLUMN IF NOT EXISTS action text CONSTRAINT mfa_challenge_action_chk CHECK (char_length(action) <= 100);

ALTER TABLE identity.mfa_challenge ADD COLUMN IF NOT EXISTS session_id uuid;

ALTER TABLE identity.mfa_challenge ADD COLUMN IF NOT EXISTS code_hash text;

ALTER TABLE identity.mfa_challenge ADD COLUMN IF NOT EXISTS status text CONSTRAINT mfa_challenge_status_chk CHECK (status IN ('pending', 'verified', 'consumed', 'voided', 'expired'));

ALTER TABLE identity.mfa_challenge ADD COLUMN IF NOT EXISTS failed_attempts integer NOT NULL DEFAULT 0;

ALTER TABLE identity.mfa_challenge ADD COLUMN IF NOT EXISTS expires_at timestamptz;

ALTER TABLE identity.mfa_challenge ADD COLUMN IF NOT EXISTS verified_at timestamptz;

ALTER TABLE identity.mfa_challenge ADD COLUMN IF NOT EXISTS consumed_at timestamptz;

ALTER TABLE identity.mfa_challenge ADD COLUMN IF NOT EXISTS voided_at timestamptz;

ALTER TABLE identity.mfa_recovery_code ADD COLUMN IF NOT EXISTS code_hash text;

ALTER TABLE identity.mfa_recovery_code ADD COLUMN IF NOT EXISTS issued_at timestamptz;

ALTER TABLE identity.mfa_recovery_code ADD COLUMN IF NOT EXISTS used_at timestamptz;

ALTER TABLE identity.otp_challenge ADD COLUMN IF NOT EXISTS identifier_hash text;

ALTER TABLE identity.otp_challenge ADD COLUMN IF NOT EXISTS channel text CONSTRAINT otp_challenge_channel_chk CHECK (channel IN ('whatsapp', 'sms', 'email', 'emailLink'));

ALTER TABLE identity.otp_challenge ADD COLUMN IF NOT EXISTS purpose text CONSTRAINT otp_challenge_purpose_chk CHECK (purpose IN ('login', 'register', 'verify', 'passwordReset', 'stepUp', 'emailVerification'));

ALTER TABLE identity.otp_challenge ADD COLUMN IF NOT EXISTS code_hash text;

ALTER TABLE identity.otp_challenge ADD COLUMN IF NOT EXISTS failed_attempts integer NOT NULL DEFAULT 0;

ALTER TABLE identity.otp_challenge ADD COLUMN IF NOT EXISTS attempt_limit integer;

ALTER TABLE identity.otp_challenge ADD COLUMN IF NOT EXISTS expires_at timestamptz;

ALTER TABLE identity.otp_challenge ADD COLUMN IF NOT EXISTS resend_after timestamptz;

ALTER TABLE identity.otp_challenge ADD COLUMN IF NOT EXISTS consumed_at timestamptz;

ALTER TABLE identity.otp_challenge ADD COLUMN IF NOT EXISTS invalidated_at timestamptz;

ALTER TABLE identity.password_policy ADD COLUMN IF NOT EXISTS pin_length integer DEFAULT 4 CONSTRAINT password_policy_pin_length_chk CHECK (pin_length IN (4, 6, 8));

ALTER TABLE identity.password_policy ADD COLUMN IF NOT EXISTS pin_reuse_prevention text DEFAULT 'last5' CONSTRAINT password_policy_pin_reuse_prevention_chk CHECK (pin_reuse_prevention IN ('none', 'last3', 'last5'));

ALTER TABLE identity.password_policy ADD COLUMN IF NOT EXISTS pin_lockout_after_attempts integer DEFAULT 5 CONSTRAINT password_policy_pin_lockout_after_attempts_chk CHECK (pin_lockout_after_attempts IN (3, 5, 10));

ALTER TABLE identity.principal ADD COLUMN IF NOT EXISTS must_change_credential boolean DEFAULT true;

ALTER TABLE identity.principal ADD COLUMN IF NOT EXISTS sso_provider_id uuid;

ALTER TABLE identity.principal_credential ADD COLUMN IF NOT EXISTS method text CONSTRAINT principal_credential_method_chk CHECK (method IN ('password', 'pin'));

ALTER TABLE identity.principal_credential ADD COLUMN IF NOT EXISTS credential_hash text;

ALTER TABLE identity.principal_credential ADD COLUMN IF NOT EXISTS set_at timestamptz;

ALTER TABLE identity.principal_credential ADD COLUMN IF NOT EXISTS failed_attempts integer NOT NULL DEFAULT 0;

ALTER TABLE identity.principal_credential ADD COLUMN IF NOT EXISTS locked_until timestamptz;

CREATE TABLE IF NOT EXISTS identity.principal_credential_history (
    principal_credential_id           uuid NOT NULL,
    credential_hash                   text NOT NULL,
    replaced_at                       timestamptz NOT NULL,
    id                                uuid PRIMARY KEY NOT NULL
);

CREATE TABLE IF NOT EXISTS identity.subject_holding (
    subject_id                        uuid,
    holding_kind                      text NOT NULL CONSTRAINT subject_holding_holding_kind_chk CHECK (holding_kind IN ('order', 'entitlement')),
    holding_id                        uuid NOT NULL,
    order_id                          uuid,
    order_line_id                     uuid,
    status                            text NOT NULL CONSTRAINT subject_holding_status_chk CHECK (char_length(status) <= 40),
    valid_to                          timestamptz,
    last_event_at                     timestamptz,
    updated_at                        timestamptz NOT NULL,
    id                                uuid PRIMARY KEY NOT NULL
);

ALTER TABLE inventory.supplier ADD COLUMN IF NOT EXISTS contacts jsonb;

ALTER TABLE ledger.event_budget ADD COLUMN IF NOT EXISTS cost_lines jsonb;

ALTER TABLE ledger.journal_entry ADD COLUMN IF NOT EXISTS posting_date date;

ALTER TABLE ledger.recognition_schedule ADD COLUMN IF NOT EXISTS scope_path ltree;

ALTER TABLE ledger.tax_code ADD COLUMN IF NOT EXISTS scope_path ltree;

ALTER TABLE ledger.tax_exemption ADD COLUMN IF NOT EXISTS scope_path ltree;

ALTER TABLE maintenance.priority_scoring_model ADD COLUMN IF NOT EXISTS bands jsonb;

ALTER TABLE maintenance.work_order ADD COLUMN IF NOT EXISTS time_entries jsonb;

ALTER TABLE maintenance.work_order ADD COLUMN IF NOT EXISTS parts jsonb;

ALTER TABLE marketing.badge ADD COLUMN IF NOT EXISTS scope_path ltree;

ALTER TABLE marketing.case_message ADD COLUMN IF NOT EXISTS scope_path ltree;

ALTER TABLE marketing.communication_routing_rule ADD COLUMN IF NOT EXISTS providers jsonb;

ALTER TABLE marketing.consent_capture_point ADD COLUMN IF NOT EXISTS steps jsonb;

ALTER TABLE marketing.cookie_banner_design ADD COLUMN IF NOT EXISTS buttons jsonb;

ALTER TABLE marketing.cookie_banner_design ADD COLUMN IF NOT EXISTS links jsonb;

ALTER TABLE marketing.cookie_banner_design ADD COLUMN IF NOT EXISTS categories jsonb;

ALTER TABLE marketing.duplicate_candidate ADD COLUMN IF NOT EXISTS conflicts jsonb;

ALTER TABLE marketing.guest_attribute_model ADD COLUMN IF NOT EXISTS field_groups jsonb;

ALTER TABLE marketing.guest_attribute_model ADD COLUMN IF NOT EXISTS attributes jsonb;

ALTER TABLE marketing.guest_attribute_model ADD COLUMN IF NOT EXISTS identifiers jsonb;

ALTER TABLE marketing.guest_device ADD COLUMN IF NOT EXISTS installation_id uuid;

ALTER TABLE marketing.guest_extra_option ADD COLUMN IF NOT EXISTS scope_path ltree;

ALTER TABLE marketing.guest_extra_value ADD COLUMN IF NOT EXISTS scope_path ltree;

ALTER TABLE marketing.identity_rules ADD COLUMN IF NOT EXISTS matchers jsonb;

ALTER TABLE marketing.identity_rules ADD COLUMN IF NOT EXISTS survivorship jsonb;

ALTER TABLE marketing.invitation ADD COLUMN IF NOT EXISTS campaign_id uuid;

ALTER TABLE marketing.invitation ADD COLUMN IF NOT EXISTS subject_id uuid;

ALTER TABLE marketing.invitation ADD COLUMN IF NOT EXISTS token text;

ALTER TABLE marketing.invitation ADD COLUMN IF NOT EXISTS plus_ones integer DEFAULT 0;

ALTER TABLE marketing.invitation ADD COLUMN IF NOT EXISTS status text CONSTRAINT invitation_status_chk CHECK (status IN ('issued', 'viewed', 'accepted', 'declined', 'expired', 'revoked'));

ALTER TABLE marketing.invitation ADD COLUMN IF NOT EXISTS responded_at timestamptz;

ALTER TABLE marketing.kiosk_assist_session ADD COLUMN IF NOT EXISTS actions_taken jsonb;

ALTER TABLE marketing.loyalty_campaign ADD COLUMN IF NOT EXISTS scope_path ltree;

ALTER TABLE marketing.loyalty_points ADD COLUMN IF NOT EXISTS scope_path ltree;

ALTER TABLE marketing.points_redemption_rule ADD COLUMN IF NOT EXISTS scope_path ltree;

ALTER TABLE marketing.privacy_action ADD COLUMN IF NOT EXISTS system_results jsonb;

ALTER TABLE marketing.privacy_change_set ADD COLUMN IF NOT EXISTS items jsonb;

ALTER TABLE marketing.privacy_export_package ADD COLUMN IF NOT EXISTS identifiers jsonb;

ALTER TABLE marketing.privacy_export_package ADD COLUMN IF NOT EXISTS results jsonb;

ALTER TABLE marketing.privacy_export_package ADD COLUMN IF NOT EXISTS corrections jsonb;

ALTER TABLE marketing.privacy_request_type ADD COLUMN IF NOT EXISTS stages jsonb;

ALTER TABLE marketing.quality_evaluation ADD COLUMN IF NOT EXISTS criteria jsonb;

ALTER TABLE marketing.quality_evaluation ADD COLUMN IF NOT EXISTS ai_findings jsonb;

ALTER TABLE marketing.quality_evaluation ADD COLUMN IF NOT EXISTS coaching_actions jsonb;

ALTER TABLE marketing.reward ADD COLUMN IF NOT EXISTS scope_path ltree;

ALTER TABLE marketing.waiver_form_layout ADD COLUMN IF NOT EXISTS sections jsonb;

ALTER TABLE marketing.waiver_localisation ADD COLUMN IF NOT EXISTS languages jsonb;

ALTER TABLE marketing.waiver_signatory_rule ADD COLUMN IF NOT EXISTS guardian_threshold_by_country jsonb;

ALTER TABLE marketing.waiver_trigger_rule ADD COLUMN IF NOT EXISTS eligibility jsonb;

ALTER TABLE marketing.waiver_trigger_rule ADD COLUMN IF NOT EXISTS reminders jsonb;

ALTER TABLE marketing.waiver_version_control ADD COLUMN IF NOT EXISTS history jsonb;

ALTER TABLE orders.deposit_box ADD COLUMN IF NOT EXISTS recorded_at timestamptz;

ALTER TABLE orders.group_enquiry ADD COLUMN IF NOT EXISTS scope_path ltree;

ALTER TABLE orders.invitation ADD COLUMN IF NOT EXISTS scope_path ltree;

ALTER TABLE orders.invitation_allowance ADD COLUMN IF NOT EXISTS scope_path ltree;

ALTER TABLE orders.member_exception ADD COLUMN IF NOT EXISTS scope_path ltree;

ALTER TABLE orders.membership_migration ADD COLUMN IF NOT EXISTS scope_path ltree;

ALTER TABLE orders.refund_calculation_policy ADD COLUMN IF NOT EXISTS scope_path ltree;

ALTER TABLE orders.ticket_template ADD COLUMN IF NOT EXISTS scope_path ltree;

ALTER TABLE payments.chargeback_evidence ADD COLUMN IF NOT EXISTS documents jsonb;

ALTER TABLE payments.deposit_activity ADD COLUMN IF NOT EXISTS scope_path ltree;

ALTER TABLE payments.fee_rule ADD COLUMN IF NOT EXISTS scope_path ltree;

ALTER TABLE payments.mixed_tender_rules ADD COLUMN IF NOT EXISTS allowed_combinations jsonb;

ALTER TABLE payments.risk_rules ADD COLUMN IF NOT EXISTS rules jsonb;

ALTER TABLE payments.risk_rules ADD COLUMN IF NOT EXISTS lists jsonb;

ALTER TABLE payments.routing_rule ADD COLUMN IF NOT EXISTS targets jsonb;

ALTER TABLE platform.denomination ADD COLUMN IF NOT EXISTS scope_path ltree;

ALTER TABLE platform.device ADD COLUMN IF NOT EXISTS scope_path ltree;

CREATE TABLE IF NOT EXISTS platform.outlet_opening_hour (
    outlet_id                         uuid NOT NULL,
    day                               text NOT NULL,
    "from"                            text NOT NULL,
    "to"                              text NOT NULL,
    ends_next_day                     boolean,
    id                                uuid PRIMARY KEY NOT NULL
);

ALTER TABLE platform.region_settings ADD COLUMN IF NOT EXISTS scope_path ltree;

ALTER TABLE platform.sale_board_tile ADD COLUMN IF NOT EXISTS position integer;

ALTER TABLE platform.sale_board_tile ADD COLUMN IF NOT EXISTS kind text CONSTRAINT sale_board_tile_kind_chk CHECK (kind IN ('product', 'category', 'action', 'spacer'));

ALTER TABLE platform.sale_board_tile ADD COLUMN IF NOT EXISTS variant_id uuid;

ALTER TABLE platform.sale_board_tile ADD COLUMN IF NOT EXISTS category_id uuid;

ALTER TABLE platform.sale_board_tile ADD COLUMN IF NOT EXISTS action_code text CONSTRAINT sale_board_tile_action_code_chk CHECK (action_code IN ('holdSale', 'recallHeld', 'applyDiscount', 'guestLookup', 'scanMedia', 'reprintReceipt'));

ALTER TABLE platform.sale_board_tile ADD COLUMN IF NOT EXISTS label text;

ALTER TABLE platform.sale_board_tile ADD COLUMN IF NOT EXISTS colour text;

ALTER TABLE platform.sale_board_tile ADD COLUMN IF NOT EXISTS image_asset_ref text;

ALTER TABLE platform.workstation ADD COLUMN IF NOT EXISTS cashier_input_mode text DEFAULT 'hybrid' CONSTRAINT workstation_cashier_input_mode_chk CHECK (cashier_input_mode IN ('keyboard', 'touch', 'scanner', 'hybrid'));

ALTER TABLE platform.workstation ADD COLUMN IF NOT EXISTS guest_display_content text[];

ALTER TABLE promotions.promotion_variant ADD COLUMN IF NOT EXISTS scope_path ltree;

ALTER TABLE promotions.recommendation_experiment ADD COLUMN IF NOT EXISTS variants jsonb;

ALTER TABLE promotions.recommendation_outcome ADD COLUMN IF NOT EXISTS recorded_at timestamptz;

ALTER TABLE promotions.recommendation_suppression ADD COLUMN IF NOT EXISTS hard_exclusions jsonb;

ALTER TABLE promotions.upsell_rule ADD COLUMN IF NOT EXISTS scope_path ltree;

ALTER TABLE rental.agreement_rules ADD COLUMN IF NOT EXISTS product_id uuid;

ALTER TABLE rental.availability_rules ADD COLUMN IF NOT EXISTS operating_windows jsonb;

ALTER TABLE rental.availability_rules ADD COLUMN IF NOT EXISTS product_id uuid;

ALTER TABLE rental.booking ADD COLUMN IF NOT EXISTS change_reason text;

ALTER TABLE rental.damage_assessment ADD COLUMN IF NOT EXISTS booking_id uuid;

ALTER TABLE rental.duration_rules ADD COLUMN IF NOT EXISTS product_id uuid;

ALTER TABLE rental.equipment_assignment ADD COLUMN IF NOT EXISTS booking_id uuid;

ALTER TABLE rental.fee_policy ADD COLUMN IF NOT EXISTS late_fee_tiers jsonb;

ALTER TABLE rental.incident ADD COLUMN IF NOT EXISTS recorded_at timestamptz;

ALTER TABLE rental.inspection ADD COLUMN IF NOT EXISTS checklist jsonb;

ALTER TABLE rental.inspection ADD COLUMN IF NOT EXISTS recorded_at timestamptz;

ALTER TABLE rental.inspection ADD COLUMN IF NOT EXISTS booking_id uuid;

ALTER TABLE rental.inventory_model ADD COLUMN IF NOT EXISTS components jsonb;

ALTER TABLE rental.inventory_model ADD COLUMN IF NOT EXISTS product_id uuid;

ALTER TABLE rental.location_rule ADD COLUMN IF NOT EXISTS product_id uuid;

ALTER TABLE rental.operational_rules ADD COLUMN IF NOT EXISTS product_id uuid;

ALTER TABLE rental.participant ADD COLUMN IF NOT EXISTS scope_path ltree;

ALTER TABLE rental.pricing_profile ADD COLUMN IF NOT EXISTS duration_tiers jsonb;

ALTER TABLE rental.pricing_profile ADD COLUMN IF NOT EXISTS calendar_rules jsonb;

ALTER TABLE reporting.anomaly ADD COLUMN IF NOT EXISTS candidate_causes jsonb;

ALTER TABLE reporting.semantic_model ADD COLUMN IF NOT EXISTS domains jsonb;

ALTER TABLE reporting.semantic_model ADD COLUMN IF NOT EXISTS relationships jsonb;

ALTER TABLE reporting.subscription ADD COLUMN IF NOT EXISTS recipients jsonb;

ALTER TABLE resources.booking ADD COLUMN IF NOT EXISTS change_reason text;

ALTER TABLE resources.resource ADD COLUMN IF NOT EXISTS lifecycle_state text;

ALTER TABLE resources.resource ADD COLUMN IF NOT EXISTS lifecycle_effective_from timestamptz;

ALTER TABLE resources.resource ADD COLUMN IF NOT EXISTS lifecycle_reason text;

ALTER TABLE resources.resource ADD COLUMN IF NOT EXISTS replacement_resource_id uuid;

ALTER TABLE resources.resource ADD COLUMN IF NOT EXISTS disposal jsonb;

ALTER TABLE resources.resource_schedule ADD COLUMN IF NOT EXISTS windows jsonb;

ALTER TABLE resources.resource_schedule ADD COLUMN IF NOT EXISTS exceptions jsonb;

ALTER TABLE resources.venue_assignment ADD COLUMN IF NOT EXISTS resource_id uuid;

ALTER TABLE seating.accessible ADD COLUMN IF NOT EXISTS spaces jsonb;

ALTER TABLE seating.seat ADD COLUMN IF NOT EXISTS scope_path ltree;

ALTER TABLE seating.seat_price_band ADD COLUMN IF NOT EXISTS scope_path ltree;

ALTER TABLE seating.section ADD COLUMN IF NOT EXISTS boundary jsonb;

ALTER TABLE subscription.enforcement_policy ADD COLUMN IF NOT EXISTS thresholds jsonb;

ALTER TABLE subscription.go_live_readiness ADD COLUMN IF NOT EXISTS groups jsonb;

ALTER TABLE subscription.licensing_model ADD COLUMN IF NOT EXISTS overage_pricing jsonb;

ALTER TABLE subscription.vsi_model ADD COLUMN IF NOT EXISTS factors jsonb;

ALTER TABLE subscription.vsi_model ADD COLUMN IF NOT EXISTS tiers jsonb;

ALTER TABLE tenancy.device_rollout ADD COLUMN IF NOT EXISTS waves jsonb;

ALTER TABLE tenancy.device_tamper_event ADD COLUMN IF NOT EXISTS recorded_at timestamptz;

ALTER TABLE transport.network_import ADD COLUMN IF NOT EXISTS findings jsonb;

ALTER TABLE transport.route ADD COLUMN IF NOT EXISTS status_reason text CONSTRAINT route_status_reason_chk CHECK (char_length(status_reason) <= 500);

ALTER TABLE venuemap.import_job ADD COLUMN IF NOT EXISTS scope_path ltree;

ALTER TABLE venuemap.import_job ADD COLUMN IF NOT EXISTS findings jsonb;

ALTER TABLE venuemap.path ADD COLUMN IF NOT EXISTS is_closed boolean DEFAULT false;

ALTER TABLE venuemap.path ADD COLUMN IF NOT EXISTS expected_reopen_at timestamptz;

ALTER TABLE venuemap.path ADD COLUMN IF NOT EXISTS closed_note text CONSTRAINT path_closed_note_chk CHECK (char_length(closed_note) <= 500);

ALTER TABLE venuemap.placed_resource ADD COLUMN IF NOT EXISTS boundary jsonb;

ALTER TABLE venuemap.point ADD COLUMN IF NOT EXISTS media jsonb;

ALTER TABLE venuemap.visit_plan ADD COLUMN IF NOT EXISTS excluded jsonb;

ALTER TABLE wallet.accounting_mapping ADD COLUMN IF NOT EXISTS mappings jsonb;

ALTER TABLE wallet.authentication_policy ADD COLUMN IF NOT EXISTS tiers jsonb;

ALTER TABLE wallet.configuration_version ADD COLUMN IF NOT EXISTS findings jsonb;

ALTER TABLE wallet.credential ADD COLUMN IF NOT EXISTS recorded_at timestamptz;

ALTER TABLE wallet.gift_card_product ADD COLUMN IF NOT EXISTS denominations numeric(18,4)[];

ALTER TABLE wallet.reconciliation_source ADD COLUMN IF NOT EXISTS sources jsonb;

ALTER TABLE whitelabel.booking_flow_step ADD COLUMN IF NOT EXISTS scope_path ltree;

ALTER TABLE whitelabel.config_version ADD COLUMN IF NOT EXISTS pending_build_time_changes jsonb;

ALTER TABLE workforce.shift_template ADD COLUMN IF NOT EXISTS breaks jsonb;

ALTER TABLE ai.index_entry ADD CONSTRAINT index_entry_last_job_id_fkey FOREIGN KEY (last_job_id) REFERENCES ai.index_job(id);

ALTER TABLE assets.rendition ADD CONSTRAINT rendition_asset_id_fkey FOREIGN KEY (asset_id) REFERENCES assets.media_asset(id);

ALTER TABLE identity.principal ADD CONSTRAINT principal_sso_provider_id_fkey FOREIGN KEY (sso_provider_id) REFERENCES identity.sso_provider(id);

ALTER TABLE identity.principal_credential_history ADD CONSTRAINT principal_credential_history_principal_credential_id_fkey FOREIGN KEY (principal_credential_id) REFERENCES identity.principal_credential(id);

ALTER TABLE identity.subject_holding ADD CONSTRAINT subject_holding_subject_id_fkey FOREIGN KEY (subject_id) REFERENCES pii.subject(id);

ALTER TABLE marketing.invitation ADD CONSTRAINT invitation_campaign_id_fkey FOREIGN KEY (campaign_id) REFERENCES marketing.invitation_campaign(id);

ALTER TABLE platform.outlet_opening_hour ADD CONSTRAINT outlet_opening_hour_outlet_id_fkey FOREIGN KEY (outlet_id) REFERENCES platform.outlet(id);

ALTER TABLE rental.agreement_rules ADD CONSTRAINT agreement_rules_product_id_fkey FOREIGN KEY (product_id) REFERENCES rental.product(id);

ALTER TABLE rental.availability_rules ADD CONSTRAINT availability_rules_product_id_fkey FOREIGN KEY (product_id) REFERENCES rental.product(id);

ALTER TABLE rental.damage_assessment ADD CONSTRAINT damage_assessment_booking_id_fkey FOREIGN KEY (booking_id) REFERENCES rental.booking(id);

ALTER TABLE rental.duration_rules ADD CONSTRAINT duration_rules_product_id_fkey FOREIGN KEY (product_id) REFERENCES rental.product(id);

ALTER TABLE rental.equipment_assignment ADD CONSTRAINT equipment_assignment_booking_id_fkey FOREIGN KEY (booking_id) REFERENCES rental.booking(id);

ALTER TABLE rental.inspection ADD CONSTRAINT inspection_booking_id_fkey FOREIGN KEY (booking_id) REFERENCES rental.booking(id);

ALTER TABLE rental.inventory_model ADD CONSTRAINT inventory_model_product_id_fkey FOREIGN KEY (product_id) REFERENCES rental.product(id);

ALTER TABLE rental.location_rule ADD CONSTRAINT location_rule_product_id_fkey FOREIGN KEY (product_id) REFERENCES rental.product(id);

ALTER TABLE rental.operational_rules ADD CONSTRAINT operational_rules_product_id_fkey FOREIGN KEY (product_id) REFERENCES rental.product(id);

ALTER TABLE resources.resource ADD CONSTRAINT resource_replacement_resource_id_fkey FOREIGN KEY (replacement_resource_id) REFERENCES resources.resource(id);

ALTER TABLE resources.venue_assignment ADD CONSTRAINT venue_assignment_resource_id_fkey FOREIGN KEY (resource_id) REFERENCES resources.resource(id);

CREATE INDEX IF NOT EXISTS escalation_added_approver_principal_id_idx ON approvals.escalation (added_approver_principal_id);

CREATE INDEX IF NOT EXISTS escalation_escalated_by_principal_id_idx ON approvals.escalation (escalated_by_principal_id);

CREATE INDEX IF NOT EXISTS mfa_challenge_method_id_idx ON identity.mfa_challenge (method_id);

CREATE INDEX IF NOT EXISTS mfa_challenge_session_id_idx ON identity.mfa_challenge (session_id);

CREATE INDEX IF NOT EXISTS subject_holding_order_line_id_idx ON identity.subject_holding (order_line_id);

CREATE INDEX IF NOT EXISTS invitation_subject_id_idx ON marketing.invitation (subject_id);

CREATE INDEX IF NOT EXISTS sale_board_tile_variant_id_idx ON platform.sale_board_tile (variant_id);

CREATE INDEX IF NOT EXISTS index_entry_last_job_id_idx ON ai.index_entry (last_job_id);

CREATE INDEX IF NOT EXISTS rendition_asset_id_idx ON assets.rendition (asset_id);

CREATE INDEX IF NOT EXISTS principal_sso_provider_id_idx ON identity.principal (sso_provider_id);

CREATE INDEX IF NOT EXISTS principal_credential_history_principal_credential_id_idx ON identity.principal_credential_history (principal_credential_id);

CREATE INDEX IF NOT EXISTS subject_holding_subject_id_idx ON identity.subject_holding (subject_id);

CREATE INDEX IF NOT EXISTS invitation_campaign_id_idx ON marketing.invitation (campaign_id);

CREATE INDEX IF NOT EXISTS kiosk_assist_session_device_id_idx ON marketing.kiosk_assist_session (device_id);

CREATE INDEX IF NOT EXISTS outlet_opening_hour_outlet_id_idx ON platform.outlet_opening_hour (outlet_id);

CREATE INDEX IF NOT EXISTS entry_priority_tier_id_idx ON queue.entry (priority_tier_id);

CREATE INDEX IF NOT EXISTS agreement_rules_product_id_idx ON rental.agreement_rules (product_id);

CREATE INDEX IF NOT EXISTS availability_rules_product_id_idx ON rental.availability_rules (product_id);

CREATE INDEX IF NOT EXISTS damage_assessment_booking_id_idx ON rental.damage_assessment (booking_id);

CREATE INDEX IF NOT EXISTS duration_rules_product_id_idx ON rental.duration_rules (product_id);

CREATE INDEX IF NOT EXISTS equipment_assignment_booking_id_idx ON rental.equipment_assignment (booking_id);

CREATE INDEX IF NOT EXISTS inspection_booking_id_idx ON rental.inspection (booking_id);

CREATE INDEX IF NOT EXISTS inventory_model_product_id_idx ON rental.inventory_model (product_id);

CREATE INDEX IF NOT EXISTS location_rule_product_id_idx ON rental.location_rule (product_id);

CREATE INDEX IF NOT EXISTS operational_rules_product_id_idx ON rental.operational_rules (product_id);

CREATE INDEX IF NOT EXISTS resource_replacement_resource_id_idx ON resources.resource (replacement_resource_id);

CREATE INDEX IF NOT EXISTS venue_assignment_resource_id_idx ON resources.venue_assignment (resource_id);

CREATE UNIQUE INDEX IF NOT EXISTS admission_rules_code_uniq ON access.admission_rules (lower(code));

CREATE UNIQUE INDEX IF NOT EXISTS reason_code_code_uniq ON access.reason_code (lower(code));

CREATE UNIQUE INDEX IF NOT EXISTS programme_code_uniq ON accreditation.programme (lower(code));

DROP INDEX IF EXISTS approvals.external_provider_code_uniq;

CREATE UNIQUE INDEX IF NOT EXISTS external_provider_code_uniq ON approvals.external_provider (lower(code));

DROP INDEX IF EXISTS assets.media_collection_name_uniq;

CREATE UNIQUE INDEX IF NOT EXISTS media_collection_name_uniq ON assets.media_collection (lower(name));

CREATE UNIQUE INDEX IF NOT EXISTS entitlement_template_code_uniq ON catalogue.entitlement_template (lower(code));

DROP INDEX IF EXISTS catalogue.event_code_uniq;

CREATE UNIQUE INDEX IF NOT EXISTS event_code_uniq ON catalogue.event (lower(code));

CREATE UNIQUE INDEX IF NOT EXISTS price_list_code_uniq ON catalogue.price_list (lower(code));

DROP INDEX IF EXISTS catalogue.product_code_uniq;

CREATE UNIQUE INDEX IF NOT EXISTS product_code_uniq ON catalogue.product (lower(code));

DROP INDEX IF EXISTS catalogue.product_category_code_uniq;

CREATE UNIQUE INDEX IF NOT EXISTS product_category_code_uniq ON catalogue.product_category (lower(code)) WHERE code IS NOT NULL;

CREATE UNIQUE INDEX IF NOT EXISTS entitlement_code_uniq ON games.entitlement (lower(code));

CREATE UNIQUE INDEX IF NOT EXISTS authorisation_policy_code_uniq ON identity.authorisation_policy (lower(code));

CREATE UNIQUE INDEX IF NOT EXISTS principal_username_uniq ON identity.principal (lower(username));

DROP INDEX IF EXISTS identity.role_code_uniq;

CREATE UNIQUE INDEX IF NOT EXISTS role_code_uniq ON identity.role (lower(code));

DROP INDEX IF EXISTS inventory.supplier_code_uniq;

CREATE UNIQUE INDEX IF NOT EXISTS supplier_code_uniq ON inventory.supplier (lower(code));

CREATE UNIQUE INDEX IF NOT EXISTS supplier_contract_number_uniq ON inventory.supplier_contract (lower(number));

DROP INDEX IF EXISTS ledger.account_code_uniq;

CREATE UNIQUE INDEX IF NOT EXISTS account_code_uniq ON ledger.account (lower(code));

CREATE UNIQUE INDEX IF NOT EXISTS cost_center_code_uniq ON ledger.cost_center (lower(code));

DROP INDEX IF EXISTS ledger.credit_memo_credit_memo_number_uniq;

CREATE UNIQUE INDEX IF NOT EXISTS credit_memo_credit_memo_number_uniq ON ledger.credit_memo (lower(credit_memo_number));

DROP INDEX IF EXISTS ledger.journal_entry_entry_number_uniq;

CREATE UNIQUE INDEX IF NOT EXISTS journal_entry_entry_number_uniq ON ledger.journal_entry (lower(entry_number));

CREATE UNIQUE INDEX IF NOT EXISTS legal_entity_code_uniq ON ledger.legal_entity (lower(code));

DROP INDEX IF EXISTS ledger.tax_code_code_uniq;

CREATE UNIQUE INDEX IF NOT EXISTS tax_code_code_uniq ON ledger.tax_code (lower(code));

DROP INDEX IF EXISTS ledger.tax_invoice_invoice_number_uniq;

CREATE UNIQUE INDEX IF NOT EXISTS tax_invoice_invoice_number_uniq ON ledger.tax_invoice (lower(invoice_number));

CREATE UNIQUE INDEX IF NOT EXISTS asset_category_code_uniq ON maintenance.asset_category (lower(code));

CREATE UNIQUE INDEX IF NOT EXISTS inspection_template_code_uniq ON maintenance.inspection_template (lower(code));

DROP INDEX IF EXISTS marketing.loyalty_programme_code_uniq;

CREATE UNIQUE INDEX IF NOT EXISTS loyalty_programme_code_uniq ON marketing.loyalty_programme (lower(code));

CREATE UNIQUE INDEX IF NOT EXISTS message_template_tenant_id_code_uniq ON marketing.message_template (tenant_id, lower(code));

CREATE UNIQUE INDEX IF NOT EXISTS referral_code_uniq ON marketing.referral (lower(code));

DROP INDEX IF EXISTS orders.sales_order_order_number_uniq;

CREATE UNIQUE INDEX IF NOT EXISTS sales_order_order_number_uniq ON orders.sales_order (lower(order_number)) WHERE order_number IS NOT NULL;

CREATE UNIQUE INDEX IF NOT EXISTS method_code_uniq ON payments.method (lower(code));

CREATE UNIQUE INDEX IF NOT EXISTS provider_connection_code_uniq ON payments.provider_connection (lower(code));

CREATE UNIQUE INDEX IF NOT EXISTS device_serial_number_uniq ON platform.device (lower(serial_number)) WHERE serial_number IS NOT NULL;

CREATE UNIQUE INDEX IF NOT EXISTS bundle_code_uniq ON promotions.bundle (lower(code));

CREATE UNIQUE INDEX IF NOT EXISTS coupon_campaign_code_uniq ON promotions.coupon_campaign (lower(code));

DROP INDEX IF EXISTS promotions.promotion_code_uniq;

CREATE UNIQUE INDEX IF NOT EXISTS promotion_code_uniq ON promotions.promotion (lower(code));

CREATE UNIQUE INDEX IF NOT EXISTS recommendation_experiment_code_uniq ON promotions.recommendation_experiment (lower(code));

CREATE UNIQUE INDEX IF NOT EXISTS recommendation_strategy_code_uniq ON promotions.recommendation_strategy (lower(code));

CREATE UNIQUE INDEX IF NOT EXISTS agreement_rules_product_id_uniq ON rental.agreement_rules (product_id) WHERE product_id IS NOT NULL;

CREATE UNIQUE INDEX IF NOT EXISTS availability_rules_product_id_uniq ON rental.availability_rules (product_id) WHERE product_id IS NOT NULL;

CREATE UNIQUE INDEX IF NOT EXISTS duration_rules_product_id_uniq ON rental.duration_rules (product_id) WHERE product_id IS NOT NULL;

CREATE UNIQUE INDEX IF NOT EXISTS inventory_model_product_id_uniq ON rental.inventory_model (product_id) WHERE product_id IS NOT NULL;

CREATE UNIQUE INDEX IF NOT EXISTS operational_rules_product_id_uniq ON rental.operational_rules (product_id) WHERE product_id IS NOT NULL;

CREATE UNIQUE INDEX IF NOT EXISTS pricing_profile_code_uniq ON rental.pricing_profile (lower(code));

CREATE UNIQUE INDEX IF NOT EXISTS product_tenant_id_code_uniq ON rental.product (tenant_id, lower(code));

CREATE UNIQUE INDEX IF NOT EXISTS kpi_definition_code_uniq ON reporting.kpi_definition (lower(code));

CREATE UNIQUE INDEX IF NOT EXISTS attribute_definition_code_uniq ON resources.attribute_definition (lower(code));

CREATE UNIQUE INDEX IF NOT EXISTS resource_category_code_uniq ON resources.resource_category (lower(code));

CREATE UNIQUE INDEX IF NOT EXISTS resource_package_code_uniq ON resources.resource_package (lower(code));

CREATE UNIQUE INDEX IF NOT EXISTS resource_type_code_uniq ON resources.resource_type (lower(code));

CREATE UNIQUE INDEX IF NOT EXISTS plan_code_uniq ON subscription.plan (lower(code));

DROP INDEX IF EXISTS tenancy.data_retention_setting_data_class_uniq;

CREATE UNIQUE INDEX IF NOT EXISTS data_retention_setting_data_class_uniq ON tenancy.data_retention_setting (lower(data_class));

CREATE UNIQUE INDEX IF NOT EXISTS credit_type_code_uniq ON wallet.credit_type (lower(code));

CREATE UNIQUE INDEX IF NOT EXISTS voucher_type_code_uniq ON wallet.voucher_type (lower(code));

CREATE UNIQUE INDEX IF NOT EXISTS wallet_type_code_uniq ON wallet.wallet_type (lower(code));

CREATE UNIQUE INDEX IF NOT EXISTS content_page_slug_uniq ON whitelabel.content_page (lower(slug));

CREATE UNIQUE INDEX IF NOT EXISTS access_point_venue_id_code_uniq ON access.access_point (venue_id, lower(code));

DROP INDEX IF EXISTS catalogue.product_venue_id_family_key_uniq;

CREATE UNIQUE INDEX IF NOT EXISTS product_venue_id_family_key_uniq ON catalogue.product (venue_id, lower(family_key)) WHERE family_key IS NOT NULL;

CREATE UNIQUE INDEX IF NOT EXISTS delivery_location_venue_id_label_uniq ON fnb.delivery_location (venue_id, lower(label));

CREATE UNIQUE INDEX IF NOT EXISTS dining_table_scope_path_label_uniq ON fnb.dining_table (scope_path, lower(label));

CREATE UNIQUE INDEX IF NOT EXISTS modifier_group_scope_path_code_uniq ON fnb.modifier_group (scope_path, lower(code));

DROP INDEX IF EXISTS fnb.outlet_template_scope_path_code_uniq;

CREATE UNIQUE INDEX IF NOT EXISTS outlet_template_scope_path_code_uniq ON fnb.outlet_template (scope_path, lower(code));

CREATE UNIQUE INDEX IF NOT EXISTS game_venue_id_code_uniq ON games.game (venue_id, lower(code));

CREATE UNIQUE INDEX IF NOT EXISTS location_venue_id_code_uniq ON inventory.location (venue_id, lower(code));

DROP INDEX IF EXISTS maintenance.asset_venue_id_asset_tag_uniq;

CREATE UNIQUE INDEX IF NOT EXISTS asset_venue_id_asset_tag_uniq ON maintenance.asset (venue_id, lower(asset_tag));

CREATE UNIQUE INDEX IF NOT EXISTS outlet_venue_id_code_uniq ON platform.outlet (venue_id, lower(code));

CREATE UNIQUE INDEX IF NOT EXISTS sale_board_venue_id_code_uniq ON platform.sale_board (venue_id, lower(code));

CREATE UNIQUE INDEX IF NOT EXISTS campaign_venue_id_code_uniq ON promotions.campaign (venue_id, lower(code)) WHERE code IS NOT NULL;

CREATE UNIQUE INDEX IF NOT EXISTS queue_venue_id_code_uniq ON queue.queue (venue_id, lower(code));

CREATE UNIQUE INDEX IF NOT EXISTS resource_venue_id_code_uniq ON resources.resource (venue_id, lower(code));

DROP INDEX IF EXISTS seating.seat_category_venue_id_code_uniq;

CREATE UNIQUE INDEX IF NOT EXISTS seat_category_venue_id_code_uniq ON seating.seat_category (venue_id, lower(code));

DROP INDEX IF EXISTS transport.pass_type_venue_id_code_uniq;

CREATE UNIQUE INDEX IF NOT EXISTS pass_type_venue_id_code_uniq ON transport.pass_type (venue_id, lower(code));

DROP INDEX IF EXISTS transport.route_venue_id_code_uniq;

CREATE UNIQUE INDEX IF NOT EXISTS route_venue_id_code_uniq ON transport.route (venue_id, lower(code));

DROP INDEX IF EXISTS transport.station_venue_id_code_uniq;

CREATE UNIQUE INDEX IF NOT EXISTS station_venue_id_code_uniq ON transport.station (venue_id, lower(code));

CREATE UNIQUE INDEX IF NOT EXISTS index_entry_source_id_record_key_uniq ON ai.index_entry (source_id, lower(record_key));

CREATE UNIQUE INDEX IF NOT EXISTS credit_ledger_play_id_uniq ON games.credit_ledger (play_id);

CREATE UNIQUE INDEX IF NOT EXISTS principal_credential_principal_id_method_uniq ON identity.principal_credential (principal_id, lower(method));

CREATE UNIQUE INDEX IF NOT EXISTS subject_holding_holding_kind_holding_id_uniq ON identity.subject_holding (lower(holding_kind), holding_id);

CREATE UNIQUE INDEX IF NOT EXISTS guest_device_subject_id_installation_id_uniq ON marketing.guest_device (subject_id, installation_id);

CREATE UNIQUE INDEX IF NOT EXISTS guest_device_subject_id_token_fingerprint_uniq ON marketing.guest_device (subject_id, token_fingerprint);

CREATE UNIQUE INDEX IF NOT EXISTS wishlist_item_subject_id_variant_id_performance_id_uniq ON marketing.wishlist_item (subject_id, variant_id, performance_id) NULLS NOT DISTINCT;

DROP INDEX IF EXISTS seating.seat_seat_map_id_section_code_row_label_seat_number_uniq;

CREATE UNIQUE INDEX IF NOT EXISTS seat_seat_map_id_section_code_row_label_seat_number_uniq ON seating.seat (seat_map_id, lower(section_code), lower(row_label), lower(seat_number));

DROP INDEX IF EXISTS seating.seat_price_band_seat_category_id_code_uniq;

CREATE UNIQUE INDEX IF NOT EXISTS seat_price_band_seat_category_id_code_uniq ON seating.seat_price_band (seat_category_id, lower(code));

CREATE INDEX IF NOT EXISTS accreditation_badge_scope_path_idx ON approvals.accreditation_badge USING gist (scope_path);

CREATE INDEX IF NOT EXISTS alternative_code_scope_path_idx ON catalogue.alternative_code USING gist (scope_path);

CREATE INDEX IF NOT EXISTS badge_scope_path_idx ON marketing.badge USING gist (scope_path);

CREATE INDEX IF NOT EXISTS booking_flow_step_scope_path_idx ON whitelabel.booking_flow_step USING gist (scope_path);

CREATE INDEX IF NOT EXISTS case_message_scope_path_idx ON marketing.case_message USING gist (scope_path);

CREATE INDEX IF NOT EXISTS cold_chain_event_scope_path_idx ON fnb.cold_chain_event USING gist (scope_path);

CREATE INDEX IF NOT EXISTS combo_scope_path_idx ON fnb.combo USING gist (scope_path);

CREATE INDEX IF NOT EXISTS combo_slot_scope_path_idx ON fnb.combo_slot USING gist (scope_path);

CREATE INDEX IF NOT EXISTS config_source_scope_path_idx ON ai.config_source USING gist (scope_path);

CREATE INDEX IF NOT EXISTS denomination_scope_path_idx ON platform.denomination USING gist (scope_path);

CREATE INDEX IF NOT EXISTS deposit_activity_scope_path_idx ON payments.deposit_activity USING gist (scope_path);

CREATE INDEX IF NOT EXISTS device_scope_path_idx ON platform.device USING gist (scope_path);

CREATE INDEX IF NOT EXISTS dining_table_scope_path_idx ON fnb.dining_table USING gist (scope_path);

CREATE INDEX IF NOT EXISTS fee_rule_scope_path_idx ON payments.fee_rule USING gist (scope_path);

CREATE INDEX IF NOT EXISTS group_enquiry_scope_path_idx ON orders.group_enquiry USING gist (scope_path);

CREATE INDEX IF NOT EXISTS guest_extra_option_scope_path_idx ON marketing.guest_extra_option USING gist (scope_path);

CREATE INDEX IF NOT EXISTS guest_extra_value_scope_path_idx ON marketing.guest_extra_value USING gist (scope_path);

CREATE INDEX IF NOT EXISTS import_job_scope_path_idx ON venuemap.import_job USING gist (scope_path);

CREATE INDEX IF NOT EXISTS invitation_allowance_scope_path_idx ON orders.invitation_allowance USING gist (scope_path);

CREATE INDEX IF NOT EXISTS invitation_scope_path_idx ON orders.invitation USING gist (scope_path);

CREATE INDEX IF NOT EXISTS kitchen_exception_scope_path_idx ON fnb.kitchen_exception USING gist (scope_path);

CREATE INDEX IF NOT EXISTS kitchen_station_scope_path_idx ON fnb.kitchen_station USING gist (scope_path);

CREATE INDEX IF NOT EXISTS loyalty_campaign_scope_path_idx ON marketing.loyalty_campaign USING gist (scope_path);

CREATE INDEX IF NOT EXISTS loyalty_points_scope_path_idx ON marketing.loyalty_points USING gist (scope_path);

CREATE INDEX IF NOT EXISTS member_exception_scope_path_idx ON orders.member_exception USING gist (scope_path);

CREATE INDEX IF NOT EXISTS membership_benefit_scope_path_idx ON catalogue.membership_benefit USING gist (scope_path);

CREATE INDEX IF NOT EXISTS membership_migration_scope_path_idx ON orders.membership_migration USING gist (scope_path);

CREATE INDEX IF NOT EXISTS membership_programme_scope_path_idx ON catalogue.membership_programme USING gist (scope_path);

CREATE INDEX IF NOT EXISTS participant_scope_path_idx ON rental.participant USING gist (scope_path);

CREATE INDEX IF NOT EXISTS play_scope_path_idx ON games.play USING gist (scope_path);

CREATE INDEX IF NOT EXISTS points_redemption_rule_scope_path_idx ON marketing.points_redemption_rule USING gist (scope_path);

CREATE INDEX IF NOT EXISTS production_plan_scope_path_idx ON fnb.production_plan USING gist (scope_path);

CREATE INDEX IF NOT EXISTS promotion_variant_scope_path_idx ON promotions.promotion_variant USING gist (scope_path);

CREATE INDEX IF NOT EXISTS reader_deployment_scope_path_idx ON games.reader_deployment USING gist (scope_path);

CREATE INDEX IF NOT EXISTS recognition_schedule_scope_path_idx ON ledger.recognition_schedule USING gist (scope_path);

CREATE INDEX IF NOT EXISTS refund_calculation_policy_scope_path_idx ON orders.refund_calculation_policy USING gist (scope_path);

CREATE INDEX IF NOT EXISTS region_settings_scope_path_idx ON platform.region_settings USING gist (scope_path);

CREATE INDEX IF NOT EXISTS reward_scope_path_idx ON marketing.reward USING gist (scope_path);

CREATE INDEX IF NOT EXISTS seat_price_band_scope_path_idx ON seating.seat_price_band USING gist (scope_path);

CREATE INDEX IF NOT EXISTS seat_scope_path_idx ON seating.seat USING gist (scope_path);

CREATE INDEX IF NOT EXISTS tax_code_scope_path_idx ON ledger.tax_code USING gist (scope_path);

CREATE INDEX IF NOT EXISTS tax_exemption_scope_path_idx ON ledger.tax_exemption USING gist (scope_path);

CREATE INDEX IF NOT EXISTS temperature_log_scope_path_idx ON fnb.temperature_log USING gist (scope_path);

CREATE INDEX IF NOT EXISTS ticket_template_scope_path_idx ON orders.ticket_template USING gist (scope_path);

CREATE INDEX IF NOT EXISTS upsell_rule_scope_path_idx ON promotions.upsell_rule USING gist (scope_path);

CREATE OR REPLACE FUNCTION platform.drop_rls_policies(target regclass)
    RETURNS void
    LANGUAGE plpgsql
AS $$
DECLARE
    pol record;
BEGIN
    FOR pol IN SELECT polname FROM pg_policy WHERE polrelid = target LOOP
        EXECUTE format('DROP POLICY IF EXISTS %I ON %s', pol.polname, target);
    END LOOP;
END
$$;

CREATE OR REPLACE FUNCTION platform.grant_holder()
    RETURNS boolean
    LANGUAGE sql
    STABLE
    PARALLEL SAFE
AS $$
    SELECT cardinality(platform.current_scope_paths()) > 0
       AND NULLIF(current_setting('ticvai.subject_id', true), '') IS NULL;
$$;

CREATE OR REPLACE FUNCTION platform.above_scope(row_scope_path ltree)
    RETURNS boolean
    LANGUAGE sql
    STABLE
    PARALLEL SAFE
AS $$
    SELECT row_scope_path IS NOT NULL
       AND cardinality(platform.current_scope_paths()) > 0
       AND row_scope_path @> ANY (platform.current_scope_paths());
$$;

CREATE OR REPLACE FUNCTION platform.apply_split_rls(target regclass, read_check text, write_check text)
    RETURNS void
    LANGUAGE plpgsql
AS $$
DECLARE
    base text := (SELECT left(c.relname, 55) FROM pg_class c WHERE c.oid = target);
BEGIN
    EXECUTE format('ALTER TABLE %s ENABLE ROW LEVEL SECURITY', target);
    EXECUTE format('ALTER TABLE %s FORCE ROW LEVEL SECURITY', target);
    PERFORM platform.drop_rls_policies(target);
    EXECUTE format('CREATE POLICY %I ON %s FOR SELECT USING (%s)', base || '_read', target, read_check);
    EXECUTE format('CREATE POLICY %I ON %s FOR INSERT WITH CHECK (%s)', base || '_append', target, write_check);
    EXECUTE format('CREATE POLICY %I ON %s FOR UPDATE USING (%s) WITH CHECK (%s)',
                   base || '_update', target, write_check, write_check);
    EXECUTE format('CREATE POLICY %I ON %s FOR DELETE USING (%s)', base || '_delete', target, write_check);
END
$$;

CREATE OR REPLACE FUNCTION platform.apply_read_beneath_rls(target regclass)
    RETURNS void
    LANGUAGE plpgsql
AS $$
BEGIN
    PERFORM platform.apply_split_rls(target,
        'platform.in_scope(scope_path) OR platform.above_scope(scope_path)',
        'platform.in_scope(scope_path)');
END
$$;

CREATE OR REPLACE FUNCTION platform.apply_grant_holder_read_rls(target regclass, write_check text)
    RETURNS void
    LANGUAGE plpgsql
AS $$
BEGIN
    PERFORM platform.apply_split_rls(target, 'platform.grant_holder()', write_check);
END
$$;

CREATE OR REPLACE FUNCTION platform.apply_grant_holder_subject_read_rls(target regclass)
    RETURNS void
    LANGUAGE plpgsql
AS $$
BEGIN
    PERFORM platform.apply_split_rls(target,
        'platform.grant_holder() OR platform.subject_in_scope(subject_id)',
        'platform.subject_in_scope(subject_id)');
END
$$;

CREATE OR REPLACE FUNCTION platform.apply_parent_split_rls(target regclass, fk_column text, parent regclass,
                                                           parent_key text, parent_write text)
    RETURNS void
    LANGUAGE plpgsql
AS $$
DECLARE
    link text := format('parent_row.%I = %s.%I', parent_key, target, fk_column);
BEGIN
    PERFORM platform.apply_split_rls(target,
        format('EXISTS (SELECT 1 FROM %s parent_row WHERE %s)', parent, link),
        format('EXISTS (SELECT 1 FROM %s parent_row WHERE %s AND (%s))', parent, link, parent_write));
END
$$;

SELECT platform.drop_rls_policies('orders.invitation'::regclass);

SELECT platform.apply_scope_rls('orders.invitation'::regclass);

SELECT platform.drop_rls_policies('access.hardware_model'::regclass);

SELECT platform.apply_read_beneath_rls('access.hardware_model'::regclass);

SELECT platform.drop_rls_policies('ai.assistant_profile'::regclass);

SELECT platform.apply_read_beneath_rls('ai.assistant_profile'::regclass);

SELECT platform.drop_rls_policies('ai.capability'::regclass);

SELECT platform.apply_read_beneath_rls('ai.capability'::regclass);

SELECT platform.drop_rls_policies('ai.config_source'::regclass);

SELECT platform.apply_grant_holder_read_rls('ai.config_source'::regclass, 'platform.in_scope(scope_path)');

SELECT platform.drop_rls_policies('ai.governance_policy'::regclass);

SELECT platform.apply_read_beneath_rls('ai.governance_policy'::regclass);

SELECT platform.drop_rls_policies('ai.governance_policy_version'::regclass);

SELECT platform.apply_read_beneath_rls('ai.governance_policy_version'::regclass);

SELECT platform.drop_rls_policies('ai.knowledge_collection'::regclass);

SELECT platform.apply_read_beneath_rls('ai.knowledge_collection'::regclass);

SELECT platform.drop_rls_policies('ai.knowledge_document'::regclass);

SELECT platform.apply_read_beneath_rls('ai.knowledge_document'::regclass);

SELECT platform.drop_rls_policies('ai.model'::regclass);

SELECT platform.apply_read_beneath_rls('ai.model'::regclass);

SELECT platform.drop_rls_policies('ai.policy'::regclass);

SELECT platform.apply_read_beneath_rls('ai.policy'::regclass);

SELECT platform.drop_rls_policies('ai.policy_exception'::regclass);

SELECT platform.apply_read_beneath_rls('ai.policy_exception'::regclass);

SELECT platform.drop_rls_policies('ai.prompt_template'::regclass);

SELECT platform.apply_read_beneath_rls('ai.prompt_template'::regclass);

SELECT platform.drop_rls_policies('ai.release'::regclass);

SELECT platform.apply_read_beneath_rls('ai.release'::regclass);

SELECT platform.drop_rls_policies('ai.tool'::regclass);

SELECT platform.apply_read_beneath_rls('ai.tool'::regclass);

SELECT platform.drop_rls_policies('approvals.accreditation_badge'::regclass);

SELECT platform.apply_grant_holder_read_rls('approvals.accreditation_badge'::regclass, 'platform.in_scope(scope_path)');

SELECT platform.drop_rls_policies('approvals.control_policy'::regclass);

SELECT platform.apply_read_beneath_rls('approvals.control_policy'::regclass);

SELECT platform.drop_rls_policies('approvals.external_provider'::regclass);

SELECT platform.apply_read_beneath_rls('approvals.external_provider'::regclass);

SELECT platform.drop_rls_policies('approvals.sla_policy'::regclass);

SELECT platform.apply_read_beneath_rls('approvals.sla_policy'::regclass);

SELECT platform.drop_rls_policies('approvals.step_up_policy'::regclass);

SELECT platform.apply_grant_holder_read_rls('approvals.step_up_policy'::regclass, 'platform.tenant_root_in_scope()');

SELECT platform.drop_rls_policies('assets.distribution_channel'::regclass);

SELECT platform.apply_read_beneath_rls('assets.distribution_channel'::regclass);

SELECT platform.drop_rls_policies('assets.taxonomy'::regclass);

SELECT platform.apply_read_beneath_rls('assets.taxonomy'::regclass);

SELECT platform.drop_rls_policies('catalogue.alternative_code'::regclass);

SELECT platform.apply_grant_holder_read_rls('catalogue.alternative_code'::regclass, 'platform.in_scope(scope_path)');

SELECT platform.drop_rls_policies('catalogue.event_type'::regclass);

SELECT platform.apply_read_beneath_rls('catalogue.event_type'::regclass);

SELECT platform.drop_rls_policies('catalogue.membership_benefit'::regclass);

SELECT platform.apply_grant_holder_read_rls('catalogue.membership_benefit'::regclass, 'platform.in_scope(scope_path)');

SELECT platform.drop_rls_policies('catalogue.membership_programme'::regclass);

SELECT platform.apply_grant_holder_read_rls('catalogue.membership_programme'::regclass, 'platform.in_scope(scope_path)');

SELECT platform.drop_rls_policies('catalogue.price_category'::regclass);

SELECT platform.apply_read_beneath_rls('catalogue.price_category'::regclass);

SELECT platform.drop_rls_policies('catalogue.pricing_market'::regclass);

SELECT platform.apply_read_beneath_rls('catalogue.pricing_market'::regclass);

SELECT platform.drop_rls_policies('catalogue.rounding_profile'::regclass);

SELECT platform.apply_read_beneath_rls('catalogue.rounding_profile'::regclass);

SELECT platform.drop_rls_policies('catalogue.signal_registry'::regclass);

SELECT platform.apply_read_beneath_rls('catalogue.signal_registry'::regclass);

SELECT platform.drop_rls_policies('fnb.cold_chain_event'::regclass);

SELECT platform.apply_grant_holder_read_rls('fnb.cold_chain_event'::regclass, 'platform.in_scope(scope_path)');

SELECT platform.drop_rls_policies('fnb.combo'::regclass);

SELECT platform.apply_grant_holder_read_rls('fnb.combo'::regclass, 'platform.in_scope(scope_path)');

SELECT platform.drop_rls_policies('fnb.combo_slot'::regclass);

SELECT platform.apply_grant_holder_read_rls('fnb.combo_slot'::regclass, 'platform.in_scope(scope_path)');

SELECT platform.drop_rls_policies('fnb.delivery_location_outlet'::regclass);

SELECT platform.apply_grant_holder_read_rls('fnb.delivery_location_outlet'::regclass, 'platform.tenant_root_in_scope()');

SELECT platform.drop_rls_policies('fnb.dining_table'::regclass);

SELECT platform.apply_grant_holder_read_rls('fnb.dining_table'::regclass, 'platform.in_scope(scope_path)');

SELECT platform.drop_rls_policies('fnb.kitchen_exception'::regclass);

SELECT platform.apply_grant_holder_read_rls('fnb.kitchen_exception'::regclass, 'platform.in_scope(scope_path)');

SELECT platform.drop_rls_policies('fnb.kitchen_station'::regclass);

SELECT platform.apply_grant_holder_read_rls('fnb.kitchen_station'::regclass, 'platform.in_scope(scope_path)');

SELECT platform.drop_rls_policies('fnb.production_plan'::regclass);

SELECT platform.apply_grant_holder_read_rls('fnb.production_plan'::regclass, 'platform.in_scope(scope_path)');

SELECT platform.drop_rls_policies('fnb.temperature_log'::regclass);

SELECT platform.apply_grant_holder_read_rls('fnb.temperature_log'::regclass, 'platform.in_scope(scope_path)');

SELECT platform.drop_rls_policies('games.attraction_type'::regclass);

SELECT platform.apply_read_beneath_rls('games.attraction_type'::regclass);

SELECT platform.drop_rls_policies('games.play'::regclass);

SELECT platform.apply_grant_holder_read_rls('games.play'::regclass, 'platform.in_scope(scope_path)');

SELECT platform.drop_rls_policies('games.reader_deployment'::regclass);

SELECT platform.apply_grant_holder_read_rls('games.reader_deployment'::regclass, 'platform.in_scope(scope_path)');

SELECT platform.drop_rls_policies('identity.capability_template'::regclass);

SELECT platform.apply_read_beneath_rls('identity.capability_template'::regclass);

SELECT platform.drop_rls_policies('identity.password_policy'::regclass);

SELECT platform.apply_read_beneath_rls('identity.password_policy'::regclass);

SELECT platform.drop_rls_policies('identity.principal'::regclass);

SELECT platform.apply_grant_holder_read_rls('identity.principal'::regclass, 'platform.tenant_root_in_scope()');

SELECT platform.drop_rls_policies('identity.role'::regclass);

SELECT platform.apply_grant_holder_read_rls('identity.role'::regclass, 'platform.tenant_root_in_scope()');

SELECT platform.drop_rls_policies('identity.segregation_rule'::regclass);

SELECT platform.apply_read_beneath_rls('identity.segregation_rule'::regclass);

SELECT platform.drop_rls_policies('inventory.stock_batch'::regclass);

SELECT platform.apply_grant_holder_read_rls('inventory.stock_batch'::regclass, 'platform.tenant_root_in_scope()');

SELECT platform.drop_rls_policies('inventory.supplier'::regclass);

SELECT platform.apply_read_beneath_rls('inventory.supplier'::regclass);

SELECT platform.drop_rls_policies('ledger.deposit'::regclass);

SELECT platform.apply_grant_holder_subject_read_rls('ledger.deposit'::regclass);

SELECT platform.drop_rls_policies('ledger.legal_entity'::regclass);

SELECT platform.apply_read_beneath_rls('ledger.legal_entity'::regclass);

SELECT platform.drop_rls_policies('ledger.recognition_schedule'::regclass);

SELECT platform.apply_grant_holder_read_rls('ledger.recognition_schedule'::regclass, 'platform.in_scope(scope_path)');

SELECT platform.drop_rls_policies('ledger.tax_code'::regclass);

SELECT platform.apply_grant_holder_read_rls('ledger.tax_code'::regclass, 'platform.in_scope(scope_path)');

SELECT platform.drop_rls_policies('ledger.tax_exemption'::regclass);

SELECT platform.apply_grant_holder_read_rls('ledger.tax_exemption'::regclass, 'platform.in_scope(scope_path)');

SELECT platform.drop_rls_policies('maintenance.asset_category'::regclass);

SELECT platform.apply_read_beneath_rls('maintenance.asset_category'::regclass);

SELECT platform.drop_rls_policies('marketing.agent_availability'::regclass);

SELECT platform.apply_grant_holder_read_rls('marketing.agent_availability'::regclass, 'platform.tenant_root_in_scope()');

SELECT platform.drop_rls_policies('marketing.audience_list'::regclass);

SELECT platform.apply_read_beneath_rls('marketing.audience_list'::regclass);

SELECT platform.drop_rls_policies('marketing.badge'::regclass);

SELECT platform.apply_grant_holder_read_rls('marketing.badge'::regclass, 'platform.in_scope(scope_path)');

SELECT platform.drop_rls_policies('marketing.case_message'::regclass);

SELECT platform.apply_grant_holder_read_rls('marketing.case_message'::regclass, 'platform.in_scope(scope_path)');

SELECT platform.drop_rls_policies('marketing.consent_purpose'::regclass);

SELECT platform.apply_grant_holder_read_rls('marketing.consent_purpose'::regclass, 'platform.tenant_root_in_scope()');

SELECT platform.drop_rls_policies('marketing.consent_purpose_channel'::regclass);

SELECT platform.apply_grant_holder_read_rls('marketing.consent_purpose_channel'::regclass, 'platform.tenant_root_in_scope()');

SELECT platform.drop_rls_policies('marketing.consent_record'::regclass);

SELECT platform.apply_grant_holder_subject_read_rls('marketing.consent_record'::regclass);

SELECT platform.drop_rls_policies('marketing.consent_record_channel'::regclass);

SELECT platform.apply_grant_holder_read_rls('marketing.consent_record_channel'::regclass, 'platform.tenant_root_in_scope()');

SELECT platform.drop_rls_policies('marketing.form_submission'::regclass);

SELECT platform.apply_grant_holder_subject_read_rls('marketing.form_submission'::regclass);

SELECT platform.drop_rls_policies('marketing.guest_document'::regclass);

SELECT platform.apply_grant_holder_subject_read_rls('marketing.guest_document'::regclass);

SELECT platform.drop_rls_policies('marketing.guest_extra_option'::regclass);

SELECT platform.apply_grant_holder_read_rls('marketing.guest_extra_option'::regclass, 'platform.in_scope(scope_path)');

SELECT platform.drop_rls_policies('marketing.guest_extra_value'::regclass);

SELECT platform.apply_grant_holder_read_rls('marketing.guest_extra_value'::regclass, 'platform.in_scope(scope_path)');

SELECT platform.drop_rls_policies('marketing.guest_preference'::regclass);

SELECT platform.apply_grant_holder_subject_read_rls('marketing.guest_preference'::regclass);

SELECT platform.drop_rls_policies('marketing.loyalty_campaign'::regclass);

SELECT platform.apply_grant_holder_read_rls('marketing.loyalty_campaign'::regclass, 'platform.in_scope(scope_path)');

SELECT platform.drop_rls_policies('marketing.loyalty_points'::regclass);

SELECT platform.apply_grant_holder_read_rls('marketing.loyalty_points'::regclass, 'platform.in_scope(scope_path)');

SELECT platform.drop_rls_policies('marketing.message_dispatch'::regclass);

SELECT platform.apply_grant_holder_subject_read_rls('marketing.message_dispatch'::regclass);

SELECT platform.drop_rls_policies('marketing.message_template'::regclass);

SELECT platform.apply_grant_holder_read_rls('marketing.message_template'::regclass, 'platform.tenant_root_in_scope()');

SELECT platform.drop_rls_policies('marketing.points_redemption_rule'::regclass);

SELECT platform.apply_grant_holder_read_rls('marketing.points_redemption_rule'::regclass, 'platform.in_scope(scope_path)');

SELECT platform.drop_rls_policies('marketing.privacy_audit_event'::regclass);

SELECT platform.apply_grant_holder_subject_read_rls('marketing.privacy_audit_event'::regclass);

SELECT platform.drop_rls_policies('marketing.privacy_incident'::regclass);

SELECT platform.apply_read_beneath_rls('marketing.privacy_incident'::regclass);

SELECT platform.drop_rls_policies('marketing.retention_policy'::regclass);

SELECT platform.apply_read_beneath_rls('marketing.retention_policy'::regclass);

SELECT platform.drop_rls_policies('marketing.reward'::regclass);

SELECT platform.apply_grant_holder_read_rls('marketing.reward'::regclass, 'platform.in_scope(scope_path)');

SELECT platform.drop_rls_policies('marketing.suppression'::regclass);

SELECT platform.apply_read_beneath_rls('marketing.suppression'::regclass);

SELECT platform.drop_rls_policies('marketing.touch_point'::regclass);

SELECT platform.apply_grant_holder_subject_read_rls('marketing.touch_point'::regclass);

SELECT platform.drop_rls_policies('marketing.tracking_technology_catalogue'::regclass);

SELECT platform.apply_read_beneath_rls('marketing.tracking_technology_catalogue'::regclass);

SELECT platform.drop_rls_policies('orders.fraud_rule'::regclass);

SELECT platform.apply_read_beneath_rls('orders.fraud_rule'::regclass);

SELECT platform.drop_rls_policies('orders.group_enquiry'::regclass);

SELECT platform.apply_grant_holder_read_rls('orders.group_enquiry'::regclass, 'platform.in_scope(scope_path)');

SELECT platform.drop_rls_policies('orders.invitation_allowance'::regclass);

SELECT platform.apply_grant_holder_read_rls('orders.invitation_allowance'::regclass, 'platform.in_scope(scope_path)');

SELECT platform.drop_rls_policies('orders.member_exception'::regclass);

SELECT platform.apply_grant_holder_read_rls('orders.member_exception'::regclass, 'platform.in_scope(scope_path)');

SELECT platform.drop_rls_policies('orders.membership_activation_action'::regclass);

SELECT platform.apply_grant_holder_subject_read_rls('orders.membership_activation_action'::regclass);

SELECT platform.drop_rls_policies('orders.membership_migration'::regclass);

SELECT platform.apply_grant_holder_read_rls('orders.membership_migration'::regclass, 'platform.in_scope(scope_path)');

SELECT platform.drop_rls_policies('orders.refund_calculation_policy'::regclass);

SELECT platform.apply_grant_holder_read_rls('orders.refund_calculation_policy'::regclass, 'platform.in_scope(scope_path)');

SELECT platform.drop_rls_policies('orders.ticket_template'::regclass);

SELECT platform.apply_grant_holder_read_rls('orders.ticket_template'::regclass, 'platform.in_scope(scope_path)');

SELECT platform.drop_rls_policies('payments.deposit_activity'::regclass);

SELECT platform.apply_grant_holder_read_rls('payments.deposit_activity'::regclass, 'platform.in_scope(scope_path)');

SELECT platform.drop_rls_policies('payments.fee_rule'::regclass);

SELECT platform.apply_grant_holder_read_rls('payments.fee_rule'::regclass, 'platform.in_scope(scope_path)');

SELECT platform.drop_rls_policies('payments.instalment_policy'::regclass);

SELECT platform.apply_read_beneath_rls('payments.instalment_policy'::regclass);

SELECT platform.drop_rls_policies('payments.provider_connection'::regclass);

SELECT platform.apply_read_beneath_rls('payments.provider_connection'::regclass);

SELECT platform.drop_rls_policies('payments.terminal_certification'::regclass);

SELECT platform.apply_read_beneath_rls('payments.terminal_certification'::regclass);

SELECT platform.drop_rls_policies('payments.token'::regclass);

SELECT platform.apply_grant_holder_subject_read_rls('payments.token'::regclass);

SELECT platform.drop_rls_policies('pii.subject'::regclass);

SELECT platform.apply_grant_holder_read_rls('pii.subject'::regclass, 'platform.tenant_root_in_scope()');

SELECT platform.drop_rls_policies('pii.subject_contact'::regclass);

SELECT platform.apply_grant_holder_subject_read_rls('pii.subject_contact'::regclass);

SELECT platform.drop_rls_policies('platform.denomination'::regclass);

SELECT platform.apply_grant_holder_read_rls('platform.denomination'::regclass, 'platform.in_scope(scope_path)');

SELECT platform.drop_rls_policies('platform.device'::regclass);

SELECT platform.apply_grant_holder_read_rls('platform.device'::regclass, 'platform.in_scope(scope_path)');

SELECT platform.drop_rls_policies('platform.region_settings'::regclass);

SELECT platform.apply_read_beneath_rls('platform.region_settings'::regclass);

SELECT platform.drop_rls_policies('promotions.promotion_variant'::regclass);

SELECT platform.apply_grant_holder_read_rls('promotions.promotion_variant'::regclass, 'platform.in_scope(scope_path)');

SELECT platform.drop_rls_policies('promotions.upsell_rule'::regclass);

SELECT platform.apply_read_beneath_rls('promotions.upsell_rule'::regclass);

SELECT platform.drop_rls_policies('rental.participant'::regclass);

SELECT platform.apply_grant_holder_read_rls('rental.participant'::regclass, 'platform.in_scope(scope_path)');

SELECT platform.drop_rls_policies('reporting.kpi_definition'::regclass);

SELECT platform.apply_read_beneath_rls('reporting.kpi_definition'::regclass);

SELECT platform.drop_rls_policies('reporting.semantic_model'::regclass);

SELECT platform.apply_read_beneath_rls('reporting.semantic_model'::regclass);

SELECT platform.drop_rls_policies('resources.attribute_definition'::regclass);

SELECT platform.apply_read_beneath_rls('resources.attribute_definition'::regclass);

SELECT platform.drop_rls_policies('resources.resource_category'::regclass);

SELECT platform.apply_read_beneath_rls('resources.resource_category'::regclass);

SELECT platform.drop_rls_policies('resources.resource_type'::regclass);

SELECT platform.apply_read_beneath_rls('resources.resource_type'::regclass);

SELECT platform.drop_rls_policies('seating.seat'::regclass);

SELECT platform.apply_grant_holder_read_rls('seating.seat'::regclass, 'platform.in_scope(scope_path)');

SELECT platform.drop_rls_policies('seating.seat_price_band'::regclass);

SELECT platform.apply_grant_holder_read_rls('seating.seat_price_band'::regclass, 'platform.in_scope(scope_path)');

SELECT platform.drop_rls_policies('venuemap.import_job'::regclass);

SELECT platform.apply_grant_holder_read_rls('venuemap.import_job'::regclass, 'platform.in_scope(scope_path)');

SELECT platform.drop_rls_policies('wallet.accounting_mapping'::regclass);

SELECT platform.apply_read_beneath_rls('wallet.accounting_mapping'::regclass);

SELECT platform.drop_rls_policies('wallet.balance'::regclass);

SELECT platform.apply_grant_holder_read_rls('wallet.balance'::regclass, 'platform.tenant_root_in_scope()');

SELECT platform.drop_rls_policies('wallet.credit_type'::regclass);

SELECT platform.apply_read_beneath_rls('wallet.credit_type'::regclass);

SELECT platform.drop_rls_policies('wallet.gift_card'::regclass);

SELECT platform.apply_grant_holder_subject_read_rls('wallet.gift_card'::regclass);

SELECT platform.drop_rls_policies('wallet.wallet'::regclass);

SELECT platform.apply_grant_holder_subject_read_rls('wallet.wallet'::regclass);

SELECT platform.drop_rls_policies('whitelabel.banner'::regclass);

SELECT platform.apply_grant_holder_read_rls('whitelabel.banner'::regclass, 'platform.tenant_root_in_scope()');

SELECT platform.drop_rls_policies('whitelabel.booking_flow_step'::regclass);

SELECT platform.apply_grant_holder_read_rls('whitelabel.booking_flow_step'::regclass, 'platform.in_scope(scope_path)');

SELECT platform.drop_rls_policies('whitelabel.config_version'::regclass);

SELECT platform.apply_read_beneath_rls('whitelabel.config_version'::regclass);

SELECT platform.drop_rls_policies('whitelabel.content_page'::regclass);

SELECT platform.apply_read_beneath_rls('whitelabel.content_page'::regclass);

SELECT platform.drop_rls_policies('whitelabel.homepage_section'::regclass);

SELECT platform.apply_grant_holder_read_rls('whitelabel.homepage_section'::regclass, 'platform.tenant_root_in_scope()');

SELECT platform.drop_rls_policies('whitelabel.promo_block'::regclass);

SELECT platform.apply_read_beneath_rls('whitelabel.promo_block'::regclass);

SELECT platform.drop_rls_policies('workforce.training_record'::regclass);

SELECT platform.apply_grant_holder_read_rls('workforce.training_record'::regclass, 'platform.tenant_root_in_scope()');

SELECT platform.drop_rls_policies('access.access_change'::regclass);

SELECT platform.apply_parent_rls('access.access_change'::regclass, 'old_entitlement_id', 'access.entitlement'::regclass, 'id');

SELECT platform.drop_rls_policies('access.entry_rule_point'::regclass);

SELECT platform.apply_parent_rls('access.entry_rule_point'::regclass, 'admission_rules_id', 'access.admission_rules'::regclass, 'id');

SELECT platform.drop_rls_policies('ai.chunk_embedding'::regclass);

SELECT platform.apply_parent_split_rls('ai.chunk_embedding'::regclass, 'document_id', 'ai.knowledge_document'::regclass, 'id', 'platform.in_scope(parent_row.scope_path)');

SELECT platform.drop_rls_policies('ai.index_source'::regclass);

SELECT platform.apply_parent_split_rls('ai.index_source'::regclass, 'collection_id', 'ai.knowledge_collection'::regclass, 'id', 'platform.in_scope(parent_row.scope_path)');

SELECT platform.drop_rls_policies('assets.media_collection_member'::regclass);

SELECT platform.apply_parent_rls('assets.media_collection_member'::regclass, 'collection_id', 'assets.media_collection'::regclass, 'id');

SELECT platform.drop_rls_policies('catalogue.product_media'::regclass);

SELECT platform.apply_parent_rls('catalogue.product_media'::regclass, 'product_id', 'catalogue.product'::regclass, 'id');

SELECT platform.drop_rls_policies('fnb.combo_slot_option'::regclass);

SELECT platform.apply_parent_split_rls('fnb.combo_slot_option'::regclass, 'combo_slot_id', 'fnb.combo_slot'::regclass, 'id', 'platform.in_scope(parent_row.scope_path)');

SELECT platform.drop_rls_policies('fnb.kitchen_sla'::regclass);

SELECT platform.apply_parent_rls('fnb.kitchen_sla'::regclass, 'outlet_id', 'platform.outlet'::regclass, 'id');

SELECT platform.drop_rls_policies('fnb.production_plan_line'::regclass);

SELECT platform.apply_parent_split_rls('fnb.production_plan_line'::regclass, 'production_plan_id', 'fnb.production_plan'::regclass, 'id', 'platform.in_scope(parent_row.scope_path)');

SELECT platform.drop_rls_policies('fnb.reservation_table'::regclass);

SELECT platform.apply_parent_split_rls('fnb.reservation_table'::regclass, 'table_id', 'fnb.dining_table'::regclass, 'id', 'platform.in_scope(parent_row.scope_path)');

SELECT platform.drop_rls_policies('identity.benefit_usage'::regclass);

SELECT platform.apply_parent_split_rls('identity.benefit_usage'::regclass, 'membership_benefit_id', 'catalogue.membership_benefit'::regclass, 'id', 'platform.in_scope(parent_row.scope_path)');

SELECT platform.drop_rls_policies('identity.customer_membership'::regclass);

SELECT platform.apply_parent_rls('identity.customer_membership'::regclass, 'entitlement_template_id', 'catalogue.entitlement_template'::regclass, 'id');

SELECT platform.drop_rls_policies('inventory.count'::regclass);

SELECT platform.apply_parent_rls('inventory.count'::regclass, 'location_id', 'inventory.location'::regclass, 'id');

SELECT platform.drop_rls_policies('inventory.quotation_line'::regclass);

SELECT platform.apply_parent_rls('inventory.quotation_line'::regclass, 'quotation_id', 'inventory.quotation'::regclass, 'id');

SELECT platform.drop_rls_policies('inventory.supplier_contract'::regclass);

SELECT platform.apply_parent_split_rls('inventory.supplier_contract'::regclass, 'supplier_id', 'inventory.supplier'::regclass, 'id', 'platform.in_scope(parent_row.scope_path)');

SELECT platform.drop_rls_policies('ledger.account'::regclass);

SELECT platform.apply_parent_split_rls('ledger.account'::regclass, 'legal_entity_id', 'ledger.legal_entity'::regclass, 'id', 'platform.in_scope(parent_row.scope_path)');

SELECT platform.drop_rls_policies('ledger.fiscal_period'::regclass);

SELECT platform.apply_parent_split_rls('ledger.fiscal_period'::regclass, 'legal_entity_id', 'ledger.legal_entity'::regclass, 'id', 'platform.in_scope(parent_row.scope_path)');

SELECT platform.drop_rls_policies('ledger.inter_entity_obligation'::regclass);

SELECT platform.apply_parent_split_rls('ledger.inter_entity_obligation'::regclass, 'from_legal_entity_id', 'ledger.legal_entity'::regclass, 'id', 'platform.in_scope(parent_row.scope_path)');

SELECT platform.drop_rls_policies('maintenance.asset_document'::regclass);

SELECT platform.apply_parent_rls('maintenance.asset_document'::regclass, 'asset_id', 'maintenance.asset'::regclass, 'id');

SELECT platform.drop_rls_policies('maintenance.asset_status_change'::regclass);

SELECT platform.apply_parent_rls('maintenance.asset_status_change'::regclass, 'asset_id', 'maintenance.asset'::regclass, 'id');

SELECT platform.drop_rls_policies('maintenance.incident_authority_notification'::regclass);

SELECT platform.apply_parent_rls('maintenance.incident_authority_notification'::regclass, 'incident_id', 'maintenance.incident'::regclass, 'id');

SELECT platform.drop_rls_policies('maintenance.incident_history'::regclass);

SELECT platform.apply_parent_rls('maintenance.incident_history'::regclass, 'incident_id', 'maintenance.incident'::regclass, 'id');

SELECT platform.drop_rls_policies('maintenance.incident_investigation_note'::regclass);

SELECT platform.apply_parent_rls('maintenance.incident_investigation_note'::regclass, 'incident_id', 'maintenance.incident'::regclass, 'id');

SELECT platform.drop_rls_policies('maintenance.incident_involved_party'::regclass);

SELECT platform.apply_parent_rls('maintenance.incident_involved_party'::regclass, 'incident_id', 'maintenance.incident'::regclass, 'id');

SELECT platform.drop_rls_policies('maintenance.incident_media'::regclass);

SELECT platform.apply_parent_rls('maintenance.incident_media'::regclass, 'incident_id', 'maintenance.incident'::regclass, 'id');

SELECT platform.drop_rls_policies('marketing.campaign_target'::regclass);

SELECT platform.apply_parent_rls('marketing.campaign_target'::regclass, 'campaign_id', 'marketing.campaign'::regclass, 'id');

SELECT platform.drop_rls_policies('marketing.consent_question_version'::regclass);

SELECT platform.apply_parent_rls('marketing.consent_question_version'::regclass, 'question_id', 'marketing.consent_question'::regclass, 'id');

SELECT platform.drop_rls_policies('marketing.customer_badge'::regclass);

SELECT platform.apply_parent_split_rls('marketing.customer_badge'::regclass, 'badge_id', 'marketing.badge'::regclass, 'id', 'platform.in_scope(parent_row.scope_path)');

SELECT platform.drop_rls_policies('marketing.loyalty_rule'::regclass);

SELECT platform.apply_parent_rls('marketing.loyalty_rule'::regclass, 'campaign_id', 'marketing.campaign'::regclass, 'id');

SELECT platform.drop_rls_policies('marketing.message_dispatch_attempt'::regclass);

SELECT platform.apply_parent_rls('marketing.message_dispatch_attempt'::regclass, 'communication_provider_id', 'marketing.communication_provider'::regclass, 'id');

SELECT platform.drop_rls_policies('marketing.review_response'::regclass);

SELECT platform.apply_parent_rls('marketing.review_response'::regclass, 'review_id', 'marketing.review'::regclass, 'id');

SELECT platform.drop_rls_policies('marketing.reward_assignment'::regclass);

SELECT platform.apply_parent_split_rls('marketing.reward_assignment'::regclass, 'reward_id', 'marketing.reward'::regclass, 'id', 'platform.in_scope(parent_row.scope_path)');

SELECT platform.drop_rls_policies('marketing.waiver_signature'::regclass);

SELECT platform.apply_parent_rls('marketing.waiver_signature'::regclass, 'form_definition_id', 'marketing.form_definition'::regclass, 'id');

SELECT platform.drop_rls_policies('orders.ticket_template_channel'::regclass);

SELECT platform.apply_parent_split_rls('orders.ticket_template_channel'::regclass, 'ticket_template_id', 'orders.ticket_template'::regclass, 'id', 'platform.in_scope(parent_row.scope_path)');

SELECT platform.drop_rls_policies('payments.terminal_certification_level3'::regclass);

SELECT platform.apply_parent_split_rls('payments.terminal_certification_level3'::regclass, 'terminal_certification_id', 'payments.terminal_certification'::regclass, 'id', 'platform.in_scope(parent_row.scope_path)');

SELECT platform.apply_parent_rls('platform.outlet_opening_hour'::regclass, 'outlet_id', 'platform.outlet'::regclass, 'id');

SELECT platform.drop_rls_policies('platform.profile_deployment'::regclass);

SELECT platform.apply_parent_rls('platform.profile_deployment'::regclass, 'profile_id', 'platform.configuration_profile'::regclass, 'id');

SELECT platform.drop_rls_policies('pricing.dynamic_price_action'::regclass);

SELECT platform.apply_parent_rls('pricing.dynamic_price_action'::regclass, 'dynamic_price_rule_id', 'pricing.dynamic_price_rule'::regclass, 'id');

SELECT platform.drop_rls_policies('pricing.dynamic_price_condition'::regclass);

SELECT platform.apply_parent_rls('pricing.dynamic_price_condition'::regclass, 'dynamic_price_rule_id', 'pricing.dynamic_price_rule'::regclass, 'id');

SELECT platform.drop_rls_policies('promotions.coupon_code_batch'::regclass);

SELECT platform.apply_parent_rls('promotions.coupon_code_batch'::regclass, 'campaign_id', 'promotions.campaign'::regclass, 'id');

SELECT platform.drop_rls_policies('promotions.partner_bundle_product'::regclass);

SELECT platform.apply_parent_rls('promotions.partner_bundle_product'::regclass, 'bundle_component_id', 'promotions.bundle_component'::regclass, 'id');

SELECT platform.drop_rls_policies('rental.inspection_item'::regclass);

SELECT platform.apply_parent_rls('rental.inspection_item'::regclass, 'rental_inspection_id', 'rental.inspection'::regclass, 'id');

SELECT platform.drop_rls_policies('reporting.dashboard_tile'::regclass);

SELECT platform.apply_parent_rls('reporting.dashboard_tile'::regclass, 'dashboard_id', 'reporting.dashboard'::regclass, 'id');

SELECT platform.drop_rls_policies('retail.sale'::regclass);

SELECT platform.apply_parent_rls('retail.sale'::regclass, 'outlet_id', 'platform.outlet'::regclass, 'id');

SELECT platform.drop_rls_policies('seating.seat_block_item'::regclass);

SELECT platform.apply_parent_rls('seating.seat_block_item'::regclass, 'block_id', 'seating.seat_block'::regclass, 'id');

SELECT platform.drop_rls_policies('transport.fare_table'::regclass);

SELECT platform.apply_parent_rls('transport.fare_table'::regclass, 'route_id', 'transport.route'::regclass, 'id');

SELECT platform.drop_rls_policies('transport.timetable'::regclass);

SELECT platform.apply_parent_rls('transport.timetable'::regclass, 'route_id', 'transport.route'::regclass, 'id');

SELECT platform.drop_rls_policies('venuemap.map_version'::regclass);

SELECT platform.apply_parent_rls('venuemap.map_version'::regclass, 'map_id', 'venuemap.map'::regclass, 'id');

SELECT platform.drop_rls_policies('venuemap.placed_resource'::regclass);

SELECT platform.apply_parent_rls('venuemap.placed_resource'::regclass, 'map_id', 'venuemap.map'::regclass, 'id');

SELECT platform.drop_rls_policies('workforce.attendance_amendment'::regclass);

SELECT platform.apply_parent_rls('workforce.attendance_amendment'::regclass, 'attendance_record_id', 'workforce.attendance'::regclass, 'id');

SELECT platform.drop_rls_policies('workforce.staff_conversation_participant'::regclass);

SELECT platform.apply_parent_rls('workforce.staff_conversation_participant'::regclass, 'staff_conversation_id', 'workforce.staff_conversation'::regclass, 'id');

SELECT platform.drop_rls_policies('workforce.staff_message'::regclass);

SELECT platform.apply_parent_rls('workforce.staff_message'::regclass, 'staff_conversation_id', 'workforce.staff_conversation'::regclass, 'id');

SELECT platform.drop_rls_policies('ai.index_entry'::regclass);

SELECT platform.apply_parent_split_rls('ai.index_entry'::regclass, 'source_id', 'ai.index_source'::regclass, 'id', 'EXISTS (SELECT 1 FROM ai.knowledge_collection p1 WHERE p1.id = parent_row.collection_id AND (platform.in_scope(p1.scope_path)))');

SELECT platform.drop_rls_policies('ai.index_job'::regclass);

SELECT platform.apply_parent_split_rls('ai.index_job'::regclass, 'source_id', 'ai.index_source'::regclass, 'id', 'EXISTS (SELECT 1 FROM ai.knowledge_collection p1 WHERE p1.id = parent_row.collection_id AND (platform.in_scope(p1.scope_path)))');

SELECT platform.drop_rls_policies('identity.membership_history'::regclass);

SELECT platform.apply_parent_rls('identity.membership_history'::regclass, 'customer_membership_id', 'identity.customer_membership'::regclass, 'id');

SELECT platform.drop_rls_policies('ledger.fiscal_period_event'::regclass);

SELECT platform.apply_parent_split_rls('ledger.fiscal_period_event'::regclass, 'fiscal_period_id', 'ledger.fiscal_period'::regclass, 'id', 'EXISTS (SELECT 1 FROM ledger.legal_entity p1 WHERE p1.id = parent_row.legal_entity_id AND (platform.in_scope(p1.scope_path)))');

SELECT platform.drop_rls_policies('ledger.journal_entry'::regclass);

SELECT platform.apply_parent_split_rls('ledger.journal_entry'::regclass, 'fiscal_period_id', 'ledger.fiscal_period'::regclass, 'id', 'EXISTS (SELECT 1 FROM ledger.legal_entity p1 WHERE p1.id = parent_row.legal_entity_id AND (platform.in_scope(p1.scope_path)))');

SELECT platform.drop_rls_policies('orders.group_participant_list'::regclass);

SELECT platform.apply_parent_rls('orders.group_participant_list'::regclass, 'group_booking_id', 'orders.group_booking'::regclass, 'id');

SELECT platform.drop_rls_policies('orders.group_payment_schedule'::regclass);

SELECT platform.apply_parent_rls('orders.group_payment_schedule'::regclass, 'group_booking_id', 'orders.group_booking'::regclass, 'id');

SELECT platform.drop_rls_policies('orders.group_ticket_allocation'::regclass);

SELECT platform.apply_parent_rls('orders.group_ticket_allocation'::regclass, 'group_booking_id', 'orders.group_booking'::regclass, 'id');

SELECT platform.drop_rls_policies('orders.group_ticket_fulfillment'::regclass);

SELECT platform.apply_parent_rls('orders.group_ticket_fulfillment'::regclass, 'group_booking_id', 'orders.group_booking'::regclass, 'id');

SELECT platform.drop_rls_policies('orders.membership_renewal'::regclass);

SELECT platform.apply_parent_rls('orders.membership_renewal'::regclass, 'customer_membership_id', 'identity.customer_membership'::regclass, 'id');

SELECT platform.drop_rls_policies('platform.sale_board_tile'::regclass);

SELECT platform.apply_parent_rls('platform.sale_board_tile'::regclass, 'sale_board_page_id', 'platform.sale_board_page'::regclass, 'id');

SELECT platform.drop_rls_policies('resources.performance_participant'::regclass);

SELECT platform.apply_parent_rls('resources.performance_participant'::regclass, 'performance_id', 'catalogue.performance'::regclass, 'id');

SELECT platform.drop_rls_policies('retail.exchange'::regclass);

SELECT platform.apply_parent_rls('retail.exchange'::regclass, 'new_sale_id', 'retail.sale'::regclass, 'id');

SELECT platform.drop_rls_policies('retail."return"'::regclass);

SELECT platform.apply_parent_rls('retail."return"'::regclass, 'sale_id', 'retail.sale'::regclass, 'id');

SELECT platform.drop_rls_policies('retail.sale_line'::regclass);

SELECT platform.apply_parent_rls('retail.sale_line'::regclass, 'sale_id', 'retail.sale'::regclass, 'id');

SELECT platform.drop_rls_policies('transport.departure'::regclass);

SELECT platform.apply_parent_rls('transport.departure'::regclass, 'timetable_id', 'transport.timetable'::regclass, 'id');

SELECT platform.drop_rls_policies('transport.fare_matrix_cell'::regclass);

SELECT platform.apply_parent_rls('transport.fare_matrix_cell'::regclass, 'fare_table_id', 'transport.fare_table'::regclass, 'id');

SELECT platform.drop_rls_policies('transport.fare_passenger_type'::regclass);

SELECT platform.apply_parent_rls('transport.fare_passenger_type'::regclass, 'fare_table_id', 'transport.fare_table'::regclass, 'id');

SELECT platform.drop_rls_policies('transport.timetable_run'::regclass);

SELECT platform.apply_parent_rls('transport.timetable_run'::regclass, 'timetable_id', 'transport.timetable'::regclass, 'id');

SELECT platform.drop_rls_policies('fnb.menu_item'::regclass);

SELECT platform.apply_parent_rls('fnb.menu_item'::regclass, 'menu_section_id', 'fnb.menu_section'::regclass, 'id');

SELECT platform.drop_rls_policies('orders.group_participant'::regclass);

SELECT platform.apply_parent_rls('orders.group_participant'::regclass, 'group_participant_list_id', 'orders.group_participant_list'::regclass, 'id');

SELECT platform.drop_rls_policies('orders.group_payment_milestone'::regclass);

SELECT platform.apply_parent_rls('orders.group_payment_milestone'::regclass, 'group_payment_schedule_id', 'orders.group_payment_schedule'::regclass, 'id');

SELECT platform.drop_rls_policies('orders.group_ticket_allocation_line'::regclass);

SELECT platform.apply_parent_rls('orders.group_ticket_allocation_line'::regclass, 'group_ticket_allocation_id', 'orders.group_ticket_allocation'::regclass, 'id');

SELECT platform.drop_rls_policies('retail.return_line'::regclass);

SELECT platform.apply_parent_rls('retail.return_line'::regclass, 'return_id', 'retail."return"'::regclass, 'id');

SELECT platform.drop_rls_policies('fnb.allergen_verdict'::regclass);

SELECT platform.apply_parent_rls('fnb.allergen_verdict'::regclass, 'menu_item_id', 'fnb.menu_item'::regclass, 'id');

SELECT platform.drop_rls_policies('fnb.menu_item_modifier'::regclass);

SELECT platform.apply_parent_rls('fnb.menu_item_modifier'::regclass, 'item_id', 'fnb.menu_item'::regclass, 'id');

SELECT platform.drop_rls_policies('fnb.sold_out_item'::regclass);

SELECT platform.apply_parent_rls('fnb.sold_out_item'::regclass, 'menu_item_id', 'fnb.menu_item'::regclass, 'id');

SELECT platform.drop_rls_policies('fnb.substitution_rule'::regclass);

SELECT platform.apply_parent_rls('fnb.substitution_rule'::regclass, 'recipe_id', 'fnb.recipe'::regclass, 'id');

SELECT platform.drop_rls_policies('identity.role_permission'::regclass);

SELECT platform.apply_parent_split_rls('identity.role_permission'::regclass, 'role_id', 'identity.role'::regclass, 'id', 'platform.tenant_root_in_scope()');

SELECT platform.apply_subject_rls('identity.subject_holding'::regclass);

SELECT platform.apply_tenant_rls('identity.principal_credential_history'::regclass);

SELECT platform.drop_rls_policies('identity.authz_audit'::regclass);

SELECT platform.apply_append_audit_rls('identity.authz_audit'::regclass);

SELECT platform.drop_rls_policies('platform.audit_record'::regclass);

SELECT platform.apply_append_audit_rls('platform.audit_record'::regclass);

INSERT INTO platform.schema_version (version, description, checksum)
VALUES ('V0104', 'after r1 (9cec72d): 3 table(s), 271 column(s), 154 index(es), 29 other statement(s), 204 row-level security polic(ies) re-applied', '23cd158c06e82a9784c99defa8644e5eccdb70411645474aa65c3a6266f96b74')
ON CONFLICT (version) DO NOTHING;

-- ============================================================================
-- ROLLBACK
-- ============================================================================
-- Commented out so that applying this file never runs it: the rollback is run by removing the
-- leading `-- `, and is tested in CI against a restored snapshot (backend/MIGRATIONS.md).
-- SELECT platform.drop_rls_policies('platform.audit_record'::regclass); SELECT platform.apply_tenant_rls('platform.audit_record'::regclass);
-- SELECT platform.drop_rls_policies('identity.authz_audit'::regclass); SELECT platform.apply_tenant_rls('identity.authz_audit'::regclass);
-- SELECT platform.drop_rls_policies('identity.role_permission'::regclass); SELECT platform.apply_tenant_rls('identity.role_permission'::regclass);
-- SELECT platform.drop_rls_policies('fnb.substitution_rule'::regclass); SELECT platform.apply_tenant_rls('fnb.substitution_rule'::regclass);
-- SELECT platform.drop_rls_policies('fnb.sold_out_item'::regclass); SELECT platform.apply_tenant_rls('fnb.sold_out_item'::regclass);
-- SELECT platform.drop_rls_policies('fnb.menu_item_modifier'::regclass); SELECT platform.apply_tenant_rls('fnb.menu_item_modifier'::regclass);
-- SELECT platform.drop_rls_policies('fnb.allergen_verdict'::regclass); SELECT platform.apply_tenant_rls('fnb.allergen_verdict'::regclass);
-- SELECT platform.drop_rls_policies('retail.return_line'::regclass); SELECT platform.apply_tenant_rls('retail.return_line'::regclass);
-- SELECT platform.drop_rls_policies('orders.group_ticket_allocation_line'::regclass); SELECT platform.apply_tenant_rls('orders.group_ticket_allocation_line'::regclass);
-- SELECT platform.drop_rls_policies('orders.group_payment_milestone'::regclass); SELECT platform.apply_tenant_rls('orders.group_payment_milestone'::regclass);
-- SELECT platform.drop_rls_policies('orders.group_participant'::regclass); SELECT platform.apply_tenant_rls('orders.group_participant'::regclass);
-- SELECT platform.drop_rls_policies('fnb.menu_item'::regclass); SELECT platform.apply_parent_rls('fnb.menu_item'::regclass, 'product_variant_id', 'catalogue.variant'::regclass, 'id');
-- SELECT platform.drop_rls_policies('transport.timetable_run'::regclass); SELECT platform.apply_tenant_rls('transport.timetable_run'::regclass);
-- SELECT platform.drop_rls_policies('transport.fare_passenger_type'::regclass); SELECT platform.apply_tenant_rls('transport.fare_passenger_type'::regclass);
-- SELECT platform.drop_rls_policies('transport.fare_matrix_cell'::regclass); SELECT platform.apply_tenant_rls('transport.fare_matrix_cell'::regclass);
-- SELECT platform.drop_rls_policies('transport.departure'::regclass); SELECT platform.apply_tenant_rls('transport.departure'::regclass);
-- SELECT platform.drop_rls_policies('retail.sale_line'::regclass); SELECT platform.apply_tenant_rls('retail.sale_line'::regclass);
-- SELECT platform.drop_rls_policies('retail."return"'::regclass); SELECT platform.apply_tenant_rls('retail."return"'::regclass);
-- SELECT platform.drop_rls_policies('retail.exchange'::regclass); SELECT platform.apply_tenant_rls('retail.exchange'::regclass);
-- SELECT platform.drop_rls_policies('resources.performance_participant'::regclass); SELECT platform.apply_subject_rls('resources.performance_participant'::regclass);
-- SELECT platform.drop_rls_policies('platform.sale_board_tile'::regclass); SELECT platform.apply_tenant_rls('platform.sale_board_tile'::regclass);
-- SELECT platform.drop_rls_policies('orders.membership_renewal'::regclass); SELECT platform.apply_tenant_rls('orders.membership_renewal'::regclass);
-- SELECT platform.drop_rls_policies('orders.group_ticket_fulfillment'::regclass); SELECT platform.apply_tenant_rls('orders.group_ticket_fulfillment'::regclass);
-- SELECT platform.drop_rls_policies('orders.group_ticket_allocation'::regclass); SELECT platform.apply_tenant_rls('orders.group_ticket_allocation'::regclass);
-- SELECT platform.drop_rls_policies('orders.group_payment_schedule'::regclass); SELECT platform.apply_tenant_rls('orders.group_payment_schedule'::regclass);
-- SELECT platform.drop_rls_policies('orders.group_participant_list'::regclass); SELECT platform.apply_tenant_rls('orders.group_participant_list'::regclass);
-- SELECT platform.drop_rls_policies('ledger.journal_entry'::regclass); SELECT platform.apply_parent_rls('ledger.journal_entry'::regclass, 'fiscal_period_id', 'ledger.fiscal_period'::regclass, 'id');
-- SELECT platform.drop_rls_policies('ledger.fiscal_period_event'::regclass); SELECT platform.apply_parent_rls('ledger.fiscal_period_event'::regclass, 'fiscal_period_id', 'ledger.fiscal_period'::regclass, 'id');
-- SELECT platform.drop_rls_policies('identity.membership_history'::regclass); SELECT platform.apply_tenant_rls('identity.membership_history'::regclass);
-- SELECT platform.drop_rls_policies('ai.index_job'::regclass); SELECT platform.apply_parent_rls('ai.index_job'::regclass, 'source_id', 'ai.index_source'::regclass, 'id');
-- SELECT platform.drop_rls_policies('ai.index_entry'::regclass); SELECT platform.apply_parent_rls('ai.index_entry'::regclass, 'source_id', 'ai.index_source'::regclass, 'id');
-- SELECT platform.drop_rls_policies('workforce.staff_message'::regclass); SELECT platform.apply_tenant_rls('workforce.staff_message'::regclass);
-- SELECT platform.drop_rls_policies('workforce.staff_conversation_participant'::regclass); SELECT platform.apply_tenant_rls('workforce.staff_conversation_participant'::regclass);
-- SELECT platform.drop_rls_policies('workforce.attendance_amendment'::regclass); SELECT platform.apply_tenant_rls('workforce.attendance_amendment'::regclass);
-- SELECT platform.drop_rls_policies('venuemap.placed_resource'::regclass); SELECT platform.apply_parent_rls('venuemap.placed_resource'::regclass, 'resource_id', 'resources.resource'::regclass, 'id');
-- SELECT platform.drop_rls_policies('venuemap.map_version'::regclass); SELECT platform.apply_tenant_rls('venuemap.map_version'::regclass);
-- SELECT platform.drop_rls_policies('transport.timetable'::regclass); SELECT platform.apply_tenant_rls('transport.timetable'::regclass);
-- SELECT platform.drop_rls_policies('transport.fare_table'::regclass); SELECT platform.apply_tenant_rls('transport.fare_table'::regclass);
-- SELECT platform.drop_rls_policies('seating.seat_block_item'::regclass); SELECT platform.apply_tenant_rls('seating.seat_block_item'::regclass);
-- SELECT platform.drop_rls_policies('retail.sale'::regclass); SELECT platform.apply_subject_rls('retail.sale'::regclass);
-- SELECT platform.drop_rls_policies('reporting.dashboard_tile'::regclass); SELECT platform.apply_tenant_rls('reporting.dashboard_tile'::regclass);
-- SELECT platform.drop_rls_policies('rental.inspection_item'::regclass); SELECT platform.apply_tenant_rls('rental.inspection_item'::regclass);
-- SELECT platform.drop_rls_policies('promotions.partner_bundle_product'::regclass); SELECT platform.apply_tenant_rls('promotions.partner_bundle_product'::regclass);
-- SELECT platform.drop_rls_policies('promotions.coupon_code_batch'::regclass); SELECT platform.apply_tenant_rls('promotions.coupon_code_batch'::regclass);
-- SELECT platform.drop_rls_policies('pricing.dynamic_price_condition'::regclass); SELECT platform.apply_tenant_rls('pricing.dynamic_price_condition'::regclass);
-- SELECT platform.drop_rls_policies('pricing.dynamic_price_action'::regclass); SELECT platform.apply_tenant_rls('pricing.dynamic_price_action'::regclass);
-- SELECT platform.drop_rls_policies('platform.profile_deployment'::regclass); SELECT platform.apply_tenant_rls('platform.profile_deployment'::regclass);
-- SELECT platform.drop_rls_policies('payments.terminal_certification_level3'::regclass); SELECT platform.apply_parent_rls('payments.terminal_certification_level3'::regclass, 'terminal_certification_id', 'payments.terminal_certification'::regclass, 'id');
-- SELECT platform.drop_rls_policies('orders.ticket_template_channel'::regclass); SELECT platform.apply_tenant_rls('orders.ticket_template_channel'::regclass);
-- SELECT platform.drop_rls_policies('marketing.waiver_signature'::regclass); SELECT platform.apply_tenant_rls('marketing.waiver_signature'::regclass);
-- SELECT platform.drop_rls_policies('marketing.reward_assignment'::regclass); SELECT platform.apply_tenant_rls('marketing.reward_assignment'::regclass);
-- SELECT platform.drop_rls_policies('marketing.review_response'::regclass); SELECT platform.apply_tenant_rls('marketing.review_response'::regclass);
-- SELECT platform.drop_rls_policies('marketing.message_dispatch_attempt'::regclass); SELECT platform.apply_tenant_rls('marketing.message_dispatch_attempt'::regclass);
-- SELECT platform.drop_rls_policies('marketing.loyalty_rule'::regclass); SELECT platform.apply_tenant_rls('marketing.loyalty_rule'::regclass);
-- SELECT platform.drop_rls_policies('marketing.customer_badge'::regclass); SELECT platform.apply_tenant_rls('marketing.customer_badge'::regclass);
-- SELECT platform.drop_rls_policies('marketing.consent_question_version'::regclass); SELECT platform.apply_tenant_rls('marketing.consent_question_version'::regclass);
-- SELECT platform.drop_rls_policies('marketing.campaign_target'::regclass); SELECT platform.apply_tenant_rls('marketing.campaign_target'::regclass);
-- SELECT platform.drop_rls_policies('maintenance.incident_media'::regclass); SELECT platform.apply_tenant_rls('maintenance.incident_media'::regclass);
-- SELECT platform.drop_rls_policies('maintenance.incident_involved_party'::regclass); SELECT platform.apply_subject_rls('maintenance.incident_involved_party'::regclass);
-- SELECT platform.drop_rls_policies('maintenance.incident_investigation_note'::regclass); SELECT platform.apply_tenant_rls('maintenance.incident_investigation_note'::regclass);
-- SELECT platform.drop_rls_policies('maintenance.incident_history'::regclass); SELECT platform.apply_tenant_rls('maintenance.incident_history'::regclass);
-- SELECT platform.drop_rls_policies('maintenance.incident_authority_notification'::regclass); SELECT platform.apply_tenant_rls('maintenance.incident_authority_notification'::regclass);
-- SELECT platform.drop_rls_policies('maintenance.asset_status_change'::regclass); SELECT platform.apply_tenant_rls('maintenance.asset_status_change'::regclass);
-- SELECT platform.drop_rls_policies('maintenance.asset_document'::regclass); SELECT platform.apply_tenant_rls('maintenance.asset_document'::regclass);
-- SELECT platform.drop_rls_policies('ledger.inter_entity_obligation'::regclass); SELECT platform.apply_tenant_rls('ledger.inter_entity_obligation'::regclass);
-- SELECT platform.drop_rls_policies('ledger.fiscal_period'::regclass); SELECT platform.apply_parent_rls('ledger.fiscal_period'::regclass, 'legal_entity_id', 'ledger.legal_entity'::regclass, 'id');
-- SELECT platform.drop_rls_policies('ledger.account'::regclass); SELECT platform.apply_parent_rls('ledger.account'::regclass, 'legal_entity_id', 'ledger.legal_entity'::regclass, 'id');
-- SELECT platform.drop_rls_policies('inventory.supplier_contract'::regclass); SELECT platform.apply_tenant_rls('inventory.supplier_contract'::regclass);
-- SELECT platform.drop_rls_policies('inventory.quotation_line'::regclass); SELECT platform.apply_tenant_rls('inventory.quotation_line'::regclass);
-- SELECT platform.drop_rls_policies('inventory.count'::regclass); SELECT platform.apply_tenant_rls('inventory.count'::regclass);
-- SELECT platform.drop_rls_policies('identity.customer_membership'::regclass); SELECT platform.apply_tenant_rls('identity.customer_membership'::regclass);
-- SELECT platform.drop_rls_policies('identity.benefit_usage'::regclass); SELECT platform.apply_tenant_rls('identity.benefit_usage'::regclass);
-- SELECT platform.drop_rls_policies('fnb.reservation_table'::regclass); SELECT platform.apply_tenant_rls('fnb.reservation_table'::regclass);
-- SELECT platform.drop_rls_policies('fnb.production_plan_line'::regclass); SELECT platform.apply_tenant_rls('fnb.production_plan_line'::regclass);
-- SELECT platform.drop_rls_policies('fnb.kitchen_sla'::regclass); SELECT platform.apply_tenant_rls('fnb.kitchen_sla'::regclass);
-- SELECT platform.drop_rls_policies('fnb.combo_slot_option'::regclass); SELECT platform.apply_tenant_rls('fnb.combo_slot_option'::regclass);
-- SELECT platform.drop_rls_policies('catalogue.product_media'::regclass); SELECT platform.apply_tenant_rls('catalogue.product_media'::regclass);
-- SELECT platform.drop_rls_policies('assets.media_collection_member'::regclass); SELECT platform.apply_tenant_rls('assets.media_collection_member'::regclass);
-- SELECT platform.drop_rls_policies('ai.index_source'::regclass); SELECT platform.apply_parent_rls('ai.index_source'::regclass, 'collection_id', 'ai.knowledge_collection'::regclass, 'id');
-- SELECT platform.drop_rls_policies('ai.chunk_embedding'::regclass); SELECT platform.apply_parent_rls('ai.chunk_embedding'::regclass, 'document_id', 'ai.knowledge_document'::regclass, 'id');
-- SELECT platform.drop_rls_policies('access.entry_rule_point'::regclass); SELECT platform.apply_parent_rls('access.entry_rule_point'::regclass, 'admission_profile_id', 'access.admission_rules'::regclass, 'id');
-- SELECT platform.drop_rls_policies('access.access_change'::regclass); SELECT platform.apply_tenant_rls('access.access_change'::regclass);
-- SELECT platform.drop_rls_policies('workforce.training_record'::regclass); SELECT platform.apply_tenant_rls('workforce.training_record'::regclass);
-- SELECT platform.drop_rls_policies('whitelabel.promo_block'::regclass); SELECT platform.apply_scope_rls('whitelabel.promo_block'::regclass);
-- SELECT platform.drop_rls_policies('whitelabel.homepage_section'::regclass); SELECT platform.apply_tenant_rls('whitelabel.homepage_section'::regclass);
-- SELECT platform.drop_rls_policies('whitelabel.content_page'::regclass); SELECT platform.apply_scope_rls('whitelabel.content_page'::regclass);
-- SELECT platform.drop_rls_policies('whitelabel.config_version'::regclass); SELECT platform.apply_scope_rls('whitelabel.config_version'::regclass);
-- SELECT platform.drop_rls_policies('whitelabel.booking_flow_step'::regclass); SELECT platform.apply_tenant_rls('whitelabel.booking_flow_step'::regclass);
-- SELECT platform.drop_rls_policies('whitelabel.banner'::regclass); SELECT platform.apply_tenant_rls('whitelabel.banner'::regclass);
-- SELECT platform.drop_rls_policies('wallet.wallet'::regclass); SELECT platform.apply_subject_rls('wallet.wallet'::regclass);
-- SELECT platform.drop_rls_policies('wallet.gift_card'::regclass); SELECT platform.apply_subject_rls('wallet.gift_card'::regclass);
-- SELECT platform.drop_rls_policies('wallet.credit_type'::regclass); SELECT platform.apply_scope_rls('wallet.credit_type'::regclass);
-- SELECT platform.drop_rls_policies('wallet.balance'::regclass); SELECT platform.apply_tenant_rls('wallet.balance'::regclass);
-- SELECT platform.drop_rls_policies('wallet.accounting_mapping'::regclass); SELECT platform.apply_scope_rls('wallet.accounting_mapping'::regclass);
-- SELECT platform.drop_rls_policies('venuemap.import_job'::regclass); SELECT platform.apply_tenant_rls('venuemap.import_job'::regclass);
-- SELECT platform.drop_rls_policies('seating.seat_price_band'::regclass); SELECT platform.apply_tenant_rls('seating.seat_price_band'::regclass);
-- SELECT platform.drop_rls_policies('seating.seat'::regclass); SELECT platform.apply_tenant_rls('seating.seat'::regclass);
-- SELECT platform.drop_rls_policies('resources.resource_type'::regclass); SELECT platform.apply_scope_rls('resources.resource_type'::regclass);
-- SELECT platform.drop_rls_policies('resources.resource_category'::regclass); SELECT platform.apply_scope_rls('resources.resource_category'::regclass);
-- SELECT platform.drop_rls_policies('resources.attribute_definition'::regclass); SELECT platform.apply_scope_rls('resources.attribute_definition'::regclass);
-- SELECT platform.drop_rls_policies('reporting.semantic_model'::regclass); SELECT platform.apply_scope_rls('reporting.semantic_model'::regclass);
-- SELECT platform.drop_rls_policies('reporting.kpi_definition'::regclass); SELECT platform.apply_scope_rls('reporting.kpi_definition'::regclass);
-- SELECT platform.drop_rls_policies('rental.participant'::regclass); SELECT platform.apply_tenant_rls('rental.participant'::regclass);
-- SELECT platform.drop_rls_policies('promotions.upsell_rule'::regclass); SELECT platform.apply_tenant_rls('promotions.upsell_rule'::regclass);
-- SELECT platform.drop_rls_policies('promotions.promotion_variant'::regclass); SELECT platform.apply_tenant_rls('promotions.promotion_variant'::regclass);
-- SELECT platform.drop_rls_policies('platform.region_settings'::regclass); SELECT platform.apply_tenant_rls('platform.region_settings'::regclass);
-- SELECT platform.drop_rls_policies('platform.device'::regclass); SELECT platform.apply_tenant_rls('platform.device'::regclass);
-- SELECT platform.drop_rls_policies('platform.denomination'::regclass); SELECT platform.apply_tenant_rls('platform.denomination'::regclass);
-- SELECT platform.drop_rls_policies('pii.subject_contact'::regclass); SELECT platform.apply_subject_rls('pii.subject_contact'::regclass);
-- SELECT platform.drop_rls_policies('pii.subject'::regclass); SELECT platform.apply_tenant_rls('pii.subject'::regclass);
-- SELECT platform.drop_rls_policies('payments.token'::regclass); SELECT platform.apply_subject_rls('payments.token'::regclass);
-- SELECT platform.drop_rls_policies('payments.terminal_certification'::regclass); SELECT platform.apply_scope_rls('payments.terminal_certification'::regclass);
-- SELECT platform.drop_rls_policies('payments.provider_connection'::regclass); SELECT platform.apply_scope_rls('payments.provider_connection'::regclass);
-- SELECT platform.drop_rls_policies('payments.instalment_policy'::regclass); SELECT platform.apply_scope_rls('payments.instalment_policy'::regclass);
-- SELECT platform.drop_rls_policies('payments.fee_rule'::regclass); SELECT platform.apply_tenant_rls('payments.fee_rule'::regclass);
-- SELECT platform.drop_rls_policies('payments.deposit_activity'::regclass); SELECT platform.apply_tenant_rls('payments.deposit_activity'::regclass);
-- SELECT platform.drop_rls_policies('orders.ticket_template'::regclass); SELECT platform.apply_tenant_rls('orders.ticket_template'::regclass);
-- SELECT platform.drop_rls_policies('orders.refund_calculation_policy'::regclass); SELECT platform.apply_tenant_rls('orders.refund_calculation_policy'::regclass);
-- SELECT platform.drop_rls_policies('orders.membership_migration'::regclass); SELECT platform.apply_tenant_rls('orders.membership_migration'::regclass);
-- SELECT platform.drop_rls_policies('orders.membership_activation_action'::regclass); SELECT platform.apply_subject_rls('orders.membership_activation_action'::regclass);
-- SELECT platform.drop_rls_policies('orders.member_exception'::regclass); SELECT platform.apply_tenant_rls('orders.member_exception'::regclass);
-- SELECT platform.drop_rls_policies('orders.invitation_allowance'::regclass); SELECT platform.apply_tenant_rls('orders.invitation_allowance'::regclass);
-- SELECT platform.drop_rls_policies('orders.group_enquiry'::regclass); SELECT platform.apply_tenant_rls('orders.group_enquiry'::regclass);
-- SELECT platform.drop_rls_policies('orders.fraud_rule'::regclass); SELECT platform.apply_scope_rls('orders.fraud_rule'::regclass);
-- SELECT platform.drop_rls_policies('marketing.tracking_technology_catalogue'::regclass); SELECT platform.apply_scope_rls('marketing.tracking_technology_catalogue'::regclass);
-- SELECT platform.drop_rls_policies('marketing.touch_point'::regclass); SELECT platform.apply_subject_rls('marketing.touch_point'::regclass);
-- SELECT platform.drop_rls_policies('marketing.suppression'::regclass); SELECT platform.apply_scope_rls('marketing.suppression'::regclass);
-- SELECT platform.drop_rls_policies('marketing.reward'::regclass); SELECT platform.apply_tenant_rls('marketing.reward'::regclass);
-- SELECT platform.drop_rls_policies('marketing.retention_policy'::regclass); SELECT platform.apply_scope_rls('marketing.retention_policy'::regclass);
-- SELECT platform.drop_rls_policies('marketing.privacy_incident'::regclass); SELECT platform.apply_scope_rls('marketing.privacy_incident'::regclass);
-- SELECT platform.drop_rls_policies('marketing.privacy_audit_event'::regclass); SELECT platform.apply_subject_rls('marketing.privacy_audit_event'::regclass);
-- SELECT platform.drop_rls_policies('marketing.points_redemption_rule'::regclass); SELECT platform.apply_tenant_rls('marketing.points_redemption_rule'::regclass);
-- SELECT platform.drop_rls_policies('marketing.message_template'::regclass); SELECT platform.apply_tenant_rls('marketing.message_template'::regclass);
-- SELECT platform.drop_rls_policies('marketing.message_dispatch'::regclass); SELECT platform.apply_subject_rls('marketing.message_dispatch'::regclass);
-- SELECT platform.drop_rls_policies('marketing.loyalty_points'::regclass); SELECT platform.apply_tenant_rls('marketing.loyalty_points'::regclass);
-- SELECT platform.drop_rls_policies('marketing.loyalty_campaign'::regclass); SELECT platform.apply_tenant_rls('marketing.loyalty_campaign'::regclass);
-- SELECT platform.drop_rls_policies('marketing.guest_preference'::regclass); SELECT platform.apply_subject_rls('marketing.guest_preference'::regclass);
-- SELECT platform.drop_rls_policies('marketing.guest_extra_value'::regclass); SELECT platform.apply_tenant_rls('marketing.guest_extra_value'::regclass);
-- SELECT platform.drop_rls_policies('marketing.guest_extra_option'::regclass); SELECT platform.apply_tenant_rls('marketing.guest_extra_option'::regclass);
-- SELECT platform.drop_rls_policies('marketing.guest_document'::regclass); SELECT platform.apply_subject_rls('marketing.guest_document'::regclass);
-- SELECT platform.drop_rls_policies('marketing.form_submission'::regclass); SELECT platform.apply_subject_rls('marketing.form_submission'::regclass);
-- SELECT platform.drop_rls_policies('marketing.consent_record_channel'::regclass); SELECT platform.apply_tenant_rls('marketing.consent_record_channel'::regclass);
-- SELECT platform.drop_rls_policies('marketing.consent_record'::regclass); SELECT platform.apply_subject_rls('marketing.consent_record'::regclass);
-- SELECT platform.drop_rls_policies('marketing.consent_purpose_channel'::regclass); SELECT platform.apply_tenant_rls('marketing.consent_purpose_channel'::regclass);
-- SELECT platform.drop_rls_policies('marketing.consent_purpose'::regclass); SELECT platform.apply_tenant_rls('marketing.consent_purpose'::regclass);
-- SELECT platform.drop_rls_policies('marketing.case_message'::regclass); SELECT platform.apply_tenant_rls('marketing.case_message'::regclass);
-- SELECT platform.drop_rls_policies('marketing.badge'::regclass); SELECT platform.apply_tenant_rls('marketing.badge'::regclass);
-- SELECT platform.drop_rls_policies('marketing.audience_list'::regclass); SELECT platform.apply_scope_rls('marketing.audience_list'::regclass);
-- SELECT platform.drop_rls_policies('marketing.agent_availability'::regclass); SELECT platform.apply_tenant_rls('marketing.agent_availability'::regclass);
-- SELECT platform.drop_rls_policies('maintenance.asset_category'::regclass); SELECT platform.apply_scope_rls('maintenance.asset_category'::regclass);
-- SELECT platform.drop_rls_policies('ledger.tax_exemption'::regclass); SELECT platform.apply_tenant_rls('ledger.tax_exemption'::regclass);
-- SELECT platform.drop_rls_policies('ledger.tax_code'::regclass); SELECT platform.apply_tenant_rls('ledger.tax_code'::regclass);
-- SELECT platform.drop_rls_policies('ledger.recognition_schedule'::regclass); SELECT platform.apply_tenant_rls('ledger.recognition_schedule'::regclass);
-- SELECT platform.drop_rls_policies('ledger.legal_entity'::regclass); SELECT platform.apply_scope_rls('ledger.legal_entity'::regclass);
-- SELECT platform.drop_rls_policies('ledger.deposit'::regclass); SELECT platform.apply_subject_rls('ledger.deposit'::regclass);
-- SELECT platform.drop_rls_policies('inventory.supplier'::regclass); SELECT platform.apply_scope_rls('inventory.supplier'::regclass);
-- SELECT platform.drop_rls_policies('inventory.stock_batch'::regclass); SELECT platform.apply_tenant_rls('inventory.stock_batch'::regclass);
-- SELECT platform.drop_rls_policies('identity.segregation_rule'::regclass); SELECT platform.apply_scope_rls('identity.segregation_rule'::regclass);
-- SELECT platform.drop_rls_policies('identity.role'::regclass); SELECT platform.apply_tenant_rls('identity.role'::regclass);
-- SELECT platform.drop_rls_policies('identity.principal'::regclass); SELECT platform.apply_tenant_rls('identity.principal'::regclass);
-- SELECT platform.drop_rls_policies('identity.password_policy'::regclass); SELECT platform.apply_scope_rls('identity.password_policy'::regclass);
-- SELECT platform.drop_rls_policies('identity.capability_template'::regclass); SELECT platform.apply_scope_rls('identity.capability_template'::regclass);
-- SELECT platform.drop_rls_policies('games.reader_deployment'::regclass); SELECT platform.apply_tenant_rls('games.reader_deployment'::regclass);
-- SELECT platform.drop_rls_policies('games.play'::regclass); SELECT platform.apply_tenant_rls('games.play'::regclass);
-- SELECT platform.drop_rls_policies('games.attraction_type'::regclass); SELECT platform.apply_scope_rls('games.attraction_type'::regclass);
-- SELECT platform.drop_rls_policies('fnb.temperature_log'::regclass); SELECT platform.apply_tenant_rls('fnb.temperature_log'::regclass);
-- SELECT platform.drop_rls_policies('fnb.production_plan'::regclass); SELECT platform.apply_tenant_rls('fnb.production_plan'::regclass);
-- SELECT platform.drop_rls_policies('fnb.kitchen_station'::regclass); SELECT platform.apply_tenant_rls('fnb.kitchen_station'::regclass);
-- SELECT platform.drop_rls_policies('fnb.kitchen_exception'::regclass); SELECT platform.apply_tenant_rls('fnb.kitchen_exception'::regclass);
-- SELECT platform.drop_rls_policies('fnb.dining_table'::regclass); SELECT platform.apply_tenant_rls('fnb.dining_table'::regclass);
-- SELECT platform.drop_rls_policies('fnb.delivery_location_outlet'::regclass); SELECT platform.apply_tenant_rls('fnb.delivery_location_outlet'::regclass);
-- SELECT platform.drop_rls_policies('fnb.combo_slot'::regclass); SELECT platform.apply_tenant_rls('fnb.combo_slot'::regclass);
-- SELECT platform.drop_rls_policies('fnb.combo'::regclass); SELECT platform.apply_tenant_rls('fnb.combo'::regclass);
-- SELECT platform.drop_rls_policies('fnb.cold_chain_event'::regclass); SELECT platform.apply_tenant_rls('fnb.cold_chain_event'::regclass);
-- SELECT platform.drop_rls_policies('catalogue.signal_registry'::regclass); SELECT platform.apply_scope_rls('catalogue.signal_registry'::regclass);
-- SELECT platform.drop_rls_policies('catalogue.rounding_profile'::regclass); SELECT platform.apply_scope_rls('catalogue.rounding_profile'::regclass);
-- SELECT platform.drop_rls_policies('catalogue.pricing_market'::regclass); SELECT platform.apply_scope_rls('catalogue.pricing_market'::regclass);
-- SELECT platform.drop_rls_policies('catalogue.price_category'::regclass); SELECT platform.apply_scope_rls('catalogue.price_category'::regclass);
-- SELECT platform.drop_rls_policies('catalogue.membership_programme'::regclass); SELECT platform.apply_tenant_rls('catalogue.membership_programme'::regclass);
-- SELECT platform.drop_rls_policies('catalogue.membership_benefit'::regclass); SELECT platform.apply_tenant_rls('catalogue.membership_benefit'::regclass);
-- SELECT platform.drop_rls_policies('catalogue.event_type'::regclass); SELECT platform.apply_scope_rls('catalogue.event_type'::regclass);
-- SELECT platform.drop_rls_policies('catalogue.alternative_code'::regclass); SELECT platform.apply_tenant_rls('catalogue.alternative_code'::regclass);
-- SELECT platform.drop_rls_policies('assets.taxonomy'::regclass); SELECT platform.apply_scope_rls('assets.taxonomy'::regclass);
-- SELECT platform.drop_rls_policies('assets.distribution_channel'::regclass); SELECT platform.apply_scope_rls('assets.distribution_channel'::regclass);
-- SELECT platform.drop_rls_policies('approvals.step_up_policy'::regclass); SELECT platform.apply_tenant_rls('approvals.step_up_policy'::regclass);
-- SELECT platform.drop_rls_policies('approvals.sla_policy'::regclass); SELECT platform.apply_scope_rls('approvals.sla_policy'::regclass);
-- SELECT platform.drop_rls_policies('approvals.external_provider'::regclass); SELECT platform.apply_scope_rls('approvals.external_provider'::regclass);
-- SELECT platform.drop_rls_policies('approvals.control_policy'::regclass); SELECT platform.apply_scope_rls('approvals.control_policy'::regclass);
-- SELECT platform.drop_rls_policies('approvals.accreditation_badge'::regclass); SELECT platform.apply_tenant_rls('approvals.accreditation_badge'::regclass);
-- SELECT platform.drop_rls_policies('ai.tool'::regclass); SELECT platform.apply_scope_rls('ai.tool'::regclass);
-- SELECT platform.drop_rls_policies('ai.release'::regclass); SELECT platform.apply_scope_rls('ai.release'::regclass);
-- SELECT platform.drop_rls_policies('ai.prompt_template'::regclass); SELECT platform.apply_scope_rls('ai.prompt_template'::regclass);
-- SELECT platform.drop_rls_policies('ai.policy_exception'::regclass); SELECT platform.apply_scope_rls('ai.policy_exception'::regclass);
-- SELECT platform.drop_rls_policies('ai.policy'::regclass); SELECT platform.apply_scope_rls('ai.policy'::regclass);
-- SELECT platform.drop_rls_policies('ai.model'::regclass); SELECT platform.apply_scope_rls('ai.model'::regclass);
-- SELECT platform.drop_rls_policies('ai.knowledge_document'::regclass); SELECT platform.apply_scope_rls('ai.knowledge_document'::regclass);
-- SELECT platform.drop_rls_policies('ai.knowledge_collection'::regclass); SELECT platform.apply_scope_rls('ai.knowledge_collection'::regclass);
-- SELECT platform.drop_rls_policies('ai.governance_policy_version'::regclass); SELECT platform.apply_scope_rls('ai.governance_policy_version'::regclass);
-- SELECT platform.drop_rls_policies('ai.governance_policy'::regclass); SELECT platform.apply_scope_rls('ai.governance_policy'::regclass);
-- SELECT platform.drop_rls_policies('ai.config_source'::regclass); SELECT platform.apply_tenant_rls('ai.config_source'::regclass);
-- SELECT platform.drop_rls_policies('ai.capability'::regclass); SELECT platform.apply_scope_rls('ai.capability'::regclass);
-- SELECT platform.drop_rls_policies('ai.assistant_profile'::regclass); SELECT platform.apply_scope_rls('ai.assistant_profile'::regclass);
-- SELECT platform.drop_rls_policies('access.hardware_model'::regclass); SELECT platform.apply_scope_rls('access.hardware_model'::regclass);
-- SELECT platform.drop_rls_policies('orders.invitation'::regclass); SELECT platform.apply_parent_rls('orders.invitation'::regclass, 'product_id', 'catalogue.product'::regclass, 'id');
-- DROP INDEX IF EXISTS promotions.upsell_rule_scope_path_idx;
-- DROP INDEX IF EXISTS orders.ticket_template_scope_path_idx;
-- DROP INDEX IF EXISTS fnb.temperature_log_scope_path_idx;
-- DROP INDEX IF EXISTS ledger.tax_exemption_scope_path_idx;
-- DROP INDEX IF EXISTS ledger.tax_code_scope_path_idx;
-- DROP INDEX IF EXISTS seating.seat_scope_path_idx;
-- DROP INDEX IF EXISTS seating.seat_price_band_scope_path_idx;
-- DROP INDEX IF EXISTS marketing.reward_scope_path_idx;
-- DROP INDEX IF EXISTS platform.region_settings_scope_path_idx;
-- DROP INDEX IF EXISTS orders.refund_calculation_policy_scope_path_idx;
-- DROP INDEX IF EXISTS ledger.recognition_schedule_scope_path_idx;
-- DROP INDEX IF EXISTS games.reader_deployment_scope_path_idx;
-- DROP INDEX IF EXISTS promotions.promotion_variant_scope_path_idx;
-- DROP INDEX IF EXISTS fnb.production_plan_scope_path_idx;
-- DROP INDEX IF EXISTS marketing.points_redemption_rule_scope_path_idx;
-- DROP INDEX IF EXISTS games.play_scope_path_idx;
-- DROP INDEX IF EXISTS rental.participant_scope_path_idx;
-- DROP INDEX IF EXISTS catalogue.membership_programme_scope_path_idx;
-- DROP INDEX IF EXISTS orders.membership_migration_scope_path_idx;
-- DROP INDEX IF EXISTS catalogue.membership_benefit_scope_path_idx;
-- DROP INDEX IF EXISTS orders.member_exception_scope_path_idx;
-- DROP INDEX IF EXISTS marketing.loyalty_points_scope_path_idx;
-- DROP INDEX IF EXISTS marketing.loyalty_campaign_scope_path_idx;
-- DROP INDEX IF EXISTS fnb.kitchen_station_scope_path_idx;
-- DROP INDEX IF EXISTS fnb.kitchen_exception_scope_path_idx;
-- DROP INDEX IF EXISTS orders.invitation_scope_path_idx;
-- DROP INDEX IF EXISTS orders.invitation_allowance_scope_path_idx;
-- DROP INDEX IF EXISTS venuemap.import_job_scope_path_idx;
-- DROP INDEX IF EXISTS marketing.guest_extra_value_scope_path_idx;
-- DROP INDEX IF EXISTS marketing.guest_extra_option_scope_path_idx;
-- DROP INDEX IF EXISTS orders.group_enquiry_scope_path_idx;
-- DROP INDEX IF EXISTS payments.fee_rule_scope_path_idx;
-- DROP INDEX IF EXISTS fnb.dining_table_scope_path_idx;
-- DROP INDEX IF EXISTS platform.device_scope_path_idx;
-- DROP INDEX IF EXISTS payments.deposit_activity_scope_path_idx;
-- DROP INDEX IF EXISTS platform.denomination_scope_path_idx;
-- DROP INDEX IF EXISTS ai.config_source_scope_path_idx;
-- DROP INDEX IF EXISTS fnb.combo_slot_scope_path_idx;
-- DROP INDEX IF EXISTS fnb.combo_scope_path_idx;
-- DROP INDEX IF EXISTS fnb.cold_chain_event_scope_path_idx;
-- DROP INDEX IF EXISTS marketing.case_message_scope_path_idx;
-- DROP INDEX IF EXISTS whitelabel.booking_flow_step_scope_path_idx;
-- DROP INDEX IF EXISTS marketing.badge_scope_path_idx;
-- DROP INDEX IF EXISTS catalogue.alternative_code_scope_path_idx;
-- DROP INDEX IF EXISTS approvals.accreditation_badge_scope_path_idx;
-- DROP INDEX IF EXISTS seating.seat_price_band_seat_category_id_code_uniq; CREATE UNIQUE INDEX IF NOT EXISTS seat_price_band_seat_category_id_code_uniq ON seating.seat_price_band (seat_category_id, code);
-- DROP INDEX IF EXISTS seating.seat_seat_map_id_section_code_row_label_seat_number_uniq; CREATE UNIQUE INDEX IF NOT EXISTS seat_seat_map_id_section_code_row_label_seat_number_uniq ON seating.seat (seat_map_id, section_code, row_label, seat_number);
-- DROP INDEX IF EXISTS marketing.wishlist_item_subject_id_variant_id_performance_id_uniq;
-- DROP INDEX IF EXISTS marketing.guest_device_subject_id_token_fingerprint_uniq;
-- DROP INDEX IF EXISTS marketing.guest_device_subject_id_installation_id_uniq;
-- DROP INDEX IF EXISTS identity.subject_holding_holding_kind_holding_id_uniq;
-- DROP INDEX IF EXISTS identity.principal_credential_principal_id_method_uniq;
-- DROP INDEX IF EXISTS games.credit_ledger_play_id_uniq;
-- DROP INDEX IF EXISTS ai.index_entry_source_id_record_key_uniq;
-- DROP INDEX IF EXISTS transport.station_venue_id_code_uniq; CREATE UNIQUE INDEX IF NOT EXISTS station_venue_id_code_uniq ON transport.station (venue_id, code);
-- DROP INDEX IF EXISTS transport.route_venue_id_code_uniq; CREATE UNIQUE INDEX IF NOT EXISTS route_venue_id_code_uniq ON transport.route (venue_id, code);
-- DROP INDEX IF EXISTS transport.pass_type_venue_id_code_uniq; CREATE UNIQUE INDEX IF NOT EXISTS pass_type_venue_id_code_uniq ON transport.pass_type (venue_id, code);
-- DROP INDEX IF EXISTS seating.seat_category_venue_id_code_uniq; CREATE UNIQUE INDEX IF NOT EXISTS seat_category_venue_id_code_uniq ON seating.seat_category (venue_id, code);
-- DROP INDEX IF EXISTS resources.resource_venue_id_code_uniq;
-- DROP INDEX IF EXISTS queue.queue_venue_id_code_uniq;
-- DROP INDEX IF EXISTS promotions.campaign_venue_id_code_uniq;
-- DROP INDEX IF EXISTS platform.sale_board_venue_id_code_uniq;
-- DROP INDEX IF EXISTS platform.outlet_venue_id_code_uniq;
-- DROP INDEX IF EXISTS maintenance.asset_venue_id_asset_tag_uniq; CREATE UNIQUE INDEX IF NOT EXISTS asset_venue_id_asset_tag_uniq ON maintenance.asset (venue_id, asset_tag);
-- DROP INDEX IF EXISTS inventory.location_venue_id_code_uniq;
-- DROP INDEX IF EXISTS games.game_venue_id_code_uniq;
-- DROP INDEX IF EXISTS fnb.outlet_template_scope_path_code_uniq; CREATE UNIQUE INDEX IF NOT EXISTS outlet_template_scope_path_code_uniq ON fnb.outlet_template (scope_path, code);
-- DROP INDEX IF EXISTS fnb.modifier_group_scope_path_code_uniq;
-- DROP INDEX IF EXISTS fnb.dining_table_scope_path_label_uniq;
-- DROP INDEX IF EXISTS fnb.delivery_location_venue_id_label_uniq;
-- DROP INDEX IF EXISTS catalogue.product_venue_id_family_key_uniq; CREATE UNIQUE INDEX IF NOT EXISTS product_venue_id_family_key_uniq ON catalogue.product (venue_id, family_key) WHERE family_key IS NOT NULL;
-- DROP INDEX IF EXISTS access.access_point_venue_id_code_uniq;
-- DROP INDEX IF EXISTS whitelabel.content_page_slug_uniq;
-- DROP INDEX IF EXISTS wallet.wallet_type_code_uniq;
-- DROP INDEX IF EXISTS wallet.voucher_type_code_uniq;
-- DROP INDEX IF EXISTS wallet.credit_type_code_uniq;
-- DROP INDEX IF EXISTS tenancy.data_retention_setting_data_class_uniq; CREATE UNIQUE INDEX IF NOT EXISTS data_retention_setting_data_class_uniq ON tenancy.data_retention_setting (data_class);
-- DROP INDEX IF EXISTS subscription.plan_code_uniq;
-- DROP INDEX IF EXISTS resources.resource_type_code_uniq;
-- DROP INDEX IF EXISTS resources.resource_package_code_uniq;
-- DROP INDEX IF EXISTS resources.resource_category_code_uniq;
-- DROP INDEX IF EXISTS resources.attribute_definition_code_uniq;
-- DROP INDEX IF EXISTS reporting.kpi_definition_code_uniq;
-- DROP INDEX IF EXISTS rental.product_tenant_id_code_uniq;
-- DROP INDEX IF EXISTS rental.pricing_profile_code_uniq;
-- DROP INDEX IF EXISTS rental.operational_rules_product_id_uniq;
-- DROP INDEX IF EXISTS rental.inventory_model_product_id_uniq;
-- DROP INDEX IF EXISTS rental.duration_rules_product_id_uniq;
-- DROP INDEX IF EXISTS rental.availability_rules_product_id_uniq;
-- DROP INDEX IF EXISTS rental.agreement_rules_product_id_uniq;
-- DROP INDEX IF EXISTS promotions.recommendation_strategy_code_uniq;
-- DROP INDEX IF EXISTS promotions.recommendation_experiment_code_uniq;
-- DROP INDEX IF EXISTS promotions.promotion_code_uniq; CREATE UNIQUE INDEX IF NOT EXISTS promotion_code_uniq ON promotions.promotion (code);
-- DROP INDEX IF EXISTS promotions.coupon_campaign_code_uniq;
-- DROP INDEX IF EXISTS promotions.bundle_code_uniq;
-- DROP INDEX IF EXISTS platform.device_serial_number_uniq;
-- DROP INDEX IF EXISTS payments.provider_connection_code_uniq;
-- DROP INDEX IF EXISTS payments.method_code_uniq;
-- DROP INDEX IF EXISTS orders.sales_order_order_number_uniq; CREATE UNIQUE INDEX IF NOT EXISTS sales_order_order_number_uniq ON orders.sales_order (order_number) WHERE order_number IS NOT NULL;
-- DROP INDEX IF EXISTS marketing.referral_code_uniq;
-- DROP INDEX IF EXISTS marketing.message_template_tenant_id_code_uniq;
-- DROP INDEX IF EXISTS marketing.loyalty_programme_code_uniq; CREATE UNIQUE INDEX IF NOT EXISTS loyalty_programme_code_uniq ON marketing.loyalty_programme (code);
-- DROP INDEX IF EXISTS maintenance.inspection_template_code_uniq;
-- DROP INDEX IF EXISTS maintenance.asset_category_code_uniq;
-- DROP INDEX IF EXISTS ledger.tax_invoice_invoice_number_uniq; CREATE UNIQUE INDEX IF NOT EXISTS tax_invoice_invoice_number_uniq ON ledger.tax_invoice (invoice_number);
-- DROP INDEX IF EXISTS ledger.tax_code_code_uniq; CREATE UNIQUE INDEX IF NOT EXISTS tax_code_code_uniq ON ledger.tax_code (code);
-- DROP INDEX IF EXISTS ledger.legal_entity_code_uniq;
-- DROP INDEX IF EXISTS ledger.journal_entry_entry_number_uniq; CREATE UNIQUE INDEX IF NOT EXISTS journal_entry_entry_number_uniq ON ledger.journal_entry (entry_number);
-- DROP INDEX IF EXISTS ledger.credit_memo_credit_memo_number_uniq; CREATE UNIQUE INDEX IF NOT EXISTS credit_memo_credit_memo_number_uniq ON ledger.credit_memo (credit_memo_number);
-- DROP INDEX IF EXISTS ledger.cost_center_code_uniq;
-- DROP INDEX IF EXISTS ledger.account_code_uniq; CREATE UNIQUE INDEX IF NOT EXISTS account_code_uniq ON ledger.account (code);
-- DROP INDEX IF EXISTS inventory.supplier_contract_number_uniq;
-- DROP INDEX IF EXISTS inventory.supplier_code_uniq; CREATE UNIQUE INDEX IF NOT EXISTS supplier_code_uniq ON inventory.supplier (code);
-- DROP INDEX IF EXISTS identity.role_code_uniq; CREATE UNIQUE INDEX IF NOT EXISTS role_code_uniq ON identity.role (code);
-- DROP INDEX IF EXISTS identity.principal_username_uniq;
-- DROP INDEX IF EXISTS identity.authorisation_policy_code_uniq;
-- DROP INDEX IF EXISTS games.entitlement_code_uniq;
-- DROP INDEX IF EXISTS catalogue.product_category_code_uniq; CREATE UNIQUE INDEX IF NOT EXISTS product_category_code_uniq ON catalogue.product_category (code) WHERE code IS NOT NULL;
-- DROP INDEX IF EXISTS catalogue.product_code_uniq; CREATE UNIQUE INDEX IF NOT EXISTS product_code_uniq ON catalogue.product (code);
-- DROP INDEX IF EXISTS catalogue.price_list_code_uniq;
-- DROP INDEX IF EXISTS catalogue.event_code_uniq; CREATE UNIQUE INDEX IF NOT EXISTS event_code_uniq ON catalogue.event (code);
-- DROP INDEX IF EXISTS catalogue.entitlement_template_code_uniq;
-- DROP INDEX IF EXISTS assets.media_collection_name_uniq; CREATE UNIQUE INDEX IF NOT EXISTS media_collection_name_uniq ON assets.media_collection (name);
-- DROP INDEX IF EXISTS approvals.external_provider_code_uniq; CREATE UNIQUE INDEX IF NOT EXISTS external_provider_code_uniq ON approvals.external_provider (code);
-- DROP INDEX IF EXISTS accreditation.programme_code_uniq;
-- DROP INDEX IF EXISTS access.reason_code_code_uniq;
-- DROP INDEX IF EXISTS access.admission_rules_code_uniq;
-- DROP INDEX IF EXISTS resources.venue_assignment_resource_id_idx;
-- DROP INDEX IF EXISTS resources.resource_replacement_resource_id_idx;
-- DROP INDEX IF EXISTS rental.operational_rules_product_id_idx;
-- DROP INDEX IF EXISTS rental.location_rule_product_id_idx;
-- DROP INDEX IF EXISTS rental.inventory_model_product_id_idx;
-- DROP INDEX IF EXISTS rental.inspection_booking_id_idx;
-- DROP INDEX IF EXISTS rental.equipment_assignment_booking_id_idx;
-- DROP INDEX IF EXISTS rental.duration_rules_product_id_idx;
-- DROP INDEX IF EXISTS rental.damage_assessment_booking_id_idx;
-- DROP INDEX IF EXISTS rental.availability_rules_product_id_idx;
-- DROP INDEX IF EXISTS rental.agreement_rules_product_id_idx;
-- DROP INDEX IF EXISTS queue.entry_priority_tier_id_idx;
-- DROP INDEX IF EXISTS platform.outlet_opening_hour_outlet_id_idx;
-- DROP INDEX IF EXISTS marketing.kiosk_assist_session_device_id_idx;
-- DROP INDEX IF EXISTS marketing.invitation_campaign_id_idx;
-- DROP INDEX IF EXISTS identity.subject_holding_subject_id_idx;
-- DROP INDEX IF EXISTS identity.principal_credential_history_principal_credential_id_idx;
-- DROP INDEX IF EXISTS identity.principal_sso_provider_id_idx;
-- DROP INDEX IF EXISTS assets.rendition_asset_id_idx;
-- DROP INDEX IF EXISTS ai.index_entry_last_job_id_idx;
-- DROP INDEX IF EXISTS platform.sale_board_tile_variant_id_idx;
-- DROP INDEX IF EXISTS marketing.invitation_subject_id_idx;
-- DROP INDEX IF EXISTS identity.subject_holding_order_line_id_idx;
-- DROP INDEX IF EXISTS identity.mfa_challenge_session_id_idx;
-- DROP INDEX IF EXISTS identity.mfa_challenge_method_id_idx;
-- DROP INDEX IF EXISTS approvals.escalation_escalated_by_principal_id_idx;
-- DROP INDEX IF EXISTS approvals.escalation_added_approver_principal_id_idx;
-- ALTER TABLE resources.venue_assignment DROP CONSTRAINT IF EXISTS venue_assignment_resource_id_fkey;
-- ALTER TABLE resources.resource DROP CONSTRAINT IF EXISTS resource_replacement_resource_id_fkey;
-- ALTER TABLE rental.operational_rules DROP CONSTRAINT IF EXISTS operational_rules_product_id_fkey;
-- ALTER TABLE rental.location_rule DROP CONSTRAINT IF EXISTS location_rule_product_id_fkey;
-- ALTER TABLE rental.inventory_model DROP CONSTRAINT IF EXISTS inventory_model_product_id_fkey;
-- ALTER TABLE rental.inspection DROP CONSTRAINT IF EXISTS inspection_booking_id_fkey;
-- ALTER TABLE rental.equipment_assignment DROP CONSTRAINT IF EXISTS equipment_assignment_booking_id_fkey;
-- ALTER TABLE rental.duration_rules DROP CONSTRAINT IF EXISTS duration_rules_product_id_fkey;
-- ALTER TABLE rental.damage_assessment DROP CONSTRAINT IF EXISTS damage_assessment_booking_id_fkey;
-- ALTER TABLE rental.availability_rules DROP CONSTRAINT IF EXISTS availability_rules_product_id_fkey;
-- ALTER TABLE rental.agreement_rules DROP CONSTRAINT IF EXISTS agreement_rules_product_id_fkey;
-- ALTER TABLE marketing.invitation DROP CONSTRAINT IF EXISTS invitation_campaign_id_fkey;
-- ALTER TABLE identity.principal DROP CONSTRAINT IF EXISTS principal_sso_provider_id_fkey;
-- ALTER TABLE assets.rendition DROP CONSTRAINT IF EXISTS rendition_asset_id_fkey;
-- ALTER TABLE ai.index_entry DROP CONSTRAINT IF EXISTS index_entry_last_job_id_fkey;
-- ALTER TABLE workforce.shift_template DROP COLUMN IF EXISTS breaks;
-- ALTER TABLE whitelabel.config_version DROP COLUMN IF EXISTS pending_build_time_changes;
-- ALTER TABLE whitelabel.booking_flow_step DROP COLUMN IF EXISTS scope_path;
-- ALTER TABLE wallet.reconciliation_source DROP COLUMN IF EXISTS sources;
-- ALTER TABLE wallet.gift_card_product DROP COLUMN IF EXISTS denominations;
-- ALTER TABLE wallet.credential DROP COLUMN IF EXISTS recorded_at;
-- ALTER TABLE wallet.configuration_version DROP COLUMN IF EXISTS findings;
-- ALTER TABLE wallet.authentication_policy DROP COLUMN IF EXISTS tiers;
-- ALTER TABLE wallet.accounting_mapping DROP COLUMN IF EXISTS mappings;
-- ALTER TABLE venuemap.visit_plan DROP COLUMN IF EXISTS excluded;
-- ALTER TABLE venuemap.point DROP COLUMN IF EXISTS media;
-- ALTER TABLE venuemap.placed_resource DROP COLUMN IF EXISTS boundary;
-- ALTER TABLE venuemap.path DROP COLUMN IF EXISTS closed_note;
-- ALTER TABLE venuemap.path DROP COLUMN IF EXISTS expected_reopen_at;
-- ALTER TABLE venuemap.path DROP COLUMN IF EXISTS is_closed;
-- ALTER TABLE venuemap.import_job DROP COLUMN IF EXISTS findings;
-- ALTER TABLE venuemap.import_job DROP COLUMN IF EXISTS scope_path;
-- ALTER TABLE transport.route DROP COLUMN IF EXISTS status_reason;
-- ALTER TABLE transport.network_import DROP COLUMN IF EXISTS findings;
-- ALTER TABLE tenancy.device_tamper_event DROP COLUMN IF EXISTS recorded_at;
-- ALTER TABLE tenancy.device_rollout DROP COLUMN IF EXISTS waves;
-- ALTER TABLE subscription.vsi_model DROP COLUMN IF EXISTS tiers;
-- ALTER TABLE subscription.vsi_model DROP COLUMN IF EXISTS factors;
-- ALTER TABLE subscription.licensing_model DROP COLUMN IF EXISTS overage_pricing;
-- ALTER TABLE subscription.go_live_readiness DROP COLUMN IF EXISTS groups;
-- ALTER TABLE subscription.enforcement_policy DROP COLUMN IF EXISTS thresholds;
-- ALTER TABLE seating.section DROP COLUMN IF EXISTS boundary;
-- ALTER TABLE seating.seat_price_band DROP COLUMN IF EXISTS scope_path;
-- ALTER TABLE seating.seat DROP COLUMN IF EXISTS scope_path;
-- ALTER TABLE seating.accessible DROP COLUMN IF EXISTS spaces;
-- ALTER TABLE resources.venue_assignment DROP COLUMN IF EXISTS resource_id;
-- ALTER TABLE resources.resource_schedule DROP COLUMN IF EXISTS exceptions;
-- ALTER TABLE resources.resource_schedule DROP COLUMN IF EXISTS windows;
-- ALTER TABLE resources.resource DROP COLUMN IF EXISTS disposal;
-- ALTER TABLE resources.resource DROP COLUMN IF EXISTS replacement_resource_id;
-- ALTER TABLE resources.resource DROP COLUMN IF EXISTS lifecycle_reason;
-- ALTER TABLE resources.resource DROP COLUMN IF EXISTS lifecycle_effective_from;
-- ALTER TABLE resources.resource DROP COLUMN IF EXISTS lifecycle_state;
-- ALTER TABLE resources.booking DROP COLUMN IF EXISTS change_reason;
-- ALTER TABLE reporting.subscription DROP COLUMN IF EXISTS recipients;
-- ALTER TABLE reporting.semantic_model DROP COLUMN IF EXISTS relationships;
-- ALTER TABLE reporting.semantic_model DROP COLUMN IF EXISTS domains;
-- ALTER TABLE reporting.anomaly DROP COLUMN IF EXISTS candidate_causes;
-- ALTER TABLE rental.pricing_profile DROP COLUMN IF EXISTS calendar_rules;
-- ALTER TABLE rental.pricing_profile DROP COLUMN IF EXISTS duration_tiers;
-- ALTER TABLE rental.participant DROP COLUMN IF EXISTS scope_path;
-- ALTER TABLE rental.operational_rules DROP COLUMN IF EXISTS product_id;
-- ALTER TABLE rental.location_rule DROP COLUMN IF EXISTS product_id;
-- ALTER TABLE rental.inventory_model DROP COLUMN IF EXISTS product_id;
-- ALTER TABLE rental.inventory_model DROP COLUMN IF EXISTS components;
-- ALTER TABLE rental.inspection DROP COLUMN IF EXISTS booking_id;
-- ALTER TABLE rental.inspection DROP COLUMN IF EXISTS recorded_at;
-- ALTER TABLE rental.inspection DROP COLUMN IF EXISTS checklist;
-- ALTER TABLE rental.incident DROP COLUMN IF EXISTS recorded_at;
-- ALTER TABLE rental.fee_policy DROP COLUMN IF EXISTS late_fee_tiers;
-- ALTER TABLE rental.equipment_assignment DROP COLUMN IF EXISTS booking_id;
-- ALTER TABLE rental.duration_rules DROP COLUMN IF EXISTS product_id;
-- ALTER TABLE rental.damage_assessment DROP COLUMN IF EXISTS booking_id;
-- ALTER TABLE rental.booking DROP COLUMN IF EXISTS change_reason;
-- ALTER TABLE rental.availability_rules DROP COLUMN IF EXISTS product_id;
-- ALTER TABLE rental.availability_rules DROP COLUMN IF EXISTS operating_windows;
-- ALTER TABLE rental.agreement_rules DROP COLUMN IF EXISTS product_id;
-- ALTER TABLE promotions.upsell_rule DROP COLUMN IF EXISTS scope_path;
-- ALTER TABLE promotions.recommendation_suppression DROP COLUMN IF EXISTS hard_exclusions;
-- ALTER TABLE promotions.recommendation_outcome DROP COLUMN IF EXISTS recorded_at;
-- ALTER TABLE promotions.recommendation_experiment DROP COLUMN IF EXISTS variants;
-- ALTER TABLE promotions.promotion_variant DROP COLUMN IF EXISTS scope_path;
-- ALTER TABLE platform.workstation DROP COLUMN IF EXISTS guest_display_content;
-- ALTER TABLE platform.workstation DROP COLUMN IF EXISTS cashier_input_mode;
-- ALTER TABLE platform.sale_board_tile DROP COLUMN IF EXISTS image_asset_ref;
-- ALTER TABLE platform.sale_board_tile DROP COLUMN IF EXISTS colour;
-- ALTER TABLE platform.sale_board_tile DROP COLUMN IF EXISTS label;
-- ALTER TABLE platform.sale_board_tile DROP COLUMN IF EXISTS action_code;
-- ALTER TABLE platform.sale_board_tile DROP COLUMN IF EXISTS category_id;
-- ALTER TABLE platform.sale_board_tile DROP COLUMN IF EXISTS variant_id;
-- ALTER TABLE platform.sale_board_tile DROP COLUMN IF EXISTS kind;
-- ALTER TABLE platform.sale_board_tile DROP COLUMN IF EXISTS position;
-- ALTER TABLE platform.region_settings DROP COLUMN IF EXISTS scope_path;
-- DROP TABLE IF EXISTS platform.outlet_opening_hour;
-- ALTER TABLE platform.device DROP COLUMN IF EXISTS scope_path;
-- ALTER TABLE platform.denomination DROP COLUMN IF EXISTS scope_path;
-- ALTER TABLE payments.routing_rule DROP COLUMN IF EXISTS targets;
-- ALTER TABLE payments.risk_rules DROP COLUMN IF EXISTS lists;
-- ALTER TABLE payments.risk_rules DROP COLUMN IF EXISTS rules;
-- ALTER TABLE payments.mixed_tender_rules DROP COLUMN IF EXISTS allowed_combinations;
-- ALTER TABLE payments.fee_rule DROP COLUMN IF EXISTS scope_path;
-- ALTER TABLE payments.deposit_activity DROP COLUMN IF EXISTS scope_path;
-- ALTER TABLE payments.chargeback_evidence DROP COLUMN IF EXISTS documents;
-- ALTER TABLE orders.ticket_template DROP COLUMN IF EXISTS scope_path;
-- ALTER TABLE orders.refund_calculation_policy DROP COLUMN IF EXISTS scope_path;
-- ALTER TABLE orders.membership_migration DROP COLUMN IF EXISTS scope_path;
-- ALTER TABLE orders.member_exception DROP COLUMN IF EXISTS scope_path;
-- ALTER TABLE orders.invitation_allowance DROP COLUMN IF EXISTS scope_path;
-- ALTER TABLE orders.invitation DROP COLUMN IF EXISTS scope_path;
-- ALTER TABLE orders.group_enquiry DROP COLUMN IF EXISTS scope_path;
-- ALTER TABLE orders.deposit_box DROP COLUMN IF EXISTS recorded_at;
-- ALTER TABLE marketing.waiver_version_control DROP COLUMN IF EXISTS history;
-- ALTER TABLE marketing.waiver_trigger_rule DROP COLUMN IF EXISTS reminders;
-- ALTER TABLE marketing.waiver_trigger_rule DROP COLUMN IF EXISTS eligibility;
-- ALTER TABLE marketing.waiver_signatory_rule DROP COLUMN IF EXISTS guardian_threshold_by_country;
-- ALTER TABLE marketing.waiver_localisation DROP COLUMN IF EXISTS languages;
-- ALTER TABLE marketing.waiver_form_layout DROP COLUMN IF EXISTS sections;
-- ALTER TABLE marketing.reward DROP COLUMN IF EXISTS scope_path;
-- ALTER TABLE marketing.quality_evaluation DROP COLUMN IF EXISTS coaching_actions;
-- ALTER TABLE marketing.quality_evaluation DROP COLUMN IF EXISTS ai_findings;
-- ALTER TABLE marketing.quality_evaluation DROP COLUMN IF EXISTS criteria;
-- ALTER TABLE marketing.privacy_request_type DROP COLUMN IF EXISTS stages;
-- ALTER TABLE marketing.privacy_export_package DROP COLUMN IF EXISTS corrections;
-- ALTER TABLE marketing.privacy_export_package DROP COLUMN IF EXISTS results;
-- ALTER TABLE marketing.privacy_export_package DROP COLUMN IF EXISTS identifiers;
-- ALTER TABLE marketing.privacy_change_set DROP COLUMN IF EXISTS items;
-- ALTER TABLE marketing.privacy_action DROP COLUMN IF EXISTS system_results;
-- ALTER TABLE marketing.points_redemption_rule DROP COLUMN IF EXISTS scope_path;
-- ALTER TABLE marketing.loyalty_points DROP COLUMN IF EXISTS scope_path;
-- ALTER TABLE marketing.loyalty_campaign DROP COLUMN IF EXISTS scope_path;
-- ALTER TABLE marketing.kiosk_assist_session DROP COLUMN IF EXISTS actions_taken;
-- ALTER TABLE marketing.invitation DROP COLUMN IF EXISTS responded_at;
-- ALTER TABLE marketing.invitation DROP COLUMN IF EXISTS status;
-- ALTER TABLE marketing.invitation DROP COLUMN IF EXISTS plus_ones;
-- ALTER TABLE marketing.invitation DROP COLUMN IF EXISTS token;
-- ALTER TABLE marketing.invitation DROP COLUMN IF EXISTS subject_id;
-- ALTER TABLE marketing.invitation DROP COLUMN IF EXISTS campaign_id;
-- ALTER TABLE marketing.identity_rules DROP COLUMN IF EXISTS survivorship;
-- ALTER TABLE marketing.identity_rules DROP COLUMN IF EXISTS matchers;
-- ALTER TABLE marketing.guest_extra_value DROP COLUMN IF EXISTS scope_path;
-- ALTER TABLE marketing.guest_extra_option DROP COLUMN IF EXISTS scope_path;
-- ALTER TABLE marketing.guest_device DROP COLUMN IF EXISTS installation_id;
-- ALTER TABLE marketing.guest_attribute_model DROP COLUMN IF EXISTS identifiers;
-- ALTER TABLE marketing.guest_attribute_model DROP COLUMN IF EXISTS attributes;
-- ALTER TABLE marketing.guest_attribute_model DROP COLUMN IF EXISTS field_groups;
-- ALTER TABLE marketing.duplicate_candidate DROP COLUMN IF EXISTS conflicts;
-- ALTER TABLE marketing.cookie_banner_design DROP COLUMN IF EXISTS categories;
-- ALTER TABLE marketing.cookie_banner_design DROP COLUMN IF EXISTS links;
-- ALTER TABLE marketing.cookie_banner_design DROP COLUMN IF EXISTS buttons;
-- ALTER TABLE marketing.consent_capture_point DROP COLUMN IF EXISTS steps;
-- ALTER TABLE marketing.communication_routing_rule DROP COLUMN IF EXISTS providers;
-- ALTER TABLE marketing.case_message DROP COLUMN IF EXISTS scope_path;
-- ALTER TABLE marketing.badge DROP COLUMN IF EXISTS scope_path;
-- ALTER TABLE maintenance.work_order DROP COLUMN IF EXISTS parts;
-- ALTER TABLE maintenance.work_order DROP COLUMN IF EXISTS time_entries;
-- ALTER TABLE maintenance.priority_scoring_model DROP COLUMN IF EXISTS bands;
-- ALTER TABLE ledger.tax_exemption DROP COLUMN IF EXISTS scope_path;
-- ALTER TABLE ledger.tax_code DROP COLUMN IF EXISTS scope_path;
-- ALTER TABLE ledger.recognition_schedule DROP COLUMN IF EXISTS scope_path;
-- ALTER TABLE ledger.journal_entry DROP COLUMN IF EXISTS posting_date;
-- ALTER TABLE ledger.event_budget DROP COLUMN IF EXISTS cost_lines;
-- ALTER TABLE inventory.supplier DROP COLUMN IF EXISTS contacts;
-- DROP TABLE IF EXISTS identity.subject_holding;
-- DROP TABLE IF EXISTS identity.principal_credential_history;
-- ALTER TABLE identity.principal_credential DROP COLUMN IF EXISTS locked_until;
-- ALTER TABLE identity.principal_credential DROP COLUMN IF EXISTS failed_attempts;
-- ALTER TABLE identity.principal_credential DROP COLUMN IF EXISTS set_at;
-- ALTER TABLE identity.principal_credential DROP COLUMN IF EXISTS credential_hash;
-- ALTER TABLE identity.principal_credential DROP COLUMN IF EXISTS method;
-- ALTER TABLE identity.principal DROP COLUMN IF EXISTS sso_provider_id;
-- ALTER TABLE identity.principal DROP COLUMN IF EXISTS must_change_credential;
-- ALTER TABLE identity.password_policy DROP COLUMN IF EXISTS pin_lockout_after_attempts;
-- ALTER TABLE identity.password_policy DROP COLUMN IF EXISTS pin_reuse_prevention;
-- ALTER TABLE identity.password_policy DROP COLUMN IF EXISTS pin_length;
-- ALTER TABLE identity.otp_challenge DROP COLUMN IF EXISTS invalidated_at;
-- ALTER TABLE identity.otp_challenge DROP COLUMN IF EXISTS consumed_at;
-- ALTER TABLE identity.otp_challenge DROP COLUMN IF EXISTS resend_after;
-- ALTER TABLE identity.otp_challenge DROP COLUMN IF EXISTS expires_at;
-- ALTER TABLE identity.otp_challenge DROP COLUMN IF EXISTS attempt_limit;
-- ALTER TABLE identity.otp_challenge DROP COLUMN IF EXISTS failed_attempts;
-- ALTER TABLE identity.otp_challenge DROP COLUMN IF EXISTS code_hash;
-- ALTER TABLE identity.otp_challenge DROP COLUMN IF EXISTS purpose;
-- ALTER TABLE identity.otp_challenge DROP COLUMN IF EXISTS channel;
-- ALTER TABLE identity.otp_challenge DROP COLUMN IF EXISTS identifier_hash;
-- ALTER TABLE identity.mfa_recovery_code DROP COLUMN IF EXISTS used_at;
-- ALTER TABLE identity.mfa_recovery_code DROP COLUMN IF EXISTS issued_at;
-- ALTER TABLE identity.mfa_recovery_code DROP COLUMN IF EXISTS code_hash;
-- ALTER TABLE identity.mfa_challenge DROP COLUMN IF EXISTS voided_at;
-- ALTER TABLE identity.mfa_challenge DROP COLUMN IF EXISTS consumed_at;
-- ALTER TABLE identity.mfa_challenge DROP COLUMN IF EXISTS verified_at;
-- ALTER TABLE identity.mfa_challenge DROP COLUMN IF EXISTS expires_at;
-- ALTER TABLE identity.mfa_challenge DROP COLUMN IF EXISTS failed_attempts;
-- ALTER TABLE identity.mfa_challenge DROP COLUMN IF EXISTS status;
-- ALTER TABLE identity.mfa_challenge DROP COLUMN IF EXISTS code_hash;
-- ALTER TABLE identity.mfa_challenge DROP COLUMN IF EXISTS session_id;
-- ALTER TABLE identity.mfa_challenge DROP COLUMN IF EXISTS action;
-- ALTER TABLE identity.mfa_challenge DROP COLUMN IF EXISTS method_id;
-- ALTER TABLE identity.benefit_usage DROP COLUMN IF EXISTS recorded_at;
-- ALTER TABLE identity.authorisation_policy DROP COLUMN IF EXISTS status_reason;
-- ALTER TABLE identity.access_decision DROP COLUMN IF EXISTS matched_policies;
-- ALTER TABLE games.redemption_rules DROP COLUMN IF EXISTS earn_rules;
-- ALTER TABLE games.reader_deployment DROP COLUMN IF EXISTS scope_path;
-- ALTER TABLE games.pricing DROP COLUMN IF EXISTS calendar_exceptions;
-- ALTER TABLE games.pricing DROP COLUMN IF EXISTS peak_pricing;
-- ALTER TABLE games.pricing DROP COLUMN IF EXISTS group_pricing;
-- ALTER TABLE games.play DROP COLUMN IF EXISTS scope_path;
-- ALTER TABLE games.operational_config DROP COLUMN IF EXISTS operating_hours;
-- ALTER TABLE games.credit_ledger DROP COLUMN IF EXISTS synced_at;
-- ALTER TABLE games.credit_ledger DROP COLUMN IF EXISTS recorded_at;
-- ALTER TABLE games.credit_ledger DROP COLUMN IF EXISTS reconciled_at;
-- ALTER TABLE games.credit_ledger DROP COLUMN IF EXISTS is_divergence;
-- ALTER TABLE games.credit_ledger DROP COLUMN IF EXISTS points_after;
-- ALTER TABLE games.credit_ledger DROP COLUMN IF EXISTS credits_after;
-- ALTER TABLE games.credit_ledger DROP COLUMN IF EXISTS points_awarded;
-- ALTER TABLE games.credit_ledger DROP COLUMN IF EXISTS bonus_credits_used;
-- ALTER TABLE games.credit_ledger DROP COLUMN IF EXISTS credits_used;
-- ALTER TABLE games.credit_ledger DROP COLUMN IF EXISTS sequence;
-- ALTER TABLE games.credit_ledger DROP COLUMN IF EXISTS reader_id;
-- ALTER TABLE games.credit_ledger DROP COLUMN IF EXISTS play_id;
-- ALTER TABLE games.authorisation DROP COLUMN IF EXISTS trace;
-- ALTER TABLE fnb.temperature_log DROP COLUMN IF EXISTS scope_path;
-- ALTER TABLE fnb.table_visit DROP COLUMN IF EXISTS note;
-- ALTER TABLE fnb.reservation_policy DROP COLUMN IF EXISTS turn_time_bands;
-- ALTER TABLE fnb.production_plan DROP COLUMN IF EXISTS scope_path;
-- ALTER TABLE fnb.menu_item DROP COLUMN IF EXISTS unavailable_note;
-- ALTER TABLE fnb.kitchen_station DROP COLUMN IF EXISTS scope_path;
-- ALTER TABLE fnb.kitchen_exception DROP COLUMN IF EXISTS scope_path;
-- ALTER TABLE fnb.dining_table DROP COLUMN IF EXISTS scope_path;
-- ALTER TABLE fnb.combo_slot DROP COLUMN IF EXISTS scope_path;
-- ALTER TABLE fnb.combo DROP COLUMN IF EXISTS scope_path;
-- ALTER TABLE fnb.cold_chain_event DROP COLUMN IF EXISTS scope_path;
-- ALTER TABLE catalogue.variant_dimension DROP COLUMN IF EXISTS values;
-- ALTER TABLE catalogue.product DROP COLUMN IF EXISTS display_tags;
-- ALTER TABLE catalogue.performance_template DROP COLUMN IF EXISTS bands;
-- ALTER TABLE catalogue.membership_programme DROP COLUMN IF EXISTS scope_path;
-- ALTER TABLE catalogue.membership_benefit DROP COLUMN IF EXISTS scope_path;
-- ALTER TABLE catalogue.import_job DROP COLUMN IF EXISTS findings;
-- ALTER TABLE catalogue.event_schedule DROP COLUMN IF EXISTS performances;
-- ALTER TABLE catalogue.event_resource_plan DROP COLUMN IF EXISTS contractors;
-- ALTER TABLE catalogue.event_resource_plan DROP COLUMN IF EXISTS requirements;
-- ALTER TABLE catalogue.event_registration DROP COLUMN IF EXISTS participant_categories;
-- ALTER TABLE catalogue.entitlement_template DROP COLUMN IF EXISTS valid_time_windows;
-- ALTER TABLE catalogue.donation_campaign DROP COLUMN IF EXISTS fixed_amounts;
-- ALTER TABLE catalogue.channel_incident DROP COLUMN IF EXISTS resolution_note;
-- ALTER TABLE catalogue.alternative_code DROP COLUMN IF EXISTS scope_path;
-- ALTER TABLE assets.taxonomy DROP COLUMN IF EXISTS keyword_vocabularies;
-- ALTER TABLE assets.taxonomy DROP COLUMN IF EXISTS fields;
-- ALTER TABLE assets.taxonomy DROP COLUMN IF EXISTS categories;
-- ALTER TABLE assets.rendition DROP COLUMN IF EXISTS asset_id;
-- ALTER TABLE approvals.sla_policy DROP COLUMN IF EXISTS reminders;
-- ALTER TABLE approvals.escalation DROP COLUMN IF EXISTS added_approver_principal_id;
-- ALTER TABLE approvals.escalation DROP COLUMN IF EXISTS escalated_by_principal_id;
-- ALTER TABLE approvals.escalation DROP COLUMN IF EXISTS was_automatic;
-- ALTER TABLE approvals.escalation DROP COLUMN IF EXISTS to_level;
-- ALTER TABLE approvals.escalation DROP COLUMN IF EXISTS from_level;
-- ALTER TABLE approvals.escalation DROP COLUMN IF EXISTS reason;
-- ALTER TABLE approvals.escalation DROP COLUMN IF EXISTS escalated_at;
-- ALTER TABLE approvals.decision_record DROP COLUMN IF EXISTS policy_versions;
-- ALTER TABLE approvals.accreditation_badge DROP COLUMN IF EXISTS scope_path;
-- ALTER TABLE ai.venue_settings DROP COLUMN IF EXISTS opening_hours;
-- ALTER TABLE ai.risk_strategy DROP COLUMN IF EXISTS outcome_map;
-- ALTER TABLE ai.risk_case DROP COLUMN IF EXISTS entities;
-- ALTER TABLE ai.provider DROP COLUMN IF EXISTS fitness_warnings;
-- ALTER TABLE ai.model DROP COLUMN IF EXISTS task_fitness;
-- ALTER TABLE ai.index_entry DROP COLUMN IF EXISTS last_job_id;
-- ALTER TABLE ai.index_entry DROP COLUMN IF EXISTS indexed_at;
-- ALTER TABLE ai.index_entry DROP COLUMN IF EXISTS point_ids;
-- ALTER TABLE ai.index_entry DROP COLUMN IF EXISTS embedding_model;
-- ALTER TABLE ai.index_entry DROP COLUMN IF EXISTS chunk_count;
-- ALTER TABLE ai.index_entry DROP COLUMN IF EXISTS content_hash;
-- ALTER TABLE ai.index_entry DROP COLUMN IF EXISTS subject_id;
-- ALTER TABLE ai.index_entry DROP COLUMN IF EXISTS record_key;
-- ALTER TABLE ai.incident DROP COLUMN IF EXISTS containment;
-- ALTER TABLE ai.history_import DROP COLUMN IF EXISTS findings;
-- ALTER TABLE ai.guided_choice_suggestion DROP COLUMN IF EXISTS questions;
-- ALTER TABLE ai.forecast_scenario DROP COLUMN IF EXISTS changes;
-- ALTER TABLE ai.decision_record DROP COLUMN IF EXISTS annotations;
-- ALTER TABLE ai.config_source DROP COLUMN IF EXISTS scope_path;
-- ALTER TABLE ai.approval_request_score DROP COLUMN IF EXISTS signals;
-- ALTER TABLE accreditation.requirements DROP COLUMN IF EXISTS rows;
-- ALTER TABLE accreditation.programme DROP COLUMN IF EXISTS categories;
-- ALTER TABLE accreditation.print_job DROP COLUMN IF EXISTS failures;
-- ALTER TABLE accreditation.notification_rules DROP COLUMN IF EXISTS rules;
-- ALTER TABLE accreditation.holder DROP COLUMN IF EXISTS status_review_at;
-- ALTER TABLE accreditation.holder DROP COLUMN IF EXISTS status_effective_from;
-- ALTER TABLE access.security_alert DROP COLUMN IF EXISTS note;
-- ALTER TABLE access.configuration_change DROP COLUMN IF EXISTS reason;
-- ALTER TABLE access.access_point DROP COLUMN IF EXISTS direction_change_reason;
-- ALTER TABLE access.access_point DROP COLUMN IF EXISTS direction_effective_at;
-- DELETE FROM platform.schema_version WHERE version = 'V0104';
