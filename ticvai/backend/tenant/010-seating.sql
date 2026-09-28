-- seating — 21 tables
-- **Derived. Do not hand-edit.**

-- Holds 5 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS seating.accessible (
    seat_map_id                       uuid,
    eligibility                       text DEFAULT 'selfDeclared' CONSTRAINT accessible_eligibility_chk CHECK (eligibility IN ('open', 'selfDeclared', 'verifiedOnce', 'verifiedEachTime')),
    minimum_provision_percent         numeric(18,4),
    scope_path                        ltree NOT NULL,
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
    accessible_spaces_needed          integer DEFAULT 0,
    preferred_section_ids             text[],
    budget_per_head                   numeric(18,4),
    status                            text CONSTRAINT group_request_status_chk CHECK (status IN ('enquiry', 'quoted', 'accepted', 'allocated', 'deposited', 'confirmed', 'cancelled', 'lapsed')),
    quote_expires_at                  timestamptz,
    deposit_amount                    numeric(18,4),
    order_id                          text,
    scope_path                        ltree NOT NULL
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
    status                            text CONSTRAINT hold_pool_status_chk CHECK (status IN ('active', 'partiallyReleased', 'released', 'expired')),
    created_by                        uuid,
    scope_path                        ltree NOT NULL
);

-- Holds 11 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS seating.hold_type (
    id                                uuid PRIMARY KEY,
    code                              text NOT NULL,
    name                              text NOT NULL,
    purpose                           text CONSTRAINT hold_type_purpose_chk CHECK (purpose IN ('production', 'house', 'accessibility', 'press', 'sponsor', 'contractual', 'maintenance', 'distancing')),
    owner_role                        text,
    release_rule                      text DEFAULT 'hoursBeforePerformance' CONSTRAINT hold_type_release_rule_chk CHECK (release_rule IN ('manual', 'hoursBeforePerformance', 'onDate', 'onSelloutThreshold')),
    release_hours_before              integer,
    release_to                        text DEFAULT 'generalSale' CONSTRAINT hold_type_release_to_chk CHECK (release_to IN ('generalSale', 'anotherPool', 'remainsHeld')),
    counts_against_capacity           boolean DEFAULT true,
    visible_to_guest                  boolean DEFAULT false,
    scope_path                        ltree NOT NULL
);

-- A seat map read from a plan or a manifest. It proposes a draft; a person accepts it (ADR-0020)
CREATE TABLE IF NOT EXISTS seating.import_job (
    id                                uuid PRIMARY KEY NOT NULL,
    seat_map_id                       uuid NOT NULL,
    kind                              text NOT NULL CONSTRAINT import_job_kind_chk CHECK (kind IN ('manifest', 'geometry')),
    status                            text NOT NULL CONSTRAINT import_job_status_chk CHECK (status IN ('parsing', 'previewReady', 'committing', 'committed', 'failed')),
    parsed_seat_count                 integer,
    matched_seat_count                integer,
    unmatched_seat_count              integer,
    outcome                           text CONSTRAINT import_job_outcome_chk CHECK (outcome IN ('parsed', 'parsedWithFindings', 'noSeatsFound', 'noLayersMatched', 'unreadable')),
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
    refund_issued                     boolean DEFAULT false,
    guest_notified_at                 timestamptz,
    performed_by                      uuid,
    at                                timestamptz,
    scope_path                        ltree NOT NULL
);

-- Holds 6 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS seating.recommendation_rules (
    seat_map_id                       uuid,
    performance_id                    uuid,
    reverse_row_order                 boolean DEFAULT false,
    explain_to_guest                  boolean DEFAULT true,
    scope_path                        ltree NOT NULL,
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
    attribute                         text NOT NULL CONSTRAINT seat_attribute_chk CHECK (attribute IN ('standard', 'accessible', 'companion', 'obstructedView', 'restrictedLegroom', 'premium', 'houseSeat', 'buffer', 'aisle', 'endOfRow', 'extraLegroom', 'powerOutlet', 'tableService', 'shaded', 'covered', 'nearExit', 'nearAccessibleWc', 'wheelchairTransfer', 'limitedRecline', 'sofa', 'beanbag')),
    companion_seat_ids                text[],
    is_active                         boolean,
    seat_map_id                       uuid
);

-- Seats withheld from sale — house seats, accessibility, production hold
CREATE TABLE IF NOT EXISTS seating.seat_block (
    id                                uuid PRIMARY KEY NOT NULL,
    performance_id                    uuid NOT NULL,
    seat_ids                          text[] NOT NULL,
    reason                            text NOT NULL CONSTRAINT seat_block_reason_chk CHECK (reason IN ('productionHold', 'houseSeats', 'groupAllocation', 'maintenance', 'accessibilityReserve', 'distancing', 'other')),
    note                              text,
    created_by_principal_id           uuid,
    created_at                        timestamptz NOT NULL,
    release_at                        timestamptz,
    released_at                       timestamptz,
    scope_path                        ltree NOT NULL
);

-- Holds 4 columns. No description has been written for this table — the name is the only thing
-- saying what it is
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
    status                            text NOT NULL CONSTRAINT seat_hold_status_chk CHECK (status IN ('held', 'converted', 'released', 'expired')),
    gross_amount                      numeric(18,4),
    held_by_principal_id              uuid,
    subject_id                        uuid,
    extension_count                   integer,
    created_at                        timestamptz NOT NULL,
    expires_at                        timestamptz NOT NULL,
    block_id                          uuid
);

-- Holds 5 columns. No description has been written for this table — the name is the only thing
-- saying what it is
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
    id                                uuid PRIMARY KEY NOT NULL,
    name                              text NOT NULL,
    venue_id                          uuid NOT NULL,
    status                            text NOT NULL CONSTRAINT seat_map_status_chk CHECK (status IN ('draft', 'validated', 'published', 'archived')),
    seat_count                        integer NOT NULL,
    section_count                     integer,
    has_geometry                      boolean,
    published_at                      timestamptz,
    description                       text,
    view_box                          jsonb,
    stage_position                    jsonb,
    is_active                         boolean
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

-- Holds 10 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS seating.seat_price_band (
    id                                uuid PRIMARY KEY,
    seat_category_id                  uuid,
    code                              text NOT NULL CONSTRAINT seat_price_band_code_chk CHECK (char_length(code) <= 64),
    display_label                     text NOT NULL CONSTRAINT seat_price_band_display_label_chk CHECK (char_length(display_label) <= 200),
    display_colour                    text,
    amount                            numeric(18,4) NOT NULL,
    channel                           text,
    customer_segment_id               uuid,
    effective_from                    timestamptz NOT NULL,
    effective_to                      timestamptz
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
    scope_path                        ltree NOT NULL,
    id                                uuid PRIMARY KEY NOT NULL
);

-- How seats may be chosen — best available, adjacency, party splitting
CREATE TABLE IF NOT EXISTS seating.seating_rules (
    id                                uuid PRIMARY KEY,
    seat_map_id                       uuid NOT NULL,
    buffer_seats                      integer DEFAULT 0,
    buffer_rows                       integer DEFAULT 0,
    prevent_orphan_seats              boolean DEFAULT false,
    max_party_size                    integer,
    require_contiguous                boolean DEFAULT false,
    accessible_companion_count        integer DEFAULT 1,
    allow_split_across_rows           boolean DEFAULT true
);

-- A named part of a room, holding rows
CREATE TABLE IF NOT EXISTS seating.section (
    code                              text NOT NULL,
    name                              text NOT NULL,
    row_count                         integer NOT NULL,
    seat_count                        integer NOT NULL,
    scope_path                        ltree NOT NULL,
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
    kind                              text NOT NULL CONSTRAINT zone_kind_chk CHECK (kind IN ('standing', 'suite', 'box', 'lounge', 'accessiblePlatform', 'stage', 'entry', 'exit', 'concourse', 'obstruction', 'camera', 'aisle')),
    name                              text NOT NULL,
    capacity                          integer,
    seat_category_id                  uuid,
    contains_seat_ids                 text[],
    obstructs_zone_ids                text[],
    geometry                          text
);

