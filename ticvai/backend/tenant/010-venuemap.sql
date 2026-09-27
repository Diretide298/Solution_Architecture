-- venuemap — 5 tables
-- **Derived. Do not hand-edit.**

-- Two-phase geometry extraction, following seating.ImportJob. A job that finds nothing is not a
-- successful job. Hangs off: reaches venuemap.map through its keys; references venuemap.map.
-- Reached by: 4 operations read it and 1 write it.
CREATE TABLE IF NOT EXISTS venuemap.import_job (
    id                                uuid PRIMARY KEY NOT NULL,
    map_id                            uuid,
    status                            text NOT NULL CONSTRAINT import_job_status_chk CHECK (status IN ('parsing', 'previewReady', 'committed', 'failed')),
    outcome                           text NOT NULL CONSTRAINT import_job_outcome_chk CHECK (outcome IN ('parsed', 'parsedWithFindings', 'nothingFound', 'noLayersMatched', 'unreadable')),
    shapes_found                      integer,
    layers_found                      text[],
    unmapped_layers                   text[],
    manifest_rows_read                integer,
    manifest_rows_joined              integer
);

-- A park map or floor plan (19.2.55, CF-123). Not a seat map — nothing on it is sold. Published
-- rather than saved, because editing a live map under a guest routes them into a wall
CREATE TABLE IF NOT EXISTS venuemap.map (
    id                                uuid PRIMARY KEY NOT NULL,
    name                              text NOT NULL,
    venue_id                          uuid NOT NULL,
    scope_path                        ltree NOT NULL,
    kind                              text CONSTRAINT map_kind_chk CHECK (kind IN ('park', 'floor', 'zone', 'parking')),
    floor_level                       integer,
    status                            text NOT NULL CONSTRAINT map_status_chk CHECK (status IN ('draft', 'published', 'archived')),
    published_version                 integer,
    graph_version                     integer,
    is_georeferenced                  boolean,
    base_asset_id                     uuid,
    base_image_alignment              jsonb,
    tile_set_ref                      text,
    bounds_geo_json                   text,
    graph_status                      text CONSTRAINT map_graph_status_chk CHECK (graph_status IN ('notBuilt', 'connected', 'disconnected', 'partial'))
);

-- Holds 7 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS venuemap.map_version (
    id                                uuid PRIMARY KEY NOT NULL,
    map_id                            uuid NOT NULL,
    version                           integer NOT NULL,
    published_at                      timestamptz NOT NULL,
    published_by_principal_id         uuid NOT NULL,
    note                              text CONSTRAINT map_version_note_chk CHECK (char_length(note) <= 300),
    snapshot                          jsonb NOT NULL
);

-- The navigation graph (19.2.56). isStepFree is the most important attribute on it — a wheelchair
-- user routed up a staircase was failed by the map
CREATE TABLE IF NOT EXISTS venuemap.path (
    id                                uuid PRIMARY KEY NOT NULL,
    map_id                            uuid NOT NULL,
    from_point_id                     uuid NOT NULL,
    to_point_id                       uuid NOT NULL,
    geometry                          text,
    distance_metres                   numeric(18,4),
    is_step_free                      boolean DEFAULT true,
    is_indoor                         boolean DEFAULT false,
    restricted_by_point_id            uuid,
    closed_reason                     text
);

-- What a venue places on the map (19.2.57–19.2.60) — rides, restaurants, toilets, exits.
-- emergencyExit is separate from exit on purpose. Hangs off: reaches venuemap.map through its
-- keys; references access.access_point, catalogue.product, platform.outlet. Reached by: 14
-- operations read it and 4 write it; 3 tables reference it.
CREATE TABLE IF NOT EXISTS venuemap.point (
    id                                uuid PRIMARY KEY NOT NULL,
    map_id                            uuid NOT NULL,
    kind                              text NOT NULL CONSTRAINT point_kind_chk CHECK (kind IN ('ride', 'attraction', 'show', 'restaurant', 'cafe', 'shop', 'kiosk', 'toilet', 'babyCare', 'prayerRoom', 'firstAid', 'atm', 'lockers', 'entrance', 'exit', 'emergencyExit', 'assemblyPoint', 'parking', 'guestServices', 'smokingArea', 'waterFountain', 'chargingPoint', 'photoSpot', 'junction', 'other')),
    name                              text NOT NULL,
    name_localised                    jsonb,
    position                          jsonb NOT NULL,
    outlet_id                         uuid,
    product_id                        uuid,
    access_point_id                   uuid,
    is_step_free                      boolean DEFAULT true,
    opening_hours                     text,
    icon_ref                          text,
    is_active                         boolean DEFAULT true,
    is_navigable                      boolean DEFAULT true,
    is_destination                    boolean DEFAULT true
);

