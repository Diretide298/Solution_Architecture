-- subscription — 13 tables
-- **Derived. Do not hand-edit.**

-- Holds 10 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS subscription.capacity_pack (
    id                                uuid PRIMARY KEY,
    tenant_id                         uuid NOT NULL,
    unit                              text NOT NULL,
    quantity                          integer NOT NULL,
    price                             numeric(18,4),
    valid_from                        date,
    valid_to                          date,
    temporary                         boolean,
    approved_by                       uuid,
    invoice_id                        uuid
);

-- What a tenant is paying for, and which modules that licenses
CREATE TABLE IF NOT EXISTS subscription.contract (
    tenant_id                         uuid NOT NULL,
    plan_id                           uuid NOT NULL,
    plan_name                         text,
    plan_version                      text NOT NULL,
    status                            text NOT NULL,
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
    hard_stop_allowed                 boolean,
    grace_days                        integer
);

-- Holds 8 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS subscription.go_live_readiness (
    tenant_id                         uuid,
    run_at                            timestamptz,
    status                            text,
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
    billable_unit                     text NOT NULL,
    unit_price                        numeric(18,4),
    revenue_share_percent             numeric(18,4),
    minimum_guarantee                 numeric(18,4),
    minimum_guarantee_period          text,
    on_below_minimum                  text,
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
    price                             numeric(18,4),
    pricing_basis                     text,
    provisioning_minutes              integer,
    requires_professional_services    boolean,
    status                            text,
    id                                uuid PRIMARY KEY NOT NULL
);

-- Holds 8 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS subscription.partner_quote (
    id                                uuid PRIMARY KEY NOT NULL,
    partner_id                        uuid,
    agreement_id                      uuid,
    total_minor                       integer,
    state                             text,
    valid_until                       timestamptz,
    created_at                        timestamptz
);

-- What a tenant pays for — the modules, the limits, the price. Renamed from plan, which sat beside
-- migration_plan and production_plan
CREATE TABLE IF NOT EXISTS subscription.plan (
    code                              text,
    name                              text,
    description                       text,
    cell_tier                         text,
    base_price                        numeric(18,4),
    billing_period                    text,
    includes_branded_app              boolean,
    included_ai_tokens                integer,
    id                                uuid PRIMARY KEY,
    version                           text,
    is_active                         boolean,
    subscriber_count                  integer,
    published_at                      timestamptz
);

CREATE TABLE IF NOT EXISTS subscription.tier_allowance (
    id                                uuid PRIMARY KEY,
    tier_id                           uuid NOT NULL,
    code                              text NOT NULL,
    name                              text NOT NULL,
    limit_value                       numeric(18,4),
    period                            text,
    is_unlimited                      boolean NOT NULL,
    is_active                         boolean NOT NULL,
    created_at                        timestamptz NOT NULL,
    updated_at                        timestamptz
);

CREATE TABLE IF NOT EXISTS subscription.tier_module (
    id                                uuid PRIMARY KEY,
    tier_id                           uuid NOT NULL,
    code                              text NOT NULL,
    is_included                       boolean NOT NULL,
    notes                             text,
    is_active                         boolean NOT NULL,
    created_at                        timestamptz NOT NULL,
    updated_at                        timestamptz
);

-- Holds 10 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS subscription.trial_config (
    id                                uuid PRIMARY KEY,
    tier_code                         text,
    duration_days                     integer,
    included_modules                  text[],
    usage_caps                        jsonb,
    payment_method_required_up_front  boolean,
    conversion_offer_percent          numeric(18,4),
    notice_days_before_expiry         text[],
    on_expiry                         text,
    retain_data_days                  integer
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

