-- V0101 -- tenant database, after r1 (a1ba956) (20261002).
-- **Written by tools/derive-ddl.py in frozen mode. Do not edit after merge; a mistake is a new migration.**
--
-- The baseline under backend/tenant/ is frozen at r1 (a1ba956), so the change to the schema reference
-- since then is written here instead: additive only. Changes that are not additive (drops, renames,
-- type changes) are not generated; they are listed for a person in handoff/migration-review.md.
-- 13 table(s), 110 column(s), 14 index(es), 13 other statement(s).

ALTER TABLE access.access_area ADD COLUMN IF NOT EXISTS security_classification_level text CONSTRAINT access_area_security_classification_level_chk CHECK (security_classification_level IN ('public', 'restricted', 'secure', 'critical'));

ALTER TABLE access.access_point ADD COLUMN IF NOT EXISTS temporary_closure jsonb;

ALTER TABLE access.entitlement ADD COLUMN IF NOT EXISTS first_entry_at timestamptz;

ALTER TABLE access.entitlement ADD COLUMN IF NOT EXISTS time_bound_until timestamptz;

ALTER TABLE access.entitlement ADD COLUMN IF NOT EXISTS cancellation_kind text CONSTRAINT entitlement_cancellation_kind_chk CHECK (cancellation_kind IN ('voided', 'refunded', 'performanceCancelled', 'superseded'));

ALTER TABLE access.gate_mode_change ADD COLUMN IF NOT EXISTS from_direction text;

ALTER TABLE access.gate_mode_change ADD COLUMN IF NOT EXISTS to_direction text;

CREATE TABLE IF NOT EXISTS access.hardware_certification (
    id                                uuid PRIMARY KEY NOT NULL,
    model_id                          uuid NOT NULL,
    outcome                           text NOT NULL CONSTRAINT hardware_certification_outcome_chk CHECK (outcome IN ('certified', 'failed')),
    results                           jsonb NOT NULL,
    valid_until                       date,
    firmware_version_tested           text CONSTRAINT hardware_certification_firmware_version_tested_chk CHECK (char_length(firmware_version_tested) <= 64),
    certified_by_principal_id         uuid,
    certified_at                      timestamptz,
    scope_path                        ltree NOT NULL
);

ALTER TABLE access.journey_sequence_rule ADD COLUMN IF NOT EXISTS applies_to jsonb;

ALTER TABLE access.operating_calendar_entry ADD COLUMN IF NOT EXISTS is_venue_closed boolean DEFAULT false;

ALTER TABLE access.operating_calendar_entry ADD COLUMN IF NOT EXISTS priority integer DEFAULT 0;

ALTER TABLE accreditation.programme ADD COLUMN IF NOT EXISTS face_matching jsonb;

ALTER TABLE accreditation.programme ADD COLUMN IF NOT EXISTS identity_verification jsonb;

ALTER TABLE ai.byok_enablement ADD COLUMN IF NOT EXISTS task_model_map jsonb;

ALTER TABLE ai.forecast_definition ADD COLUMN IF NOT EXISTS module text;

ALTER TABLE ai.forecast_version ADD COLUMN IF NOT EXISTS module text;

ALTER TABLE ai.incident ADD COLUMN IF NOT EXISTS impact text;

ALTER TABLE ai.incident ADD COLUMN IF NOT EXISTS control_failure text;

ALTER TABLE ai.incident ADD COLUMN IF NOT EXISTS lessons_learned text;

ALTER TABLE ai.model ADD COLUMN IF NOT EXISTS vendor text;

ALTER TABLE ai.model ADD COLUMN IF NOT EXISTS curated_range jsonb;

ALTER TABLE ai.model ADD COLUMN IF NOT EXISTS residency_classes text[];

ALTER TABLE ai.policy ADD COLUMN IF NOT EXISTS scrubbing jsonb;

ALTER TABLE ai.policy ADD COLUMN IF NOT EXISTS ceiling_behaviour_by_capability jsonb;

ALTER TABLE ai.policy ADD COLUMN IF NOT EXISTS autonomy_overrides jsonb;

ALTER TABLE ai.provider ADD COLUMN IF NOT EXISTS vendor text;

ALTER TABLE ai.provider ADD COLUMN IF NOT EXISTS credential_hint text CONSTRAINT provider_credential_hint_chk CHECK (char_length(credential_hint) <= 4);

ALTER TABLE ai.provider ADD COLUMN IF NOT EXISTS compatibility jsonb;

ALTER TABLE ai.provider ADD COLUMN IF NOT EXISTS residency_classes text[];

ALTER TABLE ai.release ADD COLUMN IF NOT EXISTS module text;

CREATE TABLE IF NOT EXISTS ai.spend_ceiling (
    id                                uuid PRIMARY KEY NOT NULL,
    scope_path                        ltree NOT NULL,
    spend                             numeric(18,4) NOT NULL,
    token_equivalent                  integer,
    updated_at                        timestamptz
);

ALTER TABLE approvals.request ADD COLUMN IF NOT EXISTS assigned_to_principal_id uuid;

ALTER TABLE approvals.request ADD COLUMN IF NOT EXISTS assigned_to_department_id uuid;

ALTER TABLE approvals.request ADD COLUMN IF NOT EXISTS assigned_at timestamptz;

ALTER TABLE approvals.rule ADD COLUMN IF NOT EXISTS subject_types text[];

ALTER TABLE approvals.rule ADD COLUMN IF NOT EXISTS signature_methods text[];

CREATE TABLE IF NOT EXISTS catalogue.event_change_treatment_policy (
    id                                uuid PRIMARY KEY,
    scope_path                        ltree NOT NULL,
    treatments                        jsonb NOT NULL,
    updated_at                        timestamptz
);

CREATE TABLE IF NOT EXISTS catalogue.seat_pricing_rule (
    id                                uuid PRIMARY KEY,
    name                              text NOT NULL CONSTRAINT seat_pricing_rule_name_chk CHECK (char_length(name) <= 200),
    strategy_id                       uuid NOT NULL,
    seat_map_id                       uuid NOT NULL,
    performance_id                    uuid,
    seat_section_codes                text[],
    rows                              text[],
    seat_ids                          text[],
    seat_category                     text CONSTRAINT seat_pricing_rule_seat_category_chk CHECK (char_length(seat_category) <= 64),
    floor_price                       numeric(18,4) NOT NULL,
    ceiling_price                     numeric(18,4) NOT NULL,
    step_price                        numeric(18,4),
    priority                          integer DEFAULT 0,
    is_active                         boolean DEFAULT true,
    scope_path                        ltree NOT NULL,
    updated_at                        timestamptz
);

CREATE TABLE IF NOT EXISTS fnb.kitchen_routing_rule (
    id                                uuid PRIMARY KEY NOT NULL,
    outlet_id                         uuid,
    category_rules                    jsonb,
    default_station_id                uuid NOT NULL,
    fallback_station_id               uuid,
    scope_path                        ltree NOT NULL
);

ALTER TABLE fnb.kitchen_station ADD COLUMN IF NOT EXISTS printer_device_ids text[];

ALTER TABLE fnb.kitchen_station ADD COLUMN IF NOT EXISTS serves_outlet_ids text[];

ALTER TABLE fnb.menu_item ADD COLUMN IF NOT EXISTS daily_count integer;

ALTER TABLE fnb.menu_item ADD COLUMN IF NOT EXISTS remaining_count integer;

CREATE TABLE IF NOT EXISTS fnb.prep_sheet_template (
    id                                uuid PRIMARY KEY NOT NULL,
    group_by                          text DEFAULT 'station' CONSTRAINT prep_sheet_template_group_by_chk CHECK (group_by IN ('station', 'item')),
    browser_paper                     text DEFAULT 'a4' CONSTRAINT prep_sheet_template_browser_paper_chk CHECK (browser_paper IN ('a4', 'letter')),
    printer_paper                     text DEFAULT 'thermal80mm' CONSTRAINT prep_sheet_template_printer_paper_chk CHECK (printer_paper IN ('thermal80mm', 'thermal58mm')),
    columns                           text[],
    header_text                       text CONSTRAINT prep_sheet_template_header_text_chk CHECK (char_length(header_text) <= 200),
    scope_path                        ltree NOT NULL
);

ALTER TABLE fnb.reservation_policy ADD COLUMN IF NOT EXISTS reserved_lead_minutes integer;

ALTER TABLE fnb.service_order ADD COLUMN IF NOT EXISTS payment_timing text;

ALTER TABLE fnb.service_order ADD COLUMN IF NOT EXISTS sent_to_kitchen_at timestamptz;

ALTER TABLE fnb.sold_out_item ADD COLUMN IF NOT EXISTS source text DEFAULT 'manual' CONSTRAINT sold_out_item_source_chk CHECK (source IN ('manual', 'dailyCount'));

ALTER TABLE fnb.table_reservation ADD COLUMN IF NOT EXISTS seating_preference text CONSTRAINT table_reservation_seating_preference_chk CHECK (char_length(seating_preference) <= 64);

ALTER TABLE fnb.table_reservation ADD COLUMN IF NOT EXISTS occasion text CONSTRAINT table_reservation_occasion_chk CHECK (occasion IN ('birthday', 'anniversary', 'business', 'celebration', 'other'));

ALTER TABLE fnb.table_reservation ADD COLUMN IF NOT EXISTS taken_by_principal_id uuid;

CREATE TABLE IF NOT EXISTS fnb.waste_approval_policy (
    id                                uuid PRIMARY KEY NOT NULL,
    is_enabled                        boolean NOT NULL DEFAULT false,
    bands                             jsonb,
    photo_required_above              numeric(18,4),
    scope_path                        ltree NOT NULL,
    updated_at                        timestamptz
);

ALTER TABLE games.entitlement ADD COLUMN IF NOT EXISTS covers_games_added_later boolean DEFAULT true;

ALTER TABLE games.pricing ADD COLUMN IF NOT EXISTS retry_offer_lead_seconds integer;

ALTER TABLE games.reader_sync_status ADD COLUMN IF NOT EXISTS offline_since timestamptz;

ALTER TABLE games.reader_sync_status ADD COLUMN IF NOT EXISTS refusing_offline_taps boolean;

ALTER TABLE identity.capability_template ADD COLUMN IF NOT EXISTS module text;

ALTER TABLE identity.capability_template ADD COLUMN IF NOT EXISTS preset_level text CONSTRAINT capability_template_preset_level_chk CHECK (preset_level IN ('all', 'viewer', 'midLevel'));

ALTER TABLE identity.capability_template ADD COLUMN IF NOT EXISTS is_preset boolean DEFAULT false;

ALTER TABLE identity.guest_verification_policy ADD COLUMN IF NOT EXISTS verification_provider text CONSTRAINT guest_verification_policy_verification_provider_chk CHECK (verification_provider IN ('icp'));

ALTER TABLE identity.role ADD COLUMN IF NOT EXISTS preset_code text CONSTRAINT role_preset_code_chk CHECK (char_length(preset_code) <= 64);

CREATE TABLE IF NOT EXISTS marketing.cookie_scan_finding (
    id                                uuid PRIMARY KEY,
    scan_run_id                       uuid NOT NULL,
    technology_id                     uuid,
    name                              text NOT NULL CONSTRAINT cookie_scan_finding_name_chk CHECK (char_length(name) <= 200),
    provider                          text NOT NULL CONSTRAINT cookie_scan_finding_provider_chk CHECK (char_length(provider) <= 150),
    technology_type                   text NOT NULL CONSTRAINT cookie_scan_finding_technology_type_chk CHECK (char_length(technology_type) <= 40),
    is_third_party                    boolean NOT NULL,
    duration_days                     integer,
    domain_application                text CONSTRAINT cookie_scan_finding_domain_application_chk CHECK (char_length(domain_application) <= 255),
    consent_state                     text CONSTRAINT cookie_scan_finding_consent_state_chk CHECK (consent_state IN ('noDecision', 'rejectedAll', 'acceptedAll')),
    page_url                          text CONSTRAINT cookie_scan_finding_page_url_chk CHECK (char_length(page_url) <= 2000),
    initiator_url                     text CONSTRAINT cookie_scan_finding_initiator_url_chk CHECK (char_length(initiator_url) <= 2000),
    cookie_domain                     text CONSTRAINT cookie_scan_finding_cookie_domain_chk CHECK (char_length(cookie_domain) <= 255),
    same_site                         text CONSTRAINT cookie_scan_finding_same_site_chk CHECK (same_site IN ('strict', 'lax', 'none')),
    is_secure                         boolean,
    suggested_category                text,
    classification_source             text CONSTRAINT cookie_scan_finding_classification_source_chk CHECK (classification_source IN ('openCookieDatabase', 'vendor', 'platformCatalogue', 'none')),
    pre_consent_violation             boolean NOT NULL,
    scope_path                        ltree NOT NULL
);

ALTER TABLE marketing.cookie_scan_policy ADD COLUMN IF NOT EXISTS scan_source text DEFAULT 'boughtScanner' CONSTRAINT cookie_scan_policy_scan_source_chk CHECK (scan_source IN ('boughtScanner', 'manualUpload'));

ALTER TABLE marketing.cookie_scan_policy ADD COLUMN IF NOT EXISTS scanner_vendor_ref text CONSTRAINT cookie_scan_policy_scanner_vendor_ref_chk CHECK (char_length(scanner_vendor_ref) <= 200);

ALTER TABLE marketing.cookie_scan_run ADD COLUMN IF NOT EXISTS pre_consent_violation_count integer;

ALTER TABLE marketing.form_definition ADD COLUMN IF NOT EXISTS consent_purposes text[];

ALTER TABLE marketing.segment ADD COLUMN IF NOT EXISTS rule_groups jsonb;

ALTER TABLE marketing.segment ADD COLUMN IF NOT EXISTS effective_from timestamptz;

ALTER TABLE marketing.segment ADD COLUMN IF NOT EXISTS effective_to timestamptz;

ALTER TABLE marketing.segment ADD COLUMN IF NOT EXISTS owner_principal_id uuid;

ALTER TABLE marketing.segment ADD COLUMN IF NOT EXISTS requires_approval boolean DEFAULT false;

CREATE TABLE IF NOT EXISTS marketing.tracking_technology_catalogue (
    id                                uuid PRIMARY KEY,
    entry_key                         text,
    name_pattern                      text NOT NULL CONSTRAINT tracking_technology_catalogue_name_pattern_chk CHECK (char_length(name_pattern) <= 200),
    provider                          text NOT NULL CONSTRAINT tracking_technology_catalogue_provider_chk CHECK (char_length(provider) <= 150),
    category                          text NOT NULL CONSTRAINT tracking_technology_catalogue_category_chk CHECK (category IN ('strictlyNecessary', 'functional', 'analytics', 'personalisation', 'marketing')),
    technology_type                   text NOT NULL CONSTRAINT tracking_technology_catalogue_technology_type_chk CHECK (char_length(technology_type) <= 40),
    purpose                           text CONSTRAINT tracking_technology_catalogue_purpose_chk CHECK (char_length(purpose) <= 1000),
    typical_duration_days             integer,
    is_third_party                    boolean,
    privacy_information_url           text CONSTRAINT tracking_technology_catalogue_privacy_information_url_chk CHECK (char_length(privacy_information_url) <= 2000),
    source                            text CONSTRAINT tracking_technology_catalogue_source_chk CHECK (source IN ('openCookieDatabase', 'platformCuration')),
    is_active                         boolean DEFAULT true,
    updated_at                        timestamptz,
    scope_path                        ltree NOT NULL
);

ALTER TABLE orders.pos_shift ADD COLUMN IF NOT EXISTS cashier_reason text CONSTRAINT pos_shift_cashier_reason_chk CHECK (cashier_reason IN ('tillError', 'unrecordedRefund', 'miscount', 'other'));

ALTER TABLE orders.pos_shift ADD COLUMN IF NOT EXISTS cashier_note text CONSTRAINT pos_shift_cashier_note_chk CHECK (char_length(cashier_note) <= 1000);

ALTER TABLE orders.pos_shift ADD COLUMN IF NOT EXISTS recount_requested_at timestamptz;

ALTER TABLE orders.pos_shift ADD COLUMN IF NOT EXISTS recount_requested_by_principal_id uuid;

ALTER TABLE orders.pos_shift ADD COLUMN IF NOT EXISTS recount_reason text CONSTRAINT pos_shift_recount_reason_chk CHECK (char_length(recount_reason) <= 500);

ALTER TABLE orders.pos_shift ADD COLUMN IF NOT EXISTS count_number integer;

CREATE TABLE IF NOT EXISTS orders.till_shift_policy (
    id                                uuid PRIMARY KEY,
    venue_id                          uuid NOT NULL,
    scope_path                        ltree NOT NULL,
    require_open_approval             boolean DEFAULT false,
    opening_float_tolerance           numeric(18,4),
    is_deposit_box_required           boolean DEFAULT true,
    is_bag_number_required            boolean DEFAULT false,
    require_close_approval            boolean DEFAULT false,
    auto_close_after_hours            integer DEFAULT 14,
    no_sale_alert_count               integer DEFAULT 10,
    updated_at                        timestamptz
);

ALTER TABLE pii.subject_biometric ADD COLUMN IF NOT EXISTS enrolment_channel text CONSTRAINT subject_biometric_enrolment_channel_chk CHECK (enrolment_channel IN ('guestApp', 'ticketCounter', 'annualPassCounter', 'selfServiceKiosk', 'entryGate'));

ALTER TABLE pii.subject_biometric ADD COLUMN IF NOT EXISTS consent_form_id uuid;

ALTER TABLE pii.subject_biometric ADD COLUMN IF NOT EXISTS consent_form_version integer;

ALTER TABLE platform.device ADD COLUMN IF NOT EXISTS test_result jsonb;

ALTER TABLE platform.device ADD COLUMN IF NOT EXISTS approval_status text DEFAULT 'pendingApproval';

ALTER TABLE platform.device ADD COLUMN IF NOT EXISTS enrolment_code text CONSTRAINT device_enrolment_code_chk CHECK (char_length(enrolment_code) <= 12);

ALTER TABLE platform.device ADD COLUMN IF NOT EXISTS enrolment_code_expires_at timestamptz;

ALTER TABLE platform.device ADD COLUMN IF NOT EXISTS tested_by_principal_id uuid;

ALTER TABLE platform.device ADD COLUMN IF NOT EXISTS approved_by_principal_id uuid;

ALTER TABLE platform.device ADD COLUMN IF NOT EXISTS approved_at timestamptz;

ALTER TABLE platform.outlet ADD COLUMN IF NOT EXISTS name_translations jsonb;

ALTER TABLE platform.outlet ADD COLUMN IF NOT EXISTS outlet_type text;

ALTER TABLE platform.outlet ADD COLUMN IF NOT EXISTS department_id uuid;

ALTER TABLE platform.outlet ADD COLUMN IF NOT EXISTS payment_timing text DEFAULT 'sendFirst';

ALTER TABLE platform.outlet ADD COLUMN IF NOT EXISTS admission_context text DEFAULT 'insideVenue';

ALTER TABLE platform.outlet ADD COLUMN IF NOT EXISTS produces_for_outlet_ids text[];

ALTER TABLE platform.outlet ADD COLUMN IF NOT EXISTS sale_board_id uuid;

ALTER TABLE platform.region_settings ADD COLUMN IF NOT EXISTS ai_residency_class text DEFAULT 'uaeOnly' CONSTRAINT region_settings_ai_residency_class_chk CHECK (ai_residency_class IN ('uaeOnly', 'globalAllowed', 'onPrem'));

ALTER TABLE platform.region_settings ADD COLUMN IF NOT EXISTS is_ai_residency_class_locked boolean DEFAULT false;

ALTER TABLE platform.region_settings ADD COLUMN IF NOT EXISTS ai_residency_opt_in jsonb;

ALTER TABLE platform.region_settings ADD COLUMN IF NOT EXISTS local_language_name_locales text[];

ALTER TABLE platform.region_settings ADD COLUMN IF NOT EXISTS required_billing_documents jsonb;

ALTER TABLE platform.region_settings ADD COLUMN IF NOT EXISTS minor_age_threshold integer DEFAULT 18;

ALTER TABLE platform.venue_settings ADD COLUMN IF NOT EXISTS cash_drawer_limit text;

ALTER TABLE platform.workstation ADD COLUMN IF NOT EXISTS outlet_id uuid;

ALTER TABLE platform.workstation ADD COLUMN IF NOT EXISTS sale_board_source text CONSTRAINT workstation_sale_board_source_chk CHECK (sale_board_source IN ('outlet', 'workstation'));

ALTER TABLE platform.workstation ADD COLUMN IF NOT EXISTS cash_drawer_limit text;

CREATE TABLE IF NOT EXISTS reporting.analytics_governance_policy (
    id                                uuid PRIMARY KEY NOT NULL,
    masking                           jsonb,
    export                            jsonb,
    retention                         jsonb,
    sharing                           jsonb,
    ai_and_api_access                 jsonb,
    scope_path                        ltree NOT NULL,
    updated_at                        timestamptz
);

ALTER TABLE retail.store_rule ADD COLUMN IF NOT EXISTS limit_kind text CONSTRAINT store_rule_limit_kind_chk CHECK (limit_kind IN ('percent', 'amount'));

ALTER TABLE retail.store_rule ADD COLUMN IF NOT EXISTS threshold_percent numeric(18,4);

ALTER TABLE wallet.refund_policy ADD COLUMN IF NOT EXISTS destinations_by_source jsonb;

ALTER TABLE wallet.wallet_type ADD COLUMN IF NOT EXISTS is_auto_reload_allowed boolean DEFAULT true;

ALTER TABLE whitelabel.config_version ADD COLUMN IF NOT EXISTS review_status text DEFAULT 'notRequired' CONSTRAINT config_version_review_status_chk CHECK (review_status IN ('notRequired', 'pending', 'approved', 'rejected'));

ALTER TABLE whitelabel.config_version ADD COLUMN IF NOT EXISTS approval_request_id uuid;

ALTER TABLE whitelabel.custom_domain ADD COLUMN IF NOT EXISTS routing text DEFAULT 'cname' CONSTRAINT custom_domain_routing_chk CHECK (routing IN ('cname', 'delegatedSubdomain', 'apex'));

ALTER TABLE whitelabel.custom_domain ADD COLUMN IF NOT EXISTS dns_records jsonb;

ALTER TABLE whitelabel.custom_domain ADD COLUMN IF NOT EXISTS revalidation text DEFAULT 'none' CONSTRAINT custom_domain_revalidation_chk CHECK (revalidation IN ('none', 'pendingRevalidation', 'timedOut'));

ALTER TABLE whitelabel.custom_domain ADD COLUMN IF NOT EXISTS cname_lost boolean;

ALTER TABLE whitelabel.custom_domain ADD COLUMN IF NOT EXISTS is_primary boolean;

ALTER TABLE whitelabel.custom_domain ADD COLUMN IF NOT EXISTS readiness jsonb;

ALTER TABLE whitelabel.homepage_section ADD COLUMN IF NOT EXISTS template_key text;

ALTER TABLE whitelabel.homepage_section ADD COLUMN IF NOT EXISTS landing_source text DEFAULT 'storefront' CONSTRAINT homepage_section_landing_source_chk CHECK (landing_source IN ('storefront', 'ownSite'));

CREATE TABLE IF NOT EXISTS whitelabel.publish_review_policy (
    id                                uuid PRIMARY KEY NOT NULL,
    is_enabled                        boolean NOT NULL DEFAULT false,
    reviewer_must_differ_from_author  boolean DEFAULT true,
    applies_to                        text[],
    scope_path                        ltree NOT NULL
);

CREATE TABLE IF NOT EXISTS whitelabel.site_package (
    id                                uuid PRIMARY KEY NOT NULL,
    version                           text,
    status                            text NOT NULL CONSTRAINT site_package_status_chk CHECK (status IN ('building', 'ready', 'failed')),
    download_url                      text,
    expires_at                        timestamptz,
    requested_by_principal_id         uuid,
    platform_staff_grant_id           uuid,
    created_at                        timestamptz,
    scope_path                        ltree NOT NULL
);

CREATE INDEX IF NOT EXISTS sales_order_charge_fx_rate_id_idx ON orders.sales_order (charge_fx_rate_id);

CREATE INDEX IF NOT EXISTS analytics_governance_policy_scope_path_idx ON reporting.analytics_governance_policy USING gist (scope_path);

CREATE INDEX IF NOT EXISTS cookie_scan_finding_scope_path_idx ON marketing.cookie_scan_finding USING gist (scope_path);

CREATE INDEX IF NOT EXISTS event_change_treatment_policy_scope_path_idx ON catalogue.event_change_treatment_policy USING gist (scope_path);

CREATE INDEX IF NOT EXISTS hardware_certification_scope_path_idx ON access.hardware_certification USING gist (scope_path);

CREATE INDEX IF NOT EXISTS kitchen_routing_rule_scope_path_idx ON fnb.kitchen_routing_rule USING gist (scope_path);

CREATE INDEX IF NOT EXISTS prep_sheet_template_scope_path_idx ON fnb.prep_sheet_template USING gist (scope_path);

CREATE INDEX IF NOT EXISTS publish_review_policy_scope_path_idx ON whitelabel.publish_review_policy USING gist (scope_path);

CREATE INDEX IF NOT EXISTS seat_pricing_rule_scope_path_idx ON catalogue.seat_pricing_rule USING gist (scope_path);

CREATE INDEX IF NOT EXISTS site_package_scope_path_idx ON whitelabel.site_package USING gist (scope_path);

CREATE INDEX IF NOT EXISTS spend_ceiling_scope_path_idx ON ai.spend_ceiling USING gist (scope_path);

CREATE INDEX IF NOT EXISTS till_shift_policy_scope_path_idx ON orders.till_shift_policy USING gist (scope_path);

CREATE INDEX IF NOT EXISTS tracking_technology_catalogue_scope_path_idx ON marketing.tracking_technology_catalogue USING gist (scope_path);

CREATE INDEX IF NOT EXISTS waste_approval_policy_scope_path_idx ON fnb.waste_approval_policy USING gist (scope_path);

SELECT platform.apply_scope_rls('access.hardware_certification'::regclass);

SELECT platform.apply_scope_rls('ai.spend_ceiling'::regclass);

SELECT platform.apply_scope_rls('catalogue.event_change_treatment_policy'::regclass);

SELECT platform.apply_scope_rls('catalogue.seat_pricing_rule'::regclass);

SELECT platform.apply_scope_rls('fnb.kitchen_routing_rule'::regclass);

SELECT platform.apply_scope_rls('fnb.prep_sheet_template'::regclass);

SELECT platform.apply_scope_rls('fnb.waste_approval_policy'::regclass);

SELECT platform.apply_scope_rls('marketing.cookie_scan_finding'::regclass);

SELECT platform.apply_scope_rls('marketing.tracking_technology_catalogue'::regclass);

SELECT platform.apply_scope_rls('orders.till_shift_policy'::regclass);

SELECT platform.apply_scope_rls('reporting.analytics_governance_policy'::regclass);

SELECT platform.apply_scope_rls('whitelabel.publish_review_policy'::regclass);

SELECT platform.apply_scope_rls('whitelabel.site_package'::regclass);

INSERT INTO platform.schema_version (version, description, checksum)
VALUES ('V0101', 'after r1 (a1ba956): 13 table(s), 110 column(s), 14 index(es), 13 other statement(s)', 'cd11f5a0659202c95e9112a330873f1f7ba285e402e22c22f292430e29b1cd59')
ON CONFLICT (version) DO NOTHING;

-- ============================================================================
-- ROLLBACK
-- ============================================================================
-- Commented out so that applying this file never runs it: the rollback is run by removing the
-- leading `-- `, and is tested in CI against a restored snapshot (backend/MIGRATIONS.md).
-- DROP INDEX IF EXISTS fnb.waste_approval_policy_scope_path_idx;
-- DROP INDEX IF EXISTS marketing.tracking_technology_catalogue_scope_path_idx;
-- DROP INDEX IF EXISTS orders.till_shift_policy_scope_path_idx;
-- DROP INDEX IF EXISTS ai.spend_ceiling_scope_path_idx;
-- DROP INDEX IF EXISTS whitelabel.site_package_scope_path_idx;
-- DROP INDEX IF EXISTS catalogue.seat_pricing_rule_scope_path_idx;
-- DROP INDEX IF EXISTS whitelabel.publish_review_policy_scope_path_idx;
-- DROP INDEX IF EXISTS fnb.prep_sheet_template_scope_path_idx;
-- DROP INDEX IF EXISTS fnb.kitchen_routing_rule_scope_path_idx;
-- DROP INDEX IF EXISTS access.hardware_certification_scope_path_idx;
-- DROP INDEX IF EXISTS catalogue.event_change_treatment_policy_scope_path_idx;
-- DROP INDEX IF EXISTS marketing.cookie_scan_finding_scope_path_idx;
-- DROP INDEX IF EXISTS reporting.analytics_governance_policy_scope_path_idx;
-- DROP INDEX IF EXISTS orders.sales_order_charge_fx_rate_id_idx;
-- DROP TABLE IF EXISTS whitelabel.site_package;
-- DROP TABLE IF EXISTS whitelabel.publish_review_policy;
-- ALTER TABLE whitelabel.homepage_section DROP COLUMN IF EXISTS landing_source;
-- ALTER TABLE whitelabel.homepage_section DROP COLUMN IF EXISTS template_key;
-- ALTER TABLE whitelabel.custom_domain DROP COLUMN IF EXISTS readiness;
-- ALTER TABLE whitelabel.custom_domain DROP COLUMN IF EXISTS is_primary;
-- ALTER TABLE whitelabel.custom_domain DROP COLUMN IF EXISTS cname_lost;
-- ALTER TABLE whitelabel.custom_domain DROP COLUMN IF EXISTS revalidation;
-- ALTER TABLE whitelabel.custom_domain DROP COLUMN IF EXISTS dns_records;
-- ALTER TABLE whitelabel.custom_domain DROP COLUMN IF EXISTS routing;
-- ALTER TABLE whitelabel.config_version DROP COLUMN IF EXISTS approval_request_id;
-- ALTER TABLE whitelabel.config_version DROP COLUMN IF EXISTS review_status;
-- ALTER TABLE wallet.wallet_type DROP COLUMN IF EXISTS is_auto_reload_allowed;
-- ALTER TABLE wallet.refund_policy DROP COLUMN IF EXISTS destinations_by_source;
-- ALTER TABLE retail.store_rule DROP COLUMN IF EXISTS threshold_percent;
-- ALTER TABLE retail.store_rule DROP COLUMN IF EXISTS limit_kind;
-- DROP TABLE IF EXISTS reporting.analytics_governance_policy;
-- ALTER TABLE platform.workstation DROP COLUMN IF EXISTS cash_drawer_limit;
-- ALTER TABLE platform.workstation DROP COLUMN IF EXISTS sale_board_source;
-- ALTER TABLE platform.workstation DROP COLUMN IF EXISTS outlet_id;
-- ALTER TABLE platform.venue_settings DROP COLUMN IF EXISTS cash_drawer_limit;
-- ALTER TABLE platform.region_settings DROP COLUMN IF EXISTS minor_age_threshold;
-- ALTER TABLE platform.region_settings DROP COLUMN IF EXISTS required_billing_documents;
-- ALTER TABLE platform.region_settings DROP COLUMN IF EXISTS local_language_name_locales;
-- ALTER TABLE platform.region_settings DROP COLUMN IF EXISTS ai_residency_opt_in;
-- ALTER TABLE platform.region_settings DROP COLUMN IF EXISTS is_ai_residency_class_locked;
-- ALTER TABLE platform.region_settings DROP COLUMN IF EXISTS ai_residency_class;
-- ALTER TABLE platform.outlet DROP COLUMN IF EXISTS sale_board_id;
-- ALTER TABLE platform.outlet DROP COLUMN IF EXISTS produces_for_outlet_ids;
-- ALTER TABLE platform.outlet DROP COLUMN IF EXISTS admission_context;
-- ALTER TABLE platform.outlet DROP COLUMN IF EXISTS payment_timing;
-- ALTER TABLE platform.outlet DROP COLUMN IF EXISTS department_id;
-- ALTER TABLE platform.outlet DROP COLUMN IF EXISTS outlet_type;
-- ALTER TABLE platform.outlet DROP COLUMN IF EXISTS name_translations;
-- ALTER TABLE platform.device DROP COLUMN IF EXISTS approved_at;
-- ALTER TABLE platform.device DROP COLUMN IF EXISTS approved_by_principal_id;
-- ALTER TABLE platform.device DROP COLUMN IF EXISTS tested_by_principal_id;
-- ALTER TABLE platform.device DROP COLUMN IF EXISTS enrolment_code_expires_at;
-- ALTER TABLE platform.device DROP COLUMN IF EXISTS enrolment_code;
-- ALTER TABLE platform.device DROP COLUMN IF EXISTS approval_status;
-- ALTER TABLE platform.device DROP COLUMN IF EXISTS test_result;
-- ALTER TABLE pii.subject_biometric DROP COLUMN IF EXISTS consent_form_version;
-- ALTER TABLE pii.subject_biometric DROP COLUMN IF EXISTS consent_form_id;
-- ALTER TABLE pii.subject_biometric DROP COLUMN IF EXISTS enrolment_channel;
-- DROP TABLE IF EXISTS orders.till_shift_policy;
-- ALTER TABLE orders.pos_shift DROP COLUMN IF EXISTS count_number;
-- ALTER TABLE orders.pos_shift DROP COLUMN IF EXISTS recount_reason;
-- ALTER TABLE orders.pos_shift DROP COLUMN IF EXISTS recount_requested_by_principal_id;
-- ALTER TABLE orders.pos_shift DROP COLUMN IF EXISTS recount_requested_at;
-- ALTER TABLE orders.pos_shift DROP COLUMN IF EXISTS cashier_note;
-- ALTER TABLE orders.pos_shift DROP COLUMN IF EXISTS cashier_reason;
-- DROP TABLE IF EXISTS marketing.tracking_technology_catalogue;
-- ALTER TABLE marketing.segment DROP COLUMN IF EXISTS requires_approval;
-- ALTER TABLE marketing.segment DROP COLUMN IF EXISTS owner_principal_id;
-- ALTER TABLE marketing.segment DROP COLUMN IF EXISTS effective_to;
-- ALTER TABLE marketing.segment DROP COLUMN IF EXISTS effective_from;
-- ALTER TABLE marketing.segment DROP COLUMN IF EXISTS rule_groups;
-- ALTER TABLE marketing.form_definition DROP COLUMN IF EXISTS consent_purposes;
-- ALTER TABLE marketing.cookie_scan_run DROP COLUMN IF EXISTS pre_consent_violation_count;
-- ALTER TABLE marketing.cookie_scan_policy DROP COLUMN IF EXISTS scanner_vendor_ref;
-- ALTER TABLE marketing.cookie_scan_policy DROP COLUMN IF EXISTS scan_source;
-- DROP TABLE IF EXISTS marketing.cookie_scan_finding;
-- ALTER TABLE identity.role DROP COLUMN IF EXISTS preset_code;
-- ALTER TABLE identity.guest_verification_policy DROP COLUMN IF EXISTS verification_provider;
-- ALTER TABLE identity.capability_template DROP COLUMN IF EXISTS is_preset;
-- ALTER TABLE identity.capability_template DROP COLUMN IF EXISTS preset_level;
-- ALTER TABLE identity.capability_template DROP COLUMN IF EXISTS module;
-- ALTER TABLE games.reader_sync_status DROP COLUMN IF EXISTS refusing_offline_taps;
-- ALTER TABLE games.reader_sync_status DROP COLUMN IF EXISTS offline_since;
-- ALTER TABLE games.pricing DROP COLUMN IF EXISTS retry_offer_lead_seconds;
-- ALTER TABLE games.entitlement DROP COLUMN IF EXISTS covers_games_added_later;
-- DROP TABLE IF EXISTS fnb.waste_approval_policy;
-- ALTER TABLE fnb.table_reservation DROP COLUMN IF EXISTS taken_by_principal_id;
-- ALTER TABLE fnb.table_reservation DROP COLUMN IF EXISTS occasion;
-- ALTER TABLE fnb.table_reservation DROP COLUMN IF EXISTS seating_preference;
-- ALTER TABLE fnb.sold_out_item DROP COLUMN IF EXISTS source;
-- ALTER TABLE fnb.service_order DROP COLUMN IF EXISTS sent_to_kitchen_at;
-- ALTER TABLE fnb.service_order DROP COLUMN IF EXISTS payment_timing;
-- ALTER TABLE fnb.reservation_policy DROP COLUMN IF EXISTS reserved_lead_minutes;
-- DROP TABLE IF EXISTS fnb.prep_sheet_template;
-- ALTER TABLE fnb.menu_item DROP COLUMN IF EXISTS remaining_count;
-- ALTER TABLE fnb.menu_item DROP COLUMN IF EXISTS daily_count;
-- ALTER TABLE fnb.kitchen_station DROP COLUMN IF EXISTS serves_outlet_ids;
-- ALTER TABLE fnb.kitchen_station DROP COLUMN IF EXISTS printer_device_ids;
-- DROP TABLE IF EXISTS fnb.kitchen_routing_rule;
-- DROP TABLE IF EXISTS catalogue.seat_pricing_rule;
-- DROP TABLE IF EXISTS catalogue.event_change_treatment_policy;
-- ALTER TABLE approvals.rule DROP COLUMN IF EXISTS signature_methods;
-- ALTER TABLE approvals.rule DROP COLUMN IF EXISTS subject_types;
-- ALTER TABLE approvals.request DROP COLUMN IF EXISTS assigned_at;
-- ALTER TABLE approvals.request DROP COLUMN IF EXISTS assigned_to_department_id;
-- ALTER TABLE approvals.request DROP COLUMN IF EXISTS assigned_to_principal_id;
-- DROP TABLE IF EXISTS ai.spend_ceiling;
-- ALTER TABLE ai.release DROP COLUMN IF EXISTS module;
-- ALTER TABLE ai.provider DROP COLUMN IF EXISTS residency_classes;
-- ALTER TABLE ai.provider DROP COLUMN IF EXISTS compatibility;
-- ALTER TABLE ai.provider DROP COLUMN IF EXISTS credential_hint;
-- ALTER TABLE ai.provider DROP COLUMN IF EXISTS vendor;
-- ALTER TABLE ai.policy DROP COLUMN IF EXISTS autonomy_overrides;
-- ALTER TABLE ai.policy DROP COLUMN IF EXISTS ceiling_behaviour_by_capability;
-- ALTER TABLE ai.policy DROP COLUMN IF EXISTS scrubbing;
-- ALTER TABLE ai.model DROP COLUMN IF EXISTS residency_classes;
-- ALTER TABLE ai.model DROP COLUMN IF EXISTS curated_range;
-- ALTER TABLE ai.model DROP COLUMN IF EXISTS vendor;
-- ALTER TABLE ai.incident DROP COLUMN IF EXISTS lessons_learned;
-- ALTER TABLE ai.incident DROP COLUMN IF EXISTS control_failure;
-- ALTER TABLE ai.incident DROP COLUMN IF EXISTS impact;
-- ALTER TABLE ai.forecast_version DROP COLUMN IF EXISTS module;
-- ALTER TABLE ai.forecast_definition DROP COLUMN IF EXISTS module;
-- ALTER TABLE ai.byok_enablement DROP COLUMN IF EXISTS task_model_map;
-- ALTER TABLE accreditation.programme DROP COLUMN IF EXISTS identity_verification;
-- ALTER TABLE accreditation.programme DROP COLUMN IF EXISTS face_matching;
-- ALTER TABLE access.operating_calendar_entry DROP COLUMN IF EXISTS priority;
-- ALTER TABLE access.operating_calendar_entry DROP COLUMN IF EXISTS is_venue_closed;
-- ALTER TABLE access.journey_sequence_rule DROP COLUMN IF EXISTS applies_to;
-- DROP TABLE IF EXISTS access.hardware_certification;
-- ALTER TABLE access.gate_mode_change DROP COLUMN IF EXISTS to_direction;
-- ALTER TABLE access.gate_mode_change DROP COLUMN IF EXISTS from_direction;
-- ALTER TABLE access.entitlement DROP COLUMN IF EXISTS cancellation_kind;
-- ALTER TABLE access.entitlement DROP COLUMN IF EXISTS time_bound_until;
-- ALTER TABLE access.entitlement DROP COLUMN IF EXISTS first_entry_at;
-- ALTER TABLE access.access_point DROP COLUMN IF EXISTS temporary_closure;
-- ALTER TABLE access.access_area DROP COLUMN IF EXISTS security_classification_level;
-- DELETE FROM platform.schema_version WHERE version = 'V0101';
