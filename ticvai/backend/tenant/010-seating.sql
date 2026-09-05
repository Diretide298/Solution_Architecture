-- seating — 11 tables
-- **Derived. Do not hand-edit.**

-- A seat map read from a plan or a manifest. It proposes a draft; a person accepts it (ADR-0020)
CREATE TABLE IF NOT EXISTS seating.import_job (
    id                                uuid PRIMARY KEY NOT NULL,
    seat_map_id                       uuid NOT NULL,
    kind                              text NOT NULL,
    status                            text NOT NULL,
    parsed_seat_count                 integer,
    matched_seat_count                integer,
    unmatched_seat_count              integer,
    outcome                           text,
    layers_found                      text[],
    created_at                        timestamptz NOT NULL,
    completed_at                      timestamptz
);

-- One seat, addressable and holdable. 396 rows in the sample manifest is one amphitheatre
CREATE TABLE IF NOT EXISTS seating.seat (
    id                                text PRIMARY KEY NOT NULL,
    section_code                      text NOT NULL,
    row_label                         text NOT NULL,
    seat_number                       text NOT NULL,
    display_label                     text,
    position                          jsonb,
    category_id                       uuid,
    attribute                         text NOT NULL,
    companion_seat_ids                text[],
    is_active                         boolean,
    seat_map_id                       uuid
);

-- Seats withheld from sale — house seats, accessibility, production hold
CREATE TABLE IF NOT EXISTS seating.seat_block (
    id                                uuid PRIMARY KEY NOT NULL,
    performance_id                    uuid NOT NULL,
    seat_ids                          text[] NOT NULL,
    reason                            text NOT NULL,
    note                              text,
    created_by_principal_id           uuid,
    created_at                        timestamptz NOT NULL,
    release_at                        timestamptz,
    released_at                       timestamptz,
    scope_path                        text
);

-- A price band or a physical class — restricted view, accessible, premium
CREATE TABLE IF NOT EXISTS seating.seat_category (
    id                                uuid PRIMARY KEY NOT NULL,
    code                              text NOT NULL,
    name                              text NOT NULL,
    venue_id                          uuid NOT NULL,
    display_colour                    text,
    rank                              integer NOT NULL,
    seat_count                        integer
);

-- A temporary claim on a seat. Expires, which is what stops two channels selling it
CREATE TABLE IF NOT EXISTS seating.seat_hold (
    id                                text PRIMARY KEY NOT NULL,
    performance_id                    uuid NOT NULL,
    seat_ids                          text[] NOT NULL,
    buffered_seat_ids                 text[],
    status                            text NOT NULL,
    total_price                       numeric(18,4),
    held_by_principal_id              uuid,
    subject_id                        uuid,
    extension_count                   integer,
    created_at                        timestamptz NOT NULL,
    expires_at                        timestamptz NOT NULL,
    block_id                          uuid
);

-- The plan of a room — sections, rows, seats, and what may combine with what. Versioned, so
-- diffSeatMapVersions can answer what changed between two layouts
CREATE TABLE IF NOT EXISTS seating.seat_map (
    description                       text,
    view_box                          jsonb,
    stage_position                    jsonb,
    is_active                         boolean,
    id                                uuid PRIMARY KEY NOT NULL,
    name                              text NOT NULL,
    venue_id                          uuid NOT NULL,
    status                            text NOT NULL,
    seat_count                        integer NOT NULL,
    section_count                     integer,
    has_geometry                      boolean,
    published_at                      timestamptz
);

-- A known venue shape, which raises the confidence of an import sharply
CREATE TABLE IF NOT EXISTS seating.seat_map_template (
    id                                uuid PRIMARY KEY NOT NULL,
    name                              text NOT NULL,
    description                       text,
    seat_count                        integer NOT NULL,
    section_count                     integer NOT NULL,
    has_geometry                      boolean,
    created_at                        timestamptz,
    region_id                         uuid NOT NULL
);

-- How seats may be chosen — best available, adjacency, party splitting
CREATE TABLE IF NOT EXISTS seating.seating_rules (
    id                                uuid PRIMARY KEY,
    seat_map_id                       uuid NOT NULL,
    buffer_seats                      integer,
    buffer_rows                       integer,
    prevent_orphan_seats              boolean,
    max_party_size                    integer,
    require_contiguous                boolean,
    accessible_companion_count        integer,
    allow_split_across_rows           boolean
);

-- A named part of a room, holding rows
CREATE TABLE IF NOT EXISTS seating.section (
    code                              text NOT NULL,
    name                              text NOT NULL,
    row_count                         integer NOT NULL,
    seat_count                        integer NOT NULL,
    scope_path                        text,
    id                                uuid PRIMARY KEY NOT NULL
);

-- A row within a section, carrying its own numbering scheme
CREATE TABLE IF NOT EXISTS seating.section_row (
    section_id                        uuid NOT NULL,
    label                             text NOT NULL,
    seat_count                        integer NOT NULL,
    numbering_direction               text,
    id                                uuid PRIMARY KEY NOT NULL
);

-- Standing areas, suites, stages and obstructions (BL-166). A standing zone is a capacity without
-- individual seats — modelling it as seats means inventing numbers nobody prints
CREATE TABLE IF NOT EXISTS seating.zone (
    id                                uuid PRIMARY KEY NOT NULL,
    seat_map_id                       uuid NOT NULL,
    kind                              text NOT NULL,
    name                              text NOT NULL,
    capacity                          integer,
    seat_category_id                  uuid,
    contains_seat_ids                 text[],
    obstructs_zone_ids                text[],
    geometry                          text
);

