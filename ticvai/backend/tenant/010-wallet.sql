-- wallet — 31 tables
-- **Derived. Do not hand-edit.**

-- Holds 3 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS wallet.accounting_mapping (
    breakage_policy                   jsonb,
    scope_path                        ltree NOT NULL,
    id                                uuid PRIMARY KEY NOT NULL
);

-- Holds 10 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS wallet.adjustment (
    id                                uuid PRIMARY KEY,
    wallet_id                         uuid,
    kind                              text CONSTRAINT adjustment_kind_chk CHECK (kind IN ('reversal', 'chargeback', 'goodwill', 'correction', 'writeOff')),
    amount                            numeric(18,4),
    affected_lot_ids                  text[],
    reason                            text,
    performed_by                      uuid,
    approved_by                       uuid,
    at                                timestamptz,
    scope_path                        ltree NOT NULL
);

-- Holds 2 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS wallet.authentication_policy (
    scope_path                        ltree NOT NULL,
    id                                uuid PRIMARY KEY NOT NULL
);

-- Holds 11 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS wallet.auto_reload_setting (
    wallet_id                         uuid,
    subject_id                        uuid,
    is_enabled                        boolean NOT NULL,
    threshold_amount                  numeric(18,4),
    reload_amount                     numeric(18,4),
    payment_token_id                  uuid,
    maximum_per_day                   integer,
    status                            text CONSTRAINT auto_reload_setting_status_chk CHECK (status IN ('active', 'suspendedAfterDecline', 'disabledByVenue')),
    last_reload_at                    timestamptz,
    scope_path                        ltree NOT NULL,
    id                                uuid PRIMARY KEY NOT NULL
);

-- Holds 9 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS wallet.balance (
    wallet_balance_id                 uuid NOT NULL,
    wallet_id                         uuid NOT NULL,
    available_balance                 numeric(18,4) NOT NULL,
    hold_balance                      numeric(18,4) NOT NULL,
    balance_amount                    numeric(18,4) NOT NULL,
    currency_code                     text NOT NULL CONSTRAINT balance_currency_code_chk CHECK (char_length(currency_code) <= 10),
    version                           integer NOT NULL,
    updated_at                        timestamptz NOT NULL,
    id                                uuid PRIMARY KEY NOT NULL
);

-- Holds 10 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS wallet.channel_rules (
    allowed_channels                  text[],
    allowed_credential_kinds          text[],
    requires_pin                      boolean DEFAULT false,
    pin_above_amount                  numeric(18,4),
    is_offline_allowed                boolean DEFAULT false,
    offline_floor_limit               numeric(18,4),
    offline_maximum_age_minutes       integer,
    acceptance_point_ids              text[],
    scope_path                        ltree NOT NULL,
    id                                uuid PRIMARY KEY NOT NULL
);

-- Holds 6 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS wallet.configuration_version (
    version                           integer,
    published_at                      timestamptz,
    published_by                      uuid,
    note                              text,
    scope_path                        ltree NOT NULL,
    id                                uuid PRIMARY KEY NOT NULL
);

-- Holds 6 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS wallet.configuration_version_snapshot (
    id                                uuid PRIMARY KEY,
    configuration_version_id          uuid NOT NULL,
    area                              text NOT NULL CONSTRAINT configuration_version_snapshot_area_chk CHECK (area IN ('walletTypes', 'creditTypes', 'consumptionPolicy', 'fundingRules', 'channelRules', 'authenticationPolicy', 'transferRules', 'refundPolicy', 'riskRules', 'accountingMapping', 'reconciliationSources', 'integrationMappings')),
    values                            jsonb NOT NULL,
    captured_at                       timestamptz NOT NULL,
    scope_path                        ltree NOT NULL
);

-- Holds 7 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS wallet.consumption_policy (
    strategy                          text DEFAULT 'expiringFirst' CONSTRAINT consumption_policy_strategy_chk CHECK (strategy IN ('expiringFirst', 'typePriority', 'nonRefundableFirst', 'manual')),
    type_order                        text[],
    within_type_order                 text DEFAULT 'fefo' CONSTRAINT consumption_policy_within_type_order_chk CHECK (within_type_order IN ('fefo', 'fifo', 'lifo')),
    allow_split_tender                boolean DEFAULT true,
    allow_guest_choice                boolean DEFAULT false,
    scope_path                        ltree NOT NULL,
    id                                uuid PRIMARY KEY NOT NULL
);

-- Holds 9 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS wallet.credential (
    id                                uuid PRIMARY KEY,
    wallet_id                         uuid NOT NULL,
    kind                              text NOT NULL CONSTRAINT credential_kind_chk CHECK (kind IN ('card', 'wristband', 'nfc', 'rfid', 'qr', 'mobileApp', 'digitalKey')),
    identifier                        text NOT NULL,
    linked_at                         timestamptz,
    unlinked_at                       timestamptz,
    status                            text CONSTRAINT credential_status_chk CHECK (status IN ('active', 'lost', 'replaced', 'blocked', 'expired')),
    replaced_by_credential_id         uuid,
    scope_path                        ltree NOT NULL
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
    scope_path                        ltree NOT NULL,
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
    source_kind                       text CONSTRAINT credit_lot_source_kind_chk CHECK (source_kind IN ('topUp', 'refund', 'promotion', 'giftCard', 'membershipBenefit', 'loyaltyConversion', 'transfer', 'adjustment')),
    source_reference                  text,
    terms_snapshot                    jsonb,
    status                            text CONSTRAINT credit_lot_status_chk CHECK (status IN ('active', 'exhausted', 'expired', 'forfeited', 'reversed')),
    scope_path                        ltree NOT NULL
);

-- Holds 15 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS wallet.credit_type (
    id                                uuid PRIMARY KEY,
    code                              text NOT NULL,
    name                              text NOT NULL,
    category                          text CONSTRAINT credit_type_category_chk CHECK (category IN ('cash', 'refund', 'bonus', 'promotional', 'giftCard', 'membership', 'loyalty', 'ride', 'attraction', 'redemption', 'fnb', 'retail', 'parking', 'event', 'other')),
    is_monetary                       boolean DEFAULT true,
    conversion_rate                   numeric(18,4),
    is_refundable                     boolean DEFAULT false,
    is_transferable                   boolean DEFAULT false,
    expires                           boolean DEFAULT false,
    validity_days                     integer,
    is_breakage_eligible              boolean DEFAULT false,
    ledger_account_code               text,
    priority                          integer DEFAULT 0,
    scope_path                        ltree NOT NULL,
    is_active                         boolean DEFAULT true
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
    status                            text CONSTRAINT dispute_status_chk CHECK (status IN ('open', 'investigating', 'escalated', 'upheld', 'rejected', 'withdrawn')),
    resolution                        text,
    escalated_to_role_id              uuid,
    reprocessed_transaction_ids       text[],
    resolved_by                       uuid,
    resolved_at                       timestamptz,
    adjustment_id                     uuid,
    scope_path                        ltree NOT NULL
);

-- Holds 13 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS wallet.exit_settlement (
    id                                uuid PRIMARY KEY NOT NULL,
    wallet_id                         uuid NOT NULL,
    action                            text NOT NULL CONSTRAINT exit_settlement_action_chk CHECK (action IN ('collect', 'refund', 'waive')),
    method                            text CONSTRAINT exit_settlement_method_chk CHECK (method IN ('card', 'cash', 'storedCard', 'originalPayment')),
    amount                            numeric(18,4) NOT NULL,
    balance_before                    numeric(18,4),
    payment_id                        uuid,
    refund_id                         uuid,
    wallet_transaction_id             uuid,
    reason                            text,
    settled_by_principal_id           uuid,
    settled_at                        timestamptz NOT NULL,
    scope_path                        ltree NOT NULL
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
    scope_path                        ltree NOT NULL,
    id                                uuid PRIMARY KEY NOT NULL
);

-- Holds 10 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS wallet.gift_card (
    card_code                         text NOT NULL,
    kind                              text,
    face_value                        numeric(18,4) NOT NULL,
    balance                           numeric(18,4) NOT NULL,
    status                            text NOT NULL CONSTRAINT gift_card_status_chk CHECK (status IN ('issued', 'active', 'partiallyRedeemed', 'redeemed', 'expired', 'blocked')),
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
    is_open_amount_allowed            boolean DEFAULT false,
    minimum_amount                    numeric(18,4),
    maximum_amount                    numeric(18,4),
    is_reloadable                     boolean DEFAULT false,
    validity_months                   integer,
    is_activation_required            boolean DEFAULT true,
    credit_type_id                    uuid,
    is_physical                       boolean DEFAULT false,
    scope_path                        ltree NOT NULL
);

-- Holds 12 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS wallet.hold (
    wallet_hold_id                    uuid NOT NULL,
    wallet_id                         uuid NOT NULL,
    order_id                          uuid,
    payment_id                        uuid,
    wallet_hold_amount                numeric(18,4) NOT NULL,
    currency_code                     text NOT NULL CONSTRAINT hold_currency_code_chk CHECK (char_length(currency_code) <= 10),
    wallet_hold_status                text NOT NULL CONSTRAINT hold_wallet_hold_status_chk CHECK (char_length(wallet_hold_status) <= 20),
    expires_at                        timestamptz NOT NULL,
    created_at                        timestamptz NOT NULL,
    captured_at                       timestamptz,
    released_at                       timestamptz,
    id                                uuid PRIMARY KEY NOT NULL
);

-- Holds 5 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS wallet.integration_mapping (
    api_client_id                     uuid NOT NULL,
    date_time_format                  text DEFAULT 'ISO-8601',
    time_zone                         text,
    scope_path                        ltree NOT NULL,
    id                                uuid PRIMARY KEY NOT NULL
);

-- Holds 2 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS wallet.reconciliation_source (
    scope_path                        ltree NOT NULL,
    id                                uuid PRIMARY KEY NOT NULL
);

-- Holds 7 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS wallet.refund_policy (
    default_destination               text CONSTRAINT refund_policy_default_destination_chk CHECK (default_destination IN ('originalTender', 'wallet', 'guestChoice')),
    wallet_refund_credit_type_id      uuid,
    restore_to_original_lots          boolean DEFAULT true,
    restore_original_expiry           boolean DEFAULT true,
    wallet_refund_bonus_percent       numeric(18,4),
    scope_path                        ltree NOT NULL,
    id                                uuid PRIMARY KEY NOT NULL
);

-- Holds 10 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS wallet.restriction (
    id                                uuid PRIMARY KEY,
    wallet_id                         uuid NOT NULL,
    kind                              text NOT NULL CONSTRAINT restriction_kind_chk CHECK (kind IN ('freeze', 'block', 'restrict', 'none')),
    blocked_channels                  text[],
    blocked_category_ids              text[],
    reason                            text NOT NULL,
    applied_by                        uuid,
    applied_at                        timestamptz,
    expires_at                        timestamptz,
    scope_path                        ltree NOT NULL
);

-- Holds 2 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS wallet.risk_rules (
    scope_path                        ltree NOT NULL,
    id                                uuid PRIMARY KEY NOT NULL
);

-- Holds 8 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS wallet.shared_wallet (
    id                                uuid PRIMARY KEY,
    wallet_id                         uuid NOT NULL,
    kind                              text NOT NULL CONSTRAINT shared_wallet_kind_chk CHECK (kind IN ('family', 'household', 'corporate', 'school', 'group')),
    owner_principal_id                uuid,
    organisation_id                   uuid,
    budget_amount                     numeric(18,4),
    approval_above_amount             numeric(18,4),
    scope_path                        ltree NOT NULL
);

-- Holds 11 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS wallet.shared_wallet_member (
    subject_id                        uuid NOT NULL,
    role                              text CONSTRAINT shared_wallet_member_role_chk CHECK (role IN ('owner', 'administrator', 'spender', 'viewer')),
    allowance_amount                  numeric(18,4),
    allowance_cadence                 text DEFAULT 'none' CONSTRAINT shared_wallet_member_allowance_cadence_chk CHECK (allowance_cadence IN ('daily', 'weekly', 'monthly', 'none')),
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
    is_peer_to_peer_allowed           boolean DEFAULT false,
    transferable_credit_type_ids      text[],
    maximum_per_transfer              numeric(18,4),
    maximum_per_day                   numeric(18,4),
    approval_above_amount             numeric(18,4),
    is_both_parties_identified        boolean DEFAULT true,
    within_shared_wallet_only         boolean DEFAULT false,
    scope_path                        ltree NOT NULL,
    id                                uuid PRIMARY KEY NOT NULL
);

-- Holds 12 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS wallet.voucher_type (
    id                                uuid PRIMARY KEY,
    code                              text NOT NULL,
    name                              text NOT NULL,
    benefit_kind                      text CONSTRAINT voucher_type_benefit_kind_chk CHECK (benefit_kind IN ('freeItem', 'percentDiscount', 'fixedDiscount', 'upgrade', 'accessEntitlement', 'companionEntry')),
    benefit_value                     numeric(18,4),
    conditions                        jsonb,
    single_use                        boolean DEFAULT true,
    is_combinable                     boolean DEFAULT false,
    valid_from                        date,
    valid_to                          date,
    issue_limit                       integer,
    scope_path                        ltree NOT NULL
);

-- Holds 9 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS wallet.wallet (
    id                                uuid PRIMARY KEY,
    subject_id                        uuid NOT NULL,
    balance                           numeric(18,4) NOT NULL,
    bonus_balance                     numeric(18,4),
    currency                          text NOT NULL,
    status                            text NOT NULL CONSTRAINT wallet_status_chk CHECK (status IN ('active', 'suspended', 'closed')),
    home_cell_name                    text,
    expires_at                        timestamptz,
    last_activity_at                  timestamptz
);

-- Holds 9 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS wallet.wallet_transaction (
    id                                uuid PRIMARY KEY NOT NULL,
    wallet_id                         uuid,
    wallet_hold_id                    uuid,
    kind                              text NOT NULL CONSTRAINT wallet_transaction_kind_chk CHECK (kind IN ('topUp', 'spend', 'refund', 'adjustment', 'bonus', 'expiry', 'transfer')),
    amount                            numeric(18,4) NOT NULL,
    balance_after                     numeric(18,4) NOT NULL,
    order_id                          uuid,
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
    owner_kind                        text CONSTRAINT wallet_type_owner_kind_chk CHECK (owner_kind IN ('guest', 'registeredCustomer', 'family', 'parent', 'child', 'corporate', 'school', 'employee')),
    stored_value_capability           boolean DEFAULT true,
    top_up_capability                 boolean DEFAULT false,
    transfer_capability               boolean DEFAULT false,
    refund_capability                 boolean DEFAULT false,
    gift_card_support                 boolean DEFAULT false,
    voucher_support                   boolean DEFAULT false,
    membership_credit_support         boolean DEFAULT false,
    wearable_support                  boolean DEFAULT false,
    usage_channels                    text[],
    preset_name                       text,
    holder_may_differ_from_owner      boolean DEFAULT false,
    requires_identification           boolean DEFAULT false,
    maximum_balance                   numeric(18,4),
    allowed_credit_type_ids           text[],
    allow_negative_balance            boolean DEFAULT false,
    is_shared_structure_allowed       boolean DEFAULT false,
    lifecycle_states                  text[],
    numbering_pattern                 text,
    scope_path                        ltree NOT NULL,
    is_active                         boolean DEFAULT true
);

