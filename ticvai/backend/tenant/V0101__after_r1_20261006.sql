-- V0101 -- tenant database, after r1 (9cec72d) (20261006).
-- **Written by tools/derive-ddl.py in frozen mode. Do not edit after merge; a mistake is a new migration.**
--
-- The baseline under backend/tenant/ is frozen at r1 (9cec72d), so the change to the schema reference
-- since then is written here instead: additive only. Changes that are not additive (drops, renames,
-- type changes) are not generated; they are listed for a person in handoff/migration-review.md.
-- 0 table(s), 3 column(s), 10 index(es), 0 other statement(s).

ALTER TABLE catalogue.performance ADD COLUMN IF NOT EXISTS minutes_on_screen integer DEFAULT 0;

ALTER TABLE catalogue.product ADD COLUMN IF NOT EXISTS name_localised jsonb;

ALTER TABLE catalogue.product ADD COLUMN IF NOT EXISTS description_localised jsonb;

CREATE INDEX IF NOT EXISTS kiosk_assignment_assigned_by_principal_id_idx ON whitelabel.kiosk_assignment (assigned_by_principal_id);

CREATE INDEX IF NOT EXISTS kiosk_assignment_kiosk_config_id_idx ON whitelabel.kiosk_assignment (kiosk_config_id);

CREATE INDEX IF NOT EXISTS kiosk_assignment_venue_id_idx ON whitelabel.kiosk_assignment (venue_id);

CREATE INDEX IF NOT EXISTS kiosk_assignment_workstation_id_idx ON whitelabel.kiosk_assignment (workstation_id);

CREATE INDEX IF NOT EXISTS kiosk_config_venue_id_idx ON whitelabel.kiosk_config (venue_id);

CREATE INDEX IF NOT EXISTS kiosk_config_attract_slide_kiosk_config_id_idx ON whitelabel.kiosk_config_attract_slide (kiosk_config_id);

CREATE INDEX IF NOT EXISTS kiosk_config_start_tile_kiosk_config_id_idx ON whitelabel.kiosk_config_start_tile (kiosk_config_id);

CREATE INDEX IF NOT EXISTS kiosk_config_version_kiosk_config_id_idx ON whitelabel.kiosk_config_version (kiosk_config_id);

CREATE INDEX IF NOT EXISTS kiosk_config_version_published_by_principal_id_idx ON whitelabel.kiosk_config_version (published_by_principal_id);

CREATE UNIQUE INDEX IF NOT EXISTS promotion_code_uniq ON promotions.promotion (code);

INSERT INTO platform.schema_version (version, description, checksum)
VALUES ('V0101', 'after r1 (9cec72d): 0 table(s), 3 column(s), 10 index(es), 0 other statement(s)', '8b891d806cb319ebaeeffd3af0b1362402ce940e4fc417fea2b72a99538edbe0')
ON CONFLICT (version) DO NOTHING;

-- ============================================================================
-- ROLLBACK
-- ============================================================================
-- Commented out so that applying this file never runs it: the rollback is run by removing the
-- leading `-- `, and is tested in CI against a restored snapshot (backend/MIGRATIONS.md).
-- DROP INDEX IF EXISTS promotions.promotion_code_uniq;
-- DROP INDEX IF EXISTS whitelabel.kiosk_config_version_published_by_principal_id_idx;
-- DROP INDEX IF EXISTS whitelabel.kiosk_config_version_kiosk_config_id_idx;
-- DROP INDEX IF EXISTS whitelabel.kiosk_config_start_tile_kiosk_config_id_idx;
-- DROP INDEX IF EXISTS whitelabel.kiosk_config_attract_slide_kiosk_config_id_idx;
-- DROP INDEX IF EXISTS whitelabel.kiosk_config_venue_id_idx;
-- DROP INDEX IF EXISTS whitelabel.kiosk_assignment_workstation_id_idx;
-- DROP INDEX IF EXISTS whitelabel.kiosk_assignment_venue_id_idx;
-- DROP INDEX IF EXISTS whitelabel.kiosk_assignment_kiosk_config_id_idx;
-- DROP INDEX IF EXISTS whitelabel.kiosk_assignment_assigned_by_principal_id_idx;
-- ALTER TABLE catalogue.product DROP COLUMN IF EXISTS description_localised;
-- ALTER TABLE catalogue.product DROP COLUMN IF EXISTS name_localised;
-- ALTER TABLE catalogue.performance DROP COLUMN IF EXISTS minutes_on_screen;
-- DELETE FROM platform.schema_version WHERE version = 'V0101';
