-- marketing — 127 tables
-- **Derived. Do not hand-edit.**

-- Available, busy, away or offline, with a concurrency limit. Expires — an agent who forgets to go
-- offline is one conversations queue for Hangs off: reaches marketing.guest_profile through its
-- keys; references identity.principal. Reached by: 6 operations read it and 1 write it.
CREATE TABLE IF NOT EXISTS marketing.agent_availability (
    id                                uuid PRIMARY KEY,
    principal_id                      uuid NOT NULL,
    state                             text NOT NULL CONSTRAINT agent_availability_state_chk CHECK (state IN ('available', 'busy', 'away', 'offline')),
    max_concurrent                    integer,
    queue_ids                         text[],
    expires_at                        timestamptz,
    updated_at                        timestamptz
);

-- Holds 10 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS marketing.agent_service_profile (
    id                                uuid PRIMARY KEY,
    principal_id                      uuid NOT NULL,
    team                              text CONSTRAINT agent_service_profile_team_chk CHECK (char_length(team) <= 100),
    skills                            text[] NOT NULL,
    languages                         text[] NOT NULL,
    queue_ids                         text[],
    max_concurrent_cases              integer,
    availability_override             jsonb,
    scope_path                        ltree NOT NULL,
    updated_at                        timestamptz
);

-- Every marketing touch, not just the converting one (BL-177). A platform storing only its chosen
-- attribution model cannot answer a question asked in a different one. Hangs off: reaches
-- marketing.guest_profile through its keys; references marketing.campaign, marketing.journey,
-- orders.sales_order. Reached by: 2 operations read it and 0 write it.
CREATE TABLE IF NOT EXISTS marketing.attribution_touch (
    id                                uuid PRIMARY KEY NOT NULL,
    subject_id                        uuid NOT NULL,
    campaign_id                       uuid NOT NULL,
    journey_id                        uuid,
    touched_at                        timestamptz NOT NULL,
    channel                           text NOT NULL CONSTRAINT attribution_touch_channel_chk CHECK (channel IN ('email', 'sms', 'whatsapp', 'push', 'web', 'app', 'paidSearch', 'paidSocial', 'organic', 'referral', 'direct')),
    interaction                       text CONSTRAINT attribution_touch_interaction_chk CHECK (interaction IN ('delivered', 'opened', 'clicked', 'viewed', 'converted')),
    order_id                          text
);

-- Holds 16 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS marketing.audience_activation (
    id                                uuid PRIMARY KEY,
    segment_id                        uuid NOT NULL,
    destination                       text NOT NULL CONSTRAINT audience_activation_destination_chk CHECK (destination IN ('campaign', 'journey', 'website', 'mobileApp', 'externalAdPlatform', 'partnerFeed')),
    destination_reference             text,
    is_external                       boolean DEFAULT false,
    suppression_list_ids              text[],
    enforce_consent                   boolean DEFAULT true,
    frequency_cap_per_week            integer,
    refresh_schedule                  text,
    expires_at                        date,
    pre_flight                        jsonb,
    approval_request_id               uuid,
    status                            text CONSTRAINT audience_activation_status_chk CHECK (status IN ('draft', 'pendingApproval', 'active', 'failed', 'expired')),
    last_synced_at                    timestamptz,
    last_sync_errors                  integer DEFAULT 0,
    scope_path                        ltree NOT NULL
);

-- Holds 17 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS marketing.audience_list (
    id                                uuid PRIMARY KEY,
    name                              text NOT NULL,
    kind                              text CONSTRAINT audience_list_kind_chk CHECK (kind IN ('manual', 'imported', 'suppression')),
    asset_id                          uuid,
    field_mapping                     jsonb,
    rows_read                         integer,
    matched                           integer,
    unmatched                         integer,
    duplicates_removed                integer,
    rejected                          integer,
    unmatched_handling                text DEFAULT 'quarantine' CONSTRAINT audience_list_unmatched_handling_chk CHECK (unmatched_handling IN ('createLead', 'quarantine')),
    source                            text,
    owner                             uuid,
    purpose                           text,
    consent_basis                     text,
    expires_at                        date,
    scope_path                        ltree NOT NULL
);

-- Holds 9 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS marketing.badge (
    id                                uuid PRIMARY KEY,
    code                              text NOT NULL CONSTRAINT badge_code_chk CHECK (char_length(code) <= 100),
    name                              text NOT NULL CONSTRAINT badge_name_chk CHECK (char_length(name) <= 150),
    description                       text CONSTRAINT badge_description_chk CHECK (char_length(description) <= 500),
    icon_url                          text CONSTRAINT badge_icon_url_chk CHECK (char_length(icon_url) <= 1000),
    type                              text NOT NULL CONSTRAINT badge_type_chk CHECK (char_length(type) <= 30),
    is_active                         boolean NOT NULL,
    created_at                        timestamptz NOT NULL,
    updated_at                        timestamptz
);

-- Holds 20 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS marketing.booking_consent_record (
    id                                text PRIMARY KEY NOT NULL,
    question_id                       text NOT NULL,
    question_version                  integer NOT NULL,
    question_kind                     text NOT NULL CONSTRAINT booking_consent_record_question_kind_chk CHECK (question_kind IN ('swim', 'scuba', 'risk', 'custom')),
    answer                            text NOT NULL CONSTRAINT booking_consent_record_answer_chk CHECK (answer IN ('yes', 'no')),
    scope                             text NOT NULL CONSTRAINT booking_consent_record_scope_chk CHECK (scope IN ('perPerson', 'perBooking')),
    blocks_booking                    boolean,
    cart_id                           uuid,
    cart_line_id                      uuid,
    order_id                          text,
    order_line_id                     text,
    person_index                      integer,
    person_name                       text CONSTRAINT booking_consent_record_person_name_chk CHECK (char_length(person_name) <= 120),
    person_subject_id                 uuid,
    answered_by_subject_id            uuid,
    answered_by_principal_id          uuid,
    source                            text NOT NULL CONSTRAINT booking_consent_record_source_chk CHECK (source IN ('guestApp', 'website', 'kiosk', 'pos', 'callCentre', 'import', 'agentRecorded')),
    answered_at                       timestamptz NOT NULL,
    superseded_at                     timestamptz,
    scope_path                        ltree NOT NULL
);

-- Holds 9 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS marketing.business_event (
    id                                uuid PRIMARY KEY NOT NULL,
    event_type                        text NOT NULL CONSTRAINT business_event_event_type_chk CHECK (char_length(event_type) <= 100),
    source_module                     text NOT NULL CONSTRAINT business_event_source_module_chk CHECK (source_module IN ('crm', 'ticketing', 'membership', 'waiver', 'groupSales', 'customerService', 'finance', 'wallet', 'resourceManagement', 'accessControl', 'other')),
    event_state                       text CONSTRAINT business_event_event_state_chk CHECK (char_length(event_state) <= 100),
    payload_fields                    text[],
    priority                          text NOT NULL DEFAULT 'P3' CONSTRAINT business_event_priority_chk CHECK (priority IN ('P1', 'P2', 'P3', 'P4')),
    status                            text NOT NULL DEFAULT 'active' CONSTRAINT business_event_status_chk CHECK (status IN ('active', 'inactive')),
    scope_path                        ltree NOT NULL,
    updated_at                        timestamptz
);

-- A send with an audience and a schedule. Every dispatch it produces is a message_dispatch row,
-- which is where consent was checked
CREATE TABLE IF NOT EXISTS marketing.campaign (
    name                              text NOT NULL CONSTRAINT campaign_name_chk CHECK (char_length(name) <= 200),
    kind                              text NOT NULL CONSTRAINT campaign_kind_chk CHECK (kind IN ('oneOff', 'scheduled', 'triggered', 'recurring')),
    channel                           text NOT NULL CONSTRAINT campaign_channel_chk CHECK (channel IN ('email', 'sms', 'whatsapp', 'push', 'inApp', 'post')),
    venue_id                          uuid,
    segment_id                        uuid NOT NULL,
    content                           jsonb NOT NULL,
    trigger                           jsonb,
    scheduled_for                     timestamptz,
    consent_purpose                   text DEFAULT 'marketing',
    send_window                       jsonb,
    id                                uuid PRIMARY KEY NOT NULL,
    budget_cap                        numeric(18,4),
    budget_spent                      numeric(18,4),
    status                            text NOT NULL CONSTRAINT campaign_status_chk CHECK (status IN ('draft', 'scheduled', 'sending', 'paused', 'completed', 'stopped', 'failed')),
    is_paused                         boolean,
    created_by_principal_id           uuid,
    created_at                        timestamptz NOT NULL,
    launched_at                       timestamptz,
    completed_at                      timestamptz
);

-- Holds 7 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS marketing.campaign_target (
    id                                uuid PRIMARY KEY,
    campaign_id                       uuid NOT NULL,
    domain                            text NOT NULL CONSTRAINT campaign_target_domain_chk CHECK (char_length(domain) <= 30),
    type                              text NOT NULL CONSTRAINT campaign_target_type_chk CHECK (char_length(type) <= 50),
    target_id                         uuid NOT NULL,
    is_primary                        boolean NOT NULL,
    created_at                        timestamptz NOT NULL
);

-- A guest problem with a lifecycle — raised, assigned, answered, closed. The messages are
-- children; the SLA is not yet modelled
CREATE TABLE IF NOT EXISTS marketing."case" (
    id                                text PRIMARY KEY NOT NULL,
    case_number                       text NOT NULL,
    subject_id                        uuid,
    title                             text NOT NULL,
    kind                              text,
    channel                           text,
    recorded_at                       timestamptz,
    synced_at                         timestamptz,
    category_id                       uuid,
    queue_id                          uuid,
    membership_id                     uuid,
    status                            text NOT NULL CONSTRAINT case_status_chk CHECK (status IN ('open', 'inProgress', 'awaitingGuest', 'escalated', 'resolved', 'closed')),
    priority                          text NOT NULL CONSTRAINT case_priority_chk CHECK (priority IN ('low', 'normal', 'high', 'urgent')),
    assigned_to_principal_id          uuid,
    venue_id                          uuid,
    related_order_id                  text,
    sla_due_at                        timestamptz,
    sla_paused_seconds                integer,
    escalation_count                  integer,
    created_at                        timestamptz NOT NULL,
    resolved_at                       timestamptz,
    description                       text,
    resolution_note                   text
);

-- Holds 9 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS marketing.case_category (
    id                                uuid PRIMARY KEY NOT NULL,
    code                              text NOT NULL CONSTRAINT case_category_code_chk CHECK (char_length(code) <= 60),
    name                              text NOT NULL CONSTRAINT case_category_name_chk CHECK (char_length(name) <= 150),
    parent_category_id                uuid,
    default_priority                  text,
    is_active                         boolean NOT NULL DEFAULT true,
    scope_path                        ltree NOT NULL,
    created_at                        timestamptz,
    updated_at                        timestamptz
);

-- Holds 17 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS marketing.case_compensation_request (
    id                                text PRIMARY KEY NOT NULL,
    scope_path                        ltree NOT NULL,
    case_id                           text NOT NULL,
    order_id                          text,
    line_ids                          text[],
    request_type                      text NOT NULL CONSTRAINT case_compensation_request_request_type_chk CHECK (request_type IN ('fullRefund', 'partialRefund', 'serviceCredit', 'walletCredit', 'voucher', 'complimentaryTicket', 'feeWaiver', 'upgrade', 'discount', 'policyException')),
    value                             numeric(18,4) NOT NULL,
    reason                            text NOT NULL CONSTRAINT case_compensation_request_reason_chk CHECK (char_length(reason) <= 1000),
    is_policy_exception               boolean DEFAULT false,
    exception_reason                  text CONSTRAINT case_compensation_request_exception_reason_chk CHECK (char_length(exception_reason) <= 1000),
    is_submit                         boolean DEFAULT false,
    status                            text CONSTRAINT case_compensation_request_status_chk CHECK (status IN ('draft', 'pendingApproval', 'approved', 'declined', 'fulfilled', 'failed', 'withdrawn')),
    approval_request_id               text,
    fulfilment_operation              text,
    fulfilment_reference              text,
    requested_by_principal_id         uuid,
    updated_at                        timestamptz
);

-- Holds 11 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS marketing.case_escalation (
    id                                uuid PRIMARY KEY NOT NULL,
    case_id                           text NOT NULL,
    reason                            text NOT NULL CONSTRAINT case_escalation_reason_chk CHECK (char_length(reason) <= 500),
    reason_category                   text CONSTRAINT case_escalation_reason_category_chk CHECK (reason_category IN ('slaRisk', 'customerComplaint', 'repeatedContact', 'highValue', 'refundException', 'operationalFailure', 'systemFailure', 'legalCompliance', 'vipCustomer', 'supervisorRequested', 'other')),
    is_automatic                      boolean DEFAULT false,
    escalated_by_principal_id         uuid,
    escalated_to_principal_id         uuid,
    previous_priority                 text CONSTRAINT case_escalation_previous_priority_chk CHECK (previous_priority IN ('low', 'normal', 'high', 'urgent')),
    new_priority                      text,
    escalated_at                      timestamptz NOT NULL,
    scope_path                        ltree NOT NULL
);

-- Holds 17 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS marketing.case_internal_request (
    id                                text PRIMARY KEY NOT NULL,
    scope_path                        ltree NOT NULL,
    case_id                           text NOT NULL,
    department                        text NOT NULL CONSTRAINT case_internal_request_department_chk CHECK (department IN ('ticketing', 'finance', 'operations', 'accessControl', 'membership', 'crm', 'fnb', 'retail', 'groupSales', 'technicalSupport', 'venueManagement', 'management')),
    assignee_principal_id             uuid,
    request                           text NOT NULL CONSTRAINT case_internal_request_request_chk CHECK (char_length(request) <= 2000),
    priority                          text NOT NULL CONSTRAINT case_internal_request_priority_chk CHECK (priority IN ('low', 'normal', 'high', 'urgent')),
    escalation_type                   text NOT NULL CONSTRAINT case_internal_request_escalation_type_chk CHECK (escalation_type IN ('functional', 'supervisor', 'management', 'technical', 'financial', 'emergencyEventDay')),
    due_at                            timestamptz,
    related_transaction               jsonb,
    attachment_refs                   text[],
    status                            text DEFAULT 'open' CONSTRAINT case_internal_request_status_chk CHECK (status IN ('open', 'inProgress', 'completed', 'cancelled')),
    response                          text CONSTRAINT case_internal_request_response_chk CHECK (char_length(response) <= 2000),
    requested_by_principal_id         uuid,
    created_at                        timestamptz,
    completed_at                      timestamptz,
    updated_at                        timestamptz
);

-- Holds 9 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS marketing.case_linked_record (
    id                                uuid PRIMARY KEY,
    scope_path                        ltree NOT NULL,
    case_id                           text NOT NULL,
    kind                              text NOT NULL CONSTRAINT case_linked_record_kind_chk CHECK (kind IN ('order', 'ticket', 'payment', 'refund', 'membership', 'walletTransaction', 'groupBooking', 'accessEvent')),
    reference_id                      text NOT NULL CONSTRAINT case_linked_record_reference_id_chk CHECK (char_length(reference_id) <= 64),
    note                              text CONSTRAINT case_linked_record_note_chk CHECK (char_length(note) <= 500),
    is_active                         boolean DEFAULT true,
    linked_by_principal_id            uuid,
    updated_at                        timestamptz
);

-- One exchange in a case, from either side
CREATE TABLE IF NOT EXISTS marketing.case_message (
    resolution                        text,
    id                                text PRIMARY KEY NOT NULL,
    body                              text NOT NULL,
    is_internal                       boolean NOT NULL,
    author_kind                       text NOT NULL CONSTRAINT case_message_author_kind_chk CHECK (author_kind IN ('agent', 'guest', 'system', 'ai')),
    author_principal_id               uuid,
    channel                           text CONSTRAINT case_message_channel_chk CHECK (channel IN ('email', 'sms', 'whatsapp', 'push', 'inApp', 'post')),
    attachment_refs                   text[],
    recorded_at                       timestamptz NOT NULL,
    synced_at                         timestamptz,
    case_id                           text
);

-- Holds 14 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS marketing.case_resolution (
    id                                uuid PRIMARY KEY,
    scope_path                        ltree NOT NULL,
    case_id                           text NOT NULL,
    resolution_category               text NOT NULL CONSTRAINT case_resolution_resolution_category_chk CHECK (resolution_category IN ('informationProvided', 'ticketReissued', 'bookingChanged', 'refundProcessed', 'compensationIssued', 'technicalIssueResolved', 'customerError', 'policyApplied', 'duplicate', 'noActionRequired', 'other')),
    resolution_summary                text NOT NULL CONSTRAINT case_resolution_resolution_summary_chk CHECK (char_length(resolution_summary) <= 2000),
    action_taken                      text CONSTRAINT case_resolution_action_taken_chk CHECK (char_length(action_taken) <= 2000),
    financial_impact                  numeric(18,4),
    compensation_request_ids          text[],
    root_cause                        text NOT NULL CONSTRAINT case_resolution_root_cause_chk CHECK (root_cause IN ('customer', 'product', 'payment', 'system', 'integration', 'operational', 'content', 'policy', 'staff', 'unknown')),
    duplicate_of_case_id              text,
    customer_notification             jsonb,
    resolved_by                       uuid,
    resolution_date                   timestamptz,
    updated_at                        timestamptz
);

-- Holds 17 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS marketing.case_routing_rule (
    id                                uuid PRIMARY KEY,
    code                              text NOT NULL CONSTRAINT case_routing_rule_code_chk CHECK (char_length(code) <= 60),
    name                              text NOT NULL CONSTRAINT case_routing_rule_name_chk CHECK (char_length(name) <= 150),
    rank                              integer NOT NULL,
    queue_id                          uuid,
    match                             jsonb,
    strategy                          text NOT NULL CONSTRAINT case_routing_rule_strategy_chk CHECK (strategy IN ('roundRobin', 'leastBusy', 'skillBased', 'priorityBased', 'languageBased', 'customerTierBased', 'aiRecommended')),
    required_skills                   text[],
    require_language_match            boolean DEFAULT true,
    max_utilization_rate              numeric(18,4),
    respect_sla_capability            boolean DEFAULT true,
    sticky_ownership                  boolean DEFAULT false,
    sticky_window_hours               integer,
    fallback_queue_id                 uuid,
    is_active                         boolean NOT NULL,
    scope_path                        ltree NOT NULL,
    updated_at                        timestamptz
);

-- Holds 17 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS marketing.case_service_action (
    id                                text PRIMARY KEY NOT NULL,
    scope_path                        ltree NOT NULL,
    mode                              text NOT NULL CONSTRAINT case_service_action_mode_chk CHECK (mode IN ('evaluate', 'execute')),
    case_id                           text,
    order_id                          text NOT NULL,
    line_ids                          text[],
    action                            text CONSTRAINT case_service_action_action_chk CHECK (action IN ('resendTicket', 'downloadTicket', 'reissue', 'transfer', 'changeName', 'reschedule', 'exchange', 'upgrade', 'cancel')),
    target_performance_id             uuid,
    target_product_id                 uuid,
    recipient_subject_id              uuid,
    delivery_channel                  text,
    reason                            text CONSTRAINT case_service_action_reason_chk CHECK (char_length(reason) <= 500),
    status                            text CONSTRAINT case_service_action_status_chk CHECK (status IN ('completed', 'pendingPayment', 'refused', 'failed')),
    downstream_operation              text,
    downstream_reference              text,
    performed_by_principal_id         uuid,
    updated_at                        timestamptz
);

-- A challenge, mission or streak (22.6, CF-137). Gamification is not loyalty — loyalty pays for
-- spend, a challenge pays for behaviour spend does not produce
CREATE TABLE IF NOT EXISTS marketing.challenge (
    id                                uuid PRIMARY KEY NOT NULL,
    name                              text NOT NULL,
    kind                              text NOT NULL CONSTRAINT challenge_kind_chk CHECK (kind IN ('visit', 'spend', 'ride', 'collection', 'streak', 'referral', 'survey', 'social', 'milestone', 'scan', 'activity', 'purchase')),
    scope                             text DEFAULT 'individual' CONSTRAINT challenge_scope_chk CHECK (scope IN ('individual', 'family', 'group', 'team')),
    goal                              jsonb NOT NULL,
    event_id                          uuid,
    reward_kind                       text CONSTRAINT challenge_reward_kind_chk CHECK (reward_kind IN ('badge', 'loyaltyPoints', 'walletCredit', 'voucher', 'entitlement', 'none')),
    reward_value                      integer,
    reward_amount                     numeric(18,4),
    badge_asset_id                    uuid,
    starts_at                         timestamptz,
    ends_at                           timestamptz,
    status                            text NOT NULL CONSTRAINT challenge_status_chk CHECK (status IN ('draft', 'active', 'paused', 'ended', 'archived')),
    scope_path                        ltree NOT NULL
);

-- How far a guest is (22.6.15). Progress is shown, not just the outcome — a guest two visits from
-- a reward behaves differently from one who does not know
CREATE TABLE IF NOT EXISTS marketing.challenge_progress (
    id                                uuid PRIMARY KEY NOT NULL,
    challenge_id                      uuid NOT NULL,
    subject_id                        uuid NOT NULL,
    portfolio_id                      uuid,
    current                           numeric(18,4) NOT NULL,
    target                            numeric(18,4) NOT NULL,
    streak_count                      integer,
    completed_at                      timestamptz,
    reward_issued_at                  timestamptz
);

-- Holds 18 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS marketing.communication_policy_decision (
    id                                uuid PRIMARY KEY NOT NULL,
    communication_id                  text NOT NULL,
    subject_id                        uuid NOT NULL,
    message_class                     text NOT NULL CONSTRAINT communication_policy_decision_message_class_chk CHECK (message_class IN ('transactional', 'operational', 'service', 'marketing')),
    channel                           text NOT NULL CONSTRAINT communication_policy_decision_channel_chk CHECK (channel IN ('email', 'sms', 'whatsapp', 'push', 'inApp', 'post')),
    marketing_consent                 text CONSTRAINT communication_policy_decision_marketing_consent_chk CHECK (marketing_consent IN ('granted', 'withdrawn', 'notAsked')),
    email_preference                  boolean,
    sms_preference                    boolean,
    whatsapp_preference               boolean,
    push_preference                   boolean,
    language                          text,
    is_contact_restricted             boolean,
    jurisdiction                      text,
    suppression_reason                text CONSTRAINT communication_policy_decision_suppression_reason_chk CHECK (suppression_reason IN ('unsubscribed', 'invalidEmail', 'invalidMobile', 'hardBounce', 'complaint', 'administrative')),
    decision                          text NOT NULL CONSTRAINT communication_policy_decision_decision_chk CHECK (decision IN ('allowed', 'blocked', 'rerouted', 'suppressed')),
    reasons                           text[],
    rerouted_to_channel               text CONSTRAINT communication_policy_decision_rerouted_to_channel_chk CHECK (rerouted_to_channel IN ('email', 'sms', 'whatsapp', 'push', 'inApp', 'post')),
    evaluated_at                      timestamptz NOT NULL
);

-- Holds 17 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS marketing.communication_preference_type (
    category_code                     text NOT NULL CONSTRAINT communication_preference_type_category_code_chk CHECK (char_length(category_code) <= 60),
    name                              text NOT NULL CONSTRAINT communication_preference_type_name_chk CHECK (char_length(name) <= 150),
    description                       text CONSTRAINT communication_preference_type_description_chk CHECK (char_length(description) <= 1000),
    classification                    text NOT NULL CONSTRAINT communication_preference_type_classification_chk CHECK (classification IN ('transactional', 'marketing')),
    communication_type                text CONSTRAINT communication_preference_type_communication_type_chk CHECK (communication_type IN ('orderConfirmation', 'ticketDelivery', 'paymentInformation', 'eventChanges', 'securityMessages', 'promotions', 'newEvents', 'membershipOffers', 'loyaltyOffers', 'birthdayCampaigns', 'partnerOffers', 'surveys', 'other')),
    consent_purpose                   text,
    available_channels                text[] NOT NULL,
    applicable_brand_ids              text[],
    applicable_countries              text[],
    is_customer_editable              boolean NOT NULL,
    default_behavior                  text NOT NULL CONSTRAINT communication_preference_type_default_behavior_chk CHECK (default_behavior IN ('on', 'off')),
    reconfirm_after_months            integer,
    status                            text DEFAULT 'active' CONSTRAINT communication_preference_type_status_chk CHECK (status IN ('active', 'retired')),
    id                                uuid PRIMARY KEY NOT NULL,
    version                           integer NOT NULL,
    scope_path                        ltree NOT NULL,
    updated_at                        timestamptz
);

-- Holds 21 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS marketing.communication_provider (
    id                                uuid PRIMARY KEY,
    scope_path                        ltree NOT NULL,
    provider_name                     text NOT NULL CONSTRAINT communication_provider_provider_name_chk CHECK (char_length(provider_name) <= 120),
    channel                           text NOT NULL CONSTRAINT communication_provider_channel_chk CHECK (channel IN ('email', 'sms', 'whatsapp', 'push', 'inApp', 'post')),
    account                           text NOT NULL CONSTRAINT communication_provider_account_chk CHECK (char_length(account) <= 200),
    environment                       text NOT NULL CONSTRAINT communication_provider_environment_chk CHECK (environment IN ('production', 'sandbox')),
    region                            text,
    country                           text,
    brand_id                          uuid,
    legal_entity_id                   uuid,
    credentials_secret_ref            text NOT NULL,
    api_configuration                 jsonb,
    webhook_configuration             jsonb,
    rate_limit_per_second             integer,
    rate_limit_per_minute             integer,
    timeout_seconds                   integer,
    retry_policy                      jsonb,
    role                              text NOT NULL CONSTRAINT communication_provider_role_chk CHECK (role IN ('primary', 'secondary', 'emergencyFallback')),
    priority                          integer,
    status                            text NOT NULL CONSTRAINT communication_provider_status_chk CHECK (status IN ('active', 'standby', 'degraded', 'suspended', 'disabled')),
    updated_at                        timestamptz
);

-- Holds 14 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS marketing.communication_routing_rule (
    id                                uuid PRIMARY KEY NOT NULL,
    scope_path                        ltree NOT NULL,
    channel                           text NOT NULL CONSTRAINT communication_routing_rule_channel_chk CHECK (channel IN ('email', 'sms', 'whatsapp', 'push', 'inApp', 'post')),
    country                           text,
    brand_id                          uuid,
    message_class                     text CONSTRAINT communication_routing_rule_message_class_chk CHECK (message_class IN ('transactional', 'operational', 'service', 'marketing')),
    priority_class                    text CONSTRAINT communication_routing_rule_priority_class_chk CHECK (priority_class IN ('P1', 'P2', 'P3', 'P4')),
    recipient_type                    text CONSTRAINT communication_routing_rule_recipient_type_chk CHECK (recipient_type IN ('customer', 'partner', 'employee')),
    skip_unhealthy_providers          boolean,
    cost_aware                        boolean,
    channel_fallback                  text[],
    throttle                          jsonb,
    is_active                         boolean NOT NULL,
    updated_at                        timestamptz
);

-- Holds 13 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS marketing.consent_capture_point (
    capture_point                     text NOT NULL CONSTRAINT consent_capture_point_capture_point_chk CHECK (capture_point IN ('accountRegistration', 'guestCheckout', 'ticketPurchase', 'membershipEnrolment', 'annualPassEnrolment', 'mobileAppRegistration', 'posCustomerCreation', 'kiosk', 'crmCustomerCreation', 'walletEnrolment', 'faceEnrolment', 'newsletterSignup', 'customerPortal', 'competitionPromotion', 'apiPartnerJourney')),
    channel                           text NOT NULL CONSTRAINT consent_capture_point_channel_chk CHECK (channel IN ('guestApp', 'website', 'kiosk', 'pos', 'callCentre', 'import', 'agentRecorded')),
    brand_id                          uuid,
    country                           text,
    customer_type                     text CONSTRAINT consent_capture_point_customer_type_chk CHECK (customer_type IN ('individual', 'member', 'corporate', 'group', 'school')),
    skip_if_current_version_accepted  boolean DEFAULT true,
    languages                         text[],
    status                            text DEFAULT 'active' CONSTRAINT consent_capture_point_status_chk CHECK (status IN ('active', 'retired')),
    id                                uuid PRIMARY KEY NOT NULL,
    version                           integer NOT NULL,
    publication_status                text NOT NULL CONSTRAINT consent_capture_point_publication_status_chk CHECK (publication_status IN ('draft', 'review', 'approved', 'published', 'superseded')),
    scope_path                        ltree NOT NULL,
    updated_at                        timestamptz
);

-- Holds 9 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS marketing.consent_propagation (
    id                                uuid PRIMARY KEY NOT NULL,
    consent_record_id                 text NOT NULL,
    target                            text NOT NULL CONSTRAINT consent_propagation_target_chk CHECK (target IN ('crm', 'marketing', 'campaignAudience', 'connectedSystem')),
    target_name                       text CONSTRAINT consent_propagation_target_name_chk CHECK (char_length(target_name) <= 200),
    status                            text NOT NULL DEFAULT 'requested' CONSTRAINT consent_propagation_status_chk CHECK (status IN ('requested', 'processed', 'propagated', 'acknowledged', 'failed', 'retryRequired')),
    attempts                          integer DEFAULT 0,
    error                             text CONSTRAINT consent_propagation_error_chk CHECK (char_length(error) <= 500),
    created_at                        timestamptz,
    updated_at                        timestamptz
);

-- What a tenant may ask consent for. The question is the tenant’s; the answer is the guest’s
CREATE TABLE IF NOT EXISTS marketing.consent_purpose (
    purpose                           text NOT NULL CONSTRAINT consent_purpose_purpose_chk CHECK (purpose IN ('marketing', 'personalisation', 'profiling', 'thirdPartySharing', 'aiProcessing', 'transactional')),
    display_name                      text,
    description                       text,
    notice_version                    text NOT NULL,
    is_required_for_service           boolean NOT NULL,
    expires_after_months              integer,
    id                                uuid PRIMARY KEY NOT NULL,
    tenant_id                         uuid NOT NULL
);

-- Holds 3 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS marketing.consent_purpose_channel (
    consent_purpose_id                uuid NOT NULL,
    channel                           text NOT NULL,
    id                                uuid PRIMARY KEY NOT NULL
);

-- Holds 11 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS marketing.consent_question (
    id                                text PRIMARY KEY NOT NULL,
    kind                              text NOT NULL CONSTRAINT consent_question_kind_chk CHECK (kind IN ('swim', 'scuba', 'risk', 'custom')),
    text                              jsonb NOT NULL,
    help_text                         jsonb,
    version                           integer NOT NULL,
    scope                             text NOT NULL DEFAULT 'perPerson' CONSTRAINT consent_question_scope_chk CHECK (scope IN ('perPerson', 'perBooking')),
    is_required                       boolean NOT NULL DEFAULT true,
    blocking_answer                   text NOT NULL DEFAULT 'none' CONSTRAINT consent_question_blocking_answer_chk CHECK (blocking_answer IN ('yes', 'no', 'none')),
    status                            text NOT NULL DEFAULT 'active' CONSTRAINT consent_question_status_chk CHECK (status IN ('active', 'retired')),
    scope_path                        ltree NOT NULL,
    updated_at                        timestamptz
);

-- Holds 6 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS marketing.consent_question_version (
    question_id                       text NOT NULL,
    version                           integer NOT NULL,
    text                              jsonb NOT NULL,
    published_at                      timestamptz NOT NULL,
    published_by                      uuid,
    id                                uuid PRIMARY KEY NOT NULL
);

-- What a guest agreed to and when. A merge takes the narrower of two (CF-160)
CREATE TABLE IF NOT EXISTS marketing.consent_record (
    purpose                           text NOT NULL CONSTRAINT consent_record_purpose_chk CHECK (purpose IN ('marketing', 'personalisation', 'profiling', 'thirdPartySharing', 'aiProcessing', 'transactional')),
    decision                          text NOT NULL CONSTRAINT consent_record_decision_chk CHECK (decision IN ('granted', 'withdrawn', 'notAsked')),
    notice_version                    text NOT NULL,
    source                            text NOT NULL CONSTRAINT consent_record_source_chk CHECK (source IN ('guestApp', 'website', 'kiosk', 'pos', 'callCentre', 'import', 'agentRecorded')),
    recorded_at                       timestamptz NOT NULL,
    id                                text PRIMARY KEY NOT NULL,
    subject_id                        uuid NOT NULL,
    recorded_by_principal_id          uuid,
    superseded_at                     timestamptz
);

-- Holds 3 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS marketing.consent_record_channel (
    consent_record_id                 text NOT NULL,
    channel                           text NOT NULL,
    id                                uuid PRIMARY KEY NOT NULL
);

-- Holds 22 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS marketing.contact_automation (
    id                                uuid PRIMARY KEY,
    code                              text NOT NULL CONSTRAINT contact_automation_code_chk CHECK (char_length(code) <= 60),
    name                              text NOT NULL CONSTRAINT contact_automation_name_chk CHECK (char_length(name) <= 150),
    owner_principal_id                uuid,
    level                             text NOT NULL CONSTRAINT contact_automation_level_chk CHECK (level IN ('recommendOnly', 'agentConfirmation', 'supervisorGoverned', 'fullyAutomated')),
    trigger                           jsonb NOT NULL,
    scope                             jsonb,
    allowed_actions                   text[] NOT NULL,
    confidence_threshold              numeric(18,4) NOT NULL,
    on_exception                      text NOT NULL CONSTRAINT contact_automation_on_exception_chk CHECK (on_exception IN ('leaveForAgent', 'routeToQueue', 'notifySupervisor')),
    exception_queue_id                uuid,
    effective_from                    timestamptz,
    effective_to                      timestamptz,
    kill_switch                       boolean DEFAULT false,
    status                            text NOT NULL CONSTRAINT contact_automation_status_chk CHECK (status IN ('draft', 'approved', 'active', 'paused', 'retired')),
    version                           integer,
    approved_by_principal_id          uuid,
    approved_at                       timestamptz,
    last_simulation                   jsonb,
    executions_last30_days            integer,
    scope_path                        ltree NOT NULL,
    updated_at                        timestamptz
);

-- A live session with somebody waiting. Not a case — a case is a ticket measured in hours, this is
-- measured in seconds. A conversation may create a case; it is not one Hangs off: reaches
-- marketing.guest_profile through its keys; references identity.principal, marketing.case,
-- marketing.kiosk_assist_session. Reached by: 13 operations read it and 6 write it; 2 tables
-- reference it.
CREATE TABLE IF NOT EXISTS marketing.conversation (
    id                                uuid PRIMARY KEY NOT NULL,
    telephony                         jsonb,
    assist_session_id                 uuid,
    channel                           text NOT NULL CONSTRAINT conversation_channel_chk CHECK (channel IN ('webChat', 'inAppChat', 'whatsapp', 'sms', 'email', 'kiosk', 'voice')),
    state                             text NOT NULL CONSTRAINT conversation_state_chk CHECK (state IN ('withAssistant', 'queued', 'withAgent', 'waitingOnGuest', 'resolved', 'abandoned', 'timedOut')),
    subject_id                        uuid,
    venue_id                          uuid,
    assigned_principal_id             uuid,
    queue_id                          uuid,
    queue_position                    integer,
    estimated_wait_seconds            integer,
    handover_reason                   text CONSTRAINT conversation_handover_reason_chk CHECK (handover_reason IN ('guestRequested', 'assistantRefused', 'assistantFailed', 'outOfScope', 'negativeSentiment', 'complexIntent', 'paymentIssue')),
    handover_summary                  text,
    sentiment                         text CONSTRAINT conversation_sentiment_chk CHECK (sentiment IN ('positive', 'neutral', 'negative', 'escalating')),
    intent                            text,
    locale                            text,
    case_id                           text,
    first_response_seconds            integer,
    started_at                        timestamptz,
    closed_at                         timestamptz,
    outcome                           text CONSTRAINT conversation_outcome_chk CHECK (outcome IN ('resolved', 'caseRaised', 'abandonedByGuest', 'timedOut', 'spam'))
);

-- One message. The sender is resolved, never declared, and the assistant is labelled as one — a
-- guest talking to a bot that presents as a person is a complaint waiting to happen Hangs off: a
-- child of marketing.conversation; reaches marketing.guest_profile through its keys; references
-- ai.activity, identity.principal, marketing.conversation. Reached by: 8 operations read it and 1
-- write it; 1 tables re
CREATE TABLE IF NOT EXISTS marketing.conversation_message (
    id                                uuid PRIMARY KEY NOT NULL,
    sender                            text NOT NULL CONSTRAINT conversation_message_sender_chk CHECK (sender IN ('guest', 'agent', 'assistant', 'system')),
    sender_principal_id               uuid,
    body                              text NOT NULL,
    ai_interaction_id                 uuid,
    sent_at                           timestamptz NOT NULL,
    read_at                           timestamptz,
    conversation_id                   uuid NOT NULL
);

-- Holds 4 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS marketing.conversation_message_attachment (
    conversation_message_id           uuid NOT NULL,
    asset_id                          uuid,
    kind                              text,
    id                                uuid PRIMARY KEY NOT NULL
);

-- Holds 16 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS marketing.cookie_banner_design (
    id                                uuid PRIMARY KEY,
    brand_id                          uuid,
    inherits_from_id                  uuid,
    channel                           text NOT NULL CONSTRAINT cookie_banner_design_channel_chk CHECK (channel IN ('b2cWebsite', 'customerPortal', 'mobileApp', 'embeddedCheckout', 'whiteLabelSite', 'partnerMicrosite')),
    logo_asset_id                     uuid,
    title                             jsonb,
    body                              jsonb,
    position                          text NOT NULL CONSTRAINT cookie_banner_design_position_chk CHECK (position IN ('top', 'bottom', 'popup', 'modal')),
    theme_id                          text,
    reject_is_one_click               boolean NOT NULL DEFAULT true,
    languages                         text[] NOT NULL,
    notice_version                    text,
    version                           integer,
    status                            text CONSTRAINT cookie_banner_design_status_chk CHECK (status IN ('draft', 'published', 'superseded')),
    scope_path                        ltree NOT NULL,
    updated_at                        timestamptz
);

-- Holds 9 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS marketing.customer_badge (
    id                                uuid PRIMARY KEY,
    customer_id                       uuid NOT NULL,
    badge_id                          uuid NOT NULL,
    challenge_id                      uuid,
    source_type                       text CONSTRAINT customer_badge_source_type_chk CHECK (char_length(source_type) <= 30),
    source_reference_id               uuid,
    awarded_at                        timestamptz NOT NULL,
    expires_at                        timestamptz,
    status                            text NOT NULL CONSTRAINT customer_badge_status_chk CHECK (char_length(status) <= 20)
);

-- Holds 10 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS marketing.duplicate_candidate (
    id                                uuid PRIMARY KEY,
    subject_ids                       text[],
    score                             numeric(18,4),
    band                              text CONSTRAINT duplicate_candidate_band_chk CHECK (band IN ('match', 'possibleMatch')),
    matched_on                        text[],
    linked_record_counts              jsonb,
    status                            text CONSTRAINT duplicate_candidate_status_chk CHECK (status IN ('pending', 'merged', 'rejected', 'split')),
    decided_by                        uuid,
    decided_at                        timestamptz,
    scope_path                        ltree NOT NULL
);

-- Holds 11 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS marketing.feedback_classification (
    id                                uuid PRIMARY KEY NOT NULL,
    source                            text NOT NULL CONSTRAINT feedback_classification_source_chk CHECK (source IN ('csatSurvey', 'serviceRating', 'nps', 'postCaseSurvey', 'complaint', 'appFeedback', 'webFeedback', 'directComment')),
    form_submission_id                uuid,
    review_id                         text,
    case_id                           text,
    sentiment                         text CONSTRAINT feedback_classification_sentiment_chk CHECK (sentiment IN ('positive', 'neutral', 'negative')),
    topic                             text CONSTRAINT feedback_classification_topic_chk CHECK (char_length(topic) <= 100),
    confidence                        numeric(18,4),
    model_version                     text CONSTRAINT feedback_classification_model_version_chk CHECK (char_length(model_version) <= 100),
    classified_at                     timestamptz NOT NULL,
    scope_path                        ltree NOT NULL
);

-- A waiver, survey or capture form (CF-129). One mechanism, three uses — three implementations
-- would drift on the version rule first
CREATE TABLE IF NOT EXISTS marketing.form_definition (
    id                                uuid PRIMARY KEY NOT NULL,
    name                              text NOT NULL,
    kind                              text NOT NULL CONSTRAINT form_definition_kind_chk CHECK (kind IN ('waiver', 'survey', 'dataCapture', 'consentForm', 'incidentReport', 'registration')),
    version                           integer NOT NULL,
    requires_signature                boolean DEFAULT false,
    signature_kind                    text DEFAULT 'none' CONSTRAINT form_definition_signature_kind_chk CHECK (signature_kind IN ('drawn', 'typed', 'checkbox', 'none')),
    score_scale                       text CONSTRAINT form_definition_score_scale_chk CHECK (score_scale IN ('nps', 'csat', 'ces', 'likert5', 'likert7', 'stars')),
    applies_to_product_ids            text[],
    valid_for_months                  integer,
    minimum_age                       integer,
    requires_guardian_for_minors      boolean DEFAULT true,
    status                            text NOT NULL CONSTRAINT form_definition_status_chk CHECK (status IN ('draft', 'published', 'superseded', 'retired')),
    legal_reviewed_by                 text,
    legal_reviewed_at                 timestamptz,
    scope_path                        ltree NOT NULL
);

-- Holds 11 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS marketing.form_definition_field (
    label_localised                   jsonb,
    type                              text NOT NULL,
    options                           text[],
    is_required                       boolean,
    consent_purpose_id                uuid,
    show_when                         jsonb,
    form_definition_id                uuid NOT NULL,
    form_id                           uuid NOT NULL,
    form_version                      integer NOT NULL,
    key                               text NOT NULL CONSTRAINT form_definition_field_key_chk CHECK (char_length(key) <= 60),
    label                             jsonb NOT NULL,
    help_text                         jsonb,
    field_type                        text NOT NULL CONSTRAINT form_definition_field_field_type_chk CHECK (field_type IN ('shortText', 'longText', 'number', 'date', 'yesNo', 'checkbox', 'singleSelect', 'multiSelect', 'dropdown', 'email', 'mobile', 'address', 'customerLookup', 'participantLookup', 'signature', 'initials')),
    standard_field                    text CONSTRAINT form_definition_field_standard_field_chk CHECK (standard_field IN ('participantName', 'dateOfBirth', 'customerId', 'bookingReference', 'ticketNumber', 'guardianName', 'guardianRelationship', 'emergencyContact')),
    requirement                       text NOT NULL CONSTRAINT form_definition_field_requirement_chk CHECK (requirement IN ('required', 'optional', 'conditional', 'readOnly', 'autoPopulated')),
    validation                        jsonb,
    maps_to                           text CONSTRAINT form_definition_field_maps_to_chk CHECK (maps_to IN ('guestName', 'guestDateOfBirth', 'guestEmail', 'guestMobile', 'guestAddress', 'guestId', 'ticketHolderName', 'orderReference', 'ticketNumber')),
    is_personal_data                  boolean DEFAULT false,
    sort_order                        integer DEFAULT 0,
    is_deleted                        boolean DEFAULT false,
    scope_path                        ltree NOT NULL,
    updated_at                        timestamptz,
    id                                uuid PRIMARY KEY NOT NULL
);

-- The acceptance record, and it is evidence (2.15.13). Bound to the version accepted, not to the
-- form. Hangs off: reaches marketing.guest_profile through its keys; references
-- assets.media_asset, pii.subject. Reached by: 18 operations read it and 1 write it; 3 tables
-- reference it.
CREATE TABLE IF NOT EXISTS marketing.form_submission (
    id                                uuid PRIMARY KEY NOT NULL,
    form_id                           uuid NOT NULL,
    form_version                      integer NOT NULL,
    subject_id                        uuid NOT NULL,
    on_behalf_of_subject_id           uuid,
    answers                           jsonb,
    signature_asset_id                uuid,
    submitted_at                      timestamptz NOT NULL,
    synced_at                         timestamptz,
    expires_at                        timestamptz,
    captured_at_channel               text CONSTRAINT form_submission_captured_at_channel_chk CHECK (captured_at_channel IN ('pos', 'kiosk', 'guestApp', 'guestWeb', 'callCentre', 'partner', 'api', 'backOffice', 'b2b', 'ota')),
    ip_address                        text
);

-- Holds 4 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS marketing.guest_attribute_model (
    version                           integer,
    published_at                      timestamptz,
    scope_path                        ltree NOT NULL,
    id                                uuid PRIMARY KEY NOT NULL
);

-- A phone or browser a guest has registered. How they revoke an old one that still holds tickets
CREATE TABLE IF NOT EXISTS marketing.guest_device (
    id                                uuid PRIMARY KEY NOT NULL,
    subject_id                        uuid NOT NULL,
    platform                          text NOT NULL CONSTRAINT guest_device_platform_chk CHECK (platform IN ('ios', 'android', 'web')),
    token_fingerprint                 text,
    token_ref                         text,
    app_version                       text,
    os_version                        text,
    device_model                      text,
    locale                            text,
    status                            text NOT NULL CONSTRAINT guest_device_status_chk CHECK (status IN ('active', 'revoked', 'failed')),
    failure_count                     integer,
    registered_at                     timestamptz NOT NULL,
    last_seen_at                      timestamptz,
    revoked_at                        timestamptz
);

-- A guest photo, ID or signed document (BL-133). Deliberately not assets — a passport scan is not
-- a marketing asset and has a different retention clock
CREATE TABLE IF NOT EXISTS marketing.guest_document (
    id                                uuid PRIMARY KEY NOT NULL,
    subject_id                        uuid NOT NULL,
    kind                              text NOT NULL CONSTRAINT guest_document_kind_chk CHECK (kind IN ('avatar', 'idDocument', 'visa', 'signedWaiver', 'medicalNote', 'accessibilityEvidence', 'photo', 'other')),
    storage_ref                       text NOT NULL,
    content_type                      text,
    consent_purpose_id                uuid,
    retain_until                      date NOT NULL,
    uploaded_at                       timestamptz,
    uploaded_by_principal_id          uuid
);

-- Holds 9 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS marketing.guest_extra_field (
    id                                uuid PRIMARY KEY,
    tenant_id                         uuid NOT NULL,
    name                              text NOT NULL CONSTRAINT guest_extra_field_name_chk CHECK (char_length(name) <= 150),
    type                              text NOT NULL CONSTRAINT guest_extra_field_type_chk CHECK (char_length(type) <= 30),
    is_required                       boolean NOT NULL,
    display_order                     integer NOT NULL,
    is_active                         boolean NOT NULL,
    created_at                        timestamptz NOT NULL,
    updated_at                        timestamptz
);

-- Holds 5 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS marketing.guest_extra_option (
    id                                uuid PRIMARY KEY,
    field_id                          uuid NOT NULL,
    name                              text NOT NULL CONSTRAINT guest_extra_option_name_chk CHECK (char_length(name) <= 150),
    display_order                     integer NOT NULL,
    is_active                         boolean NOT NULL
);

-- Holds 6 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS marketing.guest_extra_value (
    id                                uuid PRIMARY KEY,
    customer_id                       uuid NOT NULL,
    field_id                          uuid NOT NULL,
    field_value                       text CONSTRAINT guest_extra_value_field_value_chk CHECK (char_length(field_value) <= 2000),
    created_at                        timestamptz NOT NULL,
    updated_at                        timestamptz
);

-- Every offered profile match and the guest's answer. Kept so a merge done later by staff can see
-- that the guest once said *not me*
CREATE TABLE IF NOT EXISTS marketing.guest_match_decision (
    id                                uuid PRIMARY KEY,
    cart_id                           text,
    matched_profile_id                uuid,
    matched_on                        text CONSTRAINT guest_match_decision_matched_on_chk CHECK (matched_on IN ('email', 'mobile')),
    decision                          text NOT NULL CONSTRAINT guest_match_decision_decision_chk CHECK (decision IN ('useExisting', 'keepSeparate')),
    decided_at                        timestamptz,
    scope_path                        ltree NOT NULL
);

-- How a returning guest is recognised at checkout: by email, mobile or either. One per venue. The
-- match is offered to the guest, never applied for them
CREATE TABLE IF NOT EXISTS marketing.guest_match_policy (
    id                                uuid PRIMARY KEY,
    match_by                          text NOT NULL DEFAULT 'email' CONSTRAINT guest_match_policy_match_by_chk CHECK (match_by IN ('email', 'mobile', 'emailOrMobile')),
    offer_at_checkout                 boolean DEFAULT true,
    scope_path                        ltree NOT NULL
);

-- Holds 9 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS marketing.guest_note (
    id                                text PRIMARY KEY NOT NULL,
    subject_id                        uuid NOT NULL,
    kind                              text NOT NULL CONSTRAINT guest_note_kind_chk CHECK (kind IN ('allergy', 'dietary', 'seatingPreference', 'occasion', 'serviceRecovery', 'vip', 'general')),
    text                              text NOT NULL,
    is_allergy                        boolean DEFAULT false,
    visible_to_server                 boolean DEFAULT true,
    author_principal_id               uuid,
    recorded_at                       timestamptz NOT NULL,
    synced_at                         timestamptz
);

-- Holds 7 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS marketing.guest_preference (
    id                                uuid PRIMARY KEY,
    subject_id                        uuid,
    seating_preference                text CONSTRAINT guest_preference_seating_preference_chk CHECK (char_length(seating_preference) <= 200),
    drink_preferences                 text[],
    dietary                           text[],
    accessibility                     text[],
    updated_at                        timestamptz
);

-- What a venue knows about a guest that is not their identity — preferences, lifetime value,
-- segments, consent. Twenty operations touch it and it references pii.subject rather than
-- duplicating it
CREATE TABLE IF NOT EXISTS marketing.guest_profile (
    id                                uuid PRIMARY KEY,
    subject_id                        uuid NOT NULL,
    display_name                      text,
    email                             text,
    phone                             text,
    preferred_language                text,
    preferred_channel                 text CONSTRAINT guest_profile_preferred_channel_chk CHECK (preferred_channel IN ('email', 'sms', 'whatsapp', 'push', 'inApp', 'post')),
    guest_link_id                     text,
    tags                              text[],
    engagement_score                  integer,
    engagement_tier                   text CONSTRAINT guest_profile_engagement_tier_chk CHECK (engagement_tier IN ('new', 'active', 'occasional', 'lapsing', 'lapsed', 'dormant')),
    lifetime_value                    numeric(18,4),
    visit_count                       integer,
    last_visit_at                     timestamptz,
    is_active                         boolean NOT NULL,
    merged_into_subject_id            uuid,
    merged_at                         timestamptz,
    loyalty_position_id               uuid,
    open_case_count                   integer,
    recent_order_ids                  text[],
    membership_ids                    text[],
    notes                             text,
    segment_id                        uuid NOT NULL
);

-- Holds 10 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS marketing.guest_relationship (
    id                                uuid PRIMARY KEY,
    related_subject_id                uuid,
    organisation_id                   uuid,
    kind                              text NOT NULL CONSTRAINT guest_relationship_kind_chk CHECK (kind IN ('parent', 'guardian', 'spouse', 'dependant', 'householdMember', 'employee', 'student', 'groupLeader', 'travelAgent', 'reseller')),
    authorities                       text[],
    effective_from                    date,
    effective_to                      date,
    shared_benefits                   boolean DEFAULT false,
    verified_at                       timestamptz,
    scope_path                        ltree NOT NULL
);

-- Holds 7 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS marketing.identity_rules (
    match_threshold                   numeric(18,4),
    possible_match_threshold          numeric(18,4),
    excluded_sources                  text[],
    jurisdiction_restrictions         text[],
    is_auto_merge_allowed             boolean DEFAULT false,
    scope_path                        ltree NOT NULL,
    id                                uuid PRIMARY KEY NOT NULL
);

-- One addressed invitation with a single-use token (BL-150). A link forwarded to a group chat is
-- the failure mode. Hangs off: reaches marketing.guest_profile through its keys; references
-- catalogue.performance, catalogue.product, identity.principal. Reached by: 1 operations read it
-- and 1 write it.
CREATE TABLE IF NOT EXISTS marketing.invitation (
    id                                uuid PRIMARY KEY NOT NULL,
    product_id                        uuid NOT NULL,
    performance_id                    uuid,
    quantity                          integer NOT NULL,
    reason                            text NOT NULL,
    offered_by_principal_id           uuid NOT NULL,
    issued_by_principal_id            uuid,
    recipient_name                    text,
    recipient_email                   text,
    cost_center_id                    uuid,
    entitlement_ids                   text[],
    issued_at                         timestamptz NOT NULL,
    scope_path                        ltree NOT NULL
);

-- A quota-bounded addressed invitation (BL-150). A campaign broadcasts; an invitation expects a
-- response. quota is places and overInvitePercent is invitations
CREATE TABLE IF NOT EXISTS marketing.invitation_campaign (
    id                                uuid PRIMARY KEY NOT NULL,
    name                              text NOT NULL,
    event_id                          uuid,
    product_id                        uuid,
    quota                             integer NOT NULL,
    over_invite_percent               numeric(18,4) DEFAULT 0,
    issued_count                      integer,
    accepted_count                    integer,
    respond_by_at                     timestamptz,
    status                            text NOT NULL CONSTRAINT invitation_campaign_status_chk CHECK (status IN ('draft', 'open', 'closed', 'cancelled')),
    scope_path                        ltree NOT NULL
);

-- An automated multi-step journey (22.3.1b–22.3.10b, CF-137). A MessageTrigger is one step of it —
-- a journey is what you need when the next message depends on what the guest did about the last
CREATE TABLE IF NOT EXISTS marketing.journey (
    id                                uuid PRIMARY KEY NOT NULL,
    name                              text NOT NULL,
    template_kind                     text CONSTRAINT journey_template_kind_chk CHECK (template_kind IN ('abandonedCart', 'membershipLifecycle', 'loyaltyLifecycle', 'walletLifecycle', 'birthday', 'onboarding', 'winBack', 'custom')),
    entry_event                       text NOT NULL,
    entry_conditions                  jsonb,
    status                            text NOT NULL CONSTRAINT journey_status_chk CHECK (status IN ('draft', 'active', 'paused', 'archived')),
    max_duration_days                 integer DEFAULT 30,
    reentry_policy                    text DEFAULT 'afterCompletion' CONSTRAINT journey_reentry_policy_chk CHECK (reentry_policy IN ('never', 'afterCompletion', 'always')),
    scope_path                        ltree NOT NULL
);

-- A guest inside a journey, at a step. Pausing does not evict them, because a half-finished
-- recovery sequence that restarts sends the first message twice
CREATE TABLE IF NOT EXISTS marketing.journey_enrollment (
    id                                uuid PRIMARY KEY NOT NULL,
    journey_id                        uuid NOT NULL,
    subject_id                        uuid NOT NULL,
    step_id                           uuid NOT NULL,
    status                            text CONSTRAINT journey_enrollment_status_chk CHECK (status IN ('active', 'paused', 'completed', 'exited', 'suppressed')),
    entered_at                        timestamptz,
    step_entered_at                   timestamptz,
    next_action_at                    timestamptz,
    exited_at                         timestamptz,
    scope_path                        ltree NOT NULL
);

-- Holds 14 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS marketing.journey_step (
    channel_preference                text[],
    wait_until                        jsonb,
    condition                         jsonb,
    on_true                           text,
    on_false                          text,
    goal_event                        text,
    id                                uuid PRIMARY KEY,
    journey_id                        uuid NOT NULL,
    number                            integer NOT NULL,
    type                              text NOT NULL CONSTRAINT journey_step_type_chk CHECK (char_length(type) <= 40),
    name                              text CONSTRAINT journey_step_name_chk CHECK (char_length(name) <= 150),
    message_template_id               uuid,
    campaign_id                       uuid,
    wait_minutes                      integer,
    condition_json                    text,
    action_config_json                text,
    next_journey_step_id              uuid,
    failure_journey_step_id           uuid,
    is_active                         boolean NOT NULL,
    created_at                        timestamptz NOT NULL
);

-- A staff member acting on a kiosk session remotely (2.1.25). The guest can always see it and
-- always end it — assistance a guest cannot stop is surveillance Hangs off: reaches
-- marketing.guest_profile through its keys; references identity.principal, orders.cart,
-- platform.scope. Reached by: 3 operations read it and 2 write it; 1 tables reference it.
CREATE TABLE IF NOT EXISTS marketing.kiosk_assist_session (
    id                                uuid PRIMARY KEY NOT NULL,
    device_id                         uuid NOT NULL,
    venue_id                          uuid,
    staff_principal_id                uuid NOT NULL,
    staff_display_name                text,
    cart_id                           uuid,
    reason                            text CONSTRAINT kiosk_assist_session_reason_chk CHECK (reason IN ('guestCalled', 'healthAlert', 'stuckSession', 'paymentIssue', 'proactive')),
    ended_by                          text CONSTRAINT kiosk_assist_session_ended_by_chk CHECK (ended_by IN ('staff', 'guest', 'timeout')),
    started_at                        timestamptz NOT NULL,
    ended_at                          timestamptz
);

-- Holds 16 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS marketing.legal_hold (
    hold_id                           uuid,
    kind                              text DEFAULT 'legal' CONSTRAINT legal_hold_kind_chk CHECK (kind IN ('legal', 'operational', 'fraudInvestigation', 'regulatorRequest')),
    reason                            text NOT NULL CONSTRAINT legal_hold_reason_chk CHECK (char_length(reason) <= 1000),
    scope                             jsonb NOT NULL,
    owner_principal_id                uuid,
    starts_at                         timestamptz,
    review_date                       date,
    status                            text DEFAULT 'pendingApproval' CONSTRAINT legal_hold_status_chk CHECK (status IN ('pendingApproval', 'active', 'released')),
    placed_by_principal_id            uuid,
    approved_by_principal_id          uuid,
    approved_at                       timestamptz,
    release_reason                    text CONSTRAINT legal_hold_release_reason_chk CHECK (char_length(release_reason) <= 1000),
    released_at                       timestamptz,
    scope_path                        ltree NOT NULL,
    updated_at                        timestamptz,
    id                                uuid PRIMARY KEY NOT NULL
);

-- A reported or found item (BL-021). The match between the two is the whole capability — without
-- both sides modelled, somebody searches a case list by hand
CREATE TABLE IF NOT EXISTS marketing.lost_item (
    id                                uuid PRIMARY KEY NOT NULL,
    found_or_lost                     text NOT NULL CONSTRAINT lost_item_found_or_lost_chk CHECK (found_or_lost IN ('lost', 'found')),
    kind                              text NOT NULL CONSTRAINT lost_item_kind_chk CHECK (kind IN ('bag', 'phone', 'wallet', 'keys', 'clothing', 'jewellery', 'documents', 'toy', 'buggy', 'other')),
    description                       text,
    colour                            text,
    brand                             text,
    venue_id                          uuid NOT NULL,
    last_seen_point_id                uuid,
    reported_at                       timestamptz NOT NULL,
    synced_at                         timestamptz,
    reported_by_subject_id            uuid,
    storage_location                  text,
    status                            text CONSTRAINT lost_item_status_chk CHECK (status IN ('open', 'matched', 'claimed', 'disposed', 'returned')),
    photo_asset_ids                   text[],
    matched_item_id                   uuid,
    case_id                           text,
    dispose_after                     date
);

-- Holds 9 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS marketing.loyalty_campaign (
    id                                uuid PRIMARY KEY,
    program_id                        uuid NOT NULL,
    campaign_id                       uuid,
    code                              text NOT NULL CONSTRAINT loyalty_campaign_code_chk CHECK (char_length(code) <= 100),
    name                              text NOT NULL CONSTRAINT loyalty_campaign_name_chk CHECK (char_length(name) <= 200),
    start_at                          timestamptz NOT NULL,
    end_at                            timestamptz NOT NULL,
    is_active                         boolean NOT NULL,
    created_at                        timestamptz NOT NULL
);

-- Holds 12 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS marketing.loyalty_points (
    id                                uuid PRIMARY KEY,
    program_id                        uuid NOT NULL,
    customer_id                       uuid NOT NULL,
    transaction_type                  text NOT NULL CONSTRAINT loyalty_points_transaction_type_chk CHECK (char_length(transaction_type) <= 30),
    points                            numeric(18,4) NOT NULL,
    balance_after                     numeric(18,4) NOT NULL,
    source_type                       text CONSTRAINT loyalty_points_source_type_chk CHECK (char_length(source_type) <= 50),
    source_reference_id               uuid,
    expires_at                        timestamptz,
    reversed_loyalty_points_id        uuid,
    notes                             text CONSTRAINT loyalty_points_notes_chk CHECK (char_length(notes) <= 500),
    reason                            text CONSTRAINT loyalty_points_reason_chk CHECK (reason IN ('goodwill', 'correction', 'expiryReversal')),
    author_principal_id               uuid,
    created_at                        timestamptz NOT NULL
);

-- Where a guest stands — points, tier, progress. A balance, not a history
CREATE TABLE IF NOT EXISTS marketing.loyalty_position (
    leaderboard_nickname              text CONSTRAINT loyalty_position_leaderboard_nickname_chk CHECK (char_length(leaderboard_nickname) <= 24),
    subject_id                        uuid NOT NULL,
    programme_id                      uuid NOT NULL,
    points_balance                    integer NOT NULL,
    lifetime_points                   integer,
    tier_id                           uuid,
    tier_code                         text NOT NULL,
    tier_name                         text,
    points_to_next_tier               integer,
    next_expiry_points                integer,
    next_expiry_at                    timestamptz,
    id                                uuid PRIMARY KEY NOT NULL
);

-- The rules of earning and burning. Tiers are children
CREATE TABLE IF NOT EXISTS marketing.loyalty_programme (
    id                                uuid PRIMARY KEY NOT NULL,
    code                              text NOT NULL,
    name                              text NOT NULL,
    venue_id                          uuid,
    points_liability_account_id       uuid,
    points_expire_after_months        integer,
    is_active                         boolean
);

-- Holds 9 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS marketing.loyalty_rule (
    id                                uuid PRIMARY KEY,
    campaign_id                       uuid NOT NULL,
    type                              text NOT NULL CONSTRAINT loyalty_rule_type_chk CHECK (char_length(type) <= 30),
    points_earning_rule_id            uuid,
    reward_id                         uuid,
    bonus_points                      numeric(18,4),
    multiplier                        numeric(18,4),
    conditions_json                   text,
    is_active                         boolean NOT NULL
);

-- one row per recipient per send. Delivery, bounce and engagement Hangs off: reaches
-- marketing.guest_profile through its keys; references marketing.campaign. Reached by: 1
-- operations read it and 0 write it.
CREATE TABLE IF NOT EXISTS marketing.message_delivery (
    id                                uuid PRIMARY KEY NOT NULL,
    campaign_id                       uuid NOT NULL
);

-- One message to one person. Consent was checked here, which is why it is a row and not a log line
CREATE TABLE IF NOT EXISTS marketing.message_dispatch (
    id                                text PRIMARY KEY NOT NULL,
    subject_id                        uuid NOT NULL,
    campaign_id                       uuid,
    channel                           text NOT NULL CONSTRAINT message_dispatch_channel_chk CHECK (channel IN ('email', 'sms', 'whatsapp', 'push', 'inApp', 'post')),
    template_id                       uuid,
    message_trigger_id                uuid,
    status                            text NOT NULL CONSTRAINT message_dispatch_status_chk CHECK (status IN ('queued', 'sent', 'delivered', 'opened', 'clicked', 'bounced', 'failed', 'suppressed')),
    failure_reason                    text,
    provider_reference                text,
    queued_at                         timestamptz NOT NULL,
    delivered_at                      timestamptz,
    is_test                           boolean DEFAULT false,
    opened_at                         timestamptz,
    clicked_at                        timestamptz,
    complained_at                     timestamptz,
    unsubscribed_at                   timestamptz
);

-- Holds 15 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS marketing.message_dispatch_attempt (
    id                                uuid PRIMARY KEY NOT NULL,
    message_dispatch_id               text NOT NULL,
    attempt_number                    integer NOT NULL,
    communication_provider_id         uuid NOT NULL,
    channel                           text NOT NULL CONSTRAINT message_dispatch_attempt_channel_chk CHECK (channel IN ('email', 'sms', 'whatsapp', 'push', 'inApp', 'post')),
    is_fallback                       boolean DEFAULT false,
    outcome                           text NOT NULL CONSTRAINT message_dispatch_attempt_outcome_chk CHECK (outcome IN ('accepted', 'delivered', 'failed', 'rateLimited', 'timedOut')),
    failure_category                  text CONSTRAINT message_dispatch_attempt_failure_category_chk CHECK (failure_category IN ('providerUnavailable', 'invalidAddress', 'invalidMobile', 'rateLimited', 'authenticationError', 'templateRejected', 'timeout', 'consentBlock', 'unknownError')),
    failure_message                   text CONSTRAINT message_dispatch_attempt_failure_message_chk CHECK (char_length(failure_message) <= 1000),
    provider_reference                text,
    api_latency_ms                    integer,
    cost                              numeric(18,4),
    attempted_at                      timestamptz NOT NULL,
    delivered_at                      timestamptz,
    next_attempt_at                   timestamptz
);

-- Reusable content for a channel, with the variables a dispatch fills
CREATE TABLE IF NOT EXISTS marketing.message_template (
    id                                uuid PRIMARY KEY NOT NULL,
    code                              text NOT NULL CONSTRAINT message_template_code_chk CHECK (char_length(code) <= 64),
    name                              text NOT NULL CONSTRAINT message_template_name_chk CHECK (char_length(name) <= 200),
    channel                           text NOT NULL CONSTRAINT message_template_channel_chk CHECK (channel IN ('email', 'sms', 'whatsapp', 'push', 'inApp', 'post')),
    subjects                          jsonb,
    bodies                            jsonb NOT NULL,
    merge_fields                      text[],
    missing_languages                 text[],
    provider_template_id              text,
    brand_id                          uuid,
    ownership                         text DEFAULT 'crm' CONSTRAINT message_template_ownership_chk CHECK (ownership IN ('platform', 'crm')),
    tenant_id                         uuid NOT NULL
);

-- Holds 16 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS marketing.message_template_version (
    id                                uuid PRIMARY KEY NOT NULL,
    message_template_id               uuid NOT NULL,
    language                          text NOT NULL CONSTRAINT message_template_version_language_chk CHECK (char_length(language) <= 35),
    version                           integer NOT NULL,
    status                            text NOT NULL CONSTRAINT message_template_version_status_chk CHECK (status IN ('draft', 'published', 'archived')),
    subject                           text CONSTRAINT message_template_version_subject_chk CHECK (char_length(subject) <= 500),
    header                            text,
    body                              text,
    footer                            text,
    cta_label                         text CONSTRAINT message_template_version_cta_label_chk CHECK (char_length(cta_label) <= 100),
    cta_url                           text CONSTRAINT message_template_version_cta_url_chk CHECK (char_length(cta_url) <= 2000),
    attachment_kinds                  text[],
    variables                         text[],
    published_at                      timestamptz,
    published_by_principal_id         uuid,
    created_at                        timestamptz
);

-- What fires a message (BL-052). Before, during and after a visit are one mechanism with a
-- different sign on the offset
CREATE TABLE IF NOT EXISTS marketing.message_trigger (
    id                                uuid PRIMARY KEY NOT NULL,
    event                             text NOT NULL,
    template_id                       uuid NOT NULL,
    offset_minutes                    integer DEFAULT 0,
    anchor                            text DEFAULT 'eventTime' CONSTRAINT message_trigger_anchor_chk CHECK (anchor IN ('eventTime', 'performanceStart', 'visitEnd')),
    priority                          text DEFAULT 'transactional' CONSTRAINT message_trigger_priority_chk CHECK (priority IN ('operational', 'transactional', 'marketing')),
    is_active                         boolean NOT NULL DEFAULT true,
    scope_path                        ltree NOT NULL
);

-- Holds 6 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS marketing.message_trigger_condition (
    id                                uuid PRIMARY KEY NOT NULL,
    message_trigger_id                uuid NOT NULL,
    dimension                         text NOT NULL CONSTRAINT message_trigger_condition_dimension_chk CHECK (dimension IN ('product', 'event', 'venue', 'brand', 'customer', 'channel', 'time', 'transactionStatus', 'membership', 'bookingType')),
    operator                          text NOT NULL CONSTRAINT message_trigger_condition_operator_chk CHECK (operator IN ('equals', 'notEquals', 'in', 'withinMinutes', 'isValid', 'isPermitted')),
    value                             text CONSTRAINT message_trigger_condition_value_chk CHECK (char_length(value) <= 500),
    scope_path                        ltree NOT NULL
);

-- Holds 15 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS marketing.minor_privacy_rule (
    country                           text NOT NULL,
    minor_below_age                   integer NOT NULL,
    guardian_required_below_age       integer NOT NULL,
    age_verification_method           text NOT NULL CONSTRAINT minor_privacy_rule_age_verification_method_chk CHECK (age_verification_method IN ('selfDeclaredDateOfBirth', 'identityDocument', 'staffVerification', 'accountRecord')),
    guardian_verification_methods     text[] NOT NULL,
    guardian_data_required            text[],
    restrict_marketing                boolean DEFAULT true,
    restrict_tracking                 boolean DEFAULT true,
    restrict_personalisation          boolean DEFAULT true,
    restricted_processing_purpose_codes text[],
    consent_purposes_requiring_guardian text[],
    id                                uuid PRIMARY KEY NOT NULL,
    version                           integer,
    scope_path                        ltree NOT NULL,
    updated_at                        timestamptz
);

-- One level, with its threshold and benefits
CREATE TABLE IF NOT EXISTS marketing.points_earning_rule (
    loyalty_programme_id              uuid NOT NULL,
    trigger                           text NOT NULL,
    points                            numeric(18,4) NOT NULL,
    product_kinds                     text[],
    multiplier                        numeric(18,4),
    id                                uuid PRIMARY KEY NOT NULL
);

-- Holds 13 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS marketing.points_redemption_rule (
    id                                uuid PRIMARY KEY,
    loyalty_program_id                uuid NOT NULL,
    point_redemption_rule_code        text NOT NULL CONSTRAINT points_redemption_rule_point_redemption_rule_code_chk CHECK (char_length(point_redemption_rule_code) <= 100),
    name                              text NOT NULL CONSTRAINT points_redemption_rule_name_chk CHECK (char_length(name) <= 200),
    redemption_type                   text NOT NULL CONSTRAINT points_redemption_rule_redemption_type_chk CHECK (char_length(redemption_type) <= 30),
    required                          numeric(18,4),
    monetary_value                    numeric(18,4),
    minimum_points                    numeric(18,4),
    maximum_points                    numeric(18,4),
    product_id                        uuid,
    valid_from                        timestamptz,
    valid_to                          timestamptz,
    is_active                         boolean NOT NULL
);

-- Holds 16 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS marketing.privacy_action (
    action_id                         uuid,
    request_id                        uuid,
    retention_run_id                  uuid,
    subject_id                        uuid NOT NULL,
    action_type                       text NOT NULL CONSTRAINT privacy_action_action_type_chk CHECK (action_type IN ('delete', 'anonymise', 'pseudonymise', 'restrictProcessing', 'suppressMarketing', 'removeBiometricReference', 'disconnectThirdPartyProfile', 'other')),
    other_action_label                text CONSTRAINT privacy_action_other_action_label_chk CHECK (char_length(other_action_label) <= 100),
    requires_approval                 boolean,
    decision                          jsonb,
    status                            text CONSTRAINT privacy_action_status_chk CHECK (status IN ('planned', 'awaitingApproval', 'approved', 'rejected', 'executing', 'completed', 'completedWithRetention', 'failed', 'manualActionRequired', 'cancelled')),
    dsar_request_id                   text,
    evidence_asset_id                 uuid,
    created_at                        timestamptz,
    completed_at                      timestamptz,
    scope_path                        ltree NOT NULL,
    updated_at                        timestamptz,
    id                                uuid PRIMARY KEY NOT NULL
);

-- Holds 17 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS marketing.privacy_audit_event (
    event_id                          uuid NOT NULL,
    subject_id                        uuid,
    action                            text NOT NULL CONSTRAINT privacy_audit_event_action_chk CHECK (action IN ('consentGranted', 'consentWithdrawn', 'preferenceChanged', 'policyAccepted', 'privacyRequestCreated', 'identityVerified', 'dataExportGenerated', 'correctionRequested', 'deletionApproved', 'anonymisationExecuted', 'retentionAction', 'legalHold', 'administrativeOverride', 'configurationChange')),
    actor_type                        text CONSTRAINT privacy_audit_event_actor_type_chk CHECK (actor_type IN ('customer', 'guardian', 'staff', 'system', 'ai')),
    actor_principal_id                uuid,
    actor_role                        text,
    source                            text CONSTRAINT privacy_audit_event_source_chk CHECK (source IN ('core', 'ticketing', 'access', 'fnb', 'retail', 'inventory', 'seating', 'membership', 'marketing', 'resources', 'queue', 'transport', 'games', 'maintenance', 'accreditation', 'partner', 'developerApi', 'analytics', 'ai')),
    channel                           text,
    occurred_at                       timestamptz NOT NULL,
    before                            jsonb,
    after                             jsonb,
    reason                            text CONSTRAINT privacy_audit_event_reason_chk CHECK (char_length(reason) <= 1000),
    approval_reference                text,
    related_request_id                uuid,
    related_case_id                   uuid,
    evidence_reference                text,
    id                                uuid PRIMARY KEY NOT NULL
);

-- Holds 8 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS marketing.privacy_change_set (
    change_set_id                     uuid NOT NULL,
    status                            text NOT NULL CONSTRAINT privacy_change_set_status_chk CHECK (status IN ('draft', 'validated', 'submitted', 'approved', 'scheduled', 'published', 'rolledBack', 'rejected')),
    approval_request_id               text,
    publish_at                        timestamptz,
    published_at                      timestamptz,
    scope_path                        ltree NOT NULL,
    updated_at                        timestamptz,
    id                                uuid PRIMARY KEY NOT NULL
);

-- Holds 24 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS marketing.privacy_exception (
    id                                uuid PRIMARY KEY NOT NULL,
    category                          text NOT NULL CONSTRAINT privacy_exception_category_chk CHECK (category IN ('missingConsentEvidence', 'consentPropagationFailure', 'marketingAfterWithdrawal', 'policyVersionMismatch', 'missingGuardianConsent', 'retentionFailure', 'deletionFailure', 'unknownTrackingTechnology', 'unauthorisedDataAccess', 'unmappedProcessingPurpose', 'biometricPrivacyException', 'dataExportFailure', 'other')),
    severity                          text NOT NULL CONSTRAINT privacy_exception_severity_chk CHECK (severity IN ('low', 'medium', 'high', 'critical')),
    summary                           text NOT NULL CONSTRAINT privacy_exception_summary_chk CHECK (char_length(summary) <= 1000),
    subject_id                        uuid,
    system                            text CONSTRAINT privacy_exception_system_chk CHECK (system IN ('core', 'ticketing', 'access', 'fnb', 'retail', 'inventory', 'seating', 'membership', 'marketing', 'resources', 'queue', 'transport', 'games', 'maintenance', 'accreditation', 'partner', 'developerApi', 'analytics', 'ai')),
    brand_id                          uuid,
    country                           text,
    owner_principal_id                uuid,
    status                            text DEFAULT 'detected' CONSTRAINT privacy_exception_status_chk CHECK (status IN ('detected', 'triaged', 'assigned', 'investigated', 'correctiveAction', 'reviewed', 'closed')),
    related_evidence_ids              text[],
    policy_reference                  text CONSTRAINT privacy_exception_policy_reference_chk CHECK (char_length(policy_reference) <= 200),
    root_cause                        text CONSTRAINT privacy_exception_root_cause_chk CHECK (char_length(root_cause) <= 2000),
    corrective_action                 text CONSTRAINT privacy_exception_corrective_action_chk CHECK (char_length(corrective_action) <= 2000),
    notes                             text CONSTRAINT privacy_exception_notes_chk CHECK (char_length(notes) <= 4000),
    attachment_asset_ids              text[],
    escalated_to                      text CONSTRAINT privacy_exception_escalated_to_chk CHECK (escalated_to IN ('privacy', 'legal', 'security', 'it', 'marketing', 'operations', 'dataOwner')),
    privacy_incident_id               uuid,
    detected_at                       timestamptz NOT NULL,
    detected_by                       text CONSTRAINT privacy_exception_detected_by_chk CHECK (detected_by IN ('platformCheck', 'aiDetection', 'user')),
    sla_due_at                        timestamptz,
    closed_at                         timestamptz,
    scope_path                        ltree NOT NULL,
    updated_at                        timestamptz
);

-- Holds 7 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS marketing.privacy_export_package (
    sources                           text[],
    request_id                        uuid NOT NULL,
    discovered_at                     timestamptz,
    export_package                    jsonb,
    scope_path                        ltree NOT NULL,
    updated_at                        timestamptz,
    id                                uuid PRIMARY KEY NOT NULL
);

-- A personal-data breach (BL-176). UAE PDPL gives 72 hours from discovery — discoveredAt starts
-- the clock, and a discovery nobody recorded is a deadline nobody is counting
CREATE TABLE IF NOT EXISTS marketing.privacy_incident (
    id                                uuid PRIMARY KEY NOT NULL,
    discovered_at                     timestamptz NOT NULL,
    occurred_at                       timestamptz,
    severity                          text NOT NULL CONSTRAINT privacy_incident_severity_chk CHECK (severity IN ('low', 'medium', 'high', 'critical')),
    affected_subject_count            integer,
    data_categories                   text[],
    contained_at                      timestamptz,
    regulator_notified_at             timestamptz,
    subjects_notified_at              timestamptz,
    not_notified_rationale            text,
    status                            text NOT NULL CONSTRAINT privacy_incident_status_chk CHECK (status IN ('open', 'assessing', 'contained', 'notified', 'closed')),
    scope_path                        ltree NOT NULL
);

-- Holds 14 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS marketing.privacy_notice_governance (
    id                                uuid PRIMARY KEY NOT NULL,
    policy_id                         uuid NOT NULL,
    document_type                     text NOT NULL CONSTRAINT privacy_notice_governance_document_type_chk CHECK (document_type IN ('privacyPolicy', 'privacyNotice', 'cookieNotice', 'marketingNotice', 'biometricPrivacyNotice', 'childrensPrivacyNotice', 'locationServicesNotice', 'other')),
    status                            text NOT NULL DEFAULT 'draft' CONSTRAINT privacy_notice_governance_status_chk CHECK (status IN ('draft', 'review', 'approved', 'scheduled', 'published', 'superseded', 'archived')),
    change_classification             text CONSTRAINT privacy_notice_governance_change_classification_chk CHECK (change_classification IN ('minor', 'material')),
    requires_re_acceptance            boolean DEFAULT false,
    requires_notification             boolean DEFAULT false,
    owner_principal_id                uuid,
    approved_by_principal_id          uuid,
    approval_request_id               uuid,
    approved_at                       timestamptz,
    scope_path                        ltree NOT NULL,
    created_at                        timestamptz,
    updated_at                        timestamptz
);

-- Holds 29 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS marketing.privacy_request (
    request_id                        uuid,
    subject_id                        uuid NOT NULL,
    request_type                      text NOT NULL CONSTRAINT privacy_request_request_type_chk CHECK (char_length(request_type) <= 60),
    source                            text NOT NULL CONSTRAINT privacy_request_source_chk CHECK (source IN ('customerPortal', 'b2c', 'mobileApp', 'emailManual', 'customerService', 'pos', 'api')),
    requester_role                    text NOT NULL CONSTRAINT privacy_request_requester_role_chk CHECK (requester_role IN ('self', 'guardian', 'authorisedRepresentative')),
    requester_subject_id              uuid,
    jurisdiction                      text NOT NULL,
    submitted_at                      timestamptz,
    due_at                            timestamptz,
    is_deadline_configured            boolean,
    days_remaining                    integer,
    at_risk                           boolean,
    sla_state                         text CONSTRAINT privacy_request_sla_state_chk CHECK (sla_state IN ('onTrack', 'atRisk', 'overdue', 'escalated', 'noDeadline')),
    priority                          text DEFAULT 'P3' CONSTRAINT privacy_request_priority_chk CHECK (priority IN ('P1', 'P2', 'P3', 'P4')),
    owner_principal_id                uuid,
    verification_method               text CONSTRAINT privacy_request_verification_method_chk CHECK (verification_method IN ('accountLogin', 'otp', 'emailVerification', 'mobileVerification', 'idReview', 'manualVerification')),
    verification_status               text DEFAULT 'notStarted' CONSTRAINT privacy_request_verification_status_chk CHECK (verification_status IN ('notStarted', 'pending', 'verified', 'failed')),
    status                            text DEFAULT 'submitted' CONSTRAINT privacy_request_status_chk CHECK (status IN ('submitted', 'inProgress', 'completed')),
    stage                             text CONSTRAINT privacy_request_stage_chk CHECK (char_length(stage) <= 60),
    outcome                           text CONSTRAINT privacy_request_outcome_chk CHECK (outcome IN ('fulfilled', 'partiallyFulfilled', 'refused', 'withdrawnByRequester')),
    outcome_reason                    text CONSTRAINT privacy_request_outcome_reason_chk CHECK (char_length(outcome_reason) <= 1000),
    is_escalated                      boolean DEFAULT false,
    dsar_request_id                   text,
    case_id                           uuid,
    notes                             text CONSTRAINT privacy_request_notes_chk CHECK (char_length(notes) <= 4000),
    completed_at                      timestamptz,
    scope_path                        ltree NOT NULL,
    updated_at                        timestamptz,
    id                                uuid PRIMARY KEY NOT NULL
);

-- Holds 3 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS marketing.privacy_request_deadline (
    privacy_request_type_id           uuid NOT NULL,
    verification_method               text NOT NULL,
    id                                uuid PRIMARY KEY NOT NULL
);

-- Holds 8 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS marketing.privacy_request_type (
    id                                uuid PRIMARY KEY,
    code                              text NOT NULL CONSTRAINT privacy_request_type_code_chk CHECK (char_length(code) <= 60),
    name                              text NOT NULL CONSTRAINT privacy_request_type_name_chk CHECK (char_length(name) <= 150),
    kind                              text NOT NULL CONSTRAINT privacy_request_type_kind_chk CHECK (kind IN ('access', 'dataExport', 'correction', 'deletion', 'anonymisation', 'restriction', 'objection', 'consentWithdrawal', 'marketingOptOut', 'other')),
    allow_representatives             boolean DEFAULT true,
    status                            text NOT NULL DEFAULT 'active' CONSTRAINT privacy_request_type_status_chk CHECK (status IN ('active', 'retired')),
    scope_path                        ltree NOT NULL,
    updated_at                        timestamptz
);

-- Holds 26 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS marketing.processing_purpose (
    purpose_id                        uuid,
    purpose_code                      text NOT NULL CONSTRAINT processing_purpose_purpose_code_chk CHECK (char_length(purpose_code) <= 60),
    purpose_name                      text NOT NULL CONSTRAINT processing_purpose_purpose_name_chk CHECK (char_length(purpose_name) <= 150),
    description                       text CONSTRAINT processing_purpose_description_chk CHECK (char_length(description) <= 2000),
    business_owner                    text CONSTRAINT processing_purpose_business_owner_chk CHECK (char_length(business_owner) <= 150),
    data_controller_applicable_organization text CONSTRAINT processing_purpose_data_controller_applicable_organization_chk CHECK (char_length(data_controller_applicable_organization) <= 200),
    data_categories                   text[],
    data_subject_categories           text[],
    processing_activities             text[],
    systems_modules                   text[],
    countries_jurisdictions           text[],
    lawful_basis                      text NOT NULL DEFAULT 'unclassified' CONSTRAINT processing_purpose_lawful_basis_chk CHECK (lawful_basis IN ('consent', 'contractualNecessity', 'legalObligation', 'legitimateInterest', 'vitalInterest', 'publicInterest', 'other', 'unclassified')),
    lawful_basis_note                 text CONSTRAINT processing_purpose_lawful_basis_note_chk CHECK (char_length(lawful_basis_note) <= 500),
    sensitive_categories              text[],
    consent_purposes                  text[],
    policy_ids                        text[],
    capture_point_ids                 text[],
    retention_policy_codes            text[],
    third_party_processors            text[],
    effective_from                    timestamptz,
    effective_to                      timestamptz,
    status                            text NOT NULL DEFAULT 'draft' CONSTRAINT processing_purpose_status_chk CHECK (status IN ('draft', 'active', 'retired')),
    version                           integer,
    scope_path                        ltree NOT NULL,
    updated_at                        timestamptz,
    id                                uuid PRIMARY KEY NOT NULL
);

-- Holds 9 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS marketing.programme_tier (
    id                                uuid PRIMARY KEY,
    loyalty_programme_id              uuid NOT NULL,
    code                              text NOT NULL CONSTRAINT programme_tier_code_chk CHECK (char_length(code) <= 40),
    name                              text NOT NULL CONSTRAINT programme_tier_name_chk CHECK (char_length(name) <= 120),
    rank                              integer NOT NULL,
    min_lifetime_points               integer,
    retain_lifetime_points            integer,
    validity_months                   integer,
    benefits                          text[],
    earn_multiplier                   numeric(18,4),
    is_active                         boolean DEFAULT true
);

-- Holds 18 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS marketing.quality_evaluation (
    id                                uuid PRIMARY KEY NOT NULL,
    agent_principal_id                uuid NOT NULL,
    evaluator_principal_id            uuid,
    source_type                       text NOT NULL CONSTRAINT quality_evaluation_source_type_chk CHECK (source_type IN ('call', 'chat', 'email', 'whatsapp', 'case', 'complaint')),
    case_id                           text,
    conversation_id                   uuid,
    evaluated_by                      text NOT NULL CONSTRAINT quality_evaluation_evaluated_by_chk CHECK (evaluated_by IN ('human', 'ai')),
    status                            text NOT NULL CONSTRAINT quality_evaluation_status_chk CHECK (status IN ('draft', 'scored', 'acknowledged')),
    critical_failures                 text[],
    overall_score                     integer,
    feedback                          text CONSTRAINT quality_evaluation_feedback_chk CHECK (char_length(feedback) <= 2000),
    resolution_seconds                integer,
    sla_met                           boolean,
    agent_comment                     text CONSTRAINT quality_evaluation_agent_comment_chk CHECK (char_length(agent_comment) <= 1000),
    acknowledged_at                   timestamptz,
    evaluated_at                      timestamptz,
    scope_path                        ltree NOT NULL,
    updated_at                        timestamptz
);

-- A referral code and its reward (BL-034). The reward is conditional on the referred guest doing
-- something, not on the referral being sent
CREATE TABLE IF NOT EXISTS marketing.referral (
    id                                uuid PRIMARY KEY NOT NULL,
    referrer_subject_id               uuid NOT NULL,
    referee_subject_id                uuid,
    code                              text NOT NULL,
    status                            text NOT NULL CONSTRAINT referral_status_chk CHECK (status IN ('issued', 'registered', 'qualified', 'rewarded', 'expired', 'void')),
    qualifying_action                 text CONSTRAINT referral_qualifying_action_chk CHECK (qualifying_action IN ('firstPurchase', 'firstVisit', 'membershipPurchase')),
    referrer_reward_id                uuid,
    referee_reward_id                 uuid,
    expires_at                        timestamptz,
    scope_path                        ltree NOT NULL
);

-- Holds 13 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS marketing.retention_policy (
    id                                uuid PRIMARY KEY,
    code                              text NOT NULL,
    data_category                     text,
    jurisdictions                     text[],
    purposes                          text[],
    guest_status                      text[],
    retain_months                     integer,
    action                            text CONSTRAINT retention_policy_action_chk CHECK (action IN ('archive', 'anonymise', 'pseudonymise', 'delete')),
    is_legal_holds_respected          boolean DEFAULT true,
    fraud_exception_months            integer,
    is_approval_required              boolean DEFAULT true,
    schedule                          text,
    scope_path                        ltree NOT NULL
);

-- Holds 9 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS marketing.retention_run (
    id                                uuid PRIMARY KEY,
    policy_id                         uuid,
    mode                              text CONSTRAINT retention_run_mode_chk CHECK (mode IN ('preview', 'execute')),
    records_affected                  integer,
    by_action                         jsonb,
    held_back                         integer,
    held_back_reasons                 jsonb,
    evidence_asset_id                 uuid,
    completed_at                      timestamptz
);

-- What a guest said afterwards, with the venue’s response and whether it is public
CREATE TABLE IF NOT EXISTS marketing.review (
    id                                text PRIMARY KEY NOT NULL,
    subject_id                        uuid,
    venue_id                          uuid NOT NULL,
    related_order_id                  text,
    rating                            integer NOT NULL,
    body                              text CONSTRAINT review_body_chk CHECK (char_length(body) <= 5000),
    aspects                           text[],
    recorded_at                       timestamptz NOT NULL,
    status                            text NOT NULL CONSTRAINT review_status_chk CHECK (status IN ('pendingModeration', 'published', 'hidden', 'rejected')),
    response                          text,
    response_is_public                boolean,
    responded_by_principal_id         uuid,
    opened_case_id                    text
);

-- Holds 7 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS marketing.review_response (
    id                                uuid PRIMARY KEY,
    review_id                         uuid NOT NULL,
    text                              text NOT NULL CONSTRAINT review_response_text_chk CHECK (char_length(text) <= 2000),
    status                            text NOT NULL CONSTRAINT review_response_status_chk CHECK (char_length(status) <= 30),
    responded_by_principal_id         uuid,
    responded_at                      timestamptz NOT NULL,
    updated_at                        timestamptz
);

-- Holds 10 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS marketing.reward (
    id                                uuid PRIMARY KEY,
    loyalty_program_id                uuid NOT NULL,
    code                              text NOT NULL CONSTRAINT reward_code_chk CHECK (char_length(code) <= 100),
    name                              text NOT NULL CONSTRAINT reward_name_chk CHECK (char_length(name) <= 200),
    type                              text NOT NULL CONSTRAINT reward_type_chk CHECK (char_length(type) <= 30),
    product_id                        uuid,
    points_cost                       numeric(18,4),
    discount_value                    numeric(18,4),
    validity_days                     integer,
    is_active                         boolean NOT NULL
);

-- Holds 11 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS marketing.reward_assignment (
    id                                uuid PRIMARY KEY,
    customer_id                       uuid NOT NULL,
    reward_id                         uuid NOT NULL,
    code                              text NOT NULL CONSTRAINT reward_assignment_code_chk CHECK (char_length(code) <= 100),
    source_type                       text CONSTRAINT reward_assignment_source_type_chk CHECK (char_length(source_type) <= 30),
    source_reference_id               uuid,
    status                            text NOT NULL CONSTRAINT reward_assignment_status_chk CHECK (char_length(status) <= 30),
    issued_at                         timestamptz NOT NULL,
    expires_at                        timestamptz,
    redeemed_at                       timestamptz,
    redeemed_order_id                 uuid
);

-- A rule that selects an audience, evaluated rather than stored as a list
CREATE TABLE IF NOT EXISTS marketing.segment (
    name                              text NOT NULL CONSTRAINT segment_name_chk CHECK (char_length(name) <= 200),
    description                       text CONSTRAINT segment_description_chk CHECK (char_length(description) <= 1000),
    venue_id                          uuid,
    match                             text DEFAULT 'all' CONSTRAINT segment_match_chk CHECK (match IN ('all', 'any')),
    exclude_segment_ids               text[],
    id                                uuid PRIMARY KEY NOT NULL,
    last_evaluated_size               integer,
    last_evaluated_at                 timestamptz,
    created_at                        timestamptz NOT NULL
);

-- One condition in a segment rule. Hangs off: a child of marketing.segment; reaches
-- marketing.guest_profile through its keys; references marketing.segment. Reached by: 10
-- operations read it and 4 write it.
CREATE TABLE IF NOT EXISTS marketing.segment_criterion (
    segment_id                        uuid NOT NULL,
    attribute                         text NOT NULL,
    operator                          text NOT NULL CONSTRAINT segment_criterion_operator_chk CHECK (operator IN ('equals', 'notEquals', 'greaterThan', 'lessThan', 'between', 'in', 'notIn', 'exists', 'notExists', 'withinDays')),
    value                             text,
    values                            text[],
    id                                uuid PRIMARY KEY NOT NULL
);

-- Holds 22 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS marketing.sender_identity (
    id                                uuid PRIMARY KEY,
    scope_path                        ltree NOT NULL,
    channel                           text NOT NULL CONSTRAINT sender_identity_channel_chk CHECK (channel IN ('email', 'sms', 'whatsapp', 'push', 'inApp', 'post')),
    brand_id                          uuid NOT NULL,
    legal_entity_id                   uuid,
    region                            text,
    country                           text,
    provider_id                       uuid NOT NULL,
    sending_domain                    text CONSTRAINT sender_identity_sending_domain_chk CHECK (char_length(sending_domain) <= 253),
    from_name                         text CONSTRAINT sender_identity_from_name_chk CHECK (char_length(from_name) <= 120),
    from_address                      text,
    reply_to                          text,
    sender_id                         text CONSTRAINT sender_identity_sender_id_chk CHECK (char_length(sender_id) <= 15),
    approved_uses                     text[],
    business_account                  text,
    phone_number                      text,
    application                       text,
    platform                          text CONSTRAINT sender_identity_platform_chk CHECK (platform IN ('ios', 'android', 'web')),
    environment                       text CONSTRAINT sender_identity_environment_chk CHECK (environment IN ('production', 'sandbox')),
    status                            text NOT NULL CONSTRAINT sender_identity_status_chk CHECK (status IN ('pendingVerification', 'verified', 'active', 'suspended', 'expired')),
    approved_template_ids             text[],
    updated_at                        timestamptz
);

-- Holds 12 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS marketing.service_copilot_config (
    id                                uuid PRIMARY KEY,
    scope_level                       text NOT NULL CONSTRAINT service_copilot_config_scope_level_chk CHECK (scope_level IN ('tenant', 'venue')),
    scope_path                        ltree NOT NULL,
    is_enabled                        boolean DEFAULT false,
    data_sources                      text[] NOT NULL,
    knowledge_collection_ids          text[],
    draft_channels                    text[] NOT NULL,
    brand_tone                        text CONSTRAINT service_copilot_config_brand_tone_chk CHECK (char_length(brand_tone) <= 1000),
    reply_in_customer_language        boolean DEFAULT true,
    auto_send                         text[],
    pattern_detection                 jsonb,
    updated_at                        timestamptz
);

-- Holds 8 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS marketing.service_queue (
    id                                uuid PRIMARY KEY NOT NULL,
    code                              text NOT NULL CONSTRAINT service_queue_code_chk CHECK (char_length(code) <= 60),
    name                              text NOT NULL CONSTRAINT service_queue_name_chk CHECK (char_length(name) <= 150),
    overflow_wait_seconds             integer,
    is_active                         boolean NOT NULL DEFAULT true,
    scope_path                        ltree NOT NULL,
    created_at                        timestamptz,
    updated_at                        timestamptz
);

-- Holds 12 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS marketing.sla_policy (
    id                                uuid PRIMARY KEY,
    scope_path                        ltree NOT NULL,
    code                              text NOT NULL CONSTRAINT sla_policy_code_chk CHECK (char_length(code) <= 100),
    name                              text NOT NULL CONSTRAINT sla_policy_name_chk CHECK (char_length(name) <= 150),
    priority                          text CONSTRAINT sla_policy_priority_chk CHECK (char_length(priority) <= 20),
    first_response_minutes            integer,
    resolution_minutes                integer,
    escalation_minutes                integer,
    business_hours_only               boolean NOT NULL,
    is_active                         boolean NOT NULL,
    created_at                        timestamptz NOT NULL,
    updated_at                        timestamptz
);

-- Holds 8 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS marketing.subscription (
    id                                uuid PRIMARY KEY NOT NULL,
    subject_id                        uuid NOT NULL,
    channel                           text NOT NULL CONSTRAINT subscription_channel_chk CHECK (channel IN ('email', 'sms', 'push')),
    list_name                         text NOT NULL,
    is_subscribed                     boolean NOT NULL,
    source                            text,
    unsubscribe_token                 text,
    updated_at                        timestamptz
);

-- Who must not be contacted, whatever a campaign says
CREATE TABLE IF NOT EXISTS marketing.suppression (
    id                                uuid PRIMARY KEY,
    channel                           text NOT NULL CONSTRAINT suppression_channel_chk CHECK (channel IN ('email', 'sms', 'whatsapp', 'push', 'inApp', 'post')),
    address                           text NOT NULL,
    reason                            text NOT NULL,
    suppressed_at                     timestamptz NOT NULL,
    suppressed_by_principal_id        uuid,
    scope_path                        ltree NOT NULL
);

-- One marketing touch (BL-177). The platform records touches and does not pick an attribution
-- model — hard-coding one would make every other unanswerable
CREATE TABLE IF NOT EXISTS marketing.touch_point (
    id                                uuid PRIMARY KEY NOT NULL,
    subject_id                        uuid NOT NULL,
    campaign_id                       uuid,
    journey_id                        uuid,
    channel                           text NOT NULL,
    kind                              text CONSTRAINT touch_point_kind_chk CHECK (kind IN ('impression', 'open', 'click', 'visit', 'conversion')),
    occurred_at                       timestamptz NOT NULL,
    order_id                          text
);

-- Holds 23 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS marketing.tracking_technology (
    technology_id                     uuid,
    name                              text NOT NULL CONSTRAINT tracking_technology_name_chk CHECK (char_length(name) <= 200),
    provider                          text NOT NULL CONSTRAINT tracking_technology_provider_chk CHECK (char_length(provider) <= 150),
    domain_application                text CONSTRAINT tracking_technology_domain_application_chk CHECK (char_length(domain_application) <= 255),
    technology_type                   text NOT NULL CONSTRAINT tracking_technology_technology_type_chk CHECK (technology_type IN ('firstPartyCookie', 'thirdPartyCookie', 'mobileSdk', 'analyticsTracker', 'advertisingPixel', 'sessionTechnology', 'personalisationTechnology', 'embeddedService', 'other')),
    category                          text CONSTRAINT tracking_technology_category_chk CHECK (category IN ('strictlyNecessary', 'functional', 'analytics', 'personalisation', 'marketing', 'other')),
    other_category_label              text CONSTRAINT tracking_technology_other_category_label_chk CHECK (char_length(other_category_label) <= 80),
    purpose                           text CONSTRAINT tracking_technology_purpose_chk CHECK (char_length(purpose) <= 500),
    data_collected                    text CONSTRAINT tracking_technology_data_collected_chk CHECK (char_length(data_collected) <= 500),
    duration_days                     integer,
    is_third_party                    boolean NOT NULL,
    channels                          text[] NOT NULL,
    countries                         text[],
    processing_purpose_code           text,
    is_consent_required               boolean DEFAULT true,
    privacy_information               text CONSTRAINT tracking_technology_privacy_information_chk CHECK (char_length(privacy_information) <= 1000),
    source                            text DEFAULT 'manual' CONSTRAINT tracking_technology_source_chk CHECK (source IN ('manual', 'scan')),
    status                            text NOT NULL CONSTRAINT tracking_technology_status_chk CHECK (status IN ('detected', 'approved', 'blocked', 'retired')),
    first_detected_at                 timestamptz,
    last_seen_at                      timestamptz,
    scope_path                        ltree NOT NULL,
    updated_at                        timestamptz,
    id                                uuid PRIMARY KEY NOT NULL
);

-- Holds 15 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS marketing.waiver_association (
    id                                uuid PRIMARY KEY,
    form_id                           uuid NOT NULL,
    waiver_name                       text,
    target_type                       text NOT NULL CONSTRAINT waiver_association_target_type_chk CHECK (target_type IN ('global', 'brand', 'venue', 'product', 'ticketType', 'event', 'performance', 'attraction', 'activity', 'membership', 'camp', 'rental', 'resource', 'package', 'addOn')),
    target_id                         uuid,
    target_name                       text,
    requirement                       text NOT NULL CONSTRAINT waiver_association_requirement_chk CHECK (requirement IN ('mandatory', 'optional', 'conditional', 'informational')),
    condition_rule_id                 uuid,
    sequence                          integer DEFAULT 1,
    overrides_association_id          uuid,
    inherited_from                    jsonb,
    status                            text NOT NULL DEFAULT 'active' CONSTRAINT waiver_association_status_chk CHECK (status IN ('active', 'removed')),
    impact                            jsonb,
    scope_path                        ltree NOT NULL,
    updated_at                        timestamptz
);

-- Holds 19 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS marketing.waiver_exception (
    id                                uuid PRIMARY KEY,
    requirement_id                    uuid NOT NULL,
    reason_code                       text NOT NULL CONSTRAINT waiver_exception_reason_code_chk CHECK (reason_code IN ('guardianUnreachable', 'deviceOrConnectivityFailure', 'signedOnPaper', 'accessibilityNeed', 'operationalDecision', 'other')),
    reason                            text NOT NULL CONSTRAINT waiver_exception_reason_chk CHECK (char_length(reason) <= 1000),
    supporting_evidence_asset_ids     text[],
    supervisor_staff_id               uuid,
    status                            text NOT NULL DEFAULT 'requested' CONSTRAINT waiver_exception_status_chk CHECK (status IN ('requested', 'approved', 'rejected', 'revoked', 'expired')),
    scope                             text NOT NULL CONSTRAINT waiver_exception_scope_chk CHECK (scope IN ('oneTime', 'ticketSpecific', 'activitySpecific', 'timeLimited')),
    ticket_id                         text,
    performance_id                    uuid,
    valid_until                       timestamptz,
    decision_note                     text CONSTRAINT waiver_exception_decision_note_chk CHECK (char_length(decision_note) <= 1000),
    used_at                           timestamptz,
    requested_by                      uuid,
    requested_at                      timestamptz,
    decided_by                        uuid,
    decided_at                        timestamptz,
    scope_path                        ltree NOT NULL,
    updated_at                        timestamptz
);

-- Holds 5 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS marketing.waiver_field_rule (
    form_definition_field_id          uuid NOT NULL,
    subject                           text NOT NULL,
    operator                          text NOT NULL,
    value                             text,
    id                                uuid PRIMARY KEY NOT NULL
);

-- Holds 6 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS marketing.waiver_form_layout (
    form_id                           uuid NOT NULL,
    form_version                      integer NOT NULL,
    status                            text CONSTRAINT waiver_form_layout_status_chk CHECK (status IN ('draft', 'published', 'superseded', 'retired')),
    scope_path                        ltree NOT NULL,
    updated_at                        timestamptz,
    id                                uuid PRIMARY KEY NOT NULL
);

-- Holds 8 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS marketing.waiver_localisation (
    form_id                           uuid NOT NULL,
    form_version                      integer NOT NULL,
    source_language                   text NOT NULL CONSTRAINT waiver_localisation_source_language_chk CHECK (char_length(source_language) <= 10),
    branding                          jsonb,
    channels                          text[],
    scope_path                        ltree NOT NULL,
    updated_at                        timestamptz,
    id                                uuid PRIMARY KEY NOT NULL
);

-- Holds 26 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS marketing.waiver_master (
    waiver_id                         uuid NOT NULL,
    waiver_name                       text,
    internal_description              text CONSTRAINT waiver_master_internal_description_chk CHECK (char_length(internal_description) <= 2000),
    waiver_type                       text NOT NULL CONSTRAINT waiver_master_waiver_type_chk CHECK (waiver_type IN ('liabilityWaiver', 'parentGuardianConsent', 'participationConsent', 'medicalDeclaration', 'safetyAcknowledgement', 'mediaConsent', 'rentalAgreement', 'termsAcceptance', 'membershipDeclaration', 'customForm')),
    custom_type_label                 text CONSTRAINT waiver_master_custom_type_label_chk CHECK (char_length(custom_type_label) <= 80),
    owner_user_id                     uuid NOT NULL,
    department                        text CONSTRAINT waiver_master_department_chk CHECK (char_length(department) <= 100),
    brand_id                          uuid,
    legal_entity_id                   uuid,
    default_language                  text NOT NULL CONSTRAINT waiver_master_default_language_chk CHECK (char_length(default_language) <= 10),
    applicable_countries              text[],
    applicable_jurisdiction           text CONSTRAINT waiver_master_applicable_jurisdiction_chk CHECK (char_length(applicable_jurisdiction) <= 100),
    status                            text CONSTRAINT waiver_master_status_chk CHECK (status IN ('draft', 'review', 'pendingApproval', 'approved', 'scheduled', 'published', 'suspended', 'expired', 'archived')),
    template_source                   text NOT NULL DEFAULT 'createNew' CONSTRAINT waiver_master_template_source_chk CHECK (template_source IN ('createNew', 'duplicateExisting', 'masterTemplate', 'corporateTemplate')),
    source_waiver_id                  uuid,
    source_version                    integer,
    is_master_template                boolean DEFAULT false,
    business_owner_user_id            uuid NOT NULL,
    legal_reviewer_user_id            uuid,
    compliance_owner_user_id          uuid,
    operational_owner_user_id         uuid,
    is_legal_review_required          boolean DEFAULT true,
    usage                             jsonb,
    scope_path                        ltree NOT NULL,
    updated_at                        timestamptz,
    id                                uuid PRIMARY KEY NOT NULL
);

-- Holds 30 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS marketing.waiver_requirement (
    id                                uuid PRIMARY KEY NOT NULL,
    participant_subject_id            uuid NOT NULL,
    order_id                          text NOT NULL,
    order_line_id                     text,
    ticket_id                         text,
    product_id                        uuid,
    performance_id                    uuid,
    group_booking_id                  uuid,
    venue_id                          uuid,
    form_definition_id                uuid NOT NULL,
    form_version                      integer,
    is_mandatory                      boolean NOT NULL,
    status                            text NOT NULL DEFAULT 'assigned' CONSTRAINT waiver_requirement_status_chk CHECK (status IN ('notAssigned', 'assigned', 'sent', 'opened', 'inProgress', 'completed', 'verified', 'rejected', 'expired', 'superseded')),
    is_declined                       boolean DEFAULT false,
    signatory_subject_id              uuid,
    signatory_type                    text CONSTRAINT waiver_requirement_signatory_type_chk CHECK (signatory_type IN ('participant', 'guardian', 'organisationRepresentative')),
    delivery_channel                  text CONSTRAINT waiver_requirement_delivery_channel_chk CHECK (delivery_channel IN ('email', 'sms', 'whatsapp', 'push', 'inApp', 'qrCode', 'pos', 'kiosk', 'staffAssistedDevice', 'groupPortal')),
    link_use                          text DEFAULT 'singleUse' CONSTRAINT waiver_requirement_link_use_chk CHECK (link_use IN ('singleUse', 'multiUse')),
    link_authentication               text DEFAULT 'oneTimeCode' CONSTRAINT waiver_requirement_link_authentication_chk CHECK (link_authentication IN ('oneTimeCode', 'accountSignIn', 'bookingReference')),
    link_issued_at                    timestamptz,
    link_expires_at                   timestamptz,
    link_used_at                      timestamptz,
    last_sent_at                      timestamptz,
    next_reminder_at                  timestamptz,
    form_submission_id                uuid,
    completed_at                      timestamptz,
    owner_staff_id                    uuid,
    scope_path                        ltree NOT NULL,
    created_at                        timestamptz,
    updated_at                        timestamptz
);

-- Holds 10 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS marketing.waiver_requirement_event (
    id                                uuid PRIMARY KEY NOT NULL,
    waiver_requirement_id             uuid NOT NULL,
    event                             text NOT NULL CONSTRAINT waiver_requirement_event_event_chk CHECK (event IN ('linkIssued', 'linkSent', 'reminderSent', 'qrGenerated', 'deliveryFailed', 'linkOpened', 'linkExpired', 'participantIdentified', 'guardianInformationCompleted', 'questionsCompleted', 'acknowledgementsAccepted', 'signatureSubmitted', 'validationPassed', 'validationFailed', 'evidenceStored', 'markedComplete', 'verified', 'rejected', 'correctionRequested', 'resignRequested', 'versionAssigned', 'signatoryReplaced', 'ownerAssigned', 'groupLeaderNotified', 'exceptionApproved', 'evidenceViewed')),
    actor                             text NOT NULL CONSTRAINT waiver_requirement_event_actor_chk CHECK (actor IN ('participant', 'guardian', 'staff', 'system')),
    staff_id                          uuid,
    channel                           text,
    message_dispatch_id               text,
    reason                            text CONSTRAINT waiver_requirement_event_reason_chk CHECK (char_length(reason) <= 500),
    occurred_at                       timestamptz NOT NULL,
    scope_path                        ltree NOT NULL
);

-- Holds 20 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS marketing.waiver_signatory_rule (
    form_id                           uuid NOT NULL,
    form_version                      integer NOT NULL,
    primary_signatory                 text NOT NULL CONSTRAINT waiver_signatory_rule_primary_signatory_chk CHECK (primary_signatory IN ('ticketHolder', 'purchaser', 'participant', 'parent', 'legalGuardian', 'groupLeader', 'corporateRepresentative', 'member', 'rentalCustomer', 'otherAuthorizedSignatory')),
    allowed_signatories               text[],
    co_signature                      text CONSTRAINT waiver_signatory_rule_co_signature_chk CHECK (co_signature IN ('participantAndGuardian', 'customerAndAuthorizedRepresentative')),
    is_signature_required             boolean DEFAULT true,
    is_initials_required              boolean DEFAULT false,
    acceptance_method                 text NOT NULL CONSTRAINT waiver_signatory_rule_acceptance_method_chk CHECK (acceptance_method IN ('drawnSignature', 'typedName', 'checkbox')),
    capture_relationship              boolean DEFAULT true,
    identity_verification             text DEFAULT 'none' CONSTRAINT waiver_signatory_rule_identity_verification_chk CHECK (identity_verification IN ('none', 'signedInAccount', 'oneTimeCode', 'idDocumentCheck')),
    requires_guardian_for_minors      boolean NOT NULL,
    guardian_threshold_age            integer,
    guardian_signs_for_each_minor     boolean DEFAULT true,
    group_signing_modes               text[],
    recorded_evidence                 text[],
    legal_approved_by                 text,
    legal_approved_at                 timestamptz,
    scope_path                        ltree NOT NULL,
    updated_at                        timestamptz,
    id                                uuid PRIMARY KEY NOT NULL
);

-- Holds 20 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS marketing.waiver_signatory_rule (guardian threshold and flag on marketing.form_definition) (
    id                                uuid PRIMARY KEY NOT NULL,
    form_id                           uuid NOT NULL,
    form_version                      integer NOT NULL,
    primary_signatory                 text NOT NULL CONSTRAINT waiver_signatory_rule (guardian threshold and flag_9fcc822f_chk CHECK (primary_signatory IN ('ticketHolder', 'purchaser', 'participant', 'parent', 'legalGuardian', 'groupLeader', 'corporateRepresentative', 'member', 'rentalCustomer', 'otherAuthorizedSignatory')),
    allowed_signatories               text[],
    co_signature                      text CONSTRAINT waiver_signatory_rule (guardian threshold and flag_a1241dcb_chk CHECK (co_signature IN ('participantAndGuardian', 'customerAndAuthorizedRepresentative')),
    is_signature_required             boolean DEFAULT true,
    is_initials_required              boolean DEFAULT false,
    acceptance_method                 text NOT NULL CONSTRAINT waiver_signatory_rule (guardian threshold and flag_b0814a86_chk CHECK (acceptance_method IN ('drawnSignature', 'typedName', 'checkbox')),
    capture_relationship              boolean DEFAULT true,
    identity_verification             text DEFAULT 'none' CONSTRAINT waiver_signatory_rule (guardian threshold and flag_318dfe24_chk CHECK (identity_verification IN ('none', 'signedInAccount', 'oneTimeCode', 'idDocumentCheck')),
    requires_guardian_for_minors      boolean NOT NULL,
    guardian_threshold_age            integer,
    guardian_signs_for_each_minor     boolean DEFAULT true,
    group_signing_modes               text[],
    recorded_evidence                 text[],
    legal_approved_by                 text,
    legal_approved_at                 timestamptz,
    scope_path                        ltree NOT NULL,
    updated_at                        timestamptz
);

-- Holds 15 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS marketing.waiver_signature (
    id                                uuid PRIMARY KEY,
    template_id                       uuid NOT NULL,
    customer_id                       uuid,
    subject_name                      text NOT NULL CONSTRAINT waiver_signature_subject_name_chk CHECK (char_length(subject_name) <= 200),
    signed_name                       text NOT NULL CONSTRAINT waiver_signature_signed_name_chk CHECK (char_length(signed_name) <= 200),
    signer_type                       text NOT NULL CONSTRAINT waiver_signature_signer_type_chk CHECK (char_length(signer_type) <= 20),
    guardian_name                     text CONSTRAINT waiver_signature_guardian_name_chk CHECK (char_length(guardian_name) <= 200),
    source_type                       text CONSTRAINT waiver_signature_source_type_chk CHECK (char_length(source_type) <= 30),
    source_reference_id               uuid,
    data_reference                    text CONSTRAINT waiver_signature_data_reference_chk CHECK (char_length(data_reference) <= 1000),
    document_hash                     text NOT NULL CONSTRAINT waiver_signature_document_hash_chk CHECK (char_length(document_hash) <= 128),
    ip_address                        text CONSTRAINT waiver_signature_ip_address_chk CHECK (char_length(ip_address) <= 64),
    device_info                       text CONSTRAINT waiver_signature_device_info_chk CHECK (char_length(device_info) <= 500),
    status                            text NOT NULL CONSTRAINT waiver_signature_status_chk CHECK (char_length(status) <= 20),
    signed_at                         timestamptz NOT NULL
);

-- Holds 10 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS marketing.waiver_trigger_rule (
    id                                uuid PRIMARY KEY,
    form_id                           uuid NOT NULL,
    name                              text NOT NULL CONSTRAINT waiver_trigger_rule_name_chk CHECK (char_length(name) <= 150),
    trigger_point                     text NOT NULL CONSTRAINT waiver_trigger_rule_trigger_point_chk CHECK (trigger_point IN ('duringCheckout', 'afterPurchase', 'beforeTicketIssuance', 'beforeTicketDownload', 'beforeEvent', 'beforeCheckIn', 'beforeAccess', 'beforeEquipmentCollection', 'beforeMembershipActivation', 'beforeActivityStart')),
    completion_deadline               jsonb NOT NULL,
    enforcement                       text[],
    allow_staff_override              boolean DEFAULT false,
    status                            text NOT NULL DEFAULT 'active' CONSTRAINT waiver_trigger_rule_status_chk CHECK (status IN ('active', 'inactive')),
    scope_path                        ltree NOT NULL,
    updated_at                        timestamptz
);

-- Holds 14 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS marketing.waiver_verification (
    id                                uuid PRIMARY KEY,
    submission_id                     uuid NOT NULL,
    result                            text NOT NULL CONSTRAINT waiver_verification_result_chk CHECK (result IN ('verified', 'rejected', 'correctionRequired', 'escalated')),
    participant_match                 boolean,
    booking_match                     boolean,
    guardian_relationship_present     boolean,
    required_evidence_present         boolean,
    reason_code                       text CONSTRAINT waiver_verification_reason_code_chk CHECK (reason_code IN ('signatoryNotAuthorised', 'participantMismatch', 'wrongVersion', 'incompleteAnswers', 'evidenceMissing', 'suspectedFraud', 'other')),
    note                              text CONSTRAINT waiver_verification_note_chk CHECK (char_length(note) <= 2000),
    escalated_to                      uuid,
    reviewed_by                       uuid,
    reviewed_at                       timestamptz,
    scope_path                        ltree NOT NULL,
    updated_at                        timestamptz
);

-- Holds 15 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS marketing.waiver_version_control (
    form_id                           uuid NOT NULL,
    form_version                      integer NOT NULL,
    lifecycle_status                  text NOT NULL CONSTRAINT waiver_version_control_lifecycle_status_chk CHECK (lifecycle_status IN ('draft', 'review', 'pendingApproval', 'approved', 'scheduled', 'published', 'suspended', 'expired', 'archived')),
    simulation                        jsonb,
    change_reason                     text,
    effective_from                    timestamptz,
    effective_to                      timestamptz,
    resign_rule                       text CONSTRAINT waiver_version_control_resign_rule_chk CHECK (resign_rule IN ('noResign', 'resignAtNextBooking', 'resignBeforeNextVisit')),
    publication                       jsonb,
    is_suspended                      boolean DEFAULT false,
    suspension_reason                 text,
    audit                             jsonb,
    scope_path                        ltree NOT NULL,
    updated_at                        timestamptz,
    id                                uuid PRIMARY KEY NOT NULL
);

-- Holds 15 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS marketing.waiver_version_control (checklist, simulation and aiFindings computed at read time) (
    id                                uuid PRIMARY KEY NOT NULL,
    form_id                           uuid NOT NULL,
    form_version                      integer NOT NULL,
    lifecycle_status                  text NOT NULL CONSTRAINT waiver_version_control (checklist, simulation and _1766f151_chk CHECK (lifecycle_status IN ('draft', 'review', 'pendingApproval', 'approved', 'scheduled', 'published', 'suspended', 'expired', 'archived')),
    simulation                        jsonb,
    change_reason                     text,
    effective_from                    timestamptz,
    effective_to                      timestamptz,
    resign_rule                       text CONSTRAINT waiver_version_control (checklist, simulation and _ef43c00a_chk CHECK (resign_rule IN ('noResign', 'resignAtNextBooking', 'resignBeforeNextVisit')),
    publication                       jsonb,
    is_suspended                      boolean DEFAULT false,
    suspension_reason                 text,
    audit                             jsonb,
    scope_path                        ltree NOT NULL,
    updated_at                        timestamptz
);

-- Something a guest saved. Per guest, synced across their devices
CREATE TABLE IF NOT EXISTS marketing.wishlist_item (
    subject_id                        uuid NOT NULL,
    id                                uuid PRIMARY KEY NOT NULL,
    variant_id                        uuid NOT NULL,
    product_name                      text,
    performance_id                    uuid,
    performance_starts_at             timestamptz,
    price                             text,
    image_asset_ref                   text,
    is_available                      boolean NOT NULL,
    unavailable_reason                text,
    note                              text,
    added_at                          timestamptz NOT NULL
);

