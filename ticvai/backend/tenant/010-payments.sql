-- payments — 16 tables
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
    currency                          text,
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

