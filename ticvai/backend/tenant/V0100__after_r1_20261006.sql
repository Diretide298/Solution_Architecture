-- V0100 -- tenant database, after r1 (9cec72d) (20261006).
-- **Written by tools/derive-ddl.py in frozen mode. Do not edit after merge; a mistake is a new migration.**
--
-- The baseline under backend/tenant/ is frozen at r1 (9cec72d), so the change to the schema reference
-- since then is written here instead: additive only. Changes that are not additive (drops, renames,
-- type changes) are not generated; they are listed for a person in handoff/migration-review.md.
-- 5 table(s), 0 column(s), 6 index(es), 5 other statement(s).

CREATE TABLE IF NOT EXISTS whitelabel.kiosk_assignment (
    id                                uuid PRIMARY KEY NOT NULL,
    workstation_id                    uuid,
    venue_id                          uuid,
    kiosk_config_id                   uuid,
    assigned_at                       timestamptz,
    assigned_by_principal_id          uuid,
    scope_path                        ltree NOT NULL
);

CREATE TABLE IF NOT EXISTS whitelabel.kiosk_config (
    id                                uuid PRIMARY KEY NOT NULL,
    venue_id                          uuid,
    name                              text NOT NULL CONSTRAINT kiosk_config_name_chk CHECK (char_length(name) <= 80),
    is_default                        boolean DEFAULT false,
    placement_kind                    text CONSTRAINT kiosk_config_placement_kind_chk CHECK (placement_kind IN ('venue', 'accessPoint', 'operatingArea', 'outlet')),
    placement_id                      uuid,
    display                           jsonb,
    attract_loop                      jsonb,
    start_screen                      jsonb,
    header_footer                     jsonb,
    journey                           jsonb,
    "session"                         jsonb,
    payment_output                    jsonb,
    languages                         jsonb,
    messages                          jsonb,
    opening_hours                     jsonb,
    out_of_service                    jsonb,
    enabled_functions                 text[],
    assigned_kiosk_count              integer,
    published_version                 integer,
    has_unpublished_changes           boolean,
    scope_path                        ltree NOT NULL,
    updated_at                        timestamptz
);

CREATE TABLE IF NOT EXISTS whitelabel.kiosk_config_attract_slide (
    id                                uuid PRIMARY KEY NOT NULL,
    kiosk_config_id                   uuid,
    kind                              text NOT NULL CONSTRAINT kiosk_config_attract_slide_kind_chk CHECK (kind IN ('video', 'photo', 'text')),
    media_asset_ref                   uuid,
    text                              jsonb,
    sort_order                        integer NOT NULL,
    duration_seconds                  integer DEFAULT 8,
    plays_when                        text DEFAULT 'open' CONSTRAINT kiosk_config_attract_slide_plays_when_chk CHECK (plays_when IN ('open', 'closed')),
    scope_path                        ltree NOT NULL
);

CREATE TABLE IF NOT EXISTS whitelabel.kiosk_config_start_tile (
    id                                uuid PRIMARY KEY NOT NULL,
    kiosk_config_id                   uuid,
    function                          text NOT NULL CONSTRAINT kiosk_config_start_tile_function_chk CHECK (function IN ('sellTickets', 'collectReservation', 'orderFood', 'shop', 'membership', 'walletTopUp', 'map', 'assistant')),
    is_enabled                        boolean DEFAULT true,
    sort_order                        integer NOT NULL,
    tile_size                         text CONSTRAINT kiosk_config_start_tile_tile_size_chk CHECK (tile_size IN ('small', 'medium', 'large')),
    image_asset_ref                   uuid,
    label                             jsonb,
    scope_path                        ltree NOT NULL
);

CREATE TABLE IF NOT EXISTS whitelabel.kiosk_config_version (
    id                                uuid PRIMARY KEY NOT NULL,
    kiosk_config_id                   uuid NOT NULL,
    version_number                    integer NOT NULL,
    published_at                      timestamptz NOT NULL,
    published_by_principal_id         uuid,
    note                              text NOT NULL CONSTRAINT kiosk_config_version_note_chk CHECK (char_length(note) <= 500),
    is_current                        boolean NOT NULL,
    content_hash                      text,
    snapshot                          jsonb,
    scope_path                        ltree NOT NULL
);

CREATE UNIQUE INDEX IF NOT EXISTS kiosk_assignment_workstation_id_uniq ON whitelabel.kiosk_assignment (workstation_id) WHERE workstation_id IS NOT NULL;

CREATE INDEX IF NOT EXISTS kiosk_assignment_scope_path_idx ON whitelabel.kiosk_assignment USING gist (scope_path);

CREATE INDEX IF NOT EXISTS kiosk_config_attract_slide_scope_path_idx ON whitelabel.kiosk_config_attract_slide USING gist (scope_path);

CREATE INDEX IF NOT EXISTS kiosk_config_scope_path_idx ON whitelabel.kiosk_config USING gist (scope_path);

CREATE INDEX IF NOT EXISTS kiosk_config_start_tile_scope_path_idx ON whitelabel.kiosk_config_start_tile USING gist (scope_path);

CREATE INDEX IF NOT EXISTS kiosk_config_version_scope_path_idx ON whitelabel.kiosk_config_version USING gist (scope_path);

SELECT platform.apply_scope_rls('whitelabel.kiosk_assignment'::regclass);

SELECT platform.apply_scope_rls('whitelabel.kiosk_config'::regclass);

SELECT platform.apply_scope_rls('whitelabel.kiosk_config_attract_slide'::regclass);

SELECT platform.apply_scope_rls('whitelabel.kiosk_config_start_tile'::regclass);

SELECT platform.apply_scope_rls('whitelabel.kiosk_config_version'::regclass);

INSERT INTO platform.schema_version (version, description, checksum)
VALUES ('V0100', 'after r1 (9cec72d): 5 table(s), 0 column(s), 6 index(es), 5 other statement(s)', 'e8522fbc76f2f3099f3ea7d9252a1a861b8e92d7eccb5f342cf77b8e826e4e12')
ON CONFLICT (version) DO NOTHING;

-- ============================================================================
-- ROLLBACK
-- ============================================================================
-- Commented out so that applying this file never runs it: the rollback is run by removing the
-- leading `-- `, and is tested in CI against a restored snapshot (backend/MIGRATIONS.md).
-- DROP INDEX IF EXISTS whitelabel.kiosk_config_version_scope_path_idx;
-- DROP INDEX IF EXISTS whitelabel.kiosk_config_start_tile_scope_path_idx;
-- DROP INDEX IF EXISTS whitelabel.kiosk_config_scope_path_idx;
-- DROP INDEX IF EXISTS whitelabel.kiosk_config_attract_slide_scope_path_idx;
-- DROP INDEX IF EXISTS whitelabel.kiosk_assignment_scope_path_idx;
-- DROP INDEX IF EXISTS whitelabel.kiosk_assignment_workstation_id_uniq;
-- DROP TABLE IF EXISTS whitelabel.kiosk_config_version;
-- DROP TABLE IF EXISTS whitelabel.kiosk_config_start_tile;
-- DROP TABLE IF EXISTS whitelabel.kiosk_config_attract_slide;
-- DROP TABLE IF EXISTS whitelabel.kiosk_config;
-- DROP TABLE IF EXISTS whitelabel.kiosk_assignment;
-- DELETE FROM platform.schema_version WHERE version = 'V0100';
