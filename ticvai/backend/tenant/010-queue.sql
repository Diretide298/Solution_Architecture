-- queue — 4 tables
-- **Derived. Do not hand-edit.**

-- A person in a virtual queue, with their position and their window. Renamed from entry: it is
-- somebody waiting, not a row in a log
CREATE TABLE IF NOT EXISTS queue.entry (
    id                                text PRIMARY KEY NOT NULL,
    queue_id                          uuid NOT NULL,
    queue_name                        jsonb,
    subject_id                        uuid,
    party_number                      integer NOT NULL,
    party_size                        integer NOT NULL,
    status                            text NOT NULL,
    position_in_queue                 integer,
    parties_ahead                     integer,
    estimated_call_at                 timestamptz,
    is_fast_pass                      boolean,
    entitlement_id                    text,
    called_at                         timestamptz,
    return_window_ends_at             timestamptz,
    redeemed_at                       timestamptz,
    admitted_count                    integer,
    joined_at                         timestamptz NOT NULL,
    synced_at                         timestamptz
);

-- Where readings come from — an adaptor to a venue’s own system (ADR-0012)
CREATE TABLE IF NOT EXISTS queue.feed (
    id                                uuid PRIMARY KEY NOT NULL,
    queue_id                          uuid NOT NULL,
    adaptor                           text NOT NULL,
    adaptor_name                      text,
    credentials_ref                   text,
    expected_interval_seconds         integer,
    is_enabled                        boolean NOT NULL
);

-- A line, physical or virtual. The platform holds what a venue’s own queue system reports
-- (ADR-0012) rather than trying to be one
CREATE TABLE IF NOT EXISTS queue.queue (
    code                              text,
    name                              jsonb,
    venue_id                          uuid,
    attraction_product_id             uuid,
    asset_id                          uuid,
    access_point_id                   uuid,
    kind                              text,
    parent_queue_id                   uuid,
    load_balance_with_queue_ids       text[],
    in_queue_offer_enabled            boolean,
    notify_before_call_minutes        integer,
    capacity_per_cycle                integer,
    cycle_minutes                     numeric(18,4),
    max_party_size                    integer,
    return_window_minutes             integer,
    height_requirement_cm             integer,
    fast_pass_allocation_percent      numeric(18,4),
    zone                              text,
    id                                uuid PRIMARY KEY,
    status                            text,
    status_reason                     text,
    waiting_party_count               integer,
    waiting_guest_count               integer,
    current_wait_minutes              integer,
    wait_time_source                  text,
    expected_reopen_at                timestamptz,
    now_serving_party_number          integer,
    last_called_at                    timestamptz,
    throughput_last_hour              integer,
    no_show_rate_percent              numeric(18,4),
    feed                              jsonb
);

-- What a queue system reported at a moment. The platform stores readings, not estimates
CREATE TABLE IF NOT EXISTS queue.reading (
    id                                text PRIMARY KEY NOT NULL,
    kind                              text NOT NULL,
    value                             numeric(18,4) NOT NULL,
    confidence                        numeric(18,4),
    observed_at                       timestamptz NOT NULL,
    queue_id                          uuid NOT NULL
);

