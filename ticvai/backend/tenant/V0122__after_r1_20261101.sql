-- V0122 -- tenant database, after r1 (9cec72d) (20261101).
-- **Written by tools/derive-ddl.py in frozen mode. Do not edit after merge; a mistake is a new migration.**
--
-- The baseline under backend/tenant/ is frozen at r1 (9cec72d), so the change to the schema reference
-- since then is written here instead: additive only. Changes that are not additive (drops, renames,
-- type changes) are not generated; they are listed for a person in handoff/migration-review.md.
-- Every statement that needs a table is a guarded block (CHG-R9MIG-002): it does nothing where its table
-- or a column it names is not there yet, so the file applies as one transaction, twice, on any database;
-- the migration that creates such a table later copies the block. A table's policy change is one block.
-- 2 table(s), 30 column(s), 17 index(es), 19 other statement(s), 2 row-level security polic(ies) re-applied.

DO $$ BEGIN IF to_regclass('access.biometric_profile') IS NOT NULL THEN
ALTER TABLE access.biometric_profile ADD COLUMN IF NOT EXISTS consent_form_id uuid;
END IF; END $$;

DO $$ BEGIN IF to_regclass('access.device_placement') IS NOT NULL THEN
ALTER TABLE access.device_placement ADD COLUMN IF NOT EXISTS activation_zone jsonb;
END IF; END $$;

DO $$ BEGIN IF to_regclass('access.gate_mode_change') IS NOT NULL THEN
ALTER TABLE access.gate_mode_change ADD COLUMN IF NOT EXISTS target_turnstile_mode text;
END IF; END $$;

DO $$ BEGIN IF to_regclass('catalogue.channel_envelope') IS NOT NULL THEN
ALTER TABLE catalogue.channel_envelope ADD COLUMN IF NOT EXISTS envelope_percent numeric(18,4);
END IF; END $$;

DO $$ BEGIN IF to_regclass('catalogue.channel_envelope') IS NOT NULL THEN
ALTER TABLE catalogue.channel_envelope ADD COLUMN IF NOT EXISTS released_units integer DEFAULT 0;
END IF; END $$;

DO $$ BEGIN IF to_regclass('catalogue.channel_envelope') IS NOT NULL THEN
ALTER TABLE catalogue.channel_envelope ADD COLUMN IF NOT EXISTS returned_units integer DEFAULT 0;
END IF; END $$;

CREATE TABLE IF NOT EXISTS catalogue.competitor_price_observation (
    id                                uuid PRIMARY KEY NOT NULL,
    scope_path                        ltree NOT NULL,
    demand_signal_id                  uuid NOT NULL,
    price_date                        date NOT NULL,
    timeslot                          text CONSTRAINT competitor_price_observation_timeslot_chk CHECK (char_length(timeslot) <= 40),
    published_amount                  numeric(18,4),
    promotional_amount                numeric(18,4),
    weekend_amount                    numeric(18,4),
    peak_amount                       numeric(18,4),
    resident_amount                   numeric(18,4),
    member_amount                     numeric(18,4),
    currency_code                     text NOT NULL CONSTRAINT competitor_price_observation_currency_code_chk CHECK (char_length(currency_code) <= 3),
    availability                      text NOT NULL DEFAULT 'unknown' CONSTRAINT competitor_price_observation_availability_chk CHECK (availability IN ('available', 'limited', 'soldOut', 'unknown')),
    observed_at                       timestamptz NOT NULL,
    created_at                        timestamptz NOT NULL
);

DO $$ BEGIN IF to_regclass('catalogue.demand_forecast') IS NOT NULL THEN
ALTER TABLE catalogue.demand_forecast ADD COLUMN IF NOT EXISTS day_type text CONSTRAINT demand_forecast_day_type_chk CHECK (day_type IN ('weekday', 'weekend'));
END IF; END $$;

DO $$ BEGIN IF to_regclass('catalogue.demand_forecast') IS NOT NULL THEN
ALTER TABLE catalogue.demand_forecast ADD COLUMN IF NOT EXISTS peak_period text CONSTRAINT demand_forecast_peak_period_chk CHECK (peak_period IN ('peak', 'offPeak'));
END IF; END $$;

DO $$ BEGIN IF to_regclass('catalogue.demand_forecast') IS NOT NULL THEN
ALTER TABLE catalogue.demand_forecast ADD COLUMN IF NOT EXISTS season text CONSTRAINT demand_forecast_season_chk CHECK (char_length(season) <= 60);
END IF; END $$;

DO $$ BEGIN IF to_regclass('catalogue.demand_forecast') IS NOT NULL THEN
ALTER TABLE catalogue.demand_forecast ADD COLUMN IF NOT EXISTS event_proximity_from_days integer;
END IF; END $$;

DO $$ BEGIN IF to_regclass('catalogue.demand_forecast') IS NOT NULL THEN
ALTER TABLE catalogue.demand_forecast ADD COLUMN IF NOT EXISTS event_proximity_to_days integer;
END IF; END $$;

DO $$ BEGIN IF to_regclass('catalogue.dynamic_pricing_control') IS NOT NULL THEN
ALTER TABLE catalogue.dynamic_pricing_control ADD COLUMN IF NOT EXISTS pending_automation_level text CONSTRAINT dynamic_pricing_control_pending_automation_level_chk CHECK (pending_automation_level IN ('advisory', 'humanInTheLoop', 'conditionalAutonomous', 'autonomous'));
END IF; END $$;

DO $$ BEGIN IF to_regclass('catalogue.dynamic_pricing_control') IS NOT NULL THEN
ALTER TABLE catalogue.dynamic_pricing_control ADD COLUMN IF NOT EXISTS pending_approval_request_id uuid;
END IF; END $$;

DO $$ BEGIN IF to_regclass('marketing.message_dispatch') IS NOT NULL THEN
ALTER TABLE marketing.message_dispatch ADD COLUMN IF NOT EXISTS source_ref text;
END IF; END $$;

DO $$ BEGIN IF to_regclass('platform.audit_record') IS NOT NULL THEN
ALTER TABLE platform.audit_record ADD COLUMN IF NOT EXISTS reason text CONSTRAINT audit_record_reason_chk CHECK (char_length(reason) <= 500);
END IF; END $$;

DO $$ BEGIN IF to_regclass('platform.workstation') IS NOT NULL THEN
ALTER TABLE platform.workstation ADD COLUMN IF NOT EXISTS channel text NOT NULL DEFAULT 'pos' CONSTRAINT workstation_channel_chk CHECK (channel IN ('pos', 'kiosk'));
END IF; END $$;

DO $$ BEGIN IF to_regclass('pricing.dynamic_price_rule') IS NOT NULL THEN
ALTER TABLE pricing.dynamic_price_rule ADD COLUMN IF NOT EXISTS dimension text CONSTRAINT dynamic_price_rule_dimension_chk CHECK (dimension IN ('channel', 'customerSegment', 'location'));
END IF; END $$;

DO $$ BEGIN IF to_regclass('pricing.dynamic_price_rule') IS NOT NULL THEN
ALTER TABLE pricing.dynamic_price_rule ADD COLUMN IF NOT EXISTS sales_channel text;
END IF; END $$;

DO $$ BEGIN IF to_regclass('pricing.dynamic_price_rule') IS NOT NULL THEN
ALTER TABLE pricing.dynamic_price_rule ADD COLUMN IF NOT EXISTS customer_segment text CONSTRAINT dynamic_price_rule_customer_segment_chk CHECK (customer_segment IN ('standardCustomer', 'member', 'loyaltyTier', 'resident', 'vip', 'corporate', 'group', 'b2b', 'customSegment'));
END IF; END $$;

DO $$ BEGIN IF to_regclass('pricing.dynamic_price_rule') IS NOT NULL THEN
ALTER TABLE pricing.dynamic_price_rule ADD COLUMN IF NOT EXISTS segment_ref text CONSTRAINT dynamic_price_rule_segment_ref_chk CHECK (char_length(segment_ref) <= 100);
END IF; END $$;

DO $$ BEGIN IF to_regclass('pricing.dynamic_price_rule') IS NOT NULL THEN
ALTER TABLE pricing.dynamic_price_rule ADD COLUMN IF NOT EXISTS location_level text CONSTRAINT dynamic_price_rule_location_level_chk CHECK (location_level IN ('country', 'market', 'venue', 'attraction', 'zone', 'eventLocation'));
END IF; END $$;

DO $$ BEGIN IF to_regclass('pricing.dynamic_price_rule') IS NOT NULL THEN
ALTER TABLE pricing.dynamic_price_rule ADD COLUMN IF NOT EXISTS location_id text CONSTRAINT dynamic_price_rule_location_id_chk CHECK (char_length(location_id) <= 100);
END IF; END $$;

DO $$ BEGIN IF to_regclass('pricing.dynamic_price_rule') IS NOT NULL THEN
ALTER TABLE pricing.dynamic_price_rule ADD COLUMN IF NOT EXISTS is_dynamic_pricing_enabled boolean DEFAULT true;
END IF; END $$;

DO $$ BEGIN IF to_regclass('seating.seat_map_template') IS NOT NULL THEN
ALTER TABLE seating.seat_map_template ADD COLUMN IF NOT EXISTS scope_path ltree;
END IF; END $$;

DO $$ BEGIN IF to_regclass('seating.seat_map_template') IS NOT NULL THEN
ALTER TABLE seating.seat_map_template ADD COLUMN IF NOT EXISTS source_seat_map_id uuid;
END IF; END $$;

DO $$ BEGIN IF to_regclass('seating.seat_map_template') IS NOT NULL THEN
ALTER TABLE seating.seat_map_template ADD COLUMN IF NOT EXISTS structure jsonb;
END IF; END $$;

DO $$ BEGIN IF to_regclass('seating.seat_map_template') IS NOT NULL THEN
ALTER TABLE seating.seat_map_template ADD COLUMN IF NOT EXISTS view_box jsonb;
END IF; END $$;

DO $$ BEGIN IF to_regclass('seating.seat_map_template') IS NOT NULL THEN
ALTER TABLE seating.seat_map_template ADD COLUMN IF NOT EXISTS stage_position jsonb;
END IF; END $$;

DO $$ BEGIN IF to_regclass('seating.section') IS NOT NULL THEN
ALTER TABLE seating.section ADD COLUMN IF NOT EXISTS seat_map_id uuid;
END IF; END $$;

DO $$ BEGIN IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'whitelabel' AND table_name = 'banner' AND column_name = 'tenant_config_id' AND is_nullable = 'NO') THEN ALTER TABLE whitelabel.banner ALTER COLUMN tenant_config_id DROP NOT NULL; END IF; END $$;

DO $$ BEGIN IF to_regclass('whitelabel.kiosk_config') IS NOT NULL THEN
ALTER TABLE whitelabel.kiosk_config ADD COLUMN IF NOT EXISTS deleted_at timestamptz;
END IF; END $$;

CREATE TABLE IF NOT EXISTS workforce.guest_broadcast (
    id                                uuid PRIMARY KEY NOT NULL,
    venue_id                          uuid NOT NULL,
    kind                              text NOT NULL CONSTRAINT guest_broadcast_kind_chk CHECK (kind IN ('evacuation', 'weather', 'rideClosure', 'lostChild', 'operational', 'allClear')),
    message                           text NOT NULL CONSTRAINT guest_broadcast_message_chk CHECK (char_length(message) <= 300),
    message_localised                 jsonb,
    assembly_point_ids                text[],
    sent_by_principal_id              uuid NOT NULL,
    second_principal_id               uuid,
    recipient_count                   integer NOT NULL,
    accepted_at                       timestamptz NOT NULL,
    scope_path                        ltree NOT NULL
);

DO $$ BEGIN IF to_regclass('catalogue.competitor_price_observation') IS NOT NULL AND to_regclass('catalogue.demand_signal') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'catalogue' AND table_name = 'competitor_price_observation' AND column_name = 'demand_signal_id') AND NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'competitor_price_observation_demand_signal_id_fkey' AND conrelid = to_regclass('catalogue.competitor_price_observation')) THEN
ALTER TABLE catalogue.competitor_price_observation ADD CONSTRAINT competitor_price_observation_demand_signal_id_fkey FOREIGN KEY (demand_signal_id) REFERENCES catalogue.demand_signal(id);
END IF; END $$;

DO $$ BEGIN IF to_regclass('seating.seat_map_template') IS NOT NULL AND to_regclass('seating.seat_map') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'seating' AND table_name = 'seat_map_template' AND column_name = 'source_seat_map_id') AND NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'seat_map_template_source_seat_map_id_fkey' AND conrelid = to_regclass('seating.seat_map_template')) THEN
ALTER TABLE seating.seat_map_template ADD CONSTRAINT seat_map_template_source_seat_map_id_fkey FOREIGN KEY (source_seat_map_id) REFERENCES seating.seat_map(id);
END IF; END $$;

DO $$ BEGIN IF to_regclass('seating.section') IS NOT NULL AND to_regclass('seating.seat_map') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'seating' AND table_name = 'section' AND column_name = 'seat_map_id') AND NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'section_seat_map_id_fkey' AND conrelid = to_regclass('seating.section')) THEN
ALTER TABLE seating.section ADD CONSTRAINT section_seat_map_id_fkey FOREIGN KEY (seat_map_id) REFERENCES seating.seat_map(id);
END IF; END $$;

DO $$ BEGIN IF to_regclass('workforce.guest_broadcast') IS NOT NULL AND to_regclass('identity.principal') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'workforce' AND table_name = 'guest_broadcast' AND column_name = 'second_principal_id') AND NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'guest_broadcast_second_principal_id_fkey' AND conrelid = to_regclass('workforce.guest_broadcast')) THEN
ALTER TABLE workforce.guest_broadcast ADD CONSTRAINT guest_broadcast_second_principal_id_fkey FOREIGN KEY (second_principal_id) REFERENCES identity.principal(id);
END IF; END $$;

DO $$ BEGIN IF to_regclass('workforce.guest_broadcast') IS NOT NULL AND to_regclass('identity.principal') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'workforce' AND table_name = 'guest_broadcast' AND column_name = 'sent_by_principal_id') AND NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'guest_broadcast_sent_by_principal_id_fkey' AND conrelid = to_regclass('workforce.guest_broadcast')) THEN
ALTER TABLE workforce.guest_broadcast ADD CONSTRAINT guest_broadcast_sent_by_principal_id_fkey FOREIGN KEY (sent_by_principal_id) REFERENCES identity.principal(id);
END IF; END $$;

DO $$ BEGIN IF to_regclass('workforce.guest_broadcast') IS NOT NULL AND to_regclass('platform.scope') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'workforce' AND table_name = 'guest_broadcast' AND column_name = 'venue_id') AND NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'guest_broadcast_venue_id_fkey' AND conrelid = to_regclass('workforce.guest_broadcast')) THEN
ALTER TABLE workforce.guest_broadcast ADD CONSTRAINT guest_broadcast_venue_id_fkey FOREIGN KEY (venue_id) REFERENCES platform.scope(id);
END IF; END $$;

DO $$ BEGIN IF to_regclass('catalogue.dynamic_pricing_control') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'catalogue' AND table_name = 'dynamic_pricing_control' AND column_name = 'pending_approval_request_id') THEN
CREATE INDEX IF NOT EXISTS dynamic_pricing_control_pending_approval_request_id_idx ON catalogue.dynamic_pricing_control (pending_approval_request_id);
END IF; END $$;

DO $$ BEGIN IF to_regclass('catalogue.competitor_price_observation') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'catalogue' AND table_name = 'competitor_price_observation' AND column_name = 'demand_signal_id') AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'catalogue' AND table_name = 'competitor_price_observation' AND column_name = 'observed_at') AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'catalogue' AND table_name = 'competitor_price_observation' AND column_name = 'price_date') AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'catalogue' AND table_name = 'competitor_price_observation' AND column_name = 'timeslot') THEN
CREATE INDEX IF NOT EXISTS competitor_price_observation_demand_signal_id_pric_f60f9715_idx ON catalogue.competitor_price_observation (demand_signal_id, price_date, timeslot, observed_at);
END IF; END $$;

DO $$ BEGIN IF to_regclass('marketing.message_dispatch') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'marketing' AND table_name = 'message_dispatch' AND column_name = 'source_ref') THEN
CREATE INDEX IF NOT EXISTS message_dispatch_source_ref_idx ON marketing.message_dispatch (source_ref);
END IF; END $$;

DO $$ BEGIN IF to_regclass('catalogue.competitor_price_observation') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'catalogue' AND table_name = 'competitor_price_observation' AND column_name = 'demand_signal_id') THEN
CREATE INDEX IF NOT EXISTS competitor_price_observation_demand_signal_id_idx ON catalogue.competitor_price_observation (demand_signal_id);
END IF; END $$;

DO $$ BEGIN IF to_regclass('pricing.dynamic_price_rule') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'pricing' AND table_name = 'dynamic_price_rule' AND column_name = 'channel_id') THEN
CREATE INDEX IF NOT EXISTS dynamic_price_rule_channel_id_idx ON pricing.dynamic_price_rule (channel_id);
END IF; END $$;

DO $$ BEGIN IF to_regclass('seating.seat_map_template') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'seating' AND table_name = 'seat_map_template' AND column_name = 'source_seat_map_id') THEN
CREATE INDEX IF NOT EXISTS seat_map_template_source_seat_map_id_idx ON seating.seat_map_template (source_seat_map_id);
END IF; END $$;

DO $$ BEGIN IF to_regclass('seating.section') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'seating' AND table_name = 'section' AND column_name = 'seat_map_id') THEN
CREATE INDEX IF NOT EXISTS section_seat_map_id_idx ON seating.section (seat_map_id);
END IF; END $$;

DO $$ BEGIN IF to_regclass('workforce.guest_broadcast') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'workforce' AND table_name = 'guest_broadcast' AND column_name = 'second_principal_id') THEN
CREATE INDEX IF NOT EXISTS guest_broadcast_second_principal_id_idx ON workforce.guest_broadcast (second_principal_id);
END IF; END $$;

DO $$ BEGIN IF to_regclass('workforce.guest_broadcast') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'workforce' AND table_name = 'guest_broadcast' AND column_name = 'sent_by_principal_id') THEN
CREATE INDEX IF NOT EXISTS guest_broadcast_sent_by_principal_id_idx ON workforce.guest_broadcast (sent_by_principal_id);
END IF; END $$;

DO $$ BEGIN IF to_regclass('workforce.guest_broadcast') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'workforce' AND table_name = 'guest_broadcast' AND column_name = 'venue_id') THEN
CREATE INDEX IF NOT EXISTS guest_broadcast_venue_id_idx ON workforce.guest_broadcast (venue_id);
END IF; END $$;

DO $$ BEGIN IF to_regclass('catalogue.sales_channel') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'catalogue' AND table_name = 'sales_channel' AND column_name = 'code') THEN
CREATE UNIQUE INDEX IF NOT EXISTS sales_channel_code_uniq ON catalogue.sales_channel (lower(code));
END IF; END $$;

DO $$ BEGIN IF to_regclass('catalogue.calculation_profile') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'catalogue' AND table_name = 'calculation_profile' AND column_name = 'code') AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'catalogue' AND table_name = 'calculation_profile' AND column_name = 'scope_path') AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'catalogue' AND table_name = 'calculation_profile' AND column_name = 'version') THEN
CREATE UNIQUE INDEX IF NOT EXISTS calculation_profile_scope_path_code_version_uniq ON catalogue.calculation_profile (scope_path, lower(code), version);
END IF; END $$;

DO $$ BEGIN IF to_regclass('seating.section') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'seating' AND table_name = 'section' AND column_name = 'code') AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'seating' AND table_name = 'section' AND column_name = 'seat_map_id') THEN
CREATE UNIQUE INDEX IF NOT EXISTS section_seat_map_id_code_uniq ON seating.section (seat_map_id, code);
END IF; END $$;

DO $$ BEGIN IF to_regclass('whitelabel.policy') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'whitelabel' AND table_name = 'policy' AND column_name = 'kind') AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'whitelabel' AND table_name = 'policy' AND column_name = 'version') THEN
CREATE UNIQUE INDEX IF NOT EXISTS policy_kind_version_uniq ON whitelabel.policy (lower(kind), lower(version));
END IF; END $$;

DO $$ BEGIN IF to_regclass('catalogue.competitor_price_observation') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'catalogue' AND table_name = 'competitor_price_observation' AND column_name = 'scope_path') THEN
CREATE INDEX IF NOT EXISTS competitor_price_observation_scope_path_idx ON catalogue.competitor_price_observation USING gist (scope_path);
END IF; END $$;

DO $$ BEGIN IF to_regclass('workforce.guest_broadcast') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'workforce' AND table_name = 'guest_broadcast' AND column_name = 'scope_path') THEN
CREATE INDEX IF NOT EXISTS guest_broadcast_scope_path_idx ON workforce.guest_broadcast USING gist (scope_path);
END IF; END $$;

DO $$ BEGIN IF to_regclass('seating.seat_map_template') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'seating' AND table_name = 'seat_map_template' AND column_name = 'scope_path') THEN
CREATE INDEX IF NOT EXISTS seat_map_template_scope_path_idx ON seating.seat_map_template USING gist (scope_path);
END IF; END $$;

DO $$ BEGIN IF to_regclass('catalogue.competitor_price_observation') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'catalogue' AND table_name = 'competitor_price_observation' AND column_name = 'scope_path') THEN
PERFORM platform.apply_scope_rls('catalogue.competitor_price_observation'::regclass);
END IF; END $$;

DO $$ BEGIN IF to_regclass('workforce.guest_broadcast') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'workforce' AND table_name = 'guest_broadcast' AND column_name = 'scope_path') THEN
PERFORM platform.apply_scope_rls('workforce.guest_broadcast'::regclass);
END IF; END $$;

DO $$ BEGIN IF to_regclass('seating.seat_map_template') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'seating' AND table_name = 'seat_map_template' AND column_name = 'scope_path') THEN
PERFORM platform.drop_rls_policies('seating.seat_map_template'::regclass);
PERFORM platform.apply_read_beneath_rls('seating.seat_map_template'::regclass);
END IF; END $$;

DO $$ BEGIN IF to_regclass('whitelabel.module_enablement') IS NOT NULL THEN
PERFORM platform.drop_rls_policies('whitelabel.module_enablement'::regclass);
PERFORM platform.apply_grant_holder_read_rls('whitelabel.module_enablement'::regclass, 'platform.tenant_root_in_scope()');
END IF; END $$;

DO $$ BEGIN IF EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'operations') AND EXISTS (SELECT 1 FROM pg_namespace WHERE nspname = 'access') THEN GRANT USAGE ON SCHEMA access TO operations; END IF; END $$;

DO $$ BEGIN IF EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'operations') AND to_regclass('access.entitlement') IS NOT NULL THEN GRANT SELECT ON access.entitlement TO operations; END IF; END $$;

DO $$ BEGIN IF EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'operations') AND EXISTS (SELECT 1 FROM pg_namespace WHERE nspname = 'payments') THEN GRANT USAGE ON SCHEMA payments TO operations; END IF; END $$;

DO $$ BEGIN IF EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'operations') AND to_regclass('payments.method') IS NOT NULL THEN GRANT SELECT ON payments.method TO operations; END IF; END $$;

DO $$ BEGIN IF EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'access') AND to_regclass('platform.device') IS NOT NULL THEN GRANT SELECT ON platform.device TO access; END IF; END $$;

DO $$ BEGIN IF EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'access') AND to_regclass('platform.venue_settings') IS NOT NULL THEN GRANT SELECT ON platform.venue_settings TO access; END IF; END $$;

DO $$ BEGIN IF EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'operations') AND to_regclass('catalogue.event') IS NOT NULL THEN GRANT SELECT ON catalogue.event TO operations; END IF; END $$;

DO $$ BEGIN IF EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'access') AND EXISTS (SELECT 1 FROM pg_namespace WHERE nspname = 'identity') THEN GRANT USAGE ON SCHEMA identity TO access; END IF; END $$;

DO $$ BEGIN IF EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'access') AND to_regclass('identity.delegated_access') IS NOT NULL THEN GRANT SELECT ON identity.delegated_access TO access; END IF; END $$;

DO $$ BEGIN IF EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'access') AND to_regclass('platform.scope') IS NOT NULL THEN GRANT SELECT ON platform.scope TO access; END IF; END $$;

INSERT INTO platform.schema_version (version, description, checksum)
VALUES ('V0122', 'after r1 (9cec72d): 2 table(s), 30 column(s), 17 index(es), 19 other statement(s), 2 row-level security polic(ies) re-applied', '2a329b9f2c1cb1b7a0f92fb15315d37b634b1c338bf7c3c9177d7d041aa383c9')
ON CONFLICT (version) DO NOTHING;

-- ============================================================================
-- ROLLBACK
-- ============================================================================
-- Commented out so that applying this file never runs it: the rollback is run by removing the
-- leading `-- `, and is tested in CI against a restored snapshot (backend/MIGRATIONS.md).
-- REVOKE SELECT ON platform.scope FROM access;
-- REVOKE SELECT ON identity.delegated_access FROM access;
-- REVOKE USAGE ON SCHEMA identity FROM access;
-- REVOKE SELECT ON catalogue.event FROM operations;
-- REVOKE SELECT ON platform.venue_settings FROM access;
-- REVOKE SELECT ON platform.device FROM access;
-- REVOKE SELECT ON payments.method FROM operations;
-- REVOKE USAGE ON SCHEMA payments FROM operations;
-- REVOKE SELECT ON access.entitlement FROM operations;
-- REVOKE USAGE ON SCHEMA access FROM operations;
-- SELECT platform.drop_rls_policies('whitelabel.module_enablement'::regclass); SELECT platform.apply_tenant_rls('whitelabel.module_enablement'::regclass);
-- SELECT platform.drop_rls_policies('seating.seat_map_template'::regclass); SELECT platform.apply_parent_rls('seating.seat_map_template'::regclass, 'region_id', 'platform.scope'::regclass, 'id');
-- DROP INDEX IF EXISTS seating.seat_map_template_scope_path_idx;
-- DROP INDEX IF EXISTS workforce.guest_broadcast_scope_path_idx;
-- DROP INDEX IF EXISTS catalogue.competitor_price_observation_scope_path_idx;
-- DROP INDEX IF EXISTS whitelabel.policy_kind_version_uniq;
-- DROP INDEX IF EXISTS seating.section_seat_map_id_code_uniq;
-- DROP INDEX IF EXISTS catalogue.calculation_profile_scope_path_code_version_uniq;
-- DROP INDEX IF EXISTS catalogue.sales_channel_code_uniq;
-- DROP INDEX IF EXISTS workforce.guest_broadcast_venue_id_idx;
-- DROP INDEX IF EXISTS workforce.guest_broadcast_sent_by_principal_id_idx;
-- DROP INDEX IF EXISTS workforce.guest_broadcast_second_principal_id_idx;
-- DROP INDEX IF EXISTS seating.section_seat_map_id_idx;
-- DROP INDEX IF EXISTS seating.seat_map_template_source_seat_map_id_idx;
-- DROP INDEX IF EXISTS pricing.dynamic_price_rule_channel_id_idx;
-- DROP INDEX IF EXISTS catalogue.competitor_price_observation_demand_signal_id_idx;
-- DROP INDEX IF EXISTS marketing.message_dispatch_source_ref_idx;
-- DROP INDEX IF EXISTS catalogue.competitor_price_observation_demand_signal_id_pric_f60f9715_idx;
-- DROP INDEX IF EXISTS catalogue.dynamic_pricing_control_pending_approval_request_id_idx;
-- ALTER TABLE seating.section DROP CONSTRAINT IF EXISTS section_seat_map_id_fkey;
-- ALTER TABLE seating.seat_map_template DROP CONSTRAINT IF EXISTS seat_map_template_source_seat_map_id_fkey;
-- DROP TABLE IF EXISTS workforce.guest_broadcast;
-- ALTER TABLE whitelabel.kiosk_config DROP COLUMN IF EXISTS deleted_at;
-- ALTER TABLE whitelabel.banner ALTER COLUMN tenant_config_id SET NOT NULL;
-- ALTER TABLE seating.section DROP COLUMN IF EXISTS seat_map_id;
-- ALTER TABLE seating.seat_map_template DROP COLUMN IF EXISTS stage_position;
-- ALTER TABLE seating.seat_map_template DROP COLUMN IF EXISTS view_box;
-- ALTER TABLE seating.seat_map_template DROP COLUMN IF EXISTS structure;
-- ALTER TABLE seating.seat_map_template DROP COLUMN IF EXISTS source_seat_map_id;
-- ALTER TABLE seating.seat_map_template DROP COLUMN IF EXISTS scope_path;
-- ALTER TABLE pricing.dynamic_price_rule DROP COLUMN IF EXISTS is_dynamic_pricing_enabled;
-- ALTER TABLE pricing.dynamic_price_rule DROP COLUMN IF EXISTS location_id;
-- ALTER TABLE pricing.dynamic_price_rule DROP COLUMN IF EXISTS location_level;
-- ALTER TABLE pricing.dynamic_price_rule DROP COLUMN IF EXISTS segment_ref;
-- ALTER TABLE pricing.dynamic_price_rule DROP COLUMN IF EXISTS customer_segment;
-- ALTER TABLE pricing.dynamic_price_rule DROP COLUMN IF EXISTS sales_channel;
-- ALTER TABLE pricing.dynamic_price_rule DROP COLUMN IF EXISTS dimension;
-- ALTER TABLE platform.workstation DROP COLUMN IF EXISTS channel;
-- ALTER TABLE platform.audit_record DROP COLUMN IF EXISTS reason;
-- ALTER TABLE marketing.message_dispatch DROP COLUMN IF EXISTS source_ref;
-- ALTER TABLE catalogue.dynamic_pricing_control DROP COLUMN IF EXISTS pending_approval_request_id;
-- ALTER TABLE catalogue.dynamic_pricing_control DROP COLUMN IF EXISTS pending_automation_level;
-- ALTER TABLE catalogue.demand_forecast DROP COLUMN IF EXISTS event_proximity_to_days;
-- ALTER TABLE catalogue.demand_forecast DROP COLUMN IF EXISTS event_proximity_from_days;
-- ALTER TABLE catalogue.demand_forecast DROP COLUMN IF EXISTS season;
-- ALTER TABLE catalogue.demand_forecast DROP COLUMN IF EXISTS peak_period;
-- ALTER TABLE catalogue.demand_forecast DROP COLUMN IF EXISTS day_type;
-- DROP TABLE IF EXISTS catalogue.competitor_price_observation;
-- ALTER TABLE catalogue.channel_envelope DROP COLUMN IF EXISTS returned_units;
-- ALTER TABLE catalogue.channel_envelope DROP COLUMN IF EXISTS released_units;
-- ALTER TABLE catalogue.channel_envelope DROP COLUMN IF EXISTS envelope_percent;
-- ALTER TABLE access.gate_mode_change DROP COLUMN IF EXISTS target_turnstile_mode;
-- ALTER TABLE access.device_placement DROP COLUMN IF EXISTS activation_zone;
-- ALTER TABLE access.biometric_profile DROP COLUMN IF EXISTS consent_form_id;
-- DELETE FROM platform.schema_version WHERE version = 'V0122';
