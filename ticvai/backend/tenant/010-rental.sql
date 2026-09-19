-- rental — 21 tables
-- **Derived. Do not hand-edit.**

-- Holds 10 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS rental.agreement_rules (
    customer_fields                   jsonb,
    agreement_required                boolean,
    liability_waiver_required         boolean,
    terms_document_asset_id           uuid,
    agreement_version                 text,
    e_signature_required              boolean,
    guardian_signature_for_minor      boolean,
    group_waiver_mode                 text,
    scope_path                        text,
    id                                uuid PRIMARY KEY NOT NULL
);

-- Holds 10 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS rental.agreement_signature (
    id                                uuid PRIMARY KEY,
    participant_id                    uuid,
    agreement_version                 text NOT NULL,
    signatory_name                    text,
    signatory_role                    text,
    signature_asset_id                uuid,
    document_asset_id                 uuid,
    signed_at                         timestamptz,
    ip_address                        text,
    scope_path                        text
);

-- Holds 6 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS rental.availability_rules (
    slot_minutes                      integer,
    hold_minutes                      integer,
    release_on_payment_failure        boolean,
    overbook_percent                  numeric(18,4),
    scope_path                        text,
    id                                uuid PRIMARY KEY NOT NULL
);

-- Holds 8 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS rental.blackout (
    id                                uuid PRIMARY KEY,
    product_id                        uuid,
    location_id                       uuid,
    "from"                            timestamptz NOT NULL,
    "to"                              timestamptz NOT NULL,
    reason                            text NOT NULL,
    capacity_percent                  integer,
    scope_path                        text
);

-- Holds 17 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS rental.booking (
    id                                uuid PRIMARY KEY NOT NULL,
    reference                         text,
    product_id                        uuid NOT NULL,
    location_id                       uuid,
    return_location_id                uuid,
    customer_id                       uuid,
    order_id                          uuid,
    "from"                            timestamptz NOT NULL,
    "to"                              timestamptz NOT NULL,
    quantity                          integer,
    status                            text NOT NULL,
    checked_out_at                    timestamptz,
    due_back_at                       timestamptz,
    returned_at                       timestamptz,
    deposit_authorisation_id          uuid,
    accrued_late_fee                  numeric(18,4),
    scope_path                        text
);

-- Holds 14 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS rental.category (
    id                                uuid PRIMARY KEY,
    code                              text NOT NULL,
    name                              text NOT NULL,
    description                       text,
    parent_category_id                uuid,
    icon_asset_id                     uuid,
    default_tracking_model            text,
    default_duration_minutes          integer,
    default_turnaround_minutes        integer,
    default_waiver_required           boolean,
    default_deposit_policy_id         uuid,
    overridable_fields                text[],
    scope_path                        text,
    is_active                         boolean
);

-- Holds 10 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS rental.damage_assessment (
    id                                uuid PRIMARY KEY,
    asset_id                          uuid,
    description                       text NOT NULL,
    amount                            numeric(18,4) NOT NULL,
    inspection_id                     uuid,
    assessed_by                       uuid,
    approved_by                       uuid,
    customer_acknowledgement          text,
    work_order_id                     uuid,
    scope_path                        text
);

-- Holds 17 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS rental.deposit_policy (
    id                                uuid PRIMARY KEY,
    product_id                        uuid,
    category_id                       uuid,
    required                          boolean,
    basis                             text,
    fixed_amount                      numeric(18,4),
    percentage                        numeric(18,4),
    minimum_amount                    numeric(18,4),
    maximum_amount                    numeric(18,4),
    instruments                       text[],
    auto_release                      boolean,
    inspection_required_before_releaseboolean,
    auto_release_delay_hours          integer,
    partial_capture_permitted         boolean,
    supervisor_approval_threshold     numeric(18,4),
    waiver_eligible                   boolean,
    scope_path                        text
);

-- Holds 11 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS rental.duration_rules (
    minimum_minutes                   integer,
    maximum_minutes                   integer,
    increment_minutes                 integer,
    default_minutes                   integer,
    turnaround_minutes                integer,
    extension_allowed                 boolean,
    maximum_extension_minutes         integer,
    same_day_return_required          boolean,
    overnight_allowed                 boolean,
    scope_path                        text,
    id                                uuid PRIMARY KEY NOT NULL
);

-- Holds 8 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS rental.equipment_assignment (
    id                                uuid PRIMARY KEY,
    asset_id                          uuid NOT NULL,
    serial_number                     text,
    scanned_code                      text,
    assigned_manually                 boolean,
    assigned_at                       timestamptz,
    returned_at                       timestamptz,
    scope_path                        text
);

-- Holds 10 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS rental.fee_policy (
    id                                uuid PRIMARY KEY,
    product_id                        uuid,
    grace_period_minutes              integer,
    late_fee_basis                    text,
    late_fee_amount                   numeric(18,4),
    maximum_daily_charge              numeric(18,4),
    extension_price_per_increment     numeric(18,4),
    extension_increment_minutes       integer,
    not_returned_after_hours          integer,
    scope_path                        text
);

-- Holds 12 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS rental.incident (
    id                                uuid PRIMARY KEY,
    booking_id                        uuid,
    asset_id                          uuid,
    kind                              text NOT NULL,
    description                       text NOT NULL,
    severity                          text,
    reported_by                       uuid,
    reported_at                       timestamptz,
    photo_asset_ids                   text[],
    work_order_id                     uuid,
    authority_notified                boolean,
    scope_path                        text
);

-- Holds 9 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS rental.inspection (
    id                                uuid PRIMARY KEY,
    asset_id                          uuid,
    phase                             text NOT NULL,
    condition                         text NOT NULL,
    note                              text,
    photo_asset_ids                   text[],
    inspected_by                      uuid,
    inspected_at                      timestamptz,
    scope_path                        text
);

-- Holds 10 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS rental.inventory_model (
    tracking_model                    text NOT NULL,
    inventory_unit                    text,
    total_quantity                    integer,
    assignment_required_at_checkout   boolean,
    scan_required                     boolean,
    allow_manual_assignment           boolean,
    allow_substitution                boolean,
    allow_equipment_swap              boolean,
    scope_path                        text,
    id                                uuid PRIMARY KEY NOT NULL
);

-- Holds 10 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS rental.location_rule (
    location_id                       uuid NOT NULL,
    enabled                           boolean,
    pickup_allowed                    boolean,
    return_allowed                    boolean,
    cross_location_return_allowed     boolean,
    inventory_allocation              integer,
    inventory_buffer                  integer,
    operating_hours                   jsonb,
    scope_path                        text,
    id                                uuid PRIMARY KEY NOT NULL
);

-- Holds 20 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS rental.operational_rules (
    minimum_age                       integer,
    maximum_age                       integer,
    minimum_height_cm                 integer,
    maximum_weight_kg                 integer,
    id_required                       text,
    guardian_required                 text,
    membership_required               text,
    driving_licence_required          text,
    safety_briefing_required          text,
    checkout_scan_required            text,
    return_scan_required              text,
    condition_inspection_required     text,
    photo_at_checkout_required        text,
    photo_at_return_required          text,
    maximum_quantity_per_customer     integer,
    return_location_restricted        boolean,
    partial_return_allowed            boolean,
    staff_approval_required           boolean,
    scope_path                        text,
    id                                uuid PRIMARY KEY NOT NULL
);

-- Holds 11 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS rental.override (
    id                                uuid PRIMARY KEY,
    booking_id                        uuid,
    kind                              text NOT NULL,
    original_amount                   numeric(18,4),
    adjusted_amount                   numeric(18,4),
    reason                            text NOT NULL,
    requested_by                      uuid,
    approved_by                       uuid,
    approval_request_id               uuid,
    at                                timestamptz,
    scope_path                        text
);

-- Holds 9 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS rental.participant (
    id                                uuid PRIMARY KEY,
    name                              text,
    is_primary_renter                 boolean,
    date_of_birth                     date,
    id_number                         text,
    guardian_name                     text,
    emergency_contact                 text,
    has_signed_waiver                 boolean,
    custom_fields                     jsonb
);

-- Holds 23 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS rental.pricing_profile (
    id                                uuid PRIMARY KEY,
    code                              text NOT NULL,
    name                              text NOT NULL,
    product_id                        uuid,
    venue_id                          uuid,
    location_ids                      text[],
    sales_channel                     text,
    customer_segment_id               uuid,
    model                             text NOT NULL,
    base_price                        numeric(18,4),
    minimum_charge                    numeric(18,4),
    billing_increment_minutes         integer,
    additional_increment_price        numeric(18,4),
    rounding                          text,
    dynamic_enabled                   boolean,
    dynamic_max_increase_percent      numeric(18,4),
    dynamic_max_decrease_percent      numeric(18,4),
    priority                          integer,
    effective_from                    date,
    effective_to                      date,
    status                            text,
    scope_path                        text
);

-- Holds 18 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS rental.product (
    id                                uuid PRIMARY KEY,
    code                              text NOT NULL,
    name                              text NOT NULL,
    internal_name                     text,
    description                       text,
    category_id                       uuid,
    image_asset_id                    uuid,
    tags                              text[],
    tenant_id                         uuid,
    venue_id                          uuid NOT NULL,
    scope_path                        text,
    tracking_model                    text,
    catalogue_product_id              uuid,
    resource_type_id                  uuid,
    status                            text,
    effective_from                    timestamptz,
    version                           integer,
    is_active                         boolean
);

-- Holds 15 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS rental.settlement (
    booking_id                        uuid,
    expected_return_at                timestamptz,
    actual_return_at                  timestamptz,
    grace_period_minutes              integer,
    chargeable_late_minutes           integer,
    late_fee                          numeric(18,4),
    damage_fee                        numeric(18,4),
    missing_item_fee                  numeric(18,4),
    total_charged                     numeric(18,4),
    deposit_captured                  numeric(18,4),
    deposit_released                  numeric(18,4),
    balance_due                       numeric(18,4),
    outcome                           text,
    scope_path                        text,
    id                                uuid PRIMARY KEY NOT NULL
);

