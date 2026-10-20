-- V0112 -- control database, after r1 (9cec72d) (20261021).
-- **Written by tools/derive-ddl.py in frozen mode. Do not edit after merge; a mistake is a new migration.**
--
-- The baseline under backend/control/ is frozen at r1 (9cec72d), so the change to the schema reference
-- since then is written here instead: additive only. Changes that are not additive (drops, renames,
-- type changes) are not generated; they are listed for a person in handoff/migration-review.md.
-- 0 table(s), 3 column(s), 0 index(es), 0 other statement(s).

ALTER TABLE control.licence_add_on ADD COLUMN IF NOT EXISTS removed_at timestamptz;

ALTER TABLE control.licence_add_on ADD COLUMN IF NOT EXISTS removed_by_principal_id uuid;

ALTER TABLE control.licence_add_on ADD COLUMN IF NOT EXISTS removal_reason text CONSTRAINT licence_add_on_removal_reason_chk CHECK (char_length(removal_reason) <= 500);

INSERT INTO platform.schema_version (version, description, checksum)
VALUES ('V0112', 'after r1 (9cec72d): 0 table(s), 3 column(s), 0 index(es), 0 other statement(s)', '310c31c73fb2945cb444b573ae31b98104b12ab347044b0e843240b54a29b79d')
ON CONFLICT (version) DO NOTHING;

-- ============================================================================
-- ROLLBACK
-- ============================================================================
-- Commented out so that applying this file never runs it: the rollback is run by removing the
-- leading `-- `, and is tested in CI against a restored snapshot (backend/MIGRATIONS.md).
-- ALTER TABLE control.licence_add_on DROP COLUMN IF EXISTS removal_reason;
-- ALTER TABLE control.licence_add_on DROP COLUMN IF EXISTS removed_by_principal_id;
-- ALTER TABLE control.licence_add_on DROP COLUMN IF EXISTS removed_at;
-- DELETE FROM platform.schema_version WHERE version = 'V0112';
