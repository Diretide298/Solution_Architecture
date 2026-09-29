-- transport — 12 tables
-- **Derived. Do not hand-edit.**

-- Holds 10 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS transport.departure (
    id                                text PRIMARY KEY NOT NULL,
    route_id                          text NOT NULL,
    timetable_id                      text NOT NULL,
    performance_id                    uuid NOT NULL,
    service_date                      date NOT NULL,
    departs_at                        timestamptz NOT NULL,
    status                            text NOT NULL CONSTRAINT departure_status_chk CHECK (status IN ('scheduled', 'onSale', 'soldOut', 'departed', 'cancelled')),
    seat_capacity                     integer NOT NULL,
    vehicle_resource_id               uuid,
    note                              text
);

-- Holds 5 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS transport.fare_matrix_cell (
    fare_table_id                     text NOT NULL,
    from_station_id                   text NOT NULL,
    to_station_id                     text NOT NULL,
    fare                              numeric(18,4) NOT NULL,
    id                                uuid PRIMARY KEY NOT NULL
);

-- Holds 11 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS transport.fare_passenger_type (
    fare_table_id                     text NOT NULL,
    code                              text NOT NULL,
    name                              jsonb NOT NULL,
    description                       jsonb,
    fare_multiplier                   numeric(18,4) NOT NULL,
    min_age                           integer,
    max_age                           integer,
    proof_required                    jsonb,
    is_default                        boolean DEFAULT false,
    catalogue_variant_id              uuid,
    id                                uuid PRIMARY KEY NOT NULL
);

-- Holds 6 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS transport.fare_table (
    model                             text NOT NULL CONSTRAINT fare_table_model_chk CHECK (model IN ('stopCount', 'matrix')),
    base_fare                         numeric(18,4),
    per_stop_fare                     numeric(18,4),
    effective_from                    timestamptz NOT NULL,
    id                                text PRIMARY KEY NOT NULL,
    route_id                          text NOT NULL
);

-- Holds 8 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS transport.favourite_route (
    id                                text PRIMARY KEY NOT NULL,
    venue_id                          uuid NOT NULL,
    from_station_id                   text NOT NULL,
    to_station_id                     text NOT NULL,
    from_station_name                 text,
    to_station_name                   text,
    label                             text,
    created_at                        timestamptz NOT NULL
);

-- Holds 10 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS transport.network_import (
    id                                text PRIMARY KEY NOT NULL,
    venue_id                          uuid NOT NULL,
    format                            text NOT NULL CONSTRAINT network_import_format_chk CHECK (format IN ('csvBundle', 'gtfs')),
    source_ref                        uuid NOT NULL,
    status                            text NOT NULL CONSTRAINT network_import_status_chk CHECK (status IN ('validating', 'previewReady', 'failed', 'applied', 'expired')),
    preview                           jsonb,
    created_by                        uuid,
    created_at                        timestamptz,
    applied_by                        uuid,
    applied_at                        timestamptz
);

-- Holds 14 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS transport.pass_type (
    venue_id                          uuid NOT NULL,
    code                              text NOT NULL CONSTRAINT pass_type_code_chk CHECK (char_length(code) <= 32),
    name                              jsonb NOT NULL,
    description                       jsonb,
    kind                              text NOT NULL CONSTRAINT pass_type_kind_chk CHECK (kind IN ('multiTrip', 'unlimited')),
    trips                             integer,
    fare_multiplier                   numeric(18,4) NOT NULL,
    reference_trips                   integer NOT NULL,
    validity_days                     integer NOT NULL,
    route_ids                         text[],
    sort_order                        integer DEFAULT 0,
    id                                text PRIMARY KEY NOT NULL,
    is_active                         boolean NOT NULL DEFAULT true,
    catalogue_product_id              uuid
);

-- Holds 12 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS transport.route (
    venue_id                          uuid NOT NULL,
    code                              text NOT NULL CONSTRAINT route_code_chk CHECK (char_length(code) <= 32),
    line_code                         text CONSTRAINT route_line_code_chk CHECK (char_length(line_code) <= 16),
    name                              jsonb NOT NULL,
    colour                            text,
    paired_route_id                   text,
    booking_cutoff_minutes            integer DEFAULT 5,
    id                                text PRIMARY KEY NOT NULL,
    status                            text NOT NULL CONSTRAINT route_status_chk CHECK (status IN ('draft', 'active', 'suspended', 'retired')),
    total_minutes                     integer,
    catalogue_event_id                uuid,
    catalogue_product_id              uuid
);

-- Holds 7 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS transport.route_stop (
    route_id                          text NOT NULL,
    station_id                        text NOT NULL,
    offset_minutes                    integer NOT NULL,
    is_boarding_allowed               boolean DEFAULT true,
    is_alighting_allowed              boolean DEFAULT true,
    id                                text PRIMARY KEY NOT NULL,
    sequence                          integer NOT NULL
);

-- Holds 8 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS transport.station (
    venue_id                          uuid NOT NULL,
    code                              text NOT NULL CONSTRAINT station_code_chk CHECK (char_length(code) <= 32),
    name                              jsonb NOT NULL,
    short_name                        jsonb,
    latitude                          numeric(18,4),
    longitude                         numeric(18,4),
    id                                text PRIMARY KEY NOT NULL,
    is_active                         boolean NOT NULL DEFAULT true
);

-- Holds 12 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS transport.timetable (
    name                              text NOT NULL CONSTRAINT timetable_name_chk CHECK (char_length(name) <= 120),
    valid_from                        date NOT NULL,
    valid_to                          date,
    release_horizon_days              integer DEFAULT 30,
    seat_capacity                     integer NOT NULL,
    seat_map_id                       uuid,
    id                                text PRIMARY KEY NOT NULL,
    route_id                          text NOT NULL,
    status                            text NOT NULL CONSTRAINT timetable_status_chk CHECK (status IN ('draft', 'published', 'superseded', 'withdrawn')),
    published_at                      timestamptz,
    released_through                  date,
    superseded_by_id                  text
);

-- Holds 4 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS transport.timetable_run (
    timetable_id                      text NOT NULL,
    departs_at                        text NOT NULL,
    days                              text[] NOT NULL,
    id                                uuid PRIMARY KEY NOT NULL
);

