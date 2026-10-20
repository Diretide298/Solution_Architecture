-- V0109 -- control database, after r1 (9cec72d) (20261020): the names the contracts use.
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
-- 0 column rename(s), 2 key(s) added, renamed or dropped, 1 index(es) renamed or dropped.

-- control.tenant | foreign key | tenant_plan_id_fkey | control.plan
DO $$ BEGIN IF to_regclass('control.tenant') IS NOT NULL AND to_regclass('control.plan') IS NOT NULL AND NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'tenant_plan_id_fkey' AND conrelid = to_regclass('control.tenant')) AND (SELECT atttypid FROM pg_attribute WHERE attrelid = to_regclass('control.tenant') AND attname = 'plan_id') = (SELECT atttypid FROM pg_attribute WHERE attrelid = to_regclass('control.plan') AND attname = 'id') AND (SELECT atttypid FROM pg_attribute WHERE attrelid = to_regclass('control.tenant') AND attname = 'plan_version') = (SELECT atttypid FROM pg_attribute WHERE attrelid = to_regclass('control.plan') AND attname = 'version') AND EXISTS (SELECT 1 FROM pg_index i WHERE i.indrelid = to_regclass('control.plan') AND i.indisunique AND i.indpred IS NULL AND i.indexprs IS NULL AND (SELECT array_agg(a.attname::text ORDER BY a.attname) FROM pg_attribute a WHERE a.attrelid = i.indrelid AND a.attnum = ANY (i.indkey)) = ARRAY['id', 'version']) THEN ALTER TABLE control.tenant ADD CONSTRAINT tenant_plan_id_fkey FOREIGN KEY (plan_id, plan_version) REFERENCES control.plan(id, version) NOT VALID; END IF; END $$;

-- control.tenant | foreign key | tenant_subscription_id_fkey | control.contract
DO $$ BEGIN IF to_regclass('control.tenant') IS NOT NULL AND to_regclass('control.contract') IS NOT NULL AND NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'tenant_subscription_id_fkey' AND conrelid = to_regclass('control.tenant')) AND (SELECT atttypid FROM pg_attribute WHERE attrelid = to_regclass('control.tenant') AND attname = 'subscription_id') = (SELECT atttypid FROM pg_attribute WHERE attrelid = to_regclass('control.contract') AND attname = 'id') AND EXISTS (SELECT 1 FROM pg_index i WHERE i.indrelid = to_regclass('control.contract') AND i.indisunique AND i.indpred IS NULL AND i.indexprs IS NULL AND (SELECT array_agg(a.attname::text ORDER BY a.attname) FROM pg_attribute a WHERE a.attrelid = i.indrelid AND a.attnum = ANY (i.indkey)) = ARRAY['id']) THEN ALTER TABLE control.tenant ADD CONSTRAINT tenant_subscription_id_fkey FOREIGN KEY (subscription_id) REFERENCES control.contract(id) NOT VALID; END IF; END $$;

-- control.tenant_domain | drop index | tenant_domain_tenant_id_hostname_uniq
DO $$ BEGIN IF to_regclass('control.tenant_domain_tenant_id_hostname_uniq') IS NOT NULL THEN DROP INDEX control.tenant_domain_tenant_id_hostname_uniq; END IF; END $$;

INSERT INTO platform.schema_version (version, description, checksum)
VALUES ('V0109', 'after r1 (9cec72d), names the contracts use: 0 column rename(s), 2 key(s) added, renamed or dropped, 1 index(es) renamed or dropped', '6af1cea09e631829906b8086b349fc5d0e0b05bd2eb93011de83ca0a03f75851')
ON CONFLICT (version) DO NOTHING;

-- ============================================================================
-- ROLLBACK
-- ============================================================================
-- Commented out so that applying this file never runs it: the rollback is run by removing the
-- leading `-- `, and is tested in CI against a restored snapshot (backend/MIGRATIONS.md).
-- CREATE UNIQUE INDEX IF NOT EXISTS tenant_domain_tenant_id_hostname_uniq ON control.tenant_domain (tenant_id, lower(hostname));
-- ALTER TABLE control.tenant DROP CONSTRAINT IF EXISTS tenant_subscription_id_fkey;
-- ALTER TABLE control.tenant DROP CONSTRAINT IF EXISTS tenant_plan_id_fkey;
-- DELETE FROM platform.schema_version WHERE version = 'V0109';
