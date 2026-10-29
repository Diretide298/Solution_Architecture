-- V0118 -- tenant database, after r1 (9cec72d) (20261029).
-- **Written by tools/derive-ddl.py in frozen mode. Do not edit after merge; a mistake is a new migration.**
--
-- The baseline under backend/tenant/ is frozen at r1 (9cec72d), so the change to the schema reference
-- since then is written here instead: additive only. Changes that are not additive (drops, renames,
-- type changes) are not generated; they are listed for a person in handoff/migration-review.md.
-- Every statement that needs a table is a guarded block (CHG-R9MIG-002): it does nothing where its table
-- or a column it names is not there yet, so the file applies as one transaction, twice, on any database;
-- the migration that creates such a table later copies the block. A table's policy change is one block.
-- 1 table(s), 1 column(s), 7 index(es), 13 other statement(s), 10 row-level security polic(ies) re-applied.

CREATE TABLE IF NOT EXISTS identity.subject_data_export_part (
    id                                uuid PRIMARY KEY NOT NULL,
    export_id                         uuid NOT NULL,
    owner                             text NOT NULL CONSTRAINT subject_data_export_part_owner_chk CHECK (char_length(owner) <= 40),
    file_ref                          text NOT NULL CONSTRAINT subject_data_export_part_file_ref_chk CHECK (char_length(file_ref) <= 500),
    tables                            text[],
    row_count                         integer NOT NULL,
    written_at                        timestamptz NOT NULL
);

DO $$ BEGIN IF to_regclass('platform.outlet') IS NOT NULL THEN
ALTER TABLE platform.outlet ADD COLUMN IF NOT EXISTS order_number_prefix text CONSTRAINT outlet_order_number_prefix_chk CHECK (order_number_prefix IN ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z') AND char_length(order_number_prefix) <= 1);
END IF; END $$;

DO $$ BEGIN IF to_regclass('identity.subject_data_export_part') IS NOT NULL AND to_regclass('identity.subject_data_export') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'identity' AND table_name = 'subject_data_export_part' AND column_name = 'export_id') AND NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'subject_data_export_part_export_id_fkey' AND conrelid = to_regclass('identity.subject_data_export_part')) THEN
ALTER TABLE identity.subject_data_export_part ADD CONSTRAINT subject_data_export_part_export_id_fkey FOREIGN KEY (export_id) REFERENCES identity.subject_data_export(id);
END IF; END $$;

DO $$ BEGIN IF to_regclass('ai.proposed_action') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'ai' AND table_name = 'proposed_action' AND column_name = 'map_id') THEN
CREATE INDEX IF NOT EXISTS proposed_action_map_id_idx ON ai.proposed_action (map_id);
END IF; END $$;

DO $$ BEGIN IF to_regclass('marketing.privacy_request') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'marketing' AND table_name = 'privacy_request' AND column_name = 'approval_request_id') THEN
CREATE INDEX IF NOT EXISTS privacy_request_approval_request_id_idx ON marketing.privacy_request (approval_request_id);
END IF; END $$;

DO $$ BEGIN IF to_regclass('identity.subject_data_export_part') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'identity' AND table_name = 'subject_data_export_part' AND column_name = 'export_id') THEN
CREATE INDEX IF NOT EXISTS subject_data_export_part_export_id_idx ON identity.subject_data_export_part (export_id);
END IF; END $$;

DO $$ BEGIN IF to_regclass('marketing.guest_preference') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'marketing' AND table_name = 'guest_preference' AND column_name = 'subject_id') THEN
CREATE UNIQUE INDEX IF NOT EXISTS guest_preference_subject_id_uniq ON marketing.guest_preference (subject_id) WHERE subject_id IS NOT NULL;
END IF; END $$;

DO $$ BEGIN IF to_regclass('marketing.guest_profile') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'marketing' AND table_name = 'guest_profile' AND column_name = 'subject_id') THEN
CREATE UNIQUE INDEX IF NOT EXISTS guest_profile_subject_id_uniq ON marketing.guest_profile (subject_id);
END IF; END $$;

DO $$ BEGIN IF to_regclass('identity.subject_data_export_part') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'identity' AND table_name = 'subject_data_export_part' AND column_name = 'export_id') AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'identity' AND table_name = 'subject_data_export_part' AND column_name = 'owner') THEN
CREATE UNIQUE INDEX IF NOT EXISTS subject_data_export_part_export_id_owner_uniq ON identity.subject_data_export_part (export_id, lower(owner));
END IF; END $$;

DO $$ BEGIN IF to_regclass('tenancy.device_firmware') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'tenancy' AND table_name = 'device_firmware' AND column_name = 'device_kind') AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'tenancy' AND table_name = 'device_firmware' AND column_name = 'version') THEN
CREATE UNIQUE INDEX IF NOT EXISTS device_firmware_device_kind_version_uniq ON tenancy.device_firmware (lower(device_kind), lower(version));
END IF; END $$;

CREATE OR REPLACE FUNCTION platform.apply_grant_holder_subject_rls(target regclass)
    RETURNS void
    LANGUAGE plpgsql
AS $$
BEGIN
    PERFORM platform.apply_split_rls(target,
        'platform.grant_holder() OR platform.subject_in_scope(subject_id)',
        'platform.grant_holder() OR platform.subject_in_scope(subject_id)');
END
$$;

DO $$ BEGIN IF to_regclass('marketing.consent_record') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'marketing' AND table_name = 'consent_record' AND column_name = 'subject_id') THEN
PERFORM platform.drop_rls_policies('marketing.consent_record'::regclass);
PERFORM platform.apply_grant_holder_subject_rls('marketing.consent_record'::regclass);
END IF; END $$;

DO $$ BEGIN IF to_regclass('orders.cart') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'orders' AND table_name = 'cart' AND column_name = 'subject_id') AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'orders' AND table_name = 'cart' AND column_name = 'venue_id') THEN
PERFORM platform.drop_rls_policies('orders.cart'::regclass);
PERFORM platform.apply_split_rls('orders.cart'::regclass, '(NULLIF(current_setting(''ticvai.subject_id'', true), '''') IS NULL AND platform.venue_in_scope(venue_id)) OR (subject_id = (SELECT NULLIF(current_setting(''ticvai.subject_id'', true), '''')::uuid))', '(NULLIF(current_setting(''ticvai.subject_id'', true), '''') IS NULL AND platform.venue_in_scope(venue_id)) OR (subject_id = (SELECT NULLIF(current_setting(''ticvai.subject_id'', true), '''')::uuid))');
END IF; END $$;

DO $$ BEGIN IF to_regclass('orders.order_event') IS NOT NULL AND to_regclass('orders.sales_order') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'orders' AND table_name = 'order_event' AND column_name = 'scope_path') THEN
PERFORM platform.drop_rls_policies('orders.order_event'::regclass);
PERFORM platform.apply_split_rls('orders.order_event'::regclass, '(NULLIF(current_setting(''ticvai.subject_id'', true), '''') IS NULL AND scope_path IS NOT NULL AND scope_path <@ ANY ((SELECT platform.current_scope_paths())::ltree[])) OR (EXISTS (SELECT 1 FROM orders.sales_order gp WHERE gp.id = orders.order_event.order_id AND gp.subject_id = (SELECT NULLIF(current_setting(''ticvai.subject_id'', true), '''')::uuid)))', 'scope_path IS NOT NULL AND scope_path <@ ANY ((SELECT platform.current_scope_paths())::ltree[])');
END IF; END $$;

DO $$ BEGIN IF to_regclass('orders.order_line') IS NOT NULL AND to_regclass('orders.sales_order') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'orders' AND table_name = 'order_line' AND column_name = 'venue_id') THEN
PERFORM platform.drop_rls_policies('orders.order_line'::regclass);
PERFORM platform.apply_split_rls('orders.order_line'::regclass, '(NULLIF(current_setting(''ticvai.subject_id'', true), '''') IS NULL AND platform.venue_in_scope(venue_id)) OR (EXISTS (SELECT 1 FROM orders.sales_order gp WHERE gp.id = orders.order_line.sales_order_id AND gp.subject_id = (SELECT NULLIF(current_setting(''ticvai.subject_id'', true), '''')::uuid)))', 'platform.venue_in_scope(venue_id)');
END IF; END $$;

DO $$ BEGIN IF to_regclass('orders.sales_order') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'orders' AND table_name = 'sales_order' AND column_name = 'scope_path') AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'orders' AND table_name = 'sales_order' AND column_name = 'subject_id') THEN
PERFORM platform.drop_rls_policies('orders.sales_order'::regclass);
PERFORM platform.apply_split_rls('orders.sales_order'::regclass, '(NULLIF(current_setting(''ticvai.subject_id'', true), '''') IS NULL AND scope_path IS NOT NULL AND scope_path <@ ANY ((SELECT platform.current_scope_paths())::ltree[])) OR (subject_id = (SELECT NULLIF(current_setting(''ticvai.subject_id'', true), '''')::uuid))', 'scope_path IS NOT NULL AND scope_path <@ ANY ((SELECT platform.current_scope_paths())::ltree[])');
END IF; END $$;

DO $$ BEGIN IF to_regclass('payments.token') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'payments' AND table_name = 'token' AND column_name = 'subject_id') THEN
PERFORM platform.drop_rls_policies('payments.token'::regclass);
PERFORM platform.apply_grant_holder_subject_rls('payments.token'::regclass);
END IF; END $$;

DO $$ BEGIN IF to_regclass('wallet.balance') IS NOT NULL THEN
PERFORM platform.drop_rls_policies('wallet.balance'::regclass);
PERFORM platform.apply_grant_holder_read_rls('wallet.balance'::regclass, 'platform.grant_holder()');
END IF; END $$;

DO $$ BEGIN IF to_regclass('wallet.wallet') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'wallet' AND table_name = 'wallet' AND column_name = 'subject_id') THEN
PERFORM platform.drop_rls_policies('wallet.wallet'::regclass);
PERFORM platform.apply_grant_holder_subject_rls('wallet.wallet'::regclass);
END IF; END $$;

DO $$ BEGIN IF to_regclass('marketing.guest_profile') IS NOT NULL AND to_regclass('marketing.segment') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'marketing' AND table_name = 'guest_profile' AND column_name = 'subject_id') THEN
PERFORM platform.drop_rls_policies('marketing.guest_profile'::regclass);
PERFORM platform.apply_split_rls('marketing.guest_profile'::regclass, '(NULLIF(current_setting(''ticvai.subject_id'', true), '''') IS NULL AND EXISTS (SELECT 1 FROM marketing.segment pr WHERE pr.id = marketing.guest_profile.segment_id)) OR platform.subject_in_scope(subject_id)', '(NULLIF(current_setting(''ticvai.subject_id'', true), '''') IS NULL AND EXISTS (SELECT 1 FROM marketing.segment pr WHERE pr.id = marketing.guest_profile.segment_id)) OR platform.subject_in_scope(subject_id)');
END IF; END $$;

DO $$ BEGIN IF to_regclass('orders.cart_line') IS NOT NULL AND to_regclass('orders.cart') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'orders' AND table_name = 'cart' AND column_name = 'id') AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'orders' AND table_name = 'cart_line' AND column_name = 'cart_id') THEN
PERFORM platform.drop_rls_policies('orders.cart_line'::regclass);
PERFORM platform.apply_parent_split_rls('orders.cart_line'::regclass, 'cart_id', 'orders.cart'::regclass, 'id', '((NULLIF(current_setting(''ticvai.subject_id'', true), '''') IS NULL AND platform.venue_in_scope(parent_row.venue_id)) OR (parent_row.subject_id = (SELECT NULLIF(current_setting(''ticvai.subject_id'', true), '''')::uuid)))');
END IF; END $$;

DO $$ BEGIN IF to_regclass('identity.subject_data_export_part') IS NOT NULL THEN
PERFORM platform.apply_tenant_rls('identity.subject_data_export_part'::regclass);
END IF; END $$;

DO $$ BEGIN IF EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'operations') AND EXISTS (SELECT 1 FROM pg_namespace WHERE nspname = 'catalogue') THEN GRANT USAGE ON SCHEMA catalogue TO operations; END IF; END $$;

DO $$ BEGIN IF EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'operations') AND to_regclass('catalogue.variant') IS NOT NULL THEN GRANT SELECT ON catalogue.variant TO operations; END IF; END $$;

DO $$ BEGIN IF EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'operations') AND to_regclass('catalogue.product') IS NOT NULL THEN GRANT SELECT ON catalogue.product TO operations; END IF; END $$;

DO $$ BEGIN IF EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'operations') AND to_regclass('catalogue.product_media') IS NOT NULL THEN GRANT SELECT ON catalogue.product_media TO operations; END IF; END $$;

DO $$ BEGIN IF EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'operations') AND to_regclass('catalogue.price') IS NOT NULL THEN GRANT SELECT ON catalogue.price TO operations; END IF; END $$;

DO $$ BEGIN IF EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'operations') AND to_regclass('catalogue.price_assignment') IS NOT NULL THEN GRANT SELECT ON catalogue.price_assignment TO operations; END IF; END $$;

DO $$ BEGIN IF EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'operations') AND to_regclass('catalogue.price_list') IS NOT NULL THEN GRANT SELECT ON catalogue.price_list TO operations; END IF; END $$;

DO $$ BEGIN IF EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'operations') AND to_regclass('catalogue.performance') IS NOT NULL THEN GRANT SELECT ON catalogue.performance TO operations; END IF; END $$;

DO $$ BEGIN IF EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'operations') AND to_regclass('catalogue.product_category') IS NOT NULL THEN GRANT SELECT ON catalogue.product_category TO operations; END IF; END $$;

DO $$ BEGIN IF EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'operations') AND to_regclass('platform.workstation') IS NOT NULL THEN GRANT SELECT ON platform.workstation TO operations; END IF; END $$;

INSERT INTO platform.schema_version (version, description, checksum)
VALUES ('V0118', 'after r1 (9cec72d): 1 table(s), 1 column(s), 7 index(es), 13 other statement(s), 10 row-level security polic(ies) re-applied', '4cf0f7842c51db502d4275a510337f669e8b86ddc442fbbbe8a0bc91501b621e')
ON CONFLICT (version) DO NOTHING;

-- ============================================================================
-- ROLLBACK
-- ============================================================================
-- Commented out so that applying this file never runs it: the rollback is run by removing the
-- leading `-- `, and is tested in CI against a restored snapshot (backend/MIGRATIONS.md).
-- REVOKE SELECT ON platform.workstation FROM operations;
-- REVOKE SELECT ON catalogue.product_category FROM operations;
-- REVOKE SELECT ON catalogue.performance FROM operations;
-- REVOKE SELECT ON catalogue.price_list FROM operations;
-- REVOKE SELECT ON catalogue.price_assignment FROM operations;
-- REVOKE SELECT ON catalogue.price FROM operations;
-- REVOKE SELECT ON catalogue.product_media FROM operations;
-- REVOKE SELECT ON catalogue.product FROM operations;
-- REVOKE SELECT ON catalogue.variant FROM operations;
-- REVOKE USAGE ON SCHEMA catalogue FROM operations;
-- SELECT platform.drop_rls_policies('orders.cart_line'::regclass); SELECT platform.apply_parent_rls('orders.cart_line'::regclass, 'cart_id', 'orders.cart'::regclass, 'id'); SELECT platform.apply_parent_split_rls('orders.cart_line'::regclass, 'cart_id', 'orders.cart'::regclass, 'id', '((platform.venue_in_scope(parent_row.venue_id)) OR (parent_row.subject_id = (SELECT NULLIF(current_setting(''ticvai.subject_id'', true), '''')::uuid)))');
-- SELECT platform.drop_rls_policies('marketing.guest_profile'::regclass); SELECT platform.apply_parent_rls('marketing.guest_profile'::regclass, 'segment_id', 'marketing.segment'::regclass, 'id');
-- SELECT platform.drop_rls_policies('wallet.wallet'::regclass); SELECT platform.apply_subject_rls('wallet.wallet'::regclass); SELECT platform.apply_grant_holder_subject_read_rls('wallet.wallet'::regclass);
-- SELECT platform.drop_rls_policies('wallet.balance'::regclass); SELECT platform.apply_tenant_rls('wallet.balance'::regclass); SELECT platform.apply_grant_holder_read_rls('wallet.balance'::regclass, 'platform.tenant_root_in_scope()');
-- SELECT platform.drop_rls_policies('payments.token'::regclass); SELECT platform.apply_subject_rls('payments.token'::regclass); SELECT platform.apply_grant_holder_subject_read_rls('payments.token'::regclass);
-- SELECT platform.drop_rls_policies('orders.sales_order'::regclass); SELECT platform.apply_scope_rls('orders.sales_order'::regclass); SELECT platform.apply_split_rls('orders.sales_order'::regclass, '(scope_path IS NOT NULL AND scope_path <@ ANY ((SELECT platform.current_scope_paths())::ltree[])) OR (subject_id = (SELECT NULLIF(current_setting(''ticvai.subject_id'', true), '''')::uuid))', 'scope_path IS NOT NULL AND scope_path <@ ANY ((SELECT platform.current_scope_paths())::ltree[])');
-- SELECT platform.drop_rls_policies('orders.order_line'::regclass); SELECT platform.apply_venue_rls('orders.order_line'::regclass); SELECT platform.apply_split_rls('orders.order_line'::regclass, '(platform.venue_in_scope(venue_id)) OR (EXISTS (SELECT 1 FROM orders.sales_order gp WHERE gp.id = orders.order_line.sales_order_id AND gp.subject_id = (SELECT NULLIF(current_setting(''ticvai.subject_id'', true), '''')::uuid)))', 'platform.venue_in_scope(venue_id)');
-- SELECT platform.drop_rls_policies('orders.order_event'::regclass); SELECT platform.apply_scope_rls('orders.order_event'::regclass); SELECT platform.apply_split_rls('orders.order_event'::regclass, '(scope_path IS NOT NULL AND scope_path <@ ANY ((SELECT platform.current_scope_paths())::ltree[])) OR (EXISTS (SELECT 1 FROM orders.sales_order gp WHERE gp.id = orders.order_event.order_id AND gp.subject_id = (SELECT NULLIF(current_setting(''ticvai.subject_id'', true), '''')::uuid)))', 'scope_path IS NOT NULL AND scope_path <@ ANY ((SELECT platform.current_scope_paths())::ltree[])');
-- SELECT platform.drop_rls_policies('orders.cart'::regclass); SELECT platform.apply_venue_rls('orders.cart'::regclass); SELECT platform.apply_split_rls('orders.cart'::regclass, '(platform.venue_in_scope(venue_id)) OR (subject_id = (SELECT NULLIF(current_setting(''ticvai.subject_id'', true), '''')::uuid))', '(platform.venue_in_scope(venue_id)) OR (subject_id = (SELECT NULLIF(current_setting(''ticvai.subject_id'', true), '''')::uuid))');
-- SELECT platform.drop_rls_policies('marketing.consent_record'::regclass); SELECT platform.apply_subject_rls('marketing.consent_record'::regclass); SELECT platform.apply_grant_holder_subject_read_rls('marketing.consent_record'::regclass);
-- DROP INDEX IF EXISTS tenancy.device_firmware_device_kind_version_uniq;
-- DROP INDEX IF EXISTS identity.subject_data_export_part_export_id_owner_uniq;
-- DROP INDEX IF EXISTS marketing.guest_profile_subject_id_uniq;
-- DROP INDEX IF EXISTS marketing.guest_preference_subject_id_uniq;
-- DROP INDEX IF EXISTS identity.subject_data_export_part_export_id_idx;
-- DROP INDEX IF EXISTS marketing.privacy_request_approval_request_id_idx;
-- DROP INDEX IF EXISTS ai.proposed_action_map_id_idx;
-- ALTER TABLE platform.outlet DROP COLUMN IF EXISTS order_number_prefix;
-- DROP TABLE IF EXISTS identity.subject_data_export_part;
-- DELETE FROM platform.schema_version WHERE version = 'V0118';
