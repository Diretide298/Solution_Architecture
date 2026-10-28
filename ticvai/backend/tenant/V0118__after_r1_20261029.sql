-- V0118 -- tenant database, after r1 (9cec72d) (20261029).
-- **Written by tools/derive-ddl.py in frozen mode. Do not edit after merge; a mistake is a new migration.**
--
-- The baseline under backend/tenant/ is frozen at r1 (9cec72d), so the change to the schema reference
-- since then is written here instead: additive only. Changes that are not additive (drops, renames,
-- type changes) are not generated; they are listed for a person in handoff/migration-review.md.
-- Every statement that needs a table is a guarded block (CHG-R9MIG-002): it does nothing where its table
-- or a column it names is not there yet, so the file applies as one transaction, twice, on any database;
-- the migration that creates such a table later copies the block. A table's policy change is one block.
-- 0 table(s), 1 column(s), 3 index(es), 10 other statement(s).

DO $$ BEGIN IF to_regclass('platform.outlet') IS NOT NULL THEN
ALTER TABLE platform.outlet ADD COLUMN IF NOT EXISTS order_number_prefix text CONSTRAINT outlet_order_number_prefix_chk CHECK (order_number_prefix IN ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z') AND char_length(order_number_prefix) <= 1);
END IF; END $$;

DO $$ BEGIN IF to_regclass('ai.proposed_action') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'ai' AND table_name = 'proposed_action' AND column_name = 'map_id') THEN
CREATE INDEX IF NOT EXISTS proposed_action_map_id_idx ON ai.proposed_action (map_id);
END IF; END $$;

DO $$ BEGIN IF to_regclass('marketing.privacy_request') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'marketing' AND table_name = 'privacy_request' AND column_name = 'approval_request_id') THEN
CREATE INDEX IF NOT EXISTS privacy_request_approval_request_id_idx ON marketing.privacy_request (approval_request_id);
END IF; END $$;

DO $$ BEGIN IF to_regclass('tenancy.device_firmware') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'tenancy' AND table_name = 'device_firmware' AND column_name = 'device_kind') AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'tenancy' AND table_name = 'device_firmware' AND column_name = 'version') THEN
CREATE UNIQUE INDEX IF NOT EXISTS device_firmware_device_kind_version_uniq ON tenancy.device_firmware (lower(device_kind), lower(version));
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
VALUES ('V0118', 'after r1 (9cec72d): 0 table(s), 1 column(s), 3 index(es), 10 other statement(s)', 'a28c97e3d278804326558a96c2ad80567952e9d469d72eb77869646bebc6affa')
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
-- DROP INDEX IF EXISTS tenancy.device_firmware_device_kind_version_uniq;
-- DROP INDEX IF EXISTS marketing.privacy_request_approval_request_id_idx;
-- DROP INDEX IF EXISTS ai.proposed_action_map_id_idx;
-- ALTER TABLE platform.outlet DROP COLUMN IF EXISTS order_number_prefix;
-- DELETE FROM platform.schema_version WHERE version = 'V0118';
