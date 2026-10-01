-- V0100 -- control database, after r1 (a1ba956) (20261002).
-- **Written by tools/derive-ddl.py in frozen mode. Do not edit after merge; a mistake is a new migration.**
--
-- The baseline under backend/control/ is frozen at r1 (a1ba956), so the change to the schema reference
-- since then is written here instead: additive only. Changes that are not additive (drops, renames,
-- type changes) are not generated; they are listed for a person in handoff/migration-review.md.
-- 0 table(s), 0 column(s), 2 index(es), 0 other statement(s).

CREATE INDEX IF NOT EXISTS outbox_republish_requested_by_principal_id_idx ON control.outbox_republish (requested_by_principal_id);

CREATE INDEX IF NOT EXISTS outbox_republish_tenant_id_idx ON control.outbox_republish (tenant_id);

INSERT INTO platform.schema_version (version, description, checksum)
VALUES ('V0100', 'after r1 (a1ba956): 0 table(s), 0 column(s), 2 index(es), 0 other statement(s)', 'f340e55b41b38898f33f6d7cc1e34a66088c3654001fdd777ef5c2b9a441381d')
ON CONFLICT (version) DO NOTHING;

-- ============================================================================
-- ROLLBACK
-- ============================================================================
-- Commented out so that applying this file never runs it: the rollback is run by removing the
-- leading `-- `, and is tested in CI against a restored snapshot (backend/MIGRATIONS.md).
-- DROP INDEX IF EXISTS control.outbox_republish_tenant_id_idx;
-- DROP INDEX IF EXISTS control.outbox_republish_requested_by_principal_id_idx;
-- DELETE FROM platform.schema_version WHERE version = 'V0100';
