-- V0112 -- control database, after r1 (9cec72d) (20261021).
-- **Written by tools/derive-ddl.py in frozen mode. Do not edit after merge; a mistake is a new migration.**
--
-- The baseline under backend/control/ is frozen at r1 (9cec72d), so the change to the schema reference
-- since then is written here instead: additive only. Changes that are not additive (drops, renames,
-- type changes) are not generated; they are listed for a person in handoff/migration-review.md.
-- 0 table(s), 3 column(s), 1 index(es), 0 other statement(s).

ALTER TABLE control.licence_add_on ADD COLUMN IF NOT EXISTS removed_at timestamptz;

ALTER TABLE control.licence_add_on ADD COLUMN IF NOT EXISTS removed_by_principal_id uuid;

ALTER TABLE control.licence_add_on ADD COLUMN IF NOT EXISTS removal_reason text CONSTRAINT licence_add_on_removal_reason_chk CHECK (char_length(removal_reason) <= 500);

CREATE INDEX IF NOT EXISTS licence_add_on_removed_by_principal_id_idx ON control.licence_add_on (removed_by_principal_id);

INSERT INTO platform.schema_version (version, description, checksum)
VALUES ('V0112', 'after r1 (9cec72d): 0 table(s), 3 column(s), 1 index(es), 0 other statement(s)', '4d1a3518b64e272c97fa08a042568f5af9bc63a5f069232af3bf839796212425')
ON CONFLICT (version) DO NOTHING;

-- ============================================================================
-- ROLLBACK
-- ============================================================================
-- Commented out so that applying this file never runs it: the rollback is run by removing the
-- leading `-- `, and is tested in CI against a restored snapshot (backend/MIGRATIONS.md).
-- DROP INDEX IF EXISTS control.licence_add_on_removed_by_principal_id_idx;
-- ALTER TABLE control.licence_add_on DROP COLUMN IF EXISTS removal_reason;
-- ALTER TABLE control.licence_add_on DROP COLUMN IF EXISTS removed_by_principal_id;
-- ALTER TABLE control.licence_add_on DROP COLUMN IF EXISTS removed_at;
-- DELETE FROM platform.schema_version WHERE version = 'V0112';
