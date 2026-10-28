-- V0119 -- tenant database, after r1 (9cec72d) (20261029): the names the contracts use.
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
-- 0 column rename(s), 0 key(s) added, renamed or dropped, 6 index(es) renamed or dropped.

-- catalogue.group_package | drop index | group_package_product_id_idx
DO $$ BEGIN IF to_regclass('catalogue.group_package_product_id_idx') IS NOT NULL THEN DROP INDEX catalogue.group_package_product_id_idx; END IF; END $$;

-- catalogue.product_eligibility_rule | drop index | product_eligibility_rule_product_id_idx
DO $$ BEGIN IF to_regclass('catalogue.product_eligibility_rule_product_id_idx') IS NOT NULL THEN DROP INDEX catalogue.product_eligibility_rule_product_id_idx; END IF; END $$;

-- games.reader_sync_status | drop index | reader_sync_status_reader_id_idx
DO $$ BEGIN IF to_regclass('games.reader_sync_status_reader_id_idx') IS NOT NULL THEN DROP INDEX games.reader_sync_status_reader_id_idx; END IF; END $$;

-- seating.accessible | drop index | accessible_seat_map_id_idx
DO $$ BEGIN IF to_regclass('seating.accessible_seat_map_id_idx') IS NOT NULL THEN DROP INDEX seating.accessible_seat_map_id_idx; END IF; END $$;

-- tenancy.device_assignment | drop index | device_assignment_device_id_idx
DO $$ BEGIN IF to_regclass('tenancy.device_assignment_device_id_idx') IS NOT NULL THEN DROP INDEX tenancy.device_assignment_device_id_idx; END IF; END $$;

-- catalogue.product_channel_text | drop index | product_channel_text_product_id_idx
DO $$ BEGIN IF to_regclass('catalogue.product_channel_text_product_id_idx') IS NOT NULL THEN DROP INDEX catalogue.product_channel_text_product_id_idx; END IF; END $$;

INSERT INTO platform.schema_version (version, description, checksum)
VALUES ('V0119', 'after r1 (9cec72d), names the contracts use: 0 column rename(s), 0 key(s) added, renamed or dropped, 6 index(es) renamed or dropped', '2547f397ffa1251d10ae3539365a779894433b179630b66502544a7f343b9105')
ON CONFLICT (version) DO NOTHING;

-- ============================================================================
-- ROLLBACK
-- ============================================================================
-- Commented out so that applying this file never runs it: the rollback is run by removing the
-- leading `-- `, and is tested in CI against a restored snapshot (backend/MIGRATIONS.md).
-- CREATE INDEX IF NOT EXISTS product_channel_text_product_id_idx ON catalogue.product_channel_text (product_id);
-- CREATE INDEX IF NOT EXISTS device_assignment_device_id_idx ON tenancy.device_assignment (device_id);
-- CREATE INDEX IF NOT EXISTS accessible_seat_map_id_idx ON seating.accessible (seat_map_id);
-- CREATE INDEX IF NOT EXISTS reader_sync_status_reader_id_idx ON games.reader_sync_status (reader_id);
-- CREATE INDEX IF NOT EXISTS product_eligibility_rule_product_id_idx ON catalogue.product_eligibility_rule (product_id);
-- CREATE INDEX IF NOT EXISTS group_package_product_id_idx ON catalogue.group_package (product_id);
-- DELETE FROM platform.schema_version WHERE version = 'V0119';
