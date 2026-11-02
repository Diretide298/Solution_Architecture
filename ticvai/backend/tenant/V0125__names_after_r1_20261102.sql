-- V0125 -- tenant database, after r1 (9cec72d) (20261102): the names the contracts use.
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
-- 0 column rename(s), 1 key(s) added, renamed or dropped, 0 index(es) renamed or dropped.

-- marketing.privacy_change_set | foreign key | privacy_change_set_approval_request_id_fkey | approvals.request
DO $$ BEGIN IF to_regclass('marketing.privacy_change_set') IS NOT NULL AND to_regclass('approvals.request') IS NOT NULL AND NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'privacy_change_set_approval_request_id_fkey' AND conrelid = to_regclass('marketing.privacy_change_set')) AND (SELECT atttypid FROM pg_attribute WHERE attrelid = to_regclass('marketing.privacy_change_set') AND attname = 'approval_request_id') = (SELECT atttypid FROM pg_attribute WHERE attrelid = to_regclass('approvals.request') AND attname = 'id') AND EXISTS (SELECT 1 FROM pg_index i WHERE i.indrelid = to_regclass('approvals.request') AND i.indisunique AND i.indpred IS NULL AND i.indexprs IS NULL AND (SELECT array_agg(a.attname::text ORDER BY a.attname) FROM pg_attribute a WHERE a.attrelid = i.indrelid AND a.attnum = ANY (i.indkey)) = ARRAY['id']) THEN ALTER TABLE marketing.privacy_change_set ADD CONSTRAINT privacy_change_set_approval_request_id_fkey FOREIGN KEY (approval_request_id) REFERENCES approvals.request(id) NOT VALID; END IF; END $$;

INSERT INTO platform.schema_version (version, description, checksum)
VALUES ('V0125', 'after r1 (9cec72d), names the contracts use: 0 column rename(s), 1 key(s) added, renamed or dropped, 0 index(es) renamed or dropped', 'd57f3c8a51ce90eac35a6ee024e9200fb1eb741bb13734f71fe1805c7b38a371')
ON CONFLICT (version) DO NOTHING;

-- ============================================================================
-- ROLLBACK
-- ============================================================================
-- Commented out so that applying this file never runs it: the rollback is run by removing the
-- leading `-- `, and is tested in CI against a restored snapshot (backend/MIGRATIONS.md).
-- ALTER TABLE marketing.privacy_change_set DROP CONSTRAINT IF EXISTS privacy_change_set_approval_request_id_fkey;
-- DELETE FROM platform.schema_version WHERE version = 'V0125';
