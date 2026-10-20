-- V0105a -- tenant database, after r1 (9cec72d) (20261020): the names the contracts use.
-- **Written by tools/derive-ddl.py in frozen mode. Do not edit after merge; a mistake is a new migration.**
--
-- The baseline under backend/tenant/ is frozen at r1 (9cec72d), but the schema reference has renamed columns,
-- added foreign keys and stopped generating some indexes since. Migrations written from the baseline DDL
-- create the old names; this file brings a database built from them to the names the contracts use.
-- Every statement is a guarded block: it does nothing when its table, key or index is not there yet, or is
-- there already under the new name, so the file can be applied twice and in any database. A table created
-- by a migration that runs after this one copies the blocks that name it (ticket text: 'Changes this file
-- makes to your tables'). A foreign key is added NOT VALID: it checks every new write, and the owner runs
-- ALTER TABLE ... VALIDATE CONSTRAINT when the rows already there are known to be clean.
-- 1 table(s) renamed or moved, 0 column rename(s), 0 key(s) added, renamed or dropped, 0 index(es) renamed or dropped.
--
-- **This file runs before V0107__names_after_r1_20261019.sql**: the renames the package declares (tools/derive-schema-history.py
-- RENAMES and COLUMN_RENAMES), each with the keys, indexes, checks and row-level security policies named for
-- it, so V0107__names_after_r1_20261019.sql and every file after it see the names the contracts use (a frozen file that applies
-- row-level security on a column by its new name stops a fresh database without it). A table moved into another
-- schema keeps its objects' names. A rename a frozen file still needs under its old name runs in the names
-- file after that one. The keys and indexes that do not follow a rename are in V0109.

-- sync.dsar_request | move table | platform.dsar_request to sync
DO $$ BEGIN IF to_regclass('platform.dsar_request') IS NOT NULL AND to_regclass('sync.dsar_request') IS NULL THEN ALTER TABLE platform.dsar_request SET SCHEMA sync; END IF; END $$;

INSERT INTO platform.schema_version (version, description, checksum)
VALUES ('V0105a', 'after r1 (9cec72d), names the contracts use: 1 table(s) renamed or moved, 0 column rename(s), 0 key(s) added, renamed or dropped, 0 index(es) renamed or dropped', '92e82dfd416d0655b78b1cf02aee09ad1e89de8017d3db48e9830ccf846a2975')
ON CONFLICT (version) DO NOTHING;

-- ============================================================================
-- ROLLBACK
-- ============================================================================
-- Commented out so that applying this file never runs it: the rollback is run by removing the
-- leading `-- `, and is tested in CI against a restored snapshot (backend/MIGRATIONS.md).
-- ALTER TABLE sync.dsar_request SET SCHEMA platform;
-- DELETE FROM platform.schema_version WHERE version = 'V0105a';
