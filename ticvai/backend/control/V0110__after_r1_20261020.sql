-- V0110 -- control database, after r1 (9cec72d) (20261020).
-- **Written by tools/derive-ddl.py in frozen mode. Do not edit after merge; a mistake is a new migration.**
--
-- The baseline under backend/control/ is frozen at r1 (9cec72d), so the change to the schema reference
-- since then is written here instead: additive only. Changes that are not additive (drops, renames,
-- type changes) are not generated; they are listed for a person in handoff/migration-review.md.
-- 0 table(s), 0 column(s), 1 index(es), 0 other statement(s).

CREATE INDEX IF NOT EXISTS onboarding_application_requested_plan_id_idx ON control.onboarding_application (requested_plan_id);

INSERT INTO platform.schema_version (version, description, checksum)
VALUES ('V0110', 'after r1 (9cec72d): 0 table(s), 0 column(s), 1 index(es), 0 other statement(s)', '2bc597c62fc601ccd656ca6ba488dba6dbe9f860e0c7737e3a2b135b836ecc15')
ON CONFLICT (version) DO NOTHING;

-- ============================================================================
-- ROLLBACK
-- ============================================================================
-- Commented out so that applying this file never runs it: the rollback is run by removing the
-- leading `-- `, and is tested in CI against a restored snapshot (backend/MIGRATIONS.md).
-- DROP INDEX IF EXISTS control.onboarding_application_requested_plan_id_idx;
-- DELETE FROM platform.schema_version WHERE version = 'V0110';
