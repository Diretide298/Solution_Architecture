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
-- 0 column rename(s), 1 key(s) added, renamed or dropped, 2 index(es) renamed or dropped.

-- catalogue.product | foreign key | product_venue_id_event_id_fkey | catalogue.event
DO $$ BEGIN IF to_regclass('catalogue.product') IS NOT NULL AND to_regclass('catalogue.event') IS NOT NULL AND NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'product_venue_id_event_id_fkey' AND conrelid = to_regclass('catalogue.product')) AND (SELECT atttypid FROM pg_attribute WHERE attrelid = to_regclass('catalogue.product') AND attname = 'venue_id') = (SELECT atttypid FROM pg_attribute WHERE attrelid = to_regclass('catalogue.event') AND attname = 'venue_id') AND (SELECT atttypid FROM pg_attribute WHERE attrelid = to_regclass('catalogue.product') AND attname = 'event_id') = (SELECT atttypid FROM pg_attribute WHERE attrelid = to_regclass('catalogue.event') AND attname = 'id') AND EXISTS (SELECT 1 FROM pg_index i WHERE i.indrelid = to_regclass('catalogue.event') AND i.indisunique AND i.indpred IS NULL AND i.indexprs IS NULL AND (SELECT array_agg(a.attname::text ORDER BY a.attname) FROM pg_attribute a WHERE a.attrelid = i.indrelid AND a.attnum = ANY (i.indkey)) = ARRAY['id', 'venue_id']) THEN ALTER TABLE catalogue.product ADD CONSTRAINT product_venue_id_event_id_fkey FOREIGN KEY (venue_id, event_id) REFERENCES catalogue.event(venue_id, id) NOT VALID; END IF; END $$;

-- tenancy.device_assignment | drop index | device_assignment_device_id_idx
DO $$ BEGIN IF to_regclass('tenancy.device_assignment_device_id_idx') IS NOT NULL THEN DROP INDEX tenancy.device_assignment_device_id_idx; END IF; END $$;

-- approvals.rule | drop index | rule_matrix_id_code_uniq
DO $$ BEGIN IF to_regclass('approvals.rule_matrix_id_code_uniq') IS NOT NULL THEN DROP INDEX approvals.rule_matrix_id_code_uniq; END IF; END $$;

INSERT INTO platform.schema_version (version, description, checksum)
VALUES ('V0119', 'after r1 (9cec72d), names the contracts use: 0 column rename(s), 1 key(s) added, renamed or dropped, 2 index(es) renamed or dropped', 'dc95083cc65bbdd6b7205b4f2ff6f6d2b1fd0854ff68ef26d43f2633500194ef')
ON CONFLICT (version) DO NOTHING;

-- ============================================================================
-- ROLLBACK
-- ============================================================================
-- Commented out so that applying this file never runs it: the rollback is run by removing the
-- leading `-- `, and is tested in CI against a restored snapshot (backend/MIGRATIONS.md).
-- CREATE UNIQUE INDEX IF NOT EXISTS rule_matrix_id_code_uniq ON approvals.rule (matrix_id, lower(code));
-- CREATE INDEX IF NOT EXISTS device_assignment_device_id_idx ON tenancy.device_assignment (device_id);
-- ALTER TABLE catalogue.product DROP CONSTRAINT IF EXISTS product_venue_id_event_id_fkey;
-- DELETE FROM platform.schema_version WHERE version = 'V0119';
