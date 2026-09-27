-- promotions — 19 tables
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
    method                            text NOT NULL CONSTRAINT allocation_split_method_chk CHECK (method IN ('percentage', 'fixedAmount', 'proRataListPrice')),
    crosses_legal_entities            boolean
);

-- Several products sold as one, with the components priced by allocation
CREATE TABLE IF NOT EXISTS promotions.bundle (
    code                              text NOT NULL CONSTRAINT bundle_code_chk CHECK (char_length(code) <= 64),
    name                              text NOT NULL CONSTRAINT bundle_name_chk CHECK (char_length(name) <= 200),
    description                       text CONSTRAINT bundle_description_chk CHECK (char_length(description) <= 1000),
    venue_id                          uuid NOT NULL,
    kind                              text NOT NULL CONSTRAINT bundle_kind_chk CHECK (kind IN ('fixed', 'dynamic', 'mandatory', 'optional', 'promotional')),
    list_price                        numeric(18,4) NOT NULL,
    allocation                        jsonb NOT NULL,
    valid_from                        timestamptz,
    valid_to                          timestamptz,
    id                                uuid PRIMARY KEY NOT NULL,
    savings_amount                    numeric(18,4) NOT NULL,
    savings_percentage                numeric(18,4),
    has_been_sold                     boolean NOT NULL,
    is_active                         boolean NOT NULL
);

-- Pick n from a set. The bundle price does not move with the choice (ADR-0019) — the allocation
-- does Hangs off: a child of promotions.bundle; reaches promotions.promotion through its keys;
-- references promotions.bundle. Reached by: 4 operations read it and 1 write it; 1 tables
-- reference it.
CREATE TABLE IF NOT EXISTS promotions.bundle_choice_group (
    id                                uuid PRIMARY KEY,
    label                             text NOT NULL,
    choose                            integer NOT NULL,
    allow_duplicates                  boolean DEFAULT false,
    unavailable_behaviour             text DEFAULT 'hideOption' CONSTRAINT bundle_choice_group_unavailable_behaviour_chk CHECK (unavailable_behaviour IN ('hideOption', 'hideBundle')),
    bundle_id                         uuid NOT NULL
);

-- Holds 5 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS promotions.bundle_choice_option (
    bundle_choice_group_id            uuid NOT NULL,
    id                                uuid PRIMARY KEY,
    variant_id                        uuid NOT NULL,
    quantity                          integer,
    is_default                        boolean
);

-- One product inside a bundle, with its quantity
CREATE TABLE IF NOT EXISTS promotions.bundle_component (
    bundle_id                         uuid NOT NULL,
    id                                uuid PRIMARY KEY,
    variant_id                        uuid NOT NULL,
    quantity                          integer NOT NULL,
    is_optional                       boolean DEFAULT false,
    substitute_variant_ids            text[],
    venue_id                          uuid
);

-- A batch of codes with shared rules. The codes are children
CREATE TABLE IF NOT EXISTS promotions.coupon_campaign (
    code                              text NOT NULL CONSTRAINT coupon_campaign_code_chk CHECK (char_length(code) <= 64),
    name                              text NOT NULL CONSTRAINT coupon_campaign_name_chk CHECK (char_length(name) <= 200),
    venue_id                          uuid NOT NULL,
    discount                          jsonb NOT NULL,
    conditions                        jsonb,
    is_single_use                     boolean DEFAULT true,
    max_redemptions_per_code          integer DEFAULT 1,
    valid_from                        timestamptz NOT NULL,
    valid_to                          timestamptz,
    id                                uuid PRIMARY KEY NOT NULL,
    generated_count                   integer NOT NULL,
    redeemed_count                    integer NOT NULL,
    is_active                         boolean
);

-- One issued code, with its own redemption state
CREATE TABLE IF NOT EXISTS promotions.coupon_code (
    code                              text NOT NULL,
    campaign_id                       uuid NOT NULL,
    batch_id                          uuid,
    status                            text NOT NULL CONSTRAINT coupon_code_status_chk CHECK (status IN ('issued', 'assigned', 'redeemed', 'expired', 'voided')),
    assigned_subject_id               uuid,
    redemption_count                  integer,
    max_redemptions                   integer,
    discount                          jsonb,
    invalid_reason                    text CONSTRAINT coupon_code_invalid_reason_chk CHECK (invalid_reason IN ('expired', 'alreadyRedeemed', 'voided', 'notYetValid', 'wrongVenue', 'conditionsNotMet', 'notAssignedToGuest')),
    valid_from                        timestamptz,
    valid_to                          timestamptz,
    redeemed_at                       timestamptz,
    redeemed_order_id                 text,
    scope_path                        ltree NOT NULL,
    id                                uuid PRIMARY KEY NOT NULL
);

-- Holds 11 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS promotions.coupon_code_batch (
    id                                uuid PRIMARY KEY NOT NULL,
    campaign_id                       uuid NOT NULL,
    quantity                          integer NOT NULL,
    generated_count                   integer,
    prefix                            text CONSTRAINT coupon_code_batch_prefix_chk CHECK (char_length(prefix) <= 16),
    length                            integer,
    status                            text NOT NULL CONSTRAINT coupon_code_batch_status_chk CHECK (status IN ('queued', 'generating', 'complete', 'failed')),
    failure_reason                    text,
    requested_by_principal_id         uuid,
    requested_at                      timestamptz,
    completed_at                      timestamptz
);

-- Holds 10 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS promotions.product_relationship (
    id                                uuid PRIMARY KEY,
    from_product_id                   uuid NOT NULL,
    to_product_id                     uuid NOT NULL,
    kind                              text NOT NULL CONSTRAINT product_relationship_kind_chk CHECK (kind IN ('upgradesTo', 'downgradesTo', 'crossSell', 'accessory', 'substitute', 'requires', 'incompatibleWith')),
    ladder_position                   integer,
    source                            text DEFAULT 'declared' CONSTRAINT product_relationship_source_chk CHECK (source IN ('declared', 'measured', 'aiProposed')),
    strength                          numeric(18,4),
    effective_from                    date,
    effective_to                      date,
    scope_path                        ltree NOT NULL
);

-- A rule that changes a price, with eligibility and a budget. Evaluated at the basket rather than
-- stored on a product
CREATE TABLE IF NOT EXISTS promotions.promotion (
    code                              text NOT NULL CONSTRAINT promotion_code_chk CHECK (char_length(code) <= 64),
    name                              text NOT NULL CONSTRAINT promotion_name_chk CHECK (char_length(name) <= 200),
    description                       text CONSTRAINT promotion_description_chk CHECK (char_length(description) <= 1000),
    venue_id                          uuid NOT NULL,
    discount                          jsonb NOT NULL,
    conditions                        jsonb,
    stacking_mode                     text DEFAULT 'bestOnly',
    stacking_group                    text CONSTRAINT promotion_stacking_group_chk CHECK (char_length(stacking_group) <= 64),
    precedence                        integer DEFAULT 0,
    valid_from                        timestamptz NOT NULL,
    valid_to                          timestamptz,
    max_redemptions                   integer,
    max_redemptions_per_guest         integer,
    budget_cap                        numeric(18,4),
    id                                uuid PRIMARY KEY NOT NULL,
    status                            text NOT NULL CONSTRAINT promotion_status_chk CHECK (status IN ('draft', 'scheduled', 'live', 'paused', 'expired', 'ended')),
    is_paused                         boolean,
    redemption_count                  integer,
    discount_given                    numeric(18,4),
    published_at                      timestamptz
);

-- Holds 5 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS promotions.promotion_variant (
    id                                uuid PRIMARY KEY,
    promotion_id                      uuid,
    label                             text NOT NULL,
    traffic_percent                   integer NOT NULL,
    discount_percent                  numeric(18,4)
);

-- Holds 12 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS promotions.recommendation_experiment (
    id                                uuid PRIMARY KEY,
    code                              text NOT NULL,
    name                              text,
    placement                         text,
    holdout_percent                   integer DEFAULT 5,
    primary_metric                    text,
    minimum_sample_size               integer,
    started_at                        timestamptz,
    ended_at                          timestamptz,
    status                            text CONSTRAINT recommendation_experiment_status_chk CHECK (status IN ('draft', 'running', 'concluded', 'abandoned')),
    winning_variant                   text,
    scope_path                        ltree NOT NULL
);

-- Holds 8 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS promotions.recommendation_outcome (
    recommendation_id                 uuid NOT NULL,
    outcome                           text NOT NULL CONSTRAINT recommendation_outcome_outcome_chk CHECK (outcome IN ('shown', 'clicked', 'accepted', 'dismissed', 'expired')),
    at                                timestamptz,
    order_id                          text,
    attributed_gross_amount           numeric(18,4),
    is_holdout                        boolean DEFAULT false,
    scope_path                        ltree NOT NULL,
    id                                uuid PRIMARY KEY NOT NULL
);

-- Holds 17 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS promotions.recommendation_strategy (
    id                                uuid PRIMARY KEY,
    code                              text NOT NULL,
    name                              text NOT NULL,
    objective                         text NOT NULL CONSTRAINT recommendation_strategy_objective_chk CHECK (objective IN ('attachRevenue', 'averageOrderValue', 'upgradeRate', 'visitFrequency', 'inventoryBalance', 'guestSatisfaction')),
    kinds                             text[],
    placements                        text[],
    channels                          text[],
    max_recommendations               integer DEFAULT 3,
    min_confidence                    numeric(18,4),
    ranking_weights                   jsonb,
    require_availability              boolean DEFAULT true,
    exclude_in_basket                 boolean DEFAULT true,
    guardrails                        jsonb,
    status                            text CONSTRAINT recommendation_strategy_status_chk CHECK (status IN ('draft', 'active', 'paused', 'retired')),
    effective_from                    date,
    effective_to                      date,
    scope_path                        ltree NOT NULL
);

-- Holds 6 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS promotions.recommendation_suppression (
    scope_path                        ltree NOT NULL,
    max_impressions_per_product_per_day integer,
    max_impressions_per_guest_per_session integer,
    cooldown_after_dismiss_days       integer,
    cooldown_after_accept_days        integer,
    id                                uuid PRIMARY KEY NOT NULL
);

-- What to offer alongside what, and where it may appear
CREATE TABLE IF NOT EXISTS promotions.upsell_rule (
    id                                uuid PRIMARY KEY NOT NULL,
    name                              text NOT NULL CONSTRAINT upsell_rule_name_chk CHECK (char_length(name) <= 200),
    placement                         text NOT NULL CONSTRAINT upsell_rule_placement_chk CHECK (placement IN ('productDetail', 'cart', 'checkout', 'postPurchase', 'atGate', 'inVenue')),
    trigger_variant_ids               text[] NOT NULL,
    trigger_category_ids              text[],
    suggested_variant_ids             text[] NOT NULL,
    suggested_bundle_id               uuid,
    channels                          text[],
    priority                          integer DEFAULT 0,
    max_suggestions                   integer DEFAULT 3,
    is_active                         boolean
);

-- A named value a guest can spend, with its own balance and expiry
CREATE TABLE IF NOT EXISTS promotions.voucher (
    code                              text NOT NULL,
    batch_id                          uuid NOT NULL,
    face_value                        numeric(18,4) NOT NULL,
    balance                           numeric(18,4) NOT NULL,
    status                            text NOT NULL CONSTRAINT voucher_status_chk CHECK (status IN ('issued', 'partiallyRedeemed', 'redeemed', 'expired', 'voided')),
    valid_to                          timestamptz,
    id                                uuid PRIMARY KEY NOT NULL
);

-- Vouchers issued together, sharing rules and an expiry
CREATE TABLE IF NOT EXISTS promotions.voucher_batch (
    name                              text NOT NULL CONSTRAINT voucher_batch_name_chk CHECK (char_length(name) <= 200),
    venue_id                          uuid NOT NULL,
    face_value                        numeric(18,4) NOT NULL,
    quantity                          integer NOT NULL,
    allow_partial_redemption          boolean DEFAULT true,
    valid_from                        timestamptz,
    valid_to                          timestamptz NOT NULL,
    restrict_to_variant_ids           text[],
    id                                uuid PRIMARY KEY NOT NULL,
    issued_count                      integer NOT NULL,
    redeemed_value                    numeric(18,4) NOT NULL,
    outstanding_liability             numeric(18,4) NOT NULL
);

