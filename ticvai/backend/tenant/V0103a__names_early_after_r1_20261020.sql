-- V0103a -- tenant database, after r1 (9cec72d) (20261020): the names the contracts use.
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
-- 4 column rename(s), 0 key(s) added or renamed, 0 index(es) renamed or dropped.
--
-- **This file runs before V0104__after_r1_20261015.sql**, which applies row-level security on these columns by their new
-- names: without it a database built from the files in name order stops at V0104__after_r1_20261015.sql. The other renames,
-- with the keys and indexes that follow them, are in V0107; its blocks for these columns find them renamed
-- and do nothing.

-- access.access_change | rename column | old_access_id to old_entitlement_id
DO $$ BEGIN IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'access' AND table_name = 'access_change' AND column_name = 'old_access_id') AND NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'access' AND table_name = 'access_change' AND column_name = 'old_entitlement_id') THEN ALTER TABLE access.access_change RENAME COLUMN old_access_id TO old_entitlement_id; END IF; END $$;

-- access.entry_rule_point | rename column | admission_profile_id to admission_rules_id
DO $$ BEGIN IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'access' AND table_name = 'entry_rule_point' AND column_name = 'admission_profile_id') AND NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'access' AND table_name = 'entry_rule_point' AND column_name = 'admission_rules_id') THEN ALTER TABLE access.entry_rule_point RENAME COLUMN admission_profile_id TO admission_rules_id; END IF; END $$;

-- marketing.waiver_signature | rename column | template_id to form_definition_id
DO $$ BEGIN IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'marketing' AND table_name = 'waiver_signature' AND column_name = 'template_id') AND NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'marketing' AND table_name = 'waiver_signature' AND column_name = 'form_definition_id') THEN ALTER TABLE marketing.waiver_signature RENAME COLUMN template_id TO form_definition_id; END IF; END $$;

-- platform.sale_board_tile | rename column | page_id to sale_board_page_id
DO $$ BEGIN IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'platform' AND table_name = 'sale_board_tile' AND column_name = 'page_id') AND NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'platform' AND table_name = 'sale_board_tile' AND column_name = 'sale_board_page_id') THEN ALTER TABLE platform.sale_board_tile RENAME COLUMN page_id TO sale_board_page_id; END IF; END $$;

INSERT INTO platform.schema_version (version, description, checksum)
VALUES ('V0103a', 'after r1 (9cec72d), names the contracts use: 4 column rename(s), 0 key(s) added or renamed, 0 index(es) renamed or dropped', 'e5695659c216e8db02741241516bb58dc28f65a65bba60f655f2824786da0001')
ON CONFLICT (version) DO NOTHING;

-- ============================================================================
-- ROLLBACK
-- ============================================================================
-- Commented out so that applying this file never runs it: the rollback is run by removing the
-- leading `-- `, and is tested in CI against a restored snapshot (backend/MIGRATIONS.md).
-- ALTER TABLE platform.sale_board_tile RENAME COLUMN sale_board_page_id TO page_id;
-- ALTER TABLE marketing.waiver_signature RENAME COLUMN form_definition_id TO template_id;
-- ALTER TABLE access.entry_rule_point RENAME COLUMN admission_rules_id TO admission_profile_id;
-- ALTER TABLE access.access_change RENAME COLUMN old_entitlement_id TO old_access_id;
-- DELETE FROM platform.schema_version WHERE version = 'V0103a';
