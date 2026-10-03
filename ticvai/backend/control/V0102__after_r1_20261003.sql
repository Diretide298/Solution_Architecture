-- V0102 -- control database, after r1 (a1ba956) (20261003).
-- **Written by tools/derive-ddl.py in frozen mode. Do not edit after merge; a mistake is a new migration.**
--
-- The baseline under backend/control/ is frozen at r1 (a1ba956), so the change to the schema reference
-- since then is written here instead: additive only. Changes that are not additive (drops, renames,
-- type changes) are not generated; they are listed for a person in handoff/migration-review.md.
-- 0 table(s), 0 column(s), 4 index(es), 0 other statement(s).

CREATE INDEX IF NOT EXISTS billing_entity_tenant_id_idx ON control.billing_entity (tenant_id);

CREATE INDEX IF NOT EXISTS config_package_tenant_id_idx ON control.config_package (tenant_id);

CREATE INDEX IF NOT EXISTS config_package_application_previous_package_id_idx ON control.config_package_application (previous_package_id);

CREATE INDEX IF NOT EXISTS config_package_diff_package_id_idx ON control.config_package_diff (package_id);

INSERT INTO platform.schema_version (version, description, checksum)
VALUES ('V0102', 'after r1 (a1ba956): 0 table(s), 0 column(s), 4 index(es), 0 other statement(s)', 'fb0c9873ea3618ffbccc7cb3cfbe3f1fc5fd26810b59af60997f49311494118a')
ON CONFLICT (version) DO NOTHING;

-- ============================================================================
-- ROLLBACK
-- ============================================================================
-- Commented out so that applying this file never runs it: the rollback is run by removing the
-- leading `-- `, and is tested in CI against a restored snapshot (backend/MIGRATIONS.md).
-- DROP INDEX IF EXISTS control.config_package_diff_package_id_idx;
-- DROP INDEX IF EXISTS control.config_package_application_previous_package_id_idx;
-- DROP INDEX IF EXISTS control.config_package_tenant_id_idx;
-- DROP INDEX IF EXISTS control.billing_entity_tenant_id_idx;
-- DELETE FROM platform.schema_version WHERE version = 'V0102';
