-- V0124 -- tenant database, after r1 (9cec72d) (20261102).
-- **Written by tools/derive-ddl.py in frozen mode. Do not edit after merge; a mistake is a new migration.**
--
-- The baseline under backend/tenant/ is frozen at r1 (9cec72d), so the change to the schema reference
-- since then is written here instead: additive only. Changes that are not additive (drops, renames,
-- type changes) are not generated; they are listed for a person in handoff/migration-review.md.
-- Every statement that needs a table is a guarded block (CHG-R9MIG-002): it does nothing where its table
-- or a column it names is not there yet, so the file applies as one transaction, twice, on any database;
-- the migration that creates such a table later copies the block. A table's policy change is one block.
-- 0 table(s), 5 column(s), 2 index(es), 52 other statement(s).

DO $$ BEGIN IF to_regclass('catalogue.product') IS NOT NULL THEN
ALTER TABLE catalogue.product ADD COLUMN IF NOT EXISTS is_featured boolean DEFAULT false;
END IF; END $$;

DO $$ BEGIN IF to_regclass('catalogue.product') IS NOT NULL THEN
ALTER TABLE catalogue.product ADD COLUMN IF NOT EXISTS compare_at_amount numeric(18,4);
END IF; END $$;

DO $$ BEGIN IF to_regclass('catalogue.variant') IS NOT NULL THEN
ALTER TABLE catalogue.variant ADD COLUMN IF NOT EXISTS price_category_id uuid;
END IF; END $$;

DO $$ BEGIN IF to_regclass('marketing.message_dispatch') IS NOT NULL THEN
ALTER TABLE marketing.message_dispatch ADD COLUMN IF NOT EXISTS body text;
END IF; END $$;

DO $$ BEGIN IF to_regclass('tenancy.device_credential') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'tenancy' AND table_name = 'device_credential' AND column_name = 'kind') THEN
ALTER TABLE tenancy.device_credential DROP CONSTRAINT IF EXISTS device_credential_kind_chk;
END IF; END $$;

DO $$ BEGIN IF to_regclass('tenancy.device_credential') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'tenancy' AND table_name = 'device_credential' AND column_name = 'kind') THEN
ALTER TABLE tenancy.device_credential ADD CONSTRAINT device_credential_kind_chk CHECK (kind IN ('clientCertificate', 'deviceToken', 'mutualTls', 'apiKey')) NOT VALID;
END IF; END $$;

DO $$ BEGIN IF to_regclass('tenancy.device_credential') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'tenancy' AND table_name = 'device_credential' AND column_name = 'kind') THEN
ALTER TABLE tenancy.device_credential VALIDATE CONSTRAINT device_credential_kind_chk;
END IF; END $$;

DO $$ BEGIN IF to_regclass('whitelabel.config_version') IS NOT NULL AND NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'whitelabel' AND table_name = 'config_version' AND column_name = 'activated_at') THEN
ALTER TABLE whitelabel.config_version ADD COLUMN IF NOT EXISTS activated_at timestamptz;
UPDATE whitelabel.config_version SET activated_at = published_at WHERE is_current;
END IF; END $$;

DO $$ BEGIN IF to_regclass('catalogue.variant') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'catalogue' AND table_name = 'variant' AND column_name = 'price_category_id') THEN
CREATE INDEX IF NOT EXISTS variant_price_category_id_idx ON catalogue.variant (price_category_id);
END IF; END $$;

DO $$ BEGIN IF to_regclass('marketing.message_dispatch') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'marketing' AND table_name = 'message_dispatch' AND column_name = 'channel') AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'marketing' AND table_name = 'message_dispatch' AND column_name = 'source_ref') AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'marketing' AND table_name = 'message_dispatch' AND column_name = 'subject_id') THEN
CREATE INDEX IF NOT EXISTS message_dispatch_source_ref_subject_id_channel_idx ON marketing.message_dispatch (source_ref, subject_id, channel);
END IF; END $$;

DO $$ BEGIN IF EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'commerce') AND to_regclass('access.media_template') IS NOT NULL THEN GRANT SELECT ON access.media_template TO commerce; END IF; END $$;

DO $$ BEGIN IF EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'operations') AND EXISTS (SELECT 1 FROM pg_namespace WHERE nspname = 'tenancy') THEN GRANT USAGE ON SCHEMA tenancy TO operations; END IF; END $$;

DO $$ BEGIN IF EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'operations') AND to_regclass('tenancy.device_credential') IS NOT NULL THEN GRANT SELECT ON tenancy.device_credential TO operations; END IF; END $$;

DO $$ BEGIN IF EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'operations') AND to_regclass('platform.device') IS NOT NULL THEN GRANT SELECT ON platform.device TO operations; END IF; END $$;

DO $$ BEGIN IF EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'operations') AND to_regclass('catalogue.rate') IS NOT NULL THEN GRANT SELECT ON catalogue.rate TO operations; END IF; END $$;

DO $$ BEGIN IF EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'operations') AND EXISTS (SELECT 1 FROM pg_namespace WHERE nspname = 'orders') THEN GRANT USAGE ON SCHEMA orders TO operations; END IF; END $$;

DO $$ BEGIN IF EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'operations') AND to_regclass('orders.order_line') IS NOT NULL THEN GRANT SELECT ON orders.order_line TO operations; END IF; END $$;

DO $$ BEGIN IF EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'operations') AND EXISTS (SELECT 1 FROM pg_namespace WHERE nspname = 'promotions') THEN GRANT USAGE ON SCHEMA promotions TO operations; END IF; END $$;

DO $$ BEGIN IF EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'operations') AND to_regclass('promotions.promotion') IS NOT NULL THEN GRANT SELECT ON promotions.promotion TO operations; END IF; END $$;

DO $$ BEGIN IF EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'operations') AND to_regclass('promotions.promotion_rule') IS NOT NULL THEN GRANT SELECT ON promotions.promotion_rule TO operations; END IF; END $$;

DO $$ BEGIN IF EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'operations') AND EXISTS (SELECT 1 FROM pg_namespace WHERE nspname = 'accreditation') THEN GRANT USAGE ON SCHEMA accreditation TO operations; END IF; END $$;

DO $$ BEGIN IF EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'operations') AND to_regclass('accreditation.application') IS NOT NULL THEN GRANT SELECT ON accreditation.application TO operations; END IF; END $$;

DO $$ BEGIN IF EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'operations') AND to_regclass('accreditation.credential') IS NOT NULL THEN GRANT SELECT ON accreditation.credential TO operations; END IF; END $$;

DO $$ BEGIN IF EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'operations') AND to_regclass('accreditation.holder') IS NOT NULL THEN GRANT SELECT ON accreditation.holder TO operations; END IF; END $$;

DO $$ BEGIN IF EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'operations') AND to_regclass('accreditation.validity') IS NOT NULL THEN GRANT SELECT ON accreditation.validity TO operations; END IF; END $$;

DO $$ BEGIN IF EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'operations') AND EXISTS (SELECT 1 FROM pg_namespace WHERE nspname = 'approvals') THEN GRANT USAGE ON SCHEMA approvals TO operations; END IF; END $$;

DO $$ BEGIN IF EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'operations') AND to_regclass('approvals.request') IS NOT NULL THEN GRANT SELECT ON approvals.request TO operations; END IF; END $$;

DO $$ BEGIN IF EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'operations') AND to_regclass('tenancy.data_retention_setting') IS NOT NULL THEN GRANT SELECT ON tenancy.data_retention_setting TO operations; END IF; END $$;

DO $$ BEGIN IF EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'operations') AND EXISTS (SELECT 1 FROM pg_namespace WHERE nspname = 'workforce') THEN GRANT USAGE ON SCHEMA workforce TO operations; END IF; END $$;

DO $$ BEGIN IF EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'operations') AND to_regclass('workforce.shift') IS NOT NULL THEN GRANT SELECT ON workforce.shift TO operations; END IF; END $$;

DO $$ BEGIN IF EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'operations') AND to_regclass('catalogue.channel_capacity') IS NOT NULL THEN GRANT SELECT ON catalogue.channel_capacity TO operations; END IF; END $$;

DO $$ BEGIN IF EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'operations') AND to_regclass('catalogue.product_eligibility_rule') IS NOT NULL THEN GRANT SELECT ON catalogue.product_eligibility_rule TO operations; END IF; END $$;

DO $$ BEGIN IF EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'operations') AND to_regclass('catalogue.tax_profile') IS NOT NULL THEN GRANT SELECT ON catalogue.tax_profile TO operations; END IF; END $$;

DO $$ BEGIN IF EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'operations') AND to_regclass('promotions.bundle') IS NOT NULL THEN GRANT SELECT ON promotions.bundle TO operations; END IF; END $$;

DO $$ BEGIN IF EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'operations') AND EXISTS (SELECT 1 FROM pg_namespace WHERE nspname = 'seating') THEN GRANT USAGE ON SCHEMA seating TO operations; END IF; END $$;

DO $$ BEGIN IF EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'operations') AND to_regclass('seating.seat') IS NOT NULL THEN GRANT SELECT ON seating.seat TO operations; END IF; END $$;

DO $$ BEGIN IF EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'operations') AND to_regclass('orders.cart') IS NOT NULL THEN GRANT SELECT ON orders.cart TO operations; END IF; END $$;

DO $$ BEGIN IF EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'operations') AND to_regclass('orders.cart_line') IS NOT NULL THEN GRANT SELECT ON orders.cart_line TO operations; END IF; END $$;

DO $$ BEGIN IF EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'operations') AND to_regclass('orders.deposit') IS NOT NULL THEN GRANT SELECT ON orders.deposit TO operations; END IF; END $$;

DO $$ BEGIN IF EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'operations') AND to_regclass('orders.deposit_policy') IS NOT NULL THEN GRANT SELECT ON orders.deposit_policy TO operations; END IF; END $$;

DO $$ BEGIN IF EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'operations') AND to_regclass('orders.group_booking') IS NOT NULL THEN GRANT SELECT ON orders.group_booking TO operations; END IF; END $$;

DO $$ BEGIN IF EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'operations') AND to_regclass('orders.invitation') IS NOT NULL THEN GRANT SELECT ON orders.invitation TO operations; END IF; END $$;

DO $$ BEGIN IF EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'operations') AND to_regclass('orders.order_fee') IS NOT NULL THEN GRANT SELECT ON orders.order_fee TO operations; END IF; END $$;

DO $$ BEGIN IF EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'operations') AND to_regclass('orders.order_line_discount') IS NOT NULL THEN GRANT SELECT ON orders.order_line_discount TO operations; END IF; END $$;

DO $$ BEGIN IF EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'operations') AND to_regclass('orders.payment') IS NOT NULL THEN GRANT SELECT ON orders.payment TO operations; END IF; END $$;

DO $$ BEGIN IF EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'operations') AND to_regclass('orders.refund') IS NOT NULL THEN GRANT SELECT ON orders.refund TO operations; END IF; END $$;

DO $$ BEGIN IF EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'operations') AND to_regclass('orders.refund_policy') IS NOT NULL THEN GRANT SELECT ON orders.refund_policy TO operations; END IF; END $$;

DO $$ BEGIN IF EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'operations') AND to_regclass('orders.reservation') IS NOT NULL THEN GRANT SELECT ON orders.reservation TO operations; END IF; END $$;

DO $$ BEGIN IF EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'operations') AND to_regclass('orders.sales_order') IS NOT NULL THEN GRANT SELECT ON orders.sales_order TO operations; END IF; END $$;

DO $$ BEGIN IF EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'operations') AND to_regclass('payments.instalment_policy') IS NOT NULL THEN GRANT SELECT ON payments.instalment_policy TO operations; END IF; END $$;

DO $$ BEGIN IF EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'operations') AND to_regclass('payments.provider') IS NOT NULL THEN GRANT SELECT ON payments.provider TO operations; END IF; END $$;

DO $$ BEGIN IF EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'operations') AND to_regclass('payments.provider_connection') IS NOT NULL THEN GRANT SELECT ON payments.provider_connection TO operations; END IF; END $$;

DO $$ BEGIN IF EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'access') AND EXISTS (SELECT 1 FROM pg_namespace WHERE nspname = 'approvals') THEN GRANT USAGE ON SCHEMA approvals TO access; END IF; END $$;

DO $$ BEGIN IF EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'access') AND to_regclass('approvals.request') IS NOT NULL THEN GRANT SELECT ON approvals.request TO access; END IF; END $$;

DO $$ BEGIN IF EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'access') AND to_regclass('approvals.rule') IS NOT NULL THEN GRANT SELECT ON approvals.rule TO access; END IF; END $$;

DO $$ BEGIN IF EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'access') AND to_regclass('platform.region_settings') IS NOT NULL THEN GRANT SELECT ON platform.region_settings TO access; END IF; END $$;

DO $$ BEGIN IF EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'access') AND EXISTS (SELECT 1 FROM pg_namespace WHERE nspname = 'tenancy') THEN GRANT USAGE ON SCHEMA tenancy TO access; END IF; END $$;

DO $$ BEGIN IF EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'access') AND to_regclass('tenancy.data_retention_setting') IS NOT NULL THEN GRANT SELECT ON tenancy.data_retention_setting TO access; END IF; END $$;

DO $$ BEGIN IF EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'access') AND to_regclass('catalogue.product') IS NOT NULL THEN GRANT SELECT ON catalogue.product TO access; END IF; END $$;

DO $$ BEGIN IF EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'access') AND to_regclass('catalogue.product_media') IS NOT NULL THEN GRANT SELECT ON catalogue.product_media TO access; END IF; END $$;

DO $$ BEGIN IF EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'commerce') AND to_regclass('access.access_point') IS NOT NULL THEN GRANT SELECT ON access.access_point TO commerce; END IF; END $$;

INSERT INTO platform.schema_version (version, description, checksum)
VALUES ('V0124', 'after r1 (9cec72d): 0 table(s), 5 column(s), 2 index(es), 52 other statement(s)', '7844569c0b8030ec3187c249b5ecd715656d29f7bf3cdd7cf50abc63702dd961')
ON CONFLICT (version) DO NOTHING;

-- ============================================================================
-- ROLLBACK
-- ============================================================================
-- Commented out so that applying this file never runs it: the rollback is run by removing the
-- leading `-- `, and is tested in CI against a restored snapshot (backend/MIGRATIONS.md).
-- REVOKE SELECT ON access.access_point FROM commerce;
-- REVOKE SELECT ON catalogue.product_media FROM access;
-- REVOKE SELECT ON catalogue.product FROM access;
-- REVOKE SELECT ON tenancy.data_retention_setting FROM access;
-- REVOKE USAGE ON SCHEMA tenancy FROM access;
-- REVOKE SELECT ON platform.region_settings FROM access;
-- REVOKE SELECT ON approvals.rule FROM access;
-- REVOKE SELECT ON approvals.request FROM access;
-- REVOKE USAGE ON SCHEMA approvals FROM access;
-- REVOKE SELECT ON payments.provider_connection FROM operations;
-- REVOKE SELECT ON payments.provider FROM operations;
-- REVOKE SELECT ON payments.instalment_policy FROM operations;
-- REVOKE SELECT ON orders.sales_order FROM operations;
-- REVOKE SELECT ON orders.reservation FROM operations;
-- REVOKE SELECT ON orders.refund_policy FROM operations;
-- REVOKE SELECT ON orders.refund FROM operations;
-- REVOKE SELECT ON orders.payment FROM operations;
-- REVOKE SELECT ON orders.order_line_discount FROM operations;
-- REVOKE SELECT ON orders.order_fee FROM operations;
-- REVOKE SELECT ON orders.invitation FROM operations;
-- REVOKE SELECT ON orders.group_booking FROM operations;
-- REVOKE SELECT ON orders.deposit_policy FROM operations;
-- REVOKE SELECT ON orders.deposit FROM operations;
-- REVOKE SELECT ON orders.cart_line FROM operations;
-- REVOKE SELECT ON orders.cart FROM operations;
-- REVOKE SELECT ON seating.seat FROM operations;
-- REVOKE USAGE ON SCHEMA seating FROM operations;
-- REVOKE SELECT ON promotions.bundle FROM operations;
-- REVOKE SELECT ON catalogue.tax_profile FROM operations;
-- REVOKE SELECT ON catalogue.product_eligibility_rule FROM operations;
-- REVOKE SELECT ON catalogue.channel_capacity FROM operations;
-- REVOKE SELECT ON workforce.shift FROM operations;
-- REVOKE USAGE ON SCHEMA workforce FROM operations;
-- REVOKE SELECT ON tenancy.data_retention_setting FROM operations;
-- REVOKE SELECT ON approvals.request FROM operations;
-- REVOKE USAGE ON SCHEMA approvals FROM operations;
-- REVOKE SELECT ON accreditation.validity FROM operations;
-- REVOKE SELECT ON accreditation.holder FROM operations;
-- REVOKE SELECT ON accreditation.credential FROM operations;
-- REVOKE SELECT ON accreditation.application FROM operations;
-- REVOKE USAGE ON SCHEMA accreditation FROM operations;
-- REVOKE SELECT ON promotions.promotion_rule FROM operations;
-- REVOKE SELECT ON promotions.promotion FROM operations;
-- REVOKE USAGE ON SCHEMA promotions FROM operations;
-- REVOKE SELECT ON orders.order_line FROM operations;
-- REVOKE USAGE ON SCHEMA orders FROM operations;
-- REVOKE SELECT ON catalogue.rate FROM operations;
-- REVOKE SELECT ON platform.device FROM operations;
-- REVOKE SELECT ON tenancy.device_credential FROM operations;
-- REVOKE USAGE ON SCHEMA tenancy FROM operations;
-- REVOKE SELECT ON access.media_template FROM commerce;
-- DROP INDEX IF EXISTS marketing.message_dispatch_source_ref_subject_id_channel_idx;
-- DROP INDEX IF EXISTS catalogue.variant_price_category_id_idx;
-- ALTER TABLE whitelabel.config_version DROP COLUMN IF EXISTS activated_at;
-- ALTER TABLE tenancy.device_credential DROP CONSTRAINT IF EXISTS device_credential_kind_chk; ALTER TABLE tenancy.device_credential ADD CONSTRAINT device_credential_kind_chk CHECK (kind IN ('clientCertificate', 'deviceToken', 'mutualTls')) NOT VALID;
-- ALTER TABLE marketing.message_dispatch DROP COLUMN IF EXISTS body;
-- ALTER TABLE catalogue.variant DROP COLUMN IF EXISTS price_category_id;
-- ALTER TABLE catalogue.product DROP COLUMN IF EXISTS compare_at_amount;
-- ALTER TABLE catalogue.product DROP COLUMN IF EXISTS is_featured;
-- DELETE FROM platform.schema_version WHERE version = 'V0124';
