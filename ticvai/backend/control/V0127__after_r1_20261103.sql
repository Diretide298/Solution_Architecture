-- V0127 -- control database, after r1 (9cec72d) (20261103).
-- **Written by tools/derive-ddl.py in frozen mode. Do not edit after merge; a mistake is a new migration.**
--
-- The baseline under backend/control/ is frozen at r1 (9cec72d), so the change to the schema reference
-- since then is written here instead: additive only. Changes that are not additive (drops, renames,
-- type changes) are not generated; they are listed for a person in handoff/migration-review.md.
-- Every statement that needs a table is a guarded block (CHG-R9MIG-002): it does nothing where its table
-- or a column it names is not there yet, so the file applies as one transaction, twice, on any database;
-- the migration that creates such a table later copies the block. A table's policy change is one block.
-- 0 table(s), 0 column(s), 3 index(es), 0 other statement(s).

DO $$ BEGIN IF to_regclass('control.plan') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'control' AND table_name = 'plan' AND column_name = 'code') AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'control' AND table_name = 'plan' AND column_name = 'version') THEN
CREATE UNIQUE INDEX IF NOT EXISTS plan_code_version_uniq ON control.plan (lower(code), version);
END IF; END $$;

DO $$ BEGIN IF to_regclass('control.plan_limit') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'control' AND table_name = 'plan_limit' AND column_name = 'metric') AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'control' AND table_name = 'plan_limit' AND column_name = 'plan_id') AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'control' AND table_name = 'plan_limit' AND column_name = 'plan_version') THEN
CREATE UNIQUE INDEX IF NOT EXISTS plan_limit_plan_id_plan_version_metric_uniq ON control.plan_limit (plan_id, plan_version, metric);
END IF; END $$;

DO $$ BEGIN IF to_regclass('control.plan_module') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'control' AND table_name = 'plan_module' AND column_name = 'licensed_module') AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'control' AND table_name = 'plan_module' AND column_name = 'plan_id') AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'control' AND table_name = 'plan_module' AND column_name = 'plan_version') THEN
CREATE UNIQUE INDEX IF NOT EXISTS plan_module_plan_id_plan_version_licensed_module_uniq ON control.plan_module (plan_id, plan_version, licensed_module);
END IF; END $$;

INSERT INTO platform.schema_version (version, description, checksum)
VALUES ('V0127', 'after r1 (9cec72d): 0 table(s), 0 column(s), 3 index(es), 0 other statement(s)', '7592812def14863b13799af8d75faeeb3ba5398614dc375a130910defe2438fa')
ON CONFLICT (version) DO NOTHING;

-- ============================================================================
-- ROLLBACK
-- ============================================================================
-- Commented out so that applying this file never runs it: the rollback is run by removing the
-- leading `-- `, and is tested in CI against a restored snapshot (backend/MIGRATIONS.md).
-- DROP INDEX IF EXISTS control.plan_module_plan_id_plan_version_licensed_module_uniq;
-- DROP INDEX IF EXISTS control.plan_limit_plan_id_plan_version_metric_uniq;
-- DROP INDEX IF EXISTS control.plan_code_version_uniq;
-- DELETE FROM platform.schema_version WHERE version = 'V0127';
