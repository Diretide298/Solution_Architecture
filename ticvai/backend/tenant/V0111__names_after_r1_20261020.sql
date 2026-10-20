-- V0111 -- tenant database, after r1 (9cec72d) (20261020): the names the contracts use.
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
-- 0 column rename(s), 2 key(s) added, renamed or dropped, 0 index(es) renamed or dropped.

-- catalogue.bundle_application | foreign key | bundle_application_venue_id_fkey | platform.scope
DO $$ BEGIN IF to_regclass('catalogue.bundle_application') IS NOT NULL AND to_regclass('platform.scope') IS NOT NULL AND NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'bundle_application_venue_id_fkey' AND conrelid = to_regclass('catalogue.bundle_application')) AND (SELECT atttypid FROM pg_attribute WHERE attrelid = to_regclass('catalogue.bundle_application') AND attname = 'venue_id') = (SELECT atttypid FROM pg_attribute WHERE attrelid = to_regclass('platform.scope') AND attname = 'id') AND EXISTS (SELECT 1 FROM pg_index i WHERE i.indrelid = to_regclass('platform.scope') AND i.indisunique AND i.indpred IS NULL AND i.indexprs IS NULL AND (SELECT array_agg(a.attname::text ORDER BY a.attname) FROM pg_attribute a WHERE a.attrelid = i.indrelid AND a.attnum = ANY (i.indkey)) = ARRAY['id']) THEN ALTER TABLE catalogue.bundle_application ADD CONSTRAINT bundle_application_venue_id_fkey FOREIGN KEY (venue_id) REFERENCES platform.scope(id) NOT VALID; END IF; END $$;

-- catalogue.bundle_application | foreign key | bundle_application_venue_id_workstation_id_fkey | platform.workstation
DO $$ BEGIN IF to_regclass('catalogue.bundle_application') IS NOT NULL AND to_regclass('platform.workstation') IS NOT NULL AND NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'bundle_application_venue_id_workstation_id_fkey' AND conrelid = to_regclass('catalogue.bundle_application')) AND (SELECT atttypid FROM pg_attribute WHERE attrelid = to_regclass('catalogue.bundle_application') AND attname = 'venue_id') = (SELECT atttypid FROM pg_attribute WHERE attrelid = to_regclass('platform.workstation') AND attname = 'venue_id') AND (SELECT atttypid FROM pg_attribute WHERE attrelid = to_regclass('catalogue.bundle_application') AND attname = 'workstation_id') = (SELECT atttypid FROM pg_attribute WHERE attrelid = to_regclass('platform.workstation') AND attname = 'id') AND EXISTS (SELECT 1 FROM pg_index i WHERE i.indrelid = to_regclass('platform.workstation') AND i.indisunique AND i.indpred IS NULL AND i.indexprs IS NULL AND (SELECT array_agg(a.attname::text ORDER BY a.attname) FROM pg_attribute a WHERE a.attrelid = i.indrelid AND a.attnum = ANY (i.indkey)) = ARRAY['id', 'venue_id']) THEN ALTER TABLE catalogue.bundle_application ADD CONSTRAINT bundle_application_venue_id_workstation_id_fkey FOREIGN KEY (venue_id, workstation_id) REFERENCES platform.workstation(venue_id, id) NOT VALID; END IF; END $$;

INSERT INTO platform.schema_version (version, description, checksum)
VALUES ('V0111', 'after r1 (9cec72d), names the contracts use: 0 column rename(s), 2 key(s) added, renamed or dropped, 0 index(es) renamed or dropped', 'a1ee8f514f1213d98c5bc727e1cac117c3c617ed588446e223fc8e68ca95e482')
ON CONFLICT (version) DO NOTHING;

-- ============================================================================
-- ROLLBACK
-- ============================================================================
-- Commented out so that applying this file never runs it: the rollback is run by removing the
-- leading `-- `, and is tested in CI against a restored snapshot (backend/MIGRATIONS.md).
-- ALTER TABLE catalogue.bundle_application DROP CONSTRAINT IF EXISTS bundle_application_venue_id_workstation_id_fkey;
-- ALTER TABLE catalogue.bundle_application DROP CONSTRAINT IF EXISTS bundle_application_venue_id_fkey;
-- DELETE FROM platform.schema_version WHERE version = 'V0111';
