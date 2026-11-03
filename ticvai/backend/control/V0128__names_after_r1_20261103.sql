-- V0128 -- control database, after r1 (9cec72d) (20261103): the names the contracts use.
-- **Written by tools/derive-ddl.py in frozen mode. Do not edit after merge; a mistake is a new migration.**
--
-- The baseline under backend/control/ is frozen at r1 (9cec72d), but the schema reference has renamed columns,
-- added foreign keys and stopped generating some indexes since. Migrations written from the baseline DDL
-- create the old names; this file brings a database built from them to the names the contracts use.
-- Every statement is a guarded block: it does nothing when its table, key or index is not there yet, or is
-- there already under the new name, so the file can be applied twice and in any database. A table created
-- by a migration that runs after this one copies the blocks that name it (ticket text: 'Changes this file
-- makes to your tables'). A foreign key is added NOT VALID: it checks every new write, and the owner runs
-- ALTER TABLE ... VALIDATE CONSTRAINT when the rows already there are known to be clean.
-- 0 column rename(s), 0 key(s) added, renamed or dropped, 1 index(es) renamed or dropped.

-- control.plan | drop index | plan_code_uniq
DO $$ BEGIN IF to_regclass('control.plan_code_uniq') IS NOT NULL THEN DROP INDEX control.plan_code_uniq; END IF; END $$;

INSERT INTO platform.schema_version (version, description, checksum)
VALUES ('V0128', 'after r1 (9cec72d), names the contracts use: 0 column rename(s), 0 key(s) added, renamed or dropped, 1 index(es) renamed or dropped', '7239468b911901968464094a3e12046ed75ac7ee4f2e005259dc2bad858f3f84')
ON CONFLICT (version) DO NOTHING;

-- ============================================================================
-- ROLLBACK
-- ============================================================================
-- Commented out so that applying this file never runs it: the rollback is run by removing the
-- leading `-- `, and is tested in CI against a restored snapshot (backend/MIGRATIONS.md).
-- CREATE UNIQUE INDEX IF NOT EXISTS plan_code_uniq ON control.plan (lower(code));
-- DELETE FROM platform.schema_version WHERE version = 'V0128';
