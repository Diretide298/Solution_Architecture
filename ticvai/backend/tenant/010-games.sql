-- games — 8 tables
-- **Derived. Do not hand-edit.**

-- An arcade card holding credits. The credit ledger is its history
CREATE TABLE IF NOT EXISTS games.card (
    card_code                         text PRIMARY KEY NOT NULL,
    kind                              text,
    venue_id                          uuid NOT NULL,
    subject_id                        uuid,
    credits                           integer NOT NULL,
    bonus_credits                     integer NOT NULL,
    points                            integer NOT NULL,
    status                            text NOT NULL,
    blocked_reason                    text,
    transferred_to_card_code          text,
    last_played_at                    timestamptz,
    issued_at                         timestamptz NOT NULL,
    expires_at                        timestamptz
);

-- credits bought, played and won. The arcade equivalent of a wallet Hangs off: a child of
-- games.card; reaches games.prize through its keys; references games.card. Reached by: 1
-- operations read it and 1 write it
CREATE TABLE IF NOT EXISTS games.credit_ledger (
    id                                uuid PRIMARY KEY NOT NULL,
    card_id                           text NOT NULL
);

-- A machine or attraction, with its cost in credits
CREATE TABLE IF NOT EXISTS games.game (
    id                                uuid PRIMARY KEY NOT NULL,
    code                              text NOT NULL,
    name                              text NOT NULL,
    venue_id                          uuid NOT NULL,
    zone                              text,
    asset_id                          uuid,
    reader_id                         uuid,
    credit_cost                       integer NOT NULL,
    min_points_awarded                integer,
    max_points_awarded                integer,
    height_requirement_cm             integer,
    status                            text NOT NULL,
    plays_today                       integer,
    credits_taken_today               integer,
    points_awarded_today              integer
);

-- One game played, what it cost and what it won
CREATE TABLE IF NOT EXISTS games.play (
    play_id                           text PRIMARY KEY NOT NULL,
    card_code                         text,
    game_id                           uuid,
    credits_used                      integer NOT NULL,
    points_awarded                    integer NOT NULL,
    credits_remaining                 integer NOT NULL,
    points_balance                    integer NOT NULL,
    recorded_at                       timestamptz,
    synced_at                         timestamptz
);

-- What credits can be redeemed for, with its own stock
CREATE TABLE IF NOT EXISTS games.prize (
    id                                uuid PRIMARY KEY NOT NULL,
    name                              text NOT NULL,
    description                       text,
    venue_id                          uuid NOT NULL,
    merchandise_id                    uuid,
    point_cost                        integer NOT NULL,
    on_hand                           integer NOT NULL,
    is_available                      boolean,
    tier                              text,
    image_asset_ref                   text,
    is_active                         boolean
);

-- How a game reader behaves and what it shows (BL-153). A guest at an arcade machine cannot read a
-- message, they can only see a light. Hangs off: reaches games.prize through its keys. Reached by:
-- 1 operations read it and 1 write it
CREATE TABLE IF NOT EXISTS games.reader_profile (
    id                                uuid PRIMARY KEY NOT NULL,
    name                              text NOT NULL,
    display_behaviour                 jsonb,
    retry_pricing                     jsonb,
    re_play_window_seconds            integer,
    entitlement_product_ids           text[],
    scope_path                        text
);

-- Credits exchanged for prizes. Lines are children
CREATE TABLE IF NOT EXISTS games.redemption (
    id                                text PRIMARY KEY NOT NULL,
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
    redemption_id                     text NOT NULL,
    prize_id                          uuid,
    name                              text,
    quantity                          integer,
    point_cost                        integer,
    id                                uuid PRIMARY KEY NOT NULL
);

