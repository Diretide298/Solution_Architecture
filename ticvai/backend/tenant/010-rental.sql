-- rental — 24 tables
-- **Derived. Do not hand-edit.**

-- Holds 13 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS rental.agreement (
    id                                uuid PRIMARY KEY,
    rental_number                     text NOT NULL CONSTRAINT agreement_rental_number_chk CHECK (char_length(rental_number) <= 50),
    order_id                          uuid NOT NULL,
    customer_id                       uuid NOT NULL,
    venue_id                          uuid NOT NULL,
    scheduled_start_at                timestamptz NOT NULL,
    scheduled_return_at               timestamptz NOT NULL,
    actual_start_at                   timestamptz,
    actual_return_at                  timestamptz,
    status                            text NOT NULL CONSTRAINT agreement_status_chk CHECK (char_length(status) <= 30),
    overdue_minutes                   integer NOT NULL,
    created_at                        timestamptz,
    updated_at                        timestamptz
);

-- Holds 19 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS rental.agreement_item (
    id                                uuid PRIMARY KEY,
    rental_agreement_id               uuid NOT NULL,
    order_line_id                     uuid NOT NULL,
    catalogue_product_id              uuid NOT NULL,
    tracking_mode                     text NOT NULL CONSTRAINT agreement_item_tracking_mode_chk CHECK (char_length(tracking_mode) <= 30),
    resource_booking_id               uuid,
    resource_id                       uuid,
    asset_id                          uuid,
    inventory_item_id                 uuid,
    stock_reservation_id              uuid,
    quantity_booked                   numeric(18,4) NOT NULL,
    quantity_checked_out              numeric(18,4) NOT NULL,
    quantity_returned                 numeric(18,4) NOT NULL,
    quantity_missing                  numeric(18,4) NOT NULL,
    status                            text CONSTRAINT agreement_item_status_chk CHECK (char_length(status) <= 30),
    checked_out_at                    timestamptz,
    returned_at                       timestamptz,
    created_at                        timestamptz,
    updated_at                        timestamptz
);

-- Holds 10 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS rental.agreement_rules (
    customer_fields                   jsonb,
    is_agreement_required             boolean DEFAULT false,
    is_liability_waiver_required      boolean DEFAULT false,
    terms_document_asset_id           uuid,
    agreement_version                 text,
    is_e_signature_required           boolean DEFAULT false,
    guardian_signature_for_minor      boolean DEFAULT true,
    group_waiver_mode                 text DEFAULT 'perParticipant' CONSTRAINT agreement_rules_group_waiver_mode_chk CHECK (group_waiver_mode IN ('perParticipant', 'singleGroupWaiver')),
    scope_path                        ltree NOT NULL,
    id                                uuid PRIMARY KEY NOT NULL
);

-- Holds 10 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS rental.agreement_signature (
    id                                uuid PRIMARY KEY,
    participant_id                    uuid,
    agreement_version                 text NOT NULL,
    signatory_name                    text,
    signatory_role                    text CONSTRAINT agreement_signature_signatory_role_chk CHECK (signatory_role IN ('renter', 'participant', 'guardian')),
    signature_asset_id                uuid,
    document_asset_id                 uuid,
    signed_at                         timestamptz,
    ip_address                        text,
    scope_path                        ltree NOT NULL
);

-- Holds 6 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS rental.availability_rules (
    slot_minutes                      integer,
    hold_minutes                      integer DEFAULT 15,
    release_on_payment_failure        boolean DEFAULT true,
    overbook_percent                  numeric(18,4) DEFAULT 0,
    scope_path                        ltree NOT NULL,
    id                                uuid PRIMARY KEY NOT NULL
);

-- Holds 8 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS rental.blackout (
    id                                uuid PRIMARY KEY,
    product_id                        uuid,
    location_id                       uuid,
    valid_from                        timestamptz NOT NULL,
    valid_to                          timestamptz NOT NULL,
    reason                            text NOT NULL,
    capacity_percent                  integer DEFAULT 0,
    scope_path                        ltree NOT NULL
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
    valid_from                        timestamptz NOT NULL,
    valid_to                          timestamptz NOT NULL,
    quantity                          integer,
    status                            text NOT NULL CONSTRAINT booking_status_chk CHECK (status IN ('draft', 'confirmed', 'awaitingArrival', 'checkedOut', 'overdue', 'partiallyReturned', 'completed', 'completedWithDamage', 'notReturned', 'cancelled', 'noShow')),
    checked_out_at                    timestamptz,
    due_back_at                       timestamptz,
    returned_at                       timestamptz,
    deposit_authorisation_id          uuid,
    accrued_late_fee                  numeric(18,4),
    scope_path                        ltree NOT NULL
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
    customer_acknowledgement          text DEFAULT 'notPresented' CONSTRAINT damage_assessment_customer_acknowledgement_chk CHECK (customer_acknowledgement IN ('accepted', 'disputed', 'notPresented')),
    work_order_id                     uuid,
    scope_path                        ltree NOT NULL
);

-- Holds 17 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS rental.deposit_policy (
    id                                uuid PRIMARY KEY,
    product_id                        uuid,
    category_id                       uuid,
    is_required                       boolean DEFAULT true,
    basis                             text CONSTRAINT deposit_policy_basis_chk CHECK (basis IN ('fixed', 'percentage', 'riskBased')),
    fixed_amount                      numeric(18,4),
    percentage                        numeric(18,4),
    minimum_amount                    numeric(18,4),
    maximum_amount                    numeric(18,4),
    instruments                       text[],
    is_auto_release                   boolean DEFAULT true,
    inspection_required_before_release boolean DEFAULT false,
    auto_release_delay_hours          integer DEFAULT 0,
    is_partial_capture_permitted      boolean DEFAULT true,
    supervisor_approval_threshold     numeric(18,4),
    is_waiver_eligible                boolean DEFAULT false,
    scope_path                        ltree NOT NULL
);

-- Holds 11 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS rental.duration_rules (
    minimum_minutes                   integer,
    maximum_minutes                   integer,
    increment_minutes                 integer DEFAULT 15,
    default_minutes                   integer,
    turnaround_minutes                integer DEFAULT 0,
    is_extension_allowed              boolean DEFAULT true,
    maximum_extension_minutes         integer,
    is_same_day_return_required       boolean DEFAULT false,
    is_overnight_allowed              boolean DEFAULT false,
    scope_path                        ltree NOT NULL,
    id                                uuid PRIMARY KEY NOT NULL
);

-- Holds 8 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS rental.equipment_assignment (
    id                                uuid PRIMARY KEY,
    asset_id                          uuid NOT NULL,
    serial_number                     text,
    scanned_code                      text,
    assigned_manually                 boolean DEFAULT false,
    assigned_at                       timestamptz,
    returned_at                       timestamptz,
    scope_path                        ltree NOT NULL
);

-- Holds 10 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS rental.fee_policy (
    id                                uuid PRIMARY KEY,
    product_id                        uuid,
    grace_period_minutes              integer DEFAULT 0,
    late_fee_basis                    text CONSTRAINT fee_policy_late_fee_basis_chk CHECK (late_fee_basis IN ('fixed', 'perMinute', 'per15Minutes', 'per30Minutes', 'perHour', 'tiered')),
    late_fee_amount                   numeric(18,4),
    maximum_daily_charge              numeric(18,4),
    extension_price_per_increment     numeric(18,4),
    extension_increment_minutes       integer DEFAULT 30,
    not_returned_after_hours          integer,
    damage_fee_maximum                numeric(18,4),
    damage_fee_approval_above         numeric(18,4),
    missing_item_fee_basis            text CONSTRAINT fee_policy_missing_item_fee_basis_chk CHECK (missing_item_fee_basis IN ('replacementCost', 'fixedAmount')),
    missing_item_fee_amount           numeric(18,4),
    scope_path                        ltree NOT NULL
);

-- Holds 12 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS rental.incident (
    id                                uuid PRIMARY KEY,
    booking_id                        uuid,
    asset_id                          uuid,
    kind                              text NOT NULL CONSTRAINT incident_kind_chk CHECK (kind IN ('injury', 'loss', 'theft', 'complaint', 'equipmentFailure', 'safetyBreach', 'other')),
    description                       text NOT NULL,
    severity                          text CONSTRAINT incident_severity_chk CHECK (severity IN ('low', 'medium', 'high', 'critical')),
    reported_by                       uuid,
    reported_at                       timestamptz,
    photo_asset_ids                   text[],
    work_order_id                     uuid,
    is_authority_notified             boolean DEFAULT false,
    scope_path                        ltree NOT NULL
);

-- Holds 9 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS rental.inspection (
    id                                uuid PRIMARY KEY,
    asset_id                          uuid,
    phase                             text NOT NULL CONSTRAINT inspection_phase_chk CHECK (phase IN ('preRental', 'postRental')),
    condition                         text NOT NULL CONSTRAINT inspection_condition_chk CHECK (condition IN ('good', 'minorDamage', 'majorDamage', 'faulty', 'notReturned')),
    note                              text,
    photo_asset_ids                   text[],
    inspected_by                      uuid,
    inspected_at                      timestamptz,
    scope_path                        ltree NOT NULL
);

-- Holds 9 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS rental.inspection_item (
    id                                uuid PRIMARY KEY,
    rental_inspection_id              uuid NOT NULL,
    rental_agreement_item_id          uuid NOT NULL,
    component_code                    text CONSTRAINT inspection_item_component_code_chk CHECK (char_length(component_code) <= 100),
    component_name                    text CONSTRAINT inspection_item_component_name_chk CHECK (char_length(component_name) <= 200),
    condition_status                  text NOT NULL CONSTRAINT inspection_item_condition_status_chk CHECK (char_length(condition_status) <= 30),
    severity                          text CONSTRAINT inspection_item_severity_chk CHECK (char_length(severity) <= 20),
    note                              text CONSTRAINT inspection_item_note_chk CHECK (char_length(note) <= 1000),
    created_at                        timestamptz NOT NULL
);

-- Holds 10 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS rental.inventory_model (
    tracking_model                    text NOT NULL CONSTRAINT inventory_model_tracking_model_chk CHECK (tracking_model IN ('pooled', 'serialised', 'hybrid')),
    inventory_unit                    text,
    total_quantity                    integer,
    assignment_required_at_checkout   boolean DEFAULT false,
    is_scan_required                  boolean DEFAULT false,
    allow_manual_assignment           boolean DEFAULT true,
    allow_substitution                boolean DEFAULT true,
    allow_equipment_swap              boolean DEFAULT true,
    scope_path                        ltree NOT NULL,
    id                                uuid PRIMARY KEY NOT NULL
);

-- Holds 10 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS rental.location_rule (
    location_id                       uuid NOT NULL,
    is_enabled                        boolean DEFAULT true,
    is_pickup_allowed                 boolean DEFAULT true,
    is_return_allowed                 boolean DEFAULT true,
    is_cross_location_return_allowed  boolean DEFAULT false,
    inventory_allocation              integer,
    inventory_buffer                  integer DEFAULT 0,
    operating_hours                   jsonb,
    scope_path                        ltree NOT NULL,
    id                                uuid PRIMARY KEY NOT NULL
);

-- Holds 20 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS rental.operational_rules (
    minimum_age                       integer,
    maximum_age                       integer,
    minimum_height_cm                 integer,
    maximum_weight_kg                 integer,
    id_required                       text DEFAULT 'notApplicable' CONSTRAINT operational_rules_id_required_chk CHECK (id_required IN ('required', 'optional', 'notApplicable')),
    guardian_required                 text DEFAULT 'notApplicable' CONSTRAINT operational_rules_guardian_required_chk CHECK (guardian_required IN ('required', 'optional', 'notApplicable')),
    membership_required               text DEFAULT 'notApplicable' CONSTRAINT operational_rules_membership_required_chk CHECK (membership_required IN ('required', 'optional', 'notApplicable')),
    driving_licence_required          text DEFAULT 'notApplicable' CONSTRAINT operational_rules_driving_licence_required_chk CHECK (driving_licence_required IN ('required', 'optional', 'notApplicable')),
    safety_briefing_required          text DEFAULT 'notApplicable' CONSTRAINT operational_rules_safety_briefing_required_chk CHECK (safety_briefing_required IN ('required', 'optional', 'notApplicable')),
    checkout_scan_required            text DEFAULT 'notApplicable' CONSTRAINT operational_rules_checkout_scan_required_chk CHECK (checkout_scan_required IN ('required', 'optional', 'notApplicable')),
    return_scan_required              text DEFAULT 'notApplicable' CONSTRAINT operational_rules_return_scan_required_chk CHECK (return_scan_required IN ('required', 'optional', 'notApplicable')),
    condition_inspection_required     text DEFAULT 'notApplicable' CONSTRAINT operational_rules_condition_inspection_required_chk CHECK (condition_inspection_required IN ('required', 'optional', 'notApplicable')),
    photo_at_checkout_required        text DEFAULT 'notApplicable' CONSTRAINT operational_rules_photo_at_checkout_required_chk CHECK (photo_at_checkout_required IN ('required', 'optional', 'notApplicable')),
    photo_at_return_required          text DEFAULT 'notApplicable' CONSTRAINT operational_rules_photo_at_return_required_chk CHECK (photo_at_return_required IN ('required', 'optional', 'notApplicable')),
    maximum_quantity_per_customer     integer,
    is_return_location_restricted     boolean DEFAULT false,
    is_partial_return_allowed         boolean DEFAULT true,
    is_staff_approval_required        boolean DEFAULT false,
    scope_path                        ltree NOT NULL,
    id                                uuid PRIMARY KEY NOT NULL
);

-- Holds 11 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS rental.override (
    id                                uuid PRIMARY KEY,
    booking_id                        uuid,
    kind                              text NOT NULL CONSTRAINT override_kind_chk CHECK (kind IN ('priceOverride', 'complimentary', 'depositWaiver', 'depositReduction', 'lateFeeWaiver', 'damageFeeWaiver', 'extensionFeeWaiver', 'manualRefund', 'goodwill')),
    original_amount                   numeric(18,4),
    adjusted_amount                   numeric(18,4),
    reason                            text NOT NULL,
    requested_by                      uuid,
    approved_by                       uuid,
    approval_request_id               uuid,
    at                                timestamptz,
    scope_path                        ltree NOT NULL
);

-- Holds 9 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS rental.participant (
    id                                uuid PRIMARY KEY,
    name                              text,
    is_primary_renter                 boolean DEFAULT false,
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
    model                             text NOT NULL CONSTRAINT pricing_profile_model_chk CHECK (model IN ('flat', 'durationBased', 'tiered', 'peakOffPeak', 'weekend', 'seasonal', 'dynamic', 'hybrid')),
    base_price                        numeric(18,4),
    minimum_charge                    numeric(18,4),
    billing_increment_minutes         integer,
    additional_increment_price        numeric(18,4),
    rounding                          text DEFAULT 'exactUsage' CONSTRAINT pricing_profile_rounding_chk CHECK (rounding IN ('exactUsage', 'roundUp15', 'roundUp30', 'roundUpHour')),
    is_dynamic_enabled                boolean DEFAULT false,
    dynamic_max_increase_percent      numeric(18,4) DEFAULT 25,
    dynamic_max_decrease_percent      numeric(18,4) DEFAULT 15,
    priority                          integer DEFAULT 0,
    effective_from                    date,
    effective_to                      date,
    status                            text CONSTRAINT pricing_profile_status_chk CHECK (status IN ('draft', 'pendingApproval', 'active', 'scheduled', 'expired')),
    scope_path                        ltree NOT NULL
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
    scope_path                        ltree NOT NULL,
    tracking_model                    text CONSTRAINT product_tracking_model_chk CHECK (tracking_model IN ('pooled', 'serialised', 'hybrid')),
    catalogue_product_id              uuid,
    resource_type_id                  uuid,
    status                            text CONSTRAINT product_status_chk CHECK (status IN ('draft', 'configurationReview', 'approved', 'active', 'suspended', 'archived')),
    effective_from                    timestamptz,
    version                           integer DEFAULT 1,
    is_active                         boolean DEFAULT true
);

-- Holds 17 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS rental.quote (
    quote_id                          uuid PRIMARY KEY NOT NULL,
    product_id                        uuid NOT NULL,
    location_id                       uuid,
    valid_from                        timestamptz NOT NULL,
    valid_to                          timestamptz NOT NULL,
    quantity                          integer DEFAULT 1,
    customer_id                       uuid,
    rental_amount                     numeric(18,4) NOT NULL,
    tax_amount                        numeric(18,4),
    add_on_amount                     numeric(18,4),
    discount_amount                   numeric(18,4),
    total_payable                     numeric(18,4),
    deposit_amount                    numeric(18,4) NOT NULL,
    deposit_instrument                text,
    expires_at                        timestamptz,
    created_at                        timestamptz,
    scope_path                        ltree NOT NULL
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
    gross_charged_amount              numeric(18,4),
    deposit_captured                  numeric(18,4),
    deposit_released                  numeric(18,4),
    balance_due                       numeric(18,4),
    outcome                           text CONSTRAINT settlement_outcome_chk CHECK (outcome IN ('completed', 'completedWithDamage', 'partiallyReturned', 'notReturned')),
    scope_path                        ltree NOT NULL,
    id                                uuid PRIMARY KEY NOT NULL
);

