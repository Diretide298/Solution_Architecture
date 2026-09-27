-- marketing — 70 tables
-- **Derived. Do not hand-edit.**

-- Available, busy, away or offline, with a concurrency limit. Expires — an agent who forgets to go
-- offline is one conversations queue for Hangs off: reaches marketing.guest_profile through its
-- keys; references identity.principal. Reached by: 3 operations read it and 1 write it.
CREATE TABLE IF NOT EXISTS marketing.agent_availability (
    id                                uuid PRIMARY KEY,
    principal_id                      uuid NOT NULL,
    state                             text NOT NULL CONSTRAINT agent_availability_state_chk CHECK (state IN ('available', 'busy', 'away', 'offline')),
    max_concurrent                    integer,
    queue_ids                         text[],
    expires_at                        timestamptz,
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

-- A challenge, mission or streak (22.6, CF-137). Gamification is not loyalty — loyalty pays for
-- spend, a challenge pays for behaviour spend does not produce
CREATE TABLE IF NOT EXISTS marketing.challenge (
    id                                uuid PRIMARY KEY NOT NULL,
    name                              text NOT NULL,
    kind                              text NOT NULL CONSTRAINT challenge_kind_chk CHECK (kind IN ('visit', 'spend', 'ride', 'collection', 'streak', 'referral', 'survey', 'social', 'milestone')),
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

-- A live session with somebody waiting. Not a case — a case is a ticket measured in hours, this is
-- measured in seconds. A conversation may create a case; it is not one Hangs off: reaches
-- marketing.guest_profile through its keys; references identity.principal, marketing.case,
-- marketing.kiosk_assist_session. Reached by: 8 operations read it and 6 write it; 1 tables
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
-- ai.activity, identity.principal, marketing.conversation. Reached by: 7 operations read it and 1
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
    form_definition_id                uuid NOT NULL,
    key                               text NOT NULL,
    label                             text NOT NULL,
    label_localised                   jsonb,
    type                              text NOT NULL,
    options                           text[],
    is_required                       boolean,
    is_personal_data                  boolean,
    consent_purpose_id                uuid,
    show_when                         jsonb,
    id                                uuid PRIMARY KEY NOT NULL
);

-- The acceptance record, and it is evidence (2.15.13). Bound to the version accepted, not to the
-- form. Hangs off: reaches marketing.guest_profile through its keys; references
-- assets.media_asset, pii.subject. Reached by: 3 operations read it and 1 write it.
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
-- platform.scope. Reached by: 2 operations read it and 2 write it; 1 tables reference it.
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
    reason                            text CONSTRAINT loyalty_points_reason_chk CHECK (reason IN ('correction', 'goodwill', 'serviceRecovery', 'fraudReversal', 'expiryAdjustment', 'migration')),
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
    tenant_id                         uuid NOT NULL
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
-- marketing.guest_profile through its keys; references marketing.segment. Reached by: 9 operations
-- read it and 4 write it.
CREATE TABLE IF NOT EXISTS marketing.segment_criterion (
    segment_id                        uuid NOT NULL,
    attribute                         text NOT NULL,
    operator                          text NOT NULL CONSTRAINT segment_criterion_operator_chk CHECK (operator IN ('equals', 'notEquals', 'greaterThan', 'lessThan', 'between', 'in', 'notIn', 'exists', 'notExists', 'withinDays')),
    value                             text,
    values                            text[],
    id                                uuid PRIMARY KEY NOT NULL
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

