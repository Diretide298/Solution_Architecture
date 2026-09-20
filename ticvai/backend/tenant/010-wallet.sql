-- wallet — 25 tables
-- **Derived. Do not hand-edit.**

-- Holds 3 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS wallet.accounting_mapping (
    breakage_policy                   jsonb,
    scope_path                        text,
    id                                uuid PRIMARY KEY NOT NULL
);

-- Holds 10 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS wallet.adjustment (
    id                                uuid PRIMARY KEY,
    wallet_id                         uuid,
    kind                              text,
    amount                            numeric(18,4),
    affected_lot_ids                  text[],
    reason                            text,
    performed_by                      uuid,
    approved_by                       uuid,
    at                                timestamptz,
    scope_path                        text
);

-- Holds 9 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS wallet.balance (
    wallet_balance_id                 uuid NOT NULL,
    wallet_id                         uuid NOT NULL,
    available_balance                 numeric(18,4) NOT NULL,
    hold_balance                      numeric(18,4) NOT NULL,
    total_balance                     numeric(18,4) NOT NULL,
    currency_code                     text NOT NULL,
    version                           integer NOT NULL,
    updated_at                        timestamptz NOT NULL,
    id                                uuid PRIMARY KEY NOT NULL
);

-- Holds 10 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS wallet.channel_rules (
    allowed_channels                  text[],
    allowed_credential_kinds          text[],
    requires_pin                      boolean,
    pin_above_amount                  numeric(18,4),
    offline_allowed                   boolean,
    offline_floor_limit               numeric(18,4),
    offline_maximum_age_minutes       integer,
    acceptance_point_ids              text[],
    scope_path                        text,
    id                                uuid PRIMARY KEY NOT NULL
);

-- Holds 6 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS wallet.configuration_version (
    version                           integer,
    published_at                      timestamptz,
    published_by                      uuid,
    note                              text,
    scope_path                        text,
    id                                uuid PRIMARY KEY NOT NULL
);

-- Holds 7 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS wallet.consumption_policy (
    strategy                          text,
    type_order                        text[],
    within_type_order                 text,
    allow_split_tender                boolean,
    allow_guest_choice                boolean,
    scope_path                        text,
    id                                uuid PRIMARY KEY NOT NULL
);

-- Holds 9 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS wallet.credential (
    id                                uuid PRIMARY KEY,
    wallet_id                         uuid NOT NULL,
    kind                              text NOT NULL,
    identifier                        text NOT NULL,
    linked_at                         timestamptz,
    unlinked_at                       timestamptz,
    status                            text,
    replaced_by_credential_id         uuid,
    scope_path                        text
);

-- Holds 11 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS wallet.credit_eligibility (
    credit_type_id                    uuid,
    allowed_venue_ids                 text[],
    allowed_outlet_kinds              text[],
    allowed_product_category_ids      text[],
    excluded_product_ids              text[],
    allowed_channels                  text[],
    minimum_spend                     numeric(18,4),
    maximum_percent_of_basket         numeric(18,4),
    valid_days_of_week                text[],
    scope_path                        text,
    id                                uuid PRIMARY KEY NOT NULL
);

-- Holds 12 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS wallet.credit_lot (
    id                                uuid PRIMARY KEY NOT NULL,
    wallet_id                         uuid NOT NULL,
    credit_type_id                    uuid NOT NULL,
    issued_amount                     numeric(18,4),
    remaining_amount                  numeric(18,4),
    issued_at                         timestamptz,
    expires_at                        timestamptz,
    source_kind                       text,
    source_reference                  text,
    terms_snapshot                    jsonb,
    status                            text,
    scope_path                        text
);

-- Holds 15 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS wallet.credit_type (
    id                                uuid PRIMARY KEY,
    code                              text NOT NULL,
    name                              text NOT NULL,
    category                          text,
    monetary                          boolean,
    conversion_rate                   numeric(18,4),
    refundable                        boolean,
    transferable                      boolean,
    expires                           boolean,
    validity_days                     integer,
    breakage_eligible                 boolean,
    ledger_account_code               text,
    priority                          integer,
    scope_path                        text,
    is_active                         boolean
);

-- Holds 11 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS wallet.dispute (
    id                                uuid PRIMARY KEY,
    wallet_id                         uuid NOT NULL,
    transaction_ids                   text[],
    amount                            numeric(18,4),
    description                       text NOT NULL,
    raised_by                         uuid,
    raised_at                         timestamptz,
    status                            text,
    resolution                        text,
    adjustment_id                     uuid,
    scope_path                        text
);

-- Holds 11 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS wallet.funding_rules (
    wallet_type_id                    uuid,
    minimum_top_up                    numeric(18,4),
    maximum_top_up                    numeric(18,4),
    allowed_channels                  text[],
    allowed_funding_sources           text[],
    auto_reload                       jsonb,
    recurring_funding                 jsonb,
    approval_above_amount             numeric(18,4),
    velocity_limits                   jsonb,
    scope_path                        text,
    id                                uuid PRIMARY KEY NOT NULL
);

-- Holds 10 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS wallet.gift_card (
    card_code                         text NOT NULL,
    kind                              text,
    face_value                        numeric(18,4) NOT NULL,
    balance                           numeric(18,4) NOT NULL,
    status                            text NOT NULL,
    blocked_reason                    text,
    issued_at                         timestamptz NOT NULL,
    activated_at                      timestamptz,
    expires_at                        timestamptz,
    id                                uuid PRIMARY KEY NOT NULL,
    subject_id                        uuid NOT NULL
);

-- Holds 12 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS wallet.gift_card_product (
    id                                uuid PRIMARY KEY,
    code                              text,
    name                              text,
    open_amount_allowed               boolean,
    minimum_amount                    numeric(18,4),
    maximum_amount                    numeric(18,4),
    reloadable                        boolean,
    validity_months                   integer,
    activation_required               boolean,
    credit_type_id                    uuid,
    physical                          boolean,
    scope_path                        text
);

-- Holds 12 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS wallet.hold (
    wallet_hold_id                    uuid NOT NULL,
    wallet_id                         uuid NOT NULL,
    order_id                          text,
    payment_id                        uuid,
    wallet_hold_amount                numeric(18,4) NOT NULL,
    currency_code                     text NOT NULL,
    wallet_hold_status                text NOT NULL,
    expires_at                        timestamptz NOT NULL,
    created_at                        timestamptz NOT NULL,
    captured_at                       timestamptz,
    released_at                       timestamptz,
    id                                uuid PRIMARY KEY NOT NULL
);

-- Holds 7 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS wallet.refund_policy (
    default_destination               text,
    wallet_refund_credit_type_id      uuid,
    restore_to_original_lots          boolean,
    restore_original_expiry           boolean,
    wallet_refund_bonus_percent       numeric(18,4),
    scope_path                        text,
    id                                uuid PRIMARY KEY NOT NULL
);

-- Holds 10 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS wallet.restriction (
    id                                uuid PRIMARY KEY,
    wallet_id                         uuid NOT NULL,
    kind                              text NOT NULL,
    blocked_channels                  text[],
    blocked_category_ids              text[],
    reason                            text NOT NULL,
    applied_by                        uuid,
    applied_at                        timestamptz,
    expires_at                        timestamptz,
    scope_path                        text
);

-- Holds 2 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS wallet.risk_rules (
    scope_path                        text,
    id                                uuid PRIMARY KEY NOT NULL
);

-- Holds 8 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS wallet.shared_wallet (
    id                                uuid PRIMARY KEY,
    wallet_id                         uuid NOT NULL,
    kind                              text NOT NULL,
    owner_principal_id                uuid,
    organisation_id                   uuid,
    total_budget                      numeric(18,4),
    approval_above_amount             numeric(18,4),
    scope_path                        text
);

-- Holds 11 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS wallet.shared_wallet_member (
    subject_id                        uuid NOT NULL,
    role                              text,
    allowance_amount                  numeric(18,4),
    allowance_cadence                 text,
    spend_cap_per_transaction         numeric(18,4),
    allowed_category_ids              text[],
    blocked_category_ids              text[],
    allowed_venue_ids                 text[],
    active_from                       date,
    active_to                         date,
    id                                uuid PRIMARY KEY NOT NULL
);

-- Holds 9 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS wallet.transfer_rules (
    peer_to_peer_allowed              boolean,
    transferable_credit_type_ids      text[],
    maximum_per_transfer              numeric(18,4),
    maximum_per_day                   numeric(18,4),
    approval_above_amount             numeric(18,4),
    both_parties_identified           boolean,
    within_shared_wallet_only         boolean,
    scope_path                        text,
    id                                uuid PRIMARY KEY NOT NULL
);

-- Holds 12 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS wallet.voucher_type (
    id                                uuid PRIMARY KEY,
    code                              text NOT NULL,
    name                              text NOT NULL,
    benefit_kind                      text,
    benefit_value                     numeric(18,4),
    conditions                        jsonb,
    single_use                        boolean,
    combinable                        boolean,
    valid_from                        date,
    valid_to                          date,
    issue_limit                       integer,
    scope_path                        text
);

-- Holds 9 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS wallet.wallet (
    id                                uuid PRIMARY KEY,
    subject_id                        uuid NOT NULL,
    balance                           numeric(18,4) NOT NULL,
    bonus_balance                     numeric(18,4),
    currency                          text NOT NULL,
    status                            text NOT NULL,
    home_cell_name                    text,
    expires_at                        timestamptz,
    last_activity_at                  timestamptz
);

-- Holds 9 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS wallet.wallet_transaction (
    id                                text PRIMARY KEY NOT NULL,
    kind                              text NOT NULL,
    amount                            numeric(18,4) NOT NULL,
    balance_after                     numeric(18,4) NOT NULL,
    order_id                          text,
    venue_id                          uuid,
    reason                            text,
    principal_id                      uuid,
    recorded_at                       timestamptz NOT NULL,
    subject_id                        uuid NOT NULL
);

-- Holds 14 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS wallet.wallet_type (
    id                                uuid PRIMARY KEY,
    code                              text NOT NULL,
    name                              text NOT NULL,
    owner_kind                        text,
    stored_value_capability           boolean,
    top_up_capability                 boolean,
    transfer_capability               boolean,
    refund_capability                 boolean,
    gift_card_support                 boolean,
    voucher_support                   boolean,
    membership_credit_support         boolean,
    wearable_support                  boolean,
    usage_channels                    text[],
    preset_name                       text,
    holder_may_differ_from_owner      boolean,
    requires_identification           boolean,
    maximum_balance                   numeric(18,4),
    allowed_credit_type_ids           text[],
    allow_negative_balance            boolean,
    shared_structure_allowed          boolean,
    lifecycle_states                  text[],
    numbering_pattern                 text,
    scope_path                        text,
    is_active                         boolean
);

