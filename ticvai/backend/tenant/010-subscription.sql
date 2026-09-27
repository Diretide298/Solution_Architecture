-- subscription — 15 tables
-- **Derived. Do not hand-edit.**

-- Holds 10 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS subscription.capacity_pack (
    id                                uuid PRIMARY KEY,
    tenant_id                         uuid NOT NULL,
    unit                              text NOT NULL,
    quantity                          integer NOT NULL,
    list_price                        numeric(18,4),
    valid_from                        date,
    valid_to                          date,
    is_temporary                      boolean DEFAULT true,
    approved_by                       uuid,
    invoice_id                        uuid
);

-- What a tenant is paying for, and which modules that licenses
CREATE TABLE IF NOT EXISTS subscription.contract (
    tenant_id                         uuid NOT NULL,
    plan_id                           uuid NOT NULL,
    plan_name                         text,
    plan_version                      text NOT NULL,
    status                            text NOT NULL CONSTRAINT contract_status_chk CHECK (status IN ('trial', 'active', 'pastDue', 'cancelled', 'expired')),
    starts_at                         date NOT NULL,
    renews_at                         date,
    cancelled_at                      date,
    current_price                     numeric(18,4),
    billing_period                    text,
    id                                uuid PRIMARY KEY NOT NULL
);

-- Holds 3 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS subscription.enforcement_policy (
    id                                uuid PRIMARY KEY,
    is_hard_stop_allowed              boolean DEFAULT false,
    grace_days                        integer DEFAULT 7
);

-- Holds 8 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS subscription.go_live_readiness (
    tenant_id                         uuid,
    run_at                            timestamptz,
    status                            text CONSTRAINT go_live_readiness_status_chk CHECK (status IN ('notStarted', 'running', 'blocked', 'readyWithWarnings', 'ready')),
    blockers                          integer,
    warnings                          integer,
    signed_off_by                     uuid,
    signed_off_at                     timestamptz,
    id                                uuid PRIMARY KEY NOT NULL
);

-- Holds 12 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS subscription.licensing_model (
    id                                uuid PRIMARY KEY,
    code                              text NOT NULL,
    name                              text,
    billable_unit                     text NOT NULL CONSTRAINT licensing_model_billable_unit_chk CHECK (billable_unit IN ('perVenue', 'perAdmission', 'perTransaction', 'perActiveUser', 'perDevice', 'perModule', 'flatFee', 'revenueShare')),
    unit_price                        numeric(18,4),
    revenue_share_percent             numeric(18,4),
    minimum_guarantee                 numeric(18,4),
    minimum_guarantee_period          text CONSTRAINT licensing_model_minimum_guarantee_period_chk CHECK (minimum_guarantee_period IN ('monthly', 'quarterly', 'annual')),
    on_below_minimum                  text DEFAULT 'chargeMinimum' CONSTRAINT licensing_model_on_below_minimum_chk CHECK (on_below_minimum IN ('chargeMinimum', 'carryForward', 'waive')),
    included_allowances               jsonb,
    tier_code                         text,
    effective_from                    date
);

-- Holds 13 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS subscription.module_listing (
    module_code                       text NOT NULL,
    name                              text,
    description                       text,
    category                          text,
    requires_modules                  text[],
    incompatible_with_modules         text[],
    included_in_tiers                 text[],
    list_price                        numeric(18,4),
    pricing_basis                     text CONSTRAINT module_listing_pricing_basis_chk CHECK (pricing_basis IN ('included', 'flatFee', 'perVenue', 'perUnit', 'revenueShare')),
    provisioning_minutes              integer,
    requires_professional_services    boolean DEFAULT false,
    status                            text CONSTRAINT module_listing_status_chk CHECK (status IN ('available', 'beta', 'deprecated', 'withdrawn')),
    id                                uuid PRIMARY KEY NOT NULL
);

-- Holds 8 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS subscription.partner_quote (
    id                                uuid PRIMARY KEY NOT NULL,
    partner_id                        uuid,
    agreement_id                      uuid,
    total_minor                       integer,
    state                             text CONSTRAINT partner_quote_state_chk CHECK (state IN ('draft', 'sent', 'accepted', 'declined', 'expired')),
    valid_until                       timestamptz,
    created_at                        timestamptz
);

-- What a tenant pays for — the modules, the limits, the price. Renamed from plan, which sat beside
-- migration_plan and production_plan
CREATE TABLE IF NOT EXISTS subscription.plan (
    code                              text NOT NULL CONSTRAINT plan_code_chk CHECK (char_length(code) <= 64),
    name                              text NOT NULL CONSTRAINT plan_name_chk CHECK (char_length(name) <= 200),
    description                       text CONSTRAINT plan_description_chk CHECK (char_length(description) <= 1000),
    cell_tier                         text NOT NULL CONSTRAINT plan_cell_tier_chk CHECK (cell_tier IN ('shared', 'dedicated', 'isolated', 'clientHosted')),
    base_price                        numeric(18,4) NOT NULL,
    billing_period                    text CONSTRAINT plan_billing_period_chk CHECK (billing_period IN ('monthly', 'quarterly', 'annual')),
    includes_branded_app              boolean,
    included_ai_tokens                integer,
    id                                uuid PRIMARY KEY NOT NULL,
    version                           text NOT NULL,
    is_active                         boolean NOT NULL,
    subscriber_count                  integer NOT NULL,
    published_at                      timestamptz
);

-- Holds 6 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS subscription.plan_limit (
    plan_id                           uuid NOT NULL,
    metric                            text NOT NULL,
    limit_value                       integer,
    is_overage_allowed                boolean,
    overage_unit_price                numeric(18,4),
    id                                uuid PRIMARY KEY NOT NULL
);

-- Holds 3 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS subscription.plan_module (
    plan_id                           uuid NOT NULL,
    licensed_module                   text NOT NULL,
    id                                uuid PRIMARY KEY NOT NULL
);

-- Holds 10 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS subscription.tier_allowance (
    id                                uuid PRIMARY KEY,
    tier_id                           uuid NOT NULL,
    code                              text NOT NULL CONSTRAINT tier_allowance_code_chk CHECK (char_length(code) <= 100),
    name                              text NOT NULL CONSTRAINT tier_allowance_name_chk CHECK (char_length(name) <= 150),
    limit_value                       numeric(18,4),
    period                            text CONSTRAINT tier_allowance_period_chk CHECK (char_length(period) <= 20),
    is_unlimited                      boolean NOT NULL,
    is_active                         boolean NOT NULL,
    created_at                        timestamptz NOT NULL,
    updated_at                        timestamptz
);

-- Holds 8 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS subscription.tier_module (
    id                                uuid PRIMARY KEY,
    tier_id                           uuid NOT NULL,
    code                              text NOT NULL CONSTRAINT tier_module_code_chk CHECK (char_length(code) <= 100),
    is_included                       boolean NOT NULL,
    notes                             text CONSTRAINT tier_module_notes_chk CHECK (char_length(notes) <= 500),
    is_active                         boolean NOT NULL,
    created_at                        timestamptz NOT NULL,
    updated_at                        timestamptz
);

-- Holds 10 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS subscription.trial_config (
    id                                uuid PRIMARY KEY,
    tier_code                         text,
    duration_days                     integer DEFAULT 30,
    included_modules                  text[],
    usage_caps                        jsonb,
    payment_method_required_up_front  boolean DEFAULT false,
    conversion_offer_percent          numeric(18,4),
    notice_days_before_expiry         text[],
    on_expiry                         text DEFAULT 'suspend' CONSTRAINT trial_config_on_expiry_chk CHECK (on_expiry IN ('suspend', 'convert', 'decommission')),
    retain_data_days                  integer DEFAULT 90
);

-- Holds 7 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS subscription.vsi_assessment (
    id                                uuid PRIMARY KEY,
    organisation_name                 text,
    contact_email                     text,
    venue_type                        text,
    answers                           jsonb,
    requested_modules                 text[],
    submitted_at                      timestamptz
);

-- Holds 3 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS subscription.vsi_model (
    version                           integer,
    published_at                      timestamptz,
    id                                uuid PRIMARY KEY NOT NULL
);

