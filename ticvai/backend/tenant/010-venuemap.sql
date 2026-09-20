-- venuemap — 4 tables
-- **Derived. Do not hand-edit.**

-- Two-phase geometry extraction, following seating.ImportJob. A job that finds nothing is not a
-- successful job. Hangs off: reaches venuemap.point through its keys; references venuemap.map.
-- Reached by: 3 operations read it and 1 write it; 1 tables reference it.
CREATE TABLE IF NOT EXISTS venuemap.import_job (
    id                                uuid PRIMARY KEY NOT NULL,
    map_id                            uuid,
    status                            text NOT NULL,
    outcome                           text NOT NULL,
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
    scope_path                        text,
    kind                              text,
    floor_level                       integer,
    status                            text NOT NULL,
    published_version                 integer,
    is_georeferenced                  boolean,
    base_asset_id                     uuid,
    base_image_alignment              jsonb,
    tile_set_ref                      text,
    bounds_geo_json                   text,
    graph_status                      text
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
    is_step_free                      boolean,
    is_indoor                         boolean,
    restricted_by_point_id            uuid,
    closed_reason                     text
);

-- What a venue places on the map (19.2.57–19.2.60) — rides, restaurants, toilets, exits.
-- emergencyExit is separate from exit on purpose. Hangs off: a root — nothing above it in its
-- schema; references access.access_point, catalogue.product, platform.outlet. Reached by: 14
-- operations read it and 4 write it; 5 tables reference it.
CREATE TABLE IF NOT EXISTS venuemap.point (
    id                                uuid PRIMARY KEY NOT NULL,
    map_id                            uuid NOT NULL,
    kind                              text NOT NULL,
    name                              text NOT NULL,
    name_localised                    jsonb,
    position                          jsonb NOT NULL,
    outlet_id                         uuid,
    product_id                        uuid,
    access_point_id                   uuid,
    is_accessible                     boolean,
    opening_hours                     text,
    icon_ref                          text,
    is_active                         boolean,
    is_navigable                      boolean,
    is_destination                    boolean
);

