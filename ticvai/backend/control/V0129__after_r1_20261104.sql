-- V0129 -- control database, after r1 (9cec72d) (20261104).
-- **Written by tools/derive-ddl.py in frozen mode. Do not edit after merge; a mistake is a new migration.**
--
-- The baseline under backend/control/ is frozen at r1 (9cec72d), so the change to the schema reference
-- since then is written here instead: additive only. Changes that are not additive (drops, renames,
-- type changes) are not generated; they are listed for a person in handoff/migration-review.md.
-- Every statement that needs a table is a guarded block (CHG-R9MIG-002): it does nothing where its table
-- or a column it names is not there yet, so the file applies as one transaction, twice, on any database;
-- the migration that creates such a table later copies the block. A table's policy change is one block.
-- 0 table(s), 4 column(s), 3 index(es), 1 other statement(s).

DO $$ BEGIN IF to_regclass('control.api_version') IS NOT NULL THEN
ALTER TABLE control.api_version ADD COLUMN IF NOT EXISTS deprecation_reason text;
END IF; END $$;

DO $$ BEGIN IF to_regclass('control.api_version') IS NOT NULL THEN
ALTER TABLE control.api_version ADD COLUMN IF NOT EXISTS deprecation_notified_at timestamptz;
END IF; END $$;

DO $$ BEGIN IF to_regclass('control.capacity_pack') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'control' AND table_name = 'capacity_pack' AND column_name = 'unit') THEN
ALTER TABLE control.capacity_pack DROP CONSTRAINT IF EXISTS capacity_pack_unit_chk;
END IF; END $$;

DO $$ BEGIN IF to_regclass('control.capacity_pack') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'control' AND table_name = 'capacity_pack' AND column_name = 'unit') THEN
ALTER TABLE control.capacity_pack ADD CONSTRAINT capacity_pack_unit_chk CHECK (unit IN ('venues', 'workstations', 'activeUsers', 'devices', 'brandedApps', 'aiTokens', 'apiCalls', 'storageGb', 'transactions', 'guestProfiles')) NOT VALID;
END IF; END $$;

DO $$ BEGIN IF to_regclass('control.contract') IS NOT NULL THEN
ALTER TABLE control.contract ADD COLUMN IF NOT EXISTS pending_proration numeric(18,4);
END IF; END $$;

DO $$ BEGIN IF to_regclass('control.integration_listing') IS NOT NULL THEN
ALTER TABLE control.integration_listing ADD COLUMN IF NOT EXISTS review_notes text CONSTRAINT integration_listing_review_notes_chk CHECK (char_length(review_notes) <= 1000);
END IF; END $$;

DO $$ BEGIN IF to_regclass('control.api_client') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'control' AND table_name = 'api_client' AND column_name = 'client_id') THEN
CREATE UNIQUE INDEX IF NOT EXISTS api_client_client_id_uniq ON control.api_client (client_id);
END IF; END $$;

DO $$ BEGIN IF to_regclass('control.api_version') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'control' AND table_name = 'api_version' AND column_name = 'version') THEN
CREATE UNIQUE INDEX IF NOT EXISTS api_version_version_uniq ON control.api_version (version);
END IF; END $$;

DO $$ BEGIN IF to_regclass('control.developer_member') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'control' AND table_name = 'developer_member' AND column_name = 'email') AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'control' AND table_name = 'developer_member' AND column_name = 'status') THEN
CREATE UNIQUE INDEX IF NOT EXISTS developer_member_email_uniq ON control.developer_member (lower(email)) WHERE status = 'active';
END IF; END $$;

INSERT INTO platform.schema_version (version, description, checksum)
VALUES ('V0129', 'after r1 (9cec72d): 0 table(s), 4 column(s), 3 index(es), 1 other statement(s)', '9c258b2bb320a5fd9a76cab27b0ef22460670104835e6a0264f0d8650d3804e8')
ON CONFLICT (version) DO NOTHING;

-- ============================================================================
-- ROLLBACK
-- ============================================================================
-- Commented out so that applying this file never runs it: the rollback is run by removing the
-- leading `-- `, and is tested in CI against a restored snapshot (backend/MIGRATIONS.md).
-- DROP INDEX IF EXISTS control.developer_member_email_uniq;
-- DROP INDEX IF EXISTS control.api_version_version_uniq;
-- DROP INDEX IF EXISTS control.api_client_client_id_uniq;
-- ALTER TABLE control.integration_listing DROP COLUMN IF EXISTS review_notes;
-- ALTER TABLE control.contract DROP COLUMN IF EXISTS pending_proration;
-- ALTER TABLE control.capacity_pack DROP CONSTRAINT IF EXISTS capacity_pack_unit_chk;
-- ALTER TABLE control.api_version DROP COLUMN IF EXISTS deprecation_notified_at;
-- ALTER TABLE control.api_version DROP COLUMN IF EXISTS deprecation_reason;
-- DELETE FROM platform.schema_version WHERE version = 'V0129';
