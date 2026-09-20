-- seating — 20 tables
-- **Derived. Do not hand-edit.**

-- Holds 5 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS seating.accessible (
    seat_map_id                       uuid,
    eligibility                       text,
    minimum_provision_percent         numeric(18,4),
    scope_path                        text,
    id                                uuid PRIMARY KEY NOT NULL
);

-- Holds 15 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS seating.group_request (
    id                                uuid PRIMARY KEY,
    reference                         text,
    performance_id                    uuid NOT NULL,
    organisation_id                   uuid,
    contact_name                      text,
    party_size                        integer NOT NULL,
    minimum_contiguous                integer,
    accessible_spaces_needed          integer,
    preferred_section_ids             text[],
    budget_per_head                   numeric(18,4),
    status                            text,
    quote_expires_at                  timestamptz,
    deposit_amount                    numeric(18,4),
    order_id                          text,
    scope_path                        text
);

-- Holds 13 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS seating.hold_pool (
    id                                uuid PRIMARY KEY,
    hold_type_id                      uuid NOT NULL,
    performance_id                    uuid NOT NULL,
    seat_ids                          text[],
    seat_count                        integer,
    used_count                        integer,
    released_count                    integer,
    holder_name                       text,
    reason                            text,
    release_at                        timestamptz,
    status                            text,
    created_by                        uuid,
    scope_path                        text
);

-- Holds 11 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS seating.hold_type (
    id                                uuid PRIMARY KEY,
    code                              text NOT NULL,
    name                              text NOT NULL,
    purpose                           text,
    owner_role                        text,
    release_rule                      text,
    release_hours_before              integer,
    release_to                        text,
    counts_against_capacity           boolean,
    visible_to_guest                  boolean,
    scope_path                        text
);

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

-- Holds 11 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS seating.reassignment (
    id                                uuid PRIMARY KEY,
    order_id                          text,
    from_seat_ids                     text[],
    to_seat_ids                       text[],
    reason                            text,
    price_difference                  numeric(18,4),
    refund_issued                     boolean,
    guest_notified_at                 timestamptz,
    performed_by                      uuid,
    at                                timestamptz,
    scope_path                        text
);

-- Holds 6 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS seating.recommendation_rules (
    seat_map_id                       uuid,
    performance_id                    uuid,
    reverse_row_order                 boolean,
    explain_to_guest                  boolean,
    scope_path                        text,
    id                                uuid PRIMARY KEY NOT NULL
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

CREATE TABLE IF NOT EXISTS seating.seat_block_item (
    id                                uuid PRIMARY KEY,
    block_id                          uuid NOT NULL,
    seat_id                           uuid NOT NULL,
    created_at                        timestamptz NOT NULL
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

CREATE TABLE IF NOT EXISTS seating.seat_hold_item (
    id                                uuid PRIMARY KEY,
    hold_id                           uuid NOT NULL,
    seat_id                           uuid NOT NULL,
    held_price                        numeric(18,4),
    created_at                        timestamptz NOT NULL
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

-- Holds 8 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS seating.seat_rules (
    seat_map_id                       uuid,
    killed_seat_ids                   text[],
    kill_reasons                      jsonb,
    buffer_rule                       jsonb,
    companion_rule                    jsonb,
    flexible_spacing                  jsonb,
    scope_path                        text,
    id                                uuid PRIMARY KEY NOT NULL
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

