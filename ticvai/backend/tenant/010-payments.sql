-- payments — 32 tables
-- **Derived. Do not hand-edit.**

-- Holds 9 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS payments.authentication_policy (
    three_d_secure_mode               text DEFAULT 'whenRequired' CONSTRAINT authentication_policy_three_d_secure_mode_chk CHECK (three_d_secure_mode IN ('never', 'whenRequired', 'aboveThreshold', 'always')),
    three_d_secure_threshold          numeric(18,4),
    claimed_exemptions                text[],
    is_tokenisation_enabled           boolean DEFAULT false,
    token_retention_months            integer,
    is_recurring_mandate_required     boolean DEFAULT true,
    mandate_text_asset_id             uuid,
    scope_path                        ltree NOT NULL,
    id                                uuid PRIMARY KEY NOT NULL
);

-- Holds 7 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS payments.chargeback_evidence (
    chargeback_id                     uuid NOT NULL,
    narrative                         text,
    submitted_at                      timestamptz,
    deadline_at                       timestamptz,
    outcome                           text CONSTRAINT chargeback_evidence_outcome_chk CHECK (outcome IN ('pending', 'won', 'lost', 'withdrawn')),
    scope_path                        ltree NOT NULL,
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
    status                            text CONSTRAINT credit_account_status_chk CHECK (status IN ('active', 'onHold', 'suspended', 'closed')),
    over_limit                        boolean,
    scope_path                        ltree NOT NULL
);

-- Holds 12 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS payments.currency_rule (
    id                                uuid PRIMARY KEY,
    payment_policy_id                 uuid NOT NULL,
    scope_path                        ltree NOT NULL,
    channel_id                        uuid,
    code                              text NOT NULL CONSTRAINT currency_rule_code_chk CHECK (char_length(code) <= 10),
    settlement_currency_code          text CONSTRAINT currency_rule_settlement_currency_code_chk CHECK (char_length(settlement_currency_code) <= 10),
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
    type                              text NOT NULL CONSTRAINT deposit_activity_type_chk CHECK (char_length(type) <= 30),
    amount                            numeric(18,4) NOT NULL,
    reason                            text CONSTRAINT deposit_activity_reason_chk CHECK (char_length(reason) <= 1000),
    created_by_principal_id           uuid,
    occurred_at                       timestamptz NOT NULL,
    created_at                        timestamptz NOT NULL
);

-- Holds 12 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS payments.dunning_case (
    id                                uuid PRIMARY KEY NOT NULL,
    subject_id                        uuid,
    order_id                          text,
    amount                            numeric(18,4),
    state                             text NOT NULL CONSTRAINT dunning_case_state_chk CHECK (state IN ('scheduled', 'inProgress', 'exhausted', 'recovered', 'resolvedManually')),
    decline_class                     text,
    attempts_made                     integer NOT NULL,
    next_attempt_at                   timestamptz,
    first_failed_at                   timestamptz NOT NULL,
    resolved_at                       timestamptz,
    resolution                        text CONSTRAINT dunning_case_resolution_chk CHECK (resolution IN ('paidByOtherMeans', 'cardReplaced', 'writeOff', 'cancelledByGuest')),
    resolution_note                   text CONSTRAINT dunning_case_resolution_note_chk CHECK (char_length(resolution_note) <= 500),
    resolved_by_principal_id          uuid,
    scope_path                        ltree NOT NULL
);

-- Holds 7 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS payments.dunning_policy (
    id                                uuid PRIMARY KEY,
    max_attempts                      integer NOT NULL DEFAULT 4,
    attempt_offset_days               text[],
    minimum_hours_between_attempts    integer DEFAULT 24,
    retryable_decline_classes         text[],
    notify_guest_on_each_attempt      boolean DEFAULT false,
    terminal_action                   text NOT NULL DEFAULT 'suspendBilling' CONSTRAINT dunning_policy_terminal_action_chk CHECK (terminal_action IN ('suspendBilling', 'cancelRenewal')),
    scope_path                        ltree NOT NULL
);

-- Holds 14 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS payments.eligibility_rule (
    id                                uuid PRIMARY KEY,
    payment_policy_id                 uuid NOT NULL,
    payment_method_id                 uuid NOT NULL,
    scope_path                        ltree NOT NULL,
    channel_id                        uuid,
    business_area                     text CONSTRAINT eligibility_rule_business_area_chk CHECK (char_length(business_area) <= 30),
    currency_code                     text CONSTRAINT eligibility_rule_currency_code_chk CHECK (char_length(currency_code) <= 10),
    min_order_amount                  numeric(18,4),
    max_order_amount                  numeric(18,4),
    effect                            text NOT NULL CONSTRAINT eligibility_rule_effect_chk CHECK (char_length(effect) <= 10),
    priority                          integer NOT NULL,
    is_active                         boolean NOT NULL,
    created_at                        timestamptz NOT NULL,
    updated_at                        timestamptz
);

-- Holds 7 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS payments.failover_policy (
    retryable_outcomes                text[],
    max_attempts                      integer DEFAULT 2,
    backoff_ms                        integer DEFAULT 500,
    failover_to_next_provider         boolean DEFAULT true,
    circuit_breaker                   jsonb,
    scope_path                        ltree NOT NULL,
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
    business_area                     text CONSTRAINT fee_rule_business_area_chk CHECK (char_length(business_area) <= 30),
    currency_code                     text CONSTRAINT fee_rule_currency_code_chk CHECK (char_length(currency_code) <= 10),
    name                              text NOT NULL CONSTRAINT fee_rule_name_chk CHECK (char_length(name) <= 150),
    category                          text NOT NULL CONSTRAINT fee_rule_category_chk CHECK (char_length(category) <= 20),
    calculation_type                  text NOT NULL CONSTRAINT fee_rule_calculation_type_chk CHECK (char_length(calculation_type) <= 20),
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
    session_timeout_minutes           integer DEFAULT 15,
    orphan_reconciliation_window_minutes integer DEFAULT 60,
    branding_asset_id                 uuid,
    scope_path                        ltree NOT NULL,
    id                                uuid PRIMARY KEY NOT NULL
);

-- Holds 9 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS payments.instalment (
    instalment_plan_id                uuid NOT NULL,
    sequence                          integer NOT NULL,
    due_date                          date NOT NULL,
    amount                            numeric(18,4) NOT NULL,
    status                            text NOT NULL,
    payment_id                        text,
    dunning_case_id                   uuid,
    attempted_at                      timestamptz,
    id                                uuid PRIMARY KEY NOT NULL
);

-- Holds 11 columns. No description has been written for this table — the name is the only thing
-- saying what it is. Reached by: 2 operations read it and 1 write it; 1 tables reference it.
CREATE TABLE IF NOT EXISTS payments.instalment_plan (
    id                                uuid PRIMARY KEY NOT NULL,
    order_id                          text NOT NULL,
    subject_id                        uuid,
    frequency                         text NOT NULL CONSTRAINT instalment_plan_frequency_chk CHECK (frequency IN ('monthly', 'quarterly', 'custom')),
    payment_token_id                  uuid,
    status                            text NOT NULL CONSTRAINT instalment_plan_status_chk CHECK (status IN ('active', 'completed', 'inArrears', 'cancelled')),
    total                             numeric(18,4) NOT NULL,
    paid_to_date                      numeric(18,4),
    next_due_date                     date,
    created_at                        timestamptz,
    scope_path                        ltree NOT NULL
);

-- Holds 10 columns. No description has been written for this table — the name is the only thing
-- saying what it is. Reached by: 3 operations read it and 1 write it.
CREATE TABLE IF NOT EXISTS payments.instalment_policy (
    is_enabled                        boolean DEFAULT false,
    eligible_product_kinds            text[],
    minimum_order_value               numeric(18,4),
    allowed_frequencies               text[],
    maximum_instalments               integer,
    due_at_purchase_percent           numeric(18,4),
    instalment_fee                    numeric(18,4),
    require_stored_card               boolean DEFAULT true,
    scope_path                        ltree NOT NULL,
    id                                uuid PRIMARY KEY NOT NULL
);

-- Holds 8 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS payments.matching_rules (
    primary_key                       text CONSTRAINT matching_rules_primary_key_chk CHECK (primary_key IN ('providerReference', 'platformReference', 'authorisationCode', 'retrievalReference')),
    fallback_keys                     text[],
    amount_tolerance_minor            integer DEFAULT 0,
    date_window_days                  integer DEFAULT 2,
    net_of_fees                       boolean DEFAULT true,
    auto_resolve_below_minor          integer DEFAULT 0,
    scope_path                        ltree NOT NULL,
    id                                uuid PRIMARY KEY NOT NULL
);

-- Holds 9 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS payments.merchant_account (
    id                                uuid PRIMARY KEY,
    code                              text NOT NULL,
    legal_entity_id                   uuid,
    venue_ids                         text[],
    settlement_calendar               text CONSTRAINT merchant_account_settlement_calendar_chk CHECK (settlement_calendar IN ('daily', 'weekly', 'monthly', 'custom')),
    settlement_delay_days             integer DEFAULT 1,
    bank_account_reference            text,
    scope_path                        ltree NOT NULL
);

-- Holds 16 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS payments.method (
    id                                uuid PRIMARY KEY,
    code                              text NOT NULL,
    name                              text NOT NULL,
    kind                              text NOT NULL CONSTRAINT method_kind_chk CHECK (kind IN ('card', 'digitalWallet', 'bankTransfer', 'cash', 'storedValue', 'giftCard', 'voucher', 'onAccount', 'buyNowPayLater', 'paymentLink')),
    card_schemes                      text[],
    currencies                        text[],
    channels                          text[],
    venue_ids                         text[],
    minimum_amount                    numeric(18,4),
    maximum_amount                    numeric(18,4),
    surcharge                         jsonb,
    is_refundable                     boolean DEFAULT true,
    is_partial_refund_supported       boolean DEFAULT true,
    display_order                     integer DEFAULT 0,
    scope_path                        ltree NOT NULL,
    is_active                         boolean DEFAULT true
);

-- Holds 11 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS payments.method_config (
    id                                uuid PRIMARY KEY,
    payment_policy_id                 uuid NOT NULL,
    payment_method_id                 uuid NOT NULL,
    scope_path                        ltree NOT NULL,
    channel_id                        uuid,
    currency_code                     text CONSTRAINT method_config_currency_code_chk CHECK (char_length(currency_code) <= 10),
    is_enabled                        boolean NOT NULL,
    display_order                     integer NOT NULL,
    is_active                         boolean NOT NULL,
    created_at                        timestamptz NOT NULL,
    updated_at                        timestamptz
);

-- Holds 7 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS payments.mixed_tender_rules (
    is_split_payment_allowed          boolean DEFAULT true,
    maximum_tenders                   integer DEFAULT 3,
    tender_order                      text[],
    is_partial_payment_allowed        boolean DEFAULT false,
    on_partial_failure                text DEFAULT 'reverseAll' CONSTRAINT mixed_tender_rules_on_partial_failure_chk CHECK (on_partial_failure IN ('reverseAll', 'keepAndRetry', 'keepAndHold')),
    scope_path                        ltree NOT NULL,
    id                                uuid PRIMARY KEY NOT NULL
);

-- Holds 16 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS payments.payment_attempt (
    id                                uuid PRIMARY KEY,
    payment_id                        text,
    order_id                          text,
    provider_connection_id            uuid NOT NULL,
    payment_method_id                 uuid,
    card_type                         text,
    channel                           text,
    outcome                           text NOT NULL CONSTRAINT payment_attempt_outcome_chk CHECK (outcome IN ('authorised', 'declined', 'errored', 'abandoned')),
    decline_class                     text,
    decline_code                      text,
    decline_reason                    text,
    latency_ms                        integer,
    authentication_outcome            text CONSTRAINT payment_attempt_authentication_outcome_chk CHECK (authentication_outcome IN ('notAttempted', 'exempted', 'frictionless', 'challengePassed', 'challengeFailed')),
    amount                            numeric(18,4),
    attempted_at                      timestamptz NOT NULL,
    scope_path                        ltree NOT NULL
);

-- Holds 11 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS payments.payment_terms (
    account_id                        uuid,
    credit_limit                      numeric(18,4),
    payment_term_days                 integer DEFAULT 30,
    billing_cycle                     text CONSTRAINT payment_terms_billing_cycle_chk CHECK (billing_cycle IN ('perBooking', 'weekly', 'fortnightly', 'monthly')),
    is_purchase_order_required        boolean DEFAULT false,
    deposit_percent                   numeric(18,4),
    balance_due                       text DEFAULT 'beforeArrival' CONSTRAINT payment_terms_balance_due_chk CHECK (balance_due IN ('onArrival', 'beforeArrival', 'onTerms')),
    at_limit                          text DEFAULT 'allowWithOverride' CONSTRAINT payment_terms_at_limit_chk CHECK (at_limit IN ('refuse', 'warn', 'allowWithOverride')),
    override_approval_role            text,
    scope_path                        ltree NOT NULL,
    id                                uuid PRIMARY KEY NOT NULL
);

-- A configured gateway (BL-116, CF-131). Two are confirmed for Phase 1, which is the number that
-- forces an abstraction — one can be hard-coded and two cannot. Credentials live in the vault
CREATE TABLE IF NOT EXISTS payments.provider (
    id                                uuid PRIMARY KEY NOT NULL,
    name                              text NOT NULL,
    kind                              text NOT NULL CONSTRAINT provider_kind_chk CHECK (kind IN ('networkInternational', 'stripe', 'adyen', 'checkout', 'cash', 'wallet', 'other')),
    supported_methods                 text[],
    supported_currencies              text[],
    supports_tokenisation             boolean,
    supports_partial_capture          boolean DEFAULT true,
    accepted_on_channels              text[],
    presentment_currencies            text[],
    supports3ds                       boolean DEFAULT true,
    terminal                          jsonb,
    credential_ref                    text,
    scope_level                       text CONSTRAINT provider_scope_level_chk CHECK (scope_level IN ('tenant', 'region', 'venue')),
    scope_path                        ltree NOT NULL,
    is_active                         boolean NOT NULL
);

-- Holds 11 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS payments.provider_connection (
    id                                uuid PRIMARY KEY,
    code                              text NOT NULL,
    name                              text,
    provider_kind                     text NOT NULL CONSTRAINT provider_connection_provider_kind_chk CHECK (provider_kind IN ('gateway', 'psp', 'acquirer', 'walletProvider', 'bnplProvider')),
    environment                       text CONSTRAINT provider_connection_environment_chk CHECK (environment IN ('sandbox', 'production')),
    credential_fingerprint            text,
    capabilities                      jsonb,
    merchant_account_id               uuid,
    status                            text CONSTRAINT provider_connection_status_chk CHECK (status IN ('draft', 'testing', 'active', 'degraded', 'disabled')),
    last_tested_at                    timestamptz,
    scope_path                        ltree NOT NULL
);

-- Holds 8 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS payments.provider_cost (
    id                                uuid PRIMARY KEY,
    payment_id                        text,
    provider_connection_id            uuid NOT NULL,
    cost_kind                         text NOT NULL CONSTRAINT provider_cost_cost_kind_chk CHECK (cost_kind IN ('schemeFee', 'interchange', 'acquirerMargin', 'fxSpread')),
    amount                            numeric(18,4) NOT NULL,
    settlement_id                     uuid,
    incurred_at                       timestamptz NOT NULL,
    scope_path                        ltree NOT NULL
);

-- Holds 10 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS payments.reconciliation_source (
    id                                uuid PRIMARY KEY,
    code                              text NOT NULL,
    connection_id                     uuid,
    transport                         text CONSTRAINT reconciliation_source_transport_chk CHECK (transport IN ('sftp', 'api', 'email', 'manualUpload')),
    format                            text CONSTRAINT reconciliation_source_format_chk CHECK (format IN ('csv', 'fixedWidth', 'json', 'xml', 'camt053')),
    expected_schedule                 text DEFAULT 'daily',
    expected_by_time                  text,
    alert_if_missing                  boolean DEFAULT true,
    field_mapping                     jsonb,
    scope_path                        ltree NOT NULL
);

-- Holds 2 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS payments.risk_rules (
    scope_path                        ltree NOT NULL,
    id                                uuid PRIMARY KEY NOT NULL
);

-- Holds 7 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS payments.routing_rule (
    provider_id                       uuid NOT NULL,
    fallback_provider_id              uuid,
    id                                uuid PRIMARY KEY,
    code                              text NOT NULL,
    priority                          integer DEFAULT 0,
    conditions                        jsonb,
    strategy                          text DEFAULT 'priorityOrder' CONSTRAINT routing_rule_strategy_chk CHECK (strategy IN ('priorityOrder', 'loadShare', 'lowestCost', 'highestAuthRate')),
    scope_path                        ltree NOT NULL,
    is_active                         boolean DEFAULT true
);

-- Holds 9 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS payments.stored_forward (
    id                                uuid PRIMARY KEY,
    device_id                         uuid,
    amount                            numeric(18,4),
    taken_at                          timestamptz,
    masked_pan                        text,
    status                            text CONSTRAINT stored_forward_status_chk CHECK (status IN ('held', 'forwarding', 'accepted', 'rejected', 'expired')),
    attempts                          integer DEFAULT 0,
    rejection_reason                  text,
    scope_path                        ltree NOT NULL
);

-- Holds 11 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS payments.terminal (
    device_id                         uuid NOT NULL,
    merchant_account_id               uuid,
    acquirer_connection_id            uuid,
    terminal_identifier               text,
    emv_configuration_version         text,
    terminal_model_code               text,
    entry_modes                       text[],
    is_dcc_enabled                    boolean DEFAULT false,
    dcc_provider_connection_id        uuid,
    contactless_limit                 numeric(18,4),
    is_pin_bypass_allowed             boolean DEFAULT false,
    store_and_forward                 jsonb,
    status                            text CONSTRAINT terminal_status_chk CHECK (status IN ('unconfigured', 'active', 'offline', 'suspended')),
    scope_path                        ltree NOT NULL,
    id                                uuid PRIMARY KEY NOT NULL
);

-- Holds 11 columns. No description has been written for this table — the name is the only thing
-- saying what it is. Reached by: 3 operations read it and 1 write it; 1 tables reference it.
CREATE TABLE IF NOT EXISTS payments.terminal_certification (
    id                                uuid PRIMARY KEY,
    model_code                        text NOT NULL CONSTRAINT terminal_certification_model_code_chk CHECK (char_length(model_code) <= 100),
    manufacturer                      text NOT NULL CONSTRAINT terminal_certification_manufacturer_chk CHECK (char_length(manufacturer) <= 200),
    emv_level1_approval_reference     text,
    emv_level1_expires_at             date,
    emv_level2_kernel_versions        text[],
    emv_level2_expires_at             date,
    pci_pts_approval_number           text,
    pci_pts_expires_at                date,
    document_asset_ids                text[],
    scope_path                        ltree NOT NULL
);

-- Holds 7 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS payments.terminal_certification_level3 (
    terminal_certification_id         uuid NOT NULL,
    acquirer_connection_id            uuid,
    card_scheme                       text,
    reference                         text,
    certified_at                      date,
    expires_at                        date,
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

