-- marketing — 45 tables
-- **Derived. Do not hand-edit.**

-- Available, busy, away or offline, with a concurrency limit. Expires — an agent who forgets to go
-- offline is one conversations queue for Hangs off: reaches marketing.guest_profile through its
-- keys; references identity.principal. Reached by: 2 operations read it and 1 write it.
CREATE TABLE IF NOT EXISTS marketing.agent_availability (
    id                                uuid PRIMARY KEY NOT NULL,
    principal_id                      uuid NOT NULL
);

-- Every marketing touch, not just the converting one (BL-177). A platform storing only its chosen
-- attribution model cannot answer a question asked in a different one. Hangs off: reaches
-- marketing.guest_profile through its keys; references marketing.campaign, marketing.journey,
-- pii.subject. Reached by: 2 operations read it and 0 write it.
CREATE TABLE IF NOT EXISTS marketing.attribution_touch (
    id                                uuid PRIMARY KEY NOT NULL,
    subject_id                        uuid NOT NULL,
    campaign_id                       uuid NOT NULL,
    journey_id                        uuid,
    touched_at                        timestamptz NOT NULL,
    channel                           text NOT NULL,
    interaction                       text,
    order_id                          uuid
);

-- Holds 16 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS marketing.audience_activation (
    id                                uuid PRIMARY KEY,
    segment_id                        uuid NOT NULL,
    destination                       text NOT NULL,
    destination_reference             text,
    external                          boolean,
    suppression_list_ids              text[],
    enforce_consent                   boolean,
    frequency_cap_per_week            integer,
    refresh_schedule                  text,
    expires_at                        date,
    pre_flight                        jsonb,
    approval_request_id               uuid,
    status                            text,
    last_synced_at                    timestamptz,
    last_sync_errors                  integer,
    scope_path                        text
);

-- Holds 17 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS marketing.audience_list (
    id                                uuid PRIMARY KEY,
    name                              text NOT NULL,
    kind                              text,
    asset_id                          uuid,
    field_mapping                     jsonb,
    rows_read                         integer,
    matched                           integer,
    unmatched                         integer,
    duplicates_removed                integer,
    rejected                          integer,
    unmatched_handling                text,
    source                            text,
    owner                             uuid,
    purpose                           text,
    consent_basis                     text,
    expires_at                        date,
    scope_path                        text
);

-- A send with an audience and a schedule. Every dispatch it produces is a message_dispatch row,
-- which is where consent was checked
CREATE TABLE IF NOT EXISTS marketing.campaign (
    name                              text,
    kind                              text,
    channel                           text,
    venue_id                          uuid,
    segment_id                        uuid,
    content                           jsonb,
    trigger                           jsonb,
    scheduled_for                     timestamptz,
    consent_purpose                   text,
    send_window                       jsonb,
    id                                uuid PRIMARY KEY,
    budget_cap                        numeric(18,4),
    budget_spent                      numeric(18,4),
    status                            text,
    is_paused                         boolean,
    created_by_principal_id           uuid,
    created_at                        timestamptz,
    launched_at                       timestamptz,
    completed_at                      timestamptz,
    performance                       jsonb
);

-- A guest problem with a lifecycle — raised, assigned, answered, closed. The messages are
-- children; the SLA is not yet modelled
CREATE TABLE IF NOT EXISTS marketing."case" (
    id                                text PRIMARY KEY,
    case_number                       text,
    subject_id                        uuid,
    guest_name                        text,
    subject                           text,
    category_id                       uuid,
    status                            text,
    priority                          text,
    assigned_to_principal_id          uuid,
    venue_id                          uuid,
    related_order_id                  text,
    sla_due_at                        timestamptz,
    is_sla_breached                   boolean,
    sla_paused_seconds                integer,
    escalation_count                  integer,
    created_at                        timestamptz,
    resolved_at                       timestamptz,
    description                       text,
    resolution_note                   text
);

-- One exchange in a case, from either side
CREATE TABLE IF NOT EXISTS marketing.case_message (
    id                                text PRIMARY KEY NOT NULL,
    body                              text NOT NULL,
    is_internal                       boolean NOT NULL,
    author_kind                       text NOT NULL,
    author_principal_id               uuid,
    channel                           text,
    attachment_refs                   text[],
    recorded_at                       timestamptz NOT NULL,
    case_id                           text
);

-- A challenge, mission or streak (22.6, CF-137). Gamification is not loyalty — loyalty pays for
-- spend, a challenge pays for behaviour spend does not produce
CREATE TABLE IF NOT EXISTS marketing.challenge (
    id                                uuid PRIMARY KEY NOT NULL,
    name                              text NOT NULL,
    kind                              text NOT NULL,
    scope                             text,
    goal                              jsonb NOT NULL,
    event_id                          uuid,
    reward_kind                       text,
    reward_value                      numeric(18,4),
    badge_asset_id                    uuid,
    starts_at                         timestamptz,
    ends_at                           timestamptz,
    status                            text NOT NULL,
    scope_path                        text
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
    purpose                           text NOT NULL,
    display_name                      text,
    description                       text,
    notice_version                    text NOT NULL,
    is_required_for_service           boolean NOT NULL,
    expires_after_months              integer,
    id                                uuid PRIMARY KEY NOT NULL,
    tenant_id                         uuid NOT NULL
);

-- What a guest agreed to and when. A merge takes the narrower of two (CF-160)
CREATE TABLE IF NOT EXISTS marketing.consent_record (
    purpose                           text,
    decision                          text,
    notice_version                    text,
    source                            text,
    recorded_at                       timestamptz,
    id                                text PRIMARY KEY,
    subject_id                        uuid,
    recorded_by_principal_id          uuid,
    superseded_at                     timestamptz
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
    channel                           text NOT NULL,
    state                             text NOT NULL,
    subject_id                        uuid,
    venue_id                          uuid,
    assigned_principal_id             uuid,
    queue_id                          uuid,
    queue_position                    integer,
    estimated_wait_seconds            integer,
    handover_reason                   text,
    handover_summary                  text,
    sentiment                         text,
    intent                            text,
    locale                            text,
    case_id                           text,
    first_response_seconds            integer,
    started_at                        timestamptz,
    closed_at                         timestamptz,
    outcome                           text
);

-- One message. The sender is resolved, never declared, and the assistant is labelled as one — a
-- guest talking to a bot that presents as a person is a complaint waiting to happen Hangs off: a
-- child of marketing.conversation; reaches marketing.guest_profile through its keys; references
-- ai.interaction, identity.principal, marketing.conversation. Reached by: 1 operations read it and
-- 1 write it.
CREATE TABLE IF NOT EXISTS marketing.conversation_message (
    id                                uuid PRIMARY KEY NOT NULL,
    sender                            text NOT NULL,
    sender_principal_id               uuid,
    body                              text NOT NULL,
    ai_interaction_id                 uuid,
    sent_at                           timestamptz NOT NULL,
    read_at                           timestamptz,
    conversation_id                   uuid NOT NULL
);

-- Holds 10 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS marketing.duplicate_candidate (
    id                                uuid PRIMARY KEY,
    guest_ids                         text[],
    score                             numeric(18,4),
    band                              text,
    matched_on                        text[],
    linked_record_counts              jsonb,
    status                            text,
    decided_by                        uuid,
    decided_at                        timestamptz,
    scope_path                        text
);

-- A waiver, survey or capture form (CF-129). One mechanism, three uses — three implementations
-- would drift on the version rule first
CREATE TABLE IF NOT EXISTS marketing.form_definition (
    id                                uuid PRIMARY KEY NOT NULL,
    name                              text NOT NULL,
    kind                              text NOT NULL,
    version                           integer NOT NULL,
    requires_signature                boolean,
    signature_kind                    text,
    score_scale                       text,
    applies_to_product_ids            text[],
    valid_for_months                  integer,
    minimum_age                       integer,
    requires_guardian_for_minors      boolean,
    status                            text NOT NULL,
    legal_reviewed_by                 text,
    legal_reviewed_at                 timestamptz,
    scope_path                        text
);

-- The acceptance record, and it is evidence (2.15.13). Bound to the version accepted, not to the
-- form. Hangs off: reaches marketing.guest_profile through its keys; references maintenance.asset,
-- pii.subject. Reached by: 2 operations read it and 1 write it.
CREATE TABLE IF NOT EXISTS marketing.form_submission (
    id                                uuid PRIMARY KEY NOT NULL,
    form_id                           uuid NOT NULL,
    form_version                      integer NOT NULL,
    subject_id                        uuid NOT NULL,
    on_behalf_of_subject_id           uuid,
    answers                           jsonb,
    signature_asset_id                uuid,
    submitted_at                      timestamptz NOT NULL,
    expires_at                        timestamptz,
    captured_at_channel               text,
    ip_address                        text
);

-- Holds 4 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS marketing.guest_attribute_model (
    version                           integer,
    published_at                      timestamptz,
    scope_path                        text,
    id                                uuid PRIMARY KEY NOT NULL
);

-- A phone or browser a guest has registered. How they revoke an old one that still holds tickets
CREATE TABLE IF NOT EXISTS marketing.guest_device (
    id                                uuid PRIMARY KEY NOT NULL,
    subject_id                        uuid NOT NULL,
    platform                          text NOT NULL,
    token_fingerprint                 text,
    app_version                       text,
    os_version                        text,
    device_model                      text,
    locale                            text,
    status                            text NOT NULL,
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
    kind                              text NOT NULL,
    storage_ref                       text NOT NULL,
    content_type                      text,
    consent_purpose_id                uuid,
    retain_until                      date,
    uploaded_at                       timestamptz,
    uploaded_by_principal_id          uuid
);

-- What a venue knows about a guest that is not their identity — preferences, lifetime value,
-- segments, consent. Twenty operations touch it and it references pii.subject rather than
-- duplicating it
CREATE TABLE IF NOT EXISTS marketing.guest_profile (
    id                                uuid PRIMARY KEY,
    subject_id                        uuid,
    display_name                      text,
    email                             text,
    phone                             text,
    preferred_language                text,
    preferred_channel                 text,
    guest_link_id                     text,
    tags                              text[],
    engagement_score                  integer,
    engagement_tier                   text,
    lifetime_value                    numeric(18,4),
    visit_count                       integer,
    last_visit_at                     timestamptz,
    is_active                         boolean,
    consents                          jsonb,
    loyalty                           uuid,
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
    related_guest_id                  uuid NOT NULL,
    organisation_id                   uuid,
    kind                              text NOT NULL,
    authorities                       text[],
    effective_from                    date,
    effective_to                      date,
    shared_benefits                   boolean,
    verified_at                       timestamptz,
    scope_path                        text
);

-- Holds 7 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS marketing.identity_rules (
    match_threshold                   numeric(18,4),
    possible_match_threshold          numeric(18,4),
    excluded_sources                  text[],
    jurisdiction_restrictions         text[],
    auto_merge_allowed                boolean,
    scope_path                        text,
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
    scope_path                        text
);

-- A quota-bounded addressed invitation (BL-150). A campaign broadcasts; an invitation expects a
-- response. quota is places and overInvitePercent is invitations
CREATE TABLE IF NOT EXISTS marketing.invitation_campaign (
    id                                uuid PRIMARY KEY NOT NULL,
    name                              text NOT NULL,
    event_id                          uuid,
    product_id                        uuid,
    quota                             integer NOT NULL,
    over_invite_percent               numeric(18,4),
    issued_count                      integer,
    accepted_count                    integer,
    respond_by_at                     timestamptz,
    status                            text NOT NULL,
    scope_path                        text
);

-- An automated multi-step journey (22.3.1b–22.3.10b, CF-137). A MessageTrigger is one step of it —
-- a journey is what you need when the next message depends on what the guest did about the last
CREATE TABLE IF NOT EXISTS marketing.journey (
    id                                uuid PRIMARY KEY NOT NULL,
    name                              text NOT NULL,
    template_kind                     text,
    entry_event                       text NOT NULL,
    entry_conditions                  jsonb,
    status                            text NOT NULL,
    max_duration_days                 integer,
    reentry_policy                    text,
    scope_path                        text
);

-- A guest inside a journey, at a step. Pausing does not evict them, because a half-finished
-- recovery sequence that restarts sends the first message twice
CREATE TABLE IF NOT EXISTS marketing.journey_entrant (
    id                                uuid PRIMARY KEY NOT NULL,
    journey_id                        uuid NOT NULL,
    subject_id                        uuid NOT NULL,
    step_id                           uuid NOT NULL,
    status                            text,
    entered_at                        timestamptz,
    step_entered_at                   timestamptz,
    next_action_at                    timestamptz,
    exited_at                         timestamptz,
    scope_path                        text
);

-- A staff member acting on a kiosk session remotely (2.1.25). The guest can always see it and
-- always end it — assistance a guest cannot stop is surveillance Hangs off: reaches
-- marketing.guest_profile through its keys; references identity.principal, orders.cart,
-- platform.device. Reached by: 1 operations read it and 2 write it; 1 tables reference it.
CREATE TABLE IF NOT EXISTS marketing.kiosk_assist_session (
    id                                uuid PRIMARY KEY NOT NULL,
    device_id                         uuid NOT NULL,
    venue_id                          uuid,
    staff_principal_id                uuid NOT NULL,
    staff_display_name                text,
    cart_id                           uuid,
    reason                            text,
    ended_by                          text,
    started_at                        timestamptz NOT NULL,
    ended_at                          timestamptz
);

-- A reported or found item (BL-021). The match between the two is the whole capability — without
-- both sides modelled, somebody searches a case list by hand
CREATE TABLE IF NOT EXISTS marketing.lost_item (
    id                                uuid PRIMARY KEY NOT NULL,
    found_or_lost                     text NOT NULL,
    kind                              text NOT NULL,
    description                       text,
    colour                            text,
    brand                             text,
    venue_id                          uuid NOT NULL,
    last_seen_point_id                uuid,
    reported_at                       timestamptz NOT NULL,
    reported_by_subject_id            uuid,
    storage_location                  text,
    status                            text,
    photo_asset_ids                   text[],
    dispose_after                     date
);

-- Where a guest stands — points, tier, progress. A balance, not a history
CREATE TABLE IF NOT EXISTS marketing.loyalty_position (
    subject_id                        uuid NOT NULL,
    programme_id                      uuid NOT NULL,
    points_balance                    integer NOT NULL,
    lifetime_points                   integer,
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

-- One level, with its threshold and benefits
CREATE TABLE IF NOT EXISTS marketing.loyalty_tier (
    loyalty_programme_id              uuid NOT NULL,
    trigger                           text NOT NULL,
    points                            numeric(18,4) NOT NULL,
    product_kinds                     text[],
    multiplier                        numeric(18,4),
    id                                uuid PRIMARY KEY NOT NULL
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
    channel                           text NOT NULL,
    template_id                       uuid,
    status                            text NOT NULL,
    failure_reason                    text,
    provider_reference                text,
    queued_at                         timestamptz NOT NULL,
    delivered_at                      timestamptz
);

-- Reusable content for a channel, with the variables a dispatch fills
CREATE TABLE IF NOT EXISTS marketing.message_template (
    id                                uuid PRIMARY KEY NOT NULL,
    code                              text NOT NULL,
    name                              text NOT NULL,
    channel                           text NOT NULL,
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
    offset_minutes                    integer,
    anchor                            text,
    priority                          text,
    is_active                         boolean NOT NULL,
    scope_path                        text
);

-- A personal-data breach (BL-176). UAE PDPL gives 72 hours from discovery — discoveredAt starts
-- the clock, and a discovery nobody recorded is a deadline nobody is counting
CREATE TABLE IF NOT EXISTS marketing.privacy_incident (
    id                                uuid PRIMARY KEY NOT NULL,
    discovered_at                     timestamptz NOT NULL,
    occurred_at                       timestamptz,
    severity                          text NOT NULL,
    affected_subject_count            integer,
    data_categories                   text[],
    contained_at                      timestamptz,
    regulator_notified_at             timestamptz,
    subjects_notified_at              timestamptz,
    not_notified_rationale            text,
    status                            text NOT NULL,
    scope_path                        text
);

-- A referral code and its reward (BL-034). The reward is conditional on the referred guest doing
-- something, not on the referral being sent
CREATE TABLE IF NOT EXISTS marketing.referral (
    id                                uuid PRIMARY KEY NOT NULL,
    referrer_subject_id               uuid NOT NULL,
    referee_subject_id                uuid,
    code                              text NOT NULL,
    status                            text NOT NULL,
    qualifying_action                 text,
    referrer_reward_id                uuid,
    referee_reward_id                 uuid,
    expires_at                        timestamptz,
    scope_path                        text
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
    action                            text,
    legal_holds_respected             boolean,
    fraud_exception_months            integer,
    approval_required                 boolean,
    schedule                          text,
    scope_path                        text
);

-- What a guest said afterwards, with the venue’s response and whether it is public
CREATE TABLE IF NOT EXISTS marketing.review (
    id                                text PRIMARY KEY,
    subject_id                        uuid,
    venue_id                          uuid,
    related_order_id                  text,
    rating                            integer,
    body                              text,
    aspects                           text[],
    recorded_at                       timestamptz,
    status                            text,
    response                          text,
    response_is_public                boolean,
    responded_by_principal_id         uuid,
    opened_case_id                    text
);

-- A rule that selects an audience, evaluated rather than stored as a list
CREATE TABLE IF NOT EXISTS marketing.segment (
    name                              text,
    description                       text,
    venue_id                          uuid,
    match                             text,
    exclude_segment_ids               text[],
    id                                uuid PRIMARY KEY,
    last_evaluated_size               integer,
    last_evaluated_at                 timestamptz,
    created_at                        timestamptz
);

-- One condition in a segment rule. Hangs off: a child of marketing.segment; reaches
-- marketing.guest_profile through its keys; references marketing.segment. Reached by: 4 operations
-- read it and 4 write it.
CREATE TABLE IF NOT EXISTS marketing.segment_criterion (
    segment_id                        uuid NOT NULL,
    attribute                         text NOT NULL,
    operator                          text NOT NULL,
    value                             text,
    values                            text[],
    id                                uuid PRIMARY KEY NOT NULL
);

-- Holds 8 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS marketing.subscription (
    id                                uuid PRIMARY KEY NOT NULL,
    guest_id                          uuid,
    channel                           text,
    list_name                         text,
    subscribed                        boolean,
    source                            text,
    unsubscribe_token                 text,
    updated_at                        timestamptz
);

-- Who must not be contacted, whatever a campaign says
CREATE TABLE IF NOT EXISTS marketing.suppression (
    id                                uuid PRIMARY KEY,
    channel                           text NOT NULL,
    address                           text NOT NULL,
    reason                            text NOT NULL,
    suppressed_at                     timestamptz NOT NULL,
    suppressed_by_principal_id        uuid,
    scope_path                        text
);

-- One marketing touch (BL-177). The platform records touches and does not pick an attribution
-- model — hard-coding one would make every other unanswerable
CREATE TABLE IF NOT EXISTS marketing.touch_point (
    id                                uuid PRIMARY KEY NOT NULL,
    subject_id                        uuid NOT NULL,
    campaign_id                       uuid,
    journey_id                        uuid,
    channel                           text NOT NULL,
    kind                              text,
    occurred_at                       timestamptz NOT NULL,
    order_id                          uuid
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

