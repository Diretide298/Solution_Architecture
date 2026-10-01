-- catalogue — 80 tables
-- **Derived. Do not hand-edit.**

-- Holds 13 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS catalogue.ai_catalogue_session (
    id                                uuid PRIMARY KEY NOT NULL,
    scope_path                        ltree NOT NULL,
    venue_id                          uuid,
    input_method                      text NOT NULL CONSTRAINT ai_catalogue_session_input_method_chk CHECK (input_method IN ('naturalLanguage', 'excel', 'csv', 'pdf', 'brochure', 'existingCatalogue', 'referenceProduct')),
    prompt                            text,
    file_id                           uuid,
    reference_product_id              uuid,
    recommendations                   jsonb,
    draft_product_id                  uuid,
    status                            text NOT NULL DEFAULT 'open' CONSTRAINT ai_catalogue_session_status_chk CHECK (status IN ('open', 'draftCreated', 'abandoned')),
    created_by_principal_id           uuid,
    created_at                        timestamptz,
    updated_at                        timestamptz
);

-- Holds 23 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS catalogue.ai_finding (
    id                                uuid PRIMARY KEY NOT NULL,
    scope_path                        ltree NOT NULL,
    domain                            text NOT NULL CONSTRAINT ai_finding_domain_chk CHECK (domain IN ('productGovernance', 'channel')),
    finding_type                      text NOT NULL CONSTRAINT ai_finding_finding_type_chk CHECK (char_length(finding_type) <= 60),
    product_id                        uuid,
    venue_id                          uuid,
    sales_channel_ids                 text[],
    severity                          text CONSTRAINT ai_finding_severity_chk CHECK (severity IN ('critical', 'high', 'medium', 'low')),
    confidence                        numeric(18,4),
    summary                           text,
    explanation                       text,
    business_impact                   text,
    recommended_action                text,
    constraints                       text[],
    signals                           text[],
    simulation                        jsonb,
    required_approval                 text CONSTRAINT ai_finding_required_approval_chk CHECK (char_length(required_approval) <= 100),
    owner_principal_id                uuid,
    due_date                          date,
    status                            text NOT NULL DEFAULT 'open' CONSTRAINT ai_finding_status_chk CHECK (status IN ('open', 'acknowledged', 'accepted', 'dismissed', 'resolved')),
    model_version                     text CONSTRAINT ai_finding_model_version_chk CHECK (char_length(model_version) <= 60),
    detected_at                       timestamptz NOT NULL,
    resolved_at                       timestamptz
);

-- Another way to name the same product — a barcode, a supplier code, a legacy id
CREATE TABLE IF NOT EXISTS catalogue.alternative_code (
    code                              text NOT NULL CONSTRAINT alternative_code_code_chk CHECK (char_length(code) <= 128),
    partner_id                        uuid NOT NULL,
    partner_name                      text,
    variant_id                        uuid,
    note                              text CONSTRAINT alternative_code_note_chk CHECK (char_length(note) <= 200),
    id                                uuid PRIMARY KEY NOT NULL,
    product_id                        uuid
);

-- Holds 24 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS catalogue.approval_policy (
    id                                uuid PRIMARY KEY NOT NULL,
    scope_path                        ltree NOT NULL,
    subject                           text NOT NULL CONSTRAINT approval_policy_subject_chk CHECK (subject IN ('product', 'pricing')),
    name                              text NOT NULL CONSTRAINT approval_policy_name_chk CHECK (char_length(name) <= 200),
    is_default                        boolean DEFAULT false,
    venue_id                          uuid,
    market_code                       text CONSTRAINT approval_policy_market_code_chk CHECK (char_length(market_code) <= 40),
    legal_entity_id                   uuid,
    department_id                     uuid,
    product_kinds                     text[],
    change_types                      text[],
    stages                            jsonb,
    tiers                             jsonb,
    rejection_behavior                text CONSTRAINT approval_policy_rejection_behavior_chk CHECK (rejection_behavior IN ('returnToDraft', 'returnToPreviousStage', 'closeRequest')),
    resubmission_behavior             text CONSTRAINT approval_policy_resubmission_behavior_chk CHECK (resubmission_behavior IN ('restartFromFirstStage', 'resumeAtRejectingStage')),
    creator_cannot_give_final_approval boolean DEFAULT true,
    expected_approval_hours           integer,
    reminder_after_hours              integer,
    escalate_after_hours              integer,
    escalate_to_role                  text CONSTRAINT approval_policy_escalate_to_role_chk CHECK (char_length(escalate_to_role) <= 100),
    alternate_approver_role           text CONSTRAINT approval_policy_alternate_approver_role_chk CHECK (char_length(alternate_approver_role) <= 100),
    is_active                         boolean DEFAULT true,
    created_at                        timestamptz,
    updated_at                        timestamptz
);

-- Holds 28 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS catalogue.audit_entry (
    id                                uuid PRIMARY KEY NOT NULL,
    scope_path                        ltree NOT NULL,
    domain                            text NOT NULL CONSTRAINT audit_entry_domain_chk CHECK (domain IN ('product', 'pricing', 'channel')),
    occurred_at                       timestamptz NOT NULL,
    actor_principal_id                uuid,
    actor_role                        text CONSTRAINT audit_entry_actor_role_chk CHECK (char_length(actor_role) <= 100),
    actor_system                      text CONSTRAINT audit_entry_actor_system_chk CHECK (char_length(actor_system) <= 100),
    action                            text NOT NULL CONSTRAINT audit_entry_action_chk CHECK (char_length(action) <= 60),
    category                          text CONSTRAINT audit_entry_category_chk CHECK (char_length(category) <= 60),
    entity_type                       text NOT NULL CONSTRAINT audit_entry_entity_type_chk CHECK (char_length(entity_type) <= 60),
    entity_id                         uuid NOT NULL,
    product_id                        uuid,
    sales_channel_id                  uuid,
    version                           integer,
    field                             text CONSTRAINT audit_entry_field_chk CHECK (char_length(field) <= 100),
    previous_value                    text,
    new_value                         text,
    reason                            text,
    result                            text CONSTRAINT audit_entry_result_chk CHECK (result IN ('success', 'failure', 'partial')),
    source                            text CONSTRAINT audit_entry_source_chk CHECK (source IN ('backOffice', 'api', 'bulkImport', 'environmentTransfer', 'scheduler', 'aiAssistant', 'dynamicPricingEngine', 'rollback', 'emergencyAction', 'partner', 'sync')),
    environment                       text CONSTRAINT audit_entry_environment_chk CHECK (environment IN ('development', 'sandbox', 'uat', 'staging', 'production')),
    change_request_id                 uuid,
    approval_request_id               uuid,
    rollback_action_id                uuid,
    pricing_publication_id            uuid,
    reference                         text CONSTRAINT audit_entry_reference_chk CHECK (char_length(reference) <= 200),
    device_metadata                   jsonb,
    trace                             jsonb
);

-- Holds 11 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS catalogue.calculation_profile (
    id                                uuid PRIMARY KEY NOT NULL,
    scope_path                        ltree NOT NULL,
    code                              text NOT NULL CONSTRAINT calculation_profile_code_chk CHECK (char_length(code) <= 40),
    name                              text NOT NULL CONSTRAINT calculation_profile_name_chk CHECK (char_length(name) <= 200),
    version                           integer NOT NULL,
    is_default                        boolean DEFAULT false,
    effective_from                    timestamptz,
    effective_to                      timestamptz,
    status                            text NOT NULL DEFAULT 'draft',
    created_at                        timestamptz,
    updated_at                        timestamptz
);

-- Holds 11 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS catalogue.calculation_step (
    id                                uuid PRIMARY KEY NOT NULL,
    calculation_profile_id            uuid NOT NULL,
    sequence                          integer NOT NULL,
    step_type                         text NOT NULL CONSTRAINT calculation_step_step_type_chk CHECK (step_type IN ('commercialBaseRate', 'contextualRateSelection', 'dynamicPricingAdjustment', 'promotionDiscount', 'packageBundleAdjustment', 'feesSurcharges', 'taxCalculation', 'rounding', 'finalPayableAmount')),
    formula_type                      text NOT NULL CONSTRAINT calculation_step_formula_type_chk CHECK (formula_type IN ('fixedAmount', 'percentage', 'percentageOfBase', 'percentageOfSubtotal', 'tiered', 'conditional', 'minimum', 'maximum', 'customGovernedFormula')),
    input                             text CONSTRAINT calculation_step_input_chk CHECK (char_length(input) <= 200),
    formula                           text,
    depends_on                        text[],
    output                            text CONSTRAINT calculation_step_output_chk CHECK (char_length(output) <= 200),
    taxability                        text CONSTRAINT calculation_step_taxability_chk CHECK (taxability IN ('inTaxBase', 'outsideTaxBase')),
    rounding_profile_id               uuid
);

-- Holds 32 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS catalogue.change_request (
    id                                uuid PRIMARY KEY NOT NULL,
    scope_path                        ltree NOT NULL,
    subject                           text NOT NULL CONSTRAINT change_request_subject_chk CHECK (subject IN ('product', 'pricing')),
    name                              text NOT NULL CONSTRAINT change_request_name_chk CHECK (char_length(name) <= 200),
    change_type                       text NOT NULL CONSTRAINT change_request_change_type_chk CHECK (change_type IN ('newProduct', 'description', 'price', 'validity', 'capacity', 'entitlement', 'eligibility', 'tax', 'channel', 'media', 'policy', 'relationship', 'retirement', 'priceChange', 'newRate', 'rateRemoval', 'priceListChange', 'eligibilityRuleChange', 'taxChange', 'feeChange', 'formulaChange', 'currencyRoundingChange', 'emergencyChange')),
    product_id                        uuid,
    current_version                   integer,
    proposed_version                  integer,
    price_list_id                     uuid,
    business_reason                   text,
    reason_code                       text CONSTRAINT change_request_reason_code_chk CHECK (reason_code IN ('annualPriceReview', 'newSeason', 'commercialStrategy', 'contractUpdate', 'regulatoryChange', 'costIncrease', 'marketAdjustment', 'correction', 'emergency')),
    priority                          text DEFAULT 'normal' CONSTRAINT change_request_priority_chk CHECK (priority IN ('low', 'normal', 'high', 'urgent')),
    risk_level                        text CONSTRAINT change_request_risk_level_chk CHECK (risk_level IN ('low', 'medium', 'high', 'critical')),
    supporting_notes                  text,
    attachment_file_ids               text[],
    venue_id                          uuid,
    market_code                       text CONSTRAINT change_request_market_code_chk CHECK (char_length(market_code) <= 40),
    legal_entity_id                   uuid,
    business_unit                     text CONSTRAINT change_request_business_unit_chk CHECK (char_length(business_unit) <= 100),
    impacted_channels                 text[],
    owner_principal_id                uuid,
    requested_by_principal_id         uuid NOT NULL,
    requested_at                      timestamptz NOT NULL,
    assigned_approver_principal_id    uuid,
    approval_policy_id                uuid,
    approval_request_id               uuid,
    effective_date                    timestamptz,
    expiry_date                       timestamptz,
    status                            text NOT NULL DEFAULT 'draft' CONSTRAINT change_request_status_chk CHECK (status IN ('draft', 'pendingValidation', 'pendingApproval', 'returnedForModification', 'approved', 'rejected', 'scheduled', 'published', 'rolledBack')),
    decided_at                        timestamptz,
    created_at                        timestamptz,
    updated_at                        timestamptz
);

-- Holds 14 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS catalogue.change_request_line (
    id                                uuid PRIMARY KEY NOT NULL,
    change_request_id                 uuid NOT NULL,
    sequence                          integer NOT NULL,
    object_type                       text CONSTRAINT change_request_line_object_type_chk CHECK (object_type IN ('product', 'rate', 'priceList', 'eligibilityRule', 'tax', 'fee', 'formula', 'currencyRounding')),
    object_id                         uuid,
    configuration_area                text CONSTRAINT change_request_line_configuration_area_chk CHECK (configuration_area IN ('basicInformation', 'validity', 'pricing', 'capacity', 'entitlements', 'eligibility', 'media', 'channels', 'policies', 'relationships', 'lifecycle')),
    field                             text CONSTRAINT change_request_line_field_chk CHECK (char_length(field) <= 100),
    venue_id                          uuid,
    market_code                       text CONSTRAINT change_request_line_market_code_chk CHECK (char_length(market_code) <= 40),
    current_value                     text,
    proposed_value                    text,
    current_amount                    numeric(18,4),
    proposed_amount                   numeric(18,4),
    is_removal                        boolean DEFAULT false
);

-- How much of a capacity each channel may sell. Web cannot consume the counter’s share
CREATE TABLE IF NOT EXISTS catalogue.channel_allocation (
    id                                uuid PRIMARY KEY,
    channel                           text NOT NULL CONSTRAINT channel_allocation_channel_chk CHECK (channel IN ('pos', 'kiosk', 'web', 'mobile', 'b2b', 'ota', 'callCentre')),
    allocated_units                   integer NOT NULL,
    sold_units                        integer,
    leased_units                      integer,
    remaining_units                   integer,
    release_at                        timestamptz,
    sales_channel_id                  uuid,
    allocation_type                   text DEFAULT 'dedicated' CONSTRAINT channel_allocation_allocation_type_chk CHECK (allocation_type IN ('sharedPool', 'dedicated', 'percentage', 'dynamic')),
    minimum_units                     integer,
    maximum_units                     integer,
    replenishment_rule                jsonb,
    waitlist_behavior                 text DEFAULT 'none' CONSTRAINT channel_allocation_waitlist_behavior_chk CHECK (waitlist_behavior IN ('none', 'joinWaitlist', 'notifyOnRelease')),
    release_threshold_units           integer,
    release_hours_before_event        integer,
    contractual_units                 integer,
    minimum_guaranteed_units          integer,
    is_frozen                         boolean DEFAULT false,
    envelope_id                       uuid NOT NULL
);

-- How much of a performance each sales channel may sell. Two hundred seats with eighty to the web,
-- eighty to the box office and forty held back. Renamed from envelope, which was unguessable
CREATE TABLE IF NOT EXISTS catalogue.channel_capacity (
    id                                uuid PRIMARY KEY NOT NULL,
    performance_id                    uuid NOT NULL,
    name                              text,
    seat_category_id                  uuid,
    oversell_allowance                integer DEFAULT 0,
    oversell_basis                    text CONSTRAINT channel_capacity_oversell_basis_chk CHECK (oversell_basis IN ('fixedCount', 'historicNoShowRate', 'percentage')),
    capacity                          integer NOT NULL,
    sold                              integer NOT NULL,
    leased                            integer NOT NULL,
    remaining                         integer NOT NULL,
    has_channel_allocations           boolean,
    is_seated                         boolean NOT NULL
);

-- Holds 23 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS catalogue.channel_connection (
    id                                uuid PRIMARY KEY NOT NULL,
    scope_path                        ltree NOT NULL,
    sales_channel_id                  uuid NOT NULL,
    connector_name                    text NOT NULL CONSTRAINT channel_connection_connector_name_chk CHECK (char_length(connector_name) <= 200),
    partner                           text CONSTRAINT channel_connection_partner_chk CHECK (char_length(partner) <= 200),
    environment                       text NOT NULL CONSTRAINT channel_connection_environment_chk CHECK (environment IN ('sandbox', 'uat', 'production')),
    connection_type                   text NOT NULL CONSTRAINT channel_connection_connection_type_chk CHECK (connection_type IN ('ticvaiNative', 'restApi', 'webhook', 'otaAdapter', 'resellerApi', 'partnerApi', 'middleware', 'fileSftp', 'customConnector')),
    direction                         text DEFAULT 'outbound' CONSTRAINT channel_connection_direction_chk CHECK (direction IN ('outbound', 'inbound', 'bidirectional')),
    endpoint                          text CONSTRAINT channel_connection_endpoint_chk CHECK (char_length(endpoint) <= 500),
    api_version                       text CONSTRAINT channel_connection_api_version_chk CHECK (char_length(api_version) <= 40),
    authentication_type               text CONSTRAINT channel_connection_authentication_type_chk CHECK (authentication_type IN ('none', 'oauth', 'apiKey', 'clientCredentials', 'certificate', 'signedRequest')),
    credentials_reference             text CONSTRAINT channel_connection_credentials_reference_chk CHECK (char_length(credentials_reference) <= 200),
    certificate_reference             text CONSTRAINT channel_connection_certificate_reference_chk CHECK (char_length(certificate_reference) <= 200),
    certificate_expires_at            timestamptz,
    timeout_ms                        integer,
    rate_limit_per_minute             integer,
    ip_restrictions                   text[],
    retry_policy                      jsonb,
    adapter_id                        text CONSTRAINT channel_connection_adapter_id_chk CHECK (char_length(adapter_id) <= 100),
    connection_status                 text DEFAULT 'notTested' CONSTRAINT channel_connection_connection_status_chk CHECK (connection_status IN ('notTested', 'connected', 'degraded', 'offline', 'disabled')),
    last_tests                        jsonb,
    created_at                        timestamptz,
    updated_at                        timestamptz
);

-- Holds 23 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS catalogue.channel_incident (
    id                                uuid PRIMARY KEY NOT NULL,
    scope_path                        ltree NOT NULL,
    sales_channel_id                  uuid NOT NULL,
    channel_connection_id             uuid,
    partner                           text CONSTRAINT channel_incident_partner_chk CHECK (char_length(partner) <= 200),
    severity                          text NOT NULL CONSTRAINT channel_incident_severity_chk CHECK (severity IN ('critical', 'high', 'medium', 'low')),
    error_type                        text NOT NULL CONSTRAINT channel_incident_error_type_chk CHECK (error_type IN ('connectionFailure', 'authenticationFailure', 'productSyncFailure', 'pricingMismatch', 'inventoryMismatch', 'orderFailure', 'paymentError', 'timeout', 'cancellationFailure', 'duplicateTransaction', 'fulfillmentFailure', 'rateLimit', 'partnerError')),
    product_id                        uuid,
    event_id                          uuid,
    transactions_affected             integer DEFAULT 0,
    business_impact                   numeric(18,4),
    first_detected_at                 timestamptz NOT NULL,
    owner_principal_id                uuid,
    sla_due_at                        timestamptz,
    status                            text NOT NULL DEFAULT 'open' CONSTRAINT channel_incident_status_chk CHECK (status IN ('open', 'investigating', 'retrying', 'resolved', 'closed')),
    error_code                        text CONSTRAINT channel_incident_error_code_chk CHECK (char_length(error_code) <= 100),
    api_request_reference             text CONSTRAINT channel_incident_api_request_reference_chk CHECK (char_length(api_request_reference) <= 200),
    response_excerpt                  text,
    correlation_id                    text CONSTRAINT channel_incident_correlation_id_chk CHECK (char_length(correlation_id) <= 100),
    retry_count                       integer DEFAULT 0,
    ai_summary                        text,
    resolved_at                       timestamptz,
    updated_at                        timestamptz
);

-- Holds 50 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS catalogue.channel_sales_rule (
    id                                uuid PRIMARY KEY NOT NULL,
    scope_path                        ltree NOT NULL,
    sales_channel_id                  uuid NOT NULL,
    product_id                        uuid,
    rule_kind                         text NOT NULL CONSTRAINT channel_sales_rule_rule_kind_chk CHECK (rule_kind IN ('salesWindow', 'salesLimit', 'eligibility')),
    name                              text CONSTRAINT channel_sales_rule_name_chk CHECK (char_length(name) <= 200),
    rule_level                        text DEFAULT 'channel' CONSTRAINT channel_sales_rule_rule_level_chk CHECK (rule_level IN ('platform', 'product', 'channel', 'contractPartner')),
    overrides_product_rule            boolean DEFAULT false,
    effective_from                    timestamptz,
    effective_to                      timestamptz,
    is_active                         boolean NOT NULL DEFAULT true,
    sales_start_date                  date,
    sales_start_time                  time,
    sales_end_date                    date,
    sales_end_time                    time,
    time_zone                         text CONSTRAINT channel_sales_rule_time_zone_chk CHECK (char_length(time_zone) <= 64),
    days_of_week                      text[],
    hours_of_operation                jsonb,
    blackout_dates                    text[],
    event_relative_window             jsonb,
    minimum_lead_days                 integer,
    minimum_quantity                  integer,
    maximum_quantity                  integer,
    maximum_per_transaction           integer,
    maximum_per_customer              integer,
    maximum_per_day                   integer,
    maximum_per_event                 integer,
    maximum_per_product               integer,
    is_reservation_permitted          boolean,
    is_hold_permitted                 boolean,
    is_payment_link_permitted         boolean,
    is_partial_payment_permitted      boolean,
    is_split_payment_permitted        boolean,
    is_discount_permitted             boolean,
    is_promo_code_permitted           boolean,
    is_exchange_permitted             boolean,
    is_reschedule_permitted           boolean,
    is_upgrade_permitted              boolean,
    restrictions                      text[],
    eligibility_dimension             text CONSTRAINT channel_sales_rule_eligibility_dimension_chk CHECK (eligibility_dimension IN ('customerType', 'membership', 'loyaltyTier', 'country', 'residency', 'age', 'corporateAccount', 'partner', 'customerSegment', 'promoEligibility', 'authenticationStatus', 'purchaseHistory', 'salesTerritory')),
    eligibility_operator              text CONSTRAINT channel_sales_rule_eligibility_operator_chk CHECK (eligibility_operator IN ('equals', 'notEquals', 'in', 'notIn', 'greaterThanOrEqual', 'lessThanOrEqual', 'between')),
    eligibility_values                text[],
    eligibility_effect                text CONSTRAINT channel_sales_rule_eligibility_effect_chk CHECK (eligibility_effect IN ('allow', 'deny')),
    is_guest_allowed                  boolean,
    is_login_required                 boolean,
    is_membership_required            boolean,
    is_corporate_account_required     boolean,
    is_identity_verification_required boolean,
    created_at                        timestamptz,
    updated_at                        timestamptz
);

-- Holds 18 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS catalogue.channel_sync (
    id                                uuid PRIMARY KEY NOT NULL,
    scope_path                        ltree NOT NULL,
    sales_channel_id                  uuid NOT NULL,
    channel_connection_id             uuid,
    domain                            text NOT NULL CONSTRAINT channel_sync_domain_chk CHECK (domain IN ('product', 'productDescription', 'schedule', 'availability', 'capacity', 'price', 'tax', 'fees', 'media', 'restrictions', 'salesStatus')),
    direction                         text DEFAULT 'ticvaiToChannel' CONSTRAINT channel_sync_direction_chk CHECK (direction IN ('ticvaiToChannel', 'channelToTicvai', 'bidirectional')),
    frequency                         text DEFAULT 'nearRealTime' CONSTRAINT channel_sync_frequency_chk CHECK (frequency IN ('realTime', 'nearRealTime', 'scheduled', 'manual', 'eventTriggered')),
    is_paused                         boolean DEFAULT false,
    last_successful_sync_at           timestamptz,
    next_sync_at                      timestamptz,
    records_processed                 integer,
    successful                        integer,
    failed                            integer,
    pending                           integer,
    warnings                          integer,
    duration_ms                       integer,
    mismatch_count                    integer,
    updated_at                        timestamptz
);

-- Holds 17 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS catalogue.configuration_template (
    id                                uuid PRIMARY KEY NOT NULL,
    scope_path                        ltree NOT NULL,
    subject                           text NOT NULL CONSTRAINT configuration_template_subject_chk CHECK (subject IN ('product', 'priceList')),
    name                              text NOT NULL CONSTRAINT configuration_template_name_chk CHECK (char_length(name) <= 200),
    description                       text,
    template_kind                     text CONSTRAINT configuration_template_template_kind_chk CHECK (char_length(template_kind) <= 60),
    product_kind                      text,
    venue_id                          uuid,
    source_product_id                 uuid,
    source_price_list_id              uuid,
    included_components               text[],
    review_fields                     text[],
    is_ai_drafted                     boolean DEFAULT false,
    status                            text NOT NULL DEFAULT 'draft',
    owner_principal_id                uuid,
    created_at                        timestamptz,
    updated_at                        timestamptz
);

-- Holds 26 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS catalogue.demand_forecast (
    id                                uuid PRIMARY KEY NOT NULL,
    scope_path                        ltree NOT NULL,
    forecast_kind                     text NOT NULL CONSTRAINT demand_forecast_forecast_kind_chk CHECK (forecast_kind IN ('demand', 'elasticity')),
    venue_id                          uuid,
    product_id                        uuid,
    event_id                          uuid,
    performance_id                    uuid,
    price_category_id                 uuid,
    section_code                      text CONSTRAINT demand_forecast_section_code_chk CHECK (char_length(section_code) <= 40),
    forecast_date                     date,
    timeslot                          text CONSTRAINT demand_forecast_timeslot_chk CHECK (char_length(timeslot) <= 40),
    channel                           text,
    customer_segment                  text CONSTRAINT demand_forecast_customer_segment_chk CHECK (char_length(customer_segment) <= 60),
    horizon                           text CONSTRAINT demand_forecast_horizon_chk CHECK (horizon IN ('intraday', 'tomorrow', 'days7', 'days30', 'eventHorizon', 'seasonalHorizon')),
    confidence                        numeric(18,4),
    outputs                           jsonb,
    booking_curve                     jsonb,
    signal_contributions              jsonb,
    error_metrics                     jsonb,
    confidence_reasons                text[],
    elasticity_coefficient            numeric(18,4),
    price_sensitivity                 text CONSTRAINT demand_forecast_price_sensitivity_chk CHECK (price_sensitivity IN ('low', 'medium', 'high')),
    response_curve                    jsonb,
    revenue_zone_min                  numeric(18,4),
    revenue_zone_max                  numeric(18,4),
    model_version                     text NOT NULL CONSTRAINT demand_forecast_model_version_chk CHECK (char_length(model_version) <= 60),
    generated_at                      timestamptz NOT NULL
);

-- Holds 28 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS catalogue.demand_signal (
    id                                uuid PRIMARY KEY NOT NULL,
    scope_path                        ltree NOT NULL,
    signal_kind                       text NOT NULL CONSTRAINT demand_signal_signal_kind_chk CHECK (signal_kind IN ('weather', 'nearbyEvent', 'competitorPrice', 'calendar', 'tourism', 'transport', 'market')),
    signal_type                       text CONSTRAINT demand_signal_signal_type_chk CHECK (char_length(signal_type) <= 60),
    name                              text CONSTRAINT demand_signal_name_chk CHECK (char_length(name) <= 200),
    source                            text NOT NULL CONSTRAINT demand_signal_source_chk CHECK (char_length(source) <= 100),
    venue_id                          uuid,
    product_id                        uuid,
    geography                         text CONSTRAINT demand_signal_geography_chk CHECK (char_length(geography) <= 100),
    market_code                       text CONSTRAINT demand_signal_market_code_chk CHECK (char_length(market_code) <= 40),
    period_start                      timestamptz,
    period_end                        timestamptz,
    current_value                     numeric(18,4),
    unit                              text CONSTRAINT demand_signal_unit_chk CHECK (char_length(unit) <= 20),
    reading                           jsonb,
    configuration                     jsonb,
    weight                            numeric(18,4),
    reliability                       numeric(18,4),
    historical_correlation            numeric(18,4),
    confidence                        numeric(18,4),
    impact_min_percent                numeric(18,4),
    impact_max_percent                numeric(18,4),
    refresh_frequency                 text CONSTRAINT demand_signal_refresh_frequency_chk CHECK (refresh_frequency IN ('realTime', 'hourly', 'daily', 'weekly', 'manual')),
    is_approved                       boolean DEFAULT false,
    is_active                         boolean DEFAULT true,
    observed_at                       timestamptz,
    last_updated_at                   timestamptz,
    created_at                        timestamptz
);

-- Fixed, free or round-up. Posts to a liability account, not revenue — money collected for a
-- charity is not the venue’s to recognise Hangs off: reaches catalogue.product through its keys;
-- references ledger.account, platform.scope. Reached by: 3 operations read it and 2 write it.
CREATE TABLE IF NOT EXISTS catalogue.donation_campaign (
    id                                uuid PRIMARY KEY,
    name                              text NOT NULL CONSTRAINT donation_campaign_name_chk CHECK (char_length(name) <= 200),
    description                       text CONSTRAINT donation_campaign_description_chk CHECK (char_length(description) <= 1000),
    beneficiary                       text,
    venue_ids                         text[],
    amount_mode                       text NOT NULL CONSTRAINT donation_campaign_amount_mode_chk CHECK (amount_mode IN ('fixedChoices', 'freeAmount', 'roundUp')),
    min_amount                        numeric(18,4),
    max_amount                        numeric(18,4),
    liability_account_id              uuid,
    channels                          text[],
    is_active                         boolean NOT NULL,
    valid_from                        timestamptz,
    valid_to                          timestamptz,
    raised_total                      numeric(18,4),
    venue_id                          uuid NOT NULL
);

-- Holds 39 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS catalogue.dynamic_pricing_control (
    id                                uuid PRIMARY KEY NOT NULL,
    scope_path                        ltree NOT NULL,
    scope_level                       text NOT NULL CONSTRAINT dynamic_pricing_control_scope_level_chk CHECK (scope_level IN ('global', 'market', 'venue', 'strategy', 'product', 'event', 'performance', 'channel')),
    scope_id                          uuid,
    absolute_minimum_price            numeric(18,4),
    absolute_maximum_price            numeric(18,4),
    minimum_margin_percent            numeric(18,4),
    maximum_uplift_percent            numeric(18,4),
    maximum_reduction_percent         numeric(18,4),
    maximum_single_change_percent     numeric(18,4),
    maximum_daily_change_percent      numeric(18,4),
    maximum_weekly_change_percent     numeric(18,4),
    minimum_change_interval_minutes   integer,
    maximum_changes_per_day           integer,
    minimum_inventory                 integer,
    maximum_occupancy_trigger_percent numeric(18,4),
    protected_rate_types              text[],
    is_frozen                         boolean DEFAULT false,
    is_kill_switch_active             boolean DEFAULT false,
    automation_level                  text NOT NULL DEFAULT 'advisory' CONSTRAINT dynamic_pricing_control_automation_level_chk CHECK (automation_level IN ('advisory', 'humanInTheLoop', 'conditionalAutonomous', 'autonomous')),
    authority_tiers                   jsonb,
    max_adjustment_percent            numeric(18,4),
    min_ai_confidence                 numeric(18,4),
    min_revenue_uplift_percent        numeric(18,4),
    evaluation_frequency_minutes      integer,
    execution_frequency_minutes       integer,
    quiet_period_minutes              integer,
    no_change_windows                 jsonb,
    circuit_breakers                  jsonb,
    require_guardrails_passed         boolean DEFAULT true,
    exclude_protected_rates           boolean DEFAULT true,
    require_healthy_forecast_data     boolean DEFAULT true,
    safe_failure_behavior             text DEFAULT 'holdLastPrice' CONSTRAINT dynamic_pricing_control_safe_failure_behavior_chk CHECK (safe_failure_behavior IN ('holdLastPrice', 'returnToBase', 'freeze', 'requestReview')),
    active_override                   jsonb,
    is_paused                         boolean DEFAULT false,
    effective_from                    timestamptz,
    effective_to                      timestamptz,
    created_at                        timestamptz,
    updated_at                        timestamptz
);

-- Holds 26 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS catalogue.dynamic_pricing_strategy (
    id                                uuid PRIMARY KEY NOT NULL,
    scope_path                        ltree NOT NULL,
    code                              text NOT NULL CONSTRAINT dynamic_pricing_strategy_code_chk CHECK (char_length(code) <= 40),
    name                              text NOT NULL CONSTRAINT dynamic_pricing_strategy_name_chk CHECK (char_length(name) <= 200),
    description                       text,
    strategy_type                     text NOT NULL CONSTRAINT dynamic_pricing_strategy_strategy_type_chk CHECK (strategy_type IN ('demandBased', 'occupancyBased', 'availabilityBased', 'inventoryBased', 'bookingVelocity', 'timeToEvent', 'seasonal', 'dayOfWeek', 'timeslot', 'channel', 'segment', 'location', 'hybrid')),
    scope_type                        text NOT NULL CONSTRAINT dynamic_pricing_strategy_scope_type_chk CHECK (scope_type IN ('singleProduct', 'productFamily', 'event', 'multiplePerformances', 'venue', 'selectedTimeslots', 'selectedPriceCategories')),
    venue_id                          uuid,
    product_id                        uuid,
    product_family                    text CONSTRAINT dynamic_pricing_strategy_product_family_chk CHECK (char_length(product_family) <= 100),
    event_id                          uuid,
    performance_ids                   text[],
    timeslot_ids                      text[],
    price_category_ids                text[],
    business_unit                     text CONSTRAINT dynamic_pricing_strategy_business_unit_chk CHECK (char_length(business_unit) <= 100),
    market_code                       text CONSTRAINT dynamic_pricing_strategy_market_code_chk CHECK (char_length(market_code) <= 40),
    base_price_source                 text CONSTRAINT dynamic_pricing_strategy_base_price_source_chk CHECK (char_length(base_price_source) <= 100),
    evaluation_frequency              text DEFAULT 'hourly' CONSTRAINT dynamic_pricing_strategy_evaluation_frequency_chk CHECK (evaluation_frequency IN ('every15Minutes', 'every30Minutes', 'hourly', 'daily', 'onInventoryChange', 'onThresholdTrigger')),
    combination_mode                  text DEFAULT 'independent' CONSTRAINT dynamic_pricing_strategy_combination_mode_chk CHECK (combination_mode IN ('independent', 'combinable', 'exclusive', 'fallback')),
    effective_from                    timestamptz,
    effective_to                      timestamptz,
    cloned_from_strategy_id           uuid,
    owner_principal_id                uuid,
    status                            text NOT NULL DEFAULT 'draft' CONSTRAINT dynamic_pricing_strategy_status_chk CHECK (status IN ('draft', 'active', 'paused', 'frozen', 'expired', 'retired')),
    created_at                        timestamptz,
    updated_at                        timestamptz
);

-- The rules a ticket carries before anybody buys one — validity, entries allowed, transferability,
-- what a gate does with it. access.entitlement is the issued instance
CREATE TABLE IF NOT EXISTS catalogue.entitlement_template (
    description                       text,
    id                                uuid PRIMARY KEY NOT NULL,
    code                              text NOT NULL CONSTRAINT entitlement_template_code_chk CHECK (char_length(code) <= 64),
    name                              text NOT NULL CONSTRAINT entitlement_template_name_chk CHECK (char_length(name) <= 200),
    validity_kind                     text NOT NULL CONSTRAINT entitlement_template_validity_kind_chk CHECK (validity_kind IN ('singleUse', 'dated', 'dateRange', 'rolling', 'unlimited', 'countLimited')),
    valid_from_offset_days            integer,
    valid_for_days                    integer,
    days_of_week                      text[],
    expiry_anchor                     text CONSTRAINT entitlement_template_expiry_anchor_chk CHECK (expiry_anchor IN ('offsetDays', 'endOfMonth', 'endOfQuarter', 'endOfYear', 'fixedDate', 'seasonEnd')),
    expiry_date                       date,
    expiry_notice_days                integer,
    carries_stored_value              boolean DEFAULT false,
    included_value                    numeric(18,4),
    blackout_dates                    text[],
    fast_track_tier                   text CONSTRAINT entitlement_template_fast_track_tier_chk CHECK (fast_track_tier IN ('none', 'priority', 'express', 'unlimited')),
    entries_allowed                   integer,
    transport_restriction             jsonb,
    is_reentry_allowed                boolean DEFAULT false,
    purchase_eligibility              jsonb,
    person_type                       text CONSTRAINT entitlement_template_person_type_chk CHECK (person_type IN ('adult', 'child', 'infant', 'senior', 'student', 'resident', 'staff')),
    admission_rules_id                uuid,
    is_transferable                   boolean DEFAULT true,
    can_share_media                   boolean DEFAULT true,
    can_claim_shop_and_drop           boolean DEFAULT false,
    is_name_bound                     boolean DEFAULT false,
    is_auto_renew_default             boolean DEFAULT false,
    renewal_term_days                 integer,
    renewal_grace_days                integer DEFAULT 0,
    renewal_variant_id                uuid,
    crosses_cells                     boolean DEFAULT false,
    is_active                         boolean,
    scope_path                        ltree NOT NULL
);

-- A named thing on at a venue, grouping performances. A concert is an event; each showing is a
-- performance
CREATE TABLE IF NOT EXISTS catalogue.event (
    id                                uuid PRIMARY KEY NOT NULL,
    code                              text NOT NULL,
    name                              text NOT NULL,
    venue_id                          uuid NOT NULL,
    scope_path                        ltree NOT NULL,
    parent_event_id                   uuid,
    performance_count                 integer,
    is_active                         boolean
);

-- Holds 12 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS catalogue.event_capacity_profile (
    event_id                          uuid,
    performance_id                    uuid,
    mode                              text CONSTRAINT event_capacity_profile_mode_chk CHECK (mode IN ('reservedSeating', 'unreservedSeating', 'standing', 'mixed', 'capacityOnly')),
    safe_maximum                      integer,
    sellable                          integer,
    held                              integer DEFAULT 0,
    accessible_provision              integer DEFAULT 0,
    companion_seats                   integer DEFAULT 0,
    overbook_percent                  numeric(18,4) DEFAULT 0,
    seat_map_id                       uuid,
    scope_path                        ltree NOT NULL,
    id                                uuid PRIMARY KEY NOT NULL
);

-- Holds 7 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS catalogue.event_registration (
    event_id                          uuid,
    is_required                       boolean DEFAULT false,
    form_id                           uuid,
    capture_per_attendee              boolean DEFAULT true,
    admission_policy                  jsonb,
    scope_path                        ltree NOT NULL,
    id                                uuid PRIMARY KEY NOT NULL
);

-- Holds 14 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS catalogue.event_reschedule (
    id                                uuid PRIMARY KEY,
    kind                              text NOT NULL CONSTRAINT event_reschedule_kind_chk CHECK (kind IN ('moveTime', 'moveDate', 'moveVenue', 'cancel', 'abandon')),
    performance_ids                   text[],
    new_starts_at                     timestamptz,
    new_space_id                      uuid,
    reason                            text NOT NULL,
    ticket_treatment                  text CONSTRAINT event_reschedule_ticket_treatment_chk CHECK (ticket_treatment IN ('moveAutomatically', 'offerChoice', 'refund', 'creditToWallet', 'honourAtAnyPerformance')),
    refund_fees                       boolean DEFAULT true,
    notify_guests                     boolean DEFAULT true,
    notification_template_id          uuid,
    affected_orders                   integer,
    affected_guests                   integer,
    approval_request_id               uuid,
    scope_path                        ltree NOT NULL
);

-- Holds 4 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS catalogue.event_resource_plan (
    event_id                          uuid,
    readiness                         text CONSTRAINT event_resource_plan_readiness_chk CHECK (readiness IN ('notPlanned', 'planning', 'atRisk', 'ready')),
    scope_path                        ltree NOT NULL,
    id                                uuid PRIMARY KEY NOT NULL
);

-- Holds 6 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS catalogue.event_schedule (
    event_id                          uuid,
    duration_is_dynamic               boolean DEFAULT false,
    maximum_overrun_minutes           integer,
    cascade_overrun                   boolean DEFAULT true,
    scope_path                        ltree NOT NULL,
    id                                uuid PRIMARY KEY NOT NULL
);

-- Holds 12 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS catalogue.event_type (
    id                                uuid PRIMARY KEY,
    code                              text NOT NULL,
    name                              text NOT NULL,
    has_performances                  boolean DEFAULT true,
    capacity_basis                    text CONSTRAINT event_type_capacity_basis_chk CHECK (capacity_basis IN ('perPerformance', 'perDay', 'unlimited')),
    ticket_names_date                 boolean DEFAULT true,
    multi_day                         boolean DEFAULT false,
    requires_registration             boolean DEFAULT false,
    requires_accreditation            boolean DEFAULT false,
    seating_modes_allowed             text[],
    default_lifecycle                 text[],
    scope_path                        ltree NOT NULL
);

-- Holds 19 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS catalogue.fee (
    id                                uuid PRIMARY KEY NOT NULL,
    scope_path                        ltree NOT NULL,
    code                              text NOT NULL CONSTRAINT fee_code_chk CHECK (char_length(code) <= 40),
    name                              text NOT NULL CONSTRAINT fee_name_chk CHECK (char_length(name) <= 200),
    description                       text,
    fee_type                          text NOT NULL CONSTRAINT fee_fee_type_chk CHECK (fee_type IN ('bookingFee', 'transactionFee', 'serviceFee', 'convenienceFee', 'deliveryFee', 'handlingFee', 'modificationFee', 'reschedulingFee', 'cancellationFee', 'refundFee', 'paymentFee', 'channelFee', 'facilityFee', 'surcharge', 'customFee')),
    value_type                        text NOT NULL CONSTRAINT fee_value_type_chk CHECK (value_type IN ('fixedAmount', 'percentage', 'tiered')),
    charge_basis                      text NOT NULL CONSTRAINT fee_charge_basis_chk CHECK (charge_basis IN ('perTicket', 'perProduct', 'perPerson', 'perOrder', 'perTransaction', 'perDay')),
    amount                            numeric(18,4),
    percentage                        numeric(18,4),
    tiers                             jsonb,
    tax_treatment                     text CONSTRAINT fee_tax_treatment_chk CHECK (char_length(tax_treatment) <= 60),
    refundability                     text DEFAULT 'nonRefundable' CONSTRAINT fee_refundability_chk CHECK (refundability IN ('refundable', 'nonRefundable')),
    visibility                        text DEFAULT 'shownSeparately' CONSTRAINT fee_visibility_chk CHECK (visibility IN ('customerVisible', 'includedInDisplayPrice', 'shownSeparately', 'internalOnly')),
    effective_from                    timestamptz,
    effective_to                      timestamptz,
    status                            text NOT NULL DEFAULT 'draft',
    created_at                        timestamptz,
    updated_at                        timestamptz
);

-- Holds 27 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS catalogue.fee_rule (
    id                                uuid PRIMARY KEY NOT NULL,
    scope_path                        ltree NOT NULL,
    rule_kind                         text NOT NULL CONSTRAINT fee_rule_rule_kind_chk CHECK (rule_kind IN ('applicability', 'exception')),
    name                              text NOT NULL CONSTRAINT fee_rule_name_chk CHECK (char_length(name) <= 200),
    fee_id                            uuid,
    conditions                        jsonb,
    combination                       text CONSTRAINT fee_rule_combination_chk CHECK (combination IN ('stack', 'replace', 'exclude')),
    excluded_fee_ids                  text[],
    application                       text CONSTRAINT fee_rule_application_chk CHECK (application IN ('applyOnce', 'applyPerItem')),
    on_match                          text DEFAULT 'continueProcessing' CONSTRAINT fee_rule_on_match_chk CHECK (on_match IN ('stopProcessing', 'continueProcessing')),
    mutual_exclusion_group            text CONSTRAINT fee_rule_mutual_exclusion_group_chk CHECK (char_length(mutual_exclusion_group) <= 60),
    priority                          integer NOT NULL DEFAULT 0,
    exception_type                    text CONSTRAINT fee_rule_exception_type_chk CHECK (exception_type IN ('feeWaiver', 'feeReduction', 'taxExemption', 'zeroRatedTax', 'complimentaryTransaction', 'operationalWaiver', 'contractualWaiver')),
    target_fee_ids                    text[],
    target_tax_profile_ids            text[],
    reduction_percent                 numeric(18,4),
    reduction_amount                  numeric(18,4),
    eligibility_basis                 text CONSTRAINT fee_rule_eligibility_basis_chk CHECK (eligibility_basis IN ('membershipBenefit', 'loyaltyTier', 'corporateAgreement', 'b2bContract', 'customerSegment', 'staffRole', 'promotion', 'serviceRecovery', 'operationalIssue', 'legalExemption', 'supervisorOverride')),
    eligibility_ref_id                uuid,
    is_approval_required              boolean DEFAULT false,
    is_evidence_required              boolean DEFAULT false,
    is_reason_required                boolean DEFAULT true,
    effective_from                    timestamptz,
    effective_to                      timestamptz,
    status                            text NOT NULL DEFAULT 'draft',
    created_at                        timestamptz,
    updated_at                        timestamptz
);

-- What makes a product a school-trip format or a party package: participants, duration, hosts,
-- free leaders per pupils and how it is paid. The product row still carries the price
CREATE TABLE IF NOT EXISTS catalogue.group_package (
    id                                uuid PRIMARY KEY,
    product_id                        text,
    kind                              text NOT NULL CONSTRAINT group_package_kind_chk CHECK (kind IN ('school', 'party')),
    max_participants                  integer NOT NULL,
    duration_minutes                  integer NOT NULL,
    host_count                        integer DEFAULT 1,
    pricing_basis                     text CONSTRAINT group_package_pricing_basis_chk CHECK (pricing_basis IN ('perParticipant', 'perPackage')),
    free_leader_ratio                 integer DEFAULT 10,
    payment_mode                      text CONSTRAINT group_package_payment_mode_chk CHECK (payment_mode IN ('invoice', 'deposit', 'full')),
    includes                          text[],
    scope_path                        ltree NOT NULL
);

-- Two-phase catalogue import (BL-057), following seating.ImportJob. A job that parses zero
-- products is not a parsed job. Hangs off: reaches catalogue.product through its keys; references
-- catalogue.change_request, identity.principal. Reached by: 6 operations read it and 3 write it.
CREATE TABLE IF NOT EXISTS catalogue.import_job (
    id                                uuid PRIMARY KEY NOT NULL,
    status                            text NOT NULL CONSTRAINT import_job_status_chk CHECK (status IN ('parsing', 'previewReady', 'committing', 'committed', 'failed')),
    outcome                           text CONSTRAINT import_job_outcome_chk CHECK (outcome IN ('parsed', 'parsedWithFindings', 'nothingFound', 'unreadable')),
    parsed_count                      integer NOT NULL,
    create_count                      integer,
    update_count                      integer,
    scope_path                        ltree NOT NULL,
    job_kind                          text DEFAULT 'productImport' CONSTRAINT import_job_job_kind_chk CHECK (job_kind IN ('productImport', 'environmentTransfer', 'pricingBulkUpdate', 'pricingImport')),
    direction                         text CONSTRAINT import_job_direction_chk CHECK (direction IN ('export', 'import')),
    source_environment                text CONSTRAINT import_job_source_environment_chk CHECK (source_environment IN ('development', 'sandbox', 'uat', 'staging', 'production')),
    target_environment                text CONSTRAINT import_job_target_environment_chk CHECK (target_environment IN ('development', 'sandbox', 'uat', 'staging', 'production')),
    product_ids                       text[],
    components                        text[],
    reference_mappings                jsonb,
    missing_references                text[],
    file_id                           uuid,
    source_format                     text CONSTRAINT import_job_source_format_chk CHECK (char_length(source_format) <= 40),
    column_mappings                   jsonb,
    parameters                        jsonb,
    warning_count                     integer DEFAULT 0,
    error_count                       integer DEFAULT 0,
    change_request_id                 uuid,
    requested_by_principal_id         uuid,
    created_at                        timestamptz,
    completed_at                      timestamptz
);

-- A short-lived claim on contended stock while somebody decides. A seat in a basket is held, not
-- sold — CF-115 settled that contended inventory is leased rather than reserved, and the hold
-- expires on its own. Renamed from lease, which read as a rental agreement
CREATE TABLE IF NOT EXISTS catalogue.inventory_hold (
    id                                uuid PRIMARY KEY NOT NULL,
    channel_capacity_id               uuid NOT NULL,
    holder_kind                       text NOT NULL DEFAULT 'workstation' CONSTRAINT inventory_hold_holder_kind_chk CHECK (holder_kind IN ('workstation', 'cart')),
    holder_workstation_id             uuid,
    holder_cart_id                    uuid,
    converted_order_id                uuid,
    converted_at                      timestamptz,
    parent_lease_id                   text,
    requested_units                   integer,
    channel                           text,
    granted_units                     integer NOT NULL,
    consumed_units                    integer NOT NULL,
    status                            text NOT NULL CONSTRAINT inventory_hold_status_chk CHECK (status IN ('active', 'expired', 'released', 'forceReleased', 'converted')),
    acquired_at                       timestamptz NOT NULL,
    expires_at                        timestamptz NOT NULL,
    released_at                       timestamptz,
    force_released_by_principal_id    uuid,
    force_release_reason              text
);

-- Holds 24 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS catalogue.lifecycle_action (
    id                                uuid PRIMARY KEY NOT NULL,
    scope_path                        ltree NOT NULL,
    product_id                        uuid NOT NULL,
    venue_id                          uuid,
    action_type                       text NOT NULL CONSTRAINT lifecycle_action_action_type_chk CHECK (action_type IN ('publication', 'salesStart', 'activation', 'salesSuspension', 'deactivation', 'endOfSale', 'retirement', 'archive')),
    scheduled_at                      timestamptz NOT NULL,
    time_zone                         text CONSTRAINT lifecycle_action_time_zone_chk CHECK (char_length(time_zone) <= 64),
    channels                          text[],
    target_state                      text,
    notify_roles                      text[],
    pre_action_validation             boolean DEFAULT true,
    failure_handling                  text DEFAULT 'retryThenNotify' CONSTRAINT lifecycle_action_failure_handling_chk CHECK (failure_handling IN ('retryThenNotify', 'skipAndNotify', 'holdForManualAction')),
    reason                            text,
    replacement_product_id            uuid,
    existing_reservation_treatment    text CONSTRAINT lifecycle_action_existing_reservation_treatment_chk CHECK (existing_reservation_treatment IN ('honour', 'moveToReplacement', 'cancel')),
    existing_ticket_treatment         text CONSTRAINT lifecycle_action_existing_ticket_treatment_chk CHECK (existing_ticket_treatment IN ('remainValid', 'exchangeForReplacement', 'invalidate')),
    communication_requirements        text,
    reporting_treatment               text CONSTRAINT lifecycle_action_reporting_treatment_chk CHECK (reporting_treatment IN ('keepInReports', 'reportUnderReplacement', 'historicalOnly')),
    status                            text NOT NULL DEFAULT 'scheduled' CONSTRAINT lifecycle_action_status_chk CHECK (status IN ('scheduled', 'running', 'completed', 'failed', 'heldForManualAction')),
    failure_reason                    text,
    executed_at                       timestamptz,
    created_by_principal_id           uuid,
    created_at                        timestamptz,
    updated_at                        timestamptz
);

-- Holds 9 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS catalogue.lifecycle_workflow (
    id                                uuid PRIMARY KEY NOT NULL,
    scope_path                        ltree NOT NULL,
    venue_id                          uuid,
    statuses                          jsonb NOT NULL,
    transitions                       jsonb NOT NULL,
    edit_permissions                  jsonb,
    updated_by_principal_id           uuid,
    created_at                        timestamptz,
    updated_at                        timestamptz
);

-- Holds 10 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS catalogue.membership_benefit (
    id                                uuid PRIMARY KEY,
    code                              text NOT NULL CONSTRAINT membership_benefit_code_chk CHECK (char_length(code) <= 100),
    name                              text NOT NULL CONSTRAINT membership_benefit_name_chk CHECK (char_length(name) <= 150),
    type                              text NOT NULL CONSTRAINT membership_benefit_type_chk CHECK (char_length(type) <= 30),
    description                       text CONSTRAINT membership_benefit_description_chk CHECK (char_length(description) <= 500),
    value                             numeric(18,4),
    unit                              text CONSTRAINT membership_benefit_unit_chk CHECK (char_length(unit) <= 30),
    entitlement_template_id           uuid,
    is_active                         boolean NOT NULL,
    created_at                        timestamptz NOT NULL
);

-- Holds 8 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS catalogue.membership_programme (
    program_id                        uuid NOT NULL,
    program_code                      text NOT NULL CONSTRAINT membership_programme_program_code_chk CHECK (char_length(program_code) <= 100),
    program_name                      text NOT NULL CONSTRAINT membership_programme_program_name_chk CHECK (char_length(program_name) <= 150),
    description                       text CONSTRAINT membership_programme_description_chk CHECK (char_length(description) <= 500),
    is_active                         boolean NOT NULL,
    created_at                        timestamptz NOT NULL,
    updated_at                        timestamptz,
    id                                uuid PRIMARY KEY NOT NULL
);

-- Holds 14 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS catalogue.package_pricing (
    id                                uuid PRIMARY KEY NOT NULL,
    scope_path                        ltree NOT NULL,
    product_id                        uuid NOT NULL,
    record_kind                       text NOT NULL CONSTRAINT package_pricing_record_kind_chk CHECK (record_kind IN ('package', 'bundle', 'addOn')),
    name                              text CONSTRAINT package_pricing_name_chk CHECK (char_length(name) <= 200),
    price_list_id                     uuid,
    pricing_model                     text NOT NULL CONSTRAINT package_pricing_pricing_model_chk CHECK (pricing_model IN ('fixedPackagePrice', 'sumOfComponents', 'discountedComponentSum', 'componentOverride')),
    add_on_type                       text CONSTRAINT package_pricing_add_on_type_chk CHECK (add_on_type IN ('fastTrack', 'parking', 'meal', 'photo', 'equipment', 'upgrade', 'additionalPerformance', 'premiumAccess', 'other')),
    package_price                     numeric(18,4),
    components                        jsonb,
    component_price_visibility        text DEFAULT 'packageTotalOnly' CONSTRAINT package_pricing_component_price_visibility_chk CHECK (component_price_visibility IN ('packageTotalOnly', 'individualComponents', 'componentAndSaving')),
    status                            text NOT NULL DEFAULT 'draft',
    created_at                        timestamptz,
    updated_at                        timestamptz
);

-- When a product happens — a session, a showing, a timed entry slot. Capacity lives here and in
-- catalogue.channel_capacity, never on the product
CREATE TABLE IF NOT EXISTS catalogue.performance (
    id                                uuid PRIMARY KEY NOT NULL,
    event_id                          uuid NOT NULL,
    starts_at                         timestamptz NOT NULL,
    ends_at                           timestamptz NOT NULL,
    approval_request_id               uuid,
    requires_approval_to_cancel       boolean DEFAULT true,
    status                            text NOT NULL CONSTRAINT performance_status_chk CHECK (status IN ('scheduled', 'onSale', 'soldOut', 'suspended', 'cancelled', 'completed')),
    admission_rules_id                uuid,
    seat_map_id                       uuid,
    language                          text CONSTRAINT performance_language_chk CHECK (char_length(language) <= 35),
    format                            text CONSTRAINT performance_format_chk CHECK (char_length(format) <= 40)
);

-- Holds 7 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS catalogue.performance_media (
    id                                uuid PRIMARY KEY NOT NULL,
    scope_path                        ltree NOT NULL,
    performance_id                    uuid NOT NULL,
    participant_id                    uuid NOT NULL,
    asset_id                          uuid NOT NULL,
    assigned_by_principal_id          uuid,
    assigned_at                       timestamptz
);

-- Holds 9 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS catalogue.performance_template (
    id                                uuid PRIMARY KEY,
    code                              text NOT NULL,
    name                              text,
    space_id                          uuid,
    slot_minutes                      integer,
    turnaround_minutes                integer DEFAULT 0,
    concurrent_capacity               integer,
    walk_in                           jsonb,
    scope_path                        ltree NOT NULL
);

-- Holds 8 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS catalogue.plan_benefit (
    entitlement_template_id           uuid NOT NULL,
    membership_benefit_id             uuid NOT NULL,
    usage_limit                       numeric(18,4),
    usage_period                      text CONSTRAINT plan_benefit_usage_period_chk CHECK (char_length(usage_period) <= 30),
    priority                          integer NOT NULL,
    is_active                         boolean NOT NULL,
    created_at                        timestamptz NOT NULL,
    id                                uuid PRIMARY KEY NOT NULL
);

-- Holds 13 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS catalogue.prepaid_minutes (
    id                                uuid PRIMARY KEY,
    code                              text NOT NULL,
    name                              text,
    minutes                           integer NOT NULL,
    list_price                        numeric(18,4),
    credit_type_id                    uuid,
    rounding_minutes                  integer DEFAULT 1,
    minimum_draw_minutes              integer DEFAULT 0,
    band_multipliers_apply            boolean DEFAULT true,
    validity_months                   integer,
    transferable_within_household     boolean DEFAULT false,
    applicable_space_ids              text[],
    scope_path                        ltree NOT NULL
);

-- What something costs on one price list. A change here never rewrites what somebody already paid
CREATE TABLE IF NOT EXISTS catalogue.price (
    id                                uuid PRIMARY KEY,
    price_list_id                     uuid NOT NULL,
    variant_id                        uuid NOT NULL,
    amount                            numeric(18,4) NOT NULL,
    tax_code_id                       uuid
);

-- Holds 26 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS catalogue.price_assignment (
    id                                uuid PRIMARY KEY NOT NULL,
    scope_path                        ltree NOT NULL,
    price_list_id                     uuid NOT NULL,
    object_type                       text CONSTRAINT price_assignment_object_type_chk CHECK (object_type IN ('ticketProduct', 'ticketType', 'admission', 'event', 'performance', 'membership', 'annualPass', 'addOn', 'fnbItem', 'retailProduct', 'rentalItem', 'resource', 'reservationService', 'experience', 'otherSellableService')),
    object_ids                        text[],
    assignment_scope                  text CONSTRAINT price_assignment_assignment_scope_chk CHECK (assignment_scope IN ('productLevel', 'productVariant', 'ticketType', 'event', 'performance', 'venue')),
    scope_ref_id                      uuid,
    category_rates                    jsonb,
    sales_channel_id                  uuid,
    pricing_source                    text CONSTRAINT price_assignment_pricing_source_chk CHECK (pricing_source IN ('standardPriceList', 'channelPriceList', 'b2bRate', 'resellerRate', 'otaRate', 'posPrice', 'promotionalPriceProfile', 'dynamicPricingProfile')),
    venue_id                          uuid,
    event_id                          uuid,
    product_id                        uuid,
    customer_segment                  text CONSTRAINT price_assignment_customer_segment_chk CHECK (char_length(customer_segment) <= 60),
    priority                          integer NOT NULL DEFAULT 0,
    effective_from                    timestamptz,
    effective_to                      timestamptz,
    override_permission               text CONSTRAINT price_assignment_override_permission_chk CHECK (char_length(override_permission) <= 100),
    is_fixed_price_only               boolean DEFAULT false,
    is_promotion_allowed              boolean DEFAULT true,
    is_discount_allowed               boolean DEFAULT true,
    is_price_override_allowed         boolean DEFAULT false,
    override_requires_approval        boolean DEFAULT true,
    is_dynamic_pricing_allowed        boolean DEFAULT false,
    created_at                        timestamptz,
    updated_at                        timestamptz
);

-- Holds 16 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS catalogue.price_category (
    id                                uuid PRIMARY KEY NOT NULL,
    scope_path                        ltree NOT NULL,
    entry_kind                        text NOT NULL CONSTRAINT price_category_entry_kind_chk CHECK (entry_kind IN ('priceCategory', 'rateType')),
    code                              text NOT NULL CONSTRAINT price_category_code_chk CHECK (char_length(code) <= 40),
    name                              text NOT NULL CONSTRAINT price_category_name_chk CHECK (char_length(name) <= 200),
    description                       text,
    category_family                   text CONSTRAINT price_category_category_family_chk CHECK (char_length(category_family) <= 60),
    display_name                      text CONSTRAINT price_category_display_name_chk CHECK (char_length(display_name) <= 200),
    localized_display_names           jsonb,
    icon_label                        text CONSTRAINT price_category_icon_label_chk CHECK (char_length(icon_label) <= 40),
    parent_id                         uuid,
    is_standard                       boolean DEFAULT false,
    sort_order                        integer DEFAULT 100,
    is_active                         boolean NOT NULL DEFAULT true,
    created_at                        timestamptz,
    updated_at                        timestamptz
);

-- Holds 20 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS catalogue.price_execution (
    id                                uuid PRIMARY KEY NOT NULL,
    scope_path                        ltree NOT NULL,
    product_id                        uuid,
    event_id                          uuid,
    performance_id                    uuid,
    previous_price                    numeric(18,4),
    new_price                         numeric(18,4) NOT NULL,
    dynamic_pricing_strategy_id       uuid,
    pricing_recommendation_id         uuid,
    approval_request_id               uuid,
    execution_source                  text NOT NULL CONSTRAINT price_execution_execution_source_chk CHECK (execution_source IN ('manual', 'humanApproved', 'scheduled', 'conditionalAutonomous', 'autonomous')),
    trigger                           text CONSTRAINT price_execution_trigger_chk CHECK (char_length(trigger) <= 200),
    channel_deployments               jsonb,
    price_inconsistency               boolean DEFAULT false,
    ai_confidence                     numeric(18,4),
    status                            text NOT NULL DEFAULT 'executing' CONSTRAINT price_execution_status_chk CHECK (status IN ('scheduled', 'executing', 'deployed', 'partiallyDeployed', 'failed', 'reverted')),
    scheduled_for                     timestamptz,
    executed_at                       timestamptz,
    executed_by_principal_id          uuid,
    created_at                        timestamptz NOT NULL
);

-- Holds 22 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS catalogue.price_ladder (
    id                                uuid PRIMARY KEY NOT NULL,
    scope_path                        ltree NOT NULL,
    dynamic_pricing_strategy_id       uuid NOT NULL,
    base_price_source                 text CONSTRAINT price_ladder_base_price_source_chk CHECK (char_length(base_price_source) <= 100),
    adjustment_model                  text NOT NULL CONSTRAINT price_ladder_adjustment_model_chk CHECK (adjustment_model IN ('fixedPriceBands', 'percentageBands', 'fixedAmountSteps', 'derivedBands', 'continuousRange')),
    bands                             jsonb,
    base_band_code                    text CONSTRAINT price_ladder_base_band_code_chk CHECK (char_length(base_band_code) <= 40),
    step_amount                       numeric(18,4),
    minimum_price                     numeric(18,4),
    base_price                        numeric(18,4),
    maximum_price                     numeric(18,4),
    allow_upward                      boolean DEFAULT true,
    allow_downward                    boolean DEFAULT true,
    max_increase_percent_per_adjustment numeric(18,4),
    max_decrease_percent_per_adjustment numeric(18,4),
    maximum_bands_per_movement        integer,
    minimum_minutes_between_movements integer,
    cooldown_minutes                  integer,
    reversal_rule                     text DEFAULT 'afterCooldown' CONSTRAINT price_ladder_reversal_rule_chk CHECK (reversal_rule IN ('allowed', 'afterCooldown', 'notAllowed')),
    allowed_endpoints                 text[],
    created_at                        timestamptz,
    updated_at                        timestamptz
);

-- A named set of prices for a region and channel. Region-scoped, because currency is (ADR-0018)
CREATE TABLE IF NOT EXISTS catalogue.price_list (
    id                                uuid PRIMARY KEY NOT NULL,
    code                              text NOT NULL,
    name                              text NOT NULL,
    venue_id                          uuid NOT NULL,
    channels                          text[] NOT NULL,
    valid_from                        timestamptz,
    valid_to                          timestamptz,
    priority                          integer,
    description                       text,
    price_list_type                   text DEFAULT 'standardRetail' CONSTRAINT price_list_price_list_type_chk CHECK (price_list_type IN ('standardRetail', 'venue', 'attraction', 'event', 'membership', 'group', 'corporate', 'b2b', 'reseller', 'ota', 'internal', 'specialMarket')),
    status                            text DEFAULT 'active',
    owner_principal_id                uuid,
    tags                              text[],
    legal_entity_id                   uuid,
    brand                             text CONSTRAINT price_list_brand_chk CHECK (char_length(brand) <= 100),
    business_unit                     text CONSTRAINT price_list_business_unit_chk CHECK (char_length(business_unit) <= 100),
    country_code                      text CONSTRAINT price_list_country_code_chk CHECK (char_length(country_code) <= 2),
    market_code                       text CONSTRAINT price_list_market_code_chk CHECK (char_length(market_code) <= 40),
    scope_level                       text DEFAULT 'venue' CONSTRAINT price_list_scope_level_chk CHECK (scope_level IN ('global', 'country', 'market', 'brand', 'venue', 'event', 'businessUnit')),
    default_price_category_id         uuid,
    rounding_profile_id               uuid,
    price_resolution_policy_id        uuid,
    allow_overrides                   boolean DEFAULT false,
    allow_inheritance                 boolean DEFAULT true,
    allow_multiple_currencies         boolean DEFAULT false,
    allow_product_specific_rates      boolean DEFAULT true,
    cloned_from_price_list_id         uuid,
    current_version                   integer
);

-- Holds 19 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS catalogue.price_list_version (
    id                                uuid PRIMARY KEY NOT NULL,
    scope_path                        ltree NOT NULL,
    price_list_id                     uuid NOT NULL,
    version                           integer NOT NULL,
    effective_from                    timestamptz,
    change_request_id                 uuid,
    product_count                     integer,
    change_count                      integer,
    added                             integer,
    removed                           integer,
    modified                          integer,
    unchanged                         integer,
    is_commercial_baseline            boolean DEFAULT false,
    status                            text NOT NULL DEFAULT 'scheduled' CONSTRAINT price_list_version_status_chk CHECK (status IN ('scheduled', 'active', 'superseded', 'rolledBack')),
    snapshot                          jsonb,
    content_hash                      text CONSTRAINT price_list_version_content_hash_chk CHECK (char_length(content_hash) <= 128),
    restored_from_version             integer,
    created_by_principal_id           uuid,
    created_at                        timestamptz NOT NULL
);

-- Holds 11 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS catalogue.price_resolution_policy (
    id                                uuid PRIMARY KEY NOT NULL,
    scope_path                        ltree NOT NULL,
    policy_kind                       text NOT NULL CONSTRAINT price_resolution_policy_policy_kind_chk CHECK (policy_kind IN ('staticHierarchy', 'dynamicRuleResolution')),
    name                              text NOT NULL CONSTRAINT price_resolution_policy_name_chk CHECK (char_length(name) <= 200),
    levels                            jsonb,
    resolution_method                 text CONSTRAINT price_resolution_policy_resolution_method_chk CHECK (resolution_method IN ('highestPriorityWins', 'mostSpecificRuleWins', 'cumulativeAdjustment', 'maximumAdjustmentWins', 'minimumAdjustmentWins', 'weightedCombination', 'stopProcessing', 'customGovernedResolution')),
    priority_hierarchy                text[],
    is_default                        boolean DEFAULT false,
    updated_by_principal_id           uuid,
    created_at                        timestamptz,
    updated_at                        timestamptz
);

-- Holds 25 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS catalogue.pricing_experiment (
    id                                uuid PRIMARY KEY NOT NULL,
    scope_path                        ltree NOT NULL,
    name                              text NOT NULL CONSTRAINT pricing_experiment_name_chk CHECK (char_length(name) <= 200),
    objective                         text,
    product_id                        uuid,
    event_id                          uuid,
    performance_id                    uuid,
    channel                           text,
    customer_segment                  text CONSTRAINT pricing_experiment_customer_segment_chk CHECK (char_length(customer_segment) <= 60),
    start_date                        date,
    end_date                          date,
    minimum_price                     numeric(18,4),
    maximum_price                     numeric(18,4),
    variants                          jsonb,
    success_metrics                   text[],
    target_confidence_level           numeric(18,4),
    sample_size                       integer,
    guardrail_checks                  jsonb,
    variant_results                   jsonb,
    recommended_winner                text CONSTRAINT pricing_experiment_recommended_winner_chk CHECK (char_length(recommended_winner) <= 200),
    statistical_significance          boolean,
    stage                             text NOT NULL DEFAULT 'draft' CONSTRAINT pricing_experiment_stage_chk CHECK (stage IN ('draft', 'pendingApproval', 'running', 'paused', 'completed', 'cancelled')),
    created_by_principal_id           uuid,
    created_at                        timestamptz,
    updated_at                        timestamptz
);

-- Holds 19 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS catalogue.pricing_market (
    id                                uuid PRIMARY KEY NOT NULL,
    scope_path                        ltree NOT NULL,
    hierarchy_level                   text NOT NULL CONSTRAINT pricing_market_hierarchy_level_chk CHECK (hierarchy_level IN ('global', 'country', 'region', 'market', 'venue')),
    parent_id                         uuid,
    country_code                      text CONSTRAINT pricing_market_country_code_chk CHECK (char_length(country_code) <= 2),
    market_code                       text CONSTRAINT pricing_market_market_code_chk CHECK (char_length(market_code) <= 40),
    region                            text CONSTRAINT pricing_market_region_chk CHECK (char_length(region) <= 100),
    venue_id                          uuid,
    brand                             text CONSTRAINT pricing_market_brand_chk CHECK (char_length(brand) <= 100),
    legal_entity_id                   uuid,
    base_currency                     text CONSTRAINT pricing_market_base_currency_chk CHECK (char_length(base_currency) <= 3),
    selling_currency                  text CONSTRAINT pricing_market_selling_currency_chk CHECK (char_length(selling_currency) <= 3),
    rounding_profile_id               uuid,
    display_format                    text CONSTRAINT pricing_market_display_format_chk CHECK (char_length(display_format) <= 40),
    price_list_id                     uuid,
    inherits_from_parent              boolean DEFAULT true,
    fx_reference_rate                 numeric(18,4),
    created_at                        timestamptz,
    updated_at                        timestamptz
);

-- Holds 19 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS catalogue.pricing_publication (
    id                                uuid PRIMARY KEY NOT NULL,
    scope_path                        ltree NOT NULL,
    change_request_id                 uuid NOT NULL,
    price_list_version_id             uuid,
    publication_mode                  text NOT NULL CONSTRAINT pricing_publication_publication_mode_chk CHECK (publication_mode IN ('immediate', 'scheduled', 'futureEffectiveDate', 'staged')),
    publication_date                  timestamptz,
    effective_date                    timestamptz NOT NULL,
    visit_effective_from              timestamptz,
    expiry_date                       timestamptz,
    venue_id                          uuid,
    market_code                       text CONSTRAINT pricing_publication_market_code_chk CHECK (char_length(market_code) <= 40),
    channel                           text,
    stages                            jsonb,
    pre_publication_checks            jsonb,
    status                            text NOT NULL DEFAULT 'scheduled' CONSTRAINT pricing_publication_status_chk CHECK (status IN ('scheduled', 'publishing', 'published', 'partiallyFailed', 'failed', 'cancelled')),
    cancelled_at                      timestamptz,
    created_by_principal_id           uuid,
    created_at                        timestamptz,
    updated_at                        timestamptz
);

-- Holds 11 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS catalogue.pricing_publication_target (
    id                                uuid PRIMARY KEY NOT NULL,
    pricing_publication_id            uuid NOT NULL,
    target                            text NOT NULL CONSTRAINT pricing_publication_target_target_chk CHECK (target IN ('b2c', 'mobileApp', 'pos', 'mobilePos', 'kiosk', 'callCenter', 'b2b', 'reseller', 'ota', 'api', 'cacheCdn', 'externalSystem')),
    target_name                       text CONSTRAINT pricing_publication_target_target_name_chk CHECK (char_length(target_name) <= 200),
    status                            text NOT NULL DEFAULT 'pending' CONSTRAINT pricing_publication_target_status_chk CHECK (status IN ('pending', 'publishing', 'inSync', 'failed')),
    started_at                        timestamptz,
    last_updated_at                   timestamptz,
    records_published                 integer DEFAULT 0,
    records_failed                    integer DEFAULT 0,
    latency_ms                        numeric(18,4),
    failure_reason                    text
);

-- Holds 29 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS catalogue.pricing_recommendation (
    id                                uuid PRIMARY KEY NOT NULL,
    scope_path                        ltree NOT NULL,
    venue_id                          uuid,
    product_id                        uuid,
    event_id                          uuid,
    performance_id                    uuid,
    price_category_id                 uuid,
    dynamic_pricing_strategy_id       uuid,
    demand_forecast_id                uuid,
    current_price                     numeric(18,4) NOT NULL,
    recommended_price                 numeric(18,4) NOT NULL,
    adjustment_percent                numeric(18,4),
    demand_forecast                   integer,
    expected_occupancy                numeric(18,4),
    demand_impact                     numeric(18,4),
    revenue_opportunity               numeric(18,4),
    confidence                        numeric(18,4),
    confidence_breakdown              jsonb,
    risk                              text CONSTRAINT pricing_recommendation_risk_chk CHECK (risk IN ('low', 'medium', 'high')),
    urgency                           text CONSTRAINT pricing_recommendation_urgency_chk CHECK (urgency IN ('low', 'medium', 'high', 'critical')),
    drivers                           jsonb,
    counterfactuals                   jsonb,
    explanation                       text,
    governance_level                  text CONSTRAINT pricing_recommendation_governance_level_chk CHECK (char_length(governance_level) <= 60),
    is_guardrails_passed              boolean,
    status                            text NOT NULL DEFAULT 'pending' CONSTRAINT pricing_recommendation_status_chk CHECK (status IN ('pending', 'accepted', 'rejected', 'modified', 'ignored', 'sentToSimulation', 'sentForApproval')),
    model_version                     text CONSTRAINT pricing_recommendation_model_version_chk CHECK (char_length(model_version) <= 60),
    generated_at                      timestamptz NOT NULL,
    expires_at                        timestamptz,
    recommendation_type               text DEFAULT 'standard' CONSTRAINT pricing_recommendation_recommendation_type_chk CHECK (recommendation_type IN ('standard', 'earlyBird', 'lastMinute', 'volumeDiscount', 'conversion')),
    valid_from                        timestamptz,
    valid_to                          timestamptz,
    quantity_tier                     jsonb,
    objective                         text DEFAULT 'revenue' CONSTRAINT pricing_recommendation_objective_chk CHECK (objective IN ('revenue', 'occupancy', 'conversion'))
);

-- Holds 13 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS catalogue.pricing_recommendation_decision (
    id                                uuid PRIMARY KEY NOT NULL,
    recommendation_id                 uuid NOT NULL,
    decision                          text NOT NULL CONSTRAINT pricing_recommendation_decision_decision_chk CHECK (decision IN ('accept', 'modify', 'reject', 'schedule', 'sendForApproval')),
    rejection_reason                  text CONSTRAINT pricing_recommendation_decision_rejection_reason_chk CHECK (rejection_reason IN ('commercialJudgment', 'brandPositioning', 'customerSensitivity', 'eventStrategy', 'incorrectSignal', 'dataConcern', 'other')),
    rejection_note                    text,
    recommended_price                 numeric(18,4),
    human_selected_price              numeric(18,4),
    scheduled_for                     timestamptz,
    approval_request_id               uuid,
    execution_id                      text,
    decided_by_principal_id           uuid NOT NULL,
    decided_at                        timestamptz NOT NULL,
    scope_path                        ltree NOT NULL
);

-- Holds 35 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS catalogue.pricing_simulation (
    id                                uuid PRIMARY KEY NOT NULL,
    scope_path                        ltree NOT NULL,
    simulation_kind                   text NOT NULL CONSTRAINT pricing_simulation_simulation_kind_chk CHECK (simulation_kind IN ('priceChange', 'whatIfScenario')),
    name                              text CONSTRAINT pricing_simulation_name_chk CHECK (char_length(name) <= 200),
    simulation_source                 text CONSTRAINT pricing_simulation_simulation_source_chk CHECK (simulation_source IN ('manualPriceChange', 'dynamicRule', 'aiRecommendation', 'newDynamicStrategy', 'strategyModification', 'bulkPriceChange')),
    source_reference                  text CONSTRAINT pricing_simulation_source_reference_chk CHECK (char_length(source_reference) <= 100),
    pricing_recommendation_id         uuid,
    venue_id                          uuid,
    product_id                        uuid,
    event_id                          uuid,
    performance_id                    uuid,
    timeslot                          text CONSTRAINT pricing_simulation_timeslot_chk CHECK (char_length(timeslot) <= 40),
    price_category_id                 uuid,
    channel                           text,
    customer_segment                  text CONSTRAINT pricing_simulation_customer_segment_chk CHECK (char_length(customer_segment) <= 60),
    date_from                         date,
    date_to                           date,
    current_price                     numeric(18,4),
    proposed_price                    numeric(18,4),
    proposed_adjustment_percent       numeric(18,4),
    scenario_types                    text[],
    scenario_inputs                   jsonb,
    baseline_revenue                  numeric(18,4),
    expected_revenue                  numeric(18,4),
    baseline                          jsonb,
    forecast                          jsonb,
    impact                            jsonb,
    customer_impacts                  jsonb,
    cannibalisation                   jsonb,
    strategy_results                  jsonb,
    guardrail_checks                  jsonb,
    review_stage                      text CONSTRAINT pricing_simulation_review_stage_chk CHECK (char_length(review_stage) <= 40),
    created_by_principal_id           uuid,
    created_at                        timestamptz NOT NULL,
    updated_at                        timestamptz
);

-- Holds 14 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS catalogue.pricing_test_case (
    id                                uuid PRIMARY KEY NOT NULL,
    scope_path                        ltree NOT NULL,
    case_kind                         text NOT NULL CONSTRAINT pricing_test_case_case_kind_chk CHECK (case_kind IN ('calculation', 'dynamicRule')),
    name                              text NOT NULL CONSTRAINT pricing_test_case_name_chk CHECK (char_length(name) <= 200),
    case_type                         text CONSTRAINT pricing_test_case_case_type_chk CHECK (char_length(case_type) <= 60),
    inputs                            jsonb,
    expected_price                    numeric(18,4),
    last_result                       jsonb,
    is_passed                         boolean,
    calculation_version               text CONSTRAINT pricing_test_case_calculation_version_chk CHECK (char_length(calculation_version) <= 40),
    last_run_at                       timestamptz,
    created_by_principal_id           uuid,
    created_at                        timestamptz,
    updated_at                        timestamptz
);

-- What a venue sells — admission, a session, a bundle, a membership, a locker. Not the instance: a
-- product is the offer and catalogue.performance is the occasion
CREATE TABLE IF NOT EXISTS catalogue.product (
    id                                uuid PRIMARY KEY NOT NULL,
    code                              text NOT NULL CONSTRAINT product_code_chk CHECK (char_length(code) <= 64),
    family_key                        text CONSTRAINT product_family_key_chk CHECK (char_length(family_key) <= 64),
    name                              text NOT NULL CONSTRAINT product_name_chk CHECK (char_length(name) <= 200),
    description                       text,
    kind                              text NOT NULL CONSTRAINT product_kind_chk CHECK (kind IN ('admission', 'timedAdmission', 'datedAdmission', 'openDated', 'seated', 'membership', 'bundle', 'fnb', 'retail', 'rental', 'addOn', 'giftCard')),
    venue_id                          uuid NOT NULL,
    scope_path                        ltree NOT NULL,
    created_by_principal_id           uuid,
    approved_by_principal_id          uuid,
    responsible_department_id         uuid,
    on_sale_from                      timestamptz,
    on_sale_to                        timestamptz,
    category_id                       uuid,
    lifecycle_state                   text CONSTRAINT product_lifecycle_state_chk CHECK (lifecycle_state IN ('draft', 'inReview', 'approved', 'live', 'withdrawn', 'archived')),
    is_sellable                       boolean NOT NULL,
    is_stock_tracked                  boolean DEFAULT false,
    has_variants                      boolean NOT NULL,
    variant_count                     integer,
    segment_tags                      text[],
    code_schema                       text,
    channels                          text[],
    entitlement_template_id           uuid,
    blocked_offline                   boolean,
    data_mask_values                  jsonb,
    guest_listing                     text DEFAULT 'bookable' CONSTRAINT product_guest_listing_chk CHECK (guest_listing IN ('bookable', 'infoOnly', 'hidden')),
    not_bookable_label                jsonb,
    sales_contact                     jsonb,
    booking_flow_id                   uuid,
    consent_question_ids              text[],
    requires_time_window              boolean DEFAULT false,
    product_owner_principal_id        uuid,
    operational_contact               text CONSTRAINT product_operational_contact_chk CHECK (char_length(operational_contact) <= 200),
    business_unit_id                  uuid,
    legal_entity_id                   uuid,
    attraction_id                     uuid,
    site_id                           uuid,
    location_id                       uuid,
    brand_id                          uuid,
    market_code                       text CONSTRAINT product_market_code_chk CHECK (char_length(market_code) <= 40),
    sales_territory                   text CONSTRAINT product_sales_territory_chk CHECK (char_length(sales_territory) <= 100)
);

-- The merchandise hierarchy — categories, brands, collections (Retail Board 2, 20 August).
-- listSeatCategories existed and a product category did not. One tree rather than four tables,
-- because a brand under a department under a category is how a real hierarchy runs
CREATE TABLE IF NOT EXISTS catalogue.product_category (
    id                                uuid PRIMARY KEY NOT NULL,
    name                              text NOT NULL,
    code                              text CONSTRAINT product_category_code_chk CHECK (char_length(code) <= 64),
    name_localised                    jsonb,
    kind                              text NOT NULL CONSTRAINT product_category_kind_chk CHECK (kind IN ('category', 'brand', 'collection', 'season', 'department')),
    parent_id                         uuid,
    scope_path                        ltree NOT NULL,
    display_order                     integer DEFAULT 100,
    image_asset_id                    uuid,
    description                       jsonb,
    booking_flow_id                   uuid,
    is_active                         boolean DEFAULT true
);

-- Holds 17 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS catalogue.product_channel_assignment (
    id                                uuid PRIMARY KEY NOT NULL,
    scope_path                        ltree NOT NULL,
    product_id                        uuid NOT NULL,
    sales_channel_id                  uuid,
    channel                           text NOT NULL CONSTRAINT product_channel_assignment_channel_chk CHECK (channel IN ('pos', 'kiosk', 'web', 'mobile', 'b2b', 'ota', 'callCentre')),
    is_enabled                        boolean NOT NULL DEFAULT true,
    site_ids                          text[],
    pos_group_ids                     text[],
    venue_ids                         text[],
    assignment_method                 text DEFAULT 'individualProduct' CONSTRAINT product_channel_assignment_assignment_method_chk CHECK (assignment_method IN ('individualProduct', 'productFamily', 'productCategory', 'event', 'attraction', 'venueCatalogue', 'productCollection', 'entireApprovedCatalogue')),
    assignment_target_id              uuid,
    inherited_from                    text CONSTRAINT product_channel_assignment_inherited_from_chk CHECK (inherited_from IN ('globalChannelCatalogue', 'venueCatalogue', 'channelOverride')),
    is_excluded                       boolean DEFAULT false,
    effective_from                    timestamptz,
    effective_to                      timestamptz,
    created_at                        timestamptz,
    updated_at                        timestamptz
);

-- Who may take part in a product: age, height, supervision, swim ability. Declared by the guest at
-- booking, checked by staff at the gate; whether a guest who fails there is refunded is a column,
-- because the design says they are not
CREATE TABLE IF NOT EXISTS catalogue.product_eligibility_rule (
    id                                uuid PRIMARY KEY,
    product_id                        text,
    min_age_years                     integer,
    max_age_years                     integer,
    min_height_cm                     integer,
    max_height_cm                     integer,
    height_bands_cm                   integer[],
    accompanied_below_age             integer,
    guardian_signature_age_from       integer,
    guardian_signature_age_to         integer,
    is_waiver_required                boolean DEFAULT false,
    swim_ability                      text DEFAULT 'notRequired' CONSTRAINT product_eligibility_rule_swim_ability_chk CHECK (swim_ability IN ('notRequired', 'confident')),
    refundable_if_ineligible_at_gate  boolean DEFAULT false,
    required_certification_code       text CONSTRAINT product_eligibility_rule_required_certification_code_chk CHECK (char_length(required_certification_code) <= 60),
    scope_path                        ltree NOT NULL
);

-- Holds 10 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS catalogue.product_link (
    id                                uuid PRIMARY KEY NOT NULL,
    scope_path                        ltree NOT NULL,
    source_product_id                 uuid NOT NULL,
    dependency_type                   text NOT NULL CONSTRAINT product_link_dependency_type_chk CHECK (dependency_type IN ('parentProduct', 'childProduct', 'bundle', 'addOn', 'upgrade', 'membership', 'package', 'promotion', 'priceProfile', 'capacityPool', 'entitlement', 'salesChannel', 'mediaTemplate')),
    linked_object_id                  uuid NOT NULL,
    linked_object_name                text CONSTRAINT product_link_linked_object_name_chk CHECK (char_length(linked_object_name) <= 200),
    propagates_changes                boolean DEFAULT true,
    overridden_fields                 text[],
    created_at                        timestamptz,
    updated_at                        timestamptz
);

-- Holds 6 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS catalogue.product_media (
    asset_id                          uuid NOT NULL,
    kind                              text NOT NULL CONSTRAINT product_media_kind_chk CHECK (kind IN ('image', 'video')),
    is_primary                        boolean NOT NULL DEFAULT false,
    display_order                     integer DEFAULT 100,
    alt_text                          jsonb,
    id                                uuid PRIMARY KEY NOT NULL
);

-- Version history for a product (BL-030, BL-047, BL-058). A restore creates a new version rather
-- than rewinding, so a price that was wrong for three days stays reproducible
CREATE TABLE IF NOT EXISTS catalogue.product_version (
    version                           integer NOT NULL,
    product_id                        uuid,
    published_at                      timestamptz NOT NULL,
    published_by_principal_id         uuid NOT NULL,
    note                              text,
    is_current                        boolean,
    content_hash                      text,
    restored_from_version             integer,
    id                                uuid PRIMARY KEY NOT NULL
);

-- A catalogue snapshot a till can trade from offline (ADR-0013). Published, versioned, and the
-- reason a counter works with no network
CREATE TABLE IF NOT EXISTS catalogue.published_bundle (
    version                           text NOT NULL,
    venue_id                          uuid NOT NULL,
    is_delta                          boolean NOT NULL,
    base_version                      text,
    signature                         text NOT NULL,
    signature_key_id                  text NOT NULL,
    content_hash                      text NOT NULL,
    stale_after                       timestamptz NOT NULL,
    payload                           jsonb NOT NULL,
    id                                uuid PRIMARY KEY NOT NULL
);

-- Holds 17 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS catalogue.rate (
    id                                uuid PRIMARY KEY NOT NULL,
    scope_path                        ltree NOT NULL,
    price_list_id                     uuid NOT NULL,
    price_category_id                 uuid NOT NULL,
    rate_type_id                      uuid,
    code                              text NOT NULL CONSTRAINT rate_code_chk CHECK (char_length(code) <= 40),
    name                              text NOT NULL CONSTRAINT rate_name_chk CHECK (char_length(name) <= 200),
    amount                            numeric(18,4),
    unit_basis                        text NOT NULL CONSTRAINT rate_unit_basis_chk CHECK (unit_basis IN ('perTicket', 'perPerson', 'perUnit', 'perHour', 'perDay', 'perPerformance', 'perResource', 'perPackage', 'perMembershipPeriod')),
    precision                         integer,
    rounding_profile_id               uuid,
    base_rate_id                      uuid,
    adjustment_type                   text CONSTRAINT rate_adjustment_type_chk CHECK (adjustment_type IN ('percentage', 'fixedAmount')),
    adjustment_value                  numeric(18,4),
    status                            text NOT NULL DEFAULT 'draft',
    created_at                        timestamptz,
    updated_at                        timestamptz
);

-- Holds 26 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS catalogue.rollback_action (
    id                                uuid PRIMARY KEY NOT NULL,
    scope_path                        ltree NOT NULL,
    subject                           text NOT NULL CONSTRAINT rollback_action_subject_chk CHECK (subject IN ('product', 'pricing')),
    action_type                       text NOT NULL CONSTRAINT rollback_action_action_type_chk CHECK (action_type IN ('rollback', 'freezePriceList', 'freezeProductPricing', 'freezeVenuePricing', 'stopScheduledPublication', 'stopDistribution', 'restoreLastKnownGood')),
    product_id                        uuid,
    price_list_id                     uuid,
    from_version                      integer,
    to_version                        integer,
    product_scope                     text[],
    rollback_target                   text CONSTRAINT rollback_action_rollback_target_chk CHECK (rollback_target IN ('previousVersion', 'selectedVersion', 'previousPrice', 'commercialBaseline')),
    rollback_scope                    text CONSTRAINT rollback_action_rollback_scope_chk CHECK (rollback_scope IN ('selectedProducts', 'selectedVenue', 'selectedMarket', 'selectedChannel', 'entirePublication')),
    scope_ids                         text[],
    dependencies                      text[],
    reason                            text NOT NULL,
    execution_mode                    text DEFAULT 'immediate' CONSTRAINT rollback_action_execution_mode_chk CHECK (execution_mode IN ('immediate', 'scheduled')),
    is_emergency                      boolean DEFAULT false,
    scheduled_at                      timestamptz,
    incident_reference                text CONSTRAINT rollback_action_incident_reference_chk CHECK (char_length(incident_reference) <= 200),
    authorised_role                   text CONSTRAINT rollback_action_authorised_role_chk CHECK (char_length(authorised_role) <= 100),
    is_retrospective_approval_required boolean DEFAULT false,
    approval_request_id               uuid,
    change_request_id                 uuid,
    status                            text NOT NULL DEFAULT 'requested' CONSTRAINT rollback_action_status_chk CHECK (status IN ('requested', 'scheduled', 'executing', 'completed', 'failed', 'cancelled')),
    requested_by_principal_id         uuid NOT NULL,
    requested_at                      timestamptz NOT NULL,
    completed_at                      timestamptz
);

-- Holds 15 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS catalogue.rounding_profile (
    id                                uuid PRIMARY KEY NOT NULL,
    scope_path                        ltree NOT NULL,
    code                              text CONSTRAINT rounding_profile_code_chk CHECK (char_length(code) <= 40),
    name                              text CONSTRAINT rounding_profile_name_chk CHECK (char_length(name) <= 200),
    currency                          text NOT NULL CONSTRAINT rounding_profile_currency_chk CHECK (char_length(currency) <= 3),
    decimal_places                    integer NOT NULL,
    minimum_monetary_unit             numeric(18,4),
    display_precision                 integer,
    calculation_precision             integer DEFAULT 4,
    rounding_method                   text NOT NULL CONSTRAINT rounding_profile_rounding_method_chk CHECK (rounding_method IN ('standard', 'roundUp', 'roundDown', 'bankers', 'nearestCurrencyUnit', 'customRegulatoryRule')),
    rounding_stage                    text NOT NULL CONSTRAINT rounding_profile_rounding_stage_chk CHECK (rounding_stage IN ('perItem', 'perTax', 'perFee', 'perLine', 'atOrderTotal')),
    cash_rounding_increment           numeric(18,4),
    status                            text NOT NULL DEFAULT 'active',
    created_at                        timestamptz,
    updated_at                        timestamptz
);

-- Holds 45 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS catalogue.sales_channel (
    id                                uuid PRIMARY KEY NOT NULL,
    scope_path                        ltree NOT NULL,
    code                              text NOT NULL CONSTRAINT sales_channel_code_chk CHECK (char_length(code) <= 40),
    name                              text NOT NULL CONSTRAINT sales_channel_name_chk CHECK (char_length(name) <= 200),
    customer_facing_name              text CONSTRAINT sales_channel_customer_facing_name_chk CHECK (char_length(customer_facing_name) <= 200),
    internal_description              text,
    channel_type                      text NOT NULL CONSTRAINT sales_channel_channel_type_chk CHECK (channel_type IN ('b2cWeb', 'b2cMobileApp', 'pos', 'mobilePos', 'flyingPos', 'kiosk', 'callCentre', 'b2bPortal', 'reseller', 'ota', 'api', 'partnerPortal', 'marketplace', 'thirdPartyChannel', 'customChannel')),
    sales_channel                     text NOT NULL CONSTRAINT sales_channel_sales_channel_chk CHECK (sales_channel IN ('pos', 'kiosk', 'guestApp', 'guestWeb', 'callCentre', 'partner', 'api', 'backOffice', 'b2b', 'ota')),
    scope_level                       text DEFAULT 'venue' CONSTRAINT sales_channel_scope_level_chk CHECK (scope_level IN ('global', 'country', 'region', 'venue', 'attraction', 'event', 'location', 'businessUnit')),
    scope_id                          uuid,
    venue_id                          uuid,
    brand                             text CONSTRAINT sales_channel_brand_chk CHECK (char_length(brand) <= 100),
    business_unit                     text CONSTRAINT sales_channel_business_unit_chk CHECK (char_length(business_unit) <= 100),
    country_code                      text CONSTRAINT sales_channel_country_code_chk CHECK (char_length(country_code) <= 2),
    market_code                       text CONSTRAINT sales_channel_market_code_chk CHECK (char_length(market_code) <= 40),
    time_zone                         text CONSTRAINT sales_channel_time_zone_chk CHECK (char_length(time_zone) <= 64),
    owner_principal_id                uuid,
    responsible_department_id         uuid,
    commercial_owner_principal_id     uuid,
    operational_owner_principal_id    uuid,
    technical_owner_principal_id      uuid,
    finance_owner_principal_id        uuid,
    settings                          jsonb,
    fee_profiles                      jsonb,
    payment_methods                   text[],
    other_payment_method_codes        text[],
    fulfillment_methods               text[],
    partner_owner                     text CONSTRAINT sales_channel_partner_owner_chk CHECK (char_length(partner_owner) <= 200),
    commercial_agreement_reference    text CONSTRAINT sales_channel_commercial_agreement_reference_chk CHECK (char_length(commercial_agreement_reference) <= 200),
    sla_targets                       jsonb,
    transaction_limit                 integer,
    rate_limit                        integer,
    contract_start                    date,
    contract_end                      date,
    renewal_date                      date,
    support_contacts                  text[],
    escalation_contacts               text[],
    review_frequency                  text CONSTRAINT sales_channel_review_frequency_chk CHECK (review_frequency IN ('monthly', 'quarterly', 'semiAnnual', 'annual')),
    compliance_flags                  text[],
    readiness_score                   numeric(18,4),
    readiness_checked_at              timestamptz,
    activation_scheduled_at           timestamptz,
    status                            text NOT NULL DEFAULT 'draft' CONSTRAINT sales_channel_status_chk CHECK (status IN ('draft', 'pendingApproval', 'scheduled', 'active', 'suspended')),
    created_at                        timestamptz,
    updated_at                        timestamptz
);

-- Holds 25 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS catalogue.signal_registry (
    id                                uuid PRIMARY KEY NOT NULL,
    scope_path                        ltree NOT NULL,
    registry_kind                     text NOT NULL CONSTRAINT signal_registry_registry_kind_chk CHECK (registry_kind IN ('signal', 'model')),
    name                              text NOT NULL CONSTRAINT signal_registry_name_chk CHECK (char_length(name) <= 200),
    category                          text CONSTRAINT signal_registry_category_chk CHECK (category IN ('internalSales', 'inventory', 'weather', 'nearbyEvents', 'competitor', 'tourism', 'calendar', 'transport', 'market', 'other')),
    provider                          text CONSTRAINT signal_registry_provider_chk CHECK (char_length(provider) <= 100),
    source                            text CONSTRAINT signal_registry_source_chk CHECK (char_length(source) <= 100),
    internal_external                 text CONSTRAINT signal_registry_internal_external_chk CHECK (internal_external IN ('internal', 'external')),
    market_code                       text CONSTRAINT signal_registry_market_code_chk CHECK (char_length(market_code) <= 40),
    refresh_frequency                 text CONSTRAINT signal_registry_refresh_frequency_chk CHECK (refresh_frequency IN ('realTime', 'minutes10', 'hourly', 'daily', 'weekly', 'manual')),
    trust_level                       text NOT NULL DEFAULT 'experimental' CONSTRAINT signal_registry_trust_level_chk CHECK (trust_level IN ('approved', 'experimental', 'advisoryOnly', 'blocked')),
    ai_use_permissions                text[],
    fallback_policy                   text CONSTRAINT signal_registry_fallback_policy_chk CHECK (fallback_policy IN ('useHistoricalValue', 'ignore', 'substitute', 'reduceConfidence', 'stopAiRecommendation')),
    status                            text CONSTRAINT signal_registry_status_chk CHECK (char_length(status) <= 40),
    owner_principal_id                uuid,
    version                           text CONSTRAINT signal_registry_version_chk CHECK (char_length(version) <= 40),
    purpose                           text,
    deployed_at                       timestamptz,
    training_window                   text CONSTRAINT signal_registry_training_window_chk CHECK (char_length(training_window) <= 60),
    validation_result                 text,
    last_update_at                    timestamptz,
    quality_counts                    jsonb,
    performance                       jsonb,
    created_at                        timestamptz,
    updated_at                        timestamptz
);

-- Holds 14 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS catalogue.space (
    id                                uuid PRIMARY KEY,
    code                              text NOT NULL,
    name                              text NOT NULL,
    venue_id                          uuid,
    venue_map_zone_id                 uuid,
    resource_id                       uuid,
    parent_space_id                   uuid,
    maximum_capacity                  integer,
    safe_capacity                     integer,
    setup_minutes                     integer DEFAULT 0,
    teardown_minutes                  integer DEFAULT 0,
    access_rules                      jsonb,
    is_bookable                       boolean DEFAULT true,
    scope_path                        ltree NOT NULL
);

-- Holds 18 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS catalogue.tax_profile (
    id                                uuid PRIMARY KEY NOT NULL,
    scope_path                        ltree NOT NULL,
    tax_code_id                       uuid NOT NULL,
    code                              text NOT NULL CONSTRAINT tax_profile_code_chk CHECK (char_length(code) <= 64),
    name                              text NOT NULL CONSTRAINT tax_profile_name_chk CHECK (char_length(name) <= 200),
    tax_type                          text NOT NULL CONSTRAINT tax_profile_tax_type_chk CHECK (tax_type IN ('vat', 'gst', 'salesTax', 'entertainmentTax', 'tourismTax', 'municipalityTax', 'serviceTax', 'customRegulatoryTax')),
    jurisdiction                      text CONSTRAINT tax_profile_jurisdiction_chk CHECK (char_length(jurisdiction) <= 100),
    jurisdiction_level                text DEFAULT 'country' CONSTRAINT tax_profile_jurisdiction_level_chk CHECK (jurisdiction_level IN ('country', 'region', 'municipality')),
    legal_entity_id                   uuid,
    tax_registration_number           text CONSTRAINT tax_profile_tax_registration_number_chk CHECK (char_length(tax_registration_number) <= 60),
    applicability                     jsonb,
    tax_base                          text DEFAULT 'discountedPrice' CONSTRAINT tax_profile_tax_base_chk CHECK (tax_base IN ('discountedPrice', 'preDiscountPrice')),
    effective_from                    date NOT NULL,
    effective_to                      date,
    status                            text NOT NULL DEFAULT 'draft',
    owner_principal_id                uuid,
    created_at                        timestamptz,
    updated_at                        timestamptz
);

-- Holds 21 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS catalogue.tax_rule (
    id                                uuid PRIMARY KEY NOT NULL,
    scope_path                        ltree NOT NULL,
    name                              text NOT NULL CONSTRAINT tax_rule_name_chk CHECK (char_length(name) <= 200),
    product_id                        uuid,
    product_category_id               uuid,
    venue_id                          uuid,
    country_code                      text CONSTRAINT tax_rule_country_code_chk CHECK (char_length(country_code) <= 2),
    legal_entity_id                   uuid,
    transaction_type                  text CONSTRAINT tax_rule_transaction_type_chk CHECK (char_length(transaction_type) <= 60),
    customer_type                     text CONSTRAINT tax_rule_customer_type_chk CHECK (char_length(customer_type) <= 60),
    sales_channel                     text,
    treatment                         text NOT NULL CONSTRAINT tax_rule_treatment_chk CHECK (treatment IN ('taxInclusive', 'taxExclusive', 'taxExempt', 'zeroRated', 'outOfScope')),
    calculation_method                text NOT NULL CONSTRAINT tax_rule_calculation_method_chk CHECK (calculation_method IN ('percentage', 'fixedTax', 'tiered', 'compound', 'sequential', 'multipleConcurrent')),
    taxes                             jsonb,
    tiers                             jsonb,
    exemption_rule_ids                text[],
    effective_from                    timestamptz,
    effective_to                      timestamptz,
    status                            text NOT NULL DEFAULT 'draft',
    created_at                        timestamptz,
    updated_at                        timestamptz
);

-- One sellable configuration of a product — a size, a colour, a tier. Varies along the dimensions
-- in catalogue.variant_dimension
CREATE TABLE IF NOT EXISTS catalogue.variant (
    id                                uuid PRIMARY KEY NOT NULL,
    product_id                        uuid NOT NULL,
    sku                               text NOT NULL,
    axis_values                       jsonb NOT NULL,
    name                              text CONSTRAINT variant_name_chk CHECK (char_length(name) <= 150),
    barcode                           text CONSTRAINT variant_barcode_chk CHECK (char_length(barcode) <= 64),
    is_default                        boolean DEFAULT false,
    is_active                         boolean NOT NULL,
    description                       jsonb
);

-- The axis a product varies along — size, colour, session length. A t-shirt has one; a timed
-- ticket has none. Renamed from variant_dimension
CREATE TABLE IF NOT EXISTS catalogue.variant_dimension (
    code                              text NOT NULL CONSTRAINT variant_dimension_code_chk CHECK (char_length(code) <= 64),
    name                              text NOT NULL CONSTRAINT variant_dimension_name_chk CHECK (char_length(name) <= 200),
    id                                uuid PRIMARY KEY NOT NULL,
    product_id                        uuid NOT NULL
);

CREATE TABLE IF NOT EXISTS catalogue.waiting_room_setting (
    id                                uuid PRIMARY KEY,
    performance_id                    uuid NOT NULL,
    venue_id                          uuid NOT NULL,
    mode                              text NOT NULL DEFAULT 'off' CONSTRAINT waiting_room_setting_mode_chk CHECK (mode IN ('off', 'onSaleWindow', 'on')),
    active_until                      timestamptz,
    max_release_per_second            integer DEFAULT 50,
    is_automatic_release_enabled      boolean DEFAULT true,
    admission_ttl_seconds             integer DEFAULT 900,
    provider                          text DEFAULT 'inHouse' CONSTRAINT waiting_room_setting_provider_chk CHECK (provider IN ('inHouse', 'vendor')),
    scope_path                        ltree NOT NULL,
    updated_at                        timestamptz,
    updated_by_principal_id           uuid
);

-- Who asked to be told when a sold-out session frees up. Not a queue — a queue is people standing
-- at a ride Hangs off: reaches catalogue.product through its keys; references
-- catalogue.performance, catalogue.variant, pii.subject. Reached by: 5 operations read it and 3
-- write it.
CREATE TABLE IF NOT EXISTS catalogue.waitlist_entry (
    id                                uuid PRIMARY KEY,
    performance_id                    uuid NOT NULL,
    variant_id                        uuid,
    subject_id                        uuid,
    contact_point                     text,
    party_size                        integer NOT NULL,
    status                            text,
    position                          integer,
    offered_at                        timestamptz,
    offer_expires_at                  timestamptz,
    joined_at                         timestamptz
);

