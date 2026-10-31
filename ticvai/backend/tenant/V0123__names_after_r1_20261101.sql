-- V0123 -- tenant database, after r1 (9cec72d) (20261101): the names the contracts use.
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

-- pricing.dynamic_price_rule | foreign key | dynamic_price_rule_channel_id_fkey | catalogue.sales_channel
DO $$ BEGIN IF to_regclass('pricing.dynamic_price_rule') IS NOT NULL AND to_regclass('catalogue.sales_channel') IS NOT NULL AND NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'dynamic_price_rule_channel_id_fkey' AND conrelid = to_regclass('pricing.dynamic_price_rule')) AND (SELECT atttypid FROM pg_attribute WHERE attrelid = to_regclass('pricing.dynamic_price_rule') AND attname = 'channel_id') = (SELECT atttypid FROM pg_attribute WHERE attrelid = to_regclass('catalogue.sales_channel') AND attname = 'id') AND EXISTS (SELECT 1 FROM pg_index i WHERE i.indrelid = to_regclass('catalogue.sales_channel') AND i.indisunique AND i.indpred IS NULL AND i.indexprs IS NULL AND (SELECT array_agg(a.attname::text ORDER BY a.attname) FROM pg_attribute a WHERE a.attrelid = i.indrelid AND a.attnum = ANY (i.indkey)) = ARRAY['id']) THEN ALTER TABLE pricing.dynamic_price_rule ADD CONSTRAINT dynamic_price_rule_channel_id_fkey FOREIGN KEY (channel_id) REFERENCES catalogue.sales_channel(id) NOT VALID; END IF; END $$;

INSERT INTO platform.schema_version (version, description, checksum)
VALUES ('V0123', 'after r1 (9cec72d), names the contracts use: 0 column rename(s), 1 key(s) added, renamed or dropped, 0 index(es) renamed or dropped', 'db06a328362cfa4448cb01d3ed1559888f71334e527fad115ed18887fe3bb124')
ON CONFLICT (version) DO NOTHING;

-- ============================================================================
-- ROLLBACK
-- ============================================================================
-- Commented out so that applying this file never runs it: the rollback is run by removing the
-- leading `-- `, and is tested in CI against a restored snapshot (backend/MIGRATIONS.md).
-- ALTER TABLE pricing.dynamic_price_rule DROP CONSTRAINT IF EXISTS dynamic_price_rule_channel_id_fkey;
-- DELETE FROM platform.schema_version WHERE version = 'V0123';
