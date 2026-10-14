-- V0104 -- tenant database, after r1 (9cec72d) (20261014).
-- **Written by tools/derive-ddl.py in frozen mode. Do not edit after merge; a mistake is a new migration.**
--
-- The baseline under backend/tenant/ is frozen at r1 (9cec72d), so the change to the schema reference
-- since then is written here instead: additive only. Changes that are not additive (drops, renames,
-- type changes) are not generated; they are listed for a person in handoff/migration-review.md.
-- 3 table(s), 73 column(s), 42 index(es), 14 other statement(s), 27 row-level security polic(ies) re-applied.

ALTER TABLE ai.index_entry ADD COLUMN IF NOT EXISTS record_key text CONSTRAINT index_entry_record_key_chk CHECK (char_length(record_key) <= 200);

ALTER TABLE ai.index_entry ADD COLUMN IF NOT EXISTS subject_id uuid;

ALTER TABLE ai.index_entry ADD COLUMN IF NOT EXISTS content_hash text;

ALTER TABLE ai.index_entry ADD COLUMN IF NOT EXISTS chunk_count integer;

ALTER TABLE ai.index_entry ADD COLUMN IF NOT EXISTS embedding_model text CONSTRAINT index_entry_embedding_model_chk CHECK (char_length(embedding_model) <= 200);

ALTER TABLE ai.index_entry ADD COLUMN IF NOT EXISTS point_ids text[];

ALTER TABLE ai.index_entry ADD COLUMN IF NOT EXISTS indexed_at timestamptz;

ALTER TABLE ai.index_entry ADD COLUMN IF NOT EXISTS last_job_id uuid;

ALTER TABLE approvals.escalation ADD COLUMN IF NOT EXISTS escalated_at timestamptz;

ALTER TABLE approvals.escalation ADD COLUMN IF NOT EXISTS reason text;

ALTER TABLE approvals.escalation ADD COLUMN IF NOT EXISTS from_level integer;

ALTER TABLE approvals.escalation ADD COLUMN IF NOT EXISTS to_level integer;

ALTER TABLE approvals.escalation ADD COLUMN IF NOT EXISTS was_automatic boolean;

ALTER TABLE approvals.escalation ADD COLUMN IF NOT EXISTS escalated_by_principal_id uuid;

ALTER TABLE approvals.escalation ADD COLUMN IF NOT EXISTS added_approver_principal_id uuid;

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
    id                                uuid PRIMARY KEY NOT NULL,
    principal_credential_id           uuid NOT NULL,
    credential_hash                   text NOT NULL,
    replaced_at                       timestamptz NOT NULL
);

CREATE TABLE IF NOT EXISTS identity.subject_holding (
    id                                uuid PRIMARY KEY NOT NULL,
    subject_id                        uuid,
    holding_kind                      text NOT NULL CONSTRAINT subject_holding_holding_kind_chk CHECK (holding_kind IN ('order', 'entitlement')),
    holding_id                        uuid NOT NULL,
    order_id                          uuid,
    order_line_id                     uuid,
    status                            text NOT NULL CONSTRAINT subject_holding_status_chk CHECK (char_length(status) <= 40),
    valid_to                          timestamptz,
    last_event_at                     timestamptz,
    updated_at                        timestamptz NOT NULL
);

ALTER TABLE marketing.guest_device ADD COLUMN IF NOT EXISTS installation_id uuid;

CREATE TABLE IF NOT EXISTS platform.outlet_opening_hour (
    id                                uuid PRIMARY KEY NOT NULL,
    outlet_id                         uuid NOT NULL,
    day                               text NOT NULL,
    "from"                            text NOT NULL,
    "to"                              text NOT NULL,
    ends_next_day                     boolean
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

ALTER TABLE promotions.upsell_rule ADD COLUMN IF NOT EXISTS scope_path ltree;

ALTER TABLE ai.index_entry ADD CONSTRAINT index_entry_last_job_id_fkey FOREIGN KEY (last_job_id) REFERENCES ai.index_job(id);

ALTER TABLE identity.principal ADD CONSTRAINT principal_sso_provider_id_fkey FOREIGN KEY (sso_provider_id) REFERENCES identity.sso_provider(id);

ALTER TABLE identity.principal_credential_history ADD CONSTRAINT principal_credential_history_principal_credential_id_fkey FOREIGN KEY (principal_credential_id) REFERENCES identity.principal_credential(id);

ALTER TABLE identity.subject_holding ADD CONSTRAINT subject_holding_subject_id_fkey FOREIGN KEY (subject_id) REFERENCES pii.subject(id);

ALTER TABLE platform.outlet_opening_hour ADD CONSTRAINT outlet_opening_hour_outlet_id_fkey FOREIGN KEY (outlet_id) REFERENCES platform.outlet(id);

CREATE INDEX IF NOT EXISTS index_entry_last_job_id_idx ON ai.index_entry (last_job_id);

CREATE INDEX IF NOT EXISTS principal_sso_provider_id_idx ON identity.principal (sso_provider_id);

CREATE INDEX IF NOT EXISTS principal_credential_history_principal_credential_id_idx ON identity.principal_credential_history (principal_credential_id);

CREATE INDEX IF NOT EXISTS subject_holding_subject_id_idx ON identity.subject_holding (subject_id);

CREATE INDEX IF NOT EXISTS outlet_opening_hour_outlet_id_idx ON platform.outlet_opening_hour (outlet_id);

CREATE INDEX IF NOT EXISTS entry_priority_tier_id_idx ON queue.entry (priority_tier_id);

DROP INDEX IF EXISTS approvals.external_provider_code_uniq;

CREATE UNIQUE INDEX IF NOT EXISTS external_provider_code_uniq ON approvals.external_provider (lower(code));

DROP INDEX IF EXISTS assets.media_collection_name_uniq;

CREATE UNIQUE INDEX IF NOT EXISTS media_collection_name_uniq ON assets.media_collection (lower(name));

DROP INDEX IF EXISTS catalogue.event_code_uniq;

CREATE UNIQUE INDEX IF NOT EXISTS event_code_uniq ON catalogue.event (lower(code));

DROP INDEX IF EXISTS catalogue.product_code_uniq;

CREATE UNIQUE INDEX IF NOT EXISTS product_code_uniq ON catalogue.product (lower(code));

DROP INDEX IF EXISTS catalogue.product_category_code_uniq;

CREATE UNIQUE INDEX IF NOT EXISTS product_category_code_uniq ON catalogue.product_category (lower(code)) WHERE code IS NOT NULL;

DROP INDEX IF EXISTS identity.role_code_uniq;

CREATE UNIQUE INDEX IF NOT EXISTS role_code_uniq ON identity.role (lower(code));

DROP INDEX IF EXISTS inventory.supplier_code_uniq;

CREATE UNIQUE INDEX IF NOT EXISTS supplier_code_uniq ON inventory.supplier (lower(code));

DROP INDEX IF EXISTS ledger.account_code_uniq;

CREATE UNIQUE INDEX IF NOT EXISTS account_code_uniq ON ledger.account (lower(code));

DROP INDEX IF EXISTS ledger.credit_memo_credit_memo_number_uniq;

CREATE UNIQUE INDEX IF NOT EXISTS credit_memo_credit_memo_number_uniq ON ledger.credit_memo (lower(credit_memo_number));

DROP INDEX IF EXISTS ledger.journal_entry_entry_number_uniq;

CREATE UNIQUE INDEX IF NOT EXISTS journal_entry_entry_number_uniq ON ledger.journal_entry (lower(entry_number));

DROP INDEX IF EXISTS ledger.tax_code_code_uniq;

CREATE UNIQUE INDEX IF NOT EXISTS tax_code_code_uniq ON ledger.tax_code (lower(code));

DROP INDEX IF EXISTS ledger.tax_invoice_invoice_number_uniq;

CREATE UNIQUE INDEX IF NOT EXISTS tax_invoice_invoice_number_uniq ON ledger.tax_invoice (lower(invoice_number));

DROP INDEX IF EXISTS marketing.loyalty_programme_code_uniq;

CREATE UNIQUE INDEX IF NOT EXISTS loyalty_programme_code_uniq ON marketing.loyalty_programme (lower(code));

DROP INDEX IF EXISTS orders.sales_order_order_number_uniq;

CREATE UNIQUE INDEX IF NOT EXISTS sales_order_order_number_uniq ON orders.sales_order (lower(order_number)) WHERE order_number IS NOT NULL;

DROP INDEX IF EXISTS promotions.promotion_code_uniq;

CREATE UNIQUE INDEX IF NOT EXISTS promotion_code_uniq ON promotions.promotion (lower(code));

DROP INDEX IF EXISTS tenancy.data_retention_setting_data_class_uniq;

CREATE UNIQUE INDEX IF NOT EXISTS data_retention_setting_data_class_uniq ON tenancy.data_retention_setting (lower(data_class));

DROP INDEX IF EXISTS catalogue.product_venue_id_family_key_uniq;

CREATE UNIQUE INDEX IF NOT EXISTS product_venue_id_family_key_uniq ON catalogue.product (venue_id, lower(family_key)) WHERE family_key IS NOT NULL;

DROP INDEX IF EXISTS fnb.outlet_template_scope_path_code_uniq;

CREATE UNIQUE INDEX IF NOT EXISTS outlet_template_scope_path_code_uniq ON fnb.outlet_template (scope_path, lower(code));

DROP INDEX IF EXISTS maintenance.asset_venue_id_asset_tag_uniq;

CREATE UNIQUE INDEX IF NOT EXISTS asset_venue_id_asset_tag_uniq ON maintenance.asset (venue_id, lower(asset_tag));

CREATE UNIQUE INDEX IF NOT EXISTS outlet_venue_id_code_uniq ON platform.outlet (venue_id, lower(code));

CREATE UNIQUE INDEX IF NOT EXISTS sale_board_venue_id_code_uniq ON platform.sale_board (venue_id, lower(code));

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

CREATE INDEX IF NOT EXISTS region_settings_scope_path_idx ON platform.region_settings USING gist (scope_path);

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

SELECT platform.drop_rls_policies('inventory.supplier'::regclass);

SELECT platform.apply_read_beneath_rls('inventory.supplier'::regclass);

SELECT platform.drop_rls_policies('platform.region_settings'::regclass);

SELECT platform.apply_read_beneath_rls('platform.region_settings'::regclass);

SELECT platform.drop_rls_policies('promotions.upsell_rule'::regclass);

SELECT platform.apply_read_beneath_rls('promotions.upsell_rule'::regclass);

SELECT platform.drop_rls_policies('catalogue.product_media'::regclass);

SELECT platform.apply_parent_rls('catalogue.product_media'::regclass, 'product_id', 'catalogue.product'::regclass, 'id');

SELECT platform.drop_rls_policies('inventory.quotation_line'::regclass);

SELECT platform.apply_parent_rls('inventory.quotation_line'::regclass, 'quotation_id', 'inventory.quotation'::regclass, 'id');

SELECT platform.drop_rls_policies('marketing.consent_question_version'::regclass);

SELECT platform.apply_parent_rls('marketing.consent_question_version'::regclass, 'question_id', 'marketing.consent_question'::regclass, 'id');

SELECT platform.drop_rls_policies('reporting.dashboard_tile'::regclass);

SELECT platform.apply_parent_rls('reporting.dashboard_tile'::regclass, 'dashboard_id', 'reporting.dashboard'::regclass, 'id');

SELECT platform.drop_rls_policies('retail.sale'::regclass);

SELECT platform.apply_parent_rls('retail.sale'::regclass, 'outlet_id', 'platform.outlet'::regclass, 'id');

SELECT platform.drop_rls_policies('seating.seat_block_item'::regclass);

SELECT platform.apply_parent_rls('seating.seat_block_item'::regclass, 'block_id', 'seating.seat_block'::regclass, 'id');

SELECT platform.drop_rls_policies('venuemap.map_version'::regclass);

SELECT platform.apply_parent_rls('venuemap.map_version'::regclass, 'map_id', 'venuemap.map'::regclass, 'id');

SELECT platform.drop_rls_policies('venuemap.placed_resource'::regclass);

SELECT platform.apply_parent_rls('venuemap.placed_resource'::regclass, 'map_id', 'venuemap.map'::regclass, 'id');

SELECT platform.drop_rls_policies('workforce.attendance_amendment'::regclass);

SELECT platform.apply_parent_rls('workforce.attendance_amendment'::regclass, 'attendance_record_id', 'workforce.attendance'::regclass, 'id');

SELECT platform.drop_rls_policies('orders.group_participant_list'::regclass);

SELECT platform.apply_parent_rls('orders.group_participant_list'::regclass, 'group_booking_id', 'orders.group_booking'::regclass, 'id');

SELECT platform.drop_rls_policies('platform.sale_board_tile'::regclass);

SELECT platform.apply_parent_rls('platform.sale_board_tile'::regclass, 'sale_board_page_id', 'platform.sale_board_page'::regclass, 'id');

SELECT platform.drop_rls_policies('retail.exchange'::regclass);

SELECT platform.apply_parent_rls('retail.exchange'::regclass, 'new_sale_id', 'retail.sale'::regclass, 'id');

SELECT platform.drop_rls_policies('retail."return"'::regclass);

SELECT platform.apply_parent_rls('retail."return"'::regclass, 'sale_id', 'retail.sale'::regclass, 'id');

SELECT platform.drop_rls_policies('retail.sale_line'::regclass);

SELECT platform.apply_parent_rls('retail.sale_line'::regclass, 'sale_id', 'retail.sale'::regclass, 'id');

SELECT platform.drop_rls_policies('orders.group_participant'::regclass);

SELECT platform.apply_parent_rls('orders.group_participant'::regclass, 'group_participant_list_id', 'orders.group_participant_list'::regclass, 'id');

SELECT platform.drop_rls_policies('retail.return_line'::regclass);

SELECT platform.apply_parent_rls('retail.return_line'::regclass, 'return_id', 'retail."return"'::regclass, 'id');

SELECT platform.drop_rls_policies('identity.role_permission'::regclass);

SELECT platform.apply_parent_split_rls('identity.role_permission'::regclass, 'role_id', 'identity.role'::regclass, 'id', 'platform.tenant_root_in_scope()');

SELECT platform.apply_subject_rls('identity.subject_holding'::regclass);

SELECT platform.apply_tenant_rls('identity.principal_credential_history'::regclass);

SELECT platform.drop_rls_policies('identity.authz_audit'::regclass);

SELECT platform.apply_append_audit_rls('identity.authz_audit'::regclass);

SELECT platform.drop_rls_policies('platform.audit_record'::regclass);

SELECT platform.apply_append_audit_rls('platform.audit_record'::regclass);

INSERT INTO platform.schema_version (version, description, checksum)
VALUES ('V0104', 'after r1 (9cec72d): 3 table(s), 73 column(s), 42 index(es), 14 other statement(s), 27 row-level security polic(ies) re-applied', '7ccc922147885ef7ffcad93485c4d8b4f1b29e48333193f87c9bbcfd6c345651')
ON CONFLICT (version) DO NOTHING;

-- ============================================================================
-- ROLLBACK
-- ============================================================================
-- Commented out so that applying this file never runs it: the rollback is run by removing the
-- leading `-- `, and is tested in CI against a restored snapshot (backend/MIGRATIONS.md).
-- SELECT platform.drop_rls_policies('platform.audit_record'::regclass); SELECT platform.apply_tenant_rls('platform.audit_record'::regclass);
-- SELECT platform.drop_rls_policies('identity.authz_audit'::regclass); SELECT platform.apply_tenant_rls('identity.authz_audit'::regclass);
-- SELECT platform.drop_rls_policies('identity.role_permission'::regclass); SELECT platform.apply_tenant_rls('identity.role_permission'::regclass);
-- SELECT platform.drop_rls_policies('retail.return_line'::regclass); SELECT platform.apply_tenant_rls('retail.return_line'::regclass);
-- SELECT platform.drop_rls_policies('orders.group_participant'::regclass); SELECT platform.apply_tenant_rls('orders.group_participant'::regclass);
-- SELECT platform.drop_rls_policies('retail.sale_line'::regclass); SELECT platform.apply_tenant_rls('retail.sale_line'::regclass);
-- SELECT platform.drop_rls_policies('retail."return"'::regclass); SELECT platform.apply_tenant_rls('retail."return"'::regclass);
-- SELECT platform.drop_rls_policies('retail.exchange'::regclass); SELECT platform.apply_tenant_rls('retail.exchange'::regclass);
-- SELECT platform.drop_rls_policies('platform.sale_board_tile'::regclass); SELECT platform.apply_tenant_rls('platform.sale_board_tile'::regclass);
-- SELECT platform.drop_rls_policies('orders.group_participant_list'::regclass); SELECT platform.apply_tenant_rls('orders.group_participant_list'::regclass);
-- SELECT platform.drop_rls_policies('workforce.attendance_amendment'::regclass); SELECT platform.apply_tenant_rls('workforce.attendance_amendment'::regclass);
-- SELECT platform.drop_rls_policies('venuemap.placed_resource'::regclass); SELECT platform.apply_parent_rls('venuemap.placed_resource'::regclass, 'resource_id', 'resources.resource'::regclass, 'id');
-- SELECT platform.drop_rls_policies('venuemap.map_version'::regclass); SELECT platform.apply_tenant_rls('venuemap.map_version'::regclass);
-- SELECT platform.drop_rls_policies('seating.seat_block_item'::regclass); SELECT platform.apply_tenant_rls('seating.seat_block_item'::regclass);
-- SELECT platform.drop_rls_policies('retail.sale'::regclass); SELECT platform.apply_subject_rls('retail.sale'::regclass);
-- SELECT platform.drop_rls_policies('reporting.dashboard_tile'::regclass); SELECT platform.apply_tenant_rls('reporting.dashboard_tile'::regclass);
-- SELECT platform.drop_rls_policies('marketing.consent_question_version'::regclass); SELECT platform.apply_tenant_rls('marketing.consent_question_version'::regclass);
-- SELECT platform.drop_rls_policies('inventory.quotation_line'::regclass); SELECT platform.apply_tenant_rls('inventory.quotation_line'::regclass);
-- SELECT platform.drop_rls_policies('catalogue.product_media'::regclass); SELECT platform.apply_tenant_rls('catalogue.product_media'::regclass);
-- SELECT platform.drop_rls_policies('promotions.upsell_rule'::regclass); SELECT platform.apply_tenant_rls('promotions.upsell_rule'::regclass);
-- SELECT platform.drop_rls_policies('platform.region_settings'::regclass); SELECT platform.apply_tenant_rls('platform.region_settings'::regclass);
-- SELECT platform.drop_rls_policies('inventory.supplier'::regclass); SELECT platform.apply_scope_rls('inventory.supplier'::regclass);
-- SELECT platform.drop_rls_policies('identity.segregation_rule'::regclass); SELECT platform.apply_scope_rls('identity.segregation_rule'::regclass);
-- SELECT platform.drop_rls_policies('identity.role'::regclass); SELECT platform.apply_tenant_rls('identity.role'::regclass);
-- SELECT platform.drop_rls_policies('identity.principal'::regclass); SELECT platform.apply_tenant_rls('identity.principal'::regclass);
-- SELECT platform.drop_rls_policies('identity.password_policy'::regclass); SELECT platform.apply_scope_rls('identity.password_policy'::regclass);
-- SELECT platform.drop_rls_policies('identity.capability_template'::regclass); SELECT platform.apply_scope_rls('identity.capability_template'::regclass);
-- DROP INDEX IF EXISTS promotions.upsell_rule_scope_path_idx;
-- DROP INDEX IF EXISTS platform.region_settings_scope_path_idx;
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
-- DROP INDEX IF EXISTS platform.sale_board_venue_id_code_uniq;
-- DROP INDEX IF EXISTS platform.outlet_venue_id_code_uniq;
-- DROP INDEX IF EXISTS maintenance.asset_venue_id_asset_tag_uniq; CREATE UNIQUE INDEX IF NOT EXISTS asset_venue_id_asset_tag_uniq ON maintenance.asset (venue_id, asset_tag);
-- DROP INDEX IF EXISTS fnb.outlet_template_scope_path_code_uniq; CREATE UNIQUE INDEX IF NOT EXISTS outlet_template_scope_path_code_uniq ON fnb.outlet_template (scope_path, code);
-- DROP INDEX IF EXISTS catalogue.product_venue_id_family_key_uniq; CREATE UNIQUE INDEX IF NOT EXISTS product_venue_id_family_key_uniq ON catalogue.product (venue_id, family_key) WHERE family_key IS NOT NULL;
-- DROP INDEX IF EXISTS tenancy.data_retention_setting_data_class_uniq; CREATE UNIQUE INDEX IF NOT EXISTS data_retention_setting_data_class_uniq ON tenancy.data_retention_setting (data_class);
-- DROP INDEX IF EXISTS promotions.promotion_code_uniq; CREATE UNIQUE INDEX IF NOT EXISTS promotion_code_uniq ON promotions.promotion (code);
-- DROP INDEX IF EXISTS orders.sales_order_order_number_uniq; CREATE UNIQUE INDEX IF NOT EXISTS sales_order_order_number_uniq ON orders.sales_order (order_number) WHERE order_number IS NOT NULL;
-- DROP INDEX IF EXISTS marketing.loyalty_programme_code_uniq; CREATE UNIQUE INDEX IF NOT EXISTS loyalty_programme_code_uniq ON marketing.loyalty_programme (code);
-- DROP INDEX IF EXISTS ledger.tax_invoice_invoice_number_uniq; CREATE UNIQUE INDEX IF NOT EXISTS tax_invoice_invoice_number_uniq ON ledger.tax_invoice (invoice_number);
-- DROP INDEX IF EXISTS ledger.tax_code_code_uniq; CREATE UNIQUE INDEX IF NOT EXISTS tax_code_code_uniq ON ledger.tax_code (code);
-- DROP INDEX IF EXISTS ledger.journal_entry_entry_number_uniq; CREATE UNIQUE INDEX IF NOT EXISTS journal_entry_entry_number_uniq ON ledger.journal_entry (entry_number);
-- DROP INDEX IF EXISTS ledger.credit_memo_credit_memo_number_uniq; CREATE UNIQUE INDEX IF NOT EXISTS credit_memo_credit_memo_number_uniq ON ledger.credit_memo (credit_memo_number);
-- DROP INDEX IF EXISTS ledger.account_code_uniq; CREATE UNIQUE INDEX IF NOT EXISTS account_code_uniq ON ledger.account (code);
-- DROP INDEX IF EXISTS inventory.supplier_code_uniq; CREATE UNIQUE INDEX IF NOT EXISTS supplier_code_uniq ON inventory.supplier (code);
-- DROP INDEX IF EXISTS identity.role_code_uniq; CREATE UNIQUE INDEX IF NOT EXISTS role_code_uniq ON identity.role (code);
-- DROP INDEX IF EXISTS catalogue.product_category_code_uniq; CREATE UNIQUE INDEX IF NOT EXISTS product_category_code_uniq ON catalogue.product_category (code) WHERE code IS NOT NULL;
-- DROP INDEX IF EXISTS catalogue.product_code_uniq; CREATE UNIQUE INDEX IF NOT EXISTS product_code_uniq ON catalogue.product (code);
-- DROP INDEX IF EXISTS catalogue.event_code_uniq; CREATE UNIQUE INDEX IF NOT EXISTS event_code_uniq ON catalogue.event (code);
-- DROP INDEX IF EXISTS assets.media_collection_name_uniq; CREATE UNIQUE INDEX IF NOT EXISTS media_collection_name_uniq ON assets.media_collection (name);
-- DROP INDEX IF EXISTS approvals.external_provider_code_uniq; CREATE UNIQUE INDEX IF NOT EXISTS external_provider_code_uniq ON approvals.external_provider (code);
-- DROP INDEX IF EXISTS queue.entry_priority_tier_id_idx;
-- DROP INDEX IF EXISTS platform.outlet_opening_hour_outlet_id_idx;
-- DROP INDEX IF EXISTS identity.subject_holding_subject_id_idx;
-- DROP INDEX IF EXISTS identity.principal_credential_history_principal_credential_id_idx;
-- DROP INDEX IF EXISTS identity.principal_sso_provider_id_idx;
-- DROP INDEX IF EXISTS ai.index_entry_last_job_id_idx;
-- ALTER TABLE identity.principal DROP CONSTRAINT IF EXISTS principal_sso_provider_id_fkey;
-- ALTER TABLE ai.index_entry DROP CONSTRAINT IF EXISTS index_entry_last_job_id_fkey;
-- ALTER TABLE promotions.upsell_rule DROP COLUMN IF EXISTS scope_path;
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
-- ALTER TABLE marketing.guest_device DROP COLUMN IF EXISTS installation_id;
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
-- ALTER TABLE approvals.escalation DROP COLUMN IF EXISTS added_approver_principal_id;
-- ALTER TABLE approvals.escalation DROP COLUMN IF EXISTS escalated_by_principal_id;
-- ALTER TABLE approvals.escalation DROP COLUMN IF EXISTS was_automatic;
-- ALTER TABLE approvals.escalation DROP COLUMN IF EXISTS to_level;
-- ALTER TABLE approvals.escalation DROP COLUMN IF EXISTS from_level;
-- ALTER TABLE approvals.escalation DROP COLUMN IF EXISTS reason;
-- ALTER TABLE approvals.escalation DROP COLUMN IF EXISTS escalated_at;
-- ALTER TABLE ai.index_entry DROP COLUMN IF EXISTS last_job_id;
-- ALTER TABLE ai.index_entry DROP COLUMN IF EXISTS indexed_at;
-- ALTER TABLE ai.index_entry DROP COLUMN IF EXISTS point_ids;
-- ALTER TABLE ai.index_entry DROP COLUMN IF EXISTS embedding_model;
-- ALTER TABLE ai.index_entry DROP COLUMN IF EXISTS chunk_count;
-- ALTER TABLE ai.index_entry DROP COLUMN IF EXISTS content_hash;
-- ALTER TABLE ai.index_entry DROP COLUMN IF EXISTS subject_id;
-- ALTER TABLE ai.index_entry DROP COLUMN IF EXISTS record_key;
-- DELETE FROM platform.schema_version WHERE version = 'V0104';
