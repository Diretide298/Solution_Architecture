-- V0126 -- control database, after r1 (9cec72d) (20261103).
-- **Written by tools/derive-ddl.py in frozen mode. Do not edit after merge; a mistake is a new migration.**
--
-- The baseline under backend/control/ is frozen at r1 (9cec72d), so the change to the schema reference
-- since then is written here instead: additive only. Changes that are not additive (drops, renames,
-- type changes) are not generated; they are listed for a person in handoff/migration-review.md.
-- Every statement that needs a table is a guarded block (CHG-R9MIG-002): it does nothing where its table
-- or a column it names is not there yet, so the file applies as one transaction, twice, on any database;
-- the migration that creates such a table later copies the block. A table's policy change is one block.
-- 0 table(s), 0 column(s), 1 index(es), 0 other statement(s).

DO $$ BEGIN IF to_regclass('control.module_listing') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'control' AND table_name = 'module_listing' AND column_name = 'module_code') THEN
CREATE UNIQUE INDEX IF NOT EXISTS module_listing_module_code_uniq ON control.module_listing (lower(module_code));
END IF; END $$;

INSERT INTO platform.schema_version (version, description, checksum)
VALUES ('V0126', 'after r1 (9cec72d): 0 table(s), 0 column(s), 1 index(es), 0 other statement(s)', 'a126b7784ff8f8e0f7d819bc75004fea690e20480021bc4862ede4438bffe417')
ON CONFLICT (version) DO NOTHING;

-- ============================================================================
-- ROLLBACK
-- ============================================================================
-- Commented out so that applying this file never runs it: the rollback is run by removing the
-- leading `-- `, and is tested in CI against a restored snapshot (backend/MIGRATIONS.md).
-- DROP INDEX IF EXISTS control.module_listing_module_code_uniq;
-- DELETE FROM platform.schema_version WHERE version = 'V0126';
