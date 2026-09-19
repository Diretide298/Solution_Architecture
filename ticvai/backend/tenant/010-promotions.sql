-- promotions — 16 tables
-- **Derived. Do not hand-edit.**

-- One component’s share, fixed or proportional
CREATE TABLE IF NOT EXISTS promotions.allocation_component (
    allocation_split_id               uuid NOT NULL,
    id                                uuid PRIMARY KEY,
    variant_id                        uuid NOT NULL,
    percentage                        numeric(18,4),
    fixed_amount                      numeric(18,4),
    list_price                        numeric(18,4),
    revenue_account_id                uuid,
    legal_entity_id                   uuid,
    venue_id                          uuid
);

-- How a bundle price divides across its components. What the ledger posts against
CREATE TABLE IF NOT EXISTS promotions.allocation_split (
    id                                uuid PRIMARY KEY NOT NULL,
    bundle_id                         uuid NOT NULL,
    method                            text NOT NULL,
    crosses_legal_entities            boolean
);

-- Several products sold as one, with the components priced by allocation
CREATE TABLE IF NOT EXISTS promotions.bundle (
    code                              text,
    name                              text,
    description                       text,
    venue_id                          uuid,
    kind                              text,
    price                             numeric(18,4),
    allocation                        jsonb,
    valid_from                        timestamptz,
    valid_to                          timestamptz,
    id                                uuid PRIMARY KEY,
    savings_amount                    numeric(18,4),
    savings_percentage                numeric(18,4),
    has_been_sold                     boolean,
    is_active                         boolean
);

-- Pick n from a set. The bundle price does not move with the choice (ADR-0019) — the allocation
-- does Hangs off: a child of promotions.bundle; reaches promotions.promotion through its keys;
-- references promotions.bundle.
CREATE TABLE IF NOT EXISTS promotions.bundle_choice_group (
    id                                uuid PRIMARY KEY,
    label                             text NOT NULL,
    choose                            integer NOT NULL,
    allow_duplicates                  boolean,
    unavailable_behaviour             text,
    bundle_id                         uuid NOT NULL
);

-- One product inside a bundle, with its quantity
CREATE TABLE IF NOT EXISTS promotions.bundle_component (
    bundle_id                         uuid NOT NULL,
    id                                uuid PRIMARY KEY,
    variant_id                        uuid NOT NULL,
    quantity                          integer NOT NULL,
    is_optional                       boolean,
    substitute_variant_ids            text[],
    venue_id                          uuid
);

-- A batch of codes with shared rules. The codes are children
CREATE TABLE IF NOT EXISTS promotions.coupon_campaign (
    code                              text,
    name                              text,
    venue_id                          uuid,
    discount                          jsonb,
    conditions                        jsonb,
    is_single_use                     boolean,
    max_redemptions_per_code          integer,
    valid_from                        timestamptz,
    valid_to                          timestamptz,
    id                                uuid PRIMARY KEY,
    generated_count                   integer,
    redeemed_count                    integer,
    is_active                         boolean
);

-- One issued code, with its own redemption state
CREATE TABLE IF NOT EXISTS promotions.coupon_code (
    code                              text NOT NULL,
    campaign_id                       uuid NOT NULL,
    status                            text NOT NULL,
    assigned_subject_id               uuid,
    redemption_count                  integer,
    max_redemptions                   integer,
    discount                          jsonb,
    invalid_reason                    text,
    valid_from                        timestamptz,
    valid_to                          timestamptz,
    redeemed_at                       timestamptz,
    redeemed_order_id                 text,
    scope_path                        text,
    id                                uuid PRIMARY KEY NOT NULL
);

-- Holds 10 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS promotions.product_relationship (
    id                                uuid PRIMARY KEY,
    from_product_id                   uuid NOT NULL,
    to_product_id                     uuid NOT NULL,
    kind                              text NOT NULL,
    ladder_position                   integer,
    source                            text,
    strength                          numeric(18,4),
    effective_from                    date,
    effective_to                      date,
    scope_path                        text
);

-- A rule that changes a price, with eligibility and a budget. Evaluated at the basket rather than
-- stored on a product
CREATE TABLE IF NOT EXISTS promotions.promotion (
    code                              text,
    name                              text,
    description                       text,
    venue_id                          uuid,
    discount                          jsonb,
    conditions                        jsonb,
    stacking_mode                     text,
    stacking_group                    text,
    precedence                        integer,
    valid_from                        timestamptz,
    valid_to                          timestamptz,
    max_redemptions                   integer,
    max_redemptions_per_guest         integer,
    budget_cap                        numeric(18,4),
    id                                uuid PRIMARY KEY,
    status                            text,
    is_paused                         boolean,
    redemption_count                  integer,
    discount_given                    numeric(18,4),
    published_at                      timestamptz
);

-- Holds 12 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS promotions.recommendation_experiment (
    id                                uuid PRIMARY KEY,
    code                              text NOT NULL,
    name                              text,
    placement                         text,
    holdout_percent                   integer,
    primary_metric                    text,
    minimum_sample_size               integer,
    started_at                        timestamptz,
    ended_at                          timestamptz,
    status                            text,
    winning_variant                   text,
    scope_path                        text
);

-- Holds 8 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS promotions.recommendation_outcome (
    recommendation_id                 uuid NOT NULL,
    outcome                           text NOT NULL,
    at                                timestamptz,
    order_id                          uuid,
    value                             numeric(18,4),
    holdout                           boolean,
    scope_path                        text,
    id                                uuid PRIMARY KEY NOT NULL
);

-- Holds 17 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS promotions.recommendation_strategy (
    id                                uuid PRIMARY KEY,
    code                              text NOT NULL,
    name                              text NOT NULL,
    objective                         text NOT NULL,
    kinds                             text[],
    placements                        text[],
    channels                          text[],
    max_recommendations               integer,
    min_confidence                    numeric(18,4),
    ranking_weights                   jsonb,
    require_availability              boolean,
    exclude_in_basket                 boolean,
    guardrails                        jsonb,
    status                            text,
    effective_from                    date,
    effective_to                      date,
    scope_path                        text
);

-- Holds 6 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS promotions.recommendation_suppression (
    scope_path                        text,
    max_impressions_per_product_per_dayinteger,
    max_impressions_per_guest_per_sessioninteger,
    cooldown_after_dismiss_days       integer,
    cooldown_after_accept_days        integer,
    id                                uuid PRIMARY KEY NOT NULL
);

-- What to offer alongside what, and where it may appear
CREATE TABLE IF NOT EXISTS promotions.upsell_rule (
    id                                uuid PRIMARY KEY NOT NULL,
    name                              text NOT NULL,
    placement                         text NOT NULL,
    trigger_variant_ids               text[] NOT NULL,
    trigger_category_ids              text[],
    suggested_variant_ids             text[] NOT NULL,
    suggested_bundle_id               uuid,
    channels                          text[],
    priority                          integer,
    max_suggestions                   integer,
    is_active                         boolean
);

-- A named value a guest can spend, with its own balance and expiry
CREATE TABLE IF NOT EXISTS promotions.voucher (
    code                              text NOT NULL,
    batch_id                          uuid NOT NULL,
    face_value                        numeric(18,4) NOT NULL,
    balance                           numeric(18,4) NOT NULL,
    status                            text NOT NULL,
    valid_to                          timestamptz,
    id                                uuid PRIMARY KEY NOT NULL
);

-- Vouchers issued together, sharing rules and an expiry
CREATE TABLE IF NOT EXISTS promotions.voucher_batch (
    name                              text,
    venue_id                          uuid,
    face_value                        numeric(18,4),
    quantity                          integer,
    allow_partial_redemption          boolean,
    valid_from                        timestamptz,
    valid_to                          timestamptz,
    restrict_to_variant_ids           text[],
    id                                uuid PRIMARY KEY,
    issued_count                      integer,
    redeemed_value                    numeric(18,4),
    outstanding_liability             numeric(18,4)
);

