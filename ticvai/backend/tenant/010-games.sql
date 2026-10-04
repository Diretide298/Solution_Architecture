-- games — 23 tables
-- **Derived. Do not hand-edit.**

-- Holds 10 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS games.attraction_type (
    id                                uuid PRIMARY KEY NOT NULL,
    code                              text NOT NULL,
    name                              text NOT NULL,
    family                            text CONSTRAINT attraction_type_family_chk CHECK (family IN ('ride', 'arcadeGame', 'redemptionGame', 'crane', 'vrExperience', 'softPlay', 'attraction', 'show')),
    has_ticket_payout                 boolean DEFAULT false,
    has_direct_pay                    boolean DEFAULT false,
    has_cycle_time                    boolean DEFAULT true,
    has_height_restriction            boolean DEFAULT false,
    supports_entitlements             boolean DEFAULT true,
    scope_path                        ltree NOT NULL
);

-- Holds 11 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS games.authorisation (
    id                                uuid PRIMARY KEY NOT NULL,
    decision                          text CONSTRAINT authorisation_decision_chk CHECK (decision IN ('allow', 'refuse')),
    reason                            text CONSTRAINT authorisation_reason_chk CHECK (reason IN ('ok', 'cardNotFound', 'cardExpired', 'cardBlocked', 'retapTooSoon', 'heightRestriction', 'ageRestriction', 'insufficientFunds', 'entitlementExhausted', 'entitlementNotValidHere', 'cooldownActive', 'dailyCapReached', 'readerNotConfigured', 'gameUnavailable')),
    guest_message                     text,
    charged_from                      text,
    amount                            numeric(18,4),
    entitlement_id                    uuid,
    remaining_balance                 numeric(18,4),
    remaining_plays                   integer,
    decided_offline                   boolean DEFAULT false,
    scope_path                        ltree NOT NULL
);

-- An arcade card holding credits. The credit ledger is its history
CREATE TABLE IF NOT EXISTS games.card (
    card_code                         text NOT NULL,
    kind                              text,
    venue_id                          uuid NOT NULL,
    subject_id                        uuid,
    credits                           integer NOT NULL,
    bonus_credits                     integer NOT NULL,
    points                            integer NOT NULL,
    status                            text NOT NULL CONSTRAINT card_status_chk CHECK (status IN ('active', 'blocked', 'expired', 'transferred')),
    blocked_reason                    text,
    transferred_to_card_code          text,
    last_played_at                    timestamptz,
    issued_at                         timestamptz NOT NULL,
    expires_at                        timestamptz,
    id                                uuid PRIMARY KEY NOT NULL,
    wallet_id                         uuid
);

-- Holds 9 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS games.card_expiry_rules (
    basis                             text DEFAULT 'fromLastActivity' CONSTRAINT card_expiry_rules_basis_chk CHECK (basis IN ('fromIssue', 'fromLastActivity', 'fromLastRecharge')),
    validity_months                   integer,
    warn_before_days                  integer[],
    warning_channels                  text[],
    extend_on_recharge                boolean DEFAULT true,
    on_expiry                         text DEFAULT 'holdForClaim' CONSTRAINT card_expiry_rules_on_expiry_chk CHECK (on_expiry IN ('forfeit', 'holdForClaim', 'transferToBreakage')),
    hold_for_claim_days               integer,
    scope_path                        ltree NOT NULL,
    id                                uuid PRIMARY KEY NOT NULL
);

-- credits bought, played and won. The arcade equivalent of a wallet Hangs off: reaches games.game
-- through its keys; references games.card. Reached by: 1 operations read it and 1 write it.
CREATE TABLE IF NOT EXISTS games.credit_ledger (
    id                                uuid PRIMARY KEY NOT NULL,
    card_id                           uuid NOT NULL
);

-- Holds 15 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS games.entitlement (
    id                                uuid PRIMARY KEY NOT NULL,
    code                              text NOT NULL,
    name                              text,
    kind                              text NOT NULL CONSTRAINT entitlement_kind_chk CHECK (kind IN ('allGamesPass', 'unlimitedSingleGame', 'limitedSingleGame', 'package', 'freePlay')),
    game_ids                          text[],
    attraction_type_ids               text[],
    includes_games_added_later        boolean DEFAULT true,
    play_count                        integer,
    validity_kind                     text CONSTRAINT entitlement_validity_kind_chk CHECK (validity_kind IN ('sameDay', 'days', 'untilDate', 'untilUsed')),
    validity_days                     integer,
    activation_kind                   text DEFAULT 'onFirstUse' CONSTRAINT entitlement_activation_kind_chk CHECK (activation_kind IN ('onPurchase', 'onFirstUse', 'onDate')),
    daily_play_cap                    integer,
    cooldown_minutes                  integer,
    linked_product_id                 uuid,
    scope_path                        ltree NOT NULL,
    is_active                         boolean DEFAULT true
);

-- A machine or attraction, with its cost in credits
CREATE TABLE IF NOT EXISTS games.game (
    id                                uuid PRIMARY KEY NOT NULL,
    code                              text NOT NULL CONSTRAINT game_code_chk CHECK (char_length(code) <= 64),
    name                              text NOT NULL CONSTRAINT game_name_chk CHECK (char_length(name) <= 200),
    venue_id                          uuid NOT NULL,
    zone                              text,
    asset_id                          uuid,
    reader_id                         uuid,
    credit_cost                       integer NOT NULL,
    min_points_awarded                integer,
    max_points_awarded                integer,
    height_requirement_cm             integer,
    status                            text NOT NULL CONSTRAINT game_status_chk CHECK (status IN ('inService', 'outOfService', 'maintenance', 'retired')),
    plays_today                       integer,
    credits_taken_today               integer,
    points_awarded_today              integer
);

-- Holds 14 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS games.gameplay_transaction (
    id                                uuid PRIMARY KEY NOT NULL,
    reader_id                         uuid,
    game_id                           uuid,
    card_id                           uuid,
    at                                timestamptz,
    outcome                           text CONSTRAINT gameplay_transaction_outcome_chk CHECK (outcome IN ('allowed', 'refused', 'reversed')),
    reason                            text,
    amount                            numeric(18,4),
    charged_from                      text,
    entitlement_id                    uuid,
    tickets_earned                    integer,
    decided_offline                   boolean DEFAULT false,
    synced_at                         timestamptz,
    scope_path                        ltree NOT NULL
);

-- Holds 8 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS games.kiosk_config (
    kiosk_device_id                   uuid,
    steps                             text[],
    languages                         text[],
    theme_code                        text,
    idle_timeout_seconds              integer DEFAULT 30,
    requires_pin_for_top_up           boolean DEFAULT false,
    scope_path                        ltree NOT NULL,
    id                                uuid PRIMARY KEY NOT NULL
);

-- Holds 13 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS games.operational_config (
    game_id                           uuid,
    cycle_seconds                     integer,
    rider_capacity                    integer,
    throughput_per_hour               integer,
    minimum_height_cm                 integer,
    maximum_height_cm                 integer,
    minimum_age                       integer,
    supervision_required_below_age    integer,
    health_restrictions               text[],
    staff_positions                   integer,
    scope_path                        ltree NOT NULL,
    id                                uuid PRIMARY KEY NOT NULL
);

-- One game played, what it cost and what it won
CREATE TABLE IF NOT EXISTS games.play (
    play_id                           uuid PRIMARY KEY NOT NULL,
    card_code                         text,
    game_id                           uuid,
    credits_used                      integer NOT NULL,
    points_awarded                    integer NOT NULL,
    credits_remaining                 integer NOT NULL,
    points_balance                    integer NOT NULL,
    recorded_at                       timestamptz,
    synced_at                         timestamptz
);

-- Holds 8 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS games.pricing (
    game_id                           uuid,
    standard_price                    numeric(18,4),
    vip_price                         numeric(18,4),
    retry_price                       numeric(18,4),
    retry_window_seconds              integer,
    retry_offer_lead_seconds          integer,
    priority                          text[],
    scope_path                        ltree NOT NULL,
    id                                uuid PRIMARY KEY NOT NULL
);

-- Holds 11 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS games.pricing_exception (
    id                                uuid PRIMARY KEY NOT NULL,
    game_id                           uuid NOT NULL,
    kind                              text NOT NULL CONSTRAINT pricing_exception_kind_chk CHECK (kind IN ('group', 'peak', 'calendarException')),
    minimum_players                   integer,
    days_of_week                      text[],
    from_time                         text,
    to_time                           text,
    date                              date,
    price                             numeric(18,4),
    is_closed                         boolean DEFAULT false,
    scope_path                        ltree NOT NULL
);

-- What credits can be redeemed for, with its own stock
CREATE TABLE IF NOT EXISTS games.prize (
    id                                uuid PRIMARY KEY NOT NULL,
    name                              text NOT NULL CONSTRAINT prize_name_chk CHECK (char_length(name) <= 200),
    description                       text,
    venue_id                          uuid NOT NULL,
    merchandise_id                    uuid,
    point_cost                        integer NOT NULL,
    on_hand                           integer NOT NULL,
    is_available                      boolean,
    tier                              text,
    image_asset_ref                   text,
    barcode                           text CONSTRAINT prize_barcode_chk CHECK (char_length(barcode) <= 64),
    is_active                         boolean
);

-- Holds 9 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS games.prize_cost (
    prize_id                          uuid,
    ticket_price                      integer,
    unit_cost                         numeric(18,4),
    margin_percent                    numeric(18,4),
    inventory_item_id                 uuid,
    direct_pay_price                  numeric(18,4),
    display_tier                      text,
    scope_path                        ltree NOT NULL,
    id                                uuid PRIMARY KEY NOT NULL
);

-- Holds 11 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS games.reader (
    device_id                         uuid NOT NULL,
    game_id                           uuid,
    reader_profile_id                 uuid,
    accepted_credit_type_ids          text[],
    accepts_direct_pay                boolean DEFAULT false,
    retap_delay_seconds               integer DEFAULT 3,
    display_rules                     jsonb,
    io_mapping                        jsonb,
    status                            text CONSTRAINT reader_status_chk CHECK (status IN ('unconfigured', 'active', 'offline', 'maintenance', 'disabled')),
    scope_path                        ltree NOT NULL,
    id                                uuid PRIMARY KEY NOT NULL
);

-- Holds 8 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS games.reader_deployment (
    id                                uuid PRIMARY KEY NOT NULL,
    reader_id                         uuid,
    configuration_version             integer,
    edge_package_expires_at           timestamptz,
    deployed_at                       timestamptz,
    acknowledged_at                   timestamptz,
    status                            text CONSTRAINT reader_deployment_status_chk CHECK (status IN ('queued', 'sent', 'acknowledged', 'failed', 'stale')),
    failure_reason                    text
);

-- How a game reader behaves and what it shows (BL-153). A guest at an arcade machine cannot read a
-- message, they can only see a light. Hangs off: reaches games.game through its keys. Reached by:
-- 3 operations read it and 1 write it; 1 tables reference it.
CREATE TABLE IF NOT EXISTS games.reader_profile (
    id                                uuid PRIMARY KEY NOT NULL,
    name                              text NOT NULL,
    display_behaviour                 jsonb,
    retry_pricing                     jsonb,
    re_play_window_seconds            integer,
    entitlement_product_ids           text[],
    scope_path                        ltree NOT NULL
);

-- Holds 8 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS games.reader_sync_status (
    id                                uuid PRIMARY KEY NOT NULL,
    reader_id                         uuid NOT NULL,
    pending_transactions              integer NOT NULL,
    pending_value                     numeric(18,4),
    oldest_pending_at                 timestamptz,
    last_sync_at                      timestamptz,
    reported_at                       timestamptz NOT NULL,
    offline_since                     timestamptz,
    is_refusing_offline_taps          boolean,
    scope_path                        ltree NOT NULL
);

-- Credits exchanged for prizes. Lines are children
CREATE TABLE IF NOT EXISTS games.redemption (
    id                                uuid PRIMARY KEY NOT NULL,
    redemption_number                 text,
    card_code                         text NOT NULL,
    venue_id                          uuid,
    points_used                       integer NOT NULL,
    points_remaining                  integer NOT NULL,
    stock_movement_ids                text[],
    issued_by_principal_id            uuid,
    recorded_at                       timestamptz NOT NULL
);

-- One prize taken, drawn against its stock
CREATE TABLE IF NOT EXISTS games.redemption_line (
    redemption_id                     uuid NOT NULL,
    prize_id                          uuid,
    name                              text,
    quantity                          integer,
    point_cost                        integer,
    id                                uuid PRIMARY KEY NOT NULL
);

-- Holds 8 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS games.redemption_rules (
    ticket_credit_type_id             uuid,
    is_ticket_eater_enabled           boolean DEFAULT false,
    is_ticketless_enabled             boolean DEFAULT true,
    tickets_expire                    boolean DEFAULT false,
    ticket_validity_days              integer,
    counter_approval_above_tickets    integer,
    scope_path                        ltree NOT NULL,
    id                                uuid PRIMARY KEY NOT NULL
);

-- Holds 8 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS games.validation_rules (
    deduction_order                   text[],
    check_order                       text[],
    allow_partial_entitlement         boolean DEFAULT false,
    refuse_below_balance              numeric(18,4),
    is_offline_decision_allowed       boolean DEFAULT true,
    offline_maximum_value             numeric(18,4),
    scope_path                        ltree NOT NULL,
    id                                uuid PRIMARY KEY NOT NULL
);

