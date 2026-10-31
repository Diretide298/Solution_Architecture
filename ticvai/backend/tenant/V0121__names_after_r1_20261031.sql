-- V0121 -- tenant database, after r1 (9cec72d) (20261031): the names the contracts use.
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
-- A foreign key the schema reference has changed since a forward migration added it (its referenced table or
-- its columns) is put in the reference's form: where the constraint of that name is any other key, it is
-- dropped and added again NOT VALID in one ALTER TABLE; where it is already the reference's key, the block does
-- nothing (CHG-R9KEY-001).
-- 0 column rename(s), 3 key(s) added, renamed or dropped, 2 index(es) renamed or dropped.

-- marketing.form_definition_field | foreign key | form_definition_field_form_id_fkey | marketing.form_definition
DO $$ BEGIN IF to_regclass('marketing.form_definition_field') IS NOT NULL AND to_regclass('marketing.form_definition') IS NOT NULL AND NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'form_definition_field_form_id_fkey' AND conrelid = to_regclass('marketing.form_definition_field')) AND (SELECT atttypid FROM pg_attribute WHERE attrelid = to_regclass('marketing.form_definition_field') AND attname = 'form_id') = (SELECT atttypid FROM pg_attribute WHERE attrelid = to_regclass('marketing.form_definition') AND attname = 'id') AND (SELECT atttypid FROM pg_attribute WHERE attrelid = to_regclass('marketing.form_definition_field') AND attname = 'form_version') = (SELECT atttypid FROM pg_attribute WHERE attrelid = to_regclass('marketing.form_definition') AND attname = 'version') AND EXISTS (SELECT 1 FROM pg_index i WHERE i.indrelid = to_regclass('marketing.form_definition') AND i.indisunique AND i.indpred IS NULL AND i.indexprs IS NULL AND (SELECT array_agg(a.attname::text ORDER BY a.attname) FROM pg_attribute a WHERE a.attrelid = i.indrelid AND a.attnum = ANY (i.indkey)) = ARRAY['id', 'version']) THEN ALTER TABLE marketing.form_definition_field ADD CONSTRAINT form_definition_field_form_id_fkey FOREIGN KEY (form_id, form_version) REFERENCES marketing.form_definition(id, version) NOT VALID; END IF; END $$;

-- marketing.waiver_requirement | change foreign key | waiver_requirement_form_definition_id_fkey | marketing.form_definition
DO $$ BEGIN IF to_regclass('marketing.waiver_requirement') IS NOT NULL AND to_regclass('marketing.form_definition') IS NOT NULL AND (SELECT atttypid FROM pg_attribute WHERE attrelid = to_regclass('marketing.waiver_requirement') AND attname = 'form_definition_id') = (SELECT atttypid FROM pg_attribute WHERE attrelid = to_regclass('marketing.form_definition') AND attname = 'id') AND (SELECT atttypid FROM pg_attribute WHERE attrelid = to_regclass('marketing.waiver_requirement') AND attname = 'form_version') = (SELECT atttypid FROM pg_attribute WHERE attrelid = to_regclass('marketing.form_definition') AND attname = 'version') AND EXISTS (SELECT 1 FROM pg_index i WHERE i.indrelid = to_regclass('marketing.form_definition') AND i.indisunique AND i.indpred IS NULL AND i.indexprs IS NULL AND (SELECT array_agg(a.attname::text ORDER BY a.attname) FROM pg_attribute a WHERE a.attrelid = i.indrelid AND a.attnum = ANY (i.indkey)) = ARRAY['id', 'version']) AND NOT EXISTS (SELECT 1 FROM pg_constraint c WHERE c.conname = 'waiver_requirement_form_definition_id_fkey' AND c.conrelid = to_regclass('marketing.waiver_requirement') AND c.contype = 'f' AND c.confrelid = to_regclass('marketing.form_definition') AND (SELECT array_agg(a.attname::text ORDER BY k.n) FROM unnest(c.conkey) WITH ORDINALITY k(attnum, n) JOIN pg_attribute a ON a.attrelid = c.conrelid AND a.attnum = k.attnum) = ARRAY['form_definition_id', 'form_version'] AND (SELECT array_agg(a.attname::text ORDER BY k.n) FROM unnest(c.confkey) WITH ORDINALITY k(attnum, n) JOIN pg_attribute a ON a.attrelid = c.confrelid AND a.attnum = k.attnum) = ARRAY['id', 'version']) THEN ALTER TABLE marketing.waiver_requirement DROP CONSTRAINT IF EXISTS waiver_requirement_form_definition_id_fkey, ADD CONSTRAINT waiver_requirement_form_definition_id_fkey FOREIGN KEY (form_definition_id, form_version) REFERENCES marketing.form_definition(id, version) NOT VALID; END IF; END $$;

-- marketing.waiver_signature | change foreign key | waiver_signature_form_definition_id_fkey | marketing.form_definition
DO $$ BEGIN IF to_regclass('marketing.waiver_signature') IS NOT NULL AND to_regclass('marketing.form_definition') IS NOT NULL AND (SELECT atttypid FROM pg_attribute WHERE attrelid = to_regclass('marketing.waiver_signature') AND attname = 'form_definition_id') = (SELECT atttypid FROM pg_attribute WHERE attrelid = to_regclass('marketing.form_definition') AND attname = 'id') AND (SELECT atttypid FROM pg_attribute WHERE attrelid = to_regclass('marketing.waiver_signature') AND attname = 'form_version') = (SELECT atttypid FROM pg_attribute WHERE attrelid = to_regclass('marketing.form_definition') AND attname = 'version') AND EXISTS (SELECT 1 FROM pg_index i WHERE i.indrelid = to_regclass('marketing.form_definition') AND i.indisunique AND i.indpred IS NULL AND i.indexprs IS NULL AND (SELECT array_agg(a.attname::text ORDER BY a.attname) FROM pg_attribute a WHERE a.attrelid = i.indrelid AND a.attnum = ANY (i.indkey)) = ARRAY['id', 'version']) AND NOT EXISTS (SELECT 1 FROM pg_constraint c WHERE c.conname = 'waiver_signature_form_definition_id_fkey' AND c.conrelid = to_regclass('marketing.waiver_signature') AND c.contype = 'f' AND c.confrelid = to_regclass('marketing.form_definition') AND (SELECT array_agg(a.attname::text ORDER BY k.n) FROM unnest(c.conkey) WITH ORDINALITY k(attnum, n) JOIN pg_attribute a ON a.attrelid = c.conrelid AND a.attnum = k.attnum) = ARRAY['form_definition_id', 'form_version'] AND (SELECT array_agg(a.attname::text ORDER BY k.n) FROM unnest(c.confkey) WITH ORDINALITY k(attnum, n) JOIN pg_attribute a ON a.attrelid = c.confrelid AND a.attnum = k.attnum) = ARRAY['id', 'version']) THEN ALTER TABLE marketing.waiver_signature DROP CONSTRAINT IF EXISTS waiver_signature_form_definition_id_fkey, ADD CONSTRAINT waiver_signature_form_definition_id_fkey FOREIGN KEY (form_definition_id, form_version) REFERENCES marketing.form_definition(id, version) NOT VALID; END IF; END $$;

-- marketing.waiver_requirement | drop index | waiver_requirement_form_definition_id_idx
DO $$ BEGIN IF to_regclass('marketing.waiver_requirement_form_definition_id_idx') IS NOT NULL THEN DROP INDEX marketing.waiver_requirement_form_definition_id_idx; END IF; END $$;

-- marketing.waiver_signature | drop index | waiver_signature_form_definition_id_idx
DO $$ BEGIN IF to_regclass('marketing.waiver_signature_form_definition_id_idx') IS NOT NULL THEN DROP INDEX marketing.waiver_signature_form_definition_id_idx; END IF; END $$;

INSERT INTO platform.schema_version (version, description, checksum)
VALUES ('V0121', 'after r1 (9cec72d), names the contracts use: 0 column rename(s), 3 key(s) added, renamed or dropped, 2 index(es) renamed or dropped', '1221278568f87770dfdaa64da89d6de0b237aa016d984115f46a0ac16e4eee05')
ON CONFLICT (version) DO NOTHING;

-- ============================================================================
-- ROLLBACK
-- ============================================================================
-- Commented out so that applying this file never runs it: the rollback is run by removing the
-- leading `-- `, and is tested in CI against a restored snapshot (backend/MIGRATIONS.md).
-- CREATE INDEX IF NOT EXISTS waiver_signature_form_definition_id_idx ON marketing.waiver_signature (form_definition_id);
-- CREATE INDEX IF NOT EXISTS waiver_requirement_form_definition_id_idx ON marketing.waiver_requirement (form_definition_id);
-- ALTER TABLE marketing.waiver_signature DROP CONSTRAINT IF EXISTS waiver_signature_form_definition_id_fkey; ALTER TABLE marketing.waiver_signature ADD CONSTRAINT waiver_signature_form_definition_id_fkey FOREIGN KEY (form_definition_id) REFERENCES marketing.form_definition(id) NOT VALID;
-- ALTER TABLE marketing.waiver_requirement DROP CONSTRAINT IF EXISTS waiver_requirement_form_definition_id_fkey; ALTER TABLE marketing.waiver_requirement ADD CONSTRAINT waiver_requirement_form_definition_id_fkey FOREIGN KEY (form_definition_id) REFERENCES marketing.form_definition(id) NOT VALID;
-- ALTER TABLE marketing.form_definition_field DROP CONSTRAINT IF EXISTS form_definition_field_form_id_fkey;
-- DELETE FROM platform.schema_version WHERE version = 'V0121';
