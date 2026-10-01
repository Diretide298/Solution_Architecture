-- subscription — 23 tables
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
    scheduled_change                  jsonb,
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

-- Holds 8 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS subscription.membership_eligibility_rule (
    id                                uuid PRIMARY KEY NOT NULL,
    membership_product_id             uuid NOT NULL,
    dimension                         text NOT NULL CONSTRAINT membership_eligibility_rule_dimension_chk CHECK (dimension IN ('age', 'personType', 'residency', 'country', 'customerSegment', 'corporateAffiliation', 'studentStatus', 'existingMembership', 'previousPurchase', 'membershipHistory', 'channel', 'venue', 'promotionalQualification')),
    operator                          text NOT NULL CONSTRAINT membership_eligibility_rule_operator_chk CHECK (operator IN ('equals', 'notEquals', 'in', 'notIn', 'between', 'atLeast', 'atMost')),
    values                            text[],
    applies_at                        text[],
    scope_path                        ltree NOT NULL,
    created_at                        timestamptz
);

-- Holds 19 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS subscription.membership_entitlement (
    id                                uuid PRIMARY KEY NOT NULL,
    membership_product_id             uuid NOT NULL,
    entitlement_type                  text NOT NULL CONSTRAINT membership_entitlement_entitlement_type_chk CHECK (entitlement_type IN ('unlimitedAdmission', 'limitedAdmissions', 'attractionAccess', 'eventAccess', 'zoneAccess', 'fastTrack', 'priorityEntry', 'guestTickets', 'parking', 'fnbBenefit', 'retailBenefit', 'rentalBenefit', 'specialEventAccess', 'bookingPrivileges', 'other')),
    venue                             text,
    attraction                        text,
    event_type                        text,
    admission_type                    text,
    quantity                          integer,
    limit_period                      text CONSTRAINT membership_entitlement_limit_period_chk CHECK (limit_period IN ('perDay', 'perWeek', 'perMonth', 'perMembershipYear', 'lifetimeOfMembership')),
    days                              text[],
    time_from                         text,
    time_to                           text,
    timeslots                         text[],
    blackout_dates                    text[],
    requires_same_day_visit           boolean,
    pricing_rule_id                   text,
    ownership                         text CONSTRAINT membership_entitlement_ownership_chk CHECK (ownership IN ('memberSpecific', 'familyShared', 'dependentSpecific', 'accountShared')),
    scope_path                        ltree NOT NULL,
    created_at                        timestamptz
);

-- Holds 20 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS subscription.membership_household_policy (
    id                                uuid PRIMARY KEY NOT NULL,
    membership_product_id             uuid NOT NULL,
    minimum_age                       integer,
    maximum_age                       integer,
    relationship_requirement          text CONSTRAINT membership_household_policy_relationship_requirement_chk CHECK (relationship_requirement IN ('none', 'declared', 'verified')),
    verification_requirement          text CONSTRAINT membership_household_policy_verification_requirement_chk CHECK (verification_requirement IN ('none', 'customerDeclaration', 'documentVerification', 'identityVerification', 'staffVerification', 'externalVerification')),
    is_same_household_required        boolean,
    is_member_changes_allowed         boolean,
    member_change_effective           text CONSTRAINT membership_household_policy_member_change_effective_chk CHECK (member_change_effective IN ('immediately', 'nextRenewal')),
    member_changes_per_term           integer,
    member_change_fee                 numeric(18,4),
    is_member_change_approval_required boolean,
    eligibility_revalidation          boolean,
    membership_structure              text NOT NULL CONSTRAINT membership_household_policy_membership_structure_chk CHECK (membership_structure IN ('individual', 'couple', 'family', 'household', 'parentChild', 'corporateGroup', 'custom')),
    entitlement_model                 text CONSTRAINT membership_household_policy_entitlement_model_chk CHECK (entitlement_model IN ('individual', 'shared', 'mixed')),
    age_transition_action             text CONSTRAINT membership_household_policy_age_transition_action_chk CHECK (age_transition_action IN ('gracePeriod', 'upgradeRequired', 'renewalCorrection', 'manualReview')),
    age_transition_grace_days         integer,
    scope_path                        ltree NOT NULL,
    created_at                        timestamptz,
    updated_at                        timestamptz
);

-- Holds 5 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS subscription.membership_household_policy_role_limit (
    id                                uuid PRIMARY KEY,
    membership_household_policy_id    uuid,
    role                              text NOT NULL CONSTRAINT membership_household_policy_role_limit_role_chk CHECK (role IN ('primaryMember', 'secondaryAdult', 'dependent', 'child', 'guardian', 'authorizedManager')),
    min_count                         integer,
    max_count                         integer
);

-- Holds 58 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS subscription.membership_product (
    id                                uuid PRIMARY KEY NOT NULL,
    membership_name                   text NOT NULL,
    membership_code                   text NOT NULL,
    description                       text,
    membership_type                   text NOT NULL CONSTRAINT membership_product_membership_type_chk CHECK (membership_type IN ('annualPass', 'seasonPass', 'monthlyMembership', 'fixedTermMembership', 'corporateMembership', 'familyMembership', 'individualMembership', 'studentMembership', 'vipMembership', 'customMembership')),
    brand                             text,
    venue                             text,
    attraction                        text,
    market                            text,
    currency_context                  text,
    effective_from                    date,
    effective_to                      date,
    tier_level                        integer,
    display_order                     integer,
    parent_membership                 text,
    replacement_membership            text,
    holder_model                      text CONSTRAINT membership_product_holder_model_chk CHECK (holder_model IN ('individual', 'family', 'corporate')),
    is_transferable                   boolean,
    credential_form                   text CONSTRAINT membership_product_credential_form_chk CHECK (credential_form IN ('physical', 'digital', 'both')),
    is_renewable                      boolean,
    is_auto_renew_eligible            boolean,
    benefit_model                     text CONSTRAINT membership_product_benefit_model_chk CHECK (benefit_model IN ('admissionBased', 'benefitBased', 'hybrid')),
    tier                              text,
    upgrade_path                      text[],
    downgrade_path                    text[],
    catalogue_product_id              uuid,
    configured_start                  date,
    configured_end                    date,
    validity_method                   text CONSTRAINT membership_product_validity_method_chk CHECK (validity_method IN ('fixedCalendar', 'durationFromPurchase', 'durationFromActivation', 'seasonBased', 'customPeriod')),
    duration_days                     integer,
    season_name                       text,
    activation_method                 text CONSTRAINT membership_product_activation_method_chk CHECK (activation_method IN ('immediateOnPurchase', 'fixedStartDate', 'firstVisit', 'manualActivation', 'customerActivation', 'membershipCardCollection', 'identityVerification', 'configuredTrigger')),
    activation_deadline_days          integer,
    expiry_rule                       text CONSTRAINT membership_product_expiry_rule_chk CHECK (expiry_rule IN ('exactExpiryDate', 'endOfDay', 'endOfSeason', 'duration')),
    grace_period_days                 integer,
    is_backdating_allowed             boolean,
    is_backdating_approval_required   boolean,
    base_pricing_profile              text,
    tax_profile                       text,
    fee_profile                       text,
    upgrade_price_policy              text,
    promotional_pricing_eligibility   boolean,
    payment_terms                     text[],
    sales_period                      text CONSTRAINT membership_product_sales_period_chk CHECK (sales_period IN ('alwaysAvailable', 'fixedSalesWindow', 'seasonalSale', 'invitationOnly', 'capacityLimited')),
    billing_frequency                 text DEFAULT 'upFront' CONSTRAINT membership_product_billing_frequency_chk CHECK (billing_frequency IN ('upFront', 'monthly', 'quarterly', 'semiAnnual', 'annual', 'custom')),
    billing_interval_months           integer,
    billing_anchor                    text DEFAULT 'purchaseDate' CONSTRAINT membership_product_billing_anchor_chk CHECK (billing_anchor IN ('purchaseDate', 'calendarMonthStart')),
    is_multiple_memberships_allowed   boolean,
    mutually_exclusive_memberships    text[],
    prerequisite_membership           text,
    existing_tier_requirement         text,
    separate_purchase_and_activation_rules boolean,
    verification_method               text CONSTRAINT membership_product_verification_method_chk CHECK (verification_method IN ('none', 'customerDeclaration', 'documentVerification', 'identityVerification', 'staffVerification', 'externalVerification')),
    version                           integer NOT NULL,
    status                            text NOT NULL CONSTRAINT membership_product_status_chk CHECK (status IN ('draft', 'inReview', 'approved', 'scheduled', 'active', 'suspended', 'expired', 'retired')),
    approval_stage                    text CONSTRAINT membership_product_approval_stage_chk CHECK (approval_stage IN ('draft', 'review', 'commercialApproval', 'operationalApproval', 'approved', 'scheduled', 'published')),
    approval_request_id               uuid,
    published_at                      timestamptz,
    scope_path                        ltree NOT NULL,
    created_at                        timestamptz,
    updated_at                        timestamptz
);

-- Holds 14 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS subscription.membership_product_history (
    id                                uuid PRIMARY KEY NOT NULL,
    membership_product_id             uuid NOT NULL,
    action                            text NOT NULL CONSTRAINT membership_product_history_action_chk CHECK (action IN ('validate', 'submitForReview', 'approveCommercial', 'approveOperational', 'reject', 'schedule', 'publish')),
    from_status                       text CONSTRAINT membership_product_history_from_status_chk CHECK (from_status IN ('draft', 'inReview', 'approved', 'scheduled', 'active', 'suspended', 'expired', 'retired')),
    to_status                         text CONSTRAINT membership_product_history_to_status_chk CHECK (to_status IN ('draft', 'inReview', 'approved', 'scheduled', 'active', 'suspended', 'expired', 'retired')),
    previous_version                  integer,
    new_version                       integer,
    effective_from                    date,
    migration_policy                  text CONSTRAINT membership_product_history_migration_policy_chk CHECK (migration_policy IN ('remainOnCurrentVersion', 'moveAtNextRenewal', 'moveOnEffectiveDate')),
    reason                            text,
    approval_request_id               uuid,
    changed_by_principal_id           uuid NOT NULL,
    scope_path                        ltree NOT NULL,
    occurred_at                       timestamptz NOT NULL
);

-- Holds 21 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS subscription.membership_renewal_policy (
    id                                uuid PRIMARY KEY NOT NULL,
    membership_product_id             uuid NOT NULL,
    is_auto_renew_eligible            boolean,
    auto_renew_terms_version          text,
    is_card_on_file_required          boolean,
    pre_renewal_notice_days           integer,
    failure_handling                  text CONSTRAINT membership_renewal_policy_failure_handling_chk CHECK (failure_handling IN ('gracePeriod', 'manualAction', 'expire')),
    renewal_modes                     text[],
    renewal_window_opens_days_before  integer,
    renewal_window_closes_days_after  integer,
    early_renewal_start               text CONSTRAINT membership_renewal_policy_early_renewal_start_chk CHECK (early_renewal_start IN ('immediately', 'afterCurrentExpiry')),
    renewal_price_basis               text CONSTRAINT membership_renewal_policy_renewal_price_basis_chk CHECK (renewal_price_basis IN ('currentMembershipPrice', 'protectedRenewalPrice', 'renewalDiscount', 'loyaltyRate', 'fixedRenewalRate')),
    renewal_pricing_profile           text,
    retry_intervals_days              integer[],
    renewal_grace_days                integer,
    revalidate_on_renewal             text[],
    tier_movement_at_renewal          text[],
    cancellation_policy_id            text,
    scope_path                        ltree NOT NULL,
    created_at                        timestamptz,
    updated_at                        timestamptz
);

-- Holds 22 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS subscription.membership_usage_policy (
    id                                uuid PRIMARY KEY NOT NULL,
    membership_product_id             uuid NOT NULL,
    maximum_visits_per_day            integer,
    maximum_admissions_per_period     integer,
    re_entry_cooldown_minutes         integer,
    concurrent_reservations           integer,
    no_show_treatment                 text CONSTRAINT membership_usage_policy_no_show_treatment_chk CHECK (no_show_treatment IN ('none', 'restrictReservations')),
    cancellation_limit                integer,
    guest_usage                       text CONSTRAINT membership_usage_policy_guest_usage_chk CHECK (guest_usage IN ('withMemberOnly', 'independent')),
    benefit_consumption               text CONSTRAINT membership_usage_policy_benefit_consumption_chk CHECK (benefit_consumption IN ('onRedemption', 'onValidatedVisit')),
    is_walk_in_allowed                boolean,
    maximum_advance_booking_days      integer,
    maximum_active_future_reservations integer,
    admission_period                  text CONSTRAINT membership_usage_policy_admission_period_chk CHECK (admission_period IN ('perDay', 'perWeek', 'perMonth', 'perMembershipYear')),
    re_entry_policy                   text CONSTRAINT membership_usage_policy_re_entry_policy_chk CHECK (re_entry_policy IN ('unlimitedSameDay', 'noReEntry', 'afterMinutes', 'venueSpecific')),
    reservation_requirement           text CONSTRAINT membership_usage_policy_reservation_requirement_chk CHECK (reservation_requirement IN ('required', 'optional')),
    no_show_threshold                 integer,
    no_show_window_days               integer,
    no_show_restriction_days          integer,
    scope_path                        ltree NOT NULL,
    created_at                        timestamptz,
    updated_at                        timestamptz
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
    pricing_basis                     text CONSTRAINT module_listing_pricing_basis_chk CHECK (pricing_basis IN ('included', 'flatFee', 'perVenue', 'perUnit', 'revenueShare', 'metered')),
    metered_metric                    text,
    metered_unit_size                 integer,
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
    request_limits                    jsonb,
    package_kind                      text DEFAULT 'standard' CONSTRAINT plan_package_kind_chk CHECK (package_kind IN ('standard', 'custom')),
    offered_to_tenant_id              uuid,
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
    notice_days_before_expiry         integer[],
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

