-- subscription — 9 tables
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

