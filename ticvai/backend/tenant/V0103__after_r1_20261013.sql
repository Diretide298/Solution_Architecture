-- V0103 -- tenant database, after r1 (9cec72d) (20261013).
-- **Written by tools/derive-ddl.py in frozen mode. Do not edit after merge; a mistake is a new migration.**
--
-- The baseline under backend/tenant/ is frozen at r1 (9cec72d), so the change to the schema reference
-- since then is written here instead: additive only. Changes that are not additive (drops, renames,
-- type changes) are not generated; they are listed for a person in handoff/migration-review.md.
-- 0 table(s), 0 column(s), 1 index(es), 0 other statement(s).

CREATE INDEX IF NOT EXISTS production_plan_line_item_id_idx ON fnb.production_plan_line (item_id);

INSERT INTO platform.schema_version (version, description, checksum)
VALUES ('V0103', 'after r1 (9cec72d): 0 table(s), 0 column(s), 1 index(es), 0 other statement(s)', '49cda78210da28ac3805d97aa6fda9a37dd3895166dce4189fee6a1559bd02c3')
ON CONFLICT (version) DO NOTHING;

-- ============================================================================
-- ROLLBACK
-- ============================================================================
-- Commented out so that applying this file never runs it: the rollback is run by removing the
-- leading `-- `, and is tested in CI against a restored snapshot (backend/MIGRATIONS.md).
-- DROP INDEX IF EXISTS fnb.production_plan_line_item_id_idx;
-- DELETE FROM platform.schema_version WHERE version = 'V0103';
