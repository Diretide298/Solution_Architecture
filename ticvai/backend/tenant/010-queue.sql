-- queue — 5 tables
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
    status                            text NOT NULL CONSTRAINT entry_status_chk CHECK (status IN ('waiting', 'called', 'redeemed', 'expired', 'noShow', 'cancelled', 'released')),
    position_in_queue                 integer,
    parties_ahead                     integer,
    estimated_call_at                 timestamptz,
    is_fast_pass                      boolean,
    priority_basis                    text DEFAULT 'none' CONSTRAINT entry_priority_basis_chk CHECK (priority_basis IN ('none', 'entitlement', 'loyaltyTier', 'promotion', 'accessibility')),
    priority_tier_id                  uuid,
    priority_promotion_id             uuid,
    is_accessibility_need_declared    boolean DEFAULT false,
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
    adaptor                           text NOT NULL CONSTRAINT feed_adaptor_chk CHECK (adaptor IN ('generic', 'mock', 'vendorAdaptor')),
    adaptor_name                      text,
    credentials_ref                   text,
    expected_interval_seconds         integer DEFAULT 60,
    is_enabled                        boolean NOT NULL
);

-- A line, physical or virtual. The platform holds what a venue’s own queue system reports
-- (ADR-0012) rather than trying to be one
CREATE TABLE IF NOT EXISTS queue.queue (
    code                              text NOT NULL CONSTRAINT queue_code_chk CHECK (char_length(code) <= 64),
    name                              jsonb NOT NULL,
    venue_id                          uuid NOT NULL,
    attraction_product_id             uuid,
    asset_id                          uuid,
    access_point_id                   uuid,
    kind                              text DEFAULT 'standby' CONSTRAINT queue_kind_chk CHECK (kind IN ('standby', 'singleRider', 'fastPass', 'virtual', 'accessible', 'groupOnly', 'staffOnly')),
    parent_queue_id                   uuid,
    load_balance_with_queue_ids       text[],
    is_in_queue_offer_enabled         boolean DEFAULT false,
    notify_before_call_minutes        integer DEFAULT 5,
    capacity_per_cycle                integer NOT NULL,
    cycle_minutes                     numeric(18,4) NOT NULL,
    max_party_size                    integer DEFAULT 6,
    height_requirement_cm             integer,
    fast_pass_allocation_percent      numeric(18,4) DEFAULT 0,
    zone                              text,
    fast_pass_id                      uuid,
    id                                uuid PRIMARY KEY NOT NULL,
    status                            text NOT NULL CONSTRAINT queue_status_chk CHECK (status IN ('open', 'paused', 'closed', 'atCapacity')),
    status_reason                     text,
    waiting_party_count               integer NOT NULL,
    waiting_guest_count               integer,
    current_wait_minutes              integer,
    wait_time_source                  text CONSTRAINT queue_wait_time_source_chk CHECK (wait_time_source IN ('sensor', 'throughput', 'manual', 'unavailable')),
    wait_time_as_of                   timestamptz,
    manual_wait_expires_at            timestamptz,
    manual_wait_note                  text CONSTRAINT queue_manual_wait_note_chk CHECK (char_length(manual_wait_note) <= 200),
    expected_reopen_at                timestamptz,
    now_serving_party_number          integer,
    last_called_at                    timestamptz,
    throughput_last_hour              integer,
    no_show_rate_percent              numeric(18,4),
    entitlement_product_ids           text[] NOT NULL,
    loyalty_tier_ids                  text[],
    promotion_ids                     text[],
    accessibility_priority            boolean DEFAULT false,
    return_window_minutes             integer DEFAULT 60,
    max_per_guest_per_day             integer,
    allowed_access_point_ids          text[]
);

-- Holds 6 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS queue.queue_operating_window (
    queue_id                          uuid NOT NULL,
    day                               text NOT NULL,
    "from"                            text NOT NULL,
    "to"                              text NOT NULL,
    last_entry_minutes_before         integer,
    id                                uuid PRIMARY KEY NOT NULL
);

-- What a queue system reported at a moment. The platform stores readings, not estimates
CREATE TABLE IF NOT EXISTS queue.reading (
    id                                text PRIMARY KEY NOT NULL,
    feed_id                           uuid,
    disposition                       text CONSTRAINT reading_disposition_chk CHECK (disposition IN ('applied', 'discardedOutOfOrder')),
    kind                              text NOT NULL CONSTRAINT reading_kind_chk CHECK (kind IN ('peopleCount', 'dwellSeconds', 'throughputPerHour', 'queueLengthMetres')),
    value                             numeric(18,4) NOT NULL,
    confidence                        numeric(18,4),
    observed_at                       timestamptz NOT NULL,
    queue_id                          uuid NOT NULL
);

