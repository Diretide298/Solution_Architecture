-- promotions — 31 tables
-- **Derived. Do not hand-edit.**

-- One component’s share, fixed or proportional
CREATE TABLE IF NOT EXISTS promotions.allocation_component (
    allocation_split_id               uuid NOT NULL,
    id                                uuid PRIMARY KEY NOT NULL,
    variant_id                        uuid NOT NULL,
    percentage                        numeric(18,4),
    fixed_amount                      numeric(18,4),
    list_price                        numeric(18,4),
    revenue_account_id                uuid,
    legal_entity_id                   uuid,
    venue_id                          uuid
);

-- How a bundle price divides across its components. What the ledger posts against
CREATE TABLE IF NOT EXISTS promotions.allocation_split (
    id                                uuid PRIMARY KEY NOT NULL,
    bundle_id                         uuid NOT NULL,
    method                            text NOT NULL CONSTRAINT allocation_split_method_chk CHECK (method IN ('percentage', 'fixedAmount', 'proRataListPrice')),
    crosses_legal_entities            boolean
);

-- Several products sold as one, with the components priced by allocation
CREATE TABLE IF NOT EXISTS promotions.bundle (
    code                              text NOT NULL CONSTRAINT bundle_code_chk CHECK (char_length(code) <= 64),
    name                              text NOT NULL CONSTRAINT bundle_name_chk CHECK (char_length(name) <= 200),
    description                       text CONSTRAINT bundle_description_chk CHECK (char_length(description) <= 1000),
    venue_id                          uuid NOT NULL,
    kind                              text NOT NULL CONSTRAINT bundle_kind_chk CHECK (kind IN ('fixed', 'dynamic', 'mandatory', 'optional', 'promotional')),
    list_price                        numeric(18,4) NOT NULL,
    allocation                        jsonb NOT NULL,
    valid_from                        timestamptz,
    valid_to                          timestamptz,
    campaign_id                       uuid,
    owner_principal_id                uuid,
    category                          text CONSTRAINT bundle_category_chk CHECK (char_length(category) <= 100),
    is_standalone_product             boolean DEFAULT true,
    is_recommended_at_checkout        boolean DEFAULT false,
    required_variant_ids              text[],
    id                                uuid PRIMARY KEY NOT NULL,
    savings_amount                    numeric(18,4) NOT NULL,
    savings_percentage                numeric(18,4),
    has_been_sold                     boolean NOT NULL,
    is_active                         boolean NOT NULL
);

-- Holds 12 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS promotions.bundle_capacity_policy (
    id                                uuid PRIMARY KEY NOT NULL,
    bundle_id                         uuid NOT NULL,
    channel                           text,
    venue_id                          uuid,
    partner_id                        uuid,
    capacity_source                   text NOT NULL CONSTRAINT bundle_capacity_policy_capacity_source_chk CHECK (capacity_source IN ('sharedPool', 'dedicatedBundleAllocation', 'channelAllocation', 'partnerAllocation', 'eventCapacity', 'timeslotCapacity', 'seatInventory', 'resourceCapacity')),
    allocation_mode                   text DEFAULT 'hard' CONSTRAINT bundle_capacity_policy_allocation_mode_chk CHECK (allocation_mode IN ('hard', 'soft')),
    capacity_ceiling                  integer,
    hold_duration_minutes             integer,
    booking_cutoff_minutes            integer,
    allow_overbooking                 boolean DEFAULT false,
    allow_waitlist                    boolean DEFAULT false
);

-- Pick n from a set. The bundle price does not move with the choice (ADR-0019) — the allocation
-- does Hangs off: a child of promotions.bundle; reaches promotions.promotion through its keys;
-- references promotions.bundle. Reached by: 8 operations read it and 1 write it; 1 tables
-- reference it.
CREATE TABLE IF NOT EXISTS promotions.bundle_choice_group (
    id                                uuid PRIMARY KEY NOT NULL,
    label                             text NOT NULL,
    choose                            integer NOT NULL,
    allow_duplicates                  boolean DEFAULT false,
    unavailable_behaviour             text DEFAULT 'hideOption' CONSTRAINT bundle_choice_group_unavailable_behaviour_chk CHECK (unavailable_behaviour IN ('hideOption', 'hideBundle')),
    bundle_id                         uuid NOT NULL
);

-- Holds 5 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS promotions.bundle_choice_option (
    bundle_choice_group_id            uuid NOT NULL,
    id                                uuid PRIMARY KEY NOT NULL,
    variant_id                        uuid NOT NULL,
    quantity                          integer,
    is_default                        boolean
);

-- One product inside a bundle, with its quantity
CREATE TABLE IF NOT EXISTS promotions.bundle_component (
    bundle_id                         uuid NOT NULL,
    id                                uuid PRIMARY KEY NOT NULL,
    variant_id                        uuid NOT NULL,
    component_kind                    text DEFAULT 'admission' CONSTRAINT bundle_component_component_kind_chk CHECK (component_kind IN ('admission', 'fnbMenuItem', 'retail', 'addOn', 'other')),
    menu_item_id                      uuid,
    redeem_at_outlet_ids              text[],
    quantity                          integer NOT NULL,
    is_optional                       boolean DEFAULT false,
    substitute_variant_ids            text[],
    substitution_triggers             text[],
    substitution_price_effect         text DEFAULT 'samePrice' CONSTRAINT bundle_component_substitution_price_effect_chk CHECK (substitution_price_effect IN ('samePrice', 'surcharge', 'reducedPrice')),
    substitution_approval             text DEFAULT 'customer' CONSTRAINT bundle_component_substitution_approval_chk CHECK (substitution_approval IN ('none', 'customer', 'operator')),
    venue_id                          uuid
);

-- Holds 9 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS promotions.campaign (
    id                                uuid PRIMARY KEY NOT NULL,
    venue_id                          uuid NOT NULL,
    code                              text CONSTRAINT campaign_code_chk CHECK (char_length(code) <= 64),
    name                              text NOT NULL CONSTRAINT campaign_name_chk CHECK (char_length(name) <= 200),
    description                       text CONSTRAINT campaign_description_chk CHECK (char_length(description) <= 1000),
    owner_principal_id                uuid,
    legal_entity_id                   uuid,
    valid_from                        timestamptz,
    valid_to                          timestamptz
);

-- Holds 13 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS promotions.campaign_budget (
    campaign_id                       uuid NOT NULL,
    id                                uuid PRIMARY KEY NOT NULL,
    budget_type                       text NOT NULL CONSTRAINT campaign_budget_budget_type_chk CHECK (budget_type IN ('total', 'discount', 'reward', 'freeProduct')),
    funding_source                    text CONSTRAINT campaign_budget_funding_source_chk CHECK (funding_source IN ('venue', 'department', 'marketing', 'partner')),
    amount                            numeric(18,4) NOT NULL,
    scope                             text DEFAULT 'entireCampaign' CONSTRAINT campaign_budget_scope_chk CHECK (scope IN ('entireCampaign', 'promotion', 'product', 'channel', 'partner', 'customerSegment')),
    scope_ref                         text,
    owner_principal_id                uuid,
    cost_centre                       text CONSTRAINT campaign_budget_cost_centre_chk CHECK (char_length(cost_centre) <= 64),
    department                        text CONSTRAINT campaign_budget_department_chk CHECK (char_length(department) <= 100),
    valid_from                        timestamptz,
    valid_to                          timestamptz,
    threshold_policy                  jsonb
);

CREATE TABLE IF NOT EXISTS promotions.code_assignment (
    id                                uuid PRIMARY KEY NOT NULL,
    batch_id                          uuid NOT NULL,
    channels_type                     text NOT NULL,
    assignee_type                     text NOT NULL,
    assignee_reference                text,
    quantity                          integer NOT NULL,
    assigned_at                       timestamptz,
    assigned_by_principal_id          uuid,
    scope_path                        ltree NOT NULL
);

-- A batch of codes with shared rules. The codes are children
CREATE TABLE IF NOT EXISTS promotions.coupon_campaign (
    code                              text NOT NULL CONSTRAINT coupon_campaign_code_chk CHECK (char_length(code) <= 64),
    name                              text NOT NULL CONSTRAINT coupon_campaign_name_chk CHECK (char_length(name) <= 200),
    venue_id                          uuid NOT NULL,
    discount                          jsonb NOT NULL,
    conditions                        jsonb,
    is_single_use                     boolean DEFAULT true,
    max_redemptions_per_code          integer DEFAULT 1,
    valid_from                        timestamptz NOT NULL,
    valid_to                          timestamptz,
    campaign_id                       uuid,
    id                                uuid PRIMARY KEY NOT NULL,
    generated_count                   integer NOT NULL,
    redeemed_count                    integer NOT NULL,
    is_active                         boolean
);

-- One issued code, with its own redemption state
CREATE TABLE IF NOT EXISTS promotions.coupon_code (
    code                              text NOT NULL,
    campaign_id                       uuid NOT NULL,
    batch_id                          uuid,
    status                            text NOT NULL CONSTRAINT coupon_code_status_chk CHECK (status IN ('issued', 'assigned', 'redeemed', 'expired', 'voided')),
    assigned_subject_id               uuid,
    redemption_count                  integer,
    max_redemptions                   integer,
    discount                          jsonb,
    invalid_reason                    text CONSTRAINT coupon_code_invalid_reason_chk CHECK (invalid_reason IN ('expired', 'alreadyRedeemed', 'voided', 'notYetValid', 'wrongVenue', 'conditionsNotMet', 'notAssignedToGuest')),
    valid_from                        timestamptz,
    valid_to                          timestamptz,
    redeemed_at                       timestamptz,
    redeemed_order_id                 uuid,
    scope_path                        ltree NOT NULL,
    assignment_id                     uuid,
    distribution_status               text CONSTRAINT coupon_code_distribution_status_chk CHECK (distribution_status IN ('pending', 'sent', 'delivered', 'viewed', 'cancelled')),
    id                                uuid PRIMARY KEY NOT NULL
);

-- Holds 11 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS promotions.coupon_code_batch (
    id                                uuid PRIMARY KEY NOT NULL,
    campaign_id                       uuid NOT NULL,
    quantity                          integer NOT NULL,
    generated_count                   integer,
    prefix                            text CONSTRAINT coupon_code_batch_prefix_chk CHECK (char_length(prefix) <= 16),
    length                            integer,
    status                            text NOT NULL CONSTRAINT coupon_code_batch_status_chk CHECK (status IN ('queued', 'generating', 'complete', 'failed')),
    failure_reason                    text,
    requested_by_principal_id         uuid,
    requested_at                      timestamptz,
    completed_at                      timestamptz
);

-- Holds 15 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS promotions.partner_bundle_product (
    id                                uuid PRIMARY KEY NOT NULL,
    bundle_component_id               uuid NOT NULL,
    partner_id                        uuid NOT NULL,
    external_product_id               text NOT NULL CONSTRAINT partner_bundle_product_external_product_id_chk CHECK (char_length(external_product_id) <= 128),
    product_name                      text CONSTRAINT partner_bundle_product_product_name_chk CHECK (char_length(product_name) <= 200),
    api_source                        text CONSTRAINT partner_bundle_product_api_source_chk CHECK (char_length(api_source) <= 100),
    availability_source               text DEFAULT 'partnerApi' CONSTRAINT partner_bundle_product_availability_source_chk CHECK (availability_source IN ('partnerApi', 'allocation', 'onRequest')),
    external_price                    numeric(18,4),
    selling_price                     numeric(18,4),
    commission                        numeric(18,4),
    settlement_rule                   text CONSTRAINT partner_bundle_product_settlement_rule_chk CHECK (char_length(settlement_rule) <= 500),
    cancellation_rule                 text CONSTRAINT partner_bundle_product_cancellation_rule_chk CHECK (char_length(cancellation_rule) <= 500),
    redemption_method                 text CONSTRAINT partner_bundle_product_redemption_method_chk CHECK (char_length(redemption_method) <= 100),
    connection_status                 text CONSTRAINT partner_bundle_product_connection_status_chk CHECK (connection_status IN ('connected', 'available', 'degraded', 'apiError', 'productUnavailable', 'mappingError')),
    last_checked_at                   timestamptz
);

-- Holds 10 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS promotions.product_relationship (
    id                                uuid PRIMARY KEY NOT NULL,
    from_product_id                   uuid NOT NULL,
    to_product_id                     uuid NOT NULL,
    kind                              text NOT NULL CONSTRAINT product_relationship_kind_chk CHECK (kind IN ('upgradesTo', 'downgradesTo', 'crossSell', 'accessory', 'substitute', 'requires', 'incompatibleWith')),
    ladder_position                   integer,
    source                            text DEFAULT 'declared' CONSTRAINT product_relationship_source_chk CHECK (source IN ('declared', 'measured', 'aiProposed')),
    strength                          numeric(18,4),
    effective_from                    date,
    effective_to                      date,
    scope_path                        ltree NOT NULL
);

-- A rule that changes a price, with eligibility and a budget. Evaluated at the basket rather than
-- stored on a product
CREATE TABLE IF NOT EXISTS promotions.promotion (
    code                              text NOT NULL CONSTRAINT promotion_code_chk CHECK (char_length(code) <= 64),
    name                              text NOT NULL CONSTRAINT promotion_name_chk CHECK (char_length(name) <= 200),
    description                       text CONSTRAINT promotion_description_chk CHECK (char_length(description) <= 1000),
    venue_id                          uuid NOT NULL,
    discount                          jsonb NOT NULL,
    conditions                        jsonb,
    stacking_mode                     text DEFAULT 'bestOnly',
    stacking_group                    text CONSTRAINT promotion_stacking_group_chk CHECK (char_length(stacking_group) <= 64),
    precedence                        integer DEFAULT 0,
    valid_from                        timestamptz NOT NULL,
    valid_to                          timestamptz,
    max_redemptions                   integer,
    max_redemptions_per_guest         integer,
    budget_cap                        numeric(18,4),
    campaign_id                       uuid,
    is_recommendable                  boolean DEFAULT false,
    recommendable_segment_ids         text[],
    id                                uuid PRIMARY KEY NOT NULL,
    status                            text NOT NULL CONSTRAINT promotion_status_chk CHECK (status IN ('draft', 'scheduled', 'live', 'paused', 'expired', 'ended')),
    is_paused                         boolean,
    redemption_count                  integer,
    discount_given                    numeric(18,4),
    published_at                      timestamptz,
    version                           integer
);

-- Holds 13 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS promotions.promotion_alert (
    id                                uuid PRIMARY KEY NOT NULL,
    venue_id                          uuid NOT NULL,
    promotion_id                      uuid,
    coupon_campaign_id                uuid,
    coupon_code_batch_id              uuid,
    coupon_code                       text,
    alert_type                        text NOT NULL CONSTRAINT promotion_alert_alert_type_chk CHECK (alert_type IN ('missingProduct', 'missingEligibility', 'invalidDates', 'invalidDiscount', 'invalidCode', 'missingApproval', 'budgetNearLimit', 'budgetExceeded', 'marginBelowThreshold', 'excessiveDiscountExposure', 'promotionFailedToPublish', 'productUnavailable', 'bundleComponentUnavailable', 'channelSynchronizationFailure', 'lowConversion', 'lowRedemption', 'unexpectedHighRedemption', 'campaignUnderperforming', 'abnormalCouponUsage', 'excessiveRepeatRedemption', 'suspiciousCustomerBehavior', 'promoCodeLeakage', 'excessiveRedemptionVelocity', 'repeatedFailedAttempts', 'multipleCustomersUsingCustomerSpecificCode', 'unusualGeographicUsage', 'highVolumeRedemptionFromOneDevice', 'suspiciousPosOperatorActivity', 'codeEnumerationAttempts', 'partnerCodeLeakage', 'redemptionAboveExpectedCampaignPattern')),
    category                          text NOT NULL CONSTRAINT promotion_alert_category_chk CHECK (category IN ('configuration', 'financial', 'operational', 'commercial', 'fraudRisk')),
    severity                          text NOT NULL CONSTRAINT promotion_alert_severity_chk CHECK (severity IN ('information', 'warning', 'critical')),
    risk_level                        text CONSTRAINT promotion_alert_risk_level_chk CHECK (risk_level IN ('low', 'medium', 'high', 'critical')),
    details                           text,
    raised_at                         timestamptz NOT NULL,
    resolved_at                       timestamptz
);

-- Holds 14 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS promotions.promotion_audit (
    id                                uuid PRIMARY KEY NOT NULL,
    venue_id                          uuid NOT NULL,
    entity_type                       text NOT NULL CONSTRAINT promotion_audit_entity_type_chk CHECK (entity_type IN ('promotion', 'promotionRule', 'stackingRule', 'campaign', 'campaignBudget', 'couponCampaign', 'couponCode', 'bundle')),
    entity_id                         text NOT NULL,
    promotion_id                      uuid,
    promotion_version                 integer,
    event_type                        text NOT NULL CONSTRAINT promotion_audit_event_type_chk CHECK (event_type IN ('promotionCreated', 'promotionEdited', 'ruleChanged', 'discountChanged', 'productAdded', 'productRemoved', 'eligibilityChanged', 'channelChanged', 'datesChanged', 'budgetChanged', 'approvalSubmitted', 'approvalGranted', 'approvalRejected', 'promotionActivated', 'promotionPaused', 'promotionSuspended', 'promotionExpired', 'promotionArchived', 'promotionEnded', 'promotionUnscheduled', 'created', 'modified', 'assigned', 'suspended', 'reactivated', 'cancelled')),
    previous_value                    jsonb,
    new_value                         jsonb,
    reason                            text,
    approval_reference                text,
    actor_principal_id                uuid,
    actor_role                        text,
    occurred_at                       timestamptz NOT NULL
);

-- Holds 9 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS promotions.promotion_channel_publication (
    id                                uuid PRIMARY KEY NOT NULL,
    venue_id                          uuid NOT NULL,
    promotion_id                      uuid,
    coupon_campaign_id                uuid,
    channel                           text NOT NULL CONSTRAINT promotion_channel_publication_channel_chk CHECK (channel IN ('pos', 'kiosk', 'guestApp', 'guestWeb', 'callCentre', 'partner', 'api', 'backOffice', 'b2b', 'ota')),
    status                            text NOT NULL CONSTRAINT promotion_channel_publication_status_chk CHECK (status IN ('notAssigned', 'pendingPublication', 'synchronizing', 'published', 'publicationFailed', 'outOfSync', 'suspended')),
    published_version                 integer,
    last_synchronized_at              timestamptz,
    last_error                        text
);

-- Holds 8 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS promotions.promotion_conflict (
    id                                uuid PRIMARY KEY NOT NULL,
    venue_id                          uuid NOT NULL,
    conflict_type                     text NOT NULL CONSTRAINT promotion_conflict_conflict_type_chk CHECK (conflict_type IN ('sameProduct', 'sameAudience', 'sameChannel', 'sameValidity', 'incompatiblePromotions', 'missingHierarchy', 'missingStackingRule', 'discountCapBreach', 'circularDependency')),
    severity                          text CONSTRAINT promotion_conflict_severity_chk CHECK (severity IN ('information', 'warning', 'high', 'critical')),
    promotion_ids                     text[] NOT NULL,
    resolution_method                 text CONSTRAINT promotion_conflict_resolution_method_chk CHECK (resolution_method IN ('automatic', 'ruleBased', 'bestPrice', 'priority', 'manualIntervention')),
    detected_at                       timestamptz NOT NULL,
    resolved_at                       timestamptz
);

-- Holds 9 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS promotions.promotion_evaluation_trace (
    id                                uuid PRIMARY KEY NOT NULL,
    venue_id                          uuid NOT NULL,
    order_id                          uuid NOT NULL,
    evaluated_at                      timestamptz NOT NULL,
    evaluated_promotion_ids           text[],
    eligible_promotion_ids            text[],
    applied_promotion_ids             text[],
    total_saving                      numeric(18,4),
    decision                          jsonb
);

-- Holds 13 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS promotions.promotion_rule (
    id                                uuid PRIMARY KEY NOT NULL,
    venue_id                          uuid NOT NULL,
    promotion_id                      uuid,
    campaign_id                       uuid,
    rule_type                         text NOT NULL CONSTRAINT promotion_rule_rule_type_chk CHECK (rule_type IN ('benefit', 'eligibility')),
    name                              text NOT NULL CONSTRAINT promotion_rule_name_chk CHECK (char_length(name) <= 200),
    description                       text CONSTRAINT promotion_rule_description_chk CHECK (char_length(description) <= 1000),
    owner_principal_id                uuid,
    priority                          integer DEFAULT 0,
    conditions                        jsonb NOT NULL,
    effect                            text CONSTRAINT promotion_rule_effect_chk CHECK (effect IN ('include', 'exclude')),
    outcomes                          jsonb,
    is_active                         boolean DEFAULT false
);

-- Holds 5 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS promotions.promotion_variant (
    id                                uuid PRIMARY KEY NOT NULL,
    promotion_id                      uuid,
    label                             text NOT NULL,
    traffic_percent                   integer NOT NULL,
    discount_percent                  numeric(18,4)
);

-- Holds 12 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS promotions.recommendation_experiment (
    id                                uuid PRIMARY KEY NOT NULL,
    code                              text NOT NULL,
    name                              text,
    placement                         text,
    holdout_percent                   integer DEFAULT 5,
    primary_metric                    text,
    minimum_sample_size               integer,
    started_at                        timestamptz,
    ended_at                          timestamptz,
    status                            text CONSTRAINT recommendation_experiment_status_chk CHECK (status IN ('draft', 'running', 'concluded', 'abandoned')),
    winning_variant                   text,
    scope_path                        ltree NOT NULL
);

-- Holds 8 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS promotions.recommendation_outcome (
    recommendation_id                 uuid NOT NULL,
    outcome                           text NOT NULL CONSTRAINT recommendation_outcome_outcome_chk CHECK (outcome IN ('shown', 'clicked', 'accepted', 'dismissed', 'expired')),
    at                                timestamptz,
    order_id                          uuid,
    attributed_gross_amount           numeric(18,4),
    is_holdout                        boolean DEFAULT false,
    scope_path                        ltree NOT NULL,
    id                                uuid PRIMARY KEY NOT NULL
);

-- Holds 17 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS promotions.recommendation_strategy (
    id                                uuid PRIMARY KEY NOT NULL,
    code                              text NOT NULL,
    name                              text NOT NULL,
    objective                         text NOT NULL CONSTRAINT recommendation_strategy_objective_chk CHECK (objective IN ('attachRevenue', 'averageOrderValue', 'upgradeRate', 'visitFrequency', 'inventoryBalance', 'guestSatisfaction')),
    kinds                             text[],
    item_kinds                        text[],
    placements                        text[],
    channels                          text[],
    max_recommendations               integer DEFAULT 3,
    min_confidence                    numeric(18,4),
    ranking_weights                   jsonb,
    require_availability              boolean DEFAULT true,
    exclude_in_basket                 boolean DEFAULT true,
    guardrails                        jsonb,
    status                            text CONSTRAINT recommendation_strategy_status_chk CHECK (status IN ('draft', 'active', 'paused', 'retired')),
    effective_from                    date,
    effective_to                      date,
    scope_path                        ltree NOT NULL
);

-- Holds 6 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS promotions.recommendation_suppression (
    scope_path                        ltree NOT NULL,
    max_impressions_per_product_per_day integer,
    max_impressions_per_guest_per_session integer,
    cooldown_after_dismiss_days       integer,
    cooldown_after_accept_days        integer,
    id                                uuid PRIMARY KEY NOT NULL
);

-- Holds 8 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS promotions.stacking_rule (
    scope                             text CONSTRAINT stacking_rule_scope_chk CHECK (scope IN ('entireTransaction', 'product', 'productCategory', 'individualTicket', 'bundleComponent', 'customer', 'channel')),
    stacking_model                    text CONSTRAINT stacking_rule_stacking_model_chk CHECK (stacking_model IN ('fullyStackable', 'nonStackable', 'conditional', 'categoryStacking', 'maximumN')),
    maximum_promotions                integer,
    promotion_type_a                  text,
    promotion_type_b                  text,
    can_stack                         boolean,
    id                                uuid PRIMARY KEY NOT NULL,
    venue_id                          uuid NOT NULL
);

-- What to offer alongside what, and where it may appear
CREATE TABLE IF NOT EXISTS promotions.upsell_rule (
    id                                uuid PRIMARY KEY NOT NULL,
    region_id                         uuid,
    name                              text NOT NULL CONSTRAINT upsell_rule_name_chk CHECK (char_length(name) <= 200),
    placement                         text NOT NULL CONSTRAINT upsell_rule_placement_chk CHECK (placement IN ('productDetail', 'cart', 'checkout', 'postPurchase', 'atGate', 'inVenue')),
    trigger_variant_ids               text[] NOT NULL,
    trigger_category_ids              text[],
    suggested_variant_ids             text[] NOT NULL,
    suggested_bundle_id               uuid,
    channels                          text[],
    priority                          integer DEFAULT 0,
    max_suggestions                   integer DEFAULT 3,
    is_active                         boolean
);

-- A named value a guest can spend, with its own balance and expiry
CREATE TABLE IF NOT EXISTS promotions.voucher (
    code                              text NOT NULL,
    batch_id                          uuid NOT NULL,
    face_value                        numeric(18,4) NOT NULL,
    balance                           numeric(18,4) NOT NULL,
    status                            text NOT NULL CONSTRAINT voucher_status_chk CHECK (status IN ('issued', 'partiallyRedeemed', 'redeemed', 'expired', 'voided')),
    valid_to                          timestamptz,
    id                                uuid PRIMARY KEY NOT NULL
);

-- Vouchers issued together, sharing rules and an expiry
CREATE TABLE IF NOT EXISTS promotions.voucher_batch (
    name                              text NOT NULL CONSTRAINT voucher_batch_name_chk CHECK (char_length(name) <= 200),
    venue_id                          uuid NOT NULL,
    face_value                        numeric(18,4) NOT NULL,
    quantity                          integer NOT NULL,
    allow_partial_redemption          boolean DEFAULT true,
    valid_from                        timestamptz,
    valid_to                          timestamptz NOT NULL,
    restrict_to_variant_ids           text[],
    id                                uuid PRIMARY KEY NOT NULL,
    issued_count                      integer NOT NULL,
    redeemed_value                    numeric(18,4) NOT NULL,
    outstanding_liability             numeric(18,4) NOT NULL
);

