-- V0113 -- tenant database, after r1 (9cec72d) (20261021).
-- **Written by tools/derive-ddl.py in frozen mode. Do not edit after merge; a mistake is a new migration.**
--
-- The baseline under backend/tenant/ is frozen at r1 (9cec72d), so the change to the schema reference
-- since then is written here instead: additive only. Changes that are not additive (drops, renames,
-- type changes) are not generated; they are listed for a person in handoff/migration-review.md.
-- Every statement that needs a table is a guarded block (CHG-R9MIG-002): it does nothing where its table
-- or a column it names is not there yet, so the file applies as one transaction, twice, on any database;
-- the migration that creates such a table later copies the block. A table's policy change is one block.
-- A table the contract says takes no scope (x-ticvai-scope: none) loses the scope_path, its index and its
-- scope policy a forward migration gave it, in one block guarded on the column (CHG-R9MIG-001).
-- 0 table(s), 0 column(s), 0 index(es), 1 other statement(s), 1 row-level security polic(ies) re-applied.

-- platform.outbox_sequence | scope removed | scope_path (x-ticvai-scope: none)
DO $$ BEGIN IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'platform' AND table_name = 'outbox_sequence' AND column_name = 'scope_path') THEN
PERFORM platform.drop_rls_policies('platform.outbox_sequence'::regclass);
DROP INDEX IF EXISTS platform.outbox_sequence_scope_path_idx;
ALTER TABLE platform.outbox_sequence DROP COLUMN IF EXISTS scope_path;
PERFORM platform.apply_split_rls('platform.outbox_sequence'::regclass, 'cardinality(platform.current_scope_paths()) > 0', 'cardinality(platform.current_scope_paths()) > 0');
DROP POLICY IF EXISTS outbox_sequence_delete ON platform.outbox_sequence;
END IF; END $$;

INSERT INTO platform.schema_version (version, description, checksum)
VALUES ('V0113', 'after r1 (9cec72d): 0 table(s), 0 column(s), 0 index(es), 1 other statement(s), 1 row-level security polic(ies) re-applied', '540a00ea3537b877d82702752ca8860580a30428c7c55f53ef2f7a45bb211a46')
ON CONFLICT (version) DO NOTHING;

-- ============================================================================
-- ROLLBACK
-- ============================================================================
-- Commented out so that applying this file never runs it: the rollback is run by removing the
-- leading `-- `, and is tested in CI against a restored snapshot (backend/MIGRATIONS.md).
-- ALTER TABLE platform.outbox_sequence ADD COLUMN IF NOT EXISTS scope_path ltree; CREATE INDEX IF NOT EXISTS outbox_sequence_scope_path_idx ON platform.outbox_sequence USING gist (scope_path); SELECT platform.drop_rls_policies('platform.outbox_sequence'::regclass); SELECT platform.apply_scope_rls('platform.outbox_sequence'::regclass); (each row's scope_path is gone: backfill it, then ALTER COLUMN scope_path SET NOT NULL)
-- DELETE FROM platform.schema_version WHERE version = 'V0113';
