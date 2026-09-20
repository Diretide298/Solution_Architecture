-- payments — 25 tables
-- **Derived. Do not hand-edit.**

-- Holds 9 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS payments.authentication_policy (
    three_d_secure_mode               text,
    three_d_secure_threshold          numeric(18,4),
    claimed_exemptions                text[],
    tokenisation_enabled              boolean,
    token_retention_months            integer,
    recurring_mandate_required        boolean,
    mandate_text_asset_id             uuid,
    scope_path                        text,
    id                                uuid PRIMARY KEY NOT NULL
);

-- Holds 7 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS payments.chargeback_evidence (
    chargeback_id                     uuid NOT NULL,
    narrative                         text,
    submitted_at                      timestamptz,
    deadline_at                       timestamptz,
    outcome                           text,
    scope_path                        text,
    id                                uuid PRIMARY KEY NOT NULL
);

-- Holds 10 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS payments.credit_account (
    id                                uuid PRIMARY KEY,
    organisation_id                   uuid NOT NULL,
    account_code                      text,
    credit_limit                      numeric(18,4),
    outstanding_invoiced              numeric(18,4),
    outstanding_unbilled              numeric(18,4),
    available_credit                  numeric(18,4),
    status                            text,
    over_limit                        boolean,
    scope_path                        text
);

-- Holds 12 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS payments.currency_rule (
    id                                uuid PRIMARY KEY,
    payment_policy_id                 uuid NOT NULL,
    scope_path                        text,
    channel_id                        uuid,
    code                              text NOT NULL,
    settlement_currency_code          text,
    min_payment_amount                numeric(18,4),
    max_payment_amount                numeric(18,4),
    rounding_increment                numeric(18,4),
    is_active                         boolean NOT NULL,
    created_at                        timestamptz NOT NULL,
    updated_at                        timestamptz
);

-- Holds 9 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS payments.deposit_activity (
    id                                uuid PRIMARY KEY,
    deposit_id                        uuid NOT NULL,
    payment_id                        text,
    type                              text NOT NULL,
    amount                            numeric(18,4) NOT NULL,
    reason                            text,
    created_by_principal_id           uuid,
    occurred_at                       timestamptz NOT NULL,
    created_at                        timestamptz NOT NULL
);

-- Holds 12 columns. No description has been written for this table — the name is the only thing
-- saying what it is. Reached by: 2 operations read it and 0 write it.
CREATE TABLE IF NOT EXISTS payments.dunning_case (
    id                                uuid PRIMARY KEY NOT NULL,
    subject_id                        uuid,
    order_id                          text,
    amount                            numeric(18,4),
    state                             text NOT NULL,
    decline_class                     text,
    attempts_made                     integer NOT NULL,
    next_attempt_at                   timestamptz,
    first_failed_at                   timestamptz NOT NULL,
    resolved_at                       timestamptz,
    resolution                        text,
    resolution_note                   text,
    resolved_by_principal_id          uuid,
    scope_path                        text
);

-- Holds 7 columns. No description has been written for this table — the name is the only thing
-- saying what it is. Reached by: 2 operations read it and 1 write it.
CREATE TABLE IF NOT EXISTS payments.dunning_policy (
    id                                uuid PRIMARY KEY,
    max_attempts                      integer NOT NULL,
    attempt_offset_days               text[],
    minimum_hours_between_attempts    integer,
    notify_guest_on_each_attempt      boolean,
    terminal_action                   text NOT NULL,
    scope_path                        text
);

-- Holds 14 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS payments.eligibility_rule (
    id                                uuid PRIMARY KEY,
    payment_policy_id                 uuid NOT NULL,
    payment_method_id                 uuid NOT NULL,
    scope_path                        text,
    channel_id                        uuid,
    business_area                     text,
    currency_code                     text,
    min_order_amount                  numeric(18,4),
    max_order_amount                  numeric(18,4),
    effect                            text NOT NULL,
    priority                          integer NOT NULL,
    is_active                         boolean NOT NULL,
    created_at                        timestamptz NOT NULL,
    updated_at                        timestamptz
);

-- Holds 7 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS payments.failover_policy (
    retryable_outcomes                text[],
    max_attempts                      integer,
    backoff_ms                        integer,
    failover_to_next_provider         boolean,
    circuit_breaker                   jsonb,
    scope_path                        text,
    id                                uuid PRIMARY KEY NOT NULL
);

-- Holds 16 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS payments.fee_rule (
    id                                uuid PRIMARY KEY,
    payment_policy_id                 uuid NOT NULL,
    payment_method_id                 uuid,
    provider_id                       uuid,
    channel_id                        uuid,
    business_area                     text,
    currency_code                     text,
    name                              text NOT NULL,
    category                          text NOT NULL,
    calculation_type                  text NOT NULL,
    value                             numeric(18,4) NOT NULL,
    min_fee                           numeric(18,4),
    max_fee                           numeric(18,4),
    is_active                         boolean NOT NULL,
    created_at                        timestamptz NOT NULL,
    updated_at                        timestamptz
);

-- Holds 9 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS payments.hosted_checkout (
    return_url                        text,
    cancel_url                        text,
    webhook_url                       text,
    webhook_secret_fingerprint        text,
    session_timeout_minutes           integer,
    orphan_reconciliation_window_minutesinteger,
    branding_asset_id                 uuid,
    scope_path                        text,
    id                                uuid PRIMARY KEY NOT NULL
);

-- Holds 8 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS payments.matching_rules (
    primary_key                       text,
    fallback_keys                     text[],
    amount_tolerance_minor            integer,
    date_window_days                  integer,
    net_of_fees                       boolean,
    auto_resolve_below_minor          integer,
    scope_path                        text,
    id                                uuid PRIMARY KEY NOT NULL
);

-- Holds 9 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS payments.merchant_account (
    id                                uuid PRIMARY KEY,
    code                              text NOT NULL,
    legal_entity_id                   uuid,
    venue_ids                         text[],
    settlement_calendar               text,
    settlement_delay_days             integer,
    bank_account_reference            text,
    scope_path                        text
);

-- Holds 16 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS payments.method (
    id                                uuid PRIMARY KEY,
    code                              text NOT NULL,
    name                              text NOT NULL,
    kind                              text NOT NULL,
    card_schemes                      text[],
    currencies                        text[],
    channels                          text[],
    venue_ids                         text[],
    minimum_amount                    numeric(18,4),
    maximum_amount                    numeric(18,4),
    surcharge                         jsonb,
    refundable                        boolean,
    partial_refund_supported          boolean,
    display_order                     integer,
    scope_path                        text,
    is_active                         boolean
);

-- Holds 11 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS payments.method_config (
    id                                uuid PRIMARY KEY,
    payment_policy_id                 uuid NOT NULL,
    payment_method_id                 uuid NOT NULL,
    scope_path                        text,
    channel_id                        uuid,
    currency_code                     text,
    is_enabled                        boolean NOT NULL,
    display_order                     integer NOT NULL,
    is_active                         boolean NOT NULL,
    created_at                        timestamptz NOT NULL,
    updated_at                        timestamptz
);

-- Holds 7 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS payments.mixed_tender_rules (
    split_payment_allowed             boolean,
    maximum_tenders                   integer,
    tender_order                      text[],
    partial_payment_allowed           boolean,
    on_partial_failure                text,
    scope_path                        text,
    id                                uuid PRIMARY KEY NOT NULL
);

-- Holds 11 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS payments.payment_terms (
    account_id                        uuid,
    credit_limit                      numeric(18,4),
    payment_term_days                 integer,
    billing_cycle                     text,
    purchase_order_required           boolean,
    deposit_percent                   numeric(18,4),
    balance_due                       text,
    at_limit                          text,
    override_approval_role            text,
    scope_path                        text,
    id                                uuid PRIMARY KEY NOT NULL
);

-- A configured gateway (BL-116, CF-131). Two are confirmed for Phase 1, which is the number that
-- forces an abstraction — one can be hard-coded and two cannot. Credentials live in the vault
CREATE TABLE IF NOT EXISTS payments.provider (
    id                                uuid PRIMARY KEY NOT NULL,
    name                              text NOT NULL,
    kind                              text NOT NULL,
    supported_methods                 text[],
    supported_currencies              text[],
    supports_tokenisation             boolean,
    supports_partial_capture          boolean,
    presentment_currencies            text[],
    supports3ds                       boolean,
    terminal                          jsonb,
    credential_ref                    text,
    scope_level                       text,
    scope_path                        text,
    is_active                         boolean NOT NULL
);

-- Holds 11 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS payments.provider_connection (
    id                                uuid PRIMARY KEY,
    code                              text NOT NULL,
    name                              text,
    provider_kind                     text NOT NULL,
    environment                       text,
    credential_fingerprint            text,
    capabilities                      jsonb,
    merchant_account_id               uuid,
    status                            text,
    last_tested_at                    timestamptz,
    scope_path                        text
);

-- Holds 10 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS payments.reconciliation_source (
    id                                uuid PRIMARY KEY,
    code                              text NOT NULL,
    connection_id                     uuid,
    transport                         text,
    format                            text,
    expected_schedule                 text,
    expected_by_time                  text,
    alert_if_missing                  boolean,
    field_mapping                     jsonb,
    scope_path                        text
);

-- Holds 2 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS payments.risk_rules (
    scope_path                        text,
    id                                uuid PRIMARY KEY NOT NULL
);

-- Holds 7 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS payments.routing_rule (
    provider_id                       uuid NOT NULL,
    fallback_provider_id              uuid,
    id                                uuid PRIMARY KEY,
    code                              text NOT NULL,
    priority                          integer,
    conditions                        jsonb,
    strategy                          text,
    scope_path                        text,
    is_active                         boolean
);

-- Holds 9 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS payments.stored_forward (
    id                                uuid PRIMARY KEY,
    device_id                         uuid,
    amount                            numeric(18,4),
    taken_at                          timestamptz,
    masked_pan                        text,
    status                            text,
    attempts                          integer,
    rejection_reason                  text,
    scope_path                        text
);

-- Holds 11 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS payments.terminal (
    device_id                         uuid NOT NULL,
    merchant_account_id               uuid,
    acquirer_connection_id            uuid,
    terminal_identifier               text,
    emv_configuration_version         text,
    contactless_limit                 numeric(18,4),
    pin_bypass_allowed                boolean,
    store_and_forward                 jsonb,
    status                            text,
    scope_path                        text,
    id                                uuid PRIMARY KEY NOT NULL
);

-- A stored credential held by the provider (BL-116). The platform never sees a card number.
-- Provider-scoped, so a routing change means asking the guest again rather than silently losing
-- their card
CREATE TABLE IF NOT EXISTS payments.token (
    id                                uuid PRIMARY KEY NOT NULL,
    subject_id                        uuid NOT NULL,
    provider_id                       uuid NOT NULL,
    token                             text NOT NULL,
    method                            text,
    masked_identifier                 text,
    expires_at                        date,
    is_default                        boolean NOT NULL,
    consent_purpose_id                uuid
);

